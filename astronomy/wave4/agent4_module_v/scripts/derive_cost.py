import sys, os, csv, math
sys.path.insert(0, os.path.dirname(__file__)); from common import *
A=f"{REPO}/astronomy"; Z=1.96+0.8416
PB=f"{A}/agent5_resolution_replay/planning_mde_bracket.csv"; PB3=f"{A}/wave3/agent1_cohort_finish/planning_mde_bracket_w3.csv"
assert sha(PB)=="c00718b7440664c6c41c90d93645d5fb68cb397414a7822c29897fe28031ad43"
def nmin(s,dl): return math.ceil(Z*Z*s*s/(dl*dl))
res={}
for path in (PB,PB3):
    rows=[r for r in csv.DictReader(open(path)) if r["family"]=="B"]
    for dl in (0.018,0.05):
        real=[nmin(float(r["sigma_d_realised_by_power_py"]),dl) for r in rows]
        theo=[nmin(math.sqrt(float(r["sigma_d_basis"].split("=")[1])),dl) for r in rows]
        res[f"{os.path.basename(path)}|delta={dl}"]={"n_rows":len(rows),"realised_sigma_lo_hi":[min(real),max(real)],"theoretical_sqrt_q_lo_hi":[min(theo),max(theo)]}
# premise: perturb one sigma by 1%
rows=[r for r in csv.DictReader(open(PB)) if r["family"]=="B"]
pert=[nmin(float(r["sigma_d_realised_by_power_py"])*(1.01 if i==len(rows)-1 else 1),0.018) for i,r in enumerate(rows)]
prem={"perturb_last_row_sigma_x1.01_hi_0.018":max(pert)}
seal("N01",{k:v for k,v in res.items() if "0.018" in k},"own N_min=ceil((1.96+0.8416)^2 sigma^2/delta^2) over the 16 family-B rows; realised sigma column (what power.py saw, 6 dp) and theoretical sqrt(q)",{"bracket":sha(PB),"bracket_w3":sha(PB3)},{"premise":prem})
seal("N02",{k:v for k,v in res.items() if "0.05" in k},"as N01 at delta 0.05",{"bracket":sha(PB),"bracket_w3":sha(PB3)},{"premise":prem})
# truth cost table
TC=f"{A}/wave3/agent2_measured_labels/truth_cost_table.csv"
tr=list(csv.DictReader(open(TC)))
def price(r):
    N=int(r["N"]); L=int(r["L"]); p=float(r["purity_p"]); s=float(r["success_s"]); c=float(r["capacity_c"]); Av=float(r["A_reachable_arrivals_per_night_cp95_lo"])
    Nn=max(0,N-L); S=math.ceil(Nn/(p*s)-1e-12) if Nn else 0
    # guard float: exact rational ceil
    from fractions import Fraction as F
    S=math.ceil(F(Nn)/(F(r["purity_p"])*F(r["success_s"]))) if Nn else 0
    H=0.5*S; W=S-math.ceil(F(Nn)/F(r["success_s"])) if Nn else 0
    rate=min(F(r["capacity_c"]),F(r["A_reachable_arrivals_per_night_cp95_lo"]))
    nights=math.ceil(F(S)/rate) if S else 0
    return dict(N_need=Nn,S=S,H=H,W=W,nights=nights,binding="arrivals" if F(r["A_reachable_arrivals_per_night_cp95_lo"])<F(r["capacity_c"]) else "capacity")
mism=[]; ranges={}
for i,r in enumerate(tr):
    q=price(r)
    got=dict(N_need=int(r["N_need"]),S=int(r["spectra_S"]),H=float(r["P60_hours_H"]),W=int(r["wrong_routine_commitments_W"]),nights=int(r["rubin_on_sky_nights"]),binding=r["binding"])
    if q!=got: mism.append({"row":i,"derived":q,"input_row_values":got})
    if r["L"]=="0" or r["L_case"].startswith("L=0"):
        k=f"delta_{r['delta']}_N_{r['N']}"
        R=ranges.setdefault(k,{"spectra":[10**9,0],"nights":[10**9,0],"hours":[1e18,0],"wrong":[10**9,0]})
        for key,v in (("spectra",q["S"]),("nights",q["nights"]),("hours",q["H"]),("wrong",q["W"])):
            R[key]=[min(R[key][0],v),max(R[key][1],v)]
# premise: perturb purity of row 0
r0=dict(tr[0]); r0["purity_p"]="0.5"; prem2={"row0_S_with_p=0.5":price(r0)["S"],"row0_S_orig":price(tr[0])["S"]}
# note: R01 compares rows against the table's own derived columns; those columns are the claim, so the mismatch count is sealed as derived and the claim is 'all rows follow the formula' (0 mismatches)
seal("R01",{"n_rows":len(tr),"rows_mismatching_formula":len(mism),"first_mismatches":mism[:5],"L_values_seen":sorted({r["L"] for r in tr})},
     "own rational-arithmetic reimplementation of census_protocol_FROZEN §10 over input columns; compared row-wise to the output columns",{"truth_cost_table.csv":sha(TC),"census_protocol":sha(f"{A}/wave3/agent2_measured_labels/census_protocol_FROZEN.md")},{"premise":prem2})
for tid,keys in (("R02",["delta_0.05_N_63"]),("R03",["delta_0.018_N_485"]),("R04",["delta_0.05_N_1666","delta_0.018_N_12855"])):
    seal(tid,{k:ranges[k] for k in keys},"min/max over the L=0 grid rows of own recomputed S and nights",{"truth_cost_table.csv":sha(TC)})
print(json.dumps(res,indent=0)); print(len(mism)); print(json.dumps(ranges,indent=0)); print(prem,prem2)
