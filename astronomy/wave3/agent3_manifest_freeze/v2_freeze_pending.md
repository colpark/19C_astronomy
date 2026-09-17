# v2 freeze: pending

**v2 is NOT frozen.** `domain_manifest_v2_DRAFT.json` has `frozen_hash: ""`, and validate.py FAILs on that field alone (by design). v1 is frozen and unchanged: `ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8`.

## Awaited before freezing v2 (exactly these)

1. **Wave-3 agent 2 results (PENDING-V2-01).** None have been delivered. The directory `astronomy/wave3/agent2_measured_labels/` exists, but no file in it was opened.
   - **Track one (per-object reporter split, Rubin-era non-bot classifications):** BLOCKED (TNS_API_KEY absent; AMD-V2-07). A statement from agent 2 confirming it ran nothing under track one, or what it ran, is still needed.
   - **Track two, census:** every programme that filed spectroscopic classifications to TNS in 2026, with its monthly throughput (prospective supply P per month).
   - **Track two, truth cost:** nights, and spectra per night, a dedicated follow-up programme needs to reach 485 labelled cohort objects at each plausible purity.
   - **Any update to `label_source_slot.json` or its SNIascore / CCSNscore bounds.**
2. **Coordinator hand-off** of those files with their sha256.

## What happens to them on arrival

| Agent 2 input | Manifest effect | Axis ledger effect |
|---|---|---|
| census P per month | `label_source.wave3`; `candidates[0]` supply projection | positive/negative supply stay UNDEMONSTRATED unless the census yields per-object measured labels crossmatched to cohort objects at ≤1″ (bands section 4). Programme throughput alone is not P or Ng. |
| truth cost | `S` and budget context for the PI's re-ratification (ruling 1); reported at both deltas (485 at 0.018, 63–1,666 at 0.05 beside) | none |
| updated label slot | `label_source` value and provenance replaced, with a new SU-V2 ledger entry | precondition (c) stays UNMET until the PI ratifies a label source or measured P and Ng exist |
| measured P, Ng (if any) | `candidates` | precondition (a) can clear; bands evaluated at 0.018, with 0.05 beside |

The freeze then runs `build_v2_draft.py` extended with the agent-2 fold-in, sets `frozen_hash` by the recorded method, runs validate.py, renders a v2 D5 presentation, and logs every hash.

## Not awaited (v2 can freeze with these still open, recorded as they stand)

- **S:** UNDEMONSTRATED until R1 runs (ruling 1).
- **Rulings transfer:** PENDING_RECEIPT until the holder's receipt hash is written by the coordinator (ruling 4, preamble item 2).
- **tau, exposure_key, subject_set:** DERIVED with no PI ruling. D5 does not advance until the PI ratifies or overrides them.
- **P4 ruling:** preconditions (a) and (c) UNMET, (b) CLEARED (verified here). The validator FAIL on `axis_ledger_v2_against_frozen_bands.json` stands.

## Open questions for the PI (listed, not reconciled; they do not block the freeze)

1. **S2 stratum.** Ruling 6 says S0, S1 and S2 are "reported and excluded", but bands_FROZEN.md section 3 keeps S2 in the cohort. Excluding S2 needs a new hashed band registration. S2 cannot be counted today (PPDB not released).
2. **Truth-cost target.** The brief prices truth at 485 objects, which is the delta-0.018 lower bracket. Under the delta-0.05 override, the planning bracket is 63–1,666.
3. **Metric vs cost asymmetry.** A missed rare event costs ≥100 slots against 1 slot for a wrong routine commitment, yet delta is on the committed-set purity scale. The A1 primary metric is unregistered.
4. **Tool recount format.** Preamble item 5 says "no substitute format is improvised", but the recount ran on Fink JSON rows with v11_1 field names. The band reading (ESCALATE) holds either way.
