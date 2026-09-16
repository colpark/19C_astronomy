# queue.py returns wrong intervals without raising, near the underflow boundary and at small k with large n, so it can issue a false LICENSED or a false ESCAPE supply

**Status:** ready-to-file draft (not filed).
**Found by:** agent 5, wave 2, while checking the fix for issue 01 against scipy.
**Affected file:** `fm-advantage-benchmark/scripts/queue.py`, lines 20-31 (the midpoint-sum `ibeta`). The wrong interval reaches the queue at lines 64-65 and the supply escape at lines 72-77.
**Patch:** `patches/01-queue-logspace-ibeta.patch`, the same patch as issue 01.

## Minimal repro (pristine copy, `logs/queue_cli_before.txt`)

**A. Just below the crash boundary.** The interval does not contain the point estimate, the pessimistic queue is smaller than the point queue, and the script licenses a plan anyway.

```
$ python3 scripts/queue.py --counted 1071 --passed 1071 --survivors 535 --target 600
observed      535/1071 = 0.500
95% interval  [0.513, 0.514]

queue for 65 more survivor(s)
  optimistic    127
  point         131
  pessimistic   127

LICENSED. Spread 1.0x. Plan against the point estimate.
[exit=0]
```

**B. Small k, large n.** The upper bound is about 700 times too small, so the script falsely closes the domain.

```
$ python3 scripts/queue.py --counted 100000 --passed 1 --survivors 1 --target 10 --remaining 1000000
observed      1/100000 = 0.000
95% interval  [0.000, 0.000]

queue for 9 more survivor(s)
  optimistic    113517821
  point         900000
  pessimistic   18715262339868

supply remaining 1000000, optimistic yield 0.1
ESCAPE supply. Even optimistically the pool cannot reach S=10.
Close the domain and write the finding.
[exit=3]
```

**C. Where the error starts.** `repro/queue_silent.py` compares against `scipy.stats.beta.ppf` (`logs/queue_silent_before.txt`):

```
k=n//2: first n whose printed interval differs from scipy = 1063; orig=('0.468', '0.530') scipy=('0.469', '0.530')
k=1 n=     10: orig hi=0.445 scipy hi=0.445 ratio=1
k=1 n=    100: orig hi=0.05448 scipy hi=0.05446 ratio=1
k=1 n=   1000: orig hi=0.005789 scipy hi=0.005559 ratio=0.96
k=1 n=  10000: orig hi=0.6956 scipy hi=0.000557 ratio=0.000801
k=1 n= 100000: orig hi=7.928e-08 scipy hi=5.572e-05 ratio=703
k=1 n=1000000: orig hi=4.337e-19 scipy hi=5.572e-06 ratio=1.28e+13
```

## Expected vs actual

**Expected:** the exact interval. For repro A that is [0.469, 0.530], which is LICENSED with spread 1.1x. For repro B it is [2.5e-07, 5.57e-05], with an optimistic yield of 55.7 on the remaining supply, which is PROVISIONAL and not an escape.

**Actual:**
- **Repro A:** an interval about 60 times too narrow that excludes the observed rate.
- **Repro B:** an upper bound about 700 times too small, which triggers exit 3 ("Close the domain"). That is a false closure finding, which is the skill's primary product.
- **At k = 1 and n = 10,000:** the upper bound is 0.70 instead of 0.00056, too wide by a factor of about 1,250. Nothing raises in any of these cases.

## Root cause

The code integrates the density `x^(a-1)(1-x)^(b-1)` with a fixed step of 1/3000 over [0, m] and over [0, 1]. Two things go wrong:

- **Peaked density.** When the density is narrower than the step, the midpoint sum misses or over-weights its mass. For k = 1 the mass lies within about 1/n of 0.
- **Underflow near n ≈ 1070.** Most terms underflow and only a few survive in `s` and `t`. The ratio `s/t` then jumps and the bisection lands in the wrong place.

The ZeroDivisionError in issue 01 is the final stage of the same loss of precision.

## Proposed fix

Same as issue 01: evaluate the regularised incomplete beta in log space with a continued fraction.

## Verification (run)

Patched copy (`logs/queue_cli_after.txt`, identical in `logs/queue_cli_after_series.txt`):

```
$ python3 scripts/queue.py --counted 1071 --passed 1071 --survivors 535 --target 600
observed      535/1071 = 0.500
95% interval  [0.469, 0.530]

queue for 65 more survivor(s)
  optimistic    123
  point         131
  pessimistic   139

LICENSED. Spread 1.1x. Plan against the point estimate.
[exit=0]

$ python3 scripts/queue.py --counted 100000 --passed 1 --survivors 1 --target 10 --remaining 1000000
95% interval  [0.000, 0.000]
...
supply remaining 1000000, optimistic yield 55.7

PROVISIONAL. Pessimistic queue is 39x the point estimate.
Enumerate 900000 against the point estimate, then re-derive.
Do not commit paid-tier effort on this number.
[exit=1]
```

In the log, the second block also begins with an `observed      1/100000 = 0.000` line and prints the queue lines at the `...`. The block is abridged here.

**Agreement with scipy.** For k = 1 at n = 100,000 and n = 1,000,000, the patched values match scipy to 3e-15 or better (`logs/queue_compare.txt`). Across a sweep of 2,382 (k, n) pairs the largest difference is 4.72e-14.

**Suite check.** `replay.py audit` on the patched copy prints `suite shape ok`.

## Controls

- **Must fire.**
  - Repro A must print an interval that contains 0.500.
  - Repro B must not exit 3.
  - Both pass on the patched copy.
- **Must not fire.** The documented small-n cases must stay byte-identical: `7/40`, `1/6` and `9/250`. They do, per issue 01.

## Residual (not fixed, recorded only)

The interval line prints 3 decimals, so repro B shows `[0.000, 0.000]` before and after the patch. That is a display limit, not a numerical error. The patch does not change the format.
