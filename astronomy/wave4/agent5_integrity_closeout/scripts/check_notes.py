#!/usr/bin/env python3
"""Checker for the community-note drafts.

Flags
  NO_LOCATOR          a claim sentence (or table row) with no [loc: ...]
  BAD_LOCATOR         a locator whose file, line range or JSON field does not resolve
  NUMBER_NOT_AT_LOC   a number in the sentence that does not occur in the text its locators resolve to
  DIRECTIONAL         a comparative / directional benchmark phrase, anywhere in the file (headings and non-claim blocks included)
  MISSING_BANNER      the DRAFT banner line is absent

Locator syntax (repo-relative paths):
  [loc: path:L12]  [loc: path:L12-L15]  [loc: path#json.path[3].key[tool=CATS]]
Exempt from NO_LOCATOR / NUMBER checks (never from DIRECTIONAL): headings, fenced code, table header rows and
separators, and lines between <!-- nonclaim --> and <!-- /nonclaim -->. [V: ...] markers are ignored for numbers.

usage: check_notes.py note.md [note.md ...]   exit 0 if no flags, 1 otherwise
"""
import json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
BANNER = "DRAFT – PI REVIEW – NOT FOR DISTRIBUTION"
LOC = re.compile(r"\[loc:\s*((?:[^\[\]]|\[[^\[\]]*\])+)\]")
VMARK = re.compile(r"\[V:[^\]]*\]")
NUM = re.compile(r"\d+(?:\.\d+)?")
DIRECTIONAL = re.compile(
    r"\b(better|worse|outperform\w*|underperform\w*|beats?|beaten|superior|inferior|stronger|weaker|"
    r"more accurate|less accurate|advantage\w*|disadvantage\w*|wins?|winning|loses?|losing|improv\w*|degrad\w*|"
    r"helps?|helped|hurts?|surpass\w*|exceed\w*|dominat\w*|edge over|ahead of|falls? behind|lags?|"
    r"best|worst|than|versus|vs\.?|compared (to|with)|relative to|headroom|gain over|FM helps|FM does not help)\b", re.I)

def json_get(obj, path):
    for part in re.findall(r"\[[^\]]*\]|[^.\[\]]+", path):
        if part.startswith("["):
            inner = part[1:-1]
            if "=" in inner:
                k, v = inner.split("=", 1)
                obj = next(x for x in obj if str(x.get(k)) == v)
            else:
                obj = obj[int(inner)]
        else:
            obj = obj[part]
    return obj

def resolve(loc):
    loc = loc.strip()
    m = re.match(r"^(.+?):L(\d+)(?:-L(\d+))?$", loc)
    if m:
        p = os.path.join(ROOT, m.group(1)); a = int(m.group(2)); b = int(m.group(3) or a)
        lines = open(p, encoding="utf-8").read().split("\n")
        if not (1 <= a <= b <= len(lines)): raise ValueError(f"line range {a}-{b} outside 1-{len(lines)}")
        return "\n".join(lines[a - 1:b])
    if "#" in loc:
        f, path = loc.split("#", 1)
        v = json_get(json.load(open(os.path.join(ROOT, f), encoding="utf-8")), path)
        last = re.findall(r"[^.\[\]]+", path)[-1]
        return last + " " + (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
    p = os.path.join(ROOT, loc)
    if not os.path.isfile(p): raise ValueError("file not found")
    return open(p, encoding="utf-8").read()

def nums(s):
    return set(NUM.findall(re.sub(r"(?<=\d),(?=\d{3})", "", s)))

def sentences(line):
    body = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", line)
    parts, buf, depth = [], "", 0
    for i, ch in enumerate(body):
        buf += ch
        if ch == "[": depth += 1
        elif ch == "]": depth = max(0, depth - 1)
        if depth == 0 and ch in ".;" and (i + 1 == len(body) or body[i + 1] == " ") and not re.search(r"(e\.g|i\.e|et al|approx|vs|No|no)\.$", buf):
            parts.append(buf.strip()); buf = ""
    if buf.strip(): parts.append(buf.strip())
    return [p for p in parts if re.search(r"[A-Za-z0-9]", p)]

def check(path):
    text = open(path, encoding="utf-8").read(); flags = []; units = 0
    if BANNER not in text: flags.append(("MISSING_BANNER", 0, ""))
    lines = text.split("\n"); in_code = in_nc = False; prev_table = False
    for n, line in enumerate(lines, 1):
        s = line.strip()
        for m in DIRECTIONAL.finditer(LOC.sub("", line)):
            flags.append(("DIRECTIONAL", n, m.group(0)))
        if s.startswith("```"): in_code = not in_code; continue
        if "<!-- nonclaim -->" in s: in_nc = True; continue
        if "<!-- /nonclaim -->" in s: in_nc = False; continue
        if in_code or in_nc or not s or s.startswith("#") or s.startswith("<!--"): prev_table = False; continue
        if s.startswith("|"):
            if re.match(r"^\|[\s:|-]+\|$", s): prev_table = True; continue
            if not prev_table: prev_table = True; continue      # header row
            unit_list = [s]
        else:
            prev_table = False; unit_list = sentences(s)
        for u in unit_list:
            units += 1
            locs = LOC.findall(u)
            if not locs: flags.append(("NO_LOCATOR", n, u[:120])); continue
            texts = []
            for l in locs:
                try: texts.append(resolve(l))
                except Exception as e: flags.append(("BAD_LOCATOR", n, f"{l}: {type(e).__name__} {e}"))
            if not texts: continue
            have = set().union(*(nums(t) for t in texts))
            bare = VMARK.sub("", LOC.sub("", u))
            for x in sorted(nums(bare) - have):
                flags.append(("NUMBER_NOT_AT_LOC", n, f"{x} in: {bare[:100]}"))
    return units, flags

rc = 0
for p in sys.argv[1:]:
    units, flags = check(p)
    print(f"== {os.path.relpath(p)}: {units} claim units checked, {len(flags)} flag(s)")
    for f in flags: print(f"  {f[0]:<18} line {f[1]}: {f[2]}")
    rc |= 1 if flags else 0
print("RESULT:", "PASS (no flags)" if rc == 0 else "FAIL (flags above)")
sys.exit(rc)
