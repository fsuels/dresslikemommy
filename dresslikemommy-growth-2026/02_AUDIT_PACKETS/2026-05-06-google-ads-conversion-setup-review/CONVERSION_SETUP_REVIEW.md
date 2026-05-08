# Google Ads / Shopify Conversion Setup Review

Generated: 2026-05-06

## Decision

`GOOGLE_ADS_REPORTING_CLEANUP_COMPLETED__PURCHASE_PRIMARY_DYNAMIC_LEFT_UNCHANGED__MICRO_VALUES_NOW_NO_VALUE`

## Correct Setup

- Use the Shopify Google & YouTube app / app pixel as the Google measurement path.
- Do not paste Google Ads purchase snippets into `theme.liquid`, checkout, GTM, or a Shopify custom pixel while the Google & YouTube app owns purchase tracking.
- In Google Ads, `Google Shopping App Purchase` should be the only primary account-level purchase action used for bidding.
- Purchase should use transaction-specific / dynamic value, currency, order ID / dedupe key, and enhanced conversions.
- Add to cart, begin checkout, view item, page view, search, and add payment info should stay secondary / observe-only unless a later explicit measurement workstream intentionally uses a custom goal.
- Do not treat `All conv. value` as ROAS when it is coming from secondary funnel events instead of primary purchase conversions.

## Current Evidence Checked In This Pass

- Theme files `layout/theme.liquid`, `sections/main-product.liquid`, `snippets/cart-drawer.liquid`, `snippets/meta-tags.liquid`, and `assets/analytics.js` have no current local diff.
- Theme source initializes `window.dataLayer` and loads local `assets/analytics.js`; it does not hardcode `gtag`, `AW-853411529`, `G-N4EQNK0MMB`, `googleadservices`, `send_to`, or a purchase conversion snippet.
- Live storefront HTML currently includes Shopify Web Pixels Manager with an app pixel for Google tags:
  - Google tag IDs: `G-N4EQNK0MMB`, `AW-853411529`, `GT-WRH8Q3MD`
  - Target country: `US`
  - Purchase destination label: `AW-853411529/UbkpCN-fhogBEMmN-JYD`
  - Other funnel labels: `page_view`, `view_item`, `search`, `add_to_cart`, `begin_checkout`, `add_payment_info`
  - Data sharing state: `optimized`
- Prior logged-in Shopify Customer Events evidence showed Google & YouTube app pixel as `Connected` / `Optimized`.
- Prior logged-in Google Ads conversion readback showed:
  - `Google Shopping App Purchase`: Website, Purchases / Primary action, included in account-level goals, value setting `Use different values. If there's no value, use 0.`, enhanced conversions enabled.
  - Legacy/parallel purchase actions remained Secondary and excluded from account-level goals.
- Prior paid-order capture proved a real Shopify paid order reached Google Ads purchase tracking with:
  - order `#9476`
  - Shopify order id / dedupe key `6575644803169`
  - value `19.99`
  - currency `USD`
  - Google Ads conversion id `853411529`
  - label `UbkpCN-fhogBEMmN-JYD`
  - enhanced conversion hash present

## Fresh Google Ads UI Readback Before Cleanup

Read-only UI readback was completed on 2026-05-06 through the logged-in Atlas/Playwright browser for Google Ads account `dresslikemommy.com`, before the owner-approved reporting cleanup.

Date range shown in Google Ads: `Last 7 days`, `Apr 29 - May 5, 2026`.

Conversion action table:

| Goal/category | Conversion action | Source | Tracking status | Action optimization | Included in account-level goals | All conv. | All conv. value |
|---|---:|---|---|---|---|---:|---:|
| Purchases | Google Shopping App Purchase | Website | No recent conversions | Primary | Yes | 0.00 | 0.00 |
| Purchases | Purchases from google Adwords | Website | Needs attention | Secondary | No | 0.00 | 0.00 |
| Purchases | Purchases from google analytics data | Website (Google Analytics UA) | No recent conversions | Secondary | No | 0.00 | 0.00 |
| Purchases | dresslikemommy.com - GA4 (web) purchase | Website (Google Analytics GA4) | No recent conversions | Secondary | No | 0.00 | 0.00 |
| Add to cart | Google Shopping App Add To Cart | Website | Needs attention | Secondary | No | 11.00 | 298.89 |
| Add to cart | dresslikemommy.com - GA4 (web) add_to_cart | Website (Google Analytics GA4) | Active | Secondary | No | 11.00 | 298.89 |
| Add to cart | Add To Cart button click from adwords | Website | Needs attention | Secondary | No | 0.00 | 0.00 |
| Begin checkout | Google Shopping App Begin Checkout | Website | Active | Secondary | No | 1.00 | 80.97 |
| Begin checkout | dresslikemommy.com - GA4 (web) begin_checkout | Website (Google Analytics GA4) | Active | Secondary | No | 1.00 | 80.97 |
| Begin checkout | Begin Checkout from adwords | Website | Needs attention | Secondary | No | 0.00 | 0.00 |
| Page views | Google Shopping App Page View | Website | Needs attention | Secondary | No | 292.00 | 0.00 |
| Page views | Google Shopping App View Item | Website | Needs attention | Secondary | No | 175.00 | 0.00 |
| Other | Search button from website that came adwords | Website | Needs attention | Secondary | No | 0.00 | 0.00 |
| Other | Payment Info visit from adwords | Website | Needs attention | Secondary | No | 0.00 | 0.00 |
| Other | Google Shopping App Add Payment Info | Website | No recent conversions | Secondary | No | 0.00 | 0.00 |

Removed historical actions were visible for `Purchase` and `Add to cart`. They still show Primary/Yes in the removed row metadata, but they are removed and reported `0.00` conversions/value in this date range.

Detail-page readbacks:

- `Google Shopping App Purchase`: `Purchases, Primary action`; value `Use different values. If there's no value, use 0.`; source `Website`; count `Every conversion`; click-through window `90 days`; attribution `Data-driven`; enhanced conversions `Managed through Google Tag. Enhanced conversions is enabled.`
- `Google Shopping App Add To Cart`: `Add to cart, Secondary action`; value `Use different values. If there's no value, use $0.`; source `Website`; count `Every conversion`.
- `Google Shopping App Begin Checkout`: `Begin checkout, Secondary action`; value `Use different values. If there's no value, use $0.`; source `Website`; count `Every conversion`; enhanced conversions enabled.
- `Google Shopping App Page View`: `Page views, Secondary action`; value `Use different values. If there's no value, use 0.`; source `Website`; count `Every conversion`.
- `Google Shopping App View Item`: `Page views, Secondary action`; value `Use different values. If there's no value, use $0.`; source `Website`; count `Every conversion`.

Conclusion:

- Purchase tracking is configured correctly for bidding/reporting: one live primary account-level purchase action, dynamic value, enhanced conversions enabled.
- `Conversions` and `Conv. value` are correctly `0.00` for the last 7 days because there were no attributed primary purchase conversions in the selected range.
- `All conv. value` is not purchase revenue. It is coming from secondary add-to-cart and begin-checkout actions.
- The secondary micro values are duplicated in `All conv. value` because both Google Shopping App actions and GA4 imported actions are present for add-to-cart / begin-checkout. This does not affect primary `Conversions` as long as these remain Secondary and excluded from account-level goals, but it makes `All conv. value`, `All conv. value / cost`, and related All-conversion ratios unsuitable as ROAS.

## Campaign Segmentation Readback

Campaigns table was segmented by `Conversions -> Conversion action` for the same `Apr 29 - May 5, 2026` range.

Account visible totals:

- Cost: `$19.88`
- Primary conversions: `0.00`
- Primary conversion value: `0.00`
- All conv. value / cost: `38.22`
- All conv. value: `759.72`

Segment result for campaigns with spend/value:

| Campaign | Cost | Primary conv. value | All conv. value / cost | All conv. value source |
|---|---:|---:|---:|---|
| `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` | `$1.30` | `0.00` | `203.00` | `Google Shopping App Add To Cart` `131.95` + GA4 add_to_cart `131.95` |
| `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` | `$18.58` | `0.00` | `26.69` | Google Shopping App add-to-cart `166.94`, Google Shopping App begin-checkout `80.97`, GA4 add_to_cart `166.94`, GA4 begin_checkout `80.97` |

Therefore the visible `38.22 All conv. value / cost` is exactly the misleading metric the owner was worried about. It is secondary funnel/cart value divided by ad cost, not purchase ROAS.

## Owner-Approved Reporting Cleanup

Approval received:

`APPROVE GOOGLE ADS REPORTING CLEANUP: LEAVE PURCHASE PRIMARY/DYNAMIC; SET NON-PURCHASE MICRO-CONVERSION VALUES TO $0/NO VALUE; REMOVE OR ZERO DUPLICATE GA4 ADD_TO_CART AND BEGIN_CHECKOUT IMPORTS IN GOOGLE ADS ONLY; NO PURCHASE TAG, PRODUCT SCOPE, OR CAMPAIGN ENABLE/PAUSE CHANGES.`

Live changes made in Google Ads only:

| Conversion action | Source | Post-cleanup action optimization | Post-cleanup value readback |
|---|---|---|---|
| `Google Shopping App Add To Cart` | Website | Add to cart, Secondary action | `Don't use a value` |
| `Google Shopping App Begin Checkout` | Website | Begin checkout, Secondary action | `Don't use a value` |
| `Google Shopping App Page View` | Website | Page views, Secondary action | `Don't use a value` |
| `Google Shopping App View Item` | Website | Page views, Secondary action | `Don't use a value` |
| `Google Shopping App Add Payment Info` | Website | Other, Secondary action | `Don't use a value` |
| `dresslikemommy.com - GA4 (web) add_to_cart` | Google Analytics (GA4) | Add to cart, Secondary action | `Don't use a value` |
| `dresslikemommy.com - GA4 (web) begin_checkout` | Google Analytics (GA4) | Begin checkout, Secondary action | `Don't use a value` |

Purchase readback after cleanup:

- `Google Shopping App Purchase`: `Purchases, Primary action`; value `Use different values. If there's no value, use 0.`; source `Website`; count `Every conversion`; click-through window `90 days`; attribution `Data-driven`; enhanced conversions `Managed through Google Tag. Enhanced conversions is enabled.`
- Conversion-action table still shows `Google Shopping App Purchase` as `Primary` and `Included in account-level goals = Yes`.

No live edits were made to:

- `Google Shopping App Purchase`
- Shopify theme, Shopify tags, Shopify Customer Events, Google & YouTube app, GA4 property, GTM, Merchant Center, product scope, feeds, product groups, campaign enable/pause state, campaign budgets, bid strategies, PMax, Remarketing, Brand Search assets, or campaign conversion goals.

Important reporting note:

- The selected historical date range (`Apr 29 - May 5, 2026`) can still show previously recorded `All conv. value` for add-to-cart and begin-checkout rows. The value-setting cleanup is not expected to retroactively rewrite historical All-conversion value already recorded before the change.
- Going forward, these micro actions should stop adding monetary value to `All conv. value`, while purchase revenue should continue to come only from the primary dynamic purchase action.

## Separate Campaign-Governance Observation

This was outside the conversion-action setup question, but the live campaigns table no longer matches the last stored 2026-05-01 paid-media memory for Brand Search:

- `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` currently shows `$2.00/day` and `Maximize conversions`.
- The stored continuity file expected Brand Search not above `$5.00/day` and previously documented `Maximize clicks`.
- The same table shows Standard Shopping still at `$20.00/day`, `Manual CPC`, `$18.58` cost in the selected range, `81` clicks, `0.00` primary conversions, and `0.00` primary conversion value.

No campaign, budget, bidding, status, or conversion-goal changes were made in this pass.

## Required Live Recheck

Next live checks:

1. Monitor the next 24-72 hours of Google Ads reporting to confirm new micro-conversions no longer add monetary `All conv. value`; historical `Apr 29 - May 5, 2026` values are not retroactive.
2. Confirm each active campaign uses account-default purchase goals unless there is an explicitly approved custom-goal reason.
3. Run the overdue Standard Shopping 48-hour review/owner decision flow documented in `ops/GOOGLE_ADS_CONTINUITY.md`.
4. Review the unexpected Brand Search posture change against the owner-approved plan before making any edits.

## Sources

- Google Ads Help: Set up conversion tracking with the Google & YouTube app on Shopify.
- Google Merchant Center Help: Understand the conversion actions tracked in Google Ads.
- Google Ads Help: About primary and secondary conversion actions.
- Google Ads Help: About All conversions.
- Google Ads Help: Track transaction-specific conversion values.
- Shopify Help Center: Migrating pixels.
