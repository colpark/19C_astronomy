#!/usr/bin/env python3
"""Axis ledger v2 against the FROZEN bands (bands_FROZEN.md, delta 0.018). Never re-bands.
0.05 thresholds (PLANNING-ONLY, agent 1 w3-09) are reported beside. P4 preconditions are checked here;
precondition (b) is verified from timestamps and hashes, not taken from agent 4's claim."""
import json, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa
import oplog
FINAL = "--final" in sys.argv
A2W3 = "astronomy/wave3/agent2_measured_labels"
HANDOFF = {"tns_census_2026.json": "c7b035f04fa77b41386555ba1258fcc6624f9fc1b5354aa913fd20a78b7eeaa9", "supply_P_per_month.json": "b028de4a80b30d875358f1594c4a2b6fc3ceda7e4bfadb958debc56c4527b2ce", "truth_cost.json": "53f229b3deb4137781ce06c80016bdf54dde506e80f06024d129d4feb0b81c6e", "truth_cost_table.csv": "8eee9f94b55d5ccad10e32cf721073d729865c442aff662661117a0f703b09a3", "label_source_slot.json": "fdae64921d6749e466932d13ffd0aa4e14359b0a946a31b32bacf9a97ce83719"}

A1W3 = "astronomy/wave3/agent1_cohort_finish"
A4W3 = "astronomy/wave3/agent4_tool_recount"
A1W2 = "astronomy/wave2/agent1_rubin_bands"
assert sha(BANDS) == BANDS_SHA

def ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))

# ------------------------------------------------ precondition (b) verification
chk = {}
# band hash time from agent 1 wave-2 log
w2log = open(rp(f"{A1W2}/order_of_operations.log")).read().splitlines()
band_line = [l for l in w2log if "bands_FROZEN.md hashed" in l][0]
band_t = ts(band_line.split(" | ")[0])
chk["band_hash"] = {"sha256_now": sha(BANDS), "sha256_logged": re.search(r"bands_FROZEN.md sha256=([0-9a-f]{64})", band_line).group(1),
                    "logged_utc": band_line.split(" | ")[0],
                    "file_mtime_utc": datetime.datetime.fromtimestamp(os.path.getmtime(rp(BANDS)), datetime.timezone.utc).isoformat(),
                    "file_mode": oct(os.stat(rp(BANDS)).st_mode & 0o777)}
chk["band_hash"]["match"] = chk["band_hash"]["sha256_now"] == chk["band_hash"]["sha256_logged"] == BANDS_SHA

# agent 4 recount
a4log = open(rp(f"{A4W3}/order_of_operations.log")).read().splitlines()
def logged(logl, fname):
    out = []
    for l in logl:
        for mm in re.finditer(re.escape(fname) + r" sha256=([0-9a-f]{64})", l):
            out.append((l.split(" | ")[0], mm.group(1)))
    return out
prot = logged(a4log, "recount_protocol_FROZEN.md")
runlog_logged = logged(a4log, "run_log.jsonl")
axis_logged = logged(a4log, "tool_coverage_axis.json")
seal_logged = logged(a4log, "sealed/alert_ids_SEALED_v2.json")
rows = [json.loads(l) for l in open(rp(f"{A4W3}/run_log.jsonl")) if l.strip()]
starts = sorted(ts(r["start_utc"]) for r in rows)
alert_rows = [r for r in rows if r["alert_id"] not in ("PRECHECK", "LOAD")]
am2_t = ts("2026-09-16T21:15:20Z")  # AM2 recorded (agent 4 log step 11c)
voided = [r for r in alert_rows if r["tool"] == "GHOST" and r["status"] == "error:infer" and ts(r["start_utc"]) < am2_t]
def passes(tool):
    rr = [r for r in alert_rows if r["tool"] == tool and r not in voided]
    return sum(1 for r in rr if r["status"] == "ok" and r.get("non_default")), len(rr)
axis4 = load(f"{A4W3}/tool_coverage_axis.json")
pt = {t["tool"]: t for t in axis4["value"]["per_tool"]}
recomputed = {t: passes(t) for t in pt}
mism = [t for t in pt if pt[t]["alerts_run"] and (recomputed[t][0] != pt[t]["passes"] or recomputed[t][1] != pt[t]["alerts_run"])]
chk["tool_recount"] = {
 "protocol_sha256_now": sha(f"{A4W3}/recount_protocol_FROZEN.md"), "protocol_logged": prot,
 "sealed_ids_v2_sha256_now": sha(f"{A4W3}/sealed/alert_ids_SEALED_v2.json"), "sealed_ids_v2_logged": seal_logged,
 "run_log_sha256_now": sha(f"{A4W3}/run_log.jsonl"), "run_log_last_logged": runlog_logged[-1],
 "axis_sha256_now": sha(f"{A4W3}/tool_coverage_axis.json"), "axis_logged": axis_logged,
 "run_log_rows": len(rows), "alert_runs": len(alert_rows), "load_rows": sum(r["alert_id"] == "LOAD" for r in rows),
 "precheck_rows": sum(r["alert_id"] == "PRECHECK" for r in rows),
 "earliest_run_start_utc": starts[0].isoformat(), "latest_run_start_utc": starts[-1].isoformat(),
 "rows_starting_at_or_before_band_hash": sum(1 for s in starts if s <= band_t),
 "rows_starting_at_or_before_protocol_freeze": sum(1 for s in starts if s <= ts(prot[0][0])),
 "rows_with_after_band_hash_not_true": sum(1 for r in rows if r.get("after_band_hash") is not True),
 "rule_D_cap_250_respected": len(alert_rows) <= 250,
 "ghost_voided_runs_AM2": len(voided),
 "per_tool_passes_recomputed_vs_axis_mismatches": mism,
 "tools_with_disposition": len(pt),
}
tr = chk["tool_recount"]
b_ok = (chk["band_hash"]["match"] and tr["protocol_sha256_now"] == prot[-1][1] and tr["run_log_sha256_now"] == tr["run_log_last_logged"][1]
        and tr["axis_sha256_now"] == axis_logged[-1][1] and tr["sealed_ids_v2_sha256_now"] == seal_logged[-1][1]
        and tr["rows_starting_at_or_before_band_hash"] == 0 and tr["rows_starting_at_or_before_protocol_freeze"] == 0
        and tr["rows_with_after_band_hash_not_true"] == 0 and not mism and tr["tools_with_disposition"] == 25)

# agent 1 wave-3 counts after band hash
a1log = open(rp(f"{A1W3}/order_of_operations.log")).read().splitlines()
cp = logged(a1log, "count_protocol_w3_FROZEN.md"); sealw3 = logged(a1log, "sealed/rubin_counts_w3_SEALED.json")
chk["cohort_counts_w3"] = {"count_protocol_logged": cp, "count_protocol_sha256_now": sha(f"{A1W3}/count_protocol_w3_FROZEN.md"),
                           "sealed_counts_logged": sealw3, "sealed_counts_sha256_now": sha(f"{A1W3}/sealed/rubin_counts_w3_SEALED.json"),
                           "protocol_after_band_hash": ts(cp[0][0]) > band_t}
chk["cohort_counts_w3"]["match"] = (chk["cohort_counts_w3"]["count_protocol_sha256_now"] == cp[-1][1]
                                    and chk["cohort_counts_w3"]["sealed_counts_sha256_now"] == sealw3[-1][1])
b_ok = b_ok and chk["cohort_counts_w3"]["match"] and chk["cohort_counts_w3"]["protocol_after_band_hash"]

# ------------------------------------------------ axes
led1 = load(f"{A1W3}/axis_ledger_rubin_v2.json")
ax = {a["axis"]: a for a in led1["axes"]}
T05 = {"objects": [63, 1666], "nights": [6, 197]}
T018 = {"objects": [485, 12855], "nights": [40, 1515]}

def carry(name, extra):
    a = json.loads(json.dumps(ax[name]))
    a["band_frozen_delta_0p018"] = a.pop("band_frozen_delta_0p018")
    a.update(extra)
    a["source_ledger"] = f"{A1W3}/axis_ledger_rubin_v2.json sha256 {sha(A1W3 + '/axis_ledger_rubin_v2.json')}"
    return a

axes = [
 carry("positive_supply", {"thresholds_reported_beside_delta_0p05_PLANNING_ONLY": {"CLOSE_if": "O < 63 and M_obs < 6", "PROCEED_if": "P >= 1 and (L >= 1666 or M_sc >= 197)", "not_a_band": True},
       **({"agent2_wave3": "landed and verified: cohort measured non-bot STRONG 0 on 13 readable of 627 captures (UNDEMONSTRATED, not zero); 13 typed cohort objects, classifier unknown; 2026 TNS throughput lower bounds only (non-bot spectroscopic units Jan-Sep >= 161, all objects, not cohort); P remains uncomputable"} if FINAL else {"pending": "wave-3 agent 2 (census of 2026 TNS spectroscopic classifiers and truth cost) has not landed; TNS track one BLOCKED (wave-3 preamble item 1). The census gives programme throughput, not per-object measured labels, unless it also delivers cohort crossmatches."})}),
 carry("negative_supply", {"thresholds_reported_beside_delta_0p05_PLANNING_ONLY": {"CLOSE_if": "O < 63 and M_obs < 6", "PROCEED_if": "Ng >= 1 and (L >= 1666 or M_sc >= 197)", "not_a_band": True},
       **({"agent2_wave3": "no negative-class (CV/AGN) measured count on cohort objects; 1 typed CV among the 13 existence matches, classifier unknown; Ng uncomputable"} if FINAL else {"pending": "as positive_supply"})}),
 carry("contamination_exposure", {"thresholds_reported_beside_delta_0p05_PLANNING_ONLY": {"PROCEED_if": "every subject has a published cutoff and E-labelled >= 1666 (or 197 usable nights)", "not_a_band": True},
       "band_note_agent3": "ESCALATE holds at either delta: Gemini 3.1 Pro (preview) has no published cutoff and the subject set is unratified (manifest subject_set DERIVED)."}),
 {
  "axis": "tool_coverage",
  "disposition": "PASS (counted after the band hash; verified by agent 3)",
  "band_frozen_delta_0p018": "ESCALATE",
  "band_derivation": ("bands_FROZEN.md section 6 tool_coverage. CLOSE needs no FM/deep channel accepting inputs the v11.1 packet carries: CATS "
                      "accepted them (5/10 non-default) -> not CLOSE. PROCEED needs >= 1 FM/deep channel verified on Rubin alerts AND >= 1 "
                      "classical counterpart verified for each such channel: CATS's Rubin counterparts (Fink_EarlySNIa_RF, Fink_SLSN_RF; "
                      "unchanged by AMD-V1-03, which re-mapped ATAT/Astromer1/Astromer2) both FAIL at emit on 10/10 -> not PROCEED. "
                      "Hence ESCALATE. The reading is the same whether or not JSON rows count as 'verified on Rubin alerts' (if they do "
                      "not, no FM channel is verified, and CLOSE still does not fire because CATS accepts the inputs)."),
  "thresholds_reported_beside_delta_0p05_PLANNING_ONLY": "tool_coverage band has no delta-dependent threshold; identical at 0.05",
  "value": {"counts_by_group_and_disposition": axis4["value"]["counts_by_group_and_disposition"],
            "pass_tools": {"CATS (FM/deep)": "5/10", "GHOST (classical, counterpart of AstroCLIP which is UNDEMONSTRATED)": "3/8 valid (2 voided under AM2)"},
            "packet_format_qualifier": axis4["packet_format_qualifier"],
            "remapped_rows_after_AMD-V1-03": {t: {"rubin_counterparts": pt[t]["rubin_counterparts_after_remap"], "disposition": pt[t]["disposition"]} for t in ("ATAT", "Astromer1", "Astromer2")}},
  "disagreements": [
    "wave-3 coordinator preamble item 5: 'If lsst v11_1 packets cannot be retrieved publicly ... no substitute format is improvised'. Agent 4 ran on Fink LSST API JSON rows carrying v11_1 field names (Avro returns HTTP 400) and carries a qualifier. Whether JSON rows are an improvised substitute format is listed, not reconciled; the band reading does not depend on it.",
    "agent 4 disagreement 12: Rubin off sky since 2026-07-14, cohort objects have 1-3 diaSources, so the Fink RF FAIL at emit measures the stream as much as the tools.",
    "tool_coverage_axis.json population says 158 alert runs logged; run_log.jsonl has 160 alert-run rows (158 plus 2 voided GHOST runs); REPORT.md says 160.",
    "AstroM3: wave-1 inventory UNAVAILABLE (no weights); weights now public on HF (AstroMLCore rev 8904ed33). Wave-1 count not changed."],
  "provenance": [f"{A4W3}/tool_coverage_axis.json sha256 {tr['axis_sha256_now']}", f"{A4W3}/run_log.jsonl sha256 {tr['run_log_sha256_now']}"],
 },
 carry("cluster_structure", {"thresholds_reported_beside_delta_0p05_PLANNING_ONLY": "same band at 0.05: every broker count >= 1666 and >= 63"}),
 carry("split_integrity", {"thresholds_reported_beside_delta_0p05_PLANNING_ONLY": "same band at 0.05: O minus listed objects >= 1666"}),
 carry("unprocessable_units", {"thresholds_reported_beside_delta_0p05_PLANNING_ONLY": "same band at 0.05 (U = 0)"}),
]

a2 = None
if FINAL:
    for f, h in HANDOFF.items():
        assert sha(f"{A2W3}/{f}") == h, f"handoff hash mismatch {f}"
    cen = {r["id"]: r for r in load(f"{A2W3}/tns_census_2026.json")}
    sup = load(f"{A2W3}/supply_P_per_month.json")
    lab = load(f"{A2W3}/label_source_slot.json")
    rc = lab["value"]["rubin_cohort"]
    tierA_ok = sup["fetch"]["status_by_tier"].get("A:ok"); tierA_err = sup["fetch"]["status_by_tier"].get("A:http_error")
    class_split = any(k in json.dumps(cen["w3a2-c-cohort-measured-strong"]).lower() for k in ("posa", "posb", "\"neg\""))
    a2 = {"handoff_hashes_verified": True, "handoff": HANDOFF,
          "cohort_measured_nonbot_strong": cen["w3a2-c-cohort-measured-strong"]["value"],
          "cohort_measured_population": cen["w3a2-c-cohort-measured-strong"]["population"],
          "tier_A_cohort_captures_readable": tierA_ok, "tier_A_cohort_captures_http_error": tierA_err,
          "cohort_existence_typed_moderate": cen["w3a2-c-cohort-existence"]["value"], "existence_classifier": "UNDEMONSTRATED (12 archived pages 404, 1 403)",
          "slot_measured_nonbot_status": rc["measured_nonbot_status"],
          "posA_neg_class_split_present": class_split,
          "track_one": lab["value"]["track_one"]["status"],
          "reading": ("P and Ng are not computable: 0 STRONG measured non-bot reports on cohort objects rests on 13 readable captures out of 627 tier-A cohort-matched objects (614 HTTP errors), "
                      "so it is UNDEMONSTRATED, not zero (global refusal 11); the 13 typed cohort objects have unknown classifiers and fail the bands section 4 non-bot-reporter requirement; "
                      "no posA/neg split exists. Monthly 2026 throughput is lower bounds over all TNS objects, not cohort labels.")}
pre = {
 "a": {"text": "every one of the seven axes carries a number for the Rubin cohort (bands_FROZEN.md section 7)",
       "state": "UNMET", "why": ("positive_supply and negative_supply: measured P and Ng UNDEMONSTRATED (TNS BLOCKED; agent 2 wave 3: 0 STRONG on 13 readable of 627 cohort captures, 13 typed with classifier unknown, no class split; verified by agent 3 from the handoff files)" if FINAL else "positive_supply and negative_supply: measured P and Ng UNDEMONSTRATED (TNS BLOCKED; wave-3 agent 2 pending)")},
 "b": {"text": "each axis's band hashed before its count; for tool_coverage a recount after the band hash",
       "state": "CLEARED" if b_ok else "UNMET",
       "verified_by": "agent 3 from logs, file hashes and run_log.jsonl timestamps (see precondition_b_verification)",
       "limits": "timestamps are self-logged by the agents and file mtimes are from the same host; consistency is verified, independent notarisation is not. The supply axes have no count, so (b) is vacuous for them and they fall under (a)."},
 "c": {"text": "label source ratified at D5, or P and Ng computed from measured labels (section 4)",
       "state": "UNMET", "why": ("label_source slot UNDEMONSTRATED (agent 2 wave 3: BTS SNIascore bound [954, 2057], 5,815 unresolved; Rubin cohort measured supply UNDEMONSTRATED); no PI ratification yet; the re-ratification ruling 1 requires is open, with its inputs now in PI_rerat_packet.md; P and Ng not computed" if FINAL else "label_source slot UNDEMONSTRATED in v1 and not ratified by any wave-3 ruling (ruling 1 requires re-ratification against this wave's measured label supply, which is agent 2's pending output); P and Ng not computed")},
}
unmet = [k for k, v in pre.items() if v["state"] != "CLEARED"]
ledger = {
 "candidate": led1["candidate"],
 "branch": "prediction",
 "version": ("v2 FINAL against frozen bands (agent 3, wave 3, after agent 2 handoff)" if FINAL else "v2 against frozen bands (agent 3, wave 3)"),
 "bands": f"{BANDS} sha256 {BANDS_SHA} (delta 0.018; never re-banded here)",
 "delta_note": "bands frozen at delta 0.018 (literature prior); PI override 0.05 thresholds reported beside each axis as PLANNING-ONLY (agent 1 w3-09, planning_mde_bracket_w3.csv). Re-banding at 0.05 would be a new hashed registration.",
 "planning_thresholds": {"delta_0.018_frozen": T018, "delta_0.05_beside": T05, "source": f"{A1W3}/rubin_cohort_count.json id w3-09"},
 "sealed_counts": led1["sealed_counts"],
 "ruling": None,
 "ruling_refused_because": [f"precondition ({k}) {pre[k]['state']}: {pre[k].get('why', '')}" for k in unmet],
 "p4_preconditions": pre,
 "precondition_b_verification": chk,
 "precondition_a_verification_agent2": a2,
 "binding_axis": ("positive_supply at measured labels (the unmet precondition needing an external input and survey time): frozen bands need "
                  "L >= 12,855 or M_sc >= 1,515; beside, at delta 0.05, 1,666 or 197; measured labels unread (TNS BLOCKED), Rubin off sky since 2026-07-14"),
 "combination_preview_not_a_ruling": ("with the present readings no axis is in CLOSE (O = 1,937,669 >= 485), and contamination_exposure and tool_coverage "
                                      "are in ESCALATE, so section 7 cannot yield PROCEED even if (a) and (c) clear with the subject set unchanged; "
                                      "stated for the PI, not ruled"),
 "definition_widened": False,
 "axes": axes,
 "completeness": ("Seven axes for the Rubin cohort against bands_FROZEN.md (delta 0.018) with 0.05 thresholds beside. Numbers: contamination (E 1,937,669), "
                  "tool_coverage (2 PASS / 14 FAIL / 9 UNDEMONSTRATED, recount after band hash, verified), cluster_structure, split_integrity, "
                  "unprocessable_units (agent 1 w3). UNDEMONSTRATED: positive and negative measured supply (agent 2 wave 3 pending; TNS BLOCKED). "
                  "P4 refused; ruling null by design; preconditions " + ", ".join(f"({k})" for k in unmet) + " unmet."),
}
OUTF = f"{OUT}/axis_ledger_v2_final_against_frozen_bands.json" if FINAL else f"{OUT}/axis_ledger_v2_against_frozen_bands.json"
dump(ledger, OUTF)
oplog.log("14" if FINAL else "8", f"axis_ledger_v2_against_frozen_bands.json built; precondition (b) {'CLEARED' if b_ok else 'UNMET'} by own verification; unmet {unmet}; no re-band",
          [OUTF, BANDS, f"{A4W3}/run_log.jsonl", f"{A4W3}/tool_coverage_axis.json", f"{A1W3}/axis_ledger_rubin_v2.json"])
print(json.dumps({"b_ok": b_ok, "unmet": unmet, "mism": mism, "rows_before_band": tr["rows_starting_at_or_before_band_hash"], "alert_runs": tr["alert_runs"]}, indent=1))
