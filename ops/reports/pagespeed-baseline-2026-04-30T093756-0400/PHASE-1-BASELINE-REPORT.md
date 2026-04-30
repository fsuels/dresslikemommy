# PageSpeed Phase 1 Baseline - Before Changes

- Generated: 2026-04-30T14:26:00.819301+00:00
- Code/theme edits made during Phase 1: none
- Live site root: https://www.dresslikemommy.com

## URL Inventory

- Total localized public routes inventoried: 8784
- Unique canonical/default paths: 424
- Sitemaps fetched/discovered: 85
- Sitemap fetch errors: 0

- homepage: 21
- collection: 945
- product: 6027
- page: 357
- blog_index: 21
- article: 1407
- list_collections: 1
- cart: 1
- search: 1
- customer: 2
- other: 1

Default locale has 424 canonical routes; 20 localized prefixes have 418 sitemap routes each, plus manual utility routes captured in the inventory.

## PSI Status

The direct PageSpeed Insights API batch was attempted but blocked by Google API quota (`429 RESOURCE_EXHAUSTED`, default daily quota 0 for this environment). See `psi/psi-api-blocked.md` and `psi/psi-summary.csv`.

Official pagespeed.web.dev UI capture was completed for the representative theme surfaces. Customer login and 404 were excluded from the PSI UI batch because customer login redirects to hosted Shopify accounts and Lighthouse rejects/returns non-success behavior for intentional 404s.

## Official Pagespeed.Web.Dev UI Representative Scores

| strategy | surface | ok | performance | accessibility | best_practices | seo | lcp | tbt | cls |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mobile | homepage | true | 53 | 92 | 73 | 100 | 22.5 s | 390 ms | 0.002 |
| desktop | homepage | true | 38 | 95 | 73 | 100 | 5.8 s | 1,980 ms | 0.096 |
| mobile | collection_best_sellers | true | 69 | 97 | 77 | 100 | 11.8 s | 100 ms | 0.002 |
| desktop | collection_best_sellers | true | 84 | 97 | 77 | 100 | 2.3 s | 160 ms | 0.06 |
| mobile | collection_dresses | true |  |  |  |  |  |  |  |
| desktop | collection_dresses | true | 61 | 97 | 73 | 100 | 1.4 s | 1,230 ms | 0.001 |
| mobile | product_primary | true | 23 | 89 | 73 | 100 | 7.2 s | 3,120 ms | 0.231 |
| desktop | product_primary | true |  |  |  |  |  |  |  |
| mobile | blog_index | true | 65 | 97 | 73 | 100 | 11.3 s | 270 ms | 0.002 |
| desktop | blog_index | true | 52 | 97 | 77 | 100 | 2.5 s | 1,950 ms | 0.025 |
| mobile | article | true | 61 | 97 | 77 | 100 | 5.0 s | 760 ms | 0.003 |
| desktop | article | true | 89 | 93 | 73 | 100 | 1.0 s | 250 ms | 0.045 |
| mobile | page_contact | true | 77 | 97 | 77 | 100 | 3.8 s | 440 ms | 0.001 |
| desktop | page_contact | true | 94 | 97 | 77 | 100 | 0.8 s | 200 ms | 0.012 |
| mobile | list_collections | true | 54 | 95 | 73 | 100 | 16.8 s | 500 ms | 0 |
| desktop | list_collections | true | 63 | 95 | 77 | 100 | 2.1 s | 660 ms | 0.006 |
| mobile | cart | true | 57 | 97 | 73 | 61 | 15.4 s | 380 ms | 0 |
| desktop | cart | true |  |  |  |  |  |  |  |
| mobile | search | true | 65 | 97 | 73 | 69 | 5.6 s | 440 ms | 0.002 |
| desktop | search | true | 74 | 94 | 77 | 69 | 2.2 s | 310 ms | 0.046 |

Blank score cells mean the UI report loaded but that form-factor text extraction did not produce scores in the automation window; screenshots/text files are still saved under `psi/ui/`.

## Local Lighthouse Representative Scores

| strategy | surface | ok | performance | accessibility | best_practices | seo | lcp_ms | tbt_ms | cls |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mobile | homepage | true | 74 | 92 | 58 | 100 | 5145.36 | 67.0 | 0.012 |
| desktop | homepage | true | 37 | 95 | 58 | 100 | 32305.276 | 349.0 | 0.184 |
| mobile | collection_best_sellers | true | 78 | 97 | 58 | 100 | 5609.902 | 53.0 | 0.003 |
| desktop | collection_best_sellers | true | 58 | 97 | 58 | 100 | 6210.72 | 188.0 | 0.001 |
| mobile | collection_dresses | true | 79 | 97 | 58 | 100 | 4117.341 | 179.0 | 0.09 |
| desktop | collection_dresses | true | 66 | 97 | 58 | 100 | 5298.3 | 129.5 | 0.035 |
| mobile | product_primary | true | 52 | 89 | 54 | 100 | 4810.297 | 126.5 | 0.889 |
| desktop | product_primary | true | 33 | 92 | 54 | 100 | 17397.239 | 212.0 | 0.385 |
| mobile | blog_index | true | 73 | 97 | 58 | 100 | 8217.678 | 24.0 | 0.004 |
| desktop | blog_index | true | 61 | 97 | 58 | 100 | 11444.167 | 66.5 | 0.062 |
| mobile | article | true | 71 | 97 | 58 | 100 | 14474.586 | 207.5 | 0.003 |
| desktop | article | true | 70 | 97 | 58 | 100 | 3991.776 | 45.0 | 0.066 |
| mobile | page_contact | true | 100 | 97 | 58 | 100 | 1537.041 | 31.0 | 0.005 |
| desktop | page_contact | true | 83 | 97 | 58 | 100 | 1989.021 | 27.0 | 0.035 |
| mobile | list_collections | true | 75 | 95 | 58 | 100 | 7190.281 | 23.5 | 0.005 |
| desktop | list_collections | true | 66 | 95 | 58 | 100 | 5668.742 | 43.0 | 0.038 |
| mobile | cart | true | 73 | 97 | 58 | 61 | 10032.293 | 68.0 | 0.003 |
| desktop | cart | true | 57 | 97 | 58 | 61 | 6046.945 | 185.5 | 0.086 |
| mobile | search | true | 54 | 97 | 58 | 69 | 9236.648 | 52.0 | 0.364 |
| desktop | search | true | 61 | 94 | 58 | 69 | 6119.153 | 106.0 | 0.035 |
| mobile | customer_login | true | 71 | 100 | 77 | 58 | 4682.959 | 0.0 | 0.0 |
| desktop | customer_login | true | 58 | 100 | 77 | 58 | 4879.718 | 0.0 | 0.0 |
| mobile | 404 | false |  |  |  |  |  |  |  |
| desktop | 404 | false |  |  |  |  |  |  |  |

The local Lighthouse run saves JSON and HTML for each representative route under `lighthouse/raw/`. It is not a replacement for PSI field data, but it is repeatable for before/after code validation.

## Highest Local Lab Risks To Investigate Next

| strategy | surface | performance | lcp_ms | cls | note |
| --- | --- | --- | --- | --- | --- |
| desktop | product_primary | 33 | 17397.239 | 0.385 | high CLS |
| desktop | homepage | 37 | 32305.276 | 0.184 | high CLS |
| mobile | product_primary | 52 | 4810.297 | 0.889 | high CLS |
| mobile | search | 54 | 9236.648 | 0.364 | high CLS |
| desktop | cart | 57 | 6046.945 | 0.086 | low perf/LCP |
| desktop | collection_best_sellers | 58 | 6210.72 | 0.001 | low perf/LCP |
| desktop | customer_login | 58 | 4879.718 | 0.0 | low perf/LCP |
| desktop | blog_index | 61 | 11444.167 | 0.062 | low perf/LCP |
| mobile | article | 71 | 14474.586 | 0.003 | low perf/LCP |
| mobile | blog_index | 73 | 8217.678 | 0.004 | low perf/LCP |
| mobile | cart | 73 | 10032.293 | 0.003 | low perf/LCP |

## Browser Capture Summary

| viewport | surface | status | console | failed | responses | broken_images | overflow |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mobile | homepage | 200 | 2 | 19 | 1 | 0 | False |
| desktop | homepage | 200 | 2 | 12 | 1 | 0 | False |
| mobile | collection_best_sellers | 200 | 2 | 12 | 1 | 0 | False |
| desktop | collection_best_sellers | 200 | 2 | 12 | 1 | 0 | False |
| mobile | collection_dresses | 200 | 2 | 12 | 1 | 0 | False |
| desktop | collection_dresses | 200 | 2 | 12 | 1 | 0 | False |
| mobile | product_primary | 200 | 2 | 17 | 1 | 0 | False |
| desktop | product_primary | 200 | 2 | 17 | 1 | 0 | False |
| mobile | blog_index | 200 | 2 | 11 | 1 | 0 | False |
| desktop | blog_index | 200 | 2 | 11 | 1 | 0 | False |
| mobile | article | 200 | 2 | 11 | 1 | 0 | False |
| desktop | article | 200 | 2 | 11 | 1 | 0 | False |
| mobile | page_contact | 200 | 2 | 11 | 1 | 0 | False |
| desktop | page_contact | 200 | 2 | 11 | 1 | 0 | False |
| mobile | list_collections | 200 | 2 | 11 | 1 | 0 | False |
| desktop | list_collections | 200 | 2 | 11 | 1 | 0 | False |
| mobile | cart | 200 | 2 | 12 | 1 | 0 | False |
| desktop | cart | 200 | 2 | 13 | 1 | 0 | False |
| mobile | search | 200 | 2 | 16 | 1 | 0 | False |
| desktop | search | 200 | 2 | 16 | 1 | 0 | False |
| mobile | customer_login | 403 | 14 | 0 | 2 | 0 | False |
| desktop | customer_login | 403 | 10 | 0 | 2 | 0 | False |
| mobile | 404 | 404 | 3 | 11 | 2 | 0 | False |
| desktop | 404 | 404 | 3 | 11 | 2 | 0 | False |

All representative theme-controlled pages rendered with zero broken visible images and no horizontal overflow in both 390x844 mobile and 1440x1000 desktop captures. Customer login redirected to `account.dresslikemommy.com` and is not theme-controlled. The 404 route returned HTTP 404 as expected while still rendering the storefront shell.

## Common Browser Baseline Noise

- Repeated console error: `shop.app/pay/hop` frame blocked by CSP / 403, associated with Shop Pay accelerated checkout frame behavior.
- Repeated aborted analytics/network requests from TikTok, Bing, Google Analytics/Ads, Merchant Center analytics, Shopify monorail, and internal collect endpoints.
- Customer-account route produced hosted account-domain Cloudflare/auth policy console messages, outside the theme surface.

## Artifacts

- `url-inventory.csv` / `url-inventory.json`: full localized route inventory
- `psi/ui/`: official pagespeed.web.dev screenshots and extracted text for representative routes
- `lighthouse/raw/`: local Lighthouse JSON/HTML reports for representative routes
- `browser/screenshots/`: before-change browser screenshots
- `browser/console/` and `browser/network/`: console and network evidence per route/viewport
- `browser/browser-baseline-summary.json`: visual/browser QA machine-readable summary

## Next Step

Begin remediation from the highest-risk shared surfaces: homepage/image delivery, PDP CLS/media behavior, global render-blocking requests, and third-party/app payload. Before any code change, keep this directory immutable as the before baseline; after each fix, rerun the exact same representative captures and compare.
