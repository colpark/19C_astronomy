# Wave 4 · Agent 2: price of truth

> Agent 2 returned this report as text, because the harness blocks REPORT.md writes. The coordinator saved it here without changing its substance.
>
> Everything below is **planning only, not a P7 record**. BTS inputs are **calibration only (contamination FAIL on BTS)**. Under rule E, these numbers reach kill-band pricing only through module V records.

## Headline
- **Months to target.** A dedicated P60-class program needs **2–9 months after Rubin returns** to reach N = 485, and **8–28 months** for N = 1,666.
- **Calendar dates: UNDEMONSTRATED.** Rubin has no return date.
- **Measured labels: nothing public can confirm one on any cohort object.** TNS is BLOCKED (second record) and WISeREP is BLOCKED.

## Checks and scope
- **Brief hash:** verified (8f101811…1b58).
- **Census:** not repeated.
- **Wave-3 files:** none edited. `truth_cost_table.csv` was read only.
- **Git and access control:** no git run; no access controls bypassed.

## Order of operations
Hashes are in `order_of_operations.log`.

| UTC | Step | Hash |
|---|---|---|
| 13:15 | brief verified; TNS_API_KEY presence ABSENT | |
| 13:22:03 | `calendar_model_FROZEN.md` hashed, before any month count, pricing or WISeREP read | a681d81a |
| 13:22:18 | WISeREP lookup list and predictions sealed (rule C) | ea8fffef, 1442bcdb |
| 13:22–13:58 | WISeREP probes; IRSA month queries (48 of 48 returned HTTP 200); pricing | |

## 1. Monthly pricing (`truth_cost_monthly.json` / `.csv`)

### Calendar model (frozen before computing)
- **P60-class usable nights.** Source: the ZTF P48 science-exposure archive at Palomar (IRSA TAP, 2021–2024, 48 month queries). A night counts as usable if its exposures reach at least half of that month's 90th-percentile night. Evidence strength is MODERATE: same site, different telescope.

  | Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Annual mean |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | Usable fraction | 0.34 | 0.47 | 0.30 | 0.70 | 0.74 | 0.84 | 0.83 | 0.75 | 0.75 | 0.67 | 0.62 | 0.40 | 0.617 |

  Cenko+2006, read in full, supports the seasonality only qualitatively: "rare to lose an entire night" in summer, and 15 nights closed in January 2005.
- **Program parameters.** Capacity of 4.5, 8 or 10 spectra per usable night. Purity p from 0.81 to 0.967. Classification success s of 0.93 or 1.0.
- **Rubin on-sky fraction.** 10 of 15 nights, from agent 1's scheduler record. The alternate is 11 of 16, from Fink alert nights.
- **Reachable arrivals.** At least 335 per night, so P60 capacity is the binding limit in every month.
- **Return date.** Months are reported for every candidate return month from 2026-10 to 2027-09. No date is guessed.
- **Sky overlap.** Palomar and Rubin overlap is UNDEMONSTRATED and set to 1, so all months are lower bounds.
- **Consistency check.** With zero existing labels, the spectra counts equal the wave-3 table on every row.

### Price across the full grid (no existing cohort labels)

| δ (status) | N | Spectra | P60 h | Usable P60 nights | Wrong commitments | Months after return |
|---|---|---|---|---|---|---|
| 0.05 (ratified) | 63 | 66–84 | 33–42 | 7–19 | 3–16 | 1–2 |
| 0.05 (ratified) | 1,666 | 1,723–2,212 | 862–1,106 | 173–492 | 57–420 | 8–28 |
| 0.018 (prior) | 485 | 502–644 | 251–322 | 51–144 | 17–122 | 2–9 |
| 0.018 (prior) | 12,855 | 13,294–17,065 | 6,647–8,533 | 1,330–3,793 | 439–3,242 | 70–115; >120 at 144 of 864 grid points |

- **Cost of action.** 0.5 h of P60 per spectrum; one slot per wrong commitment; at least 100 slots per missed rare event. The miss rate is UNDEMONSTRATED.
- **Seasonality.** Moving the return month changes the span only modestly. For N = 485 it ranges from 2–7 months (return 2027-06) to 5–9 months (return 2026-12).

### Reference point (p 0.93, s 0.93, 8 spectra per night, return 2027-01)

| N | Spectra | Months | Complete |
|---|---|---|---|
| 63 | 73 | 1 | 2027-01 |
| 485 | 561 | 5 | 2027-05 |
| 1,666 | 1,927 | 14 | 2028-02 |
| 12,855 | 14,863 | 101 | 2035-05 |

### Waiting on existing 2026 TNS throughput instead
These rates are all-sky lower bounds, not cohort rates, so the months are upper bounds on waiting.

| N | Human-confirmed only (≥20/mo) | Including model-annotated (≥22.4/mo) | Cohort existence rate (5.14/mo, MODERATE) |
|---|---|---|---|
| 63 | 3.3–3.9 months | 2.9–3.5 | 12.7–15.1 |
| 485 | 25.1–29.9 | 22.4–26.8 | 97.6–116.5 |
| 1,666 | 86.1–102.8 | 77.0–91.9 | 335–400 |
| 12,855 | 665–794 | 594–709 | 2,587–3,089 |

Ranges span the purity grid. At the measured cohort rate of 0, the wait is unbounded (UNDEMONSTRATED).

### Ruling-4 sensitivity: human-confirmed only vs including model-annotated
- **Existing supply rate:** 20.0 vs 22.4 per month.
- **Dedicated program:** spectra, hours and nights are the same either way. Human-only adds classifier effort, which is not priced.
- **Existence-only cohort labels:** a sensitivity row counts the 13, which brings N = 63 down to 52–67 spectra.
- **BTS calibration pool:** 1,074 human-confirmed vs 2,028 including model-annotated. The model bound is [954, 2,057], inside ruling 4's [803, 2,247].

## 2. TNS track one: BLOCKED (second record)
- TNS_API_KEY was absent at 13:13:17Z (coordinator check) and at 13:15Z (agent check).
- Request dates: 2026-09-16 and 2026-09-17.

## 3. WISeREP existence check (`wiserep_check.json`): BLOCKED
- **Live site.**
  - www.wiserep.org returns HTTP 403 (awselb/2.0) on `/`, `/search`, `/object/2026uxs`, `/robots.txt` and `/api/objects`.
  - wiserep.org without www does not respond.
- **Archive route.**
  - The sealed lookup list had 43 objects: 13 typed cohort objects, 20 sampled cohort objects, and 10 non-cohort objects classified in 2026 as controls.
  - All 43 archived pages returned 404 after retries.
  - Because the classified controls also return nothing, this channel cannot produce a positive, and its silence tells us nothing about cohort objects.
- **What WISeREP republishes.** The only readable home-page capture (2026-01-01) shows:
  - it hosts its own spectra, uploaded by registered users and groups through a report page or bulk APIs;
  - 70,387 spectra, of which 57,771 are public.

  Whether it mirrors TNS classifications, and who uploaded any given spectrum, is UNDEMONSTRATED.
- **Even if reachable, the check has limits.**
  - It could show: that a spectrum exists, who uploaded it, and the displayed type.
  - It could not show: who classified it, whether a human or a bot did, or whether the label is correct.
  - A missing page would not mean no spectrum exists.
- **What stays UNDEMONSTRATED.** Existence of measured labels and the classifier of the 13 typed cohort objects. This blocks P3 positive supply at measured labels, P4 precondition (a), and the L offset in agent 1's escalation option 1.

### Sealed predictions vs outcomes

| Prediction | Sealed | Outcome |
|---|---|---|
| Live WISeREP | 403 | 403 |
| Archived captures of typed cohort pages | 2 | 0 |
| Annual usable-night mean | 0.7 [0.5, 0.85] | 0.617 |
| Months to N = 485 at the reference point | 3 [2, 6] | 5 |

## Amendments (transport only)
- **AMW4-1:** WISeREP archive connection errors are retried, up to 3 times.
- **AMW4-2:** IRSA queries are split into 4 parallel year workers that resume from completed months.

## Disagreements (listed, not reconciled)
1. **Rubin on-sky fraction.** 10 of 15 (scheduler) vs 11 of 16 (Fink alert nights).
2. **Low P48 months.** 2021-12, 2022-01 and 2022-03 have 2, 2 and 4 usable nights, which looks like instrument downtime rather than weather. They are still included in the mean.
3. **SEDM capacity.** The SEDM paper says "average rate of 10 spectra per night". That paper was not read in full and was not used; the grid spans 4.5 to 10.
4. **Model-annotation bound.** Ruling 4 cites [803, 2,247]; the current bound is [954, 2,057].

## Still UNDEMONSTRATED

| Item | Blocks |
|---|---|
| Rubin return date | calendar completion dates |
| Palomar/Rubin sky overlap; P60-specific downtime | exact program duration |
| Rare-event miss rate | the missed-event cost term |
| Measured non-bot cohort labels (TNS and WISeREP both BLOCKED) | P3, P4 precondition (a) |

## Deliverables
- **Frozen inputs:** `calendar_model_FROZEN.md` and its `.sha256`; `sealed/` (4 files).
- **Pricing:** `truth_cost_monthly.json` and `.csv` (3,456 rows, both deltas).
- **WISeREP:** `wiserep_check.json`.
- **Logs and sources:** `order_of_operations.log`, `seed_ledger.json`.
- **Replay:** `replay_cases.csv` (AST2W4-01 and 02 must_fire; 03 and 04 must_not_fire) and `replay_rulings.csv`.
- **Supporting:** `scripts/`, `out/`, `sources/`.
- **Validation:** `validate.py provenance` passes on the monthly provenance records.
