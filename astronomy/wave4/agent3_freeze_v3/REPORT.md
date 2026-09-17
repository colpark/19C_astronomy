# Wave 4 · Agent 3: freeze v3

> Agent 3 returned this report as text, because the harness blocks REPORT.md writes. The coordinator saved it without changing its substance.

**Result.** v3 is frozen, hashed and validated.
- **P4 still cannot rule.** Precondition (a) is unmet: there are no measured labels, because TNS and WISeREP are both BLOCKED.
- **Preconditions (b) and (c) clear.**
- **The axis-ledger validator FAIL stands.**

## Checks before starting
- **Brief:** hash verified (`8f101811…1b58`); preamble items 1–7 read.
- **Module V files:**
  - `discrepancies/SHA256SUMS`: 5/5 OK.
  - `sealed/SEALED_SHA256SUMS`: 39/39 OK. The first attempt ran from the wrong directory and gave false failures (log step 1b).
  - `V-L-r1.json`: hash matches.
- **Earlier freezes:** v1 (`ca00efe0…cbae8`) and v2 (`fba4259b…2cedd5`) recompute MATCH and were left untouched.
- **Git and scope:** no git was run. Everything was written under this directory.

## Naming disagreement (NAME-V3-01)
The brief says "freeze v2", but v2 is already frozen. This freeze is **v3**, and it is the manifest P4 reads. The mismatch is recorded as a disagreement, not substituted silently.

## Freeze v3: PASS
**frozen_hash `bd0fa4c67cdbbfb0b8eea9822f536bed4bf934ee1bc81a02606ed6d5ee9585bc`** (read-only). The canonical-hash method is the same as v1 and v2, imported from the wave-3 script rather than copied.

**Validation:** `validate.py ledger --kind domain_manifest` PASS, schema check PASS, and v1/v2/v3 all MATCH.

## Amendments (`amendment_ledger_v3.json`)
The ledger is append-only. v1 and v2 entries are copied verbatim, with their hashes re-verified.

**AMD-V3-01: ruling 1, delta 0.05 RATIFIED** (was OVERRIDDEN). 0.018 stays as the literature prior.
- **Cause check V-O01:** MATCH_WITHIN_TOL. Order: override at 20:14:03Z, then the first power file at 20:44:29Z (earliest output 20:43:28Z), then resolvability at 0.05 at 20:48:29Z.
- **Time zones:** the PI's 15:14 and 15:46 are −0500 local; 20:48 is UTC.
- **Caveats:**
  - commit times are quoted, not read, since no git was run;
  - mtime reflects only the last write;
  - the host clock is not independently trusted;
  - the practitioners' ~0.045 MDE that the override cites predates the override.

**AMD-V3-02: ruling 4, label_source RATIFIED WITH CONDITIONS.** The four condition lines are recorded verbatim.

**RE-V3-01: rule E, label_source numbers V_PENDING.**
- **Pending values:** bound [954, 2,057] and counts 1,074 / 954 / 5,815. V's blind values are recorded beside them.
- **Readings that need a ruling:**
  - **(i) E5 cut:** the frozen text says 1259.5, but its own arithmetic gives 1289.5, which is what the producer implemented.
  - **(ii) Twin rows sharing an IAU name:** key them per ZTFID (as the producer did) or per IAU name.
- **Own check against `sealed/V-L-r1.json`:** all four readings fall inside [803, 2,247]:
  - [954, 2,057]
  - [954, 2,139]
  - [955, 2,056]
  - [955, 2,138]. V's report does not list this combination.
- **New finding:** ruling 4's own interval [803, 2,247] reproduces only under the 1289.5 cut. On wave-2 captures, the literal 1259.5 cut gives [803, 2,329]. The ruling-4 condition holds under every reading, but the ruled interval itself depends on reading (i).

**AMD-V3-03: precondition (c) clears under ruling 4.** It clears by ratified definition, not by a count, so it does not depend on the V_PENDING numbers.

**AMD-V3-04: ruling 3, TNS BLOCKED** (second record; dates 2026-09-16 and 2026-09-17). The sanctioned WISeREP check is also BLOCKED: live site HTTP 403, archive 404.

**AMD-V3-05: ruling 2, custody PENDING_RECEIPT.** receipt_hash is empty, and "procedural" stays on every blind result.

**AMD-V3-06: ruling 5, module V chartered; overhead cap EXCEEDED (interim).**
- V used 47% of wall time (52.4 of 110.7 min) and 59% of tool calls (122 of 207), against a 15% cap. The arithmetic was re-checked.
- V's self-report differs slightly: 51.4 min and ~125 calls.

## Rule E marking (RE-V3-02, `rule_E_index`)
Totals: 34 CLEARED, 21 V_PENDING, 2 PI_RULED.

**CLEARED (with their V records):**
- cohort C01–C04
- power P01–P08, at both deltas
- K01–K02
- AUCs A01–A04
- N brackets N01–N02. The 12,855 and 1,666 values are driven by the sample SD (0.728). The theoretical √q would give 12,113 and 1,570. V calls this not a discrepancy.
- truth cost R01–R04
- tool tally T01–T03
- O01
- precondition (b) O02
- POLICY Q01–Q04 (listed as cleared; not carried in the manifest)

**V_PENDING (no V record):**
- k = 8, 46.41 candidates and chance 0.172
- tau 1″ and 11,183 clusters
- U = 0
- 9 cohort nights
- S0 = 112,990
- the 0.018 prior
- night brackets 40–1,515 and 6–197
- census lower bounds
- leak counts
- monthly pricing
- L01–L05

**PI_RULED:** budget of 1,000 arm cells and 200 engineering hours.

**Scope disagreement.** The brief limits rule E to V's 38 targets, and everything else proceeds unverified. Marking the remaining numbers V_PENDING, as the coordinator instructed, therefore blocks nothing under the brief's own rule.

## Carried forward unchanged
- tau, exposure_key and subject_set have no PI ruling, so D5 does not advance on them.
- The S2 stratum conflict.
- Every v2 disagreement.

## Diffs (`diff_v1_v2.md`, `diff_v2_v3.md`)
Both diffs are generated from the frozen files. Each changed key carries its status before and after, the leaf-path changes, and a cause (ledger id plus brief locator). The generator script fails if any changed key lacks a cause.

**v1→v2:**
- label_source (SU-V2-03)
- delta DERIVED→OVERRIDDEN (AMD-V2-04)
- S, decision_epoch, tool_inventory, exposure_key, candidates, supply fields, graph

**v2→v3:**
- delta OVERRIDDEN→RATIFIED (AMD-V3-01)
- label_source UNDEMONSTRATED→RATIFIED (AMD-V3-02, RE-V3-01)
- TNS and custody (AMD-V3-04, AMD-V3-05)
- rule-E marks on every other slot
- tau, k, subject_set, S and epoch keep their values and statuses

## Axis ledger v3 against the FROZEN bands (`axis_ledger_v3_against_frozen_bands.json`)
No re-banding. Bands stay at 0.018, with the 0.05 thresholds listed beside them.

| Axis | Reading |
|---|---|
| contamination_exposure | ESCALATE |
| tool_coverage | ESCALATE |
| cluster_structure | PROCEED |
| split_integrity | PROCEED |
| unprocessable_units | PROCEED |
| positive_supply | UNDEMONSTRATED |
| negative_supply | UNDEMONSTRATED |

Every number carries a V id or V_PENDING. Two PROCEED readings rest partly on V_PENDING numbers:
- **cluster_structure:** the Fink and ANTARES counts are V_PENDING, though each clears the band edge by more than 100×.
- **unprocessable_units:** U = 0 has no V record.

**Preconditions:**
- **(a) UNMET:** TNS BLOCKED twice; WISeREP BLOCKED.
- **(b) CLEARED:** V-O02, plus own wave-3 check.
- **(c) CLEARED:** ruling 4.

**Validator: FAIL** on the null ruling. The FAIL stands, and precondition (a) is named. Note for agent 1, not a ruling: with the subject set unchanged, the bands cannot reach PROCEED.

## Replay cases (`replay_cases.csv`, `replay_rulings.csv`)
- **AST3W4-01** (D5, must_fire): uncleared label numbers frozen as cleared on the strength of a non-blind re-parse.
- **AST3W4-02** (P4, must_not_fire): (c) cleared by ratification, readings checked from the sealed file, (a) unmet, FAIL left standing.
- **AST3W4-03** (D5, must_fire): frozen v2 re-opened and re-hashed in place.

## Dispositions

| Criterion | Disposition |
|---|---|
| Brief and V hashes verified | PASS |
| v3 frozen, hashed, validated | PASS |
| v1→v2 and v2→v3 diffs, with a cause per changed key | PASS |
| Amendment ledger v3 (append-only) | PASS |
| Delta 0.05 ratified with cause check | PASS |
| Label source ratified with conditions | PASS |
| Label numbers L01–L05 | UNDEMONSTRATED (V_PENDING; two readings unruled) |
| Every reading inside [803, 2,247] (own check) | PASS |
| Precondition (a) | FAIL (unmet) |
| Precondition (b) | PASS (V-O02) |
| Precondition (c) | PASS (ruling 4) |
| Axis-ledger validator | FAIL (stands) |
| D5 advance | UNDEMONSTRATED (FAIL on the criterion: tau, exposure_key, subject_set) |
| S2 conflict | UNDEMONSTRATED (unruled) |
| TNS and WISeREP | BLOCKED |
| Custody | UNDEMONSTRATED (PENDING_RECEIPT; procedural) |
| Module V overhead cap | FAIL (interim) |
