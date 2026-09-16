# Issue 09 inflation: measured

A fresh evaluator (general-purpose subagent, claude-opus-5, no panel context) re-scored the wave-1 astronomy suite on opaque ids. Launch was 2026-09-16T20:24Z. Its verdicts were scored with `scripts/rescore.py`, which calls the unchanged vendored `replay.py score`.

| Run | Ids | Polarity | Unearned |
|---|---|---|---|
| Wave 1 | original (AST…, ASTC…) | 20 of 20 | 2 (both P2) |
| Wave 3 | opaque, shuffled | 20 of 20 (14/14, 6/6) | 2 (both P2) |
| **Delta** | | **+0** | **+0** |

- **Verdicts hash.** `131a6ad4…5d38`. The evaluator reported it and the coordinator recomputed it before the join.
- **Pinned skill and blind-input hashes.** Verified before launch.
- **Measured inflation from issue 09 on this suite: zero.** Removing polarity-bearing ids changed no verdict polarity and no unearned count. The same two P2 cases went through global refusal 1 again.

## Reading it

1. **This is one run per condition.** A delta of zero cannot separate "the ids carried no signal the evaluator used" from run-to-run noise that happened to cancel. What it does show is that 20 of 20 is not an artefact of the ids.
2. **The P2 gap reproduced independently.** A second fresh evaluator, blind to ids, again routed the leaked-feature floor and the unmatched pair through refusal 1 and not through a P2 rule. That strengthens the case for the wave-2 P2 amendment.
3. **Issue 09 stays open as a design defect.** Ids that encode polarity are still a leak for any evaluator that sees them. This measurement says only that this evaluator, on this suite, did not need them.
4. **Evaluator disclosures, recorded and not treated as contamination.**
   - It ran a fix-up edit on its own output file in the same command as `sha256sum`.
   - It ran non-recursive `ls` on `references/`.
   - It reports opening no forbidden file.
5. **The seal is still procedural.** Polarity stays readable in the repo (`cases.csv`, `score_*.txt`, git history), and the out-of-band transfer is PENDING_RECEIPT. The evaluator was the same model family as the panel and the subject set.

Per-case mapped output is kept in the gitignored `holder_handover/rescore_wave3/`.
