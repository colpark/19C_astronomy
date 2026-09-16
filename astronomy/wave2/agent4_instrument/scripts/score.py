"""Score once, after the compositions are hashed (FROZEN sections 4, 6, 8).
Refuses to run unless compositions/MANIFEST.sha256 verifies.
calibration only, contamination FAIL on this cohort. PRE-I1: graph edge R1->I1 unmet, escalated."""
import json, os, subprocess
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
from common import W, check_frozen, sha256, BANNER
from compose import unit_labels, CONFIGS, PERMUTED

check_frozen()
COMP = os.path.join(W, "compositions")
VENV_PY = "/tmp/claude-1000/-home-aid1-Documents-4-19C-astronomy/addb1fc3-63d3-4989-8753-aa4c400b100e/scratchpad/venv/bin/python"
POWER = "/home/aid1/Documents/4_19C_astronomy/repo/fm-advantage-benchmark/scripts/power.py"
K = 8


def verify_manifest():
    lines = [l for l in open(os.path.join(COMP, "MANIFEST.sha256")) if l.strip() and not l.startswith("#")]
    for l in lines:
        h, p = l.strip().split("  ", 1)
        if sha256(os.path.join(W, p)) != h:
            raise SystemExit(f"manifest mismatch on {p}. Refusing to score.")
    return len(lines)


def prec_at_k(sub, col):
    s = sub.sort_values([col, "ZTFkey"], ascending=[False, True])
    k = min(K, len(s))
    return s.y.iloc[:k].mean(), k


def auc_ci(y, s, B=1000, seed=0):
    rng = np.random.default_rng(seed)
    n = len(y)
    vals = []
    for _ in range(B):
        ix = rng.integers(0, n, n)
        if y[ix].min() == y[ix].max():
            continue
        vals.append(roc_auc_score(y[ix], s[ix]))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def main():
    nman = verify_manifest()
    labs = unit_labels()
    coh = pd.read_csv(os.path.join(W, "data_cache", "cohort_rows.csv"), dtype=str)
    peak_mjd = coh.groupby("object_cluster_1arcsec").peakt.apply(lambda s: s.astype(float).mean() + 2458000 - 2400000.5)
    ztfkey = coh.groupby("object_cluster_1arcsec").ZTFID.min()
    snia = coh.groupby("object_cluster_1arcsec").type.apply(lambda s: float(any(str(t).startswith("SN Ia") for t in s)))
    flog = json.load(open(os.path.join(W, "data_cache", "features", "features_log.json")))
    out = {"banner": BANNER, "manifest_files_verified": nman, "k": K, "chance_stated": 0.172, "epochs": {}}
    paired = []
    for e in ("E1", "E3"):
        preds = {c: pd.read_csv(os.path.join(COMP, "predictions", f"pred_{e}_{c}.csv"), dtype={"unit": str})
                 for c in list(CONFIGS) + [p + "__perm" for p in PERMUTED]}
        base = preds["C"][["unit", "decision_night", "t0_mjd"]].copy()
        for c, p in preds.items():
            base[c] = p.score.values
        base["label_class"] = base.unit.map(lambda u: labs[u][0])
        base["y"] = base.unit.map(lambda u: labs[u][1])
        base["ZTFkey"] = base.unit.map(ztfkey)
        base["far_from_peak"] = (base.unit.map(peak_mjd) - base.t0_mjd).abs() > 100
        pool = base[np.isfinite(base.y)].copy()
        ep = {"n_units": int(len(base)), "n_scored_pool": int(len(pool)),
              "coverage": base.label_class.value_counts().to_dict(),
              "n_posB": int(pool.y.sum()), "prevalence_posB": float(pool.y.mean()),
              "n_far_from_peak_in_pool": int(pool.far_from_peak.sum())}
        # per-object AUC
        aucs = {}
        for c in preds:
            ok = np.isfinite(pool[c].values)
            yy, ss = pool.y.values[ok].astype(int), pool[c].values[ok]
            aucs[c] = {"auc_posB": float(roc_auc_score(yy, ss)), "n": int(ok.sum()),
                       "coverage_fraction": float(ok.mean())}
            if not c.endswith("__perm"):
                aucs[c]["auc_posB_ci95"] = auc_ci(yy, ss)
                aucs[c]["auc_SNIa_descriptive"] = float(roc_auc_score(pool.unit.map(snia).values[ok].astype(int), ss))
        ep["auc"] = aucs
        perm_ok = {p: 0.45 <= aucs[p + "__perm"]["auc_posB"] <= 0.55 for p in PERMUTED}
        ep["permutation_control"] = {"band": [0.45, 0.55], "within_band": perm_ok,
                                     "disposition": "PASS" if all(perm_ok.values()) else "FAIL (numbers void)"}
        # items
        pool = pool.sort_values(["t0_mjd", "unit"])
        items = []
        for nid, sub in pool.groupby("decision_night"):
            items.append(("N", f"{e}-N{nid}", sub))
        chunks = [pool.iloc[i:i + 46] for i in range(0, len(pool), 46)]
        dropped = 0
        for j, sub in enumerate(chunks):
            if len(sub) < 46:
                dropped = len(sub)
                continue
            items.append(("R", f"{e}-R{j:03d}", sub))
        ep["round_items_dropped_partial_units"] = dropped
        prec_summary = {}
        for it, iid, sub in items:
            row = {"item_id": iid, "item_type": it, "epoch": e, "n": len(sub), "n_pos": int(sub.y.sum()),
                   "chance_measured": float(sub.y.mean()), "k_binding": bool(len(sub) > K)}
            for c in CONFIGS:
                pr, k = prec_at_k(sub, c)
                row["k_eff"] = k
                row["prec_" + c] = float(pr)
            row["prec_classical"] = row["prec_C-1"]
            row["prec_instrument"] = row["prec_C"]
            paired.append(row)
        pdf = pd.DataFrame([r for r in paired if r["epoch"] == e])
        for it in ("N", "R"):
            s = pdf[pdf.item_type == it]
            prec_summary[it] = {"n_items": int(len(s)), "n_items_k_binding": int(s.k_binding.sum()),
                                "mean_chance_measured": float(s.chance_measured.mean()),
                                **{f"mean_prec_{c}": float(s["prec_" + c].mean()) for c in CONFIGS},
                                "mean_paired_diff_classical_minus_instrument": float((s.prec_classical - s.prec_instrument).mean())}
        ep["precision_at_8"] = prec_summary
        out["epochs"][e] = ep
    pdf = pd.DataFrame(paired)
    cols = ["item_id", "item_type", "epoch", "n", "n_pos", "chance_measured", "k_eff", "k_binding",
            "prec_classical", "prec_instrument"] + ["prec_" + c for c in CONFIGS]
    pdf[cols].to_csv(os.path.join(W, "paired_scores.csv"), index=False)
    # power.py, unchanged, per (epoch, item type)
    power = {"label": "PRE-I1 CALIBRATION, not a P7 record",
             "banner": BANNER, "claim": "none: BTS cohort failed contamination (addition B)", "runs": {}}
    os.makedirs(os.path.join(W, "data_cache", "power"), exist_ok=True)
    for e in ("E1", "E3"):
        for it in ("N", "R"):
            sub = pdf[(pdf.epoch == e) & (pdf.item_type == it)]
            p = os.path.join(W, "data_cache", "power", f"paired_{e}_{it}.csv")
            sub[cols].to_csv(p, index=False)
            o = os.path.join(W, "data_cache", "power", f"power_{e}_{it}.json")
            args = [VENV_PY, POWER, "--scores", p, "--col-a", "prec_classical", "--col-b", "prec_instrument",
                    "--k", "8", "--candidates-per-item", "46.41", "--delta", "0.018", "--out", o]
            if it == "N":
                args += ["--stratum", "k_binding"]
            r = subprocess.run(args, capture_output=True, text=True)
            rec = json.load(open(o)) if os.path.exists(o) else {"error": r.stderr}
            rec["exit_code"] = r.returncode
            rec["stderr"] = r.stderr.strip()
            rec["scores_file_sha256"] = sha256(p)
            power["runs"][f"{e}_{it}"] = rec
    json.dump(power, open(os.path.join(W, "data_cache", "power", "power_runs_raw.json"), "w"), indent=1)
    json.dump(out, open(os.path.join(W, "data_cache", "score_results.json"), "w"), indent=1)
    print(json.dumps({e: {"auc": {c: round(v["auc_posB"], 3) for c, v in out["epochs"][e]["auc"].items()},
                          "prec": out["epochs"][e]["precision_at_8"], "perm": out["epochs"][e]["permutation_control"]}
                      for e in out["epochs"]}, indent=1))
    for k, v in power["runs"].items():
        print(k, {x: v.get(x) for x in ("n", "chance", "mean_paired_difference", "sigma_d", "mde", "n_min", "ruling")})


if __name__ == "__main__":
    main()
