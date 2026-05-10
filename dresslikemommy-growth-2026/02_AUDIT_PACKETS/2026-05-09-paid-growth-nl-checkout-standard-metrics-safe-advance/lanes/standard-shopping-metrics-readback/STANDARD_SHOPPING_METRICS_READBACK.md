# Standard Shopping Metrics Readback

Generated: 2026-05-09.

Mode: read-only Google Ads browser/CDP readback for campaign `23802638621` / `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`. No Save, Apply, Edit, Enable, Pause, Upload, budget, bid, product-group, product-scope, feed-label, conversion-goal, Merchant, Shopify, Pinterest, or live-spend action was taken.

## Result

- Decision: `ALL_TIME_READBACK_PASSED_CUSTOM_RANGE_PENDING_NO_ADS_WRITES`
- Campaign visible: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`
- Status: Enabled / Eligible
- Campaign type: Shopping
- Budget visible: `US$20.00/day`
- Date range visible in Google Ads UI: all time, `2017-05-04` to `2026-05-09`
- UI timezone note: `(GMT-07:00) North American Pacific Time`

## Campaign Metrics

| Metric | Readback |
|---|---:|
| Clicks | `82` |
| Impressions | `3,962` |
| CTR | `2.07%` |
| Average CPC | `US$0.23` |
| Cost | `US$18.60` |
| Conversion rate | `0.00%` |
| Conversions | `0.00` |
| Cost / conversion | `US$0.00` |
| Conversion value | `0.00` |

Compared with the prior 2026-05-06 baseline (`81` clicks, `3,906` impressions, `US$18.58` cost, `0.00` conversions/value), all-time movement appears to be `+1` click, `+56` impressions, `+US$0.02` cost, and still `0.00` conversions/value. This is an inferred delta from two all-time readbacks, not a custom post-bid-change date-range export.

## Product Groups

| Product group | Impressions | Clicks | Cost | Avg CPC | Conversion rate |
|---|---:|---:|---:|---:|---:|
| All products | `3,962` | `82` | `US$18.60` | `US$0.23` | `0.00%` |
| `us_test_ready / daddy_me` | `288` | `3` | `US$0.68` | `US$0.23` | `0.00%` |
| `us_test_ready / family_matching` | `197` | `3` | `US$0.70` | `US$0.23` | `0.00%` |
| `us_test_ready / mommy_me` | `1,957` | `35` | `US$7.65` | `US$0.22` | `0.00%` |
| `us_test_ready / pajamas` | `165` | `6` | `US$1.42` | `US$0.24` | `0.00%` |
| `us_test_ready / swimsuits` | `1,355` | `35` | `US$8.15` | `US$0.23` | `0.00%` |
| Everything else in All products | `0` | `0` | `US$0.00` | `-` | `0.00%` |

Readback also showed the included child product-group max CPC values as `US$0.04`; Everything else in All products remained excluded. No product group was edited.

## Search Terms

Visible search-term total:

- Clicks: `58`
- Impressions: `2,486`
- CTR: `2.33%`
- Average CPC: `US$0.23`
- Cost: `US$13.60`
- Conversions: `0.00`

Top visible terms:

| Search term | Match type | Clicks | Impressions | Cost | Conversions |
|---|---|---:|---:|---:|---:|
| `mommy and me dresses` | Exact | `13` | `482` | `US$2.99` | `0.00` |
| `matching sibling outfits` | Exact | `3` | `12` | `US$0.70` | `0.00` |
| `mommy and me outfits` | Exact | `3` | `101` | `US$0.75` | `0.00` |
| `family matching outfits` | Exact | `2` | `38` | `US$0.48` | `0.00` |
| `matching mom and me dresses` | Exact | `2` | `5` | `US$0.50` | `0.00` |

## Evidence

- Campaign page JSON/text/screenshot: `raw/ads_campaign_page_readback.json`, `raw/ads_campaign_page_visible_text.txt`, `raw/ads_campaign_page_screenshot.png`
- Product groups JSON/text/screenshot: `raw/ads_productgroups_readback.json`, `raw/ads_productgroups_visible_text.txt`, `raw/ads_productgroups_screenshot.png`
- Products retry JSON/text/screenshot: `raw/ads_products_retry_readback.json`, `raw/ads_products_retry_visible_text.txt`, `raw/ads_products_retry_screenshot.png`
- Search terms JSON/text/screenshot: `raw/ads_searchterms_real_readback.json`, `raw/ads_searchterms_real_visible_text.txt`, `raw/ads_searchterms_real_screenshot.png`
- Route probe summary: `raw/direct_route_probe_summary.json`

## Residual Risk

- The readback stayed on the all-time Google Ads date range. The post-2026-05-06 movement is inferred by comparing the all-time current readback to the prior 2026-05-06 baseline, not by reading a custom post-bid-change date range.
- Product rows and search terms were visible-page captures, not a full downloaded export.
- Google Ads UI displayed an ad-blocker warning, but campaign/product/search-term tables still rendered and were captured.

## Next

Use this readback as the current all-time Standard Shopping baseline. Before any Standard Shopping continue/rollback/scale decision, get an approved read-only export or a safe custom-date readback for post-bid-change-only metrics. Any live edit still requires fresh exact owner approval.
