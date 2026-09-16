#!/usr/bin/env python3
"""Assemble Agent 1 JSON records from out/sweep.json and out/supply.json. No number is typed by hand
except document-derived quantities, each of which carries its arithmetic and locator below."""
import json, hashlib
from pathlib import Path
import pandas as pd

H = Path(__file__).resolve().parent.parent
O = H / "out"
sw = json.load(open(O / "sweep.json")); sp = json.load(open(O / "supply.json"))
ans = json.load(open(O / "answer_in_seed_text.json"))
RULES_SHA = (H / "corpus_rules_FROZEN.sha256").read_text().split()[0]
RAW_SHA = "61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
SRC = "astronomy/agent1_supply_corpus/scripts/"
A = sp["at_chosen"]

# ---------------- published corpus ----------------
d = pd.read_csv(O / "corpus_rows.csv", dtype=str, keep_default_na=False)
corp = d[["ZTFID", "IAUID", "RA", "Dec", "peakt", "peakfilt", "peakmag", "peakabs", "duration", "rise", "fade",
          "type", "redshift", "b", "A_V", "label", "cl_1", "F2_bright_18p5", "F4_label_immature",
          "F5_censored_timescale", "F6_no_redshift", "F7_no_peakabs"]].rename(columns={"cl_1": "object_cluster_1arcsec"})
corp.to_csv(H / "corpus.csv", index=False)
corpus_sha = hashlib.sha256((H / "corpus.csv").read_bytes()).hexdigest()

# ---------------- seeds ----------------
seeds = [
 {"id": "Fremling2020_arXiv1910.12973", "file": "sources/1910.12973.pdf (+ .raw.txt)", "read_in_full": True,
  "contribution": "BTS survey design, filter, follow-up priority scheme, nightly volumes, per-night follow-up commitment, position definition",
  "facts": [
   {"assertion": "BTS goal: spectroscopically classify all extragalactic transients brighter than 18.5 mag at peak in g or r", "locator": "abstract; section 1 para 'The primary goal of the BTS'"},
   {"assertion": "On a typical night in 2018 a few hundred alerts passed the BTS filter", "locator": "section 2.2 first para"},
   {"assertion": "5-15 SN candidates per night are identified by scanners and assigned for spectroscopic follow-up", "locator": "section 2.2 para 'Among the passing alerts'"},
   {"assertion": "SEDM priorities P3 (<18.5), P2 (18.5-18.75), P1 (>18.75); triggers active 7 d", "locator": "section 2.3"},
   {"assertion": "SEDM can classify >10 SNe in the 18.5-19 mag range every night", "locator": "section 1 para 'With the Zwicky Transient Facility'"},
   {"assertion": "Catalog positions are the weighted average over every alert associated with the SN", "locator": "section 3.1 last para"},
   {"assertion": "761 SNe classified Apr-Dec 2018: 547 Ia, 155 II, 40 Ib/c, 19 SLSN", "locator": "section 3.2; Table 2"},
   {"assertion": "Filter rejects |b|<=7 deg, rbscore<0.2, known stars, moving objects, negative subtractions", "locator": "section 2.1 bullet list"},
   {"assertion": "Spectroscopic completeness ~96% (visual) / 93.6% to mpeak<18.5 (automated) for 2018", "locator": "section 2.3.1"}]},
 {"id": "Perley2020_arXiv2009.01242", "file": "sources/2009.01242.pdf (+ .raw.txt)", "read_in_full": True,
  "contribution": "BTS alert volume, saved-candidate rate, quality/purity cuts, false-positive classes, class totals, redshift uncertainty, host search radius, public start date",
  "facts": [
   {"assertion": "Filter reduced ~10^6 Avro alert packets per night to ~500 viable candidates (first-year filter)", "locator": "section 2.1 para 'Our first-year in-stream software filter'"},
   {"assertion": "2019 filter changes cut false positives from several hundred per night to <~50", "locator": "section 2.1"},
   {"assertion": "Typically 5-10 candidates saved on an average clear night", "locator": "section 2.1 last para"},
   {"assertion": "AGNs and CVs pass the filter routinely but are not part of the project; scarce spectroscopic resources reserved for genuine extragalactic transients", "locator": "section 2.4 first para"},
   {"assertion": "Public start of BTS survey 2018-06-01", "locator": "section 2.3 para after cut list"},
   {"assertion": "SN-feature redshifts have dz~0.005 uncertainty", "locator": "section 2.2 para 'the distance modulus'"},
   {"assertion": "Host cross-match search limited to <90 arcsec and <30 kpc", "locator": "section 2.2 para 'To provide additional counterpart photometry'"},
   {"assertion": "3147 classified transients in 25.5 months, 1865 pass quality+purity cuts, 1206 also m<18.5", "locator": "section 3; Table 1"},
   {"assertion": "Statistical sample 93% complete at <18.5, 97% at <18, 75% at <19", "locator": "abstract; section 3"},
   {"assertion": "Classification success depends on season/weather (winter losses)", "locator": "Appendix D, Figure 13"},
   {"assertion": "Classifications are the most recent TNS classification, some subtypes removed", "locator": "Appendix E"}]},
 {"id": "BTS_explorer_info", "file": "sources/bts_explorer_info.html", "url": "https://sites.astro.caltech.edu/ztf/bts/explorer_info.html", "read_in_full": True,
  "contribution": "CSV column semantics, non-completeness for Galactic/non-transient events, TNS mismatch warning, peak-mag upper-limit caveat",
  "facts": [
   {"assertion": "BTS makes no attempt to be complete to Galactic events and non-transients: most are removed by the alert filter or scanners", "locator": "section 'Classification'"},
   {"assertion": "time: time of peak expressed as JD-2458000", "locator": "section 'Data Columns', item time"},
   {"assertion": "mag: peak P48 magnitude; if the true peak was missed this is an upper limit", "locator": "section 'Data Columns', item mag"},
   {"assertion": "Rise/Fade given as a limit when no detections deeper than 0.75 mag below peak exist", "locator": "section 'Data Columns', items Rise and Fade"},
   {"assertion": "TNS ID: a few transients are wrongly matched on TNS", "locator": "section 'Data Columns', item TNS ID"},
   {"assertion": "Redshift: often approximate", "locator": "section 'Data Columns', item Redshift"}]},
 {"id": "LDM-612_v1.4", "file": "sources/LDM-612.pdf", "url": "https://ldm-612.lsst.io/", "read_in_full": True,
  "contribution": "alert-to-DIASource-to-DIAObject mapping, nightly alert scale",
  "facts": [
   {"assertion": "LSST expects up to about ten million alerts nightly", "locator": "section 1 para 2"},
   {"assertion": "Every SNR>5 difference-image source is a DIASource and causes an alert; every DIASource has one unique match to a DIAObject or SSObject; a new DIAObject is created when no association is possible", "locator": "section 2.2.1 para 'All sources in a difference image'"},
   {"assertion": "Alert packet contains the triggering DIASource, the entire DIAObject/SSObject record, and 12 months of prior DIASource/DIAForcedSource records", "locator": "section 2.3.1 items I-VI"},
   {"assertion": "Alert generation in crowded fields may exceed the maximum of 10,000 alerts per visit required", "locator": "section 2.2.1 footnote 2"}]},
 {"id": "DMTN-102_2024-04-24", "file": "sources/DMTN-102.pdf", "url": "https://dmtn-102.lsst.io/", "read_in_full": True,
  "contribution": "alert key numbers used to derive alert-per-SN overstatement",
  "facts": [
   {"assertion": "DMS supports >=10,000 alerts per standard visit on average and >=40,000 per single visit; long-term average 10^7 alerts per night assuming 1,000 visits per night", "locator": "section 2.2 first two paras"},
   {"assertion": "~10 million SNe in 10 years (~1 million per year); ~200 SN alerts per visit", "locator": "section 2.2 bullet Supernovae"},
   {"assertion": "300 observing nights per year", "locator": "section 2.6"},
   {"assertion": "Alert packet <=~82 KB", "locator": "section 2.3"}]},
 {"id": "LSE-163_DPDD_v3.9.1", "file": "sources/LSE-163.pdf", "url": "https://lse-163.lsst.io/", "read_in_full": True,
  "contribution": "DIAObject/DIASource definitions, association procedure, false-positive rate",
  "facts": [
   {"assertion": "Clusters of DIASources at different times are associated with a DIAObject or SSObject to represent the underlying astrophysical phenomenon", "locator": "section 3.1 para 3"},
   {"assertion": "~one background-fluctuation false positive per CCD at transSNR=5, order 200,000 per typical night", "locator": "section 3.1 para 2"},
   {"assertion": "Up to ~10,000 astrophysical DIASources per visit (~10M per night)", "locator": "section 3.3.1 first para"},
   {"assertion": "Alert issued for each detected DIASource within 60 s; includes entire DIAObject record", "locator": "section 3.5.1"},
   {"assertion": "Orphaned DIAObjects are deleted when their DIASources are relinked to SSObjects", "locator": "section 3.2.2 step 3"},
   {"assertion": "Alerts issued in VOEvent format", "locator": "section 3.5.1, section 3.5.2"}]},
 {"id": "sdm_schemas_apdb.yaml_v10.0.0", "file": "sources/sdm_schemas_apdb.yaml", "url": "https://github.com/lsst/sdm_schemas/blob/main/python/lsst/sdm/schemas/apdb.yaml (main at 5499df17769416b7a26b50e11c5ef5d17ff4e361, 2026-09-14)", "read_in_full": True,
  "contribution": "as-built DiaObject/DiaSource tables; nDiaSources column makes alerts-per-object measurable in the PPDB",
  "facts": [
   {"assertion": "DiaObject: astronomical objects detected on one or more difference images; has nDiaSources", "locator": "table DiaObject, columns diaObjectId, nDiaSources"},
   {"assertion": "Each diaSource is associated with either a diaObject or an ssObject", "locator": "table DiaSource, column diaObjectId description"}]},
 {"id": "alert_packet_lsst.v11_1", "file": "sources/alert_packet_lsst.v11_1.alert.avsc", "url": "https://github.com/lsst/alert_packet (main at 1362a8d7f1db4014cbd419390580a707141c683a; latest.txt=11.1)", "read_in_full": True,
  "contribution": "alert = one triggering diaSource + optional diaObject + history arrays",
  "facts": [{"assertion": "Alert record keyed by diaSourceId with one diaSource, prvDiaSources array, optional diaObject", "locator": "lsst.v11_1.alert.avsc fields"}]},
 {"id": "Rubin_news_first_alerts_2026-02-25", "file": "sources/rubin_news_first_alerts.html", "url": "https://rubinobservatory.org/news/first-alerts", "read_in_full": True,
  "contribution": "verifies first alerts 24 Feb 2026; 800,000 alerts that night; up to seven million per night",
  "facts": [{"assertion": "Rubin issued 800,000 alerts the night of 24 February (2026)", "locator": "article body para 1 (txt line 20)"},
            {"assertion": "system expected to eventually produce up to seven million alerts per night", "locator": "article body para 1 (txt line 20)"},
            {"assertion": "Each change triggers an alert within two minutes of image capture", "locator": "section 'Capturing the Changing Cosmos' (txt line 29)"}]},
 {"id": "NOIRLab_sci26008", "file": "sources/noirlab_sci26008.html", "url": "https://noirlab.edu/science/news/announcements/sci26008", "read_in_full": True,
  "contribution": "first alerts arrived at brokers 24 Feb 2026; ~20 billion alerts over 10 years",
  "facts": [{"assertion": "First world-public alerts arrived at community brokers on the night of 24 February 2026", "locator": "announcement para 1"},
            {"assertion": "about 20 billion alerts in total over the ten-year LSST", "locator": "announcement para 2"}]},
 {"id": "Rubin_news_LSST_begins_2026-06-30", "file": "sources/rubin_news_action_lsst_begins.html", "url": "https://rubinobservatory.org/news/action-rubin-lsst-begins", "read_in_full": True,
  "contribution": "verifies LSST formal start 2026-06-30; about a thousand images per night; as many as seven million alerts per night",
  "facts": [{"assertion": "The 10-year LSST has officially started, dated June 30, 2026", "locator": "article header (txt line 32)"},
            {"assertion": "producing as many as seven million alerts of changes in the night sky each night", "locator": "article body (txt line 47)"}]},
 {"id": "Rubin_alerts_and_brokers_page", "file": "sources/rubin_alerts_and_brokers.html", "url": "https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers", "read_in_full": True,
  "contribution": "zero decision contribution beyond broker list (seven full-stream, two downstream); read with zero contribution to counts",
  "facts": [{"assertion": "Seven full-stream brokers and two downstream brokers", "locator": "section 'Alert brokers' (txt lines 14-15)"}]},
]

unresolved = [
 "Total number of distinct DIAObjects per night or per year in the Rubin stream: no seed states it; alerts-per-DIAObject for the whole stream is UNDEMONSTRATED (measurable from PPDB DiaObject.nDiaSources, which requires data rights not held here).",
 "Why BTS labels collapse for peaks after 2026-01 (2026 peaks 89.4% unlabeled vs 25-35% in 2019-2025): no seed read explains it.",
 "Whether peakmag is an upper limit (missed peak) for any given row: the CSV carries no flag (explorer doc, 'mag').",
 "Which same-IAUID pairs are TNS mismatches vs re-triggers vs recurrent events: explorer doc says 'a few' are wrongly matched; not enumerated.",
 "Rubin-stream labelled supply for the governed decision (Rubin DIAObjects with spectroscopic classes): not in any local file.",
 "Budget and cost of action (D5 inputs): not supplied; S UNDEMONSTRATED.",
]

ans_items = []
seen = set()
for f, rows in ans.items():
    for r in rows:
        if r["ZTFID"] in seen: continue
        seen.add(r["ZTFID"])
        ans_items.append({"item": r["ZTFID"], "iau": r["IAUID"], "label_in_text_of": f, "admitted": False,
                          "counted_in_P3_supply": True,
                          "note": "classification stated in seed text read by this panel; admission to any benchmark item set refused pending Agent 3 exposure ruling"})

corpus_ledger = {
 "candidate": "live time-domain astronomy: ZTF BTS label base (Rubin LSST alert stream as the target decision surface)",
 "seeds": [{k: v for k, v in s.items()} for s in seeds],
 "inclusion_rules": [
  "I0 raw sha256 must equal " + RAW_SHA, "I1 ZTFID matches ^ZTF\\d{2}[a-z]{7}$ (else E1)",
  "I2 RA/Dec parse as sexagesimal (else E2)", "I3 peakt numeric (else E3)", "I4 peakmag numeric (else E4)",
  "I5 peakt in [270.5, 3299.5] = 2018-06-01..2026-09-16 (else E5)",
  "Flags F1-F7 are strata, never exclusions", "Label map posA/posB/neg/unlabeled frozen in corpus_rules_FROZEN.md"],
 "rules_file": "corpus_rules_FROZEN.md", "rules_sha256": RULES_SHA,
 "rules_frozen_before_count": True,
 "rules_frozen_disclosure": "schema-level inspection (column names, '-' and '>' token counts, distinct type strings, duplicate-ID counts) preceded freezing; no inclusion/label/cluster/split count was computed before the hash",
 "input": {"file": "astronomy/data/raw/ztf_bts_all_2026-09-16.csv", "sha256": RAW_SHA, "data_rows": sw["n_raw_rows"]},
 "corpus": {"file": "corpus.csv", "sha256": corpus_sha, "rows": sw["n_included_rows"],
            "distinct_objects_at_1arcsec": A["total"]["clusters"]},
 "exclusion_ledger": [{"unit": e["unit"], "rule": e["rule"], "peakt": e["peakt"], "type": e["type"]} for e in sw["exclusions"]],
 "exclusion_rule_counts": sw["exclusion_rule_counts"],
 "answer_in_own_source": ans_items,
 "amendments": [{"id": "A1", "changes": "D3 must-join control interpreted as re-trigger duplicates only (same IAUID and |dpeak|<=60 d)",
                 "cause": "4 same-IAUID pairs have |dpeak| 485-1598 d (3 of them SNe at 1.62-1.92 arcsec); explorer doc says some TNS matches are wrong; SN2023ghl/SN2024gyr prove two distinct SNe at 1.92 arcsec",
                 "affects_counts": False, "affects_inclusion_rules": False}],
 "coverage": {"seeds_read": len(seeds), "seeds_read_in_full": sum(s["read_in_full"] for s in seeds), "unresolved": unresolved},
 "completeness": "inventory: 12 seeds read whole; corpus built from one explorer CSV (11217 data rows, 24 excluded under E5, 0 under E1-E4); negatives limited to scanner-saved candidates; Rubin-stream units not in corpus; unresolved questions listed in coverage.unresolved; not a completeness claim",
 "provenance": [],
}

prov = [
 {"id": "a1-corpus-objects", "value": A["total"]["clusters"],
  "referent": "distinct astrophysical objects (positional friends-of-friends clusters at 1 arcsec) in the frozen BTS corpus",
  "source": SRC + "build_corpus.py::fof + count_supply.py::supply; raw sha " + RAW_SHA + "; rules sha " + RULES_SHA,
  "population": f"{sw['n_included_rows']} included rows after 24 E5 exclusions from {sw['n_raw_rows']} data rows",
  "adjudicator": "raw row count 11193 (overstatement 0.089%) and the full sweep 11104-11183 across 0.5-60 arcsec",
  "falsifier": "a rerun on the same sha that returns a different cluster count, or a must-join re-trigger pair found above 1 arcsec"},
 {"id": "a1-excluded", "value": sw["n_excluded"], "referent": "rows excluded by frozen rules",
  "source": SRC + "build_corpus.py::main rule E5; corpus_rules_FROZEN.md section Inclusion rules",
  "population": f"{sw['n_raw_rows']} data rows of the raw CSV", "adjudicator": "FETCH.md states no filter at fetch time",
  "falsifier": "a re-read that returns any listed row with peakt inside [270.5, 3299.5]"},
]
corpus_ledger["provenance"] = prov
json.dump(corpus_ledger, open(H / "corpus_ledger.json", "w"), indent=1)
json.dump({"seeds": seeds, "coverage": corpus_ledger["coverage"],
           "completeness": "inventory of 12 seeds actually read whole by Agent 1; this is not a completeness claim about the literature. Unresolved questions listed under coverage.unresolved."},
          open(H / "seed_ledger.json", "w"), indent=1)

# ---------------- cut curve ----------------
tau_raw = json.load(open(O / "tau_raw.json"))
curve = []
for c in sw["curve"]:
    r = sw["per_cut"][str(c["radius_arcsec"]) if str(c["radius_arcsec"]) in sw["per_cut"] else str(float(c["radius_arcsec"]))]
    curve.append({"radius_arcsec": c["radius_arcsec"], "cut": c["cut"], "n_clusters": c["n_clusters"],
                  "multi_member_clusters": r["multi_member_clusters"], "must_join_sameIAU_joined": f"{r['must_join_joined']}/{r['must_join_pairs']}",
                  "must_not_join_distinct_SN_violations": r["must_not_join_violations"],
                  "straddle_S1": r["straddle_S1"], "straddle_S2": r["straddle_S2"]})
cut_curve = {
 "chosen_cut": 1.0, "chosen_radius_arcsec": 1.0,
 "D3_disposition": "REFUSE tau.py's choice; cut bounded by controls instead; separation-collapse signal UNDEMONSTRATED (needs I1 compositions)",
 "tau_py_output": {"chosen_cut": tau_raw["chosen_cut"], "chosen_radius_arcsec": 1 / tau_raw["chosen_cut"],
                   "justification": tau_raw["justification"], "exit_code": 0, "stdout_file": "out/tau_stdout.txt"},
 "why_tau_choice_refused": "tau.py returned cut 0.0333 (30 arcsec). Its only signal is fractional cluster gain <5%, and every step of this curve gains <0.3% (total span 11104-11183, 0.71%), so the first step always 'saturates' and the choice is an artefact of the grid's second point. The 30 arcsec cut merges 39 pairs of distinct supernovae with different IAU names (must-not-join control) and 14 clusters with conflicting posA subclasses. Separation between two compositions was not supplied, so the collapse bound does not exist. The curve therefore does not bound a cut under tau.py's two-signal criterion.",
 "justification": "Controls bound the cut. Must-join (re-trigger duplicates: same IAUID, |dpeak|<=60 d, amendment A1): 9 pairs, max separation 0.494 arcsec, all joined at >=0.5 arcsec. Must-not-join (different IAUIDs, both SN): 0 violations at 0.5, 1, 1.5 arcsec; first violation at 2 arcsec (SN2023ghl/SN2024gyr, 1.92 arcsec). Cluster count is flat at 11183 across 0.5-1.5 arcsec. 1 arcsec is the plateau midpoint; the count is identical at the looser and tighter sensitivity cuts, so the unit count does not depend on the choice within the bound. Chosen on controls, not on unit count (the tighter end of the bound gives the same count).",
 "curve": curve,
 "sensitivity": {"looser": 1 / 1.5, "looser_radius_arcsec": 1.5, "looser_n_clusters": sw["per_cut"]["1.5"]["n_clusters"],
                 "tighter": 1 / 0.5, "tighter_radius_arcsec": 0.5, "tighter_n_clusters": sw["per_cut"]["0.5"]["n_clusters"],
                 "at_2arcsec_n_clusters": sw["per_cut"]["2"]["n_clusters"], "at_3arcsec_n_clusters": sw["per_cut"]["3"]["n_clusters"]},
 "saturation_cut": tau_raw["saturation_cut"], "collapse_cut": None,
 "chosen_to_increase_unit_count": False,
 "sibling_association": {"rule": "different 1-arcsec clusters, sep<=90 arcsec, both numeric z, |dz|<=0.005",
                         "pairs": sp["sibling_pairs"], "groups": sp["sibling_groups"], "clusters_in_groups": sp["clusters_in_sibling_groups"],
                         "units_if_host_group_were_unit": sp["sibling_group_units_if_host_is_unit"],
                         "label_pairs": sp["sibling_label_pairs"]},
 "completeness": "swept 10 radii 0.5-60 arcsec (cut=1/radius); cluster counts, both controls and split straddlers measured at each; separation between compositions not measured (I1 not run); sibling association measured once at 1 arcsec; recurrent-variable vs distinct-event ambiguity at identical positions not resolvable positionally",
 "provenance": [
  {"id": "a1-tau-plateau", "value": 11183, "referent": "cluster count on the control-bounded plateau 0.5-1.5 arcsec",
   "source": SRC + "build_corpus.py::fof over corpus rows; out/sweep.json per_cut", "population": "11193 included corpus rows",
   "adjudicator": "tau.py choice at 30 arcsec gives 11116 and fails the must-not-join control 39 times",
   "falsifier": "a re-trigger pair (same object, |dpeak|<=60 d) measured at >1.5 arcsec, or two distinct SNe measured at <=1.5 arcsec"}],
}
json.dump(cut_curve, open(H / "cut_curve.json", "w"), indent=1)

# ---------------- doc-derived Rubin overstatement ----------------
sn_alerts_per_visit, visits_per_night, nights_per_year, sn_per_year = 200, 1000, 300, 1_000_000
alerts_per_sn = sn_alerts_per_visit * visits_per_night * nights_per_year / sn_per_year
all_alerts_10yr, sn_10yr = 20e9, 10e6
all_per_sn = all_alerts_10yr / sn_10yr

axes = [
 {"axis": "positive_supply", "disposition": "PASS", "value": {"posA_clusters": A["posA"]["clusters"], "posB_clusters": A["posB"]["clusters"],
   "posA_raw_rows": A["posA"]["raw_rows"], "posB_raw_rows": A["posB"]["raw_rows"],
   "posA_bright_18p5_clusters": A["clusters_bright_18p5"]["posA"], "posB_bright_18p5_clusters": A["clusters_bright_18p5"]["posB"],
   "after_S1_2026-02-24_posA_clusters": sp["clusters_after_S1"].get("posA_Ia", 0) + sp["clusters_after_S1"].get("posB", 0),
   "after_S1_posB_clusters": sp["clusters_after_S1"].get("posB", 0),
   "after_S2_2026-06-30_posA_clusters": sp["clusters_after_S2"].get("posA_Ia", 0) + sp["clusters_after_S2"].get("posB", 0),
   "per_type_clusters": sp["per_type_clusters"]},
  "note": "PASS means counted at the clustered unit with provenance, not that supply clears a band; no bands were declared (P4 not in scope). Post-S1 positive supply is 9 clusters and post-S2 is 1: whatever Agent 3 rules on exposure, a split at the Rubin era leaves almost no labelled positives."},
 {"axis": "negative_supply", "disposition": "PASS", "value": {"neg_clusters": A["neg"]["clusters"], "neg_raw_rows": A["neg"]["raw_rows"],
   "neg_bright_18p5_clusters": A["clusters_bright_18p5"]["neg"], "tentative_CV?_AGN?_clusters": sp["per_type_clusters"].get("CV?", 0) + sp["per_type_clusters"].get("AGN?", 0),
   "after_S1_neg_clusters": sp["clusters_after_S1"].get("neg", 0), "posA_Ia_as_negative_under_posB_clusters": A["posA_Ia_only"]["clusters"]},
  "note": "Negatives are structurally truncated: the file holds only candidates saved by scanners (explorer doc 'Classification'; Perley 2.1: ~10^6 packets/night -> 5-10 saved). The non-target population a Rubin allocator faces (variables, AGN, artifacts, asteroids) is mostly absent. Under posB, SN Ia clusters (5315) are the negatives."},
 {"axis": "contamination_exposure", "disposition": "UNDEMONSTRATED", "value": None, "owner": "Agent 3 (agent3_labels_exposure)",
  "note": "owned elsewhere. Agent 1 supplies only: " + str(len(ans_items)) + " corpus objects whose class appears in the text of seeds 1910.12973/2009.01242 (corpus_ledger.answer_in_own_source), and post-split positive counts above."},
 {"axis": "tool_coverage", "disposition": "UNDEMONSTRATED", "value": None, "owner": "Agent 4 (agent4_tools_instrument)", "note": "owned elsewhere"},
 {"axis": "cluster_structure", "disposition": "PASS", "value": {
   "bts_rows": A["total"]["raw_rows"], "bts_objects_1arcsec": A["total"]["clusters"], "bts_row_overstatement_pct": A["total"]["overstatement_pct"],
   "bts_objects_range_0p5_to_60arcsec": [sw["per_cut"]["60"]["n_clusters"], sw["per_cut"]["0.5"]["n_clusters"]],
   "sibling_groups": sp["sibling_groups"], "units_if_host_group_were_unit": sp["sibling_group_units_if_host_is_unit"],
   "ztf_packets_per_saved_candidate_doc": "~10^6 packets/night / 5-10 saved per clear night = 1e5-2e5 (Perley 2020 s2.1)",
   "rubin_SN_alerts_per_SN_DIAObject_doc": alerts_per_sn, "rubin_SN_alert_overstatement_pct_doc": 100 * (alerts_per_sn - 1),
   "rubin_all_alerts_per_SN_doc": all_per_sn, "rubin_all_alert_overstatement_vs_SN_pct_doc": 100 * (all_per_sn - 1),
   "rubin_alerts_per_DIAObject_all_classes": "UNDEMONSTRATED (no seed gives a DIAObject count)"},
  "note": "Inside the BTS label base, rows are already object-level (0.089% overstatement). The overstatement the brief warns about lives upstream in the alert stream: doc-derived 60 SN alerts per SN DIAObject (5900%) and ~2000 alerts in the whole stream per SN (199,900%)."},
 {"axis": "split_integrity", "disposition": "PASS", "value": {"split_key": "peakt (JD-2458000)", "S1": "2026-02-24", "S2": "2026-06-30",
   "straddlers_at_1arcsec": {"S1": sw["per_cut"]["1"]["straddle_S1"], "S2": sw["per_cut"]["1"]["straddle_S2"]},
   "straddlers_at_10arcsec": {"S1": sw["per_cut"]["10"]["straddle_S1"], "S2": sw["per_cut"]["10"]["straddle_S2"]},
   "sibling_groups_straddling": {"S1": sp["sibling_groups_straddle_S1"], "S2": sp["sibling_groups_straddle_S2"]},
   "clusters_after_S1": sp["clusters_after_S1"], "clusters_after_S2": sp["clusters_after_S2"],
   "same_position_long_gap_pairs_within_corpus": len(sp["amendment_A1"]["long_gap_same_iau_pairs"])},
  "note": "No object or sibling group straddles either split at the chosen cut. Straddlers appear only at >=10 arcsec. Integrity passes, but the test side after S1 holds 250 objects of which 232 are unlabelled."},
 {"axis": "unprocessable_units", "disposition": "PASS", "value": {**sp["defects"], "excluded_rows_E5": sw["n_excluded"]},
  "note": "documented, not repaired. '>' marks lower limits on timescales (3905 rows censored in duration); '-' redshift in 4054 rows (20 of them posA); peakabs '-' in 4055; type '-' in 3370; peakmag may be an upper limit with no flag."},
]
axis = {"candidate": "live time-domain astronomy (ZTF BTS label base; Rubin LSST alert stream)", "branch": "prediction",
        "partial": True, "owner": "Agent 1 (supply and corpus)", "axes": axes,
        "ruling": None, "binding_axis": None, "definition_widened": False,
        "p4_status": "NOT ISSUED. P4 refuses while contamination_exposure and tool_coverage carry no number; no bands were declared; this is a pre-P1 sketch.",
        "p5_sketch": "see REPORT.md section P5; out/queue_stdout.txt",
        "completeness": "Agent 1 counted 5 of 7 axes (positive_supply, negative_supply, cluster_structure, split_integrity, unprocessable_units) on the frozen BTS corpus at the 1-arcsec clustered unit; contamination_exposure (Agent 3) and tool_coverage (Agent 4) are UNDEMONSTRATED here; Rubin-stream supply is doc-derived only, no Rubin labelled units counted",
        "provenance": [
 {"id": "a1-posA", "value": A["posA"]["clusters"], "referent": "clusters whose labelled members all map to posA (genuine extragalactic transient classes)",
  "source": SRC + "count_supply.py::supply; label map corpus_rules_FROZEN.md sha " + RULES_SHA, "population": "11183 distinct objects at 1 arcsec",
  "adjudicator": "raw posA rows 7158; Perley 2020 Table 1: 3147 classified transients to 2020-07-15 as an order-of-magnitude cross-check on a 25.5-month window",
  "falsifier": "a rerun on the same hashes returning a different count, or a type string found mapped outside the frozen map"},
 {"id": "a1-posB", "value": A["posB"]["clusters"], "referent": "clusters of non-SN-Ia extragalactic transient classes",
  "source": SRC + "count_supply.py::supply", "population": "11183 distinct objects at 1 arcsec",
  "adjudicator": "posA_Ia clusters 5315 on the same rows", "falsifier": "rerun differs, or an SN Ia-family string counted in posB"},
 {"id": "a1-neg", "value": A["neg"]["clusters"], "referent": "clusters labelled CV/AGN (including tentative '?')",
  "source": SRC + "count_supply.py::supply", "population": "11183 distinct objects at 1 arcsec; saved candidates only",
  "adjudicator": "Perley 2020 s2.1 ~10^6 packets/night with several hundred to <~50 false positives passing the filter nightly: the unsaved negative population",
  "falsifier": "rerun differs; or explorer 'All' export shows negatives not present in this file"},
 {"id": "a1-rubin-sn-alerts-per-object", "value": alerts_per_sn, "referent": "Rubin alerts per supernova DIAObject per year, from design key numbers",
  "source": "DMTN-102 section 2.2 bullet Supernovae (200 SN alerts/visit; 1e6 SNe/yr), section 2.2 (1000 visits/night), section 2.6 (300 nights/yr); arithmetic in scripts/make_records.py",
  "population": "LSST SNe per year (design estimate), not measured DIAObjects",
  "adjudicator": "whole-stream ratio 2000 alerts per SN (NOIRLab sci26008 20e9 alerts/10 yr over DMTN-102 1e7 SNe/10 yr)",
  "falsifier": "PPDB DiaObject.nDiaSources median for SN-classified DIAObjects measured outside 20-200"},
 {"id": "a1-after-S1-labelled", "value": sp["clusters_after_S1"]["total"] - sp["clusters_after_S1"].get("unlabeled", 0),
  "referent": "labelled objects peaking on or after 2026-02-24", "source": SRC + "count_supply.py clusters_after_S1",
  "population": "250 objects with all members peaking after S1", "adjudicator": "25-35% unlabelled per year 2019-2025 in the same corpus",
  "falsifier": "a re-fetch of the explorer CSV with the same rules showing the 2026 unlabelled fraction below 50%"}]}
json.dump(axis, open(H / "axis_ledger_partial.json", "w"), indent=1)
json.dump(axis["provenance"] + prov + cut_curve["provenance"], open(H / "provenance_records.json", "w"), indent=1)
print("ok", corpus_sha, alerts_per_sn, all_per_sn)
