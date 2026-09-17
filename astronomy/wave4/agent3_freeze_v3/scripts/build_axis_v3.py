#!/usr/bin/env python3
"""Axis ledger v3 against the FROZEN bands (delta 0.018), 0.05 beside. No re-band. Rule E marks per axis number.
Preconditions: (a) measured labels, (b) V-O02 plus agent-3 wave-3 verification, (c) ruling 4."""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common4 import *  # noqa

assert sha(BANDS) == BANDS_SHA and sha(W4) == W4SHA
v3 = load(f"{OUT}/domain_manifest_v3.json"); assert manifest_hash(v3) == v3["frozen_hash"]
prev = load(f"{W3OUT}/axis_ledger_v2_final_against_frozen_bands.json")
VR = {r["target"]: r for r in load(f"{V}/v_records.json")}
wis = load("astronomy/wave4/agent2_price_of_truth/wiserep_check.json")
cen = {r["id"]: r for r in load("astronomy/wave3/agent2_measured_labels/tns_census_2026.json")}
assert wis["status"] == "BLOCKED"

def vid(t):
    r = VR[t]; return {"v_record": f"V-{t}", "verdict": r["verdict"], "rule_E": "CLEARED" if r["cleared_for_P4_under_rule_E"] else "V_PENDING"}
PEND = {"v_record": None, "rule_E": "V_PENDING"}

axes = copy.deepcopy(prev["axes"])
AX = {a["axis"]: a for a in axes}
AX["positive_supply"]["rule_E"] = {"O_optimistic_bound 1937669": vid("C01"), "M_obs 10": PEND, "cohort_nights 9": PEND, "P_measured": "UNDEMONSTRATED (no number to verify)"}
AX["positive_supply"]["wave4"] = "TNS BLOCKED (second record, 2026-09-16 and 2026-09-17); sanctioned WISeREP check BLOCKED (live HTTP 403; 43/43 archived pages 404, including classified controls, so silence carries no information)"
AX["negative_supply"]["rule_E"] = {"Ng_measured": "UNDEMONSTRATED (no number to verify)"}
AX["contamination_exposure"]["rule_E"] = {"E 1937669": vid("C01"), "S1_excluded 521920": vid("C03"), "S0_excluded_loci 112990": PEND, "antares_leak 193/9000": PEND}
AX["cluster_structure"]["rule_E"] = {"merged_objects 1937669": vid("C01"), "alerce_oids 1937720": vid("C02"), "raw_detections 2418954": PEND,
                                     "fink_raw_alerts 3511022": PEND, "fink_bracket": PEND, "antares_loci 1908703": PEND}
AX["cluster_structure"]["band_reading_note"] = "PROCEED rests on every broker count >= 12,855; the ALeRCE counts are CLEARED (C01, C02), the Fink and ANTARES counts are V_PENDING. Each exceeds the edge by >100x, and the ruling is refused on (a) regardless."
AX["split_integrity"]["rule_E"] = {"S1_total 521920": vid("C03"), "O_minus_all_listed_worst_case 1896117": PEND}
AX["unprocessable_units"]["rule_E"] = {"U 0": PEND}
AX["unprocessable_units"]["band_reading_note"] = "PROCEED rests on U = 0, which has no V record (V_PENDING)"
tc = AX["tool_coverage"]
tc["rule_E"] = {"counts 2/14/9": vid("T01"), "CATS 5/10, GHOST 3/8": vid("T02"), "alert_runs 160": vid("T03")}
tc["invariance_V"] = "CATS and GHOST invariant within float tolerance, not bit-identical (module V)"
tc["disposition"] = "PASS (counted after the band hash; V-O02 MATCH and agent-3 wave-3 verification)"

for a in axes:
    a.setdefault("both_deltas", "band at 0.018 (frozen); 0.05 thresholds beside (N02: 63-1,666 objects, CLEARED; nights 6-197, V_PENDING)")

pre = {
 "a": {"text": prev["p4_preconditions"]["a"]["text"], "state": "UNMET",
       "why": ("measured P and Ng UNDEMONSTRATED: TNS BLOCKED (second record, request dates 2026-09-16 and 2026-09-17); the sanctioned WISeREP existence check BLOCKED "
               "(agent 2 wave 4); wave 3: 0 STRONG on 13 readable of 627 cohort captures (" + str(cen["w3a2-c-cohort-measured-strong"]["value"]) + "), 13 typed with classifier unknown"),
       "records": [ref("astronomy/wave4/agent2_price_of_truth/wiserep_check.json"), ref("astronomy/wave3/agent2_measured_labels/tns_census_2026.json")]},
 "b": {"text": prev["p4_preconditions"]["b"]["text"], "state": "CLEARED",
       "v_record": {**vid("O02"), "sealed_sha256": VR["O02"]["sealed_sha256"]},
       "also": "agent-3 wave-3 own verification (precondition_b_verification in astronomy/wave3/agent3_manifest_freeze/axis_ledger_v2_final_against_frozen_bands.json)",
       "limits": "self-logged timestamps on one host"},
 "c": {"text": prev["p4_preconditions"]["c"]["text"], "state": "CLEARED",
       "basis": "PI ruling 4 'RATIFIED WITH CONDITIONS ... Precondition (c) clears under these conditions' (PANEL_BRIEF_WAVE4.md lines 17-20; ledger AMD-V3-02, AMD-V3-03)",
       "independence_from_unverified_numbers": ("clears by ratification of the label-source definition and conditions, not by a count; the bound numbers are V_PENDING (L01-L05), "
                                                "and every current reading of them ([954,2057], [954,2139], [955,2056], [955,2138]) lies inside [803, 2247], verified from sealed/V-L-r1.json")},
}
unmet = [k for k, v in pre.items() if v["state"] != "CLEARED"]
led = {
 "candidate": prev["candidate"], "branch": "prediction",
 "version": "v3 against frozen bands (agent 3, wave 4)",
 "manifest": {"path": f"{OUT}/domain_manifest_v3.json", "frozen_hash": v3["frozen_hash"]},
 "bands": prev["bands"],
 "delta_note": "bands frozen at delta 0.018 (literature prior); ratified delta 0.05 (ruling 1) thresholds reported beside, not re-banded; re-banding at 0.05 would be a new hashed registration",
 "planning_thresholds": {"delta_0.018_frozen": {"objects": [485, 12855], "objects_rule_E": vid("N01"), "nights": [40, 1515], "nights_rule_E": PEND},
                         "delta_0.05_beside": {"objects": [63, 1666], "objects_rule_E": vid("N02"), "nights": [6, 197], "nights_rule_E": PEND},
                         "sqrtq_note": "12,855 / 1,666 follow sample SD 0.728431; theoretical sqrt(q) gives 12,113 / 1,570 (V-N01, V-N02 finding; not a discrepancy)"},
 "sealed_counts": prev["sealed_counts"],
 "ruling": None,
 "ruling_refused_because": [f"precondition ({k}) UNMET: {pre[k]['why']}" for k in unmet],
 "p4_preconditions": pre,
 "binding_axis": "positive_supply at measured labels: TNS and WISeREP BLOCKED; frozen bands need L >= 12,855 (N01) or 1,515 nights; beside at 0.05: 1,666 (N02) or 197 nights",
 "combination_preview_not_a_ruling": "no axis in CLOSE; contamination_exposure and tool_coverage ESCALATE, so section 7 cannot yield PROCEED with the subject set unchanged; stated for agent 1 and the PI, not ruled",
 "definition_widened": False,
 "axes": axes,
 "completeness": ("Seven axes against bands_FROZEN.md at 0.018 with 0.05 beside; every axis number carries a V record id or V_PENDING. Preconditions: (a) UNMET, (b) CLEARED (V-O02), "
                  "(c) CLEARED (ruling 4). P4 refused; ruling null by design. The P4 ruling package is agent 1's."),
}
dump(led, f"{OUT}/axis_ledger_v3_against_frozen_bands.json")
log("6", f"axis_ledger_v3_against_frozen_bands.json built against frozen bands (no re-band); unmet {unmet}",
    [f"{OUT}/axis_ledger_v3_against_frozen_bands.json", BANDS, f"{V}/v_records.json", "astronomy/wave4/agent2_price_of_truth/wiserep_check.json"])
