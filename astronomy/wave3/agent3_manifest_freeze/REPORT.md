# Wave 3 · Agent 3: manifest freeze (v1 frozen; v2 draft pending agent 2)

> Agent 3 returned this report as text, because the harness blocks REPORT.md writes. The coordinator saved it here without changing its substance, apart from one correction marked [coord].

## Status
- **v1 is frozen and validates.**
- **v2 is not frozen.** It waits on agent 2's wave-3 results, as instructed.
- **P4 still cannot rule.** Precondition (b) clears under agent 3's own verification, but (a) and (c) remain unmet, so the axis-ledger validator FAIL stands.

## Checks before starting
- **Brief hashes:** both verified. Wave 2 is `31a36617…f4eb` and wave 3 is `a618d911…c4b6`.
- **Inputs:** every listed brief, skill file, schema, validate.py and slot record was read. `seed_ledger.json` has 51 files, 40 of them read in full, and marks the partial reads.
- **Scope:** no git was run, and nothing was written outside this directory.
- **Agent 2's directory:** `wave3/agent2_measured_labels/` appeared mid-run. It was listed but none of its files were opened. Log step 3c corrects an earlier "absent" line.
- **Order:** log steps 0–12 are hashed at every step.

## Part 1: freeze v1 (wave-2 brief)
**frozen_hash `ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8`**
- **Method:** sha256 of `json.dumps(manifest with frozen_hash="", sort_keys=True, separators=(',',':'), ensure_ascii=False)` in UTF-8. The pretty-printed file on disk is not what gets hashed.
- **Check:** `scripts/verify_hash.py` recomputes the hash and reports MATCH.
- **File state:** set read-only.

| Slot | v1 status | Basis |
|---|---|---|
| tau | DERIVED | 1″ plateau with controls; no PI ruling |
| k | RATIFIED | 8; rounding 327/41 = 7.976 noted (AMD-V1-01) |
| label_source | UNDEMONSTRATED | wave-2 agent 2 slot: SNIascore 803–2,247; 6,156 unresolved |
| exposure_key | DERIVED | no PI ruling |
| tool_inventory | OVERRIDDEN | Fink RF remapping (AMD-V1-03) |
| delta | DERIVED | 0.018 with a resolution warning; cost of action not yet supplied |
| S | UNDEMONSTRATED | no budget; R1 not run |
| subject_set | DERIVED | no PI ruling |
| decision_epoch (new D4 slot) | RATIFIED | first alert / night 3 (AMD-V1-02) |

- **Fink RF remapping:** the Rubin counterpart for ATAT, Astromer1 and Astromer2 is now Fink_EarlySNIa_RF and Fink_SLSN_RF, stored in `counterparts_by_survey.rubin`.
  - The wave-1 `counterparts` field, the ZTF mapping and every wave-1 count are unchanged.
  - Check (a) holds structurally on Rubin but fails functionally (see Part 2).
- **Epochs:** wave-2 agent 4's E1 and E3 (`compositions_FROZEN.md` §1) were re-checked against the ratified slot and match.
- **Unfilled SUPPLY fields:** the rulings holder and TNS credentials are UNDEMONSTRATED in v1.
- **`amendment_ledger.json`:** 10 v1 entries, each with its cause and a brief locator. The v1 entries carry their own canonical hash (`9643f2d4…`), re-verified after the v2 entries were appended.
- **`D5_presentation.md`:** each slot's derivation, its five provenance fields copied from the frozen file, and an override invitation.

**Validation (`validate_v1_stdout.txt`):**
- `validate.py ledger --kind domain_manifest`: **PASS**.
- Local schema check: **PASS**. jsonschema is not installed, so a minimal checker was written.
- Both checks fired on a deliberately broken copy (bad status, missing falsifier, empty hash) before the freeze.
- No fixes were needed. validate.py checks structure and provenance, not slot status, so it passes even though label_source and S are UNDEMONSTRATED.

**D5 disposition: UNDEMONSTRATED (does not advance).**
- Frozen and hashed: PASS.
- Every slot ratified or overridden: FAIL.
- The wave-2 brief says "This closes D5 for everything except the two SUPPLY fields". The PI rulings, however, cover only k, the epoch and the remapping. tau, exposure_key and subject_set were not ratified on the PI's behalf.

## Part 2: v2 draft (wave-3 brief)
`domain_manifest_v2_DRAFT.json` starts from the verified v1. It applies PI rulings 1–6 as AMD-V2-01..08, folds in wave-3 counts from agents 1 and 4 (SU-V2-01, SU-V2-02), and marks agent 2's inputs PENDING-V2-01.

**Rulings applied:**
- **Budget:** 1,000 arm cells (hard cap) plus 200 engineering hours, supplied.
- **S:** UNDEMONSTRATED until R1. A planning sum sits beside it, clearly labelled as not S: 71 rounds at 7 subjects × 2 agent arms, or 498 rounds for one subject.
- **Cost of action:** 0.5 h P60 per spectrum; a wrong routine commitment costs 1 slot; a missed rare event costs ≥100 slots (asymmetric).
- **Delta:** OVERRIDDEN to 0.05, with 0.018 kept as the literature prior.
  - Calibration MDE is 0.032: RESOLVABLE at 0.05 (N_min 26), CLOSE_UNRESOLVABLE at 0.018 (N_min 196).
  - The agent's text said "wave-4 calibration" here. [coord] It means the wave-3 agent-4 recalibration of the wave-2 compositions.
- **Graph escalation:** ratified as staged. The compositions stay PRE-I1 and the edges are unweakened.
- **Rulings holder:** named by role. Transfer is PENDING_RECEIPT; non-authorship is not verified.
- **TNS:** BLOCKED.
- **Epoch:** stays RATIFIED. Strata: S0 = 112,990 loci, S1 = 521,920, S2 UNDEMONSTRATED (needs PPDB).

**Counts folded in:**
- **Cohort:** O = 1,937,669. This is an upper bound, because the PPDB has not been released.
- **Position leak:** 193 of 9,000 cohort positions had a public alert before the cutoff.
- **Functional recount on Rubin:** 2 PASS, 14 FAIL, 9 UNDEMONSTRATED.

**Validation (`validate_v2_draft_stdout.txt`):** FAIL only on the empty `frozen_hash`, which is empty by design. All slot provenance passes, and the schema check passes.

### Axis ledger v2 against the frozen bands
File: `axis_ledger_v2_against_frozen_bands.json`. No re-banding: bands stay at 0.018, and the 0.05 thresholds (63–1,666 objects, 6–197 nights) are listed beside them.

**Axis readings:**
- **Tool coverage: ESCALATE.** CATS accepts Rubin inputs, so not CLOSE. Both Rubin counterparts (the Fink RFs) FAIL at emit, so not PROCEED. This holds whatever qualifier is attached to the JSON-row format.
- **Contamination:** ESCALATE.
- **Cluster, split, unprocessable:** PROCEED.
- **Positive and negative supply:** UNDEMONSTRATED.

**Preconditions:**
- **(a) UNMET:** no measured P or Ng. TNS is BLOCKED and agent 2 is pending.
- **(b) CLEARED, independently verified:**
  - The bands hash matches its log entry (18:51:26Z; file mtime 18:51:19Z; read-only).
  - All 198 run-log rows start after the band hash and after the recount-protocol freeze. The earliest is 20:55:49Z.
  - Every logged hash matches its file: protocol, sealed ids, run log and coverage axis.
  - 160 alert runs, within the cap of 250.
  - Recomputed per-tool passes match: CATS 5/10, GHOST 3/8 with 2 voided.
  - Agent 1's wave-3 count protocol and sealed counts also post-date the band and match their hashes.
  - Limit: timestamps are self-logged by agents on one host. This is a consistency check, not independent notarisation.
- **(c) UNMET:** label source not ratified.

**Validation (`validate_axis_v2_stdout.txt`):** FAIL on the missing ruling, which stands. Unmet preconditions (a) and (c) are named. **Binding axis:** positive supply at measured labels.

**Note for the PI (not a ruling):** contamination and tool coverage both read ESCALATE. The bands cannot yield PROCEED even after (a) and (c) clear, unless the subject set changes.

### v2 freeze pending
`v2_freeze_pending.md` lists what v2 is waiting for:
- agent 2's census, as monthly P per programme;
- agent 2's truth cost;
- any updated label slot, and track-one status;
- the coordinator's hand-off of those files with hashes.

## Disagreements (listed, not reconciled)
1. **S2 stratum:** ruling 6 says S0/S1/S2 are "reported and excluded", but the frozen bands keep S2 in the cohort. Excluding S2 needs a new hashed band registration. No count moves today, since S2 cannot yet be counted.
2. **D5 closure:** the wave-2 brief expects D5 closed except the SUPPLY fields, but the PI rulings do not cover tau, exposure_key or subject_set.
3. **Truth-cost target:** priced at 485 objects, the lower bound at delta 0.018. At the overridden 0.05 the planning range is 63–1,666.
4. **Metric vs cost:** the ≥100-slot rare-miss cost does not fit a delta measured on committed-set purity. The A1 metric is not registered.
5. **Recount format:** preamble item 5 says "no substitute format improvised", but agent 4 ran on Fink JSON rows rather than Avro.
6. **Run count:** `tool_coverage_axis.json` says 158 alert runs; the run log has 160 (158 plus 2 voided).
7. **Subject count:** the subject_set has 7 models; the exposure-key cutoff table has 10.
8. **AstroM3 weights:** wave 1 recorded none; they are now public. The wave-1 count is unchanged.
9. **TNS discovery date:** not a safe lower bound for label publicity (SN2017bde).

## Replay cases (`replay_cases.csv`, `replay_rulings.csv`)
- **AST3W3-01** (D5, must_fire): slots ratified on the strength of a coordinator sentence.
- **AST3W3-02** (P4, must_not_fire): ledger rebuilt without re-banding, recount verified, ruling left null.
- **AST3W3-03** (D5, must_fire): S2 silently dropped to match a ruling.
- **AST3W3-04** (D5, must_not_fire): approved remapping applied without touching the counts.

## Dispositions

| Criterion | Disposition |
|---|---|
| Brief hashes verified | PASS |
| v1 assembled (10 slots + decision_epoch, five provenance fields, status) | PASS |
| v1 frozen and hashed; method recorded; hash re-verified | PASS |
| v1 validate.py domain_manifest | PASS |
| Amendment ledger | PASS |
| D5 presentation with override invitations | PASS |
| D5 advance (every slot ratified or overridden) | UNDEMONSTRATED (the criterion itself FAILs) |
| Fink remapping applied, wave-1 counts untouched | PASS |
| v2 draft with PENDING inputs marked | PASS |
| v2 freeze | UNDEMONSTRATED (awaiting agent 2) |
| Axis ledger against frozen bands, no re-banding | PASS |
| P4 precondition (b), own verification | PASS (cleared) |
| P4 preconditions (a), (c) | FAIL (unmet) |
| Axis-ledger validator | FAIL (stands by design) |
| S | UNDEMONSTRATED (R1) |
| Rulings transfer | UNDEMONSTRATED (PENDING_RECEIPT) |
| TNS | BLOCKED |
