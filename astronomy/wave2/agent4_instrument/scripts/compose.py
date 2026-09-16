"""Build the compositions blinded (FROZEN section 7). Labels are used ONLY inside GBDT.fit on training folds.
No metric is computed here. Ends by hashing every model and prediction file into compositions/MANIFEST.sha256.
calibration only, contamination FAIL on this cohort. PRE-I1: graph edge R1->I1 unmet, escalated."""
import glob, hashlib, json, os, pickle
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from common import W, check_frozen, label_class, sha256, BANNER

check_frozen()
FEAT = os.path.join(W, "data_cache", "features")
COMP = os.path.join(W, "compositions")
PRED = os.path.join(COMP, "predictions")
MOD = os.path.join(COMP, "models")
os.makedirs(PRED, exist_ok=True)
os.makedirs(MOD, exist_ok=True)


def fold_of(cid):
    return int(hashlib.sha256(("w2a4-fold|" + str(cid)).encode()).hexdigest()[:8], 16) % 5


def unit_labels():
    coh = pd.read_csv(os.path.join(W, "data_cache", "cohort_rows.csv"), dtype=str,
                      usecols=["object_cluster_1arcsec", "type"])
    g = coh.groupby("object_cluster_1arcsec").type.apply(list)
    out = {}
    for cid, types in g.items():
        cls = {label_class(t) for t in types if t != "-"}
        typed = [t for t in types if t != "-"]
        if not typed:
            out[cid] = ("unlabeled", np.nan)
        elif len(cls) != 1 or "unmapped" in cls:
            out[cid] = ("conflict_or_unmapped", np.nan)
        else:
            c = cls.pop()
            posb = float(c == "posA" and not any(t.startswith("SN Ia") for t in typed))
            out[cid] = (c, posb)
    return out


def channel_cols(df):
    ch = {f"C{i}": [c for c in df.columns if c.startswith(f"c{i}_")] for i in range(1, 6)}
    return ch


CONFIGS = {"C": ["C1", "C2", "C3", "C4", "C5"], "C-1": ["C1", "C2", "C3", "C4"],
           "C-minus-C1": ["C2", "C3", "C4", "C5"], "C-minus-C2": ["C1", "C3", "C4", "C5"],
           "C-minus-C3": ["C1", "C2", "C4", "C5"], "C-minus-C4": ["C1", "C2", "C3", "C5"], "C5-only": ["C5"]}
PERMUTED = ["C", "C-1"]


def main():
    labs = unit_labels()
    c5 = pd.concat([pd.read_csv(p, dtype={"unit": str}) for p in sorted(glob.glob(os.path.join(COMP, "c5_fold*_E*.csv")))])
    log = {"banner": BANNER, "configs": CONFIGS, "permutation_control_configs": PERMUTED}
    for e in ("E1", "E3"):
        f = pd.read_csv(os.path.join(FEAT, f"features_{e}.csv"), dtype={"unit": str})
        f = f.merge(c5[c5.epoch == e].drop(columns=["epoch"]), on="unit", how="left")
        f["fold"] = f.unit.map(fold_of)
        f["label_class"] = f.unit.map(lambda u: labs[u][0])
        y_all = f.unit.map(lambda u: labs[u][1]).values
        scored = np.isfinite(y_all)
        ch = channel_cols(f)
        rng = np.random.default_rng(1)
        y_perm = y_all.copy()
        y_perm[scored] = rng.permutation(y_all[scored])
        log[e] = {"n_units": int(len(f)), "n_scored_pool": int(scored.sum()),
                  "channel_columns": {k: len(v) for k, v in ch.items()},
                  "units_missing_c5": int(f["c5_s1"].isna().sum()) if "c5_s1" in f else int(len(f))}
        for name, chans in list(CONFIGS.items()) + [(p + "__perm", CONFIGS[p]) for p in PERMUTED]:
            y = y_perm if name.endswith("__perm") else y_all
            cols = sum((ch[c] for c in chans), [])
            X = f[cols].astype(float).values
            score = np.full(len(f), np.nan)
            for k in range(5):
                tr = (f.fold.values != k) & scored
                te = f.fold.values == k
                keep = np.isfinite(X[tr]).any(axis=0)  # AMENDMENTS.md A-3
                m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0)
                m.fit(X[tr][:, keep], y[tr].astype(int))
                score[te] = m.predict_proba(X[te][:, keep])[:, 1]
                pickle.dump({"model": m, "columns": [c for c, kk in zip(cols, keep) if kk],
                             "dropped_all_nan_in_train": [c for c, kk in zip(cols, keep) if not kk]},
                            open(os.path.join(MOD, f"gbdt_{e}_{name}_fold{k}.pkl"), "wb"))
            pd.DataFrame({"unit": f.unit, "fold": f.fold, "decision_night": f.decision_night, "t0_mjd": f.t0_mjd,
                          "score": score}).to_csv(os.path.join(PRED, f"pred_{e}_{name}.csv"), index=False)
        # item membership/labels are written to a separate file, read only by score.py
        f[["unit", "label_class"]].to_csv(os.path.join(W, "data_cache", f"unit_label_class_{e}.csv"), index=False)
    json.dump(log, open(os.path.join(COMP, "compose_log.json"), "w"), indent=1)
    files = sorted(glob.glob(os.path.join(COMP, "**", "*"), recursive=True))
    lines = [f"{sha256(p)}  {os.path.relpath(p, W)}" for p in files if os.path.isfile(p) and not p.endswith("MANIFEST.sha256")]
    open(os.path.join(COMP, "MANIFEST.sha256"), "w").write(f"# {BANNER}\n" + "\n".join(lines) + "\n")
    print("hashed", len(lines), "files; no metric computed")


if __name__ == "__main__":
    main()
