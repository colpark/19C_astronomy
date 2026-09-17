# Panel brief, wave 4: PI resolutions, price of truth, module V, first P4 attempt

Repo state at issue: 8560c9f. Rules A through D carry over unchanged, with one addition:

**E. Verification precedence.** No number enters the P4 ruling, a kill band comparison, or a frozen manifest slot without a module V record. Scope: ruling-bearing numbers only, as listed by agent 4 below. Everything else proceeds unverified.

## PI rulings (record each in the amendment ledger with this brief as cause)

1. **Delta 0.05: RATIFIED.** Cause check, recorded so no one has to trust my memory:
   - The override was declared at 15:14 in the wave 3 brief.
   - The first decision-time MDE landed at 15:46.
   - Resolvability at 0.05 was computed at 20:48.

   The value predates every measurement it now gates. Both deltas ride through every table: 0.018 as the literature prior, 0.05 as the ratified cost of action.
2. **Rulings custody.** I execute the handover out of band today. Agent 5 closes PENDING_RECEIPT only when the holder's receipt hash sits in transfer_record.json. Until the status is RECEIVED, every blind result keeps the word "procedural" attached.
3. **TNS:** [SUPPLY: key, or second BLOCKED record with request date]. If blocked, WISeREP becomes the sanctioned public channel for measured-label existence checks, with its republication provenance recorded, under rule C sealing.
4. **Label source: RATIFIED WITH CONDITIONS.** Labels are TNS-reported spectroscopic classifications, with a model-annotation fraction bounded at [803, 2247] of 7843.
   - For calibration, the SNIascore-flagged subset stays in, stratified.
   - For any future paid claim, measured truth means human-classifier-confirmed only. Model-annotated labels are excluded, and a sensitivity row shows the result both ways.
   - Precondition (c) clears under these conditions.
5. **Module V: CHARTERED** per the agreed design.
   - The verifier files discrepancy reports and never amends producer artifacts.
   - Arithmetic discrepancies resolve to a cause.
   - Overhead is capped at fifteen percent of wave effort.

## Assignments

**Agent 1: P4 ruling package.**
- Wait for freeze v2 and the V records.
- Then assemble the ruling under the frozen bands: axis ledger v2, both deltas, validator run, and band readings per axis.
- If the ruling is ESCALATE, draft the escalation memo with exactly two priced options, each with its number:
  1. fund a follow-up program that buys measured labels at agent 2's census price;
  2. close the astronomy candidate.
- Include the PPDB precovery consequence from the Sep or Oct release check.

**Agent 2: price of truth.**
- Finish wave 3 track two:
  - census every program that filed spectroscopic classifications to TNS in 2026;
  - count monthly throughput as prospective supply;
  - price the gap in nights and spectra per month to reach the freeze v2 per-object N, at delta 0.05 and at delta 0.018, at each plausible purity.
- If ruling 3 supplies the key, run track one and update the per-object split.
- If not, run the WISeREP existence check for post-cutoff measured labels, and record what it can and cannot establish.

**Agent 3: freeze v2.**
- Fold in the wave 3 counts, the label slot under ruling 4, and both deltas.
- Publish the v1-to-v2 diff with a cause per changed slot.
- Rerun the axis ledger and validator.
- v2 is the manifest P4 reads.

**Agent 4: module V.**
- Write and hash the V charter before verifying anything.
- List the ruling-bearing numbers, targeting thirty. Include:
  - the cohort total
  - sigma_d, and every MDE and N_min
  - the SNIascore bound
  - the POLICY p value
  - the k-binding night count
  - the tool pass tally
  - both composition AUC tables
- For each number:
  - blind re-derivation through an independent implementation path;
  - premise checks, including "would this check fail if the claim were false";
  - both values and the difference logged.
- Add invariance assertions for the two passing tools: the same alert in two batches must score identically.
- Add property tests for the patched queue.py and power.py.
- Ship two verifier replay cases: a planted wrong number that must fire, and a benign float difference that must not.

**Agent 5: integrity close-out.**
- Verify the receipt hash and the holder non-authorship record, then flip the transfer to RECEIVED.
- Quarantine the polarity-leaking scoring file:
  - record the leak permanently;
  - forbid the directory in every evaluator prompt;
  - move all future scoring artifacts to the holder side.
- Draft two community notes for PI review only, one on label provenance and one on Rubin-era tool readiness. Tie every claim to a logged artifact. Make no directional benchmark claims anywhere.

## Deliverables

Per agent:
- REPORT.md
- schema-valid JSON records
- seed_ledger
- order-of-operations log, with hashes where rules C or E apply
- 2 to 4 replay cases with at least one must_not_fire, with rulings in a separate file

Hash this brief before any agent runs. No stage advances on time spent. Every criterion moves to PASS or FAIL, or says why not.

---

## Coordinator preamble (recorded 2026-09-17T13:13Z, before any wave-4 agent ran)

1. **The brief is written against a stale repo state.** It cites 8560c9f, but head at issue is d7ecfd5. After 8560c9f and before this brief, these landed:
   - 74d012c: agent 2's wave-3 census and truth cost, including track two;
   - be1254b: agent 3's **v2 freeze** (`fba4259b…`) plus PI_rerat_packet.md;
   - d7ecfd5: status.

   Consequences:
   - **Agent 3.** v2 is already frozen, so it cannot be amended in place. Folding in rulings 1 and 4 means a new freeze, v3, with a published v1→v2 diff (already frozen) and a v2→v3 diff, each with a cause per changed slot. "The manifest P4 reads" is therefore v3. This is recorded as a naming disagreement, not a silent substitution.
   - **Agent 2.** Track two already landed in 74d012c. Wave 4 re-prices at the v3 per-object N, runs the WISeREP check, and does not repeat the census.
2. **Ruling 1's cause check mixes time zones.** Checked against commit and file timestamps; git commits are logged at −0500.
   - 15:14 local is 20:14Z, the wave-3 brief commit 32229e3 at 15:14:03 −0500.
   - 15:46 local is 20:46Z, commit f898294. The file `wave2/agent4_instrument/power_calibration.json` has mtime 15:44:29 −0500, i.e. 20:44:29Z.
   - "20:48" is **UTC**: agent 4's wave-3 step 1 at 20:48:29Z.

   In one zone, the order the PI asserts holds: override 20:14Z < first measured MDE 20:44Z < resolvability at 0.05 20:48Z. Two caveats:
   - The timestamps are self-logged file mtimes and commits on one host.
   - The wave-1 planning bracket and the practitioners' unpaired MDE of ~0.045 predate the override. The override's stated cause cites the latter.

   Module V should verify this ordering independently and record it (rule E).
3. **Ruling 4 cites a superseded bound.** It gives [803, 2247]. Agent 2's wave-3 archive resume, committed in 74d012c before this brief, tightened the bound to **[954, 2057]**. That interval lies strictly inside [803, 2247], so the ratified condition still holds. Agent 3 records both values, and module V verifies the tighter one.
4. **TNS (ruling 3): BLOCKED, second record.** TNS_API_KEY is absent: presence check at 2026-09-17T13:13:17Z, no value printed. Request dates are 2026-09-16 and 2026-09-17. WISeREP is the sanctioned channel. Agent 2's wave-3 probe recorded **WISeREP HTTP 403**, so the existence check may itself come back BLOCKED; agent 2 records the exact responses.
5. **Custody (ruling 2).** At issue, `transfer_record.json` reads status PENDING_RECEIPT with receipt_hash empty. No receipt hash has reached the repo or the environment. Agent 5 cannot flip the status to RECEIVED on the brief's word; it flips only when the hash is present and verifies. Until then, "procedural" stays attached to every blind result.
6. **Ordering.**
   - Agents 2, 4 and 5 start in parallel.
   - Agent 3 (freeze v3) starts after module V has records for the manifest's ruling-bearing slot numbers (rule E).
   - Agent 1 starts after v3 and the V records.
7. **Module V overhead.** Overhead is measured as agent 4's tool calls and wall time against the wave total, and reported at close.
