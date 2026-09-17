#!/usr/bin/env python3
"""T8 (post-seal): enumerate ANTARES loci (LSST dia_object_id, oldest alert >= T0) crossmatched to tns_public_objects; fetch catalog matches."""
import json, time, urllib.parse, urllib.request, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
T0 = 61222.000428
q = {"query": {"bool": {"filter": [{"exists": {"field": "properties.survey.lsst.dia_object_id"}},
      {"range": {"properties.oldest_alert_observation_time": {"gte": T0}}}, {"term": {"catalogs": "tns_public_objects"}}]}}}
url = "https://api.antares.noirlab.edu/v1/loci?" + urllib.parse.urlencode({"elasticsearch_query[locus_listing]": json.dumps(q), "page[limit]": "250"})
loci, log = [], []
while url:
    r = urllib.request.urlopen(url, timeout=120); d = json.load(r); log.append([url, r.status])
    loci += d["data"]; url = d.get("links", {}).get("next"); time.sleep(1)
out = []
for L in loci:
    lid = L["id"]; a = L["attributes"]; p = a["properties"]
    u = f"https://api.antares.noirlab.edu/v1/loci/{lid}/catalog-matches"
    st, tns = None, None
    for k in range(3):
        try:
            r = urllib.request.urlopen(u, timeout=60); st = r.status; cm = json.load(r); break
        except Exception as e:
            st = repr(e); cm = None; time.sleep(5)
    if cm:
        tns = [x for x in cm.get("data", []) if "tns" in json.dumps(x).lower()]
    out.append(dict(locus_id=lid, ra=a["ra"], dec=a["dec"], dia_object_id=p["survey"]["lsst"]["dia_object_id"],
                    oldest=p.get("oldest_alert_observation_time"), brightest_mag=p.get("brightest_alert_magnitude"),
                    num_alerts=p.get("num_alerts"), catmatch_status=st, tns_matches=tns))
    log.append([u, st]); time.sleep(0.5)
json.dump(dict(n_loci=len(loci), loci=out, http_log=log), open(D/"out/antares_tns_cohort.json", "w"), indent=0)
print(len(loci))
