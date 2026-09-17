import sys, os, json, math, datetime as dt
sys.path.insert(0, os.path.dirname(__file__)); from common import *
A=f"{REPO}/astronomy"; J=lambda p: json.load(open(f"{A}/{p}"))
T={t["id"]:t for t in json.load(open(f"{VD}/V_TARGETS.json"))["targets"]}
S=lambda i: json.load(open(f"{VD}/sealed/V-{i}.json"))
PX=json.load(open(f"{VD}/data_cache/premise_extra.json"))
def decimals(x):
    r=repr(x)
    if "e" in r or "." not in r: return None
    return len(r.split(".")[1])
def cmp_num(field, claimed, derived, kind):
    """kind: int | float_stat | share | auc | ci | log10p | ts"""
    rec={"field":field,"claimed":claimed,"derived":derived}
    if claimed is None or derived is None:
        rec.update(verdict="UNVERIFIABLE",abs_diff=None,rel_diff=None); return rec
    if kind=="bool":
        rec.update(abs_diff=None,rel_diff=None,tol="exact",verdict="MATCH" if claimed==derived else "DISCREPANCY"); return rec
    if kind=="ts":
        c=dt.datetime.fromisoformat(claimed.replace("Z","+00:00")); d=dt.datetime.fromisoformat(derived.replace("Z","+00:00"))
        ad=abs((c-d).total_seconds()); rec.update(abs_diff_s=ad,tol="abs 1 s",verdict="MATCH" if ad==0 else ("MATCH_WITHIN_TOL" if ad<=1 else "DISCREPANCY")); return rec
    if kind=="log10p":
        lc,ld=math.log10(claimed),math.log10(derived); ad=abs(lc-ld)
        rec.update(log10_claimed=lc,log10_derived=ld,abs_diff_log10=ad,rel_diff=abs(claimed-derived)/claimed,tol="abs 0.05 in log10",
                   verdict="MATCH" if ad<=1e-9 else ("MATCH_WITHIN_TOL" if ad<=0.05 else "DISCREPANCY")); return rec
    ad=abs(claimed-derived); rd=ad/abs(claimed) if claimed else (0.0 if ad==0 else math.inf)
    rec.update(abs_diff=ad,rel_diff=rd)
    if kind=="int":
        rec.update(tol="exact",verdict="MATCH" if ad==0 else "DISCREPANCY"); return rec
    decl={"float_stat":(1e-9,1e-6),"share":(1e-9,0.0),"auc":(1e-9,1e-6),"ci":(0.01,0.0)}[kind]
    d=decimals(claimed); rounding=0.5*10**(-d) if (d is not None and d<12) else 0.0
    tol=max(decl[0],decl[1]*abs(claimed),rounding)
    rec["tol"]={"declared_abs":decl[0],"declared_rel":decl[1],"recorded_decimals":d,"rounding_allowance":rounding,"effective_abs":tol}
    eq = (ad<=4*sys.float_info.epsilon*max(1,abs(claimed))) or (rounding>0 and round(derived,d)==claimed)
    rec["verdict"]="MATCH" if eq else ("MATCH_WITHIN_TOL" if ad<=tol else "DISCREPANCY")
    return rec
recs=[]
QUOTED={"C01","C03","C04","K01","K02","L01","L02","L03","L04","L05","Q01","Q02","Q03","Q04","T01","T02","T03","N01","N02","O01"}
STATUS_SEEN={"P02":"binding-night MDE 0.032 (wave3/STATUS.md, read for orientation before sealing)","R02":"66-84 spectra, 7-19 nights (STATUS.md)","R03":"502-644 spectra, 51-144 nights (STATUS.md); also two table rows (spectra 644, nights 144) shown by a structural head of truth_cost_table.csv before sealing","R01":"two table rows shown by a structural head before sealing","L01":"[954, 2,057] also in STATUS.md","A01":"none","C02":"cohort_protocol disclosure lines only"}
def add(tid, comps, premise, provenance, extra=None):
    t=T[tid]; s=S(tid)
    order=["DISCREPANCY","UNVERIFIABLE","MATCH_WITHIN_TOL","MATCH"]
    worst=next(v for v in order if any(c["verdict"]==v for c in comps)) if comps else "UNVERIFIABLE"
    blind=("code-path blind; claimed value quoted in the launching prompt (reader not blind)" if tid in QUOTED else "code-path blind and seal-before-open")
    if tid in STATUS_SEEN and STATUS_SEEN[tid]!="none": blind+="; exposure before seal: "+STATUS_SEEN[tid]
    r={"id":f"V-{tid}","target":tid,"claim":t["claim"],**provenance,
       "recorded_at":t["recorded_at"],"inputs":t["inputs"],"number_type":t["number_type"],"feeds":t["feeds"],
       "sealed_file":f"sealed/V-{tid}.json","sealed_sha256":sha(f"{VD}/sealed/V-{tid}.json"),"sealed_utc":s["sealed_utc"],
       "comparisons":comps,"verdict":worst,"premise_check":premise,"blinding":blind}
    if extra: r.update(extra)
    ok_premise=premise.get("ran") and premise.get("behaved_as_required")
    r["cleared_for_P4_under_rule_E"]= worst in ("MATCH","MATCH_WITHIN_TOL") and bool(ok_premise)
    recs.append(r)
def prov(referent, src, pop, adj, fals):
    return {"referent":referent,"source":src,"population":pop,"adjudicator":adj,"falsifier":fals}
V="astronomy/wave4/agent4_module_v/scripts/"
# ---- cohort
cc={r["id"]:r["value"] for r in J("wave3/agent1_cohort_finish/rubin_cohort_count.json")}
d=S("C01")["derived"]; p=S("C01")["premise"]
add("C01",[cmp_num("O_merged",cc["w3-02"],d["O_merged"],"int")],
    {"test":"drop the largest C3 slice; duplicate 5,000 rows; plant 100 pre-T0 twins 0.5 arcsec from cohort oids","result":p,"ran":True,
     "behaved_as_required":p["drop_largest_slice"]["O_merged"]<d["O_merged"] and p["duplicate_5000_rows"]["O_merged"]==d["O_merged"] and p["plant_100_twins"]["O_merged"]==d["O_merged"]-100},
    prov("merged Rubin cohort objects O after X1-X3 with every member first detected at or after T0","wave3/agent1_cohort_finish/rubin_cohort_count.json::w3-02; verifier "+V+"derive_cohort.py","3,527,572 distinct ALeRCE oids (450 C3 + 1,551 P60 slice files, hashes verified)","independent KD-tree/connected-components recount on the same hashed slices: "+str(d["O_merged"]),"a slice perturbation that leaves the count unchanged, or a recount that differs from the claim"))
d=S("C02")["derived"]
add("C02",[cmp_num("O_A",cc["w3-01"],d["O_A"],"int")],{"test":"duplicate 5,000 rows (must not change), drop largest slice (must drop)","result":S("C02")["premise"],"ran":True,
    "behaved_as_required":S("C02")["premise"]["duplicate_5000_rows_O_A"]==d["O_A"] and S("C02")["premise"]["drop_largest_slice_O_A"]<d["O_A"]},
    prov("distinct ALeRCE/LSST oids with firstmjd >= T0","wave3/agent1_cohort_finish/rubin_cohort_count.json::w3-01; "+V+"derive_cohort.py","450 C3 slice files","independent dedupe recount "+str(d["O_A"]),"a recount on the hashed slices that differs from the claim"))
d=S("C03")["derived"]; v=cc["w3-05"]
add("C03",[cmp_num("S1_total",v["S1_total"],d["S1_total"],"int"),cmp_num("S1_direct_first_in_T0-60d_to_T0",v["S1_direct_first_in_T0-60d_to_T0"],d["S1_direct_from_p60"],"int"),
           cmp_num("S1_direct_first_2026-02-24_to_T0-60d",v["S1_direct_first_2026-02-24_to_T0-60d"],d["S1_direct_from_c5"],"int"),cmp_num("S1_merge",v["S1_merge"],d["S1_merge"],"int")],
    {"test":"set one straddler lastmjd below T0 (S1 must fall by 1); plant 100 pre-T0 twins (S1-merge must rise by 100)","result":{"lastmjd":PX["C03_set_one_straddler_lastmjd_below_T0"],"twins_S1_merge":S("C03")["premise"]},"ran":True,
     "behaved_as_required":PX["C03_set_one_straddler_lastmjd_below_T0"]["S1_after"]==d["S1_total"]-1 and S("C03")["premise"]["plant_100_preT0_twins_S1_merge"]==d["S1_merge"]+100},
    prov("stratum S1 straddlers: pre-T0 oids with lastmjd >= T0 plus cohort oids merged with pre-T0 oids","wave3/agent1_cohort_finish/rubin_cohort_count.json::w3-05; "+V+"derive_cohort.py","1,551 P60 + 1,500 C5 slice files and the merged union","independent recount "+str(d["S1_total"]),"a straddler whose lastmjd is moved below T0 that leaves S1 unchanged, or a recount that differs"))
d=S("C04")["derived"]; v=cc["w3-04"]
add("C04",[cmp_num("S3_one_detection_share_oids",v["S3_one_detection_share_oids"],d["share_over_all_post_T0_oids"],"share"),cmp_num("S3_one_detection_oids",v["S3_one_detection_oids"],d["n_det1"],"int"),
           cmp_num("S3_share_merged",v["S3_share_merged"],d["share_merged_level"],"share")],
    {"test":"flip n_det of 1,000 one-detection cohort oids to 2; share must fall by 1000/O_A","result":PX["C04_flip_1000_ndet"],"ran":True,
     "behaved_as_required":abs(PX["C04_flip_1000_ndet"]["observed_drop"]-PX["C04_flip_1000_ndet"]["expected_drop"])<1e-12},
    prov("share of cohort oids with exactly one detection (S3)","wave3/agent1_cohort_finish/rubin_cohort_count.json::w3-04; "+V+"derive_cohort.py","1,937,720 cohort oids; 1,937,669 merged objects","independent recount 1,566,024/1,937,720","flipping detections that leaves the share unchanged, or a recount outside 0.80815-0.80825"))
# ---- power
pc=J("wave2/agent4_instrument/power_calibration.json"); pd5=J("wave3/agent4_tool_recount/power_calibration_delta005.json")
PMAP={"P01":("E1_N",None),"P02":("E1_N","True"),"P03":("E1_N","False"),"P04":("E1_R",None),"P05":("E3_N",None),"P06":("E3_N","True"),"P07":("E3_N","False"),"P08":("E3_R",None)}
for tid,(run,st) in PMAP.items():
    d=S(tid)["derived"]; comps=[]
    g=lambda o: o if st is None else o["strata"][st]
    w2=g(pc["runs"][run]); comps+= [cmp_num(f"w2 runs.{run}{'.strata.'+st if st else ''}.n",w2["n"],d["n"],"int"),cmp_num("w2 .sigma_d",w2["sigma_d"],d["sigma_d"],"float_stat"),
                                    cmp_num("w2 .mde",w2["mde"],d["mde_doc_z"],"float_stat"),cmp_num("w2 .n_min (delta 0.018)",w2["n_min"],d["n_min_doc_z_delta_0.018"],"int")]
    for dl,key in (("0.05","delta_0.05"),("0.018","delta_0.018")):
        w3=g(pd5["runs"][run][key])
        comps+=[cmp_num(f"w3 runs.{run}.{key}{'.strata.'+st if st else ''}.sigma_d",w3["sigma_d"],d["sigma_d"],"float_stat"),cmp_num(f"w3 ...{key}.mde",w3["mde"],d["mde_doc_z"],"float_stat"),
                cmp_num(f"w3 ...{key}.n_min",w3["n_min"],d[f"n_min_doc_z_delta_{dl}"],"int")]
        tb=pd5["table_both_deltas"][run][dl]
        if st=="True": tb=tb["stratum_k_binding_True"]
        if st in (None,"True") and (st=="True" or run.endswith("_R")):
            comps+=[cmp_num(f"w3 table_both_deltas.{run}.{dl}.n_min",tb["n_min"],d[f"n_min_doc_z_delta_{dl}"],"int"),cmp_num(f"w3 table_both_deltas.{run}.{dl}.mde",tb["mde"],d["mde_doc_z"],"float_stat")]
    if tid=="P02":
        comps+=[cmp_num("w2 top-level sigma_d",pc["sigma_d"],d["sigma_d"],"float_stat"),cmp_num("w2 top-level mde",pc["mde"],d["mde_doc_z"],"float_stat"),cmp_num("w2 top-level n_min",pc["n_min"],d["n_min_doc_z_delta_0.018"],"int"),
                cmp_num("w3 top-level n_min (0.05)",pd5["n_min"],d["n_min_doc_z_delta_0.05"],"int"),cmp_num("w3 at_literature_prior_0.018.n_min",pd5["at_literature_prior_0.018"]["n_min"],d["n_min_doc_z_delta_0.018"],"int")]
    if tid in ("P01","P05"):
        comps.append(cmp_num("w3 pooled_night_runs_refused.mde",pd5["pooled_night_runs_refused"][run]["mde"],d["mde_doc_z"],"float_stat"))
        if tid=="P01": comps.append(cmp_num("w2 pooled_E1_N_refused.mde",pc["pooled_E1_N_refused"]["mde"],d["mde_doc_z"],"float_stat"))
    pr=S(tid)["derived"]
    add(tid,comps,{"test":"shuffle the pairing of col b against col a (seed 20260917) and require sigma_d to change; require N_min*delta^2 >= z^2 sd^2 > (N_min-1)*delta^2 at both deltas; cross-check against the per-run paired file","result":{"shuffle":pr["premise_pairing_shuffle"],"nmin_consistent":pr["premise_nmin_consistent_with_mde"],"per_run_file_sigma_d":pr["crosscheck_per_run_file_sigma_d"]},
        "ran":True,"behaved_as_required":pr["premise_pairing_shuffle"]["changed"] and pr["premise_nmin_consistent_with_mde"] and abs(pr["crosscheck_per_run_file_sigma_d"]-pr["sigma_d"])<1e-15},
        prov(f"paired sigma_d, MDE (alpha 0.05, power 0.80) and N_min at delta 0.018 and 0.05 for {run} {('k_binding='+st) if st else 'all items'}",
             f"wave2/agent4_instrument/power_calibration.json::runs.{run} and wave3/agent4_tool_recount/power_calibration_delta005.json::runs.{run}; verifier "+V+"derive_power.py (exact rationals, not power.py)",
             f"{d['n']} paired items from wave2/agent4_instrument/paired_scores.csv (sha256 d93b31e2...)","independent exact-rational recomputation "+f"sigma_d={d['sigma_d']:.6f}",
             "a pairing shuffle that leaves sigma_d unchanged, or a recomputation that differs beyond the recorded 6 dp"))
# ---- nights
d1=S("K01")["derived"]; d2=S("K02")["derived"]
add("K01",[cmp_num("runs.E1_N.strata.True.n",pc["runs"]["E1_N"]["strata"]["True"]["n"],d1["E1_nights_gt8"],"int"),cmp_num("runs.E1_N.n",pc["runs"]["E1_N"]["n"],d1["E1_nights_total"],"int"),
           cmp_num("runs.E3_N.strata.True.n",pc["runs"]["E3_N"]["strata"]["True"]["n"],d1["E3"]["nights_gt8"],"int")],
    {"test":"plant 60 (must fire); move one unit into an 8-candidate night (count must rise by 1)","result":{"planted":S("K01")["premise"],"move":PX["K01_move_unit_into_8_night"]},"ran":True,
     "behaved_as_required":S("K01")["premise"]["plant_60_detected"] and PX["K01_move_unit_into_8_night"]["gt8_after"]==d1["E1_nights_gt8"]+1},
    prov("E1 decision nights with more than k=8 scored candidates, of all E1 decision nights","wave2/agent4_instrument/power_calibration.json::runs.E1_N.strata.True.n; verifier "+V+"derive_auc_nights.py","2,558 scored-pool units (posA or neg by corpus type) in pred_E1_C.csv","independent count from predictions + corpus: 61 of 579","moving one unit into an 8-candidate night that leaves the count unchanged, or a recount that differs"))
add("K02",[cmp_num("runs.E1_N.strata.False.n",pc["runs"]["E1_N"]["strata"]["False"]["n"],d2["E1_nights_le8"],"int"),cmp_num("runs.E3_N.strata.False.n",pc["runs"]["E3_N"]["strata"]["False"]["n"],d2["E3"]["nights_le8"],"int")],
    {"test":"plant 517 (must fire); K01+K02 must equal total","result":{"planted":S("K02")["premise"],"sum_check":d2["sum_check"]},"ran":True,"behaved_as_required":S("K02")["premise"]["plant_517_detected"] and d2["sum_check"]},
    prov("E1 decision nights with <= 8 scored candidates","wave2/agent4_instrument/power_calibration.json::runs.E1_N.strata.False.n; "+V+"derive_auc_nights.py","2,558 scored-pool units","independent count 518","a recount that differs or K01+K02 not equal to 579"))
# ---- AUC
ic=J("wave2/agent4_instrument/i2_channels.json")["epochs"]
for tid,E,key in (("A01","E1","measured_C_minus_1"),("A02","E1","measured_C"),("A03","E3","measured_C_minus_1"),("A04","E3","measured_C")):
    d=S(tid)["derived"]; c=ic[E][key]; pm=d["premise"]
    add(tid,[cmp_num("auc_posB",c["auc_posB"],d["auc_posB"],"auc"),cmp_num("auc_ci95[0]",c["auc_ci95"][0],d["ci95_percentile_default_rng0"][0],"ci"),cmp_num("auc_ci95[1]",c["auc_ci95"][1],d["ci95_percentile_default_rng0"][1],"ci")],
        {"test":"permute posB labels (seed 1): AUC must move into [0.45,0.55]; negate scores: AUC must equal 1-AUC; producer __perm prediction file must sit near 0.5","result":pm,"ran":True,
         "behaved_as_required":0.45<=pm["label_permutation_seed1_auc"]<=0.55 and abs(pm["negated_scores_auc"]-pm["one_minus_auc"])<1e-12 and 0.45<=pm["producer_perm_prediction_file_auc_under_our_labels"]<=0.55},
        prov(f"per-object ROC AUC for posB, epoch {E}, composition {key}, with 1000-resample bootstrap 95% CI","wave2/agent4_instrument/i2_channels.json::epochs."+E+"."+key+"; verifier "+V+"derive_auc_nights.py (own midrank Mann-Whitney)",
             f"{d['n_scored']} scored-pool units, {d['n_posB']} posB, predictions verified against compositions/MANIFEST.sha256","independent rank AUC "+f"{d['auc_posB']:.6f}; sklearn cross-check equal","a label permutation that leaves AUC away from 0.5, or a recomputation that differs beyond 1e-6"))
# ---- labels (blind sealed values)
ls=J("wave3/agent2_measured_labels/label_source_slot.json")["value"]["bts"]; LR=json.load(open(f"{VD}/sealed/V-L-r1.json"))["derived"]
lab_prem=S("L01")["premise"]["marker_rename"]
def lab_prem_rec(tid):
    return {"test":"rename 'SNIascore' in one SNIascore-placed object's classifier field to a human name: MODEL must fall by 1, MEASURED or PHOT rise by 1, L fall by 1, U fall by 1; categories must partition 7,843","result":lab_prem,"ran":True,
            "behaved_as_required":lab_prem["after"]["L"]==952 and lab_prem["after"]["categories"]["MODEL_ANNOTATION"]==947 and lab_prem["after"]["categories"]["MEASURED"]==1071}
LP=lambda ref: prov(ref,"wave3/agent2_measured_labels/label_source_slot.json::value.bts; verifier "+V+"derive_labels.py (own TNS page parser), post-disclosure "+V+"labels_lib_r1.py + diff_bound_e5.py",
     "7,843 labelled BTS rows (5,067 plain SN Ia); 2,051 archived TNS captures (1,706+5 wave 2, 345 wave 3)","independent parse of the same captures under definitions_FROZEN.md; blind values differ, causes in discrepancies/","a re-parse that places a different count under the stated reading, or a marker rename that leaves the count unchanged")
res_extra=lambda: {"post_disclosure_rederivation":{"sealed_file":"sealed/V-L-r1.json","sealed_sha256":sha(f"{VD}/sealed/V-L-r1.json"),"producer_reading(key=ztfid,E5cut=1289.5)":{k:LR["key=ztfid|E5cut=1289.5"][k] for k in ("cats","L","U","U_noE5")},
     "literal_E5_reading(key=ztfid,E5cut=1259.5)":{k:LR["key=ztfid|E5cut=1259.5"][k] for k in ("cats","L","U")},"iau_key_reading(key=iau,E5cut=1289.5)":{k:LR["key=iau|E5cut=1289.5"][k] for k in ("cats","L","U")}}}
add("L01",[cmp_num("sniascore_bound.lower",ls["sniascore_bound"]["lower"],S("L01")["derived"]["L"],"int")],lab_prem_rec("L01"),LP("SNIascore model-annotation lower bound L over plain SN Ia"),res_extra())
add("L02",[cmp_num("sniascore_bound.upper",ls["sniascore_bound"]["upper"],S("L02")["derived"]["U"],"int"),cmp_num("upper_noE5_sensitivity",ls["sniascore_bound"]["upper_noE5_sensitivity_not_slot_value"],S("L02")["derived"]["U_noE5"],"int")],lab_prem_rec("L02"),LP("SNIascore upper bound U over plain SN Ia"),res_extra())
for tid,k,kd in (("L03","MEASURED","MEASURED"),("L04","MODEL_ANNOTATION","MODEL_ANNOTATION"),("L05","UNRESOLVED_UNDEMONSTRATED","UNRESOLVED")):
    dd=S(tid)["derived"]; comps=[cmp_num(f"category_counts.{k}",ls["category_counts"][k],dd["count"],"int")]
    if tid=="L03": comps.append(cmp_num("category_counts.PHOTOMETRIC_ONLY",ls["category_counts"]["PHOTOMETRIC_ONLY"],dd["all_categories"].get("PHOTOMETRIC_ONLY",0),"int"))
    add(tid,comps,lab_prem_rec(tid),LP(f"BTS label category count {k}"),res_extra())
# ---- p-values
la=J("wave2/agent1_rubin_bands/label_accrual.json")["lag_tests"]
for tid,key in (("Q01","(i) capture_2026-07-25 vs ref 2024-12-08T23:13:31"),("Q02","(i) capture_2026-07-25 vs ref 2025-08-10T06:50:56"),("Q03","(ii) file_2026-09-16 vs ref 2024-12-08T23:13:31"),("Q04","(ii) file_2026-09-16 vs ref 2025-08-10T06:50:56")):
    d=S(tid)["derived"]; c=la[key]
    add(tid,[cmp_num("P_lower_tail",c["P_lower_tail"],d["P_lower_tail"],"log10p"),cmp_num("n_included",c["n_included"],d["n_included"],"int"),cmp_num("observed_labelled",c["observed_labelled"],d["observed_labelled"],"int"),
             cmp_num("excluded_no_reference",c["excluded_no_reference"],d["excluded_no_reference"],"int"),cmp_num("expected_labelled_under_LAG",c["expected_labelled_under_LAG"],round(d["expected"],1),"float_stat")],
        {"test":"set X to its LAG expectation: P must rise to about 0.5; DP must equal scipy binom.cdf when all p_i are equal","result":{"P_at_X_equal_E":d["premise_P_at_X_equal_expectation"],"dp_vs_binom":d["premise_dp_vs_scipy_binom"]},"ran":True,
         "behaved_as_required":0.4<d["premise_P_at_X_equal_expectation"]<0.6 and abs(d["premise_dp_vs_scipy_binom"][0]-d["premise_dp_vs_scipy_binom"][1])<1e-12},
        prov(f"exact Poisson-binomial lower-tail p for labelled 2026-peak objects, {key}","wave2/agent1_rubin_bands/label_accrual.json::lag_tests; verifier "+V+"derive_accrual.py (own HTML parse + log-space DP)",
             f"{d['n_included']} 2026-peak objects; reference accrual from the named explorer capture","independent exact tail "+f"{d['P_lower_tail']:.3e}"+f"; age-from-date sensitivity {d['sensitivity_age_from_date_midnight']['P_lower_tail']:.3e}",
             "setting X to its expectation that does not return p near 0.5, or a recomputation differing by more than 0.05 in log10"),
        {"note":"residual 1-5% relative difference in p (0.004-0.020 in log10) with identical n, X and expected count to 0.1: consistent with age-reference convention (capture timestamp vs date); within declared tolerance, so no discrepancy report","decision_check":{"claimed_ruling":J("wave2/agent1_rubin_bands/label_accrual.json")["decision"]["ruling"],"derived_ruling":d["ruling_derived"]}})
# ---- tools
ax=J("wave3/agent4_tool_recount/tool_coverage_axis.json"); d=S("T01")["derived"]
add("T01",[cmp_num(f"all.{k}",ax["value"]["counts_by_group_and_disposition"]["all"][k],d["counts"].get(k,0),"int") for k in ("PASS","FAIL","UNDEMONSTRATED")]+[cmp_num("n_tools",len(ax["value"]["per_tool"]),d["n_tools"],"int")],
    {"test":"flip CATS non_default to false on every run: PASS count must fall","result":S("T01")["premise"],"ran":True,"behaved_as_required":S("T01")["premise"]["fires"]},
    prov("tool dispositions over the 25-tool inventory on Rubin alert rows","wave3/agent4_tool_recount/tool_coverage_axis.json::value.counts_by_group_and_disposition.all; verifier "+V+"derive_tools_time.py","198 run_log.jsonl lines, 25 tools","independent tally under recount_protocol_FROZEN.md section 1 and AM2","a non_default flip that leaves the tally unchanged, or a retally that differs"))
pt={x["tool"]:x for x in ax["value"]["per_tool"]}; d=S("T02")["derived"]
add("T02",[cmp_num("CATS.passes",pt["CATS"]["passes"],d["CATS"]["passes"],"int"),cmp_num("CATS.alerts_run",pt["CATS"]["alerts_run"],d["CATS"]["valid"],"int"),cmp_num("GHOST.passes",pt["GHOST"]["passes"],d["GHOST"]["passes"],"int"),cmp_num("GHOST.alerts_run",pt["GHOST"]["alerts_run"],d["GHOST"]["valid"],"int")],
    {"test":"un-void GHOST runs 1-2: denominator must become 10","result":S("T02")["premise"],"ran":True,"behaved_as_required":S("T02")["premise"]["fires"] and S("T02")["premise"]["unvoided_GHOST"]["valid"]==10},
    prov("pass counts for the two passing tools","wave3/agent4_tool_recount/tool_coverage_axis.json::value.per_tool; "+V+"derive_tools_time.py","CATS 10 and GHOST 10 logged alert runs (2 voided under AM2)","independent retally 5/10 and 3/8","un-voiding that leaves the denominator at 8, or a retally that differs"))
d=S("T03")["derived"]
add("T03",[cmp_num("alert_runs_logged",ax["value"]["alert_runs_logged"],d["alert_runs"],"int")],{"test":"count including PRECHECK/LOAD lines must differ","result":S("T03")["premise"],"ran":True,"behaved_as_required":S("T03")["premise"]["fires"]},
    prov("alert runs consumed against the rule D cap of 250","wave3/agent4_tool_recount/tool_coverage_axis.json::value.alert_runs_logged; "+V+"derive_tools_time.py","198 run_log lines","independent count 160 (voided GHOST runs included as consumed)","a count that includes load lines and still matches, or a recount that differs"))
# ---- N and truth cost
import csv
tct=list(csv.DictReader(open(f"{A}/wave3/agent2_measured_labels/truth_cost_table.csv")))
Ns=lambda dl: sorted({int(r["N"]) for r in tct if r["delta"]==dl})
for tid,dl in (("N01","0.018"),("N02","0.05")):
    d=S(tid)["derived"][f"planning_mde_bracket.csv|delta={dl}"]; d3=S(tid)["derived"][f"planning_mde_bracket_w3.csv|delta={dl}"]
    add(tid,[cmp_num(f"truth_cost_table N lo (delta {dl})",Ns(dl)[0],d["realised_sigma_lo_hi"][0],"int"),cmp_num(f"truth_cost_table N hi (delta {dl})",Ns(dl)[1],d["realised_sigma_lo_hi"][1],"int"),
             cmp_num(f"w3-09 objects_family_B {dl} lo",cc["w3-09"]["objects_family_B"][dl][0],d3["realised_sigma_lo_hi"][0],"int"),cmp_num(f"w3-09 objects_family_B {dl} hi",cc["w3-09"]["objects_family_B"][dl][1],d3["realised_sigma_lo_hi"][1],"int")],
        {"test":"scale the sigma of the max row by 1.01: hi must rise; plant 486: must fire","result":PX["N_perturb_max_row_x1.01"],"ran":True,"behaved_as_required":PX["N_perturb_max_row_x1.01"]["hi_0.018_after"]>PX["N_perturb_max_row_x1.01"]["hi_0.018_before"] and PX["N_perturb_max_row_x1.01"]["planted_486_fires"]},
        prov(f"family-B N_min lo and hi at delta {dl} (kill-band thresholds and truth-cost N)","wave3/agent2_measured_labels/truth_cost_table.csv N column; bands_FROZEN.md section 5; verifier "+V+"derive_cost.py","16 family-B synthetic rows of planning_mde_bracket.csv","independent ceil(z^2 sigma^2/delta^2)",
             "a sigma perturbation of the max row that leaves hi unchanged, or a recomputation that differs"),
        {"finding":f"hi depends on the finite-sample realised sigma of the n=50 synthetic binary column (0.728431 vs sqrt(q)=0.7071): theoretical sqrt(q) gives hi {d['theoretical_sqrt_q_lo_hi'][1]} not {d['realised_sigma_lo_hi'][1]}. Not a discrepancy (the frozen definition is min/max over the bracket rows as computed); recorded for agent 3 and the PI"})
d=S("R01")["derived"]
add("R01",[cmp_num("rows_mismatching_formula (claim: 0)",0,d["rows_mismatching_formula"],"int"),cmp_num("n_rows",J("wave3/agent2_measured_labels/truth_cost.json")["n_rows"],d["n_rows"],"int")],
    {"test":"set purity 0.5 in row 0: S must change","result":S("R01")["premise"],"ran":True,"behaved_as_required":S("R01")["premise"]["row0_S_with_p=0.5"]!=S("R01")["premise"]["row0_S_orig"]},
    prov("truth-cost table arithmetic: S, H, W, nights per row","wave3/agent2_measured_labels/truth_cost_table.csv; census_protocol_FROZEN.md section 10; verifier "+V+"derive_cost.py (exact rationals)","288 rows","independent rational recomputation, 0 mismatching rows","a purity perturbation that leaves S unchanged, or any row whose recomputation differs"))
tcj=J("wave3/agent2_measured_labels/truth_cost.json")["ranges_over_grid_L0"]
for tid,keys in (("R02",["delta_0.05_N_63"]),("R03",["delta_0.018_N_485"]),("R04",["delta_0.05_N_1666","delta_0.018_N_12855"])):
    d=S(tid)["derived"]; comps=[]
    for k in keys:
        for f,fd in (("spectra","spectra"),("nights","nights"),("hours","hours"),("wrong_commitments","wrong")):
            comps+=[cmp_num(f"{k}.{f}[0]",tcj[k][f][0],d[k][fd][0],"int" if f!="hours" else "float_stat"),cmp_num(f"{k}.{f}[1]",tcj[k][f][1],d[k][fd][1],"int" if f!="hours" else "float_stat")]
    add(tid,comps,{"test":"planted wrong range (lo+1) must fire","result":{"planted_fires":True},"ran":True,"behaved_as_required":cmp_num("x",d[keys[0]]["spectra"][0]+1,d[keys[0]]["spectra"][0],"int")["verdict"]=="DISCREPANCY"},
        prov("truth-cost ranges over the p, s, c grid at L=0","wave3/agent2_measured_labels/truth_cost.json::ranges_over_grid_L0; verifier "+V+"derive_cost.py","L=0 grid rows of truth_cost_table.csv","independent recomputation from input columns","a planted range that is not caught, or a recomputation that differs"))
# ---- timestamps
d=S("O01")["derived"]
add("O01",[cmp_num("wave-3 brief (override) time vs commit 32229e3 15:14:03-0500 quoted",("2026-09-16T20:14:03Z"),d["wave3_brief_mtime_utc"],"ts"),
           cmp_num("power_calibration.json mtime 20:44:29Z quoted",("2026-09-16T20:44:29Z"),d["power_calibration_json_mtime_utc"],"ts"),
           cmp_num("wave-3 agent 4 step 1 20:48:29Z quoted",("2026-09-16T20:48:29Z"),d["w3a4_step1_log_utc"],"ts"),
           cmp_num("ordering override < first MDE < resolvability at 0.05",True,d["order_holds_in_UTC"],"bool"),
           cmp_num("step-1 logged hash equals current delta005 file",True,d["w3a4_step1_logged_hash_equals_current_delta005_file"],"bool")],
    {"test":"swap the brief and power timestamps, and the power and step-1 timestamps: the ordering check must fail on both","result":PX["O01_planted"],"ran":True,"behaved_as_required":PX["O01_planted"]["fires_on_planted"] and PX["O01_planted"]["real"]},
    prov("ruling-1 order: delta override declared before the first decision-time MDE, which precedes resolvability at 0.05","file mtimes (os.stat) of wave3/PANEL_BRIEF_WAVE3.md, wave2/agent4_instrument/power_calibration.json and data_cache/power/*; wave3/*/order_of_operations.log; verifier "+V+"derive_tools_time.py",
         "3 events on one host clock","independent mtimes and log lines; earliest wave-2 power output mtime 20:43:28Z, 29.4 min after the brief","a swapped timestamp pair that the check does not catch, or an mtime that differs from the quoted time by more than 1 s"),
    {"cannot_establish_without_git":d["cannot_establish_without_git"],"note":"The 15:14:03-0500 commit time and the 20:46Z commit f898294 are quoted from the preamble and are not independently read (no git). Mtimes are last-modification times; an earlier overwritten version of a power file cannot be excluded. The wave-3 brief content hash a618d911... was self-logged by wave-3 agent 1 at 20:15:13Z and equals the current file, which contains the override text."})
d=S("O02")["derived"]; rt=ax["recount_timestamps"]
add("O02",[cmp_num("band_hash_utc",rt["band_hash_utc"],d["band_hash_utc"],"ts"),cmp_num("protocol_frozen_utc",rt["protocol_frozen_utc"],d["protocol_frozen_utc"],"ts"),cmp_num("first_run_utc",rt["first_run_utc"],d["first_run_start_utc"],"ts"),
           cmp_num("last_run_utc",rt["last_run_utc"],d["last_run_end_utc"],"ts"),cmp_num("all_runs_after_band_hash",rt["all_runs_after_band_hash"],d["all_runs_after_band_hash"],"bool"),
           cmp_num("precondition (b) clears (all runs after band hash and protocol freeze, 25 tools dispositioned)",True,d["precondition_b_clears"],"bool")],
    {"test":"plant one run starting at 18:00Z: the check must fire","result":S("O02")["premise"],"ran":True,"behaved_as_required":S("O02")["premise"]["planted_early_run_detected"]},
    prov("P4 precondition (b) for tool_coverage: every recount run after the band hash, protocol frozen before the first run, all 25 tools dispositioned","wave3/agent4_tool_recount/tool_coverage_axis.json::recount_timestamps; run_log.jsonl; wave2/agent1_rubin_bands/order_of_operations.log step 1; verifier "+V+"derive_tools_time.py",
         "198 run_log lines","independent parse; band hash logged equals current bands_FROZEN.md","a planted early run that the check fails to flag, or any run start measured before 18:51:26.922781Z"))
json.dump(recs,open(f"{VD}/v_records.json","w"),indent=1,default=str)
for r in recs: print(r["id"],r["verdict"],"premise_ok" if r["premise_check"]["behaved_as_required"] else "PREMISE_FAIL","cleared" if r["cleared_for_P4_under_rule_E"] else "NOT_CLEARED",[ (c["field"],c["verdict"]) for c in r["comparisons"] if c["verdict"] not in ("MATCH",)][:4])
