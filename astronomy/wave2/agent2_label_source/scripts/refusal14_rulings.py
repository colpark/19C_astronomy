#!/usr/bin/env python3
"""Refusal 14 rulings (definitions_FROZEN.md section 10). Class-in-text judgments below were made by reading
the +-3 line windows produced by refusal14_locate.py and the table/figure regions cited (line numbers = newline-split
line numbers of the raw pdftotext files, identical to sed -n / awk NR)."""
import json
from common import *

check_hashes()
loc = json.load(open(HERE / "scripts/refusal14_locate.out.json"))
S1 = "astronomy/agent1_supply_corpus/sources/1910.12973.raw.txt"
S2 = "astronomy/agent1_supply_corpus/sources/2009.01242.raw.txt"
S3 = "astronomy/agent3_labels_exposure/sources/2104.12980.raw.txt"
S4 = "astronomy/wave2/agent2_label_source/sources/2401.15167.raw.txt"
S5 = "astronomy/wave2/agent2_label_source/sources/2412.08601.raw.txt"
SEED_DATE = {S1: "2019-10-28 (arXiv v1)", S2: "2020-09-02 (arXiv v1)", S3: "2021-04-27 (arXiv v1)",
             S4: "2024-01-26 (arXiv v1)", S5: "2024-12-11 (arXiv v1)"}

# manual reading results: ZTFID -> (stated class or None, locator, partial_class_note)
T3 = "Table 3 Non-TNS classifications (lines 3178-3304): row order ZTF IDs lines 3189-3208/3273, IAU IDs 3210-3229/3275, Classification 3231-3250/3277, notes 3281-3302"
M = {
 # 1910.12973
 "ZTF18aayjyub": (None, f"{S1} line 1409 (host-position list, no class)", "IAU 'SN' prefix only"),
 "ZTF18abmrhom": ("SN Ia", f"{S1} lines 1014-1015 'We classify ZTF18abmrhom as a SN Ia'; 1028", None),
 "ZTF18aceqrrs": ("SN Ic-pec", f"{S1} lines 1160-1162 'peculiar SN Ic (Ic-pec in Table 1)'", None),
 "ZTF18acrknyn": (None, f"{S1} line 1410 (host-position list, no class)", "IAU 'SN' prefix only"),
 # 2009.01242 prose / tables
 "ZTF18abcfcoo": ("Other", f"{S2} lines 842-843 '“Other” transients are AT2018cow and AT2019cmw'; {T3} row 3 'other'", None),
 "ZTF19aaniqrr": ("Other", f"{S2} lines 842-843; {T3} row 7 'other'", None),
 "ZTF18actuhrs": ("SN Ia-CSM", f"{S2} {T3} row 4 'SN Ia-CSM' (lines 3192, 3213, 3234)", None),
 "ZTF18abukavn": ("Ic-BL", f"{S2} line 1411 'peculiar Type Ic-BL (SN2018gep'; line 1497 '2018gep (Ic−BL, z=0.032)'", None),
 "ZTF18adaykvg": ("SN Ic", f"{S2} lines 1400-1403 'Nominally spectroscopically classified as a SN Ic'; line 1507 '(Ic, z=0.053)'", None),
 "ZTF19aadnwvc": ("SN Ia", f"{S2} {T3} row 5 'SN Ia' (lines 3193, 3214, 3235)", None),
 "ZTF19aadyppr": ("ILRT", f"{S2} lines 1475-1476 'ILRT AT2019abn'", None),
 "ZTF19aailcgs": (None, f"{S2} lines 2189-2193 'two CC SN hosts (SN 2019ape and SN 2020oce'", "coarse class 'CC SN' stated; not in frozen token list"),
 "ZTF20abkiarz": (None, f"{S2} lines 2189-2193 'two CC SN hosts (SN 2019ape and SN 2020oce'", "coarse class 'CC SN' stated; not in frozen token list"),
 "ZTF19aatubsj": ("AGN (candidate; Classification 'none')", f"{S2} {T3} row 9 'none', note line 3289 'Possibly an AGN/NLSy1 based on late-time spectra'", None),
 "ZTF19aavxfib": ("TDE (candidate; Classification 'none')", f"{S2} {T3} row 11 'none', note line 3291 'TDE classification is uncertain'", None),
 "ZTF20abfhyil": ("CV (candidate; Classification 'none')", f"{S2} {T3} row 21 (lines 3273-3279) 'none', note lines 3301-3302 'featureless spectrum; probable CV'", None),
 "ZTF19aaznwze": ("Ca-rich", f"{S2} lines 1478-1481 'Among Ca-rich events ... in BTS, only SN 2019hty'", None),
 "ZTF19acdsqir": (None, f"{S2} {T3} row 12 '–' (retain TNS classification, note 1304), note 'Added redshift from NED'", "IAU 'SN' prefix only"),
 "ZTF19acnfsij": ("nova", f"{S2} {T3} row 13 'nova' (line 3243)", None),
 "ZTF19acoaiub": ("ILRT", f"{S2} {T3} row 14 'ILRT' (line 3244)", None),
 "ZTF19adakuos": ("nova", f"{S2} {T3} row 15 'nova' (line 3245)", None),
 "ZTF20aaertpj": ("SN Ib", f"{S2} {T3} row 16 'SN Ib' (line 3246)", None),
 "ZTF20aaeuxqk": (None, f"{S2} {T3} row 17 '–' (retain TNS classification), note 'Revised redshift'", "IAU 'SN' prefix only"),
 "ZTF20aapchqy": ("SN II (IIP-like)", f"{S2} lines 1450-1454 'SN2020cxd ... SN IIP-like light curve ... other Type II SNe'", None),
 # wave-2 seeds
 "ZTF18aaxmhvk": ("SN Ic (official BTS) / SN Ia-like", f"{S3} lines 812-824 'the BTS officially classified this as a SN Ic'", None),
 "ZTF21aastazz": ("SN Ia", f"{S3} lines 876-878 'first fully automated SEDM SN Ia classification was sent for SN 2021ijb'", None),
 "ZTF23abbccir": ("SN IIL", f"{S5} line 806 'SN 2023rky – a Type IIL'", None),
 "ZTF18aaunfqq": (None, f"{S4} line 1189 (Figure 8 'Typical true positive' panel label)", "'true positive' = bright transient, no class"),
 "ZTF21acjvgxg": (None, f"{S4} line 1184 (Figure 8 'Typical bts_p1 false positive')", "no class"),
 "ZTF20acjlkpe": (None, f"{S4} line 422 (Figure 2 caption, light-curve example)", "no class"),
 "ZTF23aaxtplp": (None, f"{S4} line 1505 (FN with bright host; AGN/CV tokens in window refer to other sources)", "no class"),
 "ZTF23abeuope": (None, f"{S4} lines 1506-1508 ('projected very near to the supernova')", "generic 'supernova'"),
}
for z in ["ZTF23abijnsm", "ZTF18aafdigb", "ZTF23abjexnw", "ZTF23abjzkqu", "ZTF23abjxqwr", "ZTF23ablpfnb",
          "ZTF23abkkajk", "ZTF23abnydbs", "ZTF18aaeqjmc"]:
    M[z] = ("SN Ia (Type Ia, classified by SNIascore)", f"{S4} lines 1583-1591 'more than a dozen additional Type Ia SNe ... classified by SNIascore: ...'", None)


def grid_class(hits, iau):
    import re
    name = re.sub(r"^(SN|AT)", "", iau)
    for k, ws in hits.items():
        for w in ws:
            m = re.search(re.escape(name) + r" \(([^,]+), z=", w["text"])
            if m:
                return m.group(1), f"{S2} line {w['line']} '{w['text'][:60]}' (Figure 7/8 panel label)"
    return None


raw, _ = load()
typ = dict(zip(raw.ZTFID, raw.type))
rulings = []


def rule(z, iau, bts_type, stated, locator, note, flagged_by):
    if stated:
        seed = locator.split(" ")[0]
        r = "REFUSE"
        basis = (f"refusal 14: class stated in seed text; exposure key places the seed ({SEED_DATE.get(seed, 'pre-2025')}) "
                 "before every demonstrated subject cutoff (earliest 2025-02-01), so the exception cannot apply")
    else:
        r = "NOT_FIRED_NAME_ONLY"
        basis = ("refusal 14 does not fire on the class (name occurs, no class token in the reading window); admissible for "
                 "CALIBRATION ONLY under written exposure ruling ER-W2-A2-01 (IAU name withheld, seed text withheld from every arm, "
                 "contamination FAIL disclosed)")
    rulings.append(dict(ZTFID=z, IAUID=iau, bts_type=bts_type, flagged_by=flagged_by, ruling=r,
                        class_stated_in_text=stated, stated_vs_bts_type_agree=None if not stated else None,
                        locator=locator, note=note, rule_basis=basis, use_scope="calibration only (addition B); no scored subject comparison"))


for r in loc["agent1_98"]:
    z = r["ZTFID"]
    if z in M:
        st, lc, nt = M[z]
    else:
        g = grid_class(r["hits"], r["IAUID"])
        assert g, z
        st, lc = g; nt = None
    rule(z, r["IAUID"], r["bts_type"], st, lc, nt, "agent1 corpus_ledger.answer_in_own_source")
seen = {x["ZTFID"] for x in rulings}
for r in loc["wave2_seeds"]:
    if r["ZTFID"] in seen:
        continue
    st, lc, nt = M[r["ZTFID"]]
    rule(r["ZTFID"], r["IAUID"], r["bts_type"], st, lc, nt, f"wave2 agent2 seed {r['seed']}")
    seen.add(r["ZTFID"])

# agreement between stated class and BTS type (listed, not reconciled)
def agree(stated, bts):
    if not stated: return None
    s = stated.lower().replace("−", "-").replace("type ", "").replace("sn ", "").split(" (")[0].split(" ")[0]
    b = (bts or "").lower().replace("sn ", "")
    if b in ("", "-"):
        return False
    return s == b or s.startswith(b + "-") or b.startswith(s + "-") or (s, b) in {("other", "other"), ("iip-like", "ii")}
for x in rulings:
    x["stated_vs_bts_type_agree"] = agree(x["class_stated_in_text"], x["bts_type"])

a1 = [x for x in rulings if x["flagged_by"].startswith("agent1")]
out = dict(
    stage="D2 refusal 14 (feeding D4 label_source / calibration admissibility)",
    definitions_sha256=DEFS_SHA,
    scope_statement="BTS is calibration only (addition B: contamination FAIL). Every ruling here governs calibration use only; none admits a BTS item to a scored subject comparison.",
    exposure_ruling_ER_W2_A2_01=("Written 2026-09-16 by agent2 (wave 2). Items ruled NOT_FIRED_NAME_ONLY may be used as calibration items for mechanical "
                                 "compositions and harness controls if (1) the IAU designation and ZTF ID are replaced by a neutral ID, (2) no seed text is placed in any arm's context, "
                                 "(3) the item carries 'calibration only, contamination FAIL on this cohort'. It does NOT place any source after any subject cutoff; "
                                 "every seed is pre-cutoff, so no item here is admissible to a scored subject comparison."),
    counts=dict(
        agent1_flagged=len(a1),
        agent1_REFUSE=sum(x["ruling"] == "REFUSE" for x in a1),
        agent1_NOT_FIRED_NAME_ONLY=sum(x["ruling"] == "NOT_FIRED_NAME_ONLY" for x in a1),
        agent1_NOT_FIRED_FALSE_MATCH=sum(x["ruling"] == "NOT_FIRED_FALSE_MATCH" for x in a1),
        agent1_unlabeled_in_bts=sum(x["bts_type"] == "-" for x in a1),
        wave2_additional=len(rulings) - len(a1),
        wave2_additional_REFUSE=sum(x["ruling"] == "REFUSE" for x in rulings[len(a1):]),
        stated_class_disagrees_with_bts_type=[{k: x[k] for k in ("ZTFID", "IAUID", "bts_type", "class_stated_in_text")}
                                              for x in rulings if x["stated_vs_bts_type_agree"] is False],
        partial_class_flags=[{k: x[k] for k in ("ZTFID", "IAUID", "note")} for x in rulings if x["note"] and "coarse" in x["note"]],
    ),
    rulings=rulings,
)
json.dump(out, open(HERE / "refusal14_rulings.json", "w"), indent=1)
print(json.dumps(out["counts"], indent=1))
