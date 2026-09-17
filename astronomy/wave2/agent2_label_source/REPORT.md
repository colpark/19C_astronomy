# Wave 2, Agent 2: label source

> Agent 2 returned this report as text because the harness blocks REPORT.md writes. The coordinator saved it without changing its substance. Everything here is **calibration only, contamination FAIL on this cohort** (addition B).

## Headline
- **SNIascore bound tightened.** The bound moves from **0–3,131** to **803–2,247** of the 7,843 BTS labels.
- **Per-object split only partly done.** 6,156 of 7,843 labels remain UNRESOLVED.
- **Public, credential-free evidence only.** The main source is Internet Archive captures of TNS object pages.

## Compliance
- **Brief hash:** verified (31a36617…f4eb).
- **Addition A:** `definitions_FROZEN.md` (4f89ff67…37cf) was hashed before any count.
- **Addition C:** `sealed_fileonly_placement.json` (76300235…c03eb0) was sealed before any per-object TNS page was read.
- **Scope:** no git was run, and nothing was written outside this directory.

## 1. Dispositions

| Criterion | Disposition |
|---|---|
| A: definitions before counting | **PASS** |
| C: seal before reading TNS pages | **PASS** |
| Tighten SNIascore bound | **PASS**: [803, 2,247] |
| Per-object split of all 7,843 | **UNDEMONSTRATED**: 1,687 placed, 6,156 unresolved |
| Photometric-only split | **UNDEMONSTRATED**: 0 placed; tier 3 (AGN/CV) was never reached |
| CCSNscore channel | **UNDEMONSTRATED**: bound 0–155, start date unknown |
| Refusal-14 rulings on the 98 | **PASS**: all 98 ruled |
| label_source slot | **UNDEMONSTRATED**, with its SNIascore bound DERIVED |
| Live TNS without credentials | **FAIL**: HTTP 403 (awselb) on every path, robots.txt included |
| `validate.py provenance provenance_records.json` | **PASS** |
| Slot provenance fields | **PASS** |
| One-slot manifest stub | FAIL, as expected: the other slots belong to other agents or to D5 |

## 2. Public evidence found
**The deciding field is Classifier/s, not the reporter or bot name.**
- Archived TNS pages show SNIascore reports as Sender `ZTF_Bot1` and Group `ZTF`.
- Classifier/s reads "SNIascore on behalf of the SEDM Team…" or, from about September 2022, "C. Fremling, D. Neill, Y. Sharma on behalf of the SEDM Team … **based on SNIascore**".
- `ZTF_Bot1` also sends human reports, so a bot group name is not usable evidence.

**What SNIascore can emit.** Source: arXiv:2104.12980, read in full.
- **Classes:** binary Ia vs not-Ia (§3, lines 413–415). It reports only "SN Ia", never subtypes; SEDM cannot separate Ia subtypes (fn 9).
- **Instrument:** P60/SEDM.
- **Thresholds:** 0.9 at launch, with >0.8 and σ<0.275 planned.
- **Start date:** 2021-04-15 (§7).
- **Confirmation:** TNS AstroNote 2021-122, read from a 2026-01-16 capture, confirms the date, the threshold and SN2021ijb as the first object.
- **Observed on parsed pages:** SNIascore never reported a non-Ia class and never reported before 2021-04-15.

**Other sources:**
- BTSbot (arXiv:2401.15167) names 14 objects that SNIascore classified.
- No paper gives per-period counts of automated reports.
- CCSNscore (arXiv:2412.08601v2) says real-time TNS reporting had not started as of March 2025 (lines 1089–1091).
- The BTS explorer has no reporter or classification-date field. A 2021-01-28 capture, taken before SNIascore started, exists but was archived truncated at 1 MiB; 2,691 rows were parsed.
- On the Wayback Machine, CDX returns 503 and the availability API returns 429. Only the `web/<ts>id_/` redirect route works.

## 3. New bounds and the rules behind them
**Lower bound: 803.**
- 799 STRONG: typed "SN Ia", and the latest matching archived TNS report has SNIascore in Classifier/s.
- 4 MODERATE: named in a paper but not fetched.
- The wave-1 lower bound was 0.

**Upper bound: 2,247.** This is min(3,131, the 5,067 plain "SN Ia" labels minus three exclusions):
- 884 whose archived report is a human classification (E1);
- 1,340 already typed SN Ia in the 2021-01-28 explorer capture (E4);
- 1,936 excluded by the wave-1 peak rule (E5, WEAK).

**What sits inside the upper bound:**
- 803 placed.
- 1,444 unresolved:
  - 1,198 never fetched;
  - 200 archived 403 or 404;
  - 22 failed after retries;
  - about 24 with no report in the capture, or a class mismatch.

**Sensitivity only:** without E5 the upper bound would be 2,844. The bound was not widened.

## 4. Category counts (`label_basis_per_object.csv`, 7,843 rows)

| Category | Strength | Objects |
|---|---|---|
| MEASURED | STRONG | 884 |
| MODEL_ANNOTATION (SNIascore) | STRONG | 799 |
| MODEL_ANNOTATION (SNIascore) | MODERATE | 4 |
| PHOTOMETRIC_ONLY | – | 0 |
| UNRESOLVED (UNDEMONSTRATED) | – | 6,156 |

**MEASURED by group:** ZTF 454, SCAT 135, ePESSTO+ 97, other 198.

**Fetch coverage.** The run stopped at the declared 5 h cap, having reached only tier 1 (plain SN Ia not excluded by E5).
- Attempted: 1,933 of 3,131.
- Fetched: 1,706 captures. 5 were double-gzipped and re-parsed under A1.
- Archived 403/404: 200.
- Failed: 22.
- Never attempted: 5,910.

**SNIascore share of placed plain SN Ia: 47.5%** (799 of 1,683). This is tier-1 descriptive only, not a bound.

| Year | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| SNIascore share | 0.49 | 0.67 | 0.50 | 0.35 | 0.33 |

## 5. Refusal-14 rulings (calibration use only, addition B)
**Agent 1's 98:**
- **92 REFUSE.** The class is stated in the seed text, and both seeds (2019-10, 2020-09) predate every cutoff.
- **6 NOT_FIRED_NAME_ONLY:** SN2018cod, SN2018jef, SN2019sxd, SN2020ut, SN2019ape, SN2020oce. The name appears but no class is stated. They are admissible for calibration under ER-W2-A2-01: neutral ID, and no seed text shown to any arm.
- **3 unlabelled in BTS, still refused.** The seed text gives candidate classes (AGN, TDE, CV).

**17 more from this agent's own seeds:**
- **12 REFUSE:** SN2021ijb, SN2018cne, SN2023rky, and 9 SNIascore-named 2023 SNe.
- **5 NOT_FIRED.**

## 6. Disagreements (listed, not reconciled)
1. **The WEAK E5 rule is breached.** 2 of 799 SNIascore reports came more than 30 d after peak: SN2023gbn at +553.7 d and SN2025fca at +42.5 d. Both wave 1's 3,131 and this 2,247 lean on E5.
2. **The brief's "reporter or bot group" vs the pages.** The automation marker appears only in Classifier/s, and `ZTF_Bot1` also sends human reports.
3. **Human names in SNIascore classifier strings.** From about September 2022 the strings carry human names plus "based on SNIascore", so reading names alone would count these reports as measured.
4. **"Atlas Syncatto (SCAT)" may be an automated pipeline.** It classified 11 labels counted MEASURED under the frozen markers. Unresolved.
5. **Stale captures.** 31 objects had an earlier SNIascore report that a later report superseded. The median report-to-capture gap is 568 d, so a later human re-report cannot be ruled out for the 799.
6. **SN2021sic:** Ia in BTS, SN II on TNS (two SNe in one host).
7. **TNS discovery date is not a safe proxy.** SN2017bde was discovered in 2017 but classified by SNIascore in 2023; AT2019czs likewise.
8. **Paper-named objects vs the BTS file.**
   - SN2023vtp is typed Ia-91T in BTS, but BTSbot says SNIascore classified it, and SNIascore emits only "SN Ia".
   - SN2023tyk, uty, vip, xms and xkq are absent from the file.
9. **Agent 1's flag script matches names, not classes.** 6 of its 98 state no class.
10. **Seed-text class vs BTS type.**
    - 2018ghd: II vs Ib.
    - 2019odp: Ic-BL vs Ib.
    - 2020ntt: IIn vs II.
    - 2018cne: Ic vs Ia.
    - 2023rky: IIL vs II.
    - SN2019ape and SN2020oce say "CC SN", which is not in the frozen class tokens, so they are NOT_FIRED and flagged.
11. **Locator numbering.** The sealed E2 evidence uses non-empty-line numbering (BTSbot 1318–1329); the raw-line equivalent is 1583–1591.

## 7. Amendments after freeze (parser and transport only; no rule changed)
- **A1:** double-gzipped captures are decompressed until plain.
- **A2:** the parser handles both TNS layouts (fieldset and details). The fix was found on a 3-object test; that log was deleted and those objects were refetched.
- **A3:** transport settings changed:
  - request spacing 1.5 s → 1.0 s, the declared minimum;
  - timeout 120 s → 30 s;
  - a 10 s pause after connection errors;
  - restarted and resumed from the log, with the 5 h cap anchored to the first logged fetch at 19:01:51Z.
- **A4:** refusal-14 line numbering now splits on newline only, and the figure-grid class parser takes the correct entry when two objects share a line.

## 8. Still UNDEMONSTRATED

| Item | Blocks |
|---|---|
| Basis of 6,156 labels (every non-SN Ia and every E5-excluded label) | D5 label_source ratification, P6 label strata, A3 as measured truth |
| AGN/CV: photometric-only or spectroscopic | D5 label_source |
| CCSNscore start date (GitHub page unread) | label_source for CC classes from 2025 |
| Later re-reports superseding captures; Syncatto automation | exact measured and annotation counts |
| Per-object reports without credentials | exact split (TNS credentials BLOCKED, wave-3 ruling 5) |

`scripts/fetch_tns_captures.py` can resume the fetch and narrow the bounds further.

## Files
- `definitions_FROZEN.md`, `definitions_FROZEN.sha256`
- `sealed_fileonly_placement.json`, `sealed_fileonly_placement.sha256`
- `label_basis_per_object.csv`, `label_basis_per_object_detail.csv`, `split_summary.json`
- `label_source_slot.json`, `refusal14_rulings.json`, `provenance_records.json`
- `replay_cases.csv` (AST2W2-01..04: two must_fire, two must_not_fire), `replay_rulings.csv`
- `scripts/`
- `sources/`: `seed_ledger.json`, `SHA256SUMS`, `tns_captures/`, `http/probe_log.txt`
