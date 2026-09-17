import sys, glob, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__)); from common import *
from scipy.spatial import cKDTree
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
OUT=f"{REPO}/astronomy/wave3/agent1_cohort_finish/out"
T0=61222.000428; ARC=np.deg2rad(1/3600); CH=2*np.sin(ARC/2)
def load(d):
    fs=sorted(glob.glob(f"{OUT}/{d}/*.csv")); parts=[pd.read_csv(f,dtype={"oid":str}) for f in fs]
    df=pd.concat(parts,ignore_index=True)
    for c in ["meanra","meandec","firstmjd","lastmjd","n_det","n_forced"]: df[c]=pd.to_numeric(df[c],errors="coerce")
    df["src"]=d; return df, len(fs)
def run(c3,p60,c5, tag="main"):
    raw=pd.concat([c3,p60],ignore_index=True)
    # unprocessable
    bad=raw["oid"].isna()|raw["meanra"].isna()|raw["meandec"].isna()|raw["firstmjd"].isna()|(raw["meandec"].abs()>90)
    U=int(bad.sum())
    good=raw[~bad]
    # X1 dedupe on oid; record conflicting duplicates
    dup_rows=int(good.duplicated("oid").sum())
    conflicts=int((good.groupby("oid")[["meanra","meandec","firstmjd","lastmjd","n_det"]].nunique()>1).any(axis=1).sum())
    u=good.drop_duplicates("oid",keep="first").reset_index(drop=True)
    ra=np.deg2rad(u.meanra.values); dec=np.deg2rad(u.meandec.values)
    xyz=np.c_[np.cos(dec)*np.cos(ra),np.cos(dec)*np.sin(ra),np.sin(dec)]
    pairs=cKDTree(xyz).query_pairs(CH,output_type="ndarray")
    fm=u.firstmjd.values
    dt=np.abs(fm[pairs[:,0]]-fm[pairs[:,1]]) if len(pairs) else np.array([])
    x2=pairs[dt<=60]; x3=int((dt>60).sum())
    n=len(u); g=coo_matrix((np.ones(len(x2)),(x2[:,0],x2[:,1])),shape=(n,n))
    ncomp,lab=connected_components(g,directed=False)
    u["comp"]=lab
    cmin=u.groupby("comp").firstmjd.transform("min")
    post=u.firstmjd>=T0
    incoh=cmin>=T0
    O_A=int(post.sum())
    O_merged=int(u.loc[incoh,"comp"].nunique())
    s1_merge=int((post & ~incoh).sum())
    # S1-direct: pre-T0 oids with lastmjd>=T0, from p60 (firstmjd in [T0-60,T0)) and c5 (older)
    pre=u[(u.firstmjd<T0)&(u.lastmjd>=T0)]
    c5g=c5[~(c5["oid"].isna()|c5["firstmjd"].isna())].drop_duplicates("oid")
    c5s=c5g[(c5g.firstmjd<T0)&(c5g.lastmjd>=T0)]
    c5_viol=int((c5g.lastmjd<T0).sum())
    direct=set(pre.oid)|set(c5s.oid)
    s1_direct=len(direct)
    coh=u[incoh]
    share_oid_all_post=float((u.loc[post,"n_det"]==1).sum()/O_A)
    share_oid_in_merged=float((coh.n_det==1).sum()/len(coh))
    comp_ndet=coh.groupby("comp").n_det.sum()
    share_merged=float((comp_ndet==1).sum()/len(comp_ndet))
    return dict(tag=tag,rows_c3=len(c3),rows_p60=len(p60),rows_c5=len(c5),unprocessable_U=U,duplicate_oid_rows=dup_rows,
        oids_with_conflicting_duplicate_values=conflicts,distinct_oids_union=n,pairs_le_1arcsec=int(len(pairs)),
        x2_edges=int(len(x2)),x3_same_position_distinct=x3,O_A_distinct_post_T0_oids=O_A,O_merged=O_merged,
        S1_direct=s1_direct,S1_direct_from_p60=len(set(pre.oid)),S1_direct_from_c5=len(set(c5s.oid)),c5_rows_violating_lastmjd_filter=c5_viol,
        S1_merge=s1_merge,S1_total=s1_direct+s1_merge,
        one_det_share_over_all_post_T0_oids=share_oid_all_post,one_det_share_over_oids_in_merged_cohort=share_oid_in_merged,
        one_det_share_merged_level_component_ndet_summed=share_merged,n_det1_post_T0_oids=int((u.loc[post,"n_det"]==1).sum()))
if __name__=="__main__":
    c3,n3=load("w3_c3_slices"); p60,n6=load("w3_p60_slices"); c5,n5=load("w3_c5_slices")
    r=run(c3,p60,c5); r["slice_files"]=[n3,n6,n5]; print(json.dumps(r,indent=1))
    json.dump(r,open(f"{VD}/data_cache/cohort_main.json","w"),indent=1)
    # premise checks (perturbations)
    prem={}
    fs=sorted(glob.glob(f"{OUT}/w3_c3_slices/*.csv")); big=max(fs,key=os.path.getsize)
    drop=c3[~c3.index.isin(pd.read_csv(big,dtype={'oid':str}).pipe(lambda d: c3.index[c3.oid.isin(d.oid)]))]
    r2=run(drop,p60,c5,"drop_largest_c3_slice"); prem["drop_largest_slice"]={"slice":os.path.basename(big),"O_merged":r2["O_merged"],"O_A":r2["O_A_distinct_post_T0_oids"]}
    r3=run(pd.concat([c3,c3.iloc[:5000]]),p60,c5,"dup5000"); prem["duplicate_5000_rows"]={"O_merged":r3["O_merged"],"O_A":r3["O_A_distinct_post_T0_oids"]}
    # plant pre-T0 twin 0.5 arcsec from 100 cohort oids with lastmjd>=T0
    tw=c3[c3.firstmjd>=T0].drop_duplicates("oid").iloc[:100].copy(); tw["oid"]="TWIN"+tw["oid"]; tw["meandec"]=tw["meandec"]+0.5/3600; tw["firstmjd"]=T0-1; tw["lastmjd"]=T0-0.5
    r4=run(c3,pd.concat([p60,tw]),c5,"twins"); prem["plant_100_preT0_twins_0p5arcsec"]={"O_merged":r4["O_merged"],"S1_merge":r4["S1_merge"],"S1_direct":r4["S1_direct"]}
    json.dump(prem,open(f"{VD}/data_cache/cohort_premise.json","w"),indent=1); print(json.dumps(prem,indent=1))
