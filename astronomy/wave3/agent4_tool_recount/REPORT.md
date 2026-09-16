# Wave 3 · Agent 4: tool coverage recount after the band hash, and power calibration at δ 0.05

> Agent 4 returned this report as text, because the harness blocks subagents from writing REPORT.md. The coordinator saved it here without changing its substance. `code/` (842 MB) and `data_cache/` (465 MB) are gitignored; weight hashes are in `WEIGHTS_SHA256SUMS`.

## Headline
- **P4 precondition (b) clears.** All 25 tools have a disposition from logged runs or prechecks, and every run is timestamped after the band hash.
  - Band hash: 2026-09-16T18:51:26.922781Z.
  - Protocol frozen: 20:52:25Z.
  - Runs: 20:55:49Z to 21:28:04Z.
- **Recount on real Rubin cohort alerts: 2 PASS, 14 FAIL, 9 UNDEMONSTRATED.**

  | Group | PASS | FAIL | UNDEMONSTRATED |
  |---|---|---|---|
  | FM/deep (15) | 1 (CATS, 5/10) | 9 | 5 |
  | Classical (10) | 1 (GHOST, 3/8 valid) | 5 | 4 |

- **No run used actual lsst v11_1 Avro packets.** Fink `/api/v1/sources` with `output-format=avro` returns HTTP 400: "Output format `avro` is not supported. Choose among json, csv, votable, or parquet".
  - Every run instead used Fink LSST API JSON rows carrying v11_1 field names, with values unchanged.
  - Both PASS counts carry this qualifier.
- **Band reading for P4: ESCALATE** (stated here, not ruled).
  - Not PROCEED: CATS passes, but both of its Rubin classical counterparts (Fink EarlySNIa RF, Fink SLSN RF) return code defaults on every alert.
  - Not CLOSE: CATS does accept v11_1 inputs.
- **Power (calibration only).** On the primary reading (61 k-binding nights, first alert), MDE is 0.032.
  - δ 0.05: RESOLVABLE, N_min 26.
  - δ 0.018: CLOSE_UNRESOLVABLE, N_min 196.
  - Pooled night runs stay refused under refusal 4. Wave-2 files are untouched.

## Order of operations (UTC, hashed; `order_of_operations.log`)

| Step | Time | What |
|---|---|---|
| 0 | 20:47:57 | brief hash verified (`a618d911…c4b6`); band-hash time taken from agent 1's log |
| 1 | 20:48:29 | `power_calibration_delta005.json` (no tool involved) |
| 2a | 20:48:42 | endpoint discovery probes (roots, docs, schema; no object query) |
| 3 | 20:52:25 | `recount_protocol_FROZEN.md` frozen, `f32cf288…52e6` |
| 4a–4b | 20:52:42–20:52:58 | alert ids sampled and sealed, v1 `0c2f2e03…` |
| 4c–4d | 20:53:18–20:53:26 | AM1 recorded; ids re-sealed as v2 `94c01ce1…50aa` before any fetch or run |
| 5a–5b | 20:53:40–20:53:57 | alert content fetched (`r:` columns only, via safe_fetch); Avro attempt returned 400 |
| 6–17 | 20:54–21:28 | installs and runs; first alert run at 20:58:43 |
| 18 | 21:38:51 | GHOST self-written tables deleted under rule D; only a listing kept |
| 19 | 21:40:57 | deliverables hashed |

## Alert sample (rule C)
- **Selection rule.**
  - Query ALeRCE LSST `list_objects` for first detections in [T0, T0 + 0.02 d), with T0 = MJD 61222.000428.
  - Sort by (firstmjd, oid).
  - Take the first 10 ids that Fink returns.
  - The first two windows were empty (HTTP 200, "Empty query"), so the declared window extension applied.
- **Label stripping.** class_name, classifier_name, classifier_version, probability and ranking were stripped before anything else read the rows.
- **Result.** 10 distinct diaObjectIds, each with 1–3 diaSources, all within about 1° of RA 223.6, Dec −40.0.
- **AM1.** ALeRCE returns one row per classifier, so v1 held only 8 distinct objects. Deduplication on oid was recorded and v2 sealed before any fetch or run. v1 is kept read-only.

## Dispositions (counterparts reflect the ratified Fink remapping)

| Tool | Group | Disposition | Stage / error / reason |
|---|---|---|---|
| CATS (Fink) | FM/deep | **PASS 5/10** | non-default output on exactly the 5 alerts with ≥2 diaSources; below 2 points the code default applies |
| ORACLE | FM/deep | FAIL | parse: `KeyError 'FLUXCAL'` (loads only with pinned TF/keras 2.15) |
| SuperNNova (Fink) | FM/deep | FAIL | parse (feature assembly): `KeyError ['MWEBV']`. Model cli_args need MWEBV and band `Y`; the Fink Rubin wrapper supplies neither |
| RAPID | FM/deep | FAIL | parse: its validator asserts a 10-field light-curve tuple; v11_1 supplies 7 (no photflag, redshift or mwebv) |
| BTSbot | FM/deep | FAIL | parse: `KeyError` on sgscore1, distpsnr1, … (ZTF metadata) |
| Maven | FM/deep | FAIL | parse: loader requires `ZTFBTS_TransientTable.csv` (A_V, redshift) |
| Astromer1 | FM/deep | FAIL | parse: `load_numpy` rejects the v11_1 array |
| Astromer2 | FM/deep | FAIL | parse: `load_numpy` expects float (None, 3) |
| AstroM3 | FM/deep | FAIL | parse: `process_photometry` ValueError |
| ParSNIP | FM/deep | FAIL | parse: "Couldn't find required key 'time'" (plasticc and plasticc_photoz) |
| ATAT | FM/deep | UNDEMONSTRATED | 10 GB checkpoint, over the 1 GB cap and unpinned |
| AstroCLIP | FM/deep | UNDEMONSTRATED | 1,680,929,841-byte checkpoint, over the cap |
| SCONE, AppleCiDEr, MultibandAstromer | FM/deep | UNDEMONSTRATED | no weights (rechecked at the pinned repos and on HF) |
| GHOST | classical | **PASS 3/8** | host association from ra/dec; 2 runs voided (AM2) |
| Fink EarlySNIa RF (Rubin) | classical | FAIL | emit: default −1.0 on 10/10 (every alert has fewer than 7 points) |
| Fink SLSN RF (Rubin) | classical | FAIL | emit: default 0 on 10/10 |
| SALT3 (sncosmo) | classical | FAIL | parse: "no alias found for 'time'" |
| ALeRCE BHRF 1.1.1 | classical | FAIL | parse: "Missing features" (needs the ZTF feature vector); all 5 pickles hash-match wave 1 |
| Superphot+ | classical | FAIL | parse: snapi Photometry needs a time/phase/mjd column |
| Superphot | classical | UNDEMONSTRATED | no trained classifier released |
| Sherlock | classical | UNDEMONSTRATED | catalogue DB not provisioned |
| Blast | classical | UNDEMONSTRATED | service stack; public API is GET/HEAD/OPTIONS only (POST returns 405) |
| SNANA | classical | UNDEMONSTRATED | model libraries absent (SNDATA_ROOT unset) |

**Common to every FAIL:**
- The tool loaded, with weights hash-matched to the inventory pin wherever a pin exists.
- No format conversion was supplied. The protocol forbids nJy→FLUXCAL conversion, band renames and added fields.
- Rule D: 160 alert runs logged, against a cap of 250.

## Amendments and process errors (listed, not hidden)
- **AM1:** duplicate oids in the sample; fixed before any run.
- **AM2: GHOST provisioning.** The copied tree lacked `Star_Galaxy_…PS1ClassLabels.sav`, which wave 1 had pruned after hashing.
  - The amendment was recorded before the rerun.
  - The file was re-fetched at the pinned commit and its hash matches (`48f78c9c…`).
  - The 2 failed runs stay in the log, marked voided. The remaining 8 alerts were run.
  - A third run was killed mid-run and never logged.
- **Stage reclassification.** The generic stage mapper labelled the RAPID, Astromer1, Astromer2 and SuperNNova failures as "infer". Their tracebacks show the failure is in the tool's own input handling, so the axis records them as parse. The log keeps the original labels, and each record lists the reclassification.
- **Superseded load attempts, kept in the log:**
  - ORACLE: a missing dependency, then keras 3 incompatibility.
  - ParSNIP: a missing dependency.
  - ALeRCE BHRF: `{}` was passed as the taxonomy, which was operator misuse; the retry used the default.
  - Astromer1: the README load path fails.
  - Superphot+: the `.pt` file is a pickle of a LightGBM model.
- **Environment drift.** Fink tools ran with numpy 1.26.4 and astropy 5.3.4, and later installs changed both; the pip freeze is saved. Tools with conflicting pins got separate Python 3.10 venvs (keras2, ghost, sp).

## Power calibration at δ 0.05 (PI ruling 2)
File `power_calibration_delta005.json`, sha256 `0258c82e…fa2`, validate PASS. Inputs are the 4 wave-2 paired score files (hashed).

| Run | MDE | δ 0.05 ruling (N_min) | δ 0.018 ruling (N_min) |
|---|---|---|---|
| **First alert, k-binding nights (n=61), primary** | 0.032 | RESOLVABLE (26) | CLOSE_UNRESOLVABLE (196) |
| Night 3, k-binding nights (n=61) | 0.030 | RESOLVABLE (23) | CLOSE_UNRESOLVABLE (171) |
| First alert, 46-candidate rounds (n=55) | 0.055 | CLOSE_UNRESOLVABLE (67) | CLOSE_UNRESOLVABLE (515) |
| Night 3, 46-candidate rounds (n=55) | 0.063 | CLOSE_UNRESOLVABLE (87) | CLOSE_UNRESOLVABLE (665) |

- **Pooled night runs:** MDE 0.003, RESOLVABLE, refused under refusal 4. 518 of 579 nights have ≤8 candidates, so their paired difference is exactly 0 by construction.
- **Status:** calibration only.
  - No claim, because BTS failed contamination (rule B).
  - The compositions stay PRE-I1 (ruling 3).

## Disagreements (listed, not reconciled; details in the tool cards)
1. **AstroM3.** Wave 1 recorded "no weights"; weights are now public on HF (AstroMLCore, revision `8904ed33`).
2. **Fink Rubin flux units.** The SuperNNova wrapper converts nJy to FLUXCAL, but EarlySNIa RF passes nJy unconverted to an ELAsTiCC-trained model, a factor of about 36. Its docstring calls the fluxes "Magnitude".
3. **SuperNNova requirements.**
   - It needs MWEBV and band `Y`, while Rubin supplies `y`.
   - Fink's `install_python_deps.sh` calls a `requirements.txt` that does not exist at the pin, so the supernnova version is unpinned.
4. **CATS pin.** The wave-1 inventory pinned the `.keras` file, but the code loads the savedmodel.
5. **Astromer1 loading.**
   - `from_pretraining` lacks `@classmethod`.
   - The README's `'macho'` weights return 404, and the downloaded HTML then fails as a zip.
   - The zip unpacks to `macho/`, not `macho_a0/`.
6. **Superphot+ artifacts.**
   - The `.pt` file is a pickle of SuperphotLightGBM.
   - The snapi git dependency is unpinned and resolved to `4a419fe0`.
7. **Maven.** The inference loader reads the BTS transient table (a rule-C exposure note). The code sets the ZTF-g effective wavelength to 1196.25 Å.
8. **RAPID.** Its unknown-redshift model still requires a redshift field in the tuple.
9. **ORACLE.** The README says the repo is unmaintained and points to a PyTorch rewrite, but wave 1 inventoried the old repo.
10. **BTSbot.** It downloads HF `main` without a revision; the served bin still matches the pin.
11. **Sample geography.** All 10 sealed alerts fall in one field at dec −40, because the sampling rule takes the earliest objects in time. GHOST's "PS1 dec > −30" note in the wave-1 inventory disagrees with its 3 host returns. The source catalogue was not inspected, because outputs are discarded under rule D.
12. **The pass criterion measures the stream as much as the tools.** Rubin has been off sky since mid-July, so cohort objects have 1–3 diaSources. That alone guarantees the Fink RF FAILs at emit.

## Still UNDEMONSTRATED

| Item | Blocks |
|---|---|
| runs on actual lsst v11_1 Avro packets (not served publicly) | an unqualified "verified on v11_1"; I5 on Rubin |
| ATAT and AstroCLIP (over the cap); SCONE, AppleCiDEr, MultibandAstromer and Superphot (no weights); Sherlock, Blast and SNANA (external infrastructure) | coverage for those channels; I4/I5 |
| I4 construct validity for CATS and GHOST (outputs are not the scored quantity) | any PROCEED on tool coverage; R4 grant |
| a passing classical Rubin counterpart for CATS | band PROCEED |
| cutouts and forced photometry (not fetched, per protocol) | BTSbot-style image channels |
| R1 run and PI ratification of I1 | wave-2 compositions as I1 records |

## Replay cases (`replay_cases.csv`, `replay_rulings.csv`)
- **AST4W3-01** (P3, must_fire): "2 of 25 verified on v11_1" written without the format qualifier, plus PROCEED.
- **AST4W3-02** (P3, must_not_fire): FAIL at emit on short light curves, with the threshold and the sealed sample kept.
- **AST4W3-03** (I5, must_fire): deleting failed run lines and rerunning beyond the cap.
- **AST4W3-04** (P7, must_fire): reporting the pooled MDE of 0.003 at both deltas.

## Deliverables
- **Protocol and seals:**
  - `recount_protocol_FROZEN.md` + `.sha256`
  - `amendments.md`
  - `sealed/alert_ids_SEALED.json` (v1) and `_v2.json`
- **Logs and records:**
  - `run_log.jsonl` (196 lines)
  - `order_of_operations.log`
  - `seed_ledger.json`
  - `validate_stdout.txt`
- **Axis and calibration:**
  - `tool_coverage_axis.json` (validate PASS; supersedes wave-1 `5ec00e9a…`)
  - `power_calibration_delta005.json`
- **Tool cards and hashes:**
  - `tool_cards/` (13 updated or new, all PASS)
  - `WEIGHTS_SHA256SUMS` (39)
  - `sources/`
- **Scripts:** `scripts/`
- **Replay:** `replay_cases.csv`, `replay_rulings.csv`
