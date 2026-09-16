#!/usr/bin/env python3
"""P2 prior floor estimate on the ZTF BTS catalogue (agent2, pre-P1 sketch).

This is a P2 PRIOR ESTIMATE, not an I1 composition. It uses only the BTS
Sample Explorer summary columns, one classical learner family, and a grouped
split. No foundation model, no agent, no light curves, no images.

Run:
  <venv>/bin/python floor_prior.py  > prior_floor_results.json

Declared before any number was computed (anti-widening; do not edit after the run
without an amendment note in REPORT.md):
  * unit           : one BTS object (ZTFID). Group key = union of (a) identical
                     non-'-' IAUID and (b) sky positions within 3 arcsec.
  * population     : rows whose `type` != '-' (spectroscopically classified).
  * task A         : SN Ia (type startswith 'SN Ia') vs everything else classified.
  * task B (proxy) : 'non-routine' = classified type NOT in ROUTINE below. This is a
                     panel proxy for 'worth a slot'; it is NOT the ratified label
                     (D4/D5 have not run).
  * metrics        : ROC AUC (chance 0.5) and average precision (chance = prevalence),
                     out-of-fold over StratifiedGroupKFold(5).
  * feature tiers  : see TIERS. Censored values ('>x') are parsed to x plus a flag.
  * learners       : HistGradientBoostingClassifier and LogisticRegression; the floor
                     for a tier is the stronger of the two (adjudicator = strongest).
  * controls       : label permutation (must return AUC ~0.5); temporal split
                     (train peakt < 1945.5 i.e. before 2023-01-01, test after).
"""
import hashlib, json, sys
import numpy as np, pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score

CSV = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/data/raw/ztf_bts_all_2026-09-16.csv"
SHA = "61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
SEED = 0
ROUTINE = {"SN Ia", "SN Ia-91T", "SN II", "SN IIP", "CV", "CV?", "AGN", "AGN?",
           "nova", "Other", "other"}
TIERS = {
    # everything the brief lists; peakabs and redshift exist only after spectroscopy
    "T1_full_post_spectroscopy": ["peakmag", "peakabs", "rise", "rise_cens", "fade", "fade_cens",
                                  "duration", "duration_cens", "b", "redshift"],
    # T1 without the two spectroscopy-derived columns; needs the COMPLETE light curve
    "T2_photometric_retrospective": ["peakmag", "rise", "rise_cens", "fade", "fade_cens",
                                     "duration", "duration_cens", "b"],
    # what exists at observed peak: peak mag, half-peak-to-peak rise, position
    "T3_at_peak": ["peakmag", "rise", "rise_cens", "b"],
    # what exists at the first alert among the listed columns
    "T4_at_first_alert": ["b"],
    # leakage decomposition: redshift alone added to T2
    "T2_plus_redshift": ["peakmag", "rise", "rise_cens", "fade", "fade_cens",
                         "duration", "duration_cens", "b", "redshift"],
}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def num(s):
    s = s.astype(str).str.strip()
    cens = s.str.startswith(">") | s.str.startswith("<")
    v = pd.to_numeric(s.str.lstrip("<>").replace("-", np.nan), errors="coerce")
    return v, cens.astype(float)


def load():
    got = sha256(CSV)
    d = pd.read_csv(CSV, dtype=str)
    for c in ["peakmag", "peakabs", "redshift", "b", "A_V", "peakt"]:
        d[c], _ = num(d[c])
    for c in ["rise", "fade", "duration"]:
        d[c], d[c + "_cens"] = num(d[c])
    return d, got


def groups(d):
    n = len(d)
    rows, cols = [], []
    # identical IAU names
    iau = d["IAUID"].where(d["IAUID"] != "-")
    for _, idx in d[iau.notna()].groupby("IAUID").groups.items():
        idx = list(idx)
        for j in idx[1:]:
            rows.append(idx[0]); cols.append(j)
    # sky proximity
    c = SkyCoord(d["RA"].values, d["Dec"].values, unit=(u.hourangle, u.deg))
    i1, i2, _, _ = c.search_around_sky(c, 3 * u.arcsec)
    m = i1 < i2
    rows += list(i1[m]); cols += list(i2[m])
    g = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    k, lab = connected_components(g, directed=False)
    return lab, int(k), int(m.sum())


def learners():
    return {
        "hgb": HistGradientBoostingClassifier(random_state=SEED, max_iter=300, learning_rate=0.05),
        "logreg": make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                                StandardScaler(), LogisticRegression(max_iter=2000)),
    }


def oof(X, y, g, model_name):
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    p = np.zeros(len(y))
    for tr, te in cv.split(X, y, g):
        m = learners()[model_name]
        m.fit(X[tr], y[tr])
        p[te] = m.predict_proba(X[te])[:, 1]
    return p


def boot_ci(y, p, g, fn, B=500):
    rng = np.random.default_rng(SEED)
    ug = np.unique(g)
    idx_by_g = pd.Series(np.arange(len(g))).groupby(g).apply(list).to_dict()
    vals = []
    for _ in range(B):
        take = rng.choice(ug, size=len(ug), replace=True)
        ix = np.concatenate([idx_by_g[t] for t in take])
        if y[ix].min() == y[ix].max():
            continue
        vals.append(fn(y[ix], p[ix]))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def run_task(d, g, yname):
    y = d[yname].values.astype(int)
    out = {"n_objects": int(len(y)), "n_groups": int(len(np.unique(g))),
           "n_positive": int(y.sum()), "prevalence": float(y.mean()),
           "chance_auc": 0.5, "chance_ap": float(y.mean()), "tiers": {}}
    for tier, cols in TIERS.items():
        X = d[cols].values.astype(float)
        res = {}
        for mn in ["hgb", "logreg"]:
            p = oof(X, y, g, mn)
            res[mn] = {"auc": float(roc_auc_score(y, p)), "ap": float(average_precision_score(y, p))}
        best = max(res, key=lambda k: res[k]["auc"])
        p = oof(X, y, g, best)
        res["floor_learner"] = best
        res["floor_auc_ci95_group_bootstrap"] = boot_ci(y, p, g, roc_auc_score)
        res["floor_ap_ci95_group_bootstrap"] = boot_ci(y, p, g, average_precision_score)
        res["auc_above_chance"] = res[best]["auc"] - 0.5
        out["tiers"][tier] = res
    t1 = out["tiers"]["T1_full_post_spectroscopy"]["auc_above_chance"]
    for tier in out["tiers"]:
        out["tiers"][tier]["share_of_T1_signal_above_chance"] = (
            out["tiers"][tier]["auc_above_chance"] / t1 if t1 > 0 else None)
    # permutation control on T1 with the HGB learner
    rng = np.random.default_rng(SEED + 1)
    yp = rng.permutation(y)
    X = d[TIERS["T1_full_post_spectroscopy"]].values.astype(float)
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    pp = np.zeros(len(y))
    for tr, te in cv.split(X, yp, g):
        m = learners()["hgb"]; m.fit(X[tr], yp[tr]); pp[te] = m.predict_proba(X[te])[:, 1]
    out["control_label_permutation_T1_auc"] = float(roc_auc_score(yp, pp))
    # temporal split
    tmp = {}
    tr = d["peakt"].values < 1945.5
    te = ~tr
    for tier, cols in TIERS.items():
        X = d[cols].values.astype(float)
        best = out["tiers"][tier]["floor_learner"]
        m = learners()[best]; m.fit(X[tr], y[tr]); p = m.predict_proba(X[te])[:, 1]
        tmp[tier] = {"auc": float(roc_auc_score(y[te], p)), "ap": float(average_precision_score(y[te], p)),
                     "prevalence_test": float(y[te].mean())}
    out["temporal_split"] = {"n_train": int(tr.sum()), "n_test": int(te.sum()),
                             "rule": "train peakt < 1945.5 (JD-2458000; before 2023-01-01), test otherwise",
                             "tiers": tmp}
    return out


def main():
    d, got = load()
    raw_rows = len(d)
    lab, ngroups_all, npairs = groups(d)
    d["group"] = lab
    cls = d[d["type"] != "-"].copy()
    cls["yA"] = cls["type"].str.startswith("SN Ia")
    cls["yB"] = ~cls["type"].isin(ROUTINE)
    res = {
        "label": "P2 PRIOR FLOOR ESTIMATE (not an I1 composition)",
        "script": "agent2_floor_headroom/floor_prior.py",
        "csv": CSV, "csv_sha256_expected": SHA, "csv_sha256_measured": got, "sha_match": got == SHA,
        "raw_rows_excluding_header": raw_rows,
        "distinct_ztfid": int(d["ZTFID"].nunique()),
        "distinct_groups_all_rows": ngroups_all,
        "sky_pairs_within_3arcsec": npairs,
        "classified_rows": int(len(cls)),
        "unclassified_rows_type_dash": int((d["type"] == "-").sum()),
        "classified_missing_redshift": int(cls["redshift"].isna().sum()),
        "classified_missing_peakabs": int(cls["peakabs"].isna().sum()),
        "routine_set_task_B": sorted(ROUTINE),
        "versions": {"numpy": np.__version__, "pandas": pd.__version__,
                     "sklearn": __import__("sklearn").__version__},
    }
    g = cls["group"].values
    res["task_A_SNIa_vs_nonIa"] = run_task(cls, g, "yA")
    res["task_B_nonroutine_proxy"] = run_task(cls, g, "yB")
    # Task A restricted to SNe only (types starting 'SN'), removes CV/AGN missing-redshift leakage
    sn = cls[cls["type"].str.startswith("SN")].copy()
    res["task_A_within_SNe_only"] = run_task(sn, sn["group"].values, "yA")
    json.dump(res, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
