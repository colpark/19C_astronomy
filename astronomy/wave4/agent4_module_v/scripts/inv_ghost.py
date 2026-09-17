import os, sys, json, pathlib, shutil
sys.dont_write_bytecode=True
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from inv_common import *
W3=pathlib.Path("/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave3/agent4_tool_recount")
CODE=W3/"code"
sys.path.insert(0, str(CODE/"uiucsn_astro_ghost"))
gdir=VD/"data_cache"/"ghost"; gdir.mkdir(parents=True,exist_ok=True)
os.environ["GHOST_PATH"]=str(gdir)
import hashlib
mlp=CODE/"uiucsn_astro_ghost/astro_ghost/MLP_lupton.hdf5"
assert hashlib.sha256(mlp.read_bytes()).hexdigest().startswith("13ac27c2")
from astro_ghost.ghostHelperFunctions import getGHOST, getTransientHosts
getGHOST(real=False, verbose=False, installpath=str(gdir), clobber=True)
from astropy.coordinates import SkyCoord
import astropy.units as u
A=["170609056633849114","170609056634372829","170609056634373061"]
alerts={o:load_alert(o) for o in A}
k=[0]
def call(oids):
    k[0]+=1; wd=gdir/f"inv_{k[0]}"; wd.mkdir(exist_ok=True); cwd=os.getcwd(); os.chdir(wd)
    try:
        df=getTransientHosts(transientName=[f"inv_{o}" for o in oids], transientCoord=[SkyCoord(alerts[o][-1]["r:ra"]*u.deg, alerts[o][-1]["r:dec"]*u.deg) for o in oids],
                             snClass=[""]*len(oids), verbose=False, GLADE=False, savepath=str(wd)+"/", GHOSTpath=str(gdir), redo_search=False)
    finally: os.chdir(cwd)
    per={}
    namecol=[c for c in df.columns if c.lower() in ("transientname","transient_name","name")] if df is not None else []
    for o in oids:
        if df is None or not namecol: per[o]=None; continue
        sub=df[df[namecol[0]]==f"inv_{o}"].drop(columns=namecol).reset_index(drop=True)
        rec=sub.to_dict(orient="records")
        flat=[]
        for r in rec:
            for kk in sorted(r): flat.append(r[kk])
        per[o]=(h(rec),flat,list(sub.columns))
    return per, (list(df.columns) if df is not None else None)
res={o:{} for o in A}; cols=None
plan=[("alone",[o]) for o in A]+[("batch",[A[0],A[1]]),("batch",[A[1],A[2]]),("batch",[A[2],A[0]])]
for arm,oids in plan:
    t=now()
    try:
        per,cols=call(oids)
        for o in oids:
            key="alone" if arm=="alone" else "batch_with_"+[p for p in oids if p!=o][0]
            if per[o] is not None: res[o][key]=(per[o][0],per[o][1])
        log("GHOST",arm,oids,t,"ok",[per[o][0] if per[o] else None for o in oids])
    except Exception as e:
        log("GHOST",arm,oids,t,"error",None,repr(e)[:300])
    print(arm,oids,"done",flush=True)
v=compare({o:a for o,a in res.items() if "alone" in a})
v["_columns"]=cols
json.dump(v,open(VD/"data_cache/inv_ghost_verdicts.json","w"),indent=1,default=str)
print(json.dumps({o:({kk:x[kk] for kk in ("arms","bitwise_equal","max_abs_diff_vs_alone","verdict")} if isinstance(x,dict) else x) for o,x in v.items()},indent=1,default=str))
