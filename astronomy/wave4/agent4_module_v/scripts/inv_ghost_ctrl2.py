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
import math
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
        per[o]=(h(rec),rec,list(sub.columns))
    return per, (list(df.columns) if df is not None else None)
def same(x,y):
    if isinstance(x,float) and isinstance(y,float):
        if math.isnan(x) and math.isnan(y): return True,0.0
        if math.isnan(x) or math.isnan(y): return False,float("inf")
        return x==y,abs(x-y)
    return x==y,(0.0 if x==y else float("inf"))
res={}
plan=[("alone_repeat1",["170609056634372829"]),("alone_repeat1",["170609056634373061"]),("batch",["170609056633849114","170609056634372829"]),
      ("batch",["170609056634373061","170609056633849114"]),("alone_repeat2",["170609056634372829"]),("alone_repeat2",["170609056634373061"])]
for arm,oids in plan:
    t=now(); per,cols=call(oids)
    for o in oids: res.setdefault(o,{})[arm+("" if arm!="batch" else "_with_"+[p for p in oids if p!=o][0])]=per[o]
    log("GHOST",arm+"_control2",oids,t,"ok",[per[o][0] if per[o] else None for o in oids]); print(arm,oids,"done",flush=True)
ver={}
for o,arms in res.items():
    if o=="170609056633849114": continue
    base=arms["alone_repeat1"]; rep={}
    for a,v in arms.items():
        if a=="alone_repeat1": continue
        diffcols=set(); maxd=0.0
        if len(v[1])!=len(base[1]): rep[a]={"hash_equal":v[0]==base[0],"n_rows":[len(base[1]),len(v[1])]}; continue
        for r1,r2 in zip(base[1],v[1]):
            for k in set(r1)|set(r2):
                eq,d=same(r1.get(k),r2.get(k))
                if not eq: diffcols.add(k); maxd=max(maxd,d)
        rep[a]={"hash_equal":v[0]==base[0],"differing_columns":sorted(diffcols),"max_abs_diff":maxd,"n_rows":len(v[1])}
    ver[o]=rep
json.dump(ver,open(VD/"data_cache/inv_ghost_control2.json","w"),indent=1,default=str); print(json.dumps(ver,indent=1,default=str))
