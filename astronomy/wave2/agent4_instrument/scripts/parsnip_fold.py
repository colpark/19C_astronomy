"""Deep channel C5: ParSNIP trained from scratch per fold, no redshift anywhere (compositions_FROZEN.md section 7).
calibration only, contamination FAIL on this cohort. PRE-I1: graph edge R1->I1 unmet, escalated.
Uses no label. Usage: parsnip_fold.py FOLD [MAX_EPOCHS]"""
import hashlib, json, os, pickle, sys, time
import numpy as np, pandas as pd, torch
from common import W, check_frozen, BANNER

check_frozen()
sys.path.insert(0, os.path.join(W, "code", "kboone_parsnip_dcea62f"))
import astropy.table, lcdata, parsnip  # noqa

FEAT = os.path.join(W, "data_cache", "features")
COMP = os.path.join(W, "compositions")
os.makedirs(COMP, exist_ok=True)


def fold_of(cid):
    return int(hashlib.sha256(("w2a4-fold|" + str(cid)).encode()).hexdigest()[:8], 16) % 5


def to_tables(lcs, keep, tag):
    out = []
    for cid in keep:
        df, meta = lcs[cid]
        if len(df) == 0:
            continue
        t = astropy.table.Table.from_pandas(df)
        t.meta.update({"object_id": f"{cid}_{tag}", "ra": meta["ra"], "dec": meta["dec"], "mwebv": meta["mwebv"],
                       "redshift": np.nan, "hostgal_specz": np.nan, "hostgal_photoz": 0.0,
                       "hostgal_photoz_err": 1e3, "type": "unknown"})
        out.append(t)
    return out


def main():
    fold = int(sys.argv[1])
    max_epochs = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    torch.manual_seed(fold)
    np.random.seed(fold)
    lcs = {e: pickle.load(open(os.path.join(FEAT, f"parsnip_lcs_{e}.pkl"), "rb")) for e in ("E1", "E3")}
    cids = sorted(lcs["E1"].keys(), key=int)
    train = [c for c in cids if fold_of(c) != fold]
    test = [c for c in cids if fold_of(c) == fold]
    tr_tables = to_tables(lcs["E1"], train, "E1") + to_tables(lcs["E3"], train, "E3")
    ds = lcdata.from_light_curves(tr_tables)
    path = os.path.join(COMP, f"parsnip_fold{fold}.pt")
    if os.path.exists(path):
        os.remove(path)
    settings = {"predict_redshift": True, "input_redshift": True, "learning_rate": 1e-4}  # AMENDMENTS.md A-1, A-2
    model = parsnip.ParsnipModel(path, ["ztfg", "ztfr"], device="cuda", threads=8, settings=settings)
    ds = model.preprocess(ds)
    t0 = time.time()
    model.fit(ds, max_epochs=max_epochs)
    train_s = time.time() - t0
    rec = {"banner": BANNER, "fold": fold, "n_train_units": len(train), "n_train_lcs": len(ds),
           "epochs_run": int(model.epoch), "train_seconds": train_s, "settings_overridden": settings,
           "max_epochs": max_epochs, "torch": torch.__version__}
    for e in ("E1", "E3"):
        tabs = to_tables(lcs[e], test, e)
        tds = lcdata.from_light_curves(tabs)
        pred = model.predict_dataset(tds)
        keys = ["object_id", "color", "color_error", "s1", "s1_error", "s2", "s2_error", "s3", "s3_error",
                "luminosity", "luminosity_error", "reference_time_error", "predicted_redshift",
                "predicted_redshift_error", "amplitude"]
        df = pred[[k for k in keys if k in pred.colnames]].to_pandas()
        df["unit"] = df.object_id.str.split("_").str[0]
        df = df.drop(columns=["object_id"]).rename(columns={k: "c5_" + k for k in keys if k != "object_id"})
        df["epoch"] = e
        df.to_csv(os.path.join(COMP, f"c5_fold{fold}_{e}.csv"), index=False)
        rec[f"n_test_units_{e}"] = len(test)
        rec[f"n_test_predicted_{e}"] = int(len(df))
        rec[f"finite_fraction_{e}"] = float(np.isfinite(df[["c5_s1", "c5_s2", "c5_s3", "c5_color"]].values).all(axis=1).mean())
        rec[f"weights_finite"] = bool(all(torch.isfinite(p).all() for p in model.parameters()))
    json.dump(rec, open(os.path.join(COMP, f"parsnip_fold{fold}_log.json"), "w"), indent=1)
    print(json.dumps(rec))


if __name__ == "__main__":
    main()
