# Evaluator prompt v2: opaque-id replay evaluation

**v2 of** `astronomy/wave3/agent5_integrity/evaluator/EVALUATOR_PROMPT.md` (sha256 `7cea3975055e734b00c51b1cd7ae7a5249187ad8722024597d5e4b31b8db5272`). Written in wave 4 by agent 5 under the quarantine in `QUARANTINE.md`. Nothing else changed from v1 except these three items.
1. The forbidden-path section is replaced by the canonical list, verbatim.
2. The verdict file is written under a gitignored `holder_handover/` path, never next to the blind inputs. The wave-3 verdict file was committed and matches polarity 20 of 20 (QUARANTINE.md Q2).
3. Scoring follows `holder_side_scoring_protocol.md`.

The old v1 title was: Evaluator prompt: wave-3 opaque-id re-score of the wave-1 astronomy replay

Everything below the line is the exact text the coordinator gives a fresh evaluator session. Do not add context, excerpts or summaries from any other file.

**Provenance of these rules**
- The wave-1 evaluator prompt was not saved in the repository.
- The rules below are rebuilt from `astronomy/replay/RESULT.md` ("Stage under test" paragraph: read only `SKILL.md`, `references/` and the blind inputs file; polarity and rulings withheld; rows shuffled).
- They also draw on `astronomy/agent5_resolution_replay/REPLAY_PLAN.md` §4.1 (the stage under test has no access to `astronomy/agent*/`, rulings, or panel transcripts) and §4.2 (verdict format and hashing).
- There are two intended differences from wave 1:
  - The ids are opaque.
  - The forbidden list names every place in the repository where polarity for this suite can now be read.

**Launch conditions for the coordinator**
- The session must be fresh: no panel transcript and no wave context.
- The session must not be one of the panel agents.
- Record the model and the launch time in the order-of-operations log.
- Before launch, check that these files still have the hashes listed here:

| File | sha256 |
|---|---|
| `fm-advantage-benchmark/SKILL.md` | `e673042d61499657bcebad3ba68c8910a518dd69478fcf06f830ef5a314eafba` |
| `fm-advantage-benchmark/references/graph.md` | `03b495bff2535295591c5941be1a4126d29c7b486dc9f14f02040946409cdcee` |
| `fm-advantage-benchmark/references/loop.md` | `bce6e18f23132355a293d1596a788c916b942b60917ce8ef80b5b37fa17665d4` |
| `fm-advantage-benchmark/references/manifest.md` | `3c26242b2ad3e2fa3e812bc0e46c9dba16ffbc4f2cc86789e09a42a1e139ae68` |
| `fm-advantage-benchmark/references/provenance.md` | `ca92404318db1eccf6ec18cdfd5c1ea76511887e8d32d76aaa4c81b42f45574b` |
| `fm-advantage-benchmark/references/replay.md` | `046fe64b2174f5a2cb6b1ea5b55163706ba21627e9275b808e25aaaa09e2687d` |
| `fm-advantage-benchmark/references/stages/adjudication.md` | `6d804d4055b1fa1651dce02e8e0b08cc1a549814f11ae3e5613627569ca98b58` |
| `fm-advantage-benchmark/references/stages/discovery.md` | `0b707be2a10075d7312f6f7237f33907756a3aea16e4fb0d0e694dafa4da4fc2` |
| `fm-advantage-benchmark/references/stages/instrument.md` | `1a681c09ff80a1d768acec07bb8f6238541a6cdd61f9139c7a15111c65de1cb9` |
| `fm-advantage-benchmark/references/stages/runtime.md` | `e109a57f1b8114d8f920806c1d40ed42457e50509b588d438e2acf0704172019` |
| `fm-advantage-benchmark/references/stages/supply.md` | `c49dfac26754d6e66e1bd0e75fe9a7ac2829e5d4e6524c09cab8b2384186f0bd` |
| `astronomy/wave3/agent5_integrity/evaluator/blind_inputs_opaque.csv` | `c02f6bf134c05327d4c311649246d18bf60ebafef9298689bbdfcdf3c49bd47b` |

The skill files are the unpatched vendored skill, which is the version wave 1 ran against. None of the wave-2 patches (including the P2 amendment) is applied. Applying them would change two things at once, and the delta would stop measuring the ids alone.

---

You are the stage under test for a replay of the fm-advantage-benchmark skill. Repository root: `/home/aid1/Documents/4_19C_astronomy/repo`.

## You may read only these files

1. `fm-advantage-benchmark/SKILL.md`
2. every file under `fm-advantage-benchmark/references/`
3. `astronomy/wave3/agent5_integrity/evaluator/blind_inputs_opaque.csv`

## You may not read, list, search, or run anything else

The canonical forbidden list follows. It is copied verbatim from `astronomy/wave4/agent5_integrity_closeout/evaluator_prompt_forbidden_paths.txt`. There are two exceptions. You may read the one blind input file named above. You may write your own verdict file at the path given under Output, and hash it with `sha256sum`.

```
.git/
fm-advantage-benchmark/cases/
fm-advantage-benchmark/scripts/
fm-advantage-benchmark/schemas/
astronomy/replay/
astronomy/agent1_supply_corpus/
astronomy/agent2_floor_headroom/
astronomy/agent3_labels_exposure/
astronomy/agent4_tools_instrument/
astronomy/agent5_resolution_replay/
astronomy/SYNTHESIS.md
astronomy/PANEL_BRIEF.md
astronomy/wave*/  (every file except the single blind input file named in the prompt)
**/holder_handover/
**/scratch/
**/score_*.txt
**/verdicts*.json
**/rescore_summary*
**/RESULT*.md
**/REPORT.md
**/REPLAY_PLAN.md
**/PANEL_BRIEF*.md
**/cases.csv
**/cases_blind.csv
**/cases_opaque.csv
**/blind_inputs.csv
**/replay_cases.csv
**/replay_rulings.csv
**/P2_controls_cases.csv
**/P2_controls_rulings.csv
**/RULINGS_SEALED.csv
**/POLARITY_SEALED.csv
**/polarity_*.csv
**/id_map_*.csv
**/issues/
**/amendments/
**/logs/
**/order_of_operations.log
git log, git show, git diff, git blame, git grep, or any other command that reads repository history
recursive search or listing over the repository (grep -r, rg, find, ls -R, globbing across directories)
the network: web search, web fetch, package indexes, GitHub, or any remote copy of this repository
any transcript, message or summary from a panel agent or the coordinator
```

If you open a forbidden file by mistake, stop, say which file it was, and write no verdicts.

## Task

`blind_inputs_opaque.csv` has 20 rows with columns `opaque_id`, `stage` and `input`. For each row:

1. Read the stage brief for `stage` (under `references/stages/`), plus any global refusal in `SKILL.md` or `references/` that applies.
2. Decide whether a refusal of the skill **fires** on the situation in `input`. Here, "fires" means the skill refuses or blocks the action or number the input proposes. "Does not fire" means the skill accepts it and work proceeds.
3. Judge each row on its own. The ids and the row order carry no information.
4. Record `via`:
   - `"stage"` when the owning stage's own refusal or advance rule decides it
   - `"validator"` when only a global refusal (for example refusal 1, the five provenance fields) catches it, and the stage brief itself has no rule that would

## Output

Write exactly one file, `astronomy/wave4/agent5_integrity_closeout/holder_handover/verdicts/verdicts_opaque_<RUN_ID>.json`, where the coordinator fills in `<RUN_ID>` before launch. The path sits under a gitignored `holder_handover/`. Write it as one JSON object keyed by `opaque_id` with an entry for all 20 rows:

```json
{
  "<opaque_id>": {"fired": true, "ruling": "<one to three sentences: what the skill does next>", "rule": "<stage and/or global refusal number it rests on>", "via": "stage"}
}
```

`fired` is a JSON boolean. `via` is `"stage"` or `"validator"`. Write no other file.

Then run exactly one command and report its output:

```
sha256sum astronomy/wave4/agent5_integrity_closeout/holder_handover/verdicts/verdicts_opaque_<RUN_ID>.json
```

Do not run any scoring script, and do not try to find out whether you were right.

## End your reply with

1. The sha256 line.
2. The complete list of files you opened.
3. Either "I opened no file outside the allowed list" or the list of exceptions.
