# Wave 5 · Agent 2: grader, harness and one-case pilot

> PRE-RATIFICATION PILOT (harness check only). No score record, no directional claim, not an I1 record.
> Agent 2 returned this report as text, because the harness blocks REPORT.md writes. The coordinator saved it without changing its substance. Brief hash `cd10a41c…5e4c6b` was verified before anything was written.

## Headline
- **The harness works end to end, and the pilot yields no score.** R1 on a synthetic item is R1-PASS. The pilot item was selected under a sealed outcome-blind rule; its family, read only after the seal, is **SN II**, while the only admissible grader renders SN Ia. The pilot therefore returns `OUT_OF_SCOPE:NON_IA_OBJECT`, a scope failure rather than a score. Under AM-2 that is still a valid harness check.
- **Protocol frozen first:** `grader_protocol_FROZEN.md`, sha256 `ef580054…09bc`. Every script re-checks it and aborts on mismatch. The seed for all synthetic work is `int(sha[:8],16)` = 4015521876.
- **Three graders written from code, with controls run.** G-SALT3 (salt3-f22 in sncosmo 2.13.1), G-PARAM (Bazin + Villar, numpy, written this wave) and G-ParSNIP (wave-2 ZTF fold 0). Must-fire fired for all four grader/family pairs. **Must-not-fire FIRED at v1 for three of them**, and that FAIL stands on the record (AM-1).
- **The declared must-not-fire control was wrong, not the grader.** A relative 1e-9 perturbation of `t0` (MJD 59800) is a 5.2-second epoch shift, about 10⁵ ulp. Single-parameter diagnostics: dS = −3.24e-5 from t0 alone, against −6.6e-10 (z), −7.3e-9 (x0), −3.7e-10 (x1) and −2.8e-10 (c). AM-1 changed the perturbation (t0 to +1e-9 d absolute), not the tolerance. v2 passes at |dS| 4.5e-12 to 1.2e-8, and the v1 results are kept in `tool_cards/control_results_v1.json`.
- **The mechanical floor overfits by construction, and this was left unrepaired.** On the R1 synthetic item the frozen §9 floor picked Bazin (pre-cut χ²/pt 6e-16 on 3 points per band) and then scored **S = 49.2** on held-out epochs, against **0.58** for the true parameters (floor Q 0.020 vs 0.632). On the pilot item the same floor again picked Bazin (0.182 vs SALT3 0.369) and now returns `COVERAGE_FAIL:SCOPE` under AM-2.
- **Coverage is never a zero.** Eight coverage controls fired with the expected code: missing file, non-JSON, flux key, NaN parameter, empty rivals, negative z, τ_rise = 0 and wrong item_id. `COVERAGE_FAIL:SCOPE` and `DECLINED` from AM-2 were exercised too.

## Order of operations (UTC; every step hashed in `order_of_operations.log`)

| Step | Time | What |
|---|---|---|
| 0–1 | 17:56–18:00 | brief verified; protocol frozen and hashed |
| 2a–2c | 18:00–18:04 | pinned asset copies; grader and tool code; `controls_spec_PRE_RUN.md` hashed **before** any control ran |
| 2d–2f | 18:05 | controls v1 (must-not-fire FAIL); AM-1 recorded with diagnosis; controls v2 |
| 2g | 18:08 | three tool cards from code (validate PASS) |
| 3a–3c | 18:08 | R1 dispositions hashed before the run; attempt 1 interrupted (UNDEMONSTRATED); attempt 2 R1-PASS |
| 5a–5b | 18:09–18:10 | selection rule sealed **before** any object fetch; 16 objects examined, 1 selected, seal hashed |
| 5c–5e | 18:10–18:13 | item and held-out built and hashed; IAU name read after the seal; contamination checked |
| 6a–6c | 18:14–18:15 | coordinator message, AM-2, scope implemented; controls and R1 re-run as regression, unchanged |
| 4/5f–6f | 18:15–18:18 | both floors run and graded; contamination record; arm prompts; 20 tool tests; R8 table |
| 7–10 | 18:18–18:22 | replay cases and rulings; seed ledger; disagreements; final hash manifest (190 files) |

## 1. Protocol (frozen before the work it governs)
- **Cut epoch:** `t_cut = t_first + 10 d`, declared new with cause. Manifest v3 ratified E1 and E3 **for the infer follow-up decision**; under generate the answer is a fit, and E1/E3 hold fewer points than any family has parameters. On this object E1 = 1 detection and E3 = 5, exactly the SALT3 parameter count (0 dof). Per DS-10, the value 10 d is marked UNDEMONSTRATED and is a proposal for PI ratification, not an override.
- **Held-out set:** all g/r detections in `(t_cut, t_first + 60 d]`. A band scores only with at least 5 points.
- **Score:** `σ_eff = max(σ, 0.05|f|)`; `χ²_b` is the mean r² per band; `S` is the mean over scored bands; the bounded transform is `Q = 1/(1+S)` in (0,1]. The near-ideal reference (R1 only) is `χ²_b ≤ χ²₀.₉₉₅(N_b)/N_b`.
- **Coverage codes:** MISSING, PARSE, SCHEMA, DOMAIN, EVAL, GRADER_ERROR (an instrument failure, with the arm not charged) and, from AM-2, SCOPE and DECLINED. None is ever a zero (refusal 6).
- **Arms submit parameters, never fluxes.** A flux array is an unknown key, so it fails SCHEMA (control 3 fired).
- **Separation:** `item/` holds `pre_cut.csv`, `item_meta.json` and `scope.json`, with no ZTFID, IAU name or coordinates. `grader_private/` holds the held-out set, the identity, the family and the grader's own forward-model copy. Grader assets are a separate hash-checked copy from the arms'.

## 2. I3/I4: grader cards and controls
Three cards were written from code, all validate PASS, each with a non-optional disagreement list (6, 6 and 4 entries). Notable disagreements:
- sncosmo returns **0 flux outside the SALT3 phase range**, and the grader scores that zero.
- The K21 model covariance is replaced by a 5% floor.
- ParSNIP corrects MW dust with FM07 while the grader applies F99.
- The extracted Bazin 2009 Eq. 1 text carries a **positive** exponent in the rise denominator, while the code uses the negative (rising) form.
- Villar Eq. 1 has no baseline term, while its Table 1 lists one.

**I4 ruling: does the held-out residual measure what the program scores?**
- **PASS for predictive fit** on held-out ZTF g/r photometry, which is the oracle's verdict in shape.md's A3 row for generate.
- **FAIL as a measure of physical truth.** No term in S depends on the parameters being physically right.
- Ten weaknesses are listed on every card, including family-dependent model ranges (SALT3 predicts zero past +50 rest-frame days while parametric curves are defined everywhere), the arbitrary 5% floor, equal band weighting, correlated residuals within a band, the horizon choice, unscored rejection reasons, and procedural-only separation.

**Controls** (`tool_cards/control_results.json`; the spec was hashed before running):

| Grader | S_ref | S_wrong | must-fire | must-not-fire v1 | v2 (AM-1) |
|---|---|---|---|---|---|
| G-SALT3 | 0.532 | 223.6 | fired | **FIRED** 3.24e-5 | 9.2e-9 PASS |
| G-PARAM Villar | 0.380 | 115.3 | fired | **FIRED** 5.3e-6 | 1.2e-8 PASS |
| G-PARAM Bazin | 0.379 | 117.5 | fired | **FIRED** 1.6e-6 | 1.2e-10 PASS |
| G-ParSNIP | 0.313 | 238.6 | fired | 3.6e-7 PASS | 4.5e-12 PASS |

Repeat-grade and JSON round-trip deltas are exactly 0.0 for all four, so the grader is deterministic. G-ParSNIP passed at v1 only because its decoder casts to float32; that is recorded, not credited.

## 3. R1 on a synthetic item
Dispositions were written and hashed first (`r1/dispositions_PRE_RUN.md`). The item is SALT3 at z 0.05, t0 59800, x0 1.2e-3, x1 0.5, c 0.05, mwebv 0.03, with ZTF-like cadence and noise, seed 4015521876, built through the **same builder as the real pilot** (3 g + 3 r pre-cut, 13 g + 10 r held out).
- **Attempt 1** was interrupted in the result writer (a numpy bool was not serialisable) after grading. It is recorded UNDEMONSTRATED with its cause, and only the writer was changed.
- **Attempts 2 and 3 (the latter re-run after AM-2 changed `grade.py`): R1-PASS.** True parameters give S = 0.583 and Q = 0.632, with both bands near-ideal (χ²/pt 0.871 ≤ 2.294 and 0.296 ≤ 2.519). The wrong-family Bazin submission gives S = 49.17 > S_true. All hash criteria were met.

## 4–5. Pilot item, selection seal, contamination
- **Sealed rule** (`selection/selection_rule_SEALED.md`, hashed before the first fetch): BTS rows peaking in 2022 (reading only `ZTFID` and `peakt`), dropping every ZTFID in the wave-2 ParSNIP cohort, sorted ascending, walking until an object has ≥20 positive detections in each of g and r, `0 ≤ peak − t_first ≤ 100 d`, and ≥3 pre-cut and ≥8 held-out detections per band. The fetch cap was 150.
- **Result:** 1,308 candidate rows, none in the ParSNIP cohort. 16 were examined and **ZTF18aasyjhd** was selected: 9 g + 7 r pre-cut, 35 g + 35 r held out, t_first MJD 59732.28, cut 59742.28, horizon 59792.28, mwebv 0.0298 from SFD.
- **Hashes:** `item/pre_cut.csv` `0f6ab10d…`, `item/item_meta.json` `b97dcc27…`, `grader_private/held_out.csv` `bc228eee…`.
- **Contamination** (`contamination_check.json`): 9 arXiv API name queries (`SN2022lvm`, `SN 2022lvm`, `AT 2022lvm`, `ZTF18aasyjhd`, …) returned 0 hits each, while positive controls returned 91 and 98 hits, so the query path is live. One web search returned 9 arXiv papers; all 9 PDFs were downloaded and grepped, with 0 full-text mentions.
  - **Ruling: UNDEMONSTRATED-leaning-clean, not CLEAN.** The arXiv API indexes metadata only, and ADS full text, TNS AstroNotes, the Superphot+ Zenodo table and ANTARES saved fits were not checked.
  - A web-search tool summary asserting a type, redshift and coordinates for this object is recorded as **unverified and unused**; its coordinates disagree with both ALeRCE and BTS.

## 6. AM-2: acting on agent 1's shape record
AM-2 is recorded in `amendments.md`; the frozen protocol was not edited. The pilot scope is restricted to **SALT3 only**, plus an explicit `DECLINE`. All consequences are implemented and exercised:
1. **Family read after the seal: SN II, z 0.143** (`grader_private/object_family_POST_SEAL.json`). SALT3 renders Ia only (DS-03), so a SALT3 submission is `OUT_OF_SCOPE:NON_IA_OBJECT`, and the residual survives only as `harness_diagnostic_residual_NOT_A_SCORE`.
2. **Floor of record: SALT3 `fit_lc` at defaults** (DS-11). The fit succeeded (z 0.185, t0 59747.55, pre-cut χ²/pt 0.369) and the grade is `OUT_OF_SCOPE:NON_IA_OBJECT`, with a diagnostic S of 28.6 that is not a score. The frozen §9 two-generator floor was also run; it picked Bazin and returned `COVERAGE_FAIL:SCOPE`, which exercises the scope code.
3. **ParSNIP mounted with its limitation stated** (DS-01), informational only and not submittable. The truncated training window appears in the FM prompt, the ParSNIP card and `r8_symmetry.json`. It was not retrained.
4. **R4 separation audit declared** (DS-06): a case-insensitive transcript grep for ALeRCE, Fink, IRSA, TNS, arXiv, ADS, SIMBAD and NED hosts, for `http`, `curl`, `wget`, `requests` and web tools, and for `grader_private`, `grade.py`, `data_cache/alerce_raw`, `selection/`, `floor/`, `r1/`, `tool_cards/` and `ztf_bts_all`. A hit voids that arm as `VOID:SEPARATION_BREACH`. R4 stays UNDEMONSTRATED: the audit detects, it does not enforce.
5. Conventional values are marked UNDEMONSTRATED (DS-10).

`disagreements.json` records responses to DS-01, DS-03, DS-04, DS-06, DS-07, DS-10 and DS-11, with two residual disagreements:
- A frozen Bazin/Villar grader **does** now exist (G-PARAM, hashed, controls run), so "no frozen grader" is no longer a fact about the inventory, although AM-2 still keeps it out of the pilot.
- The wave-2 ParSNIP folds need no redshift (the photo-z prior is neutralised), so DS-11's redshift objection does not apply to that checkpoint. The truncation objection does.

## 7. Arms, tools and R8
- `arms/classical_arm_prompt.md` (6,321 B, `55ce2897…`) and `arms/fm_arm_prompt.md` (7,061 B, `a6d0b218…`) are **byte-identical for their first 4,699 bytes**, and every differing byte lies inside `## Your tools and output path`.
- **Toolsets.** Classical: `salt3_fit.py`, `parametric_fit.py`, `predict.py`, `check_submission.py`, all four byte-identical across arms and sharing one `forward_models.py` identical to the grader's copy. FM: those four plus `parsnip_run.py`.
- **Tool tests.** 20 runs in `arms/tool_tests/`, including two intended negative checks (the classical toolset raises `AssetError` on ParSNIP parameters and ships no `parsnip_run.py`) and three `check_submission` scope cases returning OK, OK (DECLINE) and COVERAGE_FAIL:SCOPE.
- **`r8_symmetry.json`:** 14 rows, 7 differences, 7 rulings. The one row that blocks stage exit is **subject and sampling parameters**, which only the launching session can record: model id, temperature, the model-side tool catalogue (R4), and the **emitted** prompt hash beside the declared one (R6).

## 8. Grading script
`grade.py` (`52f12faa…`) grades any submission JSON against a private directory: protocol hash check, pinned-asset hash check, scope, schema, domain, forward model, finite check, then score. Every record carries the protocol, forward-model, grade.py, item_meta, held_out, submission and asset hashes. It was tested on the floor submissions, both R1 stubs, all control references and perturbations, and the eight coverage cases.

## Dispositions

| Criterion | Disposition |
|---|---|
| Protocol frozen before the work it governs | PASS |
| I3 cards from code, disagreements listed | PASS (3 cards, validate PASS) |
| I4 construct validity on the scored quantity | PASS for predictive fit; FAIL for physical truth; weaknesses listed |
| Must-fire control | PASS (4/4) |
| Must-not-fire control | FAIL at v1 (recorded), PASS at v2 after AM-1 |
| Coverage controls | PASS (8/8, plus SCOPE and DECLINE) |
| R1 on a synthetic item | attempt 1 UNDEMONSTRATED (interrupted); attempts 2–3 R1-PASS |
| Mechanical floor built and graded | PASS as a build; the result is a scope failure, not a score |
| Pilot item packaged under a sealed outcome-blind rule | PASS |
| Pilot score | NONE: `OUT_OF_SCOPE:NON_IA_OBJECT` |
| Contamination under generate | UNDEMONSTRATED-leaning-clean |
| R4 grant and separation | UNDEMONSTRATED (audit declared, not enforceable) |
| Arm symmetry (R8) | PASS except the subject row, which the coordinator fills |

## Final grading result (appended after the arms ran)

Both arms were graded blind. Both return `OUT_OF_SCOPE:NON_IA_OBJECT`: a coverage failure, not a score. The full final report is in `FINAL_REPORT.md`.

## What the coordinator does next
1. Launch two fresh subagents with `arms/classical_arm_prompt.md` and `arms/fm_arm_prompt.md` verbatim. Hash the emitted prompts and record them beside `55ce2897…` and `a6d0b218…` (R6), with model id, sampling parameters and the model-side tool catalogue (R4).
2. Run the AM-2 item-5 transcript grep on both arms before sending anything back.
3. Send the two submission paths for blind grading with `grade.py`. Expect `OUT_OF_SCOPE:NON_IA_OBJECT` from both, or `DECLINED` if an arm judges the object un-SALT3-able, which on this object is the better-reasoned answer. The pilot reports harness mechanics and coverage, never a comparison.
4. **For the PI:** the cut epoch (+10 d), the horizon (+60 d) and the selection thresholds need ratification or replacement. generate / inverse problem stays ESCALATE at the grader gate until either a forward model trained disjoint from the supply is budgeted at D5, or the scope is formally restricted to the SN Ia family, in which case supply must be recounted over Ia-only objects, since an outcome-blind selection cannot guarantee one.
