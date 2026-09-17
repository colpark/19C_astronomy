import sys, os, re, html, csv, math, datetime as dt
sys.path.insert(0, os.path.dirname(__file__)); from common import *
import numpy as np
from scipy.special import logsumexp
A=f"{REPO}/astronomy"
CAP={"2024-12-08T23:13:31":("wayback_bts_explorer_20241208231331.html","96b9fe72714a7e3af4e9f2cc8e22b4b60b7a5078dd488e0c9b06c05bd6d2fc43"),
     "2025-08-10T06:50:56":("wayback_bts_explorer_20250810065056.html","ec0152effff8b3e4dfb538566ad998ab5e4dd33749c229c9f7518cefcbb373d6"),
     "2026-07-25T03:35:57":("wayback_bts_explorer_20260725033557.html","9e1ad100af9e0c14d524cc12640542cee226f123e76996fe9714f8341b230748")}
RAW=f"{A}/data/raw/ztf_bts_all_2026-09-16.csv"; assert sha(RAW)=="61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
BINS=[(0,30),(30,60),(60,120),(120,240),(240,365),(365,math.inf)]
def jd(t): return (t-dt.datetime(2000,1,1,12,tzinfo=dt.timezone.utc)).total_seconds()/86400+2451545.0
def parse(fn,h):
    p=f"{A}/agent3_labels_exposure/sources/{fn}"; assert sha(p)==h
    s=open(p,encoding="utf-8",errors="replace").read(); out={}; dup=0
    for tr in re.findall(r"<tr\b.*?</tr>",s,flags=re.S):
        cells=[html.unescape(re.sub(r"<[^>]+>","",c)).replace("\xa0"," ").strip() for c in re.findall(r"<td\b.*?</td>",tr,flags=re.S)]
        if len(cells)<15 or not re.fullmatch(r"ZTF\d{2}[a-z]{7}",cells[0]): continue
        try: pk=float(cells[4])
        except: continue
        if cells[0] in out: dup+=1; continue
        out[cells[0]]=(pk,cells[11])
    return out,dup
def binof(a):
    for i,(lo,hi) in enumerate(BINS):
        if lo<=a<hi: return i
    return None
def pb_lower_tail(ps,x):
    # exact Poisson-binomial CDF Pr(X<=x) by log-space convolution
    lp=np.array([0.0]); 
    for p in ps:
        a=np.full(len(lp)+1,-np.inf)
        a[:-1]=lp+np.log1p(-p) if p<1 else -np.inf
        b=np.full(len(lp)+1,-np.inf); b[1:]=lp+(np.log(p) if p>0 else -np.inf)
        lp=np.logaddexp(a,b)
    return float(np.exp(logsumexp(lp[:x+1]))), float(logsumexp(lp[:x+1])/np.log(10)), float(np.exp(logsumexp(lp)))
caps={k:parse(*v) for k,v in CAP.items()}
def tdate(k): return dt.datetime.fromisoformat(k).replace(tzinfo=dt.timezone.utc)
def ref_curve(k, time_mode):
    obj,_=caps[k]; t=tdate(k) if time_mode=="timestamp" else tdate(k).replace(hour=0,minute=0,second=0)
    n=[0]*6; lab=[0]*6
    for z,(pk,ty) in obj.items():
        age=jd(t)-(pk+2458000)
        if age<0: continue
        b=binof(age); n[b]+=1; lab[b]+= ty!="-"
    return [lab[i]/n[i] if n[i] else None for i in range(6)], n, lab
y2026=(jd(dt.datetime(2026,1,1,tzinfo=dt.timezone.utc))-2458000, jd(dt.datetime(2027,1,1,tzinfo=dt.timezone.utc))-2458000)
def observed(which,time_mode):
    if which=="capture":
        obj,_=caps["2026-07-25T03:35:57"]; t=tdate("2026-07-25T03:35:57")
        if time_mode!="timestamp": t=t.replace(hour=0,minute=0,second=0)
        items=[(pk,ty) for z,(pk,ty) in obj.items()]
    else:
        t=dt.datetime(2026,9,16,tzinfo=dt.timezone.utc)
        rows=list(csv.DictReader(open(RAW))); items=[]
        seen=set()
        for r in rows:
            try: pk=float(r["peakt"])
            except: continue
            items.append((pk,r["type"].strip()))
    return [(jd(t)-(pk+2458000), ty!="-") for pk,ty in items if y2026[0]<=pk<y2026[1]]
res={}
for mode in ("timestamp","date"):
    for which in ("capture","file"):
        obs=observed(which,mode)
        for ref in ("2024-12-08T23:13:31","2025-08-10T06:50:56"):
            f,n,lab=ref_curve(ref,mode)
            ps=[];X=0;excl=0;neg=0
            for age,l in obs:
                b=binof(age)
                if b is None: neg+=1; continue
                if f[b] is None: excl+=1; continue
                ps.append(f[b]); X+=l
            P,log10P,tot=pb_lower_tail(ps,X)
            res[f"{mode}|{which}|{ref}"]={"n_included":len(ps),"excluded_no_reference":excl,"excluded_negative_age":neg,"observed_labelled":X,
                "expected":float(sum(ps)),"P_lower_tail":P,"log10_P":log10P,"pmf_total_check":tot}
            if mode=="timestamp":
                Pexp,_,_=pb_lower_tail(ps,int(round(sum(ps))))
                res[f"{mode}|{which}|{ref}"]["premise_P_at_X_equal_expectation"]=Pexp
                # binomial cross-check with equal p
                from scipy.stats import binom
                pbar=0.37; q,_,_=pb_lower_tail([pbar]*200,60); res[f"{mode}|{which}|{ref}"]["premise_dp_vs_scipy_binom"]=[q,float(binom.cdf(60,200,pbar))]
sizes={k:{"rows":len(v[0]),"duplicate_rows":v[1]} for k,v in caps.items()}
mp={("capture","2024-12-08T23:13:31"):"Q01",("capture","2025-08-10T06:50:56"):"Q02",("file","2024-12-08T23:13:31"):"Q03",("file","2025-08-10T06:50:56"):"Q04"}
for (w,r),tid in mp.items():
    d=dict(res[f"timestamp|{w}|{r}"]); d["sensitivity_age_from_date_midnight"]=res[f"date|{w}|{r}"]; d["capture_sizes"]=sizes
    ok=all(res[f"timestamp|{ww}|{rr}"]["P_lower_tail"]<0.05 for ww in ("capture","file") for rr in ("2024-12-08T23:13:31","2025-08-10T06:50:56"))
    d["ruling_derived"]="POLICY" if ok else "not POLICY"
    seal(tid,d,"own regex/html parse of explorer captures (cells: ZTFID..type at index 11), age=capture timestamp JD - (peakt+2458000), bins bands §9, f_C over age>=0, exact log-space Poisson-binomial CDF",
         {"raw":sha(RAW),**{k:v[1] for k,v in CAP.items()}})
print(json.dumps(res,indent=0)); print(sizes)
