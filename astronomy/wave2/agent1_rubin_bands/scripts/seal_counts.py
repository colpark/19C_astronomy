#!/usr/bin/env python3
"""Assemble all non-label counts into sealed/rubin_counts_SEALED.json and rubin_cohort_count.json (provenance records).
No classification or TNS field is read by this script or by any input it uses."""
import csv, json, hashlib, pathlib, math
from collections import defaultdict
D = pathlib.Path(__file__).resolve().parent.parent
T0 = 61222.000428
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
c1 = json.load(open(D / "out/c1_fink.json")); c2 = json.load(open(D / "out/c2_antares.json"))
c3 = json.load(open(D / "out/c3_alerce.json"));
c4 = json.load(open(D / "out/c4_crossbroker.json"))["summary"]
nights = json.load(open(D / "out/nights_observed.json"))
c3sum = c3  # C3 interrupted: no object table; X2 merge, S3/S4 and U from C3 UNDEMONSTRATED
c5 = json.load(open(D / "out/c5_straddlers.json"))
counts = dict(
  sealed_note="non-label counts only; sealed before any classification or TNS field is read",
  bands="bands_FROZEN.md sha256 " + sha(D / "bands_FROZEN.md"), protocol="count_protocol_FROZEN.md sha256 " + sha(D / "count_protocol_FROZEN.md"),
  amendments="amendments.md sha256 " + sha(D / "amendments.md"),
  C1_fink=dict(file_sha256=c1["sha256"], lower=({k: v for k, v in c1["lower_bracket_nights_ge_20260701"].items()}), upper=({k: v for k, v in c1["upper_bracket_nights_ge_20260630"].items()}),
               last_night_with_alerts=c1["last_night_with_alerts"], night_convention_inferred="Fink night = UTC date = dayObs+1 (scheduler nights shifted +1 equal Fink alert nights; Fink visits for dayObs 0710-0714 = 336 vs Rubin '337 processed visits')"),
  C2_antares={k: v for k, v in c2.items() if k != "slices"} | {"slices_file_sha256": sha(D / "out/c2_antares.json")},
  C3_alerce=c3sum,
  C4_crossbroker=c4 | {"file_sha256": sha(D / "out/c4_crossbroker.json")},
  nights=dict(M_obs_scheduler_dayObs_ge_20260629=nights["n_scheduler"], nights=nights["nights_with_science_visits_scheduler"],
              cohort_nights_after_T0=nights["cohort_nights_ge_20260701_scheduler"], fink_alert_nights=nights["nights_with_alerts_fink"],
              science_visits_total=nights["science_visits_total_ge_20260629"], last_night_with_science=nights["last_scheduler_night_with_science"],
              toc_sha256=nights["toc_sha256"]),
  lasair="UNDEMONSTRATED: status page 'fully offline from Monday morning Sept 14 through Wednesday Sept 16'; https://lasair.lsst.ac.uk/api/ HTTP 404; Lasair LSST: Down (ConnectTimeoutError to 192.41.122.98:443)",
  pitt_google="UNDEMONSTRATED: BigQuery REST unauthenticated -> HTTP 401 UNAUTHENTICATED 'Request is missing required authentication credential' (CREDENTIALS_MISSING); client requires GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS",
  C5_straddlers=c5)
(D / "sealed").mkdir(exist_ok=True)
json.dump(counts, open(D / "sealed/rubin_counts_SEALED.json", "w"), indent=1)
print(json.dumps(counts, indent=1))
