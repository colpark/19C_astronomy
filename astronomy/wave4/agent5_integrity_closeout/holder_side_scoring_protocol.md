# Holder-side scoring protocol

**Status:** in force from wave 4 onward. Cause: `QUARANTINE.md` (Q1 and Q2).
**Applies to:** every replay evaluation of any suite in this repository, whoever runs it — the coordinator, the holder or an agent.

## Rule

Everything that pairs a case with its polarity, or that equals polarity once scored, is written **only** under a gitignored `holder_handover/` path. It is never committed, pasted into a REPORT, or printed into a log that gets committed.

The rule covers:
- `replay.py score` stdout (`score_*.txt`), which carries per-case `must_fire|must_not_fire ok|FAIL` lines
- `replay.py emit` output from an unpatched `replay.py`, which prints `polarity=`
- evaluator verdict files (`verdicts*.json`), including the raw file. It equals polarity whenever accuracy is high, and nobody knows the accuracy before scoring
- translated verdicts, id maps, polarity files, per-case rescore outputs (`scripts/rescore.py --outdir`)
- any table or list that places a case id (original or opaque) next to its polarity or its `fired` value

**Canonical location:** `astronomy/<wave>/<agent dir>/holder_handover/<run_id>/`.

**Gitignore coverage:** `.gitignore` already covers `astronomy/wave4/**/holder_handover/`, `astronomy/wave3/agent5_integrity/holder_handover/` and `astronomy/wave2/agent5_skill_maintenance/holder_handover/`. A new wave directory needs its own pattern. Add it before the first run, not after.

## What may be committed

- **Hashes:** the verdict file's sha256, recorded before any join; the sha256 of the score outputs; the sha256 of every input file.
- **Aggregates:** must_fire X of Y and must_not_fire X of Y per set and per module, the unearned (validator-only) count, missing verdicts, and the delta against a stated baseline.
- **Evaluator file access:** the evaluator's list of opened files and its disclosures.

`scripts/rescore.py` (wave 3) already prints only aggregates on stdout and writes per-case output to `--outdir`. Point `--outdir` under `holder_handover/`.

## Sequence for one evaluation

1. **Before launch:**
   - Add the `holder_handover/` pattern for the run directory to `.gitignore`, if it is not already covered. Confirm it with `git check-ignore -v <path>` (coordinator).
   - Check the pinned skill and blind-input hashes.
   - Build the prompt from `EVALUATOR_PROMPT_v2.md`. It must contain every non-comment line of `evaluator_prompt_forbidden_paths.txt` verbatim.
2. **Launch.** The evaluator writes `holder_handover/verdicts/verdicts_<run_id>.json` and reports its sha256. The coordinator recomputes the hash and logs it in `order_of_operations.log` before anything else happens.
3. **Score.** Run, holder-side:

   ```
   python3 <scripts>/rescore.py --verdicts <holder_handover verdict path> --outdir <holder_handover>/<run_id>/
   ```

   Add `--with-rulings` only when the holder runs it. Never run `replay.py score` with stdout going to a tracked file or into the terminal transcript of a panel agent.
4. **Record.** Commit only the aggregate line set and the hashes, for example a `RESULT_*.md` with no per-case table.
5. **Pre-commit check (coordinator).**
   - Run `astronomy/wave4/agent5_integrity_closeout/scripts/leak_scan.py` and look at every hit outside `holder_handover/` and `scratch/`.
   - Any new R1, R3 or R5 hit, or an R4 hit on a new file, blocks the commit until the file moves holder-side or is shown to be a false positive, as `dummy_verdicts.json` was.
   - Q3 suite sources and Q4 prose already on record are known and listed in `QUARANTINE.md`.
6. **Custody.** While `custody_status.json` reads PENDING_RECEIPT, every result carries the word "procedural".

## Non-goals

- This protocol does not unleak anything already committed or pushed (`QUARANTINE.md`, "Why moving or untracking the files does not unleak them").
- It does not make a seal independent. Only new cases written and held outside this repository by the holder can do that.
