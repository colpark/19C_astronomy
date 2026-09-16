# tau.py returns CHOSEN on a flat curve that bounds nothing

**Status:** ready-to-file draft. Not filed, because no upstream is known.
**Affected file:** `fm-advantage-benchmark/scripts/tau.py`, line 31:

```python
sat = next((cuts[i] for i, g in enumerate(gains, start=1) if g < a.saturation), None)
```

The branch at lines 56-58 then takes the pick without any further check.
**Skill version:** `scripts/tau.py` sha256 `ede59f37d8cb94205165687bb35d0ea001ae561d6fbb1aee3fa03cf17e7bc2ba`.
**Found by:** wave 1 agent 1 (`agent1_supply_corpus/REPORT.md` D3 and disagreement 11), SYNTHESIS §7 item 2.
**Patch:** `patches/02-tau-refuse-unbounded-curve.patch`. The same patch fixes issues 06 and 07.

## Minimal repro

`repro/tau/flat.csv` has three cuts, which is the minimum tau.py accepts, and no separation column:

```
cut,n_clusters
0.1,1000
0.2,1001
0.3,1002
```

Run on the pristine copy (`logs/tau_cli_before.txt`):

```
$ python3 scripts/tau.py --curve repro/tau/flat.csv
     cut  clusters     gain
   0.100      1000        -
   0.200      1001   +0.001
   0.300      1002   +0.001

saturation cut   0.2

CHOSEN 0.2
  cluster gain falls below 5% at 0.2; separation not supplied
  report sensitivity at 0.1 and 0.3
[exit=0]
```

The real curve behaves the same way. That is agent 1's `out/curve_for_tau.csv`, copied to `repro/tau/astronomy_agent1_curve.csv`. On the pristine copy it prints `CHOSEN 0.03333333333333333` and exits 0. That cut is 30″, and it merges 39 pairs of distinct supernovae.

## Expected vs actual

**Expected:** REFUSE, exit 2. SKILL.md says tau.py chooses the cut "refusing when the curve does not bound one". discovery.md D3 says the cut is bounded by cluster saturation above and separation collapse below. On a curve where no step ever gains 5%, the saturation signal is absent: every cut is equally "saturated". With no separation column, the collapse signal is absent too, so nothing bounds the cut.

**Actual:** the script returns CHOSEN at the second grid point, exit 0, and `--out` writes a cut_curve record that `validate.py` accepts. So the choice is an artefact of where the grid starts.

## Root cause

`sat` is "the first cut whose step gain is below the threshold". On a flat curve the first step already qualifies, so `sat = cuts[1]`. The branch `elif sat is not None: chosen = sat` never asks whether any earlier step rose above the threshold, so saturation is never actually observed. The REFUSE at line 59 is reachable only when every step gains 5% or more.

## Proposed fix

1. **Define saturation as a rise that stops.** Let `rising` be the steps with gain ≥ threshold. If there are none, the curve is flat and `sat = None`. Otherwise `sat` is the cut after the last rising step. That change also fixes issue 06.
2. **Refuse a flat curve with its own message**, exit 2:

   ```
   REFUSE. No step gains 5% or more, so the saturation test cannot discriminate any cut in this range. Widen the sweep, or bound the cut with must-join and must-not-join controls.
   ```

3. **Refuse with separation supplied too.** A flat cluster curve still bounds nothing from above. This goes further than SYNTHESIS §7.2, which asked only for the no-separation case, and the control `flat_with_sep.csv` below pins it down.

## Verification (run; `logs/tau_cli_before.txt`, `logs/tau_cli_after.txt`, and `logs/tau_cli_after_series.txt` on the fully patched copy, which is identical)

| curve | pristine | patched |
|---|---|---|
| `flat.csv` (must fire) | CHOSEN 0.2, exit 0 | REFUSE, exit 2 |
| `flat_with_sep.csv` (must fire) | CHOSEN 0.2, exit 0, "separation not supplied" | REFUSE, exit 2 |
| `astronomy_agent1_curve.csv` (must fire, real) | CHOSEN 0.0333 (30″), exit 0 | REFUSE, exit 2 |
| `saturating.csv` (must not fire) | CHOSEN 0.3, exit 0 | CHOSEN 0.3, exit 0, identical stdout |
| `sep_holds.csv` (must not fire) | CHOSEN 3.0, exit 0 | CHOSEN 3.0, exit 0, identical stdout |

Patched output on the repro:

```
$ python3 scripts/tau.py --curve repro/tau/flat.csv
     cut  clusters     gain
   0.100      1000        -
   0.200      1001   +0.001
   0.300      1002   +0.001

saturation cut   curve flat, no step gains 5%

REFUSE. No step gains 5% or more, so the saturation test cannot discriminate any cut in this range. Widen the sweep, or bound the cut with must-join and must-not-join controls.
[exit=2]
```

Must-not-fire curve `repro/tau/saturating.csv`, which must still return CHOSEN:

```
cut,n_clusters
0.1,100
0.2,200
0.3,205
0.4,206
```

```
$ python3 scripts/tau.py --curve repro/tau/saturating.csv
     cut  clusters     gain
   0.100       100        -
   0.200       200   +1.000
   0.300       205   +0.025
   0.400       206   +0.005

saturation cut   0.3

CHOSEN 0.3
  cluster gain falls below 5% at 0.3; separation not supplied
  report sensitivity at 0.2 and 0.4
[exit=0]
```

**`--out` still works.** On `saturating.csv` the patched script writes a cut_curve that `python3 scripts/validate.py ledger ... --kind cut_curve` reports as `PASS` (`logs/verification_after_series.txt`).

**Replay suite:** `python3 scripts/replay.py audit` on the patched copy prints `suite shape ok`, exit 0.

## Controls

- **Must fire:** `flat.csv`, `flat_with_sep.csv`, and agent 1's real BTS curve all return REFUSE with exit 2. The real curve is the control derived from a real prior failure.
- **Must not fire:** `saturating.csv` returns CHOSEN 0.3, and `sep_holds.csv` returns CHOSEN 3.0, each with stdout byte-identical to the pristine script.

## Not demonstrated

Separation was never measured on the astronomy corpus, because it needs I1 compositions. No real curve with a separation column was run through either version.
