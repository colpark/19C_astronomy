# Module V charter, wave 4 (agent 4)

Written 2026-09-17 before any target is listed, any input is opened for values, or any
derivation is run. Hashed in `V_CHARTER.sha256`. Authority: wave-4 brief ruling 5 and rule E
(brief sha256 8f10181154219048bed3e8fa973c35d71d3a038cc98323fde76f509363511b58, verified
against `astronomy/wave4/BRIEF_SHA256` at 13:15:12Z).

## 1. Scope

Ruling-bearing numbers only: numbers that enter the P4 ruling, a kill-band comparison, or a
frozen manifest slot. The list is fixed in `V_TARGETS.json`, hashed before any
re-derivation. Everything outside that list proceeds unverified under rule E and is not
touched by this module. Target list changes after hashing are amendments: a new file
version, its hash, and a cause line in `order_of_operations.log`. No target is dropped
because its check came out badly.

## 2. Blind protocol (per number)

a. Derive the value from the declared inputs with code written in this directory
   (`scripts/`). Producer scripts are not imported, copied or executed. Frozen definitions
   and protocols (the `*_FROZEN.md` files, count and census protocols, reference formulas
   in the skill) may be read, because they are the specification, not the claim.
b. Write the derived value to `sealed/V-<id>.json`; hash it into `sealed/SEALED_SHA256SUMS`
   and log the hash in `order_of_operations.log` with a UTC timestamp.
c. Only after (b) open the producer's recorded value at the file and field named in
   `V_TARGETS.json`.
d. Record claimed, derived, absolute difference, relative difference and the verdict under
   section 5 in `v_records.json`.
e. Premise check: state a test that would fail if the claim were false, run it, and
   record the result. A premise check that was not run is recorded NOT_RUN, not passed.
f. Every DISCREPANCY gets a report in `discrepancies/` with a resolved cause.

Known limit of blinding, declared up front: the wave-4 task prompt that launched this
session quotes most claimed values (cohort total, S1, the SNIascore bound, p-values, tally,
truth-cost N, night counts). Blinding here is therefore code-path blindness (the
derivation never reads a producer output field) and seal-before-open for every value the
prompt did not quote (sigma_d, MDE, N_min, AUCs, CIs, and all secondary fields). It is not
reader blindness for the quoted values. This limit is recorded in every affected record.

## 3. Independence rule

- Own implementation of every statistic: rank-based AUC, Poisson-binomial tail, exact beta
  intervals, sigma_d/MDE/N_min from the documented formula (not `power.py`), counting and
  merge rules from the frozen text.
- Producer scripts may not be run to produce a derived value. They may be read only after
  the value is sealed, and only to resolve the cause of a discrepancy.
- Shared plumbing is allowed where it is not a verified number: the label-stripping alert
  fetch helper (`safe_fetch.py`) and the installed tool environments, used read-only.
- Inputs are verified against their producer hash manifests before use. A hash mismatch
  makes the dependent numbers UNVERIFIABLE (input-version), not MATCH.
- The verifier did not produce any number it verifies (new session, wave 4).

## 4. Discrepancy report format

`discrepancies/D-<target id>.md`, one per DISCREPANCY, with fields:

| Field | Content |
|---|---|
| target | id and claim text |
| claimed | value, file, field |
| derived | value, sealed file and its sha256 |
| difference | absolute and relative |
| tolerance | the declared tolerance that was exceeded |
| inputs | files and hashes used |
| cause class | exactly one of: arithmetic, definitional, input-version, rounding, producer error; or UNRESOLVED |
| cause evidence | the specific line, rule or computation that establishes the cause, read only after sealing |
| consequence | which ruling, band or manifest slot the number feeds, and whether the difference changes it |
| status | RESOLVED (cause established) or UNRESOLVED (not a pass) |

## 5. Tolerance policy (declared before any comparison)

Effective tolerance = the declared value below, or half a unit in the last recorded digit of
the claim when the claim is recorded rounded, whichever is larger. The rounding allowance
applies only to the precision at which the claim is actually written in the named field.

| Number type | Abs tol | Rel tol | Reason |
|---|---|---|---|
| Integer counts (cohort objects, straddlers, nights, label categories, tool tallies, alert runs, truth-cost N) | 0 | 0 | Deterministic counts over the same hashed inputs under frozen rules; any difference is definitional, input-version or error and must be explained |
| Integer derived by ceiling (N_min) | 0 | 0 | Deterministic given sigma_d and delta; an off-by-one is a rounding or definitional cause that must be named, not absorbed |
| Shares and proportions (e.g. one-detection share) | 1e-9 | 0 | Ratio of exact integers; only the recorded-rounding allowance applies |
| Closed-form float statistics (sigma_d, MDE, standard errors) | 1e-9 | 1e-6 | Same formula over the same rows; 1e-6 relative covers ddof/accumulation-order differences in float64 summation, nothing larger |
| AUC point estimates (rank based) | 1e-9 | 1e-6 | Mann-Whitney AUC with midranks is exact over the same predictions; differences beyond float noise mean different rows, tie handling or label polarity |
| Bootstrap CI endpoints | 0.01 | 0 | Resampling Monte Carlo error: with B around 1e3 and n in the hundreds to thousands the endpoint SE is about 0.002 to 0.005; 0.01 is about 2 to 5 SE. Independent RNG streams cannot reproduce exact endpoints. Analytic (DeLong/Hanley) CIs, if that is what the producer used, get abs 1e-4 because they are deterministic |
| Very small p-values | 0.05 in log10 | 0 | Recorded to one significant figure (e.g. 5e-146 spans 4.5 to 5.5, log10 width 0.087, half 0.044); exact Poisson-binomial tails in log space agree far tighter, so 0.05 is the rounding allowance only |
| Interval bounds that are integer counts (SNIascore bound) | 0 | 0 | Counts under frozen bound rules |
| Timestamps | 1 s | 0 | mtime and log-line granularity; ordering verdicts are boolean and exact |
| Truth-cost ranges (spectra, nights) | 0 on integers; recorded-rounding on floats | 0 | Formula applied to integer N |
| Invariance (same alert, alone vs batch) | 0 (bitwise) primary; 1e-6 abs secondary | 0 | The claim is identical scoring. Bitwise equal = INVARIANT. Within 1e-6 = INVARIANT_WITHIN_FLOAT_TOL (reported separately; float kernel nondeterminism). Larger = NOT_INVARIANT (a batch-dependence defect of the kind wave 2 found in Fink) |

Verdicts: MATCH (equal at the claim's recorded precision), MATCH_WITHIN_TOL (within
effective tolerance but not equal at recorded precision), DISCREPANCY (outside), UNVERIFIABLE
(an input is unavailable or fails its hash; reason recorded), UNRESOLVED (a discrepancy
whose cause could not be established; not a pass). Only MATCH and MATCH_WITHIN_TOL with a
premise check that ran and behaved as required clear a number for P4 use under rule E.

## 6. Never amend producer artifacts

This module writes only under `astronomy/wave4/agent4_module_v/`. It never modifies, moves,
re-hashes or amends any producer artifact, including when a discrepancy is found. It files
discrepancy reports; the owning agent or the PI acts on them. No git commands are run.

## 7. Arithmetic discrepancies resolve to a cause

A discrepancy is not closed by rerunning until numbers agree. Each is assigned one cause
class from section 4 with evidence. A discrepancy without an established cause is
UNRESOLVED and blocks the number under rule E.

## 8. Overhead cap

Cap: 15% of wave-4 effort (ruling 5). This module logs its own tool calls and wall time
(session start 2026-09-17T13:14:53Z) in `overhead.json` so the coordinator can compute the
share against the wave total. If the module sees itself approaching the cap it reports it
rather than silently truncating targets; truncation would be an amendment with cause.

## 9. Alert-run budget (rule D)

At most 90 alert runs (250 cap minus 160 used by wave-3 agent 4). Every run is logged in
`invariance_runs.jsonl` (ids, arm, hash of output, no content retained). Fetches go through a
label-stripping path only.

## 10. Replay controls

V-01 must_fire: a planted wrong number (cohort total off by 1,000) must yield DISCREPANCY.
V-02 must_not_fire: a benign float difference inside declared tolerance must yield
MATCH_WITHIN_TOL. The verdict function is not armed until both have run.
