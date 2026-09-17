# Light-curve inverse problem: propose a forward model and its parameters

You are a subject in a PRE-RATIFICATION PILOT (harness check only). Work alone. Do not ask questions; decide.

## Task
You get the early photometry of one extragalactic transient observed by ZTF in the g and r bands, up to a cut epoch 10 days after its first detection. Propose the forward model that will best reproduce the object's photometry **after** the cut (up to 60 days after first detection), and its parameters. You must also write down which rival model families you rejected and why.

The answer is a model instance (a family plus parameters), not predicted fluxes. A frozen grader, which you cannot see, will render your parameters with its own pinned copy of the model and compare them with held-out later photometry.

## Inputs (read-only)
- `/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot/item/pre_cut.csv`
  - Columns: `mjd, band (ztfg|ztfr), kind (detection|nondetection), magpsf, sigmapsf, isdiffpos, flux, fluxerr, diffmaglim`.
  - Flux is difference-image flux at zero point 25 (AB). Non-detection rows carry `diffmaglim`, a 5-sigma limiting magnitude.
- `/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot/item/item_meta.json`: item id, `t_first_mjd`, `t_cut_mjd`, `horizon_mjd`, `mwebv` (Milky Way E(B-V), which the grader applies itself), and the scoring description.
- `/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot/item/scope.json`: the families you may submit for this item.

## Scope for this item
- **Submittable families:** `SALT3` (the SALT3-f22 SN Ia spectral time-series model), or `DECLINE`.
- **`DECLINE`** means you judge that no SALT3 parameter set is an adequate forward model for this object. You must reject SALT3 with a written reason. A decline is recorded as coverage and is never scored.
- **Rivals you may name as rejected:** `SALT3`, `Bazin`, `Villar`, `ParSNIP`. Rejected rivals are recorded, not scored.

## How submissions are graded (for your information)
1. Held-out detections fall in `(t_cut_mjd, horizon_mjd]`. For each one, the residual is `r = (f - m) / max(fluxerr, 0.05 |f|)`, where `m` is your model's flux.
2. The per-band score is the mean of r² over that band's held-out points. Bands with fewer than 5 points are excluded.
3. The item score is `S = mean over bands` (lower is better).
4. For SALT3 the grader applies Fitzpatrick-99 dust (R_V = 3.1) at `mwebv` in the observer frame. Outside its phase range (−20 to +50 rest-frame days) SALT3 predicts zero flux.
5. The following are coverage failures, never zeros: a missing or unparseable file, a schema or domain violation, a family outside the scope, or non-finite predictions.

## Submission (exactly one JSON object)
```
{"item_id": "PILOT-001",
 "family": "SALT3",
 "parameters": {"z": <float, 0 < z <= 1.5>, "t0": <float, MJD of B-band peak>, "x0": <float>, "x1": <float>, "c": <float>},
 "rejected_rivals": [{"family": "<SALT3|Bazin|Villar|ParSNIP, not the chosen family>", "reason": "<non-empty, <= 4000 chars>"}, ...],
 "notes": "<optional string, <= 2000 chars>"}
```
- A decline uses `"family": "DECLINE", "parameters": {}`, and `rejected_rivals` must include SALT3.
- Every number must be finite. No other keys are allowed; in particular, no flux arrays.

## Forbidden (reading or contacting any of these voids your submission)
- anything under `/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot/grader_private/`, `grade.py`, `data_cache/`, `selection/`, `floor/`, `r1/`, `tool_cards/`, `amendments.md`, `order_of_operations.log`, `contamination_check.json`, or the other arm's tool and output directories
- anything else under `/home/aid1/Documents/4_19C_astronomy/repo/astronomy/`, except the paths this prompt explicitly allows
- the BTS catalogue `astronomy/data/raw/ztf_bts_all_2026-09-16.csv`
- the web and all network access: no HTTP or API calls to ALeRCE, Fink, IRSA/IPAC, Lasair, ANTARES, TNS, arXiv, ADS, SIMBAD, NED or anything else, and no web search or fetch tools
- your transcript will be audited for these paths and hosts

Allowed paths: the three `item/` files above, your tool directory and your output directory (below; you may write scratch files there), and the Python interpreter `/tmp/claude-1000/-home-aid1-Documents-4-19C-astronomy/addb1fc3-63d3-4989-8753-aa4c400b100e/scratchpad/venv/bin/python`.

## Limits
- At most 60 tool calls.
- Write the submission once it is final. You may overwrite it before you finish.
- The final chat message must be at most 200 words: state the family, the key parameters and the path written.

## Your tools and output path
Run every tool with `/tmp/claude-1000/-home-aid1-Documents-4-19C-astronomy/addb1fc3-63d3-4989-8753-aa4c400b100e/scratchpad/venv/bin/python <tool> --item-dir /home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot/item ...`. Each prints JSON, and `--out FILE` also saves it. The tools read model files internally; do not open those files.

Tool directory: `/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot/arms/tools/fm/`
1. `salt3_fit.py`: fits SALT3-f22 with sncosmo to the pre-cut detections, with MW dust fixed at item `mwebv`.
   - Options: `--z-min/--z-max` (default 0.005–0.3) or `--fix-z Z`; `--t0-min/--t0-max`, `--x1-min/--x1-max`, `--c-min/--c-max`; `--modelcov`.
   - Returns parameters in submission form, the fit summary and the pre-cut chi2 per point under the scoring formula.
2. `parametric_fit.py --family Bazin|Villar`: per-band parametric fits (`--p0`, `--bounds` as JSON, `--loss`), with their pre-cut chi2. Bazin and Villar are not submittable for this item; use them only to compare families.
3. `predict.py --params FILE.json`: evaluates any family and parameters with the same forward-model code the grader uses. Prints the pre-cut chi2 and model fluxes on a grid to the horizon (`--step`, `--mjd`).
4. `check_submission.py --submission FILE.json`: schema, scope and domain check, plus finite fluxes over the scoring window. It does not read held-out data.
5. `parsnip_run.py`: ParSNIP, a variational autoencoder light-curve model trained on ZTF g/r. It encodes the pre-cut detections into a latent (z, t0, amplitude, color, s1, s2, s3) and returns that latent's pre-cut chi2. `--fit` refines it with sncosmo (`--fix-z` or `--z-min/--z-max`).
   - `predict.py` can render the returned ParSNIP parameters to the horizon.
   - **Limitations:** the checkpoint was trained on ZTF Bright Transient Survey light curves from 2019–2021, truncated at most 3 nights after first detection, with no redshift information. It has seen almost no photometry at the phases that will be graded. ParSNIP is **not submittable** for this item; use it only as evidence (for example, family plausibility, time of peak or redshift).

Output path: `/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot/arms/outputs/fm/submission.json`
