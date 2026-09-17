# Wave 3, Agent 2: measured labels (the binding axis)

> Agent 2 returned this report as text, because the harness blocks REPORT.md writes. The coordinator saved it here without changing its substance.

## Headline
- **Measured label supply on the Rubin cohort: UNDEMONSTRATED.** Zero archived non-bot classification reports were found on cohort objects.
- **2026 classification throughput has only a lower bound.** No month is exact.
- **Cost of truth can be computed.** 485 labels take ~500–650 spectra and 51–144 Rubin on-sky nights.
- **Track one (credentials) is BLOCKED.** The public archive route still tightened the BTS SNIascore bound to [954, 2,057].

## Setup
- Brief hash verified (a618d911…c4b6).
- `census_protocol_FROZEN.md` (9fac8552…95fb) was hashed before any count.
- No git was used, no accounts were created, no user-agent was spoofed and no captcha was bypassed.
- BTS material is **calibration only; contamination FAIL on this cohort**.

## Order of operations (rule C)
Full log in `order_of_operations.log`.

| UTC (09-17) | Step | Hash |
|---|---|---|
| 00:06 | brief verified; TNS_API_KEY presence test ABSENT; status-only probes | |
| 00:10 | protocol frozen | 9fac8552 |
| 00:11 | predictions and lookup list sealed, incl. sample R (2,000 cohort ids, positions only) | 19a66ea1, 5c4de9b7 |
| 00:12–00:17 | first classification content read (census pages, ANTARES) | |
| 00:27 | enumeration list E sealed, before any archived object-page fetch | 6575c3dd |

## Track one: BLOCKED
TNS_API_KEY is absent (request date 2026-09-16). The public-archive fetch was resumed under a 1 h cap (AMW3-2).
- **Fetch yield:** 390 objects attempted, 345 captures readable.
- **New placements:** 151 SNIascore and 190 human (MEASURED), with 0 class mismatches.
- **New BTS bound [954, 2,057]** (was [803, 2,247]).
  - L′ = 803 plus new SNIascore placements.
  - U′ = 2,247 minus new non-SNIascore placements.
  - The wave-2 frozen rules are unchanged, and the bound was never widened.
- **Categories:** MEASURED 1,074; MODEL_ANNOTATION 954; PHOTOMETRIC_ONLY 0; UNRESOLVED 5,815.
- **`label_source_slot.json`:** updated. Status stays UNDEMONSTRATED; provenance validates.

## Track two: 2026 classification census

### Fetchability
| Source | Result |
|---|---|
| Live TNS | 403 |
| WISeREP | 403 |
| Wayback CDX | 503 |
| TNS stats captures 2026-05-01, 05-17, 08-03, 09-04 and 2025-12-24 | archived 403 pages (118 bytes) |
| Search captures 09-04, 05-01, 01-04 | archived 403 pages |
| TNS stats capture 2026-01-07 | readable, per-year aggregates only |
| rochesterastronomy.org | 19,170 entries including LSST diaObjectId aliases; used for enumeration and the aggregate "1,587 confirmed SNe discovered in 2026" |
| ATel | index readable; telegrams behind reCAPTCHA (not used) |
| Fink TNS resolver | [] |

### Archived object pages
- 2,244 objects attempted within the 4 h cap.
- 214 captures readable; 1,981 returned 404.
- The readable pages give 182 classification units (object × program).
- **Every monthly figure is a lower bound.** Exact counts are UNDEMONSTRATED for all months.

| 2026 | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep |
|---|---|---|---|---|---|---|---|---|---|
| (a) spectroscopic units | 24 | 2 | 20 | 13 | 90 | 22 | 3 | 5 | 2 |
| (a) non-spectroscopic | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| (b) non-bot measured | 17 | 2 | 19 | 10 | 84 | 20 | 3 | 5 | 1 |
| (c) Rubin cohort, archived reports | – | – | – | – | – | – | 0 | 0 | 0 |

- **Row (b)** is identical with or without Syncatto; no Syncatto classifier appeared.
- **Row (c)** is UNDEMONSTRATED, not zero.

### Programs (lower-bound totals)
- ZTF 63 (20 of them SNIascore)
- ePESSTO+ 55 (49 in May)
- GeminiClass 9
- SCAT 8
- UCSC 6
- BlackGEM 5
- 16 further programs with 1–4 each (`supply_P_per_month.json`)

Automation in 2026: 20 of 181 units, all SNIascore. No CCSNscore reports appeared.

### Rubin cohort existence evidence (MODERATE)
- 13 cohort objects first detected on or after 2026-07-01 have a typed TNS entry (position or diaObjectId match): 12 transients and 1 CV.
- Their classifier is UNDEMONSTRATED: 12 archived pages returned 404 and 1 returned 403.
- ANTARES matches 319 cohort loci to its TNS copy.

## Reachability (sample R, labels stripped)
- **f19 = 0.004:** 8 of 2,000 are brighter than mag 19 (95% CI 0.0017–0.0079). f18.5 = 0.0035.
- **~775 reachable arrivals per on-sky night** (lower CI 335), using 10 nights. With the 9 alert dates it is 861.
- **Off sky since 07-14.** The existing cohort is at least 60 days past its last detection and gets no credit. Calendar time is UNDEMONSTRATED.

## Price of the gap (`truth_cost.json`, `truth_cost_table.csv`)
- **Formulas:**
  - spectra S = ⌈N / (p·s)⌉
  - hours = 0.5·S
  - nights = ⌈S / min(c, A)⌉
  - L = 0: no existing cohort labels are subtracted.
- **Grid:**
  - purity p ∈ {0.81, 0.846, 0.92, 0.93, 0.956, 0.967}
  - success s ∈ {0.93, 1.0}
  - capacity c ∈ {4.5, 8, 10}
- **Telescope capacity binds, not arrivals.**

| δ | N | Spectra | P60 h | Rubin on-sky nights | Wrong commitments |
|---|---|---|---|---|---|
| 0.05 | 63 | 66–84 | 33–42 | 7–19 | 3–16 |
| 0.018 | 485 | 502–644 | 251–322 | 51–144 | 17–122 |
| 0.05 | 1,666 | 1,723–2,212 | 862–1,106 | 173–492 | 57–420 |
| 0.018 | 12,855 | 13,294–17,065 | 6,647–8,533 | 1,330–3,793 | 439–3,242 |

- Add 100 slots per missed rare event to every row. The miss rate is UNDEMONSTRATED.
- **Worked example:** N = 485, p = 0.93, s = 0.93, c = 8 gives 561 spectra, 280.5 h, 71 nights and 39 wrong commitments.

## Sealed predictions vs outcomes
| Prediction | Sealed | Outcome |
|---|---|---|
| all classifications per month | 250 [150, 450] | not adjudicable: only lower bounds exist. Rochester's per-year total implies ~187/month by discovery |
| non-bot share | 0.7 [0.5, 0.85] | **0.89, outside the sealed range** |
| cohort classified | 60 [0, 400] | 13 (existence only) |
| f19 | 0.005 [0.0005, 0.03] | 0.004, in range |
| reachable per night | 970 [100, 6,000] | 775, in range |

## Amendments
- **AMW3-1**, declared before any object-page fetch: E for tier B is limited to typed entries.
- **AMW3-2:** 1 h cap on the track-one resume.
- **Transport fixes only:** 30 s timeout, 10 s back-off, double-gzip handling.

## Disagreements (listed, not reconciled)
1. **Trigger purity:** 0.967 (316/327, 2401.15167 lines 1148–1149) vs 0.956 restated at line 1243.
2. **Night count:** the brief's 10 nights vs agent 1's 9 alert dates.
3. **Position leak:** ANTARES matches 7 supernovae discovered between 2025-02 and 2026-04 at cohort positions.
4. **Rochester vs ANTARES on cohort classifications:** 2026srp, tim, uii and uxs appear only in Rochester; 2026uyc appears only in ANTARES.
5. **Rochester's own 2026 totals:** 17,562 objects in its CSV vs 19,448 on its page.
6. **BTS explorer vs TNS:** the explorer labels 2 of its 333 objects discovered in 2026, while archived TNS pages show 63 ZTF classification units in 2026.
7. **Group "None":** 5 units carry the literal Group "None" and were not mapped to UNATTRIBUTED.

## Still UNDEMONSTRATED
| Item | Blocks |
|---|---|
| measured non-bot labels on Rubin cohort objects; classifier of the 13 | P3 positive supply, P4, PI re-ratification |
| exact 2026 monthly totals (credentials BLOCKED; archive copies are 403 pages) | P5 queue re-derivation |
| CCSNscore start date; whether Syncatto is automated | the (b) split |
| P60 and Rubin sky overlap; rare-event miss rate; Rubin return date | calendar pricing |
| BTS basis for 5,815 labels | D5 label-source ratification |

## Deliverables
- **Protocol and sealed files:** `census_protocol_FROZEN.md` (+ .sha256); `sealed/` (3 files, hashed).
- **Census:** `tns_census_2026.json`; `supply_P_per_month.json`.
- **Truth cost:** `truth_cost.json`; `truth_cost_table.csv` (288 rows, both deltas).
- **Label source:** `label_source_slot.json`.
- **Logs:** `order_of_operations.log`; `seed_ledger.json`.
- **Replay:** `replay_cases.csv` (AST2W3-01 and 02 must_fire, 03 and 04 must_not_fire); `replay_rulings.csv`.
- **Working files:** `scripts/`, `out/`, `sources/`.
- **Validation:** `validate.py provenance` PASS on the census, the truth-cost records and the slot.
