#!/usr/bin/env python3
"""Protocol sec 6: enumeration list E and tiers. Tier A = cohort-matched (LSST alias id in cohort, or <=1" from a cohort oid
with discovery >= 2026-06-30, or ANTARES cohort locus TNS match with discovery >= 2026-06-30). Tier B = other typed 2026 entries,
random permutation seed 20260917. Interpretation AMW3-1 (declared before any T1 fetch): E for tier B is restricted to entries with a
type (classified) in T9, because untyped objects have no classification report to census."""
import json, glob, hashlib, pathlib, re
import numpy as np
from scipy.spatial import cKDTree
D = pathlib.Path(__file__).resolve().parent.parent
A1 = D.parent / "agent1_cohort_finish"
T0 = 61222.000428
oids, xyz = [], []
for f in sorted(glob.glob(str(A1/"out/w3_c3_slices/*.csv"))):
    a = np.genfromtxt(f, delimiter=",", skip_header=1, usecols=(1, 2, 3), dtype=float)
    if a.size == 0: continue
    a = np.atleast_2d(a)
    ids = [l.split(",")[0] for l in open(f).read().splitlines()[1:]]
    m = a[:, 2] >= T0
    oids += [i for i, k in zip(ids, m) if k]
    ra, dec = np.radians(a[m, 0]), np.radians(a[m, 1])
    xyz.append(np.c_[np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)])
xyz = np.vstack(xyz); oidset = set(oids); tree = cKDTree(xyz)
R1 = 2*np.sin(np.radians(1/3600)/2)
entries = {}
for fn in ["rochester_entries_rochester_sn2026_index.json", "rochester_entries_rochester_supernova.json"]:
    for e in json.load(open(D/"out"/fn)):
        entries.setdefault(e["name"], e)
def cohort_match(e):
    ids = re.findall(r"LSST-[A-Z]+-DO-(\d+)", e.get("aliases") or "")
    hit = [i for i in ids if i in oidset]
    if hit: return "id:" + hit[0]
    if e["ra_deg"] is not None and (e["discdate"] or "") >= "2026-06-30":
        ra, dec = np.radians(e["ra_deg"]), np.radians(e["dec_deg"])
        d, j = tree.query([np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)], k=1)
        if d <= R1: return "pos:" + oids[j]
    return None
tierA, tierB = [], []
for n, e in entries.items():
    typed = e["type"] and "unknown" not in e["type"]
    cm = cohort_match(e)
    if cm: tierA.append(dict(name=n, source="T9", cohort=cm, typed_T9=bool(typed), discdate=e["discdate"], type_T9=e["type"]))
    elif typed: tierB.append(dict(name=n, source="T9", discdate=e["discdate"], type_T9=e["type"]))
ant = json.load(open(D/"out/antares_tns_cohort.json"))
names = {x["name"] for x in tierA}
for L in ant["loci"]:
    for m in L["tns_matches"] or []:
        pr = m["attributes"]["properties"]
        if (pr.get("discoverydate") or "") >= "2026-06-30" and pr["name"] not in names:
            tierA.append(dict(name=pr["name"], source="T8", cohort="antares:" + L["dia_object_id"][0], typed_T9=None,
                              discdate=pr.get("discoverydate"), type_T8=pr.get("type")))
            names.add(pr["name"])
tierB = [x for x in tierB if x["name"] not in names]
rng = np.random.default_rng(20260917)
tierB = [tierB[i] for i in rng.permutation(len(tierB))]
E = dict(interpretation="AMW3-1 declared before any T1 fetch", cohort_oids=len(oids), tierA=tierA, tierB=tierB,
         counts=dict(tierA=len(tierA), tierA_typed_T9=sum(1 for x in tierA if x.get("typed_T9")), tierB=len(tierB), T9_entries=len(entries)))
p = D/"sealed/enumeration_E_SEALED.json"; p.write_text(json.dumps(E, indent=0))
h = hashlib.sha256(p.read_bytes()).hexdigest(); (D/"sealed/enumeration_E_SEALED.sha256").write_text(f"{h}  enumeration_E_SEALED.json\n")
print(E["counts"], h)
