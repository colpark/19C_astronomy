import json, sys, pathlib, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from safe_fetch import fetch
ids=["170609056632799366","170609056633848501","170609056634372105","170609056634372804","170609056634372829","170609056633849114","170609056634373061"]
SRC = "r:diaObjectId,r:diaSourceId,r:midpointMjdTai,r:band,r:psfFlux,r:psfFluxErr,r:ra,r:dec,r:snr,r:isNegative,r:reliability"
summ=[]
for oid in ids:
    r,d=fetch(f"s4_sources_{oid}","POST","https://api.lsst.fink-portal.org/api/v1/sources",{"diaObjectId": oid, "columns": SRC, "output-format": "json"})
    summ.append({"oid":oid,"status":r.get("status"),"n_rows":len(d) if isinstance(d,list) else None,"raw_sha256":r.get("raw_sha256"),"dropped":r.get("dropped_keys"),"time_utc":r["time_utc"],
                 "sanitized_sha256":hashlib.sha256(json.dumps(d).encode()).hexdigest()})
print(json.dumps(summ,indent=0))
json.dump(summ,open("/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave4/agent4_module_v/data_cache/alert_fetch_summary.json","w"),indent=1)
