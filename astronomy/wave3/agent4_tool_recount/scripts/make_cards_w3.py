"""Wave-3 tool card updates: new code-versus-documentation/inventory disagreements found while running tools on
Rubin alerts. Written from code (I3). Recount only; no arm result."""
import json, pathlib
D = pathlib.Path(__file__).resolve().parent.parent
OUT = D / "tool_cards"
OUT.mkdir(exist_ok=True)
BAN = "tool coverage recount (rule D): no output retained as an arm result"
ALERT_Q = "public Fink LSST API rows carrying lsst v11_1 field names (Avro not served: HTTP 400)"


def card(name, **k):
    c = {"name": name, "written_from": "code", "wave": 3, "banner": BAN}
    c.update(k)
    c.setdefault("completeness", "Covered: the loader, input parser and served checkpoint hash exercised in the wave-3 recount (run_log.jsonl), and each disagreement's code locator. Not covered: the defining paper (not re-read this wave), training code, I4 construct validity and I5 certification.")
    json.dump(c, open(OUT / f"tool_card_{name}.json", "w"), indent=1)


card("CATS_Fink",
     role="predictor",
     quantity_returned="5-way broad class probability vector ('SN-like','Fast','Long','Periodic','non-Periodic (AGN)') from cats_small_nometa_serial_219_savedmodel via tf.keras.layers.TFSMLayer; [0.0]*5 when fewer than 2 points",
     defining_paper="Fink CATS (cbpf) classifier; paper not read in this wave; card from code only",
     accuracy_against_scored_measurement="Recount: end-to-end non-default output on 5/10 sealed cohort alerts (exactly the 5 with >= 2 diaSources), on " + ALERT_Q + ". I4 not assessed.",
     what_it_is_not="Not a spectroscopic-class predictor for BTS classes; trained on ELAsTiCC simulations; not metadata-aware (nometa)",
     conventions=["psfFlux and psfFluxErr normalised per object by norm_column (utilities.py), so absolute flux units do not enter",
                  "band mapped u..y -> 1..6 inside predict_nn", "sequences padded to 395 with -999"],
     served_checkpoint={"identifier": "fink_science/data/models/cats_models/cats_small_nometa_serial_219_savedmodel",
                        "pin": "fink-science 591e75ce; saved_model.pb sha256 7bd7b163d4f5e50bbc0e0ebdc014dd8070a635344b4856faa53bd54a0bd8f1f1; variables.data sha256 df3f7d973f8a4dcb3273f9cb40895d3ef98f7acfe4ca5ba0e4924d3ae279e61b"},
     disagreements=[
         {"topic": "served checkpoint vs inventory", "inventory": "wave-1 inventory pins cats_small_nometa_serial.keras (e51239df…)", "code": "processor.py loads cats_small_nometa_serial_219_savedmodel at import; the .keras file is not what is served"},
         {"topic": "dependency pin", "requirements": "fink_science/rubin/cats/requirements.txt pins tensorflow==2.8.0 and tensorflow-addons", "run": "loaded and ran under tensorflow 2.21.0 / keras 3.15.1 via TFSMLayer"}])

card("Fink_EarlySNIa_RF_Rubin",
     role="predictor",
     quantity_returned="P(Ia) from sklearn RF over [n_points] + 7 Rainbow features; -1.0 when rainbow features are zero (fewer than min_data_points=7 or fit failure)",
     defining_paper="Leoni et al. 2022 (early SN Ia RF); not read in this wave",
     accuracy_against_scored_measurement="Recount: 0/10 non-default on " + ALERT_Q + "; every sealed alert had 1-3 diaSources (< 7), so the code default -1.0 was returned. FAIL at emit.",
     what_it_is_not="Not defined below 7 diaSources; not the ZTF sigmoid RF used in the wave-2 calibration composition",
     conventions=["cpsfFlux passed to Rainbow fit in nJy with no conversion", "band wavelengths u 3671, g 4827, r 6223, i 7546, z 8691, y 9712 A (lowercase y)"],
     served_checkpoint={"identifier": "data/models/sklearn_1.7.2/elasticc_rainbow_earlyIa_nometa-1.7.2.obj",
                        "pin": "fink-science 591e75ce; sha256 089bc04959ecb87756f6d725ed4e5da1b5d68b2649eb03952388a753165d3a38"},
     disagreements=[
         {"topic": "flux units vs training", "code_rubin_snn": "fink_science/rubin/snn/processor.py converts psfFlux nJy to FLUXCAL with fac=10**(-(31.4-27.5)/2.5)", "code_rubin_rf": "random_forest_snia/processor.py passes psfFlux in nJy unconverted to a model named 'elasticc_...' (ELAsTiCC FLUXCAL); amplitude features differ by a factor ~36 between the two conventions"},
         {"topic": "docstring", "docstring": "rfscore_rainbow_elasticc_nometa docstring: 'cpsfFlux, cpsfFluxErr: Magnitude from PSF-fit photometry'", "code": "values are fluxes"},
         {"topic": "band case", "code_rf": "rfscore uses 'y'", "extract_features_rainbow default": "uses 'Y'"}])

card("Fink_SLSN_RF_Rubin",
     role="predictor",
     quantity_returned="P(SLSN) from SLSN_rainbow_no_MD.joblib over Rainbow features; 0 when the minimum points per passband is not met",
     defining_paper="Fink SLSN (Russeil et al.); not read in this wave",
     accuracy_against_scored_measurement="Recount: 0/10 non-default on " + ALERT_Q + " (all alerts below the per-passband minimum). FAIL at emit.",
     what_it_is_not="Not usable at first alert or within the ~2 weeks of Rubin on-sky data available for the sampled cohort objects",
     served_checkpoint={"identifier": "data/models/SLSN_rainbow_no_MD.joblib", "pin": "fink-science 591e75ce; sha256 855e55d0cc271efef3c3fa4c75eef00ac8f48ae6ca57b1fbe138aa9c88ce5df4"},
     disagreements=[{"topic": "kernel vs disk", "code": "kernel.py references data/models/SLSN_rainbow_MD.joblib", "disk": "absent at 591e75ce (only no_MD present); metadata=False path used by slsn_rubin"}])

card("SuperNNova_Fink_Rubin",
     role="predictor",
     quantity_returned="P(Ia) (elasticc_ia) and broad-class vector (elasticc_broad) from SuperNNova classify_lcs",
     defining_paper="Möller & de Boissière 2020 (SuperNNova); not read in this wave",
     accuracy_against_scored_measurement="Recount: 0/10; every alert run raised KeyError \"['MWEBV'] not in index\" inside supernnova classify_lcs feature assembly. FAIL.",
     what_it_is_not="Not runnable through the Fink Rubin wrapper at 591e75ce with supernnova 3.0.51: the served models require an MWEBV feature the wrapper never supplies",
     served_checkpoint={"identifier": "snn_models/elasticc_ia/model.pt and elasticc_broad/model.pt",
                        "pin": "fink-science 591e75ce; sha256 614179b963e5e1a59565fd5436861ad41ed89bed2b5d0b3c140ddfb3a5315cbe; 7109780045d709544afcd5eb31b061a017f4f36039ed24fc9effbe6317daf8ee"},
     disagreements=[
         {"topic": "model features vs wrapper", "model": "elasticc_ia/cli_args.json non_redshift_features include 'MWEBV' and band 'Y'", "wrapper": "rubin/snn/processor.py passes midpointMjdTai, band, psfFlux, psfFluxErr only; Rubin band is lowercase 'y'"},
         {"topic": "docstring vs usage", "docstring": "snn_ia_elasticc doctest block: '# Does not work for the moment'", "code": "function is exported with no guard"},
         {"topic": "dependency pin", "install_python_deps.sh": "pip install -r requirements.txt", "repo": "no requirements.txt at 591e75ce, so no supernnova version is pinned"}])

card("Astromer1",
     role="encoder",
     quantity_returned="per-observation attention embeddings (SingleBandEncoder.encode) of a single-band (time, magnitude, magnitude error) series",
     defining_paper="Donoso-Oliva et al. 2023 (ASTROMER); not read in this wave",
     accuracy_against_scored_measurement="Recount: loaded (public API, macho_a0 weights hash 76a204a3 match), 0/10: ASTROMER load_numpy generator rejects the v11_1 row array (TypeError inside tf.data). FAIL at parse.",
     what_it_is_not="Not a flux-input or multiband model; v11_1 carries psfFlux in nJy and no code path converts it",
     served_checkpoint={"identifier": "astromer-science/weights macho_a0.zip", "pin": "commit 649eda47; sha256 76a204a37a0d47bfd722477f55231624c0c56cf9eea3369b5f22ff445d95158b"},
     disagreements=[
         {"topic": "loader decorator", "code": "ASTROMER/models.py from_pretraining(cls, name='macho') has no @classmethod; SingleBandEncoder.from_pretraining('macho_a0') binds 'macho_a0' to cls and downloads the default"},
         {"topic": "README weights name", "README": "model.from_pretraining('macho')", "weights repo": "no macho.zip on main (HTTP 404; GitHub HTML page saved as zip -> BadZipFile); only macho_a0.zip and macho_a1.zip exist"},
         {"topic": "zip layout", "code": "from_pretraining reads weights/<name>/conf.json", "zip": "macho_a0.zip extracts to macho/, so the README instance-call path raises FileNotFoundError weights/macho_a0/conf.json"},
         {"topic": "unpinned fetch", "code": "weights fetched from weights/raw/main, not a commit"}])

card("Astromer2",
     role="encoder",
     quantity_returned="pretrained Astromer 2 ('base' arch, 6 layers) representations of (time, magnitude, error) windows of 200",
     defining_paper="Astromer 2 (Donoso-Oliva et al.); Zenodo 10.5281/zenodo.18207945 metadata read, paper not read",
     accuracy_against_scored_measurement="Recount: loaded (pt_macho_v2_2025.zip md5 42dfac36 match), 0/10: src.data.loaders.load_numpy rejects v11_1 rows (expects float (None,3)). FAIL at parse.",
     what_it_is_not="Not flux-input; not multiband",
     served_checkpoint={"identifier": "Zenodo 18207945 pt_macho_v2_2025.zip", "pin": "md5 42dfac36992119f5c4364c83729f3111; sha256 f06d68fc2b421efd5b2177daa943937f5f741242d94b2110b2a404fe79636bff"},
     disagreements=[
         {"topic": "dependency pin", "requirements": "main-code requirements.txt pins tensorflow==2.14", "run": "loaded under tensorflow 2.15.0"},
         {"topic": "entry point", "code": "get_loader(list) calls load_records_v2 (TFRecord files), not numpy; the numpy path is load_numpy"}])

card("AstroM3",
     role="encoder",
     quantity_returned="photometry Informer (CLIP-photo, 10-class head) over 200-step, 9-feature photometry tensors",
     defining_paper="Rizhko & Bloom 2024, arXiv:2411.08842; not read in this wave",
     accuracy_against_scored_measurement="Recount: loaded (HF AstroMLCore/AstroM3-CLIP-photo rev 8904ed33, safetensors oid 05d5f0b8), 0/10: process_photometry cannot tensorise v11_1 rows (ValueError too many dimensions 'str'). FAIL at parse.",
     what_it_is_not="Not a transient classifier: trained on ASAS-SN variable stars with LAMOST spectra",
     served_checkpoint={"identifier": "huggingface AstroMLCore/AstroM3-CLIP-photo model.safetensors", "pin": "revision 8904ed332cb9437691932a6d44e9a25a123cf76f; lfs sha256 05d5f0b8debb292a8b43095cd5c2ed15625c11365a37494d359cbf600565831d"},
     disagreements=[{"topic": "weights availability vs wave-1 inventory", "wave1": "'none found in repo; paper made available upon acceptance' (UNAVAILABLE)", "now": "weights public on Hugging Face under AstroMLCore (12 model repos), not in the GitHub repo"}])

card("Maven",
     role="encoder",
     quantity_returned="CLIP embeddings of ZTF light curves (R, g magnitudes) and SEDM spectra",
     defining_paper="Zhang et al. 2024 (Maven); not read in this wave",
     accuracy_against_scored_measurement="Recount: loaded (ckpt sha256 0fc75ccc match), 0/10: src.dataloader.load_lightcurves requires ZTFBTS_TransientTable.csv (A_V, redshift) alongside ZTF band CSVs. FAIL at parse.",
     what_it_is_not="Not decision-time or Rubin-ready: its loader joins the BTS transient table",
     served_checkpoint={"identifier": "models/clip_noiselesssimpretrain_clipreal/gallant-sweep-1/epoch=30-step=3627.ckpt", "pin": "ThomasHelfer/multimodal-supernovae 1f571aa9; sha256 0fc75ccc06ac33ae481ae08481b27d0d8a6378643f661c1f5c4a5a34dc8cd880"},
     disagreements=[{"topic": "label-bearing input", "code": "load_lightcurves reads ZTFBTS_TransientTable.csv (a BTS table; the code reads its ZTFID, A_V and redshift columns) to apply MW extinction and filter objects", "exposure": "the inference loader touches the outcome-bearing table; rule C exposure"},
                    {"topic": "band names", "code": "bands ['R','g'] with wave_eff g=1196.25 A (comment says ZTF-g effective wavelength; ZTF g is ~4800 A)"}])

card("BTSbot",
     role="predictor",
     quantity_returned="save/trigger score from ConvNeXt-pico over 63x63 science/reference/difference triplets plus 25 ZTF metadata columns",
     defining_paper="Rehemtulla et al. 2024, arXiv:2401.15167 (read in wave 1)",
     accuracy_against_scored_measurement="Recount: loaded (pytorch_model.bin sha256 c30f3202 match), 0/10: KeyError on sgscore1, distpsnr1, … (ZTF-only metadata). FAIL at parse.",
     what_it_is_not="Not a Rubin tool; trained on BTS scanner decisions (the governed decision)",
     served_checkpoint={"identifier": "HF nabeelr/BTSbot-convnext-pico-galaxyzoo-metadata pytorch_model.bin", "pin": "sha256 c30f32021da00f8778d348b1f70067532200f271ef7497c0371032b315654592"},
     disagreements=[{"topic": "unpinned download", "code": "from_HF.download_HF_model calls snapshot_download without revision (main)", "inventory": "wave-1 pinned HF revision d1014759; served bin hash still matches"},
                    {"topic": "undeclared import", "code": "alert_utils.py imports bson at package import time", "requirements": "lists bson and pymongo; in this run the bson module was supplied by pymongo"}])

card("RAPID",
     role="predictor",
     quantity_returned="per-epoch class probabilities (Pre-explosion, SNIa, SNII, SNIbc, SLSN, TDE, …) from ZTF_unknown_redshift TCN",
     defining_paper="Muthukrishna et al. 2019 (RAPID); not read in this wave",
     accuracy_against_scored_measurement="Recount: loaded under TF 2.15 (model sha256 d68ed438 match), 0/10: Classify._do_error_checks asserts len(light_curve)==10; v11_1 supplies 7 of the 10 tuple fields (no photflag, redshift, mwebv). FAIL at parse (logged as error:infer by the generic stage mapper; traceback places it in the input validator).",
     what_it_is_not="Not a Rubin model: ZTF g/r passbands only",
     served_checkpoint={"identifier": "astrorapid/ZTF_unknown_redshift.hdf5", "pin": "astrorapid 7f28499f; sha256 d68ed438c2d2e4f6f4e7a86e3eb1e02b1afb9946295f3b3225ecd788a4bad967"},
     disagreements=[{"topic": "unknown-redshift input", "docstring": "known_redshift=False model 'ZTF_unknown_redshift'", "code": "_do_error_checks still requires a 10-tuple including redshift and mwebv"},
                    {"topic": "deprecated deps", "code": "classify.py imports pkg_resources (via helpers)", "run": "load failed with ModuleNotFoundError pkg_resources until setuptools<70 was installed"}])

card("ORACLE",
     role="predictor",
     quantity_returned="hierarchical conditional class probabilities (ORACLE_lite, no metadata)",
     defining_paper="Shah et al. 2025, arXiv:2501.01496; not read in this wave",
     accuracy_against_scored_measurement="Recount: loaded only under the pinned tensorflow/keras 2.15 (keras 3 load raised GRU time_major), 0/10: prep_dataframes KeyError 'FLUXCAL'. FAIL at parse.",
     what_it_is_not="Not an lsst v11_1 alert consumer: reads ELAsTiCC SNANA columns FLUXCAL, FLUXCALERR, MJD, PHOTFLAG, BAND",
     served_checkpoint={"identifier": "models/lsst_alpha_0.5_no_md/best_model.h5", "pin": "uiucsn/Astro-ORACLE 876e0339 (in-repo)"},
     disagreements=[{"topic": "maintenance", "README": "repository 'will no longer be maintained'; users directed to dev-ved30/Oracle (PyTorch rewrite)", "inventory": "wave-1 counted this repo as the ORACLE tool"},
                    {"topic": "input naming", "paper": "described as a real-time LSST alert classifier", "code": "expects SNANA FITS column names, no Rubin alert parser"}])

card("Superphot_plus",
     role="predictor",
     quantity_returned="class probabilities from a LightGBM over light-curve fit parameters",
     defining_paper="de Soto et al. 2024 (Superphot+); read in wave 1 (agent 2)",
     accuracy_against_scored_measurement="Recount: loaded, 0/10: snapi Photometry requires a time/phase/mjd column or DatetimeIndex (TypeError). FAIL at parse.",
     what_it_is_not="Not Rubin-trained; tutorial model only",
     served_checkpoint={"identifier": "data/tutorial/model_superphot_full.pt", "pin": "superphot-plus 973e2a80; sha256 a9536ff1d277f054beff2f51557cc4e00540b3daddd4cf51d2833135da645a88"},
     disagreements=[{"topic": "file format vs extension", "file": "model_superphot_full.pt is a plain pickle of superphot_plus.model.lightgbm.SuperphotLightGBM", "code": "SuperphotMLP.load uses torch.load and fails ('Invalid magic number'); the .pt extension implies a torch MLP"},
                    {"topic": "unpinned dependency", "pyproject": "snapi @ git+https://github.com/kdesoto-astro/snapi.git (no ref)", "run": "resolved to 4a419fe0 on 2026-09-16"}])

card("GHOST",
     role="predictor",
     quantity_returned="host-galaxy association table (host coordinates and PS1-based properties) for a transient position",
     defining_paper="Gagliano et al. 2021 (GHOST); not read in this wave",
     accuracy_against_scored_measurement="Recount: 3 non-default host associations out of 8 valid alert runs (2 runs voided, AM2), on ra/dec from " + ALERT_Q + ". I4 not assessed.",
     what_it_is_not="Not a classifier of the transient itself",
     served_checkpoint={"identifier": "astro_ghost MLP_lupton.hdf5 + Star_Galaxy_RealisticModel_GHOST_PS1ClassLabels.sav", "pin": "uiucsn/astro_ghost d7a1dec6; sha256 13ac27c2f6807970b349f434158c95710cbeac2666dee86116e70f84dfb1d820; 48f78c9cdc29c9d0c9ecd6c63194a7d08430a60c598311b433f874d92ab0f040"},
     disagreements=[{"topic": "dependency pins", "setup.cfg": "numpy<1.25, scikit-learn<1.3", "run": "required a separate py3.10 environment"},
                    {"topic": "sky coverage", "wave1": "inventory note 'PS1 dec>-30 split'", "recount": "hosts returned for 3 alerts at dec ~ -40; the source catalogue for that match was not inspected (output discarded under rule D)"}])
print("cards", len(list(OUT.glob("*.json"))))
