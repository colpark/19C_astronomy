# Count protocol (FROZEN before any cohort count)

This file adds procedure only. Bands, boundaries, unit and label maps stay as in `bands_FROZEN.md` (sha256 8825ef80…00d2). It was written after the endpoint probes logged in `order_of_operations.log` steps 3a–3d, which returned 1-row samples and per-night aggregates. No cohort total had been summed when it was frozen. The per-night Fink statistics rows were printed on screen, but they were not summed. That is disclosed here.

Admission boundary: T0 = MJD(TAI) 61222.000428. S0 lower edge: T_S = 61220.500428. Window end: time of query.

## C1. Fink/LSST aggregate (whole stream)
- Endpoint: `POST https://api.lsst.fink-portal.org/api/v1/statistics`, date "2026".
- Columns: `f:night,f:alerts,f:objects,f:is_first,f:is_sso,f:visits,f:lsst_schema_version`. No label columns.
- The night convention (UTC date vs dayObs) is undocumented (`sources/probes/fink_doc_services_api_statistics_.html`). Nights ≥ 20260701 lie after T0 under both conventions. Night 20260630 may be partly after T0.
- Counted over nights ≥ 20260701, in two brackets:
  - lower bracket: nights ≥ 20260701;
  - upper bracket: nights ≥ 20260630.
- Quantities:
  - new objects: O_F,hi = Σ is_first; O_F,lo = Σ is_first − Σ is_sso. Whether is_first includes SSO alerts is undocumented, which is why there are two;
  - raw: A_F = Σ alerts;
  - per-night unique objects: Σ objects, a night-summed quantity and not distinct across nights.
- Overstatement = (A_F − O_F) / O_F × 100. A_F includes alerts of pre-T0 objects observed after T0, so this overstatement is an upper bound for the cohort.
- M_obs,Fink: nights ≥ 20260629 with alerts > 0.

## C2. ANTARES (whole stream, locus level)
- Endpoint: `GET https://api.antares.noirlab.edu/v1/loci`, elasticsearch filter `exists properties.survey.lsst.dia_object_id` AND `range properties.oldest_alert_observation_time`.
- Read `meta.count` at page[limit]=1. Any ra/dec/id in that one row is not used.
- `meta.count` caps at 10,000, so the time range is bisected until every slice returns < 10,000. The counts of the slices are summed.
- Ranges: cohort [T0, 61300); S0 [T_S, T0).
- Definitional mismatch, recorded and not repaired: a locus merges ZTF and LSST alerts. oldest_alert may be a ZTF alert, so loci with pre-T0 ZTF alerts are absent, and a locus may carry more than one dia_object_id. The count is loci, not diaObjectIds.
- Cap: 2,000 requests. If the cap is hit, the result is UNDEMONSTRATED with the partial sum marked as a lower bound.

## C3. ALeRCE/LSST (object rows)
- Endpoint: `GET https://api-lsst.alerce.online/object_api/list_objects?survey=lsst&firstmjd=a&firstmjd=b&page_size=1000&page=p`.
- The class, probability and ranking keys are stripped before writing (`scripts/safe_fetch.py`).
- The `total` field is not a count, so enumeration pages until the page returns fewer than 1000 rows. Rows are deduplicated on `oid`.
- The firstmjd range [T0, 61300) is split into slices of 0.02 d. A slice whose enumeration reaches page 30 is split in half. The request cap is 4,000.
- Any HTTP error is retried twice after 5 s. It is then recorded, and the slice is marked incomplete.
- Kept per oid: oid, meanra, meandec, firstmjd, lastmjd, n_det, n_forced.
- Quantities: distinct oids O_A; raw detections Σ n_det; S3 (n_det = 1) and S4 (n_det ≥ 2); X2 merge at 1″ and 60 d within the cohort.
- Result status: complete if every slice completed. Otherwise the count is a lower bound and O_A is UNDEMONSTRATED.

## C4. Object-level cross-broker check (declared sample)
- Sample W: every ALeRCE cohort oid with firstmjd in [T0, T0 + 0.25 d), whole sky, taken from C3.
- Check W in Fink with `POST /api/v1/objects`, `diaObjectId` as a comma list in batches of 100, columns `r:diaObjectId,r:firstDiaSourceMjdTai,r:nDiaSources,r:ra,r:dec`.
- Check W in ANTARES with a `terms` filter on `properties.survey.lsst.dia_object_id`, in batches of 100. Read only dia_object_id, num_alerts and oldest_alert_observation_time.
- Reported, never reconciled:
  - presence in each broker;
  - first detection disagreement, and whether any broker places the object before T0 (split_integrity);
  - nDiaSources vs n_det vs num_alerts.
- Cap: 3,000 sampled oids (the first 3,000 ordered by firstmjd if W is larger).

## C5. Straddlers (S1)
- ALeRCE enumeration with firstmjd in [61095, T0) and lastmjd ≥ T0 is attempted, using the lastmjd parameter the client lists (`alerce/ms_search.py`) and the same slicing as C3, with a cap of 3,000 requests.
- If the lastmjd filter is ignored by the server (shown by any returned row with lastmjd < T0), S1 is UNDEMONSTRATED.

## C6. Unprocessable (U)
Rows in C3 or C4 lacking oid/diaObjectId, position, or first-detection time.

## Lasair and Pitt-Google
- **Lasair:** record the exact status page and HTTP responses. The status page on 2026-09-16 reads "fully offline from Monday morning Sept 14 through Wednesday Sept 16" (`sources/probes/lasair.lsst.ac.uk_.body`). Retry once after all C-steps; if still down, UNDEMONSTRATED.
- **Pitt-Google:** access is via Google Cloud BigQuery/PubSub with project credentials (`pittgoogle/__init__.py` requires GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS). Record one unauthenticated BigQuery REST response. UNDEMONSTRATED.

## Sealing
- All C-step outputs go into `sealed/rubin_counts_SEALED.json`, which is hashed before any classification or TNS field is read.
- After the seal: the Fink `in_tns` aggregate, then a TNS access attempt for measured labels.
