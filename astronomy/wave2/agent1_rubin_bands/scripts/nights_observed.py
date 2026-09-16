#!/usr/bin/env python3
"""Step 4: nights observed with LSSTCam after survey start, from the Rubin scheduler reports table of contents
(sources/rubin_status/schedview_reports_toc.html, fetched 2026-09-16) beside Fink per-night statistics."""
import json, hashlib, pathlib, io, re
import pandas as pd
D = pathlib.Path(__file__).resolve().parent.parent
f = D / "sources/rubin_status/schedview_reports_toc.html"
tabs = pd.read_html(io.StringIO(f.read_text(errors="replace")))
out = {"toc_file": str(f.relative_to(D)), "toc_sha256": hashlib.sha256(f.read_bytes()).hexdigest(), "tables": []}
lsst = None
for i, t in enumerate(tabs):
    cols = [" ".join(map(str, c)) if isinstance(c, tuple) else str(c) for c in t.columns]
    t.columns = cols
    out["tables"].append({"i": i, "columns": cols, "rows": len(t)})
    if lsst is None and any("instrument" in c for c in cols) and t.astype(str).apply(lambda r: r.str.contains("lsstcam")).any().any():
        lsst = t
print(json.dumps(out["tables"], indent=0))
ncol = lsst.columns[0]
tot = [c for c in lsst.columns if c.startswith("Total")][0]; sci = [c for c in lsst.columns if c.startswith("science")][0]
lsst = lsst[lsst[ncol].astype(str).str.match(r"20\d\d-\d\d-\d\d")].copy()
lsst["night"] = lsst[ncol].astype(str)
rows = []
for r in lsst.itertuples(index=False):
    d = r._asdict() if hasattr(r, "_asdict") else dict(zip(lsst.columns, r))
rows = lsst[["night", tot, sci]].rename(columns={tot: "total_visits", sci: "science_visits"}).to_dict("records")
rows = [x for x in rows if x["night"] >= "2026-06-29"]
for x in rows:
    for k in ("total_visits", "science_visits"):
        try: x[k] = int(float(x[k]))
        except Exception: x[k] = None
fink = {int(r["f:night"]): r for r in json.load(open(D / "out/raw/fink_stats_2026.json"))}
for x in rows:
    fr = fink.get(int(x["night"].replace("-", "")))
    x["fink_alerts"] = int(fr["f:alerts"]) if fr else 0
    x["fink_visits"] = int(fr["f:visits"]) if fr else 0
rows.sort(key=lambda x: x["night"])
obs_sched = [x["night"] for x in rows if (x["science_visits"] or 0) > 0]
obs_fink = [x["night"] for x in rows if x["fink_alerts"] > 0]
out.update(rows=rows, nights_with_science_visits_scheduler=obs_sched, n_scheduler=len(obs_sched),
           nights_with_alerts_fink=obs_fink, n_fink=len(obs_fink),
           cohort_nights_ge_20260701_scheduler=[n for n in obs_sched if n >= "2026-07-01"],
           cohort_nights_ge_20260701_fink=[n for n in obs_fink if n >= "2026-07-01"],
           disagreement_nights=sorted(set(obs_sched) ^ set(obs_fink)),
           science_visits_total_ge_20260629=sum(x["science_visits"] or 0 for x in rows),
           last_scheduler_night_with_science=max(obs_sched) if obs_sched else None)
json.dump(out, open(D / "out/nights_observed.json", "w"), indent=1)
for x in rows: print(x)
print({k: v for k, v in out.items() if k not in ("rows", "tables")})
