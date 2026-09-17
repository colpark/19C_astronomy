import sys, os, csv, math
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(__file__)); from common import *
from scipy.stats import norm
PS=f"{REPO}/astronomy/wave2/agent4_instrument/paired_scores.csv"
ZDOC=1.9600+0.8416; ZEX=norm.ppf(0.975)+norm.ppf(0.80)
rows=list(csv.DictReader(open(PS)))
def stat(sub):
    d=[F(r["prec_classical"])-F(r["prec_instrument"]) for r in sub]; n=len(d)
    m=sum(d,F(0))/n; ss=sum(((x-m)**2 for x in d),F(0)); var=ss/(n-1)
    sd=math.sqrt(var)
    out={"n":n,"mean_paired_difference_a_minus_b":float(m),"sigma_d":sd,"var_exact_fraction":f"{var.numerator}/{var.denominator}"}
    for zn,z in (("doc_z",ZDOC),("exact_z",ZEX)):
        out[f"mde_{zn}"]=z*sd/math.sqrt(n)
        for dl in (0.018,0.05):
            out[f"n_min_{zn}_delta_{dl}"]=math.ceil(z*z*float(var)/(dl*dl))
            out[f"n_min_unceiled_{zn}_delta_{dl}"]=z*z*float(var)/(dl*dl)
    return out
def premise(sub):
    import random
    rng=random.Random(20260917)
    b=[r["prec_instrument"] for r in sub]; rng.shuffle(b)
    sh=[dict(r,prec_instrument=x) for r,x in zip(sub,b)]
    s0=stat(sub); s1=stat(sh)
    return {"sigma_d_orig":s0["sigma_d"],"sigma_d_pairing_shuffled":s1["sigma_d"],"changed":abs(s0["sigma_d"]-s1["sigma_d"])>1e-12 or s0["sigma_d"]==0}
res={}
spec={"P01":("E1","N",None),"P02":("E1","N","True"),"P03":("E1","N","False"),"P04":("E1","R",None),
      "P05":("E3","N",None),"P06":("E3","N","True"),"P07":("E3","N","False"),"P08":("E3","R",None)}
for tid,(E,it,kb) in spec.items():
    sub=[r for r in rows if r["epoch"]==E and r["item_type"]==it and (kb is None or r["k_binding"]==kb)]
    s=stat(sub); s["premise_pairing_shuffle"]=premise(sub)
    # cross-check against the per-run paired file
    pf=f"{REPO}/astronomy/wave2/agent4_instrument/data_cache/power/paired_{E}_{it}.csv"
    sub2=[r for r in csv.DictReader(open(pf)) if (kb is None or r["k_binding"]==kb)]
    s["crosscheck_per_run_file_sigma_d"]=stat(sub2)["sigma_d"]; s["crosscheck_per_run_file_sha256"]=sha(pf)
    # N_min consistency: N_min*delta^2 >= z^2 sd^2 > (N_min-1)*delta^2
    ok=all(s[f"n_min_doc_z_delta_{dl}"]*dl*dl>=ZDOC**2*s["sigma_d"]**2*(1-1e-12) and (s[f"n_min_doc_z_delta_{dl}"]-1)*dl*dl<ZDOC**2*s["sigma_d"]**2 for dl in (0.018,0.05)) if s["sigma_d"]>0 else True
    s["premise_nmin_consistent_with_mde"]=ok
    # MDE at N_min should be <= delta
    s["premise_mde_at_nmin_le_delta"]={str(dl):(ZDOC*s["sigma_d"]/math.sqrt(s[f"n_min_doc_z_delta_{dl}"]) if s["sigma_d"]>0 else 0) for dl in (0.018,0.05)}
    res[tid]=s
    seal(tid,s,"own exact-rational paired sd (ddof=1) over paired_scores.csv rows filtered by epoch/item_type/k_binding; MDE=z*sd/sqrt(n); N_min=ceil(z^2 var/delta^2); z doc=1.96+0.8416 (power.py documented constants) and exact scipy z reported",
         {"paired_scores.csv":sha(PS)})
print(json.dumps(res,indent=1))
