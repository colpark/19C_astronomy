#!/usr/bin/env python
"""Run the ZTF-trained ParSNIP model (fold 0, ztfg/ztfr, trained without redshift) on the pre-cut detections.

usage: parsnip_run.py --item-dir DIR [--fit [--fix-z Z | --z-min 0 --z-max 0.5]] [--out FILE]
Default: encode the light curve (MAP latent) and return sncosmo parameters z, t0, amplitude, color, s1, s2, s3
in submission form. --fit then refines t0, amplitude, color, s1..s3 (and z unless fixed) with sncosmo.fit_lc,
starting from the encoding. Milky Way dust is fixed at item_meta mwebv (F99, r_v=3.1) for the returned
forward model, as the grader applies it; the encoder corrects the input for MW dust with the same E(B-V).
Model limits (disclosed): trained on ZTF BTS 2019-2021 light curves truncated to at most 3 nights after first
detection, with a neutralised photo-z prior; the decoder has little training support later than that."""
import argparse
import os
import warnings

import numpy as np

import _toolkit as tk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item-dir", required=True)
    ap.add_argument("--fit", action="store_true")
    ap.add_argument("--fix-z", type=float)
    ap.add_argument("--z-min", type=float, default=0.0)
    ap.add_argument("--z-max", type=float, default=0.5)
    ap.add_argument("--out")
    a = ap.parse_args()
    import sncosmo
    from astropy.table import Table
    meta, det, _ = tk.load_item(a.item_dir)
    m = tk.models()
    src = m._parsnip()
    pm = m.parsnip_model
    lc = Table({"time": det.mjd.values, "flux": det.flux.values, "fluxerr": det.fluxerr.values,
                "band": det.band.values})
    lc.meta.update({"object_id": meta["item_id"], "ra": 0.0, "dec": 0.0, "mwebv": float(meta["mwebv"]),
                    "redshift": np.nan, "hostgal_specz": np.nan, "hostgal_photoz": 0.0, "hostgal_photoz_err": 1e3,
                    "type": "unknown"})
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        enc = pm.predict_sncosmo(lc)
    keys = tk.fm.PARAM_KEYS["ParSNIP"]
    params = {k: float(enc[k]) for k in keys}
    out = {"family": "ParSNIP", "model": "parsnip_fold0.pt (ZTF g/r, wave-2 fold 0)",
           "encoded_parameters": dict(params),
           "encoded_pre_cut_chi2_per_point": tk.pre_cut_chi2(m, "ParSNIP", params, det, meta)}
    if params["z"] < 0:
        out["warning"] = "encoded z < 0 is outside the submission domain 0 <= z <= 4"
    if a.fit:
        model = m.sn_model("ParSNIP", meta["mwebv"])
        model.set(**params)
        data = Table({"time": det.mjd.values, "band": det.band.values, "flux": det.flux.values,
                      "fluxerr": det.fluxerr.values, "zp": np.full(len(det), 25.0), "zpsys": np.full(len(det), "ab")})
        vparams = ["t0", "amplitude", "color", "s1", "s2", "s3"]
        bounds = {}
        if a.fix_z is not None:
            model.set(z=a.fix_z)
        else:
            vparams = ["z"] + vparams
            model.set(z=float(np.clip(params["z"], a.z_min + 1e-4, a.z_max - 1e-4)))
            bounds["z"] = (a.z_min, a.z_max)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res, fitted = sncosmo.fit_lc(data, model, vparams, bounds=bounds, guess_amplitude=False,
                                         guess_t0=False, guess_z=False)
        fp = {k: float(fitted[k]) for k in keys}
        out["fitted_parameters"] = fp
        out["fit"] = {"success": bool(res.success), "message": str(res.message), "chisq": float(res.chisq),
                      "ndof": int(res.ndof), "bounds": {k: list(v) for k, v in bounds.items()}}
        out["fitted_pre_cut_chi2_per_point"] = tk.pre_cut_chi2(m, "ParSNIP", fp, det, meta)
    out["parameters"] = out.get("fitted_parameters", out["encoded_parameters"])
    tk.emit(out, a.out)


if __name__ == "__main__":
    main()
