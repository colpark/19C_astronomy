# Escalation memo to the PI: Rubin cohort, P4 blocked on measured labels

**This is NOT a P4 ruling.** P4 refuses to rule. `references/stages/supply.md` line 37: "Refuses to rule at all when any of the seven axes in P3 is missing a number". `bands_FROZEN.md` §7: "Each one unmet means no ruling; name it". Positive and negative supply carry no number (`p4_ruling_package.json`).

**Why this memo exists.** This is loop-ladder rung 2 (`references/loop.md` line 41): "blocked on a parameter rather than the threat it protects" → "ruling, escalate now".
- **The blocker** is an external input: measured, human-confirmed spectroscopic labels for cohort objects. TNS is BLOCKED (records dated 2026-09-16 and 2026-09-17), and WISeREP is BLOCKED (live site HTTP 403; 43/43 archived pages 404, including the classified controls).
- **The threat** the labels protect against is scoring on unmeasured or model-annotated truth (ruling 4). That threat stays in force under both options below.
- **Only the PI can supply** the budget line or the closure decision. Rung 2 applies rather than rung 7, because the signature is a named missing input, not an unclassified stall.

Rule E: every priced or ruling-bearing number cites its module-V record (`v_records.json` sha256 462286d6…3a9a, all MATCH and cleared). Numbers without a V record are marked V_PENDING, context only.

## State the options are priced against
- **Cohort after every published cutoff:** O = **1,937,669** objects (V-C01). This is an upper bound: the PPDB is still unreleased, and PPDB-only detections can only lower it (`ppdb_check.json`).
- **Measured labels on cohort objects:** none readable. Positive and negative supply are UNDEMONSTRATED, not zero.
- **Frozen band thresholds for scoreable labelled objects:** 485–12,855 at δ 0.018 (V-N01). The 0.05 values, 63–1,666 (V-N02), are reported beside them and are not a band.
- **Rubin** has been off sky since 2026-07-14 with no return date; the latest primary status post is 2026-09-11. The night count is V_PENDING.

## Option 1: fund a follow-up program that buys measured labels

**Price**, with no existing cohort labels (L = 0), over the frozen grid:
- purity p 0.81–0.967, classification success s 0.93–1.0, capacity c 4.5–10 spectra per night;
- formula: S = ceil(N/(p·s)), H = 0.5·S, W = S − ceil(N/s), nights = ceil(S/min(c, A)).

The arithmetic is V-cleared (V-R01, 288 rows, 0 mismatches). V verified the arithmetic, not the literature sources of the p, s and c grid or the arrival rate A.

| δ (status) | N labelled objects | Spectra | P60-class hours | Nights | Wrong routine commitments (slots) | V record | Months after Rubin returns |
|---|---|---|---|---|---|---|---|
| 0.05 (ratified) | 63 | 66–84 | 33–42 | 7–19 | 3–16 | V-R02 | 1–2 (V_PENDING, context only) |
| 0.05 (ratified) | 1,666 | 1,723–2,212 | 861.5–1,106 | 173–492 | 57–420 | V-R04 | 8–28 (V_PENDING, context only) |
| 0.018 (prior; frozen band lo) | 485 | 502–644 | 251–322 | 51–144 | 17–122 | V-R03 | 2–9 (V_PENDING, context only) |
| 0.018 (prior; frozen band hi) | 12,855 | 13,294–17,065 | 6,647–8,532.5 | 1,330–3,793 | 439–3,242 | V-R04 | 70–115 (V_PENDING, context only) |

**Additional terms and caveats:**
- **Missed rare events** cost at least 100 slots each (wave-3 PI ruling 2, cost of action; asymmetric). The miss rate is UNDEMONSTRATED, so this term has no number and can only raise the price.
- **"Nights"** in V-R02–R04 is the frozen-table column `rubin_on_sky_nights`: nights with Rubin arrivals, capacity-limited. Agent 2's wave-4 table labels the same numbers "usable P60 nights". The two labels disagree; the disagreement is listed, not reconciled.
- **The months column** comes from `truth_cost_monthly.json` (sha256 2f679148…52bf) under an unverified calendar model. It is V_PENDING context and not a price.

**Conditions:**
- **Ruling 4.** A paid claim counts **human-classifier-confirmed labels only**. Model-annotated labels are excluded, with a both-ways sensitivity row. The program must record the classifier of every spectrum, not only its type.
- **Start depends on Rubin.** A cohort follow-up program needs new arrivals or still-observable cohort objects.
  - With Rubin off sky since 2026-07-14 and no return date, the start date is **UNDEMONSTRATED**.
  - The wave-3 cohort (1,937,669 objects, V-C01) was first detected before Rubin went off sky. Whether a spectrum taken now can still measure the class of those objects is UNDEMONSTRATED; nothing read here establishes it either way.
  - In practice, "after return" is the earliest the priced nights can begin.
- **What funding N does under the frozen bands.**
  - Supply PROCEED requires L ≥ 12,855 (V-N01): the δ 0.018 row at N = 12,855, i.e. 13,294–17,065 spectra (V-R04).
  - Buying N = 63 or 1,666 at the ratified δ 0.05 reaches a PROCEED threshold only if the PI first registers new bands at δ 0.05. That is a hashed registration made before the labels are counted (rule A; `bands_FROZEN.md` §8).
- **Even with (a) cleared, two axes still read ESCALATE** (stated, not ruled):
  - **contamination_exposure:** PROCEED needs every subject to have a published cutoff. Gemini 3.1 Pro (preview) has none, so this needs a subject-set change.
  - **tool_coverage:** PROCEED needs a verified classical counterpart for each verified FM channel. CATS passes 5/10 (V-T02), but its Rubin counterparts fail at emit (inside the 2/14/9 tally, V-T01). A subject-set change does **not** clear this; it needs a counterpart that runs end to end on Rubin rows.
  - Disagreement with the assignment wording "both ESCALATE unless the subject set changes": that holds for contamination only.

## Option 2: close the astronomy candidate

**No frozen band yields CLOSE**, so closure would be a PI "close" ruling (`references/loop.md` line 23: "write the finding, end the candidate"), not a P4 CLOSE. On cleared numbers:
- **supply:** O = 1,937,669 ≥ 485 (V-C01, V-N01);
- **contamination:** E = 1,937,669 > 0 (V-C01);
- **tool coverage:** CATS 5/10 > 0 (V-T02).

**The number that would justify closing is the price of truth against the ratified budget.**
- The smallest priced program (δ 0.05, N = 63) needs **66–84 spectra, 33–42 P60-class hours and 7–19 nights (V-R02)**.
- A program reaching the frozen supply band (N = 12,855) needs **6,647–8,532.5 P60-class hours (V-R04)**.
- The ratified budget (1,000 agent-arm cells + 200 engineering hours; PI_RULED, no V record) holds **0 telescope hours**.
- Measured labels are blocked on both public channels.
- So the binding axis (measured labels) cannot move without spend outside the ratified budget.

**Weakest point, stated.** The case rests on a budget with no spectroscopy line plus an input that is blocked, not on a measured count failing a band. If the PI adds telescope time, the case for closing lapses.

**What is lost by closing** (V ids; no directional benchmark claim):
- the prospective cohort: 1,937,669 objects first detected after every published subject cutoff (V-C01), with 521,920 straddlers already separated out (V-C03). Few domains offer units born after the cutoff (SYNTHESIS §6);
- the only FM/deep channel that ran end to end on Rubin rows: CATS, 5/10 (V-T02; tally 2/14/9, V-T01);
- the calibration instruments already measured on BTS (contamination FAIL, calibration only):
  - decision-time power rows V-P01–V-P08, e.g. the k-binding night row: σ_d 0.089778, N_min 196 at δ 0.018 and 26 at δ 0.05 (V-P02);
  - 61 of 579 nights k-binding (V-K01);
  - AUC tables V-A01–V-A04.
  None of these supports a claim; closing forfeits their use on Rubin.

## What the PI is asked to decide
1. **Option 1:** fund a human-confirmed spectroscopic label program (choose the N row and δ; if δ 0.05 is to gate PROCEED, register bands at 0.05 first). Or **Option 2:** close the candidate with the finding above.
2. **Under either option,** whether to change the subject set (Gemini 3.1 Pro has no published cutoff). This alone decides whether contamination can ever read PROCEED.
