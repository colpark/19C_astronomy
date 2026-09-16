# Skill amendment draft: two stage-owned refusals for P2

**Status:** DRAFT, NOT RATIFIED, NOT VERIFIED BY REPLAY. The text is written and applies cleanly as a patch. The verification run it requires (below) has not happened.
**Stage:** P2 prior floor estimate, in `references/stages/supply.md`.
**Patch:** `patches/P2-supply-refusals.patch`. It applies alone and in series to a pristine copy (`logs/patch_apply.txt`), and `replay.py audit` on the patched copy prints `suite shape ok`.
**Cause (amendment ledger):**
- `astronomy/replay/RESULT.md` item 3 and SYNTHESIS §7 item 6 / §11 record two unearned passes in the astronomy replay, AST-P2-04 (development) and AST-P2-02 (sealed).
- Both were caught only through global refusal 1 (provenance).
- `references/replay.md` says "A validator-only pass means the stage has no refusal of its own, and the case converts into one."

## The two refusals (text as patched)

> **Refuses a floor/ceiling pair** unless both were scored on the same items, the same split and the same metric, and neither was selected, tuned or thresholded on the items it is scored on. In the astronomy replay a spectrum classifier was priced at 0.90 against 0.53 on the 1,016 spectra used to choose its architecture and epoch, while a 1,011-spectrum held-out set existed (AST-P2-02). A floor with no matched ceiling is not a pair. State the floor and record its share UNDEMONSTRATED.
>
> **Refuses a floor built on features that exist only after the governed decision.** Check every input against the decision epoch in the manifest, never against the column name. In the astronomy replay a follow-up floor was stated as AUC 0.967 on redshift and absolute magnitude, which exist only for objects already classified; the same learner on peak magnitude, rise time and Galactic latitude gave 0.798, and at a first-alert epoch even peak magnitude post-dates the decision (AST-P2-04). Restate the floor on decision-time inputs, and report the post-hoc number beside it marked post-hoc.
>
> A refused pair or floor neither advances the stage nor closes the candidate.

The "Advances when" and "Closes the candidate when" lines now require a pair on which neither refusal fires. Without that, a floor that is priced post-hoc and "already takes the ceiling" would close a candidate. That is the regime agent 2 found in every literature pair (agent2 REPORT §4: "Their 0.95–1.00 shares describe a regime where the floor is already saturated").

## Controls

`references/replay.md` "Extending" sets two requirements. One control per refusal must derive from a real prior failure. Must-not-fire cases must be added at the same rate as refusals.

| Refusal | Must fire (real prior failure) | Must not fire |
|---|---|---|
| (i) unmatched or tuning-set pair | **AST-P2-02**, existing astronomy case, sealed. Input column only read: the classifier and both comparators were scored on the 1,016 spectra used to choose architecture and epoch, a 1,011 held-out set exists, and a stronger template tool was not run. | **W2A5-P2-N1**, marked SYNTHETIC: the repaired form of AST-P2-02. The same items, split and metric are used, selection happens on a disjoint set, and spectra exist at the governed decision. |
| (ii) post-decision features | **AST-P2-04**, existing astronomy case, development. Input column only read: a follow-up floor at AUC 0.967 on peak absolute magnitude and redshift, where redshift exists only for classified objects. | **W2A5-P2-N2**, real: agent 2's first-alert floor. Galactic latitude only, both declared learners reported (0.537 and 0.510), grouped CV, no ceiling claimed. |
| (i), second must-fire (real, found this wave) | **W2A5-P2-K1**: the BTSbot Table 6 pair (metadata-only 91.2% against multimodal 93.0% bts_p2 purity on the test split). Its ceiling was chosen as "the trial which yields the best test split performance" (arXiv:2401.15167 §4.1, source txt line 660). The pair is therefore scored on the split used to select its ceiling. | (covered by N1 and N2) |

The new cases are in `amendments/P2_controls_cases.csv`. Their rulings are in a separate file, `amendments/P2_controls_rulings.csv`.

Notes on the controls:
- **AST-P2-02 can fire through both refusals.** For a decision about which transients receive a spectrum, a spectrum classifier's inputs exist only after that decision. The expected verdict is `fired=true, via=stage`, with either refusal named.
- **W2A5-P2-K1 matters for the panel record.** Wave 1's REPLAY_PLAN row K06 treated the same Table 6 pair as a usable floor share of 98.1%. Under refusal (i) that share is refused. Agent 5 read the paper in full this wave: 1,601 lines, sha256 `4c053f1b72692917a8454b8590abce5de7ab3d6891f5b12c8e3a6da746d6d67a`.
- **The K1 case has one ambiguity.** Appendix A (line 1290) says the production model "is selected by considering best performance in policy-based metrics", and does not name the split there. §4.1 names the test split. The paper does not say how the metadata-only network's reported model was chosen, and the case input says so.
- **W2A5-P2-N2 may be contested.** A strict evaluator could object to the excluded unclassified objects. The ruling assigns that objection to P3 (unprocessable units), not to P2.
- **W2A5-P2-N1 is synthetic**, so by replay.md it carries less weight. No real matched pair on held-out data at decision-time inputs was found in the material the panel read. Agent 2 reached the same conclusion in its REPORT §4: "FM headroom has to be measured on decision-time inputs. No one has done that." Replace N1 when I1 produces a real one.

## Files not opened

`astronomy/replay/cases/RULINGS_SEALED.csv` and `fm-advantage-benchmark/cases/RULINGS_SEALED.csv` were not opened. For AST-P2-02 and AST-P2-04, only the `input` column of `astronomy/replay/cases/cases.csv` was printed.

## How the amendment must be verified (not run)

1. **Apply the patch** to a copy of the skill: `patch -p1 < patches/P2-supply-refusals.patch`. This step was run, and the patch applies cleanly.
2. **Start a fresh blind evaluator.** It reads only the patched `SKILL.md`, the patched `references/`, and a blind input file. The file must hold AST-P2-02 and AST-P2-04 under opaque ids, mixed in with W2A5-P2-K1, W2A5-P2-N1, W2A5-P2-N2, and the other 18 astronomy cases as distractors. Use `blind/astronomy_replay/cases_blind.csv` plus the three new rows re-keyed. The evaluator has not read this amendment document or any rulings.
3. **Hash the verdict file** before anyone joins polarity.
4. **Expected results:**
   - AST-P2-02: `fired=true, via=stage`
   - AST-P2-04: `fired=true, via=stage`
   - W2A5-P2-K1: `fired=true, via=stage`
   - W2A5-P2-N1: `fired=false`
   - W2A5-P2-N2: `fired=false`
   - The other 18 astronomy cases: polarity unchanged from `replay/evaluator/verdicts.json`, so the change produces no new over-firing.
5. **Score** with `replay.py score`. Pass requires `validator-only 0` in the P2 rows, and must-fire and must-not-fire both at 100% in the supply module.
6. **The seal is not independent.** AST-P2-02 is sealed, but this panel wrote it, and its ruling holder was never supplied (`transfer_record.json`). A pass on it counts as a development pass. A holder needs new sealed P2 cases, written by someone who has not seen this document.

**Disposition:** amendment text PASS (applies, audit clean). Refusal behaviour UNDEMONSTRATED, because the blind evaluator has not been re-run.
