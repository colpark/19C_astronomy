#!/usr/bin/env python3
"""Find files that expose replay-case polarity. Prints paths, sha256, matched rule and a match count;
never prints a matched line. Run from anywhere; scans the repository root.

Rules
 R1 score listing   : a line  <case_id> <stage> must_fire|must_not_fire ok|FAIL   (replay.py score output)
 R2 polarity column : CSV whose header has a 'polarity' field
 R3 emit output     : 'polarity=must_'
 R4 id+polarity line: a case-id token and must_fire/must_not_fire (or pol. fire/not) on one line
 R5 verdict file    : JSON object whose values carry a boolean 'fired' (polarity-equivalent when the scored run was 100%)
 N1 filename        : score_*.txt, *POLARITY*, *polarity*, verdicts*.json, replay_cases.csv, cases.csv
"""
import os, re, json, hashlib, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SKIP_DIRS = {".git", "code", "sources", "data_cache", "__pycache__", "node_modules"}
IDS = r"(K\d\d|N\d\d|AST0\d|AST-P2-\d\d|AST\d-\d\d|ASTC-\d\d|W\dA\d-[A-Za-z0-9-]+|AST\d\d)"
R1 = re.compile(r"^\s*\S+\s+[A-Z]+\d?\s+must_(not_)?fire\s+(ok|FAIL)", re.M)
R3 = re.compile(r"polarity=must_")
R4 = re.compile(rf"\b{IDS}\b.*\b(must_(not_)?fire|must[- ]not[- ]fire|must[- ]fire)\b|\|\s*{IDS}\s*\|[^|\n]*\|\s*(fire|not)\s*\|", re.I)
NAME = re.compile(r"^(score_.*\.txt|.*polarity.*|verdicts.*\.json|replay_cases\.csv|cases\.csv|cases_blind\.csv|cases_opaque\.csv|blind_inputs.*\.csv|P2_controls_cases\.csv)$", re.I)
IGN = ("holder_handover", "scratch", "w3_")  # gitignored per .gitignore
SELF = os.path.abspath(__file__)
hits = []
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in SKIP_DIRS]
    for f in fn:
        if f == "RULINGS_SEALED.csv": continue  # never opened, not even by this script
        p = os.path.join(dp, f); rel = os.path.relpath(p, ROOT)
        if os.path.getsize(p) > 5_000_000 or not re.search(r"\.(txt|csv|md|json|log|py)$", f): continue
        if os.path.abspath(p) == SELF: continue
        try: s = open(p, encoding="utf-8").read()
        except Exception: continue
        rules = {}
        n = len(R1.findall(s));            rules["R1"] = n if n else None
        if f.endswith(".csv"):
            head = s.split("\n", 1)[0].lower().split(",")
            rules["R2"] = 1 if "polarity" in [x.strip() for x in head] else None
        n = len(R3.findall(s));            rules["R3"] = n if n else None
        n = sum(1 for line in s.splitlines() if R4.search(line)); rules["R4"] = n if n else None
        if f.endswith(".json"):
            try:
                o = json.loads(s)
                if isinstance(o, dict) and o and sum(isinstance(v, dict) and isinstance(v.get("fired"), bool) for v in o.values()) >= max(3, len(o) // 2):
                    rules["R5"] = sum(isinstance(v, dict) and "fired" in v for v in o.values())
            except Exception: pass
        rules = {k: v for k, v in rules.items() if v}
        if rules or (NAME.match(f) and "fm-advantage-benchmark/scripts" not in rel):
            hits.append({"path": rel, "sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(), "bytes": os.path.getsize(p),
                         "rules": rules, "name_match": bool(NAME.match(f)),
                         "gitignored_by_pattern": any(x in rel.split(os.sep) or rel.split(os.sep)[-2].startswith(x) for x in IGN) or "/scratch/" in rel or "/holder_handover/" in rel})
hits.sort(key=lambda h: h["path"])
json.dump(hits, sys.stdout, indent=1)
