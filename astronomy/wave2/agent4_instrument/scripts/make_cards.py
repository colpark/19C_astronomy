"""Tool cards written from code (I3). calibration only, contamination FAIL on this cohort.
PRE-I1: graph edge R1->I1 unmet, escalated."""
import glob, json, os
from common import W, sha256, BANNER

OUT = os.path.join(W, "tool_cards")
SRC = "astronomy/wave2/agent4_instrument/sources/"
os.makedirs(OUT, exist_ok=True)
flog = json.load(open(os.path.join(W, "data_cache", "features", "features_log.json")))
af = flog["alive_fraction"]


def dump(name, card):
    card["banner"] = BANNER
    json.dump(card, open(os.path.join(OUT, f"tool_card_{name}.json"), "w"), indent=1)


dump("Fink_EarlySNIa_sigmoid_features", {
    "name": "Fink EarlySNIa sigmoid feature extractor (actsnfink get_sigmoid_features_dev_fast) as called by fink-science ztf/random_forest_snia",
    "role": "encoder",
    "written_from": "code",
    "new_card": True,
    "code_pin": "github.com/emilleishida/fink_sn_activelearning commit f424ab1fc5024a49364d41090d1c3c2b8cb733cd (actsnfink/classifier_sigmoid.py, sigmoid.py); caller fink-science 591e75ce ztf/random_forest_snia/processor.py; flux conversion fink_utils 0.77.0 wheel sha256 bfdef56938f90ed40902d58df549b127c89ee02a3b84d8783b2b9a504861c27a",
    "quantity_returned": "12 floats, [a, b, c, snratio, mse, nrise] for g then r (RF_FEATURE_NAMES, classifier_sigmoid.py:36). Per band: intraday points averaged on rounded JD; points with FLUXCAL <= -10 masked; if at least min_data_points=4 remain and every averaged point is non-decreasing by the ewma(3) derivative, a sigmoid c/(1+exp(-a(t-b))) is fit by scipy least_squares (sigmoid.py::fit_sigmoid) and snratio (mean flux/err), mse of normalised fluxes, nrise are returned; otherwise the fake values [0,0,0,0.1,1e8,0].",
    "defining_paper": "Leoni et al. 2022, A&A 663, A13 (arXiv:2111.11438), not read in this wave; card is from code only",
    "accuracy_against_scored_measurement": f"Not a scored quantity itself. Measured coverage on this cohort (3,432 BTS units, 2019-06-01..2021-04-15): alive fraction {af['E1']['C1']:.4f} at first alert (E1) and {af['E3']['C1']:.4f} at night 3 (E3). Contribution to precision@8 and AUC is in i2_channels.json (PRE-I1 CALIBRATION).",
    "what_it_is_not": "Not the Fink RF probability: the RF weights default-model_sigmoid-1.7.2.obj (sha256 77f0a463..., pruned in wave-1 code/) are not used; only the feature vector enters the calibration GBDT. Not defined at first alert: needs >=4 averaged points in a band, all rising.",
    "conventions": [
        "flux = 10^(-0.4 magpsf) * 1e11 (ZP 27.5 FLUXCAL) with err 9.21034e10 exp(-0.921034 m) sigma (fink_utils conversion.py:41-42)",
        "isdiffpos is ignored: negative-subtraction detections enter as positive flux (fink_utils data/utils.py::format_data_as_snana)",
        "time axis is JD (Fink passes jd as MJD) rounded with np.around to integer days, so intraday averaging groups on JD integer boundaries at 12:00 UTC",
        "min_rising_points=2, min_data_points=4, rising_criteria='ewma', ewma_window=3 (processor.py call site)",
        "fake-fit sentinel [0,0,0,0.1,1e8,0] is indistinguishable from a genuine zero-amplitude fit to a GBDT",
    ],
    "served_checkpoint": {"identifier": "feature extractor code only; no weights served in this composition",
                          "pin": "actsnfink commit f424ab1fc5024a49364d41090d1c3c2b8cb733cd"},
    "substitution": {"what": "Fink RF classifier replaced by a GBDT fit on BTS training folds over the same 12 features (approved Fink RF remapping, D5 amendment)",
                     "justified_against": "scored measurement (posB precision@8), not against the Fink RF",
                     "disclosed": True},
    "disagreements": [
        {"topic": "minimum points", "comment": "processor.py:64 '# Flag alerts with less than 3 points in total'", "code": "apply_selection_cuts_ztf default minpoints=4 (processor.py:41) and min_data_points=4"},
        {"topic": "feature names", "docstring": "extract_features_rf_snia docstring lists 'a_g,b_g,c_g,snratio_g,chisq_g,nrise_g' (processor.py:234)", "code": "RF_FEATURE_NAMES uses mse_g/mse_r and compute_mse is a mean squared error, not a chi-square"},
        {"topic": "rising points", "comment": "classifier_sigmoid.py:548 '# at least three points (needed for the sigmoid fit)'", "code": "min_rising_points=2 at the Fink call site"},
        {"topic": "negative subtractions", "expected": "difference flux sign follows isdiffpos", "code": "format_data_as_snana converts magpsf to positive FLUXCAL regardless of isdiffpos"},
        {"topic": "rubin vs ztf", "code": "fink-science also ships rubin/random_forest_snia; the ZTF path was used here and the Rubin path was not read in this wave"},
    ],
    "completeness": "Covered from code: actsnfink classifier_sigmoid.py and sigmoid.py in full; fink-science ztf/random_forest_snia/processor.py in full; fink_utils conversion.py and data/utils.py in full. Not covered: the paper, the RF weights, actsnfink rainbow.py, the Rubin processor.",
})
dump("Fink_fast_transient_rate", {
    "name": "Fink fast transient rate (fink-science ztf/fast_transient_rate)",
    "role": "encoder",
    "written_from": "code",
    "new_card": True,
    "code_pin": "fink-science commit 591e75ce5ec798355eeeecfd936ef2582a0745fe, ztf/fast_transient_rate/processor.py::get_last_alert, fast_transient_rate; utils.py",
    "quantity_returned": "Per alert: mag_rate (mag/day) between the current detection and the most recent previous measurement in the same band (a detection, or an upper limit when the previous record in that band is a non-detection), with sigma, 5th and 95th percentiles from N Monte-Carlo samples, delta_time, from_upper; plus jd_first_real_det and jdstarthist_dt.",
    "defining_paper": "none located; card from code only",
    "accuracy_against_scored_measurement": f"Not a scored quantity. Alive (finite mag_rate) fraction on this cohort: {af['E1']['C2']:.4f} at E1, {af['E3']['C2']:.4f} at E3.",
    "what_it_is_not": "Not a classifier. Not a light-curve fit. jdstarthist_dt was not computed here because ALeRCE light curves carry no jdstarthist field.",
    "conventions": [
        "flux = 10^(0.4(27.5 - mag)) (utils.py::to_flux)",
        "upper-limit case samples current flux against Uniform(0, flux(limit))",
        "samples are shifted by +|min| of the whole sample matrix before log (processor.py 'Fix distribution')",
        "a previous record in a band other than g/r stops the search and returns NaN (the 'TODO: change the logic for LSST' branch)",
        "N=100, seed 0 in this calibration run",
    ],
    "served_checkpoint": {"identifier": "code only, no weights", "pin": "fink-science commit 591e75ce5ec798355eeeecfd936ef2582a0745fe"},
    "substitution": {"what": "logic copied into scripts/features.py and run one unit per batch without pyspark", "disclosed": True},
    "disagreements": [
        {"topic": "batch dependence", "code": "the positivity shift uses np.min over current_mag_sample[:, idx_valid_data] for the whole DataFrame, so one alert's rate depends on which other alerts share the Spark partition", "this_run": "one unit per batch, so the shift is per unit; Fink production values would differ"},
        {"topic": "first 5-sigma time", "docstring": "jd_first_real_det is 'first variation time at 5 sigma contains in the alert history'", "code": "get_last_alert takes cjd at the first non-NaN cmagpsf in the history arrays; no significance test is applied inside the function"},
        {"topic": "shift distorts the rate", "code": "current_mag_sample += np.abs(np.min(...)) is applied unconditionally (also when every sample is positive), adding a constant to both fluxes of the ratio, so mag_rate is not the rate between the measured fluxes"},
    ],
    "completeness": "Covered from code: processor.py and utils.py in full. Not covered: notebook/, the Spark wrapper beyond the call signature, any paper.",
})

dump("Fink_SLSN_features", {
    "name": "Fink superluminous-SN feature extractor (fink-science ztf/superluminous extract_features)",
    "role": "encoder",
    "written_from": "code",
    "new_card": True,
    "code_pin": "fink-science commit 591e75ce5ec798355eeeecfd936ef2582a0745fe, ztf/superluminous/{kernel,slsn_classifier,processor}.py; SALT2 served by sncosmo 2.13.1 'salt2' = version T23 (cache dir salt2-k21-frag, salt2_template_0.dat sha256 bf9aefb263972179204c3b7d28b5ae0c993aa090925b92deee278b8d115f1d70); SFD maps sha256 50b6aaad...(ngp), 84891a59...(sgp)",
    "quantity_returned": "35 columns: distnr, ra, dec, ebv, duration, 9 light_curve statistics, 7 Rainbow (sigmoid temperature, Bazin bolometric) parameters and their S/N, Rainbow chi2, SALT2 (z,t0,x0,x1,c) with z bounded to (0,0.5) and chi2. Fits run only if every g/r band has >=3 points, total points > 7 and duration > 30 d; otherwise fit columns are NaN and the classifier returns -1.",
    "defining_paper": "Russeil et al. 2024 (Rainbow) cited in code docstring; not read in this wave",
    "accuracy_against_scored_measurement": f"Not a scored quantity. Gate-pass fraction on this cohort: {af['E1']['C3']:.4f} at E1 (dead), {af['E3']['C3']:.4f} at E3 (2 of 3,432 units).",
    "what_it_is_not": "Not an early-time tool: the gate (duration > 30 d) and processor.py (jd - jdstarthist >= 30) exclude first-alert and night-3 epochs by construction. Not redshift-free in production: processor.py applies an SDSS photo-z absolute-magnitude veto after classification (not used here).",
    "conventions": [
        "flux via fink_utils mag2fluxcal_snana (ZP 27.5) but fit_salt declares zp=25.0 for the same fluxes",
        "SALT fit uses sncosmo source 'salt2' with no version pinned, so the served model depends on the installed sncosmo (T23 here)",
        "SALT redshift is a free fit parameter bounded (0, 0.5), not an input",
        "band effective wavelengths g 4770 A, r 6231 A (kernel.py)",
        "enough_total_points = len(cjd) > min_points_total (strict), so 8 points are needed although kernel.py names the threshold 7",
    ],
    "served_checkpoint": {"identifier": "feature extractor code; classifier weights data/models/xgboost_3.4.1/superluminous_classifier.joblib not used", "pin": "fink-science commit 591e75ce5ec798355eeeecfd936ef2582a0745fe"},
    "substitution": {"what": "xgboost SLSN classifier replaced by the calibration GBDT over the same feature vector; functions copied into scripts/features.py", "disclosed": True},
    "disagreements": [
        {"topic": "zeropoint", "code": "compute_flux uses FLUXCAL at ZP 27.5 while fit_salt sets zp=25.0 for those fluxes, so SALT x0 is scaled by 10^(0.4*2.5)=10 relative to the declared zeropoint"},
        {"topic": "unsorted magnitudes", "code": "fit_rainbow sorts cjd, cflux, csigflux and cfid in place but not cmagpsf; statistical_features then indexes cmagpsf with the sorted cfid, so peak_mag_g/peak_mag_r can take magnitudes from the wrong band or epoch (replicated as-is in this run)"},
        {"topic": "threshold naming", "code": "kernel.min_points_total = 7 but the test is '>' 7"},
        {"topic": "model version", "code": "sncosmo.Model(source='salt2') unpinned; doctest values in slsn_classifier.py were produced with an unrecorded SALT2 version; this run served T23"},
        {"topic": "README vs disk (wave 1)", "code": "wave-1 found SLSN_rainbow_MD.joblib referenced but missing; the served classifier is xgboost_3.4.1/superluminous_classifier.joblib"},
    ],
    "completeness": "Covered from code: kernel.py, slsn_classifier.py and processor.py in full. Not covered: light_curve RainbowFit internals, the xgboost model, the Rainbow paper.",
})

# ParSNIP: update the wave-1 card (read-only source) with wave-2 code findings and the per-fold served models
w1 = json.load(open("/home/aid1/Documents/4_19C_astronomy/repo/astronomy/agent4_tools_instrument/tool_cards/tool_card_ParSNIP.json"))
card = dict(w1)
card["updated_in_wave2"] = True
card["code_pin"] = w1["code_pin"] + "; wave-2 copy at astronomy/wave2/agent4_instrument/code/kboone_parsnip_dcea62f (unmodified)"
pts = sorted(glob.glob(os.path.join(W, "compositions", "parsnip_fold*.pt")))
logs = {}
for p in sorted(glob.glob(os.path.join(W, "compositions", "parsnip_fold*_log.json"))):
    logs[os.path.basename(p)] = json.load(open(p))
card["served_checkpoint"] = {
    "identifier": "per-fold ParSNIP models trained from scratch on ztfg/ztfr for this calibration (compositions/parsnip_fold{0..4}.pt); shipped plasticc.pt, plasticc_photoz.pt, ps1.pt NOT mounted (no ZTF bands; I4 refusal)",
    "pin": "; ".join(f"{os.path.basename(p)} sha256 {sha256(p)}" for p in pts) or "UNDEMONSTRATED: no fold model file present",
    "matches_adjudicating_composition": True,
}
card["training_record"] = {k: {x: v.get(x) for x in ("epochs_run", "train_seconds", "n_train_lcs", "finite_fraction_E1", "finite_fraction_E3", "weights_finite")} for k, v in logs.items()}
card["conventions"] = w1["conventions"] + [
    "wave 2 settings: predict_redshift=True, input_redshift=True with constant hostgal_photoz=0, hostgal_photoz_err=1e3, hostgal_specz=NaN (AMENDMENTS.md A-1); learning_rate=1e-4 (A-2); max_epochs=60",
    "ZTF bands: MW extinction correction on, background correction off (instruments.py band_info 'ztfg','ztfr')",
    "flux from ZTF magpsf at ZP 25 AB with sign from isdiffpos (scripts/features.py::parsnip_lc)",
]
card["disagreements"] = w1["disagreements"] + [
    {"topic": "input_redshift=False path", "settings": "settings.py exposes input_redshift as a boolean (build_default_argparse adds --no_input_redshift)", "code": "_get_data (parsnip.py ~L620-630) assigns extra_input_data only inside 'if input_redshift', so input_redshift=False raises UnboundLocalError; found wave 2"},
    {"topic": "empty light curves under augmentation", "comment": "augment_light_curves/_compute_amplitude: 'can very rarely end up with no light curve points. Handle that gracefully'", "code": "on single-detection first-alert light curves augmentation empties the light curve, and nll = 0.5*weight*(flux - model_flux*amplitude)^2 becomes 0*inf = NaN at the default learning rate (step 2, fold 0); 'very rarely' does not hold for alert-epoch inputs"},
    {"topic": "numerical stability at defaults", "code": "at learning_rate 1e-3 without augmentation, amplitude_logvar reached -inf and the spectral penalty diff/(sum) was 0/0 at step 30; stable at 1e-4 over 1,075 steps"},
    {"topic": "photo-z mode metadata", "comment": "_get_data: 'this uses the keys for PLAsTiCC and should be adapted'", "code": "predict_redshift requires hostgal_specz, hostgal_photoz and hostgal_photoz_err in meta; a ZTF alert has none of them"},
]
card["what_it_is_not"] = w1["what_it_is_not"] + " Wave 2: a ZTF-band ParSNIP exists only as the per-fold calibration models trained here; they are not a released checkpoint."
card["accuracy_against_scored_measurement"] = "PRE-I1 CALIBRATION only: see i2_channels.json (C5-only and C vs C-1) on the BTS 2019-06-01..2021-04-15 cohort, which failed contamination. No claim."
card["completeness"] = w1["completeness"] + " Wave 2 added: training executed (5 folds), augment_light_curves and loss_function read in full; plotting.py and scripts still not covered."
dump("ParSNIP", card)
print("cards written", sorted(os.listdir(OUT)))
