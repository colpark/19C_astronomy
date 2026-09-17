# P3 count protocol under generate / inverse problem: DRAFT, NO COUNTING

Wave 5, agent 1. Status: **DRAFT**, pending PI ratification of `shape_record.json` (status DERIVED, disposition ESCALATE, binding gate grader).

- `shape.md` refusal 1 and global refusal 17: nothing in this file has been counted, and no query has been run against any catalogue.
- Every number below is either a recorded quantity with its source, or marked UNDEMONSTRATED with the stage that supplies it.
- Conventional values are refused (global refusal 15).

## 0. Preconditions this protocol cannot clear by itself

| Precondition | Source | State |
|---|---|---|
| Shape ratified by the PI | graph.md D4→P3 | UNMET |
| Grader admissible for every unit (scope ruling or D5 build) | `shape_record.json` binding_gate_detail | UNMET |
| D3 cut for this unit | `agent1_supply_corpus/cut_curve.json`: 1″ bounded by controls; the separation signal is UNDEMONSTRATED | 1″ reused as the cluster key; re-ruling at D3 is required because the unit changed (refusal 6) |
| Bands hashed before any count | this file | written; hash recorded in `p3_protocol_DRAFT.sha256` |

## 1. Unit

- **Unit.** One object cluster (the wave-1 `object_cluster_1arcsec`), with its ZTF g/r light curve (union of detections deduplicated on `candid`).
- **Cut.** The light curve is cut at a declared decision epoch.
- **Pre-cut data.** The arm sees only detections and non-detections at or before the cut.
- **Held-out set.** All detections strictly after the cut, in g and r, that fall inside the phase range the grader family can render.
- **Scored scalar.** One per unit: the summed Gaussian log-likelihood of the held-out set under the frozen grader's rendering of the arm's model instance (`shape_record.json` yield_per_unit).

## 2. Cut epoch (recorded, not conventional)

- **Declared cuts.** Wave-2 E1 ("first alert") and E3 ("night 3"), exactly as frozen in `astronomy/wave2/agent4_instrument/compositions_FROZEN.md` §1 (sha256 `b2f72948…427c`).
  - These are recorded decision epochs of the governed stream.
  - E3 is the primary cut, because E1 holds one detection for most units.
  - Both are counted, and reported separately; never pooled (refusal 4).
- **Screening proposal refused (DS-10).** "10 days after first detection" and "≥20 epochs" appear in no recorded quantity or seed locator.
- **Minimum pre-cut points.** UNDEMONSTRATED. Supplied at I3 from the grader and arm tool code: the smallest light curve each renders or fits without error. Known recorded failures to use then:
  - ParSNIP gives NaN on single detections (wave-2 defect 2).
  - Fink EarlySNIa requires ≥4 points in code (wave-2 disagreement 8).

## 3. The seven axes: definitions and how each is checked

| Axis | Definition under this root | Check (to run only after ratification) |
|---|---|---|
| **positive supply** | clustered units with (a) at least one pre-cut detection at the declared cut, (b) at least one held-out detection in **each** of g and r inside the grader family's renderable phase range, (c) a grader that renders the unit | count clusters, never rows; raw beside clustered with overstatement % |
| **negative supply** | specifications that must fail: units where no grader family should reproduce the held-out data. **Found negatives** come from recorded cases: light curves the empirical model cannot fit (2403.07975.layout.txt p11 §3.1 L604-629: 48 of 62); CV or AGN impostors in the BTS negatives (2009.01242.layout.txt p7 §2.4 L392-420); SN 2020eyj, where the SN Ia models fail (2104.12980.layout.txt p8 §6 L497-520). **Constructed negatives** (a rival family forced on the unit) are admitted only when the I1 mechanical floor would itself select that family (refusal 13); they sit in their own stratum | count found and constructed separately; headline never over constructed alone |
| **contamination** | "a published fit exists for this object" | exact-match the unit's ZTF IDs and IAU names against: ZTF SN Ia DR2 released tables (2409.04346.layout.txt p9 L671-686, plus the `tables/extra` alternative fits, p8 L646-648); Superphot+ Table 5 online / Zenodo and ANTARES light-curve properties (2403.07975.layout.txt p24 L1854-1868, p29 L2341-2343); an ADS full-text search on each name for a published light-curve fit. Report each source separately, and the union. Also report, beside it, the **answer-in-source exposure** (held-out photometry is public in ALeRCE, Fink and the ZTF archive) for every unit. It is 100% for archival units by construction; it is disclosed, not solved |
| **tool coverage** | units whose held-out set lies inside (i) the frozen grader's phase and band range and (ii) each arm's tool input requirements | SALT3-f22 range −20..+50 d rest frame (tool card); ParSNIP, and any D5-built model, from its card at I3 |
| **cluster structure** | raw ZTF IDs vs 1″ clusters | as in wave 1, with the must-join and must-not-join controls rerun |
| **split integrity** | (i) fold key `sha256("w2a4-fold|"+cluster_id)` (wave 2) against the 1″ cut; (ii) **grader–supply disjointness**: no unit may appear in the training set of the frozen grader | (ii) is the binding check for any ParSNIP grader. The wave-2 fold checkpoints trained on 4 of 5 folds of the 3,435-row cohort, so every unit in that cohort fails (ii) against them |
| **unprocessable units** | units where the grader raises, returns non-finite values, or the unit lacks any g or r held-out point after quality flags | recorded as a documented defect, never repaired here |

## 4. Bands (declared before counting)

Rule: a band edge must derive from a recorded quantity. Where that quantity does not exist, the band is UNDEMONSTRATED, and the stage that supplies it is named.

| Axis | PROCEED | CLOSE | ESCALATE | Edge derived from |
|---|---|---|---|---|
| positive supply | clustered ≥ N_min at each declared cut | optimistic bound on clustered < N_min | between | **N_min UNDEMONSTRATED.** It needs σ_d under this root, which does not exist. The wave-2 σ_d (0.084–0.166) is a precision@8 variance under infer and does not transfer (refusal 6). Supplier: I1 compositions under this root, then P7 (`power.py`) |
| negative supply | found negatives ≥ 1 per stratum used in the headline | found negatives = 0 (headline over constructed only is refused) | constructed only | shape.md refusal 13; the count threshold beyond "≥1 per stratum" is UNDEMONSTRATED until P6 defines strata |
| contamination | uncontaminated clustered ≥ N_min | uncontaminated optimistic bound < N_min | between | same N_min, UNDEMONSTRATED (P7) |
| tool coverage | the frozen grader renders ≥ N_min units, **and** each FM channel has a classical counterpart that runs on the same units | grader renders 0 units at a cut | otherwise | SKILL.md ratification check (a); N_min UNDEMONSTRATED (P7) |
| cluster structure | overstatement reported and the 1″ controls pass | a control fails | — | wave-1 cut_curve.json controls (recorded) |
| split integrity | 0 units shared between grader training and supply; 0 near-duplicates straddling folds | any unit shared with grader training | — | graph.md I5→R8 and the refusal to score on a checkpoint trained on the items; no tolerance is recorded, so zero is the only derivable edge |
| unprocessable | reported with cause | — | unprocessable share large enough to take clustered supply below N_min | N_min UNDEMONSTRATED (P7) |

**P4 cannot rule while N_min is UNDEMONSTRATED.**
- Under supply.md, P4 refuses to rule with any axis missing a number. A band edge missing is the same condition one level up.
- The count may still run after ratification, and would report numbers without a band ruling on the three N_min-dependent axes.
- The honest sequence is ratification → count → I1 → P7 → band ruling. Graph edge I1→P7 binds.

## 5. Quantities this root needs and does not yet have

| Quantity | Status | Supplied at |
|---|---|---|
| σ_d, MDE, N_min under this root | UNDEMONSTRATED | I1 (compositions under generate), P7 |
| chance: pass rate of unconditioned generation (parameters drawn from the grader's prior, scored on held-out epochs) | UNDEMONSTRATED | P6 after I1 |
| mechanical floor share of ceiling | UNDEMONSTRATED; the wave-1 P2 floor (0.951) is an infer classification ratio | P2 rerun under this root |
| I4: does held-out log-likelihood track the quantity the programme cares about? | UNDEMONSTRATED | I4 |
| general-transient ZTF forward model | not admissible | D5 budget line and I5 |
| minimum pre-cut points per tool | UNDEMONSTRATED | I3 from code |
| measured evidence depth | not_measured | I2 leave-one-out |

## 6. What this protocol forbids

- Counting before ratification.
- Widening "published fit" after a high contamination count, for example to "a fit in a paper the subject was trained on" (global refusal 9).
- Choosing the cut epoch after seeing supply.
- Dropping units with high held-out residuals (stratify instead, global refusal 10).
- Using any ParSNIP checkpoint trained on cohort units as the grader.
