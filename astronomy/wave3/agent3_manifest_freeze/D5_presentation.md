# D5 presentation: manifest v1 (wave-2 brief)

- **Manifest:** `domain_manifest_v1.json`, frozen_hash `ca00efe05b7562237839259a50597e7c2825292e3f4ccf84444607c50c3cbae8`.
- **Hash method:** sha256 over json.dumps(manifest with frozen_hash set to "", sort_keys=True, separators=(',', ':'), ensure_ascii=False) encoded UTF-8; file on disk is indent=1 pretty print, which is not hashed; verify with scripts/verify_hash.py.
- **Governing brief:** `astronomy/wave2/PANEL_BRIEF_WAVE2.md`, sha256 `31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb` (verified).
- **Amendment ledger:** `amendment_ledger.json`, v1 entries canonical sha256 `9643f2d47f458e02a213f1e8ef28d1b0305ccd8814571ff2fdc269e389c6192d`.

Below, each slot is shown with its derivation, its five provenance fields (copied verbatim from the frozen file) and its status, followed by an explicit invitation to override. Ratification means accepting or correcting a derivation already on the page (discovery.md D5). Any override, with its reason, becomes a new amendment-ledger entry and a new hashed manifest version. v1 itself is never edited.

## Status at a glance

| Slot | v1 value | Status | Ledger |
|---|---|---|---|
| tau | 1 arcsec | **DERIVED** | none (no PI ruling) |
| k | 8 | **RATIFIED** | AMD-V1-01 |
| label_source | SNIascore 803-2,247; 6,156 unresolved | **UNDEMONSTRATED** | SU-V1-01 |
| exposure_key | alert issuance / bracketed label date | **DERIVED** | none (no PI ruling) |
| tool_inventory | 25 channels, Fink RF remap on 3 Rubin rows | **OVERRIDDEN** | AMD-V1-03 |
| delta | 0.018 (resolution warning) | **DERIVED** | AMD-V1-05 |
| S | none | **UNDEMONSTRATED** | AMD-V1-06 |
| subject_set | 7 models | **DERIVED** | none (no PI ruling) |
| decision_epoch | first alert / night 3 | **RATIFIED** | AMD-V1-02 |

**D5 disposition: UNDEMONSTRATED (does not advance).**
- **Freeze:** PASS. The manifest is frozen and hashed.
- **Every slot ratified or overridden:** FAIL. tau, exposure_key and subject_set are still DERIVED, delta is DERIVED, and label_source and S are UNDEMONSTRATED.
- **Disagreement with the brief:** brief line 35 expects D5 to close except for the SUPPLY fields, but the PI decisions rule only on k, the decision epoch and the remapping. This freeze does not ratify anything on the PI's behalf. Listed, not reconciled.

## tau

**Value (v1):** `{"radius_arcsec": 1.0, "n_clusters_bts": 11183, "plateau_arcsec": [0.5, 1.5]}`

**Status:** DERIVED. Not ruled on in PANEL_BRIEF_WAVE2.md. The separation-collapse bound (the second D3 signal) is UNDEMONSTRATED until I1 compositions exist.

**Derivation.** Agent 1 swept 10 radii (0.5 to 60 arcsec) over the 11,193 included BTS rows and recorded cluster count plus two controls at each radius. Must-join: re-trigger duplicates (same IAU name, peaks within 60 d; amendment A1). Must-not-join: distinct supernovae with different IAU names. Cluster count is flat at 11,183 from 0.5 to 1.5 arcsec with zero must-not-join violations. The first violation is at 2 arcsec (SN2023ghl and SN2024gyr, 1.92 arcsec). 1 arcsec is the plateau midpoint, and the count is the same at the looser and tighter sensitivity cuts, so the choice does not raise the unit count. `tau.py` picked 30 arcsec. That pick was refused: every step of the curve gains under 0.3%, and 30 arcsec merges 39 distinct-SN pairs. For Rubin, bands_FROZEN.md section 2 applies the same 1 arcsec cut plus the 60 d clause to diaObjectIds. The second D3 signal, separation collapse, needs I1 compositions and is UNDEMONSTRATED.

**Provenance (five fields):**

- **referent:** similarity cut that defines the independent unit (distinct astrophysical object) for clustering and every count
- **source:** astronomy/agent1_supply_corpus/cut_curve.json sha256 32a666c8aae6b48e4ce5c69cec4749935d58f0d8bfb6f8491f9839aaf4078ceb (scripts/build_corpus.py::fof, 10 radii 0.5-60 arcsec, must-join and must-not-join controls); Rubin application bands_FROZEN.md sha256 8825ef8048b733b66e12f31ce16e67270de171f52f20f40ca8f21e5780e500d2 section 2
- **population:** 11193 included BTS corpus rows (11183 clusters); Rubin cohort diaObjectIds
- **adjudicator:** tau.py choice at 30 arcsec (11116 clusters, 39 must-not-join violations); IAU-name join 11,204 (agents 3 and 5)
- **falsifier:** a re-trigger pair (same object, |dpeak|<=60 d) measured at >1.5 arcsec, or two distinct SNe measured at <=1.5 arcsec, or an I1 separation curve that collapses at 1 arcsec

**Disagreements (listed, not reconciled):**
- distinct-object count 11,183 (agent 1, 1 arcsec + A1) vs 11,204 (agents 3 and 5, IAU-name join) vs 11,198 groups (agent 2, 3 arcsec + IAU): listed, not reconciled (SYNTHESIS.md section 8)

> **Override invitation (tau).** accept, or replace the value and give a reason; the reason enters amendment_ledger.json.
> The PI has not ruled on this slot. Reply RATIFY, or give a replacement value and a reason.

## k

**Value (v1):** `8`

**Status:** RATIFIED. Ratified with the rounding noted (AMD-V1-01). ZTF-era value; Rubin-era k is UNDEMONSTRATED (k_slot.json undemonstrated[0]).

**Derivation.** Source: arXiv:2401.15167 sections 4.1-4.2. BTS scanners triggered SEDM on 327 unique sources over 41 consecutive nights (2023-08-19 to 09-29), so k_exact = 7.976, rounded to 8. Candidates per round are 1,903 sources passing the filter over the same 41 nights, or 46.41 per night, which puts stated chance at 0.172. The adjudicators are four other seed statements: 5-15, 5-10, a median of 4.5, and about 10 per night. **The PI RATIFIED k = 8 with the rounding noted (AMD-V1-01).** Still open: Rubin-era k is UNDEMONSTRATED, and on the BTS file the measured chance is 0.225-0.230 because only 61 of 579 nights have more than 8 candidates (wave-2 agent 4, calibration).

**Provenance (five fields):**

- **referent:** number of candidate transients committed to spectroscopic follow-up (unique sources with an SEDM IFU request created by BTS scanners) per round, where a round is one observing night of the ZTF Bright Transient Survey under its post-2020 alert filter
- **source:** arXiv:2401.15167v1 section 4.1, sources/2401.15167.txt lines 757-766 (327 unique sources triggered by scanners with 2460175.5 < JD < 2460216.5) and section 4.2 lines 883-887, 953-958 (the same window is 41 nights); k_exact = 327/41 computed in scripts/build_slots.py; integer proposal by nearest-integer rounding of k_exact, recorded here as an amendment candidate for D5; RATIFIED at PANEL_BRIEF_WAVE2.md sha256 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb line 14
- **population:** rounds = 41 consecutive calendar nights (JD 2460175.5 to 2460216.5, 2023-08-19 to 2023-09-29); 327 unique sources committed; not candidates, not alerts
- **adjudicator:** the other seed statements of per-night commitment: 5-15 assigned per night in 2018 (arXiv:1910.12973 section 2.2, lines 258-265), 5-10 saved on an average clear night (arXiv:2009.01242 section 2.1, lines 147-148), median 4.5 per night for the automated bts_p1 policy (arXiv:2401.15167 section 4.2, lines 953-958), about 10 SEDM spectra per night capacity (arXiv:1710.02917 section 7, line 1076)
- **falsifier:** a BTS trigger log (Fritz SEDM request timestamps) for any other contiguous window of 30 or more nights whose unique-source triggers per night fall outside 4.5 to 10, or a window where more than half of the triggered sources are not in that window's candidate list, would show k differs from 8 or is not a per-round commitment

**Disagreements (listed, not reconciled):**
- per-night commitment differs across seeds and eras: 5-15 (2018 filter), 5-10 saved on clear nights (2019-2020), 7.98 triggered per calendar night (2023 window), median 4.5 (automated policy), about 10 spectra per night (SEDM, 2016-2017, iPTF). Not reconciled.
- candidates per round: 46.4 measured sources per night (window) versus 'about 50 new candidates per night' stated; the measured figure counts sources active in the window, the stated one counts new sources.
- chance: 0.172 (window counts) versus 0.14 (stated per-night figures).
- k is not fixed per round in practice: 30.9% of calendar nights in 2019-2025 have zero peaks in the BTS file, and weather dominates (arXiv:1910.12973 footnote 9, lines 308-311).
- Rubin era: TiDES does not select k of n within a round; 4MOST fibres are not binding (about 12 live transients per field pass selection versus 30-35 LRS fibres per pointing; arXiv:2501.16311 section 3.5 lines 559-565 and footnote 20 line 630, section 2 lines 138-140) and it cannot operate target-of-opportunity. The k-of-candidates decision shape holds for single-object robotic spectrographs (SEDM), not for TiDES.
- the local BTS file has 11,217 data rows; data/raw/FETCH.md and PANEL_BRIEF.md state 11,218.
- the explorer documentation names the column 'time'; the CSV header names it 'peakt'.
- wave-2 calibration (astronomy/wave2/agent4_instrument/REPORT.md 'Disagreements' 1): stated chance 0.172 vs measured 0.225-0.230 on the BTS file, which holds saved sources only; 518 of 579 nights have <= 8 candidates, so k binds on 61 nights

> **Override invitation (k).** accept, or replace the value and give a reason; the reason enters amendment_ledger.json.

## label_source

**Value (v1):** `{"population": 7843, "category_counts": {"MEASURED": 884, "MODEL_ANNOTATION": 803, "PHOTOMETRIC_ONLY": 0, "UNRESOLVED_UNDEMONSTRATED": 6156}, "sniascore_bound": {"status": "DERIVED", "lower": 803, "upper": 2247, "wave1": [0, 3131], "lower_rule": "E1 archived TNS report with 'SNIascore' in Classifier/s as latest matching report (STRONG, n=799) plus E2 paper-named objects still typed SN Ia with no contradicting E1 (MODERATE)", "upper_rule": "plain 'SN Ia' minus E1 non-SNIascore placement, minus E4 (SN Ia in 2021-01-28 BTS explorer capture), minus E5 (wave-1 phase rule, WEAK); min with wave-1 3131", "upper_noE5_sensitivity_not_slot_value": 2844, "excluded_by": {"E1": 884, "E4": 1340, "E5": 1936, "E1_only_not_E4_E5": 883}, "within_upper_fetch_status": {"not_attempted": 1198, "ok": 825, "http_error": 200, "failed_retries": 22, "invalid": 2}}}`

**Status:** UNDEMONSTRATED. Per-object split is DERIVED only where public archived TNS evidence exists; 6156 of 7843 labels remain UNRESOLVED, so the measured-vs-annotation share of the whole base is bounded, not determined. No TNS credentials were supplied (SUPPLY field empty). The SNIascore bound itself is DERIVED.

**Derivation.** Carried verbatim from wave-2 agent 2. Evidence came from archived TNS object pages (Internet Archive), read after a sealed file-only placement. The deciding field is Classifier/s, not the sender, because `ZTF_Bot1` also sends human reports. Of the 7,843 labels: MEASURED 884, SNIascore MODEL_ANNOTATION 803 (799 strong, 4 moderate), PHOTOMETRIC_ONLY 0, UNRESOLVED 6,156. The SNIascore bound tightens from 0-3,131 to **803-2,247**. The upper bound depends on the WEAK E5 phase rule, which is breached twice. The CCSNscore channel is bounded 0-155, with its start date unknown. Without TNS credentials the split is bounded, not determined, so the slot is **UNDEMONSTRATED**.

**Provenance (five fields):**

- **referent:** basis of each BTS object's current type label: human spectroscopic classification (MEASURED) vs automated-classifier TNS report (MODEL_ANNOTATION) vs report without prior public spectrum (PHOTOMETRIC_ONLY) vs no admissible evidence (UNRESOLVED); and the number of plain 'SN Ia' labels that are SNIascore annotation
- **source:** astronomy/wave2/agent2_label_source/scripts/split_labels.py::main (bounds block); astronomy/wave2/agent2_label_source/definitions_FROZEN.md sha256 4f89ff6718a14ad4e45a6d33d6bde848448ba6a66d895bd970330efe397b37cf; astronomy/wave2/agent2_label_source/sealed_fileonly_placement.json sha256 763002355b6129d9fe0a0eada86684e7dfb2e02bc9475554a8a57c9969c03eb0; astronomy/data/raw/ztf_bts_all_2026-09-16.csv sha256 61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570; Internet Archive captures of https://www.wis-tns.org/object/<name> via web/20260916id_/ (sources/tns_captures/fetch_log.jsonl, per-page sha256); arXiv:2104.12980 sec 3 lines 413-415, sec 7 lines 869-886; arXiv:2401.15167 sec 5.1 raw lines 1580-1591; arXiv:2412.08601 sec 6 lines 1089-1091
- **population:** 7843 BTS rows with type != '-' (unique ZTFID, pre-clustering; Agent 1 owns clustering; 13 IAU names shared by 2 ZTFIDs)
- **adjudicator:** authenticated TNS classification reports for every object (TNS API or bulk CSV with a bot/user account), which would replace every archived-capture placement and every UNRESOLVED; not reachable without credentials (HTTP 403 on all wis-tns.org paths 2026-09-16)
- **falsifier:** an authenticated TNS report list showing more than 2247 or fewer than 803 BTS 'SN Ia' labels whose latest classification report is SNIascore; or a later human re-report superseding an archived SNIascore report; or a rerun of split_labels.py on the same seal and captures returning different counts

> **Override invitation (label_source).** accept, or replace the value and give a reason; the reason enters amendment_ledger.json. Ratifying this slot as UNDEMONSTRATED does not make the labels measured; P4 precondition (c) needs either ratification of a label source or measured P and Ng.
> Options: ratify the bounded state (UNDEMONSTRATED; P4 precondition (c) stays unmet unless measured P and Ng exist), supply TNS credentials, or name a different label source.

## exposure_key

**Value (v1):** `key_definition + 10 subject cutoffs + two capture splits (see manifest; too long to inline)`

**Status:** DERIVED. key definition and brackets are derived from release metadata; exact classification-report dates are UNDEMONSTRATED for the unresolved objects listed; one candidate subject has no published cutoff. Not ruled on in PANEL_BRIEF_WAVE2.md.

**Derivation.** Input public date is alert issuance: ZTF from 2018-06-04, Rubin from 2026-02-24. The label public date is bracketed. The lower bound is the TNS discovery date. The upper bound is the earliest Internet Archive capture of the BTS explorer showing the same type string. The exact date is the TNS classification-report date, which needs credentials. Subject cutoffs come from vendor pages, 10 models in all, and Gemini 3.1 Pro has none. Split against the 2024-12-08 capture: 6,166 labels were public before every cutoff, 0 after every cutoff, and 1,677 are unresolved. Two wave-2 cross-references are attached. The Rubin admission boundary is 2026-07-01T00:00 UTC (bands section 1). Agent 2 also found that TNS discovery date is not a safe lower bound: SN2017bde was discovered in 2017 but classified by SNIascore in 2023.

**Provenance (five fields):**

- **referent:** per-object date on which the BTS label became publicly readable, bracketed, compared with each candidate subject's published knowledge cutoff
- **source:** astronomy/agent3_labels_exposure/scripts/labels_exposure.py::main split(); lower bound = TNS discovery date (sources/bts_all_extracols_2026-09-16.csv sha256 7c08daf489bbf648cb798ceba9f5ecbf56abc9f94dc6b2e320f5aaa84ad35b63, 'discdate'); upper bound = Internet Archive capture of the public explorer showing the same type string (sources/wayback_bts_explorer_20241208231331.html sha256 96b9fe72714a7e3af4e9f2cc8e22b4b60b7a5078dd488e0c9b06c05bd6d2fc43, sources/wayback_bts_explorer_20250810065056.html sha256 ec0152effff8b3e4dfb538566ad998ab5e4dd33749c229c9f7518cefcbb373d6); input-data release: sources/ztf_public_releases.txt lines 104, 301; sources/RTN-011.txt lines 2468, 2773, 1288; cutoffs: sources/anthropic_models_overview.txt line 49, sources/anthropic_transparency.txt lines 34, 69, 104, 348, sources/openai_models.txt lines 660-729, sources/deepmind_modelcard_gemini-3-8-flash.txt line 243
- **population:** 7843 labeled objects out of 11217 unique ZTFID (pre-clustering); subjects: 10 candidate models, 1 without a published cutoff
- **adjudicator:** TNS classification report dates per object (exact public date of each label), which would collapse the bracket to a point; not reachable without credentials
- **falsifier:** a TNS classification report dated after 2024-12-08 for an object counted 'before' with an unchanged type, or a subject whose training data (not reliable-knowledge cutoff) is documented to end before the object's label date, or a rerun on the same hashed files returning different counts

> **Override invitation (exposure_key).** accept, or replace the value and give a reason; the reason enters amendment_ledger.json.
> The PI has not ruled on this slot. Reply RATIFY, or give a replacement value and a reason.

## tool_inventory

**Value (v1):** `25 channels; Rubin counterparts after AMD-V1-03: ATAT, Astromer1, Astromer2 -> [Fink_EarlySNIa_RF, Fink_SLSN_RF]`

**Status:** OVERRIDDEN. The override covers the Rubin counterpart mapping of three rows only. The rest of the inventory (roles, readiness census, 25 channels) is as derived and was not ratified; readiness is a census, not certification (I5 UNDEMONSTRATED).

**Override reason:** AMD-V1-03: PI approved agent 4's Fink RF remapping (PANEL_BRIEF_WAVE2.md line 16). Cause: check (a) failed on Rubin for ATAT, Astromer 1 and Astromer 2 because ALeRCE_BHRF has no Rubin weights. Rubin classical counterpart for those three is now Fink_EarlySNIa_RF and Fink_SLSN_RF; ZTF mapping and all wave-1 counts unchanged.

**Derivation.** Agent 4 built this from 30 pinned clones plus weight hashes: 25 decision-time channels, 15 FM/deep and 10 classical, with roles read from code input and output. It carries a readiness census for ZTF and Rubin: on Rubin, 0 verified, 12 AVAILABLE_UNVERIFIED, 12 UNAVAILABLE and 1 UNDEMONSTRATED. Check (b), a role below the line, passes (ParSNIP, SALT3). Check (a), a classical counterpart per FM channel, failed on Rubin for ATAT, Astromer 1 and Astromer 2, because ALeRCE_BHRF has no Rubin weights. **The PI APPROVED the Fink RF remapping (AMD-V1-03).** For those three rows the Rubin counterpart is now Fink_EarlySNIa_RF and Fink_SLSN_RF. It is recorded in `counterparts_by_survey.rubin`, and the wave-1 `counterparts` field and all counts are kept verbatim. Structurally, check (a) on Rubin now holds (`..._after_AMD-V1-03 = true`). That is structural only: the Fink RFs are unverified on real Rubin alerts.

**Provenance (five fields):**

- **referent:** which decision-time tools exist for early classification / spectroscopic follow-up allocation of transients, what role each plays by its code-level input and output, and whether it can process ZTF alert/BTS inputs and Rubin lsst.v11_1 alert packets
- **source:** scripts/build_inventory.py rows; code/CLONE_PINS.tsv commits; weight sha256 in code/PRUNED_LARGE_FILES.tsv and code/_downloaded_artifacts/*/SHA256SUMS; schema lsst/alert_packet@1362a8d7 python/lsst/alert/packet/schema/11/1/*.avsc; papers in sources/ with section locators in seed_ledger.json
- **population:** 25 decision-time tool channels (15 FM or deep, 10 classical), one row per tool, not per variant or checkpoint; 7 repositories excluded as non-channels (datasets, schemas, training code)
- **adjudicator:** the classical counterparts in the same inventory (ALeRCE_BHRF 1.1.1 on ZTF; SALT3-f22, Fink rainbow RFs on Rubin); the strongest existing deployed alternative on ZTF is BTSbot + human BTS scanning, which is itself an FM-side channel
- **falsifier:** a released checkpoint for any row marked UNAVAILABLE that runs on the stated input format, or a source read showing a row marked AVAILABLE_UNVERIFIED was validated on real Rubin alerts, or a rerun of this script against newer commits that changes any status

> **Override invitation (tool_inventory).** accept, or replace the value and give a reason; the reason enters amendment_ledger.json.

## delta

**Value (v1):** `0.018`

**Status:** DERIVED. Cost of action was an unfilled SUPPLY field, so no override exists; per the brief delta stays at the derived prior with its resolution warning (AMD-V1-05). Not RATIFIED.

**Derivation.** Agent 5 took this from arXiv:2401.15167 Appendix B Table 6. The production selector (MM-CNN) reached bts_p2 purity 0.930 against 0.912 for the metadata-only NN on the same test split, and the authors put MM-CNN into production, giving 0.018. Three other candidates were listed and not adopted: BTSbot vs scanners (refused, unequal denominators), SNIascore vs SNID (adjacent referent) and Fink US vs RS (counted over alerts). **Resolution warning:** the unpaired MDE of the source comparison is about 0.045. Wave-2 PRE-I1 calibration on BTS binding nights gives MDE 0.032, so 0.018 is below both. Cost of action was not supplied, so per brief line 13 delta stays 0.018, **DERIVED, not ratified** (AMD-V1-05).

**Provenance (five fields):**

- **referent:** absolute difference in purity (precision) of the set of sources selected for SEDM follow-up, between two candidate selection models evaluated on the same test split, that practitioners acted on by choosing the production model
- **source:** arXiv:2401.15167v1 Appendix B Table 6, sources/2401.15167.txt lines 1323-1335 (bts_p2 purity MM-CNN 93.0%, NN 91.2%, UM-CNN 92.5%) and lines 1360-1364 ('advantage is ~0.5-2% ... even small boosts in purity are valuable'); production choice section 4.1 lines 655-662; difference 0.930-0.912 computed in scripts/build_slots.py; kept by PANEL_BRIEF_WAVE2.md sha256 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb line 13 until cost of action is supplied
- **population:** BTSbot test split: 512 bright-transient sources and 1,489 other sources (Figure 4, line 420), less 70 junk and 59 single-alert sources (lines 704-714); paired over the same sources, discordant selections not published
- **adjudicator:** the fully-connected metadata-only network (NN) on the same test split, the strongest of the two alternatives on bts_p2 purity after the production model
- **falsifier:** a rerun of the three published architectures (github.com/nabeelre/BTSbot) on a fresh contiguous window in which the MM-CNN minus NN purity difference falls outside 0 to 0.036, or a statement from BTS that the architecture choice was made on a criterion other than purity

**Resolution warning:** 0.018 is below the unpaired MDE of about 0.045 of the very comparison it comes from (agent5 REPORT.md line 48); practitioners acted below their own resolution. Wave-2 PRE-I1 calibration on BTS binding nights gives MDE 0.032 > 0.018 (CLOSE_UNRESOLVABLE, calibration only, not P7).

**Disagreements (listed, not reconciled):**
- an order of magnitude separates the values practitioners acted on: 0.018 (selection purity, architecture choice), 0.30 (Fink efficiency, alerts), 0.37 (SNIascore TPR). Not reconciled.
- the adoption of BTSbot over scanners happened at a purity deficit (93.0% versus 95.6% or 96.7%, both in one paper), i.e. practitioners traded purity for labour; the seeds show no adoption driven by a purity gain alone.
- practitioners acted on 0.018 while an unpaired MDE for that comparison is about 0.045 (own_resolution_note); the seeds act below their own resolution, which SKILL.md refusal 5 forbids for a directional claim.

> **Override invitation (delta).** accept, or replace the value and give a reason; the reason enters amendment_ledger.json. Supplying cost of action is the route manifest.md names for overriding delta.
> Supplying cost of action overrides this, and the PI may override delta directly with a stated cause. Until then it stays 0.018.

## S

**Value (v1):** `null`

**Status:** UNDEMONSTRATED. budget unfilled (SUPPLY) and hours per workflow unmeasured (R1 not run)

**Derivation.** S = budget / measured hours per workflow (manifest.md). Budget was an unfilled SUPPLY field and R1 has not run, so S is **UNDEMONSTRATED**. It blocks the P5 escape, cohort sizing and the choice of N row in the planning bracket.

**Provenance (five fields):**

- **referent:** survivor target S = budget / measured hours per workflow
- **source:** references/manifest.md ('S, the survivor target, is budget divided by measured hours per workflow'); references/graph.md D5 -> R1; UNDEMONSTRATED per PANEL_BRIEF_WAVE2.md sha256 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb coordinator preamble item 1
- **population:** workflows (one scored item through all arms)
- **adjudicator:** none until hours per workflow are measured at R1; the source record repriced its cohort from about 17 to 37 hours (references/manifest.md)
- **falsifier:** a measured hours-per-workflow figure from an R1 control run that, divided into the supplied budget, disagrees with any S used earlier

> **Override invitation (S).** Not overridable by ratification: S follows from a supplied budget and an R1 measurement.

## subject_set

**Value (v1):** `["claude-fable-5-1", "claude-opus-5", "claude-sonnet-5", "gpt-6-astra", "gpt-5.6-sol", "gemini-3.8-flash", "gemini-3.1-pro-preview"]`

**Status:** DERIVED. Not ruled on in PANEL_BRIEF_WAVE2.md. Training-data ends UNDEMONSTRATED for all members; Gemini 3.1 Pro has no published cutoff.

**Derivation.** Agent 5 read first-party model pages on 2026-09-16: 7 models from 3 providers, flagship and next tier. No required rung is stated anywhere, so availability is the only criterion. Cutoffs are 'reliable knowledge' or 'knowledge' cutoffs, not training-data ends. Gemini 3.1 Pro has none. This slot governs the Rubin admission boundary (Fable 5.1, Jun 2026) and forces the contamination band to ESCALATE while any member lacks a cutoff. Agent 3's exposure-key table lists 10 models, against 7 here; that disagreement is listed.

**Provenance (five fields):**

- **referent:** frontier general-purpose models available through first-party APIs on 2026-09-16, with the training cutoff each provider states, for use as agent subjects
- **source:** first-party documentation fetched 2026-09-16: sources/anthropic_models_overview.txt, sources/anthropic_transparency.txt, sources/openai_models.txt, sources/openai_gpt-6-astra.txt, sources/google_gemini_models.txt, sources/deepmind_modelcard_gemini-3-8-flash.txt, sources/deepmind_modelcard_gemini-3-7-flash.txt, sources/deepmind_modelcard_gemini-3-1-pro.txt, sources/deepmind_modelcard_gemini-3-pro.txt (raw HTML beside each .txt)
- **population:** 7 models from 3 providers (flagship and next tier per provider as each provider's own models page ranks them); open-weight models not surveyed
- **adjudicator:** no required rung is stated by any seed or by the panel brief, so availability is the only criterion; the strongest alternative subject is the best classical-tool arm, which is a composition, not a model
- **falsifier:** a first-party page, model card or system card dated on or before 2026-09-16 stating a different cutoff for any member, or listing a more capable generally available model from these providers that is missing here

**Disagreements (listed, not reconciled):**
- cutoff referent differs by provider: Anthropic states 'reliable knowledge cutoff', OpenAI 'knowledge cutoff', Google a 'knowledge cutoff date' with an earlier domain-dependent limit. None states the last date of training data, which is what an exposure key needs.
- Claude Fable 5.1 appears on the models overview with a June 2026 reliable-knowledge cutoff, but the Transparency Hub lists only Claude Fable 5 (January 2026).
- Gemini 3.8 Flash: March 2026 and January 2025 in one sentence of its model card.
- membership: agent 5's subject set has 7 models; agent 3's exposure-key cutoff table carries 10 (adds Claude Haiku 4.5, GPT-5.6 Terra, GPT-5.6 Luna). Listed, not reconciled.
- bands_FROZEN.md section 1: the Rubin admission boundary 2026-07-01 is set by Claude Fable 5.1 (Jun 2026); dropping Fable 5.1 would admit June objects, and that relaxation is reserved for the human at D5.

> **Override invitation (subject_set).** accept, or replace the value and give a reason; the reason enters amendment_ledger.json. The subject set governs the admission boundary and the contamination band (a subject without a cutoff forces ESCALATE).
> The PI has not ruled on this slot. Reply RATIFY, or give a replacement value and a reason.

## decision_epoch

**Value (v1):** `{"primary": "first alert", "secondary": "night 3"}`

**Status:** RATIFIED. AMD-V1-02. New D4 slot, ratified at declaration. Strata S0-S4 for the Rubin cohort are defined in bands_FROZEN.md section 3; they are not part of this v1 ruling.

**Derivation.** **Declared and RATIFIED by the PI in the hashed wave-2 brief (line 15), before any composition ran (AMD-V1-02).** Primary is first alert; secondary is night 3. Wave-2 agent 4 operationalised it for ZTF calibration in compositions_FROZEN.md section 1:
- **E1:** the triggering detection plus the 30-day prv_candidates history.
- **E3:** photometry through ZTF night n0+3, with nights split at 20:00 UTC.

This freeze re-checked that declaration against the ratified value: **MATCH**. No Rubin composition has been declared. Rubin first detection is defined in bands section 3.

**Provenance (five fields):**

- **referent:** the moment at which the governed follow-up decision is taken, which fixes the inputs any composition or arm may see
- **source:** PANEL_BRIEF_WAVE2.md sha256 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb line 15 (PI declaration); ZTF operationalisation astronomy/wave2/agent4_instrument/compositions_FROZEN.md sha256 b2f72948de0b39682ff8bc01c3c3f13f931a0a96966ede90c50466a9d045427c section 1
- **population:** one decision per candidate transient per round (observing night); units are 1 arcsec clusters (BTS) or diaObjectIds (Rubin)
- **adjudicator:** later epochs in the record: peak (SN Ia AUC 0.798) and post-spectroscopy (0.967) vs first alert (0.537), agent2_floor_headroom/REPORT.md table lines 73-77; the declared epochs are the decision-time ones
- **falsifier:** a composition input file containing photometry after the epoch cutoff (a rerun of the compositions_FROZEN.md section 5 forbidden-input check that fails), or a PI statement that differs from brief line 15

> **Override invitation (decision_epoch).** accept, or replace the value and give a reason; the reason enters amendment_ledger.json.

## SUPPLY fields (not derivable from the corpus)

| Field | v1 | Blocks |
|---|---|---|
| d5-budget | UNDEMONSTRATED (unfilled placeholder) | S, P5 queue loop escape, P7 N_min versus affordable N, R1 onward (no paid work on an unratified manifest) |
| d5-cost-of-action | UNDEMONSTRATED (unfilled placeholder) | delta override, P7 ruling, A4 claim threshold |
| d5-rulings-holder | UNDEMONSTRATED (unfilled placeholder) | rulings transfer, issue 09 re-keying, any seal with more than procedural weight |
| d5-tns-credentials | UNDEMONSTRATED (unfilled placeholder) | label_source per-object split, measured P and Ng for the Rubin cohort, P4 precondition (a) |

> **Invitation.** Supply budget (arm cells or hours), cost of action (the value of a spectrum slot and of a wrong commitment, or the smallest precision gain that would change the programme's tool), a rulings holder who authored neither the skill nor any case, and TNS credentials.

## Graph escalation (not an amendment)

Edge R1 → I1: the wave-2 compositions are PRE-I1 CALIBRATION, pending a PI ruling on the ordering (coordinator preamble item 2, ladder rung 2). Ledger ESC-V1-01.

> **Invitation.** Rule on the staging: ratify it as staged, or require R1 before any composition counts.

## Candidate

- **Candidate:** live time-domain astronomy: Rubin LSST alert stream, ZTF BTS as calibration (branch: prediction).
- **Decision governed:** spectroscopic follow-up allocation: k candidates committed per night.
- **Calibration cohort:** ZTF BTS (11,183 objects at 1 arcsec); contamination FAIL (agent3 wave 1); addition B: no claim rests on it.
- **Prospective cohort:** Rubin LSST objects first detected >= 2026-07-01T00:00 UTC (bands_FROZEN.md section 1); counts in wave2/agent1_rubin_bands/axis_ledger_rubin.json (P4 unruled).
- **P4 at v1:** no ruling; preconditions (a) supply without measured labels, (b) tool coverage not recounted after the band, (c) label source unratified.
