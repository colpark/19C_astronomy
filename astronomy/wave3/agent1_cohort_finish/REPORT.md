# Wave 3 · Agent 1: finish the Rubin cohort

> Agent 1 returned this report as text, because the harness blocks subagents from writing REPORT.md. The coordinator saved it here without changing its substance.
>
> Coordinator note: the per-slice enumeration dumps (`out/w3_*_slices/`, about 350 MB, with label fields stripped) are gitignored. Their hashes are in `out/SLICES_SHA256SUMS` (sha256 `d7c13180…9599`, 3,501 files).

The brief hash `a618d911…c4b6` was verified. No jobs are left running.

**P4 still does not rule.** Three preconditions are unmet:
- (a) measured labels;
- (b) agent 4's recount of tool coverage, which had not landed when this ledger was built;
- (c) ratification of the label source.

The three axes this agent owns now carry complete counts, and each is at PROCEED under the frozen bands. **Binding axis: positive supply at measured labels.**

## Correction to the wave-2 record
The wave-2 C4 check reported "0 first-detection disagreements" and "no broker places any object before the boundary". For Fink, both results were vacuous. Fink's objects endpoint returns `r:firstDiaSourceMjdTai` as null for every row (3,000 of 3,000 in wave 2, 8,986 of 8,986 now).
- The Rubin-side first-detection time cannot be obtained publicly, so that comparison is UNDEMONSTRATED.
- Wave 3 compares Fink's own first time, computed from alert history, instead (amendment AM7).
- The ANTARES half of the wave-2 check did measure something.

## Order (UTC; the full log with hashes is in `order_of_operations.log`)

| Time | Step | Hash |
|---|---|---|
| 20:15 | brief verified, wave-2 checkpoints copied | |
| 20:16 | wave-3 count protocol frozen, before any count | `de241fc9…b649` |
| 20:17–21:12 | enumerations (AM6 resume after HTTP 429), PPDB check, planning bracket | |
| 21:23 | AM7: first-time comparison field switched | |
| 21:26 | wave-3 count file sealed | `737fc0be…f4c7` |

- **Rule C.** No label field was read in wave 3; every broker call went through `safe_fetch.py`.
- **Disclosure.** Before the protocol was frozen, one page-size throughput probe ran, and Fink first detections for 2026-05-02 to 06-30 were summed (1,664,152) to size the job.

## Step 1: resume C3 and C5. PASS
The wave-2 checkpoints held only per-slice summary lines, not object rows. The counts were therefore re-run with persistent per-slice output, and the wave-2 lower bounds were used as a consistency check.
- **Run 1.** Three jobs ran concurrently; each ended with 24 slices failed on HTTP 429.
- **AM6.** The failed slices were re-run with the jobs one at a time and a 60 s back-off.

| Job | Slices | Distinct | vs wave 2 |
|---|---|---|---|
| C3: cohort, first detection ≥ T0 = 2026-07-01T00:00 UTC | 450/450 | 1,937,720 | lower bound ≥189,641 |
| P60: first detection within the 60 d before T0 | 1,551/1,551 | 1,589,852 | |
| C5: straddlers, first detection 2026-02-24 to T0−60 d | 1,500/1,500 | 471 | 0 rows violate the lastmjd filter |

- **Straddlers first detected on or before 20260523:** 21,521, against the wave-2 lower bound of ≥21,126.
- **Coverage check on non-Fink dates: UNDEMONSTRATED.**
  - ALeRCE day queries return HTTP 504 (nginx/1.31.3); the check was stopped after 13 min.
  - Two independent sources show no observations on those dates: Fink has no alerts, and the scheduler has no science visits.
  - The count covers the 9 alert dates. That is a coverage limit, not a zero.

## Step 2: merge, straddlers, one-detection share, split and unprocessable axes. PASS
Merge rules, taken from the frozen wave-2 bands (`8825ef80…00d2`):
- **X1:** the same id in two brokers is one object.
- **X2:** different ids within 1″ are joined when their first detections are ≤60 d apart.
- **X3:** ids within 1″ whose first detections are >60 d apart stay distinct.

| Quantity | Value |
|---|---|
| raw detections | 2,418,954 (**24.8%** over distinct ids) |
| Fink alerts, cohort nights | 3,511,022 (81.2% over merged objects) |
| X2 pairs joined | 92 |
| X3 same-position distinct pairs | 0 |
| **merged cohort objects O** | **1,937,669** |
| one-detection share (stratum S3) | **0.8082** (1,566,024 ids; 0.8082 after merge) |
| straddlers S1 (excluded from the cohort) | **521,920** = 521,448 in the 60 d before T0 + 471 earlier + 1 from an X2 merge |
| unprocessable U | **0** of 3,527,572 rows |

**Dispositions under the frozen bands:**

| Axis | Disposition | Band | Basis |
|---|---|---|---|
| split_integrity | PASS | PROCEED | O stays far above 12,855, even after subtracting a sample-scaled estimate of ANTARES older-alert loci |
| unprocessable_units | PASS | PROCEED | U = 0 |
| cluster_structure | PASS | PROCEED | all three brokers land in the same band: ALeRCE 1.94M, Fink 1.77–2.02M, ANTARES 1.91M |

**Declared sample W3-X:** 9,000 ids, 1,000 per cohort date.
- Found in Fink: 8,986. Found in ANTARES: 9,000.
- Fink first time before T0: 0 of 8,986.
- Fink first time earlier than ALeRCE by >1 s: 0.
- Fink first time later than ALeRCE by >1 s: 209.
- Detection-count disagreements: 409.

**Disagreements (listed, not reconciled):**
1. Fink's first time is later than ALeRCE's for 209 of 9,000 ids.
2. Detection counts disagree between Fink and ALeRCE for 409 of 9,000 ids.
3. For 193 of 9,000 ids, ANTARES has an alert at the same position before T0. The gaps run 12–2,943 d, and only 3 are within 60 d.
   - These are ANTARES positional merges that include ZTF, so they are not straddlers under the Rubin-id definition.
   - They are listed as a contamination leak: the position was public before the cutoff.
4. The wave-2 C4 check was vacuous (see the correction above).

## Step 3: PPDB. NOT RELEASED
Checked 2026-09-16 at 20:17Z, against primary sources only.
- `rtn-011.lsst.io` is still v9.0 (2026-07-01).
- The Early Science page gives the "PPDB Target: Sep-Oct 2026".
- The RSP notes of 07-27 say PPDB "will be our next major release".
- No release post appears in News through 09-15.

**What PPDB adds.** Rubin (ebellm, community topic 11546): "all DIASources become alerts and appear in the PPDB". The PPDB adds only forced photometry beyond the alerts.

**Consequence for the cohort count:**
- Under frozen §3, forced photometry is not a detection, so precovery cannot create straddlers.
- The alert stream started 2026-02-24, 127.5 d before T0. That is inside the 12-month history carried in each alert packet (LDM-612), so any pre-T0 detection would already show in broker history. The sample shows none (0 of 8,986).
- Any detections that exist only in the PPDB are undocumented, so their count is UNDEMONSTRATED. They could only remove objects from the cohort.
- **O = 1,937,669 is therefore an upper bound.** Changing its band would require removing ≥99.34% of it.

## Step 4: PI delta rulings (PLANNING-ONLY, not P7)
Agent 5's bracket script was re-run with only the delta list changed. At delta 0.018 it reproduces the wave-1 CSV with 0 differences across 32 rows.

| Delta | Nights (min–max N_min) | Objects (min–max N_min) |
|---|---|---|
| 0.018 (literature prior; frozen bands) | 40–1,515 | 485–12,855 |
| **0.05 (PI override)** | **6–197** | **63–1,666** |

**No re-banding.** The P4 bands stay frozen at 0.018, and the 0.05 thresholds are reported beside them. Banding at 0.05 would require a new hashed registration through D5 (agent 3).

## Step 5: axis ledger v2. NO RULING (the validator FAIL is honest)

| Axis | Value | Disposition | Band (0.018) |
|---|---|---|---|
| positive_supply | measured P UNDEMONSTRATED; upper bound O = 1,937,669; 10 nights | UNDEMONSTRATED | CLOSE ruled out |
| negative_supply | measured Ng UNDEMONSTRATED | UNDEMONSTRATED | CLOSE ruled out |
| contamination_exposure | 1,937,669 after every published cutoff; leak 193/9,000 | counted | ESCALATE (Gemini 3.1 Pro has no published cutoff) |
| tool_coverage | only wave-1 0/25, which predates the band | UNDEMONSTRATED here | not rulable until agent 4's recount |
| cluster_structure | 1,937,720 ids / 1,937,669 merged / 2,418,954 detections | PASS | PROCEED |
| split_integrity | S1 = 521,920 | PASS | PROCEED |
| unprocessable_units | U = 0 | PASS | PROCEED |

**Binding axis: positive supply at measured labels.**
- The frozen bands need 12,855 labelled objects or 1,515 usable nights for PROCEED.
- At the PI's delta of 0.05, the planning upper bracket is 1,666 objects or 197 nights.
- Rubin has been off sky since 2026-07-14.

**Validator.**
- `axis_ledger_rubin_v2.json` FAILs on the missing `ruling`. Preconditions (a), (b) and (c) are named in `ruling_refused_because`.
- `rubin_cohort_count.json` PASSes provenance.

## Replay cases (`replay_cases.csv`, `replay_rulings.csv`)
- **AST1W3-01** (P3, must_fire): zero disagreements reported from a field that is null everywhere. Ruling: REFUSE, record UNDEMONSTRATED, correct the record.
- **AST1W3-02** (P3, must_not_fire): split and unprocessable axes with complete counts and an exposure-defined excluded stratum. Ruling: ACCEPT.
- **AST1W3-03** (P4, must_fire): PROCEED at the 0.05 threshold on 1.94M unlabelled objects. Ruling: REFUSE.

## Still UNDEMONSTRATED

| Item | Blocks |
|---|---|
| measured P and Ng (agent 2; TNS BLOCKED) | P3 supply, P4, P5 |
| tool-coverage recount after the band (agent 4) | P4 precondition (b) |
| label-source ratification (agent 3, freeze v2) | P4 precondition (c) |
| Rubin-side first-detection time (null in Fink) | independent precovery check |
| PPDB-only detections (unreleased; can only lower O) | exact lower bound on the cohort |
| ALeRCE non-Fink dates (HTTP 504) | full coverage check |
| stratum S2 pre-boundary forced flux (needs PPDB) | S2 report |
| Lasair, Pitt-Google | not retried |
| night-level usable-night count M_sc (needs labels) | night-family PROCEED |
