# Agent 3: label source, exposure key, contamination (D4, P3, D2)

> Agent 3 wrote this report and returned it as text, because the subagent harness blocks report-file writes. The coordinator saved it here without changing its substance.

**Headline.**
- **Label source.** The basis of the 7,843 labels can be resolved by class, but not by who reported each label or whether a model produced it.
- **Contamination axis: FAIL.** Zero labeled BTS objects fall after every subject's cutoff.
- **Rubin stream.** The post-cutoff Rubin stream is small so far, and it is paused: the observatory has been off sky since a storm evacuation on 14–15 July 2026.

## 0. Disagreements with the brief and data files
- **Object count.** The file holds 11,217 objects (11,218 lines including the header), not 11,218. The coordinator has since corrected this.
- **peakt zero point.** It is JD − 2458000, not days since 2018-01-01. Locators: explorer doc line 79; Fremling+2020 Table 1 note d; Perley+2020 Fig. 13. The coordinator's prompt guessed wrong.
  - SN2018cne has peakt 290.83. That is 2018-06-21 under JD−2458000 and 2018-10-18 under the other offset. The SNIascore paper places its max-light spectrum on 2018-06-14.
  - The median peak-minus-discovery lag is 11 d under JD−2458000 and 130 d under the other offset.
  - A year-match check cannot tell the two apart (0.963 vs 0.961), so it was not used.
- **LSST start.** It was formally declared on 2026-06-29 (RTN-011 v9.0, line 1288). 2026-06-30 is the date the announcement was posted.
- **First Rubin alerts.** 2026-02-24 (RTN-011 line 2468). This agrees with the brief.

## 1. D4 label source: UNDEMONSTRATED
Counts are over 11,217 unique ZTFIDs, before clustering.

| Label basis | Objects | % all | % labeled |
|---|---|---|---|
| Unlabeled | 3,374 | 30.08 | – |
| Labeled | 7,843 | 69.92 | 100 |
| Spectroscopic transient class | 6,867 | 61.22 | 87.56 |
| Spectroscopic plus a photometric criterion (SLSN-I/II luminosity cut, SN IIP, SN Ia-91T) | 310 | 2.76 | 3.95 |
| AGN/CV, possibly photometric-only | 561 | 5.00 | 7.15 |
| AGN?/CV?, basis undocumented | 105 | 0.94 | 1.34 |

The basis for each class comes from Perley+2020 (Fig. 3 caption, §2.4, App. E) and Fremling+2020 (§3.1, §3.3).

**The load-bearing split cannot be made from the file.**
- **SNIascore labels are model annotation, and the file cannot say how many there are.** The count lies between 0 and 3,131, which is up to 39.9% of labeled objects.
  - SNIascore began auto-reporting to TNS on 2021-04-15.
  - The 1,936 plain "SN Ia" labels on objects that peaked more than 30 days before that date cannot be SNIascore's.
  - SN2021ijb, its first automated classification, is a certain member.
- **The reporter is unknown for all 7,843 labels.** The file does not say whether BTS, another group or the SNIascore bot made each one.
- **666 AGN/CV labels may rest on photometry alone.** That remains unresolved.
- **Resolving this needs per-object TNS classification reports.** TNS refused access without credentials (HTTP 403 on pages and the bulk CSV, 401 on the API). A registered bot or user account would be required.

**Rubin-era labels.**
- Broker classifications are annotation. RTN-011 §5.3 describes brokers adding "preliminary classifications".
- TNS spectroscopic classifications count as measured only after checking that the reporter is not a bot.

**Labels also drift.**
- The file labels SN2018cne as SN Ia, while the SNIascore paper says BTS officially classified it SN Ic.
- Compared with archived captures, 5 labels differ from the 2024-12-08 capture and 4 from the 2025-08-10 capture.

## 2. D4 exposure key: DERIVED, with gaps
**When the data became public.**
- ZTF alerts have been public in real time since 2018-06-04.
- Rubin alerts have been world-public since 2026-02-24.
- The Rubin Prompt Products Database is expected in Sep–Oct 2026. No release announcement had appeared by 2026-09-15.

**When each label became public.** The date is bracketed:
- **Lower bound:** the TNS discovery date.
- **Upper bound:** the earliest Internet Archive capture of the BTS explorer that shows the same label. Captures exist for 2024-12-08, 2025-08-10 and 2026-07-25.
- **Exact date:** the TNS classification-report date, which could not be reached.

**Subject cutoffs, from vendor pages only.**

| Vendor | Model | Cutoff |
|---|---|---|
| Anthropic ("reliable knowledge cutoff") | Claude Fable 5.1 | Jun 2026 |
| Anthropic | Opus 5 | May 2026 |
| Anthropic | Sonnet 5 | Jan 2026 |
| Anthropic | Haiku 4.5 | Feb 2025 |
| OpenAI | GPT-6 Astra | 2026-04-30 |
| OpenAI | GPT-5.6 Sol, Terra, Luna | 2026-02-16 |
| Google | Gemini 3.8 Flash | March 2026 |
| Google | Gemini 3.1 Pro | UNDEMONSTRATED (none published) |

- **Cutoff window:** 2025-02-01 to 2026-06-30, or 2026-01-01 to 2026-06-30 without Haiku 4.5.
- **Knowledge cutoff is not training-data end.** These are knowledge cutoffs; no vendor page gave a training-data end date.
- **Web access is a separate issue.** A subject with web search can read TNS directly. That is an R4 grant question, not a cutoff question.

## 3. P3 contamination axis: FAIL (pre-clustering)

| Subject set | Label public before every cutoff | After every cutoff | Unresolved |
|---|---|---|---|
| All demonstrated subjects | **6,166** (78.6% of labeled) | **0** | 1,677 |
| Excluding Haiku 4.5 | **6,729** (85.8%) | **0** | 1,114 |

- **Unresolved objects.** Of the 1,677, 1,647 are absent from the archived page because it shows only objects passing the quality cut. None can fall after the cutoffs: every labeled object was discovered on or before 2026-06-30. Only 20 objects were discovered on or after 2026-07-01, and none of those is labeled yet.
- **All BTS units whose exposure can be determined predate all subjects.** This is the skill's typical failure, so contamination is disclosed, not solved.
- **Clustering is Agent 1's.** Thirteen IAU names are each shared by two ZTFIDs, so there are at most 11,204 distinct objects.

**What the Rubin post-2026-06-30 stream offers.**
- **Which objects qualify.** Only objects first detected on or after 2026-07-01 have both their light curve and their label after every demonstrated cutoff. Detections on the nights of 29 and 30 June fall inside Fable 5.1's June 2026 cutoff month.
- **How little supply there is.**
  - The survey ran from the night of 29 June until a summit evacuation for a record storm on 14–15 July.
  - As of 2026-09-11, Rubin was still off sky with no return date.
  - Planned maintenance downtime began 2026-09-14.
  - The count of post-cutoff Rubin objects is UNDEMONSTRATED and needs broker or database queries.
- **Being prospective does not remove every leak.**
  - Host-galaxy redshifts and photometry sit in pre-cutoff catalogs. In 2018, 44% of BTS SN Ia hosts had a catalogued redshift before discovery.
  - Archival photometry and past variability at a position can reveal AGN or CV nature.
  - The SN prefix is assigned on classification, and 6,994 of the 7,252 SN-prefixed names carry an SN or SLSN label.
  - Class rates and priors are published.
  - Labels may still be bot annotation.
  - A subject with web access can read the label once it is filed, so decisions must be sealed first.
  - One subject has no published cutoff.

## 4. D2 answer-in-own-source (refusal 14)
- **Refused:** items built from TNS classification reports, ATels or AstroNotes. The class is in the source text, and every BTS-era source predates every cutoff.
- **Refused, or re-identified with a neutral ID:** items that expose the IAU name.
- **Admissible with contamination disclosed:** BTS items built from light curves with the label withheld. This is not a refusal-14 case.
- **Admissible only when all of the following hold (UNDEMONSTRATED until then):** Rubin items that
  1. were first detected after 2026-06-30,
  2. come from a frozen subject set with a cutoff for every member,
  3. carry no report text or IAU name,
  4. have a label filed after the decision is sealed, by a non-bot reporter, and
  5. have a written exposure ruling.

## 5. Disagreements (listed, not reconciled)
1. **Object count:** 11,218 claimed vs 11,217 in the file.
2. **peakt offset:** the brief's offset vs JD−2458000.
3. **LSST start:** 2026-06-30 vs 2026-06-29.
4. **Fable cutoff:** Fable 5.1 at Jun 2026 on the models page vs Fable 5 at Jan 2026 in the Transparency Hub, which has no 5.1 entry.
5. **SN2018cne:** Ic in the SNIascore paper vs Ia in the file.
6. **Subtypes:** Perley+2020 App. E says subtypes are removed, but the file carries them (e.g. 151 SN Ia-91T).
7. **Perley+2020 Table 3:** 8 of its 21 ZTFIDs are missing from the file. SN2020eyj is missing too.
8. **savedate:** it stops at 2022-10-08, while 4,503 objects were discovered later.
9. **Typed events:** the BTS home page reports 11,580 typed events vs 7,843 labeled objects in the file.
10. **Name prefix vs label:** 254 SN-prefixed objects are unlabeled in BTS, and 92 AT-prefixed objects carry SN or SLSN labels.
11. **RTN-011:** it gives ComCam First Photon as 2024-10-24 in one place and 2025-10-24 in another.

## 6. Still UNDEMONSTRATED, and what each item blocks

| Item | Blocks |
|---|---|
| Per-object reporter, bot flag and report date | D5 label-source ratification, P6 label strata, A3 scoring as measured truth, exact P3 dates |
| Gemini 3.1 Pro cutoff; training-data end dates | subject-set slot |
| Clustered count | P3 (use Agent 1's cut) |
| Rubin post-cutoff counts | prospective supply for P3 and P5 |
| Rubin data policy RDO-013 (behind a login) | nothing; RTN-011 already states alerts are world-public |

## Validation
- `label_source_slot.json`, `exposure_key_slot.json` and `contamination_axis.json` pass the skill's provenance check.
- `provenance_records.json` passes `validate.py provenance`.
- A two-slot manifest stub fails `validate.py ledger`, as expected, because the other slots belong to other agents and to D5.

## Files
`label_source_slot.json`, `exposure_key_slot.json`, `contamination_axis.json`, `provenance_records.json`, `derived_counts.json`, `seed_ledger.json`, `replay_cases.csv` (3 must_fire, 1 must_not_fire), `replay_rulings.csv`, `scripts/`, `sources/` (SHA256SUMS).
