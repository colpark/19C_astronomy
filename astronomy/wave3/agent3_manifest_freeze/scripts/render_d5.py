#!/usr/bin/env python3
"""Render D5_presentation.md from the frozen v1 manifest (provenance copied verbatim from the file)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

m = load(f"{OUT}/domain_manifest_v1.json")
led = load(f"{OUT}/amendment_ledger.json")

DERIV = {
 "tau": """Agent 1 swept 10 radii (0.5 to 60 arcsec) over the 11,193 included BTS rows and recorded cluster count plus two controls at each radius. Must-join: re-trigger duplicates (same IAU name, peaks within 60 d; amendment A1). Must-not-join: distinct supernovae with different IAU names. Cluster count is flat at 11,183 from 0.5 to 1.5 arcsec with zero must-not-join violations. The first violation is at 2 arcsec (SN2023ghl and SN2024gyr, 1.92 arcsec). 1 arcsec is the plateau midpoint, and the count is the same at the looser and tighter sensitivity cuts, so the choice does not raise the unit count. `tau.py` picked 30 arcsec. That pick was refused: every step of the curve gains under 0.3%, and 30 arcsec merges 39 distinct-SN pairs. For Rubin, bands_FROZEN.md section 2 applies the same 1 arcsec cut plus the 60 d clause to diaObjectIds. The second D3 signal, separation collapse, needs I1 compositions and is UNDEMONSTRATED.""",
 "k": """Source: arXiv:2401.15167 sections 4.1-4.2. BTS scanners triggered SEDM on 327 unique sources over 41 consecutive nights (2023-08-19 to 09-29), so k_exact = 7.976, rounded to 8. Candidates per round are 1,903 sources passing the filter over the same 41 nights, or 46.41 per night, which puts stated chance at 0.172. The adjudicators are four other seed statements: 5-15, 5-10, a median of 4.5, and about 10 per night. **The PI RATIFIED k = 8 with the rounding noted (AMD-V1-01).** Still open: Rubin-era k is UNDEMONSTRATED, and on the BTS file the measured chance is 0.225-0.230 because only 61 of 579 nights have more than 8 candidates (wave-2 agent 4, calibration).""",
 "label_source": """Carried verbatim from wave-2 agent 2. Evidence came from archived TNS object pages (Internet Archive), read after a sealed file-only placement. The deciding field is Classifier/s, not the sender, because `ZTF_Bot1` also sends human reports. Of the 7,843 labels: MEASURED 884, SNIascore MODEL_ANNOTATION 803 (799 strong, 4 moderate), PHOTOMETRIC_ONLY 0, UNRESOLVED 6,156. The SNIascore bound tightens from 0-3,131 to **803-2,247**. The upper bound depends on the WEAK E5 phase rule, which is breached twice. The CCSNscore channel is bounded 0-155, with its start date unknown. Without TNS credentials the split is bounded, not determined, so the slot is **UNDEMONSTRATED**.""",
 "exposure_key": """Input public date is alert issuance: ZTF from 2018-06-04, Rubin from 2026-02-24. The label public date is bracketed. The lower bound is the TNS discovery date. The upper bound is the earliest Internet Archive capture of the BTS explorer showing the same type string. The exact date is the TNS classification-report date, which needs credentials. Subject cutoffs come from vendor pages, 10 models in all, and Gemini 3.1 Pro has none. Split against the 2024-12-08 capture: 6,166 labels were public before every cutoff, 0 after every cutoff, and 1,677 are unresolved. Two wave-2 cross-references are attached. The Rubin admission boundary is 2026-07-01T00:00 UTC (bands section 1). Agent 2 also found that TNS discovery date is not a safe lower bound: SN2017bde was discovered in 2017 but classified by SNIascore in 2023.""",
 "tool_inventory": """Agent 4 built this from 30 pinned clones plus weight hashes: 25 decision-time channels, 15 FM/deep and 10 classical, with roles read from code input and output. It carries a readiness census for ZTF and Rubin: on Rubin, 0 verified, 12 AVAILABLE_UNVERIFIED, 12 UNAVAILABLE and 1 UNDEMONSTRATED. Check (b), a role below the line, passes (ParSNIP, SALT3). Check (a), a classical counterpart per FM channel, failed on Rubin for ATAT, Astromer 1 and Astromer 2, because ALeRCE_BHRF has no Rubin weights. **The PI APPROVED the Fink RF remapping (AMD-V1-03).** For those three rows the Rubin counterpart is now Fink_EarlySNIa_RF and Fink_SLSN_RF. It is recorded in `counterparts_by_survey.rubin`, and the wave-1 `counterparts` field and all counts are kept verbatim. Structurally, check (a) on Rubin now holds (`..._after_AMD-V1-03 = true`). That is structural only: the Fink RFs are unverified on real Rubin alerts.""",
 "delta": """Agent 5 took this from arXiv:2401.15167 Appendix B Table 6. The production selector (MM-CNN) reached bts_p2 purity 0.930 against 0.912 for the metadata-only NN on the same test split, and the authors put MM-CNN into production, giving 0.018. Three other candidates were listed and not adopted: BTSbot vs scanners (refused, unequal denominators), SNIascore vs SNID (adjacent referent) and Fink US vs RS (counted over alerts). **Resolution warning:** the unpaired MDE of the source comparison is about 0.045. Wave-2 PRE-I1 calibration on BTS binding nights gives MDE 0.032, so 0.018 is below both. Cost of action was not supplied, so per brief line 13 delta stays 0.018, **DERIVED, not ratified** (AMD-V1-05).""",
 "S": """S = budget / measured hours per workflow (manifest.md). Budget was an unfilled SUPPLY field and R1 has not run, so S is **UNDEMONSTRATED**. It blocks the P5 escape, cohort sizing and the choice of N row in the planning bracket.""",
 "subject_set": """Agent 5 read first-party model pages on 2026-09-16: 7 models from 3 providers, flagship and next tier. No required rung is stated anywhere, so availability is the only criterion. Cutoffs are 'reliable knowledge' or 'knowledge' cutoffs, not training-data ends. Gemini 3.1 Pro has none. This slot governs the Rubin admission boundary (Fable 5.1, Jun 2026) and forces the contamination band to ESCALATE while any member lacks a cutoff. Agent 3's exposure-key table lists 10 models, against 7 here; that disagreement is listed.""",
 "decision_epoch": """**Declared and RATIFIED by the PI in the hashed wave-2 brief (line 15), before any composition ran (AMD-V1-02).** Primary is first alert; secondary is night 3. Wave-2 agent 4 operationalised it for ZTF calibration in compositions_FROZEN.md section 1:
- **E1:** the triggering detection plus the 30-day prv_candidates history.
- **E3:** photometry through ZTF night n0+3, with nights split at 20:00 UTC.

This freeze re-checked that declaration against the ratified value: **MATCH**. No Rubin composition has been declared. Rubin first detection is defined in bands section 3.""",
}

ORDER = ["tau", "k", "label_source", "exposure_key", "tool_inventory", "delta", "S", "subject_set", "decision_epoch"]

def fmt_val(slot, v):
    if slot == "label_source":
        return json.dumps({k: v["value"][k] for k in ("population", "category_counts", "sniascore_bound")}, ensure_ascii=False)[:900]
    if slot == "exposure_key":
        return "key_definition + 10 subject cutoffs + two capture splits (see manifest; too long to inline)"
    if slot == "tool_inventory":
        return "25 channels; Rubin counterparts after AMD-V1-03: ATAT, Astromer1, Astromer2 -> [Fink_EarlySNIa_RF, Fink_SLSN_RF]"
    if slot == "subject_set":
        return json.dumps(v["value"])
    if slot == "tau":
        return json.dumps({k: v["value"][k] for k in ("radius_arcsec", "n_clusters_bts", "plateau_arcsec")})
    return json.dumps(v["value"], ensure_ascii=False)

L = []
L.append("# D5 presentation: manifest v1 (wave-2 brief)\n")
L.append(f"- **Manifest:** `domain_manifest_v1.json`, frozen_hash `{m['frozen_hash']}`.")
L.append(f"- **Hash method:** {m['hash_method']}.")
L.append(f"- **Governing brief:** `{W2}`, sha256 `{W2SHA}` (verified).")
L.append(f"- **Amendment ledger:** `amendment_ledger.json`, v1 entries canonical sha256 `{led['v1_entries_canonical_sha256']}`.\n")
L.append("Below, each slot is shown with its derivation, its five provenance fields (copied verbatim from the frozen file) and its status, followed by an explicit invitation to override. Ratification means accepting or correcting a derivation already on the page (discovery.md D5). Any override, with its reason, becomes a new amendment-ledger entry and a new hashed manifest version. v1 itself is never edited.\n")
L.append("## Status at a glance\n")
L.append("| Slot | v1 value | Status | Ledger |")
L.append("|---|---|---|---|")
ledmap = {"k": "AMD-V1-01", "decision_epoch": "AMD-V1-02", "tool_inventory": "AMD-V1-03", "delta": "AMD-V1-05", "S": "AMD-V1-06", "label_source": "SU-V1-01"}
short = {"tau": "1 arcsec", "k": "8", "label_source": "SNIascore 803-2,247; 6,156 unresolved", "exposure_key": "alert issuance / bracketed label date", "tool_inventory": "25 channels, Fink RF remap on 3 Rubin rows", "delta": "0.018 (resolution warning)", "S": "none", "subject_set": "7 models", "decision_epoch": "first alert / night 3"}
for s in ORDER:
    st = m[s]["status"]
    L.append(f"| {s} | {short[s]} | **{st}** | {ledmap.get(s, 'none (no PI ruling)')} |")
L.append("\n**D5 disposition: UNDEMONSTRATED (does not advance).**")
L.append("- **Freeze:** PASS. The manifest is frozen and hashed.")
L.append("- **Every slot ratified or overridden:** FAIL. tau, exposure_key and subject_set are still DERIVED, delta is DERIVED, and label_source and S are UNDEMONSTRATED.")
L.append("- **Disagreement with the brief:** brief line 35 expects D5 to close except for the SUPPLY fields, but the PI decisions rule only on k, the decision epoch and the remapping. This freeze does not ratify anything on the PI's behalf. Listed, not reconciled.\n")

for s in ORDER:
    v = m[s]
    L.append(f"## {s}\n")
    L.append(f"**Value (v1):** `{fmt_val(s, v)}`\n")
    L.append(f"**Status:** {v['status']}. {v.get('status_note', '')}")
    if v.get("override_reason"):
        L.append(f"\n**Override reason:** {v['override_reason']}")
    L.append(f"\n**Derivation.** {DERIV[s]}\n")
    L.append("**Provenance (five fields):**\n")
    for f in ("referent", "source", "population", "adjudicator", "falsifier"):
        L.append(f"- **{f}:** {v['provenance'][f]}")
    if v.get("resolution_warning"):
        L.append(f"\n**Resolution warning:** {v['resolution_warning']}")
    if v.get("disagreements"):
        L.append("\n**Disagreements (listed, not reconciled):**")
        for d in v["disagreements"]:
            L.append(f"- {d}")
    L.append(f"\n> **Override invitation ({s}).** " + v["override_invitation"].replace("Override invitation: ", ""))
    if s in ("tau", "exposure_key", "subject_set"):
        L.append("> The PI has not ruled on this slot. Reply RATIFY, or give a replacement value and a reason.")
    if s == "delta":
        L.append("> Supplying cost of action overrides this, and the PI may override delta directly with a stated cause. Until then it stays 0.018.")
    if s == "label_source":
        L.append("> Options: ratify the bounded state (UNDEMONSTRATED; P4 precondition (c) stays unmet unless measured P and Ng exist), supply TNS credentials, or name a different label source.")
    L.append("")

L.append("## SUPPLY fields (not derivable from the corpus)\n")
L.append("| Field | v1 | Blocks |")
L.append("|---|---|---|")
for r in m["d5_inputs"]:
    L.append(f"| {r['id']} | UNDEMONSTRATED (unfilled placeholder) | {', '.join(r['blocks'])} |")
L.append("\n> **Invitation.** Supply budget (arm cells or hours), cost of action (the value of a spectrum slot and of a wrong commitment, or the smallest precision gain that would change the programme's tool), a rulings holder who authored neither the skill nor any case, and TNS credentials.\n")
L.append("## Graph escalation (not an amendment)\n")
L.append("Edge R1 → I1: the wave-2 compositions are PRE-I1 CALIBRATION, pending a PI ruling on the ordering (coordinator preamble item 2, ladder rung 2). Ledger ESC-V1-01.\n")
L.append("> **Invitation.** Rule on the staging: ratify it as staged, or require R1 before any composition counts.\n")
L.append("## Candidate\n")
c = m["candidates"][0]
L.append(f"- **Candidate:** {c['name']} (branch: {c['branch']}).")
L.append(f"- **Decision governed:** {c['decision_governed']}.")
L.append(f"- **Calibration cohort:** {c['cohorts']['calibration_only']}.")
L.append(f"- **Prospective cohort:** {c['cohorts']['prospective']}.")
L.append(f"- **P4 at v1:** {c['p4_state_at_v1']}.")
open(rp(f"{OUT}/D5_presentation.md"), "w").write("\n".join(L) + "\n")
print("written")
