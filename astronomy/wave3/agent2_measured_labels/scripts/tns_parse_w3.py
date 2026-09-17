"""Wave-3 parser: wave-2 tns_parse (unchanged logic, imported) plus per-report spectra count, AT-report internal names and discovery date."""
import re, html, gzip
from tns_parse_w2 import parse as parse_w2, cells, fieldset

def decompress_all(b):
    while b[:2] == b"\x1f\x8b":
        b = gzip.decompress(b)
    return b

def parse(t, name):
    p = parse_w2(t, name)
    cls = fieldset(t, "Classification Reports")
    spec_counts = {}
    if cls:
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", cls, flags=re.S):
            c = cells(row)
            if "time_received" in c:
                spec_counts[c.get("id")] = c.get("spectra")
    for r in p["reports"]:
        r["spectra_count_cell"] = spec_counts.get(r["id"])
    at = fieldset(t, "AT Reports")
    internal = set()
    if at:
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", at, flags=re.S):
            c = cells(row)
            if c.get("internal_name"): internal.add(c["internal_name"])
    p["internal_names"] = sorted(internal)
    dd = re.search(r'field-discoverydate">\s*<span class="name">[^<]*</span>\s*<div class="value">(.*?)</div>', t, flags=re.S)
    p["discovery_date"] = html.unescape(re.sub(r"<[^>]+>", "", dd.group(1))).strip() if dd else None
    return p

AUTO = [("SNIascore", re.compile(r"sniascore", re.I)), ("CCSNscore", re.compile(r"ccsnscore", re.I)),
        ("other-automated", re.compile(r"\b(bot|robot|automatic|automated|auto)\b", re.I)),
        ("SUSPECT-AUTOMATED", re.compile(r"syncatto", re.I))]
def marker(classifier):
    for m, rx in AUTO:
        if rx.search(classifier or ""): return m
    return None

def program(rep):
    g = (rep.get("group") or "").strip()
    if g: return g
    m = re.search(r"on behalf of (?:the )?([^(,]+)", rep.get("classifier") or "")
    return m.group(1).strip() if m else "UNATTRIBUTED"
