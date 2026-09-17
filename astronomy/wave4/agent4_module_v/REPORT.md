# Wave 4 · Agent 4: module V (verifier) report

> Agent 4 returned this report as text, because the harness blocks REPORT.md writes. The coordinator saved it here without changing its substance. **Module V ran as a fresh session that produced none of the numbers it verified.** No producer artifact was changed.

## Result
- **33 of 38 ruling-bearing numbers are cleared for P4 use under rule E.**
- **The 5 label-source numbers (L01–L05) are not cleared yet.**
  - The blind re-derivation disagreed. Every unit of difference resolved to a cause, and after two verifier-side defects were fixed the independent parse reproduces the claims exactly.
  - Two definitional readings still need a ruling.
- **Invariance:** CATS and GHOST are invariant within float tolerance, but not bit-identical.
- **Property tests:** 43 of 44 pass. The failure is a real defect in unpatched `power.py`.

## Protocol
- **Brief hash** verified: 8f101811…b58.
- **Hashed before any derivation:**
  - `V_CHARTER.md` (f4bca840…);
  - `V_TARGETS.json` (4f9594a1…), with 38 targets and no claimed values.
- **Sealed before any claim was opened:** all 38 derived values, at 13:23–13:31Z. `sealed/SEALED_SHA256SUMS` has 39 entries, all OK.
- **Blindness limit:** the coordinator's prompt quoted most claimed values, and STATUS.md quoted a few more. The verifier could not be blind to those numbers. Its code never read producer outputs. Each record states which kind of blindness applies.
- **Inputs checked against their hashes:**
  - 3,501 of 3,501 cohort slices match SLICES_SHA256SUMS;
  - `compositions/MANIFEST.sha256`, `HASH_MANIFEST.sha256` and the paired-score files match;
  - the BTS csv, the frozen definitions and the frozen protocols match.
- **Validator:** `validate.py provenance v_records.json` PASS. The first run failed on the wording of V-O02's falsifier; both outputs are kept.
- **Replay controls:** all armed and all behaved correctly.
  - V-01, planted cohort +1,000: fired (must fire).
  - V-02, 5e-7 relative float difference: did not fire (must not fire).
  - V-03, p-value off by 0.10 in log10: fired.
  - V-04, bootstrap CI off by 0.002: did not fire.
  - The controls ran after the first comparison pass, and the records were then rebuilt. No verdict changed.

## Per-number verdicts
Every premise check (does the check fail if the claim is false?) ran and behaved as required.

| id | Number | Verdict |
|---|---|---|
| C01 | Cohort O = 1,937,669 (92 merge links, 0 same-position distinct) | MATCH |
| C02 | distinct cohort oids 1,937,720 | MATCH |
| C03 | S1 = 521,920 (521,448 + 471 direct, 1 via merge) | MATCH |
| C04 | one-detection share 0.8082 (1,566,024 oids; also 0.8082 at merged level) | MATCH |
| P01–P08 | sigma_d, MDE and N_min at δ 0.018 and δ 0.05, for E1/E3 × {pooled nights, k-binding True, k-binding False, rounds}. Binding night: 0.089778 / 0.032204 / N_min 196 and 26. Both power files agree with each other | MATCH |
| K01 | 61 of 579 E1 nights k-binding (same for E3) | MATCH |
| K02 | 518 nights with ≤8 candidates | MATCH |
| A01–A04 | AUCs E1 C−1 0.5996, E1 C 0.5968, E3 C−1 0.6374, E3 C 0.6184. Points agree to 1e-16, CIs exactly. Label permutation gives 0.49–0.52 | MATCH |
| L01 | SNIascore lower bound 954 (blind 953) | DISCREPANCY, cause resolved |
| L02 | upper bound 2,057 (blind 2,143); no-E5 sensitivity 2,654 (blind 2,658) | DISCREPANCY, cause resolved |
| L03 | MEASURED 1,074 (blind 1,070) | DISCREPANCY, cause resolved |
| L04 | MODEL_ANNOTATION 954 (blind 948) | DISCREPANCY, cause resolved |
| L05 | UNRESOLVED 5,815 (blind 5,825) | DISCREPANCY, cause resolved |
| Q01–Q04 | POLICY p-values: claimed 5.45e-146 / 9.37e-105 / 2.80e-131 / 2.58e-110, derived 5.20e-146 / 9.25e-105 / 2.69e-131 / 2.55e-110. Differences 0.004–0.020 in log10 (tolerance 0.05). n, observed and expected match exactly. Ruling POLICY | MATCH_WITHIN_TOL |
| T01 | 2 PASS / 14 FAIL / 9 UNDEMONSTRATED over 25 tools | MATCH |
| T02 | CATS 5/10, GHOST 3/8 | MATCH |
| T03 | 160 alert runs | MATCH |
| N01–N02 | Family-B N_min 485 and 12,855 at δ 0.018; 63 and 1,666 at δ 0.05 | MATCH |
| R01 | all 288 truth-cost rows follow the frozen formula | MATCH |
| R02–R04 | truth-cost ranges (N=63: 66–84 spectra, 7–19 nights; N=485: 502–644, 51–144; plus N=1,666 and 12,855) | MATCH |
| O01 | Ruling-1 ordering in UTC: wave-3 brief 20:14:03Z < first power output 20:43:28Z (power_calibration.json 20:44:29Z) < agent 4 step 1 20:48:29Z | MATCH_WITHIN_TOL (sub-second) |
| O02 | P4 precondition (b): all 198 runs after the band hash (18:51:26.92Z) and the protocol freeze (20:52:25Z); all 25 tools have a disposition; logged band hash equals the current file | MATCH |

**What O01 cannot establish without git:**
- the commit times (quoted from the preamble, not read);
- whether an earlier, overwritten version of the power file existed before 20:14Z (mtime shows only the last write);
- whether the host clock is trustworthy.

**Notes for agent 3 and the PI:**
- **12,855 is driven by the sample SD of the 50-row synthetic binary column (0.7284).** The theoretical √q would give 12,113 at δ 0.018, and 1,570 instead of 1,666 at δ 0.05. This is not a discrepancy, because the frozen definition says "min/max over the rows".
- **A 1–5% relative p-value offset remains.** It is consistent with an age convention (capture timestamp vs date) and within tolerance.

## Label discrepancies: causes (`discrepancies/D-L01…L05.md`)

| Cause | Whose | Class | Effect on the blind value |
|---|---|---|---|
| 1. Double-gzipped captures (5 wave-2 pages logged `invalid`, 2 in wave 3); the verifier's parser decompressed once | verifier | input-version (decoding) | MEASURED +5, MODEL +3, L +2, U −5 |
| 2. The frozen definitions let E2 (paper-named SNIascore) place MODEL_ANNOTATION; the verifier used E2 only for the bound | verifier | definitional | MODEL +4 |
| 3. Two BTS rows share an IAU name with another ZTFID (SN2024led, SN2025oxy). The verifier applied the fetched page to both twins; the producer applied it only to the fetched ZTFID. The frozen text supports both readings | ambiguous | definitional | MEASURED −1, MODEL −1, L −1, U +1 |
| 4. The frozen E5 text says "peakt < 1289.5 − 30 = 1259.5", but JD 2459319.5 − 2458000 = 1319.5. The rule as described in words gives < 1289.5, which the producer implemented and which matches wave 1's 1,936. The verifier used the literal 1259.5 | slip in frozen text | arithmetic | U +82 (82 SN Ia) |

- **Reconciled.** With causes 1–2 fixed and the producer's readings of causes 3–4, the parse gives exactly 1,074 / 954 / 0 / 5,815 and bound [954, 2,057]. It also reproduces wave 2's [803, 2,247]. This result is sealed as `sealed/V-L-r1.json` and is not blind.
- **Alternatives.** Literal E5 gives [954, 2,139]; IAU-name keying gives [955, 2,056].
- **Effect on ruling 4.** Every reading stays inside [803, 2,247], so ruling 4's condition holds either way.

## Invariance (`invariance.json`, `invariance_runs.jsonl`)
**Budget.** 38 of the remaining 90 alert runs were used, so the rule-D total is now 198 of 250. Alert content was re-fetched through the label-stripping helper, and the raw hashes match wave 3.

**CATS**
- Not bit-identical: the maximum absolute difference between batched and alone is 1.19e-7 (float32).
- The same alert run alone twice is bit-identical, so the difference is deterministic in batch composition (padding shape), not run noise.
- The top class never changes.
- Verdict: invariant within float tolerance.

**GHOST**
- One alert is bit-identical in all arms. The other two are bit-identical alone-vs-alone.
- Batched, every output column is value-equal (NaN-aware), but the serialised record hashes differ. That is consistent with a dtype coercion on concatenation. The column cannot be named, because outputs are not retained.
- Verdict: invariant within float tolerance, since the values are identical.

**Verifier comparator defect.**
- The first GHOST pass masked NaN-vs-value differences. It was logged and that verdict voided.
- The comparator was fixed, a must-fire NaN control added, and a targeted re-check rerun (8 runs).

## Property tests (`property_tests/`)
Queue patch 01 was applied in a scratch copy and tested with `hypothesis` (fixed seeds) plus a seeded grid.

**43 of 44 pass:**
- intervals contain the point estimate;
- intervals shrink in n;
- agreement with scipy `beta.ppf`;
- no crash up to n = 10⁶ (the unpatched vendored `queue.py` fails at n = 1072, as the patch's cause states);
- MDE falls as 1/√n;
- N_min is consistent with MDE at δ;
- refusals on an empty file, a missing column, a blank cell and a single row.

**Real finding:** vendored `power.py` rejects a ragged row (a short row with a missing value) by crashing with an `AttributeError` traceback instead of a clean refusal.

**Amendment:** one test's tolerance was amended after its first run to allow for power.py rounding MDE to 6 decimals. Both logs are kept.

## Cleared for P4 under rule E
- **Cleared:**
  - C01–C04, the cohort;
  - P01–P08, every sigma_d, MDE and N_min;
  - K01–K02, the night counts;
  - A01–A04, both composition AUC tables with CIs;
  - Q01–Q04, the POLICY p-values;
  - T01–T03, the tool tally;
  - N01–N02, the N brackets 63, 485, 1,666 and 12,855;
  - R01–R04, the truth-cost table and ranges;
  - O01, the ruling-1 ordering (with the git caveats above);
  - O02, precondition (b).
- **Not cleared: L01–L05.** These are the SNIascore bound [954, 2,057] and the counts MEASURED 1,074, MODEL_ANNOTATION 954 and UNRESOLVED 5,815.
  - The recommendation is to clear them once agent 3 or the PI rules on the E5 cut (1289.5 vs 1259.5) and on twin-row keying.
  - No reading changes a band or ruling 4.

## Overhead (`overhead.json`)
51.4 min wall time (13:14:53Z–14:06:16Z) and about 125 tool calls. The share of the wave is computed by the coordinator; see `astronomy/wave4/COORDINATOR_LOG.md`.
