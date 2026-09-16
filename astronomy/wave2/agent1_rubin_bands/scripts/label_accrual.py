#!/usr/bin/env python3
"""Step 5 (calibration only; BTS failed contamination; addition B). Label accrual curve, report-lag between
Internet Archive captures, and the LAG vs POLICY rule declared in bands_FROZEN.md section 9 (declared before this ran).
Unit: BTS row keyed by ZTFID (wave-1: rows->1'' objects overstate by 0.089%)."""
import hashlib, html, json, re, pathlib
import numpy as np, pandas as pd
from astropy.time import Time
D = pathlib.Path(__file__).resolve().parent.parent
AST = D.parent.parent
RAW = AST / "data/raw/ztf_bts_all_2026-09-16.csv"; RAW_SHA = "61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
CAP = {"2024-12-08T23:13:31": AST / "agent3_labels_exposure/sources/wayback_bts_explorer_20241208231331.html",
       "2025-08-10T06:50:56": AST / "agent3_labels_exposure/sources/wayback_bts_explorer_20250810065056.html",
       "2026-07-25T03:35:57": AST / "agent3_labels_exposure/sources/wayback_bts_explorer_20260725033557.html"}
FETCH = "2026-09-16T00:00:00"
BINS = [0, 30, 60, 120, 240, 365, np.inf]; LABELS = ["[0,30)", "[30,60)", "[60,120)", "[120,240)", "[240,365)", "[365,inf)"]
ALPHA = 0.05  # fm-advantage-benchmark/scripts/power.py default, the alpha that produced planning_mde_bracket.csv
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
jd = lambda iso: Time(iso, format="isot", scale="utc").jd

def parse_capture(path):  # agent3 labels_exposure.py::parse_capture, unchanged, plus the peak cell (index 4)
    t = pathlib.Path(path).read_text(encoding="utf-8", errors="replace"); out = {}
    for row in re.findall(r"<tr>\s*(<td>.*?)</tr>", t, flags=re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ").strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)]
        if len(cells) >= 15 and re.fullmatch(r"ZTF\d\d[a-z]{7}", cells[0]):
            try: pk = float(cells[4])
            except ValueError: pk = np.nan
            out[cells[0]] = (cells[11], pk)
    return out

def snapshot(name, when_iso, types, peaks):
    df = pd.DataFrame({"ZTFID": list(types.keys()), "type": list(types.values()), "peakt": [peaks[k] for k in types]})
    df = df[np.isfinite(df.peakt)].copy()
    df["age"] = jd(when_iso) - (df.peakt + 2458000.0)
    df = df[df.age >= 0].copy()
    df["labelled"] = df.type != "-"
    df["bin"] = pd.cut(df.age, BINS, right=False, labels=LABELS)
    df["peak_year"] = Time(df.peakt.values + 2458000.0, format="jd").to_datetime()
    df["peak_year"] = [d.year for d in df.peak_year]
    df["snapshot"] = name
    return df

def curve(df):
    g = df.groupby("bin", observed=False).labelled
    return {b: {"n": int(n), "labelled": int(k), "frac": (round(k / n, 4) if n else None)} for b, n, k in zip(LABELS, g.size().values, g.sum().values)}

def poibin_cdf(ps, x):
    pmf = np.array([1.0])
    for p in ps: pmf = np.convolve(pmf, [1 - p, p])
    return float(pmf[: x + 1].sum()), float(np.dot(np.arange(len(pmf)), pmf))

def lag_test(obs, ref_curve):
    f = {b: v["frac"] for b, v in ref_curve.items()}
    inc = obs[obs.bin.map(lambda b: f.get(b) is not None)]
    exc = len(obs) - len(inc)
    ps = inc.bin.map(f).astype(float).values
    X = int(inc.labelled.sum())
    if len(inc) == 0: return dict(n_included=0, excluded_no_reference=exc, P=None)
    P, E = poibin_cdf(ps, X)
    return dict(n_included=int(len(inc)), excluded_no_reference=int(exc), observed_labelled=X, expected_labelled_under_LAG=round(E, 1),
                observed_frac=round(X / len(inc), 4), expected_frac=round(E / len(inc), 4), P_lower_tail=P,
                per_bin={b: dict(n=int((inc.bin == b).sum()), obs=int(inc[inc.bin == b].labelled.sum()), ref_frac=f[b]) for b in LABELS if (inc.bin == b).any()})

def main():
    assert sha(RAW) == RAW_SHA
    raw = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    fpk = pd.to_numeric(raw.peakt, errors="coerce")
    file_types = dict(zip(raw.ZTFID, raw.type)); file_peaks = dict(zip(raw.ZTFID, fpk))
    res = {"inputs": {"raw": {"path": str(RAW.relative_to(AST.parent)), "sha256": RAW_SHA},
                      "captures": {k: {"path": str(v.relative_to(AST.parent)), "sha256": sha(v)} for k, v in CAP.items()}},
           "rule": "bands_FROZEN.md section 9 (sha256 8825ef8048b733b66e12f31ce16e67270de171f52f20f40ca8f21e5780e500d2)",
           "calibration_banner": "calibration only, contamination FAIL on this cohort (BTS); no Rubin claim rests on this"}
    snaps = {}
    for k, p in CAP.items():
        c = parse_capture(p)
        snaps[k] = snapshot(k, k, {z: v[0] for z, v in c.items()}, {z: v[1] for z, v in c.items()})
    snaps["file_2026-09-16"] = snapshot("file_2026-09-16", FETCH, file_types, file_peaks)
    res["snapshot_sizes"] = {k: int(len(v)) for k, v in snaps.items()}
    # accrual curves: all objects peaking before the snapshot, and restricted to pre-2026 peaks
    res["accrual_curve_all"] = {k: curve(v) for k, v in snaps.items()}
    res["accrual_curve_pre2026_peaks"] = {k: curve(v[v.peak_year < 2026]) for k, v in snaps.items()}
    res["accrual_curve_2026_peaks"] = {k: curve(v[v.peak_year == 2026]) for k, v in snaps.items() if (v.peak_year == 2026).any()}
    fy = snaps["file_2026-09-16"]
    res["file_unlabelled_frac_by_peak_year"] = {int(y): dict(n=int(len(g)), unlabelled=int((~g.labelled).sum()), frac=round(float((~g.labelled).mean()), 4)) for y, g in fy.groupby("peak_year")}
    # report lag between snapshots, objects peaking before 2026 and unlabelled at C1
    order = ["2024-12-08T23:13:31", "2025-08-10T06:50:56", "2026-07-25T03:35:57", "file_2026-09-16"]
    when = {"2024-12-08T23:13:31": "2024-12-08T23:13:31", "2025-08-10T06:50:56": "2025-08-10T06:50:56", "2026-07-25T03:35:57": "2026-07-25T03:35:57", "file_2026-09-16": FETCH}
    lag = {}
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            a, b = snaps[order[i]], snaps[order[j]]
            m = a[(~a.labelled) & (a.peak_year < 2026)].merge(b[["ZTFID", "labelled", "type"]], on="ZTFID", suffixes=("", "_2"))
            dt = jd(when[order[j]]) - jd(when[order[i]])
            became = m[m.labelled_2]
            lag[f"{order[i]} -> {order[j]}"] = dict(
                gap_days=round(dt, 1), unlabelled_at_C1_present_at_C2=int(len(m)), labelled_by_C2=int(len(became)),
                frac_labelled_by_C2=(round(len(became) / len(m), 4) if len(m) else None),
                by_age_at_C1={b: dict(n=int((m.bin == b).sum()), labelled_by_C2=int(became[became.bin == b].shape[0])) for b in LABELS},
                lag_bracket_days_quantiles_lower=[round(float(q), 1) for q in np.quantile(became.age, [0.1, 0.25, 0.5, 0.75, 0.9])] if len(became) else None,
                lag_bracket_days_quantiles_upper=[round(float(q + dt), 1) for q in np.quantile(became.age, [0.1, 0.25, 0.5, 0.75, 0.9])] if len(became) else None)
            # labels present at C1 that changed or vanished by C2
            l1 = a[a.labelled].merge(b[["ZTFID", "type"]], on="ZTFID", suffixes=("", "_2"))
            lag[f"{order[i]} -> {order[j]}"]["labelled_at_C1_changed_by_C2"] = int((l1.type != l1.type_2).sum())
            lag[f"{order[i]} -> {order[j]}"]["labelled_at_C1_unlabelled_at_C2"] = int((l1.type_2 == "-").sum())
    res["report_lag_between_snapshots_pre2026_peaks"] = lag
    # descriptive only (not part of the declared rule): labelled fraction by peak month, file and each capture
    def bymonth(df):
        m = Time(df.peakt.values + 2458000.0, format="jd").to_datetime()
        df = df.assign(pm=[f"{d.year}-{d.month:02d}" for d in m])
        return {k: dict(n=int(len(g)), labelled=int(g.labelled.sum()), frac=round(float(g.labelled.mean()), 4)) for k, g in df.groupby("pm") if k >= "2024-06"}
    res["descriptive_labelled_frac_by_peak_month"] = {k: bymonth(v) for k, v in snaps.items()}
    # decision
    refs = ["2024-12-08T23:13:31", "2025-08-10T06:50:56"]
    obs_i = snaps["2026-07-25T03:35:57"]; obs_i = obs_i[obs_i.peak_year == 2026]
    obs_ii = snaps["file_2026-09-16"]; obs_ii = obs_ii[obs_ii.peak_year == 2026]
    tests = {}
    for r in refs:
        rc = res["accrual_curve_all"][r]
        tests[f"(i) capture_2026-07-25 vs ref {r}"] = lag_test(obs_i, rc)
        tests[f"(ii) file_2026-09-16 vs ref {r}"] = lag_test(obs_ii, rc)
    res["lag_tests"] = tests
    Pi = [tests[f"(i) capture_2026-07-25 vs ref {r}"]["P"] if "P" in tests[f"(i) capture_2026-07-25 vs ref {r}"] else tests[f"(i) capture_2026-07-25 vs ref {r}"].get("P_lower_tail") for r in refs]
    Pii = [tests[f"(ii) file_2026-09-16 vs ref {r}"].get("P_lower_tail") for r in refs]
    ni = [tests[f"(i) capture_2026-07-25 vs ref {r}"]["n_included"] for r in refs]
    if min(ni) == 0 or any(p is None for p in Pi + Pii): ruling = "UNDEMONSTRATED"
    elif all(p < ALPHA for p in Pi) and all(p < ALPHA for p in Pii): ruling = "POLICY"
    elif all(p >= ALPHA for p in Pi): ruling = "LAG"
    else: ruling = "UNDEMONSTRATED"
    res["decision"] = dict(alpha=ALPHA, P_i=Pi, P_ii=Pii, ruling=ruling,
                           note="POLICY means normal accrual lag measured on pre-2026 captures cannot explain the 2026 deficit; it does not name the policy")
    json.dump(res, open(D / "label_accrual.json", "w"), indent=1, default=str)
    print(json.dumps({k: res[k] for k in ("snapshot_sizes", "file_unlabelled_frac_by_peak_year", "decision")}, indent=1, default=str))
    for k, v in tests.items(): print(k, {x: y for x, y in v.items() if x != "per_bin"}); print("   ", v.get("per_bin"))
    print(json.dumps(res["descriptive_labelled_frac_by_peak_month"]["file_2026-09-16"]))
    print(json.dumps(res["descriptive_labelled_frac_by_peak_month"]["2025-08-10T06:50:56"]))
    for k, v in lag.items(): print(k, {x: y for x, y in v.items() if x != "by_age_at_C1"})
main()
