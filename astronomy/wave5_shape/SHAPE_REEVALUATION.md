# Shape re-evaluation under `fm-advantage-benchmark-with-shape`

Coordinator draft, 2026-09-17. Skill source: `fm-advantage-benchmark-with-shape.zip`, sha256 `a4b98598…1240`, vendored unchanged at `fm-advantage-benchmark-with-shape/`.

**Status.** This is a screening pass, not a D4 shape record.
- Gates 1–3 are ruled here from the tool inventory and the root structure, which are already in the repo.
- The branch-point census and the evidence-depth census have not been run on the seeds. Until they are, no root may PROCEED (refusal 10: no root opened by extrapolation).
- Every "passes" below is conditional on that census.

## 1. What the new skill changes for us

**The old skill forced one shape.** Waves 1–4 ran a single task: pick k of M transients for a spectrum, scored against an answer key of spectroscopic labels. The old manifest offered only prediction or design, so no other shape was weighed. `shape.md` names exactly that failure: every candidate that survived was a selection task, and nothing in the record shows alternatives rejected.

**Our governed decision was intervene, but it was graded as infer.** `shape.md` says "which candidate to spend the instrument on is intervene."
- Intervene needs the outcome of the action not taken. BTS only has spectra for objects someone chose to observe, which is the selective-labels problem the file calls "the binding axis" for intervene.
- Scoring that decision as infer, pick k of M, put it on the predictor line. Gate 1 then requires a lift, and none was recorded.
- So the stall in waves 1–4 was a shape problem first. Contamination and label access were where that problem showed up, not its cause.

**Contamination is defined per root.** `shape.md` downstream table:

| Root | Contamination means |
|---|---|
| infer | the answer appears in the item's source |
| explain | the cause is stated in literature the subject read |
| generate | the object is published and indexed |
| intervene | the historical policy is recoverable from the data |

Under infer, a public TNS label is fatal. Under generate or explain, graded by a forward model or likelihood on data the arm never saw, there is no answer string to memorize. The archival ZTF corpus therefore becomes usable supply again for those roots.

**Wave 1–4 counts do not transfer.** Refusal 6 requires re-registering and recounting when the root changes. Carried over as instruments and infrastructure:
- the tool inventory
- the pinned SALT3-f22 and the ZTF-trained ParSNIP checkpoints
- the cohort enumeration code
- module V
- the integrity protocol

## 2. Four roots, gates ruled per subtype

Tool facts come from `astronomy/agent4_tools_instrument/REPORT.md` §2 (roles from code), `astronomy/wave2/agent4_instrument/REPORT.md` (ParSNIP trained from scratch on ZTF g/r with no redshift, 5 folds, hashed) and `astronomy/wave3/agent4_tool_recount/REPORT.md`.

| Root / subtype | Gate 1: role floor | Gate 2: grader, in inventory? | Gate 3: yield per unit | Screening disposition |
|---|---|---|---|---|
| **infer**: pick k of M (the waves 1–4 task) | on the predictor line; no lift recorded | answer key = measured spectroscopic labels. Post-cutoff: BLOCKED (TNS, WISeREP). BTS: contaminated under infer | k thresholded binaries per round. P2 floor: 0.95–1.00 of the deep ceiling post hoc; at first alert both compositions sit near AUC 0.60 | **ESCALATE**, binding gate: grader (plus role floor without a lift) |
| infer: calibrated probability per candidate | on the line; lift needed | same key, same blocks | one graded scalar per candidate, which beats pick-k | same as above; climbing the ladder raises yield but not grader access |
| **explain**: hypothesis set under a frozen likelihood | scorer and generator, **below the line** | **frozen_likelihood, in inventory**: SALT3-f22 (sha `c7de5343…`); ParSNIP decoder (ZTF-trained, hashed, wave 2); a PLAsTiCC checkpoint for LSST bands | one graded log-likelihood per hypothesis | **conditional pass.** Risk: an exhaustive template × z grid may be a floor that already reaches the ceiling (P2 must test). I4 must certify that likelihood tracks the scored quantity and not just fit flexibility |
| explain: anomaly diagnosis | scorer, below | certified judge or held-out repeat; **no judge in inventory** | one score | **CLOSE** at grader (for now) |
| explain: mechanism attribution | scorer, below | certified judge; none | one rubric score | **CLOSE** at grader |
| **generate**: inverse problem | generator, **below the line** | **forward model already in inventory**: SALT3 (Ia), ParSNIP decoder, Superphot+ parametric model (generator role, ZTF AU) | one **graded** residual per item. Scoring on held-out later epochs adds per-band, per-epoch scalars and stays graded | **conditional pass. Strongest candidate** (see §3) |
| generate: object design | generator | certified oracle or assay; none | pass/fail | **CLOSE** at grader |
| generate: procedure or code | generator | execution harness; buildable, but the action is not yet shown in the astronomy seeds | binary per test | **UNDEMONSTRATED**: action absent from corpus until the census finds it |
| **intervene**: choose next measurement / allocate / stop | simulator, below | replayable environment or held-out outcomes. SNANA is UNDEMONSTRATED (not runnable); ELAsTiCC truth tables exist but no environment is built | one realized value per episode | **CLOSE** at grader, recorded as the finding that explains waves 1–4. It can reopen only as a D5-budgeted build (an ELAsTiCC-based replay environment) |

Alternatives field (refusal 5): infer falls at the grader gate, intervene at the grader gate, and three of the four explain/generate siblings at the grader gate. Two subtypes survive screening: explain / hypothesis set, and generate / inverse problem. These are exactly the two `shape.md` calls "the cheapest doors out of infer".

## 3. Why generate / inverse problem ranks first (resolving power before cost, refusal 12)

- **No labels needed.** The grader is a forward model already in the inventory. TNS, WISeREP and the selective-labels problem no longer bind.
- **Graded, not thresholded.** A residual keeps the margin, and scoring on held-out epochs gives several scalars per object. That means smaller σ_d relative to effect and a smaller MDE per labeled unit than any infer rung. This is expected, not yet measured; P7 must compute it from compositions.
- **Hard to game when scored on held-out epochs.** The arm sees photometry up to an epoch and proposes model family and parameters. The grader then scores the forward prediction against later photometry the arm never saw. Overfitting a flexible model is penalized, and there is no answer string in any source.
- **Contamination under generate** is "object published and indexed": a published fit for that specific object. It is countable per object, and it is absent for post-cutoff objects and most archival ZTF objects.
- **Mechanical floor (I1, per the downstream table):** run the generator at defaults and keep the best on one metric.
  - classical: sncosmo SALT3 at default bounds, plus a Bazin/Villar parametric fit
  - FM channel: ParSNIP decoder at default encoding
- **Where agent value could live:**
  - choosing among model families
  - constraining redshift from host context
  - rejecting a degenerate fit with a written reason (a native branch, not a lift)
  - deciding when the evidence supports a fit at all
- **Evidence depth:** photometry bands, host photo-z, extinction, and cadence. Measure it by leave-one-out at I2. Advantage should rise with depth and vanish at depth one.

**Known weaknesses, listed and not resolved:**
1. The grader's forward models are also tools the arms may hold. The grader must be a frozen, separately pinned instance, and the arms get no access to the held-out epochs. R4 must verify both.
2. Residual on held-out epochs measures predictive fit, not physical truth. I4 must rule whether that is the quantity the program cares about.
3. Rubin supply is currently thin for this root: 80.8% of the cohort has a single detection (V-C04), and Rubin has been off sky since 2026-07-14. The ZTF public archive carries the supply for now, which is a P3 count to run under this root.
4. The branch-point census has not run. The action (practitioners choosing a model, bounds or rejections while fitting) must be located in seeds read in full, e.g. the SALT3/SALTShaker, ParSNIP, Superphot+ and Villar methods sections, before this root can PROCEED.

## 4. The "one good case" under this shape (a pilot, not a claim)

1. Pick one ZTF transient with multi-band photometry and at least 20 epochs, chosen by a declared rule and not by outcome.
2. Freeze a cut epoch, for example 10 days after first detection. Hide everything later.
3. **Task (generate / inverse problem):** propose a model family and parameters, with a written reason for rejecting the rival families.
4. **Grader:** a frozen forward model scores the prediction against the hidden epochs, as a per-band residual (χ² per point).
5. **Arms:**
   - mechanical floor (defaults)
   - classical agent (SALT3 plus parametric fits)
   - FM agent (plus ParSNIP)
6. **What it shows:** whether the harness, grader and arm symmetry work end to end, i.e. R1/R2 scale. Under A4 it supports no directional claim, because one unit is far below any MDE.

## 5. Proposed next wave (for PI ratification)

1. **D1 censuses.**
   - Branch points and evidence depth on the seeds already held, with locators.
   - Also read the SALT3, ParSNIP, Superphot+ and Villar methods sections in full.
2. **D4 shape record**, schema `domain_manifest.decision_shape`. Rule all four roots in one pass, with subtype-level gates and the alternatives field.
3. **Re-register under the chosen root.**
   - New unit, bands and P3 counts (refusal 6).
   - Contamination recounted as "published fit exists for this object".
4. **One-case pilot** per §4, after R1.
5. **Module V** scoped to the shape record's ruling-bearing numbers only, to stay inside the 15% cap.

## 6. Skill defect carried into the new version
`fm-advantage-benchmark-with-shape/scripts/queue.py` still crashes with `ZeroDivisionError` in `ibeta` at large n (reproduced: `--counted 11183 --passed 7154 --survivors 7154 --target 100`). The wave-2 log-space patch (`astronomy/wave2/agent5_skill_maintenance/patches/01`) has not been applied upstream.
