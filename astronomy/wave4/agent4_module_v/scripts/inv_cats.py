import os, sys, types, json, pathlib
sys.dont_write_bytecode=True
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from inv_common import *
W3=pathlib.Path("/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave3/agent4_tool_recount")
sys.path.insert(0, str(W3/"code"/"fink-science_591e75ce"))
_pkg=types.ModuleType("actsnfink"); _pkg.__path__=[str(W3/"code"/"actsnfink_f424ab1f"/"actsnfink")]; sys.modules["actsnfink"]=_pkg
from fink_science.rubin.cats.processor import predict_nn
fn=predict_nn.func
A=["170609056632799366","170609056633848501","170609056634372105","170609056634372804","170609056634372829"]
alerts={o:load_alert(o) for o in A}
def call(oids):
    col=lambda k: pd.Series([np.array([r[k] for r in alerts[o]]) for o in oids])
    out=fn(col("r:midpointMjdTai"),col("r:psfFlux"),col("r:psfFluxErr"),col("r:band")).tolist()
    return [list(map(float,x)) for x in out]
res={o:{} for o in A}
plan=[("alone",[o]) for o in A]+[("batch",[A[0],A[1]]),("batch",[A[2],A[3]]),("batch",[A[4],A[0]]),("batch",[A[1],A[2]]),("batch",[A[3],A[4]])]
for arm,oids in plan:
    t=now()
    try:
        out=call(oids); hs=[h(x) for x in out]
        for o,x,hh in zip(oids,out,hs):
            key="alone" if arm=="alone" else "batch_with_"+[p for p in oids if p!=o][0]
            res[o][key]=(hh,x)
        log("CATS",arm,oids,t,"ok",hs)
    except Exception as e:
        log("CATS",arm,oids,t,"error",None,repr(e)[:300])
v=compare(res)
json.dump(v,open(VD/"data_cache/inv_cats_verdicts.json","w"),indent=1)
print(json.dumps({o:{k:x[k] for k in ("arms","bitwise_equal","max_abs_diff_vs_alone","verdict")} for o,x in v.items()},indent=1))
