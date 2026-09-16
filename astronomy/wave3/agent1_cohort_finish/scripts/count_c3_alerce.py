#!/usr/bin/env python3
"""C3 (with AM2): enumerate ALeRCE/LSST objects with firstmjd in [T0, 61300); label keys stripped by safe_fetch.
Writes out/c3_alerce_objects.csv (oid, meanra, meandec, firstmjd, lastmjd, n_det, n_forced) and out/c3_alerce.json."""
import json, sys, time, pathlib, threading, csv
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent)); import safe_fetch as sf
D = pathlib.Path(__file__).resolve().parent.parent
T0, TEND = 61222.000428, 61300.0
URL = "https://api-lsst.alerce.online/object_api/list_objects?survey=lsst&firstmjd={a}&firstmjd={b}&page_size={ps}&page={p}"
lock = threading.Lock(); N = {"req": 0}; CAP = 4000
objs = {}; slices = []; errors = []
def get(a, b, ps, p):
    for attempt in range(3):
        with lock:
            if N["req"] >= CAP: return None, "cap"
            N["req"] += 1
        rec, d = sf.fetch(f"alerce_c3_{threading.get_ident()}", "GET", URL.format(a=a, b=b, ps=ps, p=p), timeout=180)
        if rec.get("status") == 200 and isinstance(d, dict) and d.get("items") is not None:
            return d["items"], None
        time.sleep(5)
    with lock: errors.append([a, b, p, rec.get("status"), rec.get("error")])
    return None, f"http {rec.get('status')}"
def enum_slice(a, b):
    p = 1; got = 0
    while True:
        items, err = get(a, b, 1000, p)
        if items is None:
            with lock: slices.append([a, b, "incomplete", err, p, got])
            return
        with lock:
            for x in items:
                objs[x["oid"]] = (x["oid"], x.get("meanra"), x.get("meandec"), x.get("firstmjd"), x.get("lastmjd"), x.get("n_det"), x.get("n_forced"))
        got += len(items)
        if len(items) < 1000:
            with lock:
                slices.append([a, b, "complete", None, p, got])
                open(D / "out/c3_progress.txt", "a").write(f"{a:.4f} {b:.4f} pages={p} rows={got} req={N['req']} distinct={len(objs)}\n")
            return
        p += 1
        if p > 30:
            m = (a + b) / 2
            with lock: slices.append([a, b, "split_at_page_30", None, p, got])
            enum_slice(a, m); enum_slice(m, b); return
# AM3: UTC dates with Fink alerts after T0 (out/c1_fink.json lower bracket)
FINK_DATES = json.load(open(D / "out/c1_fink.json"))["lower_bracket_nights_ge_20260701"]["nights"]
from astropy.time import Time
busy = []
for n in FINK_DATES:
    s0 = Time(f"{str(n)[:4]}-{str(n)[4:6]}-{str(n)[6:]}T00:00:00", scale="utc").tai.mjd
    busy.append((max(s0, T0), s0 + 1.0))
undetermined = []
tasks = []
for a, b in busy:
    x = a
    while x < b - 1e-9:
        tasks.append((x, min(x + 0.02, b))); x += 0.02
with ThreadPoolExecutor(2) as ex:
    list(ex.map(lambda ab: enum_slice(*ab), tasks))
with open(D / "out/c3_alerce_objects.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["oid", "meanra", "meandec", "firstmjd", "lastmjd", "n_det", "n_forced"])
    for v in sorted(objs.values()): w.writerow(v)
complete = not undetermined and all(s[2] != "incomplete" for s in slices) and N["req"] < CAP
json.dump(dict(amendment="AM3", fink_dates=FINK_DATES, requests=N["req"], cap=CAP, busy_days=busy, undetermined_days=undetermined, n_slices=len(tasks),
               slices=slices, errors=errors, distinct_oids=len(objs), complete=complete), open(D / "out/c3_alerce.json", "w"), indent=0)
print("requests", N["req"], "busy days", len(busy), "undetermined", len(undetermined), "distinct", len(objs), "complete", complete, "errors", len(errors))
