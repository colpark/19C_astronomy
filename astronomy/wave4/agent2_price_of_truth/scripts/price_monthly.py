#!/usr/bin/env python3
"""calendar_model_FROZEN.md secs 1-6: monthly price of truth (both deltas), return-date function, waiting on existing TNS supply, ruling-4 sensitivity."""
import json, math, csv, hashlib, pathlib, calendar, itertools, collections
import numpy as np
D = pathlib.Path(__file__).resolve().parent.parent
assert hashlib.sha256((D/"calendar_model_FROZEN.md").read_bytes()).hexdigest() == (D/"calendar_model_FROZEN.sha256").read_text().split()[0]
W3 = D.parents[1]/"wave3/agent2_measured_labels"
t3 = list(csv.DictReader(open(W3/"truth_cost_table.csv")))
reach = json.load(open(W3/"out/reachability.json"))
A_NIGHT = reach["A_per_night"]["10"]["cp95_lo"]
F_R, F_R_ALT = 10/15, 11/16
# ---- U(m)
recs = {}
for l in open(D/"out/irsa_nights.jsonl"):
    r = json.loads(l)
    if r.get("status") == 200: recs[r["ym"]] = r
Uy = collections.defaultdict(dict); Uany = collections.defaultdict(dict); irsa_detail = {}
for ym, r in sorted(recs.items()):
    y, m = map(int, ym.split("-")); days = calendar.monthrange(y, m)[1]
    ns = np.array([x["n"] for x in r["rows"] if x["n"] > 0])
    if ns.size == 0:
        u = ua = 0.0; p90 = 0
    else:
        p90 = float(np.percentile(ns, 90)); u = float((ns >= 0.5 * p90).sum()) / days; ua = float(ns.size) / days
    Uy[m][y] = u; Uany[m][y] = ua; irsa_detail[ym] = dict(nights_with_rows=int(ns.size), p90_rows=p90, usable=round(u * days), days=days, U=round(u, 4), U_any=round(ua, 4), query_seconds=r.get("seconds"))
missing = [f"{y}-{m:02d}" for y in (2021, 2022, 2023, 2024) for m in range(1, 13) if f"{y}-{m:02d}" not in recs]
U = {m: (float(np.mean(list(Uy[m].values()))) if Uy[m] else None) for m in range(1, 13)}
Ubar = float(np.mean([v for v in U.values() if v is not None])) if any(v is not None for v in U.values()) else None
P_GRID = [0.81, 0.846, 0.92, 0.93, 0.956, 0.967]; S_GRID = [0.93, 1.0]; C_GRID = [4.5, 8, 10]
N_GRID = [(0.05, 63, "ratified"), (0.05, 1666, "ratified"), (0.018, 485, "prior"), (0.018, 12855, "prior")]
L_CASES = [("L=0 (cohort measured STRONG 0; UNDEMONSTRATED)", 0), ("L=13 sensitivity (cohort existence MODERATE, classifier unknown)", 13)]
R_MONTHS = [(2026, m) for m in range(10, 13)] + [(2027, m) for m in range(1, 10)]
def months_after(R, Nneed, p, s, c):
    if Nneed <= 0: return 0, None, []
    y, m = R; cum = 0.0; k = 0; per = []
    while k < 120:
        days = calendar.monthrange(y, m)[1]
        if U[m] is None: return None, None, per
        s_cap = c * U[m] * days; a_m = A_NIGHT * F_R * days; s_eff = min(s_cap, a_m)
        cum += s_eff * p * s; k += 1; per.append(dict(month=f"{y}-{m:02d}", p60_usable_nights=round(U[m] * days, 1), rubin_on_sky_nights=round(F_R * days, 1), spectra=round(s_eff, 1), binding="capacity" if s_cap <= a_m else "arrivals"))
        if cum >= Nneed: return k, f"{y}-{m:02d}", per
        m += 1
        if m == 13: y, m = y + 1, 1
    return ">120", None, per
rows = []
for (delta, N, status), p, s, c, (lname, L) in itertools.product(N_GRID, P_GRID, S_GRID, C_GRID, L_CASES):
    Nneed = max(0, N - L); S = math.ceil(Nneed / (p * s)) if Nneed else 0; H = 0.5 * S; Wc = S - math.ceil(Nneed / s) if Nneed else 0
    if L == 0:
        m3 = [x for x in t3 if float(x["delta"]) == delta and int(x["N"]) == N and float(x["purity_p"]) == p and float(x["success_s"]) == s and float(x["capacity_c"]) == c and int(x["L"]) == 0]
        assert m3 and int(m3[0]["spectra_S"]) == S, ("wave-3 table mismatch", delta, N, p, s, c)
    nights = math.ceil(S / c) if S else 0
    agg = (Nneed / (p * s * c * Ubar * 30.44)) if (Ubar and Nneed) else (0 if not Nneed else None)
    for R in R_MONTHS:
        k, done, per = months_after(R, Nneed, p, s, c)
        rows.append(dict(delta=delta, delta_status=status, N=N, L_case=lname, N_need=Nneed, purity_p=p, success_s=s, capacity_c=c,
                         spectra_S=S, P60_hours=H, wrong_routine_commitments=Wc, cost_slots=S, missed_rare_penalty="+100 slots per missed rare event (M UNDEMONSTRATED)",
                         p60_usable_nights_needed=nights, spectra_per_month_first=per[0]["spectra"] if per else None,
                         p60_nights_per_month_first=per[0]["p60_usable_nights"] if per else None, rubin_on_sky_nights_per_month_first=per[0]["rubin_on_sky_nights"] if per else None,
                         return_month_R=f"{R[0]}-{R[1]:02d}", months_after_R=k, completion_month=done, months_aggregate_Ubar=round(agg, 2) if agg is not None else None,
                         binding_first_month=per[0]["binding"] if per else None))
with open(D/"truth_cost_monthly.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# ---- waiting on existing TNS supply
w3sup = json.load(open(W3/"supply_P_per_month.json"))
b = [w3sup["months"][f"2026-{m:02d}"]["b_nonbot_measured_lower_bound"]["incl_syncatto"] for m in range(1, 9)]
a = [w3sup["months"][f"2026-{m:02d}"]["a_spectroscopic_units_lower_bound"] for m in range(1, 9)]
r_b, r_a = sum(b) / 8, sum(a) / 8; r_c = 13 / 2.53
waiting = []
for (delta, N, status), p in itertools.product(N_GRID, P_GRID):
    waiting.append(dict(delta=delta, N=N, purity_p=p,
        months_upper_bound_human_confirmed_r_b=round(N / (r_b * p), 1), months_upper_bound_incl_model_annotated_r_a=round(N / (r_a * p), 1),
        months_cohort_existence_rate_moderate=round(N / (r_c * p), 1), months_cohort_measured_strong="unbounded (rate 0 STRONG; UNDEMONSTRATED)",
        note="r_a/r_b are all-sky all-survey TNS lower-bound rates, not cohort rates; months are upper bounds on waiting time only if every report counted toward N"))
def summ(delta, N, L=0):
    sel = [r for r in rows if r["delta"] == delta and r["N"] == N and ((r["L_case"].startswith("L=0")) == (L == 0))]
    mk = [r["months_after_R"] for r in sel if isinstance(r["months_after_R"], int)]
    return dict(spectra=[min(r["spectra_S"] for r in sel), max(r["spectra_S"] for r in sel)], P60_hours=[min(r["P60_hours"] for r in sel), max(r["P60_hours"] for r in sel)],
                p60_usable_nights=[min(r["p60_usable_nights_needed"] for r in sel), max(r["p60_usable_nights_needed"] for r in sel)],
                wrong_commitments=[min(r["wrong_routine_commitments"] for r in sel), max(r["wrong_routine_commitments"] for r in sel)],
                months_after_return=[min(mk), max(mk)] if mk else "UNDEMONSTRATED (U missing)", months_over_120=sum(1 for r in sel if r["months_after_R"] == ">120"),
                months_aggregate_Ubar=[min(r["months_aggregate_Ubar"] for r in sel), max(r["months_aggregate_Ubar"] for r in sel)] if Ubar else None)
def pick(delta, N, p, s, c, R="2027-01"):
    r = [x for x in rows if x["delta"] == delta and x["N"] == N and x["purity_p"] == p and x["success_s"] == s and x["capacity_c"] == c and x["L_case"].startswith("L=0") and x["return_month_R"] == R][0]
    return {k: r[k] for k in ("spectra_S", "P60_hours", "p60_usable_nights_needed", "spectra_per_month_first", "months_after_R", "completion_month", "months_aggregate_Ubar", "wrong_routine_commitments")}
by_R = {}
for (delta, N, _) in N_GRID:
    for R in R_MONTHS:
        key = f"{R[0]}-{R[1]:02d}"
        sel = [r for r in rows if r["delta"] == delta and r["N"] == N and r["L_case"].startswith("L=0") and r["return_month_R"] == key and isinstance(r["months_after_R"], int)]
        by_R.setdefault(f"delta_{delta}_N_{N}", {})[key] = [min(r["months_after_R"] for r in sel), max(r["months_after_R"] for r in sel)] if sel else "UNDEMONSTRATED/>120"
out = dict(
    banner="PLANNING price of measured labels per month; not a P7 record; BTS seeds calibration only (contamination FAIL on BTS); rule E: enters kill-band pricing only through module V records",
    calendar_model_sha256=(D/"calendar_model_FROZEN.sha256").read_text().split()[0],
    wave3_truth_cost_table_sha256=hashlib.sha256((W3/"truth_cost_table.csv").read_bytes()).hexdigest(),
    consistency_check="spectra_S for every L=0 row asserted equal to wave-3 truth_cost_table.csv (same formula)",
    inputs=dict(U_by_calendar_month={calendar.month_abbr[m]: (round(U[m], 4) if U[m] is not None else None) for m in range(1, 13)},
                U_by_year={calendar.month_abbr[m]: {y: round(v, 4) for y, v in Uy[m].items()} for m in range(1, 13)},
                U_any_by_calendar_month={calendar.month_abbr[m]: (round(float(np.mean(list(Uany[m].values()))), 4) if Uany[m] else None) for m in range(1, 13)},
                U_annual_mean=round(Ubar, 4) if Ubar else None, irsa_months_missing=missing, irsa_detail=irsa_detail,
                f_R=F_R, f_R_alt=F_R_ALT, A_night_cp95_lo=A_NIGHT, sky_overlap_o="UNDEMONSTRATED, applied as 1 (months are lower bounds)",
                rates=dict(r_b_human_confirmed=r_b, r_a_incl_model_annotated=r_a, r_c_cohort_existence_moderate=round(r_c, 3), r_c_cohort_measured_strong=0)),
    summary_L0={f"delta_{d}_N_{n}": summ(d, n) for d, n, _ in N_GRID},
    summary_L13_sensitivity={f"delta_{d}_N_{n}": summ(d, n, 13) for d, n, _ in N_GRID},
    months_after_return_by_R_L0=by_R,
    reference_point_p093_s093_c8_R2027_01={f"delta_{d}_N_{n}": pick(d, n, 0.93, 0.93, 8) for d, n, _ in N_GRID},
    waiting_on_existing_supply=waiting,
    ruling4_sensitivity=dict(
        existing_supply=dict(human_confirmed_only_rate=r_b, including_model_annotated_rate=r_a, cohort="STRONG split UNDEMONSTRATED (0 archived reports)"),
        dedicated_program="spectra, hours, nights identical in both cases; human confirmation adds classifier effort not priced (UNDEMONSTRATED); including model-annotated, an automated classifier (SNIascore-class) counts without human hours",
        bts_calibration_pool=dict(human_confirmed_placed=1074, including_model_annotated_placed=2028, model_annotation_bound=[954, 2057], note="calibration only; wave-3 track one")),
    cost_of_action="0.5 h P60 per spectrum; 1 slot per wrong routine commitment (W); >=100 slots per missed rare event (asymmetric; M UNDEMONSTRATED; add-on)",
    constraints=["Rubin off sky since 2026-07-14 with no return date: months are a function of R, calendar completion UNDEMONSTRATED",
                 "sky overlap Palomar/Cerro Pachon UNDEMONSTRATED (o=1): months are lower bounds on program duration",
                 "U from P48 site data (MODERATE); P60/SEDM-specific downtime not included"],
)
json.dump(out, open(D/"truth_cost_monthly.json", "w"), indent=1, default=str)
print(json.dumps({k: out[k] for k in ("summary_L0", "reference_point_p093_s093_c8_R2027_01")}, indent=1)[:4000]); print(out["inputs"]["U_by_calendar_month"], out["inputs"]["U_annual_mean"], missing)
