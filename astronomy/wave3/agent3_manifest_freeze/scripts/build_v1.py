#!/usr/bin/env python3
"""Freeze v1: wave-2 brief PI decisions over every slot as it stood at the end of wave 2.

Writes amendment_ledger.json (v1 entries), then domain_manifest_v1.json with frozen_hash.
Inputs are read-only; nothing from wave 3 enters v1 except the wave-2 agent-2 and agent-4 files,
which were produced under the wave-2 brief.
"""
import copy, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa
import oplog
DRY = "--dry" in sys.argv
SCR = "/tmp/claude-1000/-home-aid1-Documents-4-19C-astronomy/addb1fc3-63d3-4989-8753-aa4c400b100e/scratchpad/dry"
if DRY:
    os.makedirs(SCR, exist_ok=True)
    oplog.log = lambda *a, **k: None
DEST = SCR if DRY else OUT

# ---------------------------------------------------------------- inputs
P = {
    "cut": "astronomy/agent1_supply_corpus/cut_curve.json",
    "corpus": "astronomy/agent1_supply_corpus/corpus_ledger.json",
    "lab1": "astronomy/agent3_labels_exposure/label_source_slot.json",
    "exp": "astronomy/agent3_labels_exposure/exposure_key_slot.json",
    "inv": "astronomy/agent4_tools_instrument/tool_inventory_slot.json",
    "k": "astronomy/agent5_resolution_replay/k_slot.json",
    "delta": "astronomy/agent5_resolution_replay/delta_slot.json",
    "subj": "astronomy/agent5_resolution_replay/subject_set_slot.json",
    "d5": "astronomy/agent5_resolution_replay/d5_inputs.json",
    "a5rep": "astronomy/agent5_resolution_replay/REPORT.md",
    "a4rep1": "astronomy/agent4_tools_instrument/REPORT.md",
    "lab2": "astronomy/wave2/agent2_label_source/label_source_slot.json",
    "comp": "astronomy/wave2/agent4_instrument/compositions_FROZEN.md",
    "r1": "astronomy/wave2/agent4_instrument/r1_spec.md",
    "pow2": "astronomy/wave2/agent4_instrument/power_calibration.json",
    "a4rep2": "astronomy/wave2/agent4_instrument/REPORT.md",
    "a1led2": "astronomy/wave2/agent1_rubin_bands/axis_ledger_rubin.json",
    "tr2": "astronomy/wave2/agent5_skill_maintenance/transfer_record.json",
    "syn": "astronomy/SYNTHESIS.md",
}
cut, lab1, exp, inv, k, delta, subj, d5, lab2 = (load(P[x]) for x in
    ("cut", "lab1", "exp", "inv", "k", "delta", "subj", "d5", "lab2"))
d5 = {r["id"]: r for r in d5}
assert sha(W2) == W2SHA and sha(BANDS) == BANDS_SHA

W2REF = lambda loc: ref(W2, loc)
T = now()

# ---------------------------------------------------------------- amendment ledger, v1 entries
ledger_v1 = [
 {"id": "AMD-V1-01", "manifest_version": "v1", "slot": "k", "kind": "RATIFICATION",
  "before": {"value": 8, "status": "DERIVED"}, "after": {"value": 8, "status": "RATIFIED"},
  "note": "rounding noted: k_exact = 327/41 = 7.9756 unique sources triggered per night (arXiv:2401.15167 sec 4.1-4.2); 8 is the nearest integer",
  "cause": "PI ruling: 'k = 8 per night: RATIFIED, rounding noted.'",
  "source": W2REF("PI-supplied D5 inputs, line 14")},
 {"id": "AMD-V1-02", "manifest_version": "v1", "slot": "decision_epoch", "kind": "RATIFICATION (new D4 slot)",
  "before": None, "after": {"value": {"primary": "first alert", "secondary": "night 3"}, "status": "RATIFIED"},
  "note": "declared in the hashed brief before any composition ran; wave-2 agent 4 operationalised it for ZTF in compositions_FROZEN.md section 1 citing the brief hash; this freeze re-checks that operationalisation against the ratified value (MATCH, see manifest decision_epoch.recheck)",
  "cause": "PI ruling: 'Decision epoch: new D4 slot. Primary = first alert. Secondary = night 3. Declared now, before any composition runs.'",
  "source": W2REF("PI-supplied D5 inputs, line 15")},
 {"id": "AMD-V1-03", "manifest_version": "v1", "slot": "tool_inventory", "kind": "OVERRIDE (approved amendment)",
  "before": {"rubin_counterparts": {"ATAT": ["ALeRCE_BHRF"], "Astromer1": ["ALeRCE_BHRF"], "Astromer2": ["ALeRCE_BHRF"]}, "status": "DERIVED"},
  "after": {"rubin_counterparts": {"ATAT": ["Fink_EarlySNIa_RF", "Fink_SLSN_RF"], "Astromer1": ["Fink_EarlySNIa_RF", "Fink_SLSN_RF"], "Astromer2": ["Fink_EarlySNIa_RF", "Fink_SLSN_RF"]}, "status": "OVERRIDDEN"},
  "not_changed": "wave-1 counts (summary.ztf/rubin status counts, condition_a_detail as counted, per-tool ztf/rubin statuses) and the ZTF counterpart mapping; the wave-1 'counterparts' field is kept verbatim and the amended Rubin mapping is added beside it",
  "cause_of_amendment": "wave-1 agent 4: check (a) FAILS on Rubin for ATAT, Astromer 1 and Astromer 2 because the mapped classical counterpart ALeRCE_BHRF has no Rubin weights (ATAT results_rf_paper.zip holds predictions only); re-mapping to Fink's RFs (the two Fink RF rows in the inventory, both AVAILABLE_UNVERIFIED on Rubin) was proposed for D5 and deliberately not applied after the count, since that would widen a definition",
  "cause_locator": ref(P["a4rep1"], "Headline bullet 'Check (a)' lines 22-25; section 2 line 85"),
  "cause": "PI ruling: 'Fink RF remapping (agent 4 proposal): APPROVED as a D5 amendment with cause. Record it, then apply it. Do not touch the wave 1 counts.'",
  "source": W2REF("PI-supplied D5 inputs, line 16")},
 {"id": "AMD-V1-04", "manifest_version": "v1", "slot": "supplied_by_human.budget", "kind": "UNDEMONSTRATED (SUPPLY placeholder unfilled)",
  "before": None, "after": {"value": None, "status": "UNDEMONSTRATED"},
  "cause": "brief field arrived as '[SUPPLY: arm cells or hours]'; coordinator preamble item 1 records it UNDEMONSTRATED",
  "source": W2REF("line 12; coordinator preamble item 1, line 57")},
 {"id": "AMD-V1-05", "manifest_version": "v1", "slot": "supplied_by_human.cost_of_action -> delta", "kind": "UNDEMONSTRATED (SUPPLY placeholder unfilled); delta not overridden",
  "before": {"delta": 0.018, "status": "DERIVED"}, "after": {"delta": 0.018, "status": "DERIVED", "resolution_warning": "attached"},
  "cause": "brief: 'Cost of action: [SUPPLY: ...]. Until supplied, delta stays 0.018 with its resolution warning attached.'",
  "source": W2REF("line 13; coordinator preamble item 1, line 57")},
 {"id": "AMD-V1-06", "manifest_version": "v1", "slot": "S", "kind": "UNDEMONSTRATED (consequence)",
  "before": {"value": None, "status": "UNDEMONSTRATED"}, "after": {"value": None, "status": "UNDEMONSTRATED"},
  "cause": "S = budget / measured hours per workflow (references/manifest.md); budget unfilled and R1 not run; coordinator preamble item 1: 'S and the P7 ruling stay UNDEMONSTRATED'",
  "source": W2REF("coordinator preamble item 1, lines 57-58")},
 {"id": "AMD-V1-07", "manifest_version": "v1", "slot": "supplied_by_human.rulings_holder", "kind": "UNDEMONSTRATED (SUPPLY placeholder unfilled)",
  "before": None, "after": {"value": None, "status": "UNDEMONSTRATED", "transfer": "BLOCKED"},
  "cause": "brief field arrived as '[SUPPLY: a person who wrote neither the skill nor any case]'; preamble item 1: rulings transfer blocked; wave-2 agent 5 transfer_record.json status BLOCKED",
  "source": W2REF("line 17; coordinator preamble item 1, line 59"),
  "corroboration": ref(P["tr2"], "status BLOCKED")},
 {"id": "AMD-V1-08", "manifest_version": "v1", "slot": "supplied_by_human.tns_credentials", "kind": "UNDEMONSTRATED (SUPPLY placeholder unfilled)",
  "before": None, "after": {"value": None, "status": "UNDEMONSTRATED"},
  "cause": "brief field arrived as '[SUPPLY: bot or user account, else agent 2 marks UNDEMONSTRATED]'; preamble item 1: agent 2 works without TNS credentials; wave-2 agent 2 records HTTP 403 on every wis-tns.org path",
  "source": W2REF("line 18; coordinator preamble item 1, line 60")},
 {"id": "ESC-V1-01", "manifest_version": "v1", "slot": "graph (R1 -> I1, D5 -> R1)", "kind": "ESCALATION recorded, not an amendment",
  "before": None, "after": {"state": "ESCALATED to PI (ladder rung 2)", "compositions": "PRE-I1 CALIBRATION"},
  "cause": "coordinator preamble item 2: the brief asks for I1 compositions while R1 has not run and D5 cannot close; agent 4 builds compositions as PRE-I1 CALIBRATION, not I1 records, pending PI ruling; 'not as an amendment the coordinator granted itself'",
  "source": W2REF("coordinator preamble item 2, lines 61-65")},
 {"id": "SU-V1-01", "manifest_version": "v1", "slot": "label_source", "kind": "SLOT UPDATE (supersession under the brief's assignment; not a PI ruling)",
  "before": {"record": ref(P["lab1"]), "sniascore_bound": [0, 3131], "status": "UNDEMONSTRATED"},
  "after": {"record": ref(P["lab2"]), "sniascore_bound": [803, 2247], "unresolved": 6156, "status": "UNDEMONSTRATED"},
  "cause": "wave-2 brief assigns agent 2 to tighten the SNIascore bound and update label_source_slot.json; preamble item 3: agent 3's freeze reads agent 2's updated slot",
  "source": W2REF("Assignments, Agent 2, lines 26-30; coordinator preamble item 3, line 66")},
]
for e in ledger_v1:
    e["recorded_utc"] = T
ledger = {
 "record": "amendment_ledger",
 "candidate": "live time-domain astronomy (Rubin LSST alerts; ZTF BTS as calibration only)",
 "author": "wave3 agent 3 (manifest freeze)",
 "entry_kinds": "RATIFICATION, OVERRIDE, UNDEMONSTRATED supply field, ESCALATION, SLOT UPDATE (supersession), PENDING input. Only RATIFICATION and OVERRIDE are PI acts on a slot; the others are recorded so no slot changes without a ledger line.",
 "v1_entries": ledger_v1,
 "v1_entries_canonical_sha256": canonical_sha(ledger_v1),
 "v2_entries": [],
 "completeness": "v1: every PI decision in PANEL_BRIEF_WAVE2.md 'PI-supplied D5 inputs' (7 bullets) has one entry, plus S (consequence), the graph escalation and the label_source supersession. Slots the brief did not rule on (tau, exposure_key, subject_set, the rest of tool_inventory) have no ratification entry because none was given. v2 entries are appended by build_v2_draft.py.",
}
dump(ledger, f"{DEST}/amendment_ledger.json")
oplog.log("4", "amendment_ledger.json written with v1 entries only (before v1 manifest assembly)",
          [f"{OUT}/amendment_ledger.json"])

# ---------------------------------------------------------------- slots
def prov(referent, source, population, adjudicator, falsifier):
    return dict(referent=referent, source=source, population=population, adjudicator=adjudicator, falsifier=falsifier)

INVITE = "Override invitation: accept, or replace the value and give a reason; the reason enters amendment_ledger.json."

# tau
tau = {
 "value": {"radius_arcsec": cut["chosen_radius_arcsec"], "cut": cut["chosen_cut"],
           "unit_bts": "distinct astrophysical object: positional friends-of-friends at 1 arcsec plus amendment A1 re-trigger clause (same IAU name, |dpeak| <= 60 d)",
           "unit_rubin": "diaObjectId with crossmatch rules X1-X4 (1 arcsec and first detections <= 60 d apart), bands_FROZEN.md section 2",
           "n_clusters_bts": 11183, "plateau_arcsec": [0.5, 1.5],
           "sensitivity": cut["sensitivity"],
           "tau_py_choice_refused": {"radius_arcsec": 30.0, "why": "flat curve; merges 39 distinct-SN pairs (must-not-join control)"}},
 "provenance": prov(
   "similarity cut that defines the independent unit (distinct astrophysical object) for clustering and every count",
   "astronomy/agent1_supply_corpus/cut_curve.json sha256 " + sha(P["cut"]) + " (scripts/build_corpus.py::fof, 10 radii 0.5-60 arcsec, must-join and must-not-join controls); Rubin application bands_FROZEN.md sha256 " + BANDS_SHA + " section 2",
   "11193 included BTS corpus rows (11183 clusters); Rubin cohort diaObjectIds",
   "tau.py choice at 30 arcsec (11116 clusters, 39 must-not-join violations); IAU-name join 11,204 (agents 3 and 5)",
   "a re-trigger pair (same object, |dpeak|<=60 d) measured at >1.5 arcsec, or two distinct SNe measured at <=1.5 arcsec, or an I1 separation curve that collapses at 1 arcsec"),
 "status": "DERIVED",
 "status_note": "Not ruled on in PANEL_BRIEF_WAVE2.md. The separation-collapse bound (the second D3 signal) is UNDEMONSTRATED until I1 compositions exist.",
 "disagreements": ["distinct-object count 11,183 (agent 1, 1 arcsec + A1) vs 11,204 (agents 3 and 5, IAU-name join) vs 11,198 groups (agent 2, 3 arcsec + IAU): listed, not reconciled (SYNTHESIS.md section 8)"],
 "source_records": [ref(P["cut"]), ref(BANDS, "section 2")],
 "override_invitation": INVITE,
}

# k
kk = {
 "value": 8,
 "rounding": {"k_exact": round(327 / 41, 4), "numerator": 327, "denominator_nights": 41, "rule": "nearest integer"},
 "candidates_per_round": k["candidates_per_round"], "chance_stated": k["chance"],
 "provenance": prov(k["provenance"]["referent"],
   k["provenance"]["source"] + "; RATIFIED at PANEL_BRIEF_WAVE2.md sha256 " + W2SHA + " line 14",
   k["provenance"]["population"], k["provenance"]["adjudicator"], k["provenance"]["falsifier"]),
 "status": "RATIFIED",
 "status_note": "Ratified with the rounding noted (AMD-V1-01). ZTF-era value; Rubin-era k is UNDEMONSTRATED (k_slot.json undemonstrated[0]).",
 "disagreements": k["disagreements"] + [
   "wave-2 calibration (astronomy/wave2/agent4_instrument/REPORT.md 'Disagreements' 1): stated chance 0.172 vs measured 0.225-0.230 on the BTS file, which holds saved sources only; 518 of 579 nights have <= 8 candidates, so k binds on 61 nights"],
 "undemonstrated": k["undemonstrated"],
 "source_records": [ref(P["k"]), ref(W2, "line 14"), ref(P["a4rep2"], "Disagreements 1-2")],
 "override_invitation": INVITE,
}

# label_source (wave-2 agent 2 slot verbatim)
labs = {
 "value": lab2["value"],
 "provenance": lab2["provenance"],
 "status": "UNDEMONSTRATED",
 "status_note": lab2["status_reason"],
 "banner": lab2["banner"],
 "supersedes": lab2["supersedes"],
 "source_records": [ref(P["lab2"]), ref(P["lab1"], "superseded; class-level shares carried")],
 "override_invitation": INVITE + " Ratifying this slot as UNDEMONSTRATED does not make the labels measured; P4 precondition (c) needs either ratification of a label source or measured P and Ng.",
}

# exposure_key
expk = {
 "value": exp["value"],
 "provenance": exp["provenance"],
 "status": "DERIVED",
 "status_note": exp["status_note"] + ". Not ruled on in PANEL_BRIEF_WAVE2.md.",
 "wave2_cross_references": {
   "rubin_admission_boundary": "first detection >= 2026-07-01T00:00:00 UTC (MJD TAI 61222.000428) = max(survey start 2026-06-29T12:00, latest demonstrated cutoff last day + 1 d); stratum S0 = nights 20260629-20260630 (bands_FROZEN.md section 1 and 3)",
   "tns_discovery_date_not_a_safe_lower_bound": "SN2017bde discovered 2017 but classified by SNIascore in 2023; AT2019czs likewise (wave-2 agent 2 REPORT.md Disagreements 7). The exposure key uses TNS discovery date as the label-public lower bound, and that bound is contradicted for these objects. Listed, not reconciled.",
 },
 "source_records": [ref(P["exp"]), ref(BANDS, "sections 1, 3"), ref("astronomy/wave2/agent2_label_source/REPORT.md", "section 6 item 7")],
 "override_invitation": INVITE,
}

# tool_inventory with remap applied
iv = copy.deepcopy(inv["value"])
REMAP = {"ATAT", "Astromer1", "Astromer2"}
FINK = ["Fink_EarlySNIa_RF", "Fink_SLSN_RF"]
status_rubin = {t["id"]: t["rubin"] for t in iv["tools"]}
for t in iv["tools"]:
    if t.get("fm_channel"):
        t["counterparts_by_survey"] = {
            "ztf": list(t["counterparts"]),
            "rubin": list(FINK) if t["id"] in REMAP else list(t["counterparts"]),
        }
        if t["id"] in REMAP:
            t["counterparts_by_survey"]["rubin_amendment"] = "AMD-V1-03 (was " + json.dumps(t["counterparts"]) + ")"
for c in iv["condition_a_detail"]:
    if c["fm_channel"] in REMAP:
        c["counterpart_available_rubin_after_AMD-V1-03"] = [x for x in FINK if status_rubin[x] in ("AVAILABLE_VERIFIED", "AVAILABLE_UNVERIFIED")]
avail = ("AVAILABLE_VERIFIED", "AVAILABLE_UNVERIFIED")
fm_rubin = [t for t in iv["tools"] if t.get("fm_channel") and t["rubin"] in avail]
cond_after = all(any(status_rubin[x] in avail for x in t["counterparts_by_survey"]["rubin"]) for t in fm_rubin)
iv["summary"]["condition_a_every_fm_structurally_available_on_rubin_has_available_counterpart_after_AMD-V1-03"] = cond_after
iv["summary"]["amendment_note"] = ("wave-1 counts above are unchanged; the after-AMD-V1-03 flag is structural only "
    "(Fink RFs are AVAILABLE_UNVERIFIED on Rubin: code and weights exist, no run on real Rubin alerts)")
toolinv = {
 "value": iv,
 "provenance": inv["provenance"],
 "status": "OVERRIDDEN",
 "override_reason": ("AMD-V1-03: PI approved agent 4's Fink RF remapping (PANEL_BRIEF_WAVE2.md line 16). Cause: check (a) failed on Rubin for "
                     "ATAT, Astromer 1 and Astromer 2 because ALeRCE_BHRF has no Rubin weights. Rubin classical counterpart for those three "
                     "is now Fink_EarlySNIa_RF and Fink_SLSN_RF; ZTF mapping and all wave-1 counts unchanged."),
 "status_note": "The override covers the Rubin counterpart mapping of three rows only. The rest of the inventory (roles, readiness census, 25 channels) is as derived and was not ratified; readiness is a census, not certification (I5 UNDEMONSTRATED).",
 "wave2_tool_card_updates": {"path": "astronomy/wave2/agent4_instrument/tool_cards/", "note": "3 new Fink cards and an updated ParSNIP card with code defects (ParSNIP input_redshift=False crash, NaN on single-detection light curves; Fink SLSN zp 25 vs FLUXCAL 27.5; Fink fast-transient rate depends on batch); listed, statuses above not changed", "report": ref(P["a4rep2"], "Headline, four new code defects")},
 "source_records": [ref(P["inv"]), ref(W2, "line 16"), ref(P["a4rep1"], "lines 22-25, 85")],
 "override_invitation": INVITE,
}

# delta
dl = {
 "value": 0.018,
 "resolution_warning": ("0.018 is below the unpaired MDE of about 0.045 of the very comparison it comes from (agent5 REPORT.md line 48); "
                        "practitioners acted below their own resolution. Wave-2 PRE-I1 calibration on BTS binding nights gives MDE 0.032 > 0.018 "
                        "(CLOSE_UNRESOLVABLE, calibration only, not P7)."),
 "metric_caveat": delta["metric_caveat"],
 "provenance": prov(delta["provenance"]["referent"], delta["provenance"]["source"] + "; kept by PANEL_BRIEF_WAVE2.md sha256 " + W2SHA + " line 13 until cost of action is supplied",
                    delta["provenance"]["population"], delta["provenance"]["adjudicator"], delta["provenance"]["falsifier"]),
 "status": "DERIVED",
 "status_note": "Cost of action was an unfilled SUPPLY field, so no override exists; per the brief delta stays at the derived prior with its resolution warning (AMD-V1-05). Not RATIFIED.",
 "candidates_listed": delta["candidates"],
 "disagreements": delta["disagreements"],
 "source_records": [ref(P["delta"]), ref(P["a5rep"], "line 48"), ref(P["pow2"]), ref(W2, "line 13")],
 "override_invitation": INVITE + " Supplying cost of action is the route manifest.md names for overriding delta.",
}

# S
s = d5["d5-S"]
SS = {
 "value": None,
 "provenance": prov(s["referent"], s["source"] + "; UNDEMONSTRATED per PANEL_BRIEF_WAVE2.md sha256 " + W2SHA + " coordinator preamble item 1",
                    s["population"], s["adjudicator"], s["falsifier"]),
 "status": "UNDEMONSTRATED",
 "status_note": "budget unfilled (SUPPLY) and hours per workflow unmeasured (R1 not run)",
 "blocks": s["blocks"],
 "source_records": [ref(P["d5"], "id d5-S"), ref(W2, "preamble item 1")],
 "override_invitation": "Not overridable by ratification: S follows from a supplied budget and an R1 measurement.",
}

# subject_set
sb = {
 "value": subj["value"],
 "members": subj["members"],
 "provenance": subj["provenance"],
 "status": "DERIVED",
 "status_note": "Not ruled on in PANEL_BRIEF_WAVE2.md. Training-data ends UNDEMONSTRATED for all members; Gemini 3.1 Pro has no published cutoff.",
 "disagreements": subj["disagreements"] + [
   "membership: agent 5's subject set has 7 models; agent 3's exposure-key cutoff table carries 10 (adds Claude Haiku 4.5, GPT-5.6 Terra, GPT-5.6 Luna). Listed, not reconciled.",
   "bands_FROZEN.md section 1: the Rubin admission boundary 2026-07-01 is set by Claude Fable 5.1 (Jun 2026); dropping Fable 5.1 would admit June objects, and that relaxation is reserved for the human at D5."],
 "undemonstrated": subj["undemonstrated"],
 "source_records": [ref(P["subj"]), ref(P["exp"], "value.subject_cutoffs"), ref(BANDS, "section 1")],
 "override_invitation": INVITE + " The subject set governs the admission boundary and the contamination band (a subject without a cutoff forces ESCALATE).",
}

# decision_epoch
comp_ok = ("Primary epoch E1, \"first alert\"" in open(rp(P["comp"])).read()
           and "Secondary epoch E3, \"night 3\"" in open(rp(P["comp"])).read())
de = {
 "value": {"primary": "first alert", "secondary": "night 3"},
 "operationalisation": {
   "ztf_calibration": {"E1": "detections with mjd <= t0 + 1e-5 plus prior detections and non-detections in [t0-30 d, t0) (prv_candidates window); decision night n0",
                       "E3": "all photometry with mjd >= t0-30 d and night(mjd) <= n0+3; night(mjd) = floor(mjd - 0.8333)",
                       "t0": "min mjd over positive g/r ALeRCE detections",
                       "source": ref(P["comp"], "section 1")},
   "rubin": "UNDEMONSTRATED as a composition input: no Rubin composition is declared. First detection is defined in bands_FROZEN.md section 3 (min midpointMjdTai over non-forced DIASources); forced photometry is not a detection."},
 "recheck": {"what": "wave-2 agent 4 cited the brief for its epochs and must re-check against the frozen manifest (preamble item 3)",
             "result": "MATCH" if comp_ok else "MISMATCH",
             "method": "compositions_FROZEN.md section 1 declares primary E1 'first alert' and secondary E3 'night 3', equal to this slot's value"},
 "provenance": prov(
   "the moment at which the governed follow-up decision is taken, which fixes the inputs any composition or arm may see",
   "PANEL_BRIEF_WAVE2.md sha256 " + W2SHA + " line 15 (PI declaration); ZTF operationalisation astronomy/wave2/agent4_instrument/compositions_FROZEN.md sha256 " + sha(P["comp"]) + " section 1",
   "one decision per candidate transient per round (observing night); units are 1 arcsec clusters (BTS) or diaObjectIds (Rubin)",
   "later epochs in the record: peak (SN Ia AUC 0.798) and post-spectroscopy (0.967) vs first alert (0.537), agent2_floor_headroom/REPORT.md table lines 73-77; the declared epochs are the decision-time ones",
   "a composition input file containing photometry after the epoch cutoff (a rerun of the compositions_FROZEN.md section 5 forbidden-input check that fails), or a PI statement that differs from brief line 15"),
 "status": "RATIFIED",
 "status_note": "AMD-V1-02. New D4 slot, ratified at declaration. Strata S0-S4 for the Rubin cohort are defined in bands_FROZEN.md section 3; they are not part of this v1 ruling.",
 "source_records": [ref(W2, "line 15"), ref(P["comp"], "section 1"), ref(BANDS, "section 3")],
 "override_invitation": INVITE,
}

supply = {
 "budget": "UNDEMONSTRATED: arrived as unfilled '[SUPPLY: arm cells or hours]' (PANEL_BRIEF_WAVE2.md line 12); AMD-V1-04",
 "cost_of_action": "UNDEMONSTRATED: arrived as unfilled '[SUPPLY: value of one SEDM spectrum hour and of a wrong commitment]' (line 13); delta stays 0.018; AMD-V1-05",
 "rulings_holder": "UNDEMONSTRATED: arrived as unfilled '[SUPPLY: ...]' (line 17); rulings transfer BLOCKED; AMD-V1-07",
 "tns_credentials": "UNDEMONSTRATED: arrived as unfilled '[SUPPLY: ...]' (line 18); agent 2 worked from public archived pages (HTTP 403 live); AMD-V1-08",
}
d5recs = []
for rid in ("d5-budget", "d5-cost-of-action"):
    r = d5[rid]
    d5recs.append({"id": rid, "value": None, "status": "UNDEMONSTRATED",
                   "provenance": prov(r["referent"], r["source"] + "; still unfilled at PANEL_BRIEF_WAVE2.md sha256 " + W2SHA + " lines 12-13", r["population"], r["adjudicator"], r["falsifier"]),
                   "human_must_supply": r["human_must_supply"], "blocks": r["blocks"]})
d5recs += [
 {"id": "d5-rulings-holder", "value": None, "status": "UNDEMONSTRATED",
  "provenance": prov("a person who wrote neither the skill nor any replay case and holds RULINGS_SEALED.csv and the polarity column",
                     "PANEL_BRIEF_WAVE2.md sha256 " + W2SHA + " line 17 (unfilled SUPPLY); astronomy/wave2/agent5_skill_maintenance/transfer_record.json status BLOCKED",
                     "the two replay suites (astronomy 20 cases, source 38 cases)",
                     "the current procedural seal held by the orchestrating party (SYNTHESIS.md section 10)",
                     "a transfer_record.json whose receipt hash resolves against a holder-completed receipt would show the field was filled"),
  "blocks": ["rulings transfer", "issue 09 re-keying", "any seal with more than procedural weight"]},
 {"id": "d5-tns-credentials", "value": None, "status": "UNDEMONSTRATED",
  "provenance": prov("an authenticated TNS bot or user account for per-object classification reports (reporter, Classifier/s, date)",
                     "PANEL_BRIEF_WAVE2.md sha256 " + W2SHA + " line 18 (unfilled SUPPLY); astronomy/wave2/agent2_label_source/label_source_slot.json provenance.adjudicator (HTTP 403 on all wis-tns.org paths 2026-09-16)",
                     "7,843 BTS labels and every Rubin-era classification",
                     "Internet Archive captures of TNS object pages (public, partial: 1,706 fetched)",
                     "an authenticated TNS request that returns classification reports would show the field was filled and resolve the 6,156 UNRESOLVED labels"),
  "blocks": ["label_source per-object split", "measured P and Ng for the Rubin cohort", "P4 precondition (a)"]},
]

candidates = [{
 "id": "astronomy-tda-rubin-lsst",
 "name": "live time-domain astronomy: Rubin LSST alert stream, ZTF BTS as calibration",
 "branch": "prediction",
 "decision_governed": "spectroscopic follow-up allocation: k candidates committed per night",
 "cohorts": {
   "calibration_only": "ZTF BTS (11,183 objects at 1 arcsec); contamination FAIL (agent3 wave 1); addition B: no claim rests on it",
   "prospective": "Rubin LSST objects first detected >= 2026-07-01T00:00 UTC (bands_FROZEN.md section 1); counts in wave2/agent1_rubin_bands/axis_ledger_rubin.json (P4 unruled)"},
 "p4_state_at_v1": "no ruling; preconditions (a) supply without measured labels, (b) tool coverage not recounted after the band, (c) label source unratified",
 "source_records": [ref(P["a1led2"]), ref(P["syn"], "sections 2, 4")],
}]

manifest = {
 "manifest": "domain_manifest",
 "manifest_version": "v1",
 "governing_brief": ref(W2),
 "inputs_state": "every slot as it stood at the end of wave 2; no wave-3 ruling or count enters v1",
 "frozen_utc": None,
 "hash_method": HASH_METHOD,
 "candidates": candidates,
 "tau": tau, "k": kk, "label_source": labs, "exposure_key": expk, "tool_inventory": toolinv,
 "delta": dl, "S": SS, "subject_set": sb, "decision_epoch": de,
 "supplied_by_human": supply,
 "d5_inputs": d5recs,
 "graph_escalations": [{"edge": "R1 -> I1 (and D5 -> R1)", "state": "ESCALATED to PI, ladder rung 2; unruled at v1",
                         "consequence": "wave-2 compositions are PRE-I1 CALIBRATION, hashed, not I1 records", "ledger": "ESC-V1-01",
                         "source": ref(W2, "coordinator preamble item 2")}],
 "amendment_ledger": {"path": f"{OUT}/amendment_ledger.json", "v1_entries_canonical_sha256": ledger["v1_entries_canonical_sha256"],
                      "entries": [e["id"] for e in ledger_v1]},
 "d5_disposition": {
   "stage": "D5 ratification",
   "advances_when": "every slot ratified or overridden, and the manifest frozen and hashed (references/stages/discovery.md D5)",
   "frozen_and_hashed": "PASS",
   "every_slot_ratified_or_overridden": "FAIL",
   "per_slot": {"tau": "DERIVED", "k": "RATIFIED", "label_source": "UNDEMONSTRATED", "exposure_key": "DERIVED",
                "tool_inventory": "OVERRIDDEN (three Rubin counterpart rows)", "delta": "DERIVED", "S": "UNDEMONSTRATED",
                "subject_set": "DERIVED", "decision_epoch": "RATIFIED"},
   "disposition": "UNDEMONSTRATED: D5 does not advance. The brief's sentence 'This closes D5 for everything except the two SUPPLY fields' is not itself a ruling on tau, exposure_key, subject_set or the rest of tool_inventory, and this freeze does not ratify on the PI's behalf. Those four stay DERIVED with override invitations (D5_presentation.md).",
   "disagreement_with_brief": "PANEL_BRIEF_WAVE2.md line 35 expects D5 closed except the SUPPLY fields; the PI decisions (lines 12-18) rule on k, decision epoch and the remapping only. Listed, not reconciled.",
 },
 "completeness": ("v1 covers the ten schema slots plus decision_epoch; each carries value, five provenance fields and status. Inputs: wave-1 slot files "
                  "(agent1 cut_curve, agent3 exposure_key, agent4 tool_inventory, agent5 k/delta/subject_set/d5_inputs) and wave-2 agent 2 label_source; "
                  "wave-2 agent 1 bands and agent 4 compositions as cross-references. Not covered: any wave-3 ruling or count; a separation curve for tau; "
                  "Rubin-era k; training-data cutoffs; budget, cost of action, rulings holder, TNS credentials (UNDEMONSTRATED)."),
 "frozen_hash": "",
}
manifest["frozen_utc"] = now()
manifest["frozen_hash"] = manifest_hash(manifest)
dump(manifest, f"{DEST}/domain_manifest_v1.json")
oplog.log("5", f"v1 FROZEN: domain_manifest_v1.json frozen_hash={manifest['frozen_hash']} (canonical JSON, sorted keys, no whitespace, frozen_hash=\"\")",
          [f"{OUT}/domain_manifest_v1.json", f"{OUT}/amendment_ledger.json"])
print("condition_a after remap:", cond_after, "| epoch recheck:", comp_ok)
