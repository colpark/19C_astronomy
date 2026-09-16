# Astronomy supply gauge: five-agent panel synthesis

**Candidate:** live time-domain astronomy, specifically the Rubin LSST alert stream plus the ZTF Bright Transient Survey (BTS) as the label base.
**Branch:** prediction.
**Governed decision:** spectroscopic follow-up allocation, i.e. which k transients get a spectrum each night.
**Status:** this is a pre-P1 sketch and not a P4 ruling. No ruling is issued, and §4 explains why the skill still refuses one even though all seven axes now carry a number.

The date is 2026-09-16. Every number below is read from an agent ledger, and the locator for each is given. Nothing here is restated from memory.

## 1. The panel

| Seat | Scope | Ledger |
|---|---|---|
| Agent 1: supply and corpus | D1–D3, P3 (supply, cluster, split, unprocessable), P5 sketch | `agent1_supply_corpus/` |
| Agent 2: prior floor and headroom | P2 | `agent2_floor_headroom/` |
| Agent 3: labels and exposure | D4 label source and exposure key, P3 contamination, D2 refusal 14 | `agent3_labels_exposure/` |
| Agent 4: tools and instrument | D4 tool inventory, P3 tool coverage, I3 cards, I4 sketch | `agent4_tools_instrument/` |
| Agent 5: resolution | D4 k, delta and subject set; D5 inputs; P6/P7 planning bracket; replay design | `agent5_resolution_replay/` |

Seat 1 is the user's specification. The BIOSCAN panel definition is not in this repo, so seats 2–5 were cut along the skill's module boundaries so that each seat holds private evidence, as the skill partitions it. All five ran in parallel from the same brief (`PANEL_BRIEF.md`).

## 2. Seven axes (unit = distinct object at 1″, BTS; Rubin where stated)

| Axis | Number | Disposition | Locator |
|---|---|---|---|
| Positive supply | posA (extragalactic transient) **7,154**; posB (non-Ia) **1,839**. Post Rubin first alerts (2026-02-24): **9**. Post LSST start: **1** | counted | agent1 REPORT §P3 |
| Negative supply | CV/AGN **663**. Truncated by construction: negatives the scanners never saved are absent | counted, truncated | agent1 REPORT §P3 |
| Contamination exposure | Labels public before every subject cutoff: **6,166**. After every cutoff: **0**. Unresolved: 1,677 | **FAIL** (BTS) | agent3 REPORT §3 |
| Tool coverage | Verified on real Rubin alerts: **0 of 25** tools (0/15 FM or deep, 0/10 classical). On ZTF: 2/15 FM or deep, and both were trained on BTS itself | counted; no FM channel covers Rubin | agent4 REPORT §3 |
| Cluster structure | BTS rows→objects: 11,193→11,183 (**0.089%**). Upstream, from design docs: ~60 SN alerts per SN DIAObject (5,900%); ~2,000 whole-stream alerts per SN; ZTF 10⁵–2×10⁵ packets per saved candidate | counted | agent1 REPORT §D3, §P3 |
| Split integrity | Temporal key: **0** objects and 0 sibling groups straddle either Rubin date at 1″ | counted | agent1 REPORT §P3 |
| Unprocessable units | type "-" 3,370; redshift "-" 4,054; censored duration 3,905; IAU "-" 107. Documented, not repaired | counted | agent1 REPORT §P3 |

### Manifest slots

| Slot | Value | Status |
|---|---|---|
| tau | 1″ positional. tau.py's pick of 30″ was refused (it merges 39 distinct-SN pairs); separation needs I1 | DERIVED, not final |
| k | **8 per night** out of 46.4 candidates, so chance **0.172** (arXiv:2401.15167) | DERIVED (ZTF); UNDEMONSTRATED (Rubin) |
| label source | Up to **3,131 of 7,843** labels may be SNIascore model annotation, not measured truth. The file cannot separate them; TNS reports need credentials | **UNDEMONSTRATED** |
| exposure key | ZTF alerts public in real time since 2018-06-04; Rubin alerts world-public since 2026-02-24; label dates bracketed with archive captures | DERIVED, with gaps |
| tool inventory | 25 tools. Roles below the line exist (ParSNIP and SALT3 as scorer/generator), so "needs no agent" does not apply | DERIVED; check (a) fails on Rubin for ATAT and Astromer 1/2 |
| subject set | 7 frontier models with cutoffs from vendor pages; Gemini 3.1 Pro has none | DERIVED; training-data end UNDEMONSTRATED for all |
| delta prior | **0.018**. This is the purity gain practitioners put into production, and it is below its own unpaired MDE of ~0.045 | DERIVED, with a resolution warning |
| S, budget, cost of action | not supplied | **UNDEMONSTRATED** |

## 3. Floor and resolution

- **P2 floor (agent2 §3–4).**
  - On the three matched pairs in the literature, the classical floor takes **0.951–1.000** of the deep-model ceiling. All three are post-hoc: full light curves, and mostly redshift as well.
  - No FM-vs-classical pair on matched data exists at all.
  - In-corpus, SN Ia AUC falls from **0.967** with post-spectroscopy features, to **0.798** at peak, to **0.537** at first alert. Any headroom is therefore at decision-time inputs, where nobody has measured it.
  - Floor share for the governed decision: **UNDEMONSTRATED**.
- **P7 (agent5, planning only).** At delta 0.018, the MDE drops below delta only at **40–1,515 nights** or about **485–12,000 objects**, depending on σ_d. The real σ_d needs I1 compositions.

## 4. Why P4 still refuses to rule

Every axis carries a number, but three preconditions are unmet.

1. **No bands were declared before the count.** P4 rules against bands declared first. Declaring them now over the BTS counts would be post-hoc. The Rubin post-cutoff stream is still uncounted, so bands can still be declared honestly for it.
2. **The positive-supply count rests on an unratified label source.** Some unknown share of the 7,154 positives is model annotation.
3. **The inputs P4 would need are missing.** D5 has not happened, and budget, cost of action and S are absent. A ruling would be a guess at a threshold nobody has set.

## 5. Pre-ruling lean (explicitly not a ruling)

- **Binding axis, most likely contamination × post-cutoff supply.**
  - The BTS base fails contamination outright: no labelled object post-dates every cutoff.
  - The only escape is the prospective Rubin stream, meaning objects first detected on or after 2026-07-01.
  - That stream has barely started. Rubin went off-sky after a storm evacuation on 14–15 July and was still off-sky on 2026-09-11 (agent3 §3).
  - At delta 0.018 it is orders of magnitude short of the MDE bracket.
- **Second, resolution.** Delta 0.018 needs hundreds to thousands of units. An effect near 0.3 would need fewer than 50, and then supply and exposure bind instead.
- **Third, tools.** No channel of either kind has been validated on real Rubin alerts, and the Rubin packet has no host or redshift fields.
- **Likely P4 outcome once preconditions are met: ESCALATE, not CLOSE.** The binding quantity grows with survey time, and the threshold is the human's to set.
  - A CLOSE on the BTS arm alone is defensible today, on contamination.
  - A PROCEED is not.

## 6. What astronomy gives the skill

The skill asks for items whose exposure post-dates every subject. Here that means an alert stream that is world-public on issuance and began after most frontier cutoffs. Those units are born after the cutoff, which few domains can offer.

The leaks do not all close, though (agent3 §3):
- Host-galaxy redshifts and archival photometry predate the cutoff.
- The IAU `SN` prefix encodes the classification.
- A subject with web access can read TNS once a label is filed, so decisions must be sealed first.

## 7. Generality findings: defects the independent corpus exposed in the skill

These are the reason the replay was run. None was visible from the skill's own record. Item 6 comes from the replay itself.

1. **`scripts/queue.py` crashes at large n.** `ZeroDivisionError` in `ibeta` from midpoint-sum underflow. Reproduced: `queue.py --counted 11183 --passed 7154 --survivors 7154 --target 100`. P5 cannot run on a realistic astronomy corpus. Fix: compute the Clopper-Pearson bounds with `scipy.stats.beta.ppf` or in log space.
2. **`scripts/tau.py` returns CHOSEN on a curve that bounds nothing.** On a flat curve (every step under 0.3%), the 5% saturation test passes at the second grid point. There is no must-not-join control, so it picked 30″, which merges 39 distinct supernovae. It should REFUSE when no separation column is present and gains never exceed the threshold.
3. **A single scalar similarity cut is not enough for the unit.** Position alone cannot separate:
   - a re-trigger of one object,
   - a recurrent CV at one position,
   - two supernovae in one host (SN2021sic; SN2023ghl and SN2024gyr at 1.92″).

   Agent 1 needed a temporal clause (amendment A1). The skill's tau model comes from sequence identity and assumes one dimension.
4. **The replay seal protects less than it claims.** `cases.csv` carries polarity, and `replay.py emit` prints it. Since pass/fail is judged on polarity, the sealed rulings file protects only explanation text (agent5 REPLAY_PLAN).
5. **`replay.md` is internally inconsistent.** It says "Twelve cases are marked sealed" but then "Open the nine once" and reports "sealed, 9 cases". `replay.py audit` counts 12 sealed.
6. **P2 has no stage-owned refusal.** Two replay cases passed only through global refusal 1 (see §11).
7. **The load-bearing label distinction transferred cleanly and binds.** Measured vs model-annotated labels map exactly onto human spectroscopic classifications vs SNIascore auto-reports. This part of the skill generalises with no change.

## 8. Cross-agent disagreements (listed, not reconciled)

- **Distinct-object count:** 11,183 (agent1, 1″ positional, amended must-join) vs 11,204 (agents 3 and 5, IAU-name join) vs 11,198 groups (agent2, 3″ plus IAU). The difference is whether 4 same-name pairs with peaks 485–1,598 days apart are one object.
- **LSST start:** 2026-06-29 (RTN-011 formal declaration, agent3) vs 2026-06-30 (announcement, agent1 and the brief).
- **Claude Fable cutoff:** Fable 5.1 = Jun 2026 on the models page vs a Transparency Hub that lists only Fable 5 = Jan 2026 (agents 3 and 5).
- **Rubin dates:** Agent 4 could not verify them from its sources; agents 1 and 3 did.
- **"Thousandfold" overstatement in the brief:** agents 1 and 5 each measured something different: ~60×, ~2,000×, ~21,500× per night, 0.089% in-file.
- **Replay case AST5-04 is contested** on the must-join control and is excluded from the scored replay (`replay/cases/EXCLUDED.csv`).

## 9. What the human must supply (D5) before anything paid

1. **Budget** in agent-arm cells or hours, and **cost of action**: the smallest precision gain that would change your follow-up tool choice. These set delta, S and the P7 ruling.
2. **P4 bands for the Rubin post-cutoff stream,** declared before it is counted.
3. **TNS credentials** (bot or user account) to resolve the measured vs annotation label split per object.
4. **A rulings holder** who wrote neither the skill nor any case (see §10).
5. **A decision on the proposed D5 amendment** that re-maps Rubin classical counterparts to Fink RFs (agent4 §2).

## 10. Coordinator disclosures

- **Reports saved by the coordinator.** The subagent harness blocked subagents from writing `REPORT.md`. Each agent returned its report as text, and the coordinator saved it with a banner saying so.
- **Brief errors.**
  - The coordinator's brief gave 11,218 objects; the file has 11,217 data rows. Corrected in `data/raw/FETCH.md` and the brief after Agent 1 flagged it.
  - The coordinator's prompt to Agent 3 guessed the wrong `peakt` zero point. It is JD−2458000.
- **Commit history.** An early commit swept in mid-run agent files, including embedded third-party clones. A follow-up commit untracked them. A history rewrite was blocked by the permission layer, so they remain in history.
- **Replay seal.**
  - The rulings are in this public repo and are held by the same party that orchestrated the panel.
  - The seal is procedural only, which is exactly the skill's warning. The blind evaluator was instructed not to open them.
  - Two must-not-fire controls, ASTC-01 and ASTC-02, were authored by the coordinator from panel facts. They were added because the suite audit found no must-not-fire case in adjudication or instrument.

## 11. Independent-corpus replay result

**20 of 20 polarity** (14/14 must-fire, 6/6 must-not-fire, sealed 6/6), with **2 unearned**. Scored by the unchanged `replay.py` against a blind fresh evaluator; seal hashes verified. Details: `replay/RESULT.md`.

- This is the first out-of-project evidence that the stage briefs generalise. Read it as consistency, not capability: the cases were written in the skill's own vocabulary, and a clean sweep is the skill's own warning sign.
- **New skill defect.** Both unearned passes are in **P2**, which has no refusal of its own. Add two refusals there: unmatched floor/ceiling pairs, and floors built on post-decision features. The same kind of gap was found in P4 and A1 in the source record.
- **Not covered.** There are no runtime or ladder cases, because no harness has run.
