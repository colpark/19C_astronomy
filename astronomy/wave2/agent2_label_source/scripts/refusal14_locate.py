#!/usr/bin/env python3
"""Refusal 14 (definitions_FROZEN.md section 10): locate each flagged object's occurrences in seed text,
report +-3 line windows and a class-token scan. Output feeds refusal14_rulings.json (after reading windows)."""
import json, re
from pathlib import Path
from common import *

check_hashes()
A1 = ASTRO / "agent1_supply_corpus"
A3 = ASTRO / "agent3_labels_exposure"
ledger = json.load(open(A1 / "corpus_ledger.json"))["answer_in_own_source"]
raw, ext = load()
typ = dict(zip(raw.ZTFID, raw.type))
SEEDS = {
    "sources/1910.12973.raw.txt": A1 / "sources/1910.12973.raw.txt",
    "sources/2009.01242.raw.txt": A1 / "sources/2009.01242.raw.txt",
}
MY_SEEDS = {"2104.12980": A3 / "sources/2104.12980.raw.txt",
            "2401.15167": HERE / "sources/2401.15167.raw.txt",
            "2412.08601": HERE / "sources/2412.08601.raw.txt"}
CLASS_RE = re.compile(r"\b(SNe? ?I[abcIn]*(?:[- ](?:91T|91bg|pec|CSM|BL|norm|SC|Ca-rich|P|L|n|b))*|SLSN(?:-I{1,2})?|TDE|CV|AGN|nova|LBV|LRN|ILRT|Ca-rich|Iax|Ia-CSM|Ic-BL|IIn|IIb|Ibn|Icn|Type I[abcIn]*|other|Other)\b")


def patterns(z, iau):
    pats = [re.escape(z)]
    m = re.fullmatch(r"(SN|AT|TDE)?(\d{4})([a-z]+)", iau or "")
    if m:
        pats.append(r"(?:SN|AT)?\s?" + m.group(2) + m.group(3) + r"\b")
    return re.compile("|".join(pats))


def windows(lines, pat):
    out = []
    for i, l in enumerate(lines):
        if pat.search(l):
            w = lines[max(0, i - 3): i + 4]
            toks = sorted(set(CLASS_RE.findall(" ".join(w))))
            out.append(dict(line=i + 1, text=l.strip()[:200], window_class_tokens=toks))
    return out


res = []
cache = {k: Path(v).read_text(errors="replace").split("\n") for k, v in SEEDS.items()}
for it in ledger:
    z, iau, src = it["item"], it["iau"], it["label_in_text_of"]
    pat = patterns(z, iau)
    hits = {}
    for k, lines in cache.items():
        w = windows(lines, pat)
        if w:
            hits[k] = w
    res.append(dict(ZTFID=z, IAUID=iau, bts_type=typ.get(z), agent1_source=src, hits=hits))
extra = []
mycache = {k: Path(v).read_text(errors="replace").split("\n") for k, v in MY_SEEDS.items()}
for r in raw.itertuples():
    pat = patterns(r.ZTFID, r.IAUID)
    for k, lines in mycache.items():
        w = windows(lines, pat)
        if w:
            extra.append(dict(ZTFID=r.ZTFID, IAUID=r.IAUID, bts_type=r.type, seed=k, hits=w))
json.dump(dict(agent1_98=res, wave2_seeds=extra), open(HERE / "scripts/refusal14_locate.out.json", "w"), indent=1)
print(len(res), "agent1 objects;", len(extra), "hits in wave2 seeds")
print(sum(1 for r in res if not r["hits"]), "agent1 objects with zero re-located hits")
