# Economics / Market Priority Controls

Date: 2026-05-09

Lane: `economics-market-priority`

Decision: `LOCAL_READY__NO_LIVE_SPEND_READY__NEXT_QA_ORDER_DEFINED`

Parent integration note: after this economics lane was written, the sibling checkout lane completed CH and DK no-payment checkout-to-shipping QA successfully. CH and DK therefore moved from checkout-pending to checkout/rate-evidence approval-gated for paused infrastructure only. Live-spend-ready remains `0`. Remaining checkout-pending markets are `DE`, `NL`, `FR`, `BE`, `SE`, `PL`, `CZ`, and `GR`.

## Scope

This packet is local/read-only control work for the next safe paid-growth step. It uses existing repo evidence only.

No Google Ads, Merchant Center, Pinterest, Shopify Admin, live product, theme, credential, checkout, campaign, catalog, feed, budget, bid, status, conversion-goal, product-scope, product-group, feed-label, import, preview, upload, sync, enablement, payment, or order action was taken.

Write scope stayed inside:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-checkout-expansion-safe-advance/lanes/economics-market-priority/`

## Evidence Used

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/PAID_GROWTH_MARKET_READINESS_SAFE_ADVANCE_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/market-readiness/INTERNATIONAL_MARKET_READINESS_SCORECARD.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/market-readiness/market_readiness.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/ads-held-csv/held_ads_validation.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/economics-reporting/ECONOMICS_REPORTING_NEXT_CONTROL.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/gb-ca-checkout-ui/GB_CA_CHECKOUT_UI_READBACK.md`

## What Live-Spend-Ready Means

Live-spend-ready still means `0` markets.

Current tiering from existing evidence:

| Tier | Markets | Meaning |
|---|---|---|
| Checkout/rate evidence, approval-gated | `GB`, `CA`, `AU`, `ES`, `IT`, `RO`, `PT` | Enough evidence for paused infrastructure only. Still blocked from live spend by exact owner approval, tracking/catalog/readback gates, the beach URL hold where relevant, and just-in-time checkout/currency confirmation. |
| Checkout-pending | `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `PL`, `CZ`, `GR` | Product landing evidence exists, but no fresh checkout-to-shipping clearance for spend discussion. Use only as local or paused-shell candidates until no-payment checkout QA passes. |
| Live-spend-ready | none | No non-US market has all readiness, tracking/catalog, landing URL, economics, and exact approval gates cleared. |

For clarity: "paused-shell-ready" is not "live-spend-ready." A paused import/build can be useful infrastructure, but it must not be treated as permission to activate spend.

## Next-Market QA Order After CH/DK

Immediate pair:

1. `CH` - Switzerland: high-value watchlist, CHF presentment passed product-page readback after the broad detector was proven false-positive on visual readback; still needs one isolated-browser no-payment checkout-to-shipping run.
2. `DK` - Denmark: high-value watchlist, DKK product landing evidence exists; no checkout/rate proof yet.

Recommended order after `CH` and `DK`:

| Order | Market | Why This Position | Required Readback Before Spend Discussion |
|---:|---|---|---|
| 3 | `DE` - Germany | Largest remaining ecommerce market in the checkout-pending group; strong strategic value if checkout, language, and policy quality pass. | Country-qualified product/cart/checkout-to-shipping, EUR presentment, German landing/policy review, no visible 429/CAPTCHA, no payment/order. |
| 4 | `NL` - Netherlands | Prior packets mention earlier no-payment rate evidence, but it was not refreshed in the latest scorecard; efficient next refresh candidate. | Fresh country-qualified checkout/rate proof, EUR presentment, Dutch language-quality decision, no payment/order. |
| 5 | `FR` - France | Large ecommerce market and useful before BE because BE has French/Dutch split complexity. | Country-qualified checkout/rate proof, EUR presentment, French landing/policy review, no payment/order. |
| 6 | `BE` - Belgium | Valuable but more complex because language handling may need French/Dutch decisioning. | Checkout/rate proof, EUR presentment, FR/NL language split decision, no payment/order. |
| 7 | `SE` - Sweden | Good ecommerce market, but SEK reporting/language QA remains unresolved. | Checkout/rate proof, SEK presentment, Swedish language/reporting review, no payment/order. |
| 8 | `PL` - Poland | Lower-CPC discovery candidate after higher-value checkout-pending markets. | Checkout/rate proof, PLN presentment, Polish landing/policy review, no payment/order. |
| 9 | `CZ` - Czechia | Lower-CPC discovery candidate; keep CPC conservative until local QA passes. | Checkout/rate proof, CZK presentment, Czech landing/policy review, no payment/order. |
| 10 | `GR` - Greece | Lower-CPC discovery candidate with EUR simplicity but Greek language QA still unresolved. | Checkout/rate proof, EUR presentment, Greek landing/policy review, no payment/order. |

Operational rule: run one market at a time, low-volume, isolated browser or equivalent public storefront readback only, and stop the QA lane on visible `429`, CAPTCHA, verification wall, checkout breakage, currency mismatch, or missing shipping rates. Do not submit payment, do not create an order, and do not use checkout QA as live-spend approval.

## 650% ROAS Economics

Planning assumptions:

| Input | Value |
|---|---:|
| AOV | `$70.00` |
| Target ROAS | `650%` / `6.5x` |
| Max CPA at target ROAS | `$10.77` |

Formula:

`max CPA = AOV / target ROAS = 70 / 6.5 = 10.7692`

Required purchase CVR by CPC:

| CPC | Required Purchase CVR For `$10.77` CPA | Clicks Per Target CPA | Operator Use |
|---:|---:|---:|---|
| `$0.10` | `0.93%` | `108` | Conservative lower-CPC discovery and markets with incomplete local proof. |
| `$0.12` | `1.11%` | `90` | Watchlist and broader EU tests after checkout QA passes. |
| `$0.15` | `1.39%` | `72` | Current held Search packet upper common cap; needs high-intent exact/phrase traffic. |
| `$0.20` | `1.86%` | `54` | Absolute upper edge from owner-approved guardrails; do not use for unproven cold traffic without clean proof. |

Spend and click equivalents:

| Spend Threshold | At `$0.10` CPC | At `$0.12` CPC | At `$0.15` CPC | At `$0.20` CPC | Rule |
|---:|---:|---:|---:|---:|---|
| `$5.00` | `50` clicks | `42` clicks | `33` clicks | `25` clicks | Early hygiene check: wrong terms, wrong product/theme, wrong country, weak engagement, or policy/destination issue means pause/narrow the smallest approved unit. |
| `$10.77` | `108` clicks | `90` clicks | `72` clicks | `54` clicks | Target CPA ceiling: with `0` purchases, pause/narrow or require owner decision. |
| `$16.00` | `160` clicks | `133` clicks | `107` clicks | `80` clicks | Hard zero-purchase stop for the smallest visible unit. |

Kill/hold/scale controls:

| Evidence | Control |
|---|---|
| `0` purchases at about `$5` and search terms/products are weak | Pause or narrow the smallest approved unit. Do not wait for more spend. |
| `0` purchases at `$9.49-$10.77` in a weaker or mixed-evidence market | Pause, narrow, or require owner decision. |
| `0` purchases at `$10.77` in a clean evidence lane | Pause, narrow, or require owner decision. |
| `0` purchases at `$16.00` | Hard pause the smallest visible unit. |
| `1` purchase above `$10.77` CPA | Hold for more evidence only if terms, product, currency, and tracking are clean; otherwise narrow. |
| `2` purchases but CPA above `$10.77` or ROAS below `650%` | Do not scale; hold, reduce, or narrow. |
| `3+` purchases at or below `$10.77` CPA with clean value and search/product evidence | Eligible for cautious scale review only. |

Scale rule: budget increases should be gradual and evidence-led. Borderline winners should stay in a `10%-20%` review band; clean winners can be reviewed in a `20%-30%` band no more often than every `3-7` days. Do not scale on CTR, saves, add-to-cart, checkout starts, cheap CPC, or impressions alone.

## Reporting Checklist For Any Future Approved Paused Import / Readback

Use this checklist only after exact owner approval for a paused import/build. It does not authorize live spend.

Pre-import / preview:

- Exact owner approval text is present and matches the intended surface.
- Source file is the held `1496`-row Vacation Family-excluded CSV if the beach metadata blocker is still open.
- All rows are `Action=Add`; all campaign, ad group, keyword, and ad statuses are `Paused`.
- No rows touch US campaign `23827590655`.
- No PMax, Standard Shopping, product-scope, feed-label, product-group, conversion-goal, Merchant, Pinterest, Shopify product-data, theme, budget-increase, bid-increase, or enablement rows exist.
- CPC values are at or below the approved cap; current held values are `$0.10`, `$0.12`, and `$0.15`.
- Final URLs retain country parameters; ES/IT/RO/PT must use country-qualified localized URLs, never bare language paths.
- Vacation Family / product `7227378892897` / stale beach handle remains excluded unless the metadata repair has exact owner approval and public readback.

Post-preview / post-build readback, still paused:

- Count campaigns, ad groups, keywords, negatives, ads, budgets, CPCs, and statuses.
- Verify every campaign, ad group, ad, and keyword is paused.
- Verify locations are presence-only for the intended country.
- Verify no US campaign duplication and no accidental Standard Shopping/PMax/Remarketing changes.
- Verify no conversion-goal, product-scope, feed-label, product-group, Merchant, Pinterest, Shopify product, or theme changes occurred.
- Verify disapproval/limited policy status, destination status, and final URL/country behavior before any activation discussion.
- Save a dated readback packet with CSV preview/export, screenshots or structured readbacks, and a summary JSON.

If later activation is separately approved:

- Run just-in-time market checkout/currency readback.
- Confirm purchase conversion, value, transaction ID, currency, and country reporting are trusted.
- Confirm catalog/feed/event gates relevant to the platform are not stale.
- Start with the smallest approved country/campaign/ad group/theme unit.
- Apply `$5`, `$10.77`, and `$16` review stops by smallest meaningful unit.
- Report spend, clicks, CPC, purchases, CPA, AOV, conversion value, ROAS, purchase CVR, country, currency, final URL, search terms/products, tracking freshness, catalog status, action, action reason, approval reference, and next review date.

## Claim-Safe Copy Constraints

Keep paid-growth copy factual and conservative:

- Do not imply a physical store, warehouse, local pickup, local stock, stocked inventory, owned inventory, or guaranteed on-hand availability.
- Do not claim fast shipping, guaranteed delivery timing, bestseller status, review counts, ratings, promotions, discounts, free gifts, guaranteed fit, guaranteed availability, or risk-free returns unless separately verified in current evidence.
- Do not call outbound shipping rates "returns"; return shipping remains customer-paid unless separate proof says otherwise.

## Bottom Line

Next safe market QA path: `CH`, `DK`, then `DE`, `NL`, `FR`, `BE`, `SE`, `PL`, `CZ`, `GR`.

Next safe growth-infrastructure path remains approval-gated: use the held `1496`-row non-US Search CSV only for a future exact-owner-approved paused preview/import, with all entities paused and no live spend.

Live-spend-ready remains `0`.
