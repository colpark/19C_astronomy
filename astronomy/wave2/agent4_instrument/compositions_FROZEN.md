# Compositions: declarations FROZEN before any fetch, feature, model or score

calibration only, contamination FAIL on this cohort
PRE-I1: graph edge R1→I1 unmet, escalated

- Author: wave-2 agent 4. Frozen 2026-09-16, after `r1_spec.md` (sha256 `f278b0bb3818ad1de981ba14f0e331003138683ac1da5fe4b92e26ada579a07b`). The sha256 of this file is in `compositions_FROZEN.sha256`, and every script re-checks it before it runs, aborting on mismatch.
- Epoch source: the decision epochs cite the hashed brief `astronomy/wave2/PANEL_BRIEF_WAVE2.md` (sha256 `31a36617…a0f4eb`, matches `BRIEF_SHA256`). Agent 3's frozen manifest did not exist when this file was frozen (`wave2/agent3_manifest_freeze/` empty). The epochs must be re-checked against the frozen manifest hash when it exists.
- Addition A (declare before counting) governs this file. Addition B also governs it: no claim rests on this cohort.

## 0. What was seen before freezing (disclosure)
- **Code read.** I read:
  - Fink `ztf/random_forest_snia/processor.py`, `ztf/superluminous/{kernel,slsn_classifier,processor}.py` and `ztf/fast_transient_rate/{processor,utils}.py` (fink-science@591e75ce, wave-1 clone)
  - actsnfink `classifier_sigmoid.py` and `sigmoid.py` (fink_sn_activelearning@f424ab1f, cloned to `code/actsnfink`)
  - fink_utils 0.77.0 `photometry/conversion.py` and `data/utils.py` (wheel sha256 `bfdef569…861c27a`)
  - ParSNIP `parsnip.py`, `settings.py`, `instruments.py`, `light_curve.py` and `classifier.py` (kboone/parsnip@dcea62f, copied to `code/kboone_parsnip_dcea62f`)
  - ZTF avro alert `docs/schema.md` line 142
- **API probes.** Three probes on objects to time the API: ALeRCE `/objects/{oid}/lightcurve` about 1.5 s per call (3 calls); Fink `/api/v1/objects` about 1.2–2.8 s per batch of 3. For ZTF19acjiett, Fink returned 10 valid detections against ALeRCE's 26, so ALeRCE is the declared source.
- **Row counts.** Row counts of `agent1_supply_corpus/corpus.csv` by peak-date window only:
  - 2019-06-01..2020-06-01: 1,718
  - 2020: 1,771
  - 2019-06-01..2021-04-15: 3,435 rows / 3,432 1″ objects
- **Not looked at.** No label, type, redshift or outcome distribution was looked at for any window. No photometry was fetched for the cohort.

## 1. Decision epochs (D4 slot, from the brief)
- **ZTF night index:** `night(mjd) = floor(mjd − 0.8333)`. The boundary is 20:00 UTC, which is local midday at Palomar (UTC−7/−8); ZTF exposures fall at MJD fractions of about 0.08–0.60, so no night is split.
- **First detection** `t0` is the minimum `mjd` over ALeRCE `detections` rows for the unit with `isdiffpos` positive (1 or 't') and `fid` in {1, 2}. `n0 = night(t0)`.
- **Primary epoch E1, "first alert".** The inputs are exactly the contents a first alert packet can hold:
  - detections with `mjd ≤ t0 + 1e-5` (the triggering exposure)
  - earlier detections and non-detections with `t0 − 30 ≤ mjd < t0`. The 30-day history is the `prv_candidates` window (ztf-avro-alert docs/schema.md:142).

  Decision night = `n0`.
- **Secondary epoch E3, "night 3".** Every detection and non-detection with `mjd ≥ t0 − 30` and `night(mjd) ≤ n0 + 3`. That is photometry through the end of the third ZTF night after the first-detection night. Decision night = `n0 + 3`.
- **Bands:** only fid 1 (g) and 2 (r) enter. fid 3 is dropped at both epochs; Fink's SNIa and SLSN code keeps g and r only.
- **Recurrent objects:** the "first alert" is taken literally, so for recurrent objects (CV, AGN) `t0` can be long before the BTS peak. Such objects are reported as stratum `epoch_far_from_peak` (|peak − t0| > 100 d) and never removed.

## 2. Cohort (rule-based; not selected on outcome)
- **Source.** `astronomy/agent1_supply_corpus/corpus.csv`, sha256 `b059acf0656ed79fc743944b560aa3fd358096963067d96e144850403c3d8442`. These are agent 1's included rows built under `corpus_rules_FROZEN.md` (sha256 `aa4e8d21…d2aa41a`), from BTS CSV sha256 `61415979…ebe570`.
- **Rule.** Every row whose `peakt` (JD − 2458000) converts to a UTC date in **[2019-06-01, 2021-04-15)**. Nothing else excludes a row.
- **Why the end date.** 2021-04-15 is the SNIascore auto-report start named in the wave-2 brief, so labels in this window predate automated TNS reporting. That reduces model-annotation exposure without claiming it is zero.
- **Why the start date and size.** The window extends back to the largest contiguous window under a **4,000-call** ALeRCE cap: about 3,435 calls at about 1.5 s gives about 1.4 h serial, or about 25 min at 4 concurrent. That is under 1% of a day of API load, and a full two-year window would double it.
- **Membership caveat.** Membership uses peak time, a full-light-curve quantity, for membership only, never as an input. This is a timing selection, not an outcome selection. Objects whose peak falls outside the window are absent, disclosed and not repaired.
- **Unit and label pool.**
  - **Unit:** agent 1's `object_cluster_1arcsec`. The light curve of a unit with several ZTFIDs is the union of their ALeRCE detections, deduplicated on `candid`.
  - **All units:** every unit is fetched, featurised and predicted.
  - **Scored pool:** units whose `type` maps under agent 1's frozen label map to posA or neg.
  - **Coverage only:** unlabelled (`-`) and unmapped units are counted as coverage, never scored and never counted as negatives.

## 3. Grouping and split
- **Folds.** 5 folds with groups = `object_cluster_1arcsec` (the wave-1 1″ unit). Fold = `int(sha256("w2a4-fold|" + str(cluster_id))[:8], 16) % 5`, which uses no label.
- **Use of folds.** Every model is fit on 4 folds and predicts the 5th, so all predictions are out-of-fold.
- **Not merged.** Agent 1's sibling (same-host) groups are not merged, because the sibling rule uses redshift, a forbidden column. This is disclosed.

## 4. Labels, scored quantity, metrics
- **Primary positive: agent 1's posB,** a non-Ia extragalactic transient (the rare-class slot). A type is posB if it starts with one of `SN `, `SLSN`, `TDE`, `nova`, `LRN`, `LBV`, `ILRT`, `Ca-rich`, `Other`, `other` and does not start with `SN Ia`.
  - **Negatives:** every other scored-pool unit (SN Ia family, CV, AGN).
  - **Why posB.** posA prevalence among the labelled is about 0.9, which makes precision@8 uninformative; posB is the discriminating allocation. Neither label is ratified: the D4 label source is UNDEMONSTRATED.
- **Primary metric: precision@8 per item, paired.**
  - **Item N (primary, as briefed):** one decision night. Candidates are the scored-pool units whose decision night equals it. Take the top `min(8, n)` by composition score, breaking ties by ZTFID ascending; precision = posB among them / `min(8, n)`. Nights with n ≤ 8 carry stratum `k_binding = False`. Their precision equals the night prevalence for both compositions by construction. They are kept, never filtered.
  - **Item R (declared sensitivity item):** consecutive rounds of 46 scored-pool units in decision-epoch time order (the integer nearest the manifest's 46.41 candidates per round), precision@8. The last partial round (< 46) is dropped and counted.
  - **Chance.** Stated manifest chance is **0.172** (8/46.41; `agent5_resolution_replay/k_slot.json`). The measured chance of a random pick per item is n_pos/n, reported beside it. The BTS file holds saved sources only, so measured chance will differ; this is a listed disagreement, not reconciled.
- **Secondary metric:** per-object ROC AUC for posB over the scored pool (chance 0.5), with a 1,000-resample object bootstrap 95% CI, seed 0.
- **Descriptive only, no claim:** per-object AUC for SN Ia vs other, for comparability with agent 2's T4 at first alert (0.537).
- **Controls.** These are declared before the run. The primary disposition rests on both.
  - **Must fire:** a label-permutation run (posB shuffled within the scored pool with seed 1, full pipeline refit). AUC must fall inside [0.45, 0.55], otherwise leakage is declared and every number is void.
  - **Must not fire:** the unpermuted run is not voided by that check.

## 5. Forbidden inputs (any appearance voids the composition)
- **BTS CSV columns:** `peakabs`, `redshift`, `type`, `IAUID`, `peakt`, `peakmag`, `peakfilt`, `duration`, `rise`, `fade`, `A_V`, `b` as given in the CSV, and every agent-1 flag. `ZTFID` is a join key only. `peakt` is used for cohort membership and stratum reporting only.
- **Photometry:** any photometry after the epoch cutoff, and any duration, fade or peak computed over it.
- **Alert and broker fields:** `rb`, `drb`, `sgscore*`, `distpsnr*`, `classtar`, and every broker classifier output (ALeRCE probabilities; Fink `d:*` scores such as `rf_snia_vs_nonia` and `snn_*`). The only allowed alert field beyond photometry is `distnr`, which Fink's SLSN feature set uses.
- **Pretrained weights:** any pretrained weight trained on BTS labels (BTSbot, Maven).
- **Coordinates:** allowed only as ALeRCE detection ra/dec (mean over detections ≤ cutoff), plus SFD E(B−V) at that position via `dustmaps.sfd`. Both depend only on position, which is known at first alert.

## 6. Channels (I2 definitions)

| id | channel | family | code source (pinned) | features |
|---|---|---|---|---|
| C1 | Fink EarlySNIa sigmoid | classical | actsnfink@f424ab1f `get_sigmoid_features_dev_fast(min_rising_points=2, min_data_points=4, rising_criteria="ewma")`; flux by fink_utils 0.77.0 `mag2fluxcal_snana`, which ignores `isdiffpos` as Fink does | 12: a,b,c,snratio,mse,nrise × g,r |
| C2 | Fink fast transient rate | classical | fink-science@591e75ce `ztf/fast_transient_rate/processor.py::fast_transient_rate` and `get_last_alert`, logic copied verbatim into `scripts/`, N=100 samples, seed 0; current alert = last g/r detection ≤ cutoff | mag_rate, sigma_rate, lower_rate, upper_rate, delta_time, from_upper. `jdstarthist_dt` is not computable (ALeRCE lacks `jdstarthist`) and is recorded missing |
| C3 | Fink SLSN feature vector | classical | fink-science@591e75ce `ztf/superluminous/slsn_classifier.py::extract_features` with its own gate (≥3 points per band, >7 total, duration > 30 d); fits run only for gate-passers | distnr, ra, dec, ebv, duration + 30 gated fit/stat columns (NaN when gated) |
| C4 | ZTF alert candidate photometry | classical (**not Fink**; added as the strongest classical arrangement, disclosed) | ZTF alert schema candidate fields | magpsf, sigmapsf, fid of last g/r detection; n detections ≤ cutoff; days since t0; galactic b from ALeRCE ra/dec |
| C5 | ParSNIP latent | deep | kboone/parsnip@dcea62f, trained per fold (see §7) | s1,s2,s3 (+errors), color (+err), luminosity (+err), reference_time_error, predicted_redshift (+err), amplitude |

- **C** is {C1..C5}, the instrument composition.
- **C−1** is {C1..C4}, the classical composition. The last channel removed is the deep one.
- **Also measured (I2):**
  - leave-one-out C−{Ci} for i = 1..4
  - C5 alone
  - per channel, the **alive fraction**: the share of cohort units where the channel emits at least one non-default value. For C1 that means not the fake-fit default [0,0,0,0.1,1e8,0] in both bands; for C3, gate passed; for C2, a finite mag_rate; for C5, a finite encoding.
- **Dead channel.** A channel whose alive fraction is 0 at an epoch, or that raises on the supplied format, is **dead** at that epoch, whatever its card says.
- **Honest count.** The honest channel count at an epoch is Σ alive fractions over channels, reported with the leave-one-out deltas beside it.

## 7. Compositions
- **Classical GBDT (C−1) and instrument GBDT (C).** sklearn 1.9.1 `HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0)`, the same settings as agent 2's `floor_prior.py`.
  - No tuning, no early-stopping change and no class weights.
  - NaN is passed natively.
  - Fit on training-fold scored-pool units, labels = posB; predict every unit in the held-out fold.
  - One model set per epoch (E1, E3).
- **Deep channel C5: ParSNIP, trained from scratch per fold.** Settings:
  - `bands=['ztfg','ztfr']` (native ParSNIP ZTF entries: MW correction on, background correction off)
  - `predict_redshift=True`, `input_redshift=False`
  - photo-z prior neutralised: meta `hostgal_photoz=0`, `hostgal_photoz_err=1e3`, `hostgal_specz=NaN` for every object, so no redshift enters input, prior or loss
  - `mwebv` = SFD E(B−V)
  - all other settings default
  - `max_epochs=60`, device cuda, `torch.manual_seed(fold)`, numpy seed fold
- **ParSNIP training set.** Training-fold units (labelled and unlabelled alike; the VAE uses no label), each included twice, truncated at E1 and at E3. Held-out units are predicted with `predict_dataset(augment=False)` at each epoch separately. Flux uses ParSNIP zeropoint 25 AB, `flux = s·10^(−0.4(magpsf−25))`, with s = −1 when `isdiffpos` is negative. ParSNIP's `parse_ztf` drops zero flux.
- **ParSNIP rejected inputs.** An object whose light curve ParSNIP rejects at an epoch gets NaN C5 features. It is counted and not repaired.
- **Pretrained ParSNIP checkpoints are not mounted.** `plasticc.pt`, `plasticc_photoz.pt` and `ps1.pt` hold LSST/PS1 band weights. Using them on ZTF g/r needs a band substitution that no code path defines. I4 refusal: they stay **UNDEMONSTRATED** on ZTF, not converted.
- **ATAT: not built.** The only weights are the ELAsTiCC 6-band LSST checkpoint (10 GB, unpinned, wave-1 card). The ATAT repo has no ZTF dataset entry, and the ZTF ATAT path in alercebroker/pipeline ships no weights. ATAT's LC branch needs no redshift, so it is feasible without redshift **only** by training from scratch. That was not chosen; ParSNIP is the declared deep channel. ATAT on ZTF stays **UNDEMONSTRATED**.
- **Blinding and I1 discipline.** The order is fixed:
  1. features
  2. models fit, with labels used only in `fit`
  3. OOF prediction files written
  4. model files and prediction files hashed into `compositions/MANIFEST.sha256`
  5. only after that, `score.py` runs
- **Score gate.** `score.py` refuses to run if the manifest is missing, or if any hashed file changed.

## 8. Resolution calibration (not P7)
- **Inputs.** `paired_scores.csv` columns: item_id, item_type (N/R), epoch (E1/E3), n, n_pos, chance_measured, k_eff, k_binding, prec_classical, prec_instrument.
- **power.py runs.** `fm-advantage-benchmark/scripts/power.py` runs unchanged with `--k 8 --candidates-per-item 46.41 --delta 0.018`:
  - **primary calibration:** E1 × item N, with `--stratum k_binding`
  - also E3 × N, E1 × R and E3 × R
- **Labelling.** The output is labelled PRE-I1 CALIBRATION and never used as a P7 record.
- **No claim rests on this cohort (addition B).** No directional claim is made at any MDE.

## 9. Caps
- **ALeRCE fetch:** at most 4,000 calls, 4 concurrent, 3 retries with backoff, 30 s timeout. A unit whose fetch fails is recorded unprocessable and never re-pulled from another broker.
- **ParSNIP:** at most 3 GPU hours total across 5 folds. If the cap is hit, C5 and C are UNDEMONSTRATED for the unfinished folds (no partial scoring of C).
- **CPU features:** at most 4 h wall clock.
- **Dispositions.** PASS or FAIL per criterion, or UNDEMONSTRATED. An interrupted run is UNDEMONSTRATED, never zero.

## 10. Tuning-set rule
- **Nothing may change after this hash** in §1–§9. A change is an amendment with cause recorded in the report, and the affected outputs re-run.
- **Unprocessable units are documented, not repaired.**
- **Low results are reported as low.**
