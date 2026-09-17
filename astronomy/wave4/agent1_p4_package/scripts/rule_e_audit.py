#!/usr/bin/env python3
"""Rule E audit of p4_ruling_package.json: every kill-band comparison operand cites a cleared V record (or a literal);
controls: a V_PENDING number (U=0, no V id) must be refused by the gate; a cleared record (V-C01) must pass."""
import json, pathlib
D = pathlib.Path(__file__).resolve().parent.parent; W = D.parent
V = {r["id"]: r for r in json.load(open(W / "agent4_module_v/v_records.json"))}
P = json.load(open(D / "p4_ruling_package.json"))
def gate(vid):
    r = V.get(vid)
    return bool(r and r["cleared_for_P4_under_rule_E"] and r["verdict"] in ("MATCH", "MATCH_WITHIN_TOL"))
rows = []
for c in P["kill_band_comparisons"]:
    for side in ("lhs_v", "rhs_v"):
        v = c[side]; ok = (v == "literal") or gate(v)
        rows.append(dict(axis=c["axis"], delta=c["delta"], side=side, v=v, ok=ok))
controls = dict(must_fire=dict(input="U = 0 with v_record None (V_PENDING)", gate_accepts=gate(None), fired=not gate(None)),
                must_not_fire=dict(input="O = 1937669 with V-C01", gate_accepts=gate("V-C01"), fired=not gate("V-C01")))
res = dict(operands=len(rows), all_cited=all(r["ok"] for r in rows), failures=[r for r in rows if not r["ok"]], controls=controls,
           armed=controls["must_fire"]["fired"] and not controls["must_not_fire"]["fired"],
           pending_numbers_outside_comparisons=P["rule_E_leans"])
json.dump(res, open(D / "out/rule_E_audit.json", "w"), indent=1); print(json.dumps(res, indent=1))
