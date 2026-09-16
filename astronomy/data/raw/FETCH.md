# Raw data fetch log

| File | URL | Fetched (UTC date) | Rows |
|---|---|---|---|
| ztf_bts_all_2026-09-16.csv | https://sites.astro.caltech.edu/ztf/bts/explorer.php?format=csv&subsample=all | 2026-09-16 | 11,217 data rows (header excluded). Corrected from 11,218, an off-by-one in the coordinator's count that Agent 1 caught |

The explorer's CSV starts with a blank line, which was stripped. Nothing else was changed. Hashes are in `SHA256SUMS`. No quality, purity or magnitude filter was applied at fetch time. All filtering is a D2 rule and goes in the exclusion ledger.
