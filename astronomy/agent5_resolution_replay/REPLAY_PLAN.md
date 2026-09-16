# Independent-corpus replay plan: fm-advantage-benchmark suite against live time-domain astronomy

Agent 5, 2026-09-16. This is a plan and a mapping. No verdict has been produced and no case has been scored.

## 1. Why this replay exists and what it can show

`references/replay.md` says the 38-case suite and the stages come from one project, so matching its rulings says nothing about cases outside it. It also says a seal held by the party that wrote the spec proves nothing. The astronomy run supplies both missing pieces: cases drawn from a corpus that shares no stages with the source record, and a seal held by someone other than the case authors.

The replay can show one of two things per stage:
- the stage's refusal fires on an astronomy instance of the failure it was built from, and stays silent on the astronomy must-not-fire instance, or
- it does not, and the stage's rule is project-specific.

It can't show the rules are *correct* for astronomy. It can only show they transfer or fail to transfer.

**Constraint I followed.** I did not open `fm-advantage-benchmark/cases/RULINGS_SEALED.csv`. Every mapping below is written from `cases/cases.csv` inputs only. For the twelve sealed cases, that means I have read their inputs, which `replay.md` allows ("cases.csv: the stage under test"). I have not read their rulings.

## 2. Case-by-case mapping (38 cases)

Legend. **Analogue**: a concrete astronomy situation built from facts read in full, with a locator. **Harness-level**: the case is about the agent runtime (grant, prompt bytes, gates, thermal). It has no corpus analogue, but it replays unchanged once an astronomy harness exists. **No analogue**: nothing in the astronomy material read so far instantiates the failure.

Sealed astronomy analogues must stay sealed. If an analogue is built for a sealed source case, its ruling goes only to the holder (section 4).

| case_id | stage | pol. | sealed | astronomy analogue | facts and locator | owner of the evidence |
|---|---|---|---|---|---|---|
| K01 | P4 | fire | N | Supply gate passed on all BTS objects (11,204 distinct) while the binding subset is unexposed items. Counting rows that peaked after the latest subject cutoff (Claude Fable 5.1, June 2026) gives 30 rows and 1 classified transient. | agent5 out/bts_rounds.json `rows_peaking_on_or_after_cutoff_plus_one_day`; subject_set_slot.json | agent3 (exposure), agent1 (supply) |
| K02 | P3 | fire | N | A portfolio reported at abundant units: about 10^6 alert packets per night, about 500 filtered candidates, 5 to 10 saved. The independent unit is the distinct object per round. | arXiv:2009.01242 section 2.1 lines 133-137, 147-148, 159-161 | agent1 |
| K03 | P3 | fire | Y | Nominal labelled counts versus usable labels: 11,217 BTS rows, of which 3,374 carry type "-" and give no label. The Fink paper reports 23,840 alerts, which are 1,021 unique SN Ia objects. | bts CSV type counts (agent5 inspection); arXiv:2111.11438 lines 38, 130 | agent1, agent3 |
| K04 | P3 | fire | N | A split keyed on survey identifier while one astrophysical object carries two identifiers (13 IAU names shared by 26 ZTF IDs). The BTSbot splits are by source ID. | agent5 out/bts_object_identity_controls.json; arXiv:2401.15167 lines 394-400 | agent1 (split integrity) |
| K05 | P4 | fire | Y | A proceed ruling on classified SN Ia supply while the negative supply (CV/AGN/dim candidates, 1,652 non-bright sources in a 41-night window) and exposure by cutoff are uncounted. | arXiv:2401.15167 lines 898-902; agent5 bts_rounds.json | agent1 |
| K06 | P2 | fire | N | Floor headroom: a metadata-only network (no images) reaches committed-set purity 0.912 against 0.930 for the multimodal network on the same split, 98.1% of the ceiling. | arXiv:2401.15167 Table 6 lines 1323-1335 | agent2 |
| K07 | I5 | fire | Y | The served selector differs from the certified one. BTSbot v1.0 ran in production in October 2023, while the evaluated model is v1.0.1. | arXiv:2401.15167 footnote 17 lines 1019-1023 | agent4 |
| K08 | I3 | fire | N | A tool card for SNIascore written from the paper's recommended cut (score > 0.6 or > 0.8), while production reporting used a 0.9 threshold. The card has to be written from the code that runs. | arXiv:2104.12980 Table 2 lines 387-407, section 7 lines 541-546 | agent4 |
| K09 | I4 | fire | N | A construct mismatch. SNIascore classifies a spectrum that has already been taken, so it can't score *which candidates should receive* a spectrum. Substituting it as a selection tool measures a different quantity. | arXiv:2104.12980 sections 1 and 7 | agent4 |
| K10 | R5 | fire | N | Harness-level. | none | runtime owner |
| K11 | R5 | fire | Y | Harness-level. | none | runtime owner |
| K12 | R5 | fire | N | Harness-level. | none | runtime owner |
| K13 | R4 | fire | N | Harness-level (grant read from configuration). | none | runtime owner |
| K14 | R6 | fire | N | Harness-level (declared versus emitted prompt). | none | runtime owner |
| K15 | A3 | fire | N | Unequal denominators, a real instance. Selector purity 93.0% (test split, bright-transient purity) is compared with scanner purity 96.7% or 95.6% (41-night window, extragalactic-transient purity) as "93% vs ~97%". Filed as **AST5-01**. | arXiv:2401.15167 lines 739-742, 765-766, 806, 1132 | agent5 |
| K16 | A3 | fire | Y | No analogue in the corpus. A parser-coverage failure needs an agent arm's answers. | none | adjudication owner |
| K17 | A4 | fire | Y | A directional practice on an effect below its resolution: +0.018 purity acted on, with an unpaired MDE of about 0.045. Filed as **AST5-02** (sealed). | arXiv:2401.15167 lines 1323-1335, 1360-1364; delta_slot.json | agent5 |
| K18 | LADDER | fire | N | No analogue in the corpus. | none | loop owner |
| N01 | R3 | not | N | Harness-level. | none | runtime owner |
| N02 | R5 | not | N | Harness-level. | none | runtime owner |
| N03 | R7 | not | Y | A cosmetic declared-versus-received difference. The explorer documentation names the peak-time column `time`, and the CSV header names it `peakt`. The referent is the same, as the zero-point test confirms (JD-2458000, 96.27% year agreement). | sources/bts_explorer_info.txt line 102; agent5 bts_rounds.json | agent5 |
| N04 | I5 | not | N | Performance reproduced after a time shift. BTSbot on a present-day window gives ROC AUC 0.988 against 0.985 on the test split, with no data shift. | arXiv:2401.15167 section 4.2 lines 883-905 | agent4 |
| N05 | I3 | not | N | Checkpoint identity by content hash or commit pin where no version string exists. The analogue is the clone pins agent4 records for the broker and classifier code. | astronomy/agent4_tools_instrument/clone_pins.tsv (not read by agent5) | agent4 |
| N06 | P3 | not | N | Unprocessable units documented, not repaired. Fink feature extraction keeps 23,775 of 86,422 alerts, because it needs at least 3 epochs per filter. | arXiv:2111.11438 Table 1 lines 114-123, section 3.1 lines 233-243 | agent1 |
| N07 | A1 | not | Y | No analogue in the corpus. | none | adjudication owner |
| N08 | R5 | not | N | Harness-level. | none | runtime owner |
| N09 | P3 | not | N | Raw beside distinct with both controls run. 11,217 rows give 11,204 objects (0.116%); shared IAU names join, and two different SNe 1.92 arcsec apart stay separate. Filed as **AST5-04**. | agent5 out/bts_object_identity_controls.json | agent5 |
| N10 | LADDER | not | Y | No analogue in the corpus. | none | loop owner |
| K19 | D1 | fire | N | A fact adopted from an abstract would be wrong. The Fink abstract gives 23,530 test alerts, while the body gives 23,425 and 23,465. The BTS I introduction claim that SEDM is "capable of classifying >10 SNe" every night is stated for the 18.5-19 mag range only, so lifting it without the range misstates capacity. | arXiv:2111.11438 lines 40, 540, 679; arXiv:1910.12973 lines 135-137 | all agents |
| K20 | D3 | fire | Y | A cut relaxed to clear a unit floor. The proposal widens the BTS peak-magnitude cut from 18.5 to 19 to raise post-cutoff unit counts, where classification completeness falls from 93% to 75%. | arXiv:2009.01242 abstract lines 50-51 | agent1 |
| K21 | D4 | fire | N | A target without a feasibility count. A plan adopts the SNIascore TPR gain (+0.37) as the delta for follow-up *selection* with no count on the selection referent. | delta_slot.json candidates | agent5 |
| K22 | D4 | fire | N | A mixed label source. The TNS type column combines human-vetted spectra, model-assigned SN Ia classes (SNIascore, since 2021-04-15) and light-curve-only dwarf-nova removals. Filed as **AST5-03**. | arXiv:2104.12980 section 7; arXiv:2009.01242 section 2.4 | agent3 |
| K23 | D2 | fire | N | SYNTHETIC in the source suite. The analogue is pending: a rule change after a count, for example dropping rows that peaked in 2026 after seeing that only 41 of 387 carry any type (29 of them classified transients). | agent5 bts_rounds.json per_calendar_year_peak_rates 2026 | agent1 |
| K24 | D5 | fire | N | SYNTHETIC in the source suite. The analogue is pending: a slot sourced as "standard", such as a chance level written as "the conventional ~100 candidates per night". No instance has been found yet. | none yet | D5 owner |
| K25 | D2 | fire | Y | Answer in the item's own source. An allocation item built from BTS where the object's public TNS classification report predates every subject cutoff (1,648 of 11,217 rows peak after the earliest domain-limited cutoff; almost none after the latest). | agent5 bts_rounds.json; subject_set_slot.json | agent3 |
| N11 | D2 | not | N | A clean corpus publication. The candidate is agent1's frozen rules with sha256 plus exclusion ledger, if published complete. Not read by agent5. | astronomy/agent1_supply_corpus/corpus_rules_FROZEN.md | agent1 |
| N12 | D3 | not | Y | Pending a real cut sweep (agent1/agent3), for example a positional match radius for object identity. The 2-arcsec control above shows a loose radius merges distinct SNe. | none yet | agent1 |
| N13 | D4 | not | N | A well-formed k slot: k = 8 per night, population named as rounds, 327 triggers over 41 nights, falsified by any 30-night trigger log outside 4.5-10. This is agent5's own k_slot.json, so another agent must build the case input to avoid self-grading. | k_slot.json | agent other than agent5 |

Tally: 23 concrete analogues (4 filed by agent5 as AST5-01 to AST5-04), 3 pending with no instance yet (K23, K24, N12), 8 harness-level (K10-K14, N01, N02, N08), and 4 with no analogue in the corpus (K16, K18, N07, N10).

## 3. Merging the panel's replay_cases.csv files

Inputs: `astronomy/agent{1..5}_*/replay_cases.csv` and the matching `replay_rulings.csv`.

1. **Schema check.** The case files must have exactly the header `case_id,stage,polarity,sealed,input`, and the rulings files `case_id,expected_ruling,rule_it_rests_on`. A file that fails the check is returned to its author, never repaired by the merger.
2. **Namespacing.** Case IDs must be unique across agents. Agent5 uses `AST5-NN`. Other agents' IDs are prefixed `AST{n}-` if they aren't already. Keep a map from old to new IDs.
3. **Stage codes.** `stage` must be one of the codes used in `cases.csv` (D1-D5, P1-P7, I1-I5, R1-R8, A1-A4, LADDER). `replay.py::mod` maps by first letter, so an unknown code is reported as module `?` and must be rejected.
4. **Duplicates.** When two agents filed the same real fact for the same stage, keep both, mark them as a pair, and score them once each. Don't pick one, because that would be reconciliation.
5. **Shape audit.** Run the vendored `replay.py audit` logic on the merged file. Every module present needs at least one must-not-fire case, and must-not-fire cases need to make up at least a quarter of the total. If the merged set fails, the fix is to add must-not-fire cases from real facts. Dropping must-fire cases is not a fix.
6. **Seal assignment.** The case authors don't choose the seal. The holder (section 4) marks a random subset of about a third as sealed with a recorded seed. The flags that authors (agent5 included) wrote in their own files are advisory only.
7. **Layout for running the unchanged script.** `replay.py` resolves `cases/` relative to its own location. Build `astronomy/replay/scripts/replay.py` as a byte-identical copy (record the sha256 of both), `astronomy/replay/cases/cases.csv` as the merged cases with polarity removed (see 4.3), and nothing else under `cases/`. `RULINGS_SEALED.csv` for the astronomy set is never placed in the repo.

## 4. Seal protocol

### 4.1 Parties

| party | holds | may not |
|---|---|---|
| case authors (agents 1-5) | their own cases and rulings until hand-off | run `emit`, `score` or any stage under test on the merged set |
| coordinator | merged cases with polarity removed; hashes | read any rulings file after hand-off |
| holder: the human, or a party that wrote neither the skill nor any case | all rulings files, the polarity column, the seal seed | take part in producing verdicts |
| stage under test: a fresh session with no access to `astronomy/agent*/`, rulings, or panel transcripts | only `astronomy/replay/cases/cases.csv` and the skill | read rulings, polarity or the agents' directories |

### 4.2 Sequence

1. Each agent writes `replay_cases.csv` and `replay_rulings.csv` and records their sha256 values in its REPORT. For agent5 these are replay_cases.csv `0604180b98e4eec3987418e880e9063543f16b85eadd78a083e1664f0f0ca850` and replay_rulings.csv `d0760d6d955d4135322845dbc01a0ef7e349b97110d96a4bd1a004d6e031a287`.
2. The coordinator records every file hash in `astronomy/replay/HASHES.md`, then hands every `replay_rulings.csv` to the holder and deletes it from the repository working tree before the first commit that contains the merged cases. A rulings file that ever appears in a commit read by the stage under test voids the seal for those cases, and the replay must say so.
3. The coordinator merges following section 3 and removes the `polarity` column, which goes to the holder.
4. The holder draws the seal subset from a recorded seed and splits development from sealed.
5. The stage under test runs on the development set and writes `verdicts_dev.json` in the `replay.py emit` format (`fired`, `ruling`, `via`). The file is hashed before the holder releases development polarity.
6. Score the development set. Revisions are allowed and each one is recorded as an amendment with its cause.
7. The stage under test runs once on the sealed set and writes `verdicts_sealed.json`, which is hashed before release.
8. The holder releases sealed polarity and rulings. Score, then report must-fire and must-not-fire rates separately per module, plus validator-only passes (`via: validator`).
9. The two limits are reported beside every figure. A clean sweep on astronomy cases that panel agents who had read the stage briefs wrote measures consistency between those agents and the briefs, not capability. And cases without an astronomy analogue (harness-level and no-analogue rows in section 2) are untested by this replay, not passed.

### 4.3 Two problems in the vendored design that this protocol works around (listed, not repaired in the skill)

- **Polarity is visible to the stage under test.** `replay.md` lists `cases/cases.csv` as readable by the stage under test, but that file carries the `polarity` column, and `replay.py emit` prints `polarity=` for every case. A stage that reads polarity can match every case without a rule of its own. That's why the astronomy replay strips polarity before hand-off (step 3).
- **The rulings file doesn't decide pass or fail.** `replay.py score` judges each case by `fired` against `polarity` alone and reads `RULINGS_SEALED.csv` only to annotate failures with `rule_it_rests_on`. What the seal actually protects is polarity, plus the ruling text for qualitative review. The holder therefore has to hold polarity as well as the rulings.
- **Sealed count disagreement.** `replay.md` says twelve cases are sealed, to "develop on the other twenty-six" and "open the nine once". `cases.csv` has 12 sealed. The "nine" is inconsistent with the file.
- **The vendored rulings sit in the repo.** `fm-advantage-benchmark/cases/RULINGS_SEALED.csv` lives in the same repository as the spec and cases, which is the "same party" seal that `replay.md` says proves nothing. Recommendation: the human moves it to the holder too, and records its sha256 before anyone runs `replay.py score`. agent5 did not open or hash it, because hashing requires reading the bytes.

## 5. What agent5 filed

| case_id | stage | polarity | source-suite analogue | facts |
|---|---|---|---|---|
| AST5-01 | A3 | must_fire | K15 | BTSbot 93.0% (test split) versus scanners 96.7%/95.6% (41-night window) |
| AST5-02 | A4 | must_fire | K17 | +0.018 purity acted on; unpaired MDE about 0.045 |
| AST5-03 | D4 | must_fire | K22 | TNS types mix human spectra, SNIascore auto-classes and light-curve-only removals |
| AST5-04 | P3 | must_not_fire | N09 | 11,217 rows to 11,204 objects with must-join and must-separate controls |

Rulings are in `replay_rulings.csv`, a separate file, for hand-off under 4.2 step 2.
