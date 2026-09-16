# tau.py picks a cut inside the separation-collapse band and says "separation not supplied" even when it was

**Status:** ready-to-file draft, not filed.
**Affected file:** `fm-advantage-benchmark/scripts/tau.py`, lines 51-58.

```python
if sat is not None and collapse is not None and collapse < sat:
    chosen = sat ...
elif sat is not None:
    chosen = sat
    why = f"cluster gain falls below {a.saturation:.0%} at {sat}; separation not supplied"
```

**Found by:** agent 5 in wave 2, while reading the branch that issue 02 goes through.
**Patch:** `patches/02-tau-refuse-unbounded-curve.patch`.

## Minimal repro

`repro/tau/sep_collapsed_at_sat.csv`:

```
cut,n_clusters,separation
1,100,0.4
2,150,0.4
3,152,0.1
4,153,0.1
```

Run on the pristine copy (`logs/tau_cli_before.txt`):

```
$ python3 scripts/tau.py --curve repro/tau/sep_collapsed_at_sat.csv
     cut  clusters     gain  separation
   1.000       100        -      0.4000
   2.000       150   +0.500      0.4000
   3.000       152   +0.013      0.1000
   4.000       153   +0.007      0.1000

saturation cut   3.0
collapse cut     4.0

CHOSEN 3.0
  cluster gain falls below 5% at 3.0; separation not supplied
  report sensitivity at 2.0 and 4.0
[exit=0]
```

## Expected vs actual

**Expected.** Separation was supplied. At the saturation cut (3.0) it has fallen to a quarter of its maximum, and the collapse cut the script computed (4.0) is at or above the saturation cut. D3 bounds the cut on two sides: saturation above and collapse below. No cut in this range satisfies both, so the script should REFUSE.

**Actual.**
- The script returns CHOSEN 3.0 with exit 0, a cut where separation has collapsed.
- The justification it writes says "separation not supplied", which is false.
- `--out` would record that false justification in the cut_curve ledger.

## Root cause

The `elif sat is not None` branch catches every case the first branch rejects. That includes a case where separation was measured but `collapse >= sat`, and a case where it was measured but never collapsed (`collapse is None`). The justification string is hard-coded for the no-separation case.

## Proposed fix

1. Before choosing, if `sat` and `collapse` both exist and `collapse >= sat`, print `REFUSE. Separation has collapsed at {collapse}, at or above the saturation cut {sat}. No cut in this range both saturates and separates.` and exit 2.
2. In the `elif` branch, print "separation holds across the swept range" when separation was supplied, and "separation not supplied" only when it was not.

## Verification (run)

Patched copy (`logs/tau_cli_after.txt`):

```
$ python3 scripts/tau.py --curve repro/tau/sep_collapsed_at_sat.csv
     cut  clusters     gain  separation
   1.000       100        -      0.4000
   2.000       150   +0.500      0.4000
   3.000       152   +0.013      0.1000
   4.000       153   +0.007      0.1000

saturation cut   3.0
collapse cut     4.0

REFUSE. Separation has collapsed at 4.0, at or above the saturation cut 3.0. No cut in this range both saturates and separates.
[exit=2]
```

Must-not-fire control `repro/tau/sep_holds.csv` has the same cluster counts and separation `0.1,0.1,0.4,0.4`. It returns CHOSEN 3.0 with "separation holds above 2.0", and the output is identical before and after the patch.

The replay suite audit on the patched copy reports `suite shape ok`.

Second must-fire control, for the misreport only: `repro/tau/sep_never_collapses.csv`, which has cluster counts 100, 200, 205 and 206 and separation 0.4 at every cut. The pristine script prints `CHOSEN 0.3` with "separation not supplied" even though a separation column was supplied. The patched script prints `CHOSEN 0.3` with "separation holds across the swept range". The cut is the same and only the justification changes (`logs/tau_cli_before.txt`, `logs/tau_cli_after.txt`).

## Not demonstrated

The instance is synthetic. No real curve with separation exists yet, because separation needs I1.
