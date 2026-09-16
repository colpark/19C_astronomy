# Opaque-id rule (declared before any id was generated)

Applies to both replay suites: `fm-advantage-benchmark/cases/cases.csv` (suite name `fm-advantage-benchmark`, 38 rows) and `astronomy/replay/cases/cases.csv` (suite name `astronomy_replay`, 20 rows).

## Seed, not chosen by agent 5

- `B` = lowercase hex sha256 of `astronomy/wave3/PANEL_BRIEF_WAVE3.md` = `a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6` (equals `astronomy/wave3/BRIEF_SHA256`, hashed by the coordinator before any wave-3 agent ran).
- For suite `s` and attempt `t` (starting at 0): `seed(s,t) = int(sha256(f"{B}:{s}:{t}").hexdigest(), 16)`, fed to Python `random.Random`.

## Ids

1. `order = rng.sample(range(n), n)`.
2. Walking `order`, each row draws `rng.getrandbits(40)` formatted as 10 lowercase hex digits; a draw that repeats an id already issued in either suite is redrawn.
3. Output rows are sorted by opaque id, so row order carries nothing beyond the random ids.
4. Ids have no prefix, no suite marker, no counter.

## Acceptance checks (permutation tests; test rng seeded with `int(sha256(f"{B}:permtest").hexdigest(),16)`, 20,000 permutations; only p-values are printed)

- polarity vs output row position (|difference of mean ranks|), both suites
- original cases.csv row index vs output row position (|Spearman rho|), both suites; covers authoring batch and the K/N block layout
- authoring agent vs output row position (Kruskal-Wallis H), astronomy suite; author from id stem: AST01-AST04 agent1, AST-P2-* agent2, AST3-* agent3, AST4-* agent4, AST5-* agent5, ASTC-* coordinator

If any p < 0.05, discard the attempt, increment `t`, and regenerate. Every attempt is logged. At most 20 attempts; if none passes, stop and report.

## Limit stated in advance

The rule is deterministic from public inputs, so anyone holding the public `cases.csv` and the brief hash can rebuild the map, and the input text itself matches `cases.csv` verbatim. The opaque ids therefore remove the id channel (issue 09) only for an evaluator confined to the blind file. The seal stays procedural, as the coordinator preamble states.
