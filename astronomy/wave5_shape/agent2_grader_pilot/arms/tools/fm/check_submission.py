#!/usr/bin/env python
"""Check a submission file against the schema and domain rules the grader applies, and check that the
forward model returns finite fluxes from t_cut to the horizon. No held-out data is read.

usage: check_submission.py --item-dir DIR --submission FILE.json"""
import argparse
import json

import numpy as np

import _toolkit as tk


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--item-dir", required=True)
    ap.add_argument("--submission", required=True)
    a = ap.parse_args()
    meta, det, _ = tk.load_item(a.item_dir)
    try:
        sub = json.load(open(a.submission))
    except Exception as e:  # noqa
        print(json.dumps({"status": "COVERAGE_FAIL:PARSE", "message": repr(e)}))
        return
    import os
    scope_p = os.path.join(a.item_dir, "scope.json")
    scope = json.load(open(scope_p)) if os.path.exists(scope_p) else None
    if scope is not None and isinstance(sub, dict):
        fam = sub.get("family")
        if fam == "DECLINE":
            rr = sub.get("rejected_rivals")
            ok = (sub.get("item_id") == meta["item_id"] and sub.get("parameters") == {} and isinstance(rr, list)
                  and len(rr) >= 1 and all(isinstance(r, dict) and set(r) == {"family", "reason"}
                                           and r["family"] in tk.fm.FAMILIES and str(r["reason"]).strip() for r in rr)
                  and "SALT3" in [r.get("family") for r in rr]
                  and set(sub) <= {"item_id", "family", "parameters", "rejected_rivals", "notes"})
            print(json.dumps({"status": "OK (DECLINE)" if ok else "COVERAGE_FAIL:SCHEMA",
                              "message": "" if ok else "DECLINE needs parameters {} and a rejected SALT3 rival with a reason"}, indent=1))
            return
        if fam not in scope["submittable_families"]:
            print(json.dumps({"status": "COVERAGE_FAIL:SCOPE", "message": f"family {fam!r} not in {scope['submittable_families']}"}, indent=1))
            return
    code, msg = tk.fm.validate_submission(sub, meta["item_id"])
    res = {"status": code, "message": msg}
    if code == "OK":
        ts = np.arange(meta["t_cut_mjd"], meta["horizon_mjd"] + 1e-9, 0.5)
        m = tk.models()
        try:
            finite = all(np.all(np.isfinite(m.predict(sub["family"], sub["parameters"], ts, np.full(len(ts), b),
                                                      meta["mwebv"]))) for b in tk.fm.BANDS)
            res["finite_on_scoring_window_grid"] = bool(finite)
        except tk.fm.AssetError as e:
            res["finite_on_scoring_window_grid"] = f"not checkable with this toolset: {e}"
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
