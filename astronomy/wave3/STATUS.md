# Waves 2–3 status (coordinator, 2026-09-17)

All five wave-3 assignments have returned. Reports are in each `wave2/agent*/` and `wave3/agent*/` directory.

**The PI's next read is [`agent3_manifest_freeze/PI_rerat_packet.md`](agent3_manifest_freeze/PI_rerat_packet.md).**

## Where the benchmark stands

| Item | State |
|---|---|
| Manifest | v1 `ca00efe0…` and v2 `fba4259b…` frozen and validated. D5 does **not** advance: tau, exposure_key and subject_set have no PI ruling, label_source is UNDEMONSTRATED, and S waits on R1 |
| P4 | **No ruling.** (a) measured labels: UNMET. (b) tool recount after band: CLEARED and independently verified. (c) label source ratified: UNMET |
| Binding axis | Positive supply at measured labels. 0 demonstrated on 1,937,669 cohort objects. TNS is BLOCKED (no key) and Rubin has been off sky since 2026-07-14 |
| Band readings (frozen, δ 0.018) | Contamination ESCALATE; tool coverage ESCALATE; cluster, split and unprocessable PROCEED. PROCEED is unreachable without a subject-set change |
| Truth cost | 63 labels (δ 0.05, low): 66–84 spectra, 7–19 on-sky nights. 485 (δ 0.018, low): 502–644 spectra, 51–144 nights. Plus ≥100 slots per missed rare event |
| Instrument | PRE-I1 calibration only (BTS). ParSNIP without redshift adds nothing over the Fink-remapped floor. Binding-night MDE 0.032: resolvable at δ 0.05, not at 0.018. R1 not run |
| Tool coverage on Rubin | 2 PASS (CATS 5/10, GHOST 3/8), 14 FAIL, 9 UNDEMONSTRATED. Runs used JSON rows because v11_1 Avro is not publicly served |
| BTS label source (calibration) | SNIascore model labels bounded to [954, 2,057] of 7,843; 5,815 unresolved |
| Replay integrity | Opaque-id re-score: 20/20, 2 unearned, so issue-09 inflation measured at 0 (one run). Transfer to rulings holder PENDING_RECEIPT |
| Skill maintenance | 9 issue drafts; 8 patches verified in scratch copies; P2 refusal amendment drafted, its blind verification not yet run. Filed nowhere (no upstream known) |

## Decisions only the PI can make
1. Whether Rubin-era paid work starts (ruling 1 re-ratification).
2. Ratify or override tau, exposure_key, subject_set and label_source.
3. S2: keep it per the frozen bands, or exclude it through a new hashed band registration.
4. Whether to re-band at δ 0.05.
5. Supply `TNS_API_KEY`, and return the holder's receipt hash for `wave3/agent5_integrity/transfer_record.json`.

## Not yet done, and why
- **New wave-2 and wave-3 replay cases are not merged into a scored suite.** About 40 cases sit in the per-agent `replay_cases.csv` files. Merging and sealing them should wait until the holder has custody; otherwise the same party that wrote the cases holds their seal again.
- **P2 amendment blind re-run.** Held for the same custody reason, and it needs the patched skill applied in a scratch copy.
