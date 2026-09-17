# Agent 2 (wave 2): label-source definitions, FROZEN before any per-object count

Frozen 2026-09-16, before `scripts/split_labels.py` or `scripts/fetch_tns_captures.py` existed, and before any per-object TNS capture was read. Brief hash verified: 31a36617f0c6ae4179bb95ec134a6db7717ae7073f52f48b4272dde6a7a0f4eb (matches wave2/BRIEF_SHA256).
sha256 of this file: `definitions_FROZEN.sha256`. Scripts re-check it before counting and abort if it has changed.

All work below is **calibration only (addition B): BTS failed contamination.** Nothing here supports a claim resting on the BTS cohort.

## 0. What I saw before freezing (disclosed)

- **Wave-1 counts already known.** Agent 3's 0 to 3,131 SNIascore bound: 5,067 plain "SN Ia" labels, 1,936 excluded by the peak rule. Its class-basis table. Agent 1's list of 98 answer-in-seed objects and the script that produced it. None of these was recounted before this freeze.
- **Sources read in full:** SNIascore (arXiv:2104.12980v2), CCSNscore (arXiv:2412.08601v2) and BTSbot (arXiv:2401.15167v1).
- **Reachability probes.** Each was a single page and none was a count; see `sources/http/probe_log.txt`.
  - wis-tns.org returns HTTP 403 (awselb) on every path, robots.txt included.
  - The Wayback CDX API returns 503 ("Temporarily Offline"). The `/wayback/available` API returns 429.
  - `web.archive.org/web/<ts>id_/<url>` returns a 302 to the nearest capture, then 200.
  - I read one archived TNS object page in two captures: SN 2021ijb at 2021-04-13 and at 2024-12-03. This was to learn the page structure. The 2024 capture's classification table has these columns: ID, Time received, **Sender** (ZTF_Bot1), **Classifier/s** ("SNIascore on behalf of the SEDM Team (Caltech) and the Zwicky Transient Facility (ZTF)"), Group, Classification, Redshift.
  - One probe of a random name (2019zzz) was redirected to a 2025-07-09 capture.
  - The BTS explorer default page has captures at 2021-01-28 and 2021-05-13. I read only their redirect headers, not their contents.
- **No credentials used.** No accounts were created. User agents were not spoofed: every request uses the default `curl/8.5.0` UA or Python's default. No access control is bypassed; a 403 is recorded and left as a 403.

## 1. Unit and population

- **Unit:** one BTS row, keyed by ZTFID, from `astronomy/data/raw/ztf_bts_all_2026-09-16.csv` (sha256 61415979…e570). The population is the 7,843 rows whose `type` is not `-`.
  - This is pre-clustering and follows the wave-1 slot's denominator so the bounds stay comparable.
  - Clustering belongs to Agent 1. 13 IAU names are shared by 2 ZTFIDs; for those, the TNS evidence is the same page for both rows. This is reported, not merged.
- **Dates:** discovery date and discoverer ID come from `agent3_labels_exposure/sources/bts_all_extracols_2026-09-16.csv` (sha256 7c08daf4…5b63). `peakt` is JD−2458000, per the explorer documentation (line 79).

## 2. Categories (every object gets exactly one)

- **MEASURED.** The object's current label rests on a TNS classification report whose Classifier/s field names one or more people and carries no automated-classifier marker (§3). A human assigned the class from a spectrum; per Perley+2020 Fig. 3, public BTS transient classifications are spectroscopic.
  - Sub-field: the reporting group, ZTF/BTS or other.
  - A human report counts as MEASURED even when SNID or other template software assisted. SNID assisting a human is not model annotation here: SNIascore §1 describes it as "manual matching … along with careful inspection".
- **MODEL_ANNOTATION.** The current label rests on a TNS classification report whose Classifier/s field carries an automated-classifier marker (§3). Sub-field: the model (SNIascore, CCSNscore, or other-automated).
- **PHOTOMETRIC_ONLY.** The current label rests on a TNS classification report, and the archived object page lists **no spectrum** with obs-date on or before that report's time received. Alternatively, the report's Remarks state a photometric or light-curve basis and the page lists no spectrum.
- **UNRESOLVED.** No admissible evidence places the object. Its status is UNDEMONSTRATED, never guessed.

"Current label rests on report R" means all of the following:
1. R is the latest classification report (by Time received) on the latest valid archived capture.
2. R's Classification matches the BTS `type` under §4.
3. The capture is valid under §5.

If the latest report does not match, the object is UNRESOLVED and the mismatch is logged. The label may have changed after the capture, or the BTS string may differ from TNS.

## 3. Automated-classifier markers (Classifier/s field only; never Sender, because ZTF_Bot1 also sends human reports)

Case-insensitive substring match on:
- `SNIascore`, which sets model = SNIascore
- `CCSNscore`, which sets model = CCSNscore
- whole words `bot`, `robot`, `automatic`, `automated`, or `auto`, which set model = other-automated

A Classifier/s field with none of these is human.

## 4. Class-string match between TNS report and BTS `type`

1. Normalise both strings: lowercase, strip, drop a trailing `-like`, and collapse whitespace.
2. They match if any of the following holds:
   - the normalised strings are equal;
   - the TNS string starts with the BTS string plus `-`, which covers subtype removal (Perley+2020 App. E);
   - the pair is one of (BTS `sn ii`, TNS `sn iip`), (`sn ii`, `sn iil`), (`sn iip`, `sn ii`), (`sn ib/c`, `sn ibc`).
3. Nothing else matches. Unmatched pairs are counted and listed.

## 5. Evidence and strength

| Code | Evidence | Can place | Strength |
|---|---|---|---|
| E1 | Archived TNS object page (Internet Archive), latest capture at or before 2026-09-16, fetched via `web/20260916id_/https://www.wis-tns.org/object/<iau>` with redirects followed. **Valid** only if HTTP 200, the HTML `<title>` contains the object's IAU designation digits+letters, and the page contains a "Classification Reports" fieldset or no-report marker. A capture holding a 403/login/error page is invalid. | MEASURED, MODEL_ANNOTATION via §2 (STRONG); PHOTOMETRIC_ONLY via §2 (MODERATE when resting only on "no spectrum listed", because a classifying spectrum may exist without being uploaded to TNS; STRONG when Remarks state a photometric basis) | as stated |
| E2 | A peer-reviewed or arXiv paper read in full that names the object as classified by SNIascore: SN 2021ijb (arXiv:2104.12980 §7 lines 876-878); SN 2023tyk and 13 listed SNe (arXiv:2401.15167 §5.1). Applies only if the BTS `type` is still `SN Ia`. | MODEL_ANNOTATION (SNIascore) | MODERATE (a later human report of the same class cannot be excluded without E1) |
| E3 | Class string SNIascore cannot emit. SNIascore is binary SNIa/NotSNIa (2104.12980 §3 lines 413-415) and reports only "confident SN Ia classifications" (§7 lines 871-872). SEDM cannot separate Ia subtypes except in clear-cut cases (footnote 9 lines 862-865). Any `type` other than exactly `SN Ia` is therefore not SNIascore annotation. | excludes SNIascore only; does not place a category | STRONG for the exclusion |
| E4 | Internet Archive capture of the BTS explorer default page dated **before 2021-04-15** that shows the object with `type` `SN Ia`. The label was public before SNIascore auto-reporting began. SkyPortal blocks automatic follow-up on sources that already have a classification (2401.15167 §5.1 line 1288). | excludes SNIascore for the upper bound; does not place MEASURED | MODERATE |
| E5 | Carried over from wave 1: plain `SN Ia` whose peak (peakt+2458000) is more than 30 d before 2021-04-15, i.e. peakt < 1289.5 − 30 = 1259.5 (JD 2459319.5 = 2021-04-15). This rests on the SNIascore training/validation phase range (−20..+30 d, §2 lines 277-283), which is a range of the data, **not** a stated deployment restriction. | excludes SNIascore for the upper bound only | WEAK |
| E6 | Discovery date (TNS, from extracols) on or after 2021-04-15: SNIascore origin is possible. | nothing (enables membership in the candidate set only) | n/a |
| E7 | CCSNscore start: as of arXiv:2412.08601v2 (2025-03-11), real-time TNS reporting had **not** started (§6 lines 1089-1091). | excludes CCSNscore for reports before 2025-03-11 only via E1 report time | STRONG when combined with E1 |

The reporter or bot name "ZTF_Bot1" in the Sender field is **not** evidence of automation (§3).

## 6. SNIascore bound: rules (declared before counting)

Population P = objects with `type` exactly `SN Ia`.

- **Lower bound L.** Count the objects in P with (E1 → MODEL_ANNOTATION, model SNIascore) OR (E2 and no E1 contradiction). Reported as L_strong (E1 only) and L (E1 ∪ E2).
- **Upper bound U.** Count the objects in P that are **not** excluded by any of:
  - E1 → MEASURED or PHOTOMETRIC_ONLY or MODEL_ANNOTATION with model ≠ SNIascore;
  - E4;
  - E5.
  - Also reported: U_noE5, the same without the weak E5 rule. **U_noE5 is a sensitivity number, not the slot value.**
- **Bound-tightening rule.** The slot value is `[max(L, 0), min(U, 3131)]`.
  - A new bound may only replace the wave-1 bound when it is tighter.
  - **No bound is ever widened after a count.** If U_noE5 > 3,131, that fact is recorded as a disagreement with wave 1's E5 rule, with a falsifier. It does not replace the value.
- **Interruption.** Any object whose E1 fetch was not attempted or did not complete gets no E1 evidence. It stays inside U, is never counted in L, and is never counted as zero.

## 7. CCSNscore bound (declared)

- **Population.** `type` in {SN II, SN IIP, SN IIb, SN IIn, SN Ib, SN Ic, SN Ic-BL, SN Ib/c}, the CCSNscore layer classes (2412.08601 §3 lines 390-397).
- **Lower bound.** E1 with model CCSNscore.
- **Upper bound.** Objects in the population with discovery date on or after 2025-02-09, which is 2025-03-11 − 30 d, the E5-analogue margin. Excluded from it: objects with E1 → MEASURED / PHOTOMETRIC_ONLY / other model.
- **Status.** The actual start date is UNDEMONSTRATED. The CCSNscore GitHub page, which the paper says carries the reporting criteria, was not read.

## 8. Fetch scope and order (declared)

- **Scope.** E1 fetches are attempted for labeled objects that have an IAU name.
  - **Tier 1:** P (plain SN Ia) not excluded by E5.
  - **Tier 2:** P excluded by E5.
  - **Tier 3:** all other labeled objects.
  - Within each tier, the order is a random permutation with numpy seed 20260916.
- **Politeness.**
  - At least 1.0 s between requests.
  - On 429/503: sleep 60 s, then retry up to 3 times, after which the fetch is recorded as failed.
- **Time cap.** 5 hours of wall clock in total. Objects not reached are recorded as `not_attempted`, which is UNDEMONSTRATED.
- **Recording.** Every request's HTTP status chain and final capture timestamp is logged to `sources/tns_captures/fetch_log.jsonl`. Pages are saved with their sha256.

## 9. Addition C seal

Before any E1 fetch, `sealed_fileonly_placement.json` is written and hashed (`sealed_fileonly_placement.sha256`). It holds the file-only and paper-only placement of every object (E2–E6) and the predicted bound under those rules. Reading archived TNS pages happens only after the seal. No labeled object was discovered on or after 2026-07-01 (wave 1: 0), so no post-cutoff object's page is read. The seal covers objects inside the 2025-02-01..2026-06-30 cutoff window as well.

## 10. Refusal 14 for the answer-in-source objects (declared)

For each of Agent 1's 98 flagged objects, and for any object named in a seed I read in full (2104.12980, 2401.15167, 2412.08601):

1. **Locate.** Find every line in the seed's raw text containing the ZTFID or the IAU designation, with or without the SN/AT prefix and space.
2. **Class check.** "Class stated in text" = a transient class token (SN I*, SLSN*, TDE*, CV, AGN, nova, LBV, LRN, ILRT, Ca-rich, Ia/II/Ib/Ic with subtype, "other") within ±3 lines of an occurrence, confirmed by reading the lines. The token may be any class, whether or not it equals the BTS `type`: a stated wrong class is still a stated answer.
3. **Rulings.**
   - **REFUSE (refusal 14).** The class is stated in the text. The exposure key places the seed before every subject's cutoff (arXiv v1 dates: 1910.12973 = 2019-10-28, 2009.01242 = 2020-09-02; both before the earliest demonstrated cutoff, 2025-02-01), so the exception cannot apply.
   - **NOT_FIRED_NAME_ONLY.** The name occurs but no class is stated within the window. Refusal 14 does not fire on the class. The item is admissible for **calibration only** under written exposure ruling ER-W2-A2-01: IAU name withheld, seed text not given to any arm, contamination FAIL disclosed.
   - **NOT_FIRED_FALSE_MATCH.** The regex hit is not this object, for example a different year/letters collision. Admissibility is that of an ordinary BTS item: calibration only.
4. **Scope.** Every ruling governs calibration use only (addition B). No ruling admits any BTS item to a scored subject comparison.

## 11. What may change after counting, and what may not

- **May change:** bug fixes in parsers. Each is recorded in an amendment list in the report together with the counts before and after.
- **May not change:** categories, markers, match rules, evidence strengths, bound rules, fetch order, the time cap.
