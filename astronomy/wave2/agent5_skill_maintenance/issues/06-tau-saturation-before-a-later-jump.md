# tau.py picks a "saturation" cut that sits before a large later gain

**Status:** ready-to-file draft, not filed.
**Found by:** agent 5, wave 2, while building the must-not-fire curve for issue 02.
**Affected file:** `fm-advantage-benchmark/scripts/tau.py`, line 31, which is the same line as issue 02.
**Patch:** `patches/02-tau-refuse-unbounded-curve.patch`.

## Minimal repro

`repro/tau/late_jump.csv`:

```
cut,n_clusters
0.1,100
0.2,102
0.3,200
0.4,205
```

Pristine copy (`logs/tau_cli_before.txt`):

```
$ python3 scripts/tau.py --curve repro/tau/late_jump.csv
     cut  clusters     gain
   0.100       100        -
   0.200       102   +0.020
   0.300       200   +0.961
   0.400       205   +0.025

saturation cut   0.2

CHOSEN 0.2
  cluster gain falls below 5% at 0.2; separation not supplied
  report sensitivity at 0.1 and 0.3
[exit=0]
```

## Expected vs actual

**Expected.** The docstring says "cluster count saturates above some cut, so tighter buys nothing." Going tighter from 0.2 to 0.3 almost doubles the cluster count (+96%), so 0.2 is not saturated. The first cut after which every tighter step gains less than 5% is 0.4.

**Actual.** tau.py returns CHOSEN 0.2. That cut sits right before the biggest gain on the curve, and the justification text says the gain "falls below 5% at 0.2".

## Root cause

`next(... if g < a.saturation)` takes the first step under the threshold. It never checks the steps that come after.

## Proposed fix

Use the same change as issue 02. The saturation cut is the cut after the last step whose gain is at or above the threshold.

## Verification (run)

Patched copy (`logs/tau_cli_after.txt`):

```
$ python3 scripts/tau.py --curve repro/tau/late_jump.csv
     cut  clusters     gain
   0.100       100        -
   0.200       102   +0.020
   0.300       200   +0.961
   0.400       205   +0.025

saturation cut   0.4

CHOSEN 0.4
  cluster gain falls below 5% at 0.4; separation not supplied
  report sensitivity at 0.3 and None
[exit=0]
```

The "None" in the sensitivity line is how the pristine script already behaves whenever the chosen cut is the last one in the sweep. The patch does not change it. `validate.py` still accepts a record that has one of the two sensitivity cuts.

**Replay suite.** `replay.py audit` on the patched copy prints `suite shape ok`.

## Controls

- **Must fire:** `late_jump.csv` must not return 0.2. The patched script returns 0.4.
- **Must not fire:** `saturating.csv` (100, 200, 205, 206) must still return CHOSEN 0.3. Run, and the output is identical before and after the patch.

## Limitation

The only instance of this defect is synthetic. None of the curves the panel recorded has this shape.
