# Agent 1 corpus rules: FROZEN before any count under these rules

Frozen: 2026-09-16, before `scripts/build_corpus.py` was written or run.
The sha256 of this file is recorded in `corpus_rules_FROZEN.sha256` and re-checked by `build_corpus.py` before it counts anything. A changed hash aborts the build.

## Disclosure of what was seen before freezing

Before writing these rules I inspected the raw file's schema only: column names, the number of data lines (`wc -l` = 11,218 including the header), per-column counts of the literal tokens `-` and a leading `>`, the distinct `type` strings and their frequencies, the `peakfilt` values, and whether `ZTFID` or `IAUID` repeat (0 repeated ZTFID, 13 repeated non-`-` IAUID). No inclusion, exclusion, positive, negative, cluster or split count was computed. The type-string inventory was used to write the label map below so that no string is left unmapped. That is disclosed here rather than hidden.

## Governed decision and unit

- Decision: spectroscopic follow-up allocation. Each round commits k spectroscopic slots across the candidate transients saved that round.
- Candidate population represented by this file: objects saved to the ZTF BTS program by human scanners after the alert filter (Perley et al. 2020, section 2.1; BTS explorer documentation). This file is not the alert stream. Unsaved alerts are absent by construction.
- Counting unit: a **distinct astrophysical object**, defined in D3 as a positional cluster at the measured cut. Rows, ZTF IDs, IAU IDs, alerts and detections are not units.

## Inclusion rules (applied to every row, in order; first failing rule is recorded)

- I0. The input file sha256 must equal `61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570` (data/raw/SHA256SUMS). Otherwise abort, count nothing.
- I1. `ZTFID` matches `^ZTF\d{2}[a-z]{7}$`. Fail -> exclude under E1.
- I2. `RA` and `Dec` parse as sexagesimal ICRS coordinates. Fail -> exclude under E2.
- I3. `peakt` parses as a finite number (JD - 2458000, per the explorer documentation "time: Time of peak, expressed as JD-2458000"). Fail -> exclude under E3. `peakt` is the split key, so a row without it cannot be placed on either side of a split.
- I4. `peakmag` parses as a finite number. Fail -> exclude under E4.
- I5. `peakt` lies in [270.5, 3299.5], that is from 2018-06-01 (public start of BTS, Perley et al. 2020 section 2.3) to the fetch date 2026-09-16 inclusive. Fail -> exclude under E5.

Nothing else excludes a row. In particular these are NOT exclusion rules and become flags (strata) instead, so that nothing is filtered on the outcome or on label availability:

- F1 `unlabeled`: `type` is `-`.
- F2 `bright_18p5`: `peakmag` <= 18.5 (the BTS classification goal, Fremling et al. 2020 section 1).
- F3 `low_b`: |b| <= 7 deg (the alert filter rejects these, Fremling section 2.1 / Perley Appendix A; a row here is an anomaly to document, not to drop).
- F4 `label_immature`: `peakt` > 3269.5 (peak within 30 days of fetch; SEDM triggers stay active 7 d and requests are reviewed about weekly, Fremling section 2.3 / Perley section 2.2, so labels for these may not have settled).
- F5 `censored_timescale`: any of `duration`, `rise`, `fade` begins with `>`.
- F6 `no_redshift`: `redshift` is `-`. F7 `no_peakabs`: `peakabs` is `-`.

## Exclusion ledger rules

- E1 bad ZTFID; E2 unparseable coordinates; E3 unparseable peakt; E4 unparseable peakmag; E5 peak outside [2018-06-01, 2026-09-16].
- Every excluded row is listed in `corpus_ledger.json` with its ZTFID and rule. Unprocessable fields that do not trigger E1-E5 are documented in the axis ledger as defects and are not repaired.

## Label map (frozen; applies to the `type` string exactly as written)

Positive definition A (`posA`, "worth a BTS spectroscopic slot"): a genuine extragalactic transient, the BTS inclusion goal (Perley section 2.1: "a genuine transient ... extragalactic"; Perley Table 1 "Transients" rows include SN Ia, SN CC, SLSN, TDE, Gap, Novae, Other). A type is posA if it starts with any of:
`SN `, `SLSN`, `TDE`, `nova`, `LRN`, `LBV`, `ILRT`, `Ca-rich`, `Other`, `other`.

Positive definition B (`posB`, rare-class slot): posA types that do NOT start with `SN Ia` (so SN Ia, Ia-91T, Ia-91bg, Ia-pec, Ia-CSM, Ia-SC and SN Iax are all excluded from posB; Iax is thermonuclear per Perley Figure 7d).

Negative (`neg`, spent-slot-on-a-non-target): a type that starts with `CV` or `AGN` (Perley section 2.4: AGNs and CVs "are not part of our project"). Tentative strings with `?` are counted inside neg and also reported separately.

Unlabeled: `-`. Any other string -> `unmapped`, counted and reported, never silently assigned.

Both positive definitions are declared here, before counting. Neither may be widened after a count.

## Clustering rule (D3)

- Link two rows if their angular separation is <= cut (arcsec). Clusters are connected components (friends of friends).
- Sweep cut in {0.5, 1, 1.5, 2, 3, 5, 10, 20, 30, 60} arcsec. Report cluster count at each.
- tau.py measures tightness increasing with cluster count, so the curve is passed to it as `cut = 1/radius_arcsec` (tighter radius = larger cut). The radius is reported beside it.
- The cut is chosen by `scripts/tau.py` with its default saturation 0.05. It is not chosen to increase unit count.
- Controls, run at every cut: must-join = pairs of rows that share the same non-`-` IAUID (the same TNS object under two ZTF IDs); must-not-join = pairs of rows with different non-`-` IAUIDs that are both classified posA and whose peaks differ by more than 365 days are NOT used as a control because nuclear/recurrent events defeat it; instead the must-not-join control is pairs with different IAUIDs and both `type` starting `SN ` (two distinct supernovae cannot be one object).
- Label conflict inside a cluster (members mapping to different label classes) is counted and reported, not resolved.

## Sibling / same-host association (looser, reported separately, never the unit)

Two rows in different clusters at the chosen cut are siblings if separation <= 90 arcsec (the upper host-search radius, Perley section 2.2), both have a numeric redshift, and |dz| <= 0.005 (SN-feature redshift uncertainty, Perley section 2.2 citing Fremling). Sibling groups are connected components of that relation.

## Split integrity

Split key: `peakt`. Two declared split dates:
- S1 = 3095.5 (2026-02-24, first Rubin world-public alerts, NOIRLab sci26008).
- S2 = 3221.5 (2026-06-30, LSST formal start, rubinobservatory.org news "action-rubin-lsst-begins").
A cluster straddles a split if it has members on both sides. Straddlers are counted at every cut.

## Supply counts (P3)

posA, posB, neg and unlabeled are counted at the row level and at the cluster level (chosen cut). A cluster takes a label class only if all its labeled members agree; mixed clusters are counted as `conflict`. Counts are reported overall and in strata F2 and F4. Raw beside clustered with overstatement % = (raw - clustered) / clustered * 100.
