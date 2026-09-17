import sys, os, json, math, csv
sys.path.insert(0, os.path.dirname(__file__)); from common import *
import numpy as np, pandas as pd
out={}
# N01/N02: perturb the row that gives the max
Z=1.96+0.8416
rows=[r for r in csv.DictReader(open(f"{REPO}/astronomy/agent5_resolution_replay/planning_mde_bracket.csv")) if r["family"]=="B"]
sig=[float(r["sigma_d_realised_by_power_py"]) for r in rows]; i=int(np.argmax(sig))
f=lambda s,d: math.ceil(Z*Z*s*s/(d*d))
out["N_perturb_max_row_x1.01"]={"row":i,"hi_0.018_before":max(f(s,0.018) for s in sig),"hi_0.018_after":max(f(s*(1.01 if j==i else 1),0.018) for j,s in enumerate(sig)),
   "planted_486_fires": 486!=min(f(s,0.018) for s in sig)}
# O01 planted reversal
def order_ok(t_brief,t_power,t_step1): return t_brief<t_power<t_step1
d=json.load(open(f"{VD}/sealed/V-O01.json"))["derived"]
import datetime as dt
tb=dt.datetime.fromisoformat(d["wave3_brief_mtime_utc"]); tp=dt.datetime.fromisoformat(d["earliest_wave2_power_output_mtime_utc"]); ts=dt.datetime.fromisoformat(d["w3a4_step1_log_utc"])
out["O01_planted"]={"real":order_ok(tb,tp,ts),"swap_brief_power":order_ok(tp,tb,ts),"swap_power_step1":order_ok(tb,ts,tp),"fires_on_planted":not order_ok(tp,tb,ts) and not order_ok(tb,ts,tp)}
# K01: move one unit from a <=8 night into an 8-candidate night
from derive_auc_nights_lib import pool_E1
pool=pool_E1(); cnt=pool.groupby("decision_night").size()
n8=cnt[cnt==8].index[0]; donor=cnt[(cnt<=7)].index[0]
p2=pool.copy(); idx=p2.index[p2.decision_night==donor][0]; p2.loc[idx,"decision_night"]=n8
c2=p2.groupby("decision_night").size()
out["K01_move_unit_into_8_night"]={"gt8_before":int((cnt>8).sum()),"gt8_after":int((c2>8).sum()),"le8_after":int((c2<=8).sum()),"nights_after":int(len(c2))}
# C03/C04 perturbations
import derive_cohort as DC
c3,_=DC.load("w3_c3_slices"); p60,_=DC.load("w3_p60_slices"); c5,_=DC.load("w3_c5_slices")
base=json.load(open(f"{VD}/data_cache/cohort_main.json"))
k=p60.index[(p60.firstmjd<DC.T0)&(p60.lastmjd>=DC.T0)][0]; p60b=p60.copy(); p60b.loc[k,"lastmjd"]=DC.T0-0.01
r=DC.run(c3,p60b,c5,"lastmjd_below"); out["C03_set_one_straddler_lastmjd_below_T0"]={"S1_before":base["S1_total"],"S1_after":r["S1_total"]}
ks=c3.index[(c3.firstmjd>=DC.T0)&(c3.n_det==1)][:1000]; c3b=c3.copy(); c3b.loc[ks,"n_det"]=2
r=DC.run(c3b,p60,c5,"ndet_flip"); out["C04_flip_1000_ndet"]={"share_before":base["one_det_share_over_all_post_T0_oids"],"share_after":r["one_det_share_over_all_post_T0_oids"],
   "expected_drop":1000/base["O_A_distinct_post_T0_oids"],"observed_drop":base["one_det_share_over_all_post_T0_oids"]-r["one_det_share_over_all_post_T0_oids"]}
json.dump(out,open(f"{VD}/data_cache/premise_extra.json","w"),indent=1,default=str); print(json.dumps(out,indent=1,default=str))
