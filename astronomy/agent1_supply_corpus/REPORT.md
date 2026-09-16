# Agent 1: supply and corpus (D1, D2, D3, P3 partial, P5 sketch)

> Agent 1 wrote this report and returned it as text, because the subagent harness blocked it from writing report files. The coordinator saved it here without changing its substance.

This is a pre-P1 sketch; no P4 ruling is issued. Every number comes either from the scripts in `scripts/` or from a seed locator. To reproduce, run `build_corpus.py`, `count_supply.py`, `answer_in_seed_text.py` and `make_records.py` in that order, using the panel venv.

## What changes the picture
1. **The BTS file is already at object level.** Its 11,193 included rows collapse to 11,183 objects at 1″, an overstatement of 0.089%. The ~1000× overstatement belongs upstream, in the alert stream that BTS filters.
2. **Upstream overstatement, from design documents:**
   - Rubin: about 60 SN alerts per SN DIAObject (5,900%). This is 200 SN alerts per visit × 1,000 visits per night × 300 nights per year ÷ 10⁶ SNe per year (DMTN-102 §2.2, §2.6).
   - Rubin, whole stream per SN: about 2,000 (199,900%). This is 20 billion alerts over 10 years (NOIRLab sci26008) ÷ 10⁷ SNe over 10 years.
   - ZTF: 10⁵–2×10⁵ packets per saved candidate (Perley 2020 §2.1).
   - Whole-stream alerts per DIAObject has no documentary count, so it is UNDEMONSTRATED.
3. **Negatives are truncated by construction.** The file holds only scanner-saved candidates (explorer doc, "Classification"). It contains 663 negative objects.
4. **Labels collapse after January 2026.** 89.4% of 2026-peaking objects are unlabelled, against 25–35% in each year from 2019 to 2025.
   - After S1 (2026-02-24, first Rubin alerts): 250 objects, of which 9 are pos, 9 neg and 232 unlabelled.
   - After S2 (2026-06-30, LSST start): 30 objects, of which 1 is pos.
   - No source that was read explains the collapse.
5. **D3: tau.py's choice is refused.** tau.py printed CHOSEN at 30″, but the curve is flat and that cut merges 39 pairs of distinct SNe. The working cut is instead bounded by controls, on a plateau of 11,183 objects from 0.5″ to 1.5″.

## D1: read seeds in full. PASS
Twelve seeds were read whole. Full texts and their sha256 are in `sources/`; facts and locators are in `seed_ledger.json` and `corpus_ledger.json`.

- **Fremling et al. 2020, arXiv:1910.12973:**
  - a few hundred alerts pass the filter per night (§2.2)
  - 5–15 candidates are assigned for follow-up per night (§2.2)
  - SEDM priorities are P3/P2/P1, with 7-day triggers (§2.3)
  - positions are weighted means over alerts (§3.1)
- **Perley et al. 2020, arXiv:2009.01242:**
  - ~10⁶ packets per night filter to ~500 (§2.1)
  - 5–10 candidates are saved per clear night (§2.1)
  - CVs and AGN are not targets (§2.4)
  - the public start was 2018-06-01 (§2.3)
  - Δz ≈ 0.005 and host search within 90″ (§2.2); see also Table 1
- **BTS explorer_info.html:**
  - peak time is recorded as JD−2458000
  - peak mag may be an upper limit
  - "a few transients are wrongly matched on TNS"
- **Rubin design documents:**
  - LDM-612 §2.2.1: every SNR>5 detection becomes a DIASource and one alert. Each DIASource maps to one DIAObject (or a new one) or to an SSObject.
  - LSE-163 §3.1 and §3.2.1; about 200,000 background false positives per night.
  - DMTN-102: 10⁷ alerts per night.
- **Rubin data model:**
  - sdm_schemas apdb.yaml v10.0.0 (commit 5499df1): `DiaObject.nDiaSources`.
  - alert_packet v11.1: one alert is one triggering diaSource, plus history, plus an optional diaObject.
- **Rubin and NOIRLab pages:**
  - first alerts to brokers on 24 Feb 2026, 800,000 that night
  - "up to seven million alerts per night"
  - LSST formally started 2026-06-30

## D2: assemble the corpus. PASS
- **Rules frozen first.** The rules are in `corpus_rules_FROZEN.md` (sha256 aa4e8d21…a41a). The build script re-checks this hash and aborts if it has changed.
  - Disclosure: the schema (column tokens, distinct type strings, duplicate IDs) was inspected before freezing. No inclusion, label, cluster or split count was computed before freezing.
- **Rows.** The raw file has 11,217 data rows. Rule E5 (peak before 2018-06-01) excluded 24; rules E1–E4 excluded 0. The exclusion ledger is in `corpus_ledger.json`. The result is `corpus.csv`: 11,193 rows, sha256 b059acf0…8442.
- **Labels, declared before counting.** All 39 type strings map.
  - posA: a real extragalactic transient class
  - posB: posA excluding the SN Ia family
  - neg: CV or AGN, including "?" variants
- **Answer-in-own-source flag.** 98 objects have their class stated in the seed-paper text. They are flagged as not admissible to a benchmark until Agent 3 issues an exposure ruling, and they are kept in the counts.
- **Amendment A1** is recorded with its cause (see D3). It changes a control only.

## D3: cut sweep. tau.py's choice REFUSED; cut bounded by controls; separation UNDEMONSTRATED

| radius ″ | objects | same-IAU pairs joined | distinct-SN pairs merged | straddle S1/S2 |
|---|---|---|---|---|
| 0.5 / 1 / 1.5 | 11,183 | 10/13 | 0 | 0/0 |
| 2 | 11,179 | 13/13 | 1 | 0/0 |
| 3 | 11,174 | 13/13 | 3 | 0/0 |
| 5 | 11,164 | 13/13 | 9 | 0/0 |
| 10 | 11,143 | 13/13 | 19 | 2/1 |
| 20 | 11,126 | 13/13 | 32 | 3/1 |
| 30 | 11,116 | 13/13 | 39 | 4/1 |
| 60 | 11,104 | 13/13 | 45 | 4/1 |

- **Why tau.py's pick is refused.**
  - tau.py exited 0 and chose 30″. Every step on the curve gains less than 0.3%, so its 5% saturation test passes at whatever the second grid point is.
  - Separation needs I1, which does not exist yet.
  - 30″ fails the must-not-join control 39 times.
  - By tau.py's own two-signal criterion, therefore, the curve does not bound a cut.
- **Amendment A1.** Three of the frozen same-IAU must-join pairs sit 1.62–1.92″ apart, with peaks 485–1,598 days apart. SN2023ghl and SN2024gyr are two distinct SNe 1.92″ apart. A1 therefore restricts must-join to re-triggers: same IAU name and peaks within 60 days, giving 9 pairs, all ≤ 0.494″.
- **Working cut: 1″.** It is mid-plateau: all re-triggers join and no distinct SNe merge. The count is identical at 0.5″ and 1.5″, so the choice does not increase unit count.
- **Limit of position alone.** A recurrent CV at a single position (AT2019tee) and two events at one position (SN2021sic) merge at any cut ≥ 0.5″.
- **Sibling / same-host association.** Defined as different 1″ objects ≤ 90″ apart with both z known and |Δz| ≤ 0.005.
  - Result: 55 pairs in 51 groups, covering 104 objects. Treating hosts as the unit gives 11,130 units.
  - No sibling group straddles S1 or S2.

## P3 axes (unit = 1″ object)

| Axis | Disposition | Number |
|---|---|---|
| positive_supply | PASS (counted) | posA 7,154 (7,158 rows); posB 1,839; SN Ia family 5,315. At peak mag ≤ 18.5: posA 4,819, posB 1,210. After S1: 9 posA (4 posB). After S2: 1 |
| negative_supply | PASS (counted) | neg 663 (665 rows); 576 at peak mag ≤ 18.5; 104 tentative; 9 after S1. Negatives that scanners never saved are absent by construction |
| contamination_exposure | UNDEMONSTRATED | owned by Agent 3 |
| tool_coverage | UNDEMONSTRATED | owned by Agent 4 |
| cluster_structure | PASS | 11,193 rows → 11,183 objects (0.089%). Upstream: documented ratios above. Whole-stream alerts per DIAObject UNDEMONSTRATED |
| split_integrity | PASS | Split key: peak time. At 1″, 0 objects and 0 sibling groups straddle S1 or S2 (at 10″: 2 and 1). The test side after S1 is 93% unlabelled |
| unprocessable_units | PASS (documented, not repaired) | type "-": 3,370; z "-": 4,054 (20 posA); absmag "-": 4,055; ">"-censored: duration 3,905, rise 2,938, fade 2,060; IAU "-": 107; no upper-limit flag for peak mag; 24 E5 exclusions |

The 3,366 unlabelled objects are a separate group and are never counted as negatives. No 1″ object carries conflicting labels.

## P5 sketch
S is UNDEMONSTRATED because no budget has been supplied. The yields below are label yields per time window, which sits next to the P5 quantity rather than being it.
- **After S1:** 9 of 250, 95% interval [0.017, 0.067], spread 2.2×, LICENSED. At S=100 the point queue is 2,528 objects, and only 250 exist.
- **After S2:** 1 of 30, interval [0.001, 0.172], spread 40×, PROVISIONAL.
- **Whole corpus:** `queue.py` crashes with ZeroDivisionError in `ibeta` at large n (underflow), so this is UNDEMONSTRATED. **That is a defect in the skill's script.**

## Disagreements (listed, not reconciled)
1. **Row count.** The coordinator's brief and FETCH.md said 11,218 objects; the CSV has 11,217 data rows. The coordinator has since corrected both.
2. **Overstatement.** The brief says ~1000×. The documents give ~60× (SN alerts per SN object) or ~2000× (whole stream per SN). Within the file it is 0.089%.
3. **Nightly volume.** 10⁷ per night (DMTN-102, LDM-612, LSE-163) against "up to seven million" (Rubin news 2026).
4. **Alert latency.** 60 s (design docs) against "within two minutes" (news). DMTN-102 fn 2 gives 2 min as the minimum specification.
5. **Alert format.** VOEvent (LSE-163 §3.5) against Avro/Kafka (LDM-612, alert_packet v11.1).
6. **Alerts per visit.** "Maximum 10,000 per visit required" (LDM-612 fn 2) against "at least 40,000 per single visit" (DMTN-102 §2.2).
7. **Candidates per night.** 5–15 assigned (Fremling §2.2) against 5–10 saved (Perley §2.1).
8. **Completeness to mag 18.5.** ~96% or 93.6% (Fremling 2018) against 93% (Perley, a different sample).
9. **IAU name as object key.** Four same-name pairs have peaks 485–1,598 days apart. The explorer admits "a few" wrong TNS matches.
10. **2026 label collapse.** No seed explains it.
11. **tau.py.** It returns CHOSEN on a curve its own criterion cannot discriminate, and the chosen cut fails the must-not-join control.

## UNDEMONSTRATED, and what each blocks
- **Separation at each cut** (needs I1): blocks the final D3 justification and P6.
- **Contamination exposure and tool coverage:** P4 refuses to rule while these are open.
- **Rubin-native supply** (nDiaSources, Rubin classifications): blocks any count at the Rubin unit. It needs PPDB data rights.
- **Budget and cost of action:** block S, the P5 escape and P7.
- **Cause of the 2026 label collapse:** blocks knowing whether post-S1 supply grows.
- **queue.py at large n:** blocks P5 on the whole corpus.

## Validator output (`out/validate_stdout.txt`)
```
PASS corpus_ledger.json
PASS cut_curve.json
FAIL axis_ledger_partial.json
  - missing or empty 'ruling'
PASS provenance_records.json
```
The axis-ledger FAIL is deliberate. Writing a ruling would issue P4 with two axes missing and no bands declared.

## Replay cases
- **AST01** (D3, must_fire): adopt tau.py's 30″ pick. Ruling: REFUSE.
- **AST02** (P3, must_fire): report 7 million alerts per night as supply. Ruling: REFUSE; count objects.
- **AST03** (P3, must_not_fire): 11,193 → 11,183 with both controls run. Ruling: ACCEPT.
- **AST04** (D2, must_fire): relabel the 232 unlabelled post-S1 objects as negatives after the count. Ruling: REFUSE.
