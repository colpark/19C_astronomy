2026-09-17T13:15:24Z | coordinator | wave-4 agents launched in parallel: agent 2 (resumed, price of truth + WISeREP), agent 4 module V (FRESH session, independent of all producers), agent 5 (resumed, integrity close-out). Agent 3 (freeze v3) waits on V records; agent 1 (P4 package) waits on v3 + V.

## Module V overhead, interim (agents 1 and 3 have not run yet)

- agent2_price_of_truth: 44.8 min, 41 tool calls
- agent5_integrity_closeout: 13.5 min, 44 tool calls
- agent4_module_v: 52.4 min, 122 tool calls
- V share so far: 47% of wall time, 59% of tool calls. Cap is 15% (ruling 5).
- Interim disposition: **cap exceeded (FAIL)** on both measures. Agents 1 and 3 still have to run and will dilute the share, but they cannot bring it under 15% unless together they add at least about 2.2 times the wave so far in wall time (about 239 more minutes) and 2.9 times in tool calls (about 606 more calls). [Corrected: an earlier line said about 5.5 times, which was an arithmetic error.]. Rework inside V: about 22 tool calls (the label parse defects and the invariance comparator). The source is the harness usage records, not agent self-report.

## Module V overhead, final for wave 4 (all five agents)

- agent2_price_of_truth: 44.8 min, 41 tool calls
- agent5_integrity_closeout: 13.5 min, 44 tool calls
- agent4_module_v: 52.4 min, 122 tool calls
- agent3_freeze_v3: 7.6 min, 21 tool calls
- agent1_p4_package: 7.5 min, 23 tool calls
- Wave total: 125.8 min, 251 tool calls. V share: 42% wall time, 49% tool calls. Cap 15%: **FAIL**.
- Excluded: coordinator effort (not measured) and the wave-3 fresh evaluator. Source: harness usage records at each agent's completion. Agents 3 and 1 were resumed sessions; their figures cover only the wave-4 turn.
