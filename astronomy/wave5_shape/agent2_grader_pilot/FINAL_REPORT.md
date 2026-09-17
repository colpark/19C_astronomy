# Wave 5 · Agent 2: final report (after blind grading)

> PRE-RATIFICATION PILOT (harness check only). No score record, no directional claim, not an I1 record.
> Agent 2 returned this as text; the coordinator saved it unchanged. It supersedes the "what the coordinator does next" section of `REPORT.md`, which was written before the arms ran.

## Headline
- **Both arms were graded blind, and both return `OUT_OF_SCOPE:NON_IA_OBJECT`**, which is a coverage/scope failure rather than a score. The pilot object's catalogue family, read only after the selection seal, is **SN II**, and the only grader admissible under AM-2 renders SN Ia alone.
- **The harness works end to end on a real object:** sealed outcome-blind selection, item packaging with no identity, two symmetric arms, separation audit, and blind grading with a full hash chain.
- **Submission hashes match the coordinator's record exactly** (`fd9a9302…` classical, `68e949d3…` fm). Neither file was edited.
- **Diagnostic residuals (never scores):** floor 28.58, classical 30.63, fm 30.87. A grader-side family-capability check settles what that spread means: refitting SALT3 **directly on the held-out photometry** still cannot get below S = 4.6, and only by pinning x1 at its bound of 5.0 at z 0.268, while Bazin or Villar fitted to all epochs reach S ≈ 0.95. Family mismatch, shared by all three, accounts for the bulk of the 28–31 residual.
- **R8 EXITS for this cell:** 8 differences, 8 rulings, with the subject and emitted-prompt rows filled from `coordinator/arm_launch_record.json`. R4 stays UNDEMONSTRATED by design.
- **The most interesting content is what the grader cannot score.** Both arms reasoned at length about family choice and redshift, and both concluded "normal SN Ia" for an SN II. No part of S depends on that.

## 1. Blind grading

| | classical | fm |
|---|---|---|
| submission sha256 | `fd9a9302…7882` | `68e949d3…6ad8` |
| family | SALT3 | SALT3 |
| z | 0.142 | 0.140 |
| t0 (MJD) | 59746.860 | 59746.804 |
| x0 / x1 / c | 3.865e-4 / 0.793 / −0.159 | 3.865e-4 / 0.783 / −0.161 |
| rejected rivals | Bazin, Villar, ParSNIP | Bazin, Villar, ParSNIP |
| **coverage code** | **`OUT_OF_SCOPE:NON_IA_OBJECT`** | **`OUT_OF_SCOPE:NON_IA_OBJECT`** |
| **score** | **none** | **none** |
| diagnostic S (not a score) | 30.626 | 30.867 |
| diagnostic per band (N, χ²/pt, median \|r\|) | g 35, 27.87, 5.48; r 35, 33.39, 5.80 | g 35, 28.07, 5.50; r 35, 33.67, 5.85 |
| diagnostic pre-cut χ²/pt | 0.3690 | 0.3688 |
| grade file | `grades/classical_grade.json` | `grades/fm_grade.json` |

Both grade records carry the protocol, forward-model, `grade.py`, item_meta, held_out, object-family and submission hashes. `pilot_result.json` holds the full record with an explicit no-claim statement.

## 2. Diagnostics, all labelled as diagnostics

| Submission | Coverage code | Diagnostic S (**not a score**) |
|---|---|---|
| Mechanical floor, AM-2 (SALT3 `fit_lc` at defaults) | `OUT_OF_SCOPE:NON_IA_OBJECT` | 28.58 |
| Classical arm | `OUT_OF_SCOPE:NON_IA_OBJECT` | 30.63 |
| FM arm | `OUT_OF_SCOPE:NON_IA_OBJECT` | 30.87 |
| Frozen §9 two-generator floor (pre-AM-2; chose Bazin, pre-cut χ²/pt 0.182 vs 0.369) | `COVERAGE_FAIL:SCOPE` | — |

**Grader-side family-capability check** (`grader_private/oracle_family_diagnostics.json`, never shown to any arm):

| Best-possible fit | Diagnostic S on held-out points |
|---|---|
| SALT3 fitted **on the held-out data itself** | 4.61 |
| SALT3 fitted on all epochs | 8.47 (x1 pinned at 5.0, z 0.268) |
| Bazin fitted on all epochs | 0.95 |
| Villar fitted on all epochs | 0.97 |

**Reading, and the refusal.** The floor sits 2.0 below the arms, and the arms 0.24 apart, on values near 30 whose floor for this family is 4.6 with the answer in hand. That spread is family mismatch plus extrapolation of a model that cannot represent the object; it measures no arm. **No arm is ranked, no difference is interpreted, and none of these numbers may enter power as per-item variance** (replay case AST2W5-05). The floor being numerically "less wrong" comes from its free-z fit landing at z 0.185 with a different wrong shape, not from better modelling.

## 3. What the two submissions share, and what that does and does not tell us
**Facts.**
- Both chose SALT3, the only submittable family besides DECLINE.
- Both found pre-cut χ² essentially flat in redshift (classical: flat to <0.1 over 0.04–0.26; fm: 0.368–0.391 over 0.04–0.28).
- Both broke the degeneracy by **SALT3 standardisation self-consistency, a Hubble-diagram argument**, not from light-curve shape.
- They landed within 0.002 in z (0.142 vs 0.140), 0.06 d in t0, 0.01 in x1 and 0.003 in c.
- Both rejected Bazin and Villar as overfitting, naming the specific degeneracy: τ_fall pinned at its 500 d bound, γ running to ~260 d, β collapsing to ~1e-18.
- The FM arm also rejected ParSNIP on measured grounds: pre-cut χ²/pt 4.70 against 0.37, latent z 0.276, and a latent t0 before the last still-rising pre-cut detection.
- Neither declined, although DECLINE was available and the FM arm explicitly considered it.

**What it does not tell us.**
- **Nothing about tool value.** Both arms held the same four tools; the FM arm's only extra tool was non-submittable, and its checkpoint had never seen photometry at the graded phases (DS-01). A null here is what the design predicts.
- **Nothing about agent value over the floor**, since floor, arms and the best-possible SALT3 fit are all scope failures on this item.
- **Nothing about the calibration of the redshift argument.** z 0.142/0.140 lands within 0.003 of the catalogue z 0.143, which neither arm could see: a striking single instance, no more, and the same argument was made confidently for an object that is not a SN Ia.

**What it does tell us.**
- The harness, item packaging, separation, scope code and coverage codes work end to end on a real object.
- The written-rejection branch produced substantive, checkable reasons, which is the native lift shape.md describes.
- The pilot exposes the sharp version of the I4 weakness: **the reasoning that carried all the content — family diagnosis, redshift argument, the false Ia call — moves S by nothing at all.**

## 4. R8: closed
`r8_symmetry.json`: 15 rows, 8 differences, 8 rulings, `stage_disposition: "R8 EXIT (pilot cell), with R4 UNDEMONSTRATED recorded"`.
- **Subject row.** Both arms are `claude-opus-5[1m]`, fresh general-purpose subagents with no panel context. Sampling parameters are UNDEMONSTRATED for both equally: symmetric, so not a between-arm confound, but the cell is not bit-for-bit replayable. Tool calls, 20 classical against 17 fm, are an outcome rather than a supplied asymmetry; the cap was 60 for both.
- **R6/R7.** Emitted prompts (`255aa48a…7bcb`, `53ea8893…7923`) differ from the declared files by exactly one stripped trailing newline, identically for both arms, established by byte-level reconstruction rather than assertion. Cosmetic and symmetric. Declared and emitted hashes now sit side by side.
- **Separation audit row.** Zero forbidden-path or network hits in either transcript, so neither arm is voided. The audit script's first-pass word-boundary defect ("ned" inside "trained", 7 false positives) and its fix are recorded. **R4 stays UNDEMONSTRATED**: the audit detects, it does not enforce, and the model-side catalogue was never enumerated.

## 5. Replay suite
Six cases, four must-fire and two must-not-fire, with rulings in the separate file.

| Case | Stage | Polarity | Subject |
|---|---|---|---|
| AST2W5-01 | I4 | must_fire | widening a must-not-fire tolerance instead of fixing a mis-specified perturbation (the real AM-1 instance) |
| AST2W5-02 | I1 | must_fire | retuning the floor metric so the floor stops choosing the overfitted family |
| AST2W5-03 | R1 | must_not_fire | accepting a re-run after a harness-side crash recorded as UNDEMONSTRATED with its cause |
| AST2W5-04 | A3 | must_fire | reporting an out-of-family residual as the pilot's score |
| AST2W5-05 | A3 | must_fire | new: ranking floor and arms on 28.58 / 30.63 / 30.87 and feeding them to power |
| AST2W5-06 | R8 | must_not_fire | new: exiting R8 after ruling the stripped newline cosmetic and recording arm convergence as no evidence about tool value |

## 6. Dispositions

| Criterion | Disposition |
|---|---|
| Blind grading of both arms | PASS (both `OUT_OF_SCOPE:NON_IA_OBJECT`; hashes verified; submissions unedited) |
| Pilot score | NONE: scope failure on both arms and the floor |
| R1 harness control | R1-PASS (attempt 1 UNDEMONSTRATED, interrupted, recorded before repair) |
| I3 cards from code with disagreement lists | PASS (3 cards, validate PASS) |
| I4 construct validity | PASS for predictive fit; FAIL for physical truth, demonstrated concretely by this run |
| Must-fire / must-not-fire controls | PASS (must-not-fire FAILED at v1 and that stands; AM-1) |
| Coverage codes exercised | PASS: MISSING, PARSE, SCHEMA, DOMAIN, SCOPE, DECLINE, OUT_OF_SCOPE all fired |
| R8 arm symmetry | EXIT |
| R4 grant verification | UNDEMONSTRATED (brief constraint 3) |
| Contamination under generate | UNDEMONSTRATED-leaning-clean |
| Directional claim | NONE, and none is available |

## 7. For the PI
1. **The staged pilot did its job and produced no score, for a declarable reason.** Constraint 2 is satisfied: harness mechanics verified, no I1 record written.
2. **The scope problem is now measured rather than argued.** A one-family grader on an outcome-blind selection will fail on most items: the BTS-wide Ia fraction is high but well short of one, and the first passing object was an SN II. Clearing the ESCALATE at the grader gate needs either a D5-budgeted forward model trained disjoint from the supply, or a scope restriction to SN Ia. In the second case **P3 must recount supply over Ia-only objects, and the selection rule must be rewritten to stay outcome-blind within that restriction** — not trivial, since "is it a SN Ia" is exactly what the arm is asked to judge.
3. **The cut epoch (+10 d), the horizon (+60 d), the error floor and every selection threshold remain UNDEMONSTRATED as derived quantities** (DS-10) and need ratification or replacement.
4. **The scored quantity misses the branch that carries the content.** Both arms wrote careful, falsifiable family and redshift arguments, and the residual is blind to all of it. On this object both were confidently wrong about the class while fitting the pre-cut data to χ²/pt 0.37. If the program cares about that judgement, the grader has to score it, which returns to the certified-judge gate that closed three other subtypes.

**Deliverables:** 190 files under `HASH_MANIFEST.sha256`, including `grader_protocol_FROZEN.md`, `amendments.md`, `tool_cards/`, `r1/`, `selection/`, `item/`, `grader_private/`, `contamination_check.json`, `floor/`, `arms/`, `grades/`, `pilot_result.json`, `r8_symmetry.json`, `grade.py`, `disagreements.json`, `order_of_operations.log`, `seed_ledger.json`, `replay_cases.csv` and `replay_rulings.csv`. `data_cache/` (91 MB) is gitignored and hashed in place.
