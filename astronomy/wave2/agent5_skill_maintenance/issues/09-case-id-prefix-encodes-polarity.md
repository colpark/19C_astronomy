# Case ids reveal polarity: every K case must fire and every N case must not

**Status:** ready-to-file draft (not filed). **No patch.** The fix is blocked, as explained below.
**Found by:** agent 5, wave 2, while preparing polarity-stripped `cases_blind.csv` files.
**Affected files:** `fm-advantage-benchmark/cases/cases.csv` and `cases/RULINGS_SEALED.csv`, both keyed by `case_id`. `astronomy/replay/cases/cases.csv` is partly affected too.

## Minimal repro

`repro/id_leak_check.py` groups rows by the alphabetic prefix of `case_id` and checks whether each prefix maps to a single polarity. It prints only aggregates and never shows a per-case polarity.

```
$ python3 astronomy/wave2/agent5_skill_maintenance/repro/id_leak_check.py fm-advantage-benchmark/cases/cases.csv
fm-advantage-benchmark/cases/cases.csv: 38 rows, 2 alphabetic id prefixes
  every prefix maps to a single polarity: True
  prefixes that each map to one polarity: ['K', 'N'] ; mixed: []
$ python3 astronomy/wave2/agent5_skill_maintenance/repro/id_leak_check.py astronomy/replay/cases/cases.csv
astronomy/replay/cases/cases.csv: 20 rows, 2 alphabetic id prefixes
  every prefix maps to a single polarity: False
  prefixes that each map to one polarity: ['ASTC'] ; mixed: ['AST']
```

## Expected vs actual

**Expected.** A stage under test that sees only `case_id`, `stage` and `input` cannot infer polarity.

**Actual.**
- **Source suite.** The id prefix fully determines polarity. The file order also groups the K cases before the N cases, apart from the later discovery block.
- **Effect.** Patch 04 removes the polarity column, but `emit` still prints `--- K06` and `--- N10`, so the answer can still be read off the id.
- **Astronomy suite.** The `ASTC` prefix covers the two coordinator controls, and both carry one polarity. The astronomy evaluator's `blind_inputs.csv` kept the original ids (`replay/RESULT.md`).

## Root cause

The ids use a K/N naming convention: "kill" or "must-fire" against "not". The ids also serve as the join key to the sealed rulings.

## Proposed fix

1. **Re-key.** The holder re-keys every case to an opaque id and keeps the mapping. `emit` and any blind file then use the opaque ids.
2. **Shuffle.** The holder shuffles row order with a seed the holder draws.
3. **Document.** Add one line to `replay.md`: "Case ids and row order must not encode polarity."

## Why there is no patch

- **The fix needs the rulings file.** Re-keying the suite means rewriting `cases/RULINGS_SEALED.csv` so its keys match the new ids. This agent is not permitted to open that file.
- **A diff would leak.** A diff that renames ids in `cases.csv` would also carry the polarity column in its context lines.
- **Status.** Blocked on the rulings holder, which was not supplied. **UNDEMONSTRATED.**

## What was done instead (run)

**Blind files built.** `repro/make_blind.py` built a polarity-free file for each suite with opaque ids (`FMB-NN`, `ASTB-NN`) and rows shuffled with seed 20260916:
- `blind/fm-advantage-benchmark/cases_blind.csv`
- `blind/astronomy_replay/cases_blind.csv`

**Checks on the blind files.** Header is `case_id,stage,sealed,input`. No input matches `must[ _-]?(not[ _-]?)?fire|polarity`. No input mentions an original-style id (`logs/blind_fm.json`, `logs/blind_ast.json`).

**Id maps.** The maps back to the original ids are in `holder_handover/` and hashed in `transfer_record.json`. For the source suite a map is equivalent to polarity, because original ids reveal it. It stays under procedural custody until a holder exists.

## Controls for the eventual fix

- **Must fire:** `id_leak_check.py` run on the re-keyed file together with its polarity reports `every prefix maps to a single polarity: False`, or reports a single prefix covering both polarities.
- **Must not fire:** `replay.py score` over the re-keyed ids returns the same must-fire and must-not-fire tallies as the original ids for the same verdicts. The holder has to run this, because it needs the joined polarity.
