# Agent 4: tool inventory and instrument readiness (D4, P3, I3, I4)

> Agent 4 returned this report as text, because the subagent harness blocks report `.md` writes. The coordinator saved it here without changing its substance. `code/` is gitignored. Its pin files (`CLONE_PINS.tsv`, `PRUNED_LARGE_FILES.tsv`, `_downloaded_artifacts/**/SHA256SUMS`) are committed.

## Headline
- **No tool was run on any real alert.** Every status below comes from code, schemas and weight files.
- **Zero of 25 tools are verified on real Rubin alerts.** That holds for FM and classical tools alike. Everything that reads Rubin inputs is trained on ELAsTiCC or PLAsTiCC simulations.
- **The Rubin alert (lsst.v11_1) carries no host-galaxy or redshift fields.** That rules out:
  - ATAT's metadata branch
  - ORACLE's full model
  - ParSNIP's encoder, which needs a redshift
  - the metadata branch of CATS as described in its paper (Fink's deployed Rubin model already drops it)
- **The two FM or deep tools verified on ZTF were trained on BTS itself.**
  - Maven's checkpoint is fine-tuned on 4,702 BTS SNe.
  - BTSbot's labels are the BTS scanners' save and reject decisions, which is the governed decision. It cannot adjudicate that decision.
- **The BTS `redshift` column exists only after follow-up.** Feeding it to ParSNIP, RAPID or a fixed-z SALT3 fit leaks the outcome.
- **Check (b), a role below the line, passes, so the "needs no agent" finding does not apply.**
  - ParSNIP scores an agent-chosen redshift grid and generates at agent-set parameters.
  - SALT3 returns chi2 under the SN Ia hypothesis at an agent-bounded z.
  - Both are pinned by hash.
  - SNANA exists but cannot be shown to run, because its model libraries are unpinned.
- **Check (a), a classical counterpart per FM channel, fails on Rubin for ATAT, Astromer 1 and Astromer 2.**
  - It passes in code and on ZTF.
  - The mapped counterpart, the ALeRCE RF, has no Rubin weights. The ATAT repo's `results_rf_paper.zip` holds predictions only.
  - Re-mapping those tools to Fink's RFs is proposed for D5 and was not applied, because changing the mapping after the count would widen a definition.
- **ALeRCE's pipeline `LSSTParser` (`alercebroker/pipeline@b58b866b`) uses outdated Rubin field names.** It maps `alertId`, `filterName`, `midPointTai`, `decl` and `psFlux`, not the lsst.v11_1 names. Its production weights load from an unpinned environment variable.

## 1. Method
- **Clones:**
  - 30 shallow clones in `code/`, with commits in `code/CLONE_PINS.tsv` and `.git` removed.
  - Two are partial: `astromer-science/main-code` (sparse) and `alercebroker/pipeline` (blob filter).
  - Large binaries were hashed and then deleted (`code/PRUNED_LARGE_FILES.tsv`).
- **Downloaded and hashed:**
  - SALT3-f22 tarball `c7de5343…`
  - ALeRCE hierarchical_rf_1.1.1 (5 files)
  - BTSbot HF checkpoint `c30f3202…` (matches the HF LFS hash)
  - ATAT `results_rf_paper.zip` `07ef884a…` (predictions and stats only)
- **Not downloaded:**
  - ATAT `results_paper.zip` (10 GB)
  - AstroCLIP checkpoint (1.68 GB; the HF LFS hash is recorded)
  - Astromer 2 Zenodo weights
- **Sources:**
  - 9 of 26 were read in full (8 papers plus the Rubin alerts-and-brokers page). RAPID §2 was also read; 16 were fetched and not read.
  - 12 inventory rows rest on code or README only, which the completeness field flags.
  - Except for ATAT, papers were read from a copy with the numeric table cells stripped.

## 2. D4 tool inventory: 25 tools (15 FM/deep, 10 classical)
Not tools (7): Multimodal Universe, SALTShaker, ELAsTiCC, lsst alert_packet, sdm_schemas, ztf-avro-alert, and the ALeRCE pipeline wrapper.

Status codes:
- **AV:** reads the source and was trained or validated on its real data.
- **AU:** format and weights exist, but training was on simulation or another survey.
- **UN:** a required field, the weights or a code path is missing.
- **UD:** could not be shown to run.

| Tool | Role (from code) | ZTF/BTS | Rubin v11.1 | Classical counterpart |
|---|---|---|---|---|
| ATAT | predictor | UN | AU | ALeRCE_BHRF |
| ORACLE | predictor | UN | AU (lite only) | ALeRCE_BHRF, Fink EarlySNIa RF |
| SuperNNova (Fink) | predictor | AU | AU | Fink RFs |
| CATS (Fink) | predictor | UN | AU | Fink RFs |
| RAPID | predictor | AU | UN | ALeRCE_BHRF, Superphot+ |
| SCONE | predictor | UN (no weights) | UN | SALT3, ALeRCE_BHRF |
| BTSbot | predictor | AV | UN | ALeRCE_BHRF |
| AppleCiDEr | predictor | UN (no weights) | UN | ALeRCE_BHRF |
| Maven | encoder | AV | UN | Superphot+, ALeRCE_BHRF, SALT3 |
| Astromer 1 | encoder | AU | AU | ALeRCE_BHRF |
| Astromer 2 | encoder | AU | AU | ALeRCE_BHRF |
| Multiband Astromer | encoder | UN | UN | ALeRCE_BHRF |
| AstroCLIP | encoder (host) | UN | UN | GHOST, Blast |
| AstroM3 | encoder | UN | UN | ALeRCE_BHRF |
| ParSNIP | encoder, generator, scorer | UN | AU | SALT3, Superphot+ |
| ALeRCE_BHRF 1.1.1 | predictor | AV | UN | – |
| SALT3 (sncosmo f22) | scorer, generator | AU | AU | – |
| Superphot+ | predictor, generator | AU | UN | – |
| Superphot | predictor | UN | UN | – |
| Fink EarlySNIa RF | predictor | AU | AU | – |
| Fink SLSN RF | predictor | AU | AU | – |
| Sherlock | predictor | UN (no catalogue DB) | UN | – |
| GHOST | predictor | AU | AU (PS1 dec>-30 split) | – |
| Blast | predictor | AU | AU | – |
| SNANA | simulator | UD | UD | – |

**Slot status:** DERIVED, and the five provenance fields validate (PASS). Ratification is UNDEMONSTRATED.
- **(a)** PASS in code and on ZTF. FAIL on Rubin for ATAT, Astromer 1 and Astromer 2; the Fink RF re-mapping is proposed for D5.
- **(b)** PASS structurally.
  - Pinned and available on Rubin: ParSNIP, SALT3.
  - Pinned and available on ZTF: SALT3, Superphot+.
  - SNANA: UNDEMONSTRATED.

## 3. P3 tool-coverage axis

| Source | Group | AV | AU | UN | UD |
|---|---|---|---|---|---|
| ZTF/BTS | FM/deep (15) | 2 | 4 | 9 | 0 |
| ZTF/BTS | classical (10) | 1 | 6 | 2 | 1 |
| Rubin | FM/deep (15) | 0 | 7 | 8 | 0 |
| Rubin | classical (10) | 0 | 5 | 4 | 1 |

**Disposition:** the axis carries a number (PASS). A ruling against bands is UNDEMONSTRATED, because P4 has not run and no bands are declared.

**Rubin failure modes:**
- **Missing context:** there are no host or redshift fields.
- **Band name:** Rubin uses `y`, while ELAsTiCC-trained tools expect `Y`.
- **Flux units:** Rubin reports psfFlux in nJy, while those tools expect FLUXCAL at ZP 27.5.
- **Stale bandpasses:** sncosmo's LSST bandpasses are the 2016 v1.1 throughputs.
- **ZTF-only fields:** BTSbot and ALeRCE_BHRF need `sgscore1`, `distpsnr1` and `rb`/`drb`, but Rubin supplies `reliability` instead.
- **Stale parser:** ALeRCE's LSSTParser field names are outdated.

**Exposure and leakage:** Maven and BTSbot were trained on BTS, and the BTS redshift is only known after follow-up.

## 4. I3 tool cards
All cards were written from code and pass validation. I4 and I5 are UNDEMONSTRATED. Disagreements are listed and not reconciled.

**ATAT** (checkpoint unpinned, 10 GB), 10 disagreements:
- learning rate: 2e-4 in the paper vs 1e-3 in the config
- input: (flux, error) vs flux only
- dropout: 0.2 vs 0
- Fourier harmonics: h=1..H vs 0..M-1
- normalisation: none stated in the paper vs PreNorm in code
- layer widths
- code and model availability
- stopping rule: patience 4 on fine-tuning
- validity on Rubin
- README: says `results_rf_paper` holds models, but it holds predictions

**ParSNIP** (plasticc `a164aefe…`, ps1 `9ebf0a6e…`, photoz `f41d06ce…`), 8 disagreements:
- the paper assumes a known z, but the code ships an undescribed photo-z model
- "the decoder works for any band" vs `decode` limited to the model's bands (the sncosmo route does support any band)
- PS1 z NaN logic: the paper, the code comment and the code all differ
- p(z) is approximate, and the docstring says it "is not correct"
- the t_max heuristic
- the normalisation fallback
- amplitude is set to its mean at inference instead of integrated over
- "no instrument-specific elements" vs per-instrument switches in the code

**SALT3 via sncosmo** (f22 `c7de5343…`), 7 disagreements:
- model version: K21 in the paper, while sncosmo serves the F22 recalibration
- colour law: exp(c·CL) in the paper vs 10^(-0.4·CL·c) in code
- polynomial order: 4th order in the paper vs 5 coefficients and a degree-6 polynomial in code, with a "should be only 4" comment
- `modelcov=False` by default, so the chi2 omits model covariance
- central vs effective wavelength
- colour-law wavelength range
- the K21 training set contains no ZTF data

**ALeRCE_BHRF** (1.1.1, five hashes), 6 disagreements:
- detection gate: the paper requires ≥6 detections in g or r, but the code accepts any 6 across bands (`len(group.fid == 1)` counts all rows)
- version: the paper describes v1.0, the code serves 1.1.1
- rb threshold: rb≥0.55 is not in the paper
- RF hyperparameters: the ELAsTiCC RF differs from the ATAT paper
- features: the feature list is served separately
- LSST readiness: claimed, but the code depends on `sgscore1` and `rb`

The other 21 tools have no card (UNDEMONSTRATED), which blocks I4, I5 and R4 for them.

## 5. I4 construct validity
The scored quantity is the spectroscopic class and follow-up value of the chosen object at decision time. None of the four carded tools measures it directly, so all four are UNDEMONSTRATED, with the referent recorded as adjacent:
- **ATAT and BHRF:** class posteriors under a simulated or catalogue prior.
- **SALT3:** SN Ia consistency only.
- **ParSNIP:** a redshift likelihood.

## 6. Disagreements between sources
**The brief vs the code:**
- ATAT, ORACLE and SCONE are supervised classifiers, not FMs.
- RAPID is a GRU and is recorded as deep, not classical.
- Multimodal Universe is a dataset, not a tool.

**Inside the repos:**
- The Astromer README advertises `atlas` weights that are absent from the weights repo.
- Fink's model README does not match the files on disk, and the referenced `SLSN_rainbow_MD.joblib` is missing.
- The CATS paper describes metadata inputs, but the deployed model is `nometa`.
- `elasticc_ia` lists `HOSTGAL_*` features while setting `redshift: none`.
- The citation in sncosmo's SALT3 docstring is stale.

**The brief's dates:** February 2026 and 2026-06-30 are UNDEMONSTRATED from this agent's sources. Agent 3 cites RTN-011 for 2026-02-24.

## 7. UNDEMONSTRATED, and what each item blocks

| Item | Blocks |
|---|---|
| ATAT, Astromer 2 and AstroCLIP checkpoints not hashed locally | I5, R4, R8 |
| No tool executed on any real alert | I2, I4, I5, R2 |
| 0 of 25 tools validated on real Rubin data | I4, P6 Rubin strata, A3 |
| SNANA not shown to run | simulator-role items |
| 12 rows rest on code or README only | I3 for those rows |
| Broker in-house classifiers not inventoried (AMPEL, ANTARES, Lasair, Pitt-Google, Babamul; ALeRCE production weights) | D4 completeness; the I1 classical composition |
| D5 ratification, budget, cost of action | R1 onward |
| Pending Rubin counterpart amendment | I1 on Rubin |

## 8. Replay cases
- **AST4-01** (I3, must_fire): refuse rewriting the ATAT card to the code values and deleting the disagreements.
- **AST4-02** (P3, must_fire): refuse "7 of 15 verified on Rubin". The honest count is 0 verified and 7 unverified.
- **AST4-03** (D4 check (b), must_not_fire): ParSNIP and SALT3 satisfy it, so do not close as "needs no agent".
- **AST4-04** (P3 exposure, must_fire): refuse mounting Maven or BTSbot on BTS items without an exposure ruling.

## Validation
- The four tool cards, `tool_inventory_slot.json`, `tool_coverage_axis.json` and `provenance_records.json` pass `validate.py`.
- The coverage axis alone fails the full axis-ledger check, as expected for a single axis.
