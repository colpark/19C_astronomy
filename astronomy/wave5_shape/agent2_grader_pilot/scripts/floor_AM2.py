"""AM-2 mechanical floor: SALT3 fit_lc at defaults only (protocol section 9 generator 1). PRE-RATIFICATION PILOT (harness check only)."""
import json, os, sys
import pandas as pd
AGENT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot"
sys.path.insert(0, os.path.join(AGENT, "scripts"))
import floor_generators as FG  # noqa
from item_builder import check_protocol, sha256  # noqa

def run(item_dir, out_dir):
    check_protocol()
    fm = FG.load_fm()
    os.makedirs(out_dir, exist_ok=True)
    meta = json.load(open(os.path.join(item_dir, "item_meta.json")))
    pre = pd.read_csv(os.path.join(item_dir, "pre_cut.csv"))
    pre = pre[pre.kind == "detection"].reset_index(drop=True)
    params, info = FG.salt3_default(pre, meta, fm)
    m = fm.ForwardModels(salt3_dir=FG.SALT3_DIR)
    chi = fm.chi2_per_point_all(pre.flux.values, pre.fluxerr.values, m.predict("SALT3", params, pre.mjd.values, pre.band.values, meta["mwebv"]))
    sub = {"item_id": meta["item_id"], "family": "SALT3", "parameters": params,
           "rejected_rivals": [{"family": f, "reason": "mechanical floor under AM-2: not a grader-renderable submittable family"} for f in ("Bazin", "Villar", "ParSNIP")],
           "notes": "AM-2 mechanical floor: sncosmo fit_lc SALT3 at defaults (z bounds 0.005-0.3), no agent"}
    json.dump(sub, open(os.path.join(out_dir, "submission.json"), "w"), indent=1)
    log = {"item_id": meta["item_id"], "pre_cut_sha256": sha256(os.path.join(item_dir, "pre_cut.csv")), "forward_models_sha256": sha256(FG.FM_PATH),
           "fit_info": info, "pre_cut_chi2_per_point": chi, "submission_sha256": sha256(os.path.join(out_dir, "submission.json"))}
    json.dump(log, open(os.path.join(out_dir, "floor_log.json"), "w"), indent=1)
    return log

if __name__ == "__main__":
    print(json.dumps(run(sys.argv[1], sys.argv[2]), indent=1))
