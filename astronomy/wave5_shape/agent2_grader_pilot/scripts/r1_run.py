"""R1 harness control on a synthetic item (r1/dispositions_PRE_RUN.md). PRE-RATIFICATION PILOT (harness check only)."""
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import chi2

AGENT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot"
sys.path.insert(0, os.path.join(AGENT, "scripts"))
sys.path.insert(0, AGENT)
from item_builder import check_protocol, sha256, split, write_item, counts, PROTOCOL_SHA  # noqa
import simulate  # noqa
import floor_generators as FG  # noqa
import grade as G  # noqa

R1 = os.path.join(AGENT, "r1")
DISP_SHA = open(os.path.join(R1, "dispositions_PRE_RUN.sha256")).read().split()[0]


def main():
    check_protocol()
    assert sha256(os.path.join(R1, "dispositions_PRE_RUN.md")) == DISP_SHA
    seed = int(PROTOCOL_SHA[:8], 16)
    fm = simulate.load_fm()
    truth = {"z": 0.05, "t0": 59800.0, "x0": 1.2e-3, "x1": 0.5, "c": 0.05}
    lc, tinfo = simulate.simulate("SALT3", truth, 0.03, seed)
    json.dump(lc, open(os.path.join(R1, "synthetic_lightcurve_alerce_format.json"), "w"), indent=1)
    sp = split(lc)
    item_id = "R1-SYNTH-001"
    hashes = write_item(sp, item_id, 0.03, os.path.join(R1, "item"), os.path.join(R1, "grader_private"),
                        private_extra={"truth": tinfo})
    rec = {"protocol_sha256": PROTOCOL_SHA, "dispositions_sha256": DISP_SHA, "seed": seed, "truth": tinfo,
           "counts": counts(sp), "item_hashes_at_build": {os.path.relpath(k, AGENT): v for k, v in hashes.items()}}
    subs = os.path.join(R1, "submissions")
    os.makedirs(subs, exist_ok=True)
    json.dump({"item_id": item_id, "family": "SALT3", "parameters": truth,
               "rejected_rivals": [{"family": "Bazin", "reason": "R1 stub: true parameters of the simulator"}]},
              open(os.path.join(subs, "true_params.json"), "w"), indent=1)
    pre = pd.read_csv(os.path.join(R1, "item", "pre_cut.csv"))
    pre = pre[pre.kind == "detection"].reset_index(drop=True)
    bz, info = FG.bazin_default(pre, FG.load_fm())
    json.dump({"item_id": item_id, "family": "Bazin", "parameters": bz,
               "rejected_rivals": [{"family": "SALT3", "reason": "R1 stub: deliberately wrong family (floor Bazin generator on pre-cut)"}]},
              open(os.path.join(subs, "wrong_family.json"), "w"), indent=1)
    grades = {}
    for tag in ("true_params", "wrong_family"):
        g = G.grade(os.path.join(subs, tag + ".json"), os.path.join(R1, "item"), os.path.join(R1, "grader_private"))
        json.dump(g, open(os.path.join(subs, tag + ".grade.json"), "w"), indent=1)
        grades[tag] = g
    # floor end to end (recorded only)
    flog = FG.run(os.path.join(R1, "item"), os.path.join(R1, "floor"))
    gf = G.grade(os.path.join(R1, "floor", "submission.json"), os.path.join(R1, "item"), os.path.join(R1, "grader_private"))
    json.dump(gf, open(os.path.join(R1, "floor", "grade.json"), "w"), indent=1)

    a, b = grades["true_params"], grades["wrong_family"]
    held_hash = hashes[os.path.join(R1, "grader_private", "held_out.csv")]
    P1 = a["status"] != "ITEM_UNSCOREABLE"
    near = {}
    if a["status"] == "SCORED":
        for band, v in a["per_band"].items():
            thr = chi2.ppf(0.995, v["N"]) / v["N"]
            near[band] = {"chi2_per_point": v["chi2_per_point"], "threshold": float(thr), "ok": bool(v["chi2_per_point"] <= thr)}
    P2 = a["status"] == "SCORED" and all(x["ok"] for x in near.values())
    P3 = a["status"] == "SCORED" and b["status"] == "SCORED" and b["S"] > a["S"]
    keys = ("protocol_sha256", "forward_models_sha256", "grade_py_sha256", "item_meta_sha256", "held_out_sha256", "submission_sha256")
    P4 = all(all(k in g for k in keys) and g["held_out_sha256"] == held_hash for g in (a, b))
    grader_error = any(g["status"] == "GRADER_ERROR" for g in (a, b))
    if not P1:
        disp = "R1-UNDEMONSTRATED"
    elif grader_error or not (P2 and P3 and P4):
        disp = "R1-FAIL (instrument)"
    else:
        disp = "R1-PASS"
    rec.update({"criteria": {"P1_scoreable": P1, "P2_true_near_ideal": P2, "near_ideal_detail": near,
                             "P3_wrong_family_worse": P3, "P4_hashes": P4},
                "S_true": a.get("S"), "Q_true": a.get("Q"), "S_wrong_family": b.get("S"), "Q_wrong_family": b.get("Q"),
                "statuses": {"true_params": a["status"], "wrong_family": b["status"]},
                "floor_recorded_only": {"choice": flog.get("floor"), "status": gf["status"], "S": gf.get("S"), "Q": gf.get("Q"),
                                        "generators": {k: v.get("pre_cut_chi2_per_point", v.get("status")) for k, v in flog["generators"].items()}},
                "disposition": disp})
    json.dump(rec, open(os.path.join(R1, "r1_result.json"), "w"), indent=1)
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
