# Diff v1 → v2 (both frozen in wave 3; published in wave 4)

- **From:** `astronomy/wave3/agent3_manifest_freeze/domain_manifest_v1.json`, frozen_hash `ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8`.
- **To:** `astronomy/wave3/agent3_manifest_freeze/domain_manifest_v2.json`, frozen_hash `fba4259b1d5931ff8b74a3db2f438706ce29263ef7ca373a2cb5c5fd7f2cedd5`.
- **Cause authority:** PANEL_BRIEF_WAVE3.md (sha256 a618d911...c4b6) rulings 1-6 and wave-3 fold-ins. Ledger ids refer to `amendment_ledger_v3.json` (append-only).
- **Method:** leaf-path comparison of the two frozen JSON files (frozen_hash and frozen_utc excluded). Every changed top-level key has one cause line; unchanged slots are listed as unchanged.

| Key | Status before → after | Leaves added / removed / changed | Cause |
|---|---|---|---|
| manifest |  (unchanged) | 0 / 0 / 0 | unchanged |
| manifest_version | - → - | 0 / 0 / 1 | version |
| governing_brief | - → - | 0 / 0 / 2 | v2 governed by PANEL_BRIEF_WAVE3.md |
| inputs_state | - → - | 0 / 0 / 1 | version |
| hash_method |  (unchanged) | 0 / 0 / 0 | unchanged |
| candidates | - → - | 85 / 1 / 0 | SU-V2-02, SU-V2-04 (cohort counts, supply lower bounds), axis ledger v2 final |
| tau | DERIVED (unchanged) | 0 / 0 / 0 | unchanged |
| k | RATIFIED (unchanged) | 0 / 0 / 0 | unchanged |
| label_source | UNDEMONSTRATED → UNDEMONSTRATED | 35 / 101 / 14 | SU-V2-03 (agent 2 wave-3 slot supersedes wave-2 slot; bound [803,2247] -> [954,2057]); PENDING-V2-01 resolved. PANEL_BRIEF_WAVE3.md Assignments, Agent 2 and Agent 3 |
| exposure_key | DERIVED → DERIVED | 9 / 0 / 0 | SU-V2-02 (agent 1 wave-3 leak, PPDB, Rubin first-time field) and agent 2 wave-3 position leak; PANEL_BRIEF_WAVE3.md Assignments, Agent 1 and 2 |
| tool_inventory | OVERRIDDEN → OVERRIDDEN | 130 / 0 / 0 | SU-V2-01 (agent 4 wave-3 functional recount, remap consistency); PANEL_BRIEF_WAVE3.md Assignments, Agent 4 |
| delta | DERIVED → OVERRIDDEN | 56 / 34 / 14 | AMD-V2-04 (PI ruling 2: OVERRIDDEN 0.018 -> 0.05, prior carried); PANEL_BRIEF_WAVE3.md lines 18-19 |
| S | UNDEMONSTRATED → UNDEMONSTRATED | 10 / 0 / 2 | AMD-V2-01, AMD-V2-02 (ruling 1: budget supplied, S computed at R1, re-ratification gate); PANEL_BRIEF_WAVE3.md line 13 |
| subject_set | DERIVED (unchanged) | 0 / 0 / 0 | unchanged |
| decision_epoch | RATIFIED → RATIFIED | 14 / 0 / 2 | AMD-V2-08 (ruling 6: reaffirmed; strata S0/S1/S2 with S2 disagreement); PANEL_BRIEF_WAVE3.md line 23 |
| supplied_by_human | - → - | 0 / 0 / 4 | AMD-V2-01, 03, 06, 07 (rulings 1, 2, 4, 5); PANEL_BRIEF_WAVE3.md lines 13-22 |
| d5_inputs | - → - | 8 / 18 / 24 | AMD-V2-01, 03, 06, 07 (records rebuilt from rulings 1, 2, 4, 5) |
| graph_escalations | - → - | 2 / 1 / 5 | AMD-V2-05 (ruling 3: escalation RATIFIED as staged); PANEL_BRIEF_WAVE3.md line 20 |
| amendment_ledger | - → - | 16 / 10 / 0 | ledger pointer updated for v2 entries |
| d5_disposition | - → - | 0 / 2 / 4 | consequence of the v2 slot statuses (no PI ruling on tau, exposure_key, subject_set) |
| completeness | - → - | 0 / 0 / 1 | restated for v2 |
| derived_from | - → - | 4 / 1 / 0 | version lineage |
| disagreements_v2 | - → - | 9 / 1 / 0 | new wave-3 disagreements (S2, truth-cost target, metric vs cost, JSON rows, run count, agent 2 items) |
| pi_reratification_inputs | - → - | 92 / 1 / 0 | SU-V2-05 (truth cost attached for ruling 1 re-ratification) |

## manifest_version

**Cause:** version

- **changed** (1):
  - `$`: `"v1"` → `"v2"`

## governing_brief

**Cause:** v2 governed by PANEL_BRIEF_WAVE3.md

- **changed** (2):
  - `$.path`: `"astronomy/wave2/PANEL_BRIEF_WAVE2.md"` → `"astronomy/wave3/PANEL_BRIEF_WAVE3.md"`
  - `$.sha256`: `"31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb"` → `"a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6"`

## inputs_state

**Cause:** version

- **changed** (1):
  - `$`: `"every slot as it stood at the end of wave 2; no wave-3 ruling or count enters v1"` → `"v1 plus wave-3 PI rulings 1-6, wave-3 counts from agent 1 (cohort, axes), agent 4 (too...`

## candidates

**Cause:** SU-V2-02, SU-V2-04 (cohort counts, supply lower bounds), axis ledger v2 final

- **added** (85):
  - `$[0].cohorts.prospective_counts_w3.O_merged`: `1937669`
  - `$[0].cohorts.prospective_counts_w3.S1`: `521920`
  - `$[0].cohorts.prospective_counts_w3.U`: `0`
  - `$[0].cohorts.prospective_counts_w3.alerce_oids`: `1937720`
  - `$[0].cohorts.prospective_counts_w3.cohort_nights`: `9`
  - `$[0].cohorts.prospective_counts_w3.one_detection_share`: `0.8082`
  - `$[0].cohorts.prospective_counts_w3.record.path`: `"astronomy/wave3/agent1_cohort_finish/rubin_cohort_count.json"`
  - `$[0].cohorts.prospective_counts_w3.record.sha256`: `"57cf41895fac0f5493d6cdb1efb8aea6499daa935479bf500cd031543c79ddde"`
  - `$[0].p4_state_v2`: `"no ruling; astronomy/wave3/agent3_manifest_freeze/axis_ledger_v2_final_against_frozen_...`
  - `$[0].prospective_label_supply_w3.automation_2026`: `"20 of 181 spectroscopic units SNIascore (all ZTF); 0 CCSNscore; 0 Syncatto"`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-01.nonbot_measured_units`: `17`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-01.objects_first_classified`: `23`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-01.rubin_cohort_strong`: `"n/a (cohort starts 2026-07-01)"`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-01.spectroscopic_units`: `24`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-02.nonbot_measured_units`: `2`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-02.objects_first_classified`: `2`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-02.rubin_cohort_strong`: `"n/a (cohort starts 2026-07-01)"`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-02.spectroscopic_units`: `2`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-03.nonbot_measured_units`: `19`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-03.objects_first_classified`: `18`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-03.rubin_cohort_strong`: `"n/a (cohort starts 2026-07-01)"`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-03.spectroscopic_units`: `20`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-04.nonbot_measured_units`: `10`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-04.objects_first_classified`: `13`
  - `$[0].prospective_label_supply_w3.per_month_lower_bound.2026-04.rubin_cohort_strong`: `"n/a (cohort starts 2026-07-01)"`
  - ... 60 more (reproduce with scripts/diffs.py)
- **removed** (1):
  - `$[0].p4_state_at_v1`: `"no ruling; preconditions (a) supply without measured labels, (b) tool coverage not rec...`

## label_source

**Cause:** SU-V2-03 (agent 2 wave-3 slot supersedes wave-2 slot; bound [803,2247] -> [954,2057]); PENDING-V2-01 resolved. PANEL_BRIEF_WAVE3.md Assignments, Agent 2 and Agent 3

- **changed** (14):
  - `$.override_invitation`: `"Override invitation: accept, or replace the value and give a reason; the reason enters...` → `"Override invitation: accept the bounded state (UNDEMONSTRATED), supply TNS credentials...`
  - `$.provenance.adjudicator`: `"authenticated TNS classification reports for every object (TNS API or bulk CSV with a ...` → `"authenticated TNS classification reports per object (TNS_API_KEY BLOCKED)"`
  - `$.provenance.falsifier`: `"an authenticated TNS report list showing more than 2247 or fewer than 803 BTS 'SN Ia' ...` → `"an authenticated report list returning more than 2057 or fewer than 954 BTS plain SN I...`
  - `$.provenance.population`: `"7843 BTS rows with type != '-' (unique ZTFID, pre-clustering; Agent 1 owns clustering;...` → `"7,843 labeled BTS rows (pre-clustering) and Rubin cohort objects first detected >= 202...`
  - `$.provenance.referent`: `"basis of each BTS object's current type label: human spectroscopic classification (MEA...` → `"basis of BTS type labels (measured vs model annotation) with the SNIascore bound, and ...`
  - `$.provenance.source`: `"astronomy/wave2/agent2_label_source/scripts/split_labels.py::main (bounds block); astr...` → `"astronomy/wave3/agent2_measured_labels/scripts/track1_bound.py (imports wave-2 common....`
  - `$.source_records[0].path`: `"astronomy/wave2/agent2_label_source/label_source_slot.json"` → `"astronomy/wave3/agent2_measured_labels/label_source_slot.json"`
  - `$.source_records[0].sha256`: `"01ef18a98fcfd59fcb75853bbee2f6dd4e3b2d15dd3d80583535699850ce00ce"` → `"fdae64921d6749e466932d13ffd0aa4e14359b0a946a31b32bacf9a97ce83719"`
  - `$.source_records[1].path`: `"astronomy/agent3_labels_exposure/label_source_slot.json"` → `"astronomy/wave3/agent2_measured_labels/REPORT.md"`
  - `$.source_records[1].sha256`: `"09e8dff5ac6f246629feb77c6689b4b0d443ef1595f8dcf2553d08e3ad28bc82"` → `"934b7fba7579676947bd0d2edab5a78d7fd431908e62d1cdc69414fa9ba74333"`
  - `$.status_note`: `"Per-object split is DERIVED only where public archived TNS evidence exists; 6156 of 78...` → `"BTS per-object split still incomplete (5815 of 7,843 unresolved); Rubin cohort measure...`
  - `$.supersedes.file`: `"astronomy/agent3_labels_exposure/label_source_slot.json"` → `"astronomy/wave2/agent2_label_source/label_source_slot.json"`
  - `$.supersedes.sha256`: `"09e8dff5ac6f246629feb77c6689b4b0d443ef1595f8dcf2553d08e3ad28bc82"` → `"01ef18a98fcfd59fcb75853bbee2f6dd4e3b2d15dd3d80583535699850ce00ce"`
  - `$.supersedes.what_changes`: `"SNIascore bound tightened; per-object measured/annotation/photometric/unresolved split...` → `"BTS SNIascore bound tightened from [803, 2247] to [954, 2057] by 345 further public ar...`
- **added** (35):
  - `$.source_records[2].locator`: `"superseded"`
  - `$.source_records[2].path`: `"astronomy/wave2/agent2_label_source/label_source_slot.json"`
  - `$.source_records[2].sha256`: `"01ef18a98fcfd59fcb75853bbee2f6dd4e3b2d15dd3d80583535699850ce00ce"`
  - `$.value.bts.category_counts.MEASURED`: `1074`
  - `$.value.bts.category_counts.MODEL_ANNOTATION`: `954`
  - `$.value.bts.category_counts.PHOTOMETRIC_ONLY`: `0`
  - `$.value.bts.category_counts.UNRESOLVED_UNDEMONSTRATED`: `5815`
  - `$.value.bts.population`: `7843`
  - `$.value.bts.sniascore_bound.lower`: `954`
  - `$.value.bts.sniascore_bound.new_captures.failed_retries`: `7`
  - `$.value.bts.sniascore_bound.new_captures.http_error`: `38`
  - `$.value.bts.sniascore_bound.new_captures.ok`: `345`
  - `$.value.bts.sniascore_bound.new_measured`: `190`
  - `$.value.bts.sniascore_bound.new_sniascore_strong`: `151`
  - `$.value.bts.sniascore_bound.previous[0]`: `803`
  - `$.value.bts.sniascore_bound.previous[1]`: `2247`
  - `$.value.bts.sniascore_bound.rule`: `"L' = 803 + new E1 SNIascore placements; U' = 2247 - new E1 non-SNIascore placements am...`
  - `$.value.bts.sniascore_bound.status`: `"DERIVED"`
  - `$.value.bts.sniascore_bound.upper`: `2057`
  - `$.value.bts.sniascore_bound.upper_noE5_sensitivity_not_slot_value`: `2654`
  - `$.value.bts.sniascore_bound.wave1[0]`: `0`
  - `$.value.bts.sniascore_bound.wave1[1]`: `3131`
  - `$.value.rubin_cohort.automation_share_2026_T1`: `"20 of 181 spectroscopic 2026 units carry SNIascore (all ZTF); 0 CCSNscore; 0 Syncatto"`
  - `$.value.rubin_cohort.existence_classified_moderate`: `13`
  - `$.value.rubin_cohort.existence_transients_moderate`: `12`
  - ... 10 more (reproduce with scripts/diffs.py)
- **removed** (101):
  - `$.source_records[1].locator`: `"superseded; class-level shares carried"`
  - `$.value.category_by_strength[0].category`: `"MEASURED"`
  - `$.value.category_by_strength[0].n`: `884`
  - `$.value.category_by_strength[0].strength`: `"STRONG"`
  - `$.value.category_by_strength[1].category`: `"MODEL_ANNOTATION"`
  - `$.value.category_by_strength[1].n`: `4`
  - `$.value.category_by_strength[1].strength`: `"MODERATE"`
  - `$.value.category_by_strength[2].category`: `"MODEL_ANNOTATION"`
  - `$.value.category_by_strength[2].n`: `799`
  - `$.value.category_by_strength[2].strength`: `"STRONG"`
  - `$.value.category_by_strength[3].category`: `"UNRESOLVED (UNDEMONSTRATED)"`
  - `$.value.category_by_strength[3].n`: `6156`
  - `$.value.category_by_strength[3].strength`: `""`
  - `$.value.category_counts.MEASURED`: `884`
  - `$.value.category_counts.MODEL_ANNOTATION`: `803`
  - `$.value.category_counts.PHOTOMETRIC_ONLY`: `0`
  - `$.value.category_counts.UNRESOLVED_UNDEMONSTRATED`: `6156`
  - `$.value.ccsnscore_bound.ccsnscore_reports_found_discovered_before_cut`: `0`
  - `$.value.ccsnscore_bound.lower`: `0`
  - `$.value.ccsnscore_bound.note`: `"upper counts CC-class objects discovered >= 2025-02-09 not excluded by E1; start date ...`
  - `$.value.ccsnscore_bound.population`: `1604`
  - `$.value.ccsnscore_bound.status`: `"UNDEMONSTRATED (start date unknown)"`
  - `$.value.ccsnscore_bound.upper`: `155`
  - `$.value.ccsnscore_bound.upper_before_E1`: `155`
  - `$.value.fetch_status.failed_retries`: `22`
  - ... 76 more (reproduce with scripts/diffs.py)

## exposure_key

**Cause:** SU-V2-02 (agent 1 wave-3 leak, PPDB, Rubin first-time field) and agent 2 wave-3 position leak; PANEL_BRIEF_WAVE3.md Assignments, Agent 1 and 2

- **added** (9):
  - `$.wave3_additions.agent2_position_leak`: `"ANTARES matches 7 supernovae discovered 2025-02..2026-04 at cohort positions (agent 2 ...`
  - `$.wave3_additions.ppdb`: `"NOT RELEASED as of 2026-09-16; cohort O = 1,937,669 is an upper bound (PPDB-only detec...`
  - `$.wave3_additions.prior_position_leak`: `"193 of 9,000 sampled cohort ids have an ANTARES alert at the same position before the ...`
  - `$.wave3_additions.record.locator`: `"w3-07, w3-08"`
  - `$.wave3_additions.record.path`: `"astronomy/wave3/agent1_cohort_finish/rubin_cohort_count.json"`
  - `$.wave3_additions.record.sha256`: `"57cf41895fac0f5493d6cdb1efb8aea6499daa935479bf500cd031543c79ddde"`
  - `$.wave3_additions.rubin_first_detection_field`: `"Fink serves r:firstDiaSourceMjdTai as null for 8,986/8,986 sampled ids; Rubin-side fir...`
  - `$.wave3_additions.tns`: `"BLOCKED; label public dates remain bracketed"`
  - `$.wave3_additions.tns_discovery_proxy`: `"SN2017bde and AT2019czs remain counterexamples to the discovery-date lower bound"`

## tool_inventory

**Cause:** SU-V2-01 (agent 4 wave-3 functional recount, remap consistency); PANEL_BRIEF_WAVE3.md Assignments, Agent 4

- **added** (130):
  - `$.rubin_functional_recount_w3.counts.FM/deep.FAIL`: `9`
  - `$.rubin_functional_recount_w3.counts.FM/deep.PASS`: `1`
  - `$.rubin_functional_recount_w3.counts.FM/deep.UNDEMONSTRATED`: `5`
  - `$.rubin_functional_recount_w3.counts.all.FAIL`: `14`
  - `$.rubin_functional_recount_w3.counts.all.PASS`: `2`
  - `$.rubin_functional_recount_w3.counts.all.UNDEMONSTRATED`: `9`
  - `$.rubin_functional_recount_w3.counts.classical.FAIL`: `5`
  - `$.rubin_functional_recount_w3.counts.classical.PASS`: `1`
  - `$.rubin_functional_recount_w3.counts.classical.UNDEMONSTRATED`: `4`
  - `$.rubin_functional_recount_w3.disagreements[0]`: `"AstroM3: wave-1 UNAVAILABLE (no weights) vs weights public on HF rev 8904ed33 (agent 4...`
  - `$.rubin_functional_recount_w3.disagreements[1]`: `"preamble item 5 'no substitute format is improvised' vs runs on JSON rows (listed in a...`
  - `$.rubin_functional_recount_w3.note`: `"wave-1 structural counts (value.summary) are unchanged; the recount is functional and ...`
  - `$.rubin_functional_recount_w3.packet_format_qualifier`: `"No public endpoint served lsst v11_1 Avro packets (Fink /api/v1/sources output-format=...`
  - `$.rubin_functional_recount_w3.per_tool.ALeRCE_BHRF.alerts_run`: `10`
  - `$.rubin_functional_recount_w3.per_tool.ALeRCE_BHRF.disposition`: `"FAIL"`
  - `$.rubin_functional_recount_w3.per_tool.ALeRCE_BHRF.passes`: `0`
  - `$.rubin_functional_recount_w3.per_tool.ALeRCE_BHRF.rubin_counterparts_after_remap`: `[]`
  - `$.rubin_functional_recount_w3.per_tool.ATAT.alerts_run`: `0`
  - `$.rubin_functional_recount_w3.per_tool.ATAT.disposition`: `"UNDEMONSTRATED"`
  - `$.rubin_functional_recount_w3.per_tool.ATAT.passes`: `0`
  - `$.rubin_functional_recount_w3.per_tool.ATAT.rubin_counterparts_after_remap[0]`: `"Fink_EarlySNIa_RF"`
  - `$.rubin_functional_recount_w3.per_tool.ATAT.rubin_counterparts_after_remap[1]`: `"Fink_SLSN_RF"`
  - `$.rubin_functional_recount_w3.per_tool.AppleCiDEr.alerts_run`: `0`
  - `$.rubin_functional_recount_w3.per_tool.AppleCiDEr.disposition`: `"UNDEMONSTRATED"`
  - `$.rubin_functional_recount_w3.per_tool.AppleCiDEr.passes`: `0`
  - ... 105 more (reproduce with scripts/diffs.py)

## delta

**Cause:** AMD-V2-04 (PI ruling 2: OVERRIDDEN 0.018 -> 0.05, prior carried); PANEL_BRIEF_WAVE3.md lines 18-19

- **changed** (14):
  - `$.override_invitation`: `"Override invitation: accept, or replace the value and give a reason; the reason enters...` → `"Override invitation: accept 0.05, or state a different value with its cause; the liter...`
  - `$.provenance.adjudicator`: `"the fully-connected metadata-only network (NN) on the same test split, the strongest o...` → `"literature prior 0.018 (arXiv:2401.15167 Table 6), carried beside; its unpaired MDE ab...`
  - `$.provenance.falsifier`: `"a rerun of the three published architectures (github.com/nabeelre/BTSbot) on a fresh c...` → `"a PI restatement of the switching cost, or a P7 power record whose MDE at the budgeted...`
  - `$.provenance.population`: `"BTSbot test split: 512 bright-transient sources and 1,489 other sources (Figure 4, lin...` → `"the programme's follow-up allocation decision, one committed set of k=8 per night; app...`
  - `$.provenance.referent`: `"absolute difference in purity (precision) of the set of sources selected for SEDM foll...` → `"smallest improvement in committed-set purity (precision at k) that would change which ...`
  - `$.provenance.source`: `"arXiv:2401.15167v1 Appendix B Table 6, sources/2401.15167.txt lines 1323-1335 (bts_p2 ...` → `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...`
  - `$.source_records[0].path`: `"astronomy/agent5_resolution_replay/delta_slot.json"` → `"astronomy/wave3/PANEL_BRIEF_WAVE3.md"`
  - `$.source_records[0].sha256`: `"435589df327ab3814aafb21e2fbe944be3205b62eda242788af4ef20a76ee99a"` → `"a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6"`
  - `$.source_records[1].path`: `"astronomy/agent5_resolution_replay/REPORT.md"` → `"astronomy/wave3/agent4_tool_recount/power_calibration_delta005.json"`
  - `$.source_records[1].sha256`: `"dc34bfcbc8f903bf3970a74cf6eb9f98a467f18794754e21994dbeca4a5b3c16"` → `"0258c82e68c51cb3f764f4c00d992a580627939142422f4ad17391e6e00f5fa2"`
  - `$.source_records[2].path`: `"astronomy/wave2/agent4_instrument/power_calibration.json"` → `"astronomy/wave3/agent1_cohort_finish/planning_mde_bracket_w3.csv"`
  - `$.source_records[2].sha256`: `"e02fd0f2a9d608abb7f814d321d3caa1669767318a16886da04b126c63937f8d"` → `"362130b15d4fe093052b16fcbbe300d391e5b977007bd8f917d893f5cc687667"`
  - `$.status`: `"DERIVED"` → `"OVERRIDDEN"`
  - `$.value`: `0.018` → `0.05`
- **added** (56):
  - `$.calibration_context.primary_E1_binding_nights.mde`: `0.0322`
  - `$.calibration_context.primary_E1_binding_nights.n_min_at_0.018`: `196`
  - `$.calibration_context.primary_E1_binding_nights.n_min_at_0.05`: `26`
  - `$.calibration_context.primary_E1_binding_nights.ruling_at_0.018`: `"CLOSE_UNRESOLVABLE"`
  - `$.calibration_context.primary_E1_binding_nights.ruling_at_0.05`: `"RESOLVABLE"`
  - `$.calibration_context.record.path`: `"astronomy/wave3/agent4_tool_recount/power_calibration_delta005.json"`
  - `$.calibration_context.record.sha256`: `"0258c82e68c51cb3f764f4c00d992a580627939142422f4ad17391e6e00f5fa2"`
  - `$.calibration_context.status`: `"PRE-I1 CALIBRATION on BTS (contamination FAIL); not P7"`
  - `$.carry_both`: `"every P7 table reports delta 0.05 and 0.018 side by side (ruling 2)"`
  - `$.literature_prior.candidates_listed[0].adjudicator`: `"human scanners, the incumbent"`
  - `$.literature_prior.candidates_listed[0].disposition`: `"REFUSED as a delta: an aggregate across unequal denominators (SKILL.md global refusal ...`
  - `$.literature_prior.candidates_listed[0].falsifier`: `"the same paper states scanner triggering purity as 95.6% at line 806 and 96.7% at line...`
  - `$.literature_prior.candidates_listed[0].id`: `"delta-candidate-btsbot-vs-scanners"`
  - `$.literature_prior.candidates_listed[0].population`: `"unequal: test-split sources for BTSbot versus a 41-night window of scanner triggers, w...`
  - `$.literature_prior.candidates_listed[0].referent`: `"difference in follow-up purity between the adopted automated selector and human scanners"`
  - `$.literature_prior.candidates_listed[0].source`: `"arXiv:2401.15167v1 section 4.1 lines 757-766 (scanner triggering purity 96.7%, 316 of ...`
  - `$.literature_prior.candidates_listed[0].value`: `-0.037`
  - `$.literature_prior.candidates_listed[1].adjudicator`: `"SNID, the incumbent template matcher, on the same spectra"`
  - `$.literature_prior.candidates_listed[1].disposition`: `"adjacent referent: classification of a spectrum already taken, not selection of which ...`
  - `$.literature_prior.candidates_listed[1].falsifier`: `"a rerun on the 2020 testing set (1,011 spectra of 632 transients) giving a TPR gap bel...`
  - `$.literature_prior.candidates_listed[1].id`: `"delta-candidate-sniascore-vs-snid"`
  - `$.literature_prior.candidates_listed[1].population`: `"BTS18 validation sample, 1,016 SEDM spectra of 648 SNe (lines 190-196), paired on the ...`
  - `$.literature_prior.candidates_listed[1].referent`: `"difference in true-positive rate at false-positive rate below 1% for SN Ia classificat...`
  - `$.literature_prior.candidates_listed[1].source`: `"arXiv:2104.12980v2 Table 2, sources/2104.12980.txt lines 387-407 (TPR 0.90 versus 0.53...`
  - `$.literature_prior.candidates_listed[1].value`: `0.37`
  - ... 31 more (reproduce with scripts/diffs.py)
- **removed** (34):
  - `$.candidates_listed[0].adjudicator`: `"human scanners, the incumbent"`
  - `$.candidates_listed[0].disposition`: `"REFUSED as a delta: an aggregate across unequal denominators (SKILL.md global refusal ...`
  - `$.candidates_listed[0].falsifier`: `"the same paper states scanner triggering purity as 95.6% at line 806 and 96.7% at line...`
  - `$.candidates_listed[0].id`: `"delta-candidate-btsbot-vs-scanners"`
  - `$.candidates_listed[0].population`: `"unequal: test-split sources for BTSbot versus a 41-night window of scanner triggers, w...`
  - `$.candidates_listed[0].referent`: `"difference in follow-up purity between the adopted automated selector and human scanners"`
  - `$.candidates_listed[0].source`: `"arXiv:2401.15167v1 section 4.1 lines 757-766 (scanner triggering purity 96.7%, 316 of ...`
  - `$.candidates_listed[0].value`: `-0.037`
  - `$.candidates_listed[1].adjudicator`: `"SNID, the incumbent template matcher, on the same spectra"`
  - `$.candidates_listed[1].disposition`: `"adjacent referent: classification of a spectrum already taken, not selection of which ...`
  - `$.candidates_listed[1].falsifier`: `"a rerun on the 2020 testing set (1,011 spectra of 632 transients) giving a TPR gap bel...`
  - `$.candidates_listed[1].id`: `"delta-candidate-sniascore-vs-snid"`
  - `$.candidates_listed[1].population`: `"BTS18 validation sample, 1,016 SEDM spectra of 648 SNe (lines 190-196), paired on the ...`
  - `$.candidates_listed[1].referent`: `"difference in true-positive rate at false-positive rate below 1% for SN Ia classificat...`
  - `$.candidates_listed[1].source`: `"arXiv:2104.12980v2 Table 2, sources/2104.12980.txt lines 387-407 (TPR 0.90 versus 0.53...`
  - `$.candidates_listed[1].value`: `0.37`
  - `$.candidates_listed[2].adjudicator`: `"random sampling, same pool, 100 realizations"`
  - `$.candidates_listed[2].disposition`: `"population FAIL: counted over alerts, with three different test-set sizes in one paper...`
  - `$.candidates_listed[2].falsifier`: `"a per-object (not per-alert) recount whose efficiency gap falls below 0.15"`
  - `$.candidates_listed[2].id`: `"delta-candidate-fink-us-vs-rs"`
  - `$.candidates_listed[2].population`: `"test sample counted in alerts: 23,530 (abstract line 40), 23,425 (line 540) and 23,465...`
  - `$.candidates_listed[2].referent`: `"difference in SN Ia efficiency at similar purity between uncertainty sampling and rand...`
  - `$.candidates_listed[2].source`: `"arXiv:2111.11438v2 Table 2, sources/2111.11438.txt lines 437-460 (efficiency 0.54 vers...`
  - `$.candidates_listed[2].value`: `0.3`
  - `$.disagreements[0]`: `"an order of magnitude separates the values practitioners acted on: 0.018 (selection pu...`
  - ... 9 more (reproduce with scripts/diffs.py)

## S

**Cause:** AMD-V2-01, AMD-V2-02 (ruling 1: budget supplied, S computed at R1, re-ratification gate); PANEL_BRIEF_WAVE3.md line 13

- **changed** (2):
  - `$.provenance.source`: `"references/manifest.md ('S, the survivor target, is budget divided by measured hours p...` → `"references/manifest.md ('S, the survivor target, is budget divided by measured hours p...`
  - `$.status_note`: `"budget unfilled (SUPPLY) and hours per workflow unmeasured (R1 not run)"` → `"Budget now SUPPLIED (1,000 arm cells hard cap + 200 engineering hours, AMD-V2-01). S s...`
- **added** (10):
  - `$.gates[0]`: `"ruling 1: no Rubin-era paid work starts without re-ratification against this wave's me...`
  - `$.planning_arithmetic_not_S.cell_definition`: `"one cell = one subject x one arm x one round (astronomy/agent5_resolution_replay/d5_in...`
  - `$.planning_arithmetic_not_S.compare`: `"planning N_min at delta 0.05: 6-197 nights or 63-1,666 objects; calibration N_min 26 b...`
  - `$.planning_arithmetic_not_S.r1_reserve_cells`: `"3 (r1_spec.md section 6)"`
  - `$.planning_arithmetic_not_S.rounds_affordable_if_1_subject_x_2_agent_arms`: `"floor((1000-3)/2) = 498"`
  - `$.planning_arithmetic_not_S.rounds_affordable_if_7_subjects_x_2_agent_arms`: `"floor((1000-3)/14) = 71"`
  - `$.planning_arithmetic_not_S.status`: `"PLANNING-ONLY; the mechanical composition arm consumes no subject cells; hours per wor...`
  - `$.source_records[2].locator`: `"ruling 1"`
  - `$.source_records[2].path`: `"astronomy/wave3/PANEL_BRIEF_WAVE3.md"`
  - `$.source_records[2].sha256`: `"a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6"`

## decision_epoch

**Cause:** AMD-V2-08 (ruling 6: reaffirmed; strata S0/S1/S2 with S2 disagreement); PANEL_BRIEF_WAVE3.md line 23

- **changed** (2):
  - `$.provenance.source`: `"PANEL_BRIEF_WAVE2.md sha256 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7...` → `"PANEL_BRIEF_WAVE2.md sha256 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7...`
  - `$.status_note`: `"AMD-V1-02. New D4 slot, ratified at declaration. Strata S0-S4 for the Rubin cohort are...` → `"Ratified at v1 (AMD-V1-02) and reaffirmed by PI ruling 6 (AMD-V2-08) with strata S0, S...`
- **added** (14):
  - `$.source_records[3].locator`: `"ruling 6"`
  - `$.source_records[3].path`: `"astronomy/wave3/PANEL_BRIEF_WAVE3.md"`
  - `$.source_records[3].sha256`: `"a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6"`
  - `$.strata.S0.count`: `"112,990 ANTARES loci (wave 2 C2)"`
  - `$.strata.S0.definition`: `"first detection in [survey start 2026-06-29T12:00, admission boundary 2026-07-01T00:00...`
  - `$.strata.S0.in_cohort`: `false`
  - `$.strata.S1.count`: `521920`
  - `$.strata.S1.definition`: `"straddlers: a DIASource detection before the boundary and one at or after it"`
  - `$.strata.S1.in_cohort`: `false`
  - `$.strata.S2.count`: `"UNDEMONSTRATED (needs PPDB, not released)"`
  - `$.strata.S2.definition`: `"cohort objects with pre-boundary forced flux S/N >= 5"`
  - `$.strata.S2.in_cohort_per_frozen_bands`: `true`
  - `$.strata.S2.per_ruling_6`: `"excluded"`
  - `$.strata.disagreement`: `"bands_FROZEN.md section 3 declares S2 (cohort objects with pre-boundary forced flux) '...`

## supplied_by_human

**Cause:** AMD-V2-01, 03, 06, 07 (rulings 1, 2, 4, 5); PANEL_BRIEF_WAVE3.md lines 13-22

- **changed** (4):
  - `$.budget`: `"UNDEMONSTRATED: arrived as unfilled '[SUPPLY: arm cells or hours]' (PANEL_BRIEF_WAVE2....` → `"SUPPLIED (AMD-V2-01): 1,000 agent arm cells for the calibration phase, hard cap, plus ...`
  - `$.cost_of_action`: `"UNDEMONSTRATED: arrived as unfilled '[SUPPLY: value of one SEDM spectrum hour and of a...` → `"SUPPLIED (AMD-V2-03): one spectrum = 0.5 h P60-class time; wrong routine commitment = ...`
  - `$.rulings_holder`: `"UNDEMONSTRATED: arrived as unfilled '[SUPPLY: ...]' (line 17); rulings transfer BLOCKE...` → `"SUPPLIED by role (AMD-V2-06): 19C program coordinator, non-authorship asserted by PI a...`
  - `$.tns_credentials`: `"UNDEMONSTRATED: arrived as unfilled '[SUPPLY: ...]' (line 18); agent 2 worked from pub...` → `"BLOCKED (AMD-V2-07): TNS_API_KEY absent, checked 2026-09-16T20:13:38Z; request date 20...`

## d5_inputs

**Cause:** AMD-V2-01, 03, 06, 07 (records rebuilt from rulings 1, 2, 4, 5)

- **changed** (24):
  - `$[0].provenance.adjudicator`: `"none: no budget has been proposed, so there is no weaker or stronger alternative to pr...` → `"the unfilled wave-2 placeholder (AMD-V1-04)"`
  - `$[0].provenance.falsifier`: `"a written budget from the human that differs from any figure later used to size the co...` → `"a cell ledger at R1 onward that exceeds 1,000 cells, or any Rubin-era paid run logged ...`
  - `$[0].provenance.population`: `"the human programme running the benchmark, not the corpus"` → `"the human programme; arm cells = subject x arm x round"`
  - `$[0].provenance.referent`: `"hours or cells the programme can spend on this benchmark"` → `"hours or cells the programme can spend on this benchmark (calibration phase)"`
  - `$[0].provenance.source`: `"references/manifest.md 'Supplied by you at D5'; references/stages/discovery.md D5; not...` → `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...`
  - `$[0].status`: `"UNDEMONSTRATED"` → `"SUPPLIED"`
  - `$[1].provenance.adjudicator`: `"the delta prior (delta_slot.json, 0.018 on committed-set purity), which stands unless ...` → `"the delta prior 0.018 that this overrides (AMD-V2-04)"`
  - `$[1].provenance.falsifier`: `"a supplied cost of action whose implied minimum effect falls below every MDE in a meas...` → `"a PI restatement that differs, or an A1 metric whose loss weights differ from 1 vs >= ...`
  - `$[1].provenance.population`: `"the human's own follow-up programme"` → `"the programme's own follow-up allocation"`
  - `$[1].provenance.referent`: `"cost to this programme of committing one follow-up slot to a wrong candidate, and of m...` → `"cost of a follow-up slot, of a wrong commitment and of a missed rare event"`
  - `$[1].provenance.source`: `"references/manifest.md 'Supplied by you at D5' ('the seeds show what others act on, no...` → `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...`
  - `$[1].status`: `"UNDEMONSTRATED"` → `"SUPPLIED"`
  - `$[2].provenance.adjudicator`: `"the current procedural seal held by the orchestrating party (SYNTHESIS.md section 10)"` → `"procedural seal held by the orchestrating party (SYNTHESIS.md section 10)"`
  - `$[2].provenance.falsifier`: `"a transfer_record.json whose receipt hash resolves against a holder-completed receipt ...` → `"transfer_record.json receipt_hash filled and matching sha256 of the returned RECEIPT_T...`
  - `$[2].provenance.population`: `"the two replay suites (astronomy 20 cases, source 38 cases)"` → `"the two replay suites (20 and 38 cases)"`
  - `$[2].provenance.referent`: `"a person who wrote neither the skill nor any replay case and holds RULINGS_SEALED.csv ...` → `"a person who wrote neither the skill nor any case and holds RULINGS_SEALED.csv and the...`
  - `$[2].provenance.source`: `"PANEL_BRIEF_WAVE2.md sha256 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7...` → `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...`
  - `$[2].status`: `"UNDEMONSTRATED"` → `"SUPPLIED (role); custody PENDING_RECEIPT"`
  - `$[3].provenance.adjudicator`: `"Internet Archive captures of TNS object pages (public, partial: 1,706 fetched)"` → `"public archived TNS pages (partial)"`
  - `$[3].provenance.falsifier`: `"an authenticated TNS request that returns classification reports would show the field ...` → `"a TNS_API_KEY present in the environment on a later presence test would unblock track ...`
  - `$[3].provenance.population`: `"7,843 BTS labels and every Rubin-era classification"` → `"7,843 BTS labels and all Rubin-era classifications"`
  - `$[3].provenance.referent`: `"an authenticated TNS bot or user account for per-object classification reports (report...` → `"an authenticated TNS account for per-object classification reports"`
  - `$[3].provenance.source`: `"PANEL_BRIEF_WAVE2.md sha256 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7...` → `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...`
  - `$[3].status`: `"UNDEMONSTRATED"` → `"BLOCKED"`
- **added** (8):
  - `$[0].value.agent_arm_cells_hard_cap`: `1000`
  - `$[0].value.engineering_hours`: `200`
  - `$[1].value.asymmetric`: `true`
  - `$[1].value.missed_rare_event_slots_min`: `100`
  - `$[1].value.one_spectrum_h_P60`: `0.5`
  - `$[1].value.wrong_routine_commitment_slots`: `1`
  - `$[2].value.name`: `null`
  - `$[2].value.role`: `"19C program coordinator"`
- **removed** (18):
  - `$[0].blocks[0]`: `"S"`
  - `$[0].blocks[1]`: `"P5 queue loop escape"`
  - `$[0].blocks[2]`: `"P7 N_min versus affordable N"`
  - `$[0].blocks[3]`: `"R1 onward (no paid work on an unratified manifest)"`
  - `$[0].human_must_supply`: `"a number in agent-arm cells (one cell = one subject x one arm x one round) or wall-clo...`
  - `$[0].value`: `null`
  - `$[1].blocks[0]`: `"delta override"`
  - `$[1].blocks[1]`: `"P7 ruling"`
  - `$[1].blocks[2]`: `"A4 claim threshold"`
  - `$[1].human_must_supply`: `"either (a) the smallest improvement in committed-set precision (or the preregistered m...`
  - `$[1].value`: `null`
  - `$[2].blocks[0]`: `"rulings transfer"`
  - `$[2].blocks[1]`: `"issue 09 re-keying"`
  - `$[2].blocks[2]`: `"any seal with more than procedural weight"`
  - `$[2].value`: `null`
  - `$[3].blocks[0]`: `"label_source per-object split"`
  - `$[3].blocks[1]`: `"measured P and Ng for the Rubin cohort"`
  - `$[3].blocks[2]`: `"P4 precondition (a)"`

## graph_escalations

**Cause:** AMD-V2-05 (ruling 3: escalation RATIFIED as staged); PANEL_BRIEF_WAVE3.md line 20

- **changed** (5):
  - `$[0].consequence`: `"wave-2 compositions are PRE-I1 CALIBRATION, hashed, not I1 records"` → `"wave-2 compositions stay PRE-I1 CALIBRATION; the I1 designation waits for R1 plus PI r...`
  - `$[0].source.locator`: `"coordinator preamble item 2"` → `"ruling 3"`
  - `$[0].source.path`: `"astronomy/wave2/PANEL_BRIEF_WAVE2.md"` → `"astronomy/wave3/PANEL_BRIEF_WAVE3.md"`
  - `$[0].source.sha256`: `"31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb"` → `"a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6"`
  - `$[0].state`: `"ESCALATED to PI, ladder rung 2; unruled at v1"` → `"RATIFIED as staged (PI ruling 3)"`
- **added** (2):
  - `$[0].ledger[0]`: `"ESC-V1-01"`
  - `$[0].ledger[1]`: `"AMD-V2-05"`
- **removed** (1):
  - `$[0].ledger`: `"ESC-V1-01"`

## amendment_ledger

**Cause:** ledger pointer updated for v2 entries

- **added** (16):
  - `$.v2_entries[0]`: `"AMD-V2-01"`
  - `$.v2_entries[10]`: `"PENDING-V2-01"`
  - `$.v2_entries[11]`: `"SU-V2-03"`
  - `$.v2_entries[12]`: `"SU-V2-04"`
  - `$.v2_entries[13]`: `"SU-V2-05"`
  - `$.v2_entries[14]`: `"FRZ-V2"`
  - `$.v2_entries[1]`: `"AMD-V2-02"`
  - `$.v2_entries[2]`: `"AMD-V2-03"`
  - `$.v2_entries[3]`: `"AMD-V2-04"`
  - `$.v2_entries[4]`: `"AMD-V2-05"`
  - `$.v2_entries[5]`: `"AMD-V2-06"`
  - `$.v2_entries[6]`: `"AMD-V2-07"`
  - `$.v2_entries[7]`: `"AMD-V2-08"`
  - `$.v2_entries[8]`: `"SU-V2-01"`
  - `$.v2_entries[9]`: `"SU-V2-02"`
  - `$.v2_entries_canonical_sha256`: `"a1feebcb49883284c27d2a10d5313f21d64f1950085fb1f572d7f2975eb87c49"`
- **removed** (10):
  - `$.entries[0]`: `"AMD-V1-01"`
  - `$.entries[1]`: `"AMD-V1-02"`
  - `$.entries[2]`: `"AMD-V1-03"`
  - `$.entries[3]`: `"AMD-V1-04"`
  - `$.entries[4]`: `"AMD-V1-05"`
  - `$.entries[5]`: `"AMD-V1-06"`
  - `$.entries[6]`: `"AMD-V1-07"`
  - `$.entries[7]`: `"AMD-V1-08"`
  - `$.entries[8]`: `"ESC-V1-01"`
  - `$.entries[9]`: `"SU-V1-01"`

## d5_disposition

**Cause:** consequence of the v2 slot statuses (no PI ruling on tau, exposure_key, subject_set)

- **changed** (4):
  - `$.disposition`: `"UNDEMONSTRATED: D5 does not advance. The brief's sentence 'This closes D5 for everythi...` → `"UNDEMONSTRATED: D5 does not advance. tau, exposure_key and subject_set carry no PI rul...`
  - `$.per_slot.S`: `"UNDEMONSTRATED"` → `"UNDEMONSTRATED (computed at R1)"`
  - `$.per_slot.delta`: `"DERIVED"` → `"OVERRIDDEN (0.05; prior 0.018 carried)"`
  - `$.per_slot.label_source`: `"UNDEMONSTRATED"` → `"UNDEMONSTRATED (agent 2 landed; no measured cohort supply)"`
- **removed** (2):
  - `$.advances_when`: `"every slot ratified or overridden, and the manifest frozen and hashed (references/stag...`
  - `$.disagreement_with_brief`: `"PANEL_BRIEF_WAVE2.md line 35 expects D5 closed except the SUPPLY fields; the PI decisi...`

## completeness

**Cause:** restated for v2

- **changed** (1):
  - `$`: `"v1 covers the ten schema slots plus decision_epoch; each carries value, five provenanc...` → `"v2: v1 plus wave-3 rulings 1-6 (AMD-V2-01..08) and fold-ins from agents 1, 4 and 2 (SU...`

## derived_from

**Cause:** version lineage

- **added** (4):
  - `$.draft.path`: `"astronomy/wave3/agent3_manifest_freeze/domain_manifest_v2_DRAFT.json"`
  - `$.draft.sha256`: `"38bbf3d41d2b245a73da6154e0ccf8e7832812195135f9470c8d5e79540729a6"`
  - `$.frozen_hash`: `"ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8"`
  - `$.manifest`: `"astronomy/wave3/agent3_manifest_freeze/domain_manifest_v1.json"`
- **removed** (1):
  - `$`: `{}`

## disagreements_v2

**Cause:** new wave-3 disagreements (S2, truth-cost target, metric vs cost, JSON rows, run count, agent 2 items)

- **added** (9):
  - `$[0]`: `"bands_FROZEN.md section 3 declares S2 (cohort objects with pre-boundary forced flux) '...`
  - `$[1]`: `"wave-3 preamble item 5 vs agent 4's JSON-row runs (tool_inventory, axis ledger v2)"`
  - `$[2]`: `"truth cost priced at 485 objects (delta 0.018 bracket) while delta is overridden to 0....`
  - `$[3]`: `"tool_coverage_axis.json population '158 alert runs' vs run_log 160 (158 + 2 voided)"`
  - `$[4]`: `"agent 2 sealed prediction non-bot share 0.7 [0.5, 0.85] vs observed 0.89 (outside); li...`
  - `$[5]`: `"13 typed cohort objects (existence) vs 0 measured non-bot on readable captures: not th...`
  - `$[6]`: `"night count: brief 10 on-sky nights vs agent 1's 9 alert dates (agent 2 reach 775 vs 8...`
  - `$[7]`: `"BTS trigger purity 0.967 vs 0.956 within arXiv:2401.15167 (truth-cost grid carries both)"`
  - `$[8]`: `"Rochester 2026 totals 17,562 (CSV) vs 19,448 (page)"`
- **removed** (1):
  - `$`: `{}`

## pi_reratification_inputs

**Cause:** SU-V2-05 (truth cost attached for ruling 1 re-ratification)

- **added** (92):
  - `$.measured_supply_rubin_cohort`: `"none demonstrated: 0 STRONG on 13 readable captures of 627; 13 typed, classifier unkno...`
  - `$.p4_readings.escalate_axes[0]`: `"contamination_exposure"`
  - `$.p4_readings.escalate_axes[1]`: `"tool_coverage"`
  - `$.p4_readings.ledger.path`: `"astronomy/wave3/agent3_manifest_freeze/axis_ledger_v2_final_against_frozen_bands.json"`
  - `$.p4_readings.ledger.sha256`: `"d20b69607bb6adfc1011b3e3b956cf1510ab41353c4cdd1a7966ff65491c8e60"`
  - `$.p4_readings.preconditions.a`: `"UNMET"`
  - `$.p4_readings.preconditions.b`: `"CLEARED"`
  - `$.p4_readings.preconditions.c`: `"UNMET"`
  - `$.p4_readings.ruling`: `null`
  - `$.packet`: `"astronomy/wave3/agent3_manifest_freeze/PI_rerat_packet.md"`
  - `$.ruling.locator`: `"ruling 1, line 13"`
  - `$.ruling.path`: `"astronomy/wave3/PANEL_BRIEF_WAVE3.md"`
  - `$.ruling.sha256`: `"a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6"`
  - `$.state`: `"OPEN (awaiting PI)"`
  - `$.supply_P_per_month`: `"lower bounds only (see candidates[0].prospective_label_supply_w3)"`
  - `$.truth_cost.L_used.L_existence_T8_T9_not_used_as_offset`: `13`
  - `$.truth_cost.L_used.L_measured_T1`: `0`
  - `$.truth_cost.by_delta.0.018 (literature prior; frozen bands).N_12855.hours[0]`: `6647.0`
  - `$.truth_cost.by_delta.0.018 (literature prior; frozen bands).N_12855.hours[1]`: `8532.5`
  - `$.truth_cost.by_delta.0.018 (literature prior; frozen bands).N_12855.nights[0]`: `1330`
  - `$.truth_cost.by_delta.0.018 (literature prior; frozen bands).N_12855.nights[1]`: `3793`
  - `$.truth_cost.by_delta.0.018 (literature prior; frozen bands).N_12855.spectra[0]`: `13294`
  - `$.truth_cost.by_delta.0.018 (literature prior; frozen bands).N_12855.spectra[1]`: `17065`
  - `$.truth_cost.by_delta.0.018 (literature prior; frozen bands).N_12855.wrong_commitments[0]`: `439`
  - `$.truth_cost.by_delta.0.018 (literature prior; frozen bands).N_12855.wrong_commitments[1]`: `3242`
  - ... 67 more (reproduce with scripts/diffs.py)
- **removed** (1):
  - `$`: `{}`
