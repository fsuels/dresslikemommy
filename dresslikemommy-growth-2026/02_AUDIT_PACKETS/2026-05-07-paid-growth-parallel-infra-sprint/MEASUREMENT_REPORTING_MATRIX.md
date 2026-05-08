# Measurement And Reporting Matrix

Date: 2026-05-07
Owner lane: parent/orchestrator
Mode: local/read-only synthesis only

## Trusted Measurement State

- Paid purchase value gate previously passed on a real paid Shopify order: order `#9476`, order id `6575644803169`, value `19.99`, currency `USD`, Google Ads purchase label `UbkpCN-fhogBEMmN-JYD`, enhanced conversion hash present.
- Google Ads conversion cleanup was completed on 2026-05-06: `Google Shopping App Purchase` stayed primary/dynamic; non-purchase micro-conversion values were set to no value in Google Ads only.
- Theme should not receive duplicate purchase snippets, duplicate Pinterest tags, custom CAPI tokens, or new tracking code while the official app pixel paths own tracking.
- Pinterest official app pixel was set to `Always on` / share all events on 2026-05-06; storefront-to-checkout diagnostic showed Pinterest checkout was unblocked, but Pinterest Event Quality still read `Fair` pending platform refresh.

## Reporting Metrics To Use For 650% ROAS

- Use Google Ads `Conv. value / cost` and `Conversion value` only when segmented to the primary purchase action.
- Ignore historical `All conv. value / cost` for ROAS decisions where it includes pre-cleanup add-to-cart or begin-checkout value.
- For campaign decisions, export or read back: cost, clicks, average CPC, primary purchases, primary purchase value, CPA, ROAS, search terms, country, device, landing page, product/item ID when available, and product group.
- For Pinterest, do not treat Event Quality alone as launch proof. Require catalog eligibility, fresh event receipt, product/value/event_id health, and actual purchase-quality reporting once spend exists.

## 650% Target Math

- Target ROAS `650%` means max ad cost is about `15.38%` of attributed revenue.
- At assumed AOV `$70`, target max CPA is about `$10.77` before return-risk and contribution-margin cushions.
- With assumed 50% gross margin, each `$70` order has about `$35` gross margin before ad spend and operations; a `$10.77` CPA leaves about `$24.23` gross margin before returns/refunds/ops.
- Safe tests need CPC and conversion-rate pairing:
  - `$0.10` CPC can support about `0.93%` CVR at target CPA.
  - `$0.15` CPC can support about `1.39%` CVR.
  - `$0.20` CPC can support about `1.86%` CVR.
  - `$0.25` CPC can support about `2.32%` CVR, which is why it is expensive for cold tests.

## Readback Cadence

- Daily while spend is live: campaign status, spend, CPC, search terms, primary conversions, conversion value, ROAS, product/country split, and unexpected policy/feed warnings.
- After any tracking or event-quality fix: rerun a no-purchase checkout diagnostic and wait for platform event-quality refresh rather than adding duplicate tracking.
- Before enabling any paused campaign: just-in-time readback of conversion goals, status, budget, bid caps, networks, location presence, policy status, landing page, and no accidental product/feed expansion.

## Current Data Gaps

- Merchant paid-cohort `age_group` diagnostic clear remains pending after the single-product Google & YouTube toggle; this affects feed confidence, especially for Shopping/catalog expansion.
- Pinterest Event Quality may still read `Fair`; real Click ID coverage cannot be proven until Pinterest paid traffic exists, but spend should not start before catalog/tag gates are reread.
- Non-US markets have shipping rates for GB/CA/AU in the fresh checkout probe, but country-specific returns/duties/currency/localized landing-page quality and Merchant/Pinterest catalog eligibility remain unproven.

## Next Safe Action

- Build local paused campaign/import/copy/reporting packets now.
- Request action-time approval only for paused infrastructure creation or additional read-only/official refresh steps.
- Do not enable spend until measurement, feed/catalog, landing-page, and economics gates are clean by country/campaign.
