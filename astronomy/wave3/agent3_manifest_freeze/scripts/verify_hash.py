#!/usr/bin/env python3
"""Recompute a manifest's frozen_hash by the recorded method and compare."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import manifest_hash

rc = 0
for p in sys.argv[1:]:
    m = json.load(open(p))
    got = manifest_hash(m)
    stored = m.get("frozen_hash", "")
    ok = bool(stored) and got == stored
    print(f"{'MATCH' if ok else 'MISMATCH'} {p} stored={stored or '(empty)'} recomputed={got}")
    rc |= 0 if ok else 1
sys.exit(rc)
