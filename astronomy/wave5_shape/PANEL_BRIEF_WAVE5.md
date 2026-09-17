# Panel brief, wave 5: decision shape, grader, one-case pilot

**Skill.** From this wave on, the governing skill is `fm-advantage-benchmark-with-shape/` (zip sha256 `a4b98598…1240`). Rules A–E carry over. Screening input: `SHAPE_REEVALUATION.md`.

**User instruction (2026-09-17).** Run the censuses, write the shape record, recount supply under the chosen task, and run the one-case pilot.

## Ordering constraints the skill imposes (recorded before any agent runs)

1. **P3 recount is not run this wave.** `shape.md` refusal 1 says "Refuse to count any axis at P3 before the shape is ratified", and ratification is a PI act. This wave writes and hashes the P3 count protocol and bands under the proposed root. Counting waits for PI ratification of the shape record.
2. **The pilot is staged, following the wave-2 precedent that PI ruling 3 (wave 3) ratified.**
   - The graph edges D5→R1 and R1→I1 still bind.
   - Sequence: an R1 harness control on a **synthetic** item with a known-good subject, then one real ZTF object as a **PRE-RATIFICATION PILOT (harness check only)**.
   - No score record is written, no directional claim is made, and the pilot is not an I1 record.
   - The PI rules on the staging afterwards.
3. **Known pilot limitation, disclosed in advance.**
   - Subject arms are Claude subagents with shell access, so R4 grant verification (the model-side catalog) cannot be enforced, only instructed and audited from transcripts.
   - The pilot therefore checks harness mechanics. It does not isolate tool value.
4. **Custody** remains PENDING_RECEIPT, so every blind element is "procedural".

## Assignments

### Agent 1: census and shape record (D1, D4)
1. Read the seeds in full and census branch points and evidence depth (`shape.md` "Deriving the shape").
2. Rule all four roots in one pass, at subtype level, through gates 1–3.
3. Write the `decision_shape` record against the schema.
4. Draft and hash the P3 count protocol and bands for the surviving root. **Do not count.**

### Agent 2: grader, harness, pilot (I3, I4 for graders; R1; pilot)
1. Build a frozen grader instance for generate / inverse problem.
2. Define the held-out protocol and the grader-separation design.
3. Write I3/I4 cards for the graders.
4. Write the R1 spec and run it on a synthetic item.
5. Package one real ZTF item under a declared, outcome-blind selection rule.
6. Build the mechanical floor, the arm prompts, and the R8 symmetry table.
7. After the coordinator runs the two agent arms (fresh subagents), grade blind.

## Deliverables (per agent)
- REPORT text, returned to the coordinator
- schema-valid JSON records
- seed_ledger
- order-of-operations log with hashes
- 2–4 replay cases (at least one must_not_fire), with rulings in a separate file

No stage advances on time spent.
