"""Mechanical floor, grader_protocol_FROZEN.md section 9: generators at defaults, keep the best on one metric.
PRE-RATIFICATION PILOT (harness check only).

usage: floor_generators.py ITEM_DIR OUT_DIR
Uses the arm-asset SALT3 copy (not the grader copy) and the arm-tool forward_models copy for the metric."""
import importlib.util
import json
import os
import sys
import traceback

import numpy as np
import pandas as pd

AGENT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot"
sys.path.insert(0, os.path.join(AGENT, "scripts"))
from item_builder import check_protocol, sha256  # noqa

FM_PATH = os.path.join(AGENT, "arms", "tools", "classical", "forward_models.py")
SALT3_DIR = os.path.join(AGENT, "data_cache", "arm_assets_classical", "salt3-f22")


def load_fm():
    spec = importlib.util.spec_from_file_location("arm_forward_models", FM_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def salt3_default(pre, meta, fm):
    import sncosmo
    from astropy.table import Table
    models = fm.ForwardModels(salt3_dir=SALT3_DIR)
    model = models.sn_model("SALT3", meta["mwebv"])
    data = Table({"time": pre.mjd.values, "band": pre.band.values, "flux": pre.flux.values,
                  "fluxerr": pre.fluxerr.values, "zp": np.full(len(pre), 25.0), "zpsys": np.full(len(pre), "ab")})
    res, fitted = sncosmo.fit_lc(data, model, ["z", "t0", "x0", "x1", "c"], bounds={"z": (0.005, 0.3)})
    params = {k: float(fitted[k]) for k in ("z", "t0", "x0", "x1", "c")}
    return params, {"success": bool(res.success), "message": str(res.message), "ncall": int(res.ncall),
                    "sncosmo_chisq": float(res.chisq), "ndof": int(res.ndof)}


def bazin_default(pre, fm):
    from scipy.optimize import least_squares
    out, info = {}, {}
    for b in fm.BANDS:
        d = pre[pre.band == b]
        if len(d) == 0:
            raise ValueError(f"no pre-cut detections in {b}")
        t, f, e = d.mjd.values, d.flux.values, d.fluxerr.values
        i = int(np.argmax(f))
        p0 = [1.5 * f[i], t[i] - 5.0, 3.0, 20.0, 0.0]
        lo = [0.0, -np.inf, 1e-3, 1e-3, -np.inf]
        hi = [np.inf, np.inf, 500.0, 500.0, np.inf]
        p0 = list(np.clip(p0, np.array(lo) + 0.0, hi))
        r = least_squares(lambda p: (f - fm.bazin(t, *p)) / e, p0, bounds=(lo, hi), method="trf")
        out[b] = dict(zip(fm.PARAM_KEYS["Bazin"], [float(x) for x in r.x]))
        info[b] = {"status": int(r.status), "nfev": int(r.nfev), "n_points": int(len(d))}
    return out, info


def run(item_dir, out_dir):
    check_protocol()
    fm = load_fm()
    os.makedirs(out_dir, exist_ok=True)
    meta = json.load(open(os.path.join(item_dir, "item_meta.json")))
    pre_all = pd.read_csv(os.path.join(item_dir, "pre_cut.csv"))
    pre = pre_all[pre_all.kind == "detection"].reset_index(drop=True)
    models = fm.ForwardModels(salt3_dir=SALT3_DIR)
    cands, log = {}, {"item_id": meta["item_id"], "pre_cut_sha256": sha256(os.path.join(item_dir, "pre_cut.csv")),
                      "forward_models_sha256": sha256(FM_PATH), "generators": {}}
    for name, fn in (("SALT3", lambda: salt3_default(pre, meta, fm)), ("Bazin", lambda: bazin_default(pre, fm))):
        try:
            params, info = fn()
            pred = models.predict(name, params, pre.mjd.values, pre.band.values, meta["mwebv"])
            chi = fm.chi2_per_point_all(pre.flux.values, pre.fluxerr.values, pred)
            if not np.isfinite(chi):
                raise ValueError("non-finite pre-cut chi2")
            cands[name] = (chi, params)
            log["generators"][name] = {"status": "ok", "pre_cut_chi2_per_point": chi, "parameters": params, "info": info}
        except Exception:  # noqa
            log["generators"][name] = {"status": "raised", "traceback": traceback.format_exc()}
    if not cands:
        log["floor"] = "COVERAGE_FAIL:EVAL (both generators raised)"
        json.dump(log, open(os.path.join(out_dir, "floor_log.json"), "w"), indent=1)
        return log
    order = sorted(cands, key=lambda k: (cands[k][0], 0 if k == "SALT3" else 1))
    best = order[0]
    rivals = [{"family": k, "reason": f"mechanical floor: pre-cut chi2 per point {cands[k][0]:.4f} >= chosen {cands[best][0]:.4f}"}
              for k in order[1:]]
    for k in ("SALT3", "Bazin"):
        if k not in cands and k != best:
            rivals.append({"family": k, "reason": "mechanical floor: generator raised at defaults"})
    sub = {"item_id": meta["item_id"], "family": best, "parameters": cands[best][1], "rejected_rivals": rivals,
           "notes": "mechanical floor (grader_protocol_FROZEN.md section 9); no agent"}
    json.dump(sub, open(os.path.join(out_dir, "submission.json"), "w"), indent=1)
    log["floor"] = best
    log["submission_sha256"] = sha256(os.path.join(out_dir, "submission.json"))
    json.dump(log, open(os.path.join(out_dir, "floor_log.json"), "w"), indent=1)
    return log


if __name__ == "__main__":
    print(json.dumps(run(sys.argv[1], sys.argv[2]), indent=1))
