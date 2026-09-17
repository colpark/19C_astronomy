#!/usr/bin/env python3
"""Track one: apply wave-2 frozen rules (definitions_FROZEN.md sec 2-6, imported read-only) to the new captures; tighten only."""
import json, gzip, sys, pathlib, collections
D = pathlib.Path(__file__).resolve().parent.parent
W2 = D.parents[1] / "wave2/agent2_label_source"
sys.path.insert(0, str(W2/"scripts"))
from common import automated_marker, class_match
from tns_parse import parse
det = {}
import csv
for r in csv.DictReader(open(W2/"label_basis_per_object_detail.csv")): det[r["ZTFID"]] = r
seal = {o["ZTFID"]: o for o in json.load(open(W2/"sealed_fileonly_placement.json"))["objects"]}
newL = []; newExcl = []; cats = collections.Counter(); stat = collections.Counter(); mism = 0
for l in open(D/"out/track1_captures/fetch_log.jsonl"):
    r = json.loads(l); stat[r["final"]] += 1
    if r["final"] != "ok": continue
    o = seal[r["ZTFID"]]
    b = gzip.decompress((D/r["file"]).read_bytes())
    while b[:2] == b"\x1f\x8b": b = gzip.decompress(b)
    p = parse(b.decode("utf-8", errors="replace"), o["tns_name"])
    if not p["valid"] or not p["reports"]: continue
    last = sorted(p["reports"], key=lambda x: x["time"] or "")[-1]
    if not class_match(o["type"], last["classification"]): mism += 1; continue
    mk = automated_marker(last["classifier"])
    prev = det[r["ZTFID"]]
    if o["type"] != "SN Ia": continue
    if mk == "SNIascore":
        if not (prev["category"] == "MODEL_ANNOTATION" and prev["model"] == "SNIascore"): newL.append(r["ZTFID"])
    else:
        spec_before = [s for s in p["spectra"] if (s["obsdate"] or "9999") <= (last["time"] or "")]
        cats["MODEL_ANNOTATION:" + mk if mk else ("PHOTOMETRIC_ONLY" if not spec_before else "MEASURED")] += 1
        if not (o["E4"] or o["E5"]):  # MEASURED, PHOTOMETRIC_ONLY or other model all exclude from U
            newExcl.append(r["ZTFID"])
L2, U2 = 803 + len(newL), 2247 - len(newExcl)
res = dict(fetch_status=dict(stat), class_mismatch=mism, new_sniascore_strong=len(newL), new_upper_exclusions=len(newExcl),
           wave2_bound=[803, 2247], new_bound=[max(803, L2), min(2247, U2)], rule="L' = 803 + new E1 SNIascore placements; U' = 2247 - new E1 non-SNIascore placements among plain SN Ia not already excluded by E4/E5; never widened",
           new_categories_non_sniascore=dict(cats), new_L_ids=newL, new_excl_ids=newExcl)
json.dump(res, open(D/"out/track1_bound.json", "w"), indent=1); print({k: v for k, v in res.items() if not k.endswith("_ids")})
