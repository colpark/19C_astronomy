#!/usr/bin/env python3
"""Freeze v3 = frozen v2 + wave-4 PI rulings 1-5 (as amendments) + rule E marking from module V records.
The brief says 'freeze v2'; v2 is already frozen (preamble item 1), so this is v3 (naming disagreement recorded).
Writes amendment_ledger_v3.json (append-only copy of v1+v2 entries plus v3 entries) and domain_manifest_v3.json."""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common4 import *  # noqa

DRY = "--dry" in sys.argv
SCR = "/tmp/claude-1000/-home-aid1-Documents-4-19C-astronomy/addb1fc3-63d3-4989-8753-aa4c400b100e/scratchpad/dry4"
DEST = SCR if DRY else OUT
if DRY:
    os.makedirs(SCR, exist_ok=True)
    log = lambda *a, **k: None  # noqa

assert sha(W4) == W4SHA
v1 = load(f"{W3OUT}/domain_manifest_v1.json"); v2 = load(f"{W3OUT}/domain_manifest_v2.json")
assert manifest_hash(v1) == v1["frozen_hash"] == "ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8"
assert manifest_hash(v2) == v2["frozen_hash"] == "fba4259b1d5931ff8b74a3db2f438706ce29263ef7ca373a2cb5c5fd7f2cedd5"
led2 = load(f"{W3OUT}/amendment_ledger.json")
assert canonical_sha(led2["v1_entries"]) == led2["v1_entries_canonical_sha256"]
assert canonical_sha(led2["v2_entries"]) == led2["v2_entries_canonical_sha256"]

VR = {r["target"]: r for r in load(f"{V}/v_records.json")}
assert len(VR) == 38
VREC = f"{V}/v_records.json"
VSHA = sha(VREC)
r1 = load(f"{V}/sealed/V-L-r1.json")
assert sha(f"{V}/sealed/V-L-r1.json") == "8414d780b45ede281be395732e5d7cbe91a9819993bc5746c85a249e35bf5e85"
wis = load("astronomy/wave4/agent2_price_of_truth/wiserep_check.json")
cust = load("astronomy/wave4/agent5_integrity_closeout/custody_status.json")
tr = load("astronomy/wave3/agent5_integrity/transfer_record.json")
assert wis["status"] == "BLOCKED" and cust["status"] == "PENDING_RECEIPT" and tr["receipt_hash"] == ""
T = now()
W4REF = lambda loc: ref(W4, loc)

def vid(t):
    r = VR[t]
    return {"v_record": f"V-{t}", "verdict": r["verdict"], "cleared_for_P4_under_rule_E": r["cleared_for_P4_under_rule_E"], "sealed_sha256": r["sealed_sha256"]}

def E(value, target=None, note=None, status=None):
    d = {"value": value}
    if target:
        d.update(vid(target))
        d["rule_E"] = "CLEARED" if VR[target]["cleared_for_P4_under_rule_E"] else "V_PENDING"
    else:
        d["v_record"] = None
        d["rule_E"] = status or "V_PENDING"
    if note: d["note"] = note
    return d

# ------------------------------------------------ verify V's reading claim ourselves
RULED = [803, 2247]
readings = {}
for k, v in r1["derived"].items():
    readings[k] = {"L": v["L"], "U": v["U"], "cats": v["cats"], "inside_ruled_interval": RULED[0] <= v["L"] and v["U"] <= RULED[1]}
current = {k: v for k, v in readings.items() if "w2only" not in k}
w2only = {k: v for k, v in readings.items() if "w2only" in k}
all_current_inside = all(v["inside_ruled_interval"] for v in current.values())
assert all_current_inside
reading_check = {
 "source": {"path": f"{V}/sealed/V-L-r1.json", "sha256": sha(f"{V}/sealed/V-L-r1.json"), "blindness": "POST-DISCLOSURE, not blind"},
 "current_captures_all_four_readings": current,
 "all_current_readings_inside_[803,2247]": all_current_inside,
 "verified_by": "agent 3 from the sealed per-reading file, not from V's report text",
 "reading_not_listed_in_V_report": "key=iau|E5cut=1259.5 -> [955, 2138]: inside",
 "wave2_captures_only_readings": w2only,
 "finding": ("ruling 4's own interval [803, 2247] is reproduced only under E5 cut 1289.5 with ZTFID keying (and [804, 2246] under IAU keying); "
             "under the literal 1259.5 cut the wave-2-only bound is [803, 2329] (ZTFID) or [804, 2328] (IAU). The condition 'current bound inside [803, 2247]' "
             "holds under every reading; the ruled interval itself depends on the E5 reading. Listed for the PI, not reconciled."),
}

# ------------------------------------------------ ledger v3 (append-only)
v3e = [
 {"id": "NAME-V3-01", "slot": "manifest version", "kind": "NAMING DISAGREEMENT (recorded, not a silent substitution)",
  "before": {"brief_text": "Agent 3: freeze v2 ... v2 is the manifest P4 reads"},
  "after": {"freeze": "v3", "reason": "v2 already frozen (fba4259b...edd5, commit be1254b per preamble) and cannot be amended in place"},
  "cause": "wave-4 brief assignment vs coordinator preamble item 1", "source": W4REF("Assignments 'Agent 3: freeze v2' line 44; preamble item 1 lines 91-97")},
 {"id": "AMD-V3-01", "slot": "delta", "kind": "RATIFICATION",
  "before": {"value": 0.05, "status": "OVERRIDDEN", "literature_prior": 0.018, "ledger": "AMD-V2-04"},
  "after": {"value": 0.05, "status": "RATIFIED", "literature_prior": 0.018, "carry_both": "every table"},
  "cause_check": {"v_record": vid("O01"), "ordering_utc": "override 2026-09-16T20:14:03Z < first decision-time MDE file mtime 20:44:29Z (earliest wave-2 power output 20:43:28Z; commit f898294 20:46Z quoted) < resolvability at 0.05 20:48:29Z",
                  "timezone_note": "the PI's 15:14 and 15:46 are local -0500 (20:14Z, 20:46Z); '20:48' is UTC (preamble item 2)",
                  "caveats": ["git not run by V or agent 3: commit times are quoted from the preamble, not read",
                              "mtime shows only the last write; an earlier overwritten power file before 20:14Z cannot be excluded",
                              "host clock trust not established; timestamps are self-logged on one host",
                              "the wave-1 planning bracket and the practitioners' unpaired MDE ~0.045 predate the override, and the override's stated cause cites the latter"]},
  "cause": "PI ruling 1: 'Delta 0.05: RATIFIED ... Both deltas ride through every table: 0.018 as the literature prior, 0.05 as the ratified cost of action.'",
  "source": W4REF("ruling 1, lines 9-14")},
 {"id": "AMD-V3-02", "slot": "label_source", "kind": "RATIFICATION WITH CONDITIONS",
  "before": {"status": "UNDEMONSTRATED", "ledger": "SU-V2-03"},
  "after": {"status": "RATIFIED", "conditions_verbatim": [
      "Labels are TNS-reported spectroscopic classifications, with a model-annotation fraction bounded at [803, 2247] of 7843.",
      "For calibration, the SNIascore-flagged subset stays in, stratified.",
      "For any future paid claim, measured truth means human-classifier-confirmed only. Model-annotated labels are excluded, and a sensitivity row shows the result both ways.",
      "Precondition (c) clears under these conditions."]},
  "cause": "PI ruling 4", "source": W4REF("ruling 4, lines 17-20")},
 {"id": "RE-V3-01", "slot": "label_source numeric fields", "kind": "RULE E: V_PENDING",
  "fields": {"sniascore_bound": [954, 2057], "MEASURED": 1074, "MODEL_ANNOTATION": 954, "UNRESOLVED": 5815, "upper_noE5_sensitivity": 2654},
  "v_records": ["V-L01", "V-L02", "V-L03", "V-L04", "V-L05"],
  "why": "module V verdict DISCREPANCY (cause resolved); cleared_for_P4_under_rule_E false. The ruled [803, 2247] was reproduced by V only in its non-blind reconciled parse.",
  "readings_needing_ruling": ["(i) E5 cut: literal frozen text 1259.5 vs its own arithmetic 1289.5 (JD 2459319.5 - 2458000 = 1319.5; minus 30), which the producer implemented",
                              "(ii) twin IAU-name rows (SN2024led, SN2025oxy): evidence keyed per fetched ZTFID (producer) vs per IAU name"],
  "reading_check": reading_check,
  "cause": "wave-4 rule E; module V discrepancy reports D-L01..D-L05", "source": W4REF("rule E, line 5"),
  "records": [ref(f"{V}/discrepancies/D-L01.md"), ref(f"{V}/discrepancies/D-L02.md")]},
 {"id": "AMD-V3-03", "slot": "P4 precondition (c)", "kind": "CLEARS under ruling 4 conditions",
  "before": {"state": "UNMET"}, "after": {"state": "CLEARED"},
  "independence": "clears by the PI's ratification of the label-source definition and its conditions, not by any count; every current reading of the bound lies inside [803, 2247] (RE-V3-01 reading_check), so no V_PENDING number can reverse it",
  "cause": "PI ruling 4 'Precondition (c) clears under these conditions.'", "source": W4REF("ruling 4, line 20")},
 {"id": "AMD-V3-04", "slot": "supplied_by_human.tns_credentials", "kind": "BLOCKED (second record); sanctioned WISeREP check BLOCKED",
  "before": {"status": "BLOCKED", "request_dates": ["2026-09-16"], "ledger": "AMD-V2-07"},
  "after": {"status": "BLOCKED", "request_dates": ["2026-09-16", "2026-09-17"], "presence_check_utc": "2026-09-17T13:13:17Z",
            "wiserep": {"status": wis["status"], "record": ref("astronomy/wave4/agent2_price_of_truth/wiserep_check.json")}},
  "cause": "PI ruling 3 (SUPPLY: key or second BLOCKED record; WISeREP sanctioned if blocked); preamble item 4", "source": W4REF("ruling 3, line 16; preamble item 4, line 110")},
 {"id": "AMD-V3-05", "slot": "supplied_by_human.rulings_holder (custody)", "kind": "STILL PENDING_RECEIPT",
  "before": {"transfer": "PENDING_RECEIPT", "ledger": "AMD-V2-06"},
  "after": {"transfer": cust["status"], "receipt_hash": tr["receipt_hash"], "procedural": "the word 'procedural' stays attached to every blind result",
            "record": ref("astronomy/wave4/agent5_integrity_closeout/custody_status.json")},
  "cause": "PI ruling 2 (closes only when the holder's receipt hash is in transfer_record.json); preamble item 5", "source": W4REF("ruling 2, line 15; preamble item 5, line 111")},
 {"id": "AMD-V3-06", "slot": "module V", "kind": "CHARTERED; overhead cap EXCEEDED (interim)",
  "after": {"charter": ref(f"{V}/V_CHARTER.md"), "cap": "15% of wave effort",
            "interim_share": {"wall_time": "47% (52.4 of 110.7 min)", "tool_calls": "59% (122 of 207)"}, "disposition": "FAIL (interim)",
            "arithmetic_checked_by_agent3": "52.4/110.7 = 0.473; 122/207 = 0.589; to reach 15%: +238.6 min, +606 calls",
            "record": ref("astronomy/wave4/COORDINATOR_LOG.md"),
            "disagreement": "V self-report 51.4 min / ~125 calls (overhead.json) vs harness 52.4 min / 122 calls (coordinator log)"},
  "cause": "PI ruling 5", "source": W4REF("ruling 5, lines 21-24")},
 {"id": "RE-V3-02", "slot": "all slots", "kind": "RULE E marking",
  "what": "every ruling-bearing number in v3 carries its V record id (CLEARED) or V_PENDING; PI-supplied values marked PI_RULED",
  "cause": "wave-4 rule E", "source": W4REF("rule E, line 5"), "record": ref(VREC)},
]
for e in v3e:
    e["manifest_version"] = "v3"; e["recorded_utc"] = T; e["applied_to"] = "domain_manifest_v3.json (FROZEN)"

EID = {e["id"]: e for e in v3e}
# ------------------------------------------------ manifest v3
m = copy.deepcopy(v2)
m["manifest_version"] = "v3"
m["governing_brief"] = ref(W4)
m["naming_disagreement"] = "wave-4 brief says 'freeze v2'; v2 was already frozen (fba4259b...edd5), so this is v3 (NAME-V3-01, preamble item 1). 'The manifest P4 reads' is v3."
m["derived_from"] = {"v2": {"path": f"{W3OUT}/domain_manifest_v2.json", "frozen_hash": v2["frozen_hash"]},
                     "v1": {"path": f"{W3OUT}/domain_manifest_v1.json", "frozen_hash": v1["frozen_hash"]}}
m["inputs_state"] = "v2 plus wave-4 PI rulings 1-5, module V records (38), agent 2 wave-4 WISeREP check, agent 5 custody status"
m["module_v"] = {"records": ref(VREC), "charter": ref(f"{V}/V_CHARTER.md"), "cleared": 33, "not_cleared": ["L01", "L02", "L03", "L04", "L05"]}

# delta
d = m["delta"]
d["status"] = "RATIFIED"
d["override_history"] = {"ledger": "AMD-V2-04", "reason": d.pop("override_reason")}
d["ratification"] = {"ledger": "AMD-V3-01", "ruling": ref(W4, "ruling 1"), "cause_check": EID["AMD-V3-01"]["cause_check"],
                     "value_rule_E": "PI_RULED (a cost-of-action value, not a measurement); its cause check is V-O01"}
d["provenance"]["source"] += "; RATIFIED at PANEL_BRIEF_WAVE4.md sha256 " + W4SHA + " ruling 1 lines 9-14 (cause check astronomy/wave4/agent4_module_v/v_records.json V-O01)"
d["carry_both"] = "every table reports 0.05 (ratified cost of action) and 0.018 (literature prior) side by side (ruling 1)"
d["literature_prior"]["rule_E"] = E(0.018, None, "no V record (literature value, arXiv:2401.15167 Table 6)")
pw = {"P01": "E1_N pooled (REFUSED, refusal 4)", "P02": "E1_N k_binding=True (primary)", "P03": "E1_N k_binding=False", "P04": "E1_R round-46",
      "P05": "E3_N pooled (REFUSED, refusal 4)", "P06": "E3_N k_binding=True", "P07": "E3_N k_binding=False", "P08": "E3_R round-46"}
table = {}
for t, lab in pw.items():
    c = {x["field"]: x["claimed"] for x in VR[t]["comparisons"]}
    sd = next(v for k, v in c.items() if k.endswith("sigma_d"))
    md = next(v for k, v in c.items() if k.endswith(".mde"))
    n018 = next(v for k, v in c.items() if "delta_0.018" in k and k.endswith("n_min"))
    n05 = next(v for k, v in c.items() if "delta_0.05" in k and k.endswith("n_min"))
    nn = next(v for k, v in c.items() if k.endswith(".n"))
    table[t] = {"row": lab, "n": nn, "sigma_d": sd, "mde": md, "n_min_0.05": n05, "n_min_0.018": n018, **vid(t)}
d["calibration_context"]["power_table_both_deltas_rule_E"] = table
d["calibration_context"]["k_binding_nights"] = {"k_binding": E(61, "K01", "of 579 E1 nights (same for E3)"), "not_binding": E(518, "K02")}
d["calibration_context"]["composition_auc"] = {t: {"value": VR[t]["comparisons"][0]["claimed"], **vid(t)} for t in ("A01", "A02", "A03", "A04")}
d["planning_thresholds"]["rule_E"] = {
  "objects_0.018": E([485, 12855], "N01", VR["N01"]["finding"]),
  "objects_0.05": E([63, 1666], "N02", VR["N02"]["finding"]),
  "nights_0.018": E([40, 1515], None, "family-A night N_min: no V record"),
  "nights_0.05": E([6, 197], None, "family-A night N_min: no V record"),
  "sqrtq_note": "12,855 and 1,666 follow the sample SD 0.728431 of the n=50 synthetic binary column; theoretical sqrt(q)=0.7071 would give 12,113 and 1,570. Not a discrepancy: the frozen definition is min/max over the bracket rows as computed (V-N01, V-N02 finding)."}

# label_source
ls = m["label_source"]
bts = ls["value"]["bts"]
blind = {"L01": 953, "L02": 2143, "L03": 1070, "L04": 948, "L05": 5825}
bts["category_counts"] = {
  "MEASURED": {"claimed": 1074, "blind_V": 1070, **E(1074, "L03")},
  "MODEL_ANNOTATION": {"claimed": 954, "blind_V": 948, **E(954, "L04")},
  "PHOTOMETRIC_ONLY": {"claimed": 0, "blind_V": 0, **E(0, "L03", "field matched; record V-L03 not cleared")},
  "UNRESOLVED_UNDEMONSTRATED": {"claimed": 5815, "blind_V": 5825, **E(5815, "L05")}}
for x in bts["category_counts"].values(): x.pop("value")
sb = bts["sniascore_bound"]
bts["sniascore_bound"] = {
  "status_rule_E": "V_PENDING",
  "lower": {"claimed": sb["lower"], "blind_V": 953, **{k: v for k, v in E(sb["lower"], "L01").items() if k != "value"}},
  "upper": {"claimed": sb["upper"], "blind_V": 2143, **{k: v for k, v in E(sb["upper"], "L02").items() if k != "value"}},
  "upper_noE5_sensitivity_not_slot_value": {"claimed": sb["upper_noE5_sensitivity_not_slot_value"], "blind_V": 2658, "rule_E": "V_PENDING", "v_record": "V-L02"},
  "ruled_interval_ruling_4": {"value": RULED, "rule_E": "PI_RULED", "note": "reproduced by V only in its non-blind reconciled parse (V-L-r1), and only under E5 cut 1289.5"},
  "previous": sb["previous"], "wave1": sb["wave1"], "rule": sb["rule"],
  "readings_needing_ruling": EID["RE-V3-01"]["readings_needing_ruling"],
  "reading_check": reading_check}
ls["status"] = "RATIFIED"
ls["ratification"] = {"ledger": "AMD-V3-02", "conditions_verbatim": EID["AMD-V3-02"]["after"]["conditions_verbatim"],
                      "numbers": "numeric fields frozen as V_PENDING (RE-V3-01), not cleared values",
                      "condition_holds_under_all_readings": all_current_inside}
ls["status_note"] = ("RATIFIED WITH CONDITIONS (PI ruling 4). The definition and conditions are frozen; the SNIascore bound [954, 2057] and counts "
                     "1,074 / 954 / 5,815 are V_PENDING under rule E until the E5-cut and twin-keying readings are ruled.")
ls["provenance"]["source"] += "; RATIFIED WITH CONDITIONS at PANEL_BRIEF_WAVE4.md sha256 " + W4SHA + " ruling 4 lines 17-20; numeric fields V_PENDING per astronomy/wave4/agent4_module_v/v_records.json V-L01..V-L05"
ls["value"]["rubin_cohort"]["rule_E"] = "all rubin_cohort numbers (0 STRONG, 13 existence, 7 leak) V_PENDING: no V record"
ls["wave4"] = {"tns": "BLOCKED second record (AMD-V3-04)", "wiserep": "BLOCKED (agent 2 wave 4)",
               "measured_cohort_labels": "UNDEMONSTRATED: TNS and WISeREP both BLOCKED"}
ls.pop("override_invitation", None)
ls["override_invitation"] = "Ratified with conditions. Open for the PI: rule readings (i) E5 cut and (ii) twin keying so V can clear L01-L05."

# k, tau, S, subject, exposure, tool inventory, epoch, candidates: rule E marks
m["k"]["rule_E"] = {"k": E(8, None, "RATIFIED at v1; no V record"), "candidates_per_round": E(46.41), "chance_stated": E(0.1718),
                    "k_binding_nights": E(61, "K01"), "nights_k_not_binding": E(518, "K02")}
m["tau"]["rule_E"] = {"radius_arcsec": E(1.0, None, "no V record"), "n_clusters_bts": E(11183, None, "BTS calibration only")}
m["S"]["rule_E"] = {"budget_arm_cells": E(1000, None, status="PI_RULED"), "engineering_hours": E(200, None, status="PI_RULED"),
                    "planning_rounds_71_498": E([71, 498], None, "PLANNING-ONLY arithmetic, no V record")}
m["subject_set"]["rule_E"] = "no numbers bear on a ruling except cutoff dates (V_PENDING, no V record)"
m["exposure_key"]["rule_E"] = {"cohort_after_every_cutoff": E(1937669, "C01"), "antares_prior_position_leak_193_of_9000": E([193, 9000]),
                               "bts_capture_split_6166_0_1677": E([6166, 0, 1677], None, "BTS calibration only")}
ti = m["tool_inventory"]["rubin_functional_recount_w3"]
ti["rule_E"] = {"counts_all": E({"PASS": 2, "FAIL": 14, "UNDEMONSTRATED": 9}, "T01"), "CATS": E("5/10", "T02"), "GHOST": E("3/8", "T02"),
                "alert_runs": E(160, "T03")}
ti["invariance_V"] = "CATS and GHOST invariant within float tolerance, not bit-identical (module V invariance.json)"
m["tool_inventory"]["rule_E_structural_census"] = "wave-1 structural counts in value.summary: V_PENDING (no V record); P4 tool_coverage reads T01-T03"
de = m["decision_epoch"]["strata"]
de["S0"]["rule_E"] = E(112990, None, "ANTARES loci, no V record")
de["S1"]["rule_E"] = E(521920, "C03")
c = m["candidates"][0]
c["cohorts"]["prospective_counts_w3"]["rule_E"] = {"O_merged": E(1937669, "C01"), "alerce_oids": E(1937720, "C02"), "S1": E(521920, "C03"),
                                                   "one_detection_share": E(0.8082, "C04"), "U": E(0, None, "no V record"), "cohort_nights": E(9, None, "no V record")}
c["prospective_label_supply_w3"]["rule_E"] = "all census lower bounds, reachability and cohort existence counts V_PENDING (no V record)"
tc = m["pi_reratification_inputs"]["truth_cost"]
tc["rule_E"] = {"formula_rows_288": E(288, "R01"), "N63": E(tc["by_delta"]["0.05 (override)"]["N_63"], "R02"), "N485": E(tc["by_delta"]["0.018 (literature prior; frozen bands)"]["N_485"], "R03"),
                "N1666_and_N12855": E("see ranges_over_grid_L0", "R04"), "N_brackets": {"N01": vid("N01"), "N02": vid("N02")}}
tc["wave4_monthly_pricing"] = {"record": ref("astronomy/wave4/agent2_price_of_truth/truth_cost_monthly.json"), "rule_E": "V_PENDING (no V record)",
                               "months_after_return": {"N63": "1-2", "N485": "2-9", "N1666": "8-28", "N12855": "70-115"}}
m["pi_reratification_inputs"]["state"] = "OPEN: ruling 4 ratified the label source; the ruling-1 (wave 3) go/no-go on Rubin-era paid work is not given in the wave-4 brief"
m["candidates"][0]["p4_state_v3"] = "no ruling; see axis_ledger_v3_against_frozen_bands.json: (a) UNMET, (b) CLEARED (V-O02), (c) CLEARED (ruling 4)"
c.pop("p4_state_v2", None)

# supplied fields
m["supplied_by_human"]["tns_credentials"] = "BLOCKED, second record (AMD-V3-04): request dates 2026-09-16 and 2026-09-17; sanctioned WISeREP check BLOCKED (HTTP 403 live, archive 404)"
m["supplied_by_human"]["rulings_holder"] += "; wave 4: still PENDING_RECEIPT, receipt_hash empty; 'procedural' stays on every blind result (AMD-V3-05)"
for r in m["d5_inputs"]:
    if r["id"] == "d5-tns-credentials":
        r["provenance"]["source"] += "; second BLOCKED record PANEL_BRIEF_WAVE4.md sha256 " + W4SHA + " ruling 3 line 16, preamble item 4"
        r["request_dates"] = ["2026-09-16", "2026-09-17"]; r["wiserep"] = "BLOCKED"
m["graph_escalations"][0]["module_v"] = "ruling 5 chartered module V; overhead cap exceeded (interim), AMD-V3-06"

# rule E index
idx = []
def walk(o, path):
    if isinstance(o, dict):
        if "rule_E" in o and isinstance(o["rule_E"], str) and ("v_record" in o):
            idx.append({"path": path, "value": o.get("value", o.get("claimed")), "rule_E": o["rule_E"], "v_record": o.get("v_record")})
        for k, v in o.items():
            walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")
walk(m, "$")
for t, row in table.items():
    idx.append({"path": f"$.delta.calibration_context.power_table_both_deltas_rule_E.{t}", "value": {k: row[k] for k in ("sigma_d", "mde", "n_min_0.05", "n_min_0.018")}, "rule_E": "CLEARED", "v_record": f"V-{t}"})
for t in ("A01", "A02", "A03", "A04"):
    idx.append({"path": f"$.delta.calibration_context.composition_auc.{t}", "value": VR[t]["comparisons"][0]["claimed"], "rule_E": "CLEARED", "v_record": f"V-{t}"})
idx.append({"path": "$.candidates[0].p4_state_v3 (precondition b)", "value": True, "rule_E": "CLEARED", "v_record": "V-O02"})
idx.append({"path": "$.delta.ratification.cause_check", "value": "ordering", "rule_E": "CLEARED (MATCH_WITHIN_TOL)", "v_record": "V-O01"})
m["rule_E_index"] = {"entries": idx,
  "counts": {s: sum(1 for e in idx if e["rule_E"].startswith(s)) for s in ("CLEARED", "V_PENDING", "PI_RULED")},
  "scope_note": ("the brief scopes rule E to the ruling-bearing numbers listed by agent 4 (V_TARGETS, 38) and says everything else proceeds unverified; "
                 "this manifest also marks ruling-adjacent numbers outside that list V_PENDING, as instructed. V_PENDING outside V_TARGETS blocks nothing by the brief's rule."),
  "not_in_manifest_but_cleared": {t: vid(t) for t in ("Q01", "Q02", "Q03", "Q04")}}

m["d5_disposition"] = {
 "stage": "D5 ratification", "frozen_and_hashed": "PASS", "every_slot_ratified_or_overridden": "FAIL",
 "per_slot": {"tau": "DERIVED (no PI ruling)", "k": "RATIFIED", "label_source": "RATIFIED WITH CONDITIONS (numeric fields V_PENDING)",
              "exposure_key": "DERIVED (no PI ruling)", "tool_inventory": "OVERRIDDEN (three Rubin counterpart rows)", "delta": "RATIFIED (0.05; prior 0.018 carried)",
              "S": "UNDEMONSTRATED (computed at R1)", "subject_set": "DERIVED (no PI ruling)", "decision_epoch": "RATIFIED"},
 "disposition": "UNDEMONSTRATED: D5 does not advance. tau, exposure_key and subject_set still carry no PI ruling (the wave-4 brief rules on none of them); S awaits R1. Not ratified on the PI's behalf."}
m["disagreements_v3"] = [
 "naming: brief 'freeze v2' vs frozen v2 -> v3 (NAME-V3-01)",
 "ruling 4 cites [803, 2247]; current producer bound [954, 2057] is V_PENDING; [803, 2247] is reproduced by V only non-blind and only under E5 cut 1289.5 (literal 1259.5 on wave-2 captures gives [803, 2329])",
 "V report lists three bound readings; the fourth combination (IAU keying + literal E5) [955, 2138] is unlisted; agent 3 verified it inside [803, 2247]",
 "ruling 1 times mix -0500 local (15:14, 15:46) and UTC (20:48); PI's 15:46 = commit f898294 20:46Z vs power_calibration.json mtime 20:44:29Z vs V's earliest wave-2 power output 20:43:28Z; ordering holds in every reading",
 "rule E scope: brief limits it to V_TARGETS; instruction marks all other numbers V_PENDING (scope_note)",
 "module V overhead: self-report 51.4 min / ~125 calls vs harness 52.4 min / 122 calls",
 "Rubin on-sky fraction 10/15 (scheduler) vs 11/16 (Fink alert nights) in agent 2 wave-4 monthly pricing",
 "power.py (vendored, unpatched) crashes with AttributeError on a ragged row instead of refusing (module V property tests); not a manifest number",
]
m["open_items_carried"] = ["tau, exposure_key, subject_set: no PI ruling; D5 does not advance on them",
                           "S2 stratum: ruling 6 (wave 3) 'reported and excluded' vs bands_FROZEN.md section 3 'not removed'; unresolved",
                           "all disagreements_v2 entries unchanged"]
m["amendment_ledger"] = {"path": f"{OUT}/amendment_ledger_v3.json"}
m["completeness"] = ("v3: v2 plus wave-4 rulings 1-5 (AMD-V3-01..06), naming disagreement NAME-V3-01, rule E marks from 38 module V records (RE-V3-01, RE-V3-02). "
                     "Not covered: PI rulings on tau, exposure_key, subject_set, S2 and the two label readings; R1 (S); measured Rubin cohort labels (TNS and WISeREP BLOCKED).")

led3 = {"record": "amendment_ledger_v3", "append_only": True,
        "carried_from": {"path": f"{W3OUT}/amendment_ledger.json", "sha256": sha(f"{W3OUT}/amendment_ledger.json")},
        "entry_kinds": led2["entry_kinds"] + " Wave 4 adds NAMING DISAGREEMENT and RULE E marking.",
        "v1_entries": led2["v1_entries"], "v1_entries_canonical_sha256": led2["v1_entries_canonical_sha256"],
        "v2_entries": led2["v2_entries"], "v2_entries_canonical_sha256": led2["v2_entries_canonical_sha256"],
        "v3_entries": v3e, "v3_entries_canonical_sha256": canonical_sha(v3e),
        "completeness": "v1 and v2 entries copied verbatim (canonical hashes re-verified). v3: one entry per wave-4 ruling 1-5 (ruling 4 split into ratification, rule-E V_PENDING and precondition (c)), naming disagreement, rule E marking, freeze. No entry ratifies tau, exposure_key or subject_set."}
m["amendment_ledger"].update({"v1_entries_canonical_sha256": led3["v1_entries_canonical_sha256"], "v2_entries_canonical_sha256": led3["v2_entries_canonical_sha256"],
                              "v3_entries": [e["id"] for e in v3e], "v3_entries_canonical_sha256": led3["v3_entries_canonical_sha256"]})
dump(led3, f"{DEST}/amendment_ledger_v3.json")
m["frozen_utc"] = now()
m["frozen_hash"] = ""
m["frozen_hash"] = manifest_hash(m)
dump(m, f"{DEST}/domain_manifest_v3.json")
print("readings inside:", all_current_inside, "| rule E counts:", m["rule_E_index"]["counts"], "| hash:", m["frozen_hash"])
if not DRY:
    log("4", f"v3 FROZEN: domain_manifest_v3.json frozen_hash={m['frozen_hash']} (same canonical method as v1/v2); amendment_ledger_v3.json v3 entries canonical sha={led3['v3_entries_canonical_sha256']}",
        [f"{OUT}/domain_manifest_v3.json", f"{OUT}/amendment_ledger_v3.json"])
