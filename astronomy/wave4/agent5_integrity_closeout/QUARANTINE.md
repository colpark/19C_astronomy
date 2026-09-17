# QUARANTINE: polarity leaks in the replay record (permanent)

Written by agent 5 in wave 4 (integrity close-out), 2026-09-17, under `astronomy/wave4/PANEL_BRIEF_WAVE4.md`, sha256 `8f101811…1b58`.

This file is a record and is not to be edited. A later change goes in a new dated section appended at the end.

**How it was built**
- **Content scan.** `scripts/leak_scan.py` covers every `.txt/.csv/.md/.json/.log/.py` file in the repository. It skips `.git/`, `code/`, `sources/`, `data_cache/` and both `RULINGS_SEALED.csv` files. The rules are:
  - R1: `replay.py score` listing lines
  - R2: a CSV `polarity` column
  - R3: `emit`'s `polarity=`
  - R4: a case id and a polarity on one line
  - R5: a verdict file of booleans `fired`
  - N1: a matching filename
- **Output.** `logs/leak_scan.json` gives path, sha256, rule and match count. It prints no matched line.
- **First commits.** `scripts/git_first_commit.py` reads the loose objects in `.git/objects` with zlib. It never runs git. The repository has no packfiles.
  - It walks the 29 commits reachable from HEAD `bf76f534128468c40c2cb2fae51dd5b20a4da8b5`.
  - For each flagged path it reports the earliest commit whose tree holds the path, and whether HEAD's tree holds it.
  - Output: `logs/git_first_commit.json`.
- **Working tree.** Every flagged tracked file is byte-identical to its HEAD blob, and each has exactly one blob version in history.
- **Remote.** `.git/logs/refs/remotes/origin/main` records 29 `update by push` entries to `origin` (`https://github.com/colpark/19C_astronomy.git`). The last one is `bf76f534…`. Every commit below has therefore already been pushed.
  - Repository visibility on GitHub was **not checked** (no network access).
- **Disclosure.** The first scan run did not skip the rulings files by name. The script read their bytes for regex counts and printed only counts. No content was viewed. The scanner was fixed and re-run (order_of_operations.log steps 2a–2b).

## Q1. Scoring outputs that list every case with its polarity (the quarantine target)

| Path | sha256 (working tree = HEAD blob) | Scanner rule × matches | First commit | First commit time (committer, UTC) | In HEAD tree |
|---|---|---|---|---|---|
| `astronomy/replay/evaluator/score_all.txt` | `d36137f1207ea4b4ebfc8d2776ee8a0711c36d0c04594f2c86261aea53649a05` | R1×20, R4×20 | `b50d5ca59c9c254a2bf17d981debb5c42d1d91eb` | 2026-09-16T17:52:21Z | yes |
| `astronomy/replay/evaluator/score_development.txt` | `8d6f23841c2d45e50ec987c3f76b0d8335e2ef5e04469ef23b19922ac266c6f6` | R1×14, R4×14 | `b50d5ca59c9c254a2bf17d981debb5c42d1d91eb` | 2026-09-16T17:52:21Z | yes |
| `astronomy/replay/evaluator/score_sealed.txt` | `51d051625d273a57f6b1377a33e3c67405a0a7584c05b3417a11ed8254e2051b` | R1×6, R4×6 | `b50d5ca59c9c254a2bf17d981debb5c42d1d91eb` | 2026-09-16T17:52:21Z | yes |

- **What leaks.** One line per astronomy case: `<case_id> <stage> must_fire|must_not_fire ok|FAIL`. Across the three files this covers all 20 wave-1 astronomy cases. Development has 14, sealed has 6, and `score_all.txt` has all 20.
- **The seal it defeats.** Anyone who reads one of these files knows the polarity of every sealed case. That is exactly what `SEAL_SHA256SUMS` and the transfer were meant to protect.

## Q2. Verdict files that equal polarity because their run scored 100%

| Path | sha256 (working tree = HEAD blob) | Scanner rule × matches | First commit | First commit time (committer, UTC) | In HEAD tree |
|---|---|---|---|---|---|
| `astronomy/replay/evaluator/verdicts.json` | `c2a6d4904b17f4c11ce7b4e240cbc58d39feb2c4441a83f37443cf2aa93a1dcc` | R5×20 | `b50d5ca59c9c254a2bf17d981debb5c42d1d91eb` | 2026-09-16T17:52:21Z | yes |
| `astronomy/wave3/agent5_integrity/evaluator/verdicts_opaque.json` | `131a6ad4988c4b1fa509da73b9e2daba97615ec39b793ab9d274cb459e9a5d38` | R5×20 | `20391f6680e9741125d497f53b20e4eb5c5f6ef9` | 2026-09-16T20:26:39Z | yes |

- **Wave 1.** `astronomy/replay/evaluator/verdicts.json` scored 20 of 20, so each `fired` value equals `must_fire`.
- **Wave 3.** `verdicts_opaque.json` also scored 20 of 20 (`evaluator/RESULT_ISSUE09.md`). Its `fired` values give polarity by opaque id. The blind input text matches `cases.csv` verbatim, so these values can be mapped back to original case ids without the id map.

## Q3. Suite sources that carry a `polarity` column by design

| Path | sha256 (working tree = HEAD blob) | Scanner rule × matches | First commit | First commit time (committer, UTC) | In HEAD tree |
|---|---|---|---|---|---|
| `astronomy/replay/cases/cases.csv` | `60782b6b097dd505ed7242c7fb84b7c16323f4204c7d6fb6c4615954c4b6ca74` | R2×1, R4×20 | `8b01d130157ed2b6dbdb655a6fd50852a265d194` | 2026-09-16T17:50:01Z | yes |
| `fm-advantage-benchmark/cases/cases.csv` | `194b911c810f4e28a221048a12d9a7a2ea717df0b20177c45d5fdf03246cf561` | R2×1, R4×38 | `fd68058e04c4ecc0fe89d053f5b465cab54bc8a0` | 2026-09-16T17:11:29Z | yes |
| `astronomy/agent1_supply_corpus/replay_cases.csv` | `02f837817ee1c928cef5a9320e72fe551c7538aba714e9b1b21367e4a1e79480` | R2×1, R4×4 | `6c635168b989c1039e11566909cb8462ef99885c` | 2026-09-16T17:27:27Z | yes |
| `astronomy/agent2_floor_headroom/replay_cases.csv` | `c4d6f13c4fb71f619179a64f5252b3954f6f88c0fb38a76c66a0978d210a69c5` | R2×1, R4×4 | `6c635168b989c1039e11566909cb8462ef99885c` | 2026-09-16T17:27:27Z | yes |
| `astronomy/agent3_labels_exposure/replay_cases.csv` | `c247631f88ddcc61a881af2fc965194128ac95d42df6860174560764f8a4b5df` | R2×1, R4×4 | `3422302f2c7640c8cbff3c11d942042bf411775b` | 2026-09-16T17:31:02Z | yes |
| `astronomy/agent4_tools_instrument/replay_cases.csv` | `0703c404feb2d6a61b5d387ea7a9450bf2382b182bb1f7de3f58e167521d23ed` | R2×1, R4×4 | `6b0812ee6ca22fdaeb3ed2c0d5e77e7bed230f2b` | 2026-09-16T17:48:58Z | yes |
| `astronomy/agent5_resolution_replay/replay_cases.csv` | `0604180b98e4eec3987418e880e9063543f16b85eadd78a083e1664f0f0ca850` | R2×1, R4×4 | `e3bf69670399ad4b77e0fe796bc8f83f43a1a10a` | 2026-09-16T17:33:19Z | yes |
| `astronomy/wave2/agent1_rubin_bands/replay_cases.csv` | `fcf713bec874691fccc21cd35af737a6f73710d6edc3eb73cd48c33a07a6f3ca` | R2×1 | `75446f4a5bdca9294fa8073c9de57e6a141fe0aa` | 2026-09-16T19:54:17Z | yes |
| `astronomy/wave2/agent2_label_source/replay_cases.csv` | `120852f4d804304a186ce20dc6ecbc12361b940bcd067689ea325f26fc640c5f` | R2×1 | `9dc77efa140a837491f97ca49883cd1a824a917e` | 2026-09-17T00:05:15Z | yes |
| `astronomy/wave2/agent4_instrument/replay_cases.csv` | `f7cc2fae2fb016973c835a7ab356ff54a74411c41e658281efc51d7c4bf6a3e9` | R2×1 | `f8982949790daf45e321852cbef5a4aaa0b2f148` | 2026-09-16T20:46:39Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/replay_cases.csv` | `80a2d28a637400a98f7455a087e22bf67b75ff48774cda37cab0b80fbac51a63` | R2×1, R4×4 | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/amendments/P2_controls_cases.csv` | `dea27a0ff2e0414de8936d2e75dce7c830e34e7e1d8a87637ac2884dd99df1ab` | R2×1, R4×3 | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave3/agent1_cohort_finish/replay_cases.csv` | `abc5783d07cac41d8e7480daac3e4f1ff4adc55532954da001d210958b39421e` | R2×1 | `f2f7424566eb64df1cd73aa8b8b507c7535459e1` | 2026-09-16T21:29:51Z | yes |
| `astronomy/wave3/agent2_measured_labels/replay_cases.csv` | `b405e6ef256963a2c1dce19dc9f4378d3eca0518a583d1b0f47c5d27ee7e32ea` | R2×1 | `74d012c2eeb35ed8ca65fe9d2d246f1de4df74b5` | 2026-09-17T03:58:18Z | yes |
| `astronomy/wave3/agent3_manifest_freeze/replay_cases.csv` | `27632acb877a8bcc1839b9f9368caba4c6daae1ee242e3a511cde644a1249439` | R2×1 | `8560c9fd5fcedb681c8aac78d1cdf626aa238c0e` | 2026-09-17T00:19:35Z | yes |
| `astronomy/wave3/agent4_tool_recount/replay_cases.csv` | `5edf578bdec7370c22a58d078daec82af32d648c460b30fac38fd39876ed2a95` | R2×1 | `630d0ae2e19aba74593eca0730bdac80b1fdd4f6` | 2026-09-16T21:42:48Z | yes |
| `astronomy/wave3/agent5_integrity/replay_cases.csv` | `15210846d30a03edfc1c6185332c3df3cd55f85aa811702cada685a3c85dd914` | R2×1, R4×4 | `883b6e628a42992d9fbbda9fb1b8fbad09d87ec7` | 2026-09-16T20:24:18Z | yes |

- **Two kinds of file.** These are the two suites' `cases.csv` and the per-agent `replay_cases.csv` files, which the brief's deliverable format requires. Their polarity is authoring data, not a scoring by-product.
- **What leaks.** The wave-1 `astronomy/agent*/replay_cases.csv` files hold the source rows of the merged astronomy suite, so they carry its polarity too. The case ids differ only where REPLAY_PLAN §3 prefixed them.
- **Not quarantined here.** Untracking suite sources changes the deliverable contract, so it is a coordinator/PI decision. Patch 04 from wave 2 (`split-polarity`) is the tooling path.

## Q4. Prose and rulings that name cases together with their polarity

| Path | sha256 (working tree = HEAD blob) | Scanner rule × matches | First commit | First commit time (committer, UTC) | In HEAD tree |
|---|---|---|---|---|---|
| `astronomy/SYNTHESIS.md` | `fd749aec24839f6c668350119c96932c6ef5127753661f254e4287c471459137` | R4×1 | `f2a27a1b817b73bf49e7e9abe9201feb1c9b4d43` | 2026-09-16T17:51:31Z | yes |
| `astronomy/agent1_supply_corpus/REPORT.md` | `83c671939d476e1ebdbee0e168f1639ab2bd2ecda24210425e20c29353ce2780` | R4×4 | `6c635168b989c1039e11566909cb8462ef99885c` | 2026-09-16T17:27:27Z | yes |
| `astronomy/agent4_tools_instrument/REPORT.md` | `f00eb338362e42388875d80b1e0ed484bb0ec073df2adab7260bc390107ea7c2` | R4×4 | `6b0812ee6ca22fdaeb3ed2c0d5e77e7bed230f2b` | 2026-09-16T17:48:58Z | yes |
| `astronomy/agent5_resolution_replay/REPLAY_PLAN.md` | `395d956b1d4cb5457f032ec14c8405d3d6495cb4ac38dc5b20fc17d11e9fc458` | R4×42 | `e3bf69670399ad4b77e0fe796bc8f83f43a1a10a` | 2026-09-16T17:33:19Z | yes |
| `astronomy/agent5_resolution_replay/REPORT.md` | `dc34bfcbc8f903bf3970a74cf6eb9f98a467f18794754e21994dbeca4a5b3c16` | R4×4 | `e3bf69670399ad4b77e0fe796bc8f83f43a1a10a` | 2026-09-16T17:33:19Z | yes |
| `astronomy/agent3_labels_exposure/replay_rulings.csv` | `683b4069be2b6b49ded9581b9b2cbf4e707f88edbeebf37c97681d180fca151b` | R4×1 | `3422302f2c7640c8cbff3c11d942042bf411775b` | 2026-09-16T17:31:02Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/REPORT.md` | `8f10ec6f0ef145e8ba28ad1d0f7bd81671aaa7d5562d2634d879d6f210afd7a7` | R3×1, R4×5 | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/issues/04-seal-protects-polarity-only.md` | `440384bf0fbbd1a08c079599ab876ec82e99abeae088b86861484fa0ab087f54` | R3×1, R4×1 | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/logs/seal_polarity_verification.txt` | `547f124d0f5e62dde6a32dd87acd61e77ffa709b49212119c5d52056bfca1051` | R3×1, R4×1 | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/replay_rulings.csv` | `e2e831b139988d43d546d2c91450013e7bf6337f6863ac6151a96d4cc810bf40` | R4×1 | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/amendments/P2_controls_rulings.csv` | `753e4f08a59602fa6d3c6317acabc2b4422f77201d4d4735981388d71abfedbd` | R4×1 | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave3/agent5_integrity/REPORT.md` | `b049b0e1d6208175a89c3848cb4172662405a825953eb1137171441a0e8eb5c0` | R4×4 | `883b6e628a42992d9fbbda9fb1b8fbad09d87ec7` | 2026-09-16T20:24:18Z | yes |

- **What leaks.** Case lists in reports and plans, for example REPLAY_PLAN.md's 38-row mapping table with its `pol.` column (42 matching lines). Also my own wave-2 and wave-3 case summaries, and the `emit` line `K06 … polarity=must_fire` quoted in wave-2 issue 04.
- **Not quarantined.** These are narrative records. They are listed so the forbidden-path list covers them (`**/REPORT.md`, `**/REPLAY_PLAN.md`, `**/issues/`, `**/logs/`, `**/replay_rulings.csv`, `**/P2_controls_rulings.csv`, `astronomy/SYNTHESIS.md`).

## Checked and clean (name matched, no polarity content)

| Path | sha256 (working tree = HEAD blob) | Scanner rule × matches | First commit | First commit time (committer, UTC) | In HEAD tree |
|---|---|---|---|---|---|
| `astronomy/replay/evaluator/blind_inputs.csv` | `6b97a4bcf6834cce8cb2f233716b41cdfad79fa5e73af3317d63e549f298bdd2` | name only | `8b01d130157ed2b6dbdb655a6fd50852a265d194` | 2026-09-16T17:50:01Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/blind/astronomy_replay/cases_blind.csv` | `ae6b7cf5acc35411bd477986bcd54dd15772c2011b1b082bf7ecf28d365adc96` | name only | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/blind/fm-advantage-benchmark/cases_blind.csv` | `4f9d5aa9d179494b13d9c38bc58e9674b083cbeba3d4856252dffda63302e777` | name only | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave3/agent5_integrity/evaluator/blind_inputs_opaque.csv` | `c02f6bf134c05327d4c311649246d18bf60ebafef9298689bbdfcdf3c49bd47b` | name only | `883b6e628a42992d9fbbda9fb1b8fbad09d87ec7` | 2026-09-16T20:24:18Z | yes |
| `astronomy/wave3/agent5_integrity/suites/astronomy_replay/cases_opaque.csv` | `5a6991e4a62446bfb325b1789910a2852484ab62320f6a3bd894ff935e55c128` | name only | `883b6e628a42992d9fbbda9fb1b8fbad09d87ec7` | 2026-09-16T20:24:18Z | yes |
| `astronomy/wave3/agent5_integrity/suites/fm-advantage-benchmark/cases_opaque.csv` | `9fe1e3d48ded7db4d37d631a31242747a89792459b7818c87ba8863604202c76` | name only | `883b6e628a42992d9fbbda9fb1b8fbad09d87ec7` | 2026-09-16T20:24:18Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/issues/09-case-id-prefix-encodes-polarity.md` | `022e77d0954f0a44f9a5f478e720d19c00c1f02b296613ddbb57e8156ccd787e` | name only | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |
| `astronomy/wave2/agent5_skill_maintenance/logs/dummy_verdicts.json` | `cb7cac726231d5bf6ae859112e0486109e88a4e689dc33614e15c32d8c6a16cf` | R5×38 | `808506e692ea92971a67106041d4ae0b73acd9f6` | 2026-09-16T19:10:37Z | yes |

- **Polarity-free by construction.** The blind input and opaque suite files. The wave-1 `blind_inputs.csv` still carries original ids (issue 09), but no polarity.
- **Scanner false positive.** `dummy_verdicts.json` matched R5, but its `fired` values come from a hash of the case id, not from polarity.

## Rulings files in history (hash only, never opened)

| Path | sha256 | First commit | First commit time (UTC) | In HEAD tree |
|---|---|---|---|---|
| `astronomy/replay/cases/RULINGS_SEALED.csv` | `6041714a30b9143ef6ea74edd3ed35dca86c51317d42a56d2b5204f559f2e2fc` | `8b01d130157ed2b6dbdb655a6fd50852a265d194` | 2026-09-16T17:50:01Z | yes |
| `fm-advantage-benchmark/cases/RULINGS_SEALED.csv` | `69a30ccffb4500135cad78e4c03ae7345aefd1583c0ac7dfd802db2eb8e1c312` | `fd68058e04c4ecc0fe89d053f5b465cab54bc8a0` | 2026-09-16T17:11:29Z | yes |

Both are tracked at HEAD and were pushed. That is the "same party" seal `references/replay.md` warns about. The handover is PENDING_RECEIPT (`custody_status.json`).

## Gitignored local matches (expected custody, not in git)

33 matches in gitignored local paths, under: `astronomy/wave2/agent5_skill_maintenance/scratch/`; `astronomy/wave3/agent5_integrity/holder_handover/`.

These are the wave-2 scratch copies of the skill, which include `cases.csv`, and the wave-3 `holder_handover/`, which holds id maps, polarity files and per-case re-score outputs. They are not in any commit: `.gitignore` covers `astronomy/**/scratch/`, `astronomy/wave3/agent5_integrity/holder_handover/` and `astronomy/wave4/**/holder_handover/`. That was checked by pattern; `git check-ignore` was not run.

## Which evaluations could have been exposed

| Evaluation | When | Q1 score files existed? | Other polarity sources present in the tree | What the evaluator was told | Exposure |
|---|---|---|---|---|---|
| Wave-1 blind evaluator, astronomy suite | between seal commit `8b01d130…` (2026-09-16T17:50:01Z) and verdict commit `b50d5ca5…` (17:52:21Z); exact launch time not recorded in the repository | **No.** They are produced by scoring its own verdicts and first appear in `b50d5ca5…` together with them | `astronomy/replay/cases/cases.csv` (polarity column, from `8b01d130…`); the wave-1 agent `replay_cases.csv` files and REPLAY_PLAN.md (from 17:27–17:48Z) | read only `SKILL.md`, `references/`, `evaluator/blind_inputs.csv` (RESULT.md) | possible, procedural; not verifiable |
| Wave-3 opaque-id evaluator, same suite | launched 2026-09-16T20:24Z; verdicts committed `20391f66…` at 20:26:39Z | **Yes**, since `b50d5ca5…`, in the working tree and pushed | all of Q2 wave 1, Q3 and Q4 as of `883b6e62…`; wave-2 blind files with original-order maps kept local | EVALUATOR_PROMPT.md v1 forbade `astronomy/replay/` including every `score_*.txt`; the evaluator reported opening no forbidden file | possible, procedural; not verifiable; delta 0 cannot rule it out |
| Any future evaluator of either suite | from now | yes, unless untracked | everything above, plus Q2 wave 3 (`verdicts_opaque.json`) | EVALUATOR_PROMPT_v2.md + `evaluator_prompt_forbidden_paths.txt` | the same unless the files are removed from reach; history stays readable |
| Source suite (38 cases) in this repository | no evaluation run here | n/a | `fm-advantage-benchmark/cases/cases.csv` with polarity since first commit `fd68058e…` (2026-09-16T17:11:29Z), ids K/N encode polarity (issue 09) | n/a | the source suite has never had a blind evaluation in this repository |

The evaluators were the same model family as the panel, and their file access was self-reported. For every row, "not exposed" is undemonstrated.

## Why moving or untracking the files does not unleak them

1. **History keeps them.** `git rm --cached` or `mv` removes a file from future commits only. Every commit listed above keeps its blob, and `git show b50d5ca5:astronomy/replay/evaluator/score_all.txt` would still print it. The blob ids are in `logs/git_first_commit.json`.
2. **The history is already pushed** to `origin` (29 pushes, the last at `bf76f534…`). Every clone, fork, CI cache and GitHub's own views of those commits keep the files, whatever happens locally.
3. **A history rewrite does not reach existing copies.** It changes commit ids for everyone downstream, and it needs a force push. The permission layer blocked the last rewrite attempt (`astronomy/SYNTHESIS.md` §10). It also cannot recall copies already fetched.
4. **The information exists outside the files.** Polarity is recoverable from `cases.csv` in every commit, from the per-agent `replay_cases.csv` files, from the source suite's K/N ids, and from any 100%-accurate verdict file. Untracking Q1 closes the most convenient channel, not all of them.
5. **So what is left is procedural.** Quarantine limits what a future evaluator is likely to meet in the working tree, and the forbidden-path list tells it what not to read. Neither makes past or future seals on these two suites independent. A seal that carries weight needs new cases, written and held outside this repository by the holder (`references/replay.md`, "The limit that matters").

## Commands the coordinator would run (not run by agent 5; syntax not executed)

Nothing below has been run. The coordinator decides.

**A. Untrack and move the Q1 score files and Q2 verdict files to the holder side.** This leaves history unchanged and does not need PI approval under the current rules.

```bash
cd /home/aid1/Documents/4_19C_astronomy/repo
Q=astronomy/wave4/agent5_integrity_closeout/holder_handover/quarantine
mkdir -p "$Q/astronomy/replay/evaluator" "$Q/astronomy/wave3/agent5_integrity/evaluator"
cp -p astronomy/replay/evaluator/score_all.txt astronomy/replay/evaluator/score_development.txt \
      astronomy/replay/evaluator/score_sealed.txt astronomy/replay/evaluator/verdicts.json \
      "$Q/astronomy/replay/evaluator/"
cp -p astronomy/wave3/agent5_integrity/evaluator/verdicts_opaque.json "$Q/astronomy/wave3/agent5_integrity/evaluator/"
( cd "$Q" && sha256sum astronomy/replay/evaluator/score_all.txt astronomy/replay/evaluator/score_development.txt \
    astronomy/replay/evaluator/score_sealed.txt astronomy/replay/evaluator/verdicts.json \
    astronomy/wave3/agent5_integrity/evaluator/verdicts_opaque.json )
# compare the five hashes with the Q1/Q2 tables above before continuing
git rm --cached astronomy/replay/evaluator/score_all.txt astronomy/replay/evaluator/score_development.txt \
    astronomy/replay/evaluator/score_sealed.txt astronomy/replay/evaluator/verdicts.json \
    astronomy/wave3/agent5_integrity/evaluator/verdicts_opaque.json
rm astronomy/replay/evaluator/score_all.txt astronomy/replay/evaluator/score_development.txt \
   astronomy/replay/evaluator/score_sealed.txt astronomy/replay/evaluator/verdicts.json \
   astronomy/wave3/agent5_integrity/evaluator/verdicts_opaque.json
cat >> .gitignore <<'IGN'
# Wave 4 quarantine (astronomy/wave4/agent5_integrity_closeout/QUARANTINE.md): scoring outputs and verdict files stay holder-side
**/score_*.txt
**/verdicts*.json
IGN
git add .gitignore
git commit -m "quarantine: untrack polarity-listing score and verdict files (history unchanged; see QUARANTINE.md)"
# push only if the coordinator decides to: git push origin main
```

Effects to record if this is run:
- **Files that cite the moved paths.** `astronomy/replay/RESULT.md` and `astronomy/wave3/agent5_integrity/evaluator/RESULT_ISSUE09.md` cite them. Their hashes stay valid, and the files remain in the holder-side copy.
- **Scope of the new ignore rule.** It also covers the wave-2 `logs/dummy_verdicts.json` pattern for future files. Already-tracked files are unaffected.

**B. Optionally untrack Q3/Q4.** This needs a coordinator/PI decision because it changes deliverables. The mechanics are the same as A, per path.

**C. History rewrite: REQUIRES PI AND USER APPROVAL. Not recommended by agent 5. Previously blocked by the permission layer.**

```bash
# REQUIRES PI AND USER APPROVAL. Rewrites every commit id from fd68058e onward and needs a force push.
# Does not remove copies already cloned, forked or cached (see "Why moving ... does not unleak").
git filter-repo --invert-paths \
  --path astronomy/replay/evaluator/score_all.txt \
  --path astronomy/replay/evaluator/score_development.txt \
  --path astronomy/replay/evaluator/score_sealed.txt \
  --path astronomy/replay/evaluator/verdicts.json \
  --path astronomy/wave3/agent5_integrity/evaluator/verdicts_opaque.json
git push --force origin main   # REQUIRES PI AND USER APPROVAL
```

`git filter-repo` is a separate tool and may not be installed. Every hash-pinned record in this repository that cites a commit id would go stale.
