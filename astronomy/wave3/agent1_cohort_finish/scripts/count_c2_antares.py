#!/usr/bin/env python3
"""C2 (with AM1): ANTARES loci carrying an LSST dia_object_id, counted by bisection on
oldest_alert_observation_time, falling back to ra bisection for degenerate timestamps. Reads meta.count only."""
import json, sys, time, urllib.parse, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import safe_fetch as sf
D = pathlib.Path(__file__).resolve().parent.parent
T0, TS, TEND = 61222.000428, 61220.500428, 61300.0
N = {"req": 0}; CAP = 2000; log = []
def count(a, b, ra=None):
    f = [{"exists": {"field": "properties.survey.lsst.dia_object_id"}}]
    if ra is None: f.append({"range": {"properties.oldest_alert_observation_time": {"gte": a, "lt": b}}})
    else:
        f.append({"range": {"properties.oldest_alert_observation_time": {"gte": a, "lte": b}}})
        f.append({"range": {"ra": {"gte": ra[0], "lt": ra[1]}}})
    q = {"query": {"bool": {"filter": f}}}
    url = "https://api.antares.noirlab.edu/v1/loci?" + urllib.parse.urlencode({"elasticsearch_query[locus_listing]": json.dumps(q), "page[limit]": "1"})
    for attempt in range(3):
        N["req"] += 1
        rec, data = sf.fetch("antares_c2_last", "GET", url, timeout=120)
        if rec.get("status") == 200 and isinstance(data, dict) and "meta" in data:
            c = int(data["meta"]["count"]); log.append([a, b, ra, c]); return c
        time.sleep(5)
    log.append([a, b, ra, None, rec.get("status")]); return None
def total(a, b, ra=None):
    if N["req"] > CAP: return None, False
    c = count(a, b, ra)
    if c is None: return None, False
    if c < 10000: return c, True
    if ra is None and (b - a) < 1e-6:
        return total(a, b, (0.0, 360.0))
    if ra is not None:
        if ra[1] - ra[0] < 1e-4: return c, False
        m = (ra[0] + ra[1]) / 2; parts = [(a, b, (ra[0], m)), (a, b, (m, ra[1]))]
    else:
        m = (a + b) / 2; parts = [(a, m, None), (m, b, None)]
    tot, ok = 0, True
    for p in parts:
        x, o = total(*p)
        if x is None: return (tot or None), False
        tot += x; ok = ok and o
    return tot, ok
res = {}
for name, (a, b) in {"cohort_T0_to_61300": (T0, TEND), "S0_TS_to_T0": (TS, T0)}.items():
    t, ok = total(a, b); res[name] = {"loci": t, "complete": ok}
res["requests"] = N["req"]; res["slices"] = log
json.dump(res, open(D / "out/c2_antares.json", "w"), indent=0)
print({k: v for k, v in res.items() if k != "slices"}, len(log))
