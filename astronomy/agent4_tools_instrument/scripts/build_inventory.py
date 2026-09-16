#!/usr/bin/env python3
"""D4 tool inventory + P3 tool-coverage axis for the astronomy candidate.

Every row below was written from the shallow clones under ../code (commits in
../code/CLONE_PINS.tsv) and, where a paper was read, from ../sources. Status
vocabulary per input source:

  AVAILABLE_VERIFIED    code ingests that source's packet format AND the pinned
                        weights were trained or validated on real data of that
                        survey (per code/data files or a source read in full)
  AVAILABLE_UNVERIFIED  code path or a format mapping exists and weights (or a
                        weight-free model) exist, but training/validation on real
                        data from that survey is not established
  UNAVAILABLE           a required input is absent from the packet, no weights
                        exist for its bands, or no code path exists
  UNDEMONSTRATED        runnability could not be settled from pinned artifacts

Counts are computed here, never typed by hand.  Run:
    python3 scripts/build_inventory.py
"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

AV, AU, UN, UD = "AVAILABLE_VERIFIED", "AVAILABLE_UNVERIFIED", "UNAVAILABLE", "UNDEMONSTRATED"

T = []  # tool rows
def tool(**k):
    T.append(k)

# ---------------------------------------------------------------- FM / deep channels
tool(id="ATAT", family="deep_supervised_transformer", fm_channel=True,
     repo="alercebroker/ATAT@0db532f2", roles=["predictor"],
     input_from_code="ELAsTiCC SNANA FITS -> h5: FLUXCAL/FLUXCALERR in 6 bands, 65-epoch padded grid, masks; optional 64 ELAsTiCC header fields (HOSTGAL_* photo-z quantiles, REDSHIFT_HELIO, MWEBV) and 429 features (src/data/get_lc_md.py::feat_dict; datasets.py channel_dict={'ELASTICC':6})",
     output_from_code="20-class log-softmax over ELAsTiCC taxonomy (datasets.py::classes_names; layers/classifier.py LogSoftmax)",
     weights="Google Drive id 1teIi3GfPbYOZXaIHRAa_OCPTY9QYXTU1 (results_paper.zip, 10G per Drive page 2026-09-16) via get_important_files.sh; not downloaded (>500MB), no hash taken",
     trained_on="ELAsTiCC v1 simulated training set only (README 'Get data'; paper Sec 2.1)",
     ztf=UN, ztf_why="no ZTF dataset entry in the ATAT repo (datasets.py channel_dict/seq_dict only ELASTICC, ELASTICC_STREAM); a ZTF ATAT training/inference path exists in alercebroker/pipeline@b58b866b training/lc_classifier_ztf/ATAT_ALeRCE but ships no weights",
     rubin=AU, rubin_why="LC branch consumes 6-band difference flux, mappable from DIASource psfFlux; metadata branch needs HOSTGAL_*/REDSHIFT_HELIO absent from lsst.v11_1 diaObject/diaSource; trained only on simulation; weights unpinned",
     counterparts=["ALeRCE_BHRF"])
tool(id="ORACLE", family="deep_supervised_rnn", fm_channel=True,
     repo="uiucsn/Astro-ORACLE@876e0339", roles=["predictor"],
     input_from_code="FLUXCAL, FLUXCALERR, MJD, BAND(u,g,r,i,z,Y), PHOTFLAG + 23 static features incl. REDSHIFT_HELIO, HOSTGAL_PHOTOZ/SPECZ, HOSTGAL_MAG_* (src/astroOracle/dataloader.py::static_feature_list)",
     output_from_code="conditional probabilities over a 26-node hierarchy (pretrained_models.py; paper Fig 3)",
     weights="models/lsst_alpha_0.5/best_model.h5 sha256 4643e84f...53bc3f; models/lsst_alpha_0.5_no_md/best_model.h5 sha256 5be1ae62...fa698 (in-repo)",
     trained_on="ELAsTiCC2 simulated training sample (README 'Convert Elasticc 2 train dataset'; paper Sec 3)",
     ztf=UN, ztf_why="bands u..Y only; no ZTF model",
     rubin=AU, rubin_why="ORACLE-lite (no_md) needs only time-series columns mappable from DIASource/DIAForcedSource; full model needs static host/redshift features absent from the Rubin alert packet; simulation-trained",
     counterparts=["ALeRCE_BHRF", "Fink_EarlySNIa_RF"])
tool(id="SuperNNova", family="deep_supervised_rnn", fm_channel=True,
     repo="supernnova/SuperNNova@ac2aff73 + astrolabsoftware/fink-science@591e75ce", roles=["predictor"],
     input_from_code="Rubin: midpointMjdTai, band, psfFlux, psfFluxErr converted to FLUXCAL zp27.5 (fink_science/rubin/snn/processor.py L114); ZTF: fink_science/ztf/snn",
     output_from_code="class probabilities (Ia vs rest, broad 5-way) per alert",
     weights="fink data/models/snn_models/elasticc_ia/model.pt sha256 614179b9...5cbe; elasticc_broad 7109780...daf8ee; snn_snia_vs_nonia 28daec3d...913b (in-repo)",
     trained_on="ELAsTiCC for Rubin models (fink data/models/README.md 'Elasticc/Rubin' table; paper 2404.08798 Sec 5.2); ZTF model training set not established from a source read",
     ztf=AU, ztf_why="ZTF science module and model exist; training data provenance of snn_snia_vs_nonia not established",
     rubin=AU, rubin_why="code ingests Rubin DIASource columns; doctest input is datasim/rubin_test_data_10_0.parquet (simulated); ELAsTiCC-trained",
     counterparts=["Fink_EarlySNIa_RF", "Fink_SLSN_RF"])
tool(id="CATS", family="deep_supervised_lstm", fm_channel=True,
     repo="astrolabsoftware/fink-science@591e75ce (rubin/cats)", roles=["predictor"],
     input_from_code="midpointMjdTai, psfFlux, psfFluxErr, band (rubin/cats/processor.py::predict_nn); model 'cats_small_nometa' (no metadata)",
     output_from_code="5 broad-class scores (SN-like, Fast, Long, Periodic, Non-periodic)",
     weights="cats_small_nometa_serial.keras sha256 e51239df...c8f (pruned after hashing, see code/PRUNED_LARGE_FILES.tsv)",
     trained_on="ELAsTiCC v1 streamed alerts (paper 2404.08798 Sec 2, 5.1)",
     ztf=UN, ztf_why="Rubin-only module",
     rubin=AU, rubin_why="ingests Rubin schema columns; simulation-trained; deployed model drops the metadata branch described in the paper",
     counterparts=["Fink_EarlySNIa_RF", "Fink_SLSN_RF"])
tool(id="RAPID", family="deep_supervised_rnn", fm_channel=True,
     repo="daniel-muthukrishna/astrorapid@7f28499f", roles=["predictor"],
     input_from_code="mjd, flux, fluxerr, passband ('g','r'), photflag, ra, dec, objid, redshift, mwebv (README example; classify.py L38 passbands=('g','r'))",
     output_from_code="time-resolved class probabilities over 12 transient classes + Pre-explosion",
     weights="ZTF_known_redshift.hdf5 sha256 96ce0762...cc9c; ZTF_unknown_redshift.hdf5 d68ed438...d967 (in-repo, pruned after hashing)",
     trained_on="SNANA simulations with PLAsTiCC models and a ZTF MSIP observing-conditions library (paper 1904.00014 Sec 2.1; section read, paper not read in full)",
     ztf=AU, ztf_why="native g/r input; simulation-trained; known-redshift model needs a redshift not in the ZTF alert",
     rubin=UN, rubin_why="no ugrizy weights",
     counterparts=["ALeRCE_BHRF", "Superphot_plus"])
tool(id="SCONE", family="deep_supervised_cnn", fm_channel=True,
     repo="helenqu/scone@9b72001b", roles=["predictor"],
     input_from_code="SNANA HEAD/PHOT FITS (SNID, MJD, FLT, FLUXCAL, FLUXCAL_ERR, PEAKMJD, MWEBV) -> GP heatmaps (README 'Input Data')",
     output_from_code="Ia vs non-Ia or categorical probabilities",
     weights="none released in repo (no *.h5/*.keras/*.pt found); training required",
     trained_on="n/a (no weights)",
     ztf=UN, ztf_why="no weights; input requires PEAKMJD from SNANA truth header",
     rubin=UN, rubin_why="no weights; PEAKMJD not in the alert packet",
     counterparts=["SALT3_sncosmo", "ALeRCE_BHRF"])
tool(id="BTSbot", family="deep_supervised_multimodal_cnn", fm_channel=True,
     repo="nabeelre/BTSbot@f4281202; HF nabeelr/BTSbot-convnext-pico-galaxyzoo-metadata@d1014759", roles=["predictor"],
     input_from_code="ZTF alert triplet cutouts + 25 ZTF candidate fields incl. sgscore1, distpsnr1, nmtchps, new_drb, chinr, sharpnr, scorr (train_config.json metadata_cols)",
     output_from_code="unit-interval bright-transient score per alert",
     weights="pytorch_model.bin sha256 c30f3202...4592 (downloaded, matches HF LFS oid)",
     trained_on="ZTF BTS scanning decisions: positives = BTS-saved bright SNe, negatives = sources rejected by BTS (paper 2307.07618 Sec 2.1)",
     ztf=AV, ztf_why="real ZTF alerts; label is the BTS follow-up decision itself (exposure/leakage flag)",
     rubin=UN, rubin_why="sgscore1, distpsnr1, nmtchps, drb, chinr, sharpnr, scorr absent from lsst.v11_1 schema",
     counterparts=["ALeRCE_BHRF"])
tool(id="AppleCiDEr", family="deep_supervised_multimodal", fm_channel=True,
     repo="skyportal/applecider@48148937", roles=["predictor"],
     input_from_code="ZTF photometry, metadata, image cutouts, spectra (README; src/applecider)",
     output_from_code="transient class probabilities",
     weights="none in repo; default_config.toml pretrained_weights_path_='./pretrained_weights.pth' placeholder",
     trained_on="not established (paper 2507.16088 not read in full)",
     ztf=UN, ztf_why="no pinned weights", rubin=UN, rubin_why="ZTF-specific inputs; no weights",
     counterparts=["ALeRCE_BHRF"])
tool(id="Maven", family="foundation_model_contrastive", fm_channel=True,
     repo="ThomasHelfer/multimodal-supernovae@1f571aa9", roles=["encoder"],
     input_from_code="ZTF light curves in bands ['R','g'] as (time, mag, magerr) with MW extinction correction (src/dataloader.py L482-509) + SEDM spectra",
     output_from_code="contrastive embedding; downstream kNN/SVC/linear heads",
     weights="models/clip_noiselesssimpretrain_clipreal/gallant-sweep-1/epoch=30-step=3627.ckpt sha256 0fc75ccc...cd880 (one of 5 folds; pruned after hashing)",
     trained_on="0.5M SNANA ZTF-like simulations, fine-tuned on 4,702 ZTF BTS SNe (paper 2408.16829 Sec 2.1-2.2); train_filenames.txt lists BTS objects",
     ztf=AV, ztf_why="real ZTF BTS photometry; fine-tuned on the BTS label base itself (exposure flag); spectral branch unavailable before follow-up",
     rubin=UN, rubin_why="band embedding covers only ZTF r/g",
     counterparts=["Superphot_plus", "ALeRCE_BHRF", "SALT3_sncosmo"])
tool(id="Astromer1", family="foundation_model_masked", fm_channel=True,
     repo="astromer-science/python-library@75262739 + astromer-science/weights@649eda47", roles=["encoder"],
     input_from_code="single-band L x 3 arrays (time, magnitude, magnitude std), 200-epoch windows (python-library README)",
     output_from_code="attention vectors (embeddings)",
     weights="macho_a0.zip sha256 76a204a3...158b; macho_a1.zip 1da01909...ec6c (in weights repo; README also advertises 'atlas' weights not present in the weights repo)",
     trained_on="MACHO light curves (weights names; README)",
     ztf=AU, ztf_why="per-band magnitude series mappable; variable-star pretraining, no transient validation",
     rubin=AU, rubin_why="per-band series mappable from psfFlux; same caveat",
     counterparts=["ALeRCE_BHRF"])
tool(id="Astromer2", family="foundation_model_masked", fm_channel=True,
     repo="astromer-science/main-code@009634c8 (sparse checkout, output weights excluded)", roles=["encoder"],
     input_from_code="single-band magnitude time series (README)",
     output_from_code="embeddings",
     weights="Zenodo 10.5281/zenodo.18207945 (README); not downloaded, no hash taken",
     trained_on="1.5M MACHO light curves (README 'Key Features')",
     ztf=AU, ztf_why="format mappable; unpinned; variable-star domain",
     rubin=AU, rubin_why="format mappable; unpinned; variable-star domain",
     counterparts=["ALeRCE_BHRF"])
tool(id="MultibandAstromer", family="foundation_model_masked", fm_channel=True,
     repo="astromer-science/multiband-astromer@7228548b", roles=["encoder"],
     input_from_code="multiband windows of 200 (README get_MBAstromer)",
     output_from_code="embeddings",
     weights="none found in repo", trained_on="MACHO / Alcock / ATLAS per README",
     ztf=UN, ztf_why="no weights", rubin=UN, rubin_why="no weights",
     counterparts=["ALeRCE_BHRF"])
tool(id="AstroCLIP", family="foundation_model_contrastive", fm_channel=True,
     repo="PolymathicAI/AstroCLIP@e129576a; HF polymathic-ai/astroclip@4af71e52", roles=["encoder"],
     input_from_code="galaxy image cutouts (Legacy Survey g,r,z) and DESI spectra (README Pretrained Models; configs/astroclip.yaml)",
     output_from_code="shared galaxy embedding (host-galaxy channel)",
     weights="astroclip.ckpt 1,680,929,841 bytes, HF-reported LFS sha256 e1689395...6d56 (not downloaded: >500MB; not locally verified)",
     trained_on="DESI Legacy Survey images x DESI spectra (README)",
     ztf=UN, ztf_why="not in the alert; needs host association plus external Legacy Survey cutouts (footprint-limited)",
     rubin=UN, rubin_why="same; Rubin alert carries no host identification",
     counterparts=["GHOST", "Blast"])
tool(id="AstroM3", family="foundation_model_contrastive", fm_channel=True,
     repo="MeriDK/AstroM3@7f296c22", roles=["encoder"],
     input_from_code="ASAS-SN photometry + LAMOST spectra + metadata for variable stars (README Data; src/model.py)",
     output_from_code="trimodal embedding / variable-star class",
     weights="none found in repo; paper 2411.08842 'made available upon acceptance'",
     trained_on="AstroM3Dataset (variable stars)",
     ztf=UN, ztf_why="domain and inputs differ; no weights", rubin=UN, rubin_why="same",
     counterparts=["ALeRCE_BHRF"])
tool(id="ParSNIP", family="deep_generative_physics_vae", fm_channel=True,
     repo="kboone/parsnip@dcea62fe", roles=["encoder", "generator", "scorer"],
     input_from_code="encode: gridded flux + weights per model band + redshift (or photo-z) channel (parsnip.py::_get_data); decode/decode_spectra: agent-set latent s1..s3, color, amplitude, ref time, redshift (parsnip.py L856-949); predict_redshift_distribution: NLL over an agent-chosen redshift grid (L1719); ParsnipSncosmoSource exposes (amplitude,color,s1..s3) to sncosmo fitting (sncosmo.py)",
     output_from_code="latent posteriors; model spectra/photometry; per-redshift NLL",
     weights="plasticc.pt sha256 a164aefe...7366 (bands lsstu..lssty); ps1.pt 9ebf0a6e...1968 (ps1::g..z); plasticc_photoz.pt f41d06ce...2452 (in-repo)",
     trained_on="PLAsTiCC simulation; PS1-MDS real (paper Sec 2)",
     ztf=UN, ztf_why="no pretrained model with ztfg/ztfr encoder bands; internal decode restricted to model bands (sncosmo-source route can integrate any registered bandpass)",
     rubin=AU, rubin_why="plasticc model uses sncosmo 'lsst' v1.1 2016 throughputs; encoder needs redshift or hostgal_photoz not in the packet, but generator/scorer paths accept an agent-supplied redshift",
     counterparts=["SALT3_sncosmo", "Superphot_plus"])

# ---------------------------------------------------------------- classical counterparts
tool(id="ALeRCE_BHRF", family="classical_balanced_hierarchical_rf", fm_channel=False,
     repo="alercebroker/lc_classifier@b8a85200", roles=["predictor"],
     input_from_code="ZTF detections (fid 1/2, magpsf(_corr), sigmapsf, rb>=0.55), non-detections diffmaglim, sgscore1, AllWISE W1-W3 -> 152 features (features_RF_model.pkl list); ElasticcRandomForest class for ELAsTiCC features",
     output_from_code="15-class probabilities = top-level x bottom-level (classifier/models.py::predict_proba)",
     weights="https://assets.alerce.online/pipeline/hierarchical_rf_1.1.1/ sha256 features_RF_model.pkl 1e4d15cd...00d3, top_level d160264a...e88, transient_level b77ca8cc...0e29, periodic_level 8cb2f994...091b, stochastic_level 56b647a0...013e (code/_downloaded_artifacts/alerce_hrf_1.1.1/SHA256SUMS; downloaded, hashed, large pickles deleted); no ELAsTiCC/Rubin weight URL in code",
     trained_on="ZTF labelled set cross-matched to catalogues (paper 2008.03311 Sec 2.2.1)",
     ztf=AV, ztf_why="real ZTF alerts; needs AllWISE cross-match and >5 detections",
     rubin=UN, rubin_why="no Rubin/ELAsTiCC weights: ElasticcRandomForest has no download URL, and the ATAT repo's results_rf_paper.zip (sha256 07ef884a...684b) holds predictions and stats only, no model; the ZTF model needs sgscore1, rb and g/r magnitudes",
     counterparts=[])
tool(id="SALT3_sncosmo", family="classical_empirical_sed_template", fm_channel=False,
     repo="sncosmo/sncosmo@a42c9363 (+ djones1040/SALTShaker@5183c2dc training code)", roles=["scorer", "generator"],
     input_from_code="photometry table in any registered bandpass (ztfg/ztfr/ztfi; lsstu..lssty v1.1 2016) + agent-set or fitted z, t0, x0, x1, c (builtins.py L372-381, L448-457, L1033-1040; models.py::SALT3Source)",
     output_from_code="model band fluxes and relative model variance; fit_lc chi2 and parameter posteriors under the SN Ia hypothesis",
     weights="salt3-f22 v2.0 tarball sha256 c7de5343...a37e (downloaded)",
     trained_on="SALT3.K21 compilation, recalibrated 'Fragilistic' F22 (builtins.py meta note)",
     ztf=AU, ztf_why="ZTF bandpasses registered; K21 training compilation contains no ZTF data (paper Table 4)",
     rubin=AU, rubin_why="LSST bandpasses are 2016 baseline v1.1 throughputs, not as-built",
     counterparts=[])
tool(id="Superphot_plus", family="classical_parametric_fit_plus_classifier", fm_channel=False,
     repo="VTDA-Group/superphot-plus@973e2a80", roles=["predictor", "generator"],
     input_from_code="ZTF g/r photometry (priors_ZTF_g.csv, priors_ZTF_r.csv; data_generation/alerce.py); data_generation/make_fake_spp_data.py simulates light curves",
     output_from_code="fitted 14-parameter model posteriors; 5-class SN probabilities",
     weights="data/tutorial/model_superphot_full.pt sha256 a9536ff1...5a88 (tutorial model; training set not established)",
     trained_on="not established (paper 2403.07975 not read in full)",
     ztf=AU, ztf_why="ZTF priors and import path; model provenance unread",
     rubin=UN, rubin_why="no LSST-band priors or model in repo",
     counterparts=[])
tool(id="Superphot", family="classical_parametric_fit_plus_classifier", fm_channel=False,
     repo="griffin-h/superphot@eb3e31be", roles=["predictor"],
     input_from_code="PS1-MDS griz photometry", output_from_code="class probabilities after training",
     weights="none", trained_on="n/a",
     ztf=UN, ztf_why="no weights", rubin=UN, rubin_why="no weights", counterparts=[])
tool(id="Fink_EarlySNIa_RF", family="classical_rainbow_features_rf", fm_channel=False,
     repo="astrolabsoftware/fink-science@591e75ce (rubin/random_forest_snia, ztf/random_forest_snia)", roles=["predictor"],
     input_from_code="Rubin DIASource time series -> Rainbow multiband fit features (rubin/random_forest_snia/processor.py)",
     output_from_code="P(early SN Ia)",
     weights="sklearn_1.7.2/elasticc_rainbow_earlyIa_nometa-1.7.2.obj sha256 089bc049...3a38 (pruned after hashing)",
     trained_on="ELAsTiCC v1 alerts (paper 2404.08798 Sec 5.3)",
     ztf=AU, ztf_why="ZTF module and default-model_sigmoid.obj exist; training provenance not read",
     rubin=AU, rubin_why="ingests Rubin columns; simulation-trained", counterparts=[])
tool(id="Fink_SLSN_RF", family="classical_rainbow_features_rf", fm_channel=False,
     repo="astrolabsoftware/fink-science@591e75ce (rubin/slsn)", roles=["predictor"],
     input_from_code="Rubin DIASource series + optional metadata (rubin/slsn/kernel.py)",
     output_from_code="P(SLSN)",
     weights="SLSN_rainbow_no_MD.joblib sha256 855e55d0...8df4 (pruned after hashing); kernel.py also references SLSN_rainbow_MD.joblib, absent on disk",
     trained_on="ELAsTiCC v1 alerts (paper 2404.08798 Sec 5.4)",
     ztf=AU, ztf_why="ztf/superluminous module exists; provenance not read",
     rubin=AU, rubin_why="no-MD model ingests Rubin columns; simulation-trained", counterparts=[])
tool(id="Sherlock", family="classical_contextual_crossmatch", fm_channel=False,
     repo="thespacedoctor/sherlock@37ef9298", roles=["predictor"],
     input_from_code="transient coordinates + local catalogue database (transient_classifier.py association types AGN, CV, NT, SN, VS, BS, ORPHAN)",
     output_from_code="contextual classification and matched source",
     weights="no weights; catalogue database not public/provisioned",
     trained_on="rule-based",
     ztf=UN, ztf_why="catalogue DB not provisioned locally (runs as a Lasair service)",
     rubin=UN, rubin_why="same; Rubin page (sources/rubin_for-scientists_data-products_alerts-and-brokers.txt) states Lasair runs Sherlock", counterparts=[])
tool(id="GHOST", family="classical_host_association", fm_channel=False,
     repo="uiucsn/astro_ghost@d7a1dec6", roles=["predictor"],
     input_from_code="transient name/coordinates -> PS1 queries; north/south split at dec=-30 (ghostHelperFunctions.py L761); MLP_lupton.hdf5 photo-z",
     output_from_code="host galaxy match, PS1 photometry, photo-z",
     weights="MLP_lupton.hdf5 sha256 13ac27c2...c1dc (pruned after hashing)",
     trained_on="PS1 / SDSS (paper 2008.09630 not read in full)",
     ztf=AU, ztf_why="PS1 covers ZTF sky; external queries at runtime",
     rubin=AU, rubin_why="coordinates available; PS1 coverage limited for southern LSST fields", counterparts=[])
tool(id="Blast", family="classical_host_sed_service", fm_channel=False,
     repo="scimma/blast@614ace3b", roles=["predictor"],
     input_from_code="transient coordinates -> host match and SED fit (Django app; data/sbipp SBI models)",
     output_from_code="host galaxy properties (mass, SFR, redshift)",
     weights="data/sbipp/SBI_model.pt sha256 ac2d9d3b...fac5b72 (pruned after hashing)",
     trained_on="not established (paper 2410.17322 not read in full)",
     ztf=AU, ztf_why="service-style; external survey queries", rubin=AU, rubin_why="same", counterparts=[])
tool(id="SNANA", family="classical_simulator", fm_channel=False,
     repo="RickKessler/SNANA@74dfb2c5 (+ LSSTDESC/elasticc@818ae71e configs)", roles=["simulator"],
     input_from_code="agent-chosen SED models (genmag_*.c), rates, redshift range, SIMLIB cadence/noise",
     output_from_code="simulated light curves in survey format (FITS HEAD/PHOT)",
     weights="n/a; requires SNDATA_ROOT model libraries and survey SIMLIBs, not in the clone and not pinned",
     trained_on="n/a",
     ztf=UD, ztf_why="ZTF SIMLIB used by RAPID/Maven not public in the clones", rubin=UD, rubin_why="ELAsTiCC inputs at NERSC not pinned", counterparts=[])

NON_CHANNELS = [
    {"id": "MultimodalUniverse", "repo": "MultimodalUniverse/MultimodalUniverse@4e53d93d", "why": "dataset collection (includes BTS, PLAsTiCC, YSE, Foundation, PS1 SNe Ia subsets); baselines/plasticc/pretrained_model/pytorch_model.bin sha256 d4499e51...344d is a baseline, not a channel"},
    {"id": "ALeRCE_pipeline_lc_classification_step", "repo": "alercebroker/pipeline@b58b866b", "why": "deployment wrapper for ALeRCE production classifiers (balto, messi, barney, toretto, mbappe, squidward, anomaly; lc_classification_step/models_settings.py) whose weights come from env MODEL_PATH and are not pinned in code; its libs/survey_parser_plugins LSSTParser maps pre-v11 field names (alertId, filterName, midPointTai, decl, psFlux) with TODO comments, while lsst.v11_1 uses diaSourceId, band, midpointMjdTai, dec, psfFlux"},
    {"id": "SALTShaker", "repo": "djones1040/SALTShaker@5183c2dc", "why": "trains SALT3 surfaces; not a decision-time tool"},
    {"id": "ELAsTiCC", "repo": "LSSTDESC/elasticc@818ae71e", "why": "simulation configs/schemas; folded into SNANA row"},
    {"id": "lsst_alert_packet", "repo": "lsst/alert_packet@1362a8d7", "why": "Rubin alert schema lsst.v11_1 (latest.txt)"},
    {"id": "lsst_sdm_schemas", "repo": "lsst/sdm_schemas@5499df17", "why": "APDB schema v10.0.0 (yml/apdb.yaml)"},
    {"id": "ztf_avro_alert", "repo": "ZwickyTransientFacility/ztf-avro-alert@75a9831c", "why": "ZTF alert schema"},
]

# ---------------------------------------------------------------- counts
ch = T
fm = [t for t in ch if t["fm_channel"]]
cl = [t for t in ch if not t["fm_channel"]]
BELOW = {"scorer", "generator", "simulator"}
def cnt(rows, key):
    c = collections.Counter(r[key] for r in rows)
    return {s: c.get(s, 0) for s in (AV, AU, UN, UD)}

by_id = {t["id"]: t for t in ch}
cond_a = []
for t in fm:
    cps = [c for c in t["counterparts"] if c in by_id]
    cond_a.append({"fm_channel": t["id"], "counterparts": cps,
                   "counterpart_available_ztf": [c for c in cps if by_id[c]["ztf"] in (AV, AU)],
                   "counterpart_available_rubin": [c for c in cps if by_id[c]["rubin"] in (AV, AU)]})
below = [{"tool": t["id"], "roles_below_line": sorted(set(t["roles"]) & BELOW), "fm_channel": t["fm_channel"],
          "ztf": t["ztf"], "rubin": t["rubin"]} for t in ch if set(t["roles"]) & BELOW]

summary = {
    "n_channels": len(ch), "n_fm_or_deep": len(fm), "n_classical": len(cl),
    "role_counts": dict(collections.Counter(r for t in ch for r in t["roles"])),
    "ztf": {"fm_or_deep": cnt(fm, "ztf"), "classical": cnt(cl, "ztf"), "all": cnt(ch, "ztf")},
    "rubin": {"fm_or_deep": cnt(fm, "rubin"), "classical": cnt(cl, "rubin"), "all": cnt(ch, "rubin")},
    "condition_a_every_fm_has_classical_counterpart_in_code": all(len(x["counterparts"]) > 0 for x in cond_a),
    "condition_a_every_fm_structurally_available_on_rubin_has_available_counterpart": all(
        len(x["counterpart_available_rubin"]) > 0 for x in cond_a if by_id[x["fm_channel"]]["rubin"] in (AV, AU)),
    "condition_a_every_fm_structurally_available_on_ztf_has_available_counterpart": all(
        len(x["counterpart_available_ztf"]) > 0 for x in cond_a if by_id[x["fm_channel"]]["ztf"] in (AV, AU)),
    "condition_b_tools_below_line": [b["tool"] for b in below],
    "condition_b_below_line_available_rubin": [b["tool"] for b in below if b["rubin"] in (AV, AU)],
    "condition_b_below_line_available_ztf": [b["tool"] for b in below if b["ztf"] in (AV, AU)],
    "fm_channels_verified_on_real_rubin_alerts": [t["id"] for t in fm if t["rubin"] == AV],
    "fm_channels_verified_on_real_ztf": [t["id"] for t in fm if t["ztf"] == AV],
}

PROV_SLOT = {
    "referent": "which decision-time tools exist for early classification / spectroscopic follow-up allocation of transients, what role each plays by its code-level input and output, and whether it can process ZTF alert/BTS inputs and Rubin lsst.v11_1 alert packets",
    "source": "scripts/build_inventory.py rows; code/CLONE_PINS.tsv commits; weight sha256 in code/PRUNED_LARGE_FILES.tsv and code/_downloaded_artifacts/*/SHA256SUMS; schema lsst/alert_packet@1362a8d7 python/lsst/alert/packet/schema/11/1/*.avsc; papers in sources/ with section locators in seed_ledger.json",
    "population": "25 decision-time tool channels (15 FM or deep, 10 classical), one row per tool, not per variant or checkpoint; 7 repositories excluded as non-channels (datasets, schemas, training code)",
    "adjudicator": "the classical counterparts in the same inventory (ALeRCE_BHRF 1.1.1 on ZTF; SALT3-f22, Fink rainbow RFs on Rubin); the strongest existing deployed alternative on ZTF is BTSbot + human BTS scanning, which is itself an FM-side channel",
    "falsifier": "a released checkpoint for any row marked UNAVAILABLE that runs on the stated input format, or a source read showing a row marked AVAILABLE_UNVERIFIED was validated on real Rubin alerts, or a rerun of this script against newer commits that changes any status",
}

slot = {
    "id": "slot-tool_inventory-astronomy-2026-09-16",
    "slot": "tool_inventory",
    "candidate": "live time-domain astronomy (Rubin LSST alert stream + ZTF BTS label base); decision: spectroscopic follow-up allocation",
    "status": "DERIVED",
    "status_note": "derived at D4 from code; not ratified (D5 not run); readiness is a census, not certification (I5 UNDEMONSTRATED)",
    "value": {"tools": ch, "non_channels": NON_CHANNELS, "summary": summary,
              "condition_a_detail": cond_a, "condition_b_detail": below},
    "provenance": PROV_SLOT,
    **PROV_SLOT,
    "completeness": "Covered: 25 channels from 30 shallow clones read at code level (entry points, configs, weight files) plus 8 papers read in full (see seed_ledger.json). Not covered: RAPID, Superphot, Superphot+, GHOST, Blast, SNANA, SuperNNova, SCONE, Astromer 1/2, AstroCLIP, AstroM3, AppleCiDEr and Multimodal Universe papers were not read in full, so training-provenance fields for those rows rest on code/README only; AMPEL, ANTARES, Lasair, Pitt-Google and Babamul in-house classifiers were not cloned; no weight was executed; ATAT, Astromer2 and AstroCLIP checkpoints were not hashed locally.",
}

cov = {
    "id": "axis-tool_coverage-astronomy-2026-09-16",
    "axis": "tool_coverage",
    "stage": "P3 (pre-P1 sketch; one axis only)",
    "value": {"ztf_alert_or_bts": summary["ztf"], "rubin_lsst_v11_1_alert": summary["rubin"],
              "fm_verified_on_real_rubin": summary["fm_channels_verified_on_real_rubin_alerts"],
              "fm_verified_on_real_ztf": summary["fm_channels_verified_on_real_ztf"],
              "per_tool": [{"id": t["id"], "fm_channel": t["fm_channel"], "roles": t["roles"],
                            "ztf": t["ztf"], "ztf_why": t["ztf_why"], "rubin": t["rubin"], "rubin_why": t["rubin_why"]} for t in ch]},
    "referent": "number of tool channels that can structurally process each input source the task supplies, split by FM/deep vs classical, and how many are verified on real data from that source",
    "source": "scripts/build_inventory.py::summary over the per-tool status fields; Rubin packet fields from lsst/alert_packet@1362a8d7 schema/11/1/lsst.v11_1.diaObject.avsc and diaSource.avsc; ZTF fields from ztf-avro-alert@75a9831c schema/candidate.avsc",
    "population": "25 tool channels, one row per tool; statuses are per input source, not per alert or object",
    "adjudicator": "classical channels scored under the same four-status rule on the same two sources",
    "falsifier": "a Rubin-alert run of any AVAILABLE_UNVERIFIED FM channel whose outputs match the published simulation metrics would move it to AVAILABLE_VERIFIED; a Rubin alert schema release adding host/redshift fields would change ATAT, ORACLE and ParSNIP rows",
    "definition_widened": False,
    "completeness": "One of seven P3 axes. Counts are structural (format and weights), not functional: no channel was executed (I5 out of scope). Rows whose training provenance rests on README/code only are listed in tool_inventory_slot.json completeness.",
}

with open(os.path.join(OUT, "tool_inventory_slot.json"), "w") as f:
    json.dump(slot, f, indent=1)
with open(os.path.join(OUT, "tool_coverage_axis.json"), "w") as f:
    json.dump(cov, f, indent=1)
print(json.dumps(summary, indent=1))
