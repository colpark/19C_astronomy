#!/usr/bin/env python3
"""C4: object-level cross-broker check on declared sample W = ALeRCE cohort oids with firstmjd in [T0, T0+0.25 d)
(first 3000 by firstmjd). Non-label columns only. Fink /objects; ANTARES loci terms filter."""
import csv, json, sys, time, pathlib, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import safe_fetch as sf
D = pathlib.Path(__file__).resolve().parent.parent
T0 = 61222.000428
# AM4: enumerate W directly
rows = {}; x = T0
while x < T0 + 0.25 - 1e-9:
    b = min(x + 0.02, T0 + 0.25); p = 1
    while True:
        for attempt in range(3):
            rec, d = sf.fetch("c4_alerce", "GET", f"https://api-lsst.alerce.online/object_api/list_objects?survey=lsst&firstmjd={x}&firstmjd={b}&page_size=1000&page={p}", timeout=180)
            if rec.get("status") == 200 and isinstance(d, dict): break
            time.sleep(5)
        it = (d.get("items") or []) if isinstance(d, dict) else None
        if it is None: raise SystemExit(f"W enumeration failed at {x} page {p}: {rec.get('status')}")
        for o in it: rows[str(o["oid"])] = dict(oid=str(o["oid"]), firstmjd=o["firstmjd"], n_det=o["n_det"], meanra=o["meanra"], meandec=o["meandec"])
        if len(it) < 1000: break
        p += 1
    x = b
rows = list(rows.values())
rows.sort(key=lambda r: (float(r["firstmjd"]), int(r["oid"])))
W_total = len(rows); rows = rows[:3000]
ids = [r["oid"] for r in rows]
fink, ant, errs = {}, {}, []
for i in range(0, len(ids), 100):
    chunk = ids[i:i + 100]
    for attempt in range(3):
        rec, d = sf.fetch("c4_fink", "POST", "https://api.lsst.fink-portal.org/api/v1/objects",
                          {"diaObjectId": ",".join(chunk), "columns": "r:diaObjectId,r:firstDiaSourceMjdTai,r:nDiaSources,r:ra,r:dec", "output-format": "json"}, timeout=180)
        if rec.get("status") == 200 and isinstance(d, list): break
        time.sleep(5)
    if isinstance(d, list):
        for x in d: fink[str(x.get("r:diaObjectId"))] = x
    else: errs.append(["fink", i, rec.get("status")])
    q = {"query": {"bool": {"filter": {"terms": {"properties.survey.lsst.dia_object_id": chunk}}}}}
    url = "https://api.antares.noirlab.edu/v1/loci?" + urllib.parse.urlencode({"elasticsearch_query[locus_listing]": json.dumps(q), "page[limit]": "250"})
    for attempt in range(3):
        rec, d = sf.fetch("c4_antares", "GET", url, timeout=180)
        if rec.get("status") == 200 and isinstance(d, dict) and "data" in d: break
        time.sleep(5)
    if isinstance(d, dict) and "data" in d:
        for it in d["data"]:
            p = it["attributes"]["properties"]
            for oid in p.get("survey", {}).get("lsst", {}).get("dia_object_id", []):
                if oid in chunk:
                    ant.setdefault(oid, []).append(dict(locus=it["id"], num_alerts=p.get("num_alerts"),
                        oldest=p.get("oldest_alert_observation_time"), n_lsst_ids=len(p["survey"]["lsst"]["dia_object_id"]),
                        has_ztf=bool(p.get("survey", {}).get("ztf", {}).get("id"))))
    else: errs.append(["antares", i, rec.get("status")])
out = []
for r in rows:
    f = fink.get(r["oid"]); a = ant.get(r["oid"], [])
    out.append(dict(oid=r["oid"], alerce_firstmjd=float(r["firstmjd"]), alerce_n_det=int(r["n_det"]),
                    fink_present=f is not None, fink_first=(f or {}).get("r:firstDiaSourceMjdTai"), fink_nDiaSources=(f or {}).get("r:nDiaSources"),
                    antares_loci=len(a), antares_num_alerts=(a[0]["num_alerts"] if a else None), antares_oldest=(a[0]["oldest"] if a else None),
                    antares_locus_lsst_ids=(a[0]["n_lsst_ids"] if a else None), antares_locus_has_ztf=(a[0]["has_ztf"] if a else None)))
def n(pred): return sum(1 for x in out if pred(x))
summ = dict(W_total_in_alerce=W_total, sampled=len(out), errors=errs,
            in_fink=n(lambda x: x["fink_present"]), in_antares=n(lambda x: x["antares_loci"] > 0), in_both=n(lambda x: x["fink_present"] and x["antares_loci"] > 0),
            fink_places_before_T0=n(lambda x: x["fink_first"] is not None and x["fink_first"] < T0),
            antares_oldest_before_T0=n(lambda x: x["antares_oldest"] is not None and x["antares_oldest"] < T0),
            first_detection_disagree_gt_1s=n(lambda x: x["fink_first"] is not None and abs(x["fink_first"] - x["alerce_firstmjd"]) > 1 / 86400),
            ndet_disagree_fink_vs_alerce=n(lambda x: x["fink_nDiaSources"] is not None and int(x["fink_nDiaSources"]) != x["alerce_n_det"]),
            antares_locus_with_ztf=n(lambda x: bool(x["antares_locus_has_ztf"])), antares_locus_multi_lsst_ids=n(lambda x: (x["antares_locus_lsst_ids"] or 0) > 1),
            antares_multi_loci_per_oid=n(lambda x: x["antares_loci"] > 1),
            unprocessable_missing_first_or_pos=n(lambda x: x["alerce_firstmjd"] is None),
            sum_alerce_n_det=sum(x["alerce_n_det"] for x in out), sum_fink_nDiaSources=sum(int(x["fink_nDiaSources"]) for x in out if x["fink_nDiaSources"] is not None),
            sum_antares_num_alerts=sum(int(x["antares_num_alerts"]) for x in out if x["antares_num_alerts"] is not None))
json.dump(dict(summary=summ, rows=out), open(D / "out/c4_crossbroker.json", "w"), indent=0)
print(json.dumps(summ, indent=1))
