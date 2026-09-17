# PI re-ratification packet (ruling 1): Rubin-era paid work

- **Question for the PI:** ruling 1 says no Rubin-era paid work starts without re-ratification against this wave's measured label supply. Does it start?
- **Manifest:** `domain_manifest_v2.json`, frozen_hash `fba4259b1d5931ff8b74a3db2f438706ce29263ef7ca373a2cb5c5fd7f2cedd5` (v1 `ca00efe0…cbae8`).
- **Evidence files** (hashes verified): agent 2 `label_source_slot.json` `fdae6492…`, `supply_P_per_month.json` `b028de4a…`, `truth_cost.json` `53f229b3…`; axis ledger `axis_ledger_v2_final_against_frozen_bands.json`.

## 1. Measured label supply on the Rubin cohort: none demonstrated
- **Measured non-bot spectroscopic labels on cohort objects: UNDEMONSTRATED.** 0 were found, but only 13 of 627 cohort-matched TNS captures were readable, so this is not a zero.
- **Typed objects:** 13 cohort objects have a TNS type (12 transients, 1 CV). Their classifier is unknown, so they are not measured labels (bands section 4).
- **P and Ng:** cannot be computed. TNS credentials are BLOCKED (request 2026-09-16).
- **2026 TNS throughput, lower bounds only, all objects rather than the cohort:** at least 181 spectroscopic units Jan–Sep, at least 161 of them non-bot. By month: Jan 24, Feb 2, Mar 20, Apr 13, May 90, Jun 22, Jul 3, Aug 5, Sep 2. Programmes: ZTF ≥63, ePESSTO+ ≥55.
- **Reachability:** f19 = 0.004 (8 of 2,000); about 775 reachable arrivals per on-sky night. Rubin has been off sky since 2026-07-14, and its return date is unknown.
- **BTS (calibration only):** SNIascore bound [954, 2,057]; 5,815 of 7,843 labels unresolved.

## 2. Price of truth
Assumptions: no existing labels; purity 0.81–0.967; success 0.93–1.0; capacity 4.5–10 spectra per night. Telescope capacity is the binding limit.

| δ | N labelled objects | Spectra | P60 h (0.5 h each) | Rubin on-sky nights | Wrong commitments (1 slot each) |
|---|---|---|---|---|---|
| **0.05 (your override)** | 63 (bracket low) | 66–84 | 33–42 | 7–19 | 3–16 |
| **0.05** | 1,666 (bracket high) | 1,723–2,212 | 862–1,106 | 173–492 | 57–420 |
| 0.018 (prior; frozen bands) | 485 (bracket low) | 502–644 | 251–322 | 51–144 | 17–122 |
| 0.018 | 12,855 (bracket high) | 13,294–17,065 | 6,647–8,533 | 1,330–3,793 | 439–3,242 |

- **Missed rare events:** add ≥100 slots per miss to every row. The miss rate is unknown.
- **Calendar time:** unknown (off sky; P60 and Rubin sky overlap not applied).
- **Budget:** these are telescope hours, not the 1,000 arm cells or 200 engineering hours.
- **Frozen bands vs override:** P4 PROCEED under the frozen bands still needs 12,855 labels.

## 3. P4 readings against the FROZEN bands (δ 0.018; 0.05 reported beside): no ruling
- **ESCALATE:**
  - contamination_exposure: 1,937,669 objects after every published cutoff, but Gemini 3.1 Pro has no cutoff;
  - tool_coverage: CATS passes 5/10, while both of its Rubin classical counterparts fail at emit.
- **PROCEED:** cluster_structure, split_integrity, unprocessable_units.
- **UNDEMONSTRATED:** positive_supply, negative_supply.
- **Preconditions:** (a) UNMET (no measured P and Ng); (b) CLEARED (recount after the band hash, verified); (c) UNMET (label source not ratified). The validator FAIL stands.
- **Consequence:** with contamination and tool coverage both at ESCALATE, the frozen combination rule cannot reach PROCEED even once (a) and (c) clear, unless the subject set changes.

## 4. Slots still awaiting your explicit ruling (not ratified on your behalf)

| Slot | Status | Needed from you |
|---|---|---|
| tau (1″ plus 60 d re-trigger clause) | DERIVED | RATIFY or override |
| exposure_key | DERIVED | RATIFY or override |
| subject_set (7 models; Gemini 3.1 Pro has no cutoff; Fable 5.1 sets the 2026-07-01 boundary) | DERIVED | RATIFY, or drop or replace members; this changes the contamination band reading |
| label_source | UNDEMONSTRATED | ratify the bounded state, supply TNS credentials, or name a source |
| S | UNDEMONSTRATED | nothing now: computed at R1 |

Already ruled: k = 8 and the decision epoch (RATIFIED); the Fink RF remap and δ 0.05 (OVERRIDDEN); budget, cost of action, graph staging, rulings holder (transfer PENDING_RECEIPT) and TNS (BLOCKED).

## 5. Conflict for you to resolve: stratum S2
- **Ruling 6:** "S0, S1 and S2 stay reported and excluded."
- **Frozen bands, section 3:** S2 (cohort objects with pre-boundary forced flux) is counted and reported but not removed from the cohort.
- **Effect today:** S2 cannot be counted (PPDB not released), so no count moves.
- **If you mean to exclude S2:** that is a new hashed band registration with a cause (bands section 8), and it applies to counts made after it.

## Decision requested
1. Paid Rubin-era work: **start / do not start / start only after X measured labels**.
2. A ruling on each slot in section 4.
3. S2: **keep per bands / exclude via new registration**.
4. Whether to re-band at δ 0.05, which needs a new hashed registration; today 0.05 is reported beside the frozen bands only.
