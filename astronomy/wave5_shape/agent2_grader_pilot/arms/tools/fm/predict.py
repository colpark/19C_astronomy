#!/usr/bin/env python
"""Evaluate a family + parameters with the same forward-model code the grader uses.

usage: predict.py --item-dir DIR --params FILE.json [--step 2.0] [--mjd 59800.1,59805.3] [--out FILE]
FILE.json holds {"family": ..., "parameters": {...}} (a full submission file also works).
Prints the pre-cut chi2 per point under the scoring formula and model fluxes (ZP 25 AB) per band on a grid
from t_first - 30 d to the horizon (and at any --mjd values). No held-out data is read."""
import argparse
import json

import numpy as np

import _toolkit as tk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item-dir", required=True)
    ap.add_argument("--params", required=True)
    ap.add_argument("--step", type=float, default=2.0)
    ap.add_argument("--mjd", default="")
    ap.add_argument("--out")
    a = ap.parse_args()
    meta, det, _ = tk.load_item(a.item_dir)
    sub = json.load(open(a.params))
    fam, params = sub["family"], sub["parameters"]
    m = tk.models()
    grid = np.arange(meta["t_first_mjd"] - 30.0, meta["horizon_mjd"] + 1e-9, a.step)
    extra = np.array([float(x) for x in a.mjd.split(",") if x.strip()], float)
    out = {"family": fam, "parameters": params, "pre_cut_chi2_per_point": tk.pre_cut_chi2(m, fam, params, det, meta),
           "grid": {}}
    for b in tk.fm.BANDS:
        for name, ts in (("grid", grid), ("requested", extra)):
            if len(ts):
                fl = m.predict(fam, params, ts, np.full(len(ts), b), meta["mwebv"])
                out.setdefault(name, {})[b] = [[round(float(t), 4), float(v)] for t, v in zip(ts, fl)]
    tk.emit(out, a.out)


if __name__ == "__main__":
    main()
