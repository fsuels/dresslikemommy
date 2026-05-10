# Economics Reporting Next Control

Date: 2026-05-08
Lane: Worker 4 economics/reporting controls
Decision: `LOCAL_READY_NO_EXTERNAL_WRITES`

## Scope

This is a compact operator pack for the next safe paid-growth step. It is local artifact work only.

No Google Ads, Pinterest, Merchant Center, Shopify Admin, feed, catalog, campaign, import, preview, enablement, budget, bid, status, product-scope, feed-label, product-group, conversion-goal, tag, CAPI, theme, checkout payment, or live-spend action was taken.

Write scope stayed inside:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/economics-reporting/`

## Inputs Used

- `ops/GROWTH_NORTH_STAR.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `2026-05-08-paid-growth-safe-followup/lanes/economics-creative/ECONOMICS_AND_CREATIVE_SAFE_GROWTH_PACK.md`
- `2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/economics-reporting/ECONOMICS_REPORTING_OPERATOR_PACK.md`
- `2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/GOOGLE_ADS_INTL_URL_HOLD_VALIDATION.md`
- `2026-05-08-paid-growth-url-hold-checkout-safe-advance/PAID_GROWTH_URL_HOLD_CHECKOUT_SAFE_ADVANCE_REPORT.md`

## 650% ROAS Math

Formula:

`max CPA = AOV / target ROAS`

| Planning Input | Value |
|---|---:|
| AOV | `$70.00` |
| Target ROAS | `650%` / `6.5x` |
| Max CPA at target ROAS | `$10.77` |
| 50% non-marketing cost model | `$35.00` |
| Contribution after target CPA, before returns/chargebacks/reships | `$24.23` |

Operating interpretation:

- `$10.77` is the clean-evidence CPA ceiling only when purchase value, final URL country, query quality, catalog health, checkout, and tracking are current.
- `$9.49-$9.73` is the conservative decision band for weaker international lanes, mixed-language surfaces, stale catalog evidence, tracking uncertainty, or early tests.
- `$16.00` spend with `0` purchases is the hard zero-purchase stop for the smallest visible unit.
- Do not scale from CTR, add-to-cart, checkout starts, saves, outbound clicks, impressions, or cheap CPC alone.

## CPA/CPC Thresholds By CVR Scenario

At `$70.00` AOV and `650%` ROAS, target CPA is `$10.77`. The max CPC a traffic source can tolerate is:

`max CPC = target CPA x purchase CVR`

| Purchase CVR | Max CPC To Hold `$10.77` CPA | Operator Read |
|---:|---:|---|
| `0.50%` | `$0.05` | Only ultra-low CPC discovery can work; pause quickly if intent is weak. |
| `0.75%` | `$0.08` | Lower-CPC discovery ceiling after checkout/readiness gates. |
| `1.00%` | `$0.11` | Reasonable for tightly matched exact/phrase tests. |
| `1.25%` | `$0.13` | Good operating lane for watchlist and broader EU tests. |
| `1.39%` | `$0.15` | Current held Search packet cap; needs high-intent traffic. |
| `1.50%` | `$0.16` | Clean exact/phrase threshold; still do not broaden blindly. |
| `2.00%` | `$0.22` | Allows the owner-preferred upper band only after proof. |
| `2.50%` | `$0.27` | Strong buyer intent; still scale gradually only after purchase value proves out. |

Required purchase CVR by CPC:

| CPC | Required CVR For `$10.77` CPA | Clicks Per Target CPA | Use Case |
|---:|---:|---:|---|
| `$0.04` | `0.37%` | `269` | Current low-bid Shopping math; depends on clean product/query quality. |
| `$0.08` | `0.74%` | `135` | Lower-CPC discovery tests after readiness gates. |
| `$0.10` | `0.93%` | `108` | Strong cold-test cap. |
| `$0.12` | `1.11%` | `90` | Watchlist and broader EU paused tests. |
| `$0.15` | `1.39%` | `72` | Current held non-US Search packet cap. |
| `$0.20` | `1.86%` | `54` | Upper edge; only after CVR proof. |
| `$0.25` | `2.32%` | `43` | Too expensive for unproven cold traffic. |

## Zero-Purchase Kill Rules

Use the smallest meaningful unit: country, campaign, ad group, product/theme, product group, Pinterest ad group, or search-term cluster.

| Spend / Evidence | Rule |
|---|---|
| About `$5` spend, weak terms, irrelevant products, or no qualified engagement | Pause or narrow the smallest unit; add negatives only inside an approved workflow. |
| `$9.49-$9.73` spend, `0` purchases, weaker international evidence | Pause, narrow, or require owner decision. |
| `$10.77` spend, `0` purchases, clean evidence lane | Pause, narrow, or require owner decision. |
| `$16.00` spend, `0` purchases | Hard pause the unit. |
| `2` purchases but CPA above `$10.77` or ROAS below `650%` | Hold, reduce, or narrow; do not scale. |
| `3+` purchases with CPA at or below `$10.77`, clean value, and clean terms | Eligible for cautious scale review. |

Scale only after primary purchase value, currency, transaction IDs, country final URL, and search/product quality are clean. Budget increases should stay `10%-20%` for borderline winners or `20%-30%` for clean winners, no more often than every `3-7` days.

## First 72-Hour Review Cadence

These controls apply only after future explicit activation approval. They do not authorize activation.

| Window | Required Review | Decision Control |
|---|---|---|
| Preflight | Confirm exact approval, final URLs, country parameter, purchase conversion/value, Merchant/Pinterest status, checkout/currency, and no blocked themes. | Keep paused if any required readback is stale or missing. |
| 0-12 hours | Check spend, CPC, impressions, early search terms, destination country/currency, and disapproved/limited policy status. | Stop only obvious wrong-country, wrong-theme, or policy/destination failures. |
| 12-24 hours | Review terms/products, CPC, CTR only as a diagnostic, and qualified engagement. | Around `$5` with weak terms or no qualified engagement: pause or narrow. |
| 24-48 hours | Review purchases, CPA, ROAS, AOV, search terms, checkout evidence, and catalog status. | At `$9.49-$10.77` with `0` purchases: pause, narrow, or owner decision. |
| 48-72 hours | Review purchase value, CPA, ROAS, country split, product/theme split, and return-risk notes. | At `$16` with `0` purchases: hard pause. Scale only with `3+` clean purchases. |

Weekly reporting must split by platform, country, campaign, theme/ad group, product/product group, currency, spend, clicks, CPC, purchase CVR, CPA, AOV, conversion value, ROAS, query/product evidence, tracking freshness, catalog status, action, action reason, owner approval reference, and next review date.

## Market Sequencing From Current Readiness

Live-spend-ready markets remain `0`. Sequencing below is for paused infrastructure and future separately approved spend tests only.

| Sequence | Markets | Current Readiness | Next Safe Action |
|---|---|---|---|
| Governed baseline | `US` | Existing paused US nonbrand Search campaign `23827590655`; Standard Shopping live/eligible under strict separate guardrails. | Do not duplicate US. Do not change Standard Shopping. Use only for reporting template and future separate approval decisions. |
| First paused non-US build candidates | `GB`, `CA`, `AU` | English-first, checkout/currency/shipping UI evidence exists for paused infrastructure; live spend still blocked. | If owner approves paused Search build, include in held packet; activation later only one or very few markets at a time. |
| Localized paused candidates | `ES`, `IT`, `RO`, `PT` | Country-qualified localized URLs and checkout/currency evidence exist; RO requires RON normalization. | Use country-qualified localized URLs only. Do not use bare language paths. Keep live spend blocked until catalog/tracking/economics readbacks. |
| High-value watchlist | `CH`, `DK` | Product-landing-only / paused shell candidate; local language and checkout QA incomplete. | Paused English shells only; no spend until checkout, duties/returns clarity, catalog, and tracking pass. |
| Broader ecommerce QA | `DE`, `NL`, `SE`, `FR`, `BE` | Product-landing-only / paused shell candidate; native-language QA incomplete. | Paused English shells only; local-language copy held until QA. |
| Lower-CPC discovery QA | `PL`, `CZ`, `GR` | Product-landing-only / paused shell candidate; checkout/language QA incomplete. | Paused discovery shells only at lower CPC guardrails after approval; live spend remains blocked. |
| Hold / extra QA | Arabic, Hebrew, Japanese, Korean, mixed-language markets | Not in current held Search build and not spend-ready. | Do not prepare spend-facing copy until landing language, checkout, catalog, and tracking QA pass. |

If the owner approves a paused non-US Search preview/import before the beach metadata repair, use the held `1496`-row CSV that excludes `Vacation Family`. Do not use the original `1666`-row packet for upload/import while `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` remains open.

## Guardrails To Preserve

- Local artifact only; no external writes.
- No live spend, campaign enablement, campaign import, or Ads preview from this lane.
- No PMax, Standard Shopping, Remarketing, product-scope, feed-label, product-group, conversion-goal, Merchant, Shopify product-data, Pinterest, theme, budget-increase, bid-increase, or status changes.
- Do not imply physical store, warehouse, store pickup, local stock, stocked inventory, nearby inventory, or guaranteed on-hand stock.
- Do not claim fast shipping, delivery timing, bestseller status, review counts, ratings, promotions, discounts, free gifts, guaranteed fit, guaranteed availability, or no-risk returns.
- Do not call outbound shipping rates "returns"; return shipping remains customer-paid unless separately proven otherwise.

## Next Best Action

The safest next parent action is still approval-gated: either request the exact paused non-US Google Search `TEST BUILD` approval using the held `1496`-row Vacation Family-excluded CSV, or repair the blocked beach metadata in Shopify after exact owner approval and public readback. No market is ready for live spend yet.
