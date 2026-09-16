#!/usr/bin/env python3
"""Run the skill validator's provenance check on each manifest slot record and on the contamination axis record.
The slot files are single-slot records, not a full domain_manifest, so ledger mode is also run on a two-slot stub
to show which manifest-level checks fail because other slots belong to other agents."""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
SK = HERE.parent.parent / "fm-advantage-benchmark/scripts"
sys.path.insert(0, str(SK))
import validate as V
worst = 0
for name in ["label_source_slot.json", "exposure_key_slot.json", "contamination_axis.json"]:
    o = json.loads((HERE / name).read_text()); f = []
    V.prov(o["provenance"], f, name)
    if V.ASSUMED.search(str(o["provenance"].get("source", ""))): f.append("source reads assumed/conventional")
    if o.get("status", o.get("disposition")) not in ("DERIVED", "UNDEMONSTRATED", "RATIFIED", "OVERRIDDEN", "PASS", "FAIL"):
        f.append("status/disposition not in the allowed set")
    print(("FAIL " if f else "PASS ") + name); [print("  -", x) for x in f]; worst |= bool(f)
stub = {"label_source": json.loads((HERE / "label_source_slot.json").read_text()),
        "exposure_key": json.loads((HERE / "exposure_key_slot.json").read_text())}
(HERE / "scripts/_manifest_stub_domain_manifest.json").write_text(json.dumps(stub))
r = subprocess.run([sys.executable, str(SK / "validate.py"), "ledger", str(HERE / "scripts/_manifest_stub_domain_manifest.json"), "--kind", "domain_manifest"], capture_output=True, text=True)
print("stub domain_manifest (expected to fail on slots owned by other agents):"); print(r.stdout)
r = subprocess.run([sys.executable, str(SK / "validate.py"), "provenance", str(HERE / "provenance_records.json")], capture_output=True, text=True)
print(r.stdout); worst |= r.returncode
sys.exit(worst)
