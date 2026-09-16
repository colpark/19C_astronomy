# queue.py: ZeroDivisionError in the Clopper-Pearson interval from n = 1072

**Status:** ready-to-file draft. No upstream repository is known, so nothing was filed.
**Affected file:** `fm-advantage-benchmark/scripts/queue.py`. `beta_inv` and the nested `ibeta` are at lines 20-31, the division is at line 26 (`return s / t`), and the caller is line 50 (`lo, hi = clopper(a.survivors, a.counted)`).
**Skill version:** vendored copy in this repo. `scripts/queue.py` sha256 is `2f5a31c67e818ab3ea68b1b2bfd67399c90c9926b449fbebc8ad24bb92069050`.
**Found by:** wave 1 agent 1 (`astronomy/agent1_supply_corpus/REPORT.md` line 105), SYNTHESIS §7 item 1. This draft re-runs and narrows the failure.
**Patch:** `patches/01-queue-logspace-ibeta.patch`. The same patch fixes issue 05.

## Minimal repro (run on a pristine copy, `scratch/orig/`)

```
$ python3 scripts/queue.py --counted 11183 --passed 7154 --survivors 7154 --target 100
Traceback (most recent call last):
  File ".../scratch/orig/scripts/queue.py", line 90, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File ".../scratch/orig/scripts/queue.py", line 50, in main
    lo, hi = clopper(a.survivors, a.counted)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../scratch/orig/scripts/queue.py", line 34, in clopper
    return (0.0 if k == 0 else beta_inv(alpha / 2, k, n - k + 1),
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".../scratch/orig/scripts/queue.py", line 30, in beta_inv
    lo, hi = (m, hi) if ibeta(m) < p else (lo, m)
                        ^^^^^^^^
  File ".../scratch/orig/scripts/queue.py", line 26, in ibeta
    return s / t
           ~~^~~
ZeroDivisionError: float division by zero
[exit=1]
```

The `...` stands for `/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave2/agent5_skill_maintenance`. The full text is in `logs/queue_cli_before.txt`.

## Smallest failing n

`repro/queue_scan.py` imports the unmodified `queue.py`. From the code, `t` does not depend on `m`, so `clopper(k, n)` raises exactly when `t(k, n-k+1) == 0` or `t(k+1, n-k) == 0`. The script screens k within ±3 of n/2 from n = 1000 upward. It then checks every k at the first failing n and at n − 1, and confirms each failure by calling `clopper` itself. Output (`logs/queue_scan_before.txt`, abridged; the 33 identical confirm lines are cut to two):

```
screen: first n with a failing k near n/2 = 1072
exhaustive all k at n=1071: failing k = []
exhaustive all k at n=1072: failing k = [520, 521, ..., 552]
  confirm via queue.clopper(520,1072) raises ZeroDivisionError: True
  ...
  confirm via queue.clopper(552,1072) raises ZeroDivisionError: True
  control clopper(520,1071) raises: False
astronomy yield 7154/11183: smallest failing n = 1136 (k=727); clopper raises True; n-1 (k=726) raises False
source-record yield 1/6: smallest failing n = 1648 (k=275); clopper raises True; n-1 (k=274) raises False
yield 0.05: smallest failing n = 3731 (k=187); clopper raises True; n-1 (k=186) raises False
```

- **Smallest n that fails for some k: 1072.** At n = 1072, k = 520 to 552 fail. At n = 1071, no k fails.
- **Limit on that claim.** Every k was checked only at n = 1071 and n = 1072. Below that, only k near n/2 was screened, starting at n = 1000. n/2 is where `t` is smallest for a fixed a + b = n + 1, but n < 1000 was not checked exhaustively.
- **At a fixed yield**, the smallest failing n is 1136 at the astronomy corpus ratio, 1648 at the source record's 1/6, and 3731 at 5%.

## Expected vs actual

- **Expected:** an exact 95% interval for any n the corpus can produce. P5 has to run on an 11,183-object corpus.
- **Actual:** an uncaught exception from n = 1072 on, exit 1, and no queue. Issue 05 shows the output is already wrong before it starts crashing.

## Root cause (read from the code)

`ibeta(m)` approximates the regularised incomplete beta by a 3000-step midpoint sum. It divides the partial sum `s` by the full-range sum `t`, and each summand is `x**(a-1) * (1-x)**(b-1)`. With a + b = n + 1, the largest summand is about 2^-(n-1) near a = b, so every term underflows to 0.0 once n is a little above 1070. Then `t == 0.0`, and line 26 divides by zero.

## Proposed fix

Replace the midpoint sum with the regularised incomplete beta evaluated in log space. The prefactor `x^a (1-x)^b / B(a,b)` comes from `math.lgamma`, `math.log` and `math.log1p`. The continued fraction uses modified Lentz with the symmetry switch at x > (a+1)/(a+b+2). The fix uses the standard library only, like every other skill script (`scipy` is not installed for `python3` here). The bisection is kept and raised from 60 to 100 steps.

`scipy.stats.beta.ppf` would be an equivalent one-line fix if the skill accepts a scipy dependency. It serves as the reference in verification below.

## Verification (run)

`repro/queue_compare.py` compares the pristine `clopper`, the patched `clopper` and `scipy.stats.beta.ppf` (scipy 1.18.1, venv python). Output (`logs/queue_compare.txt`, abridged at `...`):

```
small-n grid: 99 (k,n) pairs, n <= 1071
  max |orig - scipy|  = 4.37e-02  worst at k=535, n=1071: orig=(0.512816131237184, 0.5138579400771943), scipy=(0.4691577347482415, 0.529911130002458)
  max |fixed - scipy| = 7.77e-15
  max |orig - fixed|  = 4.37e-02
  pairs whose printed 3-decimal interval differs orig vs fixed: 1
    (535, 1071, (0.512816131237184, 0.5138579400771943), (0.4691577347482443, 0.5299111300024579))
large n, fixed vs scipy (orig raises or is not evaluated):
  k=    520 n=    1072  orig=ZeroDivisionError          fixed=(0.454767, 0.515465)  scipy=(0.454767, 0.515465)  max|fixed-scipy|=1.6e-15
  k=    727 n=    1136  orig=ZeroDivisionError          fixed=(0.611277, 0.667925)  scipy=(0.611277, 0.667925)  max|fixed-scipy|=4.7e-15
  k=   7154 n=   11183  orig=ZeroDivisionError          fixed=(0.630743, 0.648626)  scipy=(0.630743, 0.648626)  max|fixed-scipy|=1.4e-14
  k=      9 n=     250  orig=(0.0165913, 0.0672369)     fixed=(0.0165913, 0.0672369)  scipy=(0.0165913, 0.0672369)  max|fixed-scipy|=9.7e-16
  k=      1 n=      30  orig=(0.000843567, 0.172174)    fixed=(0.000843571, 0.172169)  scipy=(0.000843571, 0.172169)  max|fixed-scipy|=5.3e-16
  ...
```

**Small n: the fix matches current output.**
- **98 of 99 grid pairs.** The printed three-decimal interval is identical. The one difference is n = 1071, where the current output is wrong (issue 05).
- **The skill's documented examples.** The CLI output is byte-identical for `7/40` (docstring), `1/6` (manifest.md, "0.004 to 0.641") and `9/250` (agent 1's post-S1 run). See `logs/queue_cli_before.txt` and `logs/queue_cli_after.txt`.
- **One visible change at small n.** For `--counted 30 --passed 1 --survivors 1 --target 100`, the optimistic queue moves from 575 to 576. The midpoint sum put the upper bound at 0.172174, and the exact value is 0.172169. Its `ceil(99/hi)` crossed an integer. The patched value agrees with scipy.

**Large n.**
- **Sweep.** 2,382 (k, n) pairs, including all 33 k that raised at n = 1072, raise no exception. The maximum |fixed − scipy| is 4.72e-14 (`logs/verification_after_series.txt`).
- **The corpus repro now runs.**

```
$ python3 scripts/queue.py --counted 11183 --passed 7154 --survivors 7154 --target 100
observed      7154/11183 = 0.640
95% interval  [0.631, 0.649]

ESCAPE target. S=100 reached. Stop enumerating.
[exit=0]
```

**Replay suite:** `python3 scripts/replay.py audit` on the fully patched copy prints `suite shape ok`, exit 0 (`logs/verification_after_series.txt`).

## Controls that verify the fix

| control | input | must |
|---|---|---|
| must-fire (the crash is gone) | `--counted 11183 --passed 7154 --survivors 7154 --target 100` | exit 0, interval [0.631, 0.649] |
| must-fire (first failing n) | `clopper(520, 1072)` | returns (0.454767, 0.515465), matching scipy to 1e-12 |
| must-not-fire (small-n behaviour unchanged) | `--counted 40 --passed 13 --survivors 7 --target 10 --remaining 200`, and `--counted 6 --passed 1 --survivors 1 --target 10` | byte-identical stdout to the pristine script: `[0.073, 0.328]` LICENSED, and `[0.004, 0.641]` PROVISIONAL |
| must-not-fire (verdict unchanged on a real small batch) | `--counted 250 --passed 9 --survivors 9 --target 100` | `[0.017, 0.067]`, LICENSED, spread 2.2x, as agent 1 reported |
