#!/usr/bin/env python3
"""Agent 5, D4 slot k support: BTS explorer CSV -> peakt zero point, row/object counts,
peak-night rates (a proxy for objects entering follow-up per round), and post-cutoff counts
for the subject-set falsifier.

    python bts_rounds.py  (writes ../out/bts_rounds.json)

Every number here is computed over the local file identified by sha256; nothing is typed in.
The peak night is NOT the trigger night. Rates here are a proxy and are labelled as such.
"""
import hashlib, json, os, re
import numpy as np
import pandas as pd
from astropy.time import Time

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.abspath(os.path.join(HERE, "..", "..", "data", "raw", "ztf_bts_all_2026-09-16.csv"))
OUT = os.path.abspath(os.path.join(HERE, "..", "out", "bts_rounds.json"))
FETCH_JD = Time("2026-09-16T00:00:00", scale="utc").jd  # fetch date from data/raw/FETCH.md

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def main():
    rec = {"file": CSV, "sha256": sha256(CSV)}
    d = pd.read_csv(CSV, dtype=str)
    rec["rows"] = int(len(d))
    rec["unique_ZTFID"] = int(d.ZTFID.nunique())
    iau = d.IAUID[d.IAUID.notna() & (d.IAUID != "-")]
    rec["rows_with_IAUID"] = int(len(iau))
    rec["unique_IAUID"] = int(iau.nunique())
    dup = iau[iau.duplicated(keep=False)]
    rec["IAUID_shared_by_multiple_ZTFID_rows"] = int(len(dup))
    rec["IAUID_values_shared"] = int(dup.nunique())
    # distinct astrophysical objects: collapse rows sharing an IAU name; rows without IAU name kept singly
    n_obj = int(iau.nunique() + (len(d) - len(iau)))
    rec["distinct_objects_by_IAUID_collapse"] = n_obj
    rec["raw_over_distinct_overstatement_pct"] = round(100.0 * (len(d) - n_obj) / n_obj, 3)

    t = d.peakt.astype(float)
    rec["peakt_min"], rec["peakt_max"] = float(t.min()), float(t.max())

    # ---- zero point test: which offset makes calendar year of peak agree with the IAU designation year?
    yr_iau = iau.str.extract(r"^(?:SN|AT|TDE|ST)\s?(\d{4})")[0].astype(float)
    sel = yr_iau.notna()
    zp_tests = {}
    for label, zp in [("JD-2400000.5 (MJD)", 2400000.5), ("JD-2450000", 2450000.0),
                      ("JD-2458000", 2458000.0), ("JD-2458000.5", 2458000.5), ("JD-2459000", 2459000.0)]:
        jd = t[yr_iau.index[sel]] + zp
        yrs = Time(jd.values, format="jd").datetime64.astype("datetime64[Y]").astype(int) + 1970
        y = yr_iau[sel].values
        same_or_next = np.mean((yrs == y) | (yrs == y + 1))
        within_span = np.mean((jd.values >= Time("2018-03-01").jd) & (jd.values <= FETCH_JD))
        zp_tests[label] = {"frac_peak_year_in_{IAU_year, IAU_year+1}": round(float(same_or_next), 4),
                           "frac_peak_between_2018-03-01_and_fetch_date": round(float(within_span), 4),
                           "n": int(sel.sum())}
    rec["peakt_zero_point_tests"] = zp_tests
    zp = 2458000.0
    rec["peakt_zero_point_adopted"] = "JD - 2458000"
    rec["peakt_min_utc"] = Time(t.min() + zp, format="jd").iso
    rec["peakt_max_utc"] = Time(t.max() + zp, format="jd").iso
    rec["zero_point_note"] = ("A half-day shift (JD vs MJD-style 2458000.5) cannot be separated by the year test; "
                              "only the documented definition separates them.")

    # ---- peak-night rates (proxy for objects entering the follow-up stream per round)
    jd = t + zp
    night = np.floor(jd - (116.86 / 360.0))  # night index: JD days start at UTC noon; Palomar local mean noon is 116.86/360 d later
    d["night"] = night.astype(int)
    d["year"] = Time(jd.values, format="jd").datetime64.astype("datetime64[Y]").astype(int) + 1970
    d["peakmag_f"] = pd.to_numeric(d.peakmag, errors="coerce")
    nonvar = ~d.type.isin(["CV", "CV?", "AGN", "AGN?", "nova"])
    classified_transient = nonvar & (d.type != "-")
    per_year = {}
    for y in sorted(d.year.unique()):
        s = d[d.year == y]
        days = 366 if (y % 4 == 0) else 365
        per_year[int(y)] = {
            "rows": int(len(s)),
            "rows_per_calendar_night": round(len(s) / days, 3),
            "classified_transients": int(classified_transient[s.index].sum()),
            "classified_transients_per_calendar_night": round(classified_transient[s.index].sum() / days, 3),
            "rows_peakmag_le_18.5": int((s.peakmag_f <= 18.5).sum()),
            "rows_peakmag_le_18.5_per_calendar_night": round((s.peakmag_f <= 18.5).sum() / days, 3),
        }
    rec["per_calendar_year_peak_rates"] = per_year
    full = d[(d.year >= 2019) & (d.year <= 2025)]
    nights_all = pd.Series(0, index=np.arange(int(full.night.min()), int(full.night.max()) + 1))
    cnt = full.groupby("night").size()
    nights_all.loc[cnt.index] = cnt.values
    rec["full_years_2019_2025"] = {
        "rows": int(len(full)),
        "calendar_nights": int(len(nights_all)),
        "mean_peaks_per_calendar_night": round(float(nights_all.mean()), 3),
        "median_peaks_per_calendar_night": float(nights_all.median()),
        "p10_p90_peaks_per_calendar_night": [float(nights_all.quantile(0.1)), float(nights_all.quantile(0.9))],
        "fraction_nights_zero_peaks": round(float((nights_all == 0).mean()), 4),
    }

    # ---- subject-set falsifier support: objects peaking after each primary-doc cutoff
    cut = {"2025-01-31 (Gemini 3 family domain-limited, card text)": "2025-02-01",
           "2026-01-31 (Claude Sonnet 5)": "2026-02-01",
           "2026-02-16 (GPT-5.6 Sol/Terra/Luna)": "2026-02-17",
           "2026-03-31 (Gemini 3.8 Flash)": "2026-04-01",
           "2026-04-30 (GPT-6 Astra)": "2026-05-01",
           "2026-05-31 (Claude Opus 5)": "2026-06-01",
           "2026-06-30 (Claude Fable 5.1, reliable-knowledge cutoff)": "2026-07-01"}
    rec["rows_peaking_on_or_after_cutoff_plus_one_day"] = {
        k: {"rows": int((jd >= Time(v).jd).sum()),
            "classified_transients": int(((jd >= Time(v).jd) & classified_transient).sum())}
        for k, v in cut.items()}
    rec["completeness"] = ("rows, unique ZTFID/IAUID, IAU-collapse object count, five candidate zero points, "
                           "per-year and 2019-2025 per-night peak rates, post-cutoff counts; NOT covered: trigger "
                           "nights, candidates passing the alert filter (not in this file), save dates")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(rec, open(OUT, "w"), indent=2)
    print(json.dumps(rec, indent=2))

if __name__ == "__main__":
    main()


def object_identity_controls():
    """Controls for the raw-vs-distinct count (N09-style): must-join = rows sharing an IAU name should be
    positionally coincident; must-separate = rows with different IAU names should not be coincident."""
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    d = pd.read_csv(CSV, dtype=str)
    c = SkyCoord(d.RA.values, d.Dec.values, unit=(u.hourangle, u.deg))
    out = {}
    iau = d.IAUID.where(d.IAUID != "-")
    shared = iau[iau.duplicated(keep=False) & iau.notna()]
    seps = []
    for name, idx in shared.groupby(shared).groups.items():
        idx = list(idx)
        seps.append(float(c[idx[0]].separation(c[idx[1]]).arcsec))
    out["shared_IAU_pairs"] = len(seps)
    out["shared_IAU_pair_separation_arcsec_max"] = round(max(seps), 3) if seps else None
    out["shared_IAU_pairs_within_2arcsec"] = int(sum(s <= 2.0 for s in seps))
    i1, i2, s2d, _ = c.search_around_sky(c, 2.0 * u.arcsec)
    m = i1 < i2
    pairs = list(zip(i1[m], i2[m], s2d[m].arcsec))
    out["row_pairs_within_2arcsec"] = len(pairs)
    diff_name = [(a, b, s) for a, b, s in pairs if not (pd.notna(iau[a]) and iau[a] == iau[b])]
    out["row_pairs_within_2arcsec_with_different_or_missing_IAU"] = len(diff_name)
    out["examples_different_IAU_within_2arcsec"] = [
        {"ZTFID": [d.ZTFID[a], d.ZTFID[b]], "IAUID": [d.IAUID[a], d.IAUID[b]], "type": [d.type[a], d.type[b]],
         "peakt": [d.peakt[a], d.peakt[b]], "sep_arcsec": round(float(s), 3)} for a, b, s in diff_name[:15]]
    # union-find over rows within 2 arcsec OR sharing an IAU name
    parent = list(range(len(d)))
    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b, _ in pairs:
        parent[f(a)] = f(b)
    for name, idx in shared.groupby(shared).groups.items():
        idx = list(idx); parent[f(idx[0])] = f(idx[1])
    n_pos = len({f(i) for i in range(len(d))})
    out["distinct_positions_2arcsec_union_IAU"] = n_pos
    out["raw_over_positional_overstatement_pct"] = round(100.0 * (len(d) - n_pos) / n_pos, 3)
    out["note"] = ("A 2 arcsec coincidence joins repeat outbursts of the same CV/AGN (one astrophysical object, "
                   "several saved episodes); whether those count as one unit or several is a D3/P3 unit decision, "
                   "not settled here.")
    p = os.path.join(os.path.dirname(OUT), "bts_object_identity_controls.json")
    json.dump(out, open(p, "w"), indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__" and os.environ.get("IDENTITY_CONTROLS"):
    object_identity_controls()
