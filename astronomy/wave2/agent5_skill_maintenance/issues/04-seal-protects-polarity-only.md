# The replay seal leaves polarity readable: cases.csv carries it, `replay.py emit` prints it, and `score` judges on it alone

**Status:** ready-to-file draft (not filed).
**Affected files:**
- `fm-advantage-benchmark/scripts/replay.py` (sha256 `d63459c3b9b377480f0fdba7f612a1f156b94eec121d41259303cc23f14b0ce6`). Line 36 is the emit print. Line 59 is the pass/fail test, line 48 loads the rulings, and line 62 is the only use of the rulings.
- `fm-advantage-benchmark/references/replay.md`, lines 13-14 (the Files table).
- `fm-advantage-benchmark/cases/cases.csv`, the `polarity` column.

**Found by:** wave 1 agent 5 (REPLAY_PLAN §4.3), SYNTHESIS §7 item 4.
**Patch:** `patches/04-seal-polarity.patch`. It must be applied after patch 03, because both edit the Files region of replay.md. Applied alone to a pristine copy, its replay.md hunk fails (`logs/patch_apply.txt`).

## What the files say

```
references/replay.md:13:| `cases/cases.csv` | the stage under test |
references/replay.md:14:| `cases/RULINGS_SEALED.csv` | held out until the stage is finished |
scripts/replay.py:36:        print(f"--- {c['case_id']}  stage={c['stage']}  polarity={c['polarity']}")
scripts/replay.py:48:    rul = {r["case_id"]: r for r in csv.DictReader(open(RULINGS, newline=""))} if os.path.exists(RULINGS) else {}
scripts/replay.py:59:        ok = bool(got.get("fired")) == (pol == "must_fire")
scripts/replay.py:62:        note = "" if ok else rul.get(cid, {}).get("rule_it_rests_on", "")
```

## Minimal repro (pristine copy, `logs/seal_polarity_verification.txt`)

1. `emit` hands the stage under test its answer:

```
$ python3 scripts/replay.py emit --set development --stage P2 | head -1
--- K06  stage=P2  polarity=must_fire
```

2. Scoring works in full with no rulings file present, which shows the rulings file decides nothing. The pristine scratch copy was made without `RULINGS_SEALED.csv`. Dummy verdicts were used: `fired` is true when the first byte of sha256(case_id) is even, chosen without looking at polarity.

```
$ ls cases/
cases.csv
$ python3 scripts/replay.py score --verdicts dummy_verdicts.json --set all | grep -E "^(must_|[0-9]+ case)"
must_fire     13 of 25
must_not_fire 5 of 13
20 case(s) failed.
```

3. The case id also encodes polarity. That is a separate problem, filed as issue 09.

## Expected vs actual

**Expected.** Whatever decides pass or fail is withheld from the stage under test. replay.md tells readers to "have someone else hold the rulings file", on the understanding that the rulings file is the sealed material.

**Actual.**
- Polarity alone decides pass or fail (line 59). Polarity sits in the file that replay.md says the stage under test may read, and `emit` prints it for every case.
- A stage that echoes `polarity` scores 100% on both must-fire and must-not-fire.
- The sealed rulings file only annotates failures (line 62). The seal therefore protects explanation text, and nothing that is scored.

## Root cause

The design pairs a per-case label with the case input in a single file. The seal instruction covers only the rulings file.

## Proposed fix (as patched)

**1. `replay.py`**
- **`emit`** never prints polarity. When `cases.csv` still has a polarity column, it warns on stderr.
- **`load()`** takes polarity from `cases/POLARITY_SEALED.csv` when `cases.csv` has none. If that file is missing, `audit` and `score` exit with "polarity is held out … Only the rulings holder can audit or score."
- **New `split-polarity` subcommand.** It moves the column into `POLARITY_SEALED.csv` and rewrites `cases.csv` without it. It prints sha256 values only, never polarity, and refuses a second run.

**2. `replay.md`, Files table.** Add `POLARITY_SEALED.csv` as holder-only. Add a sentence stating that scoring reads polarity only, so the seal must cover polarity.

The patch deliberately does not ship a split `cases.csv`. A diff of that file would contain the polarity values. The holder runs `split-polarity` instead.

## Verification (run, `logs/seal_polarity_verification.txt`)

**After the patch, before the split: emit no longer prints polarity.**

```
$ python3 scripts/replay.py emit --set development --stage P2 2>&1 | head -2
WARNING: cases.csv carries polarity. The stage under test can read it, so the seal protects only ruling text. Run split-polarity and hand POLARITY_SEALED.csv to the rulings holder.
--- K06  stage=P2
```

**The split.**

```
$ python3 scripts/replay.py split-polarity   (in s4split)
f917e653659e548cbd11844e01545096ede78924860ae75fa6023747f2dcf437  cases/cases.csv
f6b2801b21052e07b1bb5268f7b59673cf0207c29fbf8f42311fa620e36971cd  cases/POLARITY_SEALED.csv
Hand POLARITY_SEALED.csv and RULINGS_SEALED.csv to the holder, then remove both from anything the stage under test can read.
[exit=0]
$ head -1 cases/cases.csv; head -1 cases/POLARITY_SEALED.csv
case_id,stage,sealed,input
case_id,polarity
$ python3 scripts/replay.py split-polarity   (second run must refuse)
cases.csv carries no polarity column, nothing to split
[exit=1]
```

**Scoring is unchanged.** The same dummy verdicts were scored on three copies: pristine, patched but not split, and patched and split. The stdout sha256 values are identical for `audit` and for `score` on the development, sealed and all sets:

```
audit orig exit=0 stdout sha256=b668299331b3459c
score --set development orig exit=1 stdout sha256=3a5e2a37ab61b081
score --set sealed orig exit=1 stdout sha256=6f00c3f52f927d1a
score --set all orig exit=1 stdout sha256=2ee2d9ec567863db
audit s4 exit=0 stdout sha256=b668299331b3459c
score --set development s4 exit=1 stdout sha256=3a5e2a37ab61b081
score --set sealed s4 exit=1 stdout sha256=6f00c3f52f927d1a
score --set all s4 exit=1 stdout sha256=2ee2d9ec567863db
audit s4split exit=0 stdout sha256=b668299331b3459c
score --set development s4split exit=1 stdout sha256=3a5e2a37ab61b081
score --set sealed s4split exit=1 stdout sha256=6f00c3f52f927d1a
score --set all s4split exit=1 stdout sha256=2ee2d9ec567863db
```

The exit code 1 comes from the dummy verdicts failing cases. It is the same across all three copies.

**With the polarity file held out, the stage under test can still emit but cannot audit or score.**

```
$ python3 scripts/replay.py emit --set sealed --module ladder   (s4split, POLARITY_SEALED.csv moved away)
--- N10  stage=LADDER
$ python3 scripts/replay.py audit
polarity is held out (cases/POLARITY_SEALED.csv absent). Only the rulings holder can audit or score.
[exit=1]
```

**The replay suite audit on the fully patched copy** prints `suite shape ok`, exit 0. The new warning goes to stderr (`logs/verification_after_series.txt`).

## Controls

| control | must |
|---|---|
| must fire: `emit` on the suite before the split | no `polarity=` in stdout; a warning on stderr |
| must fire: `audit` or `score` with polarity held out | exit 1 with the held-out message |
| must not fire: `score` with polarity available (either layout) | stdout byte-identical to the pristine script (verified above by sha256) |
| must not fire: `split-polarity` output | prints hashes only, no polarity value |

## Not demonstrated / limits

- **The case ids still leak polarity** in the source suite (issue 09). Until the ids are re-keyed, this patch does not fully blind `emit`.
- **Nobody ran the split on the real skill directory,** and nobody moved `POLARITY_SEALED.csv` to a holder. The holder was not supplied (see `transfer_record.json`).
