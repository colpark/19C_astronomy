#!/usr/bin/env python3
"""Protocol sec 7: peak difference-flux magnitude for sample R via Fink /api/v1/sources (label keys stripped by safe_fetch)."""
import json, sys, time, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from safe_fetch import fetch
D = pathlib.Path(__file__).resolve().parent.parent
oids = json.load(open(D/"sealed/lookup_list_SEALED.json"))["sample_R"]["oids"]
out = D/"out/reach_rows.jsonl"; done = set()
if out.exists():
    for l in open(out): done.add(json.loads(l)["batch"])
cols = "r:diaObjectId,r:psfFlux,r:psfFluxErr,r:band,r:midpointMjdTai"
with open(out, "a") as fh:
    for b in range(0, len(oids), 100):
        if b in done: continue
        ids = ",".join(oids[b:b+100])
        for attempt in range(4):
            rec, data = fetch(f"reach_{b:04d}", "POST", "https://api.lsst.fink-portal.org/api/v1/sources", {"diaObjectId": ids, "columns": cols, "output-format": "json"})
            if rec.get("status") == 200 and isinstance(data, list): break
            time.sleep(60 if rec.get("status") in (429, 503) else 10)
        fh.write(json.dumps(dict(batch=b, status=rec.get("status"), n_rows=len(data) if isinstance(data, list) else None, rows=data if isinstance(data, list) else None)) + "\n"); fh.flush()
        print(b, rec.get("status"), len(data) if isinstance(data, list) else None, flush=True)
        time.sleep(1.0)
