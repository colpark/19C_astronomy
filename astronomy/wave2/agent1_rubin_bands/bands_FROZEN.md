# Agent 1, wave 2: P4 bands, boundaries and definitions for the Rubin prospective cohort (FROZEN)

Frozen 2026-09-16, before any Rubin count, broker query, TNS read or Rubin status-page read in this session (see `order_of_operations.log`, which records the sha256 of this file before step 2 begins).
Every threshold below comes from a recorded quantity, and its derivation is given inline. `scripts/derive_band_thresholds.py` reproduces the numbers from the hashed inputs into `out/band_thresholds.json`.

Recorded inputs:
- `astronomy/agent5_resolution_replay/planning_mde_bracket.csv`, sha256 c00718b7440664c6c41c90d93645d5fb68cb397414a7822c29897fe28031ad43. PLANNING-ONLY, not a P7 record, so every band built on it inherits that status.
- `k_slot.json` = 8, sha256 8980cc62…4611 (rounded from 327/41 = 7.98; the rounding is noted in the brief).
- `delta_slot.json` = 0.018, sha256 435589df…e99a, with its resolution warning.
- `agent3_labels_exposure/exposure_key_slot.json`, which holds the cutoff table and cutoff_bounds.
- `agent1_supply_corpus/corpus_rules_FROZEN.md`, sha256 aa4e8d21…a41a (label map), plus amendment A1 (re-trigger clause of 60 days).
- `fm-advantage-benchmark/scripts/power.py`, default alpha 0.05, power 0.80. This is the alpha that produced the bracket.

Everything defined here is subordinate to additions A–C. **No claim rests on BTS (B).** BTS enters only §9, as calibration.

---

## 1. Start boundary

**Survey-start boundary: 2026-06-29, the formal declaration.**
- Source: RTN-011 v9.0 §2.4 (agent3 `sources/RTN-011.txt` line 1288: "The start of the LSST was formally declared on 2026-06-29"). The ops update agrees (`rubin_community/2026-07-10…md`: "The 10-year LSST began the night of 29 June").
- Reason: the declaration names the first survey night. 2026-06-30 is only the date the announcement was posted (`rubin_community/2026-06-30_the-lsst-has-started.md`, posted 15:32 UTC). A posting date is a publication event, not a survey event. Using it would drop an LSST night from the survey-night count for no survey reason.
- Night convention: "night of 29 June" is Rubin dayObs 20260629. The survey-start instant is therefore 2026-06-29T12:00 UTC = MJD(UTC) 61220.5 = MJD(TAI) 61220.500428, taking dayObs as the local-date night that begins at UTC−12 h. This boundary governs only the survey-night count in §6 and the stratum S0 in §3.

**Interaction with subject cutoffs.**
- The latest demonstrated subject cutoff is Claude Fable 5.1, "Jun 2026", reliable knowledge cutoff (agent3 exposure_key_slot, `cutoff_bounds.latest_last_day` = 2026-06-30).
- Cutoffs are published at month granularity. Any instant in June 2026 may therefore be inside Fable 5.1's knowledge.
- Consequence: nights dayObs 20260629 and 20260630 are LSST nights, but objects first detected on them are **not after every cutoff**. They cannot enter the post-cutoff cohort under either candidate date. Choosing 2026-06-30 over 2026-06-29 would change no cohort membership. It would only drop one survey night from §6.

**Cohort admission boundary (the one P4 counts against): first detection at or after 2026-07-01T00:00:00 UTC = MJD(TAI) 61222.000428.**
- Derivation: max(survey start, latest_last_day + 1 day) = max(2026-06-29T12:00, 2026-07-01T00:00).
- If the Fable 5.1 disagreement (models page Jun 2026 vs Transparency Hub Fable 5 Jan 2026) were resolved to exclude Fable 5.1, Opus 5 (May 2026) would become latest. That would admit June objects. **That change is not made here.** The stricter bound stands until D5 ratifies the subject set, and any relaxation is an override recorded by the human.
- Caveat carried from agent 3: a "reliable knowledge cutoff" is not a training-data end. "After every cutoff" is an upper-bound claim on exposure. Gemini 3.1 Pro has no published cutoff, so "after every subject" stays UNDEMONSTRATED for any subject set that includes it (§7 contamination band).

## 2. Unit

**Unit: one distinct astrophysical object, keyed by Rubin `diaObjectId` (DiaObject).**
- apdb.yaml v10.0.0, `DiaObject.diaObjectId`, `firstDiaSourceMjdTai`, `nDiaSources`.
- LDM-612 §2.2.1: each DIASource associates to one DIAObject or to an SSObject.

**Excluded by construction, not by outcome:** DIASources associated to SSObjects (solar-system moving objects). They are not DIAObjects in the data model (LDM-612 §2.2.1), and the governed decision is transient spectroscopy. A broker record that carries only an ssObjectId is not a unit.

**Crossmatch rule for broker-mirror duplicates**, applied in order:
- **X1.** Records in different brokers with the same `diaObjectId` are one object.
- **X2.** Within the union, two diaObjectIds are one object when both hold:
  - they are ≤ 1″ apart (wave-1 D3 working cut, the 0.5–1.5″ plateau), and
  - their first detections are ≤ 60 days apart (wave-1 amendment A1, the re-trigger clause).
  - Linking uses connected components.
- **X3.** diaObjectIds ≤ 1″ apart with first detections > 60 days apart stay distinct. The pair is reported as "same position, distinct object" (for example a second SN in a host, or a recurrent AGN or CV). This is wave-1's documented limit of position alone.
- **X4.** If a broker exposes no diaObjectId, only alert or diaSource ids, its rows are raw. Its distinct count is UNDEMONSTRATED and is never counted as an object count (rule 1).

Two counts are reported: distinct diaObjectIds per broker (X1 within broker) and merged objects (X1+X2). Raw alerts or diaSources go beside both, with overstatement % = (raw − distinct) / distinct × 100.

## 3. "First detected on or after start"

**Definition.** An object's first detection time is the minimum `midpointMjdTai` over the non-forced DIASources associated with it.
- This equals `DiaObject.firstDiaSourceMjdTai` where the broker serves it.
- Otherwise it is min(diaSource.midpointMjdTai ∪ prvDiaSources.midpointMjdTai) over the alerts the broker holds.
- After X2, a merged object's first detection is the minimum over its members.

**Forced photometry does not count as detection.**
- DIAForcedSources are flux measurements at a known position. No alert is issued for them (LSE-163 §3.2.1 items 10–11, lines 922–955). Precovery forced photometry reaches back 30 days (LSE-163 line 950; LDM-612 §2.2.5).
- They are not detections, so they do not move first detection earlier.
- A forced source before the boundary with S/N ≥ 5 on a cohort object is counted and reported as stratum S2, "pre-boundary forced flux". It is not removed from the cohort. Removal would change the definition after seeing the data.

**Pre-survey, commissioning and early-operations detections count as detections.**
- A DIASource from before the survey (alerts since 2026-02-24, RTN-011 line 2468) is a detection.
- An object with any DIASource before the admission boundary is **not** in the cohort, even if most of its detections are later. It is counted as stratum S1, "straddler".

**History window.** Alert packets carry previous DIASources from the prior 12 months (LDM-612 lines 473–477; LSE-163 line 914).
- The alert stream began 2026-02-24, less than 12 months before 2026-09-16. A broker holding full packet history therefore sees every alert-stream detection.
- Detections that exist only in PPDB precovery (RTN-011 line 2575) or in pre-alert commissioning data are invisible to brokers. Their share is UNDEMONSTRATED, and the cohort count is an upper bound with respect to them.

**RTN-011 caveat (line 2479).** Early-operations alert packets for moving objects "may not include the associated historical source records". The DIAObject cohort is unaffected, because moving objects are excluded.

**Strata, declared now and reported, never filtered on outcome:**

| Stratum | Contents |
|---|---|
| S0 | first detection in [survey start, admission boundary), i.e. nights 20260629–20260630. LSST objects not after every cutoff |
| S1 | straddlers |
| S2 | cohort objects with pre-boundary forced flux |
| S3 | cohort objects with nDiaSources = 1 |
| S4 | cohort objects with nDiaSources ≥ 2 |

S3 and S4 exist because BTS's alert filter required "two detections" (Perley+2020 §2.1, agent1 `sources/2009.01242.txt` line 163). The split is reported. It does not drive a band.

**Window end.** The time of the query, recorded per broker. A later recount with a later window end is a new registration (loop.md "supersede"). Start, unit, label map and bands stay unchanged, so it is not a widening.

## 4. Labels: positive, negative, unlabelled

**Only measured labels count.**
- A measured label is a TNS spectroscopic classification of the object filed by a reporter that is not a bot.
- It must be crossmatched to the object at ≤ 1″, and filed after the object's first detection.

**These are annotation and are never labels:**
- broker classifier outputs (Fink, ALeRCE, Lasair/Sherlock, ANTARES tags, Pitt-Google): RTN-011 §5.3 "preliminary classifications";
- SNIascore-like bot reports;
- photometric-only classes.

**Positive:** wave-1 frozen map, unchanged.
- **posA:** type starts with `SN `, `SLSN`, `TDE`, `nova`, `LRN`, `LBV`, `ILRT`, `Ca-rich`, `Other`, `other`.
- **posB:** posA minus types starting `SN Ia`.

**Negative:** wave-1 frozen map, unchanged. **neg:** type starts with `CV` or `AGN`.
- **negB,** declared now before any Rubin count and reported beside neg, never replacing it: neg ∪ TNS types starting `Varstar`, `Galaxy`, `QSO`, `Blazar`, `Star`, `M dwarf`.
- Reason for negB: these also mark a spectroscopic slot spent on a non-target (Perley+2020 §2.4 names only AGN and CV). negB is declared before the count, so it is not a widening. Bands are evaluated on neg. negB is sensitivity only.

**Unlabelled is never negative.**
- This holds at any age, at any broker score, and after any waiting period. It is wave-1 agent1 D2 and AST04, reaffirmed.
- An unlabelled object is scoreable by neither class.
- A broker score saying "not a transient" is annotation and changes nothing.

**Sealing order (rule C).** Counts of P, Ng and unlabelled objects are computed only after the non-label count file is hashed. If measured labels cannot be read (TNS without credentials), P and Ng are **UNDEMONSTRATED**, not 0.

## 5. Quantities and symbols

| Symbol | Meaning | Source |
|---|---|---|
| O | distinct cohort objects (merged, X1+X2), any class, labelled or not. Optimistic bound on scoreable objects | this work |
| P, Ng | cohort objects with a measured posA / neg label | this work |
| L | P + Ng, scoreable objects | this work |
| M_obs | LSST nights (dayObs ≥ 20260629) with ≥ 1 science visit, from primary Rubin sources | this work |
| M_sc | observed nights with ≥ k+1 = 9 measured-labelled cohort candidates first detected up to that night. k = 8 from k_slot; +1 because choosing 8 of 8 is no decision | this work |
| N_B,lo = 485; N_B,hi = 12,855 | min and max over the 16 family-B rows (distinct object, binary decision correctness) of N_min at delta 0.018 | planning_mde_bracket.csv |
| N_A,lo = 40; N_A,hi = 1,515 | min and max over the 16 family-A rows (night, precision@8) of N_min at delta 0.018 | planning_mde_bracket.csv |

**Why lo and hi.**
- A cohort below N_lo cannot resolve delta 0.018 under the most favourable σ_d the bracket admits.
- A cohort at or above N_hi resolves it under the least favourable.
- Between them, resolution depends on a σ_d that only I1 can measure. That is a parameter the human or I1 must supply, which is ladder rung 2: escalate.

## 6. Bands per axis (P4)

Each axis takes exactly one of PROCEED, ESCALATE or CLOSE, or UNDEMONSTRATED when its number cannot be computed.

### positive_supply (value P; optimistic bound O; nights M_obs)
- **CLOSE:** O < N_B,lo (485) **and** M_obs < N_A,lo (40). Both unit designs have an optimistic bound below the most favourable N_min. No labelling of the existing cohort can resolve delta 0.018 under any bracket row.
- **PROCEED:** P ≥ 1 **and** (L ≥ N_B,hi = 12,855 **or** M_sc ≥ N_A,hi = 1,515).
- **ESCALATE:** every other computed case.
- **UNDEMONSTRATED:** P cannot be computed (no measured-label read). O and M_obs are still reported, and CLOSE can still fire from them because CLOSE needs no label.

### negative_supply (value Ng)
- **CLOSE:** the same optimistic condition as positive_supply (O < 485 and M_obs < 40).
- **PROCEED:** Ng ≥ 1 **and** (L ≥ 12,855 **or** M_sc ≥ 1,515).
- **ESCALATE:** otherwise. This includes Ng = 0 with O ≥ 485, because labels accrue.
- **UNDEMONSTRATED:** Ng cannot be computed.
- **Why "≥ 1 of each class":** with zero negatives in a round, every pick in both arms is correct. precision@8 is then 1 for both arms, d = 0, and the round carries no information about separation (definition of precision@k; family A). The same holds with zero positives (precision 0).

### contamination_exposure (Rubin cohort; value E = cohort objects whose first detection is at or after the admission boundary and whose measured label, if any, is filed after the decision seal)
- **CLOSE:** E = 0 with O > 0.
- **PROCEED:** every subject in the frozen subject set has a published cutoff, **and** E meets the supply PROCEED threshold (E-labelled ≥ 12,855 or its night equivalent).
- **ESCALATE:** otherwise, including when any subject lacks a cutoff. Gemini 3.1 Pro currently has none, per exposure_key_slot, and the subject set is the human's to change.
- The leaks from agent3 §3 are listed with the count, not banded: host-galaxy redshifts in pre-cutoff catalogs, archival variability, the IAU SN prefix, and web access to TNS.
- Ownership: this axis belonged to agent 3 in wave 1. The band is declared here for the Rubin cohort because no Rubin-cohort contamination count exists yet. It is offered for ratification.

### tool_coverage (value = FM/deep channels verified on real Rubin alerts, and classical counterparts verified per channel)
- **Temporal validity.** Wave 1 already counted 0/25 on Rubin (agent4 §3). A band declared now is post-hoc for that count and **must not be ruled against it**. The band governs only a recount performed after this file's hash.
- **CLOSE:** no FM or deep channel in the inventory accepts inputs the Rubin alert packet v11.1 carries. That is structural unavailability (supply.md, tool coverage "one channel structurally unavailable").
- **PROCEED:** ≥ 1 FM/deep channel verified on Rubin alerts **and** ≥ 1 classical counterpart verified for each such channel. This is the manifest.md ratification check.
- **ESCALATE:** otherwise.
- Ownership: agent 4. Declared here for P4 completeness and for ratification.

### cluster_structure (value = raw alerts or diaSources beside distinct objects, overstatement %)
- **PROCEED:** a distinct DIAObject count exists for ≥ 1 broker serving LSST, with raw reported beside it, **and** every broker's distinct count falls in the same supply band as every other (O vs 485; L vs 12,855).
- **ESCALATE:** broker distinct counts disagree in a way that places the cohort in different supply bands. The disagreement is listed, not reconciled.
- **CLOSE:** never from this axis alone. A raw-only count is refused (rule 1), not closed.
- **UNDEMONSTRATED:** only alert or diaSource rows are obtainable (X4).

### split_integrity (value = S1 straddlers, plus cohort objects that a different broker places before the boundary)
- **PROCEED:** the count is computed, and O minus these objects falls in the same supply band as O.
- **ESCALATE:** removing them moves the cohort across a band edge (485 or 12,855).
- **CLOSE:** never from this axis alone.
- **UNDEMONSTRATED:** first-detection history is not obtainable for the cohort.

### unprocessable_units (value U = candidate records lacking diaObjectId, position or first-detection time)
- **PROCEED:** U computed, and O and O + U fall in the same supply band.
- **ESCALATE:** they do not.
- **UNDEMONSTRATED:** U cannot be computed.
- Unprocessable records are documented, never repaired.

## 7. P4 combination rule

**Preconditions.** Each one unmet means no ruling; name it.
- **(a)** Every one of the seven axes carries a number for the Rubin cohort, not for BTS.
- **(b)** Each axis's band was hashed before its count. For tool_coverage, that requires a recount after this hash.
- **(c)** The label source is ratified at D5, or P and Ng are computed from measured labels as defined in §4.

**Ruling:**
- **CLOSE** if any axis is in CLOSE.
- **PROCEED** if all seven are in PROCEED.
- **ESCALATE** otherwise.

**Binding axis:**
- **Under CLOSE:** every axis in CLOSE, listed.
- **Otherwise:** the axis with the smallest ratio of value to its PROCEED threshold. For supply that is L/12,855 or M_sc/1,515, whichever is larger. For tool coverage it is verified/required. Non-ratio axes (cluster, split, unprocessable) bind only when they are in ESCALATE. Ties are listed.
- **When refusing:** the unmet precondition whose resolution needs the most survey time or an external input. The reason is stated.

**Disagreement handling.** Brokers are evaluated separately. If brokers place an axis in different bands, the axis takes ESCALATE and the disagreement is listed.

## 8. Anti-widening

After any count, none of the following may change:
- the admission boundary;
- the unit and crossmatch rules X1–X4;
- the detection definition;
- the label maps (posA, posB, neg, negB);
- the "unlabelled is never negative" rule;
- the thresholds 485, 12,855, 40, 1,515 and k+1 = 9.

A change needs a new hashed registration with its cause, and invalidates every count made before it.

## 9. Lag versus policy for the 2026 label collapse (calibration only; addition B)

Declared before computing anything in `scripts/label_accrual.py`. Inputs:
- the BTS file, `data/raw/ztf_bts_all_2026-09-16.csv`, sha256 61415979…e570;
- three Internet Archive captures of the explorer default page: 2024-12-08T23:13:31, 2025-08-10T06:50:56, 2026-07-25T03:35:57. Parsed with agent 3's `parse_capture`, reimplemented unchanged.

**Age.** Age = snapshot date − peak date, with peak = peakt + 2458000 JD. Age bins in days: [0,30), [30,60), [60,120), [120,240), [240,365), [365, ∞).
- Reason for the bin edges: 30 d is wave-1 flag F4, label_immature (Fremling §2.3, 7-day triggers reviewed about weekly). 60 d is amendment A1. The larger edges are successive doublings up to one year. The doublings are a coverage choice, not a threshold that decides anything.

**Reference accrual.** For each pre-2026 capture C ∈ {2024-12-08, 2025-08-10}, f_C(bin) = fraction of objects in the capture that are labelled (type ≠ "-"), by age at the capture date. Only objects that peak before the capture date are used.

**Observed.** Objects peaking in calendar 2026:
- (i) in the 2026-07-25 capture, age at that capture date. This is the primary comparison, because it uses the same page population as the references.
- (ii) in the 2026-09-16 file, age at 2026-09-16. Secondary, because the population differs (all objects vs the quality-cut page).

**Expectation under LAG.** For each observed object i, p_i = f_C(bin_i). The expected labelled count is E_C = Σ p_i. The observed labelled count is X.
- The one-sided tail P_C = Pr(X' ≤ X) is taken under a Poisson-binomial with {p_i}.
- It is computed exactly by convolution. Objects in bins where C has no objects are excluded, and the exclusions are counted.

**Report-lag distribution.** For objects in capture C1 unlabelled at C1 and present in a later snapshot C2 (the later capture, or the file):
- the share labelled by C2, by age at C1;
- for those that became labelled, the lag bracket (C1 − peak, C2 − peak] in days.

**Decision rule.** Alpha = 0.05 from power.py's default, which produced the bracket.
- **POLICY:** P_C < 0.05 for **both** reference captures in comparison (i), **and** for both in comparison (ii).
- **LAG:** P_C ≥ 0.05 for **both** reference captures in comparison (i).
- **UNDEMONSTRATED:** in any other combination, or if comparison (i) has zero includable objects. This covers references that disagree with each other, or (i) and (ii) disagreeing.
- Disagreements between references are listed, not reconciled.

**What the ruling is not.**
- It does not name the policy.
- It governs no Rubin claim.
- It informs only whether a label-accrual wait is expected to fill P and Ng.
