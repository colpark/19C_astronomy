#!/usr/bin/env python3
"""Write label_source_slot.json and provenance_records.json from split_summary.json and refusal14_rulings.json,
then run the skill validator."""
import json, subprocess, sys
from common import *

check_hashes()
S = json.load(open(HERE / "split_summary.json"))
R = json.load(open(HERE / "refusal14_rulings.json"))
b, cc = S["sniascore_bound"], S["ccsnscore_bound"]
cats = S["category_counts"]
N = S["population_labeled"]
fs = S["fetch_status"]
SPLIT = "astronomy/wave2/agent2_label_source/scripts/split_labels.py"
SEAL = "astronomy/wave2/agent2_label_source/sealed_fileonly_placement.json sha256 " + S["seal_sha256"]
DEFS = "astronomy/wave2/agent2_label_source/definitions_FROZEN.md sha256 " + DEFS_SHA
RAWS = "astronomy/data/raw/ztf_bts_all_2026-09-16.csv sha256 " + RAW_SHA
CAPS = "Internet Archive captures of https://www.wis-tns.org/object/<name> via web/20260916id_/ (sources/tns_captures/fetch_log.jsonl, per-page sha256)"
CAL = "calibration only, contamination FAIL on this cohort"
POP = f"{N} BTS rows with type != '-' (unique ZTFID, pre-clustering; Agent 1 owns clustering; 13 IAU names shared by 2 ZTFIDs)"


def c(k):
    return int(cats.get(k, 0))


slot = dict(
    slot="label_source",
    candidate="live time-domain astronomy (Rubin LSST alerts + ZTF BTS labels)",
    banner=CAL,
    supersedes=dict(file="astronomy/agent3_labels_exposure/label_source_slot.json", sha256="09e8dff5ac6f246629feb77c6689b4b0d443ef1595f8dcf2553d08e3ad28bc82",
                    what_changes="SNIascore bound tightened; per-object measured/annotation/photometric/unresolved split added from public archived TNS pages; CCSNscore channel added; class-level basis shares of wave 1 carried unchanged (not recounted)"),
    status="UNDEMONSTRATED",
    status_reason=("Per-object split is DERIVED only where public archived TNS evidence exists; "
                   f"{c('UNRESOLVED (UNDEMONSTRATED)')} of {N} labels remain UNRESOLVED, so the measured-vs-annotation share of the whole base is bounded, not determined. "
                   "No TNS credentials were supplied (SUPPLY field empty). The SNIascore bound itself is DERIVED."),
    value=dict(
        population=N,
        category_counts=dict(MEASURED=c("MEASURED"), MODEL_ANNOTATION=c("MODEL_ANNOTATION"), PHOTOMETRIC_ONLY=c("PHOTOMETRIC_ONLY"),
                             UNRESOLVED_UNDEMONSTRATED=c("UNRESOLVED (UNDEMONSTRATED)")),
        category_by_strength=S["category_by_strength"],
        model_annotation_by_model=S["model_annotation_by_model"],
        photometric_only_by_class=S["photometric_only_by_class"],
        sniascore_bound=dict(status="DERIVED", lower=b["lower"], upper=b["upper"], wave1=[0, 3131],
                             lower_rule="E1 archived TNS report with 'SNIascore' in Classifier/s as latest matching report (STRONG, n=%d) plus E2 paper-named objects still typed SN Ia with no contradicting E1 (MODERATE)" % b["lower_strong_only"],
                             upper_rule="plain 'SN Ia' minus E1 non-SNIascore placement, minus E4 (SN Ia in 2021-01-28 BTS explorer capture), minus E5 (wave-1 phase rule, WEAK); min with wave-1 3131",
                             upper_noE5_sensitivity_not_slot_value=b["upper_noE5_sensitivity_not_slot_value"],
                             excluded_by=b["excluded_by"], within_upper_fetch_status=b["within_upper_E1_status"]),
        ccsnscore_bound=dict(status="UNDEMONSTRATED (start date unknown)", **cc),
        fetch_status=fs,
        refusal14=R["counts"],
        wave1_class_level_shares_carried="see superseded file value.bts_shares (6867 spectroscopic transient classes, 310 with photometric criterion, 561 AGN/CV unresolved, 105 tentative); not recounted",
        rubin_era="unchanged from wave 1: broker classifications are annotation; TNS classifications count as measured only after the Classifier/s field is checked for an automated classifier (SNIascore, CCSNscore, bot markers)",
    ),
    provenance=dict(
        referent="basis of each BTS object's current type label: human spectroscopic classification (MEASURED) vs automated-classifier TNS report (MODEL_ANNOTATION) vs report without prior public spectrum (PHOTOMETRIC_ONLY) vs no admissible evidence (UNRESOLVED); and the number of plain 'SN Ia' labels that are SNIascore annotation",
        source=f"{SPLIT}::main (bounds block); {DEFS}; {SEAL}; {RAWS}; {CAPS}; arXiv:2104.12980 sec 3 lines 413-415, sec 7 lines 869-886; arXiv:2401.15167 sec 5.1 raw lines 1580-1591; arXiv:2412.08601 sec 6 lines 1089-1091",
        population=POP,
        adjudicator="authenticated TNS classification reports for every object (TNS API or bulk CSV with a bot/user account), which would replace every archived-capture placement and every UNRESOLVED; not reachable without credentials (HTTP 403 on all wis-tns.org paths 2026-09-16)",
        falsifier=(f"an authenticated TNS report list showing more than {b['upper']} or fewer than {b['lower']} BTS 'SN Ia' labels whose latest classification report is SNIascore; "
                   "or a later human re-report superseding an archived SNIascore report; or a rerun of split_labels.py on the same seal and captures returning different counts"),
    ),
)
json.dump(slot, open(HERE / "label_source_slot.json", "w"), indent=1)

def pr(i, value, referent, source, population, adjudicator, falsifier):
    return dict(id=i, value=value, referent=referent, source=source, population=population, adjudicator=adjudicator, falsifier=falsifier, banner=CAL)

recs = [
    pr("w2a2-sniascore-lower", b["lower"], "lower bound on BTS plain 'SN Ia' labels whose current basis is a SNIascore automated TNS report",
       f"{SPLIT}::bounds L; {DEFS} sec 6; {CAPS}; E2 arXiv:2104.12980 sec 7 lines 876-878, arXiv:2401.15167 sec 5.1 raw lines 1580-1591",
       "plain 'SN Ia' rows of " + POP, "authenticated TNS classification reports per object",
       "an authenticated report list returning fewer objects than this with a SNIascore latest report, or a human re-report after the capture date that replaces the SNIascore report of a counted object"),
    pr("w2a2-sniascore-lower-strong", b["lower_strong_only"], "lower bound using only E1 archived TNS pages (STRONG)", f"{SPLIT}::bounds L_strong; {CAPS}",
       "plain 'SN Ia' rows of " + POP, "authenticated TNS classification reports per object", "a rerun of split_labels.py on the same captures returning a different count, or a capture whose Classifier/s field is misparsed on inspection"),
    pr("w2a2-sniascore-upper", b["upper"], "upper bound on BTS plain 'SN Ia' labels that can be SNIascore annotation",
       f"{SPLIT}::bounds U; {DEFS} sec 6 (E1, E4 capture sha256 {CAP2021_SHA}, E5 peakt < {E5_CUT})", "plain 'SN Ia' rows of " + POP,
       "authenticated TNS classification reports; the unexcluded remainder is dominated by objects whose archived capture was unavailable or did not match",
       f"any SNIascore-reported object among those excluded by E1/E4/E5 (E5 is WEAK: an SN Ia first classified by SNIascore more than 30 d after peak would exceed this bound; sensitivity without E5 = {b['upper_noE5_sensitivity_not_slot_value']})"),
    pr("w2a2-count-measured", c("MEASURED"), "labels whose latest matching archived TNS report names human classifier(s) and follows a public spectrum", f"{SPLIT}::category; {CAPS}; {DEFS} sec 2-4", POP,
       "authenticated TNS reports; the classifying group's own records (Fritz) for whether the human report was software-assisted", "a counted object whose classifier is shown to be an automated pipeline (e.g. 'Atlas Syncatto' if SCAT documents it as automated), or a rerun returning a different count"),
    pr("w2a2-count-model-annotation", c("MODEL_ANNOTATION"), "labels whose basis is an automated-classifier TNS report (SNIascore, CCSNscore or bot marker in Classifier/s) or a paper naming the object as SNIascore-classified",
       f"{SPLIT}::category; {CAPS}; {DEFS} sec 3 and 5", POP, "authenticated TNS reports", "a human re-report after the capture date for a counted object, or a rerun returning a different count"),
    pr("w2a2-count-photometric-only", c("PHOTOMETRIC_ONLY"), "labels whose latest matching archived TNS report has no public spectrum on or before its time (MODERATE unless remarks state a photometric basis)",
       f"{SPLIT}::category; {CAPS}; {DEFS} sec 2 and 5", POP, "the classifying group's non-public spectra (Fritz/GROWTH Marshal)", "a classifying spectrum found for a counted object that was not uploaded to TNS, or a rerun returning a different count"),
    pr("w2a2-count-unresolved", c("UNRESOLVED (UNDEMONSTRATED)"), "labels no admissible public evidence places (UNDEMONSTRATED, not zero, not guessed)", f"{SPLIT}::category; fetch status {json.dumps(fs)}", POP,
       "authenticated TNS reports", "a rerun of fetch_tns_captures.py (resumable) placing objects recorded here as not_attempted/http_error/failed_retries"),
    pr("w2a2-ccsnscore-upper", cc["upper"], "upper bound on CC-class labels that can be CCSNscore annotation (reporting start date UNDEMONSTRATED)",
       f"{SPLIT}::cc_bound; arXiv:2412.08601 sec 6 lines 1089-1091; {DEFS} sec 7", "BTS rows with type in the CCSNscore layer classes", "CCSNscore GitHub page reporting criteria and TNS reports",
       "a CCSNscore TNS report measured on an object discovered before 2025-02-09 would fail the date margin (count found: %d)" % cc["ccsnscore_reports_found_discovered_before_cut"]),
    pr("w2a2-refusal14-refuse", R["counts"]["agent1_REFUSE"], "Agent 1's 98 answer-in-seed objects whose class is stated in seed text (refusal 14 fires; exception unmet)",
       "astronomy/wave2/agent2_label_source/scripts/refusal14_rulings.py::rule; refusal14_locate.py; agent1_supply_corpus/corpus_ledger.json sha256 3c619a13072092707bc51721d80b147fd903357fcc8561589acff7185f7693e0",
       "98 ZTFIDs in corpus_ledger.answer_in_own_source", "a reader independent of both agents re-reading each locator window",
       "a re-read of a locator window returning no stated class for an object ruled REFUSE, or a class stated for one ruled NOT_FIRED"),
]
json.dump(recs, open(HERE / "provenance_records.json", "w"), indent=1)

SK = ASTRO.parent / "fm-advantage-benchmark/scripts"
sys.path.insert(0, str(SK))
import validate as V
f = []
V.prov(slot["provenance"], f, "label_source_slot")
if V.ASSUMED.search(slot["provenance"]["source"]): f.append("source reads assumed")
out = ["PASS label_source_slot.json (provenance fields via validate.prov)" if not f else "FAIL label_source_slot.json " + "; ".join(f)]
r = subprocess.run([sys.executable, str(SK / "validate.py"), "provenance", str(HERE / "provenance_records.json")], capture_output=True, text=True)
out.append(r.stdout.strip())
stub = {k: slot for k in ["label_source"]}
(HERE / "scripts/_manifest_stub.json").write_text(json.dumps(stub))
r2 = subprocess.run([sys.executable, str(SK / "validate.py"), "ledger", str(HERE / "scripts/_manifest_stub.json"), "--kind", "domain_manifest"], capture_output=True, text=True)
out.append("one-slot domain_manifest stub (expected FAIL on slots owned by other agents / D5):\n" + r2.stdout.strip())
(HERE / "scripts/validate_output.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
