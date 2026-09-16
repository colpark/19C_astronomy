#!/usr/bin/env python3
"""Build rubin_cohort_count.json (provenance records) and axis_ledger_rubin.json from the sealed count file and label_accrual.json."""
import json, hashlib, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
sha = lambda p: hashlib.sha256((D / p).read_bytes()).hexdigest()
S = json.load(open(D / "sealed/rubin_counts_SEALED.json")); LA = json.load(open(D / "label_accrual.json"))
c4rows = json.load(open(D / "out/c4_crossbroker.json"))["rows"]
s3 = sum(1 for r in c4rows if r["alerce_n_det"] == 1)
F = S["C1_fink"]["lower"]; A = S["C2_antares"]
SEAL = f"sealed/rubin_counts_SEALED.json sha256 {sha('sealed/rubin_counts_SEALED.json')}"
recs = [
 dict(id="rc-01", value={"O_lo": F["O_lo"], "O_hi": F["O_hi"]}, referent="distinct Rubin DIAObjects first detected at or after 2026-07-01T00:00 UTC (MJD TAI 61222.000428), whole alert stream, as new-object alerts",
      source=f"scripts/count_c1_fink.py over POST https://api.lsst.fink-portal.org/api/v1/statistics (out/raw/fink_stats_2026.json sha256 {S['C1_fink']['file_sha256']}), sum of f:is_first (minus f:is_sso for O_lo) over Fink nights >= 20260701; {SEAL}",
      population="9 Fink nights (UTC dates 20260701, 0706, 0707, 0709-0714) = dayObs 20260630 (part after T0) plus 0705, 0706, 0708-0713; unit = first-detection alert = one new DIAObject",
      adjudicator="ANTARES locus count on the same boundary, 1,908,703 (rc-02), which lies inside [O_lo, O_hi]; an enumerated diaObjectId count (ALeRCE C3) was interrupted at >= 189,641",
      falsifier="a complete enumeration of diaObjectIds with firstDiaSourceMjdTai >= 61222.000428 (PPDB, expected Sep-Oct 2026) returning a count outside [1,773,044, 2,018,299], or a rerun of the statistics query returning different sums"),
 dict(id="rc-02", value=A["cohort_T0_to_61300"]["loci"], referent="ANTARES loci carrying an LSST dia_object_id whose oldest alert is at or after MJD 61222.000428",
      source=f"scripts/count_c2_antares.py (amendment AM1) bisection over meta.count of GET https://api.antares.noirlab.edu/v1/loci; out/c2_antares.json sha256 {A['slices_file_sha256']}; {SEAL}",
      population="loci (ANTARES positional merge of ZTF and LSST alerts), not diaObjectIds; loci with a pre-boundary ZTF alert are excluded by construction",
      adjudicator="Fink first-detection bracket [1,773,044, 2,018,299] (rc-01); declared sample check C4 found 3000/3000 sampled ALeRCE oids in ANTARES with one locus each and no ZTF member",
      falsifier="a rerun of the bisection returning a different total, or a locus-level enumeration showing loci with multiple dia_object_ids at a rate that moves the diaObjectId count outside the Fink bracket"),
 dict(id="rc-03", value={"raw_alerts": F["alerts"], "overstatement_pct_range": [F["overstatement_pct_vs_O_hi"], F["overstatement_pct_vs_O_lo"]]}, referent="raw alerts on post-boundary nights beside distinct new objects, overstatement (raw-distinct)/distinct",
      source=f"scripts/count_c1_fink.py f:alerts sum, Fink nights >= 20260701; {SEAL}", population="all alerts issued on those nights, including alerts of objects first detected before the boundary, so an upper bound for the cohort",
      adjudicator="object-level sample C4 (3000 oids first detected in the first 0.25 d): sum n_det 3386 over 3000 objects = 12.9 percent, a within-window figure far below the whole-window one because young objects have few detections",
      falsifier="an enumerated cohort table whose summed nDiaSources gives an overstatement outside 74-98 percent after removing alerts of pre-boundary objects"),
 dict(id="rc-04", value=S["nights"]["M_obs_scheduler_dayObs_ge_20260629"], referent="LSSTCam nights (dayObs >= 20260629) with at least one science visit, the survey-night supply bound M_obs",
      source=f"scripts/nights_observed.py over https://s3df.slac.stanford.edu/data/rubin/sim-data/schedview/reports/schedview_reports_toc.html (sha256 {S['nights']['toc_sha256']}), LSST observing with lsstcam table",
      population="dayObs 20260629-20260824 rows of the LSST lsstcam table; 7267 science visits; last science night 20260713; no rows with science visits after 20260714; reports suspended during storm recovery",
      adjudicator="Fink statistics nights with alerts (11 UTC dates) match scheduler dayObs shifted by +1 day one-for-one, plus Fink night 20260629 which is pre-LSST dayObs 20260628; Rubin community post 2026-07-17 states 2669 science visits for dayObs 0710-0716, matching the scheduler sum 407+822+761+679+0",
      falsifier="a Rubin nightly summary or rerun measuring a count that differs, e.g. science visits on any dayObs between 20260715 and 20260916, or on 20260701-20260704 or 20260707"),
 dict(id="rc-05", value={"C3_alerce_distinct_lower_bound": 189641, "status": "UNDEMONSTRATED (interrupted)"}, referent="ALeRCE enumerated distinct LSST oids with firstmjd >= T0",
      source="scripts/count_c3_alerce.py (AM2, AM3), interrupted at 1018 requests, 82 of about 450 slices; out/c3_alerce.json, out/c3_progress.txt",
      population="ALeRCE object rows; 0.02 d slices on the 9 Fink alert dates", adjudicator="Fink and ANTARES whole-stream counts (rc-01, rc-02)",
      falsifier="a completed rerun of scripts/count_c3_alerce.py returning a distinct count below 189,641 would show a paging defect"),
 dict(id="rc-06", value={"S1_straddlers_lower_bound": 21126, "status": "UNDEMONSTRATED (interrupted, 2 incomplete slices)"}, referent="objects first detected before T0 with a detection at or after T0 (excluded from cohort by definition)",
      source="scripts/count_c5_straddlers.py (AM5), ALeRCE lastmjd filter verified by probe (997/997 rows lastmjd >= T0); interrupted through date 20260523", population="ALeRCE oids, firstmjd 2026-02-24..T0",
      adjudicator="C4 sample: 0 of 3000 cohort oids placed before T0 by Fink or ANTARES", falsifier="a completed rerun returning fewer than 21,126 straddlers, or any returned row with lastmjd < T0"),
 dict(id="rc-07", value=A["S0_TS_to_T0"]["loci"], referent="stratum S0: ANTARES LSST loci with oldest alert in [survey start 2026-06-29T12:00 UTC, T0), LSST objects not after every cutoff",
      source=f"scripts/count_c2_antares.py; out/c2_antares.json sha256 {A['slices_file_sha256']}", population="loci, as rc-02", adjudicator="Fink first detections on Fink nights 20260629-20260630: 171,559 (is_first 49,772+121,787), a different window edge (Fink 20260629 is pre-LSST dayObs 20260628)",
      falsifier="a rerun returning a different count"),
 dict(id="rc-08", value={"sampled": 3000, "in_all_three": S["C4_crossbroker"]["in_both"], "first_detection_disagree": 0, "ndet_disagree_fink_vs_alerce": S["C4_crossbroker"]["ndet_disagree_fink_vs_alerce"], "sum_n_det_alerce": 3386, "sum_nDiaSources_fink": 3227, "sum_num_alerts_antares": 3386, "S3_n_det_eq_1": s3, "S4_n_det_ge_2": 3000 - s3, "unprocessable": 0},
      referent="object-level cross-broker agreement on the declared sample W (first 3000 of 4841 ALeRCE oids first detected in [T0, T0+0.25 d))",
      source=f"scripts/count_c4_crossbroker.py (AM4); out/c4_crossbroker.json sha256 {S['C4_crossbroker']['file_sha256']}", population="3000 diaObjectIds, one row each",
      adjudicator="none stronger available; PPDB DiaObject table not public", falsifier="a rerun giving a different presence or nDiaSources disagreement count, or PPDB nDiaSources matching neither broker"),
 dict(id="rc-09", value="UNDEMONSTRATED", referent="P and Ng: cohort objects with a measured (spectroscopic, non-bot) positive or negative label",
      source="TNS API POST https://www.wis-tns.org/api/get/search -> HTTP 401 {\"id_code\":401,\"id_message\":\"Unauthorized\"}; search CSV and public objects zip also 401 (out/raw/tns_*.body); read after seal step 7 in order_of_operations.log",
      population="cohort objects (rc-01)", adjudicator="Fink statistics f:in_tns: 5,173 alerts on cohort nights have a TNS counterpart; alerts not objects, no reporter or class, so not a measured-label count",
      falsifier="TNS classification reports read with credentials returning a measured-label count; any count at all resolves this record"),
]
json.dump(recs,
          open(D / "rubin_cohort_count.json", "w"), indent=1)  # completeness assertion carried in axis_ledger_rubin.json
json.dump(recs, open(D / "out/provenance_records_flat.json", "w"), indent=1)
Olo, Ohi = F["O_lo"], F["O_hi"]
axes = [
 dict(axis="positive_supply", disposition="UNDEMONSTRATED", band="UNDEMONSTRATED (P uncomputable); CLOSE excluded because optimistic bound O >= 485", value={"P_measured_positive": "UNDEMONSTRATED", "O_optimistic_bound": [Olo, Ohi], "O_antares_loci": A["cohort_T0_to_61300"]["loci"], "M_obs": 10, "M_obs_cohort": "9 (8 whole dayObs + dayObs 20260630 after 00:00 UTC)", "M_sc": "UNDEMONSTRATED", "PROCEED_threshold": {"L": 12855, "M_sc": 1515}}, provenance=["rc-01", "rc-02", "rc-04", "rc-09"]),
 dict(axis="negative_supply", disposition="UNDEMONSTRATED", band="UNDEMONSTRATED (Ng uncomputable); CLOSE excluded because O >= 485", value={"Ng_measured_negative": "UNDEMONSTRATED", "negB": "UNDEMONSTRATED", "unlabelled_counted_as_negative": 0}, provenance=["rc-09"]),
 dict(axis="contamination_exposure", disposition="PASS (counted)", band="ESCALATE", value={"E_first_detected_after_every_demonstrated_cutoff": [Olo, Ohi], "E_labelled": "UNDEMONSTRATED", "subjects_without_cutoff": ["Gemini 3.1 Pro (preview)"], "S0_not_after_every_cutoff_loci": A["S0_TS_to_T0"]["loci"], "sample_loci_with_prior_ZTF_alert": "0 of 3000"}, note="ESCALATE because a subject lacks a published cutoff (band section 6); leaks host-z, archival variability, IAU prefix, web access to TNS listed, not banded", provenance=["rc-01", "rc-07", "rc-08"]),
 dict(axis="tool_coverage", disposition="PASS (counted, wave 1)", band="NOT RULABLE: band declared after the wave-1 count; no recount after bands hash", value={"verified_on_rubin": "0 of 25 (agent4 wave1 REPORT section 3)"}, provenance=["astronomy/agent4_tools_instrument/REPORT.md section 3"]),
 dict(axis="cluster_structure", disposition="PASS", band="PROCEED", value={"raw_alerts": F["alerts"], "distinct_first_detections": [Olo, Ohi], "overstatement_pct": [F["overstatement_pct_vs_O_hi"], F["overstatement_pct_vs_O_lo"]], "antares_loci": A["cohort_T0_to_61300"]["loci"], "alerce_distinct_lower_bound": 189641, "per_night_unique_objects_summed_NOT_distinct": F["objects_night_summed"], "sample_W_sum_ndet_over_objects": "3386/3000"}, note="brokers that serve counts place O in the same band (all >= 485); Fink O is an aggregate of first-detection alerts, not enumerated ids", provenance=["rc-01", "rc-02", "rc-03", "rc-05", "rc-08"]),
 dict(axis="split_integrity", disposition="UNDEMONSTRATED", band="UNDEMONSTRATED (count interrupted); any value <= O-485 would give PROCEED", value={"S1_straddlers_lower_bound": 21126, "sample_cross_broker_before_T0": "0 of 3000"}, provenance=["rc-06", "rc-08"]),
 dict(axis="unprocessable_units", disposition="UNDEMONSTRATED", band="UNDEMONSTRATED (whole-cohort table not obtained)", value={"U_sample_W": 0, "sample_size": 3000}, provenance=["rc-08"]),
]
ledger = dict(candidate="live time-domain astronomy: Rubin LSST prospective cohort (first detection >= 2026-07-01T00:00 UTC)", branch="prediction",
  bands="bands_FROZEN.md sha256 " + sha("bands_FROZEN.md"), sealed_counts=SEAL, ruling=None,
  ruling_refused_because=["precondition (a): positive_supply and negative_supply carry no number (measured labels unreadable, TNS HTTP 401)",
                          "precondition (b): tool_coverage band was declared after its only count (wave-1 0/25); no recount",
                          "precondition (c): label source not ratified at D5",
                          "split_integrity and unprocessable_units counts interrupted"],
  binding_axis="positive_supply (measured labels): needs TNS credentials (external input) and survey time (off sky since 2026-07-14, no return date as of 2026-09-11; BTS-side label collapse ruled POLICY, calibration only); second: contamination x supply (subject without cutoff)",
  label_collapse_ruling_calibration_only=LA["decision"]["ruling"],
  definition_widened=False, axes=axes,
  completeness="Seven axes listed for the Rubin cohort. Numbers: contamination (E=1.77-2.02M objects after every demonstrated cutoff), cluster structure (3.51M alerts vs 1.77-2.02M objects; ANTARES 1.91M loci), tool coverage (wave-1 0/25, not rulable). UNDEMONSTRATED: positive and negative measured supply (TNS 401), split integrity (C5 interrupted, >=21,126 straddlers), unprocessable units (sample 0/3000 only). Brokers not covered: Lasair (outage), Pitt-Google (credentials). P4 ruling refused; ruling field null by design.")
json.dump(ledger, open(D / "axis_ledger_rubin.json", "w"), indent=1)
print("ok", s3)
