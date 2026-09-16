#!/usr/bin/env python3
"""C5 (AM5): ALeRCE/LSST objects first detected before T0 with a detection on or after T0 (S1 straddlers). Non-label fields only."""
import json, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import safe_fetch as sf
from astropy.time import Time
D = pathlib.Path(__file__).resolve().parent.parent
T0 = 61222.000428; CAP = 3000; N = {"req": 0}; objs = {}; incomplete = []
URL = "https://api-lsst.alerce.online/object_api/list_objects?survey=lsst&firstmjd={a}&firstmjd={b}&lastmjd=" + str(T0) + "&lastmjd=61300&page_size=1000&page={p}"
def get(a, b, p):
    for _ in range(3):
        if N["req"] >= CAP: return None
        N["req"] += 1
        rec, d = sf.fetch("c5_alerce", "GET", URL.format(a=a, b=b, p=p), timeout=180)
        if rec.get("status") == 200 and isinstance(d, dict) and d.get("items") is not None: return d["items"]
        time.sleep(5)
    return None
def run(a, b):
    it = get(a, b, 1)
    if it is None: incomplete.append([a, b]); return
    if len(it) < 1000:
        for x in it: objs[x["oid"]] = (x["firstmjd"], x["lastmjd"], x["n_det"])
        return
    if b - a > 0.0005:
        m = (a + b) / 2; run(a, m); run(m, b); return
    p = 1
    while True:
        for x in it: objs[x["oid"]] = (x["firstmjd"], x["lastmjd"], x["n_det"])
        if len(it) < 1000: return
        p += 1; it = get(a, b, p)
        if it is None: incomplete.append([a, b, p]); return
stats = json.load(open(D / "out/raw/fink_stats_2026.json"))
dates = sorted(int(r["f:night"]) for r in stats if int(r["f:alerts"]) > 0 and int(r["f:night"]) >= 20260224 and int(r["f:night"]) <= 20260701)
for n in dates:
    s0 = Time(f"{str(n)[:4]}-{str(n)[4:6]}-{str(n)[6:]}T00:00:00", scale="utc").tai.mjd
    a, b = max(s0, 61095.000428), min(s0 + 1.0, T0)
    if a < b: run(a, b)
    open(D / "out/c5_progress.txt", "a").write(f"{n} req={N['req']} straddlers={len(objs)} incomplete={len(incomplete)}\n")
bad = sum(1 for v in objs.values() if v[1] < T0 or v[0] >= T0)
out = dict(amendment="AM5", dates=dates, requests=N["req"], cap=CAP, incomplete=incomplete, complete=(not incomplete and N["req"] < CAP),
           S1_straddlers=len(objs), rows_violating_filter=bad, sum_n_det=sum(v[2] for v in objs.values()))
json.dump(out, open(D / "out/c5_straddlers.json", "w"), indent=0); print(out)
