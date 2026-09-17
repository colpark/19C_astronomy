#!/usr/bin/env python3
"""Assemble supply_P_per_month.json and tns_census_2026.json (provenance records) from census outputs; run validator."""
import json, pathlib, hashlib, subprocess, sys, collections
D = pathlib.Path(__file__).resolve().parent.parent
C = json.load(open(D/"out/census_counts.json")); E = json.load(open(D/"sealed/enumeration_E_SEALED.json"))
ant = json.load(open(D/"out/antares_tns_cohort.json")); R = json.load(open(D/"out/reachability.json"))
MONTHS = [f"2026-{m:02d}" for m in range(1, 10)]
h = lambda p: hashlib.sha256((D/p).read_bytes()).hexdigest()
tA_typed = [x for x in E["tierA"] if x.get("typed_T9")]
ant_sn_cohort = sorted({m["attributes"]["properties"]["name"] for L in ant["loci"] for m in (L["tns_matches"] or [])
                        if m["attributes"]["properties"].get("name_prefix") == "SN" and (m["attributes"]["properties"].get("discoverydate") or "") >= "2026-06-30"})
ant_sn_old = sorted({(m["attributes"]["properties"]["name"], m["attributes"]["properties"]["discoverydate"][:10]) for L in ant["loci"] for m in (L["tns_matches"] or [])
                     if m["attributes"]["properties"].get("name_prefix") == "SN" and (m["attributes"]["properties"].get("discoverydate") or "") < "2026-06-30"})
HTTP_T2 = ["Wayback stats-maps captures 20260904020708, 20260803084202, 20260517222550, 20260501052304, 20251224104902: archived TNS 403 page (118 bytes); 20260107112933: HTTP 200 (per-year only, 2026=1 classified SN)",
           "live https://www.wis-tns.org/stats-maps HTTP 403 server awselb/2.0 (2026-09-17T00:06:46Z)",
           "Wayback CDX https://web.archive.org/cdx/search/cdx?url=wis-tns.org/object/2026* HTTP 503 (2026-09-17T00:07:00Z)",
           "Wayback search captures 20260904020709, 20260501052304, 20260104161855, 20250829052011: archived 403; 20260514130743: 200 (50 rows, discovery date 2026-05-14 only)",
           "ATel ?read=17991, ?read=17982: reCAPTCHA page (access control, not bypassed)"]
months = {}
for m in MONTHS:
    months[m] = dict(
        a_spectroscopic_units_lower_bound=C["a_all_units_per_month"]["spectroscopic"][m],
        a_non_spectroscopic_or_unknown_lower_bound=C["a_all_units_per_month"]["non_spectroscopic_or_unknown"][m],
        P_objects_first_classified_lower_bound=C["P_objects_first_classified_per_month"][m],
        b_nonbot_measured_lower_bound=dict(incl_syncatto=C["b_nonbot_measured_per_month"]["b_incl_syncatto_as_human"][m], excl_syncatto=C["b_nonbot_measured_per_month"]["b_excl_syncatto_as_automated"][m]),
        c_cohort_T1_strong=C["c_cohort_per_month"]["all"][m] if m >= "2026-07" else "n/a (cohort starts 2026-07-01)",
        disposition="LOWER BOUND DERIVED (T1 STRONG, 214/2244 enumerated objects had a readable capture); exact count UNDEMONSTRATED",
        exact_blocked_by=HTTP_T2)
    if m >= "2026-07":
        months[m]["c_cohort_existence_moderate"] = "UNDEMONSTRATED per month (classification month unknown for T9/T8 existence matches; see totals)"
res = dict(
    banner="Census of 2026 TNS spectroscopic classification reports from public archives; calibration only for BTS; Rubin cohort supply",
    protocol_sha256="9fac85524f28b5e3874a0d43a2c089915d20814b7996c18a0c77cc230b3c95fb",
    track_one=dict(status="BLOCKED", reason="TNS_API_KEY absent (coordinator presence test 2026-09-16T20:13:38Z; agent re-test ABSENT 2026-09-17T00:06Z)", request_date="2026-09-16"),
    months=months,
    programs_spectroscopic_units_per_month_lower_bound=C["programs_spectroscopic_per_month"],
    programs_automation_mix=C["programs_automation_mix"],
    fetch=C["fetch"],
    aggregates_moderate=dict(
        T9_rochester_confirmed_SNe_discovered_2026_as_of_2026_09_16=dict(value=1587, locator="sources/census/rochester_supernova.html 'For the year 2026, 19448 supernovae (1587 confirmed, 17858 unconfirmed, and 3 other sources)'", note="by discovery year, not report month; confirmed = spectroscopically typed; no program attribution"),
        T9_typed_entries_enumerated=len(E["tierB"]) + len(tA_typed),
        T2_classified_SNe_discovered_2025=dict(value=2055, locator="sources/census/tns_stats_maps_20260107112933.txt 'TNS classified SNe reported by year 2025 2,055'"),
        T2_cumulative_classifications_top_groups_since_2016="ZTF 8,768 (44%), ePESSTO+ 2,455 (12%), SCAT 1,965 (10%), ePESSTO 723, UCSC 409, TCD 372, Global SN Project 359, PESSTO 277, iPTF 256, Padova-Asiago 238 (capture 2026-01-07)"),
    cohort_c=dict(
        T1_strong_reports_on_cohort_objects=len(C["c_cohort_units"]),
        tierA_objects=len(E["tierA"]), tierA_captures_ok=C["fetch"]["status_by_tier"].get("A:ok", 0), tierA_captures_with_reports=0 if not C["c_cohort_units"] else None,
        T9_typed_cohort_matches=[dict(name=x["name"], type=x["type_T9"], discdate=x["discdate"], match=x["cohort"]) for x in tA_typed],
        T8_antares_SN_classified_cohort_loci_disc_ge_2026_06_30=ant_sn_cohort,
        T8_antares_SN_at_cohort_position_discovered_before_2026_06_30_LEAK=[dict(name=n, discdate=d) for n, d in ant_sn_old],
        existence_union_T9_T8=sorted({x["name"] for x in tA_typed} | set(ant_sn_cohort)),
        existence_total_moderate=len({x["name"] for x in tA_typed} | set(ant_sn_cohort)),
        T9_T8_disagreement=dict(in_T9_not_T8=sorted({x["name"] for x in tA_typed} - set(ant_sn_cohort)), in_T8_not_T9=sorted(set(ant_sn_cohort) - {x["name"] for x in tA_typed})),
        existence_transients_moderate=len({x["name"] for x in tA_typed if x["type_T9"] != "CV"} | set(ant_sn_cohort)),
        measured_nonbot_T1_strong=0, measured_nonbot_status="UNDEMONSTRATED (12 T9-typed cohort objects: archive 404 x11, 403 x1; 2026uyc T1 404)"),
    cohort_classified_existence_T8_T9_moderate=len({x["name"] for x in tA_typed} | set(ant_sn_cohort)),
    cohort_measured_nonbot_labels_T1_strong=0,
)
(D/"supply_P_per_month.json").write_text(json.dumps(res, indent=1, default=str))
POP = "2026 TNS classification reports readable in Internet Archive captures of www.wis-tns.org/object/<name> for the sealed enumeration E (2,244 objects: 627 cohort-matched + 1,617 other typed 2026 objects from rochesterastronomy.org); dedup (object, program)"
SRC = f"astronomy/wave3/agent2_measured_labels/scripts/census.py::main; sealed/enumeration_E_SEALED.json sha256 {h('sealed/enumeration_E_SEALED.json')}; out/tns_captures_w3/fetch_log.jsonl sha256 {h('out/tns_captures_w3/fetch_log.jsonl')}; census_protocol_FROZEN.md sha256 9fac85524f28b5e3874a0d43a2c089915d20814b7996c18a0c77cc230b3c95fb"
ADJ = "authenticated TNS search/API over all 2026 classification reports (TNS_API_KEY BLOCKED), or TNS stats page with monthly per-group breakdown (archived copies are 403 pages)"
CAL = "calibration only, contamination FAIL on this cohort (BTS); Rubin cohort supply planning"
def rec(i, v, ref, fal, src=SRC, pop=POP, adj=ADJ):
    return dict(id=i, value=v, referent=ref, source=src, population=pop, adjudicator=adj, falsifier=fal, banner=CAL)
tot = lambda k: sum(C[k][x] if isinstance(C[k][x], int) else 0 for x in MONTHS) if False else None
spec_tot = sum(C["a_all_units_per_month"]["spectroscopic"].values()); b_tot = sum(C["b_nonbot_measured_per_month"]["b_incl_syncatto_as_human"].values())
recs = [
    rec("w3a2-a-spectroscopic-units-lb", dict(total_Jan_Sep=spec_tot, per_month=C["a_all_units_per_month"]["spectroscopic"]), "lower bound on 2026 spectroscopic classification reports per month (unit: object x program, earliest report)",
        "an authenticated report list returning fewer reports than this in any month, or a rerun of census.py on the same captures returning different counts"),
    rec("w3a2-b-nonbot-units-lb", dict(total_Jan_Sep=b_tot, per_month=C["b_nonbot_measured_per_month"]["b_incl_syncatto_as_human"]), "lower bound on 2026 non-bot measured spectroscopic classification reports per month (no SNIascore/CCSNscore/bot marker in Classifier/s; Syncatto both ways identical)",
        "a counted report whose Classifier/s is shown to be an automated pipeline, or a rerun returning different counts"),
    rec("w3a2-P-objects-lb", dict(per_month=C["P_objects_first_classified_per_month"]), "lower bound on distinct objects first classified per month in 2026", "an authenticated list returning fewer first classifications per month, or a rerun returning different counts"),
    rec("w3a2-c-cohort-existence", len({x["name"] for x in tA_typed} | set(ant_sn_cohort)),
        "Rubin cohort objects (first detection >= 2026-07-01, agent-1 slices) with a typed 2026 TNS name, by 1 arcsec position or LSST diaObjectId alias (T9) or ANTARES tns_public_objects SN match with discovery >= 2026-06-30 (T8), union, MODERATE; classifier UNDEMONSTRATED",
        fal="a TNS report showing one of these objects was classified before its Rubin first detection, or a rerun of build_E.py cohort_match returning a different match set",
        src=f"astronomy/wave3/agent2_measured_labels/scripts/build_E.py::cohort_match; out/rochester_entries_rochester_supernova.json sha256 {h('out/rochester_entries_rochester_supernova.json')}; out/antares_tns_cohort.json sha256 {h('out/antares_tns_cohort.json')}",
        pop="1,937,720 cohort oids (agent-1 w3_c3_slices, firstmjd >= T0) crossmatched to 19,170 rochesterastronomy.org 2026 entries and 319 ANTARES TNS-matched cohort loci",
        adj="authenticated TNS classification reports for these objects"),
    rec("w3a2-c-cohort-measured-strong", 0,
        "Rubin cohort objects with a STRONG (archived page) non-bot spectroscopic classification report: 0 found; UNDEMONSTRATED, not zero (tier-A captures: 13 readable, none with a report; typed cohort objects returned archive 404 or 403)",
        fal="an archived or authenticated page returning a non-bot classification report for one of the 627 tier-A objects would replace this record",
        pop="627 tier-A cohort-matched objects in sealed enumeration E"),
    rec("w3a2-reach-f19", R["f19"], "share of Rubin cohort objects whose brightest S/N>=5 difference-flux detection is <= 19.0 AB mag (SEDM depth, arXiv:2412.08601 line 265)",
        fal="a second declared sample returning a share outside the Clopper-Pearson 95% interval, or revised Fink photometry that changes the peak magnitudes of the 8 counted objects",
        src=f"astronomy/wave3/agent2_measured_labels/scripts/reach_compute.py; out/reach_rows.jsonl sha256 {h('out/reach_rows.jsonl')}; Fink /api/v1/sources via scripts/safe_fetch.py (labels stripped)",
        pop="sample R: 2,000 cohort oids with smallest sha1(oid) (sealed/lookup_list_SEALED.json)", adj="full-cohort photometry, or PPDB forced photometry when released"),
]
(D/"tns_census_2026.json").write_text(json.dumps(recs, indent=1, default=str))
r = subprocess.run([sys.executable, str(D.parents[2]/"fm-advantage-benchmark/scripts/validate.py"), "provenance", str(D/"tns_census_2026.json")], capture_output=True, text=True)
print(r.stdout)
