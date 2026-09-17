# Wave 5 status (coordinator, 2026-09-17)

Both wave-5 agents have returned, and the staged pilot has run end to end. Read next: [`agent1_census_shape/shape_record.json`](agent1_census_shape/shape_record.json) and [`agent2_grader_pilot/FINAL_REPORT.md`](agent2_grader_pilot/FINAL_REPORT.md).

| Item | State |
|---|---|
| Decision shape (D4) | **generate / inverse problem, ESCALATE at the grader gate.** Status DERIVED, awaiting PI ratification |
| Census (D1) | 12 seeds read in full, 236 branch points. Per-object branches: infer 30, explain 24, intervene 17, **generate 3**. Held-out-epoch scoring is practised in no seed |
| Grader | SALT3-f22 frozen and pinned; covers the **SN Ia family only**. G-PARAM (Bazin/Villar) exists and is frozen but is out of the pilot's scope. The wave-2 ParSNIP checkpoints cannot grade: truncated training, drawn from the cohort |
| R1 harness control | **PASS** on a synthetic item (truth scores near-ideal; wrong family scores far worse) |
| Pilot (PRE-RATIFICATION, harness check only) | **No score.** Both arms return `OUT_OF_SCOPE:NON_IA_OBJECT`: the outcome-blind pick is an SN II and the grader renders Ia |
| Arms | Both chose SALT3 and agreed to 0.002 in z, 0.06 d in t0. Both fixed z by standardisation, not by shape. Both rejected Bazin and Villar as overfitting, naming the degeneracy |
| Separation | Transcript audit: 0 network calls, 0 forbidden paths in either arm. R4 still UNDEMONSTRATED, because the audit detects rather than enforces |
| R8 | **EXIT** for this cell: 8 differences, 8 rulings. Emitted prompts differ from declared by one stripped trailing newline, ruled cosmetic by reconstruction |
| Mechanical floor | Overfits by construction. On the synthetic item it scored 49.2 on held-out data against 0.58 for the truth. Recorded, not repaired |
| P3 recount | **Not run.** shape.md refusal 1 forbids counting before the shape is ratified. The protocol is drafted and hashed |

## What the pilot demonstrated
- **The machinery works:** sealed outcome-blind selection, identity-free items, symmetric arms, blind grading, full hash chain.
- **The scope limit is now measured, not argued.** A one-family grader on an outcome-blind draw fails on most items.
- **The grader is blind to the content.** Both arms wrote careful family and redshift arguments, and both were confidently wrong about the class. Not one point of the score depends on that.

## PI decisions requested
1. **Ratify or override the shape record** (generate / inverse problem, ESCALATE at grader).
2. **Clear the grader gate** one of two ways:
   - budget at D5 a forward model trained disjoint from the item supply; or
   - restrict scope to SN Ia, which forces a supply recount over Ia-only objects and an outcome-blind selection rule inside that restriction.
3. **Ratify or replace** the cut epoch (+10 d), the horizon (+60 d), the 5% error floor and the selection thresholds. All are currently UNDEMONSTRATED as derived quantities.
4. **Decide whether the program cares about the judgement the grader cannot see.** Scoring it means a certified judge, which is the gate that closed three other subtypes.
5. Outstanding from earlier waves: custody receipt, TNS credentials, telescope time, the module V overhead cap, and the S2 conflict.
