# evaluator/

| File | Role | Who reads it |
|---|---|---|
| `blind_inputs_opaque.csv` | the 20 wave-1 astronomy cases under opaque ids: `opaque_id,stage,input`, rows sorted by random id | the fresh evaluator |
| `EVALUATOR_PROMPT.md` | exact launch text (below its rule line) plus the coordinator's pre-launch hash checks | coordinator |
| `verdicts_opaque.json` | written by the evaluator; absent until the coordinator launches it | coordinator, then `scripts/rescore.py` |

Re-score, after the verdict file's sha256 is logged:

```
python3 scripts/rescore.py --verdicts evaluator/verdicts_opaque.json --outdir holder_handover/rescore_wave3
```

The outdir sits under the gitignored `holder_handover/` because `score_*.txt` lists polarity per case. `rescore_summary.json` holds only aggregates and may be copied out.
