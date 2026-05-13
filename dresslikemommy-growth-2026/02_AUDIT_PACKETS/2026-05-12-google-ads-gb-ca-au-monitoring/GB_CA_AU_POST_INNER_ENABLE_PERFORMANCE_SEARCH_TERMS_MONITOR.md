# GB/CA/AU Post-Inner-Enable Performance And Search-Term Monitor

Generated: 2026-05-12T16:07:39-04:00

Mode: read-only Google Ads UI/CDP route probe. No Save, Apply, Enable, Pause, budget, bid, product-scope, feed, Merchant, Pinterest, Shopify, conversion-goal, billing, or campaign-setting action was taken.

## Executive Readback

The live GB/CA/AU exact Search micro-cohort is enabled and eligible, but reporting is still at fresh-start zero in the visible campaign/ad group/keyword surfaces.

| Market | Campaign | Clicks | Impr. | Cost | Conversions | Conv. value | Search terms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `GB` | `23838895360` | `0` | `0` | `$0.00` | `0.00` | `0.00` | Search terms page reachable through `/aw/keywords/searchterms`; no actionable term rows yet. |
| `CA` | `23834423669` | `0` | `0` | `$0.00` | `0.00` | `0.00` | Search terms page reachable through `/aw/keywords/searchterms`; no actionable term rows yet. |
| `AU` | `23834424182` | `0` | `0` | `$0.00` | `0.00` | `0.00` | Search terms page reachable through `/aw/keywords/searchterms`; no actionable term rows yet. |

## Evidence Notes

- Campaign, ad group, and keyword routes all loaded non-404 and exposed the expected performance columns.
- Direct `/aw/searchterms` and `/aw/search-terms` routes returned `404`; the working route is `/aw/keywords/searchterms`.
- The working search-term page still showed a UI filter chip `Keyword: "human hair wigs"` in the captured text. Because that filter is unrelated to the current GB/CA/AU exact micro-cohort, I did not use the search-term table for optimization decisions.
- Since all three campaigns currently show `0` impressions, `0` clicks, `$0.00` cost, `0.00` conversions, and `0.00` conversion value, there are no buyer-query search terms to mine or negate yet.

## Next Monitoring Action

Run another read-only monitor after Google Ads reporting has enough time to populate. If impressions or clicks appear, reopen the working `/aw/keywords/searchterms` route and clear/avoid the stale unrelated UI filter before acting on search terms. Do not add negatives or change bids/budgets until search terms are actually attributable to the GB/CA/AU exact cohort.

## Evidence Files

- Summary JSON: `raw/perf-search-term-probe/gb_ca_au_perf_search_terms_route_probe_summary.json`
- Route capture directories: `raw/perf-search-term-probe/GB/`, `raw/perf-search-term-probe/CA/`, `raw/perf-search-term-probe/AU/`
- Screenshots and visible text are saved under each route directory.
