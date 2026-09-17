import sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__)); from common import *
import numpy as np, pandas as pd
from scipy.stats import rankdata
W=f"{REPO}/astronomy/wave2/agent4_instrument"
# 1. manifest check
man=f"{W}/compositions/MANIFEST.sha256"; bad=[]
for line in open(man):
    if line.startswith("#") or not line.strip(): continue
    h,p=line.split(None,1); p=p.strip()
    if sha(f"{W}/{p}")!=h: bad.append(p)
print("manifest mismatches:",bad)
corpus=f"{REPO}/astronomy/agent1_supply_corpus/corpus.csv"
assert sha(corpus)=="b059acf0656ed79fc743944b560aa3fd358096963067d96e144850403c3d8442"
c=pd.read_csv(corpus,dtype=str)
POSA=("SN ","SLSN","TDE","nova","LRN","LBV","ILRT","Ca-rich","Other","other")
def cls(t):
    t=str(t)
    if t.startswith(POSA): return "posB" if not t.startswith("SN Ia") else "posA_Ia"
    if t.startswith(("CV","AGN")): return "neg"
    return "none"
c["cls"]=c["type"].map(cls)
g=c.groupby("object_cluster_1arcsec")["cls"].agg(lambda s: sorted(set(s)))
conflict={k:v for k,v in g.items() if len(v)>1}
def unit_cls(v):
    return v[0] if len(v)==1 else "CONFLICT:"+"|".join(v)
uc=g.map(unit_cls)
print("units",len(uc),"conflicting units",len(conflict), list(conflict.items())[:5])
def load(E,C):
    p=pd.read_csv(f"{W}/compositions/predictions/pred_{E}_{C}.csv")
    p["cls"]=p["unit"].astype(str).map(uc)
    return p
def auc(y,s):
    r=rankdata(s); n1=y.sum(); n0=len(y)-n1
    return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
out={}
for E in ("E1","E3"):
    p=load(E,"C"); pool=p[p.cls.isin(["posB","posA_Ia","neg"])]
    other=p[~p.cls.isin(["posB","posA_Ia","neg","none"])]
    cnt=pool.groupby("decision_night").size()
    out[f"nights_{E}"]={"scored_pool_units":int(len(pool)),"units_conflicting_class":int(len(other)),"nights_total":int(len(cnt)),
        "nights_gt8":int((cnt>8).sum()),"nights_le8":int((cnt<=8).sum())}
    # premise: plant a wrong count
    for C,tid in (("C-1","A01" if E=="E1" else "A03"),("C","A02" if E=="E1" else "A04")):
        p=load(E,C); pool=p[p.cls.isin(["posB","posA_Ia","neg"])].reset_index(drop=True)
        y=(pool.cls=="posB").astype(int).values; s=pool.score.values
        a=auc(y,s)
        rng=np.random.default_rng(0); n=len(y); bs=[]
        for _ in range(1000):
            idx=rng.integers(0,n,n); yy=y[idx]
            if yy.min()==yy.max(): continue
            bs.append(auc(yy,s[idx]))
        ci=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))]
        # alt bootstrap RNG (legacy RandomState(0)) as sensitivity
        rs=np.random.RandomState(0); bs2=[]
        for _ in range(1000):
            idx=rs.randint(0,n,n); yy=y[idx]
            if yy.min()==yy.max(): continue
            bs2.append(auc(yy,s[idx]))
        ci2=[float(np.percentile(bs2,2.5)),float(np.percentile(bs2,97.5))]
        # premise checks
        yp=np.random.default_rng(1).permutation(y); a_perm=auc(yp,s); a_neg=auc(y,-s)
        pp=load(E,C+"__perm"); pp=pp[pp.cls.isin(["posB","posA_Ia","neg"])]
        a_prodperm_file=auc((pp.cls=="posB").astype(int).values,pp.score.values)
        # sklearn cross-check if present
        try:
            from sklearn.metrics import roc_auc_score; a_sk=float(roc_auc_score(y,s))
        except Exception as e: a_sk=f"sklearn unavailable: {e}"
        d={"epoch":E,"composition":C,"n_scored":int(n),"n_posB":int(y.sum()),"auc_posB":float(a),"ci95_percentile_default_rng0":ci,
           "ci95_percentile_RandomState0_sensitivity":ci2,"bootstrap_B_used":len(bs),
           "premise":{"label_permutation_seed1_auc":float(a_perm),"negated_scores_auc":float(a_neg),"one_minus_auc":float(1-a),
                      "producer_perm_prediction_file_auc_under_our_labels":float(a_prodperm_file),"sklearn_crosscheck":a_sk}}
        out[tid]=d
        seal(tid,d,"own midrank Mann-Whitney AUC over scored pool (posA or neg by corpus type map, unit=object_cluster_1arcsec), posB positive; 1000 object-bootstrap percentile CI seeded 0",
             {"pred":sha(f"{W}/compositions/predictions/pred_{E}_{C}.csv"),"corpus":sha(corpus),"manifest_mismatches":bad})
n1=out["nights_E1"]; n3=out["nights_E3"]
seal("K01",{"E1_nights_gt8":n1["nights_gt8"],"E1_nights_total":n1["nights_total"],"E3":n3},"distinct decision_night over scored-pool units in pred_E1_C.csv; count >8 units",{"pred_E1_C":sha(f"{W}/compositions/predictions/pred_E1_C.csv"),"corpus":sha(corpus)},
     {"premise":{"plant_60_detected": 60!=n1["nights_gt8"]}})
seal("K02",{"E1_nights_le8":n1["nights_le8"],"sum_check":n1["nights_le8"]+n1["nights_gt8"]==n1["nights_total"],"E3":n3},"as K01, count <=8",{"pred_E1_C":sha(f"{W}/compositions/predictions/pred_E1_C.csv")},
     {"premise":{"plant_517_detected": 517!=n1["nights_le8"]}})
print(json.dumps(out,indent=1))
