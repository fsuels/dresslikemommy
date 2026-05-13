# Continuation Handoff

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-google-ads-gb-ca-au-performance-es-it-qa`

Use the single owner-standard continuation prompt:

- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`

## Current State

- GB/CA/AU exact Search micro-cohort is live/eligible:
  - GB `23838895360`
  - CA `23834423669`
  - AU `23834424182`
  - Exact ad group `Mommy & Me Dresses - Exact`
  - Enabled exact keywords: `mommy and me dresses`, `mother daughter dresses`, `mom and daughter matching outfits`
  - One enabled RSA per market
  - `$2/day`, Search only, presence-only, no campaign conversion override, all other GB/CA/AU ad groups paused
- Latest read-only performance/search-term monitor shows `0` clicks, `0` impressions, `$0.00` cost, `0.00` conversions, and `0.00` conversion value. No actionable search terms yet.
- Working search-term route is `/aw/keywords/searchterms`; the captured page had an unrelated stale `Keyword: "human hair wigs"` UI filter, so do not act on that search-term table until the filter is avoided/cleared and traffic exists.
- Pinterest paused US draft is exact-approved but blocked by authenticated Ads Manager access/tooling.
- ES/IT review package is ready; Golden Daisy country-qualified landing QA passed for ES/IT, but native-speaker signoff remains required before platform use.

## Exact Next Actions

1. Run the next GB/CA/AU read-only monitor after reporting has time to populate. If search terms appear, capture attributable rows and propose negatives only from evidence.
2. Restore Pinterest access: authenticate advertiser `549756244483` in the controllable Chrome/CDP session or fix macOS automation permission for Computer Use. Then build only paused US catalog/retargeting draft objects from the clean `342` EN-US scope with the `4` exclusions. No live spend, no budget/bid activation, and no catalog/source/tag/CAPI/audience/feed changes.
3. Send `ES_IT_NATIVE_REVIEW_REQUEST.md` plus the four ES/IT CSVs to a real native reviewer. Do not upload ES/IT rows until native signoff and exact approval.

## Guardrails

No additional live spend, campaign enablement, budget/bid/status changes, negative live edits, Google Ads upload/preview/apply, Pinterest account writes, Merchant uploads/source edits, Shopify product/feed/conversion writes, checkout payment/order/refund/cancel, credential/account/billing edits, or destructive filesystem actions without fresh exact action-time approval naming the action and surface.
