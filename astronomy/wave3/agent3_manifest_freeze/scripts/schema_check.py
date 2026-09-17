#!/usr/bin/env python3
"""Minimal draft-07 check of a manifest against fm-advantage-benchmark/schemas/domain_manifest.schema.json
(jsonschema is not installed in the venv). Checks: top-level required keys; for every property with
required/enum/type in the schema, those constraints; extra slot decision_epoch checked with the slot shape."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import rp
S = json.load(open(rp("fm-advantage-benchmark/schemas/domain_manifest.schema.json")))
TYPES = {"object": dict, "string": str, "array": list}
def chk(v, sch, path, f):
    t = sch.get("type")
    if t and not isinstance(v, TYPES[t]): f.append(f"{path}: type {type(v).__name__} != {t}"); return
    if "enum" in sch and v not in sch["enum"]: f.append(f"{path}: {v!r} not in enum")
    for r in sch.get("required", []):
        if not isinstance(v, dict) or r not in v: f.append(f"{path}: missing required {r}")
    if isinstance(v, dict):
        for k, sub in sch.get("properties", {}).items():
            if k in v: chk(v[k], sub, f"{path}.{k}", f)
rc = 0
for p in sys.argv[1:]:
    m = json.load(open(p)); f = []
    chk(m, S, "$", f)
    if "decision_epoch" in m: chk(m["decision_epoch"], S["properties"]["tau"], "$.decision_epoch", f)
    print(("FAIL " if f else "PASS ") + p); [print("  -", x) for x in f]; rc |= bool(f)
sys.exit(rc)
