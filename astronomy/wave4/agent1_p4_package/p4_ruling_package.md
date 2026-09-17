# P4 ruling package: Rubin prospective cohort (agent 1, wave 4)

## Decision: P4 REFUSES TO RULE. No PROCEED, CLOSE or ESCALATE.
- **Skill text.** `references/stages/supply.md` line 37: P4 "Refuses to rule at all when any of the seven axes in P3 is missing a number."
- **Frozen bands.** `bands_FROZEN.md` §7 line 184: "Each one unmet means no ruling; name it."
- **The missing numbers.** positive_supply and negative_supply are UNDEMONSTRATED. Measured labels cannot be read: TNS is BLOCKED (records of 2026-09-16 and 2026-09-17), and WISeREP is BLOCKED (live HTTP 403; 43/43 archived pages 404, including the classified controls).
- **Unmet precondition: (a).** (b) cleared (V-O02). (c) cleared by ratification (PI ruling 4, not a count).
- **No CLOSE is being withheld.** On V-cleared numbers, no axis reads CLOSE at either δ (comparisons below).
- **Not forced to ESCALATE.** ESCALATE is a ruling, and it needs all seven numbers. The escalation to the PI goes through the loop ladder instead (`escalation_memo.md`, rung 2, labelled as not a P4 ruling).

**Binding axis: positive_supply, with negative_supply, at measured labels.** Under the §7 refusal rule it is the unmet precondition that needs an external input (label access, or a funded human-confirmed spectroscopy program) and survey time (Rubin off sky since 2026-07-14, no return date).

## Inputs, verified
- **v3 manifest:** file sha256 `0bdf229e…3b6c`; `frozen_hash` `bd0fa4c6…85bc`, recomputed independently with the stated method: MATCH (`out/input_verification.json`).
- **axis_ledger_v3:** `83e75757…1a50`. **v_records.json:** `462286d6…3a9a`. **truth_cost_monthly.json:** `2f679148…52bf`. **bands_FROZEN.md:** `8825ef80…00d2`. Brief: `8f101811…1b58`.
- **Rule C:** no label field was read.

## Band readings per axis
Bands are frozen at δ 0.018; the ratified 0.05 is reported beside them, with no re-banding.

| Axis | Number (V id) | δ 0.018 frozen band | δ 0.05 beside (not a band) | Rule-E note |
|---|---|---|---|---|
| positive_supply | P: UNDEMONSTRATED. O = 1,937,669 (V-C01) | UNDEMONSTRATED; CLOSE excluded, since O ≥ 485 (V-N01) | UNDEMONSTRATED; O ≥ 63 (V-N02) | night thresholds 40/1,515 and 6/197 and M_obs 10 are V_PENDING, context only |
| negative_supply | Ng: UNDEMONSTRATED | UNDEMONSTRATED; CLOSE excluded (O ≥ 485, V-C01, V-N01) | UNDEMONSTRATED | none |
| contamination_exposure | E = 1,937,669 (V-C01); S1 excluded 521,920 (V-C03) | **ESCALATE**: not CLOSE (E > 0); not PROCEED (Gemini 3.1 Pro has no published cutoff; E-labelled unknown) | ESCALATE | S0 112,990 and ANTARES leak 193/9,000 are V_PENDING, context only |
| tool_coverage | 2 PASS / 14 FAIL / 9 UNDEM (V-T01); CATS 5/10 (V-T02); recount after band hash (V-O02) | **ESCALATE**: not CLOSE (CATS accepts v11.1-named inputs); not PROCEED (CATS's Fink RF counterparts FAIL at emit, inside the V-T01 tally) | ESCALATE (no δ term) | per-tool counterpart rows have no V record of their own; JSON-row packet qualifier listed |
| cluster_structure | O 1,937,669 (V-C01); ALeRCE oids 1,937,720 (V-C02) | PROCEED, **leaning on V_PENDING** | PROCEED, same lean | the "every broker" clause needs the Fink bracket 1.77–2.02M and ANTARES 1,908,703, both V_PENDING |
| split_integrity | S1 521,920 (V-C03) | PROCEED, **leaning on V_PENDING** | PROCEED, same lean | cross-broker before-T0 sample 0/8,986 and worst case 1,896,117 are V_PENDING |
| unprocessable_units | U = 0 is V_PENDING (no V record) | PROCEED, **resting entirely on V_PENDING** | same | under rule E this reading cannot enter a ruling |

**Kill-band comparisons.** All 24 operands cite cleared V records or literals (`out/rule_E_audit.json`). The gate is armed: a planted V_PENDING U = 0 was refused (must fire), and V-C01 was accepted (must not fire).

| Axis | δ | Test | Result |
|---|---|---|---|
| positive / negative supply | 0.018 | O < 485: 1,937,669 < 485 (V-C01, V-N01) | false |
| positive / negative supply | 0.05 | O < 63 (V-C01, V-N02) | false |
| contamination | both | E == 0 (V-C01) | false |
| cluster | 0.018 | O ≥ 12,855 (V-C01, V-N01); O_A ≥ 12,855 (V-C02, V-N01) | true |
| cluster | 0.05 | O ≥ 1,666 (V-C01, V-N02); O_A ≥ 1,666 (V-C02, V-N02) | true |
| tool coverage | both | CATS passes > 0: 5 > 0 (V-T02) | true, so not CLOSE |

**Combination preview, not a ruling.** If (a) cleared and nothing else changed: no axis is in CLOSE, and contamination and tool coverage read ESCALATE, so §7 could not yield PROCEED.
- **Contamination** needs a subject-set change.
- **Tool coverage** needs a classical counterpart that runs end to end on Rubin rows. A subject-set change does not clear it. This disagrees with the assignment wording, which says both clear with a subject-set change; the disagreement is listed.
- **Supply PROCEED** under the frozen bands needs L ≥ 12,855 (V-N01).

## Validator
`out/validate_stdout.txt`:
```
FAIL p4_ruling_package.json
  - missing or empty 'ruling'
exit=1
```
The FAIL stands because precondition (a) is unmet. The package names it in `preconditions.a` and `ruling_decision`.

## PPDB (`ppdb_check.json`): NOT RELEASED as of 2026-09-17T14:19Z
- **RTN-011:** still v9.0 (2026-07-01).
- **Early Science page:** "Target: Sep-Oct 2026".
- **community.lsst.org News:** no release topic. The newest News topic is 12695 (2026-09-15); the latest listing ends at 2026-09-16T17:54.
- **New forum domain www.rubin.community:** listings return HTTP 403 "You need to be logged in". A release post there cannot be excluded.
- **Consequence, restated from wave 3.**
  - O = 1,937,669 (V-C01) is an upper bound.
  - Forced-only precovery cannot create straddlers (bands §3).
  - PPDB-only detections, if any, can only lower O.
  - Crossing the 12,855 band edge (V-N01) would need at least 1,924,815 removals (99.34%).
- **No recount was performed.**

## Disagreements, listed and not reconciled
1. **What clears the ESCALATE readings.** The assignment says both need a subject-set change; the frozen text says only contamination does, and tool coverage needs a verified counterpart.
2. **"Nights" in V-R02–R04.** The frozen table column is `rubin_on_sky_nights`; agent 2's wave-4 table labels the same numbers "usable P60 nights".
3. **The community.lsst.org latest listing** served no topic newer than 2026-09-16T17:54 at 2026-09-17T14:19Z, possibly caching. The new forum domain requires login.
4. **Rule E scope.** v3 marks 21 numbers V_PENDING. The brief limits rule E to V's targets, so the leans above disqualify only the readings that rest on those numbers, not the refusal itself.
