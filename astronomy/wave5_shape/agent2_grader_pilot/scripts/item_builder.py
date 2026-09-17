"""Build an item (pre_cut.csv + item_meta.json) and its grader-private held_out.csv from ALeRCE-format rows.
grader_protocol_FROZEN.md sections 1, 2 and 6. PRE-RATIFICATION PILOT (harness check only)."""
import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

AGENT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot"
PROTOCOL_SHA = "ef58005482a049e5d58131267b0758ab0bfae3bb1c674650d6302f545fa709bc"
CUT_DAYS, HORIZON_DAYS, PRE_WINDOW = 10.0, 60.0, 30.0
BANDMAP = {1: "ztfg", 2: "ztfr"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def check_protocol():
    got = sha256(os.path.join(AGENT, "grader_protocol_FROZEN.md"))
    if got != PROTOCOL_SHA:
        sys.exit(f"grader_protocol_FROZEN.md hash {got} != {PROTOCOL_SHA}. Abort.")


def ispos(x):
    return str(x) in ("1", "t", "True", "1.0")


def tables(lc_json):
    det = pd.DataFrame([{"candid": str(r.get("candid")), "mjd": float(r["mjd"]), "fid": int(r["fid"]),
                         "magpsf": r["magpsf"], "sigmapsf": r["sigmapsf"], "isdiffpos": r.get("isdiffpos")}
                        for r in (lc_json.get("detections") or [])],
                       columns=["candid", "mjd", "fid", "magpsf", "sigmapsf", "isdiffpos"])
    det = det.drop_duplicates("candid")
    det = det[det.fid.isin([1, 2])].sort_values("mjd").reset_index(drop=True)
    nd = pd.DataFrame([{"mjd": float(r["mjd"]), "fid": int(r["fid"]), "diffmaglim": r.get("diffmaglim")}
                       for r in (lc_json.get("non_detections") or [])], columns=["mjd", "fid", "diffmaglim"])
    nd = nd.drop_duplicates(["mjd", "fid"])
    nd = nd[nd.fid.isin([1, 2])].sort_values("mjd").reset_index(drop=True)
    return det, nd


def to_flux(det):
    m = det.magpsf.astype(float).values
    s = det.sigmapsf.astype(float).values
    sign = np.array([1.0 if ispos(x) else -1.0 for x in det.isdiffpos])
    fa = 10 ** (-0.4 * (m - 25.0))
    out = det.copy()
    out["band"] = det.fid.map(BANDMAP)
    out["flux"] = sign * fa
    out["fluxerr"] = 0.921034 * fa * s
    return out


def split(lc_json):
    det, nd = tables(lc_json)
    pos = det[[ispos(x) for x in det.isdiffpos]]
    if len(pos) == 0:
        return None
    t_first = float(pos.mjd.min())
    t_cut = t_first + CUT_DAYS
    horizon = t_first + HORIZON_DAYS
    d = to_flux(det)
    pre_det = d[(d.mjd >= t_first - PRE_WINDOW) & (d.mjd <= t_cut)]
    held = d[(d.mjd > t_cut) & (d.mjd <= horizon)]
    pre_nd = nd[(nd.mjd >= t_first - PRE_WINDOW) & (nd.mjd <= t_cut)].copy()
    pre_nd["band"] = pre_nd.fid.map(BANDMAP)
    return dict(t_first=t_first, t_cut=t_cut, horizon=horizon, det=d, pre_det=pre_det, held=held, pre_nd=pre_nd)


def counts(sp):
    return {"pre_cut_detections": {b: int((sp["pre_det"].band == b).sum()) for b in ("ztfg", "ztfr")},
            "held_out_detections": {b: int((sp["held"].band == b).sum()) for b in ("ztfg", "ztfr")}}


def write_item(sp, item_id, mwebv, item_dir, private_dir, private_extra=None):
    os.makedirs(item_dir, exist_ok=True)
    os.makedirs(private_dir, exist_ok=True)
    pre = sp["pre_det"]
    rows = pd.concat([
        pd.DataFrame({"mjd": pre.mjd, "band": pre.band, "kind": "detection", "magpsf": pre.magpsf,
                      "sigmapsf": pre.sigmapsf, "isdiffpos": [1 if ispos(x) else -1 for x in pre.isdiffpos],
                      "flux": pre.flux, "fluxerr": pre.fluxerr, "diffmaglim": np.nan}),
        pd.DataFrame({"mjd": sp["pre_nd"].mjd, "band": sp["pre_nd"].band, "kind": "nondetection",
                      "magpsf": np.nan, "sigmapsf": np.nan, "isdiffpos": np.nan, "flux": np.nan,
                      "fluxerr": np.nan, "diffmaglim": sp["pre_nd"].diffmaglim}),
    ]).sort_values(["mjd", "band"]).reset_index(drop=True)
    rows.to_csv(os.path.join(item_dir, "pre_cut.csv"), index=False, float_format="%.6f")
    meta = {"item_id": item_id, "t_first_mjd": round(sp["t_first"], 6), "t_cut_mjd": round(sp["t_cut"], 6),
            "horizon_mjd": round(sp["horizon"], 6), "bands": ["ztfg", "ztfr"], "zp": 25.0, "zpsys": "ab",
            "flux_convention": "flux = s*10^(-0.4*(magpsf-25)), fluxerr = 0.921034*|flux|*sigmapsf, s=isdiffpos sign; nondetection rows carry diffmaglim (5-sigma limiting mag)",
            "mwebv": round(float(mwebv), 5),
            "mwebv_note": "SFD E(B-V) at the object position; the grader applies F99Dust(r_v=3.1) at this value to SALT3 and ParSNIP submissions",
            "scoring": "held-out detections in (t_cut, horizon]; per-band chi2 per point with sigma_eff = max(fluxerr, 0.05|flux|); S = mean over bands with >= 5 points; Q = 1/(1+S)"}
    json.dump(meta, open(os.path.join(item_dir, "item_meta.json"), "w"), indent=1)
    h = sp["held"]
    pd.DataFrame({"candid": h.candid, "mjd": h.mjd, "band": h.band, "flux": h.flux, "fluxerr": h.fluxerr,
                  "magpsf": h.magpsf, "sigmapsf": h.sigmapsf,
                  "isdiffpos": [1 if ispos(x) else -1 for x in h.isdiffpos]}).to_csv(
        os.path.join(private_dir, "held_out.csv"), index=False, float_format="%.6f")
    if private_extra is not None:
        json.dump(private_extra, open(os.path.join(private_dir, "identity.json"), "w"), indent=1)
    return {p: sha256(p) for p in [os.path.join(item_dir, "pre_cut.csv"), os.path.join(item_dir, "item_meta.json"),
                                   os.path.join(private_dir, "held_out.csv")]}
