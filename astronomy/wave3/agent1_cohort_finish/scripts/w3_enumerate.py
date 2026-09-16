#!/usr/bin/env python3
"""W3-C3 / W3-P60 / W3-C5 enumeration of ALeRCE/LSST object rows (label keys stripped by safe_fetch).
usage: w3_enumerate.py NAME DATE_LO DATE_HI MJD_LO MJD_HI [lastmjd_ge]
Slices every UTC date in [DATE_LO, DATE_HI] with Fink alerts > 0 into 0.02 d, clipped to [MJD_LO, MJD_HI).
Persists each completed slice to out/<NAME>_slices/. 2 h wall cap from launch."""
import csv, json, sys, time, pathlib, threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import safe_fetch as sf
from astropy.time import Time
D = pathlib.Path(__file__).resolve().parent.parent
name, dlo, dhi, mlo, mhi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
lastge = float(sys.argv[6]) if len(sys.argv) > 6 else None
import os
START = time.time(); CAP_S = 7200; PS = 5000; MAXPAGE = 200
THREADS = int(os.environ.get("W3_THREADS", "3")); RETRIES = int(os.environ.get("W3_RETRIES", "3")); BACKOFF = int(os.environ.get("W3_BACKOFF", "10"))  # AM6 resume: 1, 6, 60
out = D / f"out/{name}_slices"; out.mkdir(parents=True, exist_ok=True)
prog = D / f"out/{name}_progress.txt"; lock = threading.Lock(); st = {"req": 0, "err": []}
stats = json.load(open(D / "out/raw/fink_stats_2026.json"))
dates = sorted(int(r["f:night"]) for r in stats if dlo <= int(r["f:night"]) <= dhi and int(r["f:alerts"]) > 0)
tasks = []
for n in dates:
    s0 = Time(f"{str(n)[:4]}-{str(n)[4:6]}-{str(n)[6:]}T00:00:00", scale="utc").tai.mjd
    a, b = max(s0, mlo), min(s0 + 1.0, mhi); x = a
    while x < b - 1e-9:
        tasks.append((round(x, 6), round(min(x + 0.02, b), 6))); x += 0.02
def url(a, b, p):
    u = f"https://api-lsst.alerce.online/object_api/list_objects?survey=lsst&firstmjd={a}&firstmjd={b}&page_size={PS}&page={p}"
    return u + (f"&lastmjd={lastge}&lastmjd=61400" if lastge else "")
def slice_(ab):
    a, b = ab; f = out / f"{a:.6f}_{b:.6f}.csv"
    if f.exists(): return
    rows = {}; p = 1
    while True:
        if time.time() - START > CAP_S:
            with lock: st["err"].append([a, b, p, "time cap"]); return
        it = None
        for _ in range(RETRIES):
            with lock: st["req"] += 1
            rec, d = sf.fetch(f"{name}_{threading.get_ident()}", "GET", url(a, b, p), timeout=300)
            if rec.get("status") == 200 and isinstance(d, dict) and d.get("items") is not None:
                it = d["items"]; break
            time.sleep(BACKOFF if rec.get("status") == 429 else 10)
        if it is None:
            with lock: st["err"].append([a, b, p, rec.get("status")]); return
        for o in it: rows[o["oid"]] = (o["oid"], o.get("meanra"), o.get("meandec"), o.get("firstmjd"), o.get("lastmjd"), o.get("n_det"), o.get("n_forced"))
        if len(it) < PS: break
        p += 1
        if p > MAXPAGE:
            with lock: st["err"].append([a, b, p, "page cap"]); return
    tmp = f.with_suffix(".tmp")
    with open(tmp, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["oid", "meanra", "meandec", "firstmjd", "lastmjd", "n_det", "n_forced"]); w.writerows(rows.values())
    tmp.rename(f)
    with lock: open(prog, "a").write(f"{time.strftime('%H:%M:%S')} {a:.4f} pages={p} rows={len(rows)} req={st['req']}\n")
with ThreadPoolExecutor(THREADS) as ex: list(ex.map(slice_, tasks))
done = sum(1 for a, b in tasks if (out / f"{a:.6f}_{b:.6f}.csv").exists())
res = dict(name=name, dates=dates, lastmjd_ge=lastge, slices_planned=len(tasks), slices_done=done, complete=(done == len(tasks)),
           requests=st["req"], errors=st["err"], wall_s=round(time.time() - START))
json.dump(res, open(D / f"out/{name}.json", "w"), indent=0); print(res)
