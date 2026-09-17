# What the ZTF Bright Transient Survey labels rest on: a provenance note

<!-- nonclaim -->
**DRAFT – PI REVIEW – NOT FOR DISTRIBUTION**

- **Status:** draft for PI review only. It has not been published, posted or sent anywhere.
- **Scope:** where the type labels in the public BTS sample come from, measured by a human classifier or annotated by a model. It also covers the evidence field that tells the two apart, the bound on model annotation, and one admissibility rule for items whose answer sits in their own source text.
- **What this note does not do:** it compares no tools or models, and it makes no claim about which approach is preferable.
- **Locators:** every factual sentence below carries an inline locator of the form `[loc: file:Lline]` or `[loc: file#json.field]`. Locators point to logged artifacts in the panel repository.
- **Rule E:** any number here that bears on a ruling (the SNIascore bound and the label category counts) needs a module V record before it enters a ruling. Module V targets are marked `[V: id pending]`. At drafting time (2026-09-17, about 13:25Z), `astronomy/wave4/agent4_module_v/sealed/` held no file for L01–L05, and `discrepancies/` was empty. No V record for these numbers existed. Update the markers before the PI uses this note.
- **Calibration only:** the BTS label base is calibration material only for this panel, because it failed the contamination check.
<!-- /nonclaim -->

## 1. Population

The labelled population is 7,843 BTS rows [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.population].

The panel's label-source slot is still UNDEMONSTRATED [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#status].

## 2. The categories and the field that decides them

A label is MEASURED when its TNS classification report names one or more people in the Classifier/s field and carries no automated-classifier marker [loc: astronomy/wave2/agent2_label_source/definitions_FROZEN.md:L30].

A label is MODEL_ANNOTATION when the Classifier/s field of its report carries an automated-classifier marker [loc: astronomy/wave2/agent2_label_source/definitions_FROZEN.md:L33].

The markers are `SNIascore`, `CCSNscore`, and the whole words bot, robot, automatic, automated and auto, matched in the Classifier/s field only [loc: astronomy/wave2/agent2_label_source/definitions_FROZEN.md:L44-L51].

The reporter name `ZTF_Bot1` in the Sender field is not treated as evidence of automation [loc: astronomy/wave2/agent2_label_source/definitions_FROZEN.md:L74].

## 3. Classifier/s evidence from archived TNS pages

Archived TNS pages show SNIascore reports with Sender `ZTF_Bot1` and Group `ZTF` [loc: astronomy/wave2/agent2_label_source/REPORT.md:L35].

The Classifier/s string reads "SNIascore on behalf of the SEDM Team…" or, from about September 2022, names three people "on behalf of the SEDM Team … based on SNIascore" [loc: astronomy/wave2/agent2_label_source/REPORT.md:L36].

`ZTF_Bot1` also sends human reports, so the sender name cannot separate the two categories [loc: astronomy/wave2/agent2_label_source/REPORT.md:L37].

A reading of classifier names alone would count the later SNIascore strings as measured, because those strings carry human names [loc: astronomy/wave2/agent2_label_source/REPORT.md:L113].

SNIascore is a binary SN Ia classifier, and SEDM cannot separate Ia subtypes except in clear-cut cases, so any type except plain `SN Ia` is not SNIascore annotation [loc: astronomy/wave2/agent2_label_source/definitions_FROZEN.md:L68].

The earliest SNIascore report seen on parsed pages is dated 2021-04-15 04:27:13 [loc: astronomy/wave2/agent2_label_source/split_summary.json#sniascore_reports_seen.earliest].

No parsed SNIascore report carries a non-SN-Ia class [loc: astronomy/wave2/agent2_label_source/split_summary.json#sniascore_reports_seen.sniascore_report_not_SN_Ia].

The evidence route was public Internet Archive captures of TNS object pages [loc: astronomy/wave2/agent2_label_source/REPORT.md:L8].

Live TNS without credentials returned HTTP 403 on every path [loc: astronomy/wave2/agent2_label_source/REPORT.md:L28].

The credentialed route stays BLOCKED [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.track_one.status].

## 4. The SNIascore bound

| Recorded bound on SNIascore-annotated labels | Value | Locator |
|---|---|---|
| first panel bound | [0, 3131] | [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.sniascore_bound.wave1] |
| second bound | [803, 2247] | [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.sniascore_bound.previous] |
| current lower bound | 954 [V: L01 pending] | [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.sniascore_bound.lower] |
| current upper bound | 2057 [V: L02 pending] | [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.sniascore_bound.upper] |

The update rule adds new SNIascore placements to the lower bound, removes new non-SNIascore placements from the upper bound, and never widens it [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.sniascore_bound.rule].

Without the WEAK peak-date exclusion the upper value would be 2654, which is recorded as a sensitivity and not as the slot value [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.sniascore_bound.upper_noE5_sensitivity_not_slot_value].

The PI ratified the label source with conditions citing the interval [803, 2247] of 7843 [loc: astronomy/wave4/PANEL_BRIEF_WAVE4.md:L17].

The coordinator preamble records that the interval [954, 2057] lies strictly inside [803, 2247] [loc: astronomy/wave4/PANEL_BRIEF_WAVE4.md:L109].

## 5. Category counts over the 7,843 labels

| Category | Labels | Locator |
|---|---|---|
| MEASURED | 1074 [V: L03 pending] | [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.category_counts.MEASURED] |
| MODEL_ANNOTATION | 954 [V: L04 pending] | [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.category_counts.MODEL_ANNOTATION] |
| PHOTOMETRIC_ONLY | 0 | [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.category_counts.PHOTOMETRIC_ONLY] |
| UNRESOLVED (UNDEMONSTRATED) | 5815 [V: L05 pending] | [loc: astronomy/wave3/agent2_measured_labels/label_source_slot.json#value.bts.category_counts.UNRESOLVED_UNDEMONSTRATED] |

For any future paid claim, the PI ruling defines measured truth as human-classifier-confirmed labels only, with a sensitivity row both ways [loc: astronomy/wave4/PANEL_BRIEF_WAVE4.md:L19].

## 6. Known weak points, as logged

The peak-date exclusion rule is WEAK, and 2 of 799 SNIascore reports came over 30 d after peak [loc: astronomy/wave2/agent2_label_source/REPORT.md:L111].

For 31 objects an earlier SNIascore report had been superseded by a later report, and a later human re-report cannot be ruled out for older captures [loc: astronomy/wave2/agent2_label_source/split_summary.json#sniascore_reports_seen.sniascore_earlier_report_superseded] [loc: astronomy/wave2/agent2_label_source/REPORT.md:L115].

Whether "Atlas Syncatto (SCAT)" is an automated pipeline is unresolved, and it classified 11 labels counted MEASURED [loc: astronomy/wave2/agent2_label_source/REPORT.md:L114].

## 7. Answer in the item's own source (refusal 14)

A seed text that states the class, where the seed predates every subject's cutoff, is refused [loc: astronomy/wave2/agent2_label_source/definitions_FROZEN.md:L122].

A name that occurs with no stated class is admissible for calibration only, under a written exposure ruling [loc: astronomy/wave2/agent2_label_source/definitions_FROZEN.md:L123].

| Refusal-14 count | Value | Locator |
|---|---|---|
| objects flagged by the corpus agent | 98 | [loc: astronomy/wave2/agent2_label_source/refusal14_rulings.json#counts.agent1_flagged] |
| of those, REFUSE | 92 | [loc: astronomy/wave2/agent2_label_source/refusal14_rulings.json#counts.agent1_REFUSE] |
| of those, NOT_FIRED_NAME_ONLY | 6 | [loc: astronomy/wave2/agent2_label_source/refusal14_rulings.json#counts.agent1_NOT_FIRED_NAME_ONLY] |
| of those, unlabelled in BTS | 3 | [loc: astronomy/wave2/agent2_label_source/refusal14_rulings.json#counts.agent1_unlabeled_in_bts] |
| additional objects from further seeds | 17 | [loc: astronomy/wave2/agent2_label_source/refusal14_rulings.json#counts.wave2_additional] |
| of those, REFUSE | 12 | [loc: astronomy/wave2/agent2_label_source/refusal14_rulings.json#counts.wave2_additional_REFUSE] |

Every one of these rulings governs calibration use only, and none admits a BTS item to a scored subject comparison [loc: astronomy/wave2/agent2_label_source/refusal14_rulings.json#scope_statement].
