#!/usr/bin/env python3
"""W3-M: X1-X3 merge over W3-C3 (cohort) + W3-P60 (60 d before T0); S1 straddlers; one-detection share; unprocessable.
Non-label fields only. Writes out/w3_merge.json."""
import csv, glob, json, math, pathlib, hashlib
import numpy as np
from scipy.spatial import cKDTree
D = pathlib.Path(__file__).resolve().parent.parent
T0 = 61222.000428
def load(name):
    rows = {}; files = sorted(glob.glob(str(D / f"out/{name}_slices/*.csv")))
    h = hashlib.sha256()
    for f in files:
        h.update(pathlib.Path(f).read_bytes())
        for r in csv.DictReader(open(f)): rows[r["oid"]] = r
    st = json.load(open(D / f"out/{name}.json")) if (D / f"out/{name}.json").exists() else {"complete": False, "note": "job summary absent"}
    return rows, len(files), h.hexdigest(), st
c3, n3, h3, s3 = load("w3_c3"); p60, n60, h60, s60 = load("w3_p60"); c5, n5, h5, s5 = load("w3_c5")
def bad(r):
    try:
        ra, dec, fm = float(r["meanra"]), float(r["meandec"]), float(r["firstmjd"])
        return not (r["oid"] and -90 <= dec <= 90 and math.isfinite(ra) and math.isfinite(fm))
    except (ValueError, TypeError): return True
allrows = {**p60, **c3}
overlap = len(set(c3) & set(p60))
U = [o for o, r in allrows.items() if bad(r)]
good = {o: r for o, r in allrows.items() if not bad(r)}
oids = list(good); ra = np.radians([float(good[o]["meanra"]) for o in oids]); dec = np.radians([float(good[o]["meandec"]) for o in oids])
fm = np.array([float(good[o]["firstmjd"]) for o in oids]); lm = np.array([float(good[o]["lastmjd"]) for o in oids])
nd = np.array([int(float(good[o]["n_det"])) for o in oids])
xyz = np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
tol = 2 * math.sin(math.radians(1 / 3600) / 2)
pairs = cKDTree(xyz).query_pairs(tol, output_type="ndarray")
par = np.arange(len(oids))
def find(i):
    r = i
    while par[r] != r: r = par[r]
    while par[i] != r: par[i], i = r, par[i]
    return r
x2 = x3 = 0
for i, j in pairs:
    if abs(fm[i] - fm[j]) <= 60:
        a, b = find(i), find(j)
        if a != b: par[a] = b
        x2 += 1
    else: x3 += 1
root = np.array([find(i) for i in range(len(oids))])
coh = fm >= T0
comp_min = {}; comp_nd = {}; comp_n = {}
for i, r in enumerate(root):
    comp_min[r] = min(comp_min.get(r, 1e9), fm[i]); comp_nd[r] = comp_nd.get(r, 0) + nd[i]; comp_n[r] = comp_n.get(r, 0) + 1
coh_roots = {root[i] for i in range(len(oids)) if coh[i]}
O_merged_roots = [r for r in coh_roots if comp_min[r] >= T0]
S1_merge_oids = int(sum(1 for i in range(len(oids)) if coh[i] and comp_min[root[i]] < T0))
S1_merge_groups = len(coh_roots) - len(O_merged_roots)
pre = ~coh
S1_direct_p60 = int(np.sum(pre & (lm >= T0)))
S1_direct_c5 = len(c5)  # firstmjd in [2026-02-24, T0-60 d) with lastmjd >= T0
coh_n = int(coh.sum())
res = dict(
  inputs=dict(w3_c3=dict(slices=n3, rows_sha256=h3, summary=s3, distinct=len(c3)), w3_p60=dict(slices=n60, rows_sha256=h60, summary=s60, distinct=len(p60)),
              w3_c5=dict(slices=n5, rows_sha256=h5, summary=s5, distinct=len(c5)), c3_p60_oid_overlap=overlap),
  cohort_oids=coh_n, cohort_raw_detections_sum_n_det=int(nd[coh].sum()),
  overstatement_pct_detections_vs_oids=round((int(nd[coh].sum()) - coh_n) / coh_n * 100, 2) if coh_n else None,
  S3_one_detection_oids=int(np.sum(coh & (nd == 1))), S3_share_oids=round(float(np.mean(nd[coh] == 1)), 4) if coh_n else None,
  X2_pairs_joined=x2, X3_same_position_distinct_pairs=x3,
  O_merged=len(O_merged_roots),
  merged_overstatement_pct_oids_vs_merged=round((coh_n - S1_merge_oids - len(O_merged_roots)) / len(O_merged_roots) * 100, 3) if O_merged_roots else None,
  S3_one_detection_share_merged=round(float(np.mean([comp_nd[r] == 1 for r in O_merged_roots])), 4) if O_merged_roots else None,
  S1_merge_oids=S1_merge_oids, S1_merge_groups=S1_merge_groups,
  S1_direct_firstmjd_T0minus60_to_T0=S1_direct_p60, S1_direct_firstmjd_20260224_to_T0minus60=S1_direct_c5,
  S1_total_direct_plus_merge_oids=S1_direct_p60 + S1_direct_c5 + S1_merge_oids,
  unprocessable_U=len(U), unprocessable_examples=U[:5], c5_rows_violating_filter=sum(1 for r in c5.values() if float(r["lastmjd"]) < T0))
json.dump(res, open(D / "out/w3_merge.json", "w"), indent=1, default=int)
print(json.dumps(res, indent=1, default=int))
