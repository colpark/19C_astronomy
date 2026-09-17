# Can current transient-classification tools read public Rubin alert rows? A readiness recount note

<!-- nonclaim -->
**DRAFT – PI REVIEW – NOT FOR DISTRIBUTION**

- **Status:** draft for PI review only. It has not been published, posted or sent anywhere.
- **Scope:** whether each of 25 published transient tools completes its own input, compute and output path on a small sealed sample of real Rubin alert rows, and where each one stops.
- **What this note does not do:**
  - It does not measure classification quality.
  - It does not rank tools or tool families.
  - It makes no claim about which kind of model is preferable for any decision.
  - A PASS here means a tool ran end to end on these rows. It says nothing about whether the output is correct or useful.
- **Locators:** every factual sentence carries an inline locator of the form `[loc: file:Lline]` or `[loc: file#json.field]` pointing to a logged artifact in the panel repository.
- **Rule E:** the disposition tally, the pass fractions and the run count bear on a ruling. They need a module V record before they enter one, and are marked `[V: id pending]`.
  - At drafting time (2026-09-17, about 13:25Z), module V had sealed blind re-derivations for these targets but had not logged a comparison or a discrepancy record for them.
  - Update the markers before the PI uses this note.
<!-- /nonclaim -->

## 1. What was run

The recount covered 25 tool channels on up to 10 alerts each, drawn from 10 distinct diaObjectIds sealed before any run [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#population].

Each sealed alert carries 1-3 diaSources [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#alert_sample.diaSources_per_alert].

All sealed alerts sit within about 0.9 deg of ra 223.6, dec -40.0 [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#alert_sample.sky].

Every run timestamp falls after the frozen band hash of 2026-09-16T18:51:26.922781Z [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#recount_timestamps.all_runs_after_band_hash] [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#recount_timestamps.band_hash_utc].

Classification-bearing columns were stripped from the rows before anything else read them [loc: astronomy/wave3/agent4_tool_recount/REPORT.md:L49].

## 2. Pass criterion

An alert run passes only when the tool's own input path accepts the alert, the tool computes, and the tool returns output that is non-default by a rule declared per tool [loc: astronomy/wave3/agent4_tool_recount/recount_protocol_FROZEN.md:L16-L19].

A tool is PASS when at least 1 of up to 10 alert runs passes, and its pass count is reported [loc: astronomy/wave3/agent4_tool_recount/recount_protocol_FROZEN.md:L22].

A tool is FAIL when it loaded but failed at parse, infer or emit on every alert run [loc: astronomy/wave3/agent4_tool_recount/recount_protocol_FROZEN.md:L23].

Only reshaping of served field values was permitted, and a tool that needed a unit or band conversion outside its own code was recorded FAIL at parse [loc: astronomy/wave3/agent4_tool_recount/recount_protocol_FROZEN.md:L78] [loc: astronomy/wave3/agent4_tool_recount/recount_protocol_FROZEN.md:L88].

## 3. Format qualifier: JSON rows, not Avro packets

No public endpoint served lsst v11_1 Avro packets, and the Fink sources API answered an Avro request with HTTP 400 [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#packet_format_qualifier].

Every run used public Fink LSST API JSON rows carrying lsst v11_1 field names with values unchanged, and no tool was run on v11_1 Avro packets [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#packet_format_qualifier].

Every PASS below therefore holds only for public broker rows carrying v11_1 field names [loc: astronomy/wave3/agent4_tool_recount/recount_protocol_FROZEN.md:L26].

## 4. Dispositions

| Scope | PASS | FAIL | UNDEMONSTRATED | Locator |
|---|---|---|---|---|
| all 25 tools [V: T01 pending] | 2 | 14 | 9 | [loc: astronomy/wave4/agent5_integrity_closeout/logs/tool_stage_tally.json#n_tools] [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.counts_by_group_and_disposition.all] |
| inventory group FM/deep (15 tools) | 1 | 9 | 5 | [loc: astronomy/wave4/agent5_integrity_closeout/logs/tool_stage_tally.json#group_sizes.FM/deep] [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.counts_by_group_and_disposition.FM/deep] |
| inventory group classical (10 tools) | 1 | 5 | 4 | [loc: astronomy/wave4/agent5_integrity_closeout/logs/tool_stage_tally.json#group_sizes.classical] [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.counts_by_group_and_disposition.classical] |

The group rows follow the panel inventory's labels and are listed for completeness, not for comparison [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.counts_by_group_and_disposition].

## 5. Where each tool stopped

Among FAIL dispositions, 12 stopped at parse and 2 at emit, and none at infer [loc: astronomy/wave4/agent5_integrity_closeout/logs/tool_stage_tally.json#fail_stage_counts].

Four tools logged as failing at infer were reclassified to parse, because their tracebacks sit in the tool's own input handling [loc: astronomy/wave4/agent5_integrity_closeout/logs/tool_stage_tally.json#fail_stage_reclassified_tools] [loc: astronomy/wave3/agent4_tool_recount/REPORT.md:L93].

| Tool | Disposition | Stage | Logged error or reason | Locator |
|---|---|---|---|---|
| CATS (Fink) | PASS 5/10 [V: T02 pending] | – | non-default output on 5 of 10 alerts | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=CATS].pass_count] |
| GHOST | PASS 3/8 [V: T02 pending] | – | 2 runs voided after a provisioning amendment | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=GHOST]] |
| ORACLE | FAIL | parse | KeyError FLUXCAL | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=ORACLE]] |
| SuperNNova (Fink) | FAIL | parse | KeyError MWEBV, reclassified from infer | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=SuperNNova]] |
| RAPID | FAIL | parse | input validator assertion, reclassified from infer | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=RAPID]] |
| BTSbot | FAIL | parse | KeyError on ZTF metadata fields | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=BTSbot]] |
| Maven | FAIL | parse | loader requires a BTS transient table | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Maven]] |
| Astromer1 | FAIL | parse | array loader rejected the rows | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Astromer1]] |
| Astromer2 | FAIL | parse | array loader rejected the rows | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Astromer2]] |
| AstroM3 | FAIL | parse | photometry processing ValueError | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=AstroM3]] |
| ParSNIP | FAIL | parse | required key time not found | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=ParSNIP]] |
| ALeRCE BHRF | FAIL | parse | missing features | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=ALeRCE_BHRF]] |
| SALT3 (sncosmo) | FAIL | parse | no alias found for time | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=SALT3_sncosmo]] |
| Superphot+ | FAIL | parse | needs a time, phase or mjd column | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Superphot_plus]] |
| Fink EarlySNIa RF (Rubin) | FAIL | emit | code default output on every alert | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Fink_EarlySNIa_RF]] |
| Fink SLSN RF (Rubin) | FAIL | emit | code default output on every alert | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Fink_SLSN_RF]] |
| ATAT | UNDEMONSTRATED | – | checkpoint over the size cap and unpinned | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=ATAT]] |
| AstroCLIP | UNDEMONSTRATED | – | checkpoint over the size cap | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=AstroCLIP]] |
| SCONE | UNDEMONSTRATED | – | no weights | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=SCONE]] |
| AppleCiDEr | UNDEMONSTRATED | – | no weights | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=AppleCiDEr]] |
| MultibandAstromer | UNDEMONSTRATED | – | no weights | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=MultibandAstromer]] |
| Superphot | UNDEMONSTRATED | – | no trained classifier released | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Superphot]] |
| Sherlock | UNDEMONSTRATED | – | catalogue database not provisioned | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Sherlock]] |
| Blast | UNDEMONSTRATED | – | service stack; public API refuses POST | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=Blast]] |
| SNANA | UNDEMONSTRATED | – | model libraries absent | [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.per_tool[tool=SNANA]] |

## 6. What the recount cannot show

The two emit failures follow from the stream as much as from the tools, because Rubin has been off sky since mid-July and cohort objects carry 1–3 diaSources [loc: astronomy/wave3/agent4_tool_recount/REPORT.md:L136].

Construct validity and functional certification were not checked for the two PASS tools, and no alert beyond the 10 sealed ids was run [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#completeness].

Cutouts and forced photometry were not fetched under the protocol [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#completeness].

The axis records 160 alert runs against a cap of 250 [V: T03 pending] [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.alert_runs_logged] [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#value.rule_D_cap].

The same record's population field states 158 alert runs logged, and this disagreement is listed, not reconciled [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#population].

The band reading attached to this axis is recorded as stated and not ruled [loc: astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json#band_reading.note].
