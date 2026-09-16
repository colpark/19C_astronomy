# replay.md contradicts itself on the sealed count: "Twelve" vs "the nine" vs "sealed, 9 cases"

**Status:** ready-to-file draft (not filed).
**Affected file:** `fm-advantage-benchmark/references/replay.md` (sha256 `046fe64b2174f5a2cb6b1ea5b55163706ba21627e9275b808e25aaaa09e2687d`), lines 16, 33, 34 and 36.
**Found by:** wave 1 agent 5 (REPLAY_PLAN §4.3) and SYNTHESIS §7 item 5. This draft adds the line numbers, the probable origin of the nine, and one more wrong count (line 36).
**Patch:** `patches/03-replay-md-sealed-count.patch`.

## The quoted lines

Output of `grep -n` on the vendored file:

```
references/replay.md:16:Twelve cases are marked sealed. Develop on the other twenty-six. Open the nine once, then reseal.
references/replay.md:33:| development, 19 cases | 19 of 19 | a clean sweep usually means the suite is too easy |
references/replay.md:34:| sealed, 9 cases | 9 of 9 polarity, 2 unearned | two passed through a global refusal, not the stage |
references/replay.md:36:| discovery, development 7 | 7 of 7 | five of seven extracted from the record |
```

## Minimal repro: what the suite actually contains

Audit of a pristine copy (`logs/verification_after_series.txt`):

```
$ python3 scripts/replay.py audit
38 cases across 6 modules

module           must_fire  must_not_fire  sealed
adjudication             3              1       3
discovery                7              3       3
instrument               3              2       1
ladder                   1              1       1
runtime                  5              4       2
supply                   6              2       2

  suite shape ok
[exit=0]
```

The sealed column sums to 3+3+1+1+2+2 = **12**. `repro/suite_counts.py` on the pristine copy prints (`logs/suite_counts_before.txt`, first four lines):

```
rows 38 sealed 12 dev 26
non-discovery: total 28 dev 19 sealed 9
discovery: dev 7 sealed 3
discovery dev SYNTHETIC 3 discovery sealed SYNTHETIC 1
```

## Expected vs actual

**Expected.** Line 16 should match the file, which has 12 sealed and 26 development cases. Each table row should say which subset it counts.

**Actual.**
- Line 16 says twelve sealed and twenty-six development, which matches the file. In the same sentence, "Open the nine once" contradicts it.
- Lines 33-34 report "development, 19 cases" and "sealed, 9 cases" as if they covered the suite.
- Line 36 says "five of seven extracted from the record". `cases.csv` marks three of the seven development discovery cases SYNTHETIC, so four are extracted.

## Root cause (read from the counts; history not available)

19 + 9 = 28 is exactly the number of non-discovery cases, split exactly as they are split today. The likely cause is that the first executed pass ran before the ten discovery cases were added, and the prose "nine" was not updated when they arrived. That is an inference from the arithmetic: the skill arrived as a zip with no history. The "five of seven" count cannot be traced the same way. Either a case was relabelled SYNTHETIC after the pass, or the note is wrong.

## Proposed fix

- **Line 16:** change "Open the nine once" to "Open the twelve once".
- **Above the table:** add one sentence saying the 19/9 rows match the 28 non-discovery cases and the discovery rows count the other ten. It must not assert history that cannot be verified.
- **Rows 33-34:** label them "non-discovery".
- **Row 36:** change "five of seven" to "four of seven extracted from the record, three SYNTHETIC in cases.csv". If the maintainers hold a record showing five were extracted at the time, keep "five" and say when the relabel happened instead.

## Verification (run)

- `patch -p1` applies cleanly to a pristine copy, alone or in series (`logs/patch_apply.txt`).
- `python3 scripts/replay.py audit` on the patched copy prints the same table and `suite shape ok` (`logs/verification_after_series.txt`).
- `grep -n "nine\|twelve" references/replay.md` on the patched copy prints the lines below. The only "nine" left is in the new sentence that explains the 19/9 rows.

```
19:Twelve cases are marked sealed. Develop on the other twenty-six. Open the twelve once, then reseal.
33:The development and sealed rows count nineteen and nine, which matches the twenty-eight cases outside the discovery module in `cases/cases.csv`. The discovery rows count the other ten. The whole suite holds twenty-six development and twelve sealed.
```

## Controls

- **Must fire.** A consistency check comparing prose counts with the audit fails on the pristine line 16. This check was done by hand, not built as a script: the audit's sealed total of 12 does not match "nine".
- **Must not fire.** The same check passes on "Twelve cases are marked sealed. Develop on the other twenty-six": 12 sealed plus 26 development makes the 38 audited cases.
