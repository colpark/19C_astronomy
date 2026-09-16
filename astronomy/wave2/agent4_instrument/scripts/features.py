"""Decision-time truncation and classical channels C1-C4 (compositions_FROZEN.md sections 1, 5, 6).
calibration only, contamination FAIL on this cohort. PRE-I1: graph edge R1->I1 unmet, escalated.
Labels are NOT read here. `type` is never loaded by this script."""
import json, os, sys, pickle
import numpy as np, pandas as pd
from common import W, check_frozen, night, BANNER

check_frozen()
import types
_pkg = types.ModuleType("actsnfink")  # bypass package __init__ (it imports actsnclass, unused by the sigmoid features)
_pkg.__path__ = [os.path.join(W, "code", "actsnfink", "actsnfink")]
sys.modules["actsnfink"] = _pkg
from actsnfink.classifier_sigmoid import get_sigmoid_features_dev_fast, RF_FEATURE_NAMES  # noqa
from astropy.coordinates import SkyCoord
import astropy.units as u
from dustmaps.config import config
config["data_dir"] = os.path.join(W, "data_cache", "dustmaps")
from dustmaps.sfd import SFDQuery

RAW = os.path.join(W, "data_cache", "alerce_raw")
OUT = os.path.join(W, "data_cache", "features")
os.makedirs(OUT, exist_ok=True)
FORBIDDEN = {"peakabs", "redshift", "type", "IAUID", "peakt", "peakmag", "peakfilt", "duration_bts",
             "rise", "fade", "A_V", "rb", "drb"}

# --- units: agent1 1arcsec clusters; drop BTS columns we must not touch
coh = pd.read_csv(os.path.join(W, "data_cache", "cohort_rows.csv"), dtype=str,
                  usecols=["ZTFID", "object_cluster_1arcsec"])
units = coh.groupby("object_cluster_1arcsec").ZTFID.apply(list).to_dict()


def mag2fluxcal_snana(m, s):  # fink_utils 0.77.0 photometry/conversion.py (verbatim formula)
    return 10 ** (-0.4 * m) * 10 ** 11, 9.21034 * 10 ** 10 * np.exp(-0.921034 * m) * s


def to_flux(mag):  # fink fast_transient_rate/utils.py
    return 10 ** (0.4 * (27.5 - mag))


def to_fluxerr(magerr, flux):
    return magerr * flux * np.log(10) / 2.5


def load_unit(ids):
    det, nd, unproc = [], [], []
    for oid in ids:
        p = os.path.join(RAW, oid + ".json")
        if not os.path.exists(p):
            unproc.append((oid, "no ALeRCE file (fetch failed)"))
            continue
        try:
            j = json.load(open(p))
        except Exception as e:
            unproc.append((oid, f"unparseable json {e!r}"))
            continue
        for r in j.get("detections") or []:
            det.append({"candid": str(r.get("candid")), "mjd": r["mjd"], "fid": r["fid"], "magpsf": r["magpsf"],
                        "sigmapsf": r["sigmapsf"], "isdiffpos": r.get("isdiffpos"), "ra": r.get("ra"),
                        "dec": r.get("dec"), "distnr": r.get("distnr")})
        for r in j.get("non_detections") or []:
            nd.append({"mjd": r["mjd"], "fid": r["fid"], "diffmaglim": r.get("diffmaglim")})
    det = pd.DataFrame(det, columns=["candid", "mjd", "fid", "magpsf", "sigmapsf", "isdiffpos", "ra", "dec", "distnr"])
    det = det.drop_duplicates("candid")
    nd = pd.DataFrame(nd, columns=["mjd", "fid", "diffmaglim"]).drop_duplicates()
    det = det[det.fid.isin([1, 2])].sort_values("mjd")
    nd = nd[nd.fid.isin([1, 2])].sort_values("mjd")
    return det, nd, unproc


def ispos(x):
    return str(x) in ("1", "t", "True", "1.0")


def truncate(det, nd, t0, epoch):
    if epoch == "E1":
        dm = (det.mjd >= t0 - 30) & (det.mjd <= t0 + 1e-5)
        nm = (nd.mjd >= t0 - 30) & (nd.mjd < t0)
    else:
        n0 = int(night(t0))
        dm = (det.mjd >= t0 - 30) & (night(det.mjd) <= n0 + 3)
        nm = (nd.mjd >= t0 - 30) & (night(nd.mjd) <= n0 + 3)
    return det[dm], nd[nm]


def c1(d):
    """Fink EarlySNIa sigmoid features. Fink passes JD as MJD and ignores isdiffpos."""
    f, fe = mag2fluxcal_snana(d.magpsf.values.astype(float), d.sigmapsf.values.astype(float))
    pdf = pd.DataFrame({"MJD": d.mjd.values + 2400000.5, "FLT": d.fid.map({1: "g", 2: "r"}).values,
                        "FLUXCAL": f, "FLUXCALERR": fe})
    feats = get_sigmoid_features_dev_fast(pdf, min_rising_points=2, min_data_points=4, rising_criteria="ewma")
    fake = [0, 0, 0, 0.1, 1e8, 0]
    alive = not (list(feats[:6]) == fake and list(feats[6:]) == fake)
    return dict(zip(["c1_" + n for n in RF_FEATURE_NAMES], feats)), alive


def c2(d, n, seed=0, N=100):
    """Fink fast_transient_rate, one unit per batch. Logic from processor.py get_last_alert/fast_transient_rate."""
    names = ["c2_mag_rate", "c2_sigma_rate", "c2_lower_rate", "c2_upper_rate", "c2_delta_time", "c2_from_upper"]
    if len(d) == 0:
        return dict.fromkeys(names, np.nan), False
    cur = d.iloc[-1]
    hist = pd.concat([
        pd.DataFrame({"jd": d.mjd.values[:-1] + 2400000.5, "fid": d.fid.values[:-1], "mag": d.magpsf.values[:-1].astype(float),
                      "sig": d.sigmapsf.values[:-1].astype(float), "lim": np.nan}),
        pd.DataFrame({"jd": n.mjd.values + 2400000.5, "fid": n.fid.values, "mag": np.nan, "sig": np.nan,
                      "lim": n.diffmaglim.values.astype(float)})]).sort_values("jd")
    cjd = list(hist.jd) + [cur.mjd + 2400000.5]
    cfid = list(hist.fid) + [cur.fid]
    cmag = list(hist.mag) + [float(cur.magpsf)]
    csig = list(hist.sig) + [float(cur.sigmapsf)]
    clim = list(hist.lim) + [np.nan]
    last = [np.nan] * 4
    for idx in range(len(cfid) - 2, -1, -1):
        if cfid[idx] > 2:
            break
        elif cfid[idx] == cur.fid:
            if np.isnan(cmag[idx]):
                last = [np.nan, np.nan, clim[idx], cjd[idx]]
            else:
                last = [cmag[idx], csig[idx], clim[idx], cjd[idx]]
            break
    rng = np.random.default_rng(seed)
    dt = cjd[-1] - last[3]
    fin_mag, fin_up = np.isfinite(last[0]), np.isfinite(last[2])
    if not (fin_mag or fin_up):
        return dict(zip(names, [np.nan] * 4 + [dt, np.nan])), False
    cf = to_flux(float(cur.magpsf))
    cs = rng.normal(cf, to_fluxerr(float(cur.sigmapsf), cf), N)
    eps = np.finfo(float).eps
    cs = cs + np.abs(np.min(cs))
    cs = np.where(cs == 0, eps, cs)
    if fin_mag:
        lf = to_flux(last[0])
        ls = rng.normal(lf, to_fluxerr(last[1], lf), N)
        ls = ls + np.abs(np.min(ls))
        ls = np.where(ls == 0, eps, ls)
        s = -2.5 * np.log10(cs / ls) / dt
        up = 0.0
    else:
        uu = rng.uniform(0, to_flux(last[2]), N)
        s = -2.5 * np.log10(cs / uu) / dt
        up = 1.0
    vals = [np.mean(s), np.std(s), np.percentile(s, 5.0), np.percentile(s, 95.0), dt, up]
    return dict(zip(names, vals)), bool(np.isfinite(vals[0]))


SLSN_FIT_COLS = (["flux_amplitude", "kurtosis", "max_slope", "skew", "peak_mag_g", "peak_mag_r", "std_flux", "q15", "q85"]
                 + ["reference_time", "amplitude", "rise_time", "fall_time", "Tmin", "Tmax", "t_color"]
                 + ["snr_" + k for k in ["reference_time", "amplitude", "rise_time", "fall_time", "Tmin", "Tmax", "t_color"]]
                 + ["chi2_rainbow", "z", "t0", "x0", "x1", "c", "chi2_salt"])


def c3(d, ebv):
    """Fink SLSN feature vector with its own gate (kernel.py: min_points_perband 3, min_points_total 7, min_duration 30)."""
    out = {"c3_distnr": float(d.distnr.iloc[-1]) if len(d) and d.distnr.iloc[-1] is not None else np.nan,
           "c3_ra": d.ra.astype(float).mean() if len(d) else np.nan,
           "c3_dec": d.dec.astype(float).mean() if len(d) else np.nan, "c3_ebv": ebv}
    cjd = d.mjd.values + 2400000.5
    out["c3_duration"] = float(np.ptp(cjd)) if len(d) else np.nan
    per_band_ok = all(3 <= int((d.fid == b).sum()) for b in (1, 2))
    gate = per_band_ok and (len(cjd) > 7) and (out["c3_duration"] > 30)
    for k in SLSN_FIT_COLS:
        out["c3_" + k] = np.nan
    if gate:
        out.update(slsn_fits(d))
    return out, gate


def slsn_fits(d):
    """Order and logic of fink slsn_classifier.extract_features: rainbow (shifts/sorts lc in place), salt2, stats."""
    import sncosmo
    import light_curve as lcpckg
    from light_curve.light_curve_py import RainbowFit
    from astropy.table import Table
    m = d.magpsf.values.astype(float)
    f, fe = mag2fluxcal_snana(m, d.sigmapsf.values.astype(float))
    lc = {"cjd": d.mjd.values + 2400000.5, "cflux": f, "csigflux": fe, "cfid": d.fid.values.astype(int), "cmagpsf": m}
    rb = RainbowFit.from_angstrom({1: 4770.0, 2: 6231.0}, with_baseline=False, temperature="sigmoid", bolometric="bazin")
    # fit_rainbow
    lc["cjd"] = lc["cjd"] - lc["cjd"][np.argmax(lc["cflux"])]
    order = np.argsort(lc["cjd"], kind="stable")
    for k in ("cjd", "cflux", "csigflux", "cfid"):
        lc[k] = np.asarray(lc[k])[order]
    try:
        res, err = rb._eval_and_get_errors(t=lc["cjd"], m=lc["cflux"], sigma=lc["csigflux"], band=lc["cfid"], debug=True)
        rbf = list(res[:-1]) + list(res[:-1] / err) + [res[-1]]
    except (TypeError, RuntimeError):
        rbf = [np.nan] * (2 * len(rb.names) + 1)
    # fit_salt
    tab = Table(data={"time": lc["cjd"] - lc["cjd"][np.argmax(lc["cflux"])],
                      "band": [{1: "ztfg", 2: "ztfr", 3: "ztfi"}[k] for k in lc["cfid"]],
                      "flux": lc["cflux"], "fluxerr": lc["csigflux"], "zp": [25.0] * len(lc["cjd"]),
                      "zpsys": ["ab"] * len(lc["cjd"])})
    try:
        r, _ = sncosmo.fit_lc(tab, sncosmo.Model(source="salt2"), ["z", "t0", "x0", "x1", "c"], bounds={"z": (0, 0.5)})
        sf = list(r.parameters) + [r.chisq]
    except RuntimeError:
        sf = [np.nan] * 6
    # statistical_features (cmagpsf is NOT re-sorted by fink's fit_rainbow; replicated)
    ex = lcpckg.Extractor(lcpckg.Amplitude(), lcpckg.Kurtosis(), lcpckg.MaximumSlope(), lcpckg.Skew())
    st = list(ex(lc["cjd"], lc["cflux"], lc["csigflux"], sorted=True, check=True))
    cm = lc["cmagpsf"]
    st += [np.min(cm[lc["cfid"] == 1], initial=99), np.min(cm[lc["cfid"] == 2], initial=99),
           np.std(lc["cflux"] / np.max(lc["cflux"])), np.quantile(lc["cjd"] - np.min(lc["cjd"]), 0.15),
           np.quantile(lc["cjd"] - np.min(lc["cjd"]), 0.85)]
    vals = st + rbf + sf
    return {"c3_" + k: float(v) for k, v in zip(SLSN_FIT_COLS, vals)}


def c4(d, t0, bdeg):
    if len(d) == 0:
        return {"c4_magpsf": np.nan, "c4_sigmapsf": np.nan, "c4_fid": np.nan, "c4_ndet": 0, "c4_days_since_t0": np.nan, "c4_b": bdeg}, False
    last = d.iloc[-1]
    return {"c4_magpsf": float(last.magpsf), "c4_sigmapsf": float(last.sigmapsf), "c4_fid": float(last.fid),
            "c4_ndet": int(len(d)), "c4_days_since_t0": float(last.mjd - t0), "c4_b": bdeg}, True


def parsnip_lc(d):
    m = d.magpsf.values.astype(float)
    s = d.sigmapsf.values.astype(float)
    sign = np.array([1.0 if ispos(x) else -1.0 for x in d.isdiffpos])
    fa = 10 ** (-0.4 * (m - 25.0))
    return pd.DataFrame({"time": d.mjd.values, "flux": sign * fa, "fluxerr": 0.921034 * fa * s,
                         "band": d.fid.map({1: "ztfg", 2: "ztfr"}).values})


def main():
    print(BANNER)
    sfd = SFDQuery()
    rows = {"E1": [], "E3": []}
    lcs = {"E1": {}, "E3": {}}
    unproc, alive = [], {e: {"C1": 0, "C2": 0, "C3": 0, "C4": 0} for e in rows}
    meta = []
    for cid, ids in sorted(units.items(), key=lambda kv: int(kv[0])):
        det, nd, up = load_unit(ids)
        unproc += [{"unit": cid, "ZTFID": o, "reason": r} for o, r in up]
        posdet = det[[ispos(x) for x in det.isdiffpos]]
        if len(posdet) == 0:
            unproc.append({"unit": cid, "ZTFID": ";".join(ids), "reason": "no positive g/r detection in ALeRCE"})
            continue
        t0 = float(posdet.mjd.min())
        ra, dec = posdet.ra.astype(float).iloc[0], posdet.dec.astype(float).iloc[0]
        sc = SkyCoord(ra * u.deg, dec * u.deg)
        ebv = float(sfd(sc))
        bdeg = float(sc.galactic.b.deg)
        meta.append({"unit": cid, "ZTFIDs": ";".join(ids), "t0_mjd": t0, "n0": int(night(t0))})
        for e in ("E1", "E3"):
            d, n = truncate(det, nd, t0, e)
            r = {"unit": cid, "epoch": e, "decision_night": int(night(t0)) + (3 if e == "E3" else 0), "t0_mjd": t0}
            for name, fn in (("C1", lambda: c1(d)), ("C2", lambda: c2(d, n)), ("C3", lambda: c3(d, ebv)),
                             ("C4", lambda: c4(d, t0, bdeg))):
                try:
                    f, ok = fn()
                except Exception as ex:
                    unproc.append({"unit": cid, "ZTFID": ";".join(ids), "reason": f"{e} {name} raised {ex!r}"})
                    f, ok = {}, False
                r.update(f)
                alive[e][name] += int(ok)
            rows[e].append(r)
            lcs[e][cid] = (parsnip_lc(d), {"object_id": str(cid), "ra": ra, "dec": dec, "mwebv": ebv})
    for e in rows:
        df = pd.DataFrame(rows[e])
        assert not (set(df.columns) & FORBIDDEN), "forbidden column present"
        df.to_csv(os.path.join(OUT, f"features_{e}.csv"), index=False)
        pickle.dump(lcs[e], open(os.path.join(OUT, f"parsnip_lcs_{e}.pkl"), "wb"))
    pd.DataFrame(meta).to_csv(os.path.join(OUT, "unit_epochs.csv"), index=False)
    n_units = len(meta)
    json.dump({"banner": BANNER, "n_units_total": len(units), "n_units_featurised": n_units,
               "alive_counts": alive, "alive_fraction": {e: {k: v / n_units for k, v in a.items()} for e, a in alive.items()},
               "unprocessable": unproc}, open(os.path.join(OUT, "features_log.json"), "w"), indent=1)
    print("units", len(units), "featurised", n_units, "alive", alive, "unprocessable", len(unproc))


if __name__ == "__main__":
    main()
