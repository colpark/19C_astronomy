# Wave 4 · Agent 2: calendar model for the price of truth, and WISeREP check plan (FROZEN before computing)

Frozen 2026-09-17, before any IRSA night count, monthly pricing or WISeREP content read. The sha256 is in `calendar_model_FROZEN.sha256`, and every script checks it.

**Governing documents:**
- `astronomy/wave4/PANEL_BRIEF_WAVE4.md`, sha256 8f101811…1b58, verified;
- wave-3 `census_protocol_FROZEN.md`, sha256 9fac8552…95fb;
- wave-3 `truth_cost_table.csv`, read only, not edited (rule E);
- wave-3 `supply_P_per_month.json`, read only.

**Banner.** BTS numbers are calibration only, contamination FAIL on BTS. This is planning pricing, not a P7 record.

## 0. Seen before freezing (disclosed)

- **Wave-3 outputs (mine):**
  - (b) lower bounds per month for Jan–Sep 2026: 17, 2, 19, 10, 84, 20, 3, 5, 1;
  - (a) spectroscopic lower bounds: 24, 2, 20, 13, 90, 22, 3, 5, 2;
  - cohort existence 13 (MODERATE); cohort measured non-bot STRONG 0;
  - f19 = 0.004, CP95 [0.0017, 0.0079]; A per night (10 nights) = 775, CP95 lower 335;
  - truth cost grid ranges.
- **Agent 1** `out/nights_observed.json`:
  - scheduler science nights 2026-06-29…07-13: 10 of 15 calendar nights;
  - Fink alert nights 2026-06-29…07-14: 11 of 16.
- **Sources read for this freeze:**
  - Cenko+2006 (astro-ph/0608323, read in full): qualitative only. "In the summer months, it is rare to lose an entire night due to weather", and the P60 was closed for 15 full nights in January 2005 (§4.2).
  - Bellm+2019 (1905.02209) and Blagorodnova+2018 (1710.02917): grepped for weather statistics only, none found. SEDM's "average rate of 10 spectra per night" was seen at line 1833. Neither is used as a decision input (not read in full).
- **IRSA TAP probe:** one count query, `ztf.ztf_current_meta_sci` for JD 2459000.5–2459001.5, returned 24,510 rows (HTTP 200, 61 s). No monthly count was made.
- **TNS_API_KEY:** ABSENT at 2026-09-17T13:15Z.

## 1. Targets N (per-object, unchanged by wave-4 rulings)

| δ | N | Status |
|---|---|---|
| 0.05 | 63, 1,666 | ratified |
| 0.018 | 485, 12,855 | prior |

**Labels needed.** N_need = N − L. L = 0, because cohort measured non-bot labels are STRONG 0 and the true count is UNDEMONSTRATED. A sensitivity row uses L = 13, the cohort existence count (MODERATE), and labels it as such.

## 2. Grids carried from wave 3 (seed locators in the wave-3 seed ledger)

- **Purity p** ∈ {0.81, 0.846, 0.92, 0.93, 0.956, 0.967}
- **Classification success s** ∈ {0.93, 1.0}
- **P60-class capacity c** per usable night ∈ {4.5, 8, 10}
- **PI cost of action:**
  - 0.5 h P60 time per spectrum;
  - 1 slot per wrong routine commitment;
  - ≥ 100 slots per missed rare event (asymmetric; miss rate M UNDEMONSTRATED; reported as an add-on).

## 3. P60-class usable nights per month, U(m)

**Source.** IRSA TAP `https://irsa.ipac.caltech.edu/TAP/sync`, table `ztf.ztf_current_meta_sci`. These are science exposures of ZTF P48 at Palomar: the same site as P60, a different telescope.
- Strength MODERATE: site weather and P48 downtime are measured; P60/SEDM-specific downtime is not.

**Query.** For each calendar month of the years 2021, 2022, 2023 and 2024 (48 queries):
`SELECT FLOOR(obsjd) AS jdn, COUNT(*) AS n FROM ztf.ztf_current_meta_sci WHERE obsjd >= <month start JD> AND obsjd < <next month start JD> GROUP BY FLOOR(obsjd)`

- FLOOR(JD) groups a Palomar night: JD turns over at 12:00 UTC, which is local noon.
- Retries: 3, each 60 s apart. Timeout 600 s.
- A failed month is UNDEMONSTRATED for that year and is never filled.

**Definitions:**
- **Usable night:** a jdn whose row count n ≥ 0.5 × the 90th-percentile nightly n within that year-month.
- **Fraction:** U_y(m) = usable nights / calendar days in month.
- **Primary:** U(m) = mean over the years with a complete month.
- **Also reported:** min and max over years; U_any(m), which counts nights with n ≥ 1.

**Capacity:** spectra per month S_m = c × U(m) × days(m).

## 4. Rubin on-sky nights per month, and months as a function of the return date

**On-sky fraction.**
- f_R = 10/15 = 0.667 (scheduler science nights 2026-06-29…07-13, agent 1). Alternate 11/16 = 0.6875 (Fink alert nights).
- MODERATE: 15 nights of early operations in austral winter.
- Rubin on-sky nights per month: N_R(m) = f_R × days(m).

**Reachable arrivals per month:** A_m = A_night × N_R(m), with A_night = 335 (the f19 CP95 lower bound, 10-night basis; wave-3 `reachability.json`).

**Effective spectra per month:** S_eff(m) = min(S_m, A_m).

**Sky overlap.** The Palomar (+33°) and Cerro Pachón (−30°) overlap fraction o is UNDEMONSTRATED. o = 1 is applied, so months are lower bounds on duration.

**Return date R (not guessed).**
- For each candidate return month R ∈ {2026-10, 2026-11, …, 2027-09}: months after R needed so that Σ S_eff(m) × p × s ≥ N_need, and the completion month.
- Seasonality enters only through U(m).
- If the month count exceeds 120, report ">120" and stop.

**Aggregate row.** A season-independent row uses the annual mean U: months = N_need / (p × s × c × Ū × 30.44), with nights = S / c.

## 5. Waiting on existing 2026 TNS throughput (upper bounds on waiting time)

**Rates:**

| Rate | Definition | Value | Strength |
|---|---|---|---|
| r_b | wave-3 (b) lower bounds, Jan–Aug total / 8 | (17+2+19+10+84+20+3+5)/8 = 20.0 /month | lower bound |
| r_a | (a) spectroscopic lower bounds, Jan–Aug total / 8 | 179/8 = 22.375 /month | lower bound |
| r_c,strong | cohort non-bot STRONG | 0 | waiting time unbounded (UNDEMONSTRATED) |
| r_c,exist | 13 cohort existence / 2.53 months (2026-07-01 to 2026-09-16) | 5.14 /month | MODERATE; classifier unknown; decays while Rubin is off sky |

September is excluded from r_b and r_a because it is partial.

**Waiting months.** Waiting months = N_need / (r × p), at each p in the grid.
- p enters as the share of reports that land on target-class objects. It is not measured for TNS reports; it is carried as a grid dimension for comparability with the dedicated program.
- The rates are lower-bound supply, so waiting months are upper bounds.
- r_a and r_b are all-sky, all-survey TNS rates, not Rubin cohort rates. That is disclosed; they bound waiting only if every report counted toward N.

## 6. Ruling-4 sensitivity (human-confirmed only vs including model-annotated)

- **Existing supply:** r_b (human only) vs r_a (including SNIascore-annotated). Cohort: STRONG split UNDEMONSTRATED.
- **Dedicated program:** the spectra count is identical either way. Human confirmation adds classifier effort, which is not priced (UNDEMONSTRATED). With "including model-annotated", an automated classifier's reports count, so no extra human hours are needed.
- **BTS calibration pool** (wave-3 track one): human-confirmed placed 1,074; including model-annotated placed 2,028; model-annotation bound [954, 2,057]. Calibration only.

## 7. WISeREP existence check (ruling 3, rule C)

**Seal before any WISeREP content read.** `sealed/wiserep_lookup_SEALED.json` and `sealed/wiserep_predictions_SEALED.json` are hashed first.

**Lookup list:**
- (i) the 13 typed cohort objects: 2026rwk, srp, stj, stu, tim, trp, tzm, uii, uvw, uwo, uxs, uyc, vpl;
- (ii) a declared sample of 20 untyped tier-A cohort-matched names from wave-3 `enumeration_E_SEALED.json`, chosen by numpy seed 20260918 permutation;
- (iii) 10 positive controls: tier-B typed 2026 objects, same seed. These are non-cohort; their only purpose is to test whether the check could return a positive at all ("would it fail if false").

**Probes** (no credentials, default UA, no bypass):
- `https://www.wiserep.org/`
- `https://www.wiserep.org/search`
- `https://www.wiserep.org/object/<name>`
- `https://www.wiserep.org/api/objects` (or as linked)
- Internet Archive `web/20260916id_/https://www.wiserep.org/`, and `/object/<name>` for the lookup list

Each request's status, server header and UTC time are recorded. Spacing ≥ 1.0 s.

**If reachable, record per object:** spectrum exists; spectrum uploader or group; whether the classification shown is mirrored from TNS or WISeREP's own; reported type.

**What the check can establish:**
- existence of a public spectrum;
- the uploading group, if shown.

**What it cannot establish:**
- classifier identity, or human vs bot, unless the page states the classifier;
- that the TNS label is correct;
- anything about objects without a page (absence ≠ no spectrum).

**If blocked:** record BLOCKED with the responses and name what stays UNDEMONSTRATED and which stage it blocks.

## 8. What may change after computing

- **May change:** transport retries, parser fixes. Each is recorded as an amendment.
- **May not change:** everything in sections 1–7.
