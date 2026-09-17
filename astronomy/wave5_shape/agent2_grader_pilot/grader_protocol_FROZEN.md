# Grader protocol, generate / inverse problem: FROZEN

PRE-RATIFICATION PILOT (harness check only). No score record, no directional claim, not an I1 record.

- Author: wave-5 agent 2 (grader, harness, pilot). Frozen 2026-09-17. The sha256 of this file is in `grader_protocol_FROZEN.sha256`; `grade.py`, the R1 script and the pilot scripts re-check it and abort on mismatch.
- Brief: `astronomy/wave5_shape/PANEL_BRIEF_WAVE5.md`, sha256 `cd10a41c905a4914291b9976df7f3241960494e312f11e4f32171bfecd5e4c6b`, matches `BRIEF_SHA256` (verified before this file was written). Constraints 2 and 3 of the brief bind: staged pilot after a synthetic R1; subject arms are Claude subagents with shell access, so separation is instructed and audited, not enforced.
- Governing text: `fm-advantage-benchmark-with-shape/references/shape.md` (generate rows; downstream table I1 and A3; gate 2), `references/stages/instrument.md` (I3, I4, I5), `references/stages/runtime.md` (R1, R4, R6, R8), SKILL.md global refusal 6.

## 0. What was seen before freezing (disclosure)
- Read: the brief, `SHAPE_REEVALUATION.md` §1–§6, `shape.md`, `instrument.md`, `runtime.md`; wave-1 agent 4 REPORT and SALT3 card; wave-2 agent 4 REPORT, `compositions_FROZEN.md`, `r1_spec.md`, ParSNIP card, `scripts/{fetch_alerce,common,features,parsnip_fold}.py`, fold training logs (n_train_units only); wave-3 agent 4 REPORT; manifest v3 `decision_epoch` slot (`astronomy/wave4/agent3_freeze_v3/domain_manifest_v3.json`, sha256 `0bdf229e9e57ea1699bfd2b70eecbbd0ce58a27895f14f62af87320833e63b6c`).
- Code read: ParSNIP `sncosmo.py` (`ParsnipSncosmoSource`), `parsnip.py` (`predict_sncosmo`, `decode_spectra`), `light_curve.py` (`preprocess_light_curve`) at kboone/parsnip@dcea62f.
- Probes (no object data): SALT3 from the pinned directory evaluates in ztfg/ztfr and returns 0 flux outside its time range; `parsnip_fold0.pt` loads on CPU with bands [ztfg, ztfr], latent size 3, and exposes sncosmo parameters (z, t0, amplitude, color, s1, s2, s3).
- Literature fetched for I3: Bazin et al. 2009 arXiv:0904.1066 (pdf sha256 `8ad38cfc64fce32a92792f4288ae0d95ad622db3c093977900ef94317bb09635`), Villar et al. 2019 arXiv:1905.07422 (pdf sha256 `9288e1ac9185e6d53738fe0ee9ddfffd0d77481d67033298c0cefeffd9418305`); equation and parameter table read.
- BTS CSV: header line only. No row, type, redshift or photometry of any object was read. No object was selected.

## 1. Cut epoch (new declaration, with cause)
- **Photometry source.** ALeRCE ZTF API `https://api.alerce.online/ztf/v1/objects/{oid}/lightcurve`. Rows with `fid` in {1, 2} only (1 → `ztfg`, 2 → `ztfr`); detections de-duplicated on `candid`; non-detections de-duplicated on (mjd, fid).
- **Flux convention.** ZP 25, AB: `flux = s · 10^(−0.4 (magpsf − 25))`, `fluxerr = 0.921034 · |flux| · sigmapsf`, `s = +1` if `isdiffpos` in {1, 't', 'True', '1.0'} else −1. This is the wave-2 ParSNIP convention (`features.py::parsnip_lc`). `magpsf` (difference-image PSF magnitude), never `magpsf_corr`.
- **First detection** `t_first` = min mjd over positive g/r detections (identical to manifest v3 `t0`).
- **Cut** `t_cut = t_first + 10.0 d`.
- **Cause.** Manifest v3 ratified two decision epochs, E1 "first alert" and E3 "night 3", for the infer follow-up decision. Under generate / inverse problem the governed action is proposing a model family and its parameters. E1 carries one detection and E3 typically 1–4 across both bands, fewer points than the parameters of any admissible family (SALT3 5, Bazin 10, Villar 14, ParSNIP 7), so neither epoch admits a fit. shape.md refusal 6 requires re-registration when the root changes, so the infer epochs do not carry over by default. `t_first + 10 d` gives about 3–5 points per band at ZTF public cadence and, for a transient found on the rise, sits before peak, so the held-out window tests extrapolation through peak and decline. **This epoch is a proposal for PI ratification, not an override of the ratified slot.**
- **Pre-cut set (given to arms).** g/r detections with `t_first − 30 ≤ mjd ≤ t_cut`, and g/r non-detections (`diffmaglim`, 5σ limiting magnitude) with `t_first − 30 ≤ mjd ≤ t_cut`.

## 2. Held-out set (grader only)
- All g/r detections (either sign) with `t_cut < mjd ≤ t_first + 60.0 d` (horizon).
- Non-detections are not scored.
- **Minimum count.** A band is scored only if it holds ≥ 5 held-out detections. A band below 5 is excluded and recorded. An item with no scored band is unscoreable (item-level coverage, never an arm failure).

## 3. Score
For held-out detection i in band b with observed flux `f_i`, error `σ_i`, and forward-model prediction `m_i` at (mjd_i, b):
- **Error floor:** `σ_eff,i = max(σ_i, 0.05 · |f_i|)`.
- **Residual:** `r_i = (f_i − m_i) / σ_eff,i`.
- **Per-band score:** `χ²_b = (1/N_b) Σ_i r_i²` over scored bands.
- **Item raw score:** `S = mean_b χ²_b` (bands weighted equally). Lower is better.
- **Bounded transform:** `Q = 1 / (1 + S)`, in (0, 1], higher is better. Paired comparisons across items, if any are ever made, use Q, so one catastrophic extrapolation cannot dominate a mean. For an exact model with Gaussian errors, S ≈ 1 or below (the floor only inflates errors), so Q ≈ 0.5 or above.
- **Near-ideal reference (used by R1 only):** a band is near-ideal when `χ²_b ≤ χ²_{0.995}(N_b) / N_b`.
- **Diagnostics, never scored:** median |r| per band, N_b, the pre-cut χ² of the same submission under the same formula.
- **Forward-model convention.** The prediction is whatever the pinned forward model returns at the submitted parameters. For SALT3 that includes 0 flux outside the model's time range (−20 to +50 rest-frame days); no special handling.

## 4. Submission schema and coverage
A submission is one JSON object:
```
{"item_id": str,
 "family": "SALT3" | "Bazin" | "Villar" | "ParSNIP",
 "parameters": {...},
 "rejected_rivals": [{"family": str, "reason": str}, ...],
 "notes": str (optional)}
```
Parameters by family (no other keys allowed; every value a finite number):
- **SALT3:** `z, t0, x0, x1, c`. Domain: `0 < z ≤ 1.5`.
- **ParSNIP:** `z, t0, amplitude, color, s1, s2, s3`. Domain: `0 ≤ z ≤ 4`.
- **Bazin:** `{"ztfg": {A, t0, tau_rise, tau_fall, B}, "ztfr": {...}}`, both bands required. Domain: `tau_rise > 0, tau_fall > 0`.
- **Villar:** `{"ztfg": {A, beta, t0, gamma, tau_rise, tau_fall, B}, "ztfr": {...}}`, both bands required. Domain: `tau_rise > 0, tau_fall > 0, gamma ≥ 0`.
- `t0` in MJD for every family. Fluxes are at ZP 25 AB.
- Milky Way extinction is **not** a submitted parameter. For SALT3 and ParSNIP the grader applies `sncosmo.F99Dust(r_v=3.1)` in the observer frame at `mwebv` from the item's `item_meta.json` (SFD E(B−V) at the object position). Parametric families carry no dust term.
- `rejected_rivals`: at least one entry; each `family` in the allowed set and different from the chosen family; `reason` a non-empty string ≤ 4000 characters. Reasons are recorded, never scored.

**Coverage rules (global refusal 6: an unparsed answer is a coverage failure, never a zero).**

| Code | Fires when | Recorded as |
|---|---|---|
| `COVERAGE_FAIL:MISSING` | no file at the declared output path | coverage failure, no score |
| `COVERAGE_FAIL:PARSE` | file is not valid JSON or not an object | coverage failure, no score |
| `COVERAGE_FAIL:SCHEMA` | family not allowed, a required key missing, an unknown key present, a non-finite or non-numeric value, `rejected_rivals` invalid, `item_id` mismatch | coverage failure, no score |
| `COVERAGE_FAIL:DOMAIN` | a parameter outside its declared domain | coverage failure, no score |
| `COVERAGE_FAIL:EVAL` | the forward model returns a non-finite prediction at any held-out point | coverage failure, no score |
| `GRADER_ERROR` | an exception inside the grader on a schema-valid submission | instrument failure; work returns to the instrument, the arm is not charged |
| `SCORED` | otherwise | S, Q, per-band χ², N_b |

Coverage is always reported beside scores and never dropped.

## 5. Grader instances (frozen, separately pinned)
- **G-SALT3.** sncosmo 2.13.1, `sncosmo.SALT3Source(modeldir=<grader pinned copy>)` of salt3-f22 (tarball sha256 `c7de53438761aeaacb5b28347fb0e9b00b5f5b1036843688e3d5d5edd4f7a37e`; the seven extracted files are hash-checked at every load), wrapped in `sncosmo.Model` with the MW dust effect of §4. Band fluxes via `Model.bandflux(band, mjd, zp=25, zpsys='ab')`, bands `ztfg`, `ztfr` (sncosmo built-ins).
- **G-PARAM.** Pure numpy, written for this protocol:
  - Bazin: `F(t) = A · exp(−(t − t0)/tau_fall) / (1 + exp(−(t − t0)/tau_rise)) + B`.
  - Villar: with `t1 = t0 + gamma`, `D(t) = 1 + exp(−(t − t0)/tau_rise)`; `F = (A + beta (t − t0)) / D` for `t < t1`; `F = (A + beta · gamma) · exp(−(t − t1)/tau_fall) / D` for `t ≥ t1`; plus `B`.
  - Exponent arguments are clipped to [−700, 700] before `exp` to avoid overflow; this clip is part of the frozen definition.
- **G-ParSNIP.** kboone/parsnip@dcea62f (grader copy of `parsnip/`), `parsnip_fold0.pt` sha256 `283381682be5d5212e5502256549cc153450168bc9f9c66d4e36aa03e2bdd705` (wave-2 fold 0), loaded on CPU, wrapped as `sncosmo.Model(source=ParsnipSncosmoSource(model))` with the MW dust effect of §4.
- **Separation.** The grader loads SALT3 and ParSNIP files from `data_cache/grader_pinned/`, a copy distinct from the arms' `data_cache/arm_assets/` copy; both copies are hashed and must hash-match the pins. The forward-model code the grader runs lives in `grader_private/forward_models.py`; the arm tools carry their own copy, and both hashes are recorded. The grader evaluates only the submitted family and parameters. **Arms submit parameters, never fluxes**; a flux array anywhere in a submission is an unknown key and fails schema.

## 6. Grader-separation design
- `item/` holds `pre_cut.csv` and `item_meta.json` (item id, `t_first`, `t_cut`, horizon, bands, flux convention, `mwebv`). No ZTFID, IAU name or coordinates are given to arms (identity recall is contamination bait).
- `grader_private/` holds `held_out.csv`, `forward_models.py`, and the object identity. Arms are told not to read it, nor `grade.py`, nor anything under `astronomy/` other than the explicitly allowed paths in their prompt, nor the BTS CSV, nor the web.
- Enforcement is procedural (brief constraint 3): subagents with shell access can read any path. Audit: the coordinator inspects arm transcripts for any access to forbidden paths; any access voids that arm's submission for the pilot (recorded, not scored).
- Hashes of `item/pre_cut.csv`, `item/item_meta.json` and `grader_private/held_out.csv` are written before any arm runs.

## 7. Admissible submission families
SALT3, Bazin, Villar, ParSNIP (latent). Both arms may submit any of the four; the arms differ only in tools (R8 table).
- **ParSNIP model: wave-2 `parsnip_fold0.pt`.** Chosen as the lowest-index fold with a normal training loss; fold 4 is excluded (loss plateau near 247 vs about 6, wave-2 disagreement 5).
- **Training set of fold 0:** the wave-2 cohort units with `int(sha256("w2a4-fold|" + cluster_id)[:8], 16) % 5 != 0` (2,724 units), cohort = BTS rows with peak in [2019-06-01, 2021-04-15), light curves truncated at E1 and E3.
- **Pilot constraint:** the pilot object's ZTFID must not appear in `astronomy/wave2/agent4_instrument/data_cache/cohort_rows.csv` at all (a stronger condition than "not in fold 0 training": it excludes all folds). Checked by ZTFID only; ALeRCE associates detections within 1.5″ to one ZTFID, so another cohort ZTFID cannot carry this object's photometry.
- **Disclosed weakness, fixed now:** every fold-0 training light curve was truncated at E1 or E3, i.e. no later than night `n0 + 3`. The decoder has essentially no training support at the held-out phases (`t_first + 10` to `+60`). A ParSNIP submission is graded as the decoder predicts; no correction is made.

## 8. R1 on a synthetic item (spec; dispositions in `r1/dispositions_PRE_RUN.md`, written before the run)
- **Seed.** `seed = int(sha256(grader_protocol_FROZEN.md)[:8], 16)`. Control items use `seed + 1` (SALT3 control item), `seed + 2` (Villar control item), `seed + 3` (ParSNIP control item).
- **Simulator.** SALT3 (arm-asset copy, not the grader copy) at z = 0.05, t0(peak) = 59800.0, x0 = 1.2e-3, x1 = 0.5, c = 0.05, mwebv = 0.03 (F99). ZTF-like cadence: per band, a visit every 3.0 d from peak − 30 to peak + 70, jitter U(−0.3, 0.3) d, g and r offset by 0.02 d, each visit dropped with probability 0.2. Noise: `σ = sqrt(σ_lim² + (0.02 · f_true)² )` with `σ_lim = 10^(−0.4 (20.5 − 25)) / 5` (5σ limit 20.5 mag); observed flux `f_true + N(0, σ)`. A visit with `f_obs / σ ≥ 5` is a positive detection (magpsf from |flux|); otherwise a non-detection with `diffmaglim = 20.5`. The simulated rows pass through the same item builder as the real pilot.
- **Stub composition.** (a) TRUE parameters, family SALT3. (b) Wrong family: a Bazin fit to the pre-cut detections by the floor's Bazin generator (§9).
- **PASS** iff (a) is SCORED and every scored band is near-ideal (§3), and (b) is SCORED with `S_b > S_a`. **FAIL** otherwise, while the grader ran. **UNDEMONSTRATED** if the item is unscoreable or the run is interrupted. FAIL sends work back to the instrument, never to the subject.

## 9. Mechanical floor (I1 row for generate: run the generator at defaults, keep the best on one metric)
- **Generator 1, SALT3.** `sncosmo.fit_lc(data, model, ['z','t0','x0','x1','c'], bounds={'z': (0.005, 0.3)})` with all other arguments default (`guess_amplitude`, `guess_t0`, `guess_z` True, `minsnr=5.0`, `modelcov=False`), model = arm-asset SALT3 with MW dust fixed at item `mwebv`. Data = pre-cut detections only. The z bound is the only non-default and is required because sncosmo refuses an unbounded z.
- **Generator 2, Bazin.** Per band, `scipy.optimize.least_squares(method='trf')` on residuals `(f − F)/fluxerr` over pre-cut detections of that band, start `[1.5·max(f), mjd_at_max(f) − 5, 3.0, 20.0, 0.0]`, bounds `A∈[0, ∞)`, `t0` free, `tau_rise∈[1e-3, 500]`, `tau_fall∈[1e-3, 500]`, `B` free. All else default.
- **Metric.** Pre-cut χ² per point under the §3 formula (same floor), computed over pre-cut detections. Keep the lower; ties go to SALT3. A generator that raises is dropped and recorded; if both raise the floor is `COVERAGE_FAIL:EVAL`.
- **Rejected rival reason** (mechanical): the other generator and its pre-cut χ² per point.
- Known property, not repaired: the metric rewards in-sample fit, so the 10-parameter Bazin wins on few points and may extrapolate badly.

## 10. Pilot selection rule (sealed separately before any photometry fetch)
Declared in `selection/selection_rule_SEALED.md`; its hash is logged before the first object fetch. Only ZTFID, `peakt` (dates), detection counts and detection dates may be read before the seal on the chosen object.

## 11. Contamination under generate
"The object is published and indexed": a published light-curve fit for this object. Checked after the seal via the arXiv API (`export.arxiv.org/api/query`, `all:` field) for the IAU name variants and the ZTFID; the query strings and hit lists are recorded. The arXiv API indexes metadata (title, abstract, comments, authors, journal ref), not full text; that limit is recorded as UNDEMONSTRATED coverage of full text.

## 12. Tuning-set rule
Nothing in §1–§11 changes after this hash. A change is an amendment with cause, logged in `order_of_operations.log` before the computation it affects, and the affected outputs re-run. Low or failing results are reported as they are.
