#!/usr/bin/env python3
"""Counts behind issues 03 and 08. Prints aggregates only. Run from a skill copy root."""
import csv
cs = list(csv.DictReader(open("cases/cases.csv")))
S = lambda c: c["sealed"].strip().upper() == "Y"
nd = [c for c in cs if c["stage"][0] != "D"]; d = [c for c in cs if c["stage"][0] == "D"]
print("rows", len(cs), "sealed", sum(map(S, cs)), "dev", sum(not S(c) for c in cs))
print("non-discovery: total", len(nd), "dev", sum(not S(c) for c in nd), "sealed", sum(S(c) for c in nd))
print("discovery: dev", sum(not S(c) for c in d), "sealed", sum(S(c) for c in d))
print("discovery dev SYNTHETIC", sum("SYNTHETIC" in c["input"] for c in d if not S(c)), "discovery sealed SYNTHETIC", sum("SYNTHETIC" in c["input"] for c in d if S(c)))
rows = [l for l in open("references/graph.md") if l.startswith("| ") and not l.startswith("| From")]
st = {cell.strip().split()[0] for l in rows for cell in l.split("|")[1:3]}
print("graph.md edge rows", len(rows), "| distinct stages on an edge", len(st), sorted(st), "| stages with no edge", 29 - len(st))
