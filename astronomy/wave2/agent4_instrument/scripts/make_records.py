"""Assemble i2_channels.json, power_calibration.json, provenance_records.json, HASH_MANIFEST.sha256.
calibration only, contamination FAIL on this cohort. PRE-I1: graph edge R1->I1 unmet, escalated."""
import glob, json, os
from common import W, sha256, BANNER, FROZEN_SHA

sr = json.load(open(os.path.join(W, "data_cache", "score_results.json")))
pw = json.load(open(os.path.join(W, "data_cache", "power", "power_runs_raw.json")))
fl = json.load(open(os.path.join(W, "data_cache", "features", "features_log.json")))
cl = json.load(open(os.path.join(W, "compositions", "compose_log.json")))
plogs = {os.path.basename(p): json.load(open(p)) for p in sorted(glob.glob(os.path.join(W, "compositions", "parsnip_fold*_log.json")))}
PRE = "PRE-I1 CALIBRATION"
SRC = "astronomy/wave2/agent4_instrument/"

# ---------- I2
i2 = {"label": PRE, "banner": BANNER, "stage": "I2", "frozen_sha256": FROZEN_SHA,
      "amendments": ["A-1 ParSNIP input_redshift", "A-2 ParSNIP learning_rate 1e-4"],
      "channels": {"C1": "Fink EarlySNIa sigmoid features (classical)", "C2": "Fink fast transient rate (classical)",
                   "C3": "Fink SLSN feature vector (classical)", "C4": "ZTF alert candidate photometry + galactic b (classical, not Fink)",
                   "C5": "ParSNIP latent, trained per fold, no redshift (deep)"},
      "C": ["C1", "C2", "C3", "C4", "C5"], "C_minus_1": ["C1", "C2", "C3", "C4"],
      "parsnip_training": {k: {x: v.get(x) for x in ("epochs_run", "train_seconds", "finite_fraction_E1", "finite_fraction_E3", "weights_finite")} for k, v in plogs.items()},
      "gpu_hours_total": round(sum(v["train_seconds"] for v in plogs.values()) / 3600, 3),
      "epochs": {}}
for e in ("E1", "E3"):
    ep = sr["epochs"][e]
    alive = dict(fl["alive_fraction"][e])
    c5f = [v.get(f"finite_fraction_{e}") for v in plogs.values()]
    alive["C5"] = min(c5f) if c5f and None not in c5f else None
    dead = {k: (v == 0) for k, v in alive.items() if v is not None}
    auc = ep["auc"]
    pN, pR = ep["precision_at_8"]["N"], ep["precision_at_8"]["R"]
    configs = {}
    for c in ["C", "C-1", "C-minus-C1", "C-minus-C2", "C-minus-C3", "C-minus-C4", "C5-only"]:
        configs[c] = {"auc_posB": auc[c]["auc_posB"], "auc_posB_ci95": auc[c].get("auc_posB_ci95"),
                      "auc_SNIa_descriptive": auc[c].get("auc_SNIa_descriptive"),
                      "mean_prec8_night_items": pN[f"mean_prec_{c}"], "mean_prec8_round46_items": pR[f"mean_prec_{c}"]}
    loo = {f"C{i}": {"delta_auc_C_minus_without": auc["C"]["auc_posB"] - auc[f"C-minus-C{i}"]["auc_posB"],
                     "delta_prec8_round46": pR["mean_prec_C"] - pR[f"mean_prec_C-minus-C{i}"]} for i in range(1, 5)}
    loo["C5"] = {"delta_auc_C_minus_without": auc["C"]["auc_posB"] - auc["C-1"]["auc_posB"],
                 "delta_prec8_round46": pR["mean_prec_C"] - pR["mean_prec_C-1"],
                 "delta_prec8_night": pN["mean_prec_C"] - pN["mean_prec_C-1"]}
    i2["epochs"][e] = {
        "measured_C_minus_1": {"auc_posB": auc["C-1"]["auc_posB"], "auc_ci95": auc["C-1"]["auc_posB_ci95"],
                               "prec8_night": pN["mean_prec_C-1"], "prec8_round46": pR["mean_prec_C-1"]},
        "measured_C": {"auc_posB": auc["C"]["auc_posB"], "auc_ci95": auc["C"]["auc_posB_ci95"],
                       "prec8_night": pN["mean_prec_C"], "prec8_round46": pR["mean_prec_C"]},
        "chance": {"auc": 0.5, "prec8_stated_manifest": 0.172, "prec8_measured_mean_night_items": pN["mean_chance_measured"],
                   "prec8_measured_mean_round46_items": pR["mean_chance_measured"], "prevalence_posB_scored_pool": ep["prevalence_posB"]},
        "alive_fraction": alive, "dead": dead,
        "honest_channel_count": {"sum_alive_fractions_all": round(sum(v for v in alive.values() if v is not None), 4),
                                 "classical_C1_C4": round(sum(alive[k] for k in ("C1", "C2", "C3", "C4")), 4),
                                 "deep_C5": alive["C5"]},
        "leave_one_out": loo, "configs": configs,
        "permutation_control": ep["permutation_control"],
        "permutation_auc": {p: auc[p + "__perm"]["auc_posB"] for p in ("C", "C-1")},
        "items": {"night": {k: pN[k] for k in ("n_items", "n_items_k_binding")},
                  "round46": {"n_items": pR["n_items"], "partial_units_dropped": ep["round_items_dropped_partial_units"]}},
        "pool": {k: ep[k] for k in ("n_units", "n_scored_pool", "n_posB", "coverage", "n_far_from_peak_in_pool")},
    }
i2["completeness"] = ("C-1 and C measured at both declared epochs (E1 first alert, E3 night 3) over the 1-arcsec units of the frozen "
                      "cohort, with leave-one-out for every channel, C5 alone, alive fractions and a label-permutation control. "
                      "Not covered: ATAT (not built), pretrained ParSNIP checkpoints (not mounted, I4), Rubin inputs, any agent arm.")
json.dump(i2, open(os.path.join(W, "i2_channels.json"), "w"), indent=1)

# ---------- power (primary E1 night items)
prim = pw["runs"]["E1_N"]
powrec = {"label": "PRE-I1 CALIBRATION, not a P7 record", "banner": BANNER,
          "claim": "none. BTS cohort failed contamination (addition B); R1 not run; compositions are not I1 records",
          "primary_run": "E1_N (first alert, one item per decision night, stratum k_binding)"}
for k in ("k", "candidates_per_item", "chance", "delta", "alpha", "power"):
    powrec[k] = prim[k]
bs = prim["strata"]["True"]
powrec["primary_reading"] = "k_binding=True stratum of E1_N as emitted by power.py --stratum (equal denominator k_eff=8)"
for k in ("n", "mean_paired_difference", "sigma_d", "mde", "n_min"):
    powrec[k] = bs[k]
powrec["ruling"] = "RESOLVABLE" if bs["mde"] <= prim["delta"] else "CLOSE_UNRESOLVABLE"
powrec["strata"] = prim["strata"]
powrec["pooled_E1_N_refused"] = {"power_py_ruling": prim["ruling"], "mde": prim["mde"], "n": prim["n"],
    "refusal": "global refusal 4: the pooled night record averages precision at k_eff from 1 to 8 (unequal denominators); 518 of 579 nights have n<=8 and a paired difference of 0 by construction, which drives sigma_d and MDE toward 0"}
powrec["items_filtered_on_outcome"] = False
powrec["runs"] = pw["runs"]
powrec["chance_measured_beside_stated"] = {e: {it: sr["epochs"][e]["precision_at_8"][it]["mean_chance_measured"] for it in ("N", "R")} for e in ("E1", "E3")}
powrec["warnings"] = [
    "chance printed by power.py is k/candidates_per_item = 8/46.41 from the manifest; the measured per-item chance on this saved-sources file differs and is listed beside it",
    "night items with n <= 8 have identical precision under both compositions by construction (k not binding); they are kept and stratified (never filtered); the pooled night ruling is refused (unequal denominators) and the record reads the k_binding=True stratum",
    "power.py computes the difference as col-a minus col-b = classical minus instrument",
]
powrec["completeness"] = ("power.py (unchanged) run on paired precision@8 for 4 item sets: E1/E3 x night/round-46, over the scored pool of the frozen "
                          "cohort; label PRE-I1 CALIBRATION. Not covered: Rubin items, contamination-free items, agent arms, any P7 ruling.")
json.dump(powrec, open(os.path.join(W, "power_calibration.json"), "w"), indent=1)

# ---------- provenance records for decision-relevant numbers
recs = []
def rec(i, v, ref, src, pop, adj, fal):
    recs.append({"id": i, "value": v, "referent": ref, "source": src, "population": pop, "adjudicator": adj, "falsifier": fal, "label": PRE})
for e in ("E1", "E3"):
    x = i2["epochs"][e]
    pop = f"{x['pool']['n_scored_pool']} labelled 1-arcsec units (posA or neg) of the frozen cohort, out-of-fold, epoch {e}"
    rec(f"a4w2-{e}-auc-C-1", x["measured_C_minus_1"]["auc_posB"], f"per-object ROC AUC for posB, classical composition C-1 at {e}",
        SRC + "scripts/score.py::main auc over compositions/predictions/pred_%s_C-1.csv (MANIFEST.sha256)" % e, pop,
        "chance 0.5; label-permutation AUC in i2_channels.json", "a rerun of compose.py+score.py from the hashed features that returns an AUC outside the bootstrap CI, or a permutation AUC outside [0.45,0.55]")
    rec(f"a4w2-{e}-auc-C", x["measured_C"]["auc_posB"], f"per-object ROC AUC for posB, instrument composition C (C-1 plus ParSNIP) at {e}",
        SRC + "scripts/score.py::main auc over compositions/predictions/pred_%s_C.csv (MANIFEST.sha256)" % e, pop,
        "classical composition C-1 on the same units, paired", "a rerun with the hashed ParSNIP fold models that differs beyond the bootstrap CI, or permutation AUC outside [0.45,0.55]")
    rec(f"a4w2-{e}-prec8-round46-delta", x["leave_one_out"]["C5"]["delta_prec8_round46"], f"mean paired precision@8 difference C minus C-1 over 46-candidate rounds at {e}",
        SRC + "scripts/score.py::prec_at_k; paired_scores.csv", f"{x['items']['round46']['n_items']} rounds of 46 scored units",
        "stated chance 0.172 and measured per-round chance in i2_channels.json", "a rerun that changes the sign, or a permutation of round membership that leaves it unchanged")
    rec(f"a4w2-{e}-honest-channel-count", x["honest_channel_count"]["sum_alive_fractions_all"], f"sum over C1..C5 of the fraction of units where each channel emits a non-default value at {e}",
        SRC + "scripts/features.py::main alive counts and compositions/parsnip_fold*_log.json finite fractions", f"{x['pool']['n_units']} units (all cohort units, labelled or not)",
        "nominal channel count 5", "recomputing alive flags from data_cache/features/features_%s.csv that returns a different sum" % e)
for k, v in pw["runs"].items():
    if "sigma_d" in v:
        rec(f"a4w2-power-{k}-sigma_d", v["sigma_d"], f"sd of per-item paired precision@8 difference (classical minus instrument), item set {k}",
            "fm-advantage-benchmark/scripts/power.py unchanged on data_cache/power/paired_%s.csv sha256 %s" % (k, v.get("scores_file_sha256")),
            f"{v.get('n')} items", "agent5 planning bracket 0.040-0.250 (planning_mde_bracket.csv)",
            "a rerun of power.py on the same file that returns a different sigma_d, or a contamination-free cohort whose sigma_d falls outside this value's bootstrap range")
json.dump(recs, open(os.path.join(W, "provenance_records.json"), "w"), indent=1)

# ---------- top-level hash manifest
files = (["r1_spec.md", "compositions_FROZEN.md", "AMENDMENTS.md", "paired_scores.csv", "i2_channels.json", "power_calibration.json",
          "provenance_records.json", "seed_ledger.json", "replay_cases.csv", "replay_rulings.csv", "compositions/MANIFEST.sha256",
          "data_cache/ALERCE_RAW_SHA256SUMS", "data_cache/FEATURES_SHA256SUMS", "data_cache/DUSTMAPS_SHA256SUMS", "data_cache/fetch_log.json",
          "data_cache/score_results.json", "data_cache/power/power_runs_raw.json", "sources/SHA256SUMS"]
         + sorted(os.path.relpath(p, W) for p in glob.glob(os.path.join(W, "scripts", "*.py")))
         + sorted(os.path.relpath(p, W) for p in glob.glob(os.path.join(W, "tool_cards", "*.json"))))
lines = [f"{sha256(os.path.join(W, f))}  {f}" for f in files if os.path.exists(os.path.join(W, f))]
open(os.path.join(W, "HASH_MANIFEST.sha256"), "w").write(f"# {BANNER}\n" + "\n".join(lines) + "\n")
print("records", len(recs), "manifest", len(lines))
