#!/usr/bin/env python3
"""Aggregate census/notes/*.json into census/branch_census.json and census/depth_census.json.
Counts only; no re-tagging. measured depth stays not_measured."""
import json, glob, collections, hashlib, os
here = os.path.dirname(os.path.abspath(__file__)); base = os.path.dirname(here)
notes = sorted(glob.glob(os.path.join(base, "census/notes/*.json")))
KINDS = ["intervene","explain","generate","infer"]
seeds = []; allb = []; totals = collections.Counter()
for p in notes:
    o = json.load(open(p)); sid = o["seed_id"]
    b = o["branches"]; eps = {e["episode_id"]: e for e in o["episodes"]}
    per_ep = collections.Counter(x["episode_id"] for x in b)
    per_ep_obj = collections.Counter(x["episode_id"] for x in b if x["level"]=="per_object")
    kc = {lvl: {k: sum(1 for x in b if x["level"]==lvl and x["kind"]==k) for k in KINDS} for lvl in ("per_object","per_study")}
    rec = {"seed_id": sid, "title": o["title"], "arxiv_version_verified": o["arxiv_version_verified"],
      "read_in_full": o["read_in_full"], "reader": o["reader"], "layout_lines_read": f"1-{o['layout_lines']}", "pages": o["pages"],
      "notes_file": os.path.relpath(p, base), "notes_sha256": hashlib.sha256(open(p,"rb").read()).hexdigest(),
      "episodes": [{"episode_id": e["episode_id"], "level": e["level"], "practitioner_action": e["practitioner_action"],
                    "action_locator": e["action_locator"], "chain_length": e["chain_length"],
                    "branches_in_episode": per_ep.get(e["episode_id"],0), "per_object_branches_in_episode": per_ep_obj.get(e["episode_id"],0)} for e in o["episodes"]],
      "branch_points_total": len(b),
      "branch_points_with_alternative_visible": sum(1 for x in b if x["alternatives_visible"]),
      "branch_points_with_rejected_option_named": sum(1 for x in b if x["rejected_named"]),
      "max_branches_per_episode": max(per_ep.values()) if per_ep else 0,
      "max_per_object_branches_per_episode": max(per_ep_obj.values()) if per_ep_obj else 0,
      "by_level_and_kind": kc,
      "branches": [{k: x[k] for k in ("id","episode_id","level","kind","choice","alternatives_visible","rejected_named","rejected_option","locator","quote")} for x in b]}
    seeds.append(rec)
    for x in b:
        allb.append((sid, x)); totals[(x["level"], x["kind"])] += 1
        totals["named"] += x["rejected_named"]; totals["altvis"] += bool(x["alternatives_visible"])
summary = {"seeds": len(seeds), "branch_points_total": len(allb),
  "with_alternative_visible": totals["altvis"], "with_rejected_option_named": totals["named"],
  "per_object": {k: totals[("per_object",k)] for k in KINDS}, "per_study": {k: totals[("per_study",k)] for k in KINDS},
  "per_object_named_rejection": {k: sum(1 for s,x in allb if x["level"]=="per_object" and x["kind"]==k and x["rejected_named"]) for k in KINDS},
  "seeds_with_per_object_branch_of_kind": {k: sorted({s for s,x in allb if x["level"]=="per_object" and x["kind"]==k}) for k in KINDS},
  "per_object_episodes_with_two_or_more_branches": [f"{r['seed_id']}:{e['episode_id']}({e['per_object_branches_in_episode']})" for r in seeds for e in r["episodes"] if e["per_object_branches_in_episode"]>=2]}
out = {"record": "D1 branch-point census, wave 5 agent 1", "method": "shape.md 'The chain and the branch'; every branch carries a layout-text locator and a verbatim quote verified by checkquotes.py (0 failures on all seeds)",
  "kind_rule": "intervene=spend a scarce resource; explain=which cause; generate=which object/model to build under a constraint; infer=which value/class the data implies; tagged by the choice at the branch, ambiguity written in the notes' reason field",
  "level_rule": "per_object = a judgment specific to one object; per_study = a design choice made once for the study. A uniform cut applied to all objects is chain.",
  "summary": summary, "seeds": seeds,
  "completeness": "Covers the 12 seeds listed, each read in full (layout text L1 to last line incl. references). Tagging of generate vs infer for model-building and fitting-procedure branches is ambiguous in 9 branches, recorded in the notes' reason fields and not re-tagged. Seeds not covered: companion papers (DR2 fitting papers, AT2018cow X-ray/radio papers, Villar 2020 SuperRAENN, SALT3 F22 recalibration) were not read."}
json.dump(out, open(os.path.join(base,"census/branch_census.json"),"w"), indent=1, ensure_ascii=False)
# depth census
dseeds = []
for p in notes:
    o = json.load(open(p))
    dseeds.append({"seed_id": o["seed_id"], "conclusions": [{**{k: c[k] for k in ("id","conclusion","channels_claimed","n_channels_claimed","locator","quote")},
        "measured_depth": "not_measured", "measured_depth_method": "not_measured (I2 leave-one-out not run)"} for c in o["conclusions_depth"]]})
allc = [c for s in dseeds for c in s["conclusions"]]
dist = collections.Counter(c["n_channels_claimed"] for c in allc)
dout = {"record": "D1 evidence-depth census, wave 5 agent 1", "measured_depth_status": "not_measured for every conclusion; refusal 11: stratify on measured depth only, so all items are depth one until I2 runs leave-one-out",
  "summary": {"conclusions": len(allc), "claimed_channel_count_distribution": dict(sorted(dist.items())),
    "subset_of_channels_supported_wrong_conclusion_found": ["1808.00969 early Ic-BL association from early spectra plus radio, overturned by later time series (see 1808.00969 notes COW-B09)", "2104.12980 SN 2020eyj: spectrum-only SNID match to SN Ia overturned when light curve added (B14)", "2104.12980 SN 2018cne: SN Ia SNID matches vs light curve inconsistent with normal Ia (B15)"],
    "author_reported_ablations_not_measured_depth": ["2403.07975 with vs without redshift F1 0.61 vs 0.71", "2405.03078 light curve + metadata synergy +20-30% F1"]},
  "seeds": dseeds,
  "completeness": "Every channel-combining conclusion the readers recorded in the 12 seeds; channels are as the authors claim them. No leave-one-out has been run, so no measured depth exists. Independent systems measured at each depth (supply) are not counted: P3 is refused before shape ratification (shape.md refusal 1)."}
json.dump(dout, open(os.path.join(base,"census/depth_census.json"),"w"), indent=1, ensure_ascii=False)
print(json.dumps(summary, indent=1)); print("conclusions", len(allc), dict(sorted(dist.items())))
