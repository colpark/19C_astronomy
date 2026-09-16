# Tool coverage recount protocol: FROZEN before any alert fetch or tool run

calibration only, contamination FAIL on the BTS cohort; this recount carries no arm result (rule D)

- **Author and scope.** Wave-3 agent 4, under PANEL_BRIEF_WAVE3.md (sha256 `a618d9114ec7c937cf6115a67be188a16a69856949bde33bf6fa9c8e8981c4b6`, verified against BRIEF_SHA256 at 2026-09-16T20:47:57Z).
- **Band hash this recount must post-date.** `astronomy/wave2/agent1_rubin_bands/bands_FROZEN.md` sha256 `8825ef8048b733b66e12f31ce16e67270de171f52f20f40ca8f21e5780e500d2`, hashed at **2026-09-16T18:51:26.922781Z** (agent 1 order_of_operations.log step 1). Its §tool_coverage says the band governs only a recount performed after that hash.
- **This file's hash and freeze time.** Recorded in `recount_protocol_FROZEN.sha256` and in `order_of_operations.log`. Every recount run timestamp must be later than both.
- **Seen before freezing (disclosure).** No broker object query, cohort alert or tool run happened before this file was frozen. What was seen:
  - the wave-1 inventory (`agent4_tools_instrument/tool_inventory_slot.json`)
  - Fink Rubin processor code (`fink_science/rubin/{random_forest_snia,slsn,snn,cats}/processor.py` at 591e75ce)
  - endpoint discovery probes, logged at step 2a: Fink LSST API root, `swagger.json`, `/api/v1/schema` for sources, objects and fp; ALeRCE LSST root, docs and openapi (404); ANTARES `/v1/` (404); Lasair `/api/` (404)
  - the Fink schema output, which lists 104 `r:` (LSST original) and 30 `f:` (Fink module and crossmatch) fields for `/api/v1/sources`, and output formats json, csv, parquet and votable, with no Avro
  - the wave-2 power recompute, done from wave-2 files at step 1

## 1. Pass criterion (per tool, per alert)
An alert run **passes** when all three stages complete in one process on one real Rubin alert (§3), with no step supplied by this agent other than the permitted reshape (§4):
- **parse:** the tool's own input path accepts the alert content;
- **infer:** the tool computes;
- **emit:** the tool returns an output that is **non-default** by the tool-specific rule in §5.

**Tool disposition** (brief):
- **PASS:** at least 1 of up to 10 alert runs passes; the pass count out of the alerts run is reported.
- **FAIL:** the tool loaded but failed parse, infer or emit on every alert run. The stage and the error text are recorded.
- **UNDEMONSTRATED:** the tool could not be loaded. The reason is one of: no weights, no code, install impossible within cap, checkpoint over cap, or external service or database not provisioned.

**Packet-format honesty.** Full lsst v11_1 Avro alert packets are not served by any public endpoint found in step 2a. §3 records one exact HTTP attempt for Avro. Every PASS is therefore reported as **"end-to-end on public broker rows carrying lsst v11_1 field names, not on v11_1 Avro packets"**, and the coverage axis carries that qualifier.

## 2. Tool list (25, wave-1 inventory) with the ratified Fink remapping
- **Remapping.** The ratified D5 remapping replaces ALeRCE_BHRF, which has no Rubin weights, as the Rubin classical counterpart for ATAT, Astromer1 and Astromer2 with Fink_EarlySNIa_RF and Fink_SLSN_RF. No other row changes.
- **Precondition checks** below are pass/fail gates run before any alert run. A tool failing its precondition is UNDEMONSTRATED with that reason and runs on no alert.

| # | Tool | Group | Rubin counterpart (after remap) | Declared attempt path (from code) | Precondition (checked before any alert run) |
|---|---|---|---|---|---|
| 1 | ATAT | FM/deep | Fink_EarlySNIa_RF, Fink_SLSN_RF (remapped) | alercebroker/ATAT@0db532f2 LC branch | weights ≤ 1 GB and pinned (wave 1: 10 GB Drive zip, unpinned) |
| 2 | ORACLE | FM/deep | ALeRCE_BHRF, Fink_EarlySNIa_RF | uiucsn/Astro-ORACLE@876e0339, lite (no_md) model | package imports; lite weights hash-match |
| 3 | SuperNNova | FM/deep | Fink_EarlySNIa_RF, Fink_SLSN_RF | fink-science@591e75ce `rubin/snn/processor.py` `snn_ia_elasticc` and `snn_broad_elasticc` (underlying `.func`), models elasticc_ia and elasticc_broad | supernnova imports; model files hash-match fink repo at pin |
| 4 | CATS | FM/deep | Fink_EarlySNIa_RF, Fink_SLSN_RF | fink-science@591e75ce `rubin/cats/processor.py::predict_nn.func` | tensorflow imports; savedmodel present at pin |
| 5 | RAPID | FM/deep | ALeRCE_BHRF, Superphot_plus | astrorapid@7f28499f `Classify` | installs within cap; model hash-match |
| 6 | SCONE | FM/deep | SALT3_sncosmo, ALeRCE_BHRF | helenqu/scone@9b72001b | released weights exist (wave 1: none) |
| 7 | BTSbot | FM/deep | ALeRCE_BHRF | nabeelre/BTSbot@f4281202 + HF checkpoint | installs; checkpoint hash c30f3202… |
| 8 | AppleCiDEr | FM/deep | ALeRCE_BHRF | skyportal/applecider@48148937 | released weights exist (wave 1: none) |
| 9 | Maven | FM/deep | Superphot_plus, ALeRCE_BHRF, SALT3_sncosmo | ThomasHelfer/multimodal-supernovae@1f571aa9 | installs; ckpt hash 0fc75ccc… |
| 10 | Astromer1 | FM/deep | Fink_EarlySNIa_RF, Fink_SLSN_RF (remapped) | astromer-science python-library@75262739 + weights repo | installs; weights hash-match |
| 11 | Astromer2 | FM/deep | Fink_EarlySNIa_RF, Fink_SLSN_RF (remapped) | astromer-science main-code@009634c8 + Zenodo 10.5281/zenodo.18207945 | weights ≤ 1 GB, downloadable, hashed |
| 12 | MultibandAstromer | FM/deep | ALeRCE_BHRF | multiband-astromer@7228548b | released weights exist (wave 1: none) |
| 13 | AstroCLIP | FM/deep | GHOST, Blast | PolymathicAI/AstroCLIP@e129576a | checkpoint ≤ 1 GB (wave 1: 1.68 GB) |
| 14 | AstroM3 | FM/deep | ALeRCE_BHRF | MeriDK/AstroM3@7f296c22 | released weights exist (wave 1: none) |
| 15 | ParSNIP | FM/deep | SALT3_sncosmo, Superphot_plus | kboone/parsnip@dcea62f `plasticc.pt` and `plasticc_photoz.pt` | imports; weights hash-match (a164aefe…, f41d06ce…) |
| 16 | ALeRCE_BHRF | classical | none | alercebroker/lc_classifier@b8a85200 + hierarchical_rf_1.1.1 | installs; weights hash-match wave-1 |
| 17 | SALT3_sncosmo | classical | none | sncosmo 2.13.1 `salt3` source | imports; model downloadable and hashed |
| 18 | Superphot_plus | classical | none | VTDA-Group/superphot-plus@973e2a80 tutorial model | installs; model hash a9536ff1… |
| 19 | Superphot | classical | none | griffin-h/superphot@eb3e31be | released trained classifier exists (wave 1: none) |
| 20 | Fink_EarlySNIa_RF | classical | none | fink-science@591e75ce `rubin/random_forest_snia/processor.py::rfscore_rainbow_elasticc_nometa.func` | model `sklearn_1.7.2/elasticc_rainbow_earlyIa_nometa-1.7.2.obj` hash 089bc049… |
| 21 | Fink_SLSN_RF | classical | none | fink-science@591e75ce `rubin/slsn/processor.py::slsn_rubin.func` | model `SLSN_rainbow_no_MD.joblib` hash 855e55d0… |
| 22 | Sherlock | classical | none | thespacedoctor/sherlock@37ef9298 | catalogue database provisioned (wave 1: not public) |
| 23 | GHOST | classical | none | uiucsn/astro_ghost@d7a1dec6 | installs; MLP weights hash 13ac27c2… |
| 24 | Blast | classical | none | scimma/blast@614ace3b | service stack or public API serving arbitrary positions |
| 25 | SNANA | classical | none | RickKessler/SNANA@74dfb2c5 | model libraries pinned and present (wave 1: absent) |

- **Hash mismatch.** Where a precondition names a hash, weights fetched in wave 3 must match it. A mismatch makes the tool UNDEMONSTRATED ("served checkpoint differs from inventory pin"); the tool is not run.
- **Pins.** Code is re-fetched at the wave-1 pinned commit, or copied from the wave-1 clone (read-only), into `code/`.

## 3. Alert sample (rule C; not selected on outcome or class)
- **T0** = MJD(TAI) 61222.000428, the first-detection admission boundary 2026-07-01T00:00 UTC from bands_FROZEN.md.
- **Step S1: candidate list.** `GET https://api-lsst.alerce.online/object_api/list_objects?survey=lsst&firstmjd=61222.000428&firstmjd=61222.020428&page_size=1000&page=1` through `scripts/safe_fetch.py`, which strips class, probability, score, tag and crossmatch keys before writing (copied unchanged from wave-2 agent 1). Rows are sorted by (firstmjd ascending, oid ascending). If the page returns 0 rows, the window is extended in steps of 0.02 d, up to 10 steps.
- **Step S2: acceptance.** Walk the sorted list in order. For each oid, POST Fink `/api/v1/objects` with `columns = r:diaObjectId,r:firstDiaSourceMjdTai,r:nDiaSources,r:ra,r:dec` (no `f:` column). Accept an oid if Fink returns a row with that id.
  - Stop at 10 accepted, or after 40 oids examined.
  - Availability in Fink is the only acceptance condition. It is not an outcome.
- **Step S3: seal.** Write `sealed/alert_ids_SEALED.json` (accepted ids, examined ids, source response hashes), hash it and log it **before any tool runs and before any light curve is fetched**.
- **Step S4: alert content.**
  - Fink `/api/v1/sources` for each accepted id, `columns` restricted to `r:` fields only: `r:diaObjectId,r:diaSourceId,r:midpointMjdTai,r:band,r:psfFlux,r:psfFluxErr,r:ra,r:dec,r:snr,r:isNegative,r:reliability`, via safe_fetch.
  - Also Fink `/api/v1/objects` with `r:` columns only.
  - One alert = the object's diaSource light curve as served at fetch time (latest alert plus history).
  - Sanitized rows and response hashes are kept under `out/raw/`.
- **Avro attempt (recorded, not repaired).** One request, Fink `/api/v1/sources` with `output-format=avro` for the first accepted id. Status, headers and body hash are recorded.

## 4. Permitted and forbidden adapters (preamble item 5)
- **Permitted: reshape only.** Place the served `r:` field values, unchanged, into the container the tool's own code reads: pandas Series of per-object arrays for Fink `pandas_udf` functions called through `.func`, or the column names a tool's parser names **when those names are the lsst v11_1 names**.
  - No arithmetic on values.
  - No unit, zeropoint, band-name or time-system change.
  - No renaming of a field to a different physical quantity.
- **Forbidden.** Any conversion the tool's code does not itself perform:
  - nJy to FLUXCAL, magnitude or ZP 25 flux
  - `g` to `lsstg` / `ztfg`, or band to integer id
  - adding redshift, photo-z, host or ZTF-only fields
  - building cutouts or metadata the alert lacks

  A tool whose input path needs such a conversion is **FAIL at parse**, recorded with the field or convention its code requires (quoted from code). A conversion already inside the tool's code (e.g. Fink SNN `fac = 10**(-(31.4-27.5)/2.5)`) is the tool's and is allowed.

## 5. Non-default output rules (declared per tool)
- **Fink_EarlySNIa_RF:** returned value not in {−1.0, 0.0}. Code default: −1 when the rainbow features are zero; 0 when empty.
- **Fink_SLSN_RF:** returned value ≠ 0.0. Code: "Return 0 if the minimum number of point per passband is not respected".
- **SuperNNova (Fink):** at least one returned probability finite and not the code's empty-input default (0.0, or class −1 in `snn_broad`).
- **CATS (Fink):** returned vector not all 0.0 (code default for fewer than 2 points).
- **Any other tool:** at least one finite model output (probability, embedding or host match) that is not the code's documented empty or default return. The default is quoted from code in the run record before the run.

## 6. Caps (per tool)
- **Install and fetch:** ≤ 20 min wall clock, in a separate venv (`venv_w3tools` in the scratchpad).
- **Weights:** ≤ 1 GB per tool. Over cap: UNDEMONSTRATED "checkpoint over cap".
- **Runs:** ≤ 1 load run plus ≤ 10 alert runs; ≤ 5 min per alert run; ≤ 45 min per tool in total.
- **Global:** ≤ 25 tools × 10 alerts = 250 alert runs.
- **Interrupted:** a tool cut off by its cap before a disposition is UNDEMONSTRATED (interrupted), never zero.

## 7. Logging and retention (rule D)
- **`run_log.jsonl`**, one line per run (load or alert), with:
  - timestamp start and end (UTC)
  - tool
  - alert id or `LOAD`/`PRECHECK`
  - exact command or callable
  - exit status (`ok`, `error:<stage>`)
  - error text (truncated to 500 chars)
  - `output_sha256` of the JSON-serialised output
  - `non_default` (bool)
- **Retention.** Outputs are hashed and then discarded. No output value is written to disk or shown as a result, and nothing is kept as an arm result. Only the hash and the non-default flag are logged.
- **Order.** `order_of_operations.log` records every step with file hashes. The id seal comes before any tool run.

## 8. Coverage axis (deliverable)
- **File.** `tool_coverage_axis.json` holds:
  - the recount start and end timestamps (both after the band hash)
  - counts by group (FM/deep, classical) × disposition (PASS, FAIL, UNDEMONSTRATED)
  - per-tool dispositions with the stage, error or reason, and pass counts out of the alerts run
  - the packet-format qualifier
  - `supersedes` = `astronomy/agent4_tools_instrument/tool_coverage_axis.json` with its sha256
- **Band reading** (from bands_FROZEN.md, stated, not ruled here):
  - **PROCEED** needs ≥ 1 FM/deep PASS and ≥ 1 classical counterpart PASS for each such channel;
  - **CLOSE** if no FM/deep channel accepts v11.1 inputs;
  - **ESCALATE** otherwise.
- **P4 precondition (b) clears** iff every recount run timestamp is after 18:51:26.922781Z **and** all 25 tools carry a disposition. Zero passes is still a number.

## 9. Anti-widening and tuning rule
- **Frozen.** §1–§8 do not change after the hash. A change is an amendment recorded with its cause in `amendments.md` before the affected run.
- **Low counts.** A low pass count is reported as low.
- **Failing tools.** A failing tool is not repaired: no patching of tool source, and no gate relaxation.
