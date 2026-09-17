"""Synthetic ZTF-like light curves in ALeRCE lightcurve JSON format (grader_protocol_FROZEN.md section 8).
PRE-RATIFICATION PILOT (harness check only)."""
import importlib.util
import os

import numpy as np

AGENT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot"
FM_PATH = os.path.join(AGENT, "arms", "tools", "fm", "forward_models.py")
ASSETS = os.path.join(AGENT, "data_cache", "arm_assets_fm")
PEAK, LIM_MAG = 59800.0, 20.5
SIG_LIM = 10 ** (-0.4 * (LIM_MAG - 25.0)) / 5.0


def load_fm():
    spec = importlib.util.spec_from_file_location("sim_forward_models", FM_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sim_models(fm):
    return fm.ForwardModels(salt3_dir=os.path.join(ASSETS, "salt3-f22"),
                            parsnip_code_dir=os.path.join(ASSETS, "parsnip_code"),
                            parsnip_pt=os.path.join(ASSETS, "parsnip_fold0.pt"))


def cadence(rng):
    rows = []
    for fid, off in ((1, 0.0), (2, 0.02)):
        for k, t in enumerate(np.arange(PEAK - 30.0, PEAK + 70.0 + 1e-9, 3.0)):
            if rng.random() < 0.2:
                continue
            rows.append((t + off + rng.uniform(-0.3, 0.3), fid))
    rows.sort()
    return np.array([r[0] for r in rows]), np.array([r[1] for r in rows])


def simulate(family, params, mwebv, seed, models=None):
    fm = load_fm()
    models = models or sim_models(fm)
    rng = np.random.default_rng(seed)
    t, fid = cadence(rng)
    band = np.where(fid == 1, "ztfg", "ztfr")
    ftrue = models.predict(family, params, t, band, mwebv)
    sig = np.sqrt(SIG_LIM ** 2 + (0.02 * ftrue) ** 2)
    fobs = ftrue + rng.normal(0.0, 1.0, len(t)) * sig
    det, nd = [], []
    for i in range(len(t)):
        if fobs[i] / sig[i] >= 5.0:
            af = abs(fobs[i])
            det.append({"candid": f"sim{seed}_{i}", "mjd": float(t[i]), "fid": int(fid[i]),
                        "magpsf": float(25.0 - 2.5 * np.log10(af)), "sigmapsf": float(sig[i] / (0.921034 * af)),
                        "isdiffpos": 1 if fobs[i] > 0 else -1})
        else:
            nd.append({"mjd": float(t[i]), "fid": int(fid[i]), "diffmaglim": LIM_MAG})
    truth = {"family": family, "parameters": params, "mwebv": mwebv, "seed": seed,
             "n_visits": int(len(t)), "n_detections": len(det)}
    return {"detections": det, "non_detections": nd}, truth
