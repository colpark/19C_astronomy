"""Recount runs for Fink_EarlySNIa_RF, Fink_SLSN_RF, SuperNNova (Fink), CATS (Fink). Protocol sections 1, 4, 5.
Permitted adapter: reshape of served r: values into the per-object arrays the pandas_udf functions read (via .func).
Usage: run_fink_tools.py TOOL"""
import os, sys, types, pathlib
import numpy as np, pandas as pd

D = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D / "scripts"))
sys.path.insert(0, str(D / "code" / "fink-science_591e75ce"))
_pkg = types.ModuleType("actsnfink")  # actsnfink/__init__ imports actsnclass (unused by rainbow); load submodules directly
_pkg.__path__ = [str(D / "code" / "actsnfink_f424ab1f" / "actsnfink")]
sys.modules["actsnfink"] = _pkg
from runlog import run, load_alerts  # noqa

tool = sys.argv[1]
alerts = load_alerts()


def series(rows, key):
    return pd.Series([np.array([r[key] for r in rows])])


def load(fn_text, loader):
    """Import step; logged as a LOAD run. Returns the callable or None."""
    holder = {}

    def f():
        holder["fn"] = loader()
        return {"loaded": True}
    rec = run(tool, "LOAD", fn_text, f, lambda o: True, lambda e: "load")
    return holder.get("fn") if rec["status"] == "ok" else None


if tool == "Fink_EarlySNIa_RF":
    def L():
        from fink_science.rubin.random_forest_snia.processor import rfscore_rainbow_elasticc_nometa
        return rfscore_rainbow_elasticc_nometa.func
    fn = load("import fink_science.rubin.random_forest_snia.processor.rfscore_rainbow_elasticc_nometa", L)
    if fn:
        for oid, rows in alerts:
            run(tool, oid, "rfscore_rainbow_elasticc_nometa.func(midpointMjdTai, band, psfFlux, psfFluxErr)",
                lambda: fn(series(rows, "r:midpointMjdTai"), series(rows, "r:band"), series(rows, "r:psfFlux"), series(rows, "r:psfFluxErr")).tolist(),
                lambda o: any(np.isfinite(v) and v not in (-1.0, 0.0) for v in o), lambda e: "infer")

elif tool == "Fink_SLSN_RF":
    def L():
        from fink_science.rubin.slsn.processor import slsn_rubin
        return slsn_rubin.func
    fn = load("import fink_science.rubin.slsn.processor.slsn_rubin", L)
    if fn:
        for oid, rows in alerts:
            run(tool, oid, "slsn_rubin.func(diaObjectId, midpointMjdTai, psfFlux, psfFluxErr, band, ra, dec)",
                lambda: fn(pd.Series([int(oid)]), series(rows, "r:midpointMjdTai"), series(rows, "r:psfFlux"), series(rows, "r:psfFluxErr"),
                           series(rows, "r:band"), pd.Series([rows[-1]["r:ra"]]), pd.Series([rows[-1]["r:dec"]])).tolist(),
                lambda o: any(np.isfinite(v) and v != 0.0 for v in o), lambda e: "infer")

elif tool == "SuperNNova":
    def L():
        from fink_science.rubin.snn.processor import snn_ia_elasticc, snn_broad_elasticc
        return (snn_ia_elasticc.func, snn_broad_elasticc.func)
    fns = load("import fink_science.rubin.snn.processor.snn_ia_elasticc, snn_broad_elasticc", L)
    if fns:
        ia, broad = fns

        def both(rows):
            args = (pd.Series([rows[-1]["r:diaSourceId"]]), series(rows, "r:midpointMjdTai"), series(rows, "r:band"),
                    series(rows, "r:psfFlux"), series(rows, "r:psfFluxErr"))
            return {"ia": ia(*args, pd.Series(["elasticc_ia"])).tolist(),
                    "broad": [list(map(float, x)) for x in broad(*args, pd.Series(["elasticc_broad"])).tolist()]}

        def nd(o):
            ia_ok = any(np.isfinite(v) and v != 0.0 for v in o["ia"])
            br_ok = any(len(x) >= 2 and not (x[0] == -1 and x[1] == 0.0) and not all(v == 0.0 for v in x) for x in o["broad"])
            return ia_ok or br_ok
        for oid, rows in alerts:
            run(tool, oid, "snn_ia_elasticc.func(...,'elasticc_ia') and snn_broad_elasticc.func(...,'elasticc_broad')",
                lambda: both(rows), nd, lambda e: "infer")

elif tool == "CATS":
    def L():
        from fink_science.rubin.cats.processor import predict_nn
        return predict_nn.func
    fn = load("import fink_science.rubin.cats.processor.predict_nn (loads cats_small_nometa_serial_219_savedmodel)", L)
    if fn:
        for oid, rows in alerts:
            run(tool, oid, "predict_nn.func(midpointMjdTai, psfFlux, psfFluxErr, band)",
                lambda: [list(map(float, x)) for x in fn(series(rows, "r:midpointMjdTai"), series(rows, "r:psfFlux"),
                                                       series(rows, "r:psfFluxErr"), series(rows, "r:band")).tolist()],
                lambda o: any(any(v != 0.0 for v in x) for x in o), lambda e: "infer")
else:
    sys.exit("unknown tool")
