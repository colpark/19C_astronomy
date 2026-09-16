#!/usr/bin/env python3
"""W3-X: per cohort UTC date, the 1000 oids with smallest sha1(oid); Fink /objects (Rubin firstDiaSourceMjdTai, nDiaSources,
Fink-computed first time) and ANTARES presence. Non-label fields only (safe_fetch strips label keys)."""
import csv, glob, hashlib, json, sys, time, pathlib, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import safe_fetch as sf
from astropy.time import Time
D = pathlib.Path(__file__).resolve().parent.parent
T0 = 61222.000428
rows = {}
for f in glob.glob(str(D / "out/w3_c3_slices/*.csv")):
    for r in csv.DictReader(open(f)): rows[r["oid"]] = r
bydate = {}
for o, r in rows.items():
    d = Time(float(r["firstmjd"]), format="mjd", scale="tai").utc.strftime("%Y%m%d")
    bydate.setdefault(d, []).append(o)
sample = []
for d in sorted(bydate):
    sample += sorted(bydate[d], key=lambda o: hashlib.sha1(o.encode()).hexdigest())[:1000]
fink, ant, errs = {}, {}, []
for i in range(0, len(sample), 100):
    ch = sample[i:i + 100]; d = None
    for _ in range(3):
        rec, d = sf.fetch("w3x_fink", "POST", "https://api.lsst.fink-portal.org/api/v1/objects",
                          {"diaObjectId": ",".join(ch), "columns": "r:diaObjectId,r:firstDiaSourceMjdTai,r:nDiaSources,f:firstDiaSourceMjdTaiFink", "output-format": "json"}, timeout=180)
        if rec.get("status") == 200 and isinstance(d, list): break
        time.sleep(5)
    if isinstance(d, list):
        for x in d: fink[str(x.get("r:diaObjectId"))] = x
    else: errs.append(["fink", i, rec.get("status")])
    q = {"query": {"bool": {"filter": {"terms": {"properties.survey.lsst.dia_object_id": ch}}}}}
    u = "https://api.antares.noirlab.edu/v1/loci?" + urllib.parse.urlencode({"elasticsearch_query[locus_listing]": json.dumps(q), "page[limit]": "250"})
    d = None
    for _ in range(3):
        rec, d = sf.fetch("w3x_antares", "GET", u, timeout=180)
        if rec.get("status") == 200 and isinstance(d, dict) and "data" in d: break
        time.sleep(5)
    if isinstance(d, dict) and "data" in d:
        for it in d["data"]:
            p = it["attributes"]["properties"]
            for oid in p.get("survey", {}).get("lsst", {}).get("dia_object_id", []):
                if oid in ch: ant.setdefault(oid, []).append((p.get("num_alerts"), p.get("oldest_alert_observation_time")))
    else: errs.append(["antares", i, rec.get("status")])
def fl(v):
    try: return float(v)
    except (TypeError, ValueError): return None
out = []
for o in sample:
    f = fink.get(o, {}); r = rows[o]
    out.append(dict(oid=o, alerce_first=float(r["firstmjd"]), alerce_ndet=int(float(r["n_det"])), fink=o in fink,
                    rubin_first=fl(f.get("r:firstDiaSourceMjdTai")), fink_first=fl(f.get("f:firstDiaSourceMjdTaiFink")), rubin_nDiaSources=f.get("r:nDiaSources"),
                    antares=len(ant.get(o, [])), antares_oldest=(ant[o][0][1] if o in ant else None)))
n = lambda p: sum(1 for x in out if p(x))
S = dict(sample=len(out), per_date={d: min(1000, len(v)) for d, v in sorted(bydate.items())}, errors=errs,
         in_fink=n(lambda x: x["fink"]), in_antares=n(lambda x: x["antares"] > 0),
         rubin_first_before_T0=n(lambda x: x["rubin_first"] is not None and x["rubin_first"] < T0),
         rubin_first_earlier_than_alerce_first_gt_1s=n(lambda x: x["rubin_first"] is not None and x["rubin_first"] < x["alerce_first"] - 1 / 86400),
         rubin_first_later_than_alerce_first_gt_1s=n(lambda x: x["rubin_first"] is not None and x["rubin_first"] > x["alerce_first"] + 1 / 86400),
         fink_first_differs_rubin_first_gt_1s=n(lambda x: x["rubin_first"] is not None and x["fink_first"] is not None and abs(x["fink_first"] - x["rubin_first"]) > 1 / 86400),
         rubin_first_missing=n(lambda x: x["fink"] and x["rubin_first"] is None),
         antares_oldest_before_T0=n(lambda x: x["antares_oldest"] is not None and x["antares_oldest"] < T0),
         nDiaSources_ne_alerce_ndet=n(lambda x: x["rubin_nDiaSources"] is not None and int(x["rubin_nDiaSources"]) != x["alerce_ndet"]))
json.dump(dict(summary=S, rows=out), open(D / "out/w3_crosscheck.json", "w"), indent=0)
print(json.dumps(S, indent=1))
