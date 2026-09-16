# Procedural amendments to count_protocol_FROZEN.md (definitions and bands unchanged)

## AM1 (2026-09-16T19:0x UTC): C2 ANTARES bisection on a degenerate timestamp
- **Cause.** The first C2 run hit its 2,000-request cap and returned UNDEMONSTRATED. Its partial sum was 137,576 loci, a lower bound kept in `out/c2_antares_run1.json`.
- A single oldest_alert_observation_time, MJD 61227.17255441374, carries ≥ 10,000 loci, so bisecting on time cannot bring the count below the cap. Roughly 1,000 requests recursed on an interval of width < 1e-9 d.
- **Change.** When a time slice narrower than 1e-6 d still returns 10,000, it is split by bisection on the locus `ra` attribute, over [0, 360) deg, with the time range held fixed. Degree bisection stops at 1e-4 deg; a slice still capped there is marked incomplete.
- **Cap.** The rerun gets a fresh 2,000-request cap. Run 1's requests are recorded and not reused.
- **Does not change:** unit, boundaries, filters, label handling, bands.

## AM2 (2026-09-16T19:17 UTC): C3 ALeRCE, empty-day pre-check and concurrency
- **Cause.** Under C3 as written, [T0, 61300) has about 3,900 slices of 0.02 d. Fink statistics show alerts on only 9 cohort nights, so most slices are empty. Their page-1 requests alone would use most of the 4,000-request cap before the populated slices are reached.
- **Change 1.** Each whole day in [T0, 61300) is first checked with one page_size=1 request. Only days returning a row are sliced at 0.02 d.
- **Change 2.** Up to 3 concurrent requests.
- **Unchanged:** the 4,000 cap, the page-30 split rule, dedupe on oid, stripped label keys, and incomplete-slice marking.
- **C5 (straddlers).** Deferred until after C3 completes, under the same cap rules.

## AM3 (2026-09-16T19:22 UTC): C3 ALeRCE, replace the day pre-check
- **Cause.** Under AM2, every whole-day pre-check that ran (firstmjd days starting 61223, 61224, 61225) returned HTTP 504 Gateway Time-out from nginx/1.31.3 after about 60 s, even with page_size=1. The run was stopped after about 3 minutes, with no slice enumerated. The statuses are copied into `out/c3_alerce_run1_note.json`.
- **Change 1.** Slices of 0.02 d are enumerated only on the UTC dates on which Fink statistics show alerts > 0 after T0: 20260701, 20260706, 20260707, 20260709, 20260710, 20260711, 20260712, 20260713, 20260714. Each date is covered from max(T0, 00:00 UTC) through 24:00 UTC, with times converted to TAI.
- **Change 2.** Objects ALeRCE holds on other dates are not enumerated, so the ALeRCE count is a lower bound on ALeRCE's holdings outside that list. This is recorded as a coverage limit.
- **Change 3.** Concurrency is 2.
- **Unchanged:** the cap of 4,000, page-30 splitting, dedupe, and stripped label keys.

## AM4 (2026-09-16T19:36 UTC): C4 sample W re-enumerated directly
- **Cause.** C3 writes its object table only at the end. At about 0.55 requests/s it will run for roughly 2 hours to its cap.
- **Change.** C4 enumerates W = ALeRCE objects with firstmjd in [T0, T0 + 0.25 d) directly, using the same endpoint, 0.02 d slices and dedupe as C3.
- **Unchanged:** W's definition, the 3,000 cap and the checks.

## AM5 (2026-09-16T19:40 UTC): C5 run concurrently with C3, adaptive slicing
- **Cause.** C3 will take about 2 hours to reach its cap. A probe confirmed the server honours lastmjd: 997 of 997 distinct oids returned had lastmjd ≥ T0, against 201 of 995 without the filter (`order_of_operations.log` step 4-C5p). Fixed 0.02 d slices over 2026-02-24 to T0 would exceed the 3,000-request cap on empty slices alone.
- **Change.** C5 enumerates firstmjd per UTC date on which Fink statistics show alerts, over [61095.000428, T0), with lastmjd in [T0, 61300). It starts with page 1 of the whole date. If page 1 is full (1,000 rows), the range is halved recursively. Below 0.0005 d, it pages normally.
- **Concurrency.** 1, running alongside C3.
- **Unchanged:** the cap of 3,000; on reaching it, S1 is UNDEMONSTRATED with the partial count as a lower bound.
