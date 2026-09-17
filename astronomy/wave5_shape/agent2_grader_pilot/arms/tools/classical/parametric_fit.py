#!/usr/bin/env python
"""Fit a Bazin or Villar parametric light curve per band to the pre-cut detections.

usage: parametric_fit.py --item-dir DIR --family Bazin|Villar [--p0 JSON] [--bounds JSON]
                         [--loss linear|soft_l1|huber] [--out FILE]
Models (flux at ZP 25 AB, t in MJD):
  Bazin:  F = A exp(-(t-t0)/tau_fall) / (1 + exp(-(t-t0)/tau_rise)) + B
  Villar: t1 = t0 + gamma, D = 1 + exp(-(t-t0)/tau_rise);
          F = (A + beta (t-t0)) / D for t < t1;  F = (A + beta gamma) exp(-(t-t1)/tau_fall) / D for t >= t1;  + B
--p0 and --bounds take JSON keyed by band then parameter, e.g.
  --p0 '{"ztfg": {"tau_fall": 30}}'  --bounds '{"ztfr": {"tau_rise": [0.5, 20]}}'
Unspecified entries use the defaults printed in the output."""
import argparse
import json

import numpy as np
from scipy.optimize import least_squares

import _toolkit as tk

fm = tk.fm


def defaults(family, t, f):
    i = int(np.argmax(f))
    fmax = float(max(f[i], 1e-3))
    if family == "Bazin":
        p0 = {"A": 1.5 * fmax, "t0": float(t[i]) - 5.0, "tau_rise": 3.0, "tau_fall": 20.0, "B": 0.0}
        bd = {"A": [0.0, np.inf], "t0": [-np.inf, np.inf], "tau_rise": [1e-3, 500.0], "tau_fall": [1e-3, 500.0],
              "B": [-np.inf, np.inf]}
    else:
        p0 = {"A": 1.5 * fmax, "beta": -fmax / 300.0, "t0": float(t[i]) - 5.0, "gamma": 5.0, "tau_rise": 3.0,
              "tau_fall": 20.0, "B": 0.0}
        bd = {"A": [0.0, np.inf], "beta": [-np.inf, 0.0], "t0": [-np.inf, np.inf], "gamma": [0.0, 300.0],
              "tau_rise": [0.01, 50.0], "tau_fall": [1.0, 300.0], "B": [-np.inf, np.inf]}
    return p0, bd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item-dir", required=True)
    ap.add_argument("--family", required=True, choices=["Bazin", "Villar"])
    ap.add_argument("--p0", default="{}")
    ap.add_argument("--bounds", default="{}")
    ap.add_argument("--loss", default="linear", choices=["linear", "soft_l1", "huber"])
    ap.add_argument("--out")
    a = ap.parse_args()
    meta, det, _ = tk.load_item(a.item_dir)
    user_p0, user_bd = json.loads(a.p0), json.loads(a.bounds)
    keys = fm.PARAM_KEYS[a.family]
    params, info = {}, {}
    fn = fm.bazin if a.family == "Bazin" else fm.villar
    for b in fm.BANDS:
        d = det[det.band == b]
        if len(d) == 0:
            raise SystemExit(f"no pre-cut detections in {b}")
        t, f, e = d.mjd.values, d.flux.values, d.fluxerr.values
        p0, bd = defaults(a.family, t, f)
        p0.update(user_p0.get(b, {}))
        bd.update({k: list(v) for k, v in user_bd.get(b, {}).items()})
        lo = np.array([bd[k][0] for k in keys], float)
        hi = np.array([bd[k][1] for k in keys], float)
        x0 = np.clip(np.array([p0[k] for k in keys], float), lo, hi)
        r = least_squares(lambda p: (f - fn(t, *p)) / e, x0, bounds=(lo, hi), method="trf", loss=a.loss)
        params[b] = dict(zip(keys, [float(x) for x in r.x]))
        info[b] = {"n_points": int(len(d)), "status": int(r.status), "message": str(r.message), "nfev": int(r.nfev),
                   "p0": {k: float(v) for k, v in zip(keys, x0)}, "bounds": {k: [float(v) for v in bd[k]] for k in keys},
                   "n_params_gt_n_points": len(keys) > len(d)}
    m = tk.models()
    tk.emit({"family": a.family, "parameters": params, "fit": info,
             "pre_cut_chi2_per_point": tk.pre_cut_chi2(m, a.family, params, det, meta)}, a.out)


if __name__ == "__main__":
    main()
