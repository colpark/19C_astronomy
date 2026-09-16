#!/usr/bin/env python3
"""PLANNING-ONLY. NOT A P7 RECORD.

The real sigma_d needs the two I1 mechanical compositions scored per item (graph edge I1 -> P7).
They do not exist. This script builds SYNTHETIC paired score columns whose paired-difference
standard deviation equals a bracketed sigma_d exactly, runs the vendored
fm-advantage-benchmark/scripts/power.py on each, and tabulates MDE against cohort size so a human
can see at which N an MDE below a candidate delta becomes possible.

    python planning_mde_bracket.py   (writes ../planning_mde_bracket.csv and ../out/planning_power_runs/)

Bracket derivation (computed below, not typed):
  Family A, unit = one round (night), score = precision at k over the k committed objects.
    per-composition sd of a binomial precision: s(p) = sqrt(p(1-p)/k), k = 8 (k_slot.json).
    paired sd: sigma_d = sqrt(2 s^2 (1 - rho)).
    p spans 0.930 (BTSbot bts_p2 purity, arXiv:2401.15167 Table 6) to 0.5 (maximum binomial variance,
    which any p interval containing 0.5 attains; the chance level 327/1903 = 0.172 lies below it).
    rho spans 0.9 to 0.0. No seed reports a correlation between two compositions; the span is chosen
    to cover near-identical to independent compositions and is not a measurement.
  Family B, unit = one distinct object, score = 1 if the object's commit/no-commit decision is correct.
    paired difference d in {-1,0,+1}; with symmetric discordance q and zero mean, sigma_d = sqrt(q).
    q spans 0.02 to 0.50, again a coverage span, not a measurement.
Candidate deltas (delta_slot.json): 0.018 (DERIVED candidate), 0.037 (refused, unequal denominators),
0.30 (population FAIL, alerts), 0.37 (adjacent referent). N_min is reported at each for planning.
"""
import csv, json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
POWER = os.path.abspath(os.path.join(ROOT, "..", "..", "fm-advantage-benchmark", "scripts", "power.py"))
RUNS = os.path.join(ROOT, "out", "planning_power_runs")
OUTCSV = os.path.join(ROOT, "planning_mde_bracket.csv")
K, CANDIDATES_PER_ROUND = 8, round(1903 / 41, 2)   # k_slot.json: 327/41 = 7.98 -> 8; 1903/41 = 46.41
DELTAS = [0.018, 0.037, 0.30, 0.37]
NS = [50, 150, 500, 2000]

def s_binom(p, k=K):
    return math.sqrt(p * (1 - p) / k)

def family_a_sigmas():
    lo = math.sqrt(2 * s_binom(0.930) ** 2 * (1 - 0.9))
    a2 = math.sqrt(2 * s_binom(0.930) ** 2 * (1 - 0.0))
    a3 = math.sqrt(2 * s_binom(0.5) ** 2 * (1 - 0.5))
    hi = math.sqrt(2 * s_binom(0.5) ** 2 * (1 - 0.0))
    return [("A", "round (night); precision@8", "p=0.930;rho=0.9", lo),
            ("A", "round (night); precision@8", "p=0.930;rho=0.0", a2),
            ("A", "round (night); precision@8", "p=0.5;rho=0.5", a3),
            ("A", "round (night); precision@8", "p=0.5;rho=0.0", hi)]

def family_b_sigmas():
    return [("B", "distinct object; binary decision correctness", f"q={q}", math.sqrt(q))
            for q in (0.02, 0.10, 0.25, 0.50)]

def synth_continuous(n, sigma):
    # deterministic paired columns whose differences have sample sd exactly sigma, mean 0
    z = [math.sin(1.7 * i + 0.3) + math.cos(0.37 * i * i) for i in range(n)]
    m = sum(z) / n
    z = [x - m for x in z]
    sd = math.sqrt(sum(x * x for x in z) / (n - 1))
    d = [sigma * x / sd for x in z]
    return [0.5 + x / 2 for x in d], [0.5 - x / 2 for x in d]

def synth_binary(n, q):
    # discordant pairs split evenly between +1 and -1, concordant pairs 0; sample sd = sqrt(q*n/(n-1))
    nd = 2 * int(math.floor(q * n / 2 + 0.5))
    if nd == 0: nd = 2  # smallest symmetric discordance realisable; flagged via realised q
    d = [1] * (nd // 2) + [-1] * (nd // 2) + [0] * (n - nd)
    a = [1 if x == 1 else 0 for x in d]
    b = [1 if x == -1 else 0 for x in d]
    return a, b

def run_power(path, delta):
    r = subprocess.run([sys.executable, POWER, "--scores", path, "--col-a", "composition_a_SYNTHETIC",
                        "--col-b", "composition_b_SYNTHETIC", "--k", str(K),
                        "--candidates-per-item", str(CANDIDATES_PER_ROUND), "--delta", str(delta)],
                       capture_output=True, text=True)
    if r.returncode not in (0, 2):
        raise SystemExit(f"power.py failed: {r.stderr}")
    return json.loads(r.stdout.split("\n\nCLOSE")[0])

def main():
    os.makedirs(RUNS, exist_ok=True)
    rows = []
    for fam, unit, basis, sigma in family_a_sigmas() + family_b_sigmas():
        for n in NS:
            if fam == "A":
                a, b = synth_continuous(n, sigma)
            else:
                a, b = synth_binary(n, sigma ** 2)
            tag = f"{fam}_{basis.replace('=', '').replace(';', '_')}_N{n}"
            path = os.path.join(RUNS, f"SYNTHETIC_{tag}.csv")
            with open(path, "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["item_SYNTHETIC", "composition_a_SYNTHETIC", "composition_b_SYNTHETIC"])
                for i, (x, y) in enumerate(zip(a, b)):
                    w.writerow([f"synthetic_{i}", f"{x:.10f}", f"{y:.10f}"])
            recs = {dl: run_power(path, dl) for dl in DELTAS}
            base = recs[DELTAS[0]]
            json.dump({"label": "PLANNING-ONLY / SYNTHETIC / NOT A P7 RECORD", "runs": recs},
                      open(os.path.join(RUNS, f"SYNTHETIC_{tag}.json"), "w"), indent=2)
            row = {"label": "PLANNING-ONLY / not a P7 record", "family": fam, "unit": unit,
                   "sigma_d_basis": basis, "sigma_d_target": round(sigma, 4),
                   "sigma_d_realised_by_power_py": base["sigma_d"],
                   "discordance_q_realised": (round(sum(1 for x, y in zip(a, b) if x != y) / n, 4) if fam == "B" else ""),
                   "N_units": n,
                   "nights_equivalent": n if fam == "A" else round(n / CANDIDATES_PER_ROUND, 1),
                   "MDE_alpha0.05_power0.80": base["mde"], "chance_k_over_candidates": base["chance"]}
            for dl in DELTAS:
                row[f"N_min_at_delta_{dl}"] = recs[dl]["n_min"]
                row[f"MDE_below_delta_{dl}"] = "yes" if base["mde"] < dl else "no"
            rows.append(row)
    with open(OUTCSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(open(OUTCSV).read())

if __name__ == "__main__":
    main()
