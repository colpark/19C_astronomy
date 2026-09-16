# Wave-3 count protocol (FROZEN before any wave-3 count)

**Governing documents, unchanged and not re-banded:**
- `astronomy/wave2/agent1_rubin_bands/bands_FROZEN.md`, sha256 8825ef8048b733b66e12f31ce16e67270de171f52f20f40ca8f21e5780e500d2;
- `count_protocol_FROZEN.md`, sha256 5a5de4c8…ed82;
- amendments AM1–AM5 (`amendments.md`, sha256 e370fcd4…bdf9).

This file adds procedure only. It reuses T0 = MJD(TAI) 61222.000428, unit rules X1–X4, strata S0–S4 and the "unlabelled is never negative" rule.

**Disclosure.** Before freezing I ran two things:
- Fink per-night sums over already-held statistics: first detections for UTC dates 20260502–20260630 = 1,664,152, which sizes the merge-partner set;
- a throughput probe, one dense slice at page_size 1000 and at 5000 (log step 1p).

No wave-3 cohort, straddler, merge or unprocessable count had been computed.

## Why C3 and C5 are re-run, not resumed row by row
The wave-2 checkpoints (`checkpoints_from_wave2/c3_progress.txt`, `c5_progress.txt`) hold only per-slice summary lines. Object rows were kept in memory and lost when the jobs stopped. Resuming therefore means re-enumerating. The wave-2 lower bounds are kept as adjudicators: C3 ≥ 189,641 distinct oids over 82 slices; C5 ≥ 21,126 straddlers through UTC date 20260523. A completed wave-3 count below either lower bound, on the same slices, is a defect to be listed.

## W3-C3: cohort enumeration (ALeRCE/LSST)
- **Endpoint** as in C3, via `scripts/safe_fetch.py`, which strips label keys, at `page_size=5000`.
- **Ranges.** The 9 UTC dates carrying Fink alerts after T0 (AM3), in 0.02 d slices. Each slice is paged until a page returns fewer than 5000 rows. No page-30 split; instead, a slice reaching page 200 is marked incomplete.
- **Persistence.** Each completed slice writes its rows (oid, meanra, meandec, firstmjd, lastmjd, n_det, n_forced) to `out/w3_c3_slices/<a>_<b>.csv` before being counted, so a restart skips completed slices.
- **Retries.** 3 per request, 10 s apart. Concurrency 3.
- **Time cap.** 2 h wall clock from launch. On reaching it, the job stops and the result is UNDEMONSTRATED with the persisted rows as a lower bound.
- **Coverage-limit check.** One page_size=1 request per non-Fink UTC date between 20260701 and 20260916 whose firstmjd range is ≥ T0. A day-level query that returns 504 is recorded as undetermined, never as zero.

## W3-P60: merge partners and straddlers from the 60 d before T0 (ALeRCE/LSST)
- **Same procedure as W3-C3** (endpoint, slicing, paging, persistence, retries, concurrency) over the UTC dates in [2026-05-02 = T0 − 60 d, T0) with Fink alerts > 0, with the last slice clipped at T0. Stored in `out/w3_p60_slices/`.
- **Straddlers with firstmjd in [T0 − 60 d, T0).** Read directly from the lastmjd column: lastmjd ≥ T0.
- **Straddlers with firstmjd in [2026-02-24, T0 − 60 d).** The C5 procedure with its lastmjd ≥ T0 filter, at page_size 5000, over the Fink alert dates in that range, stored in `out/w3_c5_slices/`.
- **Time cap.** W3-P60 and W3-C5 share the same 2 h cap as W3-C3 and run concurrently with it.

## W3-M: merge (X1–X3), cohort after merge, strata
- **Input.** Union of W3-C3 and W3-P60 rows, deduplicated on oid (X1 within ALeRCE).
- **X2.** Connected components over pairs ≤ 1″ apart, by 3-D KD-tree chord distance, with |Δ firstmjd| ≤ 60 d.
- **X3.** Pairs ≤ 1″ apart with |Δ firstmjd| > 60 d stay distinct and are counted.
- **O_merged.** Components whose minimum firstmjd ≥ T0 and whose members all have firstmjd ≥ T0.
- **S1 split into two parts:**
  - **S1-direct:** pre-T0 oids with lastmjd ≥ T0;
  - **S1-merge:** cohort oids pulled out of the cohort because they merge with a pre-T0 oid.
- **One-detection share.**
  - S3: cohort oids with n_det = 1 over all cohort oids.
  - The same at merged-object level, with component n_det summed.
- **Unprocessable U.** Rows lacking oid, meanra, meandec or firstmjd, or with meandec outside [−90, 90]. Documented, never repaired.
- **Cross-epoch control.** W3-P60 can only merge pairs whose pre-T0 member has firstmjd ≥ T0 − 60 d. Merges with older objects are excluded by X2 itself (Δ > 60 d), so no older partner can change O_merged. This follows from the rule and needs no counting.

## W3-X: cross-broker and precovery check (declared sample)
- **Sample.** From W3-C3, per cohort UTC date, the 1000 oids with the smallest sha1(oid) hex. That is up to 9000 oids, fixed by the rule before the table exists.
- **Fink.** `POST /api/v1/objects`, columns `r:diaObjectId,r:firstDiaSourceMjdTai,r:nDiaSources,f:firstDiaSourceMjdTaiFink`, batches of 100.
- **ANTARES.** `terms` on dia_object_id, batches of 100: presence, num_alerts, oldest time.
- **Reported, never reconciled:**
  - Rubin `firstDiaSourceMjdTai` (APDB, carried in the alert) vs ALeRCE firstmjd vs Fink-computed first time;
  - any Rubin first time before T0 (a hidden earlier DIASource, i.e. precovery/APDB history beyond the alert stream);
  - nDiaSources vs n_det.

## W3-PPDB: release check
- **Primary Rubin sources only:** community.lsst.org News category and its latest topics JSON, rubinobservatory.org news, rtn-011.lsst.io (current revision), and the data.lsst.cloud or rsp.lsst.io PPDB documentation page if linked from those.
- **Record:** release status, with locator and fetch time.
- **If unreleased,** the precovery effect is bounded from documented depths only:
  - alert history (prvDiaSources, 12 months, LDM-612);
  - precovery forced photometry (30 days, LSE-163; forced sources are not detections under bands §3, so they cannot create S1);
  - W3-X observed disagreement between the Rubin APDB first time and the alert-stream first time.

## W3-P7: planning bracket at the PI delta override
- **Script.** Agent 5's `scripts/planning_mde_bracket.py`, copied unchanged except DELTAS = [0.018, 0.05] and output paths, running the vendored `power.py`.
- **Check.** The 0.018 column must reproduce `planning_mde_bracket.csv` exactly. Any difference is listed.
- **Status.** Labelled PLANNING-ONLY, not a P7 record.
- **Threshold reporting.** Thresholds at 0.05 (min and max N_min per family) are reported beside the frozen 0.018 thresholds. They do not re-band; the frozen bands stay the ones ruled against.

## Sealing (rule C)
- W3 outputs go to `sealed/rubin_counts_w3_SEALED.json`, hashed before any label field is read.
- No label field is planned to be read in wave 3; labels are agent 2's.
