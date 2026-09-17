#!/usr/bin/env python3
"""Assemble p4_ruling_package.json. Every ruling-bearing or kill-band number is read FROM its module-V record
(claimed value) via cite(), which asserts verdict and cleared_for_P4_under_rule_E; V_PENDING numbers are
tagged context-only and never enter a comparison. Reads no label field."""
import json, hashlib, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
W = D.parent; A = W.parent
VR = W / "agent4_module_v/v_records.json"; MAN = W / "agent3_freeze_v3/domain_manifest_v3.json"; AX3 = W / "agent3_freeze_v3/axis_ledger_v3_against_frozen_bands.json"
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
V = {r["id"]: r for r in json.load(open(VR))}
used = {}
def cite(vid, field):
    r = V[vid]
    assert r["cleared_for_P4_under_rule_E"] is True and r["verdict"] in ("MATCH", "MATCH_WITHIN_TOL"), vid
    c = [x for x in r["comparisons"] if x["field"] == field]
    assert len(c) == 1, (vid, field)
    used.setdefault(vid, dict(verdict=r["verdict"], sealed_sha256=r["sealed_sha256"], fields=[]))["fields"].append(field)
    return c[0]["claimed"]
def pending(value, what):
    return {"value": value, "rule_E": "V_PENDING", "use": "context only; not in any ruling or kill-band comparison", "what": what}
O = cite("V-C01", "O_merged"); OA = cite("V-C02", "O_A"); S1 = cite("V-C03", "S1_total"); S3 = cite("V-C04", "S3_one_detection_share_oids")
N018lo = cite("V-N01", "w3-09 objects_family_B 0.018 lo"); N018hi = cite("V-N01", "w3-09 objects_family_B 0.018 hi")
N05lo = cite("V-N02", "w3-09 objects_family_B 0.05 lo"); N05hi = cite("V-N02", "w3-09 objects_family_B 0.05 hi")
TP = cite("V-T01", "all.PASS"); TF = cite("V-T01", "all.FAIL"); TU = cite("V-T01", "all.UNDEMONSTRATED")
CATSp = cite("V-T02", "CATS.passes"); CATSn = cite("V-T02", "CATS.alerts_run")
b_ok = cite("V-O02", "band_hash_utc")
M = json.load(open(MAN)); AX = json.load(open(AX3))
comparisons = []
def cmp(axis, test, lhs, op, rhs, lhs_id, rhs_id, delta):
    res = {"<": lhs < rhs, ">=": lhs >= rhs, "==": lhs == rhs, ">": lhs > rhs}[op]
    comparisons.append(dict(axis=axis, delta=delta, test=test, expression=f"{lhs} {op} {rhs}", lhs_v=lhs_id, rhs_v=rhs_id, result=res))
    return res
# kill-band comparisons with cleared numbers only
for dl, lo, hi, idl in (("0.018 (frozen band)", N018lo, N018hi, "V-N01"), ("0.05 (ratified, reported beside, not a band)", N05lo, N05hi, "V-N02")):
    cmp("positive_supply", "CLOSE requires O < N_B,lo (and M_obs < N_A,lo)", O, "<", lo, "V-C01", idl, dl)
    cmp("negative_supply", "CLOSE requires O < N_B,lo (and M_obs < N_A,lo)", O, "<", lo, "V-C01", idl, dl)
    cmp("contamination_exposure", "CLOSE requires E == 0 with O > 0", O, "==", 0, "V-C01", "literal", dl)
    cmp("cluster_structure", "ALeRCE distinct and merged counts in the same O band (>= N_B,hi)", O, ">=", hi, "V-C01", idl, dl)
    cmp("cluster_structure", "ALeRCE distinct oids >= N_B,hi", OA, ">=", hi, "V-C02", idl, dl)
    cmp("tool_coverage", "CLOSE requires no FM/deep channel accepting v11.1-carried inputs: CATS passes > 0", CATSp, ">", 0, "V-T02", "literal", dl)
axes = [
 dict(axis="positive_supply", disposition="UNDEMONSTRATED", number=None,
      band_reading={"delta_0.018_frozen": "UNDEMONSTRATED (P unread); CLOSE excluded because O >= N_B,lo", "delta_0.05_beside": "UNDEMONSTRATED; CLOSE excluded because O >= 63; not a band"},
      rule_E={"O": {"value": O, "v": "V-C01"}, "N_B 0.018": {"value": [N018lo, N018hi], "v": "V-N01"}, "N_B 0.05": {"value": [N05lo, N05hi], "v": "V-N02"},
              "M_obs": pending(10, "survey nights"), "N_A nights 0.018 / 0.05": pending([[40, 1515], [6, 197]], "night-family thresholds"), "P": "UNDEMONSTRATED (no number)"},
      why="measured positive labels unread: TNS BLOCKED (2026-09-16, 2026-09-17), WISeREP BLOCKED (live HTTP 403; archive 404 on 43/43 incl. controls)"),
 dict(axis="negative_supply", disposition="UNDEMONSTRATED", number=None,
      band_reading={"delta_0.018_frozen": "UNDEMONSTRATED (Ng unread); CLOSE excluded because O >= N_B,lo", "delta_0.05_beside": "UNDEMONSTRATED; not a band"},
      rule_E={"O": {"value": O, "v": "V-C01"}, "Ng": "UNDEMONSTRATED (no number)", "unlabelled_counted_as_negative": 0}),
 dict(axis="contamination_exposure", disposition="PASS (counted)", number=O,
      band_reading={"delta_0.018_frozen": "ESCALATE", "delta_0.05_beside": "ESCALATE (no delta-dependent term decides it)"},
      reason="not CLOSE: E = O > 0 (V-C01). Not PROCEED: a subject lacks a published cutoff (Gemini 3.1 Pro preview; manifest subject_set, DERIVED, not a number) and E-labelled is UNDEMONSTRATED",
      rule_E={"E": {"value": O, "v": "V-C01"}, "S1_excluded": {"value": S1, "v": "V-C03"}, "S0_excluded": pending(112990, "S0 loci"), "ANTARES leak": pending([193, 9000], "prior-position alerts")}),
 dict(axis="tool_coverage", disposition="PASS (counted after the band hash; precondition b via V-O02)", number={"PASS": TP, "FAIL": TF, "UNDEMONSTRATED": TU},
      band_reading={"delta_0.018_frozen": "ESCALATE", "delta_0.05_beside": "ESCALATE (no delta-dependent threshold)"},
      reason="not CLOSE: CATS accepted Rubin v11.1-named inputs, 5/10 (V-T02). Not PROCEED: CATS's Rubin counterparts (Fink_EarlySNIa_RF, Fink_SLSN_RF) FAIL at emit on 10/10; those per-tool dispositions sit inside the V-T01 retally of all 25 tools (2/14/9) and have no separate V record",
      rule_E={"tally": {"value": [TP, TF, TU], "v": "V-T01"}, "CATS": {"value": f"{CATSp}/{CATSn}", "v": "V-T02"}, "recount after band hash": {"value": b_ok, "v": "V-O02"}},
      packet_qualifier="runs used public Fink LSST API JSON rows carrying v11.1 field names; Avro not served (HTTP 400); listed as a disagreement in v3, band reading unchanged"),
 dict(axis="cluster_structure", disposition="PASS", number={"merged_objects": O, "alerce_oids": OA},
      band_reading={"delta_0.018_frozen": "PROCEED (leans on V_PENDING numbers)", "delta_0.05_beside": "PROCEED (leans on V_PENDING numbers)"},
      rule_E={"O": {"value": O, "v": "V-C01"}, "O_A": {"value": OA, "v": "V-C02"}, "fink_first_detections": pending([1773044, 2018299], "Fink aggregate"), "antares_loci": pending(1908703, "ANTARES loci"),
              "raw_detections": pending(2418954, "ALeRCE n_det sum"), "fink_raw_alerts": pending(3511022, "Fink alerts")},
      lean="the band's 'every broker in the same band' clause needs the Fink and ANTARES counts, which are V_PENDING; with cleared numbers only, the ALeRCE counts (V-C01, V-C02) clear 12,855 and 1,666"),
 dict(axis="split_integrity", disposition="PASS", number={"S1": S1},
      band_reading={"delta_0.018_frozen": "PROCEED (leans on V_PENDING numbers)", "delta_0.05_beside": "PROCEED (leans on V_PENDING numbers)"},
      rule_E={"S1": {"value": S1, "v": "V-C03"}, "O": {"value": O, "v": "V-C01"}, "cross-broker before T0 sample": pending("0/8986", "Fink alert-history first before T0"), "O minus listed worst case": pending(1896117, "sample-scaled")},
      lean="S1 is outside O by definition (V-C03); the band also subtracts cohort objects another broker places before T0, measured only on a V_PENDING 9,000-oid sample"),
 dict(axis="unprocessable_units", disposition="PASS", number=None,
      band_reading={"delta_0.018_frozen": "PROCEED (rests entirely on a V_PENDING number)", "delta_0.05_beside": "PROCEED (rests entirely on a V_PENDING number)"},
      rule_E={"U": pending(0, "unprocessable rows"), "O": {"value": O, "v": "V-C01"}},
      lean="U = 0 has no V record; under rule E this PROCEED reading cannot enter a ruling"),
]
pkg = dict(
 candidate="live time-domain astronomy: Rubin LSST prospective cohort (first detection >= 2026-07-01T00:00 UTC)", branch="prediction",
 version="P4 ruling package (agent 1, wave 4)",
 manifest=dict(path="astronomy/wave4/agent3_freeze_v3/domain_manifest_v3.json", file_sha256=sha(MAN), frozen_hash=M["frozen_hash"], frozen_hash_recomputed="MATCH (out/input_verification.json)"),
 bands=dict(path="astronomy/wave2/agent1_rubin_bands/bands_FROZEN.md", sha256=sha(A / "wave2/agent1_rubin_bands/bands_FROZEN.md"), delta="0.018 (frozen); 0.05 ratified (ruling 1), reported beside; no re-banding"),
 inputs=dict(v_records=sha(VR), axis_ledger_v3=sha(AX3), truth_cost_monthly=sha(W / "agent2_price_of_truth/truth_cost_monthly.json")),
 ruling=None,
 ruling_decision="REFUSE (no P4 ruling). references/stages/supply.md line 37: P4 'Refuses to rule at all when any of the seven axes in P3 is missing a number'; bands_FROZEN.md section 7 line 184: 'Each one unmet means no ruling; name it.' positive_supply and negative_supply carry no number, so PROCEED, CLOSE and ESCALATE are all unavailable. No axis reads CLOSE on cleared numbers either, so no CLOSE is being suppressed.",
 preconditions=dict(a=dict(state="UNMET", why="measured P and Ng UNDEMONSTRATED: TNS BLOCKED (second record, 2026-09-16 and 2026-09-17); WISeREP BLOCKED (HTTP 403 live; 43/43 archived 404 incl. classified controls)"),
                    b=dict(state="CLEARED", v="V-O02"), c=dict(state="CLEARED", basis="PI ruling 4 (definition ratified, not a count; L01-L05 V_PENDING and not used)")),
 binding_axis="positive_supply (with negative_supply) at measured labels: the unmet precondition needing an external input (label access or a funded follow-up program) and survey time (Rubin off sky since 2026-07-14, no return date); bands_FROZEN.md section 7 refusal rule",
 combination_preview_not_a_ruling="if (a) cleared with no other change: no axis is in CLOSE on cleared numbers (comparisons below); contamination_exposure and tool_coverage read ESCALATE, so section 7 could not yield PROCEED",
 kill_band_comparisons=comparisons, definition_widened=False, axes=axes,
 rule_E_citations=used,
 rule_E_leans=["cluster_structure PROCEED needs Fink/ANTARES counts (V_PENDING)", "split_integrity PROCEED needs the cross-broker sample (V_PENDING)", "unprocessable_units PROCEED rests on U = 0 (V_PENDING)"],
 escalation="escalation_memo.md: loop-ladder rung 2 escalation to the PI (NOT a P4 ruling)",
 ppdb="ppdb_check.json: NOT RELEASED; O (V-C01) upper bound",
 completeness="All seven axes listed against bands_FROZEN.md at 0.018 with 0.05 beside. Ruling-bearing numbers read from V records (V-C01, V-C02, V-C03, V-C04, V-N01, V-N02, V-T01, V-T02, V-O02) with verdict and clearance asserted by scripts/build_package.py; V_PENDING numbers tagged context-only. positive_supply and negative_supply UNDEMONSTRATED (precondition a UNMET) so P4 refuses; ruling null by design and the validator FAIL stands. No label field read.")
json.dump(pkg, open(D / "p4_ruling_package.json", "w"), indent=1, default=str)
for c in comparisons: print(c["axis"], c["delta"][:5], c["expression"], c["result"])
print(json.dumps(used, indent=0)[:800])
