#!/usr/bin/env python3
"""C1: Fink/LSST per-night statistics aggregate (non-label columns only)."""
import json, hashlib, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
f = D / "out/raw/fink_stats_2026.json"
rows = sorted(json.load(open(f)), key=lambda r: int(r["f:night"]))
g = lambda r, k: int(r[k])
def agg(lo):
    sel = [r for r in rows if int(r["f:night"]) >= lo]
    A = sum(g(r, "f:alerts") for r in sel); F = sum(g(r, "f:is_first") for r in sel); S = sum(g(r, "f:is_sso") for r in sel)
    return dict(nights=[int(r["f:night"]) for r in sel], n_nights=len(sel), alerts=A, is_first=F, is_sso=S,
                objects_night_summed=sum(g(r, "f:objects") for r in sel), visits=sum(g(r, "f:visits") for r in sel),
                O_hi=F, O_lo=F - S, overstatement_pct_vs_O_hi=round((A - F) / F * 100, 1), overstatement_pct_vs_O_lo=round((A - (F - S)) / (F - S) * 100, 1))
out = dict(source="POST https://api.lsst.fink-portal.org/api/v1/statistics date=2026, columns f:night,f:alerts,f:objects,f:is_first,f:is_sso,f:visits,f:lsst_schema_version",
           file=str(f.relative_to(D)), sha256=hashlib.sha256(f.read_bytes()).hexdigest(),
           lower_bracket_nights_ge_20260701=agg(20260701), upper_bracket_nights_ge_20260630=agg(20260630),
           survey_nights_ge_20260629=agg(20260629), all_2026=agg(20260101),
           last_night_with_alerts=max(int(r["f:night"]) for r in rows if g(r, "f:alerts") > 0),
           nights_with_alerts_after_20260714=[int(r["f:night"]) for r in rows if int(r["f:night"]) > 20260714 and g(r, "f:alerts") > 0])
json.dump(out, open(D / "out/c1_fink.json", "w"), indent=1)
for k in ("lower_bracket_nights_ge_20260701", "upper_bracket_nights_ge_20260630", "survey_nights_ge_20260629", "all_2026"):
    print(k, {x: y for x, y in out[k].items() if x != "nights"})
print(out["survey_nights_ge_20260629"]["nights"], out["last_night_with_alerts"], out["nights_with_alerts_after_20260714"])
