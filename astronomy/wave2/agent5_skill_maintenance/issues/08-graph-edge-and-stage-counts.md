# SKILL.md says "twelve" cross-module preconditions, but graph.md lists sixteen and says "Thirteen" stages have none when the table gives twelve

**Status:** ready-to-file draft (not filed).
**Found by:** agent 5, wave 2, while reading the whole skill for the seed ledger.
**Affected files:**
- `fm-advantage-benchmark/SKILL.md`, line 25
- `fm-advantage-benchmark/references/graph.md`, line 3

**Patch:** `patches/08-graph-edge-and-stage-counts.patch`

## Quoted lines

```
SKILL.md:25:`references/graph.md` holds the twelve cross-module preconditions. Consult it before starting any stage.
references/graph.md:3:Sixteen cross-module edges. Thirteen of the twenty-nine stages carry none and chain only within their module, which is correct.
```

## Minimal repro

`repro/suite_counts.py` parses the graph.md edge table and counts its rows and the distinct stage codes in its From and To columns (`logs/suite_counts_before.txt`, last line):

```
graph.md edge rows 16 | distinct stages on an edge 17 ['A3', 'A4', 'D2', 'D3', 'D4', 'D5', 'I1', 'I5', 'P1', 'P2', 'P3', 'P6', 'P7', 'R1', 'R4', 'R7', 'R8'] | stages with no edge 12
```

## Expected vs actual

| Claim | Stated | Table |
|---|---|---|
| Cross-module edges (SKILL.md) | twelve | 16 rows. graph.md's own opening sentence also says "Sixteen". |
| Stages with no cross-module edge (graph.md) | thirteen | 29 − 17 = 12: D1, P4, P5, I2, I3, I4, R2, R3, R5, R6, A1, A2 |

## Root cause

This cannot be established from the zip. The likely cause is that the prose was not updated after edges were added. graph.md bolds two edges as "Absent in the record", which suggests a later addition.

## Proposed fix

- SKILL.md: change "twelve" to "sixteen".
- graph.md: change "Thirteen" to "Twelve".

## Verification (run)

- The patch applies alone and in series (`logs/patch_apply.txt`).
- After patching, the prose matches what `repro/suite_counts.py` still prints (`logs/suite_counts_after.txt`): 16 edges and 12 stages with no edge.
- `replay.py audit` on the patched copy prints `suite shape ok`.

## Controls

- **Must fire:** the count check flags the pristine prose, "twelve" against 16 and "Thirteen" against 12.
- **Must not fire:** the same check passes on graph.md's "Sixteen cross-module edges", which was already correct and is unchanged by the patch.
- The check was done by hand against the script output. It is not an automated test.
