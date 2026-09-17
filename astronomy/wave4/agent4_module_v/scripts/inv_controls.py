import sys,os,json,random
sys.path.insert(0,os.path.dirname(__file__))
from inv_common import compare,h,VD
rng=random.Random(20260917); X={f"a{i}":[rng.random() for _ in range(5)] for i in range(4)}
def run(fn):
    res={o:{} for o in X}
    for o in X: y=fn([X[o]])[0]; res[o]["alone"]=(h(y),y)
    for a,b in (("a0","a1"),("a2","a3"),("a0","a2"),("a1","a3")):
        ya,yb=fn([X[a],X[b]]); res[a]["batch_with_"+b]=(h(ya),ya); res[b]["batch_with_"+a]=(h(yb),yb)
    return compare(res)
per_element=lambda B:[[2*v+1 for v in x] for x in B]
batch_mean=lambda B:[[v-sum(sum(z) for z in B)/(5*len(B)) for v in x] for x in B]   # Fink-style batch dependence
tiny_float=lambda B:[[v*(1+ (1e-9 if len(B)>1 else 0)) for v in x] for x in B]
out={"must_not_fire_per_element":{o:r["verdict"] for o,r in run(per_element).items()},
     "must_fire_batch_mean":{o:r["verdict"] for o,r in run(batch_mean).items()},
     "within_float_tol_control":{o:r["verdict"] for o,r in run(tiny_float).items()}}
nan_batch=lambda B:[[ (float("nan") if (len(B)>1 and i==0) else v) for i,v in enumerate(x)] for x in B]
out["must_fire_nan_vs_value"]={o:r["verdict"] for o,r in run(nan_batch).items()}
out["armed"]=all(v=="NOT_INVARIANT" for v in out["must_fire_nan_vs_value"].values()) and all(v=="INVARIANT" for v in out["must_not_fire_per_element"].values()) and all(v=="NOT_INVARIANT" for v in out["must_fire_batch_mean"].values()) and all(v=="INVARIANT_WITHIN_FLOAT_TOL" for v in out["within_float_tol_control"].values())
json.dump(out,open(VD/"data_cache/inv_controls.json","w"),indent=1); print(json.dumps(out,indent=1))
