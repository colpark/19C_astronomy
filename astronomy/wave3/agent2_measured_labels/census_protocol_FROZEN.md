# Wave 3 · Agent 2: measured-label census and truth-cost protocol (FROZEN before any count)

Frozen 2026-09-17, before any census, cohort-match, reachability or pricing count. The sha256 is in `census_protocol_FROZEN.sha256`, and every script checks it.

**Governing documents:**
- `astronomy/wave3/PANEL_BRIEF_WAVE3.md`, sha256 a618d911…c4b6, verified;
- `astronomy/wave2/agent2_label_source/definitions_FROZEN.md`, sha256 4f89ff67…37cf. Its automation markers and Sender-is-not-evidence rule carry over.

**Scope banner.** BTS items are **calibration only, contamination FAIL on this cohort** (rule B). The Rubin cohort is the prospective supply.

## 0. Seen before freezing (disclosed)

- **Wave 2.** My own results: the 803..2,247 SNIascore bound, and the 0.475 SNIascore share of STRONG-placed plain SN Ia in BTS for 2021–2025.
  - Within ZTF, some reports carry human names plus "based on SNIascore".
  - "Atlas Syncatto (SCAT)" is unresolved.
- **Agent 1, wave 3 REPORT only:**
  - O = 1,937,669 merged cohort objects, first detection ≥ T0 = 2026-07-01;
  - 9 alert dates (the brief says 10 nights); off sky since 2026-07-14;
  - one-detection share 0.8082;
  - planning N_min: 485–12,855 at δ = 0.018 and 63–1,666 at δ = 0.05.
- **Status-only probes** (`sources/http/probe_log.txt`, prefix PRE-FREEZE-STATUS-ONLY). No body content was read.

  | Target | Response |
  |---|---|
  | wis-tns.org stats-maps | 403 |
  | Wayback redirects for TNS stats-maps, search, astronotes | 302 to captures of 2026-09-04 |
  | Wayback CDX | 503 |
  | rochesterastronomy.org/supernova.html | 200 |
  | astronomerstelegram.org | 200 |
  | wiserep.org | 403 |
  | Fink LSST statistics | 200 |
  | ALeRCE LSST list_objects | timeout, no response |
  | ANTARES loci | 200 |
  | lasair.lsst.ac.uk/api/ | 404 |

- **No TNS_API_KEY.** Presence test ABSENT at 2026-09-17T00:06Z. Track one is BLOCKED, request date 2026-09-16.

## 1. Unit and de-duplication

- **Unit.** One spectroscopic classification report per (object, program).
  - **Re-reports.** Further reports on the same object by the same program are not counted again, whether they change the class or not. The earliest report's Time received sets its month.
  - **Another program's report** on the same object counts once for that program.
- **Supply unit P.** Distinct objects that gain their first classification report in a month, counted overall and per split.
- **Spectroscopic.** The report lists ≥ 1 spectrum. That means the new layout's `cell-spectra` count > 0, or a spectrum in the object's Spectra table from the same Group with obs-date ≤ report time.
  - Reports with no spectrum are counted separately as `non_spectroscopic_or_unknown`. They are never in (b).
- **Month** = UTC month of the report's Time received, January through September 2026. September is partial, up to the fetch time.

## 2. Program

1. **Program** = the classification report's Group field (`cell-source_group_name`).
2. If Group is empty: the text after "on behalf of" in Classifier/s, up to "(" or "," or the end.
3. Otherwise: `UNATTRIBUTED`.

The Sender field is never evidence of program or automation (wave-2 finding: ZTF_Bot1 carries both human and SNIascore reports).

## 3. Automation markers (Classifier/s only)

| Marker | Model |
|---|---|
| `SNIascore`, including "based on SNIascore" | SNIascore |
| `CCSNscore` | CCSNscore |
| whole words bot, robot, automatic, automated, auto | other-automated |
| `Syncatto` | SUSPECT-AUTOMATED (SCAT) |

- **(b) non-bot measured** = spectroscopic AND no marker.
- **SUSPECT-AUTOMATED.** Reported twice: `b_incl` counts it as human, `b_excl` counts it as automated. The difference is disclosed as UNDEMONSTRATED.

## 4. Splits of P per month

- **(a)** all classification reports, deduplicated per §1: spectroscopic plus non_spectroscopic_or_unknown, each shown.
- **(b)** non-bot measured spectroscopic.
- **(c)** reports on Rubin cohort objects. The object must match a cohort object by either:
  - (i) a diaObjectId given in the TNS page's internal names or AT reports, or in a broker TNS-crossmatch record; or
  - (ii) a position within 1.0″ of a cohort oid from agent 1's slices (`astronomy/wave3/agent1_cohort_finish/out/w3_c3_slices/`, integrity from `out/SLICES_SHA256SUMS`, sha256 of that file recorded at seal), where the TNS discovery date is ≥ 2026-07-01 minus 1 d.
  - (c) is reported with (b)-type sub-counts where the report's classifier is known.

## 5. Sources and evidence strength (public, credential-free only)

| Code | Source | Gives | Strength |
|---|---|---|---|
| T1 | Internet Archive captures of `www.wis-tns.org/object/<name>` (`web/20260916id_/`), wave-2 parser with amendment A1 | per report: Group, Classifier/s, Classification, Time received, spectra | STRONG per report. Coverage is a lower bound: reports after the capture are unseen |
| T2 | Internet Archive captures of TNS `stats-maps` | aggregate classification counts | STRONG if broken down by month and group; MODERATE if annual only; used as an adjudicator of T1 completeness |
| T3 | Internet Archive captures of TNS `search` pages, and any archived search URL whose result rows are classified 2026 objects | object enumeration and row classification | STRONG per row; partial coverage |
| T4 | TNS AstroNotes via Internet Archive (listing page and notes) | program throughput statements and automation announcements | MODERATE |
| T5 | ATel (astronomerstelegram.org), 2026 classification telegrams | per-program classifications, with spectra stated | MODERATE per telegram; coverage partial |
| T6 | Program papers read in full (seeds) | historical throughput and purity | WEAK for 2026 months; used only for the pricing grid |
| T7 | Fink LSST: TNS crossmatch fields (`in_tns` or a `xm_tns` family, as served), for cohort objects | whether a cohort object has a TNS entry or type | MODERATE for (c) existence; reporter unknown unless T1 |
| T8 | ANTARES: loci whose catalogs include a TNS catalog, restricted to cohort times; ALeRCE crossmatch endpoints | the same | MODERATE for (c) existence |
| T9 | rochesterastronomy.org Latest Supernovae page (third-party aggregation) | object enumeration: 2026 SNe with type, date, position | MODERATE for enumeration only; never program or automation |
| T10 | BTS explorer (live CSV) | 2026 BTS objects and types | MODERATE for enumeration |

- **Access limits.** No credentials are used, no accounts are created, and no user agent is spoofed (default curl/python UA). A 403, 429, 5xx or timeout is recorded with status, server header and UTC time. It is never interpolated.
- **Month status.**
  - A month with no T1/T2/T3 evidence is **UNDEMONSTRATED** for that split, with the exact responses cited.
  - A month with T1/T3 evidence is a **lower bound**.
  - It becomes **exact** only if T2 gives the same month's total and T1+T3 reach it.

## 6. Enumeration and fetch order (declared)

1. Parse T9 and T10 for objects whose discovery date or classification date falls in 2026; collect T3 rows; collect T7/T8 cohort TNS matches after the rule C seal (§8). The union is the enumeration list E, written with its hash to `sealed/` before any T1 fetch.
2. **T1 fetch order:**
   - **tier A:** cohort-matched objects (§4c);
   - **tier B:** all other E objects, in a random permutation (numpy seed 20260917).
3. **Politeness.** ≥ 1.0 s between requests; on 429/503 wait 60 s, retrying 3 times; timeout 30 s.
4. **Time cap:** 4 h of wall clock from the first T1 request. Objects not reached are `not_attempted`: UNDEMONSTRATED, never zero.

## 7. Reachability of cohort objects (declared sample, no labels)

- **Sample R.** The 2,000 cohort oids with the smallest sha1(oid) hex, over all 450 slices. Only rows with firstmjd ≥ T0 = 61222.000428 are eligible.
- **Photometry.** Fink LSST `POST /api/v1/objects` (or the served equivalent), through `scripts/safe_fetch.py`, which strips label keys. Columns: `r:diaObjectId, r:psfFlux, r:psfFluxErr, r:band, r:midpointMjdTai`, in batches of 100.
  - Fallback if Fink does not serve these: ANTARES locus properties (brightest magnitude fields), same sample.
  - If both fail: UNDEMONSTRATED, with the responses.
- **Peak AB magnitude** = 31.4 − 2.5·log10(max psfFlux in nJy) over rows with psfFlux > 0 and psfFlux/psfFluxErr ≥ 5. psfFlux is a difference-image flux, so this is the transient's brightness above the template.
- **Reachable fractions**, reported with Clopper-Pearson 95% intervals:
  - `f19` = share with peak ≤ 19.0, the SEDM depth ("maximum depth attainable by SEDM", arXiv:2412.08601 line 265);
  - `f185` = share with peak ≤ 18.5, the BTS goal.
- **Arrival rate of reachable objects per on-sky night:** A = f19 × O / n_nights, where O = 1,937,669.
  - n_nights = 10 per the brief; 9 alert dates per agent 1. Both are reported, and the disagreement is listed.
- **Off-sky constraint.** Rubin has been off sky since 2026-07-14. The existing cohort's last detections are all on or before that date, and its reachable objects have since aged by ≥ 60 d. Spectroscopic reachability *today* for existing cohort objects is therefore not credited: a spectrum ≥ 60 d after the last detection is outside the phase ranges in the seeds (SNIascore −20..+30 d). Supply resumes only when Rubin returns, and the calendar date is UNDEMONSTRATED.

## 8. Rule C: order of operations

1. Freeze this protocol and hash it.
2. Write `sealed/predictions_SEALED.json` (§9) and `sealed/lookup_list_SEALED.json`, and hash both. The lookup list contains:
   - the cohort definition (slice hash file and T0);
   - the exact T7/T8 queries to be run;
   - the rule that any E object matched to the cohort is looked up;
   - sample R's oid list.
3. Only then read any classification (T1–T5, T7–T10 content) for any object first detected after 2025-02-01, the earliest demonstrated cutoff.
4. Every step is appended to `order_of_operations.log` with UTC time and file hashes.

## 9. Predictions to seal (written before reading)

Point value plus range for each:
- (a) all TNS classification reports per month in 2026;
- (b) the non-bot measured share;
- (c) cohort objects with any TNS classification, total for Jul–Sep 2026;
- f19 and f185;
- A (reachable arrivals per night).

## 10. Pricing formula (declared)

**Inputs:**
- **N** ∈ {485, 12,855} at δ = 0.018, the frozen bands; {63, 1,666} at δ = 0.05, the PI override. N counts correctly labelled positive cohort objects (genuine extragalactic transients with a measured spectroscopic class).
- **Purity grid p.** The fraction of triggered targets that are genuine extragalactic transients, from seeds:

  | p | Meaning | Locator |
  |---|---|---|
  | 0.81 | BTSbot bts_p1, present-day | 2401.15167 raw line ~1210 |
  | 0.846 | BTSbot bts_p1, test | ~985 |
  | 0.92 | BTSbot bts_p2, present-day | ~1211 |
  | 0.93 | BTSbot bts_p2, test | ~985 |
  | 0.956 | scanner triggering purity as restated in 2401.15167 | ~1033 |
  | 0.967 | scanner triggering purity | ~965 |

  The 0.956 vs 0.967 disagreement is listed and not reconciled. Exact line locators are written into the seed ledger.
- **Classification success s** ∈ {0.93, 1.0}. 0.93 = share of events at m < 18.5 with successful public classifications (Perley+2020, 2009.01242 line 854-855); 1.0 is the optimistic bound.
- **Spectra-per-night capacity c:**

  | c | Meaning | Locator |
  |---|---|---|
  | 4.5 | BTSbot median saves+triggers per night | 2401.15167 ~1238 |
  | 8 | frozen k per night | wave-1 slot k from arXiv:2401.15167 |
  | 10 | "SEDM can classify >10 SNe … every night" | 1910.12973 sec 1 |

- **Existing supply offset L.** Measured (b) cohort labels counted in §4(c); UNDEMONSTRATED counts are used as 0 for the *upper* cost and reported as such.
- **PI cost of action:** 0.5 h P60-class time per spectrum; 1 slot per wrong routine commitment; ≥ 100 slots per missed rare event (asymmetric).

**Formulas:**
- N_need = max(0, N − L)
- Spectra S = ceil(N_need / (p · s))
- Hours H = 0.5 · S
- Wrong routine commitments W = S − ceil(N_need / s), i.e. slots spent on non-targets. Cost in slots = S, of which W are wasted.
- Missed-rare-event penalty = 100 · M slots. M is UNDEMONSTRATED (no seed gives the rare-event miss rate of a dedicated program) and is reported as a per-event add-on, never as 0.
- Nights on sky = ceil(S / min(c, p_avail)), where p_avail = A × (p-independent) is the reachable arrivals per on-sky night. If A < c, arrivals bind and nights = ceil(S / A).
- Calendar time is UNDEMONSTRATED while Rubin is off sky.
- **Output.** Every combination of N (both δ), p, s, c goes to `truth_cost_table.csv`. The summary with provenance goes to `truth_cost.json`.

## 11. Track one (credentials)

- **Status: BLOCKED** (no TNS_API_KEY; request date 2026-09-16).
- If time remains after track two, resume `astronomy/wave2/agent2_label_source/scripts/fetch_tns_captures.py` logic from a copy under this directory. It writes only here, reads the wave-2 log read-only for already-attempted objects, and applies the wave-2 frozen definitions unchanged.
- Any new bound is `[max(803, L'), min(2247, U')]`. A bound is **never widened**.

## 12. What may change after counting

- **May change:** parser bug fixes and transport retries. Each is recorded as an amendment with before/after counts.
- **May not change:** unit, de-duplication, program, markers, splits, sources and strengths, sample R, thresholds, the purity/s/c grids, formulas, time caps.
