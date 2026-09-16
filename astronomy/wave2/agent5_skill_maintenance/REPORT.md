# Wave 2 · Agent 5: skill maintenance

> Agent 5 returned this report as text, because the harness blocks subagents from writing REPORT.md. The coordinator saved it here without changing its substance.
>
> **Coordinator note: files kept out of git.** The opaque-id maps in `holder_handover/` are gitignored. Committing them to a public repo would undo the blind case files, because original ids reveal polarity (issue 09). They stay local until a rulings holder takes custody. Their sha256 are in `transfer_record.json`: astronomy `a613cbac…7c85`, source suite `3ea29962…de44`.

## Checks before starting
- **Brief hash.** Verified `31a36617…f4eb`.
- **Vendored skill untouched.** No file under `fm-advantage-benchmark/` is newer than BRIEF_SHA256.
- **Nothing run externally.** No git was run and nothing was filed.
- **Sealed rulings not read.** Neither RULINGS_SEALED.csv was opened; both were only hashed.

## How fixes were verified
- Every fix was run in copies under `scratch/` (gitignored), made without the RULINGS files.
- `orig/` is pristine, `s1`–`s6` add one patch at a time, and `apply/` has the full series applied with `patch -p1`.
- `diff -r apply s6` is empty.

## 1. Issue drafts (`issues/`)

| # | Defect | Repro run | Fix | Result |
|---|---|---|---|---|
| 01 | queue.py ZeroDivisionError (line 26) | yes | patch 01 | **PASS** |
| 02 | tau.py line 31 returns CHOSEN on a flat curve | yes | patch 02 | **PASS** |
| 03 | replay.md sealed count, 9 vs 12 | yes | patch 03 | **PASS** (text) |
| 04 | The seal protects rulings text but not polarity | yes | patch 04 | **PASS** |
| 05 (new) | queue.py returns silently wrong intervals before it crashes | yes | patch 01 | **PASS** |
| 06 (new) | tau.py picks a cut just before a large later jump | yes | patch 02 | **PASS** (synthetic only) |
| 07 (new) | tau.py picks a cut where separation has collapsed, and says "separation not supplied" when it was supplied | yes | patch 02 | **PASS** (synthetic only) |
| 08 (new) | Edge and stage counts disagree between SKILL.md and graph.md | yes | patch 08 | **PASS** (text) |
| 09 (new) | Case ids reveal polarity | yes | none | **UNDEMONSTRATED**, blocked on the holder |

### Issue 01: queue.py crashes at large n
- **Where it fails.** The smallest failing n is **1072**: k from 520 to 552 fail at n=1072, and nothing fails at n=1071. All k were checked at both n; k near n/2 was screened from n=1000.
- **At fixed yields.** First failure is at n=1136 for 7154/11183, n=1648 for 1/6, and n=3731 for 5%.
- **Cause.** The 3000-step midpoint sum underflows to t == 0.
- **Fix.** A stdlib log-space regularized incomplete beta.
  - Largest difference from `scipy.stats.beta.ppf`: 7.8e-15 on small-n grids, and 4.7e-14 across 2,382 (k, n) pairs.
  - CLI output is byte-identical for 7/40, 1/6 and 9/250.
  - One small-n change: at 1/30 the optimistic queue goes from 575 to 576, because the old upper bound was 0.172174 and the exact value is 0.172169.
  - The corpus repro now returns [0.631, 0.649] with exit 0.

### Issue 05: silent wrong intervals (more serious than 01)
- **At n=1071:** the script prints [0.513, 0.514] around a point estimate of 0.500. The pessimistic queue is 127, below the point queue of 131, and it still reports LICENSED.
- **At 1/100,000 with 1,000,000 remaining:** the upper bound is about 700× too small. The script exits 3 with "Close the domain", which is a false closure.
- **Status.** Patch 01 fixes both.

### Issue 02: tau.py returns CHOSEN on flat curves
- **Repro.** `repro/tau/flat.csv` (1000, 1001, 1002, with no separation column) returns CHOSEN 0.2 with exit 0.
- **Real case.** Agent 1's curve returns CHOSEN 0.0333, i.e. 30″.
- **After the patch.** Both return REFUSE with exit 2. It also refuses a flat curve that does have a separation column (`flat_with_sep.csv`).
- **Must-not-fire curves.** `saturating.csv` (100, 200, 205, 206) and `sep_holds.csv` still return CHOSEN, with identical output.
- **Other behaviour.** The file written by `--out` validates.

### Issue 03: replay.md sealed counts
- **Line 16:** "Twelve cases are marked sealed… Open the nine once".
- **Line 33:** "development, 19 cases". **Line 34:** "sealed, 9 cases".
- **Line 36:** "five of seven extracted". This is also wrong: 3 of the 7 development discovery cases are marked SYNTHETIC, so 4 are extracted, not 5.
- **Audit count.** The sealed column sums to 12.
- **Likely origin.** 19 + 9 = 28, which is every case outside the discovery module. The table probably predates the discovery cases; that is an inference from the arithmetic, not something the file states.

### Issue 04: the seal does not protect polarity
- **Repro.**
  - `emit` prints the answer, e.g. `--- K06  stage=P2  polarity=must_fire`.
  - `score` returns full tallies with no rulings file present.
  - Line 59 judges polarity only.
- **Patch.**
  - `emit` no longer prints polarity.
  - A new `split-polarity` command moves the column into `POLARITY_SEALED.csv`.
  - `audit` and `score` refuse to run while polarity is held out.
- **Scoring unchanged.** Stdout hashes of `audit` and `score` (dev, sealed and all sets) are identical across the original script, the patched script before the split, and the patched script after it.
- **Apply order.** Patch 04 must go after 03, because its replay.md hunk fails standalone.

### Issue 08: counts disagree between SKILL.md and graph.md
- **Edges.** SKILL.md says "twelve" cross-module preconditions, but graph.md has 16 edges.
- **Stages.** graph.md says "Thirteen" stages have no edge, but the table gives 12.

### Issue 09: case ids reveal polarity
- **Source suite.** Every K case is must_fire and every N case is must_not_fire.
- **Astronomy suite.** The `ASTC` prefix marks one polarity.
- **Why no patch.** Re-keying requires editing RULINGS_SEALED.csv, which may not be opened.

### Suite check after the full series
- `python3 scripts/replay.py audit` prints "38 cases across 6 modules … suite shape ok", exit 0, with the same table as before.
- The only difference is a stderr warning from patch 04 while cases.csv still carries polarity.
- Logs: `logs/verification_after_series.txt`, `logs/patch_apply.txt`.

## 2. Patches (`patches/`)
- **Files:**
  - `01-queue-logspace-ibeta.patch`
  - `02-tau-refuse-unbounded-curve.patch`
  - `03-replay-md-sealed-count.patch`
  - `04-seal-polarity.patch`
  - `08-graph-edge-and-stage-counts.patch`
  - `P2-supply-refusals.patch`
- **Application.** All apply in series. Each applies on its own except 04, which needs 03 first.
- **Logs.** Before and after output for each patch is in `logs/`.

## 3. P2 amendment (`amendments/P2_refusals.md` plus a patch to `references/stages/supply.md`)
- **New stage-owned refusals:**
  - **(i)** Refuse a floor/ceiling pair not scored on the same items, split and metric, or a pair selected or tuned on the items it is scored on.
  - **(ii)** Refuse a floor built on features that exist only after the governed decision, judged against the manifest decision epoch.
- **Two rules stated alongside them:**
  - A floor with no ceiling is not a pair.
  - A refused pair neither advances the stage nor closes the candidate.

**Controls** (cases in `P2_controls_cases.csv`, rulings in a separate file):

| Refusal | Must fire (real failure) | Must not fire |
|---|---|---|
| (i) | AST-P2-02 (input column only) | W2A5-P2-N1, **SYNTHETIC**. arXiv:2104.12980 was read in full, and no real held-out matched pair was found |
| (ii) | AST-P2-04 (input column only) | W2A5-P2-N2, real: agent 2's first-alert floor on Galactic latitude (AUC 0.537/0.510), with no ceiling claimed |

**Additional real must-fire case for (i): W2A5-P2-K1.**
- **Source.** The BTSbot Table 6 pair. arXiv:2401.15167 was read in full; §4.1, line 660, picks the production ceiling as "the trial which yields the best test split performance".
- **Consequence.** Wave-1 REPLAY_PLAN's K06 analogue treated that 98% share as usable. Under refusal (i) it is refused.

**Possible contest.** A strict evaluator could fire N2 on the excluded unclassified objects.

**Status:** the amendment text is PASS (the patch applies and the audit is clean). Refusal behaviour is **UNDEMONSTRATED**.

**Verification protocol (not yet run):**
- **Run.** A fresh blind evaluator on AST-P2-02, AST-P2-04, K1, N1 and N2, with opaque ids mixed in among the other 18 astronomy cases.
- **Expected:**
  - fired=true with via=stage for AST-P2-02, AST-P2-04 and K1
  - fired=false for N1 and N2
  - no polarity change on the other 18 cases
  - validator-only 0 for P2
- **Scope.** A pass on AST-P2-02 counts as development only, because the panel wrote that case.

## 4. Rulings transfer: BLOCKED / UNDEMONSTRATED (`transfer_record.json`)
- **Why blocked.** The rulings-holder field is an unfilled [SUPPLY] placeholder. Nothing was handed over, moved or deleted.
- **What would be handed over:**
  - `astronomy/replay/cases/RULINGS_SEALED.csv`, sha256 `6041714a…e2fc` (matches SEAL_SHA256SUMS)
  - `fm-advantage-benchmark/cases/RULINGS_SEALED.csv`, sha256 `69a30ccf…c312` (the first recorded hash of this file)
  - each suite's polarity column, hashed in a documented canonical form without being written to disk: astronomy `ff84a240…af35f`, source `d0f89b30…853d`
  - the two id maps
- **Holder protocol.** Eight steps, in the record.

**Blind case files:**
- **Files.** `blind/fm-advantage-benchmark/cases_blind.csv` (38 rows) and `blind/astronomy_replay/cases_blind.csv` (20 rows).
- **Format.** Columns `case_id,stage,sealed,input`, with opaque ids and rows shuffled with seed 20260916.
- **Checks.** No input contains polarity words or an original id.
- **Limits.**
  - The seed was chosen by this agent, not by a holder.
  - The original cases.csv files with polarity are still in the repo, so custody is procedural only.

## 5. New replay cases (`replay_cases.csv`; rulings in `replay_rulings.csv`)

| Case | Stage | Polarity | Content |
|---|---|---|---|
| W2A5-01 | D3 | must_fire | SYNTHETIC: a patch verified only on its repro, with no must-not-fire curve and no suite audit |
| W2A5-02 | P5 | must_fire | real: LICENSED queue at n=1071 whose interval excludes its own point estimate |
| W2A5-03 | P5 | must_not_fire | real: the verified 575→576 correction |
| W2A5-04 | A3 | must_not_fire | real: a scoring-script change with byte-identical outputs |

- **Audit on these 4 cases plus the 3 P2 controls.** It reports "nothing sealed", which is expected because the holder assigns seals. It also reports "discovery: no must-not-fire", which needs re-checking after the merge.
- **Hashes.** replay_cases.csv `80a2d28a…1a63`; replay_rulings.csv `e2e831b1…0bf40`.

## Verified vs not
- **Verified by running:**
  - every repro, before and after its fix
  - applying the patches, singly and in series
  - the suite audit on the patched copy
  - scoring equivalence under patch 04
  - scipy agreement for patch 01
  - the blind file checks
  - all hashes
- **Not run:**
  - the blind evaluator re-run for the P2 amendment
  - `split-polarity` on the real skill directory
  - tau.py on a real curve with a separation column (none exists before I1)
  - an exhaustive queue.py search below n=1000
- **Blocked on a holder:**
  - the rulings transfer
  - the fix for issue 09
  - any seal with more than procedural weight

`seed_ledger.json` has 45 entries. Every vendored skill file was read in full except the two RULINGS files, which were only hashed. arXiv:2401.15167 and arXiv:2104.12980 were also read in full.
