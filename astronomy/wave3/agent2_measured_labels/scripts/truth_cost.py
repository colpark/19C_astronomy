#!/usr/bin/env python3
"""Protocol sec 10: price the gap. Every (delta, N, p, s, c) combination; L offsets from supply_P_per_month.json if present."""
import json, math, csv, pathlib, itertools, hashlib
D = pathlib.Path(__file__).resolve().parent.parent
assert hashlib.sha256((D/"census_protocol_FROZEN.md").read_bytes()).hexdigest() == "9fac85524f28b5e3874a0d43a2c089915d20814b7996c18a0c77cc230b3c95fb"
reach = json.load(open(D/"out/reachability.json"))
sup = json.load(open(D/"supply_P_per_month.json")) if (D/"supply_P_per_month.json").exists() else {}
L_meas = sup.get("cohort_measured_nonbot_labels_T1_strong", 0) or 0
L_exist = sup.get("cohort_classified_existence_T8_T9_moderate", 0) or 0
S2 = "arXiv:2401.15167 raw.txt (astronomy/wave2/agent2_label_source/sources/2401.15167.raw.txt)"
P_GRID = [(0.81, f"{S2} lines 1443,1465 (BTSbot bts_p1 present-day)"), (0.846, f"{S2} lines 1134,1170 (bts_p1 test)"),
          (0.92, f"{S2} lines 1443,1466 (bts_p2 present-day)"), (0.93, f"{S2} lines 1134,1169 (bts_p2 test)"),
          (0.956, f"{S2} line 1243 (scanner triggering, restated)"), (0.967, f"{S2} lines 1148-1149 (scanner triggering, 316/327)")]
S_GRID = [(0.93, "arXiv:2009.01242 raw lines 854-855 (93% of m<18.5 events classified)"), (1.0, "optimistic bound")]
C_GRID = [(4.5, f"{S2} line 1494 (BTSbot median bts_p1 sources per night)"), (8, "wave-1 slot k=8 per night (astronomy/agent5_resolution_replay, arXiv:2401.15167)"),
          (10, "arXiv:1910.12973 raw line 139 ('> 10 SNe in the 18.5-19 magnitude range every night')")]
N_GRID = [(0.018, 485, "frozen bands min N_min (agent1 planning_mde_bracket_w3.csv family B)"), (0.018, 12855, "frozen PROCEED (max N_min)"),
          (0.05, 63, "PI delta override min N_min"), (0.05, 1666, "PI delta override max N_min")]
A = reach["A_per_night"]["10"]["point"]; A_lo = reach["A_per_night"]["10"]["cp95_lo"]
rows = []
for (delta, N, nsrc), (p, psrc), (s, ssrc), (c, csrc) in itertools.product(N_GRID, P_GRID, S_GRID, C_GRID):
    for Lname, L in (("L=0 (upper cost; measured cohort labels UNDEMONSTRATED or 0)", 0), ("L=T1 measured non-bot cohort labels", L_meas)):
        Nn = max(0, N - L)
        S = math.ceil(Nn / (p * s)); H = 0.5 * S; W = S - math.ceil(Nn / s)
        per_night = min(c, A_lo)
        nights = math.ceil(S / per_night) if S else 0
        rows.append(dict(delta=delta, N=N, N_source=nsrc, L_case=Lname, L=L, N_need=Nn, purity_p=p, p_source=psrc, success_s=s, s_source=ssrc,
                         capacity_c=c, c_source=csrc, A_reachable_arrivals_per_night_cp95_lo=round(A_lo, 1), binding="capacity" if c <= A_lo else "arrivals",
                         spectra_S=S, P60_hours_H=H, wrong_routine_commitments_W=W, cost_slots=S, rubin_on_sky_nights=nights,
                         missed_rare_penalty="+100 slots per missed rare event (M UNDEMONSTRATED)"))
with open(D/"truth_cost_table.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def pick(delta, N, L0=True):
    r = [x for x in rows if x["delta"] == delta and x["N"] == N and (x["L"] == 0) == L0 or (not L0 and x["delta"] == delta and x["N"] == N and x["L_case"].startswith("L=T1"))]
    return dict(spectra=[min(x["spectra_S"] for x in r), max(x["spectra_S"] for x in r)], hours=[min(x["P60_hours_H"] for x in r), max(x["P60_hours_H"] for x in r)],
                nights=[min(x["rubin_on_sky_nights"] for x in r), max(x["rubin_on_sky_nights"] for x in r)],
                wrong_commitments=[min(x["wrong_routine_commitments_W"] for x in r), max(x["wrong_routine_commitments_W"] for x in r)])
summary = {f"delta_{d}_N_{n}": pick(d, n) for d, n, _ in N_GRID}
out = dict(banner="PLANNING price of measured labels; Rubin cohort; BTS numbers calibration only (contamination FAIL on BTS)",
           protocol_sha256="9fac85524f28b5e3874a0d43a2c089915d20814b7996c18a0c77cc230b3c95fb",
           formula="N_need=max(0,N-L); S=ceil(N_need/(p*s)); H=0.5*S; W=S-ceil(N_need/s); nights=ceil(S/min(c,A)); +100 slots per missed rare event (M UNDEMONSTRATED)",
           reachability=dict(f19=reach["f19"], f185=reach["f185"], A_per_night_10nights=reach["A_per_night"]["10"], A_per_night_9dates=reach["A_per_night"]["9"]),
           L_used=dict(L_measured_T1=L_meas, L_existence_T8_T9_not_used_as_offset=L_exist),
           ranges_over_grid_L0=summary, n_rows=len(rows),
           constraints=["Rubin off sky since 2026-07-14: no new cohort objects; calendar time to reach N UNDEMONSTRATED",
                        "existing cohort objects aged >=60 d since last detection: not credited as reachable today",
                        "P60 (Palomar, +33 deg) vs Rubin (Cerro Pachon, -30 deg) sky overlap fraction UNDEMONSTRATED; not applied (nights are a lower bound)",
                        "f19 counts difference-flux brightness; genuineness of bright cohort objects is carried by purity p, not by f19"])
out["provenance"] = [dict(id=f"w3a2-truthcost-{k}", value=v, referent=f"spectra, P60 hours, Rubin on-sky nights and wrong commitments to reach {k.replace('_', ' ')} correctly labelled positive cohort objects over the declared purity/success/capacity grid, L=0",
    source="astronomy/wave3/agent2_measured_labels/scripts/truth_cost.py (formula in census_protocol_FROZEN.md sec 10, sha256 9fac8552...95fb); out/reachability.json; truth_cost_table.csv",
    population="Rubin cohort (agent-1 O=1,937,669 merged objects, first detection >= 2026-07-01); grids p {0.81..0.967}, s {0.93,1.0}, c {4.5,8,10}",
    adjudicator="a dedicated follow-up program's measured yield per spectrum and per night on Rubin-selected targets (none exists; BTS/BTSbot seeds are ZTF-selected and calibration only)",
    falsifier="a measured Rubin-target trigger purity or classification success outside the grid, or a rerun of truth_cost.py on the same inputs returning different ranges") for k, v in summary.items()]
json.dump(out, open(D/"truth_cost.json", "w"), indent=1); print(json.dumps(out["ranges_over_grid_L0"], indent=1))
