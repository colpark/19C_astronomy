#!/usr/bin/env python3
"""Agent 1 P3 counts at the clustered unit, siblings, split integrity, unprocessable fields.
Reads out/corpus_rows.csv and out/sweep.json written by build_corpus.py. Writes out/supply.json.
"""
import json, math
from pathlib import Path
import numpy as np, pandas as pd
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out"
S1, S2 = 3095.5, 3221.5
CHOSEN = 1.0            # radius arcsec, see cut_curve.json for why
SENS = [0.5, 1.5, 2.0, 3.0, 30.0]
AMEND_DPEAK = 60.0      # amendment A1: re-trigger must-join control restricted to |dpeak| <= 60 d

d = pd.read_csv(OUT / "corpus_rows.csv", dtype={"IAUID": str, "type": str, "redshift": str, "peakabs": str,
                                                 "duration": str, "rise": str, "fade": str}, keep_default_na=False)
sweep = json.load(open(OUT / "sweep.json"))


def col(r):
    c = f"cl_{r}"
    return c if c in d else f"cl_{int(r)}" if f"cl_{int(r)}" in d else f"cl_{r:g}"


def cluster_labels(c):
    rows = []
    for cid, g in d.groupby(c):
        labs = set(g.label) - {"unlabeled"}
        if not labs: lab = "unlabeled"
        elif len(labs) == 1: lab = labs.pop()
        elif labs <= {"posA_Ia", "posB"}: lab = "conflict_within_posA"
        else: lab = "conflict"
        types = sorted(set(g.type) - {"-"})
        rows.append(dict(cid=cid, n=len(g), label=lab, types="|".join(types),
                         bright=bool(g.F2_bright_18p5.any()), immature=bool(g.F4_label_immature.all()),
                         pkmin=g.pk.min(), pkmax=g.pk.max()))
    return pd.DataFrame(rows)


def supply(c):
    cl = cluster_labels(c)
    raw = d.label.value_counts().to_dict()
    clc = cl.label.value_counts().to_dict()
    def both(key_rows, key_cl):
        r = int(sum(raw.get(k, 0) for k in key_rows)); k = int(sum(clc.get(x, 0) for x in key_cl))
        return {"raw_rows": r, "clusters": k, "overstatement_pct": round(100 * (r - k) / k, 3) if k else None}
    res = {
        "posA": both(["posA_Ia", "posB"], ["posA_Ia", "posB", "conflict_within_posA"]),
        "posB": both(["posB"], ["posB"]),
        "posA_Ia_only": both(["posA_Ia"], ["posA_Ia"]),
        "neg": both(["neg"], ["neg"]),
        "unlabeled": both(["unlabeled"], ["unlabeled"]),
        "conflict_clusters": int(clc.get("conflict", 0)),
        "conflict_within_posA_clusters": int(clc.get("conflict_within_posA", 0)),
        "total": {"raw_rows": len(d), "clusters": len(cl), "overstatement_pct": round(100 * (len(d) - len(cl)) / len(cl), 3)},
    }
    for name, mask in [("bright_18p5", cl.bright), ("mature_labels", ~cl.immature)]:
        sub = cl[mask].label.value_counts().to_dict()
        res[f"clusters_{name}"] = {"posA": int(sub.get("posA_Ia", 0) + sub.get("posB", 0) + sub.get("conflict_within_posA", 0)),
                                   "posB": int(sub.get("posB", 0)), "neg": int(sub.get("neg", 0)),
                                   "unlabeled": int(sub.get("unlabeled", 0)), "conflict": int(sub.get("conflict", 0)),
                                   "total": int(mask.sum())}
    return res, cl


out = {"chosen_radius_arcsec": CHOSEN, "sensitivity": {}}
res, cl = supply(col(CHOSEN))
out["at_chosen"] = res
for r in SENS:
    out["sensitivity"][str(r)] = supply(col(r))[0]

# per-class counts at clustered unit (unambiguous single-class clusters by type string)
single = cl[~cl.types.str.contains(r"\|")]
out["per_type_clusters"] = single[single.types != ""].types.value_counts().to_dict()
out["per_type_rows"] = d[d.type != "-"].type.value_counts().to_dict()
out["mixed_type_clusters"] = cl[cl.types.str.contains(r"\|")][["types", "n"]].to_dict("records")

# amendment A1 control: re-trigger duplicates (same IAUID, |dpeak|<=60 d)
mj = pd.DataFrame(sweep["must_join_detail"])
mj_rt = mj[mj.dpeak_days <= AMEND_DPEAK]
out["amendment_A1"] = {"retrigger_pairs": len(mj_rt), "max_sep_arcsec": float(mj_rt.sep_arcsec.max()),
                       "long_gap_same_iau_pairs": mj[mj.dpeak_days > AMEND_DPEAK].to_dict("records")}

# siblings: different cluster at chosen cut, sep<=90", both numeric z, |dz|<=0.005
rad = np.radians
xyz = np.c_[np.cos(rad(d.dec)) * np.cos(rad(d.ra)), np.cos(rad(d.dec)) * np.sin(rad(d.ra)), np.sin(rad(d.dec))]
chord = 2 * math.sin(math.radians(90 / 3600) / 2)
pairs = cKDTree(xyz).query_pairs(chord, output_type="ndarray")
z = pd.to_numeric(d.redshift, errors="coerce").values
c = d[col(CHOSEN)].values
keep = [(a, b) for a, b in pairs if c[a] != c[b] and not np.isnan(z[a]) and not np.isnan(z[b]) and abs(z[a] - z[b]) <= 0.005]
out["sibling_pairs"] = len(keep)
if keep:
    k = np.array(keep); n = len(d)
    # component over clusters
    ca, cb = c[k[:, 0]], c[k[:, 1]]
    ids = {v: i for i, v in enumerate(sorted(set(ca) | set(cb)))}
    g = coo_matrix((np.ones(len(k)), ([ids[x] for x in ca], [ids[x] for x in cb])), shape=(len(ids), len(ids)))
    ncomp, lab = connected_components(g, directed=False)
    inv = {i: v for v, i in ids.items()}
    grp = pd.DataFrame({"cid": [inv[i] for i in range(len(ids))], "sib": lab})
    clp = cl.set_index("cid")
    grp["pkmin"] = grp.cid.map(clp.pkmin); grp["pkmax"] = grp.cid.map(clp.pkmax); grp["label"] = grp.cid.map(clp.label)
    sg = grp.groupby("sib").agg(pkmin=("pkmin", "min"), pkmax=("pkmax", "max"), n=("cid", "size"))
    out["sibling_groups"] = int(ncomp)
    out["clusters_in_sibling_groups"] = int(len(ids))
    out["sibling_group_units_if_host_is_unit"] = int(len(cl) - len(ids) + ncomp)
    out["sibling_groups_straddle_S1"] = int(((sg.pkmin < S1) & (sg.pkmax >= S1)).sum())
    out["sibling_groups_straddle_S2"] = int(((sg.pkmin < S2) & (sg.pkmax >= S2)).sum())
    ex = []
    for a, b in keep[:8]:
        ex.append([d.ZTFID[a], d.type[a], d.ZTFID[b], d.type[b], float(z[a]), float(z[b])])
    out["sibling_examples"] = ex
    out["sibling_label_pairs"] = pd.Series([tuple(sorted((d.label[a], d.label[b]))) for a, b in keep]).astype(str).value_counts().to_dict()

# split integrity at every swept cut, plus side sizes at chosen
out["split"] = {r: {"straddle_S1": v["straddle_S1"], "straddle_S2": v["straddle_S2"]} for r, v in sweep["per_cut"].items()}
for nm, s in [("S1", S1), ("S2", S2)]:
    after = cl[cl.pkmin >= s]
    out[f"clusters_after_{nm}"] = {"total": len(after), **{k: int(v) for k, v in after.label.value_counts().items()},
                                  "label_immature_all_members": int(after.immature.sum())}

# unprocessable / defect fields (documented, not repaired), rows and clusters
defects = {}
for f in ["F5_censored_timescale", "F6_no_redshift", "F7_no_peakabs", "F3_low_b", "F4_label_immature"]:
    defects[f] = {"rows": int(d[f].sum())}
for f in ["duration", "rise", "fade"]:
    defects[f"gt_censored_{f}"] = {"rows": int(d[f].str.startswith(">").sum())}
defects["type_dash_rows"] = int((d.type == "-").sum())
defects["IAUID_dash_rows"] = int((d.IAUID == "-").sum())
defects["peakabs_dash_but_redshift_present"] = int(((d.peakabs == "-") & (d.redshift != "-")).sum())
defects["posA_rows_no_redshift"] = int((d.posA.astype(str) == "True").mul(d.redshift == "-").sum())
defects["peakmag_upper_limit_flag_available"] = False
out["defects"] = defects
out["excluded_rows"] = sweep["n_excluded"]
json.dump(out, open(OUT / "supply.json", "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print(json.dumps({k: v for k, v in out.items() if k not in ("sensitivity", "per_type_rows", "mixed_type_clusters")}, indent=1, default=str))
print(json.dumps(out["sensitivity"], indent=0))
