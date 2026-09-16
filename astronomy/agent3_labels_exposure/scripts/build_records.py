#!/usr/bin/env python3
"""Build label_source_slot.json, exposure_key_slot.json, contamination_axis.json and the flat
provenance_records.json from derived_counts.json (written by labels_exposure.py).
Run after labels_exposure.py:  python3 scripts/build_records.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
D = json.loads((HERE / "derived_counts.json").read_text())
N = D["unique_ztfid"]
LAB = D["labeled_objects"]
B = D["label_basis_counts"]
pct = lambda a, b: round(100.0 * a / b, 2)
RAWSRC = f"astronomy/data/raw/ztf_bts_all_2026-09-16.csv sha256 {D['raw_sha256']}"
SCRIPT = "astronomy/agent3_labels_exposure/scripts/labels_exposure.py::main"

# ------------------------------------------------------------------ label source
shares = {
    "population_unique_ztfid_pre_clustering": N,
    "unlabeled": dict(n=B["unlabeled"], pct_of_all=pct(B["unlabeled"], N)),
    "labeled": dict(n=LAB, pct_of_all=pct(LAB, N)),
    "spectroscopic_transient_class": dict(n=B["spectroscopic_transient_class"], pct_of_all=pct(B["spectroscopic_transient_class"], N), pct_of_labeled=pct(B["spectroscopic_transient_class"], LAB),
                                          basis="Perley+2020 Fig.3 caption: public classifications are always spectroscopic for SNe/transients"),
    "spectroscopic_with_photometric_criterion": dict(n=B["spectroscopic_with_photometric_criterion"], pct_of_all=pct(B["spectroscopic_with_photometric_criterion"], N), pct_of_labeled=pct(B["spectroscopic_with_photometric_criterion"], LAB),
                                                     classes="SLSN-I, SLSN-II (luminosity threshold), SN IIP (photometric subtype), SN Ia-91T (photometric evidence admissible)"),
    "variable_AGN_CV_spectroscopic_or_photometric_only_unresolved": dict(n=B["variable_spectroscopic_or_photometric_unresolved"], pct_of_all=pct(B["variable_spectroscopic_or_photometric_unresolved"], N), pct_of_labeled=pct(B["variable_spectroscopic_or_photometric_unresolved"], LAB),
                                                                         basis="Perley+2020 sec 2.4 permits photometric-only AGN and dwarf-nova classification"),
    "tentative_AGN?_CV?_basis_undocumented": dict(n=B["tentative_variable_basis_undocumented"], pct_of_all=pct(B["tentative_variable_basis_undocumented"], N), pct_of_labeled=pct(B["tentative_variable_basis_undocumented"], LAB)),
    "model_annotation_SNIascore": dict(status="UNDEMONSTRATED", lower_bound=0, upper_bound=D["sniascore"]["plain_SN_Ia_peak_on_or_after_deploy_minus_30d"],
                                       upper_bound_pct_of_labeled=pct(D["sniascore"]["plain_SN_Ia_peak_on_or_after_deploy_minus_30d"], LAB),
                                       excluded_by_phase_and_deploy_date=D["sniascore"]["plain_SN_Ia_peak_before_deploy_minus_30d"],
                                       plain_SN_Ia_total=D["sniascore"]["plain_SN_Ia"],
                                       known_member="ZTF21aastazz / SN2021ijb, first automated SNIascore classification (arXiv:2104.12980 sec 7), file type 'SN Ia'"),
    "reported_by_other_TNS_groups": dict(status="UNDEMONSTRATED", unresolved_objects=D["reporter_group_unresolved_labeled_objects"],
                                         only_published_share="56 of 761 (7.4%) BTS 2018 SNe classified from public TNS spectra of other groups (arXiv:1910.12973 sec 3.1); 2018 only, not the file"),
    "human_SNID_assisted_spectroscopic_by_BTS": dict(status="UNDEMONSTRATED", note="cannot be separated from other-group and SNIascore reports without TNS classification reports"),
    "photometric_or_inferred_resolvable_count": dict(status="UNDEMONSTRATED", unresolved_objects=B["variable_spectroscopic_or_photometric_unresolved"] + B["tentative_variable_basis_undocumented"]),
}
label_prov = dict(
    referent="basis of each object's current BTS 'type' label (spectroscopic human-adjudicated vs model annotation vs photometric/inferred vs other-group report), counted over unique ZTFID",
    source=f"{SCRIPT} basis(); {RAWSRC}; class-to-basis map from arXiv:1910.12973 sec 3.1 & 3.3 (sources/1910.12973.raw.txt lines 551-605, 1115-1179), arXiv:2009.01242 sec 2.2, 2.4, Fig.3, App.E (sources/2009.01242.raw.txt lines 244-248, 677-691, 912, 3308-3310), arXiv:2104.12980 sec 7 (sources/2104.12980.raw.txt lines 869-886), sources/bts_explorer_info.txt line 86",
    population=f"{N} unique ZTFID rows (pre-clustering; Agent 1 owns clustering; {D['iauid_shared_by_2plus_ztfid']} IAU names are shared by 2 ZTFIDs, so clustered n is at most {N - D['iauid_shared_by_2plus_ztfid']})",
    adjudicator="TNS classification reports (reporter group, bot flag, report date) per object, which would replace every UNDEMONSTRATED share here; not reachable without credentials (HTTP 403 on wis-tns.org pages and bulk CSV, 401 on api/get/object, 2026-09-16)",
    falsifier="TNS classification reports showing that a class mapped here as spectroscopic was assigned photometrically, or that SNIascore-reported SN Ia exceed the upper bound of 3131, or a rerun of labels_exposure.py on the same sha256 returning different counts",
)
label_slot = dict(
    slot="label_source", candidate="live time-domain astronomy (Rubin LSST alerts + ZTF BTS labels)",
    status="UNDEMONSTRATED",
    status_reason="class-level basis shares are DERIVED; the load-bearing split between human spectroscopic classification, SNIascore model annotation and other-group TNS reports is not in the file and TNS is not reachable without credentials",
    value=dict(
        bts_shares=shares,
        rubin_era=dict(
            broker_classifications=dict(kind="annotation (model output)", examples="ALeRCE, Fink and other Rubin-endorsed brokers", locator="sources/RTN-011.txt lines 2773-2778 (brokers provide 'preliminary classifications of transient and variable sources')"),
            tns_spectroscopic_classification=dict(kind="measured spectrum with adjudicated class", caveat="a TNS classification report can itself come from an automated classifier (SNIascore reports to TNS without human interaction, sources/2104.12980.raw.txt lines 869-886); per-report reporter/bot identity must be checked before counting it as measured"),
            rubin_photometric_class=dict(kind="annotation", note="no Rubin project classification of alerts is described in RTN-011; classifications in the stream are broker added-value")),
        label_instability=dict(
            SN2018cne=dict(ztfid="ZTF18aaxmhvk", file_type="SN Ia", paper_statement="BTS officially classified this as a SN Ic (arXiv:2104.12980 sec 6, sources/2104.12980.raw.txt line 824)"),
            labels_changed_since_2024_12_08_capture=D["exposure_split_all_demonstrated_subjects"]["unresolved_breakdown"]["label_changed_since_capture"],
            labels_changed_since_2025_08_10_capture=D["exposure_split_excluding_haiku45"]["unresolved_breakdown"]["label_changed_since_capture"],
            BTS_TNS_labels_preliminary="sources/1910.12973.raw.txt line 565; sources/2009.01242.raw.txt line 840"),
        resolves_with="TNS classification reports per object (reporter group, 'Bot' flag, report date) via the TNS API with a registered bot or user account, or the TNS bulk CSV with credentials",
    ),
    provenance=label_prov,
)

# ------------------------------------------------------------------ exposure key
S1 = D["exposure_split_all_demonstrated_subjects"]
S2 = D["exposure_split_excluding_haiku45"]
exp_prov = dict(
    referent="per-object date on which the BTS label became publicly readable, bracketed, compared with each candidate subject's published knowledge cutoff",
    source=f"{SCRIPT} split(); lower bound = TNS discovery date (sources/bts_all_extracols_2026-09-16.csv sha256 {D['extra_sha256']}, 'discdate'); upper bound = Internet Archive capture of the public explorer showing the same type string (sources/wayback_bts_explorer_20241208231331.html sha256 {D['captures']['2024-12-08T23:13:31']['sha256']}, sources/wayback_bts_explorer_20250810065056.html sha256 {D['captures']['2025-08-10T06:50:56']['sha256']}); input-data release: sources/ztf_public_releases.txt lines 104, 301; sources/RTN-011.txt lines 2468, 2773, 1288; cutoffs: sources/anthropic_models_overview.txt line 49, sources/anthropic_transparency.txt lines 34, 69, 104, 348, sources/openai_models.txt lines 660-729, sources/deepmind_modelcard_gemini-3-8-flash.txt line 243",
    population=f"{LAB} labeled objects out of {N} unique ZTFID (pre-clustering); subjects: {len(D['subjects'])} candidate models, {len(D['cutoff_bounds']['subjects_undemonstrated'])} without a published cutoff",
    adjudicator="TNS classification report dates per object (exact public date of each label), which would collapse the bracket to a point; not reachable without credentials",
    falsifier="a TNS classification report dated after 2024-12-08 for an object counted 'before' with an unchanged type, or a subject whose training data (not reliable-knowledge cutoff) is documented to end before the object's label date, or a rerun on the same hashed files returning different counts",
)
exposure_slot = dict(
    slot="exposure_key", candidate="live time-domain astronomy (Rubin LSST alerts + ZTF BTS labels)",
    status="DERIVED",
    status_note="key definition and brackets are derived from release metadata; exact classification-report dates are UNDEMONSTRATED for the unresolved objects listed; one candidate subject has no published cutoff",
    value=dict(
        key_definition=dict(
            input_public_date=dict(ztf="alert issuance: ZTF alerts public in real time, public distribution began 2018-06-04 (sources/ztf_public_releases.txt lines 104, 301)",
                                   rubin="alert issuance: alerts world-public (sources/RTN-011.txt lines 554, 2773); first Rubin alerts 2026-02-24 (line 2468); PPDB not public at alert start, expected Sep-Oct 2026 (lines 2471, 2597); no PPDB release post in the Rubin News category through 2026-09-15 (sources/rubin_community/news_category_topic_list_2026-09-16.json)"),
            label_public_date=dict(lower_bound="TNS discovery date (a classification report attaches to an existing TNS object)",
                                   upper_bound="earliest archived public explorer capture showing the same type string; otherwise the fetch date 2026-09-16",
                                   exact="TNS classification report date, UNDEMONSTRATED (TNS 403/401 without credentials)"),
            peakt_zero_point=dict(value="JD - 2458000", derivation=["sources/bts_explorer_info.txt line 79 'Time of peak, expressed as JD-2458000'",
                                                                    "sources/1910.12973.raw.txt line 854 'JD0 = JD - 2,458,000'",
                                                                    "sources/2009.01242.raw.txt line 3154 axis 'Observed peak time (JD-2458000)'",
                                                                    D["peakt_known_objects"], D["peakt_zero_point_test"]],
                                  disagreement="panel brief suggested days since 2018-01-01; that offset puts SN2018cne peak on 2018-10-18 against a stated maximum-light spectrum on 2018-06-14 and gives a median peak-minus-discovery lag of 130 d instead of 11 d")),
        subject_cutoffs=D["subjects"],
        cutoff_bounds=D["cutoff_bounds"],
        cutoff_caveats=["Anthropic pages state 'reliable knowledge cutoff'; no training-data cutoff was readable from a primary page, so 'after every cutoff' is an upper-bound claim on exposure, not proof of absence from training data",
                        "OpenAI 'knowledge cutoff' is not defined on the page read as a training-data end",
                        "Claude Fable 5.1 (Jun 2026) appears on the models overview but not in the Transparency Hub, which lists Claude Fable 5 at Jan 2026",
                        "Gemini 3.1 Pro has no cutoff on the pages read; any claim over 'every subject' that includes it is UNDEMONSTRATED",
                        "subjects with web search at inference read TNS directly; exposure then depends on the grant (R4), not the cutoff"],
        split_all_demonstrated_subjects=S1,
        split_excluding_claude_haiku_4_5=S2,
        rubin_dates=dict(first_alerts="2026-02-24 (sources/RTN-011.txt line 2468)",
                         lsst_start="night of 2026-06-29 (sources/RTN-011.txt line 1288; sources/rubin_community/2026-07-10_2026-07-10-early-operations-update-start-of-lsst.md), announced 2026-06-30 (sources/rubin_community/2026-06-30_the-lsst-has-started.md)",
                         off_sky="summit evacuated 2026-07-14/15 for a winter storm; still off sky with no return-to-sky date as of 2026-09-11 (sources/rubin_community/2026-07-24_lsst-update-2026-07-24.md; 2026-09-11_summit-technical-progress-week-ending-2026-09-11.md)"),
    ),
    provenance=exp_prov,
)

# ------------------------------------------------------------------ contamination axis
contam = dict(
    axis="contamination_exposure",
    candidate="live time-domain astronomy (Rubin LSST alerts + ZTF BTS labels)",
    stage="P3", note_on_order="pre-clustering count; D3 cut curve (Agent 1) not applied, so graph edge D3->P3 is unmet and the clustered figure is UNDEMONSTRATED",
    raw_unit="unique ZTFID (the file carries one row per ZTFID; alert counts are not in the file)",
    raw_n=N, clustered_n="UNDEMONSTRATED (Agent 1)", labeled_n=LAB,
    value=dict(
        all_demonstrated_subjects=dict(cutoff_window=S1["cutoff_window"], before_every_cutoff=S1["label_public_before_every_cutoff"],
                                       after_every_cutoff=S1["label_public_after_every_cutoff"], unresolved=S1["unresolved"],
                                       before_pct_of_labeled=pct(S1["label_public_before_every_cutoff"], LAB), unresolved_breakdown=S1["unresolved_breakdown"]),
        excluding_claude_haiku_4_5=dict(cutoff_window=S2["cutoff_window"], before_every_cutoff=S2["label_public_before_every_cutoff"],
                                        after_every_cutoff=S2["label_public_after_every_cutoff"], unresolved=S2["unresolved"],
                                        before_pct_of_labeled=pct(S2["label_public_before_every_cutoff"], LAB), unresolved_breakdown=S2["unresolved_breakdown"]),
        labeled_objects_discovered_after_latest_cutoff=S1["label_public_after_every_cutoff"],
        all_objects_discovered_on_or_after_2026_07_01=D["discovery_on_or_after_2026_07_01_all"],
        labeled_objects_discovered_on_or_after_2026_07_01=D["discovery_on_or_after_2026_07_01_labeled"],
        all_labeled_units_predate_latest_cutoff=D["all_units_predate_all_subjects"],
    ),
    disposition="FAIL",
    disposition_reason="zero labeled BTS units have a label public after every demonstrated subject cutoff; at least 6166 of 7843 (78.6%) demonstrably had their current label publicly displayed before every demonstrated cutoff, and the remaining 1677 cannot be placed after (every one was discovered on or before 2026-06-30). The skill's typical failure (all units predate all subjects) holds for every unit whose exposure is determinable. Contamination is disclosed, not solved.",
    rubin_prospective=dict(
        offers="objects first detected on or after 2026-07-01 (after the last day of the latest demonstrated cutoff month, Jun 2026) whose labels do not yet exist: label and light curve both post-date every demonstrated cutoff",
        count="UNDEMONSTRATED (Rubin post-cutoff object counts need broker or PPDB queries; PPDB not yet public per RTN-011 lines 2597, 2761)",
        window_so_far="LSST nights 2026-06-29 to 2026-07-14 before storm evacuation (about 16 nights, with weather loss); 2026-06-29 and 2026-06-30 fall inside Claude Fable 5.1's Jun 2026 cutoff month and are not after every cutoff; off sky through at least 2026-09-11 with no return date",
        does_not_solve=["host-galaxy redshifts and host photometry predate every cutoff (catalogs such as NED/SDSS; 44% of 2018 BTS SN Ia hosts had a catalogued redshift before discovery, sources/1910.12973.raw.txt lines 44-50)",
                        "archival photometry and prior variability history at the position (PS1, ZTF data releases through DR24 Oct 2025, sources/ztf_public_releases.txt) predate cutoffs and can reveal AGN/CV nature",
                        "TNS names are issued at report time and the SN prefix is assigned on spectroscopic SN classification: in this file 6994 of 7252 SN-prefixed names carry an SN/SLSN label, so an identifier leaks the class",
                        "class priors and population rates (e.g. SN Ia fraction of a magnitude-limited sample) are in pre-cutoff literature",
                        "labels still arrive through TNS, where some are model annotation (SNIascore-type bots); prospective does not make a label measured",
                        "subjects with web access can read the label once filed; the decision must be sealed before the classification report is public",
                        "subject cutoffs are reliable-knowledge dates, not training-data end dates, and one subject has no published cutoff"],
    ),
    provenance=dict(
        referent="count of labeled objects whose label was publicly readable before every candidate subject's cutoff, after every cutoff, or unresolved",
        source=exp_prov["source"],
        population=f"{LAB} labeled of {N} unique ZTFID, pre-clustering (raw rows = unique ZTFID; overstatement vs clustered n UNDEMONSTRATED until Agent 1's cut; {D['iauid_shared_by_2plus_ztfid']} shared IAU names bound it at >= {D['iauid_shared_by_2plus_ztfid']} duplicate rows)",
        adjudicator="exact TNS classification-report dates for the 1677 unresolved objects; a prospective Rubin stream counted after 2026-07-01",
        falsifier="any labeled object in the file with a TNS classification report dated after 2026-06-30 and discovery after 2026-06-30 (would make after_every_cutoff nonzero), or a rerun of labels_exposure.py on the same hashed inputs returning different counts",
    ),
)

for name, obj in [("label_source_slot.json", label_slot), ("exposure_key_slot.json", exposure_slot), ("contamination_axis.json", contam)]:
    (HERE / name).write_text(json.dumps(obj, indent=1, default=str))

flat = [dict(id="agent3-label-source", value=label_slot["status"], **label_prov),
        dict(id="agent3-exposure-key", value=f"before {S1['label_public_before_every_cutoff']} / after {S1['label_public_after_every_cutoff']} / unresolved {S1['unresolved']}", **exp_prov),
        dict(id="agent3-contamination-axis", value=contam["disposition"], **contam["provenance"]),
        dict(id="agent3-peakt-zero-point", value="JD-2458000",
             referent="zero point of the BTS 'peakt' column",
             source="sources/bts_explorer_info.txt line 79; sources/1910.12973.raw.txt line 854; scripts/labels_exposure.py::main peakt_known_objects",
             population=f"{D['peakt_zero_point_test']['JD-2458000 (explorer_info.txt line 79; Fremling+2020 Table 1 note d)']['n']} rows with numeric peakt, IAU year and discovery date; 1 known object with a stated maximum-light date in the file",
             adjudicator="days since 2018-01-01 (panel brief), which gives SN2018cne peak 2018-10-18 against a stated 2018-06-14 maximum",
             falsifier="a BTS documentation revision stating a different offset, or objects whose peak date under JD-2458000 differs from independently published maximum-light dates by more than 30 d"),
        dict(id="agent3-sniascore-upper-bound", value=D["sniascore"]["plain_SN_Ia_peak_on_or_after_deploy_minus_30d"],
             referent="upper bound on labeled objects whose SN Ia label could have been produced by SNIascore",
             source="scripts/labels_exposure.py::main sniascore; sources/2104.12980.raw.txt lines 279 (phase range) and 869 (deployment 2021-04-15)",
             population=f"{D['sniascore']['plain_SN_Ia']} objects typed exactly 'SN Ia' of {N} unique ZTFID",
             adjudicator="TNS classification reports with reporter 'SNIascore' / bot flag per object",
             falsifier="a SNIascore TNS report for an object peaking more than 30 d before 2021-04-15, or a count of SNIascore reports among file objects that exceeds the bound"),
        ]
(HERE / "provenance_records.json").write_text(json.dumps(flat, indent=1, default=str))
print("wrote records")
