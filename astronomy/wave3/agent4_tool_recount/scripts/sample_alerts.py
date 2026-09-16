"""Protocol section 3, steps S1-S3: candidate list, Fink acceptance, seal. No light curve fetched here.
Label keys stripped by safe_fetch before write/print."""
import hashlib, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from safe_fetch import fetch

D = pathlib.Path(__file__).resolve().parent.parent
T0 = 61222.000428
rows, used = [], None
for step in range(10):
    a, b = T0 + 0.02 * step, T0 + 0.02 * (step + 1)
    url = (f"https://api-lsst.alerce.online/object_api/list_objects?survey=lsst&firstmjd={a:.6f}"
           f"&firstmjd={b:.6f}&page_size=1000&page=1")
    rec, data = fetch(f"s1v2_alerce_list_step{step}", "GET", url)
    items = data.get("items") if isinstance(data, dict) else data
    if rec.get("status") == 200 and items:
        rows, used = items, dict(url=url, raw_sha256=rec["raw_sha256"], status=rec["status"], dropped_keys=rec["dropped_keys"])
        break
    print("step", step, rec.get("status"), "no rows")
if not rows:
    sys.exit("S1 produced no candidate rows; recorded, stop")
rows = sorted(rows, key=lambda r: (float(r.get("firstmjd", 1e9)), str(r.get("oid"))))
_seen = set(); rows = [r for r in rows if not (str(r["oid"]) in _seen or _seen.add(str(r["oid"])))]  # AM1
examined, accepted, fink_hashes = [], [], []
for r in rows[:40]:
    oid = str(r["oid"])
    examined.append(oid)
    body = {"diaObjectId": oid, "columns": "r:diaObjectId,r:firstDiaSourceMjdTai,r:nDiaSources,r:ra,r:dec", "output-format": "json"}
    rec, data = fetch(f"s2v2_fink_objects_{oid}", "POST", "https://api.lsst.fink-portal.org/api/v1/objects", body)
    fink_hashes.append({"oid": oid, "status": rec.get("status"), "raw_sha256": rec.get("raw_sha256"), "dropped_keys": rec.get("dropped_keys")})
    if rec.get("status") == 200 and isinstance(data, list) and any(str(x.get("r:diaObjectId")) == oid for x in data):
        accepted.append(oid)
    if len(accepted) == 10:
        break
seal = {"rule": "recount_protocol_FROZEN.md section 3 S1-S2 + amendments.md AM1 (dedupe on oid)", "T0_mjd_tai": T0, "s1_source": used,
        "n_candidate_rows": len(rows), "examined_in_order": examined, "accepted_ids": accepted,
        "fink_object_responses": fink_hashes}
p = D / "sealed" / "alert_ids_SEALED_v2.json"
p.write_text(json.dumps(seal, indent=1))
p.chmod(0o444)
print("candidates", len(rows), "examined", len(examined), "accepted", len(accepted))
print("sealed sha256", hashlib.sha256(p.read_bytes()).hexdigest())
