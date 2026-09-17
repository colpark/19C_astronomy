# Wave 4 · Agent 5: integrity close-out

> Agent 5 returned this report as text because the harness blocks REPORT.md writes. The coordinator saved it here without changing its substance.
>
> **Coordinator action taken after this report:** quarantine option A was executed in a separate commit.
> - The five Q1/Q2 files were copied to the gitignored `holder_handover/quarantine/`, with the hashes checked against QUARANTINE.md, then untracked.
> - `.gitignore` was extended to cover `**/score_*.txt` and `**/verdicts*.json`.
> - Git history is unchanged. Options B and C were not run.

## Pre-checks
- **Brief hash:** verified (`8f101811…1b58`).
- **Scope:** no git was run and nothing outside this directory changed. The wave-3 `transfer_record.json` still hashes to `945c1ca4…`.
- **Distribution:** nothing was published or sent.
- **Log:** steps 0–8 in `order_of_operations.log`, each with a sha256.

**Disclosure (step 2a).** The first leak-scan run did not exclude the two RULINGS_SEALED.csv files by name. It read their bytes for pattern counts and printed only path, sha256 and "R4: 2"; no content was seen. The exclusion was added and the scan re-run.

## 1. Custody (ruling 2): PENDING_RECEIPT. RECEIVED not granted
Three places were checked for a receipt:
- **Wave-3 `transfer_record.json`:** `receipt_hash` is an empty string.
- **Wave-3 `transfer/`:** contains only PACKAGE_SHA256SUMS and the unfilled RECEIPT_TEMPLATE.txt, both unchanged. A repo-wide search for `*receipt*` finds only that template.
- **Environment:** variable names only; none matches receipt, holder, transfer or rulings.

`custody_status.json` records three things:
- The brief's statement that the handover happens today is an assertion only.
- Holder identity and non-authorship are unverified.
- Every blind result keeps "procedural", including wave 1's 20/20 and wave 3's opaque 20/20 (delta 0).

No `transfer_record_v2.json` was written.

## 2. Quarantine
**How the scan worked.**
- It covers the whole repo, excluding code/, sources/, data_cache/, .git and both rulings files.
- It matches on filename and on content patterns.
- First commits were read directly from `.git/objects` with Python (no git binary; no packfiles present).

**`QUARANTINE.md`** is the permanent leak record. Each entry gives path, sha256, the rule that flagged it, first commit, and whether it is in HEAD.

| Group | What | Files |
|---|---|---|
| Q1, quarantine target | score listings with every case and its polarity | `astronomy/replay/evaluator/score_{all,development,sealed}.txt`, first commit `b50d5ca5…` (2026-09-16T17:52:21Z) |
| Q2 | verdict files equal to polarity because they scored 20 of 20 | wave-1 `verdicts.json` (`b50d5ca5…`); wave-3 `verdicts_opaque.json` (`20391f66…`), keyed by opaque id |
| Q3 | files with a polarity column by design | both `cases.csv`, 14 per-agent `replay_cases.csv`, `P2_controls_cases.csv` |
| Q4 | prose naming cases with their polarity | 12 files, e.g. REPLAY_PLAN.md (42 matching lines), agent 5's wave-2 and wave-3 reports, SYNTHESIS.md |
| Clean | name-only matches | blind and opaque inputs; `dummy_verdicts.json` is a false positive (hash-derived values) |

**Which evaluations could have been exposed:**
- **Wave-1 evaluator:** Q1 did not exist yet, since it comes from scoring that run. `cases.csv` and the agent `replay_cases.csv` files were in the tree.
- **Wave-3 opaque evaluator:** Q1 was committed, but its prompt forbade the directory, and the evaluator reported opening nothing forbidden.
- **Both:** exposure is possible and cannot be verified.

**Why moving files does not unleak.**
- The files persist in every past commit.
- All 29 commits were already pushed to github.com/colpark/19C_astronomy. The repo's visibility was not checked.
- A history rewrite does not reach existing clones, and it was blocked by the permission layer before.
- Polarity is still recoverable from `cases.csv`, the K/N ids, and the verdict files that scored 100%.

**Commands written for the coordinator**, plus their effects:
- **A:** move and untrack Q1/Q2.
- **B:** optionally untrack Q3/Q4 (coordinator or PI decision).
- **C:** history rewrite. REQUIRES PI AND USER APPROVAL. Not recommended.

**Supporting files.**
- **`evaluator_prompt_forbidden_paths.txt`:** 42-line canonical forbidden-path list.
- **`EVALUATOR_PROMPT_v2.md`:** includes that list verbatim (a script confirmed all 42 lines). It moves verdict output under a gitignored `holder_handover/verdicts/`, with a write-and-hash exception for that file.
- **`holder_side_scoring_protocol.md`:**
  - per-case scores, verdicts, maps and translated outputs live only under `holder_handover/`;
  - only aggregates and hashes are committed;
  - the coordinator runs `leak_scan.py` before each commit.

## 3. Community notes (drafts, PI review only)
Both notes are marked DRAFT – PI REVIEW – NOT FOR DISTRIBUTION.

**`notes/label_provenance_note.md`:**
- BTS label categories
- the Classifier/s marker rule
- archived-page evidence (ZTF_Bot1 sends both kinds of report; later SNIascore strings carry human names)
- bound history: [0, 3131] → [803, 2247] → [954, 2057]
- category counts, weak points, and refusal-14 counts

**`notes/rubin_tool_readiness_note.md`:**
- pass criterion
- JSON-not-Avro qualifier (HTTP 400)
- tally: 2 PASS / 14 FAIL / 9 UNDEMONSTRATED
- failure stages: 12 parse, 2 emit, 4 reclassified from infer
- 25-row per-tool table
- limits, including the 160 vs 158 run-count disagreement

**Rule E.** Numbers that bear on a ruling carry `[V: id pending]` markers: L01–L05 and T01–T03. At drafting time, module V had sealed blind derivations for T01–T03 but had no comparison records, and had nothing sealed for L01–L05.

**Checker (`scripts/check_notes.py`).** It flags:
- a missing locator
- a locator that does not resolve
- a number not found at its locator
- any directional or comparative phrase, including "than"
- a missing banner

Runs (log in `notes/checker_logs/check_notes_log.txt`):

| Run | Input | Result |
|---|---|---|
| 1 | first draft of the tool note | fired on real defects: a checker bug with nested-bracket locators, and 3 group-size numbers not found at their locator. Both fixed; totals now cite `logs/tool_stage_tally.json` |
| 2 | planted controls | 8 flags across all 5 types, exit 1 |
| 3 | both final notes | 0 flags over 90 claim units, exit 0 |

**Limit:** the checker confirms each number appears at its locator, not what the sentence means.

## 4. Replay cases (`replay_cases.csv`, rulings in `replay_rulings.csv`)

| Case | Stage | Polarity | Source |
|---|---|---|---|
| W4A5-01 | A2 | must_fire | RECEIVED flipped on the brief's word, with an empty receipt hash |
| W4A5-02 | A4 | must_not_fire | the wave-3 delta-0 write-up, with limits and "procedural" kept |
| W4A5-03 | D1 | must_fire | derived totals cited to a locator that does not hold them (checker run 1) |
| W4A5-04 | R7 | must_not_fire | the scanner's false positive on dummy verdicts, classified before action |

All four are from real events. The audit shows "nothing sealed", which is expected because the holder assigns seals.

## Status

| Item | Status |
|---|---|
| Custody | **PENDING_RECEIPT** (RECEIVED not granted; needs a verified receipt hash) |
| Quarantine record, forbidden list, v2 prompt, holder-side protocol | **PASS** (written) |
| Move or untrack leaking files | not done by agent 5 (coordinator ran option A afterwards) |
| History rewrite | not done; requires PI and user approval |
| Community notes | **PASS** as drafts (checker 0 flags; controls fire) |
| Rule-E numbers in notes | waiting on module V records |
| Replay cases | 4 (2 must_fire, 2 must_not_fire) |
