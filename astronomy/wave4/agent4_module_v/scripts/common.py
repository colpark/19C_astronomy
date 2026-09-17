import json, hashlib, os, datetime, subprocess
VD="/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave4/agent4_module_v"
REPO="/home/aid1/Documents/4_19C_astronomy/repo"
def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda: f.read(1<<20), b""): h.update(b)
    return h.hexdigest()
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
def oplog(msg, *files):
    line=f"{now()} | {msg}"
    for f in files: line+=f" | sha256:{sha(f)} {os.path.relpath(f,VD)}"
    open(f"{VD}/order_of_operations.log","a").write(line+"\n")
def seal(tid, derived, method, inputs, extra=None):
    p=f"{VD}/sealed/V-{tid}.json"
    if os.path.exists(p): raise SystemExit(f"{p} already sealed; refusing to overwrite")
    rec={"id":tid,"sealed_utc":now(),"derived":derived,"method":method,"inputs":inputs}
    if extra: rec.update(extra)
    json.dump(rec,open(p,"w"),indent=1,default=str)
    h=sha(p); open(f"{VD}/sealed/SEALED_SHA256SUMS","a").write(f"{h}  V-{tid}.json\n")
    oplog(f"sealed V-{tid} before opening claimed value", p)
    return h
