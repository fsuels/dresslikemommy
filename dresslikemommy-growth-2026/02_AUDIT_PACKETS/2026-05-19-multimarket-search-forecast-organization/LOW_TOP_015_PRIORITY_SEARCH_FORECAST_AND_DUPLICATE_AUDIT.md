# Multimarket Search Forecast And Duplicate Audit

Generated UTC: `20260519T113404Z`

Guardrail: `read_only_google_ads_api_forecast_and_inventory_no_mutations`

Max CPC tested: `0.15` (`150000` micros)

## What This Proves

- This is read-only Google Ads API evidence, not a live build.
- Existing campaign and keyword scope was read before building expansion rows.
- Candidate rows are separated by country and language so future approval packets can reuse existing campaigns where appropriate and create new language campaigns only where no matching scope exists.

## Live Account Inventory Summary

- Live campaign rows read: `20`
- Live keyword rows read: `451`
- Search campaign status counts: `{'ENABLED': 6, 'PAUSED': 10}`

## Forecast Summary By Market/Language

| Market | Rows | New To Scope | Existing Keywords | Rows With Forecast Clicks | Low Top Bid <= $0.15 | Launch Candidates After Review |
|---|---:|---:|---:|---:|---:|---:|
| `CA_FR` | 4 | 4 | 0 | 0 | 4 | 0 |
| `CH_FR` | 2 | 2 | 0 | 0 | 2 | 0 |
| `CZ_CS` | 2 | 2 | 0 | 2 | 2 | 2 |
| `ES_ES` | 10 | 10 | 0 | 7 | 10 | 7 |
| `IT_IT` | 24 | 24 | 0 | 18 | 24 | 18 |
| `NL_NL` | 2 | 2 | 0 | 0 | 2 | 0 |
| `PL_PL` | 20 | 20 | 0 | 8 | 20 | 8 |
| `PT_PT` | 12 | 12 | 0 | 0 | 12 | 0 |
| `RO_RO` | 2 | 2 | 0 | 2 | 2 | 2 |

## Files

- `live_campaign_inventory.csv`
- `live_campaign_criteria_inventory.csv`
- `live_ad_group_inventory.csv`
- `live_keyword_inventory.csv`
- `live_campaign_metrics_last_30d.csv`
- `multimarket_keyword_candidate_matrix.csv`
- `multimarket_historical_rows.csv`
- `multimarket_forecast_summary.json`
- `low_top_015_priority_candidate_matrix.csv`
- `low_top_015_priority_forecast_rows.csv`
- `low_top_015_priority_joined_decision_rows.csv`
- `low_top_015_priority_forecast_summary.json`
- `native_language_launch_candidates_all_markets.csv`
- `MULTIMARKET_NATIVE_SEARCH_EXPANSION_DECISION_PACKET.md`

## Next Use

Use `MULTIMARKET_NATIVE_SEARCH_EXPANSION_DECISION_PACKET.md` and the per-market launch candidate CSVs to build small market/language-specific approval packets. Do not upload duplicate keywords; rows marked `EXISTS_IN_ACCOUNT_DO_NOT_DUPLICATE` should repair or hold the existing structure instead. The full 986-row forecast was intentionally stopped after repeated quota throttling; the priority forecast here is limited to rows with a positive historical low top-of-page bid at or below `$0.15`.
