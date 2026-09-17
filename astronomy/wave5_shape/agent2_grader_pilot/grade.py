#!/usr/bin/env python
"""Grade one submission JSON against a grader-private held-out set.
grader_protocol_FROZEN.md sections 3-6. PRE-RATIFICATION PILOT (harness check only): no score record.

usage: grade.py --submission SUB.json --item-dir ITEM_DIR --private-dir PRIVATE_DIR [--out GRADE.json]
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import sys
import traceback

AGENT = os.path.dirname(os.path.abspath(__file__))
PROTOCOL_SHA = "ef58005482a049e5d58131267b0758ab0bfae3bb1c674650d6302f545fa709bc"
PIN_DIR = os.path.join(AGENT, "data_cache", "grader_pinned")
BANNER = "PRE-RATIFICATION PILOT (harness check only); not a score record"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def load_fm(private_dir):
    path = os.path.join(AGENT, "grader_private", "forward_models.py")
    spec = importlib.util.spec_from_file_location("grader_forward_models", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, sha256(path)


def grade(submission, item_dir, private_dir):
    import pandas as pd
    got = sha256(os.path.join(AGENT, "grader_protocol_FROZEN.md"))
    if got != PROTOCOL_SHA:
        raise SystemExit(f"protocol hash {got} != frozen {PROTOCOL_SHA}; abort")
    fm, fm_sha = load_fm(private_dir)
    meta_p = os.path.join(item_dir, "item_meta.json")
    held_p = os.path.join(private_dir, "held_out.csv")
    meta = json.load(open(meta_p))
    rec = {"banner": BANNER, "graded_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "protocol_sha256": got, "forward_models_sha256": fm_sha, "grade_py_sha256": sha256(os.path.abspath(__file__)),
           "item_id": meta["item_id"], "item_meta_sha256": sha256(meta_p), "held_out_sha256": sha256(held_p),
           "submission_path": os.path.abspath(submission)}
    if not os.path.exists(submission):
        rec.update(status="COVERAGE_FAIL:MISSING", message="no file at submission path")
        return rec
    rec["submission_sha256"] = sha256(submission)
    try:
        sub = json.load(open(submission))
    except Exception as e:  # noqa
        rec.update(status="COVERAGE_FAIL:PARSE", message=repr(e))
        return rec
    scope_p = os.path.join(private_dir, "scope_AM2.json")
    scope = json.load(open(scope_p)) if os.path.exists(scope_p) else None
    if scope is not None:
        rec["scope"] = {"file_sha256": sha256(scope_p), **scope}
        if isinstance(sub, dict) and sub.get("family") == "DECLINE":
            rr = sub.get("rejected_rivals")
            ok = (set(sub) <= {"item_id", "family", "parameters", "rejected_rivals", "notes"}
                  and sub.get("item_id") == meta["item_id"] and sub.get("parameters") == {}
                  and isinstance(rr, list) and len(rr) >= 1
                  and all(isinstance(r, dict) and set(r) == {"family", "reason"} and r["family"] in fm.FAMILIES
                          and isinstance(r["reason"], str) and r["reason"].strip() and len(r["reason"]) <= 4000 for r in rr)
                  and "SALT3" in [r["family"] for r in rr])
            if ok:
                rec.update(status="DECLINED", message="AM-2 decline: recorded as coverage, never scored",
                           rejected_rivals_families=[r["family"] for r in rr])
            else:
                rec.update(status="COVERAGE_FAIL:SCHEMA", message="invalid DECLINE submission (AM-2)")
            return rec
        if isinstance(sub, dict) and sub.get("family") in fm.FAMILIES and sub["family"] not in scope["submittable_families"]:
            rec.update(status="COVERAGE_FAIL:SCOPE", message=f"family {sub['family']} not submittable under AM-2")
            return rec
    code, msg = fm.validate_submission(sub, meta["item_id"])
    if code != "OK":
        rec.update(status=code, message=msg)
        return rec
    rec["family"] = sub["family"]
    rec["parameters"] = sub["parameters"]
    rec["rejected_rivals_families"] = [r["family"] for r in sub["rejected_rivals"]]
    try:
        models = fm.ForwardModels(salt3_dir=os.path.join(PIN_DIR, "salt3-f22"),
                                  parsnip_code_dir=os.path.join(PIN_DIR, "parsnip_code"),
                                  parsnip_pt=os.path.join(PIN_DIR, "parsnip_fold0.pt"))
        held = pd.read_csv(held_p)
        pred = models.predict(sub["family"], sub["parameters"], held.mjd.values, held.band.values, meta["mwebv"])
        rec["asset_hashes"] = models.asset_hashes
    except Exception:  # noqa
        rec.update(status="GRADER_ERROR", message=traceback.format_exc())
        return rec
    import numpy as np
    if not np.all(np.isfinite(pred)):
        rec.update(status="COVERAGE_FAIL:EVAL", message=f"{int((~np.isfinite(pred)).sum())} non-finite predictions")
        return rec
    S, per_band, excluded = fm.score_points(held.flux.values, held.fluxerr.values, pred, held.band.values)
    rec["bands_excluded_lt5"] = excluded
    if S is None:
        rec.update(status="ITEM_UNSCOREABLE", message="no band with >= 5 held-out detections")
        return rec
    rec.update(status="SCORED", S=S, Q=fm.bounded(S), per_band=per_band)
    pre_p = os.path.join(item_dir, "pre_cut.csv")
    pre = pd.read_csv(pre_p)
    pre = pre[pre.kind == "detection"]
    try:
        pp = models.predict(sub["family"], sub["parameters"], pre.mjd.values, pre.band.values, meta["mwebv"])
        rec["diagnostic_pre_cut_chi2_per_point"] = fm.chi2_per_point_all(pre.flux.values, pre.fluxerr.values, pp)
    except Exception as e:  # noqa
        rec["diagnostic_pre_cut_chi2_per_point"] = f"error {e!r}"
    if scope is not None:
        famp = os.path.join(private_dir, scope["object_family_file"])
        of = json.load(open(famp))
        rec["object_family_file_sha256"] = sha256(famp)
        if not of["salt3_renderable_family"]:
            rec["harness_diagnostic_residual_NOT_A_SCORE"] = {k: rec.pop(k) for k in ("S", "Q", "per_band")}
            rec.update(status="OUT_OF_SCOPE:NON_IA_OBJECT",
                       message="AM-2: SALT3 renders the SN Ia family only; object family recorded after the seal is not SN Ia. Scope failure, not a score.")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--submission", required=True)
    ap.add_argument("--item-dir", required=True)
    ap.add_argument("--private-dir", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    rec = grade(a.submission, a.item_dir, a.private_dir)
    s = json.dumps(rec, indent=1)
    if a.out:
        open(a.out, "w").write(s + "\n")
    print(s)


if __name__ == "__main__":
    main()
