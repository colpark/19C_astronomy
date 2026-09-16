"""Protocol section 3 S4: r:-only alert content for the sealed v2 ids, plus one recorded Avro attempt."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from safe_fetch import fetch
D = pathlib.Path(__file__).resolve().parent.parent
ids = json.load(open(D / "sealed/alert_ids_SEALED_v2.json"))["accepted_ids"]
SRC = "r:diaObjectId,r:diaSourceId,r:midpointMjdTai,r:band,r:psfFlux,r:psfFluxErr,r:ra,r:dec,r:snr,r:isNegative,r:reliability"
OBJ = "r:diaObjectId,r:firstDiaSourceMjdTai,r:nDiaSources,r:ra,r:dec"
summary = []
for oid in ids:
    r1, d1 = fetch(f"s4_sources_{oid}", "POST", "https://api.lsst.fink-portal.org/api/v1/sources",
                   {"diaObjectId": oid, "columns": SRC, "output-format": "json"})
    r2, d2 = fetch(f"s4_objects_{oid}", "POST", "https://api.lsst.fink-portal.org/api/v1/objects",
                   {"diaObjectId": oid, "columns": OBJ, "output-format": "json"})
    summary.append({"oid": oid, "sources_status": r1.get("status"), "n_source_rows": len(d1) if isinstance(d1, list) else None,
                    "sources_raw_sha256": r1.get("raw_sha256"), "sources_dropped": r1.get("dropped_keys"),
                    "objects_status": r2.get("status"), "objects_raw_sha256": r2.get("raw_sha256")})
ra, _ = fetch(f"s4_avro_attempt_{ids[0]}", "POST", "https://api.lsst.fink-portal.org/api/v1/sources",
              {"diaObjectId": ids[0], "columns": SRC, "output-format": "avro"})
(D / "out/alert_content_summary.json").write_text(json.dumps({"alerts": summary, "avro_attempt": ra}, indent=1))
print(json.dumps(summary, indent=0)[:1500]); print("AVRO", ra.get("status"), ra.get("kind"), ra.get("raw_bytes"))
