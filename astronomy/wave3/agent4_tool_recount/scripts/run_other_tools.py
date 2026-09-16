"""Recount runs for non-Fink tools. Protocol sections 1, 4, 5. Usage: run_other_tools.py TOOL
Input given to each tool's own entry point: the served r: fields under their lsst v11_1 names, values unchanged
(reshape only). No unit, band, zeropoint or field-name conversion is supplied."""
import hashlib, os, pathlib, sys
import numpy as np, pandas as pd

D = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D / "scripts"))
from runlog import run, load_alerts  # noqa

tool = sys.argv[1]
alerts = load_alerts()
CODE = D / "code"


def v11_df(rows):
    return pd.DataFrame([{k.split(":", 1)[1]: v for k, v in r.items()} for r in rows])


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load(text, loader):
    h = {}

    def f():
        h["obj"] = loader()
        return {"loaded": True, "detail": h.get("detail")}
    rec = run(tool, "LOAD", text, f, lambda o: True, lambda e: "load")
    return h.get("obj") if rec["status"] == "ok" else None


def stage_parse_else_infer(e):
    return "parse" if isinstance(e, (KeyError, ValueError, TypeError, AttributeError, IndexError)) else "infer"


if tool == "ORACLE":
    sys.path.insert(0, str(CODE / "uiucsn_Astro-ORACLE" / "src"))
    mp = CODE / "uiucsn_Astro-ORACLE" / "models" / "lsst_alpha_0.5_no_md" / "best_model.h5"

    def L():
        from astroOracle.pretrained_models import ORACLE_lite
        return ORACLE_lite(model_path=mp)
    m = load(f"astroOracle.pretrained_models.ORACLE_lite(model_path={mp.name}, sha256 {sha(mp)})", L)
    if m:
        for oid, rows in alerts:
            run(tool, oid, "ORACLE_lite.predict([DataFrame(v11_1 fields)])",
                lambda: m.predict([v11_df(rows)]).to_dict(orient="list"),
                lambda o: any(np.isfinite(v) for col in o.values() for v in col), stage_parse_else_infer)

elif tool == "ParSNIP":
    sys.path.insert(0, str(CODE / "kboone_parsnip_dcea62f"))

    def L():
        import parsnip
        p1 = CODE / "kboone_parsnip_dcea62f/parsnip/models/plasticc.pt"
        p2 = CODE / "kboone_parsnip_dcea62f/parsnip/models/plasticc_photoz.pt"
        assert sha(p1).startswith("a164aefe") and sha(p2).startswith("f41d06ce"), "checkpoint hash differs from inventory pin"
        return (parsnip.load_model("plasticc", device="cpu"), parsnip.load_model("plasticc_photoz", device="cpu"))
    ms = load("parsnip.load_model('plasticc') and ('plasticc_photoz'), hashes a164aefe…/f41d06ce…", L)
    if ms:
        import astropy.table
        for oid, rows in alerts:
            def f(rows=rows, oid=oid):
                t = astropy.table.Table.from_pandas(v11_df(rows))
                t.meta["object_id"] = oid
                return {"plasticc": dict(ms[0].predict(t)), "photoz": dict(ms[1].predict(t))}
            run(tool, oid, "ParsnipModel.predict(Table(v11_1 fields)) for plasticc and plasticc_photoz", f,
                lambda o: True, stage_parse_else_infer)

elif tool == "SALT3_sncosmo":
    def L():
        import sncosmo
        mdl = sncosmo.Model(source="salt3")
        return (sncosmo, mdl)
    ob = load("sncosmo.Model(source='salt3') (sncosmo 2.13.1 registry download)", L)
    if ob:
        sncosmo, mdl = ob
        import astropy.table
        for oid, rows in alerts:
            run(tool, oid, "sncosmo.fit_lc(Table(v11_1 fields), Model('salt3'), ['z','t0','x0','x1','c'], bounds z (0,0.5))",
                lambda rows=rows: {"params": list(sncosmo.fit_lc(astropy.table.Table.from_pandas(v11_df(rows)), mdl,
                                                                ["z", "t0", "x0", "x1", "c"], bounds={"z": (0, 0.5)})[0].parameters)},
                lambda o: any(np.isfinite(v) for v in o["params"]), stage_parse_else_infer)

elif tool == "GHOST":
    sys.path.insert(0, str(CODE / "uiucsn_astro_ghost"))
    gdir = D / "data_cache" / "ghost"
    gdir.mkdir(parents=True, exist_ok=True)
    os.environ["GHOST_PATH"] = str(gdir)

    def L():
        import astro_ghost
        from astro_ghost.ghostHelperFunctions import getGHOST, getTransientHosts
        mlp = CODE / "uiucsn_astro_ghost/astro_ghost/MLP_lupton.hdf5"
        assert mlp.exists() and sha(mlp).startswith("13ac27c2"), "MLP_lupton.hdf5 absent or hash differs from inventory pin"
        getGHOST(real=False, verbose=False, installpath=str(gdir), clobber=True)
        return getTransientHosts
    gth = load("astro_ghost getGHOST(real=False) + getTransientHosts; MLP_lupton.hdf5 hash 13ac27c2…", L)
    if gth:
        from astropy.coordinates import SkyCoord
        import astropy.units as u
        skip = int(os.environ.get('GHOST_SKIP', '0'))  # amendments.md AM2
        for i, (oid, rows) in enumerate(alerts):
            if i < skip:
                continue

            def f(rows=rows, i=i):
                c = SkyCoord(rows[-1]["r:ra"] * u.deg, rows[-1]["r:dec"] * u.deg)
                wd = gdir / f"run_{i}"
                wd.mkdir(exist_ok=True)
                cwd = os.getcwd()
                os.chdir(wd)
                try:
                    df = gth(transientName=[f"anon_{i}"], transientCoord=[c], snClass=[""], verbose=False,
                             GLADE=False, savepath=str(wd) + "/", GHOSTpath=str(gdir), redo_search=False)
                finally:
                    os.chdir(cwd)
                return df.to_dict(orient="list") if df is not None else None
            run(tool, oid, "getTransientHosts(transientCoord=[SkyCoord(ra,dec deg)], GLADE=False, redo_search=False)", f,
                lambda o: bool(o) and any(len(v) > 0 for v in o.values()), stage_parse_else_infer)
elif tool == "RAPID":
    sys.path.insert(0, str(CODE / "daniel-muthukrishna_astrorapid"))

    def L():
        mp = CODE / "daniel-muthukrishna_astrorapid/astrorapid/ZTF_unknown_redshift.hdf5"
        assert sha(mp).startswith("d68ed438"), "ZTF_unknown_redshift.hdf5 hash differs from inventory pin"
        from astrorapid.classify import Classify
        return Classify(model_name="ZTF_unknown_redshift", known_redshift=False)
    clf = load("astrorapid.classify.Classify(model_name='ZTF_unknown_redshift') hash d68ed438…", L)
    if clf:
        for oid, rows in alerts:
            def f(rows=rows, oid=oid):
                d = v11_df(rows)
                # the served v11_1 fields, in their own order; the tool's tuple needs photflag and mwebv, which v11_1 lacks
                lc = (d["midpointMjdTai"].values, d["psfFlux"].values, d["psfFluxErr"].values, d["band"].values,
                      d["ra"].values[-1], d["dec"].values[-1], oid)
                return clf.get_predictions([lc], return_predictions_at_obstime=True)[0].tolist()
            run(tool, oid, "Classify.get_predictions([(midpointMjdTai, psfFlux, psfFluxErr, band, ra, dec, diaObjectId)])", f,
                lambda o: True, stage_parse_else_infer)

elif tool == "Astromer1":
    sys.path.insert(0, str(CODE / "astromer-science_python-library"))
    wdir = D / "data_cache" / "astromer1"
    wdir.mkdir(parents=True, exist_ok=True)
    os.chdir(wdir)
    mode = os.environ.get("ASTROMER_LOAD", "readme")

    def L_readme():
        from ASTROMER.models import SingleBandEncoder
        m = SingleBandEncoder()
        return m.from_pretraining("macho_a0")  # README usage: model.from_pretraining(name)

    def L_api():
        import json as _j, urllib.request, zipfile
        from ASTROMER.models import SingleBandEncoder
        zp = wdir / "macho_a0_pin.zip"
        urllib.request.urlretrieve("https://github.com/astromer-science/weights/raw/649eda472b94aa69b1d9b2ea771a5da71bcd335c/macho_a0.zip", zp)
        h = sha(zp)
        assert h.startswith("76a204a3"), f"macho_a0.zip sha256 {h} differs from inventory pin"
        with zipfile.ZipFile(zp) as z:
            z.extractall(wdir / "pin")
        conf = _j.load(open(wdir / "pin" / "macho" / "conf.json"))
        m = SingleBandEncoder(num_layers=conf["layers"], d_model=conf["head_dim"], num_heads=conf["heads"], dff=conf["dff"],
                              base=conf["base"], dropout=conf["dropout"], maxlen=conf["max_obs"])
        m.load_weights(str(wdir / "pin" / "macho"))
        return m
    if mode == "readme":
        enc = load("SingleBandEncoder().from_pretraining('macho_a0') (README instance-call path; code fetches weights/raw/main)", L_readme)
    else:
        enc = load("public API: SingleBandEncoder(**conf.json) + load_weights(pin/macho) with macho_a0.zip@649eda47 hash 76a204a3…", L_api)
    if enc:
        for oid, rows in alerts:
            run(tool, oid, "SingleBandEncoder.encode([v11_df(rows).to_numpy()])",
                lambda rows=rows: enc.encode([v11_df(rows).to_numpy()], oids_list=["x"]),
                lambda o: True, stage_parse_else_infer)

elif tool == "Astromer2":
    sys.path.insert(0, str(CODE / "astromer-science_main-code"))
    sys.path.insert(0, str(CODE / "astromer-science_main-code" / "presentation" / "pipelines"))
    pt = D / "data_cache" / "astromer2" / "pt"

    def L():
        zp = D / "data_cache" / "astromer2" / "pt_macho_v2_2025.zip"
        assert hashlib.md5(open(zp, "rb").read()).hexdigest() == "42dfac36992119f5c4364c83729f3111", "zip md5 differs from Zenodo record"
        from steps.model_design import load_pt_model
        m, cfg = load_pt_model(str(pt))
        return m
    m = load("presentation/pipelines/steps/model_design.load_pt_model(pt_macho_v2_2025) Zenodo 10.5281/zenodo.18207945 md5 42dfac36…", L)
    if m:
        from src.data.loaders import load_numpy
        for oid, rows in alerts:
            run(tool, oid, "src.data.loaders.load_numpy([v11_df(rows).to_numpy()]) -> first element",
                lambda rows=rows: {k: v.numpy().tolist() for k, v in next(iter(load_numpy([v11_df(rows).to_numpy()]))).items() if k == "input"},
                lambda o: True, stage_parse_else_infer)

elif tool == "AstroM3":
    sys.path.insert(0, str(CODE / "MeriDK_AstroM3" / "src"))
    sys.path.insert(0, str(CODE / "MeriDK_AstroM3"))
    REV = "8904ed332cb9437691932a6d44e9a25a123cf76f"

    def L():
        from src.model import Informer
        from huggingface_hub import hf_hub_download
        st = hf_hub_download("AstroMLCore/AstroM3-CLIP-photo", "model.safetensors", revision=REV)
        h = sha(st)
        assert h.startswith("05d5f0b8"), f"model.safetensors sha256 {h} differs from HF LFS oid 05d5f0b8…"
        return Informer.from_pretrained("AstroMLCore/AstroM3-CLIP-photo", revision=REV).eval()
    m = load(f"src.model.Informer.from_pretrained('AstroMLCore/AstroM3-CLIP-photo', revision={REV}); safetensors oid 05d5f0b8…", L)
    if m:
        import torch
        from src.data import process_photometry
        for oid, rows in alerts:
            def f(rows=rows):
                ex = process_photometry({"photometry": [v11_df(rows).values.tolist()]}, seq_len=200, how="center")
                with torch.no_grad():
                    out = m(ex["photometry"][0][None], ex["photometry_mask"][0][None])
                return out.tolist() if hasattr(out, "tolist") else repr(out)
            run(tool, oid, "src.data.process_photometry({'photometry':[v11 rows]}) -> Informer(photometry, mask)", f,
                lambda o: True, stage_parse_else_infer)

elif tool == "BTSbot":
    sys.path.insert(0, str(CODE / "nabeelre_BTSbot"))
    bdir = D / "data_cache" / "btsbot"
    bdir.mkdir(parents=True, exist_ok=True)
    os.chdir(bdir)

    def L():
        from btsbot.from_HF import load_HF_model, get_local_model_dir
        m = load_HF_model("convnext", True, "galaxyzoo")
        h = sha(os.path.join(get_local_model_dir("convnext", True, "galaxyzoo"), "pytorch_model.bin"))
        assert h.startswith("c30f3202"), f"pytorch_model.bin sha256 {h} differs from inventory pin c30f3202…"
        return m.eval()
    m = load("btsbot.from_HF.load_HF_model('convnext', multi_modal=True, 'galaxyzoo') (HF nabeelr/BTSbot-convnext-pico-galaxyzoo-metadata; bin hash vs pin c30f3202…)", L)
    if m:
        import json as _j, torch
        from btsbot.from_HF import get_local_model_dir
        cfg = _j.load(open(os.path.join(get_local_model_dir("convnext", True, "galaxyzoo"), "train_config.json")))
        meta_cols = cfg.get("metadata_cols") or cfg.get("meta_cols")
        for oid, rows in alerts:
            def f(rows=rows):
                d = v11_df(rows)
                meta = torch.tensor(d[meta_cols].values.astype("float32"))  # tool's own metadata column list
                return m(images=None, metadata=meta).tolist()
            run(tool, oid, "model(images=<none in v11_1 rows fetched>, metadata=v11_df[train_config metadata cols])", f,
                lambda o: True, stage_parse_else_infer)

elif tool == "Maven":
    MROOT = CODE / "ThomasHelfer_multimodal-supernovae"
    sys.path.insert(0, str(MROOT))
    ck = MROOT / "models/clip_noiselesssimpretrain_clipreal/gallant-sweep-1/epoch=30-step=3627.ckpt"

    def L():
        assert sha(ck).startswith("0fc75ccc"), "checkpoint hash differs from inventory pin"
        cwd = os.getcwd(); os.chdir(MROOT)
        try:
            from src.models_multimodal import load_model
            out = load_model(str(ck))
        finally:
            os.chdir(cwd)
        return out[0] if isinstance(out, tuple) else out
    m = load("src.models_multimodal.load_model(clip_noiselesssimpretrain_clipreal/gallant-sweep-1/epoch=30-step=3627.ckpt) hash 0fc75ccc…", L)
    if m:
        import shutil, tempfile
        from src.dataloader import load_lightcurves
        for oid, rows in alerts:
            def f(rows=rows, oid=oid):
                td = tempfile.mkdtemp(dir=str(D / "data_cache"))
                try:
                    os.makedirs(os.path.join(td, "light-curves"))
                    v11_df(rows).to_csv(os.path.join(td, "light-curves", f"{oid}.csv"), index=False)  # served fields, v11_1 names
                    return [x.tolist() if hasattr(x, "tolist") else x for x in load_lightcurves(td)]
                finally:
                    shutil.rmtree(td)
            run(tool, oid, "src.dataloader.load_lightcurves(dir with light-curves/<oid>.csv of v11_1 fields)", f,
                lambda o: True, lambda e: "parse" if isinstance(e, (KeyError, ValueError, FileNotFoundError, TypeError)) else "infer")

elif tool == "ALeRCE_BHRF":
    sys.path.insert(0, str(CODE / "alercebroker_lc_classifier"))
    pk = D / "data_cache" / "alerce_hrf_1.1.1"

    def L():
        from lc_classifier.classifier.models import HierarchicalRandomForest
        m = HierarchicalRandomForest()  # default taxonomy; first LOAD passed {} by agent error (logged)
        m.load_model(str(pk))
        return m
    m = load("lc_classifier.classifier.models.HierarchicalRandomForest.load_model(hierarchical_rf_1.1.1; 5 pickles sha256 match wave-1)", L)
    if m:
        for oid, rows in alerts:
            run(tool, oid, "HierarchicalRandomForest.predict_proba(DataFrame(v11_1 fields, index=diaObjectId))",
                lambda rows=rows, oid=oid: m.predict_proba(v11_df(rows).set_index(pd.Index([oid] * len(rows)))).to_dict(orient="list"),
                lambda o: True, lambda e: "parse" if "Missing features" in str(e) or isinstance(e, (KeyError, ValueError)) else "infer")

elif tool == "Superphot_plus":
    mp = CODE / "VTDA-Group_superphot-plus/data/tutorial/model_superphot_full.pt"

    def L():
        assert sha(mp).startswith("a9536ff1"), "tutorial model hash differs from inventory pin"
        from superphot_plus.model.lightgbm import SuperphotLightGBM  # file is a pickle naming this class (first MLP.load attempt logged)
        return SuperphotLightGBM.load(str(mp))
    m = load("superphot_plus.model.lightgbm.SuperphotLightGBM.load(data/tutorial/model_superphot_full.pt) hash a9536ff1…; photometry via snapi (git 4a419fe0)", L)
    if m:
        from snapi import Photometry
        for oid, rows in alerts:
            run(tool, oid, "snapi.Photometry(time_series=DataFrame(v11_1 fields)) (Superphot+ photometry container)",
                lambda rows=rows: repr(Photometry(time_series=v11_df(rows)).detections),
                lambda o: True, stage_parse_else_infer)

else:
    sys.exit("unknown tool")
