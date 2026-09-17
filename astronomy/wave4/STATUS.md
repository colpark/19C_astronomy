# Wave 4 status (coordinator, 2026-09-17)

All five wave-4 assignments have returned. The PI's next read is [`agent1_p4_package/escalation_memo.md`](agent1_p4_package/escalation_memo.md).

| Item | State |
|---|---|
| P4 | **REFUSED to rule.** Positive and negative supply have no number (supply.md line 37). ESCALATE is also a ruling, so it is not available either. On V-cleared numbers, no axis reads CLOSE |
| Preconditions | (a) measured labels: **UNMET** (TNS BLOCKED ×2, WISeREP BLOCKED). (b) **CLEARED** (V-O02). (c) **CLEARED** (ruling 4) |
| Band readings (frozen 0.018; 0.05 reported beside) | Contamination and tool coverage: ESCALATE. Cluster, split and unprocessable: PROCEED, but each leans partly on V_PENDING numbers |
| Manifest | v3 `bd0fa4c6…` frozen: delta 0.05 RATIFIED; label source RATIFIED WITH CONDITIONS, with its numbers V_PENDING |
| Escalation memo (ladder rung 2, not a P4 ruling) | **Option 1: buy human-confirmed labels.** N=63: 66–84 spectra, 33–42 P60 h (V-R02); N=12,855: 13,294–17,065 spectra (V-R04). **Option 2: close.** The ratified budget contains no telescope time |
| Module V | 33 of 38 cleared. L01–L05 are held on two readings: the E5 cut (1259.5 literal vs 1289.5 arithmetic) and twin-row keying. Overhead was **42% of wall time and 49% of tool calls, against a 15% cap: FAIL** |
| Custody | PENDING_RECEIPT: no receipt hash in the repo. Every blind result stays "procedural" |
| Quarantine | Polarity-listing score and verdict files untracked and kept holder-side (bb77e30). The leak is permanently recorded; history is unchanged |
| PPDB | Not released at 2026-09-17T14:19Z. Cohort O = 1,937,669 stays an upper bound |
| Drafts for PI only | two community notes in `agent5_integrity_closeout/notes/`, not distributed |

## PI decisions requested
1. Choose option 1 (with δ and N, registering 0.05 bands first if 0.05 is to gate) or option 2 (close).
2. Subject set: whether to change it. Nothing else lets contamination ever read PROCEED.
3. E5 cut reading and twin-row keying. These let V clear L01–L05. Note that ruling 4's [803, 2,247] reproduces only under 1289.5.
4. tau, exposure_key and subject_set are still unratified, so D5 does not advance.
5. S2 stratum conflict: ruling 6 conflicts with frozen bands §3.
6. Supply the holder's receipt hash, TNS credentials, or a telescope-time line in the budget.
7. Module V overhead cap: raise it, or narrow V's scope. At 42–49% it breaches ruling 5.
