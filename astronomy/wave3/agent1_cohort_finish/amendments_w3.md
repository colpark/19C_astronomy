# Wave-3 procedural amendments (bands, definitions and protocol ranges unchanged)

## AM6 (2026-09-16T20:52Z): resume incomplete slices after HTTP 429
- **Cause.** Run 1 of W3-C3, W3-P60 and W3-C5 ran concurrently, 3 threads each. Each ended with exactly 24 slices failed on HTTP 429 (rate limit) after 3 retries 10 s apart. Summaries are in `out/w3_c3_run1.json`, `out/w3_p60_run1.json` and `out/w3_c5_run1.json`. Completed slices: 426/450, 1527/1551, 1476/1500.
- **Change.**
  - The three jobs are re-launched one at a time, W3-C3 then W3-P60 then W3-C5, each with 1 thread.
  - Completed slice files are skipped, as the protocol's persistence rule allows.
  - An HTTP 429 gets 6 retries with 60 s back-off.
  - Each resume run has its own 2 h wall cap.
  - A slice still failing is recorded incomplete, and its job is UNDEMONSTRATED with a lower bound.

## AM7 (2026-09-16T21:25Z): W3-X comparison field
- **Cause.** Fink `/api/v1/objects` serves `r:firstDiaSourceMjdTai`, `r:lastDiaSourceMjdTai` and `r:firstDiaSourceMjdTai` as null. The probe at log step 9p requested all columns for 2 cohort ids and got 'r:firstDiaSourceMjdTai': None, while 'f:firstDiaSourceMjdTaiFink' = 61235.1671142462.
- **Consequence.**
  - The Rubin APDB first-detection time is not obtainable publicly, so the W3-X "precovery vs alert stream" comparison against the Rubin field is **UNDEMONSTRATED**.
  - The wave-2 C4 fields `fink_places_before_T0 = 0` and `first_detection_disagree_gt_1s = 0` were vacuous: 3000/3000 null. This is a correction to the wave-2 record, listed and not hidden.
- **Change.** W3-X compares Fink's alert-history first time (`f:firstDiaSourceMjdTaiFink`, already stored per row) with ALeRCE firstmjd and with ANTARES oldest time. It is recomputed from `out/w3_crosscheck.json` rows, with no new requests.
