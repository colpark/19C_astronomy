"""Shared helpers for the arm tools. The toolset (classical or fm) is the name of this directory;
model assets are read from data_cache/arm_assets_<toolset>/ only."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLSET = os.path.basename(HERE)
AGENT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ASSETS = os.path.join(AGENT, "data_cache", f"arm_assets_{TOOLSET}")
sys.path.insert(0, HERE)
import forward_models as fm  # noqa: E402


def models():
    salt3 = os.path.join(ASSETS, "salt3-f22")
    pcode = os.path.join(ASSETS, "parsnip_code")
    ppt = os.path.join(ASSETS, "parsnip_fold0.pt")
    return fm.ForwardModels(salt3_dir=salt3 if os.path.isdir(salt3) else None,
                            parsnip_code_dir=pcode if os.path.isdir(pcode) else None,
                            parsnip_pt=ppt if os.path.exists(ppt) else None)


def load_item(item_dir):
    meta = json.load(open(os.path.join(item_dir, "item_meta.json")))
    rows = pd.read_csv(os.path.join(item_dir, "pre_cut.csv"))
    det = rows[rows.kind == "detection"].reset_index(drop=True)
    nondet = rows[rows.kind == "nondetection"].reset_index(drop=True)
    return meta, det, nondet


def pre_cut_chi2(m, family, params, det, meta):
    pred = m.predict(family, params, det.mjd.values, det.band.values, meta["mwebv"])
    per_band = {}
    for b in fm.BANDS:
        s = (det.band == b).values
        if s.any():
            per_band[b] = {"N": int(s.sum()), "chi2_per_point": fm.chi2_per_point_all(
                det.flux.values[s], det.fluxerr.values[s], pred[s])}
    return {"all": fm.chi2_per_point_all(det.flux.values, det.fluxerr.values, pred), "per_band": per_band}


def emit(obj, out):
    s = json.dumps(obj, indent=1, default=lambda x: float(x) if isinstance(x, np.floating) else str(x))
    if out:
        open(out, "w").write(s + "\n")
    print(s)
