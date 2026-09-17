#!/usr/bin/env python3
"""Rule C seal: predictions (protocol sec 9) and lookup list (sec 8) BEFORE reading any classification."""
import hashlib, json, glob, os, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
A1 = D.parent / "agent1_cohort_finish"
assert hashlib.sha256((D/"census_protocol_FROZEN.md").read_bytes()).hexdigest() == "9fac85524f28b5e3874a0d43a2c089915d20814b7996c18a0c77cc230b3c95fb"
T0 = 61222.000428
slices = sorted(glob.glob(str(A1/"out/w3_c3_slices/*.csv")))
best = []
import heapq
n = 0
for f in slices:
    with open(f) as fh:
        next(fh)
        for line in fh:
            oid, ra, dec, fm = line.split(",")[:4]
            if float(fm) < T0: continue
            n += 1
            h = hashlib.sha1(oid.encode()).hexdigest()
            if len(best) < 2000: heapq.heappush(best, (-int(h, 16), h, oid))
            elif -best[0][0] > int(h, 16): heapq.heapreplace(best, (-int(h, 16), h, oid))
R = sorted((h, oid) for _, h, oid in best)
pred = dict(
  written_utc="2026-09-17, before reading any classification content",
  protocol_sha256="9fac85524f28b5e3874a0d43a2c089915d20814b7996c18a0c77cc230b3c95fb",
  predictions={
    "a_all_TNS_classification_reports_per_month_2026": {"point": 250, "range": [150, 450], "basis": "recollection of TNS scale (a few thousand classifications per year); not a source, prediction only"},
    "b_non_bot_measured_share": {"point": 0.7, "range": [0.5, 0.85]},
    "c_cohort_objects_with_any_TNS_classification_Jul_Sep_2026": {"point": 60, "range": [0, 400]},
    "f19": {"point": 0.005, "range": [0.0005, 0.03]},
    "f185": {"point": 0.002, "range": [0.0002, 0.015]},
    "A_reachable_arrivals_per_on_sky_night_f19": {"point": 970, "range": [100, 6000], "note": "f19 x 1,937,669 / 10"},
  })
lookup = dict(
  written_utc="2026-09-17, before reading any classification content",
  protocol_sha256=pred["protocol_sha256"],
  cohort_definition=dict(T0_mjd_tai=T0, slices_dir="astronomy/wave3/agent1_cohort_finish/out/w3_c3_slices", slice_files=len(slices), eligible_rows=n,
      SLICES_SHA256SUMS_sha256=hashlib.sha256((A1/"out/SLICES_SHA256SUMS").read_bytes()).hexdigest()),
  queries_T7_T8=[
    "Fink LSST: GET /api/v1/schema (or served schema) to find TNS-crossmatch column names; then any served TNS search endpoint restricted to cohort times; per-object objects endpoint only for sample R (non-label columns via safe_fetch) and for E objects matched by position",
    "ANTARES: POST/GET /v1/loci with ES query: catalogs contains a TNS catalog AND properties.oldest_alert_observation_time >= T0 (MJD) ; enumerate all hits (ids, ra, dec, catalog_objects TNS name/type)",
    "ALeRCE LSST: crossmatch endpoint for E objects matched by position (if served)",
  ],
  lookup_rule="every object in enumeration list E (T3/T9/T10 plus T7/T8 hits) whose TNS discovery date >= 2026-06-30 or that matches a cohort oid within 1.0 arcsec is looked up in T1; all other E objects looked up in random order (seed 20260917) within the 4 h cap",
  sample_R=dict(n=len(R), rule="2000 cohort oids with smallest sha1(oid) hex, firstmjd>=T0", oids=[o for _, o in R]),
)
(D/"sealed").mkdir(exist_ok=True)
for name, obj in [("predictions_SEALED.json", pred), ("lookup_list_SEALED.json", lookup)]:
    p = D/"sealed"/name; p.write_text(json.dumps(obj, indent=1))
    h = hashlib.sha256(p.read_bytes()).hexdigest(); (D/"sealed"/(name.replace(".json", ".sha256"))).write_text(f"{h}  {name}\n"); print(name, h)
print("eligible cohort rows", n)
