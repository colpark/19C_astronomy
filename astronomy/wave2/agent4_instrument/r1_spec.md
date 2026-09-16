# R1 harness control: specification (written first, NOT RUN)

calibration only, contamination FAIL on this cohort
PRE-I1: graph edge R1→I1 unmet, escalated

- Author: wave-2 agent 4 (instrument), 2026-09-16.
- Written before any composition, feature, fetch or model in `astronomy/wave2/agent4_instrument/` existed. Its sha256 is in `r1_spec.sha256`.
- Governing text: `fm-advantage-benchmark/references/stages/runtime.md` §R1, `references/loop.md` (stage contract, five items), `references/graph.md` edges D5→R1 and R1→I1 (instrument module).
- Brief: `astronomy/wave2/PANEL_BRIEF_WAVE2.md`, sha256 `31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb`. This matches `astronomy/wave2/BRIEF_SHA256`, and was checked with `sha256sum` before this file was written.

## 0. Status and why it is not run

| Precondition | State | Consequence |
|---|---|---|
| D5 → R1 (no paid work on an unratified manifest) | UNMET. Budget and cost of action are unfilled SUPPLY fields (coordinator preamble item 1); agent 3's freeze has not returned | R1 is **not run** by this agent. This file is its specification only |
| R1 → I1 (no instruments before a known-good subject completes the surface) | UNMET | Every composition this agent builds is **PRE-I1 CALIBRATION**, not an I1 record, until R1 runs to D-PASS and the PI rules on the ordering (preamble item 2, ladder rung 2) |

R1 disposition today: **UNDEMONSTRATED**, not zero. It blocks I1 (as a record), R2–R8, A1–A4.

## 1. What R1 tests

It tests the surface and nothing else: prompt emission, tool mount, tool call round-trip, receipt read-back, answer parsing and cell termination. A known-good subject is used so that a failure indicts the surface and not the subject (runtime.md: "A failure inside a harness is otherwise ambiguous between surface, subject and task").
Nothing domain-specific enters. No BTS row, alert, light curve, label or astronomy word appears in the item or the stub.

## 2. The three fixtures

### 2.1 Known-good subject
- **Subject:** `claude-opus-5` (Anthropic API). It is listed in agent 5's subject set (`astronomy/agent5_resolution_replay/subject_set_slot.json`), and every wave-1 and wave-2 panel agent is running on it and completing multi-step tool tasks. That is the evidence for "known-good".
- **Rule C disclosure:** this model is also a subject. That is harmless for R1 because the item is synthetic and carries no domain content. It must not be reused as evidence about any subject's domain performance.
- **Fallback if the endpoint is unavailable:** disposition D-UNDEMONSTRATED. Do not silently substitute another model; a substitution is an amendment with cause.

### 2.2 Synthetic item (domain-free)
- **Candidates:** 46 opaque candidate identifiers `C01`…`C46`. 46 is the integer nearest 46.41, the manifest candidates-per-round (`agent5_resolution_replay/k_slot.json`), so the item has the governed shape.
- **Instruction, under 200 tokens:** "You have a tool `score(candidate_id)`. Choose exactly 8 candidates to commit. Return a JSON list of 8 distinct identifiers from the list. Cite the receipt of at least one tool call." (Its exact bytes are frozen at run time and hashed; R6 precursor.)
- **Ground truth for the record only:** the 8 highest stub scores. Correctness is recorded and is **not** a pass criterion. R1 measures the surface, not capability.

### 2.3 Stub composition
- **Function:** `score(candidate_id) -> {"value": v, "receipt": r}`, where
  - `v = int(sha256("r1-stub-seed-20260916|" + candidate_id)[:8], 16) / 2**32`
  - `r = sha256(candidate_id + "|" + repr(v))[:16]`
- **Unknown ID:** it rejects an unknown or forged `candidate_id` with an error payload.
- **Log:** it keeps a server-side call log of (timestamp, candidate_id, receipt).
- **Serving:** it is served through the same tool-mount path the arms will use, whether MCP server or function-calling. Serving it any other way voids the control.

## 3. Pass criteria (all four)
- **P1 termination:** the cell terminates without a harness error inside the cap.
- **P2 round-trip:** at least one stub call appears in the server-side log, and a receipt cited in the final answer equals a logged receipt.
- **P3 parse:** the final answer parses as exactly 8 distinct identifiers, all drawn from `C01`…`C46`. An unparsed answer is a coverage failure and is never scored zero (global refusal 6).
- **P4 hashes:** the emitted prompt bytes and the emitted tool catalogue are hashed, and each hash is recorded beside its declared hash.

## 4. Dispositions (fixed now, before any run; not reinterpretable)

| Disposition | Fires when | Action |
|---|---|---|
| **D-PASS** | P1–P4 all hold | Surface completes. The PRE-I1 calibration compositions may be re-registered as I1 records **only after** the PI rules on the ordering escalation. R2 may start |
| **D-FAIL (surface)** | Any of P1–P4 fails while the subject endpoint was reachable and the cell was not interrupted | Indicts the surface, never the subject. Work returns to the instrument module (the only non-terminal edge in graph.md). No subject is ranked or excluded. Compositions stay PRE-I1 |
| **D-UNDEMONSTRATED** | The run was interrupted, the cap was exceeded, the subject endpoint was unavailable, or D5 is still open at run time | Recorded as UNDEMONSTRATED, never zero. Re-run after the blocker clears; do not repair anything first |

## 5. Controls for the R1 check itself (global refusal 2)
The check arms only after both controls have run.
- **Must fire:** the same cell, with the stub tool unregistered from the mount (or with the stub returning a receipt that is not in its log). P2 must FAIL, and the disposition must be D-FAIL.
- **Must not fire:** the correctly served stub plus the known-good subject. The check must not fire D-FAIL on a clean surface.
- **Derivation from a real prior failure:** the must-fire control derives from the recorded failure class "a receipt that resolved was read as evidence that was relevant" (provenance.md, worked failures). P2 requires the receipt to match the server log, not merely to resolve.

## 6. Cap (loop.md item 1)
- **Cells:** 1 cell per control, so 3 cells total: must-fire, must-not-fire, and the control run itself, which is the must-not-fire configuration.
- **Model calls:** at most 30 per cell.
- **Stub tool calls:** at most 20 per cell.
- **Wall clock:** at most 0.5 h per cell and 1.5 h total.
- **GPU:** 0 GPU hours.
- **Tokens:** at most 200,000 input+output per cell.
- **On exceeding the cap:** the result is D-UNDEMONSTRATED; widening the cap is an amendment with cause.

## 7. Anti-widening and tuning-set rule (loop.md items 3–4)
- **Frozen after this hash:** the three dispositions, P1–P4, the stub function and the synthetic-item shape.
- **May change:** transport details, such as MCP vs function calling, provided the change is recorded before the run and the P4 hashes capture it.
- **Correctness:** a low correctness count on the synthetic item is reported as it is and changes nothing in the disposition.

## 8. What this spec does not cover
- It does not cover R2–R8, grant verification (R4) or arm symmetry (R8).
- It does not cover any domain item.
- It does not cover the rulings holder, which is an unfilled SUPPLY field.
