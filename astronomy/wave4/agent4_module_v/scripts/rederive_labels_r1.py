import sys,os,json,collections,csv,re
sys.path.insert(0,os.path.dirname(__file__))
import labels_lib_r1 as L
out={}
out["main"]=L.compute()
# which objects still invalid, per source
out["invalid_after_parse"]=[k for k,v in L.ev.items() if v.get("final")=="invalid_after_parse"]
out["E2_names_status"]={n:(L.ev.get(n) or {}).get("final") for n in sorted(L.E2NAMES)}
print(json.dumps(out,indent=0,default=str))
