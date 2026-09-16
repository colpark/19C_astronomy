#!/usr/bin/env python3
"""Build rubin_cohort_count.json (provenance records, wave 3) and axis_ledger_rubin_v2.json from the sealed wave-3 count file."""
import json, hashlib, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
sha = lambda p: hashlib.sha256((D / p).read_bytes()).hexdigest()
S = json.load(open(D / "sealed/rubin_counts_w3_SEALED.json")); M = S["merge"]; X = S["crosscheck_AM7"]; T = S["planning_thresholds_PLANNING_ONLY"]; W2 = S["carried_from_wave2"]
SEAL = f"sealed/rubin_counts_w3_SEALED.json sha256 {sha('sealed/rubin_counts_w3_SEALED.json')}"
BANDS = "astronomy/wave2/agent1_rubin_bands/bands_FROZEN.md sha256 8825ef8048b733b66e12f31ce16e67270de171f52f20f40ca8f21e5780e500d2"
O = M["O_merged"]
recs = [
 dict(id="w3-01", value=M["cohort_oids"], referent="distinct ALeRCE/LSST diaObjectIds (oid) with firstmjd >= MJD TAI 61222.000428 (2026-07-01T00:00 UTC), enumerated",
      source=f"scripts/w3_enumerate.py (count_protocol_w3_FROZEN.md, AM6) -> out/w3_c3_slices/*.csv rows sha256 {M['inputs']['w3_c3']['rows_sha256']}; 450/450 slices complete; {SEAL}",
      population="ALeRCE object rows on the 9 UTC dates with Fink alerts after T0, one row per oid (deduplicated)",
      adjudicator=f"Fink first-detection bracket [{W2['fink_first_detections_bracket'][0]}, {W2['fink_first_detections_bracket'][1]}] (wave 2 C1) and ANTARES {W2['antares_cohort_loci']} loci (wave 2 C2); wave-2 interrupted lower bound 189,641",
      falsifier="a rerun of scripts/w3_enumerate.py on the same ranges returning a different distinct count, or a PPDB DiaObject enumeration outside [1,773,044, 2,018,299]"),
 dict(id="w3-02", value=O, referent="cohort objects after X1-X3 merge (1 arcsec, first detections within 60 d), components whose earliest first detection is >= T0",
      source=f"scripts/w3_merge.py over W3-C3 plus W3-P60 (out/w3_p60_slices rows sha256 {M['inputs']['w3_p60']['rows_sha256']}, 1551/1551 slices); {SEAL}",
      population=f"{M['cohort_oids']} cohort oids plus {M['inputs']['w3_p60']['distinct']} oids first detected in [T0-60 d, T0); X2 pairs joined {M['X2_pairs_joined']}, X3 same-position distinct pairs {M['X3_same_position_distinct_pairs']}",
      adjudicator="ANTARES positional loci 1,908,703 (their own merge rule, includes ZTF); unmerged oid count w3-01",
      falsifier="a rerun of w3_merge.py on the same slice files returning a different O_merged, or a pair of distinct supernovae (different TNS names) found joined within 1 arcsec and 60 d"),
 dict(id="w3-03", value={"raw_detections_sum_n_det": M["cohort_raw_detections_sum_n_det"], "overstatement_pct_vs_oids": M["overstatement_pct_detections_vs_oids"], "fink_raw_alerts_cohort_nights": W2["fink_raw_alerts"], "fink_alert_overstatement_pct_vs_O_merged": round((W2["fink_raw_alerts"] - O) / O * 100, 1)},
      referent="raw detections and raw alerts beside distinct merged objects, overstatement (raw-distinct)/distinct",
      source=f"scripts/w3_merge.py n_det sum; wave-2 scripts/count_c1_fink.py f:alerts sum; {SEAL}",
      population="cohort oids (detections up to the query time, all after T0 since firstmjd >= T0); Fink alerts on cohort nights include alerts of pre-T0 objects",
      adjudicator="wave-2 sample: 3386 detections over 3000 early-window oids (12.9 percent)", falsifier="a PPDB DiaSource count per cohort object whose sum differs from 2,418,954 by more than the 409/9000 per-object nDiaSources disagreement rate allows"),
 dict(id="w3-04", value={"S3_one_detection_share_oids": M["S3_share_oids"], "S3_one_detection_oids": M["S3_one_detection_oids"], "S3_share_merged": M["S3_one_detection_share_merged"]},
      referent="cohort-wide share of objects with exactly one detection (stratum S3), S4 = complement",
      source=f"scripts/w3_merge.py (n_det == 1); {SEAL}", population=f"{M['cohort_oids']} cohort oids; {O} merged objects",
      adjudicator="Fink r:nDiaSources on the 9000-oid W3-X sample disagrees with ALeRCE n_det for 409 oids", falsifier="a rerun over the same slice files returning a different share, or PPDB nDiaSources giving a share outside 0.80-0.82"),
 dict(id="w3-05", value={"S1_total": M["S1_total_direct_plus_merge_oids"], "S1_direct_first_in_T0-60d_to_T0": M["S1_direct_firstmjd_T0minus60_to_T0"], "S1_direct_first_2026-02-24_to_T0-60d": M["S1_direct_firstmjd_20260224_to_T0minus60"], "S1_merge": M["S1_merge_oids"]},
      referent="stratum S1: objects with a DIASource detection before T0 and a detection at or after T0 (excluded from the cohort by definition), plus cohort oids pulled out by merging with a pre-T0 oid",
      source=f"scripts/w3_merge.py over W3-P60 (lastmjd >= T0) and W3-C5 (out/w3_c5_slices rows sha256 {M['inputs']['w3_c5']['rows_sha256']}, lastmjd filter, 1500/1500 slices, 0 rows violating filter); {SEAL}",
      population="ALeRCE oids first detected 2026-02-24..T0 on Fink alert dates", adjudicator="wave-2 interrupted lower bound 21,126 through UTC date 20260523; wave-3 value through that date 21,521",
      falsifier="a rerun giving a different S1, or any W3-C5 row with lastmjd < T0, or a PPDB DiaSource list showing pre-T0 detections for cohort oids"),
 dict(id="w3-06", value=M["unprocessable_U"], referent="unprocessable units U: rows lacking oid, position or first-detection time, or with declination outside [-90, 90]",
      source=f"scripts/w3_merge.py bad(); {SEAL}", population=f"{M['cohort_oids'] + M['inputs']['w3_p60']['distinct']} rows (W3-C3 plus W3-P60)",
      adjudicator="wave-2 sample 0/3000", falsifier="any row in out/w3_c3_slices or out/w3_p60_slices failing bad() on rerun"),
 dict(id="w3-07", value=X, referent="cross-broker and alert-history check on the declared sample (1000 lowest-sha1 oids per cohort UTC date)",
      source=f"scripts/w3_crosscheck.py (AM7 recompute) -> out/w3_crosscheck.json; {SEAL}", population="9000 cohort oids",
      adjudicator="Rubin APDB firstDiaSourceMjdTai, served null by Fink for 8986/8986 (UNDEMONSTRATED)", falsifier="a rerun giving different counts, or a served non-null Rubin firstDiaSourceMjdTai before T0 for any sampled oid"),
 dict(id="w3-08", value={"ppdb": "NOT RELEASED", "upper_bound_O": O, "precovery_effect": "forced-only precovery cannot create S1 (bands section 3); PPDB-only DIASources not documented; direction downward only; >= 99.34 percent of O must move to cross the 12,855 edge"},
      referent="PPDB release status on 2026-09-16 and its consequence for the cohort bound",
      source="out/w3_ppdb.json; sources/ppdb/SHA256SUMS (rtn-011.lsst.io v9.0 landing, Early Science page 'Target: Sep-Oct 2026', community topics 11546, 12345, 12346, News listing)",
      population="cohort O_merged", adjudicator="LDM-612 lines 473-477 (12-month alert history) and LSE-163 lines 950-955 (30-day forced precovery)",
      falsifier="a Rubin News post or RTN-011 revision, re-fetched, that differs by announcing PPDB release on or before 2026-09-16, or PPDB DIASources pre-dating T0 for more than 1,924,814 cohort objects"),
 dict(id="w3-09", value={"nights_family_A": T["nights_family_A"], "objects_family_B": T["objects_family_B"]}, referent="PLANNING-ONLY band-threshold quantities at delta 0.018 (literature prior) and 0.05 (PI override): min and max N_min over the synthetic sigma_d bracket",
      source=f"scripts/planning_mde_bracket_w3.py (agent 5 script, DELTAS changed only) running fm-advantage-benchmark/scripts/power.py; {T['file']}",
      population="16 night-unit rows and 16 object-unit rows, synthetic paired columns (not a P7 record)",
      adjudicator="wave-1 planning_mde_bracket.csv: 0.018 column reproduced with 0 differences over 32 rows", falsifier="a rerun of planning_mde_bracket_w3.py returning different N_min, or I1 compositions whose measured sigma_d falls outside the bracket"),
]
json.dump(recs, open(D / "rubin_cohort_count.json", "w"), indent=1, default=int)
th = T["objects_family_B"]; tn = T["nights_family_A"]
axes = [
 dict(axis="positive_supply", disposition="UNDEMONSTRATED", band_frozen_delta_0p018="UNDEMONSTRATED (P unread); CLOSE excluded (O >= 485)",
      at_delta_0p05_planning_only=f"PROCEED would need P >= 1 and L >= {th['0.05'][1]} or M_sc >= {tn['0.05'][1]}; CLOSE would need O < {th['0.05'][0]} and M_obs < {tn['0.05'][0]}; not a band",
      value={"P_measured": "UNDEMONSTRATED (labels are agent 2's; TNS BLOCKED per coordinator preamble)", "O_optimistic_bound": O, "M_obs": W2["M_obs"], "cohort_nights": W2["cohort_nights"], "M_sc": "UNDEMONSTRATED", "PROCEED_threshold_frozen": {"L": th["0.018"][1], "M_sc": tn["0.018"][1]}}, provenance=["w3-02", "w3-09"]),
 dict(axis="negative_supply", disposition="UNDEMONSTRATED", band_frozen_delta_0p018="UNDEMONSTRATED (Ng unread); CLOSE excluded (O >= 485)", value={"Ng_measured": "UNDEMONSTRATED", "unlabelled_counted_as_negative": 0}, provenance=["w3-02"]),
 dict(axis="contamination_exposure", disposition="PASS (counted)", band_frozen_delta_0p018="ESCALATE (a subject lacks a published cutoff: Gemini 3.1 Pro)",
      value={"E_first_detected_after_every_demonstrated_cutoff": O, "S0_excluded_loci": W2["antares_S0_loci"], "S1_excluded": M["S1_total_direct_plus_merge_oids"], "sample_loci_with_alert_history_before_T0_at_position_ANTARES": f"{X['antares_oldest_before_T0']}/{X['sample']} (gaps {X['antares_gap_days_quantiles'][0]}-{X['antares_gap_days_quantiles'][-1]} d; {X['antares_gap_le_60d']} within 60 d)"},
      note="the ANTARES older-alert loci are a listed leak (public alerts at the position before the cutoff), not S1 under the Rubin-diaObject definition", provenance=["w3-02", "w3-05", "w3-07"]),
 dict(axis="tool_coverage", disposition="UNDEMONSTRATED for this ledger", band_frozen_delta_0p018="NOT RULABLE here: the only count (wave-1 0/25) predates the band; agent 4's wave-3 recount had not landed when this ledger was built", value={"verified_on_rubin_wave1": "0 of 25"}, provenance=["astronomy/agent4_tools_instrument/REPORT.md section 3"]),
 dict(axis="cluster_structure", disposition="PASS", band_frozen_delta_0p018="PROCEED",
      value={"alerce_oids": M["cohort_oids"], "merged_objects": O, "raw_detections": M["cohort_raw_detections_sum_n_det"], "detections_overstatement_pct": M["overstatement_pct_detections_vs_oids"], "fink_raw_alerts": W2["fink_raw_alerts"], "fink_first_detection_bracket": W2["fink_first_detections_bracket"], "antares_loci": W2["antares_cohort_loci"]},
      note="every broker count lies in the same band (O >= 485 and >= 12,855)", provenance=["w3-01", "w3-02", "w3-03"]),
 dict(axis="split_integrity", disposition="PASS", band_frozen_delta_0p018="PROCEED",
      value={"S1_total": M["S1_total_direct_plus_merge_oids"], "S1_merge": M["S1_merge_oids"], "fink_alert_history_first_before_T0_sample": f"{X['fink_first_before_T0']}/{X['in_fink']}", "O_minus_all_listed_worst_case": O - round(X["antares_oldest_before_T0"] / X["sample"] * O)},
      note="S1 objects are outside O by definition; O minus the sample-scaled ANTARES older-locus share is still >= 12,855, so the band is unchanged. PPDB-only DIASources UNDEMONSTRATED (can only lower O; >= 99.34 percent would be needed to change band)", provenance=["w3-05", "w3-07", "w3-08"]),
 dict(axis="unprocessable_units", disposition="PASS", band_frozen_delta_0p018="PROCEED", value={"U": M["unprocessable_U"], "rows_checked": M["cohort_oids"] + M["inputs"]["w3_p60"]["distinct"], "coverage_limit_non_fink_dates": "UNDEMONSTRATED (HTTP 504), independent sources show no observations"}, provenance=["w3-06"]),
]
ledger = dict(candidate="live time-domain astronomy: Rubin LSST prospective cohort (first detection >= 2026-07-01T00:00 UTC)", branch="prediction", version="v2 (wave 3)",
  bands=BANDS, sealed_counts=SEAL, ruling=None,
  ruling_refused_because=["precondition (a) unmet: positive_supply and negative_supply carry no number (measured labels not read by this agent; TNS BLOCKED)",
                          "precondition (b) unmet in this ledger: tool_coverage recount after the band hash (agent 4, wave 3) not landed",
                          "precondition (c) unmet: label source not ratified (manifest freeze v2 pending, agent 3)"],
  preconditions_cleared_this_wave=["split_integrity, unprocessable_units and cluster_structure now carry complete numbers against frozen bands"],
  binding_axis=f"positive_supply at measured labels: frozen bands (delta 0.018) need L >= 12,855 or 1,515 scoreable nights; PLANNING-ONLY at the PI override delta 0.05 the upper bracket is {th['0.05'][1]} objects or {tn['0.05'][1]} nights; the cohort holds {O} unlabelled-to-this-agent objects over {W2['cohort_nights']} nights, off sky since 2026-07-14",
  delta_note="bands are frozen at delta 0.018; the PI override 0.05 is carried beside, planning-only, and a re-band at 0.05 is a new hashed registration for D5/agent 3, not made here",
  definition_widened=False, axes=axes,
  completeness="All seven axes listed for the Rubin cohort. Complete numbers: cluster_structure (1,937,720 oids, 1,937,669 merged, 2,418,954 detections), split_integrity (S1 521,920), unprocessable_units (U 0), contamination (E 1,937,669). UNDEMONSTRATED: positive and negative measured supply (labels, agent 2), tool_coverage recount (agent 4), PPDB-only DIASources, ALeRCE holdings on non-Fink dates (HTTP 504). Lasair and Pitt-Google not re-attempted this wave. P4 refused; ruling null by design.")
json.dump(ledger, open(D / "axis_ledger_rubin_v2.json", "w"), indent=1, default=int)
print("ok")
