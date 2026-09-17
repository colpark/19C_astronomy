#!/usr/bin/env python3
"""T9 enumeration: parse Rochester sn2026/index.html entries (name, internal names, discovery date, RA/Dec, type, section discoverer)."""
import re, html, json, pathlib, collections
D = pathlib.Path(__file__).resolve().parent.parent
import sys
src = sys.argv[1] if len(sys.argv) > 1 else "rochester_sn2026_index.html"
t = (D/"sources/census"/src).read_text(errors="replace")
secs = [(m.start(), html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))) for m in re.finditer(r"<ul><label>(.*?)</label>", t, flags=re.S)]
def sec_at(pos):
    s = None
    for p, lab in secs:
        if p < pos: s = lab
        else: break
    return re.sub(r"\s+", " ", s or "").strip()
rows = []
for m in re.finditer(r'<li id="(\d{4}[a-z]+)">(.*?)</li>', t, flags=re.S):
    body = m.group(2); txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
    ra = re.search(r"ra=([\d.\-]+)&de=([\d.\-]+)", body)
    disc = re.search(r"discovered (\d{4})/(\d{2})/(\d{2})\.(\d+)", txt)
    typ = re.search(r"Type ([^\s(,]+(?: [^\s(,]+)?)", txt)
    alias = re.findall(r"\(= ([^)]*)\)", txt)
    rows.append(dict(name=m.group(1), section=sec_at(m.start()), aliases=alias[0] if alias else "",
                     ra_deg=float(ra.group(1))*15 if ra else None, dec_deg=float(ra.group(2)) if ra else None,
                     discdate=f"{disc.group(1)}-{disc.group(2)}-{disc.group(3)}" if disc else None,
                     type=typ.group(1).strip() if typ else None, text=txt[:400]))
json.dump(rows, open(D/"out"/("rochester_entries_" + src.replace(".html", "") + ".json"), "w"))
c = collections.Counter(r["type"] for r in rows)
print(len(rows), "entries; typed:", sum(1 for r in rows if r["type"] and not r["type"].startswith("unknown")))
print(c.most_common(25))
print(collections.Counter(r["section"].split(" discovered by ")[-1][:40] for r in rows).most_common(30))
print([r for r in rows if "LSST" in r["aliases"] or "Rubin" in r["section"]][:3])
