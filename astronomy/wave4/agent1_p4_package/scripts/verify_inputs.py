#!/usr/bin/env python3
"""Independently recompute file sha256s and the v3 frozen_hash per its stated hash_method."""
import json, hashlib, pathlib
W = pathlib.Path(__file__).resolve().parent.parent.parent
A = W.parent
files = {"domain_manifest_v3.json": W / "agent3_freeze_v3/domain_manifest_v3.json", "axis_ledger_v3": W / "agent3_freeze_v3/axis_ledger_v3_against_frozen_bands.json",
         "v_records.json": W / "agent4_module_v/v_records.json", "truth_cost_monthly.json": W / "agent2_price_of_truth/truth_cost_monthly.json",
         "bands_FROZEN.md": A / "wave2/agent1_rubin_bands/bands_FROZEN.md", "PANEL_BRIEF_WAVE4.md": W / "PANEL_BRIEF_WAVE4.md"}
expect_prefix = {"domain_manifest_v3.json": ("0bdf229e", "3b6c"), "axis_ledger_v3": ("83e75757", "1a50"), "v_records.json": ("462286d6", "a9a"), "truth_cost_monthly.json": ("2f679148", "52bf"), "bands_FROZEN.md": ("8825ef80", "00d2")}
out = {}
for k, p in files.items():
    h = hashlib.sha256(p.read_bytes()).hexdigest(); e = expect_prefix.get(k)
    out[k] = dict(path=str(p.relative_to(A.parent)), sha256=h, matches_coordinator_prefix=(h.startswith(e[0]) and h.endswith(e[1])) if e else None)
m = json.loads(files["domain_manifest_v3.json"].read_text())
stored = m["frozen_hash"]; m2 = dict(m); m2["frozen_hash"] = ""
rec = hashlib.sha256(json.dumps(m2, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
out["frozen_hash"] = dict(stored=stored, recomputed=rec, match=(rec == stored), coordinator_prefix_match=(stored.startswith("bd0fa4c6") and stored.endswith("85bc")))
json.dump(out, open(pathlib.Path(__file__).resolve().parent.parent / "out/input_verification.json", "w"), indent=1)
print(json.dumps(out, indent=1))
