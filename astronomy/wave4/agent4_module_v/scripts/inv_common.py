import json, hashlib, datetime, pathlib
VD=pathlib.Path("/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave4/agent4_module_v")
RUNLOG=VD/"invariance_runs.jsonl"; CAP=90
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
def used():
    if not RUNLOG.exists(): return 0
    return sum(json.loads(l)["alert_runs"] for l in open(RUNLOG))
def load_alert(oid):
    rows=json.load(open(VD/"data_cache/alerts/out/raw"/f"s4_sources_{oid}.sanitized.json"))
    return sorted(rows,key=lambda r:r["r:midpointMjdTai"])
def h(o): return hashlib.sha256(json.dumps(o,sort_keys=True,default=str).encode()).hexdigest()
def log(tool,arm,oids,start,status,per_alert_hash,err=None):
    n=len(oids)
    if used()+n>CAP: raise SystemExit("rule D cap would be exceeded")
    rec=dict(tool=tool,arm=arm,alert_ids=oids,alert_runs=n,start_utc=start,end_utc=now(),status=status,output_sha256_per_alert=per_alert_hash,error=err,cumulative_alert_runs=used()+n)
    open(RUNLOG,"a").write(json.dumps(rec)+"\n"); return rec
def compare(results, tol=1e-6):
    """results: {oid: {arm: (hash, flat_numeric_list)}} -> verdict per oid"""
    out={}
    for oid,arms in results.items():
        hs={a:v[0] for a,v in arms.items()}
        base=arms["alone"][1]; maxd=0.0; shape_ok=True
        for a,v in arms.items():
            if len(v[1])!=len(base): shape_ok=False; continue
            for x,y in zip(v[1],base):
                try:
                    fx,fy=float(x),float(y)
                    if fx!=fx or fy!=fy:
                        if not (fx!=fx and fy!=fy): maxd=float("inf")   # NaN vs value (fixed after defect)
                    else: maxd=max(maxd,abs(fx-fy))
                except Exception:
                    if x!=y: maxd=float("inf")
        bit=len(set(hs.values()))==1
        verdict="INVARIANT" if bit else ("INVARIANT_WITHIN_FLOAT_TOL" if shape_ok and maxd<=tol else "NOT_INVARIANT")
        out[oid]={"arms":sorted(arms),"bitwise_equal":bit,"max_abs_diff_vs_alone":maxd if shape_ok else None,"shape_equal":shape_ok,"verdict":verdict,"hashes":hs}
    return out
