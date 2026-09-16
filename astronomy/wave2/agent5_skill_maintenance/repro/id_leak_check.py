#!/usr/bin/env python3
"""Does the case_id prefix determine polarity? Prints only aggregate booleans and counts,
never a per-case polarity. Usage: id_leak_check.py <cases.csv>"""
import csv, sys, re
from collections import defaultdict
rows = list(csv.DictReader(open(sys.argv[1], newline="")))
by = defaultdict(set)
for r in rows:
    by[re.match(r"[A-Za-z]+", r["case_id"]).group(0)].add(r["polarity"])
print(f"{sys.argv[1]}: {len(rows)} rows, {len(by)} alphabetic id prefixes")
print(f"  every prefix maps to a single polarity: {all(len(v) == 1 for v in by.values())}")
print(f"  prefixes that each map to one polarity: {sorted(k for k, v in by.items() if len(v) == 1)} ; mixed: {sorted(k for k, v in by.items() if len(v) > 1)}")
