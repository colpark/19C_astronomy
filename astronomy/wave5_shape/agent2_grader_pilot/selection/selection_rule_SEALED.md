# Pilot selection rule: SEALED before any object photometry is fetched

PRE-RATIFICATION PILOT (harness check only). Rule C: no `type`, `redshift`, `peakabs`, `peakmag`, `IAUID`, `RA`, `Dec` or any other BTS column except `ZTFID` and `peakt` is read before the selection record (`selection/selection_SEALED.json`) is written and hashed.
Protocol: `grader_protocol_FROZEN.md` sha256 `ef58005482a049e5d58131267b0758ab0bfae3bb1c674650d6302f545fa709bc` (§1, §2, §7, §10). R1 disposition before this rule: R1-PASS (`r1/r1_result.json`).

## Inputs
- `astronomy/data/raw/ztf_bts_all_2026-09-16.csv`, sha256 `61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570`, read with `usecols=["ZTFID", "peakt"]`, all as strings.
- `astronomy/wave2/agent4_instrument/data_cache/cohort_rows.csv`, read with `usecols=["ZTFID"]` (the ParSNIP training cohort of all five folds).
- ALeRCE `https://api.alerce.online/ztf/v1/objects/{ZTFID}/lightcurve`.

## Rule (applied in this order)
1. Keep rows whose `peakt` parses as a float and whose peak date `JD = peakt + 2458000` falls in UTC **[2022-01-01T00:00, 2023-01-01T00:00)**.
2. Drop any ZTFID present in the wave-2 cohort (so the object is in no ParSNIP fold's training set, including fold 0).
3. De-duplicate ZTFID; sort ascending as strings.
4. Walk the list. For each ZTFID fetch the ALeRCE light curve (serial, 30 s timeout, up to 3 attempts with 1/2/4 s backoff; raw response saved to `data_cache/alerce_raw/{ZTFID}.json` and hashed). Using `scripts/item_builder.py::split` and `counts` (protocol §1–§2), compute from photometry only:
   - `n_pos_g`, `n_pos_r`: positive g/r detections over the whole light curve;
   - `t_first`; `peak_mjd = peakt + 2458000 − 2400000.5`;
   - pre-cut detections per band; held-out detections per band.
5. The object **passes** iff all hold: `n_pos_g ≥ 20` and `n_pos_r ≥ 20`; `0 ≤ peak_mjd − t_first ≤ 100` d (excludes long-history recurrent sources by dates alone); pre-cut detections ≥ 3 in each band; held-out detections ≥ 8 in each band.
6. The **first passing ZTFID** is selected. Stop.
7. **Caps:** at most 150 ZTFIDs fetched. A fetch failure is recorded as `fetch_fail` and the walk continues (never re-fetched from another broker). If the cap is reached with no pass: no pilot item (UNDEMONSTRATED), rule not relaxed.

## Seal record
`selection/selection_SEALED.json`: every examined ZTFID with its counts and pass/fail reason, the selected ZTFID, the raw-response hashes, the BTS and cohort file hashes, and this rule's hash. Its sha256 is appended to `order_of_operations.log` before any other BTS column of the selected object is read, and before contamination is checked.
