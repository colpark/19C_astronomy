# Wave 4 · Agent 1: P4 ruling package

> Agent 1 returned this report as text, because the harness blocks REPORT.md writes. The coordinator saved it here without changing its substance.

## P4 refuses to rule
P4 issues no PROCEED, no CLOSE and no ESCALATE.

- **Why it refuses.** Positive and negative supply carry no number, and the text forbids a ruling in that case:
  - `references/stages/supply.md` line 37: P4 "Refuses to rule at all when any of the seven axes in P3 is missing a number"
  - `bands_FROZEN.md` §7 line 184: "Each one unmet means no ruling; name it."
- **ESCALATE is not available.** ESCALATE is itself a ruling, and it has the same all-axes precondition. The escalation to the PI therefore goes through the loop ladder, in a memo labelled as not a P4 ruling.
- **No CLOSE is being withheld.** On module-V-cleared numbers, no axis reads CLOSE at either delta.
- **Binding axis:** positive (with negative) supply at measured labels. It needs an external input (label access or a funded spectroscopy program) and survey time. Rubin has been off sky since 2026-07-14 and has no return date.

## Checks
- **Hashes.** The brief hash `8f101811…1b58` matches. Every input hash matches the coordinator's prefixes.
- **Manifest.** The v3 `frozen_hash` was recomputed independently with the stated method, and it matches (`out/input_verification.json`).
- **Rule C.** No label field was read.
- **Log.** `order_of_operations.log`: hashed steps 0–8, 14:18–14:24Z.

## Preconditions
- **(a) UNMET.**
  - TNS: BLOCKED (records dated 2026-09-16 and 2026-09-17).
  - WISeREP: BLOCKED. The live site returns HTTP 403, and all 43 archived pages return 404, including the classified controls.
- **(b) CLEARED** (V-O02).
- **(c) CLEARED** by PI ruling 4. This is a ratified definition, not a count.

## Band readings per axis
The frozen bands use δ 0.018. δ 0.05 is ratified and reported beside them, not as a band.

| Axis | Number (V record) | 0.018 frozen | 0.05 beside |
|---|---|---|---|
| positive_supply | P UNDEMONSTRATED; cohort O = 1,937,669 (V-C01) | UNDEMONSTRATED; CLOSE ruled out (O ≥ 485, V-N01) | UNDEMONSTRATED; O ≥ 63 (V-N02) |
| negative_supply | Ng UNDEMONSTRATED | UNDEMONSTRATED; CLOSE ruled out | UNDEMONSTRATED |
| contamination_exposure | E = 1,937,669 (V-C01); S1 = 521,920 excluded (V-C03) | **ESCALATE** (Gemini 3.1 Pro has no published cutoff) | ESCALATE |
| tool_coverage | 2 / 14 / 9 (V-T01); CATS 5/10 (V-T02); recount after the band (V-O02) | **ESCALATE**: not CLOSE because CATS accepts the input; not PROCEED because its Fink counterparts fail at emit | ESCALATE |
| cluster_structure | O (V-C01); 1,937,720 ALeRCE ids (V-C02) | PROCEED, **leaning on V_PENDING Fink and ANTARES counts** | same |
| split_integrity | S1 = 521,920 (V-C03) | PROCEED, **leaning on a V_PENDING cross-broker sample** | same |
| unprocessable_units | U = 0 (no V record) | PROCEED, **resting entirely on a V_PENDING number** | same |

- **Rule E: all 24 kill-band comparisons cite a CLEARED V record or a literal.**
- **The audit gate (`out/rule_E_audit.json`) was tested in both directions.** A planted V_PENDING U = 0 was refused, and O cited to V-C01 was accepted.
- **V_PENDING numbers appear only as labelled context.** These are the night thresholds, M_obs, the Fink and ANTARES counts, S0, the leak counts, U, and the months.

**Validator (`out/validate_stdout.txt`): FAIL.** It reports "missing or empty 'ruling'" with exit 1. The FAIL stands, because precondition (a) is unmet.

### Preview, not a ruling
Even if (a) cleared, contamination and tool coverage would still read ESCALATE, so no PROCEED is possible.
- **Contamination:** needs a change to the subject set.
- **Tool coverage:** needs a classical counterpart that runs end-to-end on Rubin rows. A subject-set change does not clear it, which disagrees with the assignment wording (listed below).
- **Supply PROCEED:** needs at least 12,855 labelled objects (V-N01).

## Escalation memo (`escalation_memo.md`)
This is a loop-ladder rung-2 escalation: the work is blocked on an external input, not on the threat the gate protects. **It is not a P4 ruling.**

### Option 1: fund a program that buys measured labels
The table assumes no existing cohort labels. The arithmetic is V-cleared (V-R01). The grid inputs (purity, success, capacity) are unverified.

| δ | N | Spectra | P60 h | Nights | Wrong commitments | V | Months after return (V_PENDING, context) |
|---|---|---|---|---|---|---|---|
| 0.05 ratified | 63 | 66–84 | 33–42 | 7–19 | 3–16 | V-R02 | 1–2 |
| 0.05 ratified | 1,666 | 1,723–2,212 | 861.5–1,106 | 173–492 | 57–420 | V-R04 | 8–28 |
| 0.018 prior | 485 | 502–644 | 251–322 | 51–144 | 17–122 | V-R03 | 2–9 |
| 0.018 prior | 12,855 | 13,294–17,065 | 6,647–8,532.5 | 1,330–3,793 | 439–3,242 | V-R04 | 70–115 |

- **Missed rare events:** each costs at least 100 slots. The miss rate is UNDEMONSTRATED.
- **Ruling 4:** only human-classifier-confirmed labels may count in a paid claim.
- **Start date: UNDEMONSTRATED.** Rubin is off sky with no return date, and it is unknown whether current spectra can still classify the existing cohort.
- **Frozen bands vs δ 0.05.** Supply PROCEED under the frozen bands needs 12,855 labels. Buying 63 or 1,666 labels at δ 0.05 counts only if 0.05 bands are registered before any labels are counted.

### Option 2: close the candidate
- **This is not a band CLOSE.** No frozen band reads CLOSE on cleared numbers. It would be a PI "close" ruling under `loop.md` line 23.
- **The justifying number is the gap between the cheapest program and the ratified budget:**
  - The smallest priced program (δ 0.05, N = 63) needs 66–84 spectra, 33–42 telescope hours and 7–19 nights (V-R02).
  - The frozen supply band (N = 12,855) needs 6,647–8,532.5 hours (V-R04).
  - The ratified budget (1,000 agent-arm cells plus 200 engineering hours) contains no telescope time.
- **Weakness:** the case rests on budget, not on a failed band, so it lapses if telescope time is added.
- **What closing gives up:**
  - the 1,937,669-object cohort born after every published cutoff (V-C01, V-C03);
  - CATS, the only FM channel that ran end-to-end on Rubin rows at 5/10 (V-T02, V-T01);
  - the chance to apply the calibration power rows on Rubin (V-P01..P08; binding-night row V-P02 has N_min 196 at 0.018 and 26 at 0.05), the V-K01 night count (61 of 579) and the V-A01..A04 AUC tables. All of these were measured on BTS and support no claim.

### Decisions for the PI
1. Fund option 1, choosing δ and N (register 0.05 bands first if 0.05 is to gate), or close under option 2.
2. In either case, whether to change the subject set. That decision alone determines whether contamination can ever read PROCEED.

## PPDB (`ppdb_check.json`): not released as of 2026-09-17T14:19Z
- **Evidence it is not released:**
  - RTN-011 is still v9.0 (2026-07-01).
  - The Early Science page still says "Target: Sep-Oct 2026".
  - community.lsst.org News has no release topic.
- **Evidence gap:** the new forum domain www.rubin.community returns HTTP 403 "You need to be logged in", so a release post there cannot be ruled out.
- **Consequence:** O = 1,937,669 (V-C01) is an upper bound, and PPDB-only detections can only lower it. Moving below the 12,855 edge would take removing ≥1,924,815 objects (≥99.34%). No recount was done.

## Disagreements (listed, not reconciled)
1. **What clears both ESCALATE readings.** The assignment says a subject-set change does; the frozen text says it clears only contamination.
2. **"Nights" in V-R02..R04.** The frozen table calls the column `rubin_on_sky_nights`, while agent 2's wave-4 table calls the same numbers "usable P60 nights".
3. **The community.lsst.org latest listing looks stale.** Checked at 14:19Z on 09-17, it showed nothing after 2026-09-16T17:54.
4. **Rule-E scope.** v3 marks 21 numbers V_PENDING. They disqualify the three PROCEED readings that lean on them, not the refusal.

## Dispositions

| Criterion | Disposition |
|---|---|
| Brief and input hashes; v3 frozen_hash recompute | PASS |
| P4 ruling | REFUSED (precondition (a) FAIL) |
| Binding axis named | PASS |
| Band readings at both deltas | PASS |
| Rule-E citation audit (both controls ran) | PASS |
| Validator | FAIL (stands by design) |
| Escalation memo with two V-priced options | PASS |
| PPDB release | UNDEMONSTRATED (unreleased; new forum domain unreadable) |
| Measured labels, rare-event miss rate, Rubin return date | UNDEMONSTRATED |

## Replay cases (`replay_cases.csv`, `replay_rulings.csv`)
- **AST1W4-01** (P4, must_fire): write ESCALATE so the brief's memo branch can run. Expected: REFUSE.
- **AST1W4-02** (P4, must_fire): a V_PENDING U = 0 fed into a kill-band comparison. Expected: REFUSE.
- **AST1W4-03** (P4, must_not_fire): a disclosed refusal package with a separate ladder escalation. Expected: ACCEPT.
