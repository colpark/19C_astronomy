#!/usr/bin/env python3
"""Tally FAIL stages and dispositions from the wave-3 tool coverage axis (read-only). Writes logs/tool_stage_tally.json."""
import json, hashlib, os
from collections import Counter, defaultdict
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
src = os.path.join(R, "astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json")
d = json.load(open(src)); pt = d["value"]["per_tool"]
out = {"source": "astronomy/wave3/agent4_tool_recount/tool_coverage_axis.json", "source_sha256": hashlib.sha256(open(src, "rb").read()).hexdigest(),
       "n_tools": len(pt),
       "group_sizes": dict(Counter(t["group"] for t in pt)),
       "fail_stage_counts": dict(Counter(t["stage"] for t in pt if t["disposition"] == "FAIL")),
       "fail_stage_by_group": {g: dict(Counter(t["stage"] for t in pt if t["disposition"] == "FAIL" and t["group"] == g)) for g in ("FM/deep", "classical")},
       "fail_stage_reclassified_tools": sorted(t["tool"] for t in pt if t.get("stage_reclassified")),
       "fail_tools_by_stage": {s: sorted(t["tool"] for t in pt if t["disposition"] == "FAIL" and t["stage"] == s) for s in {t.get("stage") for t in pt if t["disposition"] == "FAIL"}},
       "undemonstrated_tools": sorted(t["tool"] for t in pt if t["disposition"] == "UNDEMONSTRATED"),
       "pass_tools": sorted(t["tool"] for t in pt if t["disposition"] == "PASS")}
os.makedirs(os.path.join(os.path.dirname(__file__), "..", "logs"), exist_ok=True)
open(os.path.join(os.path.dirname(__file__), "..", "logs", "tool_stage_tally.json"), "w").write(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
