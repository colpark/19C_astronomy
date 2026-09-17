import os, sys, types, json, pathlib
sys.dont_write_bytecode=True
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from inv_common import *
exec(open(pathlib.Path(__file__).resolve().parent/"inv_cats.py").read().split("res={o:{} for o in A}")[0])
B=[A[1],A[3]]
outs={}
for rep in (1,2):
    for o in B:
        t=now(); x=call([o])[0]; log("CATS",f"alone_repeat{rep}",[o],t,"ok",[h(x)]); outs.setdefault(o,{})[f"alone{rep}"]=x
t=now(); xb=call(B); log("CATS","batch_control",B,t,"ok",[h(v) for v in xb])
for o,x in zip(B,xb): outs[o]["batch"]=x
ver={}
for o,d in outs.items():
    a1,a2,b=np.array(d["alone1"]),np.array(d["alone2"]),np.array(d["batch"])
    ver[o]={"repeat_alone_bitwise_equal":bool(np.array_equal(a1,a2)),"batch_vs_alone_bitwise_equal":bool(np.array_equal(a1,b)),
            "batch_vs_alone_max_abs":float(np.max(np.abs(a1-b))),"argmax_equal":bool(np.argmax(a1)==np.argmax(b)),"n_outputs":int(a1.size)}
json.dump(ver,open(VD/"data_cache/inv_cats_control.json","w"),indent=1); print(json.dumps(ver,indent=1))
