# Amendments to recount_protocol_FROZEN.md (sha256 f32cf288…52e6)

## AM1: deduplicate candidate oids (recorded 2026-09-16 before any light-curve fetch or tool run)
- **Cause, observed.** The ALeRCE LSST `list_objects` page returns more than one row per `oid` (one per classifier row; the classifier keys were stripped by safe_fetch). The sealed v1 list `sealed/alert_ids_SEALED.json` (sha256 0c2f2e03…12ce) therefore accepted 10 entries but only 8 distinct diaObjectIds.
- **Rule conflict.** The protocol's unit is one object per diaObjectId (bands_FROZEN.md).
- **New rule.** Deduplicate the sorted S1 rows on `oid`, keeping first occurrence and order. Walk the distinct list under the same S2 acceptance, stopping at 10 accepted or 40 distinct oids examined. Re-seal as `sealed/alert_ids_SEALED_v2.json`.
- **Kept.** v1 stays on disk, read-only.
- **Unaffected.** Sampling order, acceptance condition and window are unchanged. No outcome or class field was read (the stripped keys are listed in the seal).

## AM2: GHOST provisioning error (recorded before any further GHOST run)
- **Cause, observed.** GHOST alert runs 1–2 (ids 170609056632799366, 170609056632800306) raised `FileNotFoundError: Star_Galaxy_RealisticModel_GHOST_PS1ClassLabels.sav`.
  - That file is part of astro_ghost@d7a1dec6.
  - It was pruned from the wave-1 clone after hashing (`agent4_tools_instrument/code/PRUNED_LARGE_FILES.tsv`, sha256 48f78c9c…0f040).
  - The error is this agent's provisioning, not the tool's behaviour.
- **New rule.**
  - Re-fetch the file from GitHub at the pinned commit; the sha256 must equal 48f78c9c…0f040.
  - The 2 affected runs stay in `run_log.jsonl` and are marked **voided (provisioning)**. They are not counted as FAIL.
  - GHOST then runs on the **remaining 8 sealed alerts only** (alerts 3–10), so the per-tool cap of 10 alert runs holds.
  - The GHOST pass count is reported out of 8 valid runs.
- **Also recorded.** A third GHOST run (alert 3) was killed by this agent mid-run when the error was diagnosed. It produced no log line and no output hash, so it is not counted as a run; alert 3 is run once under the new rule.
