import json
W2A4="astronomy/wave2/agent4_instrument"; W3A4="astronomy/wave3/agent4_tool_recount"
W3A1="astronomy/wave3/agent1_cohort_finish"; W2A1="astronomy/wave2/agent1_rubin_bands"
W2A2="astronomy/wave2/agent2_label_source"; W3A2="astronomy/wave3/agent2_measured_labels"
T=[]
def t(id,claim,rec,inputs,premise,ntype,feeds):
    T.append(dict(id=id,claim=claim,recorded_at=rec,inputs=inputs,premise_check=premise,number_type=ntype,feeds=feeds))
slices=[f"{W3A1}/out/w3_c3_slices/*.csv (450, verified against {W3A1}/out/SLICES_SHA256SUMS)",
        f"{W3A1}/out/w3_p60_slices/*.csv and w3_c5_slices/*.csv (verified against SLICES_SHA256SUMS)",
        f"{W2A1}/bands_FROZEN.md §2 X1-X3, §3 (sha256 8825ef80...00d2)",
        f"{W3A1}/count_protocol_w3_FROZEN.md W3-M (sha256 de241fc9...b649)", f"{W3A1}/amendments_w3.md AM6-AM7"]
t("C01","Cohort total O: merged objects after X1-X3 with every member firstmjd >= T0",
  {"file":f"{W3A1}/rubin_cohort_count.json","field":"[id=w3-02].value"},slices,
  "Perturb one slice (drop it / duplicate rows / shift one oid across T0) and confirm the count moves by the expected amount; planted +1000 claim must fire (replay V-01)","integer_count","positive_supply axis O; manifest cohort slot; truth-cost A")
t("C02","Distinct ALeRCE/LSST oids with firstmjd >= T0 before merge (O_A)",
  {"file":f"{W3A1}/rubin_cohort_count.json","field":"[id=w3-01].value"},slices[:1]+slices[2:],
  "Duplicate a slice file and confirm dedupe on oid holds the count; remove a slice and confirm the count drops","integer_count","cluster_structure axis")
t("C03","Straddlers S1 = S1-direct (pre-T0 oids with lastmjd >= T0) + S1-merge (cohort oids merged with a pre-T0 oid)",
  {"file":f"{W3A1}/rubin_cohort_count.json","field":"[id=w3-05].value"},slices,
  "Set one pre-T0 row's lastmjd below T0 and confirm S1 drops by one; plant a pre-T0 twin 0.5 arcsec from a cohort oid and confirm S1-merge rises","integer_count","split_integrity axis")
t("C04","One-detection share S3/(S3+S4) over the cohort",
  {"file":f"{W3A1}/rubin_cohort_count.json","field":"[id=w3-04].value (and any merged-level variant in the record)"},slices,
  "Flip n_det of k cohort rows from 1 to 2 and confirm the share falls by k/N","share","stratum S3/S4 report (BTS two-detection comparison)")
PC=f"{W2A4}/power_calibration.json"; PD=f"{W3A4}/power_calibration_delta005.json"
pin=[f"{W2A4}/paired_scores.csv (sha256 in {W2A4}/HASH_MANIFEST.sha256)",
     f"{W2A4}/data_cache/power/paired_<run>.csv (sha256 scores_file_sha256 in the power records)",
     "fm-advantage-benchmark/scripts/power.py documented math: d=a-b, sd ddof=1, MDE=(z_{1-a/2}+z_power)*sd/sqrt(n), N_min=ceil(z^2 sd^2/delta^2), z table 1.9600+0.8416; own implementation",
     f"{W2A4}/compositions_FROZEN.md §4 (items N, R; k_binding stratum)"]
rows=[("P01","E1_N","pooled (all 579 night items)","[pooled]"),("P02","E1_N","k_binding=True","strata.True"),("P03","E1_N","k_binding=False","strata.False"),
      ("P04","E1_R","round-46 items",""),("P05","E3_N","pooled","[pooled]"),("P06","E3_N","k_binding=True","strata.True"),
      ("P07","E3_N","k_binding=False","strata.False"),("P08","E3_R","round-46 items","")]
for id,run,st,fld in rows:
    t(id,f"sigma_d, MDE, N_min at delta 0.018 and 0.05 for power row {run} {st} (col a=prec_classical, col b=prec_instrument)",
      {"file":[PC,PD],"field":[f"runs.{run}{('.'+fld) if fld.startswith('strata') else ''}.{{n,sigma_d,mde,n_min}} (delta 0.018)",
        f"runs.{run}.delta_0.05|delta_0.018{('.'+fld) if fld.startswith('strata') else ''}.{{n,sigma_d,mde,n_min}}; table_both_deltas; top-level sigma_d/mde/n_min for the primary run; pooled_*_refused.mde"]},
      pin,"Permute the pairing (shuffle col b against col a) and confirm sigma_d changes; plant sd*1.1 and confirm N_min changes by the predicted ratio; check N_min*delta^2 ~ z^2 sd^2","float_statistic + ceil_integer",
      "P7 resolution; binding-night MDE vs delta in P4 and kill bands")
t("K01","k-binding night count: E1 night items with more than k=8 scored candidates, out of all E1 decision nights",
  {"file":[PC,PD],"field":"runs.E1_N strata.True.n and n (pooled); primary_run text"},
  [f"{W2A4}/compositions/predictions/pred_E1_C.csv (decision_night per unit; MANIFEST.sha256)","astronomy/agent1_supply_corpus/corpus.csv (sha256 b059acf0...8442; type -> posA/neg scored pool via bands_FROZEN §4 map)",f"{W2A4}/compositions_FROZEN.md §2,§4"],
  "Plant a wrong night count (60) and confirm the comparison fires; move one unit to a night with 8 candidates and confirm the count rises by one","integer_count","binding-night stratum for MDE; P7")
t("K02","Nights with <= 8 scored candidates (k not binding), E1",
  {"file":[PC,PD],"field":"runs.E1_N strata.False.n"},T[-1]["inputs"],
  "K01+K02 must equal total nights; plant 517 and confirm fire","integer_count","P7 stratum")
predin=[f"{W2A4}/compositions/predictions/pred_<E>_<C|C-1>.csv (verified against compositions/MANIFEST.sha256)","astronomy/agent1_supply_corpus/corpus.csv posB map (compositions_FROZEN §4) keyed by object_cluster_1arcsec",f"{W2A4}/compositions_FROZEN.md §4 (1000-resample object bootstrap, seed 0)"]
for id,E,C in [("A01","E1","C-1"),("A02","E1","C"),("A03","E3","C-1"),("A04","E3","C")]:
    key="measured_C_minus_1" if C=="C-1" else "measured_C"
    t(id,f"Per-object ROC AUC for posB over the scored pool, epoch {E}, composition {C}, with 95% bootstrap CI",
      {"file":f"{W2A4}/i2_channels.json","field":f"epochs.{E}.{key}.auc_posB and .auc_ci95"},predin,
      "Permute posB labels (seeded) and confirm AUC moves into ~[0.45,0.55]; negate scores and confirm AUC -> 1-AUC; the producer's own __perm prediction file must sit near 0.5","auc + bootstrap_ci",
      "I2 channel measurement; instrument vs classical floor reading")
LB=[f"{W2A2}/label_basis_per_object_detail.csv (per-object evidence flags E2-E6, fetch_status; used only for fetch-attempt status and cross-check)",
    f"{W2A2}/sources/tns_captures/html/*.html(.gz) + fetch_log.jsonl (wave-2 E1 captures)",
    f"{W3A2}/out/track1_captures/html/*.html.gz + fetch_log.jsonl (wave-3 archive resume)",
    "astronomy/data/raw/ztf_bts_all_2026-09-16.csv (sha256 61415979...e570)",
    f"{W2A2}/definitions_FROZEN.md §2-§6 (sha256 4f89ff67...37cf); {W3A2}/census_protocol_FROZEN.md §11 bound rule",
    "NOTE: task names label_basis_per_object CSVs in wave3/agent2_measured_labels; none exists there (only out/track1_bound.json + captures). Recorded as input disagreement."]
t("L01","SNIascore bound lower L (E1 MODEL_ANNOTATION SNIascore on plain SN Ia, union E2)",
  {"file":f"{W3A2}/label_source_slot.json","field":"value.bts.sniascore_bound.lower"},LB,
  "Rename the SNIascore marker in one parsed classifier field and confirm L drops by one; plant a wrong L and confirm fire","integer_count","label_source slot (ruling 4 condition: bound inside [803,2247])")
t("L02","SNIascore bound upper U (plain SN Ia not excluded by E1 non-SNIascore, E4, E5), min with 3131 / never widened",
  {"file":f"{W3A2}/label_source_slot.json","field":"value.bts.sniascore_bound.upper"},LB,
  "Disable E5 and confirm U rises (U_noE5 >= U); remove one E1 MEASURED exclusion and confirm U rises by one","integer_count","label_source slot")
for id,cat in [("L03","MEASURED"),("L04","MODEL_ANNOTATION"),("L05","UNRESOLVED_UNDEMONSTRATED")]:
    t(id,f"BTS label category count {cat} over the 7,843 labelled rows",
      {"file":f"{W3A2}/label_source_slot.json","field":f"value.bts.category_counts.{cat}"},LB,
      "Categories must partition 7,843; plant a human classifier as 'SNIascore bot' and confirm MEASURED-1/MODEL+1","integer_count","label_source slot; ruling 4 measured-truth condition")
LA=[f"{W2A1}/label_accrual.json inputs block (paths+sha256 only): astronomy/data/raw/ztf_bts_all_2026-09-16.csv; astronomy/agent3_labels_exposure/sources/wayback_bts_explorer_{{20241208231331,20250810065056,20260725033557}}.html",
    f"{W2A1}/bands_FROZEN.md §9 (age bins, reference accrual, exact Poisson-binomial lower tail)","own Poisson-binomial (log-space DP) implementation"]
for id,cmp,ref in [("Q01","(i) capture_2026-07-25","2024-12-08T23:13:31"),("Q02","(i) capture_2026-07-25","2025-08-10T06:50:56"),
                   ("Q03","(ii) file_2026-09-16","2024-12-08T23:13:31"),("Q04","(ii) file_2026-09-16","2025-08-10T06:50:56")]:
    t(id,f"POLICY lower-tail p-value, comparison {cmp} vs reference {ref}",
      {"file":f"{W2A1}/label_accrual.json","field":f"lag_tests['{cmp} vs ref {ref}'].P_lower_tail (and decision.P_i/P_ii, decision.ruling)"},LA,
      "Replace observed labelled count X by its LAG expectation E and confirm p rises to ~0.5; check DP against scipy binom when all p_i equal","log10_pvalue","POLICY vs LAG ruling (label-accrual wait expectation)")
RL=[f"{W3A4}/run_log.jsonl (198 lines)",f"{W3A4}/recount_protocol_FROZEN.md §1,§2,§5,§6 (sha256 f32cf288...52e6)",f"{W3A4}/amendments.md AM1-AM2 (GHOST runs 1-2 voided)"]
t("T01","Tool coverage dispositions over 25 tools: PASS / FAIL / UNDEMONSTRATED counts",
  {"file":f"{W3A4}/tool_coverage_axis.json","field":"value.counts_by_group_and_disposition.all"},RL,
  "Flip one CATS non_default to false for all runs and confirm PASS count drops; plant 3 PASS and confirm fire","integer_count","tool_coverage axis (P4)")
t("T02","Per-tool pass fractions for the passing tools: CATS passes/alerts run, GHOST passes/valid alerts run",
  {"file":f"{W3A4}/tool_coverage_axis.json","field":"value.per_tool[tool=CATS|GHOST] pass counts"},RL,
  "Un-void GHOST runs 1-2 and confirm denominator becomes 10","integer_count","tool_coverage axis")
t("T03","Alert runs logged against the rule D cap of 250",
  {"file":f"{W3A4}/tool_coverage_axis.json","field":"value.alert_runs_logged"},RL,
  "Count must exclude PRECHECK/LOAD lines; including them must change the count","integer_count","rule D budget (module V gets 250 - this)")
PB=["astronomy/agent5_resolution_replay/planning_mde_bracket.csv (sha256 c00718b7...ad43; inputs sigma_d_target, sigma_d_realised_by_power_py, family)",
    f"{W3A1}/planning_mde_bracket_w3.csv (inputs sigma_d columns only)",f"{W2A1}/bands_FROZEN.md §5 definition N_B,lo/hi = min/max family-B N_min","own N_min=ceil(z^2 sigma^2/delta^2)"]
t("N01","Family-B N_min lo and hi at delta 0.018 (485, 12,855 per bands §5)",
  {"file":[f"{W3A2}/truth_cost_table.csv (N column)",f"{W2A1}/bands_FROZEN.md §5"],"field":"N where delta=0.018"},PB,
  "Recompute with sigma of one row x1.01 and confirm min/max shift; plant 486 and confirm fire","integer_count","positive_supply bands; truth-cost N")
t("N02","Family-B N_min lo and hi at delta 0.05",
  {"file":[f"{W3A2}/truth_cost_table.csv (N column)",f"{W3A1}/rubin_cohort_count.json [id=w3-09]"],"field":"N where delta=0.05"},PB,
  "As N01","integer_count","kill-band pricing at ratified delta 0.05")
TC=[f"{W3A2}/truth_cost_table.csv input columns (delta,N,L,purity_p,success_s,capacity_c,A_reachable_arrivals_per_night_cp95_lo)",f"{W3A2}/census_protocol_FROZEN.md §10 formulas (sha256 9fac8552...95fb)"]
t("R01","Truth-cost table arithmetic: spectra S, hours H, wrong commitments W, nights for every row",
  {"file":f"{W3A2}/truth_cost_table.csv","field":"spectra_S, P60_hours_H, wrong_routine_commitments_W, rubin_on_sky_nights per row"},TC,
  "Perturb p in one row and confirm S changes; count rows mismatching formula (must be 0 if claim true)","integer_count (rows)","kill-band pricing")
t("R02","Truth-cost range at N=63 (delta 0.05), L=0: spectra [lo,hi], nights [lo,hi]",
  {"file":f"{W3A2}/truth_cost.json","field":"ranges_over_grid_L0.delta_0.05_N_63.{spectra,nights}"},TC,"Plant a wrong range and confirm fire","integer_count","ESCALATE option 1 price")
t("R03","Truth-cost range at N=485 (delta 0.018), L=0: spectra [lo,hi], nights [lo,hi]",
  {"file":f"{W3A2}/truth_cost.json","field":"ranges_over_grid_L0.delta_0.018_N_485.{spectra,nights}"},TC,"Plant a wrong range and confirm fire","integer_count","ESCALATE option 1 price")
t("R04","Truth-cost ranges at N=1,666 (delta 0.05) and N=12,855 (delta 0.018), L=0",
  {"file":f"{W3A2}/truth_cost.json","field":"ranges_over_grid_L0.delta_0.05_N_1666 and delta_0.018_N_12855"},TC,"Plant a wrong range and confirm fire","integer_count","kill-band pricing upper rows")
t("O01","Ruling-1 ordering: override declared (wave-3 brief) < first decision-time MDE (power_calibration.json) < resolvability at 0.05 (wave-3 agent 4 step 1)",
  {"file":["astronomy/wave4/PANEL_BRIEF_WAVE4.md coordinator preamble item 2"],"field":"20:14Z < 20:44:29Z (mtime) / 20:46Z (commit f898294) < 20:48:29Z"},
  ["file mtimes: astronomy/wave3/PANEL_BRIEF_WAVE3.md, astronomy/wave2/agent4_instrument/power_calibration.json, astronomy/wave3/agent4_tool_recount/power_calibration_delta005.json",
   "astronomy/wave3/*/order_of_operations.log first lines (brief-verified times)","commit times as quoted in the preamble (git not run; cannot be independently established)","power_calibration.json content hash vs agent-4 w3 step-1 log line"],
  "Plant a reversed timestamp pair and confirm ordering check fires; check that mtime of a file rewritten after the fact would break the chain (hash in step-1 log vs current file)","timestamp_ordering","ruling 1 cause check (delta 0.05 ratified)")
t("O02","P4 precondition (b): every tool-recount run timestamp after the band hash 2026-09-16T18:51:26.922781Z, protocol frozen before first run, and all 25 tools carry a disposition",
  {"file":f"{W3A4}/tool_coverage_axis.json","field":"recount_timestamps.* and all_runs_after_band_hash"},
  [f"{W3A4}/run_log.jsonl start_utc/end_utc",f"{W2A1}/order_of_operations.log (band hash step)",f"{W3A4}/order_of_operations.log (protocol freeze step)","file mtimes of bands_FROZEN.md and recount_protocol_FROZEN.md"],
  "Plant one run with start_utc before the band hash and confirm the check fires","timestamp_ordering","P4 precondition (b)")
doc={"module":"V (wave 4, agent 4)","charter_sha256":open("/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave4/agent4_module_v/V_CHARTER.sha256").read().split()[0],
 "written_utc":None,"note":"Claimed values intentionally omitted. The launching prompt quoted several claimed values (see charter §2 blinding limit).","n_targets":len(T),"targets":T}
import datetime; doc["written_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(doc,open("/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave4/agent4_module_v/V_TARGETS.json","w"),indent=1)
print(len(T))
