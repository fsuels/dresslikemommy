# Measurement Controlled Readback

Date: 2026-05-08
Mode: parent local/read-only synthesis only

## Decision

`MEASUREMENT_PARTIALLY_TRUSTED_FOR_LOCAL_GUARDRAILS__LIVE_ENABLEMENT_STILL_REQUIRES_JUST_IN_TIME_READBACKS`

Purchase tracking is strong enough to keep building local paused infrastructure and economics guardrails. It is not enough to approve spend by itself.

## Trusted Evidence

- Google paid-value gate passed on real paid Shopify order `#9476`, Shopify order id `6575644803169`, value `19.99`, currency `USD`.
- Google Ads purchase endpoint proof carried `AW-853411529/UbkpCN-fhogBEMmN-JYD`, the same order id as dedupe key, and enhanced-conversion hash presence.
- GA4 / Google measurement proof carried `event=purchase`, value `19.99`, currency `USD`, and transaction id `6575644803169`.
- Google Ads reporting cleanup was completed on 2026-05-06:
  - `Google Shopping App Purchase` remained `Purchases / Primary action`.
  - Purchase value remained dynamic / transaction-specific.
  - Non-purchase Google Shopping App micro-conversion values were changed to `Don't use a value`.
  - Duplicate GA4 `add_to_cart` and `begin_checkout` imports were zeroed in Google Ads only.

## Reporting Rules For This Sprint

| Surface | Use | Avoid |
|---|---|---|
| Google Ads | Primary purchase `Conversions`, `Conversion value`, `Conv. value / cost`, segmented by conversion action when needed | Historical `All conv. value / cost` from periods before micro-value cleanup |
| Merchant | Paid-cohort source timestamp, issue count, item IDs, labels, eligibility | `Missing local inventory data` as a product-data fix target |
| Pinterest | Event Quality, event-source freshness, Tag/CAPI activity, catalog source status, item-level product proof | Draft/spend decisions from Event Quality alone |
| Storefront | Country-qualified final URL behavior, currency, language, no-payment shipping-step proof | Bare language-path final URLs for ES/IT/RO/PT |

## Current Gaps

- No fresh Google Ads account UI readback was run in this parent lane. Before any budget/status/import/enable action, read back active campaign cost, primary purchase value, search terms, and conversion-goal state.
- Merchant paid-cohort `Missing age group` remains unresolved in latest evidence. Prior exact count is `623` unique paid-cohort US/en item IDs; the latest exact CSV did not materialize before the prior lane stopped.
- Pinterest Event Quality remains `Fair` in latest stored evidence and needs a fresh account readback before any draft/spend decision.
- Pinterest catalog proof remains limited to `337/346` historical US candidate rows resolved as EN-US in-stock; the `9` unresolved rows should be excluded or re-resolved before any approved product-group build.

## Guardrail Implications

- Local paused Search packets can be prepared and validated now.
- Any Google Ads import/create, even paused, remains approval-gated.
- Any live spend or enablement remains blocked until measurement, Merchant/Pinterest catalog, landing-page, and economics readbacks are all current.
- Do not add duplicate Google or Pinterest tags to compensate for dashboard lag; official app paths own measurement.

## Just-In-Time Readback Checklist

Before approving or applying any spend-related action:

1. Google Ads: campaign status, daily budget, bid strategy/CPC cap, networks, presence-only location, conversion goals, primary purchases, primary purchase value, search terms, cost, and CPC.
2. Merchant: paid-cohort age_group issue count, source timestamp for sample `shopify_US_7227254276193_41871113158753`, and label/product-scope integrity.
3. Pinterest: advertiser `549756244483`, Event Quality updated date, Tag/CAPI timestamps, catalog source status, item-level product proof, and `0 campaigns` / `$0.00 spend` baseline if no drafts exist yet.
4. Storefront: country-qualified final URLs, language, currency, shipping-policy copy, and no-payment checkout-to-shipping for any market being activated.
5. Reporting: confirm micro-conversion value cleanup is not inflating current ROAS.
