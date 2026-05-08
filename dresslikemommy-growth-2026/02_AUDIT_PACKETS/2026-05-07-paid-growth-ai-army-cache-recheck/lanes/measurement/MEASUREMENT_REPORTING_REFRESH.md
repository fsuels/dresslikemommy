# Measurement / Reporting Refresh

Date: 2026-05-07 EDT / 2026-05-08 UTC

Mode: parent local/read-only synthesis only. No Google Ads, GA4, GTM, Shopify Customer Events, Pinterest pixel/tag/CAPI, campaign, budget, bid, status, product-scope, feed, or conversion-goal changes.

## Trusted Enough For Guardrails

- Google Ads paid-value gate previously passed on a real Shopify paid order (`#9476`, order id `6575644803169`, value `19.99`, currency `USD`) with Google Ads purchase label `AW-853411529/UbkpCN-fhogBEMmN-JYD`, transaction dedupe, and enhanced conversion hash present.
- Google Ads reporting cleanup was completed on 2026-05-06: `Google Shopping App Purchase` remained primary/dynamic, and non-purchase micro-conversion values were changed to `Don't use a value` in Google Ads only.
- Theme source should not receive duplicate purchase snippets, duplicate Pinterest tags, custom CAPI tokens, or extra hardcoded Google/Pinterest conversion code while official app pixel paths own measurement.
- For ROAS decisions, use primary purchase `Conv. value / cost` and segmented purchase conversion value. Do not use historical `All conv. value / cost` where it includes pre-cleanup cart/checkout values.

## Stale Or Not Launch-Proof

- Pinterest official app pixel was set to `Always on` / share all events, and prior checkout diagnostics showed Pinterest checkout events unblocked, but Pinterest Event Quality still read `Fair` in the latest packet and needs a fresh readback before draft/spend decisions.
- Merchant paid-cohort `age_group` still had not cleared in diagnostics after Shopify-side repair and one approved product publication toggle; exact current issue count/export remains blocked by insufficient local Merchant API OAuth scopes unless a browser/account readback is run.
- No fresh GA4/GSC/account live readback was performed in this parent lane. Current sprint decisions should rely on the prior paid-value proof plus any fresh subagent readbacks, not assume dashboard state improved.

## Reporting Board For The Next Live Readback

| Surface | Metric / Readback | Decision Use | Current Posture |
|---|---|---|---|
| Google Ads active Shopping / Brand | Cost, clicks, avg CPC, primary purchases, purchase value, ROAS, search terms, country/device split | Budget/kill/scale decisions | Needs fresh account readback before budget/status decisions. |
| Google Ads paused nonbrand / intl Search | Status, budget, Manual CPC cap, networks, presence-only location, account-default purchase goal, RSA policy | Pre-import/pre-enable gate | Local packets only; no live import without approval. |
| Merchant Center | Paid-cohort item eligibility, source timestamp, age_group issue count, custom labels | Shopping/catalog confidence | Source propagation remains blocked/stale in latest evidence. |
| Pinterest | Event Quality, event freshness, click ID/product ID/email action items, EN catalog ingestion, item-level candidate proof | Draft/spend gate | Event/catalog proof is not sufficient for spend yet. |
| Storefront/localization | Policy copy, localized route quality, currency, no-payment checkout rates | International launch gate | Public copy was partial/stale; current localization lane is rechecking. |

## Economics Reminder

- Target ROAS `650%` allows ad cost of roughly `15.38%` of attributed revenue.
- At assumed AOV `$70`, max CPA for 650% ROAS is about `$10.77` before return/ops cushions.
- Cold traffic CPCs should stay near or below `$0.20` unless conversion rate proof justifies more:
  - `$0.10` CPC needs roughly `0.93%` CVR.
  - `$0.15` CPC needs roughly `1.39%` CVR.
  - `$0.20` CPC needs roughly `1.86%` CVR.
  - `$0.25` CPC needs roughly `2.32%` CVR and is expensive for unproven cold tests.

## Next Safe Measurement Action

Before any enablement, budget move, or paid international launch:

1. Fresh Google Ads readback segmented to primary purchase conversion value only.
2. Fresh Merchant paid-cohort source/item issue readback.
3. Fresh Pinterest Event Quality/catalog/item proof.
4. Slow storefront route/currency/policy/checkout readback by country.
5. Preserve official app tracking paths; do not add duplicate tags to compensate for dashboard lag.
