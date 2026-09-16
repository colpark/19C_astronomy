# Panel brief, wave 3: PI rulings, measured labels, recounts, re-blinding

Repo state at issue: 75446f4. Wave 2 agents 1 and 5 have landed. Agents 2, 3 and 4 complete under the wave 2 brief, and this brief binds them the moment they return.

Rules A, B and C carry over unchanged. One addition:

- **D.** Tool execution for certification is capped at 25 tools times 10 public cohort alerts. Every run is logged, and no output is retained as an arm result. Nothing else runs.

## PI rulings (D5)

Record each ruling in the amendment ledger with this brief as cause.

1. **Budget.** 1,000 agent arm cells for the calibration phase, as a hard cap, plus 200 engineering hours. S is computed at R1. No Rubin-era paid work starts without a re-ratification against the measured label supply from this wave.
2. **Cost of action.**
   - One spectrum equals 0.5 hours of P60-class time.
   - A wrong routine commitment costs one slot.
   - A missed rare event costs at least 100 slots, recorded as asymmetric.
   - Delta override: 0.018 becomes 0.05. Cause: switching a production selector costs engineer weeks, and 0.018 sits below its own unpaired resolution.
   - Keep 0.018 as the literature prior, and carry both values through every P7 table.
3. **Graph escalation.** The wave 2 graph escalation is RATIFIED as the coordinator staged it. The compositions are PRE-I1 CALIBRATION. The I1 designation waits for R1 plus my ratification. The graph edges stand unweakened.
4. **Rulings holder.** The 19C program coordinator, confirmed as a non-author of the skill and the cases by checking authorship records before handover. The transfer happens out of band, and the receipt hash lands in transfer_record.json.
5. **TNS.** If TNS_API_KEY is present in the environment, use it under the registered bot identity. If it is absent, record BLOCKED with the request date and continue the public page bounds.
6. **Decision epoch.** It stands: first alert is primary, night 3 is secondary. Strata S0, S1 and S2 stay reported and excluded.

## Assignments

- **Agent 1: finish the cohort.**
  - Resume C3 and C5 from their checkpoints.
  - Complete the 1 arcsecond / 60 day merge, the straddler count, the cohort-wide one-detection share, and the split and unprocessable axes.
  - Check for the PPDB release, expected September or October 2026, and record its precovery consequence for the cohort bound.
- **Agent 2: measured labels, the binding axis.**
  - Track one: with credentials, split the 7,843 BTS labels by reporter per object, and pull every Rubin-era spectroscopic classification with a non-bot reporter.
  - Track two, regardless of credentials: census every program that filed spectroscopic classifications to TNS in 2026. Count each program's monthly throughput as prospective supply P per month. Then price the gap: the nights, and spectra per night, a dedicated follow-up program needs to reach 485 labeled cohort objects at each plausible purity. That number is what truth costs, and it feeds my re-ratification.
- **Agent 3: manifest freeze v2.**
  - Fold in the wave 2 label slot, the rulings above, and the wave 3 counts as they land.
  - Present every derivation with an override invitation, then freeze and hash.
  - Re-run the axis ledger against the frozen bands. If P4 preconditions are still unmet, the validator FAIL stands and says which ones.
- **Agent 4: tool coverage recount after the band.**
  - Under rule D, load and run each of the 25 tools on up to 10 real cohort alerts in lsst v11_1 format.
  - A tool passes only on an end-to-end run: parse, infer, emit.
  - Apply the ratified Fink remapping.
  - Update tool_coverage_axis.json with a recount timestamp after the band hash, so P4 precondition b can clear.
- **Agent 5: integrity.**
  - Re-issue both replay suites under opaque ids.
  - Hand the maps and RULINGS_SEALED.csv to the holder per ruling 4.
  - Re-score the wave 1 astronomy suite with a fresh evaluator on opaque ids only, and report the delta against 20 of 20 as the measured issue 09 inflation.
  - Add at least two ladder and two runtime replay cases, which is the gap RESULT.md names.

## Deliverables

Per agent:
- REPORT.md
- schema-valid JSON records
- seed_ledger
- an order-of-operations log, with hashes where rule C applies
- 2 to 4 replay cases with at least one must_not_fire, with rulings in a separate file

Hash this brief before any agent runs. No stage advances on time spent. Every criterion moves to PASS or FAIL, or says why not.

---

## Coordinator preamble (recorded 2026-09-16T20:13Z, before any wave-3 agent ran)

1. **TNS (ruling 5): BLOCKED.** TNS_API_KEY is absent from the coordinator's environment; checked at 2026-09-16T20:13:38Z by presence test only, with no value printed. Request date recorded as 2026-09-16. Agent 2 track one is recorded BLOCKED, and agent 2 continues with public-page bounds and track two.
2. **Rulings transfer (ruling 4) cannot be executed by an agent.** An out-of-band handover to a human holder is outside any agent's reach. Agent 5 prepares the package with hashes and records the transfer as PENDING RECEIPT. It closes only when the receipt hash from the holder is written into transfer_record.json. Until then:
   - The opaque-id maps stay local and out of git (wave 2 decision).
   - The re-scored evaluation runs on opaque ids, but its seal stays procedural.
   - The coordinator verified none of the holder's authorship checks. The PI asserts them.
3. **State of wave 2 at issue.**
   - Agent 2 (label source) and agent 4 (instrument) are still running under the wave 2 brief.
   - Agent 3's wave 2 freeze (v1) has not started, because it waits on agent 2.
   - Each of these picks up its wave 3 assignment on return.
   - Agent 3 performs freeze v1 (wave 2) and then v2 (wave 3) as two separately hashed manifests. v2 waits on the wave 3 counts from agents 1, 2 and 4.
4. **Continuity.** Agents 1 and 5 resume with their wave 2 context. The interrupted C3 and C5 counts resume from their checkpoints.
5. **Rule D scope.** Agent 4's end-to-end runs use public broker alert packets for cohort objects. If lsst v11_1 packets cannot be retrieved publicly, that is recorded with the exact responses, and no substitute format is improvised. Alerts are fetched through the label-stripping path per rule C.
