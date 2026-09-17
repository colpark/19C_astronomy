# Wave 5 · Agent 1: D1 census and D4 decision shape

> Agent 1 returned this report as text, because the harness blocks REPORT.md writes. The coordinator saved it here without changing its substance.

## Headline
**The D4 shape record picks generate / inverse problem, disposition ESCALATE, binding gate grader.** Status is DERIVED, awaiting PI ratification.
- The record passes the structure check against `schemas/domain_manifest.schema.json`. The checker's must-fire control fired.
- It also passes `validate.py provenance`.

**Only one grader can be used today, and it covers the SN Ia family alone.** That grader is SALT3-f22 (pinned `c7de5343…`). Its limits:
- It renders Ia only.
- Its phase range is −20 to +50 d.
- Its training set has no ZTF data.

**No usable forward model exists for other transients.**
- The wave-2 ZTF ParSNIP checkpoints were trained on light curves truncated at E1/E3, and on the very cohort the screening proposes to draw items from.
- Superphot+ serves a tutorial LightGBM classifier, not a frozen model.

**Two ways to clear the gate.** Either one also needs I4 certification of held-out log-likelihood as the scored quantity.
- (a) A D5-budgeted forward model, pinned separately, trained on full ZTF g/r light curves and disjoint from the item supply.
- (b) A PI scope restriction to the SALT3 family.

**The census supports this root only thinly.**
- Across 12 seeds read in full, there are 3 per-object generate branches, and only 1 of them names the rejected family.
- There are 79 per-study generate branches, which are model building.
- No seed grades predictions on unseen later epochs.

**The P3 protocol and bands are drafted and hashed, and nothing was counted** (`p3_protocol_DRAFT.md`, sha256 `cc3139a2…4035`). The three band edges that depend on N_min are UNDEMONSTRATED until I1 and P7 run.

## Method
- **Brief.** The brief hash was verified (`cd10a41c…`). All listed skill files were read in full. The stage briefs live at `references/stages/` (DS-13).
- **Sources.**
  - All 12 seeds were fetched fresh from arXiv, converted with `pdftotext -layout`, and their ids verified against the PDF headers. No id was wrong.
  - The texts held from earlier waves were not reused for locators, because wave-1 agent 4's copies had numeric table cells stripped.
- **Reading split.** ParSNIP was read personally. The other 11 seeds went to five reading forks working under one written rule set, because reading about 20k lines alone would overflow the context.
- **Quote checks.** Every branch carries a locator and a verbatim quote. A script checked all 452 quotes against the layout texts and found 0 failures. Agent 1 re-read 15 ruling-bearing locators in 7 seeds, and all matched.

## 1. D1 census (`census/branch_census.json`, `census/depth_census.json`)

| Seed | Chains (per episode) | Branches | With alternative | Rejected named | Per-object by kind |
|---|---|---|---|---|---|
| 1910.12973 BTS I | 16,9,10,8,9 | 25 | 25 | 22 | intervene 6, infer 8, explain 3 |
| 2009.01242 BTS II | 10,11,10,8,5 | 30 | 30 | 24 | intervene 4, infer 6, explain 4 |
| 2104.12980 SNIascore | 11,6,6,5 | 17 | 17 | 16 | infer 1, explain 1 |
| 2401.15167 BTSbot | 8,11,15 | 23 | 23 | 19 | intervene 5, infer 1 |
| 2109.13999 ParSNIP | 13,4,6,4 | 15 | 15 | 13 | none |
| 2403.07975 Superphot+ | 13,5,16,5 | 26 | 25 | 21 | explain 2, infer 1, generate 1 |
| 2405.03078 ATAT | 14,3 | 13 | 13 | 12 | none |
| 2104.07795 SALT3 | 11,4,3 | 17 | 17 | 13 | generate 1 |
| 1905.07422 Villar 2019 | 8,10 | 16 | 16 | 14 | infer 1, explain 1 |
| 2008.04912 Superphot | 9,5,11 | 20 | 19 | 16 | infer 4, explain 2 |
| 2409.04346 ZTF SN Ia DR2 | 15,5,4 | 14 | 14 | 8 | infer 2 |
| 1808.00969 AT2018cow (explain-type) | 16 | 20 | 20 | 17 | explain 11, infer 6, intervene 2, generate 1 |

**Totals.** 236 branches in all.

| Kind | Per object | Per object, rejected named | Per study |
|---|---|---|---|
| intervene | 17 | 11 | 8 |
| explain | 24 | 18 | 1 |
| generate | 3 | 1 | 79 |
| infer | 30 | 24 | 74 |

- **Multi-branch episodes.** 16 episodes hold at least two per-object branches. The richest is AT2018cow, with 20 in one episode.
- **Fitting is chain, not branch.** In every fitting seed, per-object fitting and fit rejection are uniform chain steps.

**Depth census.** 66 conclusions.
- Claimed channels: 4 at one channel, 26 at two, 25 at three, 8 at four, 3 at five.
- Measured depth is `not_measured` for all of them.
- Found cases where a subset of channels gave the wrong answer:
  - AT2018cow: the early Ic-BL reading was overturned by later data.
  - SN 2020eyj: the Ia call from the spectrum alone was overturned by the light curve.

## 2. D4: all four roots ruled in one pass, at subtype level (`shape_record.json`)

| Root / subtype | Gate 1 | Gate 2 | Gate 3 | Ruling |
|---|---|---|---|---|
| infer / pick k of M | predictor, on the line, no lift recorded | labels: TNS/WISeREP blocked; BTS labels public; post-2021-04-15 labels partly model-made | k = 8 thresholded; MDE 0.032–0.063; floor 0.951 | CLOSE (grader) |
| infer / calibrated probability | on the line | same labels | 1 graded per candidate | CLOSE (grader) |
| infer / point forecast of post-cut photometry (derived subtype; practised as BTSbot's mpeak ≤ 18.5 forecast, p3 L168-170) | on the line, no lift | answer key = held-out photometry, which is public in the unit's own source | 1 graded | CLOSE (role floor) |
| explain / hypothesis set | scorer, below the line | on ZTF bands, a usable likelihood exists for the Ia hypothesis only | H graded, but correctness needs an adjudicated cause | ESCALATE (grader) |
| explain / anomaly diagnosis | scorer, below | no judge, no repeat measurements | 1 | CLOSE (grader) |
| explain / mechanism attribution | scorer, below | no judge | 1 | CLOSE (grader) |
| **generate / inverse problem** | **generator, below** (holds only if the answer is a model instance) | **SALT3-f22 covers Ia only; a general model needs a D5 build** | **1 graded** | **ESCALATE (grader), chosen** |
| generate / object design | generator | no certified oracle; SNANA UD | pass/fail | CLOSE (grader) |
| generate / procedure or code | generator | a harness checks execution, not the scored quantity | binary per test | CLOSE (grader) |
| intervene / next measurement | simulator | no replayable environment; BTSbot's labels are the historical policy (p4 L225-237) | 1 per episode | CLOSE (grader) |
| intervene / allocate budget | simulator | none | per round | CLOSE (grader) |
| intervene / decide when to stop | simulator | none | 2 graded | CLOSE (grader) |

**Yield.** 1 unit yields 1 graded scalar: −0.5·χ² summed over held-out g/r detections under the frozen grader. The per-band and per-epoch terms share one parameter vector, so they are not independent.

**Alternatives.** 11 entries, spanning all three rejected roots, each with its binding gate.

**Ranking on resolving power.**
- Order: generate / inverse first, because it needs no per-unit label and is graded; explain / hypothesis set second, because it is label-bound; the closed infer rungs below both.
- This order is UNDEMONSTRATED, because no MDE exists except for pick-k.
- Grader cost was not used to rank, because both survivors need the same build.

**Item template.**
- The arm sees g/r photometry up to a recorded cut (wave-2 E1/E3).
- It returns a family from the grader's set, parameters including z or its bounds, and a written rejection of each rival family.
- A frozen instance scores the held-out epochs. That instance is pinned separately from the arm tools.
- Corpus locators: Superphot+ Fig. 17 (L1814-1819), ParSNIP §4.3 (L812-818), Superphot §5.1 (L1093-1098). Held-out-epoch scoring itself has no locator.

## Disagreements with the screening (recorded, not reconciled)

**Grader and tool status**
- **DS-01:** the wave-2 ZTF ParSNIP cannot be the grader. It was trained on E1/E3-truncated light curves from the cohort itself, its learning rate was amended, and fold 4 stalled.
- **DS-02:** Superphot+ is a predictor backed by a tutorial classifier; its parametric form has no frozen weights.
- **DS-03:** SALT3 covers the Ia family only, over −20 to +50 d, and has no ZTF training data.
- **DS-11:** the floor may use only families the grader can render. Bazin and Villar cannot be rendered, and ParSNIP's default encoding needs a z.

**Task framing and yield**
- **DS-04:** yield is 1 independent scalar per unit, not "several".
- **DS-05:** the action is not where the screening assumed. There are 3 per-object generate branches, and held-out-epoch prediction is practised nowhere.
- **DS-06:** scoring only on held-out photometry makes this a forecast, which shape.md classes as infer. The held-out points are public in the unit's own light curve, where arms with shell access can reach them.
- **DS-08:** explain / hypothesis set is ESCALATE, not a conditional pass.
- **DS-09:** rejecting a degenerate fit is a uniform cut, not a native branch.
- **DS-10:** "+10 d" and "≥20 epochs" are conventional values.

**Contamination**
- **DS-07:** published fits are common, not rare. DR2 publishes SALT2 fits for 3,628 SNe Ia, 79% of which overlap BTS. Superphot+ publishes per-object χ² on Zenodo and saves fit parameters on ANTARES.

**Other**
- **DS-12:** agreement that intervene closes at the grader.
- **DS-13:** the stage-brief path.

## 3. P3 protocol (DRAFT, not counted)
- **Unit.** One 1″ cluster, cut at a recorded E1 or E3, with held-out g/r detections inside the grader's phase range.
- **Negatives.**
  - Found negatives are listed with locators: the 48 Superphot+ unfit light curves, CV/AGN impostors, and SN 2020eyj.
  - Constructed negatives enter only if the floor itself would select the rival.
- **Contamination.** Exact-match each unit against the DR2 tables, Superphot+ Table 5 / ANTARES, and ADS full text. Answer-in-source exposure is reported beside the match result.
- **Split.** No unit may appear in the grader's training set. Every cohort unit fails this against the wave-2 checkpoints.
- **Open quantities.** N_min, σ_d, chance, the P2 floor, I4 and per-tool minimum points are UNDEMONSTRATED, each with the stage that supplies it named.

## 4. Replay cases (`replay_cases.csv`, rulings in `replay_rulings.csv`)
- **AST1W5-01** (D4, must_fire): early-truncated ParSNIP trained on the items is offered as the grader, with PROCEED.
- **AST1W5-02** (D1, must_fire): an item-template locator is claimed as practised, and uniform χ² cuts are counted as branches.
- **AST1W5-03** (D1, must_not_fire): the Superphot+ object-by-object diagnosis is a branch, and its χ² cut stays chain.
