# R1 harness control on a synthetic item: dispositions written before the run

PRE-RATIFICATION PILOT (harness check only). Governing: `grader_protocol_FROZEN.md` §8 (sha256 `ef58005482a049e5d58131267b0758ab0bfae3bb1c674650d6302f545fa709bc`), `runtime.md` R1. Written after the I4 controls (which used different seeds and items) and before `scripts/r1_run.py` existed.

## Fixtures
- **Synthetic item** `R1-SYNTH-001`: SALT3 z 0.05, t0 59800.0, x0 1.2e-3, x1 0.5, c 0.05, mwebv 0.03, simulated with seed = int(sha256(protocol)[:8], 16) = **4015521876**, passed through `scripts/item_builder.py` (the real-pilot builder) into `r1/item/` and `r1/grader_private/`.
- **Known-good subject** (stub composition, no model in the loop): (a) `r1/submissions/true_params.json` = the true parameters, family SALT3; (b) `r1/submissions/wrong_family.json` = Bazin fitted to the pre-cut detections by the floor's Bazin generator (`scripts/floor_generators.py::bazin_default`).
- **Surface under test:** item builder → pre_cut/held_out split → submission JSON on disk → `grade.py` (protocol hash check, pinned-asset hash check, schema, forward model, score) → grade JSON on disk. Also the mechanical floor end to end on the same item (recorded, not a pass criterion).

## Pass criteria
- P1: the item is scoreable (at least one band with ≥ 5 held-out detections).
- P2: (a) returns `SCORED` and every scored band satisfies χ²_b ≤ χ²_{0.995}(N_b)/N_b.
- P3: (b) returns `SCORED` with S_b > S_a.
- P4: grade JSONs carry protocol, forward_models, grade.py, item_meta, held_out and submission hashes, and the held_out hash equals the hash written at item build.

## Dispositions (fixed now; not reinterpretable)

| Disposition | Fires when | Action |
|---|---|---|
| **R1-PASS** | P1–P4 hold | Harness surface completes on a known-good subject; the real pilot item may be packaged (brief constraint 2). No score record. |
| **R1-FAIL (instrument)** | P1 holds and the grader ran, and any of P2–P4 fails, or any `GRADER_ERROR` | Indicts the instrument (grader, builder or forward model), never a subject. Work returns to the instrument module; the real pilot is not packaged until a re-run passes. |
| **R1-UNDEMONSTRATED** | P1 fails (item unscoreable), the run is interrupted, or an asset hash check aborts before grading | Recorded as UNDEMONSTRATED, never zero; no repair before recording. |
