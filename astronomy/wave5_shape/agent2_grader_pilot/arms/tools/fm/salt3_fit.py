#!/usr/bin/env python
"""Fit SALT3 (salt3-f22, sncosmo) to the pre-cut detections.

usage: salt3_fit.py --item-dir DIR [--z-min 0.005 --z-max 0.3 | --fix-z Z] [--t0-min T --t0-max T]
                    [--x1-min --x1-max] [--c-min --c-max] [--modelcov] [--out FILE]
Milky Way dust is fixed at item_meta mwebv (F99, r_v=3.1), exactly as the grader applies it.
Prints parameters in submission form, the sncosmo fit summary, and the pre-cut chi2 per point
under the scoring formula (sigma_eff = max(fluxerr, 0.05|flux|))."""
import argparse

import numpy as np

import _toolkit as tk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item-dir", required=True)
    ap.add_argument("--z-min", type=float, default=0.005)
    ap.add_argument("--z-max", type=float, default=0.3)
    ap.add_argument("--fix-z", type=float)
    for p in ("t0", "x1", "c"):
        ap.add_argument(f"--{p}-min", type=float)
        ap.add_argument(f"--{p}-max", type=float)
    ap.add_argument("--modelcov", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    import sncosmo
    from astropy.table import Table
    meta, det, _ = tk.load_item(a.item_dir)
    m = tk.models()
    model = m.sn_model("SALT3", meta["mwebv"])
    data = Table({"time": det.mjd.values, "band": det.band.values, "flux": det.flux.values,
                  "fluxerr": det.fluxerr.values, "zp": np.full(len(det), 25.0), "zpsys": np.full(len(det), "ab")})
    vparams = ["t0", "x0", "x1", "c"]
    bounds = {}
    if a.fix_z is not None:
        model.set(z=a.fix_z)
    else:
        vparams = ["z"] + vparams
        bounds["z"] = (a.z_min, a.z_max)
    for p in ("t0", "x1", "c"):
        lo, hi = getattr(a, f"{p}_min"), getattr(a, f"{p}_max")
        if lo is not None or hi is not None:
            bounds[p] = (lo if lo is not None else -np.inf, hi if hi is not None else np.inf)
    res, fitted = sncosmo.fit_lc(data, model, vparams, bounds=bounds, modelcov=a.modelcov)
    params = {k: float(fitted[k]) for k in ("z", "t0", "x0", "x1", "c")}
    tk.emit({"family": "SALT3", "parameters": params,
             "fit": {"success": bool(res.success), "message": str(res.message), "chisq": float(res.chisq),
                     "ndof": int(res.ndof), "errors": {k: float(v) for k, v in res.errors.items()},
                     "bounds": {k: list(v) for k, v in bounds.items()}, "modelcov": a.modelcov},
             "pre_cut_chi2_per_point": tk.pre_cut_chi2(m, "SALT3", params, det, meta)}, a.out)


if __name__ == "__main__":
    main()
