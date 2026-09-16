# Panel brief: astronomy supply gauge (pre-P1 sketch)

Candidate: **live time-domain astronomy**, meaning the Rubin LSST alert stream plus the ZTF Bright Transient Survey (BTS) label base.
Branch declared: **prediction**. The decision governed is spectroscopic follow-up allocation, where k slots are committed per round from the candidate transients.

Each agent in this panel works under the contract in `../fm-advantage-benchmark/` (SKILL.md, references/provenance.md, references/manifest.md, references/loop.md, references/graph.md, plus the stage briefs named in its scope). Read those files before starting.

## Status of this run

This is a pre-P1 sketch and not a P4 ruling. The skill refuses a ruling until all seven axes carry numbers from full source reads. D5 ratification has not happened, and neither budget nor cost of action has been supplied. Every stage that depends on them records UNDEMONSTRATED.

## Non-negotiable rules for every agent

1. **Count distinct astrophysical objects, never alerts, detections or rows.** Raw alert counts overstate effective n by roughly a thousandfold. Report raw beside clustered, with the overstatement percentage.
2. **Read sources whole.** Download full text with `curl` (arXiv: `https://arxiv.org/pdf/<id>` then `pdftotext -layout`; HTML docs via curl). Save each full-text file under `<your_dir>/sources/` and cite locators (section, table, page or line). A fact taken from a search snippet, abstract, WebFetch summary or memory must not enter the ledger as a decision input. If you can only get a summary, mark `read_in_full: false` and say which stages that blocks.
3. **Every number that decides anything carries five provenance fields**: referent, source (with an identifier such as a URL plus section, file plus sha256, or script plus function), population, adjudicator and falsifier. Validate with `python3 ../fm-advantage-benchmark/scripts/validate.py`.
4. **Never write "assumed", "conventional" or "standard" as a source.** If a value cannot be derived, mark it UNDEMONSTRATED and name the stages that cannot run.
5. **Dispositions are PASS, FAIL or UNDEMONSTRATED.** Nothing softer. An interrupted or uncomputable count is UNDEMONSTRATED, never zero.
6. **List disagreements, never reconcile them.** That covers disagreements between sources and between a source and the data.
7. **Don't widen definitions after a low count, and don't filter on the outcome.**
8. **Write only inside your own directory** under `astronomy/`. Do not run git. The coordinator commits.
9. Local data: `astronomy/data/raw/ztf_bts_all_2026-09-16.csv` (11,217 BTS data rows (corrected from 11,218), sha256 in SHA256SUMS). Python with numpy, pandas, astropy, scipy and scikit-learn is at `/tmp/claude-1000/-home-aid1-Documents-4-19C-astronomy/addb1fc3-63d3-4989-8753-aa4c400b100e/scratchpad/venv/bin/python`. Put analysis scripts in your directory so every number is reproducible.
10. Today is 2026-09-16. Rubin alerts began streaming to brokers in February 2026, and the ten-year LSST formally started 2026-06-30. Verify these claims from primary sources rather than repeating them.

## Deliverables per agent

- `REPORT.md`: findings, dispositions per criterion, disagreements, and what remains UNDEMONSTRATED together with the stage it blocks.
- JSON records that match `../fm-advantage-benchmark/schemas/` where a schema exists (corpus_ledger, cut_curve, axis_ledger, power_record, tool_card, provenance records), each passing `validate.py` or listing its failures honestly.
- `sources/`: the full texts actually read, plus `seed_ledger.json` recording read_in_full and contribution for each.
- `replay_cases.csv`: 2 to 4 astronomy cases drawn from real facts you found, using the columns `case_id,stage,polarity,sealed,input` from `cases/cases.csv`. Include at least one must_not_fire. Put the ruling for each in a separate `replay_rulings.csv` with the columns `case_id,expected_ruling,rule_it_rests_on`. These feed the independent-corpus replay.
