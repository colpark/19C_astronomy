"""Run the I4/I5 grader controls declared in tool_cards/controls_spec_PRE_RUN.md.
PRE-RATIFICATION PILOT (harness check only)."""
import copy
import json
import os
import sys

import numpy as np
import pandas as pd

AGENT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot"
sys.path.insert(0, os.path.join(AGENT, "scripts"))
sys.path.insert(0, AGENT)
from item_builder import check_protocol, sha256, split, write_item, counts, PROTOCOL_SHA  # noqa
import simulate  # noqa
import grade as G  # noqa

SPEC_SHA = open(os.path.join(AGENT, "tool_cards", "controls_spec_PRE_RUN.sha256")).read().split()[0]
SEED = int(PROTOCOL_SHA[:8], 16)
OUT = os.path.join(AGENT, "tool_cards", "controls")
REL = 1e-9


def mk_item(name, family, params, mwebv, seed, models):
    lc, truth = simulate.simulate(family, params, mwebv, seed, models)
    sp = split(lc)
    base = os.path.join(OUT, "items", name)
    hashes = write_item(sp, name, mwebv, os.path.join(base, "item"), os.path.join(base, "grader_private"))
    json.dump({"truth": truth, "counts": counts(sp), "hashes": hashes}, open(os.path.join(base, "truth.json"), "w"), indent=1)
    return base, sp


def sub(item, family, params):
    return {"item_id": item, "family": family, "parameters": params,
            "rejected_rivals": [{"family": "Bazin" if family != "Bazin" else "SALT3", "reason": "control submission"}]}


def run_grade(base, s, tag):
    d = os.path.join(base, "subs")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, tag + ".json")
    if isinstance(s, str):
        open(p, "w").write(s)
    elif s is not None:
        json.dump(s, open(p, "w"), indent=1, allow_nan=True)
    rec = G.grade(p, os.path.join(base, "item"), os.path.join(base, "grader_private"))
    json.dump(rec, open(os.path.join(d, tag + ".grade.json"), "w"), indent=1)
    return rec


def perturb(params):
    # AM-1 (amendments.md): t0 gets +1e-9 d absolute; all other parameters p*(1+1e-9), 0 -> 1e-12
    def f(k, v):
        if k == "t0":
            return v + 1e-9
        return v * (1 + REL) if v != 0 else 1e-12
    if all(isinstance(v, dict) for v in params.values()):
        return {b: {k: f(k, v) for k, v in blk.items()} for b, blk in params.items()}
    return {k: f(k, v) for k, v in params.items()}


def controls_for(name, base, family, ref_params, wrong_params):
    item = name
    res = {"grader_family": family}
    ref = run_grade(base, sub(item, family, ref_params), "ref")
    wrong = run_grade(base, sub(item, family, wrong_params), "wrong")
    pert = run_grade(base, sub(item, family, perturb(ref_params)), "perturbed")
    again = run_grade(base, sub(item, family, ref_params), "ref_repeat")
    rt = run_grade(base, json.loads(json.dumps(sub(item, family, ref_params))), "ref_roundtrip")
    recs = [ref, wrong, pert, again, rt]
    if any(r["status"] != "SCORED" for r in recs):
        res["disposition"] = "UNDEMONSTRATED"
        res["statuses"] = [r["status"] for r in recs]
        res["messages"] = [r.get("message") for r in recs]
        return res
    Sr, Sw = ref["S"], wrong["S"]
    fires = (Sw >= Sr + 5) and (Sw >= 3 * Sr)
    tol = 1e-6 * max(1.0, Sr)
    deltas = {"perturbed": abs(pert["S"] - Sr), "repeat": abs(again["S"] - Sr), "roundtrip": abs(rt["S"] - Sr)}
    nf_ok = all(v <= tol for v in deltas.values())
    res.update({"S_ref": Sr, "Q_ref": ref["Q"], "per_band_ref": ref["per_band"], "S_wrong": Sw, "Q_wrong": wrong["Q"],
                "must_fire": {"rule": "S_wrong >= S_ref + 5 and S_wrong >= 3 S_ref", "fired": bool(fires)},
                "must_not_fire": {"rule": f"|dS| <= {tol:.3g}", "deltas": deltas, "fired": not nf_ok},
                "disposition": "PASS" if (fires and nf_ok) else "FAIL"})
    return res


def bazin_full_fit(sp, fm):
    from scipy.optimize import least_squares
    d = sp["det"]
    d = d[(d.mjd >= sp["t_first"] - 30) & (d.mjd <= sp["horizon"])]
    out = {}
    for b in fm.BANDS:
        x = d[d.band == b]
        t, f, e = x.mjd.values, x.flux.values, x.fluxerr.values
        i = int(np.argmax(f))
        lo = [0.0, -np.inf, 1e-3, 1e-3, -np.inf]
        hi = [np.inf, np.inf, 500.0, 500.0, np.inf]
        r = least_squares(lambda p: (f - fm.bazin(t, *p)) / e, [1.5 * f[i], t[i] - 5, 3.0, 20.0, 0.0],
                          bounds=(lo, hi), method="trf")
        out[b] = dict(zip(fm.PARAM_KEYS["Bazin"], [float(v) for v in r.x]))
    return out


def main():
    check_protocol()
    got = sha256(os.path.join(AGENT, "tool_cards", "controls_spec_PRE_RUN.md"))
    assert got == SPEC_SHA, "controls spec hash mismatch"
    fm = simulate.load_fm()
    models = simulate.sim_models(fm)
    results = {"protocol_sha256": PROTOCOL_SHA, "controls_spec_sha256": SPEC_SHA, "amendment": "AM-1 (t0 perturbation +1e-9 d absolute)", "seed_base": SEED, "graders": {}}

    # G-SALT3
    s3 = {"z": 0.05, "t0": 59800.0, "x0": 1.2e-3, "x1": 0.5, "c": 0.05}
    base, sp = mk_item("CTRL-SALT3", "SALT3", s3, 0.03, SEED + 1, models)
    w = dict(s3, t0=59815.0, x1=-3.0)
    results["graders"]["G-SALT3"] = controls_for("CTRL-SALT3", base, "SALT3", s3, w)

    # G-PARAM (Villar truth, Bazin best-available)
    vg = {"A": 700.0, "beta": -2.0, "t0": 59785.0, "gamma": 8.0, "tau_rise": 3.0, "tau_fall": 25.0, "B": 0.0}
    vr = {"A": 650.0, "beta": -1.0, "t0": 59786.0, "gamma": 12.0, "tau_rise": 3.5, "tau_fall": 35.0, "B": 0.0}
    vil = {"ztfg": vg, "ztfr": vr}
    base, sp = mk_item("CTRL-VILLAR", "Villar", vil, 0.03, SEED + 2, models)
    wv = {b: dict(p, t0=p["t0"] + 15.0, tau_fall=p["tau_fall"] * 0.3) for b, p in vil.items()}
    results["graders"]["G-PARAM-Villar"] = controls_for("CTRL-VILLAR", base, "Villar", vil, wv)
    bz = bazin_full_fit(sp, fm)
    wb = {b: dict(p, t0=p["t0"] + 15.0, tau_fall=p["tau_fall"] * 0.3) for b, p in bz.items()}
    results["graders"]["G-PARAM-Bazin"] = controls_for("CTRL-VILLAR", base, "Bazin", bz, wb)

    # G-ParSNIP
    ps = {"z": 0.05, "t0": 59800.0, "amplitude": 1.0, "color": 0.0, "s1": 0.0, "s2": 0.0, "s3": 0.0}
    grid = np.arange(59770.0, 59850.0, 0.5)
    peak = float(np.max(models.predict("ParSNIP", ps, grid, np.full(len(grid), "ztfr"), 0.03)))
    ps["amplitude"] = 631.0 / peak
    base, sp = mk_item("CTRL-PARSNIP", "ParSNIP", ps, 0.03, SEED + 3, models)
    wp = dict(ps, t0=59815.0, color=0.5)
    results["graders"]["G-ParSNIP"] = controls_for("CTRL-PARSNIP", base, "ParSNIP", ps, wp)
    results["graders"]["G-ParSNIP"]["amplitude_scale_note"] = f"noiseless ztfr peak at amplitude 1 = {peak:.6g}"

    # coverage controls on CTRL-SALT3
    base = os.path.join(OUT, "items", "CTRL-SALT3")
    good = sub("CTRL-SALT3", "SALT3", s3)
    cov = {}
    cases = {
        "1_missing": (None, "COVERAGE_FAIL:MISSING"),
        "2_nonjson": ("this is not json {", "COVERAGE_FAIL:PARSE"),
        "3_flux_key": (dict(copy.deepcopy(good), predicted_flux=[1.0, 2.0]), "COVERAGE_FAIL:SCHEMA"),
        "4_nan_param": (dict(copy.deepcopy(good), parameters=dict(s3, x1=float("nan"))), "COVERAGE_FAIL:SCHEMA"),
        "5_no_rivals": (dict(copy.deepcopy(good), rejected_rivals=[]), "COVERAGE_FAIL:SCHEMA"),
        "6_neg_z": (dict(copy.deepcopy(good), parameters=dict(s3, z=-0.1)), "COVERAGE_FAIL:DOMAIN"),
        "7_bazin_tau0": (sub("CTRL-SALT3", "Bazin", {b: dict(p, tau_rise=0.0) for b, p in bz.items()}), "COVERAGE_FAIL:DOMAIN"),
        "8_wrong_item": (dict(copy.deepcopy(good), item_id="CTRL-VILLAR"), "COVERAGE_FAIL:SCHEMA"),
    }
    for tag, (s, want) in cases.items():
        if s is None:
            p = os.path.join(base, "subs", "cov_" + tag + ".json")
            if os.path.exists(p):
                os.remove(p)
            rec = G.grade(p, os.path.join(base, "item"), os.path.join(base, "grader_private"))
        else:
            rec = run_grade(base, s, "cov_" + tag)
        cov[tag] = {"expected": want, "got": rec["status"], "message": rec.get("message"),
                    "fired": rec["status"] == want}
    results["coverage_controls"] = {"cases": cov, "disposition": "PASS" if all(c["fired"] for c in cov.values()) else "FAIL"}
    json.dump(results, open(os.path.join(AGENT, "tool_cards", "control_results.json"), "w"), indent=1)
    print(json.dumps({k: (v.get("disposition"), v.get("S_ref"), v.get("S_wrong")) for k, v in results["graders"].items()}, indent=1))
    print("coverage", results["coverage_controls"]["disposition"])


if __name__ == "__main__":
    main()
