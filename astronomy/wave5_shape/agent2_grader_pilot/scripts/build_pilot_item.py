"""Build item/ and grader_private/ for the sealed pilot object. PRE-RATIFICATION PILOT (harness check only)."""
import json, os, sys
import numpy as np
AGENT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot"
sys.path.insert(0, os.path.join(AGENT, "scripts"))
from item_builder import check_protocol, sha256, split, write_item, counts, ispos  # noqa
from dustmaps.config import config
config["data_dir"] = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave2/agent4_instrument/data_cache/dustmaps"
from dustmaps.sfd import SFDQuery
from astropy.coordinates import SkyCoord
import astropy.units as u

check_protocol()
seal_p = os.path.join(AGENT, "selection", "selection_SEALED.json")
assert sha256(seal_p) == open(seal_p.replace(".json", ".sha256")).read().split()[0]
oid = json.load(open(seal_p))["selected_ZTFID"]
raw = os.path.join(AGENT, "data_cache", "alerce_raw", oid + ".json")
lc = json.load(open(raw))
sp = split(lc)
pos = [r for r in lc["detections"] if r["fid"] in (1, 2) and ispos(r.get("isdiffpos"))]
ra = float(np.mean([r["ra"] for r in pos])); dec = float(np.mean([r["dec"] for r in pos]))
ebv = float(SFDQuery()(SkyCoord(ra * u.deg, dec * u.deg)))
dust_files = {f: sha256(os.path.join(config["data_dir"], "sfd", f)) for f in ("SFD_dust_4096_ngp.fits", "SFD_dust_4096_sgp.fits")}
ident = {"item_id": "PILOT-001", "ZTFID": oid, "raw_sha256": sha256(raw), "ra_mean_pos_det": ra, "dec_mean_pos_det": dec,
         "mwebv_sfd": ebv, "sfd_files_sha256": dust_files, "counts": counts(sp)}
h = write_item(sp, "PILOT-001", ebv, os.path.join(AGENT, "item"), os.path.join(AGENT, "grader_private"), private_extra=ident)
h[os.path.join(AGENT, "grader_private", "identity.json")] = sha256(os.path.join(AGENT, "grader_private", "identity.json"))
lines = [f"{v}  {os.path.relpath(k, AGENT)}" for k, v in h.items()]
open(os.path.join(AGENT, "item", "ITEM_SHA256SUMS"), "w").write("\n".join(l for l in lines if " item/" in l) + "\n")
open(os.path.join(AGENT, "grader_private", "PRIVATE_SHA256SUMS"), "w").write("\n".join(l for l in lines if "grader_private/" in l) + "\n")
print(json.dumps(ident, indent=1)); print("\n".join(lines))
