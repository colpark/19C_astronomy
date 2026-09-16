# Panel brief, wave 2: D5 ratification, Rubin bands, label source, first instrument work

Repo state at issue: b50d5ca. All seven axes counted, no P4 ruling, replay sealed and scored.
Same contract as wave 1: the vendored skill governs, and PANEL_BRIEF.md rules 1 to 10 carry over unchanged. Three additions bind every agent this wave:

- **A.** Declare every band, boundary and definition BEFORE counting the thing it governs.
- **B.** No claim rests on the BTS cohort. It failed contamination. It is calibration material only.
- **C.** Seal any decision or prediction in a hashed file BEFORE reading TNS or any broker page for a post-cutoff object. Reading first contaminates the item.

## PI-supplied D5 inputs (record each as ratified or overridden in the amendment ledger)

- **Budget:** [SUPPLY: arm cells or hours].
- **Cost of action:** [SUPPLY: value of one SEDM spectrum hour and of a wrong commitment]. Until supplied, delta stays 0.018 with its resolution warning attached.
- **k = 8 per night:** RATIFIED, rounding noted.
- **Decision epoch:** new D4 slot. Primary = first alert. Secondary = night 3. Declared now, before any composition runs.
- **Fink RF remapping (agent 4 proposal):** APPROVED as a D5 amendment with cause. Record it, then apply it. Do not touch the wave 1 counts.
- **Rulings holder:** [SUPPLY: a person who wrote neither the skill nor any case].
- **TNS credentials:** [SUPPLY: bot or user account, else agent 2 marks UNDEMONSTRATED].

## Assignments

- **Agent 1, Rubin bands and prospective cohort.**
  - Write the P4 bands for the Rubin stream first. That includes the start boundary choice: 2026-06-29 declaration versus 2026-06-30 announcement.
  - Then count objects first detected on or after the declared start, via public broker mirrors (Fink, ALeRCE, Lasair).
  - Verify return-to-sky status after the July storm.
  - Re-derive the label accrual curve and rule lag versus policy for the 2026 collapse, using TNS report lag on pre-2026 objects from the archive captures.
- **Agent 2, label source.**
  - Split the 7,843 labels into measured versus model annotation per object using TNS reports.
  - Without credentials, tighten the 0 to 3,131 SNIascore bound using the 2021-04-15 auto-report start and reporter fields on public pages.
  - Rule refusal 14 admissibility for the 98 answer-in-source objects.
  - Update label_source_slot.json.
- **Agent 3, manifest freeze.**
  - Assemble the full domain manifest from every slot file and present each derivation with an override invitation.
  - Record the PI decisions above, then freeze and hash.
  - This closes D5 for everything except the two SUPPLY fields, which stay UNDEMONSTRATED if empty.
- **Agent 4, instrument.** Work on the frozen epoch and the BTS calibration cohort only.
  - Build both mechanical compositions blinded:
    - classical: decision-time features into a GBDT, per the approved remapping;
    - deep: ParSNIP or ATAT at the same inputs, with no redshift and no post-spectroscopy columns.
  - Publish and hash both before any arm sees anything (I1), then measure C-1 and C (I2).
  - Write the R1 harness control spec.
  - Every artifact carries the line "calibration only, contamination FAIL on this cohort".
- **Agent 5, skill maintenance.**
  - File upstream issues with minimal repros: queue.py underflow, tau.py flat curve CHOSEN, replay.md 9 versus 12, seal protects polarity.
  - Draft the two new P2 refusals (unmatched floor/ceiling pairs, floors on post-decision features) as a skill amendment.
  - Hand RULINGS_SEALED.csv plus the polarity column to the rulings holder and record the transfer.

## Deliverables per agent

REPORT.md, schema-valid JSON records, sources with seed_ledger, and 2 to 4 new replay cases with at least one must_not_fire, with rulings in a separate file.
No stage advances on time spent. A criterion moves to PASS or FAIL, or the stage says why not.

---

## Coordinator preamble (recorded before any wave-2 agent ran)

1. **The four SUPPLY fields arrived as unfilled placeholders:** budget, cost of action, rulings holder and TNS credentials. Per the brief they are recorded UNDEMONSTRATED. Consequences:
   - S and the P7 ruling stay UNDEMONSTRATED.
   - The rulings transfer (agent 5) cannot happen and is recorded as blocked.
   - Agent 2 works without TNS credentials.
2. **Graph conflict, escalated and not silently resolved.** `references/graph.md` has two edges that apply to agent 4's assignment:
   - **D5 → R1:** no paid work on an unratified manifest.
   - **R1 → I1:** do not build instruments before a known-good subject completes the surface.

   The brief asks for I1 compositions and only an R1 *spec*. D5 cannot fully close while budget and cost of action are empty. Agent 4 therefore builds the compositions as **PRE-I1 CALIBRATION** artifacts. They are hashed and published, but they do not count as I1 records until R1 has run and the PI ratifies the ordering. This mirrors wave 1's PLANNING-ONLY power bracket. It is recorded as an escalation for PI ruling (ladder rung 2), not as an amendment the coordinator granted itself.
3. **Ordering.** Agent 3's freeze reads agent 2's updated label_source slot, so agent 3 starts after agent 2 returns. Agents 1, 2, 4 and 5 run in parallel. Agent 4 cites the decision-epoch declaration in this hashed brief until the frozen manifest exists, then re-checks against the frozen hash.
4. **No upstream location for the skill is known.** It arrived as a zip. Agent 5 writes the issues as ready-to-file drafts under `wave2/agent5_skill_maintenance/issues/` and files nothing externally.
5. **Report files.** The harness blocks subagents from writing REPORT.md. Agents return report text and the coordinator saves it with a banner, as in wave 1.
6. **Rule C applies to the panel.** Panel agents run on Claude Opus 5, which is also in the subject set.
