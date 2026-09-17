# Wave 3 · Agent 3: manifest freezes v1 and v2, and the PI re-ratification packet

> Agent 3 returned this final report as text, because the harness blocks REPORT.md writes. The coordinator saved it here without changing its substance. It replaces the interim report committed in 8560c9f.

**Status.** Both manifests are frozen, hashed and validated. P4 still cannot rule: the Rubin cohort has no demonstrated measured labels, and the label source is unratified. The axis-ledger validator FAIL stands.

## Checks before starting
- **Brief hashes:** both verified.
- **Agent 2 hand-off files:** all 5 sha256 match the coordinator's list.
- **Agent 2 order of operations:** its census protocol hash matches, and its log shows the rule-C seal (00:11Z) before the first classification read (00:12Z).
- **Census provenance:** passes `validate.py provenance`.
- **Git:** not run, so commit ids were not checked.
- **Log:** `order_of_operations.log` steps 0–17 are hashed.
  - Step 3c corrects an "agent 2 directory absent" line.
  - Step 15 notes that step 14's text names the old axis-ledger filename, while its hash is of the `_final_` file.

## Freeze v1 (wave-2 brief): PASS
**frozen_hash `ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8`** (read-only)

**Hash method, used for both v1 and v2.** sha256 of `json.dumps(manifest with frozen_hash="", sort_keys=True, separators=(',',':'), ensure_ascii=False)` in UTF-8. The pretty-printed file on disk is not hashed. `scripts/verify_hash.py` recomputes the hash.

**Slots:**
- tau: DERIVED.
- k: RATIFIED at 8 (327/41 = 7.976, rounded).
- label_source: UNDEMONSTRATED, with the wave-2 bound [803, 2,247].
- exposure_key: DERIVED.
- tool_inventory: OVERRIDDEN. On Rubin, ATAT, Astromer1 and Astromer2 are remapped to the Fink RF; wave-1 counts are unchanged.
- delta: DERIVED at 0.018, with a warning.
- S: UNDEMONSTRATED.
- subject_set: DERIVED.
- decision_epoch: RATIFIED (first alert / night 3). It matches wave-2 agent 4's frozen E1/E3.
- Rulings holder and TNS credentials: UNDEMONSTRATED.

**Ledger and presentation.** The ledger has 10 v1 entries, each with a cause and a brief locator. `D5_presentation.md` gives each slot's derivation, its five provenance fields, and an override invitation.

**Validation.** `validate.py ledger --kind domain_manifest` PASS, and the local schema check PASS. Both checks were first shown to fire on a deliberately broken copy.

## Freeze v2 (wave-3 brief): PASS
**frozen_hash `fba4259b1d5931ff8b74a3db2f438706ce29263ef7ca373a2cb5c5fd7f2cedd5`** (read-only)

It is built from the verified v1 and the pre-handoff draft (sha `38bbf3d4…`, kept on record).

**Rulings 1–6 (AMD-V2-01..08):**
- Budget: 1,000 arm cells plus 200 engineering hours.
- S: UNDEMONSTRATED until R1.
- Cost of action: 0.5 h P60 per spectrum; 1 slot per wrong commitment; ≥100 slots per missed rare event (asymmetric).
- Delta: OVERRIDDEN to 0.05, with 0.018 kept as the prior.
- Graph staging: ratified; the compositions stay PRE-I1.
- Rulings holder: named by role; transfer PENDING_RECEIPT.
- TNS: BLOCKED.
- Epoch: reaffirmed, with strata S0, S1 and S2.

**Wave-3 counts folded in:**
- Agent 1's cohort: O = 1,937,669; S1 = 521,920.
- Agent 4's recount: 2 PASS, 14 FAIL, 9 UNDEMONSTRATED.

**Agent 2's results folded in (resolves PENDING-V2-01):**
- **SU-V2-03, label source:** SNIascore bound [954, 2,057]; 5,815 unresolved; UNDEMONSTRATED. Measured labels on the Rubin cohort are UNDEMONSTRATED.
- **SU-V2-04, monthly supply:** lower bounds only, over all TNS objects rather than the cohort. Jan–Sep: ≥181 spectroscopic units, ≥161 of them non-bot.
- **SU-V2-05, truth cost:** attached as the ruling-1 re-ratification input, not as a ruling.
- **FRZ-V2:** the freeze entry.

**Ledger hashes.** The canonical hash of each entry set was recorded and re-verified: v1 unchanged, v2 `a1feebcb…`.

**Validation.** `validate.py` PASS, schema check PASS, and v1 and v2 hashes MATCH.

**D5 disposition: UNDEMONSTRATED (does not advance).**
- tau, exposure_key and subject_set have no PI ruling, and they were not ratified on the PI's behalf.
- label_source is UNDEMONSTRATED.
- S waits on R1.

## Axis ledger re-run against the FROZEN bands
File: `axis_ledger_v2_final_against_frozen_bands.json`. There is no re-banding: the bands are at δ 0.018, and the δ 0.05 thresholds (63–1,666 objects, 6–197 nights) are listed beside them.

**Axis readings:**
- **contamination_exposure: ESCALATE.** Gemini 3.1 Pro has no published cutoff.
- **tool_coverage: ESCALATE.** CATS passes 5/10, but both Rubin counterparts fail at emit.
- **cluster, split, unprocessable: PROCEED.**
- **positive and negative supply: UNDEMONSTRATED.**

**P4 preconditions:**
- **(a) UNMET.** Checked against agent 2's files.
  - Zero measured non-bot reports on cohort objects. Only 13 of 627 cohort-matched captures were readable (614 HTTP errors), so this is UNDEMONSTRATED, not zero.
  - The 13 typed objects have unknown classifiers, so they fail bands §4.
  - There is no posA/neg split, so P and Ng cannot be computed.
- **(b) CLEARED, independently verified.**
  - All 198 run rows are after both the band hash and the recount protocol freeze.
  - Every logged hash matches its file.
  - Recomputed passes match.
  - Agent 1's wave-3 protocol and seal also post-date the band.
  - Limit: timestamps are self-logged on one host.
- **(c) UNMET.** No ratified label source.

**Validation.** FAIL on the null ruling, and that FAIL stands. **Binding axis: positive supply at measured labels.**

## `PI_rerat_packet.md` (one page)
The packet covers:
- Measured cohort supply: none demonstrated.
- Monthly supply as lower bounds; f19 = 0.004; ~775 reachable arrivals per on-sky night.
- Truth cost at both deltas:
  - δ 0.05, N = 63: 66–84 spectra, 33–42 P60 h, 7–19 on-sky nights.
  - δ 0.05, N = 1,666: 1,723–2,212 spectra, 862–1,106 h, 173–492 nights.
  - δ 0.018, N = 485: 502–644 spectra, 251–322 h, 51–144 nights.
  - δ 0.018, N = 12,855: 13,294–17,065 spectra.
  - Every row adds ≥100 slots per missed rare event.
- P60 hours are not the arm-cell or engineering-hour budget, and calendar time is unknown.
- The ESCALATE readings. With the subject set unchanged, the frozen rule cannot reach PROCEED.
- Slots awaiting the PI: tau, exposure_key, subject_set and label_source.
- The S2 conflict.
- Four decisions requested: whether paid work starts; the slot rulings; S2; and whether to re-band at 0.05.

## Disagreements (left as recorded, not reconciled)
1. **S2:** ruling 6 says "reported and excluded", but the frozen bands keep S2 in the cohort.
2. **D5 closure:** tau, exposure_key and subject_set have no PI ruling.
3. **Truth-cost target:** 485 comes from the 0.018 bracket, while delta is overridden to 0.05.
4. **Rare-miss cost:** the cost of a missed rare event does not fit a delta on the committed-set purity scale.
5. **Recount format:** agent 4 recounted on JSON rows, against preamble item 5.
6. **Recount runs:** 158 on the axis vs 160 in the run log.
7. **Subject set size:** 7 models vs 10 in the exposure-key table.
8. **AstroM3 weights:** absent in wave 1, now public.
9. **TNS discovery date:** not a safe lower bound for label publicity.
10. **From agent 2:**
    - The sealed non-bot share range (0.5–0.85) vs 0.89 observed.
    - 13 typed objects vs 0 measured labels.
    - 10 on-sky nights vs 9 alert dates.
    - Trigger purity 0.967 vs 0.956.
    - Rochester totals of 17,562 vs 19,448.
    - ANTARES position leak.

## Replay cases (`replay_cases.csv`, `replay_rulings.csv`)
- **AST3W3-01** (D5, must_fire): slots ratified on the strength of a coordinator sentence.
- **AST3W3-02** (P4, must_not_fire): ledger rebuilt without re-banding, recount verified, ruling left null.
- **AST3W3-03** (D5, must_fire): S2 silently dropped to match a ruling.
- **AST3W3-04** (D5, must_not_fire): approved remapping applied without touching the counts.

## Dispositions

| Criterion | Disposition |
|---|---|
| Brief and handoff hashes verified | PASS |
| v1 frozen, hashed, validated | PASS |
| v2 frozen, hashed, validated (same method) | PASS |
| Amendment ledger (v1: 10, v2: 15 entries) | PASS |
| PENDING-V2-01 resolved | PASS |
| D5 presentation with override invitations | PASS |
| D5 advance (every slot ratified or overridden) | UNDEMONSTRATED (FAIL on the criterion) |
| Axis ledger against frozen bands, no re-banding | PASS |
| P4 precondition (b) | PASS (cleared, verified) |
| P4 preconditions (a), (c) | FAIL (unmet) |
| Axis-ledger validator | FAIL (stands) |
| Measured Rubin cohort labels (P, Ng) | UNDEMONSTRATED |
| Ruling-1 re-ratification | UNDEMONSTRATED (awaiting PI; packet delivered) |
| S | UNDEMONSTRATED (R1) |
| Rulings transfer | UNDEMONSTRATED (PENDING_RECEIPT) |
| TNS | BLOCKED |
