#!/usr/bin/env python3
"""Minimal draft-07 subset validator (type, required, enum, properties, items,
minItems, minimum) for the decision_shape block of
fm-advantage-benchmark-with-shape/schemas/domain_manifest.schema.json.
jsonschema is not installed in the venv, so this implements only the keywords
the decision_shape subtree actually uses, and refuses on any other keyword.

    python check_shape_schema.py <schema.json> <shape_record.json>
"""
import json, sys
USED = {"type","required","enum","properties","items","minItems","minimum","description"}
TYPES = {"object":dict,"array":list,"string":str,"boolean":bool,"integer":int,"number":(int,float)}
def check(s, v, path, errs):
    for k in s:
        if k not in USED: errs.append(f"{path}: schema keyword {k!r} not supported by this checker"); return
    t = s.get("type")
    if t:
        ok = isinstance(v, TYPES[t]) and not (t in ("integer","number") and isinstance(v, bool))
        if not ok: errs.append(f"{path}: expected {t}, got {type(v).__name__}"); return
    if "enum" in s and v not in s["enum"]: errs.append(f"{path}: {v!r} not in enum {s['enum']}")
    if "minimum" in s and isinstance(v,(int,float)) and v < s["minimum"]: errs.append(f"{path}: {v} < minimum {s['minimum']}")
    if isinstance(v, dict):
        for r in s.get("required", []):
            if r not in v: errs.append(f"{path}: missing required {r!r}")
        for k, sub in s.get("properties", {}).items():
            if k in v: check(sub, v[k], f"{path}.{k}", errs)
    if isinstance(v, list):
        if "minItems" in s and len(v) < s["minItems"]: errs.append(f"{path}: {len(v)} items < minItems {s['minItems']}")
        if "items" in s:
            for i, x in enumerate(v): check(s["items"], x, f"{path}[{i}]", errs)
def main():
    schema = json.load(open(sys.argv[1])); rec = json.load(open(sys.argv[2]))
    sub = schema["properties"]["decision_shape"]
    target = rec["decision_shape"] if "decision_shape" in rec else rec
    errs = []; check(sub, target, "decision_shape", errs)
    # Control: the checker must fire on a known-bad copy (alternatives emptied, root invalid)
    bad = json.loads(json.dumps(target)); bad["value"]["alternatives_considered"] = []; bad["value"]["root"] = "select"
    ctrl = []; check(sub, bad, "control", ctrl)
    print("must_fire control:", "FIRED" if len(ctrl) >= 2 else "DID NOT FIRE", f"({len(ctrl)} findings)")
    for e in ctrl: print("  control -", e)
    print(("FAIL " if errs else "PASS ") + sys.argv[2])
    for e in errs: print("  -", e)
    return 1 if errs or len(ctrl) < 2 else 0
if __name__ == "__main__": raise SystemExit(main())
