# Independent-corpus replay: result

**Suite.** 20 astronomy cases: 14 must_fire and 6 must_not_fire. Six are sealed. `replay.py audit` reports "suite shape ok".
- 18 cases come from real facts found by the five panel agents.
- 2 must-not-fire controls (ASTC-01 and ASTC-02) were written by the coordinator from panel facts.
- AST5-03 was dropped as a duplicate.
- AST5-04 was excluded as contested (`cases/EXCLUDED.csv`).

**Stage under test.** A fresh agent that read only `SKILL.md`, `references/` and `evaluator/blind_inputs.csv`. That file holds case_id, stage and input; polarity and rulings are withheld, and the rows are shuffled.

**Seal.** The hashes in `SEAL_SHA256SUMS` were committed (8b01d13) before any verdict existed, and `sha256sum -c` passes after scoring.

## Scores (`scripts/replay.py`, unchanged from the skill)

| Set | must_fire | must_not_fire | validator-only (unearned) |
|---|---|---|---|
| development (14) | 10 of 10 | 4 of 4 | AST-P2-04 |
| sealed (6) | 4 of 4 | 2 of 2 | AST-P2-02 |
| all (20) | 14 of 14 | 6 of 6 | 2 |

Full output: `evaluator/score_{development,sealed,all}.txt`. Verdicts: `evaluator/verdicts.json`.

A spot check of the ruling text for AST01, AST3-03, AST4-04, AST5-02 and AST-P2-03 against the sealed rulings found the same disposition and next action in each case. `replay.py` itself scores polarity only.

## What this does and does not show

1. **Polarity reproduced on an out-of-project corpus, at 20 of 20.** The stage briefs made the right fire / not-fire call on astronomy situations their source record never saw. That includes the label-source distinction, contamination, answer-in-own-source, the alert-vs-object unit, and resolution vs delta. This is the first evidence of generality the skill asks for.
2. **The skill's own caution applies to this result.** replay.md says "a clean sweep usually means the suite is too easy." These cases were written by agents that had just applied the same skill, so they are cast in its vocabulary. Treat 20 of 20 as consistency on a new domain, not capability.
3. **Two passes were unearned, and both are in P2.** The P2 stage brief has no refusal of its own. Its unmatched-pair and leaked-feature floor cases (AST-P2-02 and AST-P2-04) were caught only by global refusal 1 (provenance). Following the skill's repair rule, P2 needs its own refusals:
   - **refuse a floor/ceiling pair** not on matched data, split and metric, or scored on a tuning set;
   - **refuse a floor built on features** that only exist after the governed decision.

   This is the same kind of gap the source record's first sealed pass found in P4 and A1.
4. **The seal is procedural.** The rulings sit in this public repo, and they are held by the party that orchestrated the panel and wrote two cases. The evaluator was told not to open them and reports it did not. That cannot be verified from outside. For a seal that carries weight, give `cases/RULINGS_SEALED.csv` and the polarity column to someone else, and re-run with new cases they hold.
5. **Weaker than the skill's suite in one respect.** It has no runtime-module or ladder cases, because nothing in this pre-P1 sketch ran a harness.
