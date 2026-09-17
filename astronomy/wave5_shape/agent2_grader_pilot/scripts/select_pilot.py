"""Apply selection/selection_rule_SEALED.md. Reads only ZTFID and peakt from BTS. PRE-RATIFICATION PILOT (harness check only)."""
import datetime
import json
import os
import sys
import time

import pandas as pd
import requests

AGENT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave5_shape/agent2_grader_pilot"
sys.path.insert(0, os.path.join(AGENT, "scripts"))
from item_builder import check_protocol, sha256, split, counts, ispos, tables  # noqa

BTS = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/data/raw/ztf_bts_all_2026-09-16.csv"
BTS_SHA = "61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
COHORT = "/home/aid1/Documents/4_19C_astronomy/repo/astronomy/wave2/agent4_instrument/data_cache/cohort_rows.csv"
RULE = os.path.join(AGENT, "selection", "selection_rule_SEALED.md")
RULE_SHA = open(RULE.replace(".md", ".sha256")).read().split()[0]
RAW = os.path.join(AGENT, "data_cache", "alerce_raw")
CAP = 150


def fetch(oid):
    path = os.path.join(RAW, oid + ".json")
    if os.path.exists(path):
        return path, "cached", 0
    url = f"https://api.alerce.online/ztf/v1/objects/{oid}/lightcurve"
    err = None
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                open(path, "wb").write(r.content)
                return path, "ok", attempt + 1
            err = f"http {r.status_code}"
        except Exception as e:  # noqa
            err = repr(e)
        time.sleep(2 ** attempt)
    return None, f"fetch_fail {err}", 3


def main():
    check_protocol()
    assert sha256(RULE) == RULE_SHA, "rule hash mismatch"
    assert sha256(BTS) == BTS_SHA, "BTS hash mismatch"
    os.makedirs(RAW, exist_ok=True)
    bts = pd.read_csv(BTS, usecols=["ZTFID", "peakt"], dtype=str)
    cohort = set(pd.read_csv(COHORT, usecols=["ZTFID"], dtype=str).ZTFID)
    pk = pd.to_numeric(bts.peakt, errors="coerce")
    jd = pk + 2458000.0
    utc = pd.to_datetime(jd - 2440587.5, unit="D")
    m = (utc >= "2022-01-01") & (utc < "2023-01-01")
    c = bts[m].copy()
    c["peak_mjd"] = (pk[m] + 2458000.0 - 2400000.5).values
    n_2022 = int(len(c))
    c = c[~c.ZTFID.isin(cohort)]
    n_after_cohort = int(len(c))
    c = c.drop_duplicates("ZTFID").sort_values("ZTFID")
    examined, selected = [], None
    for _, row in c.iterrows():
        if len(examined) >= CAP:
            break
        oid = row.ZTFID
        path, st, nreq = fetch(oid)
        rec = {"ZTFID": oid, "fetch": st, "http_attempts": nreq}
        if path is None:
            rec["result"] = "fetch_fail"
            examined.append(rec)
            continue
        rec["raw_sha256"] = sha256(path)
        lc = json.load(open(path))
        det, _ = tables(lc)
        pos = det[[ispos(x) for x in det.isdiffpos]]
        rec["n_pos_g"] = int((pos.fid == 1).sum())
        rec["n_pos_r"] = int((pos.fid == 2).sum())
        sp = split(lc)
        reasons = []
        if rec["n_pos_g"] < 20 or rec["n_pos_r"] < 20:
            reasons.append("n_pos_g or n_pos_r < 20")
        if sp is None:
            reasons.append("no positive g/r detection")
        else:
            rec["t_first"] = sp["t_first"]
            rec["peak_minus_t_first_d"] = float(row.peak_mjd) - sp["t_first"]
            rec.update(counts(sp))
            if not (0 <= rec["peak_minus_t_first_d"] <= 100):
                reasons.append("peak - t_first outside [0, 100] d")
            if min(rec["pre_cut_detections"].values()) < 3:
                reasons.append("pre-cut detections < 3 in a band")
            if min(rec["held_out_detections"].values()) < 8:
                reasons.append("held-out detections < 8 in a band")
        rec["result"] = "PASS" if not reasons else "fail: " + "; ".join(reasons)
        examined.append(rec)
        if not reasons:
            selected = oid
            break
    seal = {"banner": "PRE-RATIFICATION PILOT (harness check only)",
            "sealed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "rule_sha256": RULE_SHA, "bts_sha256": BTS_SHA, "cohort_rows_sha256": sha256(COHORT),
            "bts_columns_read": ["ZTFID", "peakt"], "n_rows_peak_2022": n_2022, "n_after_cohort_exclusion": n_after_cohort,
            "n_examined": len(examined), "selected_ZTFID": selected, "examined": examined}
    json.dump(seal, open(os.path.join(AGENT, "selection", "selection_SEALED.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in seal.items() if k != "examined"}, indent=1))
    print("examined", [(e["ZTFID"], e["result"]) for e in examined][-5:])


if __name__ == "__main__":
    main()
