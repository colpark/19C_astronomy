# Wave 2 · Agent 4: instrument (PRE-I1 calibration compositions, I2, power calibration)

> calibration only, contamination FAIL on this cohort
> PRE-I1: graph edge R1→I1 unmet, escalated. Staging ratified by the PI in wave 3, ruling 3; the I1 designation still waits for R1 plus PI ratification.
>
> Agent 4 returned this report as text, because the harness blocks subagents from writing REPORT.md. The coordinator saved it here without changing its substance.

## Headline
- **Blinded builds, hashed before scoring.** Both compositions were built blind at the two declared decision epochs. Every model and prediction file was hashed before any score was computed.
- **Deep channel adds nothing.** ParSNIP was trained from scratch on ZTF g/r with no redshift anywhere, and it gives no measurable gain over the classical (Fink-remapped) composition at either epoch.

  | Epoch | Metric | C (with ParSNIP) | C−1 (without) | Chance |
  |---|---|---|---|---|
  | E1 (first alert) | per-object AUC | 0.597 | 0.600 | 0.5 |
  | E3 (night 3) | per-object AUC | 0.618 | 0.637 | 0.5 |
  | E1 | precision@8, 46-candidate rounds | 0.309 | 0.345 | 0.230 measured |
  | E3 | precision@8, 46-candidate rounds | 0.336 | 0.361 | 0.230 measured |

  ParSNIP on its own reaches AUC 0.534 [0.505, 0.563] at E1 and 0.514 [0.487, 0.540] at E3.
- **No directional claim.** All differences sit inside the MDE (global refusal 5), and BTS failed contamination (addition B).
- **Per-night precision@8 is degenerate on this file.** 518 of 579 nights have 8 or fewer candidates, so k never binds.
  - The pooled power.py run returned RESOLVABLE. That ruling is refused because it averages over unequal denominators (refusal 4).
  - **Nights where k binds (61):** σ_d 0.090, MDE 0.032 against delta 0.018, N_min 196, **CLOSE_UNRESOLVABLE**.
  - **46-candidate rounds:** MDE 0.055 at E1 and 0.063 at E3, both CLOSE_UNRESOLVABLE.
  - These are calibration results, not P7.
- **Four new code defects**, each listed in a tool card and none repaired:
  1. ParSNIP's no-redshift path (`input_redshift=False`) crashes.
  2. ParSNIP produces NaN on single-detection light curves at default settings.
  3. Fink's SLSN fit passes FLUXCAL (ZP 27.5) but declares zp=25.
  4. Fink's fast-transient rate depends on which other alerts are in the batch.

## Order (ordering constraint)
1. `r1_spec.md` was written first (sha256 `f278b0bb…a579a07b`).
2. `compositions_FROZEN.md` was written before any fetch, feature or model (sha256 `b2f72948…9d045427c`). Every script aborts if either hash changes.
3. The brief hash `31a36617…f4eb` was verified before anything was written.
4. `AMENDMENTS.md` records three amendments, each with its cause, before the computation it affects. None was chosen after seeing labels or metrics.
   - **A-1.** ParSNIP `input_redshift=False` raises `UnboundLocalError` (parsnip.py `_get_data`). The fix keeps the code default and sets the photo-z inputs to constants shared by all objects, so no redshift information enters.
   - **A-2.** Loss went NaN at the default learning rate: an empty augmented light curve at step 2, and another failure at step 30 without augmentation. This was the second distinct repair (ladder rung 3). Setting lr to 1e-4 gave 1,075 steps without NaN, and all five folds then trained without NaN.
   - **A-3.** sklearn 1.9.1's GBDT crashes on training columns that are entirely NaN. Those columns are dropped per fold. This is information-neutral, since a tree cannot split on them.
5. The pipeline then ran in this order: fetch, features, ParSNIP (5 folds), GBDT fit and predict. `compositions/MANIFEST.sha256` (129 files, `ff84d288…c7c871`) was written before `score.py`, which refuses to run unless every hash verifies.

## Dispositions

| Criterion | Disposition |
|---|---|
| R1 spec (known-good subject, synthetic item, stub, 3 pre-written dispositions, cap) | **PASS** (written, hashed) |
| R1 run | **UNDEMONSTRATED**. D5→R1 unmet; this blocks I1-as-record and R2–R8 |
| Declarations frozen before computing (A) | **PASS**, with 3 amendments recorded with cause |
| Epochs re-checked against agent 3's frozen manifest | **UNDEMONSTRATED**. The manifest does not exist yet; the epochs cite the hashed brief |
| Decision-time photometry (ALeRCE; 3,435 of 3,435 pulls, 0 failed, 3,435 calls against a 4,000 cap) | **PASS**. Raw-pull manifest `b6eaa73e…fd62690`; 0 unprocessable |
| Blinded compositions hashed before scoring (I1 discipline) | **PASS** as calibration; **UNDEMONSTRATED as I1** |
| Classical composition (Fink remapping) | **PASS** (built) |
| Deep composition (ParSNIP, from scratch, no redshift) | **PASS** (built): 5 folds, 60 epochs, 100% finite predictions, 2.38 of 3 GPU-h |
| Pretrained ParSNIP on ZTF | **UNDEMONSTRATED**. Refused under I4: LSST/PS1 bands only, and no band conversion exists |
| ATAT on ZTF | **UNDEMONSTRATED**. No ZTF weights or dataset entry |
| I2: C−1 and C at both epochs | **PASS** (measured, calibration) |
| Label-permutation control, band [0.45, 0.55] | **PASS**: 0.515 and 0.514 at E1; 0.496 and 0.490 at E3 |
| Power calibration | **CLOSE_UNRESOLVABLE** on binding nights and on rounds (calibration, not P7) |
| I3 tool cards (4, from code, validated) | **PASS**. I4 and I5 are **UNDEMONSTRATED** |

## Cohort and definitions (frozen)
- **Cohort.** Agent 1's `corpus.csv` rows with peak in [2019-06-01, 2021-04-15): 3,435 rows, which is 3,432 objects at 1″. The window ends at the start of SNIascore auto-reporting, and its size was set by API cost. Peak is used only for membership.
- **Scored pool.** 2,558 labelled objects: posA 2,264 and neg 294. The 874 unlabelled objects count for coverage only.
- **Positive class.** posB, i.e. non-Ia extragalactic transients: 586 objects, prevalence 0.229.
- **Epochs.**
  - **E1:** the first positive g/r detection plus 30 days of history (ZTF alert schema, line 142).
  - **E3:** photometry through ZTF night n0+3, with nights split at 20:00 UTC.
- **Folds.** 5, assigned by sha256 of the 1″ cluster id.
- **Channels.**
  - C1: Fink EarlySNIa sigmoid features
  - C2: Fink fast-transient rate
  - C3: Fink SLSN feature vector
  - C4: raw alert photometry plus b. This channel is not Fink; it was added as the strongest classical arrangement, and that is disclosed.
  - C5: ParSNIP latent
  - C = C1–C5; C−1 = C1–C4.
- **Forbidden inputs, enforced in code.** peakabs, redshift, type, IAU name, peak/duration/rise/fade, A_V, rb/drb, and broker scores.

## Results (out-of-fold, chance beside each)

| | E1 C−1 | E1 C | E3 C−1 | E3 C | Chance |
|---|---|---|---|---|---|
| AUC posB [95% CI] | 0.600 [0.574, 0.626] | 0.597 [0.570, 0.622] | 0.637 [0.613, 0.663] | 0.618 [0.593, 0.643] | 0.5 |
| P@8, 46-candidate rounds (55) | 0.345 | 0.309 | 0.361 | 0.336 | 0.230 measured / 0.172 stated |
| P@8, nights (579; 61 binding) | 0.2253 | 0.2271 | 0.2277 | 0.2260 | 0.2246 measured / 0.172 stated |
| C5 alone, AUC | | 0.534 [0.505, 0.563] | | 0.514 [0.487, 0.540] | 0.5 |

### I2 (`i2_channels.json`)

| Channel | Alive E1 | Alive E3 | ΔAUC E1 | ΔAUC E3 |
|---|---|---|---|---|
| C1 | 0.0003 (dead) | 0.041 | 0.000 | −0.002 |
| C2 | 0.945 | 0.963 | +0.005 | +0.028 |
| C3 | 0.000 (dead; the gate needs duration > 30 d) | 0.0006 | +0.033 | +0.024 |
| C4 | 1.0 | 1.0 | −0.002 | +0.002 |
| C5 | 1.0 | 1.0 | −0.003 | −0.019 |

Honest channel count, as the sum of alive fractions:
- **E1:** 2.95 of 5 (classical 1.95, deep 1.0)
- **E3:** 3.00 of 5 (classical 2.00, deep 1.0)

### Power calibration (`power_calibration.json`; power.py unchanged, k=8, 46.41 candidates, delta 0.018)

| Items | d (classical − instrument) | σ_d | MDE | N_min | Ruling |
|---|---|---|---|---|---|
| E1, binding nights (n=61) | −0.016 | 0.090 | 0.032 | 196 | CLOSE_UNRESOLVABLE |
| E3, binding nights | — | 0.084 | 0.030 | 171 | CLOSE_UNRESOLVABLE |
| E1, 46-candidate rounds (n=55) | — | 0.146 | 0.055 | 515 | CLOSE_UNRESOLVABLE |
| E3, 46-candidate rounds | — | 0.166 | 0.063 | 665 | CLOSE_UNRESOLVABLE |

- The pooled nights run returned RESOLVABLE (MDE 0.003), which is refused under refusal 4.
- The measured σ_d of 0.084–0.166 falls inside agent 5's planning bracket of 0.040–0.250.

## Disagreements (listed, not reconciled)
1. **Chance.** Stated 0.172 (8/46.41) against measured 0.225–0.230. The file holds only saved sources.
2. **Per-night item.** Per-night precision@8 does not bind for 518 of 579 nights; the mean is about 4 saved objects per night.
3. **C3 alive vs contribution.** C3 is dead at E1 by its own gate, yet it has the largest ΔAUC (0.033). The contribution comes through always-present columns (ra, dec, distnr, ebv, duration). C5, by contrast, is 100% alive and near chance alone.
4. **C4.** Brightness at the epoch adds nothing (±0.002).
5. **ParSNIP fold 4.** Loss plateaued near 247, against about 6 for folds 0–3. Its predictions and weights are finite. Not repaired.
6. **SN Ia AUC.** The descriptive SN Ia AUC here is 0.47–0.50, against agent 2's first-alert tier of 0.537. The two are not comparable (different target and pool).
7. **ParSNIP code vs its own claims.**
   - The no-redshift setting crashes (A-1).
   - A comment says empty augmented light curves are "handled gracefully", but they are not (A-2).
   - The default learning rate is unstable.
8. **Fink EarlySNIa.**
   - The comment says "less than 3 points", but the code requires 4.
   - The docstring says `chisq`, but the code computes `mse`.
   - A comment says "at least three points", but `min_rising_points` is 2.
   - `isdiffpos` is ignored.
9. **Fink fast-transient rate.**
   - The shift uses the batch-wide minimum, so values depend on the batch.
   - The shift is applied unconditionally.
10. **Fink SLSN.**
    - FLUXCAL at ZP 27.5 is fit with zp=25.
    - Magnitudes are not re-sorted with time.
    - The code sets `min_points_total = 7` but tests `> 7`.
    - SALT2 is unpinned (T23 was served).
11. **Detection counts.** For ZTF19acjiett, Fink returns 10 valid detections and ALeRCE returns 26.
12. **SFD dust map.** The dataverse fetch returned HTML. The kbarbary/sfddata mirror was used instead; it reproduces Fink's doctest values (0.2548, 0.1060).
13. **Recurrent objects.** 99 objects have a first alert more than 100 days from the BTS peak, mostly recurrent objects. They are stratified, not removed.

## Still UNDEMONSTRATED

| Item | Blocks |
|---|---|
| R1 run | I1-as-record, R2–R8, A1–A4 |
| PI ruling on the R1→I1 ordering (staging ratified in wave 3; the I1 designation is still pending) | re-registering as I1 |
| Epoch check against the frozen manifest | I1-as-record |
| ATAT on ZTF; pretrained ParSNIP on ZTF | I2 completeness, I4, I5 |
| Label source (measured vs SNIascore) | any claim resting on posB |
| Contamination-free cohort | P7, A3, A4 |
| Rubin inputs | I2 and I4 on the governed stream |
| C1 and C3 papers unread | paper-side disagreements |
| I4 and I5, all channels | R4, R8 |

## Deliverables
- `r1_spec.md` (+sha)
- `compositions_FROZEN.md` (+sha)
- `AMENDMENTS.md`
- `compositions/`: 5 ParSNIP .pt, 90 GBDT .pkl, prediction CSVs, `MANIFEST.sha256`
- `HASH_MANIFEST.sha256` (`9d89d4fa…9003b`)
- `i2_channels.json`
- `paired_scores.csv` (1,268 items)
- `power_calibration.json`
- `provenance_records.json` (12)
- `tool_cards/`: 3 new Fink cards and an updated ParSNIP card
- `scripts/`
- `sources/` (SHA256SUMS)
- `seed_ledger.json`
- `data_cache/` (gitignored, hashed)
- `replay_cases.csv` (AST4W2-01, -02, -04 must_fire; -03 must_not_fire) and `replay_rulings.csv`
- `validate_stdout.txt` (PASS on provenance, the power record, 4 raw power runs, 4 tool cards)
