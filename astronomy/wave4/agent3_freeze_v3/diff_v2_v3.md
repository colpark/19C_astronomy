# Diff v2 → v3 (wave 4)

- **From:** `astronomy/wave3/agent3_manifest_freeze/domain_manifest_v2.json`, frozen_hash `fba4259b1d5931ff8b74a3db2f438706ce29263ef7ca373a2cb5c5fd7f2cedd5`.
- **To:** `astronomy/wave4/agent3_freeze_v3/domain_manifest_v3.json`, frozen_hash `bd0fa4c67cdbbfb0b8eea9822f536bed4bf934ee1bc81a02606ed6d5ee9585bc`.
- **Cause authority:** PANEL_BRIEF_WAVE4.md (sha256 8f101811...1b58) rulings 1-5, rule E, preamble items 1-5. Ledger ids refer to `amendment_ledger_v3.json` (append-only).
- **Method:** leaf-path comparison of the two frozen JSON files (frozen_hash and frozen_utc excluded). Every changed top-level key has one cause line; unchanged slots are listed as unchanged.

| Key | Status before → after | Leaves added / removed / changed | Cause |
|---|---|---|---|
| manifest |  (unchanged) | 0 / 0 / 0 | unchanged |
| manifest_version | - → - | 0 / 0 / 1 | version |
| governing_brief | - → - | 0 / 0 / 2 | v3 governed by PANEL_BRIEF_WAVE4.md |
| inputs_state | - → - | 0 / 0 / 1 | version |
| hash_method |  (unchanged) | 0 / 0 / 0 | unchanged |
| candidates | - → - | 34 / 1 / 0 | RE-V3-02 rule E marks (C01-C04 CLEARED; U, nights, census V_PENDING); P4 state from axis ledger v3 (preconditions (b) V-O02, (c) AMD-V3-03) |
| tau | DERIVED → DERIVED | 8 / 0 / 0 | RE-V3-02 rule E marks only (value unchanged; V_PENDING, no V record); no PI ruling (wave-4 brief rules on none) |
| k | RATIFIED → RATIFIED | 22 / 0 / 0 | RE-V3-02 rule E marks only (k 8 V_PENDING; K01/K02 CLEARED); value and status unchanged |
| label_source | UNDEMONSTRATED → RATIFIED | 120 / 13 / 4 | AMD-V3-02 (ruling 4 RATIFIED WITH CONDITIONS, conditions verbatim) + RE-V3-01 (numeric fields V_PENDING, V-L01..L05 DISCREPANCY, readings (i) E5 cut, (ii) twin keying) + AMD-V3-04 (TNS/WISeREP BLOCKED); PANEL_BRIEF_WAVE4.md lines 5, 16-20 |
| exposure_key | DERIVED → DERIVED | 16 / 0 / 0 | RE-V3-02 rule E marks (C01 CLEARED; leak and BTS split V_PENDING) |
| tool_inventory | OVERRIDDEN → OVERRIDDEN | 28 / 0 / 0 | RE-V3-02 rule E marks (T01-T03 CLEARED); V invariance note; status unchanged (OVERRIDDEN) |
| delta | OVERRIDDEN → RATIFIED | 161 / 1 / 3 | AMD-V3-01 (ruling 1: OVERRIDDEN -> RATIFIED; cause check V-O01 with git/time-zone caveats; 0.018 carried) + RE-V3-02 (P01-P08, K01-K02, A01-A04, N01-N02 CLEARED; family-A nights V_PENDING; sqrt(q) note); PANEL_BRIEF_WAVE4.md lines 5, 9-14 |
| S | UNDEMONSTRATED → UNDEMONSTRATED | 11 / 0 / 0 | RE-V3-02 rule E marks (budget PI_RULED; planning rounds V_PENDING); status unchanged |
| subject_set | DERIVED → DERIVED | 1 / 0 / 0 | RE-V3-02 rule E note only; no PI ruling |
| decision_epoch | RATIFIED → RATIFIED | 10 / 0 / 0 | RE-V3-02 rule E marks (S1 C03 CLEARED; S0 V_PENDING); S2 conflict carried unchanged |
| supplied_by_human | - → - | 0 / 0 / 2 | AMD-V3-04 (ruling 3: TNS second BLOCKED record, WISeREP BLOCKED) + AMD-V3-05 (ruling 2: custody PENDING_RECEIPT, procedural); PANEL_BRIEF_WAVE4.md lines 15-16 |
| d5_inputs | - → - | 3 / 0 / 1 | AMD-V3-04 (request dates, WISeREP) |
| graph_escalations | - → - | 1 / 0 / 0 | AMD-V3-06 (ruling 5: module V chartered; overhead cap exceeded, interim) |
| amendment_ledger | - → - | 10 / 15 / 1 | pointer to amendment_ledger_v3.json (append-only) with v1/v2/v3 entry hashes |
| d5_disposition | - → - | 0 / 0 / 6 | AMD-V3-01, AMD-V3-02 (delta and label_source now RATIFIED); tau, exposure_key, subject_set still DERIVED |
| completeness | - → - | 0 / 0 / 1 | restated for v3 |
| derived_from | - → - | 4 / 4 / 0 | version lineage (v2, v1 hashes) |
| disagreements_v2 |  (unchanged) | 0 / 0 / 0 | unchanged |
| pi_reratification_inputs | - → - | 53 / 0 / 1 | RE-V3-02 (truth cost R01-R04 CLEARED; wave-4 monthly pricing V_PENDING); state note |
| naming_disagreement | - → - | 0 / 0 / 1 | NAME-V3-01 (brief 'freeze v2' vs v3; preamble item 1) |
| module_v | - → - | 10 / 1 / 0 | ruling 5 / rule E: V records pointer |
| rule_E_index | - → - | 296 / 1 / 0 | RE-V3-02 |
| disagreements_v3 | - → - | 8 / 1 / 0 | new wave-4 disagreements |
| open_items_carried | - → - | 3 / 1 / 0 | carried forward unchanged (tau, exposure_key, subject_set; S2; disagreements_v2) |

## manifest_version

**Cause:** version

- **changed** (1):
  - `$`: `"v2"` → `"v3"`

## governing_brief

**Cause:** v3 governed by PANEL_BRIEF_WAVE4.md

- **changed** (2):
  - `$.path`: `"astronomy/wave3/PANEL_BRIEF_WAVE3.md"` → `"astronomy/wave4/PANEL_BRIEF_WAVE4.md"`
  - `$.sha256`: `"a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6"` → `"8f10181154219048bed3e8fa973c35d71d3a038cc98323fde76f509363511b58"`

## inputs_state

**Cause:** version

- **changed** (1):
  - `$`: `"v1 plus wave-3 PI rulings 1-6, wave-3 counts from agent 1 (cohort, axes), agent 4 (too...` → `"v2 plus wave-4 PI rulings 1-5, module V records (38), agent 2 wave-4 WISeREP check, ag...`

## candidates

**Cause:** RE-V3-02 rule E marks (C01-C04 CLEARED; U, nights, census V_PENDING); P4 state from axis ledger v3 (preconditions (b) V-O02, (c) AMD-V3-03)

- **added** (34):
  - `$[0].cohorts.prospective_counts_w3.rule_E.O_merged.cleared_for_P4_under_rule_E`: `true`
  - `$[0].cohorts.prospective_counts_w3.rule_E.O_merged.rule_E`: `"CLEARED"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.O_merged.sealed_sha256`: `"8f5262daef8930d8e21ac46d14268c365f8d172ba5bd2726cf1cb63f89c8c463"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.O_merged.v_record`: `"V-C01"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.O_merged.value`: `1937669`
  - `$[0].cohorts.prospective_counts_w3.rule_E.O_merged.verdict`: `"MATCH"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.S1.cleared_for_P4_under_rule_E`: `true`
  - `$[0].cohorts.prospective_counts_w3.rule_E.S1.rule_E`: `"CLEARED"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.S1.sealed_sha256`: `"8a5e0127ab4f0aa541cb52b231c613d06fa5889b089a3f7cedb984679d21eae9"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.S1.v_record`: `"V-C03"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.S1.value`: `521920`
  - `$[0].cohorts.prospective_counts_w3.rule_E.S1.verdict`: `"MATCH"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.U.note`: `"no V record"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.U.rule_E`: `"V_PENDING"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.U.v_record`: `null`
  - `$[0].cohorts.prospective_counts_w3.rule_E.U.value`: `0`
  - `$[0].cohorts.prospective_counts_w3.rule_E.alerce_oids.cleared_for_P4_under_rule_E`: `true`
  - `$[0].cohorts.prospective_counts_w3.rule_E.alerce_oids.rule_E`: `"CLEARED"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.alerce_oids.sealed_sha256`: `"667e1e2daa5a8640127bdc4b483da070f86294f62e8e3ce3f2bed94914bdf5b9"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.alerce_oids.v_record`: `"V-C02"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.alerce_oids.value`: `1937720`
  - `$[0].cohorts.prospective_counts_w3.rule_E.alerce_oids.verdict`: `"MATCH"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.cohort_nights.note`: `"no V record"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.cohort_nights.rule_E`: `"V_PENDING"`
  - `$[0].cohorts.prospective_counts_w3.rule_E.cohort_nights.v_record`: `null`
  - ... 9 more (reproduce with scripts/diffs.py)
- **removed** (1):
  - `$[0].p4_state_v2`: `"no ruling; astronomy/wave3/agent3_manifest_freeze/axis_ledger_v2_final_against_frozen_...`

## tau

**Cause:** RE-V3-02 rule E marks only (value unchanged; V_PENDING, no V record); no PI ruling (wave-4 brief rules on none)

- **added** (8):
  - `$.rule_E.n_clusters_bts.note`: `"BTS calibration only"`
  - `$.rule_E.n_clusters_bts.rule_E`: `"V_PENDING"`
  - `$.rule_E.n_clusters_bts.v_record`: `null`
  - `$.rule_E.n_clusters_bts.value`: `11183`
  - `$.rule_E.radius_arcsec.note`: `"no V record"`
  - `$.rule_E.radius_arcsec.rule_E`: `"V_PENDING"`
  - `$.rule_E.radius_arcsec.v_record`: `null`
  - `$.rule_E.radius_arcsec.value`: `1.0`

## k

**Cause:** RE-V3-02 rule E marks only (k 8 V_PENDING; K01/K02 CLEARED); value and status unchanged

- **added** (22):
  - `$.rule_E.candidates_per_round.rule_E`: `"V_PENDING"`
  - `$.rule_E.candidates_per_round.v_record`: `null`
  - `$.rule_E.candidates_per_round.value`: `46.41`
  - `$.rule_E.chance_stated.rule_E`: `"V_PENDING"`
  - `$.rule_E.chance_stated.v_record`: `null`
  - `$.rule_E.chance_stated.value`: `0.1718`
  - `$.rule_E.k.note`: `"RATIFIED at v1; no V record"`
  - `$.rule_E.k.rule_E`: `"V_PENDING"`
  - `$.rule_E.k.v_record`: `null`
  - `$.rule_E.k.value`: `8`
  - `$.rule_E.k_binding_nights.cleared_for_P4_under_rule_E`: `true`
  - `$.rule_E.k_binding_nights.rule_E`: `"CLEARED"`
  - `$.rule_E.k_binding_nights.sealed_sha256`: `"e58f6798e0621fd375c9cc79e4c08780653be711a25ad7c91b545a7944c5a5d3"`
  - `$.rule_E.k_binding_nights.v_record`: `"V-K01"`
  - `$.rule_E.k_binding_nights.value`: `61`
  - `$.rule_E.k_binding_nights.verdict`: `"MATCH"`
  - `$.rule_E.nights_k_not_binding.cleared_for_P4_under_rule_E`: `true`
  - `$.rule_E.nights_k_not_binding.rule_E`: `"CLEARED"`
  - `$.rule_E.nights_k_not_binding.sealed_sha256`: `"469ab291d8a9c6d6b34ca5b3eab2bcb151132ec7364aeadd88805b8f9ede58ce"`
  - `$.rule_E.nights_k_not_binding.v_record`: `"V-K02"`
  - `$.rule_E.nights_k_not_binding.value`: `518`
  - `$.rule_E.nights_k_not_binding.verdict`: `"MATCH"`

## label_source

**Cause:** AMD-V3-02 (ruling 4 RATIFIED WITH CONDITIONS, conditions verbatim) + RE-V3-01 (numeric fields V_PENDING, V-L01..L05 DISCREPANCY, readings (i) E5 cut, (ii) twin keying) + AMD-V3-04 (TNS/WISeREP BLOCKED); PANEL_BRIEF_WAVE4.md lines 5, 16-20

- **changed** (4):
  - `$.override_invitation`: `"Override invitation: accept the bounded state (UNDEMONSTRATED), supply TNS credentials...` → `"Ratified with conditions. Open for the PI: rule readings (i) E5 cut and (ii) twin keyi...`
  - `$.provenance.source`: `"astronomy/wave3/agent2_measured_labels/scripts/track1_bound.py (imports wave-2 common....` → `"astronomy/wave3/agent2_measured_labels/scripts/track1_bound.py (imports wave-2 common....`
  - `$.status`: `"UNDEMONSTRATED"` → `"RATIFIED"`
  - `$.status_note`: `"BTS per-object split still incomplete (5815 of 7,843 unresolved); Rubin cohort measure...` → `"RATIFIED WITH CONDITIONS (PI ruling 4). The definition and conditions are frozen; the ...`
- **added** (120):
  - `$.ratification.condition_holds_under_all_readings`: `true`
  - `$.ratification.conditions_verbatim[0]`: `"Labels are TNS-reported spectroscopic classifications, with a model-annotation fractio...`
  - `$.ratification.conditions_verbatim[1]`: `"For calibration, the SNIascore-flagged subset stays in, stratified."`
  - `$.ratification.conditions_verbatim[2]`: `"For any future paid claim, measured truth means human-classifier-confirmed only. Model...`
  - `$.ratification.conditions_verbatim[3]`: `"Precondition (c) clears under these conditions."`
  - `$.ratification.ledger`: `"AMD-V3-02"`
  - `$.ratification.numbers`: `"numeric fields frozen as V_PENDING (RE-V3-01), not cleared values"`
  - `$.value.bts.category_counts.MEASURED.blind_V`: `1070`
  - `$.value.bts.category_counts.MEASURED.claimed`: `1074`
  - `$.value.bts.category_counts.MEASURED.cleared_for_P4_under_rule_E`: `false`
  - `$.value.bts.category_counts.MEASURED.rule_E`: `"V_PENDING"`
  - `$.value.bts.category_counts.MEASURED.sealed_sha256`: `"4d49bf3fa25d364ab61326bb08af4dc1235c3bcf96a0a9747e996c4e00dac472"`
  - `$.value.bts.category_counts.MEASURED.v_record`: `"V-L03"`
  - `$.value.bts.category_counts.MEASURED.verdict`: `"DISCREPANCY"`
  - `$.value.bts.category_counts.MODEL_ANNOTATION.blind_V`: `948`
  - `$.value.bts.category_counts.MODEL_ANNOTATION.claimed`: `954`
  - `$.value.bts.category_counts.MODEL_ANNOTATION.cleared_for_P4_under_rule_E`: `false`
  - `$.value.bts.category_counts.MODEL_ANNOTATION.rule_E`: `"V_PENDING"`
  - `$.value.bts.category_counts.MODEL_ANNOTATION.sealed_sha256`: `"8e0a8063982edba2dae1a60b1dbf0b1684a8d9334ea60a0f558ab75b374bbc0f"`
  - `$.value.bts.category_counts.MODEL_ANNOTATION.v_record`: `"V-L04"`
  - `$.value.bts.category_counts.MODEL_ANNOTATION.verdict`: `"DISCREPANCY"`
  - `$.value.bts.category_counts.PHOTOMETRIC_ONLY.blind_V`: `0`
  - `$.value.bts.category_counts.PHOTOMETRIC_ONLY.claimed`: `0`
  - `$.value.bts.category_counts.PHOTOMETRIC_ONLY.cleared_for_P4_under_rule_E`: `false`
  - `$.value.bts.category_counts.PHOTOMETRIC_ONLY.note`: `"field matched; record V-L03 not cleared"`
  - ... 95 more (reproduce with scripts/diffs.py)
- **removed** (13):
  - `$.value.bts.category_counts.MEASURED`: `1074`
  - `$.value.bts.category_counts.MODEL_ANNOTATION`: `954`
  - `$.value.bts.category_counts.PHOTOMETRIC_ONLY`: `0`
  - `$.value.bts.category_counts.UNRESOLVED_UNDEMONSTRATED`: `5815`
  - `$.value.bts.sniascore_bound.lower`: `954`
  - `$.value.bts.sniascore_bound.new_captures.failed_retries`: `7`
  - `$.value.bts.sniascore_bound.new_captures.http_error`: `38`
  - `$.value.bts.sniascore_bound.new_captures.ok`: `345`
  - `$.value.bts.sniascore_bound.new_measured`: `190`
  - `$.value.bts.sniascore_bound.new_sniascore_strong`: `151`
  - `$.value.bts.sniascore_bound.status`: `"DERIVED"`
  - `$.value.bts.sniascore_bound.upper`: `2057`
  - `$.value.bts.sniascore_bound.upper_noE5_sensitivity_not_slot_value`: `2654`

## exposure_key

**Cause:** RE-V3-02 rule E marks (C01 CLEARED; leak and BTS split V_PENDING)

- **added** (16):
  - `$.rule_E.antares_prior_position_leak_193_of_9000.rule_E`: `"V_PENDING"`
  - `$.rule_E.antares_prior_position_leak_193_of_9000.v_record`: `null`
  - `$.rule_E.antares_prior_position_leak_193_of_9000.value[0]`: `193`
  - `$.rule_E.antares_prior_position_leak_193_of_9000.value[1]`: `9000`
  - `$.rule_E.bts_capture_split_6166_0_1677.note`: `"BTS calibration only"`
  - `$.rule_E.bts_capture_split_6166_0_1677.rule_E`: `"V_PENDING"`
  - `$.rule_E.bts_capture_split_6166_0_1677.v_record`: `null`
  - `$.rule_E.bts_capture_split_6166_0_1677.value[0]`: `6166`
  - `$.rule_E.bts_capture_split_6166_0_1677.value[1]`: `0`
  - `$.rule_E.bts_capture_split_6166_0_1677.value[2]`: `1677`
  - `$.rule_E.cohort_after_every_cutoff.cleared_for_P4_under_rule_E`: `true`
  - `$.rule_E.cohort_after_every_cutoff.rule_E`: `"CLEARED"`
  - `$.rule_E.cohort_after_every_cutoff.sealed_sha256`: `"8f5262daef8930d8e21ac46d14268c365f8d172ba5bd2726cf1cb63f89c8c463"`
  - `$.rule_E.cohort_after_every_cutoff.v_record`: `"V-C01"`
  - `$.rule_E.cohort_after_every_cutoff.value`: `1937669`
  - `$.rule_E.cohort_after_every_cutoff.verdict`: `"MATCH"`

## tool_inventory

**Cause:** RE-V3-02 rule E marks (T01-T03 CLEARED); V invariance note; status unchanged (OVERRIDDEN)

- **added** (28):
  - `$.rubin_functional_recount_w3.invariance_V`: `"CATS and GHOST invariant within float tolerance, not bit-identical (module V invarianc...`
  - `$.rubin_functional_recount_w3.rule_E.CATS.cleared_for_P4_under_rule_E`: `true`
  - `$.rubin_functional_recount_w3.rule_E.CATS.rule_E`: `"CLEARED"`
  - `$.rubin_functional_recount_w3.rule_E.CATS.sealed_sha256`: `"ee836bd17e9976bd9a5018771554f1a4b9003d87e6f3a1413b82993886fb3792"`
  - `$.rubin_functional_recount_w3.rule_E.CATS.v_record`: `"V-T02"`
  - `$.rubin_functional_recount_w3.rule_E.CATS.value`: `"5/10"`
  - `$.rubin_functional_recount_w3.rule_E.CATS.verdict`: `"MATCH"`
  - `$.rubin_functional_recount_w3.rule_E.GHOST.cleared_for_P4_under_rule_E`: `true`
  - `$.rubin_functional_recount_w3.rule_E.GHOST.rule_E`: `"CLEARED"`
  - `$.rubin_functional_recount_w3.rule_E.GHOST.sealed_sha256`: `"ee836bd17e9976bd9a5018771554f1a4b9003d87e6f3a1413b82993886fb3792"`
  - `$.rubin_functional_recount_w3.rule_E.GHOST.v_record`: `"V-T02"`
  - `$.rubin_functional_recount_w3.rule_E.GHOST.value`: `"3/8"`
  - `$.rubin_functional_recount_w3.rule_E.GHOST.verdict`: `"MATCH"`
  - `$.rubin_functional_recount_w3.rule_E.alert_runs.cleared_for_P4_under_rule_E`: `true`
  - `$.rubin_functional_recount_w3.rule_E.alert_runs.rule_E`: `"CLEARED"`
  - `$.rubin_functional_recount_w3.rule_E.alert_runs.sealed_sha256`: `"261e5c37f77f1866c0f53d626c66eb17b0e07d302e04e4c0f51faf3a5dd26c17"`
  - `$.rubin_functional_recount_w3.rule_E.alert_runs.v_record`: `"V-T03"`
  - `$.rubin_functional_recount_w3.rule_E.alert_runs.value`: `160`
  - `$.rubin_functional_recount_w3.rule_E.alert_runs.verdict`: `"MATCH"`
  - `$.rubin_functional_recount_w3.rule_E.counts_all.cleared_for_P4_under_rule_E`: `true`
  - `$.rubin_functional_recount_w3.rule_E.counts_all.rule_E`: `"CLEARED"`
  - `$.rubin_functional_recount_w3.rule_E.counts_all.sealed_sha256`: `"3c5a69425b1d4f8df62a8818a9cdfb003502b7cd88458a8a4570ff092c7ba399"`
  - `$.rubin_functional_recount_w3.rule_E.counts_all.v_record`: `"V-T01"`
  - `$.rubin_functional_recount_w3.rule_E.counts_all.value.FAIL`: `14`
  - `$.rubin_functional_recount_w3.rule_E.counts_all.value.PASS`: `2`
  - ... 3 more (reproduce with scripts/diffs.py)

## delta

**Cause:** AMD-V3-01 (ruling 1: OVERRIDDEN -> RATIFIED; cause check V-O01 with git/time-zone caveats; 0.018 carried) + RE-V3-02 (P01-P08, K01-K02, A01-A04, N01-N02 CLEARED; family-A nights V_PENDING; sqrt(q) note); PANEL_BRIEF_WAVE4.md lines 5, 9-14

- **changed** (3):
  - `$.carry_both`: `"every P7 table reports delta 0.05 and 0.018 side by side (ruling 2)"` → `"every table reports 0.05 (ratified cost of action) and 0.018 (literature prior) side b...`
  - `$.provenance.source`: `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...` → `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...`
  - `$.status`: `"OVERRIDDEN"` → `"RATIFIED"`
- **added** (161):
  - `$.calibration_context.composition_auc.A01.cleared_for_P4_under_rule_E`: `true`
  - `$.calibration_context.composition_auc.A01.sealed_sha256`: `"c2a8290596061b4e8c2746172b554efa84d7ed86b863f4c66bb44d5104366c76"`
  - `$.calibration_context.composition_auc.A01.v_record`: `"V-A01"`
  - `$.calibration_context.composition_auc.A01.value`: `0.5996251272075266`
  - `$.calibration_context.composition_auc.A01.verdict`: `"MATCH"`
  - `$.calibration_context.composition_auc.A02.cleared_for_P4_under_rule_E`: `true`
  - `$.calibration_context.composition_auc.A02.sealed_sha256`: `"940b9a8b017c89e8684a5368c7aa734b3e41ea8fd416e2ee674ba0f022128c34"`
  - `$.calibration_context.composition_auc.A02.v_record`: `"V-A02"`
  - `$.calibration_context.composition_auc.A02.value`: `0.5968101198346822`
  - `$.calibration_context.composition_auc.A02.verdict`: `"MATCH"`
  - `$.calibration_context.composition_auc.A03.cleared_for_P4_under_rule_E`: `true`
  - `$.calibration_context.composition_auc.A03.sealed_sha256`: `"41fb67f37d36c748e1ad0c7ecde7e2086d048b99da068b0651e180a15c3ac15f"`
  - `$.calibration_context.composition_auc.A03.v_record`: `"V-A03"`
  - `$.calibration_context.composition_auc.A03.value`: `0.6373746097238473`
  - `$.calibration_context.composition_auc.A03.verdict`: `"MATCH"`
  - `$.calibration_context.composition_auc.A04.cleared_for_P4_under_rule_E`: `true`
  - `$.calibration_context.composition_auc.A04.sealed_sha256`: `"b949b607b0fa6f4d33010958cd51921affa169c6d9456215f9d8bada4bab2b81"`
  - `$.calibration_context.composition_auc.A04.v_record`: `"V-A04"`
  - `$.calibration_context.composition_auc.A04.value`: `0.6184103039827205`
  - `$.calibration_context.composition_auc.A04.verdict`: `"MATCH"`
  - `$.calibration_context.k_binding_nights.k_binding.cleared_for_P4_under_rule_E`: `true`
  - `$.calibration_context.k_binding_nights.k_binding.note`: `"of 579 E1 nights (same for E3)"`
  - `$.calibration_context.k_binding_nights.k_binding.rule_E`: `"CLEARED"`
  - `$.calibration_context.k_binding_nights.k_binding.sealed_sha256`: `"e58f6798e0621fd375c9cc79e4c08780653be711a25ad7c91b545a7944c5a5d3"`
  - `$.calibration_context.k_binding_nights.k_binding.v_record`: `"V-K01"`
  - ... 136 more (reproduce with scripts/diffs.py)
- **removed** (1):
  - `$.override_reason`: `"AMD-V2-04, PI ruling 2: switching a production selector costs engineer weeks, and 0.01...`

## S

**Cause:** RE-V3-02 rule E marks (budget PI_RULED; planning rounds V_PENDING); status unchanged

- **added** (11):
  - `$.rule_E.budget_arm_cells.rule_E`: `"PI_RULED"`
  - `$.rule_E.budget_arm_cells.v_record`: `null`
  - `$.rule_E.budget_arm_cells.value`: `1000`
  - `$.rule_E.engineering_hours.rule_E`: `"PI_RULED"`
  - `$.rule_E.engineering_hours.v_record`: `null`
  - `$.rule_E.engineering_hours.value`: `200`
  - `$.rule_E.planning_rounds_71_498.note`: `"PLANNING-ONLY arithmetic, no V record"`
  - `$.rule_E.planning_rounds_71_498.rule_E`: `"V_PENDING"`
  - `$.rule_E.planning_rounds_71_498.v_record`: `null`
  - `$.rule_E.planning_rounds_71_498.value[0]`: `71`
  - `$.rule_E.planning_rounds_71_498.value[1]`: `498`

## subject_set

**Cause:** RE-V3-02 rule E note only; no PI ruling

- **added** (1):
  - `$.rule_E`: `"no numbers bear on a ruling except cutoff dates (V_PENDING, no V record)"`

## decision_epoch

**Cause:** RE-V3-02 rule E marks (S1 C03 CLEARED; S0 V_PENDING); S2 conflict carried unchanged

- **added** (10):
  - `$.strata.S0.rule_E.note`: `"ANTARES loci, no V record"`
  - `$.strata.S0.rule_E.rule_E`: `"V_PENDING"`
  - `$.strata.S0.rule_E.v_record`: `null`
  - `$.strata.S0.rule_E.value`: `112990`
  - `$.strata.S1.rule_E.cleared_for_P4_under_rule_E`: `true`
  - `$.strata.S1.rule_E.rule_E`: `"CLEARED"`
  - `$.strata.S1.rule_E.sealed_sha256`: `"8a5e0127ab4f0aa541cb52b231c613d06fa5889b089a3f7cedb984679d21eae9"`
  - `$.strata.S1.rule_E.v_record`: `"V-C03"`
  - `$.strata.S1.rule_E.value`: `521920`
  - `$.strata.S1.rule_E.verdict`: `"MATCH"`

## supplied_by_human

**Cause:** AMD-V3-04 (ruling 3: TNS second BLOCKED record, WISeREP BLOCKED) + AMD-V3-05 (ruling 2: custody PENDING_RECEIPT, procedural); PANEL_BRIEF_WAVE4.md lines 15-16

- **changed** (2):
  - `$.rulings_holder`: `"SUPPLIED by role (AMD-V2-06): 19C program coordinator, non-authorship asserted by PI a...` → `"SUPPLIED by role (AMD-V2-06): 19C program coordinator, non-authorship asserted by PI a...`
  - `$.tns_credentials`: `"BLOCKED (AMD-V2-07): TNS_API_KEY absent, checked 2026-09-16T20:13:38Z; request date 20...` → `"BLOCKED, second record (AMD-V3-04): request dates 2026-09-16 and 2026-09-17; sanctione...`

## d5_inputs

**Cause:** AMD-V3-04 (request dates, WISeREP)

- **changed** (1):
  - `$[3].provenance.source`: `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...` → `"PANEL_BRIEF_WAVE3.md sha256 a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e89...`
- **added** (3):
  - `$[3].request_dates[0]`: `"2026-09-16"`
  - `$[3].request_dates[1]`: `"2026-09-17"`
  - `$[3].wiserep`: `"BLOCKED"`

## graph_escalations

**Cause:** AMD-V3-06 (ruling 5: module V chartered; overhead cap exceeded, interim)

- **added** (1):
  - `$[0].module_v`: `"ruling 5 chartered module V; overhead cap exceeded (interim), AMD-V3-06"`

## amendment_ledger

**Cause:** pointer to amendment_ledger_v3.json (append-only) with v1/v2/v3 entry hashes

- **changed** (1):
  - `$.path`: `"astronomy/wave3/agent3_manifest_freeze/amendment_ledger.json"` → `"astronomy/wave4/agent3_freeze_v3/amendment_ledger_v3.json"`
- **added** (10):
  - `$.v3_entries[0]`: `"NAME-V3-01"`
  - `$.v3_entries[1]`: `"AMD-V3-01"`
  - `$.v3_entries[2]`: `"AMD-V3-02"`
  - `$.v3_entries[3]`: `"RE-V3-01"`
  - `$.v3_entries[4]`: `"AMD-V3-03"`
  - `$.v3_entries[5]`: `"AMD-V3-04"`
  - `$.v3_entries[6]`: `"AMD-V3-05"`
  - `$.v3_entries[7]`: `"AMD-V3-06"`
  - `$.v3_entries[8]`: `"RE-V3-02"`
  - `$.v3_entries_canonical_sha256`: `"43550720a5c0abe22d25d4087a4b7c8077702224a7f68fcc7319b5c2b5339110"`
- **removed** (15):
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

## d5_disposition

**Cause:** AMD-V3-01, AMD-V3-02 (delta and label_source now RATIFIED); tau, exposure_key, subject_set still DERIVED

- **changed** (6):
  - `$.disposition`: `"UNDEMONSTRATED: D5 does not advance. tau, exposure_key and subject_set carry no PI rul...` → `"UNDEMONSTRATED: D5 does not advance. tau, exposure_key and subject_set still carry no ...`
  - `$.per_slot.delta`: `"OVERRIDDEN (0.05; prior 0.018 carried)"` → `"RATIFIED (0.05; prior 0.018 carried)"`
  - `$.per_slot.exposure_key`: `"DERIVED"` → `"DERIVED (no PI ruling)"`
  - `$.per_slot.label_source`: `"UNDEMONSTRATED (agent 2 landed; no measured cohort supply)"` → `"RATIFIED WITH CONDITIONS (numeric fields V_PENDING)"`
  - `$.per_slot.subject_set`: `"DERIVED"` → `"DERIVED (no PI ruling)"`
  - `$.per_slot.tau`: `"DERIVED"` → `"DERIVED (no PI ruling)"`

## completeness

**Cause:** restated for v3

- **changed** (1):
  - `$`: `"v2: v1 plus wave-3 rulings 1-6 (AMD-V2-01..08) and fold-ins from agents 1, 4 and 2 (SU...` → `"v3: v2 plus wave-4 rulings 1-5 (AMD-V3-01..06), naming disagreement NAME-V3-01, rule E...`

## derived_from

**Cause:** version lineage (v2, v1 hashes)

- **added** (4):
  - `$.v1.frozen_hash`: `"ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8"`
  - `$.v1.path`: `"astronomy/wave3/agent3_manifest_freeze/domain_manifest_v1.json"`
  - `$.v2.frozen_hash`: `"fba4259b1d5931ff8b74a3db2f438706ce29263ef7ca373a2cb5c5fd7f2cedd5"`
  - `$.v2.path`: `"astronomy/wave3/agent3_manifest_freeze/domain_manifest_v2.json"`
- **removed** (4):
  - `$.draft.path`: `"astronomy/wave3/agent3_manifest_freeze/domain_manifest_v2_DRAFT.json"`
  - `$.draft.sha256`: `"38bbf3d41d2b245a73da6154e0ccf8e7832812195135f9470c8d5e79540729a6"`
  - `$.frozen_hash`: `"ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8"`
  - `$.manifest`: `"astronomy/wave3/agent3_manifest_freeze/domain_manifest_v1.json"`

## pi_reratification_inputs

**Cause:** RE-V3-02 (truth cost R01-R04 CLEARED; wave-4 monthly pricing V_PENDING); state note

- **changed** (1):
  - `$.state`: `"OPEN (awaiting PI)"` → `"OPEN: ruling 4 ratified the label source; the ruling-1 (wave 3) go/no-go on Rubin-era ...`
- **added** (53):
  - `$.truth_cost.rule_E.N1666_and_N12855.cleared_for_P4_under_rule_E`: `true`
  - `$.truth_cost.rule_E.N1666_and_N12855.rule_E`: `"CLEARED"`
  - `$.truth_cost.rule_E.N1666_and_N12855.sealed_sha256`: `"dcd8c05fff8e35d8c08438909e382d9872fc1c77197bab94451f295e626d5996"`
  - `$.truth_cost.rule_E.N1666_and_N12855.v_record`: `"V-R04"`
  - `$.truth_cost.rule_E.N1666_and_N12855.value`: `"see ranges_over_grid_L0"`
  - `$.truth_cost.rule_E.N1666_and_N12855.verdict`: `"MATCH"`
  - `$.truth_cost.rule_E.N485.cleared_for_P4_under_rule_E`: `true`
  - `$.truth_cost.rule_E.N485.rule_E`: `"CLEARED"`
  - `$.truth_cost.rule_E.N485.sealed_sha256`: `"ca104ac9f46236f694bcb809a8dfc003361cb72b33e9ffa218ffa395d3faea59"`
  - `$.truth_cost.rule_E.N485.v_record`: `"V-R03"`
  - `$.truth_cost.rule_E.N485.value.hours[0]`: `251.0`
  - `$.truth_cost.rule_E.N485.value.hours[1]`: `322.0`
  - `$.truth_cost.rule_E.N485.value.nights[0]`: `51`
  - `$.truth_cost.rule_E.N485.value.nights[1]`: `144`
  - `$.truth_cost.rule_E.N485.value.spectra[0]`: `502`
  - `$.truth_cost.rule_E.N485.value.spectra[1]`: `644`
  - `$.truth_cost.rule_E.N485.value.wrong_commitments[0]`: `17`
  - `$.truth_cost.rule_E.N485.value.wrong_commitments[1]`: `122`
  - `$.truth_cost.rule_E.N485.verdict`: `"MATCH"`
  - `$.truth_cost.rule_E.N63.cleared_for_P4_under_rule_E`: `true`
  - `$.truth_cost.rule_E.N63.rule_E`: `"CLEARED"`
  - `$.truth_cost.rule_E.N63.sealed_sha256`: `"77954c73c1385cc23c5c9680929d2bb8c6e56dd00736df3fd5b14b3a89da4ad7"`
  - `$.truth_cost.rule_E.N63.v_record`: `"V-R02"`
  - `$.truth_cost.rule_E.N63.value.hours[0]`: `33.0`
  - `$.truth_cost.rule_E.N63.value.hours[1]`: `42.0`
  - ... 28 more (reproduce with scripts/diffs.py)

## naming_disagreement

**Cause:** NAME-V3-01 (brief 'freeze v2' vs v3; preamble item 1)

- **changed** (1):
  - `$`: `{}` → `"wave-4 brief says 'freeze v2'; v2 was already frozen (fba4259b...edd5), so this is v3 ...`

## module_v

**Cause:** ruling 5 / rule E: V records pointer

- **added** (10):
  - `$.charter.path`: `"astronomy/wave4/agent4_module_v/V_CHARTER.md"`
  - `$.charter.sha256`: `"f4bca84045ae13c2aeb86ade1fc4a204bc21260fc49b02179167c1ec2a6ca251"`
  - `$.cleared`: `33`
  - `$.not_cleared[0]`: `"L01"`
  - `$.not_cleared[1]`: `"L02"`
  - `$.not_cleared[2]`: `"L03"`
  - `$.not_cleared[3]`: `"L04"`
  - `$.not_cleared[4]`: `"L05"`
  - `$.records.path`: `"astronomy/wave4/agent4_module_v/v_records.json"`
  - `$.records.sha256`: `"462286d6b4c474091f4e03e0f7587352c4a793e73d17030627d5759cb1ea3a9a"`
- **removed** (1):
  - `$`: `{}`

## rule_E_index

**Cause:** RE-V3-02

- **added** (296):
  - `$.counts.CLEARED`: `34`
  - `$.counts.PI_RULED`: `2`
  - `$.counts.V_PENDING`: `21`
  - `$.entries[0].path`: `"$.candidates[0].cohorts.prospective_counts_w3.rule_E.O_merged"`
  - `$.entries[0].rule_E`: `"CLEARED"`
  - `$.entries[0].v_record`: `"V-C01"`
  - `$.entries[0].value`: `1937669`
  - `$.entries[10].path`: `"$.k.rule_E.chance_stated"`
  - `$.entries[10].rule_E`: `"V_PENDING"`
  - `$.entries[10].v_record`: `null`
  - `$.entries[10].value`: `0.1718`
  - `$.entries[11].path`: `"$.k.rule_E.k_binding_nights"`
  - `$.entries[11].rule_E`: `"CLEARED"`
  - `$.entries[11].v_record`: `"V-K01"`
  - `$.entries[11].value`: `61`
  - `$.entries[12].path`: `"$.k.rule_E.nights_k_not_binding"`
  - `$.entries[12].rule_E`: `"CLEARED"`
  - `$.entries[12].v_record`: `"V-K02"`
  - `$.entries[12].value`: `518`
  - `$.entries[13].path`: `"$.label_source.value.bts.category_counts.MEASURED"`
  - `$.entries[13].rule_E`: `"V_PENDING"`
  - `$.entries[13].v_record`: `"V-L03"`
  - `$.entries[13].value`: `1074`
  - `$.entries[14].path`: `"$.label_source.value.bts.category_counts.MODEL_ANNOTATION"`
  - `$.entries[14].rule_E`: `"V_PENDING"`
  - ... 271 more (reproduce with scripts/diffs.py)
- **removed** (1):
  - `$`: `{}`

## disagreements_v3

**Cause:** new wave-4 disagreements

- **added** (8):
  - `$[0]`: `"naming: brief 'freeze v2' vs frozen v2 -> v3 (NAME-V3-01)"`
  - `$[1]`: `"ruling 4 cites [803, 2247]; current producer bound [954, 2057] is V_PENDING; [803, 224...`
  - `$[2]`: `"V report lists three bound readings; the fourth combination (IAU keying + literal E5) ...`
  - `$[3]`: `"ruling 1 times mix -0500 local (15:14, 15:46) and UTC (20:48); PI's 15:46 = commit f89...`
  - `$[4]`: `"rule E scope: brief limits it to V_TARGETS; instruction marks all other numbers V_PEND...`
  - `$[5]`: `"module V overhead: self-report 51.4 min / ~125 calls vs harness 52.4 min / 122 calls"`
  - `$[6]`: `"Rubin on-sky fraction 10/15 (scheduler) vs 11/16 (Fink alert nights) in agent 2 wave-4...`
  - `$[7]`: `"power.py (vendored, unpatched) crashes with AttributeError on a ragged row instead of ...`
- **removed** (1):
  - `$`: `{}`

## open_items_carried

**Cause:** carried forward unchanged (tau, exposure_key, subject_set; S2; disagreements_v2)

- **added** (3):
  - `$[0]`: `"tau, exposure_key, subject_set: no PI ruling; D5 does not advance on them"`
  - `$[1]`: `"S2 stratum: ruling 6 (wave 3) 'reported and excluded' vs bands_FROZEN.md section 3 'no...`
  - `$[2]`: `"all disagreements_v2 entries unchanged"`
- **removed** (1):
  - `$`: `{}`
