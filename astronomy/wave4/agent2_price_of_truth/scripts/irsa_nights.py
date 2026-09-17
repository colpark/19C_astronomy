#!/usr/bin/env python3
"""calendar_model_FROZEN.md sec 3: P48 nightly science-row counts per month (2021-2024) from IRSA TAP. Resumable."""
import json, time, pathlib, hashlib, urllib.parse, urllib.request, csv, io, sys
from astropy.time import Time
D = pathlib.Path(__file__).resolve().parent.parent
assert hashlib.sha256((D/"calendar_model_FROZEN.md").read_bytes()).hexdigest() == (D/"calendar_model_FROZEN.sha256").read_text().split()[0]
YEARS = [int(x) for x in sys.argv[1:]] or [2021, 2022, 2023, 2024]  # AMW4-2: one worker per year
OUT = D/"out/irsa_nights.jsonl"; done = set()
if OUT.exists():
    for l in open(OUT):
        r = json.loads(l)
        if r["status"] == 200: done.add(r["ym"])
with open(OUT, "a") as fh:
    for y in YEARS:
        for m in range(1, 13):
            ym = f"{y}-{m:02d}"
            if ym in done: continue
            a = Time(f"{y}-{m:02d}-01T00:00:00", scale="utc").jd
            b = Time(f"{y + (m == 12)}-{(m % 12) + 1:02d}-01T00:00:00", scale="utc").jd
            q = f"SELECT FLOOR(obsjd) AS jdn, COUNT(*) AS n FROM ztf.ztf_current_meta_sci WHERE obsjd >= {a} AND obsjd < {b} GROUP BY FLOOR(obsjd)"
            rec = dict(ym=ym, query=q)
            for attempt in range(3):
                t0 = time.time()
                try:
                    data = urllib.parse.urlencode({"QUERY": q, "FORMAT": "CSV"}).encode()
                    r = urllib.request.urlopen("https://irsa.ipac.caltech.edu/TAP/sync", data=data, timeout=600)
                    body = r.read().decode(); rec.update(status=r.status, seconds=round(time.time() - t0, 1),
                        rows=[dict(jdn=int(float(x["jdn"])), n=int(x["n"])) for x in csv.DictReader(io.StringIO(body))], utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
                    break
                except Exception as e:
                    rec.update(status=getattr(e, "code", None) or repr(e)[:200], seconds=round(time.time() - t0, 1), attempt=attempt + 1, utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
                    time.sleep(60)
            fh.write(json.dumps(rec) + "\n"); fh.flush(); print(ym, rec["status"], rec.get("seconds"), len(rec.get("rows", [])), flush=True)
