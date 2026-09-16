#!/usr/bin/env python3
"""Agent 5: write the D4 slot records (k, delta prior, subject set), the D5 human-input record,
a flat provenance list for validate.py, and a partial domain_manifest for an honest ledger check.

Numbers that are arithmetic on source counts are computed here; numbers read from a source are
entered once with their locator. Locators are line numbers in this directory's sources/*.txt.

    python build_slots.py && python ../../../fm-advantage-benchmark/scripts/validate.py provenance ../slot_records_flat.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BTS = json.load(open(os.path.join(ROOT, "out", "bts_rounds.json")))

def rec(id_, value, referent, source, population, adjudicator, falsifier, **extra):
    r = {"id": id_, "value": value, "referent": referent, "source": source, "population": population,
         "adjudicator": adjudicator, "falsifier": falsifier}
    r.update(extra)
    return r

def slot(slot_name, value, status, prov, **extra):
    five = {k: prov[k] for k in ("referent", "source", "population", "adjudicator", "falsifier")}
    out = {"slot": slot_name, "value": value, "status": status, "provenance": five,
           "id": prov["id"]}
    out.update(five)          # top-level copy so validate.py provenance reads the same strings
    out.update(extra)
    return out

# ------------------------------------------------------------------ k
TRIG, NIGHTS, CAND_SRC = 327, 41, 251 + 1652
k_exact = TRIG / NIGHTS
cand_exact = CAND_SRC / NIGHTS
chance_exact = TRIG / CAND_SRC
k_prov = rec(
    "slot-k", 8,
    "number of candidate transients committed to spectroscopic follow-up (unique sources with an SEDM IFU "
    "request created by BTS scanners) per round, where a round is one observing night of the ZTF Bright "
    "Transient Survey under its post-2020 alert filter",
    "arXiv:2401.15167v1 section 4.1, sources/2401.15167.txt lines 757-766 (327 unique sources triggered by "
    "scanners with 2460175.5 < JD < 2460216.5) and section 4.2 lines 883-887, 953-958 (the same window is 41 "
    "nights); k_exact = 327/41 computed in scripts/build_slots.py; integer proposal by nearest-integer rounding "
    "of k_exact, recorded here as an amendment candidate for D5",
    "rounds = 41 consecutive calendar nights (JD 2460175.5 to 2460216.5, 2023-08-19 to 2023-09-29); 327 unique "
    "sources committed; not candidates, not alerts",
    "the other seed statements of per-night commitment: 5-15 assigned per night in 2018 (arXiv:1910.12973 "
    "section 2.2, lines 258-265), 5-10 saved on an average clear night (arXiv:2009.01242 section 2.1, lines "
    "147-148), median 4.5 per night for the automated bts_p1 policy (arXiv:2401.15167 section 4.2, lines "
    "953-958), about 10 SEDM spectra per night capacity (arXiv:1710.02917 section 7, line 1076)",
    "a BTS trigger log (Fritz SEDM request timestamps) for any other contiguous window of 30 or more nights "
    "whose unique-source triggers per night fall outside 4.5 to 10, or a window where more than half of the "
    "triggered sources are not in that window's candidate list, would show k differs from 8 or is not a "
    "per-round commitment",
    k_exact=round(k_exact, 4))
cand_prov = rec(
    "slot-k-candidates-per-round", round(cand_exact, 2),
    "number of distinct candidate sources available to the per-night commitment (sources with at least one "
    "public alert passing the BTS alert filter and BTSbot cleaning cuts inside the round window), per night",
    "arXiv:2401.15167v1 section 4.2, sources/2401.15167.txt lines 898-902 (4,031 alerts from 251 bright transients "
    "and 15,159 alerts from 1,652 non-bright transients, 2460175.5 < JD < 2460216.5); divided by 41 nights in "
    "scripts/build_slots.py",
    "1,903 distinct sources over the same 41 nights as slot-k; alerts (19,190) are not the unit",
    "the per-night statement in the same paper, about 50 new candidate BTS sources per night of which about 7 "
    "are new real bright transients (arXiv:2401.15167 section 1, lines 94-95); earlier filters passed about 500 "
    "(arXiv:2009.01242 section 2.1, lines 159-161) or a few hundred alerts per night (arXiv:1910.12973 section 2.2, "
    "line 219)",
    "a nightly count of sources passing the current BTS filter in a different 30-night window that differs from "
    "46 by more than a factor of two, or evidence that the 327 triggered sources are not a subset of the 1,903",
)
chance_prov = rec(
    "slot-k-chance", round(chance_exact, 4),
    "chance precision of a random k-of-candidates commitment per round, k over candidates per item",
    "scripts/build_slots.py: 327 / 1903 from arXiv:2401.15167v1 section 4.1 lines 757-766 and section 4.2 lines "
    "898-902 (same 41-night window); references/manifest.md 'Derived later' table defines chance as k over "
    "candidates per item",
    "the 41-night window of slot-k; ratio of two counts over the same rounds",
    "the stated per-night figures give 7/50 = 0.14 (arXiv:2401.15167 section 1, lines 94-95)",
    "a recount in which the triggered set is not contained in the candidate set, which would make the ratio "
    "exceed the fraction a random picker can reach and invalidate it as a chance level",
)
k_slot = slot("k", 8, "DERIVED", k_prov,
    population_unit="rounds (observing nights)",
    candidates_per_round=round(cand_exact, 2),
    chance=round(chance_exact, 4),
    supporting_records=[cand_prov, chance_prov],
    bts_csv_proxy={
        "what": "peaks per calendar night in the local BTS explorer file, a proxy only: peak night is not trigger night",
        "source": "scripts/bts_rounds.py -> out/bts_rounds.json, file sha256 " + BTS["sha256"],
        "mean_peaks_per_calendar_night_2019_2025": BTS["full_years_2019_2025"]["mean_peaks_per_calendar_night"],
        "median": BTS["full_years_2019_2025"]["median_peaks_per_calendar_night"],
        "p10_p90": BTS["full_years_2019_2025"]["p10_p90_peaks_per_calendar_night"],
        "fraction_nights_zero_peaks": BTS["full_years_2019_2025"]["fraction_nights_zero_peaks"],
        "candidates_per_night_from_this_file": "UNDEMONSTRATED: the file holds saved sources only; filter-passing rejects and save/trigger dates are absent",
    },
    peakt_zero_point={
        "value": "JD - 2458000",
        "derivation": ["documented: sources/bts_explorer_info.txt line 102 ('time: Time of peak, expressed as JD-2458000'), column named 'peakt' in the CSV header",
                       "documented independently: arXiv:1910.12973 Table 1 note d, line 476 (JD0 = JD - 2,458,000); arXiv:2009.01242 Figure 13 axis, line 1952",
                       "measured: with JD-2458000 the peak calendar year equals the IAU designation year or the next year for 96.27% of 11,110 named rows and 100% fall between 2018-03-01 and the fetch date; MJD, JD-2450000 and JD-2459000 give 0.00%, 0.00% and 0.06%",
                       "not separable by the data: JD-2458000.5 scores identically; only the documentation fixes the half day",
                       "range: 2018-05-04 to 2026-07-30 UTC, consistent with the explorer's 'peaked after 2018 May 1st' quality-cut text (line 16)"],
        "source": "scripts/bts_rounds.py::main peakt_zero_point_tests, out/bts_rounds.json",
    },
    disagreements=[
        "per-night commitment differs across seeds and eras: 5-15 (2018 filter), 5-10 saved on clear nights (2019-2020), 7.98 triggered per calendar night (2023 window), median 4.5 (automated policy), about 10 spectra per night (SEDM, 2016-2017, iPTF). Not reconciled.",
        "candidates per round: 46.4 measured sources per night (window) versus 'about 50 new candidates per night' stated; the measured figure counts sources active in the window, the stated one counts new sources.",
        "chance: 0.172 (window counts) versus 0.14 (stated per-night figures).",
        "k is not fixed per round in practice: 30.9% of calendar nights in 2019-2025 have zero peaks in the BTS file, and weather dominates (arXiv:1910.12973 footnote 9, lines 308-311).",
        "Rubin era: TiDES does not select k of n within a round; 4MOST fibres are not binding (about 12 live transients per field pass selection versus 30-35 LRS fibres per pointing; arXiv:2501.16311 section 3.5 lines 559-565 and footnote 20 line 630, section 2 lines 138-140) and it cannot operate target-of-opportunity. The k-of-candidates decision shape holds for single-object robotic spectrographs (SEDM), not for TiDES.",
        "the local BTS file has 11,217 data rows; data/raw/FETCH.md and PANEL_BRIEF.md state 11,218.",
        "the explorer documentation names the column 'time'; the CSV header names it 'peakt'.",
    ],
    undemonstrated=[
        {"what": "k and candidates per round for the Rubin LSST alert stream", "why": "no seed read in full reports a per-night commitment or candidate count for LSST-era spectroscopic follow-up; TiDES reports a 5-year total and per-field selection counts from simulation", "blocks": ["P6 chance for any LSST-stream item", "P7 N_min for an LSST-stream cohort"]},
        {"what": "ePESSTO+ per-night commitment", "why": "no arXiv survey paper for ePESSTO+ found by arXiv API query (abs:ePESSTO+); PESSTO/ePESSTO night allocations are stated in arXiv:1812.07401 line 94 but not per-night target counts", "blocks": []},
        {"what": "SOXS per-night commitment", "why": "arXiv:1812.07401 read in full states 900 NTT nights over 5 years (line 126) and a pipeline sized for 'one typical night (series of 15-30 min exposures)' (line 392) but no target count", "blocks": []},
    ],
    completeness="k from one 41-night trigger count with four corroborating seed statements; candidates per round and chance from the same window; LSST-era k, candidates and chance not demonstrated")

# ------------------------------------------------------------------ delta prior
d_main = rec(
    "slot-delta-prior", 0.018,
    "absolute difference in purity (precision) of the set of sources selected for SEDM follow-up, between two "
    "candidate selection models evaluated on the same test split, that practitioners acted on by choosing the "
    "production model",
    "arXiv:2401.15167v1 Appendix B Table 6, sources/2401.15167.txt lines 1323-1335 (bts_p2 purity MM-CNN 93.0%, "
    "NN 91.2%, UM-CNN 92.5%) and lines 1360-1364 ('advantage is ~0.5-2% ... even small boosts in purity are "
    "valuable'); production choice section 4.1 lines 655-662; difference 0.930-0.912 computed in scripts/build_slots.py",
    "BTSbot test split: 512 bright-transient sources and 1,489 other sources (Figure 4, line 420), less 70 junk "
    "and 59 single-alert sources (lines 704-714); paired over the same sources, discordant selections not published",
    "the fully-connected metadata-only network (NN) on the same test split, the strongest of the two alternatives "
    "on bts_p2 purity after the production model",
    "a rerun of the three published architectures (github.com/nabeelre/BTSbot) on a fresh contiguous window in "
    "which the MM-CNN minus NN purity difference falls outside 0 to 0.036, or a statement from BTS that the "
    "architecture choice was made on a criterion other than purity",
    feasibility_count="512 positive and 1,489 negative test-split sources; about 550 selected sources (512 / 0.930, derived) behind each purity",
    own_resolution_note=("unpaired MDE for two purities near 0.92 on about 550 selections each is about "
                         "2.80*sqrt(2*0.92*0.08/550) = 0.045; practitioners acted on 0.018, below that. Paired "
                         "MDE cannot be computed because discordant selections are not published."))
cand_records = [
    rec("delta-candidate-btsbot-vs-scanners", -0.037,
        "difference in follow-up purity between the adopted automated selector and human scanners",
        "arXiv:2401.15167v1 section 4.1 lines 757-766 (scanner triggering purity 96.7%, 316 of 327) and Figure 7 "
        "lines 739-742 (bts_p2 purity 93.0%); summary line 1132 ('93% vs ~97%'); adoption date line 886",
        "unequal: test-split sources for BTSbot versus a 41-night window of scanner triggers, with bright-transient "
        "purity on one side and extragalactic-transient purity on the other",
        "human scanners, the incumbent",
        "the same paper states scanner triggering purity as 95.6% at line 806 and 96.7% at line 766; a paired "
        "rerun of both selectors on one window would replace this number",
        disposition="REFUSED as a delta: an aggregate across unequal denominators (SKILL.md global refusal 4). "
                    "It shows practitioners adopting at a purity deficit, not acting on a gain."),
    rec("delta-candidate-sniascore-vs-snid", 0.37,
        "difference in true-positive rate at false-positive rate below 1% for SN Ia classification of SEDM "
        "spectra, SNIascore versus SNID, which led to deployment on 2021-04-15",
        "arXiv:2104.12980v2 Table 2, sources/2104.12980.txt lines 387-407 (TPR 0.90 versus 0.53); deployment "
        "section 7 lines 523-529; hard FPR requirement section 4.1 lines 298-299",
        "BTS18 validation sample, 1,016 SEDM spectra of 648 SNe (lines 190-196), paired on the same spectra",
        "SNID, the incumbent template matcher, on the same spectra",
        "a rerun on the 2020 testing set (1,011 spectra of 632 transients) giving a TPR gap below 0.30",
        disposition="adjacent referent: classification of a spectrum already taken, not selection of which "
                    "candidates receive a spectrum. Listed, not adopted."),
    rec("delta-candidate-fink-us-vs-rs", 0.30,
        "difference in SN Ia efficiency at similar purity between uncertainty sampling and random sampling "
        "training for the Fink early SN Ia module, which Fink deployed",
        "arXiv:2111.11438v2 Table 2, sources/2111.11438.txt lines 437-460 (efficiency 0.54 versus 0.24, purity "
        "0.89 versus 0.87); deployment section 5 lines 606-615",
        "test sample counted in alerts: 23,530 (abstract line 40), 23,425 (line 540) and 23,465 (line 679); "
        "15,751 unique objects after feature extraction (line 376), 1,021 SN Ia objects (line 130)",
        "random sampling, same pool, 100 realizations",
        "a per-object (not per-alert) recount whose efficiency gap falls below 0.15",
        disposition="population FAIL: counted over alerts, with three different test-set sizes in one paper. Listed, not adopted."),
]
delta_slot = slot("delta_prior", 0.018, "DERIVED", d_main,
    candidates=cand_records,
    metric_caveat="the benchmark decision metric is not preregistered (A1 has not run); this prior is on the purity-of-committed-set scale and applies only if A1 fixes precision at k as primary",
    d5_override_note="references/manifest.md: delta is the delta prior unless the human's cost of action overrides it; cost of action is not supplied (d5_inputs.json)",
    disagreements=[
        "an order of magnitude separates the values practitioners acted on: 0.018 (selection purity, architecture choice), 0.30 (Fink efficiency, alerts), 0.37 (SNIascore TPR). Not reconciled.",
        "the adoption of BTSbot over scanners happened at a purity deficit (93.0% versus 95.6% or 96.7%, both in one paper), i.e. practitioners traded purity for labour; the seeds show no adoption driven by a purity gain alone.",
        "practitioners acted on 0.018 while an unpaired MDE for that comparison is about 0.045 (own_resolution_note); the seeds act below their own resolution, which SKILL.md refusal 5 forbids for a directional claim.",
    ],
    completeness="one DERIVED on-referent prior with a feasibility count, three listed candidates with dispositions (one refused, one adjacent referent, one population FAIL); no LSST-era effect sizes found")

# ------------------------------------------------------------------ subject set
def member(name, api_id, cutoff, cutoff_kind, status, locator, note=""):
    return {"model": name, "api_id": api_id, "cutoff": cutoff, "cutoff_kind": cutoff_kind,
            "cutoff_status": status, "source": locator, "note": note}
members = [
    member("Claude Fable 5.1", "claude-fable-5-1", "2026-06", "reliable knowledge cutoff", "DERIVED (reliable-knowledge only); training-data cutoff UNDEMONSTRATED",
           "https://platform.claude.com/docs/en/models/overview fetched 2026-09-16, sources/anthropic_models_overview.txt lines 37 and 77-78",
           "Anthropic Transparency Hub (sources/anthropic_transparency.txt line 20) lists Claude Fable 5, not 5.1; no training-data cutoff for 5.1 found"),
    member("Claude Opus 5", "claude-opus-5", "2026-05", "reliable knowledge cutoff / knowledge cutoff date", "DERIVED",
           "sources/anthropic_models_overview.txt lines 38 and 77-79; sources/anthropic_transparency.txt lines 41-42",
           "same model family as the agents running this panel"),
    member("Claude Sonnet 5", "claude-sonnet-5", "2026-01", "reliable knowledge cutoff / knowledge cutoff date", "DERIVED",
           "sources/anthropic_models_overview.txt lines 39 and 77-80; sources/anthropic_transparency.txt lines 88-89"),
    member("GPT-6 Astra", "gpt-6-astra", "2026-04-30", "knowledge cutoff", "DERIVED",
           "https://developers.openai.com/api/docs/models fetched 2026-09-16, sources/openai_models.txt lines 658-674; sources/openai_gpt-6-astra.txt line 673"),
    member("GPT-5.6 Sol", "gpt-5.6-sol", "2026-02-16", "knowledge cutoff", "DERIVED",
           "sources/openai_models.txt lines 676-694"),
    member("Gemini 3.8 Flash", "gemini-3.8-flash", "2026-03 (some domains 2025-01)", "knowledge cutoff date, stated with a domain-dependent earlier limit", "DERIVED with internal disagreement",
           "https://deepmind.google/models/model-cards/gemini-3-8-flash/ fetched 2026-09-16, sources/deepmind_modelcard_gemini-3-8-flash.txt line 352",
           "the API model page (sources/google_gemini-3.8-flash.txt lines 241-243) gives only 'Latest update September 2026', which is not a cutoff"),
    member("Gemini 3.1 Pro (preview)", "gemini-3.1-pro-preview", None, None, "UNDEMONSTRATED",
           "sources/google_gemini-3.1-pro-preview.txt lines 242-245 (Latest update February 2026, not a cutoff); sources/deepmind_modelcard_gemini-3-1-pro.txt (no cutoff statement; defers training data to Gemini 3 Pro card line 197); sources/deepmind_modelcard_gemini-3-pro.txt (no cutoff statement found by search)",
           "preview status; Gemini API models page lists no stable Pro model in the Gemini 3 family (sources/google_gemini_models.txt lines 234-242)"),
]
ss_prov = rec(
    "slot-subject-set", [m["api_id"] for m in members],
    "frontier general-purpose models available through first-party APIs on 2026-09-16, with the training "
    "cutoff each provider states, for use as agent subjects",
    "first-party documentation fetched 2026-09-16: sources/anthropic_models_overview.txt, "
    "sources/anthropic_transparency.txt, sources/openai_models.txt, sources/openai_gpt-6-astra.txt, "
    "sources/google_gemini_models.txt, sources/deepmind_modelcard_gemini-3-8-flash.txt, "
    "sources/deepmind_modelcard_gemini-3-7-flash.txt, sources/deepmind_modelcard_gemini-3-1-pro.txt, "
    "sources/deepmind_modelcard_gemini-3-pro.txt (raw HTML beside each .txt)",
    "7 models from 3 providers (flagship and next tier per provider as each provider's own models page ranks "
    "them); open-weight models not surveyed",
    "no required rung is stated by any seed or by the panel brief, so availability is the only criterion; the "
    "strongest alternative subject is the best classical-tool arm, which is a composition, not a model",
    "a first-party page, model card or system card dated on or before 2026-09-16 stating a different cutoff for "
    "any member, or listing a more capable generally available model from these providers that is missing here",
)
subject_set_slot = slot("subject_set", [m["api_id"] for m in members], "DERIVED", ss_prov,
    members=members,
    required_rung="none stated in any seed read or in PANEL_BRIEF.md",
    exposure_consequence={
        "what": "BTS explorer rows peaking after each cutoff (supporting count; exposure is agent3's axis)",
        "source": "scripts/bts_rounds.py -> out/bts_rounds.json rows_peaking_on_or_after_cutoff_plus_one_day",
        "counts": BTS["rows_peaking_on_or_after_cutoff_plus_one_day"],
        "reading": "if every member's cutoff binds, only rows peaking after 2026-06-30 are unexposed to all: 30 rows, 1 classified transient in the file fetched 2026-09-16",
    },
    disagreements=[
        "cutoff referent differs by provider: Anthropic states 'reliable knowledge cutoff', OpenAI 'knowledge cutoff', Google a 'knowledge cutoff date' with an earlier domain-dependent limit. None states the last date of training data, which is what an exposure key needs.",
        "Claude Fable 5.1 appears on the models overview with a June 2026 reliable-knowledge cutoff, but the Transparency Hub lists only Claude Fable 5 (January 2026).",
        "Gemini 3.8 Flash: March 2026 and January 2025 in one sentence of its model card.",
    ],
    undemonstrated=[
        {"what": "training-data cutoff (as opposed to knowledge cutoff) for every member", "blocks": ["exposure key ruling at D2/P3 for items peaking between a member's knowledge cutoff and its true training-data end"]},
        {"what": "Gemini 3.1 Pro cutoff", "blocks": ["including Gemini 3.1 Pro in any contamination-controlled arm"]},
        {"what": "open-weight frontier models", "blocks": ["subject-set completeness claim; recorded as an inventory of three providers only"]},
    ],
    completeness="three first-party providers surveyed from their own documentation on 2026-09-16; open-weight and other providers not surveyed; cutoffs are knowledge cutoffs, not training-data ends")

# ------------------------------------------------------------------ D5 inputs
def und(id_, referent, source, population, adjudicator, falsifier, must_supply, why_corpus_cannot, blocks):
    r = rec(id_, None, referent, source, population, adjudicator, falsifier)
    r.update({"status": "UNDEMONSTRATED", "human_must_supply": must_supply,
              "why_the_corpus_cannot_supply_it": why_corpus_cannot, "blocks": blocks})
    return r
d5 = {"id": "d5-inputs", "records": [
    und("d5-budget", "hours or cells the programme can spend on this benchmark",
        "references/manifest.md 'Supplied by you at D5'; references/stages/discovery.md D5; not supplied as of 2026-09-16 per PANEL_BRIEF.md 'Status of this run'",
        "the human programme running the benchmark, not the corpus",
        "none: no budget has been proposed, so there is no weaker or stronger alternative to price against",
        "a written budget from the human that differs from any figure later used to size the cohort would show the sizing was not grounded",
        "a number in agent-arm cells (one cell = one subject x one arm x one round) or wall-clock hours, with the arms counted (FM-tool agent, classical-tool agent, mechanical composition)",
        "the seeds record what BTS, TiDES and SEDM spent (e.g. 900 NTT nights over 5 years for SOXS, arXiv:1812.07401 line 126; 250,000 fibre-hours for TiDES, arXiv:2501.16311 line 43), which are telescope budgets of other programmes, not the compute and review hours this programme has",
        ["S", "P5 queue loop escape", "P7 N_min versus affordable N", "R1 onward (no paid work on an unratified manifest)"]),
    und("d5-cost-of-action", "cost to this programme of committing one follow-up slot to a wrong candidate, and of missing a right one, expressed so a minimum decision-relevant effect can be read from it",
        "references/manifest.md 'Supplied by you at D5' ('the seeds show what others act on, not what you would act on'); not supplied as of 2026-09-16",
        "the human's own follow-up programme",
        "the delta prior (delta_slot.json, 0.018 on committed-set purity), which stands unless this overrides it",
        "a supplied cost of action whose implied minimum effect falls below every MDE in a measured power record at the budgeted N would close the candidate at P7; until one is supplied that ruling is unmade",
        "either (a) the smallest improvement in committed-set precision (or the preregistered metric) that would change which tool the programme uses, or (b) the telescope time per spectrum and the value of a correct versus wrong classification from which (a) follows",
        "the corpus gives other programmes' costs, such as a typical SEDM classification exposure of 1800 s at m about 18.5 (arXiv:1910.12973 section 2.3, lines 336-337), but not the value the human places on a slot or the effect that would change the human's decision",
        ["delta override", "P7 ruling", "A4 claim threshold"]),
    und("d5-S", "survivor target S = budget / measured hours per workflow",
        "references/manifest.md ('S, the survivor target, is budget divided by measured hours per workflow'); references/graph.md D5 -> R1",
        "workflows (one scored item through all arms)",
        "none until hours per workflow are measured at R1; the source record repriced its cohort from about 17 to 37 hours (references/manifest.md)",
        "a measured hours-per-workflow figure from an R1 control run that, divided into the supplied budget, disagrees with any S used earlier",
        "budget (above); hours per workflow is measured at R1, not supplied",
        "S depends on this programme's budget and on its own harness speed, neither of which appears in any seed",
        ["P5 escape condition", "cohort sizing", "the choice among N rows in planning_mde_bracket.csv"]),
], "completeness": "budget, cost of action and S recorded UNDEMONSTRATED with what the human must supply; hours per workflow not measured (R1 not run)"}

flat = [k_prov, cand_prov, chance_prov, d_main] + cand_records + [ss_prov] + d5["records"]
manifest_partial = {
    "tau": None, "label_source": None, "exposure_key": None, "tool_inventory": None, "frozen_hash": "",
    "k": {"value": k_slot["value"], "provenance": k_slot["provenance"], "status": "DERIVED"},
    "delta": {"value": delta_slot["value"], "provenance": delta_slot["provenance"], "status": "DERIVED"},
    "subject_set": {"value": subject_set_slot["value"], "provenance": subject_set_slot["provenance"], "status": "DERIVED"},
    "S": {"value": None, "provenance": {k: d5["records"][2][k] for k in ("referent", "source", "population", "adjudicator", "falsifier")}, "status": "UNDEMONSTRATED"},
    "candidates": ["live time-domain astronomy: ZTF BTS + Rubin LSST, prediction branch"],
    "completeness": "partial manifest from agent5 only: tau, label_source, exposure_key, tool_inventory belong to other agents and are absent here; not frozen, not hashed",
}
for name, obj in [("k_slot.json", k_slot), ("delta_slot.json", delta_slot), ("subject_set_slot.json", subject_set_slot),
                  ("d5_inputs.json", [dict(r, set_completeness=d5["completeness"]) for r in d5["records"]]), ("slot_records_flat.json", flat), ("out/domain_manifest_partial_agent5.json", manifest_partial)]:
    json.dump(obj, open(os.path.join(ROOT, name), "w"), indent=2)
    print("wrote", name)
