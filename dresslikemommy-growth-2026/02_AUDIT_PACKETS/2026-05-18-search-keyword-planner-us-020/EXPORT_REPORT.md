# Google Ads Keyword Planner Export - Search Long-Tail CPC Gate

Date: 2026-05-18
Account observed: 399-097-6848 dresslikemommy.com
Plan observed: 1420987539

## Requested Export

- Network: Google Search only
- Geography: United States
- Language: English
- Match types: exact and phrase from the source keyword table
- CPC gate: max CPC $0.20
- Required data: Keyword Planner historical stats plus forecast data

## Exported Files

- `google_ads_api_us_search_historical_rows.csv`
  - Google Ads API Basic Access historical metrics export.
  - Filters: United States geo target `2840`, English language `1000`, Google Search.
  - Note: `GenerateKeywordHistoricalMetricsRequest` does not accept per-keyword match type; requested exact/phrase match type is retained from the source matrix for joining.
- `google_ads_api_us_search_forecast_rows.csv`
  - Google Ads API Basic Access single-keyword forecast export.
  - Filters: United States geo target `2840`, English language `1000`, Google Search, explicit `max_cpc_bid_micros=200000`.
  - Note: `GenerateKeywordForecastMetricsResponse` v24 returns clicks, cost, average CPC, conversions, and average CPA; it does not return impressions for this endpoint.
- `google_ads_api_us_search_joined_decision_rows.csv`
  - Joined historical + forecast rows with launch recommendations.
- `google_keyword_planner_saved_keyword_stats_us_google_ui_all_languages_2026-05-18.csv`
  - Raw Google Ads UI Saved Keywords Stats export.
  - Date range: April 1, 2025 through March 31, 2026.
  - UI targeting readback: United States, Google, All languages. The export has no language column.
- `google_keyword_planner_forecast_exact_us_en_google_ui_maximize_conversions_2026-05-18.csv`
  - Raw Google Ads UI forecast export.
  - Date range: June 1, 2026 through June 30, 2026.
  - UI targeting readback: United States, `en`, Google Search.
  - UI forecast controls: Exact global match type, Maximize Conversions.
- `keyword_source_matrix.csv`
  - Source keyword table mapped to ad group, requested match type, requested filters, and actual UI/export filters.
- `keyword_planner_historical_normalized.csv`
  - UTF-8 normalized historical metrics by keyword.
- `keyword_planner_forecast_normalized.csv`
  - UTF-8 normalized forecast rows from the Google Ads UI export.
- `summary.json`
  - Machine-readable export summary and blocker status.
- `google_ads_api_us_search_keyword_summary.json`
  - Machine-readable API rerun summary.

## Readback Summary

- Submitted keywords: 29.
- API historical rows: 29.
- API forecast rows: 29.
- Match types: 26 exact, 3 phrase.
- Keywords with API forecast average CPC at or below `$0.20`: 29.
- Keywords with nonzero API forecast clicks at explicit `$0.20` max CPC: 10.
- Keywords with zero API forecast clicks at explicit `$0.20` max CPC: 19.
- Keywords with Google-reported historical low top-of-page bid at or below `$0.20`: 0.
- Keywords with Google-reported historical low top-of-page bid at or below `$0.50`: 12.
- Forecast period: 2026-05-20 through 2026-06-18.

Priority launch candidates from the API forecast:

| Keyword | Match | Avg monthly searches | Competition | Low top-of-page bid | Forecast clicks | Forecast cost | Forecast avg CPC |
|---|---:|---:|---:|---:|---:|---:|---:|
| `mommy and me pajamas` | exact | 6600 | HIGH / 100 | `$0.510000` | 221.39 | `$29.90` | `$0.135` |
| `mommy and me swimsuits` | exact | 4400 | HIGH / 100 | `$0.450000` | 191.66 | `$28.60` | `$0.149` |
| `matching family swimsuits` | exact | 9900 | HIGH / 100 | `$0.474698` | 142.08 | `$20.60` | `$0.145` |
| `matching family pajamas` | exact | 40500 | HIGH / 100 | `$0.524623` | 29.15 | `$3.23` | `$0.111` |
| `matching family vacation outfits` | exact | 390 | HIGH / 100 | `$0.408262` | 6.76 | `$1.02` | `$0.150` |
| `family cruise outfits` | exact | 110 | HIGH / 100 | `$0.348166` | 3.80 | `$0.53` | `$0.139` |
| `mommy and me pajama set` | exact | 1000 | HIGH / 100 | `$0.499968` | 3.02 | `$0.36` | `$0.120` |
| `daddy and me shirts` | exact | 390 | HIGH / 100 | `$0.425787` | 2.97 | `$0.39` | `$0.133` |

## CPC Gate Status

API_CPC_GATE_COMPLETE_WITH_TOP_OF_PAGE_WARNING.

Google Ads API Basic Access is approved and the read-only export now completed with the requested max-CPC guardrail:

- `max_cpc_bid_micros=200000`
- United States geo target `2840`
- English language `1000`
- `GOOGLE_SEARCH`
- 26 exact rows and 3 phrase rows
- No Google Ads account-serving mutations

Interpretation:

- The hard CPC gate is passable for the 8 launch-priority exact keywords above because forecast average CPC is under `$0.20` and forecast clicks are nonzero.
- The top-of-page gate is not passable at `$0.20`: no keyword has a historical low top-of-page bid at or below `$0.20`.
- This means launch should expect lower-position / constrained-delivery traffic, not top-of-page coverage.
- Keep the zero-click forecast rows out of launch unless they are intentionally used as tiny exact-match probes.

## Remaining Data Limits

No CPC, volume, or competition data is fabricated. The remaining limits are API-method limits:

- `GenerateKeywordForecastMetricsResponse` v24 does not return impressions, CTR, conversion value, or ROAS for this endpoint.
- Historical metrics do not support exact/phrase match-type filtering; match type is retained from the source keyword matrix for campaign construction and forecast calls.
- Forecast conversions and average CPA returned as `0` for these single-keyword forecasts, so purchase ROAS still requires live campaign conversion data.

## Safety Boundary

No campaign, budget, bid, status, feed, conversion-goal, or account-serving changes were made. This was a planner/export workflow only.
