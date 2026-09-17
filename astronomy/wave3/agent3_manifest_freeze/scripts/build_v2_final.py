#!/usr/bin/env python3
"""Freeze v2: v2 DRAFT + agent-2 wave-3 handoff (hashes verified). Resolves PENDING-V2-01.
Writes domain_manifest_v2.json (frozen, same canonical method as v1). The DRAFT file is left as the pre-handoff record."""
import copy, json, os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa
import oplog

DRAFT_SHA = "38bbf3d41d2b245a73da6154e0ccf8e7832812195135f9470c8d5e79540729a6"  # log step 10
assert sha(f"{OUT}/domain_manifest_v2_DRAFT.json") == DRAFT_SHA
v1 = load(f"{OUT}/domain_manifest_v1.json"); assert manifest_hash(v1) == v1["frozen_hash"]
A2 = "astronomy/wave3/agent2_measured_labels"
HANDOFF = {"tns_census_2026.json": "c7b035f04fa77b41386555ba1258fcc6624f9fc1b5354aa913fd20a78b7eeaa9",
           "supply_P_per_month.json": "b028de4a80b30d875358f1594c4a2b6fc3ceda7e4bfadb958debc56c4527b2ce",
           "truth_cost.json": "53f229b3deb4137781ce06c80016bdf54dde506e80f06024d129d4feb0b81c6e",
           "truth_cost_table.csv": "8eee9f94b55d5ccad10e32cf721073d729865c442aff662661117a0f703b09a3",
           "label_source_slot.json": "fdae64921d6749e466932d13ffd0aa4e14359b0a946a31b32bacf9a97ce83719"}
for f, h in HANDOFF.items():
    assert sha(f"{A2}/{f}") == h, f
cen = {r["id"]: r for r in load(f"{A2}/tns_census_2026.json")}
sup = load(f"{A2}/supply_P_per_month.json")
tc = load(f"{A2}/truth_cost.json")
lab = load(f"{A2}/label_source_slot.json")
AXF = f"{OUT}/axis_ledger_v2_final_against_frozen_bands.json"
axf = load(AXF)
T = now()
W3REF = lambda loc: ref(W3, loc)

m = load(f"{OUT}/domain_manifest_v2_DRAFT.json")
led = load(f"{OUT}/amendment_ledger.json")
assert canonical_sha(led["v1_entries"]) == led["v1_entries_canonical_sha256"]

# ------------------------------------------------ label_source
prev_ls = m["label_source"]
m["label_source"] = {
 "value": lab["value"],
 "provenance": lab["provenance"],
 "status": "UNDEMONSTRATED",
 "status_note": lab["status_reason"],
 "banner": lab["banner"],
 "supersedes": lab["supersedes"],
 "wave3": {"tns_track_one": "BLOCKED (AMD-V2-07)",
           "resolved_pending": "PENDING-V2-01 resolved by SU-V2-03..05",
           "ratification_gate": "ruling 1: re-ratification against this wave's measured label supply before any Rubin-era paid work; OPEN (inputs in PI_rerat_packet.md)",
           "observation": prev_ls["wave3"]["observation"]},
 "source_records": [ref(f"{A2}/label_source_slot.json"), ref(f"{A2}/REPORT.md"), ref("astronomy/wave2/agent2_label_source/label_source_slot.json", "superseded")],
 "override_invitation": ("Override invitation: accept the bounded state (UNDEMONSTRATED), supply TNS credentials, or name a different label source "
                         "with a reason. P4 precondition (c) stays unmet until a label source is ratified or measured P and Ng exist."),
}

# ------------------------------------------------ supply P per month (lower bounds) and truth cost
months = sup["months"]
supply_block = {
 "status": "LOWER BOUNDS ONLY (exact monthly counts UNDEMONSTRATED; TNS BLOCKED, archived stats pages are 403 copies)",
 "unit": "object x program classification report, earliest report, readable Internet Archive captures (214 of 2,244 enumerated objects)",
 "per_month_lower_bound": {k: {"spectroscopic_units": v["a_spectroscopic_units_lower_bound"],
                                "nonbot_measured_units": v["b_nonbot_measured_lower_bound"]["excl_syncatto"],
                                "objects_first_classified": v["P_objects_first_classified_lower_bound"],
                                "rubin_cohort_strong": v["c_cohort_T1_strong"]} for k, v in months.items()},
 "totals_Jan_Sep_lower_bound": {"spectroscopic_units": cen["w3a2-a-spectroscopic-units-lb"]["value"]["total_Jan_Sep"],
                                "nonbot_units": cen["w3a2-b-nonbot-units-lb"]["value"]["total_Jan_Sep"]},
 "programs_top_lower_bound": {"ZTF": 63, "ePESSTO+": 55, "GeminiClass": 9, "SCAT": 8, "UCSC": 6, "BlackGEM": 5},
 "automation_2026": "20 of 181 spectroscopic units SNIascore (all ZTF); 0 CCSNscore; 0 Syncatto",
 "rubin_cohort": {"measured_nonbot_strong": 0, "on_readable_captures": "13 of 627 tier-A cohort-matched objects", "status": "UNDEMONSTRATED (not zero)",
                  "existence_typed_moderate": 13, "existence_classifier": "UNDEMONSTRATED"},
 "reachability": tc["reachability"],
 "records": [ref(f"{A2}/supply_P_per_month.json"), ref(f"{A2}/tns_census_2026.json")],
}
truth = {
 "role": "input to the PI re-ratification required by ruling 1; not a ruling, not S",
 "formula": tc["formula"],
 "L_used": tc["L_used"],
 "ranges_over_grid_L0": tc["ranges_over_grid_L0"],
 "by_delta": {"0.05 (override)": {"N_63": tc["ranges_over_grid_L0"]["delta_0.05_N_63"], "N_1666": tc["ranges_over_grid_L0"]["delta_0.05_N_1666"]},
              "0.018 (literature prior; frozen bands)": {"N_485": tc["ranges_over_grid_L0"]["delta_0.018_N_485"], "N_12855": tc["ranges_over_grid_L0"]["delta_0.018_N_12855"]}},
 "missed_rare_event": "+100 slots per miss on every row; miss rate UNDEMONSTRATED",
 "constraints": tc["constraints"],
 "records": [ref(f"{A2}/truth_cost.json"), ref(f"{A2}/truth_cost_table.csv")],
}
m["candidates"][0]["prospective_label_supply_w3"] = supply_block
m["S"]["gates"] = ["ruling 1: no Rubin-era paid work starts without re-ratification against this wave's measured label supply. OPEN: measured cohort supply UNDEMONSTRATED; inputs in PI_rerat_packet.md"]
m["pi_reratification_inputs"] = {
 "ruling": ref(W3, "ruling 1, line 13"),
 "state": "OPEN (awaiting PI)",
 "measured_supply_rubin_cohort": "none demonstrated: 0 STRONG on 13 readable captures of 627; 13 typed, classifier unknown; P and Ng uncomputable",
 "supply_P_per_month": "lower bounds only (see candidates[0].prospective_label_supply_w3)",
 "truth_cost": truth,
 "p4_readings": {"ledger": ref(AXF), "ruling": None, "preconditions": {k: v["state"] for k, v in axf["p4_preconditions"].items()},
                 "escalate_axes": ["contamination_exposure", "tool_coverage"]},
 "packet": f"{OUT}/PI_rerat_packet.md",
}
m["candidates"][0]["p4_state_v2"] = f"no ruling; {AXF}: preconditions (a) and (c) UNMET (verified against agent 2 files), (b) CLEARED (verified); validator FAIL stands"
m["candidates"][0].pop("p4_state_v2_draft", None)
m["candidates"][0]["source_records"].append(ref(AXF))
m["exposure_key"]["wave3_additions"]["agent2_position_leak"] = "ANTARES matches 7 supernovae discovered 2025-02..2026-04 at cohort positions (agent 2 disagreement 3); listed"
m["exposure_key"]["wave3_additions"]["tns_discovery_proxy"] = "SN2017bde and AT2019czs remain counterexamples to the discovery-date lower bound"

# ------------------------------------------------ ledger
v2e = led["v2_entries"]
for e in v2e:
    if e["id"] == "PENDING-V2-01":
        e["kind"] = "PENDING input: RESOLVED"
        e["resolved_utc"] = T
        e["resolved_by"] = ["SU-V2-03", "SU-V2-04", "SU-V2-05"]
        e["resolution"] = "agent 2 handoff (commit 74d012c per coordinator), 5 file hashes verified by agent 3"
new = [
 {"id": "SU-V2-03", "slot": "label_source", "kind": "SLOT UPDATE (supersession; not a PI ruling)",
  "before": {"record": ref("astronomy/wave2/agent2_label_source/label_source_slot.json"), "sniascore_bound": [803, 2247], "unresolved": 6156, "status": "UNDEMONSTRATED"},
  "after": {"record": ref(f"{A2}/label_source_slot.json"), "sniascore_bound": [954, 2057], "unresolved": 5815, "rubin_cohort_measured_nonbot": "UNDEMONSTRATED (0 STRONG on 13 readable of 627; 13 existence, classifier unknown)", "status": "UNDEMONSTRATED"},
  "cause": "wave-3 brief agent 2 assignment (track one BLOCKED, public-archive resume under AMW3-2) and agent 3 assignment 'fold in the wave 2 label slot'", "source": W3REF("Assignments, Agent 2 and Agent 3")},
 {"id": "SU-V2-04", "slot": "candidates[0].prospective_label_supply_w3", "kind": "SLOT UPDATE: supply P per month recorded as LOWER BOUNDS",
  "after": {"totals_Jan_Sep": supply_block["totals_Jan_Sep_lower_bound"], "exact": "UNDEMONSTRATED"},
  "cause": "wave-3 brief agent 2 track two (census)", "source": W3REF("Assignments, Agent 2, track two"), "record": ref(f"{A2}/supply_P_per_month.json")},
 {"id": "SU-V2-05", "slot": "pi_reratification_inputs.truth_cost", "kind": "INPUT ATTACHED for PI re-ratification (ruling 1); not a ruling",
  "after": {"delta_0.018_N_485": tc["ranges_over_grid_L0"]["delta_0.018_N_485"], "delta_0.05_N_63": tc["ranges_over_grid_L0"]["delta_0.05_N_63"], "delta_0.05_N_1666": tc["ranges_over_grid_L0"]["delta_0.05_N_1666"]},
  "cause": "wave-3 brief agent 2 track two ('That number is what truth costs, and it feeds my re-ratification')", "source": W3REF("Assignments, Agent 2, track two"), "record": ref(f"{A2}/truth_cost.json")},
 {"id": "FRZ-V2", "slot": "manifest", "kind": "FREEZE v2", "cause": "coordinator finalize instruction after agent 2 handoff; wave-3 brief agent 3 'freeze and hash'", "source": W3REF("Assignments, Agent 3")},
]
for e in new:
    e["manifest_version"] = "v2"; e["recorded_utc"] = T; e["applied_to"] = "domain_manifest_v2.json (FROZEN)"
for e in v2e:
    e["applied_to"] = "domain_manifest_v2.json (FROZEN); first applied to v2 DRAFT"
led["v2_entries"] = v2e + new
led["v2_entries_state"] = "FINAL: applied to frozen domain_manifest_v2.json"
led["v2_entries_canonical_sha256"] = canonical_sha(led["v2_entries"])
led.pop("v2_entries_canonical_sha256_draft", None)
led["completeness"] = led["completeness"].replace("plus two fold-ins and one PENDING input (agent 2). v2 entries are DRAFT until v2 freezes.",
    "plus fold-ins SU-V2-01..05, PENDING-V2-01 (resolved) and FRZ-V2. Slots with no PI ruling (tau, exposure_key, subject_set) have no ratification entry.")
dump(led, f"{OUT}/amendment_ledger.json")

# ------------------------------------------------ manifest header, disposition, freeze
m["manifest_version"] = "v2"
m.pop("draft_status", None)
m["derived_from"]["draft"] = {"path": f"{OUT}/domain_manifest_v2_DRAFT.json", "sha256": DRAFT_SHA}
m["inputs_state"] = "v1 plus wave-3 PI rulings 1-6, wave-3 counts from agent 1 (cohort, axes), agent 4 (tool recount) and agent 2 (label slot, census lower bounds, truth cost)"
m["amendment_ledger"] = {"path": f"{OUT}/amendment_ledger.json", "v1_entries_canonical_sha256": led["v1_entries_canonical_sha256"],
                         "v2_entries": [e["id"] for e in led["v2_entries"]], "v2_entries_canonical_sha256": led["v2_entries_canonical_sha256"]}
m["d5_disposition"]["frozen_and_hashed"] = "PASS"
m["d5_disposition"]["per_slot"]["label_source"] = "UNDEMONSTRATED (agent 2 landed; no measured cohort supply)"
m["d5_disposition"]["disposition"] = ("UNDEMONSTRATED: D5 does not advance. tau, exposure_key and subject_set carry no PI ruling; label_source UNDEMONSTRATED "
                                      "and awaits the ruling-1 re-ratification; S awaits R1. Not ratified on the PI's behalf.")
m["disagreements_v2"] = m["disagreements_v2"] + [
 "agent 2 sealed prediction non-bot share 0.7 [0.5, 0.85] vs observed 0.89 (outside); listed",
 "13 typed cohort objects (existence) vs 0 measured non-bot on readable captures: not the same quantity; neither is P",
 "night count: brief 10 on-sky nights vs agent 1's 9 alert dates (agent 2 reach 775 vs 861 per night)",
 "BTS trigger purity 0.967 vs 0.956 within arXiv:2401.15167 (truth-cost grid carries both)",
 "Rochester 2026 totals 17,562 (CSV) vs 19,448 (page)",
]
m["completeness"] = ("v2: v1 plus wave-3 rulings 1-6 (AMD-V2-01..08) and fold-ins from agents 1, 4 and 2 (SU-V2-01..05); PENDING-V2-01 resolved. "
                     "Not covered: PI rulings on tau, exposure_key, subject_set; the ruling-1 re-ratification; R1 (S); measured Rubin cohort labels (UNDEMONSTRATED).")
m["frozen_utc"] = now()
m["frozen_hash"] = ""
m["frozen_hash"] = manifest_hash(m)
dump(m, f"{OUT}/domain_manifest_v2.json")
oplog.log("15", f"note: step 14 text names the pre-handoff filename; its hashed path is axis_ledger_v2_final_against_frozen_bands.json. v2 FROZEN: domain_manifest_v2.json frozen_hash={m['frozen_hash']}; ledger v2 entries canonical sha={led['v2_entries_canonical_sha256']}",
          [f"{OUT}/domain_manifest_v2.json", f"{OUT}/amendment_ledger.json", AXF])
