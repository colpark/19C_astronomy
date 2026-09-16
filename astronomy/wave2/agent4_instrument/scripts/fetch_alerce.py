"""Select the frozen cohort (section 2) and pull ALeRCE light curves (section 9 caps).
calibration only, contamination FAIL on this cohort. PRE-I1: graph edge R1->I1 unmet, escalated."""
import json, os, time, datetime, concurrent.futures as cf
import pandas as pd, requests
from common import W, CORPUS, check_frozen, sha256, BANNER

check_frozen()
RAW = os.path.join(W, "data_cache", "alerce_raw")
os.makedirs(RAW, exist_ok=True)
d = pd.read_csv(CORPUS, dtype=str)
t = pd.to_datetime(d.peakt.astype(float) + 2458000 - 2440587.5, unit="D")
m = (t >= "2019-06-01") & (t < "2021-04-15")
coh = d[m].copy()
coh.to_csv(os.path.join(W, "data_cache", "cohort_rows.csv"), index=False)
ids = sorted(coh.ZTFID.unique())
print(BANNER)
print("cohort rows", len(coh), "ztfids", len(ids), "units", coh.object_cluster_1arcsec.nunique())
if len(ids) > 4000:
    raise SystemExit("cap exceeded before fetch")

calls = {"n": 0}


def pull(oid):
    path = os.path.join(RAW, oid + ".json")
    if os.path.exists(path):
        return oid, "cached", None
    url = f"https://api.alerce.online/ztf/v1/objects/{oid}/lightcurve"
    err = None
    for attempt in range(3):
        calls["n"] += 1
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    f.write(r.content)
                return oid, "ok", None
            err = f"http {r.status_code}"
            if r.status_code == 404:
                break
        except Exception as e:  # noqa
            err = repr(e)
        time.sleep(2 ** attempt)
    return oid, "fail", err


log = []
with cf.ThreadPoolExecutor(4) as ex:
    for oid, st, err in ex.map(pull, ids):
        log.append({"ZTFID": oid, "status": st, "error": err})
fails = [x for x in log if x["status"] == "fail"]
man = []
for oid in ids:
    p = os.path.join(RAW, oid + ".json")
    if os.path.exists(p):
        man.append(f"{sha256(p)}  data_cache/alerce_raw/{oid}.json")
open(os.path.join(W, "data_cache", "ALERCE_RAW_SHA256SUMS"), "w").write("\n".join(man) + "\n")
json.dump({"banner": BANNER, "fetched_utc": datetime.datetime.utcnow().isoformat() + "Z",
           "endpoint": "https://api.alerce.online/ztf/v1/objects/{oid}/lightcurve",
           "n_ids": len(ids), "n_ok_files": len(man), "n_fail": len(fails),
           "http_attempts_this_run": calls["n"], "fails": fails},
          open(os.path.join(W, "data_cache", "fetch_log.json"), "w"), indent=1)
print("files", len(man), "fails", len(fails), "attempts", calls["n"])
