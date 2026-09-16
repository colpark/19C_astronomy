#!/usr/bin/env python3
"""Derive P4 band thresholds from recorded wave-1 quantities only.
Inputs: astronomy/agent5_resolution_replay/planning_mde_bracket.csv (sha256 printed), k_slot.json, delta_slot.json.
Output: out/band_thresholds.json"""
import csv, json, hashlib, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
A5 = D.parent.parent / "agent5_resolution_replay"
f = A5 / "planning_mde_bracket.csv"
rows = list(csv.DictReader(open(f)))
out = {"bracket_file": str(f.relative_to(D.parent.parent.parent)), "bracket_sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
for fam, unit in (("A", "nights"), ("B", "objects")):
    r = [x for x in rows if x["family"] == fam]
    n = [int(x["N_min_at_delta_0.018"]) for x in r]
    out[fam] = {"unit": unit, "rows": len(r), "N_min_at_delta_0.018_min": min(n), "N_min_at_delta_0.018_max": max(n),
                "sigma_d_range": [min(float(x["sigma_d_realised_by_power_py"]) for x in r), max(float(x["sigma_d_realised_by_power_py"]) for x in r)],
                "chance": sorted({x["chance_k_over_candidates"] for x in r})}
for s in ("k_slot.json", "delta_slot.json"):
    p = A5 / s
    out[s] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
    j = json.loads(p.read_text())
    out[s]["value"] = j.get("value", j.get("proposed_value"))
json.dump(out, open(D / "out/band_thresholds.json", "w"), indent=1)
print(json.dumps(out, indent=1))
