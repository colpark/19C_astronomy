#!/usr/bin/env python3
"""v2 DRAFT: start from frozen v1, apply wave-3 PI rulings 1-6 as amendments, fold in landed wave-3 counts
(agent 1 cohort/axes, agent 4 tool recount). Agent 2 wave-3 inputs marked PENDING. NOT FROZEN: frozen_hash stays ""."""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa
import oplog

v1 = load(f"{OUT}/domain_manifest_v1.json")
assert manifest_hash(v1) == v1["frozen_hash"], "v1 hash does not verify"
assert sha(W3) == W3SHA
led = load(f"{OUT}/amendment_ledger.json")
assert canonical_sha(led["v1_entries"]) == led["v1_entries_canonical_sha256"]
A1W3 = "astronomy/wave3/agent1_cohort_finish"; A4W3 = "astronomy/wave3/agent4_tool_recount"; A5W3 = "astronomy/wave3/agent5_integrity"
cc = {r["id"]: r for r in load(f"{A1W3}/rubin_cohort_count.json")}
ax4 = load(f"{A4W3}/tool_coverage_axis.json")
pow05 = load(f"{A4W3}/power_calibration_delta005.json")
tr3 = load(f"{A5W3}/transfer_record.json")
axv2 = f"{OUT}/axis_ledger_v2_against_frozen_bands.json"
W3REF = lambda loc: ref(W3, loc)
T = now()

def prov(referent, source, population, adjudicator, falsifier):
    return dict(referent=referent, source=source, population=population, adjudicator=adjudicator, falsifier=falsifier)

# ---------------------------------------------------------------- v2 ledger entries
v2e = [
 {"id": "AMD-V2-01", "slot": "supplied_by_human.budget", "kind": "SUPPLIED by PI",
  "before": {"value": None, "status": "UNDEMONSTRATED", "ledger": "AMD-V1-04"},
  "after": {"value": {"agent_arm_cells_hard_cap": 1000, "engineering_hours": 200, "phase": "calibration"}},
  "condition": "No Rubin-era paid work starts without a re-ratification against the measured label supply from this wave.",
  "cause": "PI ruling 1", "source": W3REF("PI rulings (D5), ruling 1, line 13")},
 {"id": "AMD-V2-02", "slot": "S", "kind": "UNDEMONSTRATED (PI: computed at R1)",
  "before": {"value": None, "status": "UNDEMONSTRATED", "ledger": "AMD-V1-06"},
  "after": {"value": None, "status": "UNDEMONSTRATED", "resolves_at": "R1 (measured hours or cells per workflow)"},
  "cause": "PI ruling 1: 'S is computed at R1.'", "source": W3REF("ruling 1, line 13")},
 {"id": "AMD-V2-03", "slot": "supplied_by_human.cost_of_action", "kind": "SUPPLIED by PI",
  "before": {"value": None, "status": "UNDEMONSTRATED", "ledger": "AMD-V1-05"},
  "after": {"value": {"one_spectrum": "0.5 h P60-class time", "wrong_routine_commitment": "1 slot", "missed_rare_event": ">= 100 slots", "asymmetric": True}},
  "cause": "PI ruling 2", "source": W3REF("ruling 2, lines 14-17")},
 {"id": "AMD-V2-04", "slot": "delta", "kind": "OVERRIDE",
  "before": {"value": 0.018, "status": "DERIVED"},
  "after": {"value": 0.05, "status": "OVERRIDDEN", "literature_prior": 0.018, "carry_both": "every P7 table"},
  "cause": "PI ruling 2: 'Delta override: 0.018 becomes 0.05. Cause: switching a production selector costs engineer weeks, and 0.018 sits below its own unpaired resolution. Keep 0.018 as the literature prior, and carry both values through every P7 table.'",
  "source": W3REF("ruling 2, lines 18-19")},
 {"id": "AMD-V2-05", "slot": "graph_escalations (R1 -> I1)", "kind": "RATIFICATION of escalation",
  "before": {"state": "ESCALATED, unruled", "ledger": "ESC-V1-01"},
  "after": {"state": "RATIFIED as staged", "compositions": "PRE-I1 CALIBRATION", "I1_designation": "waits for R1 plus PI ratification", "edges": "unweakened"},
  "cause": "PI ruling 3", "source": W3REF("ruling 3, line 20")},
 {"id": "AMD-V2-06", "slot": "supplied_by_human.rulings_holder", "kind": "SUPPLIED by PI (by role); transfer PENDING_RECEIPT",
  "before": {"value": None, "status": "UNDEMONSTRATED", "ledger": "AMD-V1-07"},
  "after": {"value": {"role": "19C program coordinator", "name": None, "non_authorship": "asserted by PI, verified by neither coordinator nor agent"},
            "transfer": tr3["status"], "receipt_hash": tr3["receipt_hash"]},
  "cause": "PI ruling 4; coordinator preamble item 2 (handover is out of band, PENDING RECEIPT until the holder's receipt hash is written)",
  "source": W3REF("ruling 4, line 21; preamble item 2, line 65"), "corroboration": ref(f"{A5W3}/transfer_record.json", "status, receipt_hash, holder.authorship_check")},
 {"id": "AMD-V2-07", "slot": "supplied_by_human.tns_credentials", "kind": "BLOCKED",
  "before": {"value": None, "status": "UNDEMONSTRATED", "ledger": "AMD-V1-08"},
  "after": {"value": None, "status": "BLOCKED", "request_date": "2026-09-16", "checked_utc": "2026-09-16T20:13:38Z (presence test only)"},
  "cause": "PI ruling 5 (use TNS_API_KEY if present, else BLOCKED with request date); coordinator preamble item 1: key absent",
  "source": W3REF("ruling 5, line 22; preamble item 1, line 64")},
 {"id": "AMD-V2-08", "slot": "decision_epoch", "kind": "RATIFICATION (reaffirmed) with strata",
  "before": {"value": {"primary": "first alert", "secondary": "night 3"}, "status": "RATIFIED", "ledger": "AMD-V1-02"},
  "after": {"value": {"primary": "first alert", "secondary": "night 3"}, "status": "RATIFIED", "strata": "S0, S1, S2 reported and excluded"},
  "disagreement": "bands_FROZEN.md section 3 declares S2 (cohort objects with pre-boundary forced flux) 'counted and reported ... not removed from the cohort'; ruling 6 says S0, S1 and S2 'stay reported and excluded'. S0 and S1 are outside the cohort by definition; S2 is not. Not reconciled: excluding S2 changes a frozen definition and would need a new hashed band registration (bands section 8). S2 is currently uncountable (needs PPDB), so no count moves today.",
  "cause": "PI ruling 6", "source": W3REF("ruling 6, line 23")},
 {"id": "SU-V2-01", "slot": "tool_inventory (fold-in)", "kind": "SLOT UPDATE: wave-3 functional recount on real Rubin alerts",
  "before": {"rubin_verified": "0 of 25 (structural census, wave 1)"},
  "after": {"rubin_functional": ax4["value"]["counts_by_group_and_disposition"]["all"], "qualifier": "Fink LSST API JSON rows with v11_1 field names, not Avro packets"},
  "cause": "wave-3 brief agent 4 assignment (recount after the band, apply the ratified Fink remapping); rule D", "source": W3REF("Assignments, Agent 4"),
  "record": ref(f"{A4W3}/tool_coverage_axis.json")},
 {"id": "SU-V2-02", "slot": "candidates / exposure_key (fold-in)", "kind": "SLOT UPDATE: wave-3 cohort counts",
  "after": {"O_merged": cc["w3-02"]["value"], "S1": cc["w3-05"]["value"]["S1_total"], "U": cc["w3-06"]["value"], "ppdb": "NOT RELEASED", "antares_prior_position_leak": "193/9000"},
  "cause": "wave-3 brief agent 1 assignment (finish the cohort)", "source": W3REF("Assignments, Agent 1"), "record": ref(f"{A1W3}/rubin_cohort_count.json")},
 {"id": "PENDING-V2-01", "slot": "label_source; positive_supply; negative_supply; PI re-ratification (ruling 1)", "kind": "PENDING input",
  "what": "wave-3 agent 2: track one BLOCKED (TNS); track two census of 2026 TNS spectroscopic classifiers (monthly throughput P per programme) and the truth cost (nights and spectra per night to reach 485 labelled cohort objects at each plausible purity)",
  "cause": "wave-3 brief agent 2 assignment; coordinator has not delivered results", "source": W3REF("Assignments, Agent 2")},
]
for e in v2e:
    e["manifest_version"] = "v2"
    e["recorded_utc"] = T
    e["applied_to"] = "domain_manifest_v2_DRAFT.json (NOT FROZEN)"
led["v2_entries"] = v2e
led["v2_entries_state"] = "DRAFT: applied to v2 DRAFT; v2 not frozen; PENDING-V2-01 open"
led["completeness"] = (led["completeness"].split(" v2 entries")[0] +
    " v2: wave-3 PI rulings 1-6 each have an entry (budget, S, cost of action, delta override, graph ratification, rulings holder, TNS, decision epoch), plus two fold-ins and one PENDING input (agent 2). v2 entries are DRAFT until v2 freezes.")
dump(led, f"{OUT}/amendment_ledger.json")
assert canonical_sha(load(f"{OUT}/amendment_ledger.json")["v1_entries"]) == led["v1_entries_canonical_sha256"]
oplog.log("9", "amendment_ledger.json: v2 DRAFT entries appended (v1 entries unchanged; canonical sha re-verified)", [f"{OUT}/amendment_ledger.json"])

# ---------------------------------------------------------------- v2 draft manifest
m = copy.deepcopy(v1)
m["manifest_version"] = "v2 DRAFT"
m["draft_status"] = "NOT FROZEN. Awaiting wave-3 agent 2 (PENDING-V2-01). See v2_freeze_pending.md."
m["governing_brief"] = ref(W3)
m["derived_from"] = {"manifest": f"{OUT}/domain_manifest_v1.json", "frozen_hash": v1["frozen_hash"]}
m["inputs_state"] = "v1 plus wave-3 PI rulings 1-6 and the wave-3 counts landed from agent 1 (cohort, axes) and agent 4 (tool recount); agent 2 wave-3 PENDING"
m["frozen_utc"] = None
m["frozen_hash"] = ""
m["amendment_ledger"] = {"path": f"{OUT}/amendment_ledger.json", "v1_entries_canonical_sha256": led["v1_entries_canonical_sha256"],
                         "v2_entries": [e["id"] for e in v2e], "v2_entries_canonical_sha256_draft": canonical_sha(v2e)}

# delta
d = m["delta"]
lit = {"value": 0.018, "status": "DERIVED (literature prior, carried)", "provenance": d["provenance"], "resolution_warning": d["resolution_warning"],
       "candidates_listed": d.pop("candidates_listed"), "disagreements": d.pop("disagreements")}
m["delta"] = {
 "value": 0.05,
 "literature_prior": lit,
 "carry_both": "every P7 table reports delta 0.05 and 0.018 side by side (ruling 2)",
 "provenance": prov(
   "smallest improvement in committed-set purity (precision at k) that would change which selector the programme runs, set from the PI's cost of action",
   "PANEL_BRIEF_WAVE3.md sha256 " + W3SHA + " ruling 2 lines 14-19 (cost of switching a production selector = engineer weeks; 0.018 below its own unpaired resolution)",
   "the programme's follow-up allocation decision, one committed set of k=8 per night; applies on the purity scale only if A1 fixes precision at k as primary (delta_slot metric_caveat)",
   "literature prior 0.018 (arXiv:2401.15167 Table 6), carried beside; its unpaired MDE about 0.045; wave-2 PRE-I1 calibration MDE 0.032 on BTS binding nights",
   "a PI restatement of the switching cost, or a P7 power record whose MDE at the budgeted N exceeds 0.05 (closes at P7), or A1 preregistering a primary metric other than committed-set purity, which would require restating 0.05 on that scale"),
 "status": "OVERRIDDEN",
 "override_reason": "AMD-V2-04, PI ruling 2: switching a production selector costs engineer weeks, and 0.018 sits below its own unpaired resolution; 0.018 kept as literature prior and carried through every P7 table.",
 "calibration_context": {"record": ref(f"{A4W3}/power_calibration_delta005.json"),
   "primary_E1_binding_nights": {"mde": 0.0322, "n_min_at_0.05": 26, "ruling_at_0.05": "RESOLVABLE", "n_min_at_0.018": 196, "ruling_at_0.018": "CLOSE_UNRESOLVABLE"},
   "status": "PRE-I1 CALIBRATION on BTS (contamination FAIL); not P7"},
 "planning_thresholds": {"objects_N_min_range": {"0.018": [485, 12855], "0.05": [63, 1666]}, "nights_N_min_range": {"0.018": [40, 1515], "0.05": [6, 197]},
                         "source": f"{A1W3}/rubin_cohort_count.json w3-09 (PLANNING-ONLY)"},
 "open_questions": ["cost of action is asymmetric (missed rare event >= 100 slots vs wrong routine commitment 1 slot); precision at k on the committed set does not price misses. The A1 primary metric is not preregistered. Listed for A1, not reconciled here."],
 "source_records": [ref(W3, "ruling 2"), ref(f"{A4W3}/power_calibration_delta005.json"), ref(f"{A1W3}/planning_mde_bracket_w3.csv")],
 "override_invitation": "Override invitation: accept 0.05, or state a different value with its cause; the literature prior 0.018 stays carried either way.",
}

# S
m["S"]["provenance"]["source"] += "; PANEL_BRIEF_WAVE3.md sha256 " + W3SHA + " ruling 1 line 13 ('S is computed at R1')"
m["S"]["status_note"] = "Budget now SUPPLIED (1,000 arm cells hard cap + 200 engineering hours, AMD-V2-01). S stays UNDEMONSTRATED until R1 measures cost per workflow (AMD-V2-02)."
m["S"]["planning_arithmetic_not_S"] = {
  "cell_definition": "one cell = one subject x one arm x one round (astronomy/agent5_resolution_replay/d5_inputs.json d5-budget human_must_supply)",
  "r1_reserve_cells": "3 (r1_spec.md section 6)",
  "rounds_affordable_if_7_subjects_x_2_agent_arms": "floor((1000-3)/14) = 71",
  "rounds_affordable_if_1_subject_x_2_agent_arms": "floor((1000-3)/2) = 498",
  "compare": "planning N_min at delta 0.05: 6-197 nights or 63-1,666 objects; calibration N_min 26 binding nights",
  "status": "PLANNING-ONLY; the mechanical composition arm consumes no subject cells; hours per workflow unmeasured"}
m["S"]["gates"] = ["ruling 1: no Rubin-era paid work starts without re-ratification against this wave's measured label supply (PENDING-V2-01)"]
m["S"]["source_records"].append(ref(W3, "ruling 1"))

# supplied fields
m["supplied_by_human"] = {
 "budget": "SUPPLIED (AMD-V2-01): 1,000 agent arm cells for the calibration phase, hard cap, plus 200 engineering hours; no Rubin-era paid work without re-ratification against this wave's measured label supply",
 "cost_of_action": "SUPPLIED (AMD-V2-03): one spectrum = 0.5 h P60-class time; wrong routine commitment = 1 slot; missed rare event >= 100 slots, asymmetric; delta override 0.05 (AMD-V2-04)",
 "rulings_holder": f"SUPPLIED by role (AMD-V2-06): 19C program coordinator, non-authorship asserted by PI and unverified; transfer {tr3['status']}, receipt_hash empty",
 "tns_credentials": "BLOCKED (AMD-V2-07): TNS_API_KEY absent, checked 2026-09-16T20:13:38Z; request date 2026-09-16",
}
m["d5_inputs"] = [
 {"id": "d5-budget", "value": {"agent_arm_cells_hard_cap": 1000, "engineering_hours": 200}, "status": "SUPPLIED",
  "provenance": prov("hours or cells the programme can spend on this benchmark (calibration phase)", "PANEL_BRIEF_WAVE3.md sha256 " + W3SHA + " ruling 1 line 13",
                     "the human programme; arm cells = subject x arm x round", "the unfilled wave-2 placeholder (AMD-V1-04)",
                     "a cell ledger at R1 onward that exceeds 1,000 cells, or any Rubin-era paid run logged before re-ratification, would show the cap was not held")},
 {"id": "d5-cost-of-action", "value": {"one_spectrum_h_P60": 0.5, "wrong_routine_commitment_slots": 1, "missed_rare_event_slots_min": 100, "asymmetric": True}, "status": "SUPPLIED",
  "provenance": prov("cost of a follow-up slot, of a wrong commitment and of a missed rare event", "PANEL_BRIEF_WAVE3.md sha256 " + W3SHA + " ruling 2 lines 14-17",
                     "the programme's own follow-up allocation", "the delta prior 0.018 that this overrides (AMD-V2-04)",
                     "a PI restatement that differs, or an A1 metric whose loss weights differ from 1 vs >= 100 slots")},
 {"id": "d5-rulings-holder", "value": {"role": "19C program coordinator", "name": None}, "status": "SUPPLIED (role); custody PENDING_RECEIPT",
  "provenance": prov("a person who wrote neither the skill nor any case and holds RULINGS_SEALED.csv and the polarity maps",
                     "PANEL_BRIEF_WAVE3.md sha256 " + W3SHA + " ruling 4 line 21; astronomy/wave3/agent5_integrity/transfer_record.json sha256 " + sha(f"{A5W3}/transfer_record.json"),
                     "the two replay suites (20 and 38 cases)", "procedural seal held by the orchestrating party (SYNTHESIS.md section 10)",
                     "transfer_record.json receipt_hash filled and matching sha256 of the returned RECEIPT_TEMPLATE.txt would resolve custody; an authorship record naming the holder would falsify eligibility")},
 {"id": "d5-tns-credentials", "value": None, "status": "BLOCKED",
  "provenance": prov("an authenticated TNS account for per-object classification reports", "PANEL_BRIEF_WAVE3.md sha256 " + W3SHA + " ruling 5 line 22; preamble item 1 line 64",
                     "7,843 BTS labels and all Rubin-era classifications", "public archived TNS pages (partial)",
                     "a TNS_API_KEY present in the environment on a later presence test would unblock track one")},
]

# decision_epoch
AMD = v2e[7]["disagreement"]
de = m["decision_epoch"]
de["status_note"] = "Ratified at v1 (AMD-V1-02) and reaffirmed by PI ruling 6 (AMD-V2-08) with strata S0, S1, S2 reported and excluded."
de["provenance"]["source"] += "; reaffirmed PANEL_BRIEF_WAVE3.md sha256 " + W3SHA + " ruling 6 line 23"
de["strata"] = {
 "S0": {"definition": "first detection in [survey start 2026-06-29T12:00, admission boundary 2026-07-01T00:00) (bands section 3)", "count": "112,990 ANTARES loci (wave 2 C2)", "in_cohort": False},
 "S1": {"definition": "straddlers: a DIASource detection before the boundary and one at or after it", "count": cc["w3-05"]["value"]["S1_total"], "in_cohort": False},
 "S2": {"definition": "cohort objects with pre-boundary forced flux S/N >= 5", "count": "UNDEMONSTRATED (needs PPDB, not released)", "in_cohort_per_frozen_bands": True, "per_ruling_6": "excluded"},
 "disagreement": v2e[7]["disagreement"],
}
de["source_records"].append(ref(W3, "ruling 6"))

# tool_inventory
ti = m["tool_inventory"]
ti["rubin_functional_recount_w3"] = {
 "record": ref(f"{A4W3}/tool_coverage_axis.json"),
 "counts": ax4["value"]["counts_by_group_and_disposition"],
 "per_tool": {t["tool"]: {"disposition": t["disposition"], "passes": t.get("passes"), "alerts_run": t.get("alerts_run"), "rubin_counterparts_after_remap": t["rubin_counterparts_after_remap"]} for t in ax4["value"]["per_tool"]},
 "packet_format_qualifier": ax4["packet_format_qualifier"],
 "remap_consistency": "agent 4's recount protocol applies exactly AMD-V1-03 (ATAT, Astromer1, Astromer2 -> Fink_EarlySNIa_RF, Fink_SLSN_RF; no other row) - MATCH",
 "note": "wave-1 structural counts (value.summary) are unchanged; the recount is functional and sits beside them. Both Fink RFs FAIL at emit (default output on 10/10), so the structural check (a) after AMD-V1-03 does not hold functionally.",
 "disagreements": ["AstroM3: wave-1 UNAVAILABLE (no weights) vs weights public on HF rev 8904ed33 (agent 4 w3 disagreement 1)",
                   "preamble item 5 'no substitute format is improvised' vs runs on JSON rows (listed in axis ledger v2)"],
}
ti["source_records"].append(ref(f"{A4W3}/tool_coverage_axis.json"))

# label_source
ls = m["label_source"]
ls["wave3"] = {"tns_track_one": "BLOCKED (AMD-V2-07)", "pending": "PENDING-V2-01: agent 2 census of 2026 TNS spectroscopic classifiers and truth cost (not landed)",
               "ratification_gate": "ruling 1: re-ratification against this wave's measured label supply before any Rubin-era paid work",
               "observation": "the brief prices truth at 485 labelled cohort objects, the lower object bracket at delta 0.018; at the overridden delta 0.05 the planning lower bracket is 63 (upper 1,666). Listed, not reconciled."}
ls["status_note"] = "UNDEMONSTRATED (v1, wave-2 agent 2). Wave-3 agent 2 inputs PENDING."

# exposure_key
ek = m["exposure_key"]
ek["wave3_additions"] = {
 "prior_position_leak": "193 of 9,000 sampled cohort ids have an ANTARES alert at the same position before the boundary (gaps 12-2,943 d; 3 within 60 d): public position history before the cutoff; listed as a leak",
 "ppdb": "NOT RELEASED as of 2026-09-16; cohort O = 1,937,669 is an upper bound (PPDB-only detections could only lower it)",
 "rubin_first_detection_field": "Fink serves r:firstDiaSourceMjdTai as null for 8,986/8,986 sampled ids; Rubin-side first time not publicly obtainable (agent 1 AM7)",
 "tns": "BLOCKED; label public dates remain bracketed",
 "record": ref(f"{A1W3}/rubin_cohort_count.json", "w3-07, w3-08")}

# candidates
c = m["candidates"][0]
c["cohorts"]["prospective_counts_w3"] = {"O_merged": cc["w3-02"]["value"], "alerce_oids": cc["w3-01"]["value"], "S1": cc["w3-05"]["value"]["S1_total"],
                                         "one_detection_share": cc["w3-04"]["value"]["S3_one_detection_share_oids"], "U": cc["w3-06"]["value"], "cohort_nights": 9,
                                         "record": ref(f"{A1W3}/rubin_cohort_count.json")}
c.pop("p4_state_at_v1", None)
c["p4_state_v2_draft"] = f"no ruling; axis ledger {axv2}: preconditions (a) and (c) UNMET, (b) CLEARED (verified by agent 3); validator FAIL stands"
c["source_records"].append(ref(axv2))

# graph
m["graph_escalations"] = [{"edge": "R1 -> I1 (and D5 -> R1)", "state": "RATIFIED as staged (PI ruling 3)",
  "consequence": "wave-2 compositions stay PRE-I1 CALIBRATION; the I1 designation waits for R1 plus PI ratification; graph edges unweakened",
  "ledger": ["ESC-V1-01", "AMD-V2-05"], "source": ref(W3, "ruling 3")}]

# d5 disposition (draft)
m["d5_disposition"] = {
 "stage": "D5 ratification",
 "frozen_and_hashed": "UNDEMONSTRATED (draft, not frozen)",
 "every_slot_ratified_or_overridden": "FAIL",
 "per_slot": {"tau": "DERIVED", "k": "RATIFIED", "label_source": "UNDEMONSTRATED (PENDING agent 2)", "exposure_key": "DERIVED",
              "tool_inventory": "OVERRIDDEN (three Rubin counterpart rows)", "delta": "OVERRIDDEN (0.05; prior 0.018 carried)",
              "S": "UNDEMONSTRATED (computed at R1)", "subject_set": "DERIVED", "decision_epoch": "RATIFIED"},
 "disposition": "UNDEMONSTRATED: tau, exposure_key and subject_set still carry no PI ruling; label_source awaits agent 2 and the PI's re-ratification; S awaits R1.",
}
m["disagreements_v2"] = [
 AMD,
 "wave-3 preamble item 5 vs agent 4's JSON-row runs (tool_inventory, axis ledger v2)",
 "truth cost priced at 485 objects (delta 0.018 bracket) while delta is overridden to 0.05 (label_source.wave3.observation)",
 "tool_coverage_axis.json population '158 alert runs' vs run_log 160 (158 + 2 voided)",
]
m["completeness"] = ("v2 DRAFT: v1 plus wave-3 rulings 1-6 (AMD-V2-01..08) and fold-ins from agent 1 (cohort, strata, exposure leak, PPDB) and agent 4 (functional tool recount, "
                     "delta 0.05 calibration). Not covered: wave-3 agent 2 (PENDING-V2-01); PI rulings on tau, exposure_key, subject_set; R1 (S). Not frozen.")
dump(m, f"{OUT}/domain_manifest_v2_DRAFT.json")
oplog.log("10", f"domain_manifest_v2_DRAFT.json written (NOT FROZEN, frozen_hash empty; draft content canonical sha={manifest_hash(m)})",
          [f"{OUT}/domain_manifest_v2_DRAFT.json", f"{OUT}/amendment_ledger.json"])
