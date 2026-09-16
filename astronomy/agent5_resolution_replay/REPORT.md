# Agent 5: k, delta prior, subject set, resolution sketch, replay design

> Agent 5 returned this report as text, because the subagent harness blocks subagents from writing report `.md` files. The coordinator saved it here without changing its substance.

**Headline.**
- **k and chance:** k = 8 per night, drawn from ~46 candidates, so chance = 0.172.
- **Delta prior:** DERIVED at 0.018, but that value sits below the resolution of the practitioners' own comparison.
- **Human-supplied inputs:** budget, cost of action and S are UNDEMONSTRATED.
- **Validation:**
  - `validate.py provenance` passes on all 5 record files.
  - A partial manifest assembled from these three slots fails the ledger check only because tau, label source, exposure key, tool inventory and the freeze hash belong to other agents.
- **Sealed rulings:** `cases/RULINGS_SEALED.csv` was not opened.

## Dispositions
| Criterion | Disposition | Record |
|---|---|---|
| Seeds read (20 fetched) | PASS for 14 read whole; 6 partial reads are named, and none is relied on for a decision | seed_ledger.json |
| k, candidates per round, chance (ZTF BTS) | PASS, DERIVED | k_slot.json |
| k, candidates, chance (Rubin LSST stream) | UNDEMONSTRATED. Blocks P6 chance and P7 N_min for LSST items | k_slot.json |
| peakt zero point | PASS: JD − 2458000 | out/bts_rounds.json |
| Delta prior | PASS, DERIVED 0.018, with a resolution warning | delta_slot.json |
| Subject set (availability) | PASS, DERIVED | subject_set_slot.json |
| Subject training-data cutoffs | UNDEMONSTRATED for every model | subject_set_slot.json |
| Budget, cost of action, S | UNDEMONSTRATED | d5_inputs.json |
| P6/P7 | UNDEMONSTRATED (needs I1 compositions); planning bracket only | planning_mde_bracket.csv |

## k and chance
- **Round:** one night. From 2023-08-19 to 2023-09-29 (41 nights), BTS scanners requested SEDM spectra for 327 unique sources, out of 1,903 distinct sources that passed the alert filter (arXiv:2401.15167, lines 757-766, 898-902, 953-958).
- **k:** 327/41 = 7.98, rounded to 8. The rounding is flagged for ratification.
- **Candidates per round:** 46.41.
- **Chance:** 327/1,903 = 0.172.
- **Other seeds, listed and not averaged:**
  - 5–15 per night in 2018 (Fremling 2020)
  - 5–10 saved per clear night (Perley 2020)
  - median 4.5 for the automated selector (BTSbot paper)
  - ~10 SEDM spectra per night (Blagorodnova 2018)
  - round figures in the BTSbot paper ("~50 candidates, ~7 real"), which give 0.14
- **TiDES:** arXiv:2501.16311, verified with the arXiv API. TiDES is not a pick-k-of-n decision, because fibres are not scarce (~12 transients per field against 30–35 fibres). The decision shape therefore fits SEDM-like spectrographs, not 4MOST.
- **SOXS and ePESSTO+:** SOXS (arXiv:1812.07401) gives no count per night. No ePESSTO+ survey paper was located.
- **BTS file limit:** the file cannot supply candidates per night. It holds only saved sources and has no save or trigger dates. Peaks average 4.09 per calendar night, which is only a proxy.
- **Zero point of `peakt`:**
  - Documented as JD − 2458000 (explorer doc line 102, BTS I Table 1, BTS II Fig. 13).
  - Measured check: 96.27% of 11,110 named rows peak in their IAU designation year or the next, against 0–0.06% under the other offsets.
  - A half-day shift scores identically, so only the documentation fixes the zero point.

## Delta prior
- **Adopted value: 0.018.** On one test split (512 bright transients, 1,489 other sources), the multimodal selector reached purity 0.930 against 0.912 for the metadata-only network, and the authors put the multimodal selector into production.
- **Resolution warning:** the unpaired MDE for that comparison is ~0.045, so practitioners acted on an effect below its own resolution. A paired MDE cannot be computed, because the disagreeing selections are not published.
- **Values not adopted:**
  - **BTSbot vs human scanners, −0.037:** refused, because the denominators differ. The paper also gives the scanner purity as both 96.7% and 95.6%.
  - **SNIascore vs SNID, +0.37:** wrong decision; it classifies spectra that were already taken.
  - **Fink, +0.30:** alert-counted, and the paper reports three different test-set sizes.
- **Caveats:** the metric is not yet preregistered, and the human's cost of action may override the adopted value.

## Subject set (official docs, 2026-09-16)
| Model | Stated cutoff | Status |
|---|---|---|
| Claude Fable 5.1 | Jun 2026 (reliable-knowledge) | Transparency Hub lists only Fable 5 (Jan 2026) |
| Claude Opus 5 | May 2026 | DERIVED |
| Claude Sonnet 5 | Jan 2026 | DERIVED |
| GPT-6 Astra | Apr 30, 2026 | DERIVED |
| GPT-5.6 Sol | Feb 16, 2026 | DERIVED |
| Gemini 3.8 Flash | Mar 2026, with "some domains Jan 2025" in the same sentence | DERIVED, internal disagreement |
| Gemini 3.1 Pro (preview) | none found | UNDEMONSTRATED |

- **Missing from every provider:** no provider states a training-data end, and no rung (tier requirement) is stated anywhere.
- **Not covered:** open-weight models were not surveyed.
- **Exposure:** only BTS rows with peaks after 2026-06-30 are unexposed to every model. That is 30 rows, of which 1 is a classified transient.

## D5: what the human must supply
1. **Budget,** in agent-arm cells or hours, with the arms counted. The corpus only records the telescope budgets of other programmes.
2. **Cost of action.** Either the smallest precision gain that would change which selection tool you use, or telescope time per spectrum plus the value of a right versus a wrong commitment. Seeds show what others act on, not your threshold.
3. **S** = budget ÷ hours per workflow. Hours per workflow are only measured at R1.

Until these are supplied, they block the delta override, the P7 ruling, the P5 escape and all paid work from R1 onward.

## Planning bracket (PLANNING-ONLY, not a P7 record)
The vendored `power.py` was run unchanged on synthetic paired columns, with k=8, 46.41 candidates, α=0.05 and power 0.80.

| Unit | Bracketed σ_d | MDE range across N | N for MDE < 0.018 |
|---|---|---|---|
| Night, precision@8 | 0.040–0.250 | 0.016–0.099 at 50 nights; 0.003–0.016 at 2,000 | 40–1,515 nights |
| Object, right/wrong decision | 0.14–0.71 | 0.018–0.089 at 500; 0.009–0.044 at 2,000 | ~485–12,000 objects |

- **Where the σ_d brackets come from:** the night bracket spans purity 0.93 to 0.5 and correlation between methods 0.9 to 0. The object bracket spans disagreement rates of 0.02 to 0.5. These are coverage choices, not measurements.
- **Large effects:** an effect of ~0.30 needs fewer than 50 units in every row.
- **Consequence:** with 30 unexposed rows (1 classified transient), an exposure-free cohort is orders of magnitude short at delta 0.018. At ~0.3 the binding limit is supply and exposure, not resolution.
- **Unscoreable picks:** a method that selects candidates BTS never observed cannot be scored on those candidates, because they have no spectrum.

## Replay
- **Coverage of the 38 cases in REPLAY_PLAN.md:**
  - 23 have concrete astronomy analogues.
  - 3 are pending an instance.
  - 8 are harness-level.
  - 4 have no analogue.
- **Protocol:** REPLAY_PLAN.md also sets the merge rules and the seal protocol. The holder of rulings and polarity must have written neither the skill nor any case, and a fresh session acts as the stage under test.
- **Design flaw found:** `cases.csv` carries the expected polarity, and `replay.py emit` prints it. Pass/fail is judged on polarity alone, so the rulings file only protects explanation text. The holder must keep polarity as well.
- **Cases contributed:**
  - **AST5-01** (A3, must_fire): BTSbot vs scanner purity on different denominators.
  - **AST5-02** (A4, must_fire, sealed): the 0.018 was acted on below the MDE.
  - **AST5-03** (D4, must_fire): the type column mixes human spectra, SNIascore auto-classifications and light-curve-only removals.
  - **AST5-04** (P3, must_not_fire): 11,217 rows collapse to 11,204 objects, with the must-join and must-separate checks run.

## Other disagreements (listed, not reconciled)
- **Row count:** the BTS file has 11,217 data rows, but the brief and FETCH.md said 11,218 (since corrected by the coordinator).
- **Peak column name:** the docs call it `time`; the CSV header says `peakt`.
- **The brief's "thousandfold" alert overstatement** varies by stage:
  - ~21,500× per night
  - 56.5× for BTSbot training
  - 1.51× for Fink
  - 0.116% for BTS rows
- **Sealed-case count:** replay.md says 12 cases are sealed, but also says "open the nine once".
- **Crossmatch radius:** a 2″ positional match would merge two distinct SNe, SN 2023ghl and SN 2024gyr (Agent 1 found the same).
- **2026 classifications:** 346 of the 387 rows with a 2026 peak have no classification.
- **Rubin dates:** the brief's Rubin dates were not verified by this agent and were not used. Agents 1 and 3 verified them.

## Files
REPLAY_PLAN.md, k_slot.json, delta_slot.json, subject_set_slot.json, d5_inputs.json, slot_records_flat.json, planning_mde_bracket.csv, seed_ledger.json, replay_cases.csv, replay_rulings.csv, sources/, scripts/, out/
