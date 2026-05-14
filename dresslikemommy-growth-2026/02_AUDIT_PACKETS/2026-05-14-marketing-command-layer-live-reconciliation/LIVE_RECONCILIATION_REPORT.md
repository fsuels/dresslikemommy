# Marketing Command Layer Live Reconciliation

Generated: 2026-05-14 05:39 EDT

Mode: read-only live paid-growth reconciliation after the `ops/marketing/` command layer was created. No Google Ads, Pinterest, Merchant, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme writes were made.

## Decisions

| Surface | Current live readback | Decision |
|---|---|---|
| Google Ads GB exact Search | Campaign `23838895360` is `Enabled` / `Eligible`, `$2.00/day`, Search only, presence-only, no campaign conversion override, only exact ad group `194138528537` enabled, `9` other ad groups paused. Yesterday `2026-05-13` showed `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions, and `0.00` conversion value. | `HOLD_MONITOR_NO_WRITE`; no pause/scale/negative decision justified. GB search-term route is readable but has no terms because ads have not shown to enough people in the selected range/filter. |
| Google Ads CA exact Search | Campaign `23834423669` is `Enabled` / `Eligible`, `$2.00/day`, Search only, presence-only, no campaign conversion override, only exact ad group `196679079575` enabled, `9` other ad groups paused. Yesterday showed `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions, and `0.00` conversion value. | `HOLD_MONITOR_NO_WRITE`; search-term review is blocked by stale unrelated UI filter `Keyword: "human hair wigs"`. |
| Google Ads AU exact Search | Campaign `23834424182` is `Enabled` / `Eligible`, `$2.00/day`, Search only, presence-only, no campaign conversion override, only exact ad group `198852670520` enabled, `9` other ad groups paused. Yesterday showed `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions, and `0.00` conversion value. | `HOLD_MONITOR_NO_WRITE`; search-term review is blocked by stale unrelated UI filter `Keyword: "human hair wigs"`. |
| Standard Shopping US | Campaign `23802638621` / `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` is `Enabled` / `Eligible`, Shopping, `$20.00/day`. Yesterday `2026-05-13` showed `17` impressions, `0` clicks, `$0.00` cost, `0.00` conversions, and `0.00` conversion value. Product groups still show `us_test_ready` children at `$0.04`; `Everything else in "All products"` remains `Excluded`. | `HOLD_MONITOR_NO_WRITE`; no Standard Shopping status/budget/bid/product-group/product-scope decision justified. |
| Standard Shopping search terms | Visible yesterday terms: `family pictures outfits`, `family same outfit`, `mommy and me wedding guest dresses`; all `0` clicks, `$0.00` cost, `0.00` conversions. Total campaign search terms: `17` impressions, `0` clicks, `$0.00` cost. | `HOLD`; no negative edit justified from zero-click terms. |
| Pinterest Ads Manager | Advertiser URL for `549756244483` landed on public `https://ads.pinterest.com/` login/sign-up page. Create control was not found. Probe summary recorded login blocker and no saved/created Pinterest object. | `AUTH_BLOCKED`; paused US draft path remains blocked by authenticated controllable Ads Manager access, not by local spec readiness. |
| Merchant US/es age_group | Live product-list RPC found two sampled target `US` / `es` / source `10627981690` rows. Product-detail RPCs for three samples showed effective `n:age_group` and did not reproduce `Missing age group`. Current Merchant prioritized-fixes page did not show `Missing age group`. | `RECLASSIFY_TO_CURRENT_EXACT_EXPORT_REQUIRED`; do not run a repair from the old May 8 export alone. Need a current exact export or another current authoritative all-row readback before any Merchant repair approval request. |
| Merchant prioritized fixes | Current Merchant diagnostics page said `Last updated at 3:09 AM May 14, 2026` and showed `Over capacity for Shopping ads (outside of CSS program)` affecting `73.3K products (21%)`; no `Missing age group` or `Missing local inventory data` text was visible on the captured prioritized page. | `NEW_BLOCKER_DIAGNOSE_READONLY`; investigate paid-cohort impact and whether capacity is account-level noise or affects current Shopping serving. No product/feed removals or capacity request without owner decision. |
| Merchant product-issues download | Browser downloaded `product_issues_2026-05-08_02-52-49.csv` while current page showed a May 14 update. The CSV still contains the old `625` paid `US/es` Missing age_group item IDs, so it is treated as stale/superseded evidence, not today's authoritative export. | `STALE_OR_SUPERSEDED`; useful only to explain the old blocker, not to justify a live repair today. |

## Evidence

- GB/CA/AU monitor: `google-ads-gb-ca-au-monitoring/raw/monitoring_summary.json`
- GB/CA/AU search-term route probe: `google-ads-gb-ca-au-monitoring/raw/perf-search-term-probe/gb_ca_au_perf_search_terms_route_probe_summary__keywords_searchterms.json`
- Standard Shopping readback: `standard-shopping-readback/raw/01_campaign_initial.txt`, `01_productgroups_initial.txt`, `01_searchterms_initial.txt`
- Pinterest access probe: `pinterest-access-readback/pinterest_create_flow_probe_summary.json`
- Merchant US/es source/detail readback: `merchant-us-es-readback/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`
- Merchant prioritized fixes / stale export attempt: `merchant-product-issues-export/raw/product-issues-browser-export/diagnostics_page_text_before_download_priority.txt`, `merchant-product-issues-export/merchant_exact_product_issues_export_result.json`

## No-Write Proof

- Google Ads: opened/read campaign, product-group, and search-term pages plus read-only RPCs; no Save, Apply, Enable, Pause, Upload, budget, bid, negative, product-group, conversion-goal, or status mutation.
- Pinterest: opened Ads Manager URL and a non-committal create-flow probe; no campaign, ad group, ad, product group, budget, bid, catalog, tag, CAPI, source, feed, or audience object saved/created.
- Merchant: opened diagnostics/source/detail pages, used read-only RPCs, and clicked only diagnostics download controls; no upload, sync, source refresh, source edit, product edit, feed change, or save/apply action.
