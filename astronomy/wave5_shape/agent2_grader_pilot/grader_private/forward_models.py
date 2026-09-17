"""Forward models, submission schema and score formula for generate / inverse problem.
Frozen under grader_protocol_FROZEN.md sections 3, 4 and 5. PRE-RATIFICATION PILOT (harness check only).

The grader's copy lives in grader_private/; arm tool copies must be byte-identical (hash recorded).
Model assets are passed in by the caller (paths), and every asset is hash-checked at load.
"""
import hashlib
import json
import math
import os
import sys

import numpy as np

FAMILIES = ("SALT3", "Bazin", "Villar", "ParSNIP")
BANDS = ("ztfg", "ztfr")
ZP, ZPSYS = 25.0, "ab"
ERR_FLOOR_FRAC = 0.05
MIN_POINTS_PER_BAND = 5

PARAM_KEYS = {
    "SALT3": ("z", "t0", "x0", "x1", "c"),
    "ParSNIP": ("z", "t0", "amplitude", "color", "s1", "s2", "s3"),
    "Bazin": ("A", "t0", "tau_rise", "tau_fall", "B"),
    "Villar": ("A", "beta", "t0", "gamma", "tau_rise", "tau_fall", "B"),
}

SALT3_PINS = {
    "salt3_color_correction.dat": "92caf54c0adedb6aa95add602022508cac4ee99324668686c94769103da9339b",
    "salt3_color_dispersion.dat": "537a2807a1d0ac923630a5461901596ab1fe61cfda3640e21eb8d92e0c99f2bc",
    "salt3_lc_covariance_01.dat": "58dade9a3480304567c1df10000d806d50e5ab863bbb6e5f4f1a432ebecf7f51",
    "salt3_lc_variance_0.dat": "3637f1093732a15ac1254ccefdd304e46740228407649bd36b6cb330d6fa8e8b",
    "salt3_lc_variance_1.dat": "b5267e57b7c8cc11b76b1ddfa4fb723a74183995f0f914331a188ff1e74ee75b",
    "salt3_template_0.dat": "f09df51e2567a9b4e00c4846723c7b640dcbda06a4bc2f0d4bc559915f334813",
    "salt3_template_1.dat": "46a11e7c9915159496741599b3f55c2eda98c2058aec32e8300281bc1eab3bf9",
}
PARSNIP_PT_PIN = "283381682be5d5212e5502256549cc153450168bc9f9c66d4e36aa03e2bdd705"
PARSNIP_CODE_PINS = {
    "parsnip/__init__.py": "03e0a28ec76f9b45ef588524f329fb647c98f16768d6d76711b5526220725d27",
    "parsnip/instruments.py": "554255596f858357179527bf1b71680c8ccda1325d9df71ad4420ce0da20a76f",
    "parsnip/light_curve.py": "4d31fec667adec92997da0b8bcdb076e5eb1b7cd400f3cda6d9a2361904f3d9f",
    "parsnip/parsnip.py": "391174659f097a1ae6db3980dc271e036446f3f096b8fdd6a41115a0791631ad",
    "parsnip/settings.py": "5ee455dc620bb1f43c104c940e30c48ba7ce5e26f2de4784d2b2d71789d0329a",
    "parsnip/sncosmo.py": "67c73b2d23d01a2eb78378327ba9f5f43f8242ba6dc81a249a3579f08ceaccad",
    "parsnip/utils.py": "085bc872b740b6dc2d19d184da81a05e58665089303e3ba9ee7a1f12bd2bdff1",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


class AssetError(RuntimeError):
    pass


# ---------------------------------------------------------------- parametric (G-PARAM)
def _clip(x):
    return np.clip(x, -700.0, 700.0)


def bazin(t, A, t0, tau_rise, tau_fall, B):
    t = np.asarray(t, dtype=float)
    dt = t - t0
    return A * np.exp(_clip(-dt / tau_fall)) / (1.0 + np.exp(_clip(-dt / tau_rise))) + B


def villar(t, A, beta, t0, gamma, tau_rise, tau_fall, B):
    t = np.asarray(t, dtype=float)
    dt = t - t0
    t1 = t0 + gamma
    den = 1.0 + np.exp(_clip(-dt / tau_rise))
    early = (A + beta * dt) / den
    late = (A + beta * gamma) * np.exp(_clip(-(t - t1) / tau_fall)) / den
    return np.where(t < t1, early, late) + B


# ---------------------------------------------------------------- SN models (G-SALT3, G-ParSNIP)
class ForwardModels:
    """Evaluates a submission's family and parameters. SALT3 / ParSNIP assets are optional;
    a family whose assets were not supplied raises AssetError when evaluated."""

    def __init__(self, salt3_dir=None, parsnip_code_dir=None, parsnip_pt=None):
        self.salt3_dir = salt3_dir
        self.parsnip_code_dir = parsnip_code_dir
        self.parsnip_pt = parsnip_pt
        self._salt3_source = None
        self._parsnip_source = None
        self.asset_hashes = {}

    def _salt3(self):
        if self._salt3_source is None:
            if not self.salt3_dir:
                raise AssetError("SALT3 assets not supplied to this toolset")
            for fn, pin in SALT3_PINS.items():
                got = sha256_file(os.path.join(self.salt3_dir, fn))
                if got != pin:
                    raise AssetError(f"SALT3 file {fn} hash {got} != pin {pin}")
                self.asset_hashes["salt3/" + fn] = got
            import sncosmo
            self._salt3_source = sncosmo.SALT3Source(modeldir=self.salt3_dir, name="salt3", version="2.0")
        return self._salt3_source

    def _parsnip(self):
        if self._parsnip_source is None:
            if not (self.parsnip_code_dir and self.parsnip_pt):
                raise AssetError("ParSNIP assets not supplied to this toolset")
            got = sha256_file(self.parsnip_pt)
            if got != PARSNIP_PT_PIN:
                raise AssetError(f"parsnip model hash {got} != pin {PARSNIP_PT_PIN}")
            self.asset_hashes["parsnip_fold0.pt"] = got
            for rel, pin in PARSNIP_CODE_PINS.items():
                g = sha256_file(os.path.join(self.parsnip_code_dir, rel))
                if g != pin:
                    raise AssetError(f"parsnip code {rel} hash {g} != pin {pin}")
                self.asset_hashes["parsnip_code/" + rel] = g
            if self.parsnip_code_dir not in sys.path:
                sys.path.insert(0, self.parsnip_code_dir)
            import warnings
            import torch
            torch.set_num_threads(1)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import parsnip
                model = parsnip.load_model(self.parsnip_pt, device="cpu", threads=1)
            self._parsnip_source = parsnip.ParsnipSncosmoSource(model)
            self.parsnip_model = model
        return self._parsnip_source

    def sn_model(self, family, mwebv):
        import sncosmo
        src = self._salt3() if family == "SALT3" else self._parsnip()
        m = sncosmo.Model(source=src, effects=[sncosmo.F99Dust(r_v=3.1)],
                          effect_names=["mw"], effect_frames=["obs"])
        m.set(mwebv=float(mwebv))
        return m

    def predict(self, family, params, mjd, band, mwebv):
        """Flux at ZP 25 AB for each (mjd, band). band is an array of 'ztfg'/'ztfr'."""
        mjd = np.asarray(mjd, dtype=float)
        band = np.asarray(band).astype(str)
        out = np.full(mjd.shape, np.nan)
        if family in ("Bazin", "Villar"):
            fn = bazin if family == "Bazin" else villar
            for b in BANDS:
                sel = band == b
                if sel.any():
                    p = params[b]
                    out[sel] = fn(mjd[sel], *[float(p[k]) for k in PARAM_KEYS[family]])
            return out
        if family in ("SALT3", "ParSNIP"):
            m = self.sn_model(family, mwebv)
            m.set(**{k: float(params[k]) for k in PARAM_KEYS[family]})
            for b in BANDS:
                sel = band == b
                if sel.any():
                    out[sel] = m.bandflux(b, mjd[sel], zp=ZP, zpsys=ZPSYS)
            return out
        raise ValueError(f"unknown family {family}")


# ---------------------------------------------------------------- schema (section 4)
def _finite_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v))


def validate_submission(sub, item_id=None):
    """Return (code, message). code in {'OK', 'COVERAGE_FAIL:PARSE', 'COVERAGE_FAIL:SCHEMA', 'COVERAGE_FAIL:DOMAIN'}."""
    if not isinstance(sub, dict):
        return "COVERAGE_FAIL:PARSE", "submission is not a JSON object"
    allowed_top = {"item_id", "family", "parameters", "rejected_rivals", "notes"}
    required_top = {"item_id", "family", "parameters", "rejected_rivals"}
    if set(sub) - allowed_top:
        return "COVERAGE_FAIL:SCHEMA", f"unknown top-level keys {sorted(set(sub) - allowed_top)}"
    if required_top - set(sub):
        return "COVERAGE_FAIL:SCHEMA", f"missing top-level keys {sorted(required_top - set(sub))}"
    if not isinstance(sub["item_id"], str) or (item_id is not None and sub["item_id"] != item_id):
        return "COVERAGE_FAIL:SCHEMA", f"item_id {sub.get('item_id')!r} does not match {item_id!r}"
    if "notes" in sub and not isinstance(sub["notes"], str):
        return "COVERAGE_FAIL:SCHEMA", "notes must be a string"
    fam = sub["family"]
    if fam not in FAMILIES:
        return "COVERAGE_FAIL:SCHEMA", f"family {fam!r} not in {FAMILIES}"
    p = sub["parameters"]
    if not isinstance(p, dict):
        return "COVERAGE_FAIL:SCHEMA", "parameters must be an object"
    keys = PARAM_KEYS[fam]
    if fam in ("Bazin", "Villar"):
        if set(p) != set(BANDS):
            return "COVERAGE_FAIL:SCHEMA", f"{fam} parameters must have exactly keys {BANDS}"
        blocks = [(b, p[b]) for b in BANDS]
    else:
        blocks = [(None, p)]
    for b, blk in blocks:
        if not isinstance(blk, dict) or set(blk) != set(keys):
            return "COVERAGE_FAIL:SCHEMA", f"{fam} {b or ''} parameters must have exactly keys {keys}"
        for k in keys:
            if not _finite_number(blk[k]):
                return "COVERAGE_FAIL:SCHEMA", f"{fam} {b or ''} {k} is not a finite number"
    rr = sub["rejected_rivals"]
    if not isinstance(rr, list) or len(rr) < 1:
        return "COVERAGE_FAIL:SCHEMA", "rejected_rivals must be a non-empty list"
    for r in rr:
        if not isinstance(r, dict) or set(r) != {"family", "reason"}:
            return "COVERAGE_FAIL:SCHEMA", "each rejected rival must have exactly keys family, reason"
        if r["family"] not in FAMILIES or r["family"] == fam:
            return "COVERAGE_FAIL:SCHEMA", f"rejected rival family {r['family']!r} invalid"
        if not isinstance(r["reason"], str) or not r["reason"].strip() or len(r["reason"]) > 4000:
            return "COVERAGE_FAIL:SCHEMA", "rejected rival reason must be a non-empty string of at most 4000 characters"
    # domain
    if fam == "SALT3" and not (0 < p["z"] <= 1.5):
        return "COVERAGE_FAIL:DOMAIN", "SALT3 z must satisfy 0 < z <= 1.5"
    if fam == "ParSNIP" and not (0 <= p["z"] <= 4):
        return "COVERAGE_FAIL:DOMAIN", "ParSNIP z must satisfy 0 <= z <= 4"
    if fam in ("Bazin", "Villar"):
        for b, blk in blocks:
            if not (blk["tau_rise"] > 0 and blk["tau_fall"] > 0):
                return "COVERAGE_FAIL:DOMAIN", f"{fam} {b} tau_rise and tau_fall must be > 0"
            if fam == "Villar" and not blk["gamma"] >= 0:
                return "COVERAGE_FAIL:DOMAIN", f"Villar {b} gamma must be >= 0"
    return "OK", ""


# ---------------------------------------------------------------- score (section 3)
def score_points(flux, fluxerr, pred, band):
    flux = np.asarray(flux, float)
    fluxerr = np.asarray(fluxerr, float)
    pred = np.asarray(pred, float)
    band = np.asarray(band).astype(str)
    sig = np.maximum(fluxerr, ERR_FLOOR_FRAC * np.abs(flux))
    r = (flux - pred) / sig
    per_band, excluded = {}, {}
    for b in BANDS:
        sel = band == b
        n = int(sel.sum())
        if n >= MIN_POINTS_PER_BAND:
            per_band[b] = {"N": n, "chi2_per_point": float(np.mean(r[sel] ** 2)),
                           "median_abs_resid": float(np.median(np.abs(r[sel])))}
        else:
            excluded[b] = n
    if not per_band:
        return None, per_band, excluded
    S = float(np.mean([v["chi2_per_point"] for v in per_band.values()]))
    return S, per_band, excluded


def chi2_per_point_all(flux, fluxerr, pred):
    """Pre-cut diagnostic and floor metric: same floor, all points pooled."""
    flux = np.asarray(flux, float)
    sig = np.maximum(np.asarray(fluxerr, float), ERR_FLOOR_FRAC * np.abs(flux))
    return float(np.mean(((flux - np.asarray(pred, float)) / sig) ** 2))


def bounded(S):
    return 1.0 / (1.0 + S)


def load_json(path):
    with open(path) as f:
        return json.load(f)
