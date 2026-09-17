"""Shared paths, hash checks and rules for agent2 wave2 label-source work.

Rules implement definitions_FROZEN.md (sha256 checked on import)."""
import hashlib, html, json, re, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent.parent
ASTRO = HERE.parent.parent
RAW = ASTRO / "data/raw/ztf_bts_all_2026-09-16.csv"
RAW_SHA = "61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
EXTRA = ASTRO / "agent3_labels_exposure/sources/bts_all_extracols_2026-09-16.csv"
EXTRA_SHA = "7c08daf489bbf648cb798ceba9f5ecbf56abc9f94dc6b2e320f5aaa84ad35b63"
DEFS = HERE / "definitions_FROZEN.md"
DEFS_SHA = "4f89ff6718a14ad4e45a6d33d6bde848448ba6a66d895bd970330efe397b37cf"
CAP2021 = HERE / "sources/bts_explorer_captures/wayback_bts_explorer_20210128125321.html"
CAP2021_SHA = "30dbb78bd2d6379e3f3e5355ccd3eb50517e3bc2d597c396d46187f704dd47f1"
CAPDIR = HERE / "sources/tns_captures"

DEPLOY_PEAKT = 2459319.5 - 2458000  # 2021-04-15 00:00 UTC as JD-2458000 = 1319.5
E5_CUT = DEPLOY_PEAKT - 30           # wave-1 phase rule (WEAK)
WAVE1_UPPER = 3131

# E2: papers read in full naming SNIascore-classified objects
E2_NAMED = {
    "SN2021ijb": "arXiv:2104.12980 sec 7, sources/2104.12980.raw.txt lines 876-878",
}
for n in ["2023tyk", "2023vcz", "2023uxa", "2023uti", "2023vcx", "2023uty", "2023vtp", "2023vpd",
          "2023vip", "2023vwz", "2023wts", "2023xms", "2023xhc", "2023xkq"]:
    E2_NAMED["SN" + n] = "arXiv:2401.15167 sec 5.1, sources/2401.15167.raw.txt (non-empty-line numbering) lines 1318-1329"

CC_CLASSES = {"SN II", "SN IIP", "SN IIb", "SN IIn", "SN Ib", "SN Ic", "SN Ic-BL", "SN Ib/c"}
CCSN_DISC_CUT = pd.Timestamp("2025-02-09")


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check_hashes():
    for p, h in [(DEFS, DEFS_SHA), (RAW, RAW_SHA), (EXTRA, EXTRA_SHA), (CAP2021, CAP2021_SHA)]:
        got = sha256(p)
        if got != h:
            sys.exit(f"ABORT: sha256 mismatch for {p}: {got} != {h}")


def load():
    raw = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    ext = pd.read_csv(EXTRA, dtype=str, keep_default_na=False)
    ext = ext.rename(columns={c: c.strip() for c in ext.columns})
    return raw, ext


def parse_explorer_capture(path):
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    out = {}
    for row in re.findall(r"<tr>\s*(<td>.*?)</tr>", t, flags=re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ").strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)]
        if len(cells) >= 15 and re.fullmatch(r"ZTF\d\d[a-z]{7}", cells[0]):
            out[cells[0]] = cells[11]
    return out


# ---- section 3: automated markers (Classifier/s field only)
def automated_marker(classifier):
    c = classifier or ""
    if re.search(r"sniascore", c, re.I):
        return "SNIascore"
    if re.search(r"ccsnscore", c, re.I):
        return "CCSNscore"
    if re.search(r"\b(bot|robot|automatic|automated|auto)\b", c, re.I):
        return "other-automated"
    return None


# ---- section 4: class match
def _norm(s):
    s = re.sub(r"\s+", " ", (s or "").strip().lower())
    s = re.sub(r"-like$", "", s)
    return s


PAIRS = {("sn ii", "sn iip"), ("sn ii", "sn iil"), ("sn iip", "sn ii"), ("sn ib/c", "sn ibc")}


def class_match(bts, tns):
    b, t = _norm(bts), _norm(tns)
    return b == t or t.startswith(b + "-") or (b, t) in PAIRS


def iau_to_tns(iau):
    m = re.fullmatch(r"(?:SN|AT|TDE)?\s?(\d{4}[a-z]{1,4})", iau)
    return m.group(1) if m else None
