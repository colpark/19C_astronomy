# Wave 2 · Agent 1: Rubin bands and prospective cohort

> Agent 1 returned this report as text, because the harness blocks subagents from writing REPORT.md. The coordinator saved it here without changing its substance. The brief hash was verified (`31a36617…f4eb`).

**P4 does not rule.** The binding axis is **positive supply at measured labels**. About 1.8–2.0M Rubin objects were first detected after every published subject cutoff, and none of them can be scored yet.

Three preconditions are unmet:
- The Rubin cohort has no measured labels. TNS returns HTTP 401.
- Tool coverage has not been recounted since its band was frozen.
- The label source is not ratified.

## Interrupted work (after the coordinator's resume message)
Both counts below were stopped at 19:50Z. Each is recorded as **UNDEMONSTRATED (interrupted, never zero)**, with a lower bound. Nothing is still running.

| Count | Progress when stopped | Lower bound | Script | Output |
|---|---|---|---|---|
| C3, full ALeRCE listing | slice 82 of ~450, ~1.5 h left | ≥189,641 objects | `scripts/count_c3_alerce.py` | `out/c3_alerce.json`, `out/c3_alerce_objects.csv`, `out/c3_progress.txt` |
| C5, straddlers | 2 slices incomplete | ≥21,126 | `scripts/count_c5_straddlers.py` | `out/c5_straddlers.json`, `out/c5_progress.txt` |

Both are resumable.

## Order of operations (`order_of_operations.log`, UTC)

| Time | Step | Hash |
|---|---|---|
| 18:48 | brief hash verified | |
| 18:51:26 | bands_FROZEN.md frozen | `8825ef80…00d2` |
| 18:51:43 | predictions sealed, before any broker, TNS or Rubin status page | `0dd6bd88…eab4` |
| 18:53–19:00 | endpoint probes | |
| 19:02 | count_protocol_FROZEN.md frozen | `5a5de4c8…ed82` |
| 19:02–19:50 | counts C1–C5, under amendments AM1–AM5 (logged with cause in `amendments.md`; they change procedure only, never bands or definitions) | |
| 19:50:37 | count file sealed, before any classification or TNS field was read | `fd864684…c1df` |
| 19:50:50 | labels read | |

**Disclosures:**
- Fink per-night statistics rows were printed during endpoint discovery, before the protocol freeze. They were not summed until 19:15.
- All broker object rows passed through `scripts/safe_fetch.py`. It strips class, probability, score, tag and crossmatch fields before anything is written or shown.

## Step 1: bands (addition A). PASS
**Start boundary: 2026-06-29.** RTN-011 §2.4 line 1288 says "formally declared on 2026-06-29"; 2026-06-30 is the date the announcement was posted.

**Admission boundary: first detection ≥ 2026-07-01T00:00 UTC** (MJD TAI 61222.000428).
- Claude Fable 5.1's cutoff is published only as the month "Jun 2026", so objects from the 06-29 and 06-30 nights are not after every cutoff.
- Those nights form stratum S0, which is reported separately and not included in the cohort.
- Picking 06-30 instead of 06-29 as the start would change only the night count, never cohort membership.

**Unit: one object per Rubin `diaObjectId`.**
- The same id seen in several brokers is one object.
- Different ids within 1″ merge only if their first detections are within 60 days. This is the wave-1 cut plus amendment A1.
- Solar System objects are excluded.

**First detection** is the earliest real detection (`firstDiaSourceMjdTai`).
- Forced photometry is not a detection. Pre-boundary forced flux is reported as stratum S2, never removed.
- Any earlier detection, including commissioning alerts since 2026-02-24, makes the object a straddler (S1). Straddlers are outside the cohort.

**Labels.**
- Measured = a TNS spectroscopic classification by a non-bot reporter.
- Broker classes are annotation.
- The wave-1 pos/neg maps are unchanged. A wider negative set (negB) was declared before counting, for sensitivity analysis only.
- Unlabelled objects are never negative.

**Thresholds**, from `planning_mde_bracket.csv` with k=8 and delta 0.018:
- Objects: 485–12,855. Nights: 40–1,515. A night needs at least 9 labelled candidates (k+1).
- **CLOSE** if the optimistic bounds are below 485 objects and 40 nights.
- **PROCEED** needs at least one labelled object per class, and either 12,855 labelled objects or 1,515 usable nights.
- **ESCALATE** otherwise.
- Contamination, cluster, split and unprocessable bands are in §6 of the file.
- The tool-coverage band applies only to a recount made after the band hash.

**Lag vs policy rule (§9):** an age-matched Poisson-binomial test at alpha 0.05 (the `power.py` default), run against both pre-2026 captures.

## Step 2: seals (rule C). PASS
Predictions were sealed before any contact with brokers or TNS, and counts were sealed before any label was read. Outcomes against the sealed predictions:

| Prediction | Predicted | Observed | |
|---|---|---|---|
| survey nights | 14 (9–16) | 10 | hit |
| cohort nights | 12 (7–14) | 9 | hit |
| cohort objects | 1e5–5e6 | 1.77–2.02M | hit |
| overstatement | 30–1000% | 74–98% | hit |
| label-collapse ruling | POLICY | POLICY | hit |
| P4 outcome | no ruling | no ruling | hit |
| share with one detection | 0.30–0.85 | 0.898 | **miss** (sample limited to the first 0.25 d, so biased young) |
| brokers disagree by >10% | yes | no | **miss** |

The predicted ranges were wide, so the hits carry little weight.

## Step 3: cohort count. Distinct objects PASS; full enumeration and labels UNDEMONSTRATED

Public LSST availability by broker:
- **Fink: yes.** `api.lsst.fink-portal.org` (statistics, objects, conesearch).
- **ALeRCE: yes.** `api-lsst.alerce.online/object_api/list_objects`. The `total` field is not a count, and wide queries return 504.
- **ANTARES: yes.** `api.antares.noirlab.edu/v1/loci`. `meta.count` caps at 10,000.
- **Lasair: UNDEMONSTRATED.** Status page reads "fully offline … Sept 14 through Wednesday Sept 16". Lasair LSST times out, and `/api/` returns 404.
- **Pitt-Google: UNDEMONSTRATED.** BigQuery returns 401 UNAUTHENTICATED (CREDENTIALS_MISSING).

| Quantity | Value |
|---|---|
| Fink raw alerts, cohort nights | 3,511,022 |
| Fink first detections | 1,773,044–2,018,299 (with vs without Solar System alerts) |
| Overstatement | 74–98% |
| ANTARES loci (complete) | 1,908,703 |
| ANTARES S0 loci | 112,990 |
| ALeRCE distinct objects | ≥189,641 (UNDEMONSTRATED, interrupted) |
| Straddlers (S1) | ≥21,126 (UNDEMONSTRATED, interrupted) |

**Cross-broker sample.** 3,000 of the 4,841 ALeRCE objects first detected in the first 0.25 d were checked:
- all 3,000 are in Fink and ANTARES;
- none differs by more than 1 s in first-detection time;
- none is placed before the boundary by any broker;
- none shares an ANTARES locus with a ZTF alert;
- none is missing its id, position or time.

**Disagreements (listed, not reconciled):**
1. Detections per object: 159 of 3,000 objects differ between ALeRCE and Fink. Summed, ALeRCE has 3,386, Fink 3,227 and ANTARES 3,386.
2. Fink's `objects` field is unique per night, not across nights. Its sum, 2,965,148, overstates distinct objects.
3. The brokers count different units. ANTARES counts loci, which merge ZTF and LSST and exclude loci with earlier ZTF alerts. Fink counts first-detection alerts.
4. Fink's night convention is undocumented. The data imply UTC date = dayObs + 1: Fink shows 336 visits for dayObs 0710–0714, against Rubin's "337 processed visits".
5. ALeRCE and ANTARES could be enumerated only after amendments AM1–AM4.

**Labels (read after the seal).**
- The TNS search, API and bulk CSV all return 401 `{"id_code":401,"id_message":"Unauthorized"}`.
- Fink's `in_tns` field marks 5,173 alerts on cohort nights as having a TNS counterpart. Those are alerts, not objects, and carry no reporter or class, so they are not measured labels.
- **P and Ng: UNDEMONSTRATED.**

## Step 4: return to sky. PASS
Sources: the Rubin scheduler reports table of contents, community.lsst.org News, and the live status page.
- **Nights with science visits since 2026-06-29: 10.** dayObs 0629, 0630, 0705, 0706 and 0708–0713, totalling 7,267 science visits.
- **Cohort nights: 9.** The eight whole nights from 0705 on, plus the part of dayObs 0630 after 00:00 UTC.
- **dayObs 0714:** 3 visits, none of them science. There has been no science since.
- **Scheduler reports:** "suspended while recovery from the July 2026 storm continues".
- **Latest news:**
  - The last News status post (2026-09-11) says Rubin is still off sky, with no return date.
  - Planned maintenance started 09-14.
  - No return-to-sky post exists. The latest News topic, dated 09-15, is about a forum migration.
- **Cross-checks:**
  - Scheduler science visits for dayObs 0710–0713 sum to 2,669, exactly the figure in the Rubin post of 07-17.
  - Fink alert nights match the scheduler nights exactly once shifted by one day.

## Step 5: the 2026 label collapse (calibration only, contamination FAIL on BTS). Ruling: POLICY
- **Normal accrual on pre-2026 captures:** 64–78% of objects are labelled 0–120 days after peak.
- **Late labels are rare:** 0.3–1.6% of objects still unlabelled at one capture had a label by the next capture, 244–402 days later.
- **2026-07-25 capture:** 28 of the 359 objects that peaked in 2026 are labelled. Lag alone predicts 257 or 220. Lower-tail p = 5e-146 and 9e-105.
- **2026-09-16 file:** 41 of 387 labelled, against 269 or 250 expected. p = 3e-131 and 3e-110.
- **Between 07-25 and 09-16:** no new labels on pre-2026 objects.
- **Onset (descriptive only):**
  - Labelled fraction by peak month: Dec 2025 54%, Jan 2026 19%, Feb–Jul 2026 2–15%.
  - BTS also saved fewer objects per month from Feb 2026: 20–76, against roughly 100–180 before.
- **Cause:** none of the sources read names one.

## Step 6: P4. NO RULING (the axis-ledger validator FAIL is honest)

| Axis | Value | Disposition | Band |
|---|---|---|---|
| positive_supply | measured P UNDEMONSTRATED; optimistic bound 1.77–2.02M; 10 nights | UNDEMONSTRATED | CLOSE ruled out (bound ≥485) |
| negative_supply | Ng UNDEMONSTRATED | UNDEMONSTRATED | CLOSE ruled out |
| contamination_exposure | 1.77–2.02M objects after every published cutoff; Gemini 3.1 Pro has no published cutoff | counted | ESCALATE |
| tool_coverage | 0/25 (wave 1) | counted | not rulable: band set after the count |
| cluster_structure | 3.51M alerts vs 1.77–2.02M objects; ANTARES 1.91M | PASS | PROCEED |
| split_integrity | ≥21,126 straddlers; sample 0/3,000 | UNDEMONSTRATED | none (count interrupted) |
| unprocessable_units | sample 0/3,000 | UNDEMONSTRATED | none (no whole-cohort table) |

**Unmet preconditions:**
- (a) the supply axes have no number;
- (b) the tool-coverage band was set after its count;
- (c) the label source is unratified.

**Binding axis: positive_supply at measured labels.** Resolving it needs an external input (TNS credentials) and survey time; Rubin has been off sky since 07-14. Contamination × supply comes second.

**Lean, not a ruling: ESCALATE.** Even the smallest bracket value, 485 labelled objects, is far above anything obtainable today.

**Validator output:** `axis_ledger_rubin.json` FAILs on the missing `ruling`, deliberately. `rubin_cohort_count.json` PASSes provenance.

## Still UNDEMONSTRATED

| Item | Blocks |
|---|---|
| measured P and Ng (TNS credentials) | P3 supply, P4, P5 queue |
| tool-coverage recount on Rubin | P4 precondition (b) |
| full ALeRCE enumeration, the 1″/60 d id merge, cohort-wide one-detection share | merged object count; split and unprocessable axes |
| straddler count | split_integrity |
| Lasair (outage), Pitt-Google (credentials) | broker coverage |
| Gemini 3.1 Pro cutoff | contamination PROCEED |
| budget, cost of action, S | P5, P7 |
| PPDB-only precovery | the cohort count is an upper bound with respect to it |

## Replay cases (`replay_cases.csv`, `replay_rulings.csv`)
- **AST1W2-01** (P3, must_fire): per-night unique objects reported as supply. Ruling: REFUSE.
- **AST1W2-02** (P4, must_fire): a ruling issued on a post-hoc band with uncomputed labels. Ruling: REFUSE and name the binding axis.
- **AST1W2-03** (D2, must_not_fire): an exposure-derived boundary with the June nights as a reported stratum. Ruling: ACCEPT.
- **AST1W2-04** (P5, must_fire): a queue built from pre-2026 BTS label yield after the collapse was ruled POLICY. Ruling: REFUSE.
