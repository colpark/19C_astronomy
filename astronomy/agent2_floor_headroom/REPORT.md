# Agent 2: prior floor and headroom (P2)

> Agent 2 wrote this report and returned it as text, because the subagent harness blocks report-file writes. The coordinator saved it here without changing its substance.

This is a pre-P1 sketch. I1 was not run because R1 has not run. D5, delta, k, budget and cost of action are all missing.

## 1. Dispositions

| Criterion | Disposition | Record |
|---|---|---|
| Floor share of an **FM** ceiling on the same data, for the pre-spectroscopy slot decision | **UNDEMONSTRATED** | pr-a2-16 |
| Floor share of a **deep (non-FM)** ceiling on the same data, for photometric transient classification | **FAIL for headroom** (0.951–1.000 across 3 matched sources) | pr-a2-01..04 |
| FM against a deep baseline (Maven) | FM falls below the deep baseline (0.980); no classical row exists | pr-a2-06 |
| In-corpus P2 prior floor | **PASS** (stated with chance, controls and grouping) | pr-a2-12..15 |
| Leakage from post-spectroscopy features to decision-time features | **PASS** (measured) | pr-a2-15 |

The headline is UNDEMONSTRATED for three reasons. No evidence held pairs an FM with a classical model on the same data, split and metric. No pair is scored at decision time on an allocation metric. Delta is unratified, so a 0–4 point gap cannot be judged against a band. Against deep models the classical floor already takes 95–100% of the ceiling, which is higher than the source record's P2 pattern (K06: 0.2864/0.3127 = 0.916).

## 2. arXiv ids
The brief's five ids were confirmed by download and first-page title: 2104.12980, 2008.03311, 2012.12392, 2205.01677 and 2408.16829. **No id errors.**

Sixteen more were found through the arXiv API and downloaded:
- 2008.03309 (stamp classifier)
- 2405.03078 (ATAT)
- 2501.01496 (ORACLE-1)
- 2607.00228 (ORACLE-2)
- 2404.08798, 2008.04912, 2008.04921, 2403.07975, 2305.08894, 2109.13999, 2401.15167, 2502.20479, 2507.12611, 2502.02717, 2410.10963, 2412.08601

No ELAsTiCC results paper was found: `all:ELAsTiCC` returned 14 papers, none of them a results paper.

## 3. Floor/ceiling table (adjudicator is the strongest classical row per source)

| Record | Data | Metric | Classical floor | Deep ceiling | Share | In ratio? |
|---|---|---|---|---|---|---|
| 01 | ELAsTiCC sim, 20,000 test | macro F1 | BHRF 79.4±0.1 | ATAT 83.5±0.6 (Table 1, p.8) | **0.951** | yes (deep, not FM; uses redshift metadata) |
| 02 | Real ZTF, 6,061 SNe, identical LightGBM | multi-class F1 | Superphot+ (with z) 0.71±0.02 | ParSNIP/SuperRAENN 0.71±0.03 (Table 4, p.24) | **1.000** | yes (uses z) |
| 03 | same | binary F1 | 0.92±0.01 | ParSNIP 0.95±0.01 | **0.968** | yes |
| 04 | PLAsTiCC, true z | Ia AUC | Avocado 0.962 | ParSNIP 0.977 (§5.3) | 0.985 | partial (test size unstated) |
| 05 | PLAsTiCC private leaderboard | weighted log-loss | avocado 0.6850 | hybrids 0.6993/0.7002 | classical wins | no (hybrids; ranking flips without "Other") |
| 06 | BTS, 4,702 SNe | macro F1 | none | Maven 0.6874 vs supervised 0.7011 | — | no classical row |
| 07 | SEDM spectra | TPR at FPR<1% | SNID 0.53 | SNIascore 0.90 | 0.589 | no (post-spectrum; tuning set) |
| 08 | SEDM spectra | TPR at FPR 10% | SNID ~0.75 | CCSNscore ≥0.90 | ≤0.83 | no (post-spectrum; read off a plot) |
| 09 | SEDM, 4,646 spectra | accuracy | NGSF 0.876 | DASH 0.762 | 1.15 | no (post-spectrum; weak ceiling) |
| 10 | ALeRCE, real ZTF | macro F1 | XGBoost 0.71 | MLP 0.58 | 1.22 | no (shallow MLP) |
| 11 | PS1-MDS, 557 SNe | macro F1 | RF 0.628 | MLP 0.566 | 1.11 | no (shallow MLP) |

- **SuperRAENN** was not entered. RAENN alone reaches 53% against 80% for Villar 2019, but Villar 2019 was not read. The authors conclude that hand-selected features outperform (p.21).
- **ParSNIP on PS1-MDS** was not entered because its folds differ.
- **No classical row** exists for ORACLE-1/2, Astromer 1/2, SwinV2, Astro-MoE, Fink or BTSbot. BTSbot was only grepped.
- **No averaging** was done, because the denominators are unequal.

## 4. In-corpus prior floor (a P2 prior estimate, not an I1 composition)

**Setup.**
- Code is `floor_prior.py`; output is `prior_floor_results.json`. The data sha256 matches.
- Declared before the run:
  - grouped 5-fold cross-validation; groups merge identical IAU names and positions within 3″
  - gradient boosting and logistic regression, with the stronger one taken as the floor
  - controls: label permutation, and a temporal split (train before 2023, test after)
- Raw vs clustered: 11,217 rows form 11,198 groups (0.17%), and 7,843 classified objects form 7,830 groups.

**Feature tiers.**
- **T1:** all seven brief columns. Peak absolute magnitude and redshift are available only after spectroscopy.
- **T2:** photometry only, using the full light curve.
- **T2+z:** T2 plus redshift.
- **T3:** features available at observed peak (peak mag, rise, b).
- **T4:** galactic latitude b only, as at first alert.

**Task A: SN Ia vs all other classified objects** (prevalence 0.680)

| Tier | AUC (95% CI) | AP | AUC, temporal split | Share of T1 signal above chance |
|---|---|---|---|---|
| T1 | 0.967 (0.963–0.972) | 0.979 | 0.966 | 1.00 |
| T2+z | 0.964 | 0.975 | 0.962 | 0.99 |
| T2 | 0.868 | 0.905 | 0.843 | 0.79 |
| T3 | 0.798 (0.787–0.809) | 0.851 | 0.787 | 0.64 |
| T4 | 0.537 | 0.701 | 0.530 | 0.08 |

- Label-permutation control: AUC 0.486.
- Within SNe only: T1 0.951, T2 0.818, T3 0.726, T4 0.503, so T3 keeps half the signal.

**Task B: a "non-routine" proxy for worth-a-slot** (panel proxy, not ratified; prevalence 0.122)

| Tier | AUC | AP |
|---|---|---|
| T1 | 0.901 | 0.641 |
| T2 | 0.730 | 0.299 |
| T3 | 0.672 | 0.264 |
| T4 | 0.524 | 0.130 |

**Finding: the tiers split sharply.**
- **Redshift carries the post-spectroscopy lift.** T2+z recovers 98–99% of T1.
- **At decision time the floor keeps only 43–64%** of the post-hoc signal. At first alert these columns are near chance.
- **The literature pairs in §3 are all post-hoc.** They use full light curves, and the Superphot+ pairs also use z. Their 0.95–1.00 shares describe a regime where the floor is already saturated.
- **FM headroom has to be measured on decision-time inputs.** No one has done that.
- The 3,374 unclassified objects were excluded; this is disclosed, not repaired.

## 5. Disagreements (listed, not reconciled)
1. **Row count.** The CSV has 11,217 data rows, while FETCH.md and the brief said 11,218. The coordinator has since corrected both.
2. **ATAT's internal numbers.**
   - Abstract 82.9±0.4 against Table 1 82.6±0.5.
   - §4 RF 0.772 and ATAT 0.825 against Table 1 79.4 and 83.5.
3. **ORACLE-2 on the deep-vs-RF gap.** It cites "+5% to +10%" (§3.1), while ATAT Table 1 shows +3.2 to +4.1 points.
4. **ALeRCE's deployed model.** ALeRCE deployed a BRF at F1 0.59 although GBoost reached 0.71 on the same split. The authors say feature-based models beat deep learning on real data (p.28).
5. **Direction of the deep advantage.** ATAT finds one on simulated data; Superphot+ Table 4 finds none on real ZTF.
6. **SNIascore's reported TPR.** The comparison uses the tuning set (90%); the held-out test set gives 83%.
7. **PLAsTiCC ranking.** The ranking flips when "Other" is excluded (Fig. 5).
8. **MACHO test split.** "1000 per class per fold" (Astromer 2) against "100 per class" (SwinV2).

## 6. UNDEMONSTRATED and what each blocks

| Item | Blocks | Needs |
|---|---|---|
| Any FM-vs-classical matched pair | P2 ruling, I1 headroom, P6/P7 | I1 after R1: a tuned GBDT against an FM channel on identical BTS folds, at decision-time inputs |
| Decision-time pair on precision@k | P2 on the governed decision, P7 MDE | k and label source from D4 |
| Delta | pricing the 0–4 pt deep gaps | D4/D5 |
| ELAsTiCC broker results | a cross-broker table | a located results publication |
| Full reads of BTSbot, ORACLE-1, Astromer, SuperRAENN and the ORACLE-2 appendix | nothing in the current ratio; required before D1 | full reads |
| Rubin alert and LSST start dates | outside this scope | verified by Agent 1 |

## 7. Files
- `prior_floor_record.json`: 17 provenance records, validate PASS.
- `floor_prior.py` and `prior_floor_results.json`.
- `sources/`: 21 PDFs (hashed in SHA256SUMS and not committed), page-marked text and BTS explorer docs.
- `seed_ledger.json`: 23 entries. Five are `read_in_full: false`, and none of those supplies a ratio number. Ten were read in full by two helper agents, with key locators checked by grep.
- `replay_cases.csv` and `replay_rulings.csv`: four P2 cases, three must_fire and one must_not_fire.
