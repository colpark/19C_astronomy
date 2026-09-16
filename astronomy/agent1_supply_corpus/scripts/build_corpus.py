#!/usr/bin/env python3
"""Agent 1: apply the frozen corpus rules, cluster, sweep the cut, count supply.

Every number in REPORT.md, corpus_ledger.json, cut_curve.json and
axis_ledger_partial.json is produced here. Run with the panel venv:

    python scripts/build_corpus.py
"""
import hashlib, json, math, re, subprocess, sys
from pathlib import Path
import numpy as np, pandas as pd
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

HERE = Path(__file__).resolve().parent.parent
RAW = HERE.parent / "data/raw/ztf_bts_all_2026-09-16.csv"
RULES = HERE / "corpus_rules_FROZEN.md"
RAW_SHA = "61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
RULES_SHA = (HERE / "corpus_rules_FROZEN.sha256").read_text().split()[0]
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
CUTS = [0.5, 1, 1.5, 2, 3, 5, 10, 20, 30, 60]
S1, S2 = 3095.5, 3221.5
POSA = ("SN ", "SLSN", "TDE", "nova", "LRN", "LBV", "ILRT", "Ca-rich", "Other", "other")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def label(t):
    if t == "-": return "unlabeled"
    if t.startswith(("CV", "AGN")): return "neg"
    if t.startswith(POSA): return "posA_Ia" if t.startswith("SN Ia") else "posB"
    return "unmapped"


def fof(xyz, radius_arcsec):
    chord = 2 * math.sin(math.radians(radius_arcsec / 3600) / 2)
    pairs = cKDTree(xyz).query_pairs(chord, output_type="ndarray")
    n = len(xyz)
    if len(pairs) == 0:
        return np.arange(n), pairs
    g = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n))
    return connected_components(g, directed=False)[1], pairs


def main():
    # I0 and rule freeze checks
    assert sha(RULES) == RULES_SHA, "rules file changed after freeze; abort"
    assert sha(RAW) == RAW_SHA, "raw file sha mismatch; abort"
    raw = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    n_raw = len(raw)

    excl, keep = [], []
    for i, r in raw.iterrows():
        rule = None
        if not re.fullmatch(r"ZTF\d{2}[a-z]{7}", r.ZTFID): rule = "E1"
        else:
            try:
                c = SkyCoord(r.RA, r.Dec, unit=(u.hourangle, u.deg))
                ra, dec = c.ra.deg, c.dec.deg
            except Exception:
                rule = "E2"
        if rule is None:
            try:
                pk = float(r.peakt); assert math.isfinite(pk)
            except Exception:
                rule = "E3"
        if rule is None:
            try:
                pm = float(r.peakmag); assert math.isfinite(pm)
            except Exception:
                rule = "E4"
        if rule is None and not (270.5 <= pk <= 3299.5): rule = "E5"
        if rule:
            excl.append({"unit": r.ZTFID, "rule": rule, "peakt": r.peakt, "type": r.type})
        else:
            keep.append({**r.to_dict(), "ra": ra, "dec": dec, "pk": pk, "pm": pm})
    d = pd.DataFrame(keep)
    d["label"] = d.type.map(label)
    d["posA"] = d.label.isin(["posA_Ia", "posB"])
    d["F2_bright_18p5"] = d.pm <= 18.5
    d["F3_low_b"] = d.b.astype(float).abs() <= 7
    d["F4_label_immature"] = d.pk > 3269.5
    d["F5_censored_timescale"] = d[["duration", "rise", "fade"]].apply(lambda s: s.str.startswith(">")).any(axis=1)
    d["F6_no_redshift"] = d.redshift == "-"
    d["F7_no_peakabs"] = d.peakabs == "-"
    rad = np.radians
    xyz = np.c_[np.cos(rad(d.dec)) * np.cos(rad(d.ra)), np.cos(rad(d.dec)) * np.sin(rad(d.ra)), np.sin(rad(d.dec))]
    coords = SkyCoord(d.ra.values * u.deg, d.dec.values * u.deg)

    # controls: must-join (same IAUID, different ZTFID); must-not-join (different IAUID, both SN)
    iau = d[d.IAUID != "-"]
    dup_groups = iau.groupby("IAUID").filter(lambda g: len(g) > 1)
    mj_pairs = []
    for name, g in dup_groups.groupby("IAUID"):
        idx = list(g.index)
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                mj_pairs.append((idx[a], idx[b], coords[idx[a]].separation(coords[idx[b]]).arcsec, name))
    mj_detail = [{"IAUID": n, "ztf_a": d.ZTFID[a], "ztf_b": d.ZTFID[b], "sep_arcsec": round(s, 3),
                  "type_a": d.type[a], "type_b": d.type[b], "dpeak_days": round(abs(d.pk[a] - d.pk[b]), 2)}
                 for a, b, s, n in mj_pairs]

    curve, per_cut = [], {}
    for cut in CUTS:
        lab, pairs = fof(xyz, cut)
        nc = len(set(lab))
        # must-not-join violations at this cut
        mnj = 0
        mnj_ex = []
        for a, b in pairs:
            ia, ib = d.IAUID[a], d.IAUID[b]
            if ia != "-" and ib != "-" and ia != ib and d.type[a].startswith("SN ") and d.type[b].startswith("SN "):
                mnj += 1
                if len(mnj_ex) < 5:
                    mnj_ex.append([d.ZTFID[a], d.ZTFID[b], ia, ib, round(coords[a].separation(coords[b]).arcsec, 2)])
        mj_joined = sum(lab[a] == lab[b] for a, b, _, _ in mj_pairs)
        g = pd.DataFrame({"c": lab, "pk": d.pk, "label": d.label})
        span = g.groupby("c").pk.agg(["min", "max"])
        st1 = int(((span["min"] < S1) & (span["max"] >= S1)).sum())
        st2 = int(((span["min"] < S2) & (span["max"] >= S2)).sum())
        sizes = g.groupby("c").size()
        per_cut[cut] = dict(n_clusters=nc, multi_member_clusters=int((sizes > 1).sum()),
                            rows_in_multi=int(sizes[sizes > 1].sum()), linked_pairs=int(len(pairs)),
                            must_join_pairs=len(mj_pairs), must_join_joined=int(mj_joined),
                            must_not_join_violations=mnj, must_not_join_examples=mnj_ex,
                            straddle_S1=st1, straddle_S2=st2)
        curve.append({"radius_arcsec": cut, "cut": 1 / cut, "n_clusters": nc})
        d[f"cl_{cut}"] = lab

    pd.DataFrame([{"cut": c["cut"], "n_clusters": c["n_clusters"]} for c in curve]).to_csv(OUT / "curve_for_tau.csv", index=False)
    tau = subprocess.run([sys.executable, str(HERE.parent.parent / "fm-advantage-benchmark/scripts/tau.py"),
                          "--curve", str(OUT / "curve_for_tau.csv"), "--out", str(OUT / "tau_raw.json")],
                         capture_output=True, text=True)
    (OUT / "tau_stdout.txt").write_text(tau.stdout + tau.stderr + f"\nexit {tau.returncode}\n")

    json.dump({"n_raw_rows": n_raw, "n_excluded": len(excl), "n_included_rows": len(d),
               "exclusions": excl, "exclusion_rule_counts": pd.Series([e["rule"] for e in excl]).value_counts().to_dict() if excl else {},
               "must_join_detail": mj_detail, "per_cut": per_cut, "curve": curve,
               "tau_returncode": tau.returncode}, open(OUT / "sweep.json", "w"), indent=1, default=int)
    d.to_csv(OUT / "corpus_rows.csv", index=False)
    print(tau.stdout)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "must_not_join_examples"} for k, v in per_cut.items()}, indent=0))
    print("raw", n_raw, "excluded", len(excl), "kept", len(d))
    print("unmapped types", d[d.label == "unmapped"].type.value_counts().to_dict())


if __name__ == "__main__":
    main()
