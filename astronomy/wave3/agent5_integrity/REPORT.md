# Wave 3 · Agent 5 (integrity)

> Agent 5 returned this report as text, because the harness blocks subagents from writing REPORT.md files. The coordinator saved it here without changing its substance. The full step log with hashes is in `order_of_operations.log`.

**Checks run before any work:**
- Brief hash verified: `a618d911…c4b6`.
- No git was run.
- `fm-advantage-benchmark/` was not touched.
- Neither RULINGS_SEALED.csv file was opened; both were only hashed.

**Disclosure (log step 0c).** While looking for the wave-1 baseline, I printed `astronomy/replay/evaluator/score_all.txt`. That committed file lists every astronomy case together with its polarity, so polarity for this suite can be read from the repo without `cases.csv`. The evaluator prompt now forbids that directory.

## 1. Opaque-id re-issue: PASS

**The wave-2 blind files fail the wave-3 spec, so both suites were regenerated.** No correlation was detected (p ≥ 0.31), but the old files had two problems:
- The ids carry suite prefixes (`FMB-`, `ASTB-`) and are row counters.
- The agent chose the seed itself (20260916).

**The id rule was hashed before any id existed** (`OPAQUE_ID_RULE.md`, step 1):
- **Seed:** `int(sha256("<brief sha256>:<suite>:<attempt>"))`, so it is not agent-chosen.
- **Ids:** 10 random hex digits, with no prefix or counter.
- **Order:** rows are sorted by id.
- **Overlap:** the two suites share no ids.
- **Acceptance test:** permutation tests of polarity vs position, original order vs position, and author vs position (astronomy suite only). Any p < 0.05 rejects the attempt.

**Attempt 0 passed for both suites:**

| Suite | polarity p | original order p | author p |
|---|---|---|---|
| fm | 0.78 | 0.21 | — |
| astronomy | 0.90 | 0.22 | 0.11 |

- No text contains polarity words or old ids.
- Regenerating produces byte-identical files.

**Outputs:**
- `suites/fm-advantage-benchmark/cases_opaque.csv` (`9fe1e3d4…`, 38 rows)
- `suites/astronomy_replay/cases_opaque.csv` (`5a6991e4…`, 20 rows)
- Maps and polarity files are in `holder_handover/` (gitignored).

**Limit.** The rule inputs are public, and the case text matches `cases.csv` word for word. The ids therefore protect only against an evaluator who reads nothing but the blind file. The seal stays procedural.

## 2. Transfer package (ruling 4): PENDING_RECEIPT

`transfer_record.json` has status PENDING_RECEIPT and an empty `receipt_hash`. It lists six files:

| File | sha256 |
|---|---|
| astronomy RULINGS (hash only) | `6041714a…e2fc` |
| fm RULINGS (hash only) | `69a30ccf…c312` |
| astronomy polarity | `ff84a240…af35f` |
| fm polarity | `d0f89b30…853d` |
| astronomy map (wave 3) | `be5cb314…3971` |
| fm map (wave 3) | `56127599…0ebc6` |

**Checks and supporting files:**
- The polarity hashes match wave 2's canonical hashes.
- `transfer/PACKAGE_SHA256SUMS` (`f2576e62…`) verifies with `sha256sum -c`.
- `transfer/RECEIPT_TEMPLATE.txt` is the holder's receipt; its hash becomes `receipt_hash`.
- The record contains 8 verification steps for the holder.
- The authorship check is recorded as the PI's assertion. Neither the coordinator nor the agent verified it.
- The wave-2 maps are marked superseded.

**Leaks this package does not close:**
- Polarity is still in both `cases.csv` files and in git history.
- The committed `score_*.txt` files still list per-case polarity.
- The source K/N ids are still in place.

## 3. Re-score preparation: PASS as prepared; measurement UNDEMONSTRATED

**Blind input.** `evaluator/blind_inputs_opaque.csv` (`c02f6bf1…`) has 20 rows and only the columns `opaque_id,stage,input`.

**Evaluator prompt.** `evaluator/EVALUATOR_PROMPT.md`.
- **Where its rules come from.** The wave-1 prompt text was not saved, so the rules were rebuilt from RESULT.md and REPLAY_PLAN §4.1–4.2.
- **Read scope.** The evaluator reads only SKILL.md, references/ and the blind file. It is explicitly barred from fm cases/, all of astronomy/ except the blind file, wave-2 files, git, the web, and recursive search.
- **Verdicts.** Keyed by opaque id in `verdicts_opaque.json`, and hashed.
- **Skill version.** Pinned to the unpatched version that wave 1 used, so the delta isolates the ids.

**`scripts/rescore.py`** runs these steps:
1. Hashes the verdicts before any join.
2. Checks the pinned hashes of the map, the vendored `replay.py` and the astronomy `cases.csv`.
3. Rejects original ids, unknown ids and malformed verdicts.
4. Maps verdicts back to case ids.
5. Runs the unchanged `replay.py score` in a temporary layout that has no rulings.
6. Reports polarity accuracy, the unearned count, and the delta against wave 1 (20/20, 2 unearned).

Per-case output goes only to `--outdir`.

**Tests** (`tests/rescore_tests.log`). Test artifacts that pair opaque ids with polarity sit in the gitignored `holder_handover/`.

| Test | Result |
|---|---|
| T1 dummy verdicts | 12/20 |
| T2 wave-1 verdicts re-keyed | 20/20, 2 unearned, delta 0 |
| T3 one verdict missing | 19/20, 1 missing |
| T4 original ids | refused, exit 2 |
| T5 unknown id | refused, exit 2 |
| T6 malformed verdicts | refused, exit 2 |
| T7 tampered map | refused, exit 2 |
| T8 stdout | no per-case polarity lines |

**Inflation measurement: UNDEMONSTRATED.** It needs the coordinator to launch the evaluator. Even then, the delta will mix the effect of the ids with run-to-run variation between evaluators.

## 4. Replay cases (`replay_cases.csv`; rulings in `replay_rulings.csv`)

| Case | Stage | Polarity | Source |
|---|---|---|---|
| W3A5-L1 | LADDER | must_fire | Turns that ended on "waiting for fold 4" or "waiting for C5", with nothing able to wake them (rung 6, then 7). Recorded only in the coordinator's message. The repo shows ParSNIP folds 0–3 and no fold 4 |
| W3A5-L2 | LADDER | must_not_fire | Agent 3's freeze waits on agent 2's label slot, which is a real dependency (preamble item 3) |
| W3A5-R1 | R1 | must_not_fire | R1→I1 compositions staged as PRE-I1 CALIBRATION, escalated, and ratified by ruling 3 with the edge left unweakened |
| W3A5-R4 | R4 | must_fire | PARTLY SYNTHETIC. The blocked history rewrite is real (SYNTHESIS §10); the second rewrite plan is invented |

- An audit of these four cases alone shows 1 must_fire and 1 must_not_fire in each module.
- The audit reports "nothing sealed", which is expected because the holder assigns seals.
- The holder should re-key these ids.

## Still blocked
- The out-of-band handover needs a human.
- The coordinator has to launch the evaluator.
- Polarity is still readable in the working tree, git history and `score_*.txt`.
