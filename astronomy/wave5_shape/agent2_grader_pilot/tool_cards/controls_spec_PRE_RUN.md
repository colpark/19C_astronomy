# I4/I5 grader controls: specification, written before any control ran

PRE-RATIFICATION PILOT (harness check only). Governs `scripts/controls_i4.py`. Protocol: `grader_protocol_FROZEN.md` sha256 `ef58005482a049e5d58131267b0758ab0bfae3bb1c674650d6302f545fa709bc`; seed = int(sha[:8], 16) = 4015521876.

## Control items (synthetic, simulator of protocol §8, graded through `grade.py`)

| Item | Seed | Truth |
|---|---|---|
| CTRL-SALT3 | seed+1 | SALT3 z 0.05, t0 59800, x0 1.2e-3, x1 0.5, c 0.05, mwebv 0.03 |
| CTRL-VILLAR | seed+2 | Villar per band. ztfg: A 700, beta −2.0, t0 59785, gamma 8, tau_rise 3, tau_fall 25, B 0. ztfr: A 650, beta −1.0, t0 59786, gamma 12, tau_rise 3.5, tau_fall 35, B 0. mwebv 0.03 (unused by parametric) |
| CTRL-PARSNIP | seed+3 | ParSNIP z 0.05, t0 59800, color 0, s1 0, s2 0, s3 0, amplitude scaled so the noiseless ztfr peak on a 0.5 d grid is 631 (18.0 mag) |

## Reference submissions
- G-SALT3: truth on CTRL-SALT3.
- G-PARAM Villar: truth on CTRL-VILLAR.
- G-PARAM Bazin: Bazin least-squares fit (same start and bounds as floor §9) to **all** detections of CTRL-VILLAR (pre-cut and held-out), i.e. the best-available Bazin. It is a reference, not a truth.
- G-ParSNIP: truth on CTRL-PARSNIP.

## Must-fire (a deliberately wrong parameter set must score clearly worse)
- Wrong sets: SALT3 t0 + 15 d and x1 → −3; Villar/Bazin t0 + 15 d in both bands and tau_fall × 0.3; ParSNIP t0 + 15 d and color + 0.5.
- **Fires (PASS) iff** `S_wrong ≥ S_ref + 5` **and** `S_wrong ≥ 3 · S_ref`, both SCORED.

## Must-not-fire (float noise must not change the score beyond tolerance)
- Perturbation: every parameter `p → p · (1 + 1e-9)`; a parameter exactly 0 → `1e-12`. Also: the reference re-graded a second time (repeatability), and the reference serialised with `json.dumps` and re-parsed.
- **Does not fire (PASS) iff** `|S_perturbed − S_ref| ≤ 1e-6 · max(1, S_ref)` for all three variants.

## Coverage controls (must fire with the named code, never a score)
1. missing file → `COVERAGE_FAIL:MISSING`
2. non-JSON text → `COVERAGE_FAIL:PARSE`
3. a `predicted_flux` key added → `COVERAGE_FAIL:SCHEMA`
4. `"x1": NaN` → `COVERAGE_FAIL:SCHEMA`
5. `rejected_rivals` empty → `COVERAGE_FAIL:SCHEMA`
6. SALT3 `z = -0.1` → `COVERAGE_FAIL:DOMAIN`
7. Bazin `tau_rise = 0` → `COVERAGE_FAIL:DOMAIN`
8. `item_id` of another item → `COVERAGE_FAIL:SCHEMA`

## Dispositions per grader
- **PASS**: must-fire fires, must-not-fire does not fire.
- **FAIL**: either control disagrees; work returns to the instrument.
- **UNDEMONSTRATED**: a control could not run (GRADER_ERROR or unscoreable item).
