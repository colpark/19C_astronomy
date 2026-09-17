#!/usr/bin/env python3
"""Per-slot diffs v1->v2 and v2->v3 from the frozen files, with a cause (ledger id + brief locator) per changed slot."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common4 import *  # noqa

v1 = load(f"{W3OUT}/domain_manifest_v1.json"); v2 = load(f"{W3OUT}/domain_manifest_v2.json"); v3 = load(f"{OUT}/domain_manifest_v3.json")
for m in (v1, v2, v3):
    assert manifest_hash(m) == m["frozen_hash"]

def leaves(o, p="$"):
    if isinstance(o, dict):
        if not o: yield p, o
        for k, v in o.items(): yield from leaves(v, f"{p}.{k}")
    elif isinstance(o, list):
        if not o: yield p, o
        for i, v in enumerate(o): yield from leaves(v, f"{p}[{i}]")
    else:
        yield p, o

def diff(a, b):
    la, lb = dict(leaves(a)), dict(leaves(b))
    added = sorted(set(lb) - set(la)); removed = sorted(set(la) - set(lb))
    changed = sorted(k for k in set(la) & set(lb) if la[k] != lb[k])
    return la, lb, added, removed, changed

def short(v):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= 90 else s[:87] + "..."

CAUSE12 = {
 "tau": None, "k": None, "subject_set": None,
 "label_source": "SU-V2-03 (agent 2 wave-3 slot supersedes wave-2 slot; bound [803,2247] -> [954,2057]); PENDING-V2-01 resolved. PANEL_BRIEF_WAVE3.md Assignments, Agent 2 and Agent 3",
 "exposure_key": "SU-V2-02 (agent 1 wave-3 leak, PPDB, Rubin first-time field) and agent 2 wave-3 position leak; PANEL_BRIEF_WAVE3.md Assignments, Agent 1 and 2",
 "tool_inventory": "SU-V2-01 (agent 4 wave-3 functional recount, remap consistency); PANEL_BRIEF_WAVE3.md Assignments, Agent 4",
 "delta": "AMD-V2-04 (PI ruling 2: OVERRIDDEN 0.018 -> 0.05, prior carried); PANEL_BRIEF_WAVE3.md lines 18-19",
 "S": "AMD-V2-01, AMD-V2-02 (ruling 1: budget supplied, S computed at R1, re-ratification gate); PANEL_BRIEF_WAVE3.md line 13",
 "decision_epoch": "AMD-V2-08 (ruling 6: reaffirmed; strata S0/S1/S2 with S2 disagreement); PANEL_BRIEF_WAVE3.md line 23",
 "supplied_by_human": "AMD-V2-01, 03, 06, 07 (rulings 1, 2, 4, 5); PANEL_BRIEF_WAVE3.md lines 13-22",
 "d5_inputs": "AMD-V2-01, 03, 06, 07 (records rebuilt from rulings 1, 2, 4, 5)",
 "candidates": "SU-V2-02, SU-V2-04 (cohort counts, supply lower bounds), axis ledger v2 final",
 "graph_escalations": "AMD-V2-05 (ruling 3: escalation RATIFIED as staged); PANEL_BRIEF_WAVE3.md line 20",
 "d5_disposition": "consequence of the v2 slot statuses (no PI ruling on tau, exposure_key, subject_set)",
 "pi_reratification_inputs": "SU-V2-05 (truth cost attached for ruling 1 re-ratification)",
 "amendment_ledger": "ledger pointer updated for v2 entries",
 "governing_brief": "v2 governed by PANEL_BRIEF_WAVE3.md", "manifest_version": "version", "inputs_state": "version", "derived_from": "version lineage",
 "completeness": "restated for v2", "disagreements_v2": "new wave-3 disagreements (S2, truth-cost target, metric vs cost, JSON rows, run count, agent 2 items)",
}
CAUSE23 = {
 "tau": "RE-V3-02 rule E marks only (value unchanged; V_PENDING, no V record); no PI ruling (wave-4 brief rules on none)",
 "k": "RE-V3-02 rule E marks only (k 8 V_PENDING; K01/K02 CLEARED); value and status unchanged",
 "subject_set": "RE-V3-02 rule E note only; no PI ruling",
 "label_source": "AMD-V3-02 (ruling 4 RATIFIED WITH CONDITIONS, conditions verbatim) + RE-V3-01 (numeric fields V_PENDING, V-L01..L05 DISCREPANCY, readings (i) E5 cut, (ii) twin keying) + AMD-V3-04 (TNS/WISeREP BLOCKED); PANEL_BRIEF_WAVE4.md lines 5, 16-20",
 "exposure_key": "RE-V3-02 rule E marks (C01 CLEARED; leak and BTS split V_PENDING)",
 "tool_inventory": "RE-V3-02 rule E marks (T01-T03 CLEARED); V invariance note; status unchanged (OVERRIDDEN)",
 "delta": "AMD-V3-01 (ruling 1: OVERRIDDEN -> RATIFIED; cause check V-O01 with git/time-zone caveats; 0.018 carried) + RE-V3-02 (P01-P08, K01-K02, A01-A04, N01-N02 CLEARED; family-A nights V_PENDING; sqrt(q) note); PANEL_BRIEF_WAVE4.md lines 5, 9-14",
 "S": "RE-V3-02 rule E marks (budget PI_RULED; planning rounds V_PENDING); status unchanged",
 "decision_epoch": "RE-V3-02 rule E marks (S1 C03 CLEARED; S0 V_PENDING); S2 conflict carried unchanged",
 "supplied_by_human": "AMD-V3-04 (ruling 3: TNS second BLOCKED record, WISeREP BLOCKED) + AMD-V3-05 (ruling 2: custody PENDING_RECEIPT, procedural); PANEL_BRIEF_WAVE4.md lines 15-16",
 "d5_inputs": "AMD-V3-04 (request dates, WISeREP)",
 "candidates": "RE-V3-02 rule E marks (C01-C04 CLEARED; U, nights, census V_PENDING); P4 state from axis ledger v3 (preconditions (b) V-O02, (c) AMD-V3-03)",
 "graph_escalations": "AMD-V3-06 (ruling 5: module V chartered; overhead cap exceeded, interim)",
 "d5_disposition": "AMD-V3-01, AMD-V3-02 (delta and label_source now RATIFIED); tau, exposure_key, subject_set still DERIVED",
 "pi_reratification_inputs": "RE-V3-02 (truth cost R01-R04 CLEARED; wave-4 monthly pricing V_PENDING); state note",
 "amendment_ledger": "pointer to amendment_ledger_v3.json (append-only) with v1/v2/v3 entry hashes",
 "governing_brief": "v3 governed by PANEL_BRIEF_WAVE4.md", "manifest_version": "version", "inputs_state": "version", "derived_from": "version lineage (v2, v1 hashes)",
 "completeness": "restated for v3", "naming_disagreement": "NAME-V3-01 (brief 'freeze v2' vs v3; preamble item 1)",
 "module_v": "ruling 5 / rule E: V records pointer", "rule_E_index": "RE-V3-02", "disagreements_v3": "new wave-4 disagreements",
 "open_items_carried": "carried forward unchanged (tau, exposure_key, subject_set; S2; disagreements_v2)",
}

def render(a, b, na, nb, causes, fname, title, brief):
    L = [f"# {title}\n",
         f"- **From:** `{na}`, frozen_hash `{a['frozen_hash']}`.",
         f"- **To:** `{nb}`, frozen_hash `{b['frozen_hash']}`.",
         f"- **Cause authority:** {brief}. Ledger ids refer to `amendment_ledger_v3.json` (append-only).",
         "- **Method:** leaf-path comparison of the two frozen JSON files (frozen_hash and frozen_utc excluded). Every changed top-level key has one cause line; unchanged slots are listed as unchanged.\n",
         "| Key | Status before → after | Leaves added / removed / changed | Cause |", "|---|---|---|---|"]
    keys = [k for k in dict.fromkeys(list(a.keys()) + list(b.keys())) if k not in ("frozen_hash", "frozen_utc")]
    detail = []
    for k in keys:
        if a.get(k) == b.get(k):
            L.append(f"| {k} | {(a.get(k) or {}).get('status', '') if isinstance(a.get(k), dict) else ''} (unchanged) | 0 / 0 / 0 | unchanged |")
            continue
        _, _, ad, rm, ch = diff(a.get(k, {}), b.get(k, {}))
        sa = a.get(k, {}).get("status", "") if isinstance(a.get(k), dict) else ""
        sb = b.get(k, {}).get("status", "") if isinstance(b.get(k), dict) else ""
        cause = causes.get(k)
        assert cause, f"no cause for changed key {k}"
        L.append(f"| {k} | {sa or '-'} → {sb or '-'} | {len(ad)} / {len(rm)} / {len(ch)} | {cause} |")
        la, lb = dict(leaves(a.get(k, {}))), dict(leaves(b.get(k, {})))
        detail.append(f"\n## {k}\n\n**Cause:** {cause}\n")
        for label, paths, fn in (("changed", ch, lambda p: f"`{short(la[p])}` → `{short(lb[p])}`"), ("added", ad, lambda p: f"`{short(lb[p])}`"), ("removed", rm, lambda p: f"`{short(la[p])}`")):
            if not paths: continue
            detail.append(f"- **{label}** ({len(paths)}):")
            for p in paths[:25]:
                detail.append(f"  - `{p}`: {fn(p)}")
            if len(paths) > 25:
                detail.append(f"  - ... {len(paths) - 25} more (reproduce with scripts/diffs.py)")
    open(rp(f"{OUT}/{fname}"), "w").write("\n".join(L + detail) + "\n")

render(v1, v2, f"{W3OUT}/domain_manifest_v1.json", f"{W3OUT}/domain_manifest_v2.json", CAUSE12, "diff_v1_v2.md",
       "Diff v1 → v2 (both frozen in wave 3; published in wave 4)", "PANEL_BRIEF_WAVE3.md (sha256 a618d911...c4b6) rulings 1-6 and wave-3 fold-ins")
render(v2, v3, f"{W3OUT}/domain_manifest_v2.json", f"{OUT}/domain_manifest_v3.json", CAUSE23, "diff_v2_v3.md",
       "Diff v2 → v3 (wave 4)", "PANEL_BRIEF_WAVE4.md (sha256 8f101811...1b58) rulings 1-5, rule E, preamble items 1-5")
log("7", "diff_v1_v2.md and diff_v2_v3.md generated from frozen files (every changed key has a cause; script asserts)",
    [f"{OUT}/diff_v1_v2.md", f"{OUT}/diff_v2_v3.md", f"{OUT}/scripts/diffs.py"])
