# Italian purchase: attribution semantics

**The purchase is real; paid acquisition remains unresolved.** The [existing reconciliation](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/CURRENT_SALES_CANDIDATE_RECONCILIATION.md:58) records GA4 `google/cpc` with `sessionCampaignId=23866684201`, while Shopify first/last visits are Google/SEO with null UTMs. This comparison alone proves neither a tracking defect nor incremental advertising revenue.

## Documented definitions

- **No UTMs does not mean no ad click.** Google auto-tagging uses GCLID, separately from manual UTM parameters. GA4 can therefore identify paid traffic without UTMs. “Google captured an ad marker that Shopify did not classify identically” is a hypothesis, not an observed cause here. [Google tagging](https://support.google.com/analytics/answer/11242870?hl=en).
- **Session dimensions are not event attribution.** GA4 session-scoped dimensions use paid-and-organic last-click and are unaffected by changing the property's attribution model. New campaign information during an existing session does not replace that session's campaign. Thus “data-driven versus last-click” alone does not explain this specific session row. [Scopes](https://support.google.com/analytics/answer/11080067?hl=en); [session processing](https://support.google.com/analytics/answer/11242841?hl=en).
- **The numeric campaign ID is not an independent Ads join.** `sessionCampaignId` includes manual and platform campaigns. Compare `sessionGoogleAdsCampaignId`, `sessionGoogleAdsCustomerId` and `sessionManualCampaignId`; the latter can come from `utm_id`. [GA4 schema](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema).
- Shopify first/last visits describe captured session endpoints. Intermediate visits require `moments`; the journey's first-session basis can be limited by the previous order or30-day attribution window. `ready` means attributed sessions have been created, not that every real visit was captured. [Journey schema](https://shopify.dev/docs/api/admin-graphql/latest/objects/customerjourneysummary). Cookie restrictions can limit Shopify journeys, but are only a possible explanation here. [Shopify limitations](https://help.shopify.com/en/manual/fulfillment/managing-orders/analytics/conversion-summary).

## Decisive private evidence checklist

1. Root checks `ready`, `momentsCount`, all `moments` pages and terminal pagination. Compare first/last endpoints with every captured `CustomerVisit`; processing readiness is not tracking completeness.
2. For each visit inspect `occurredAt`, `landingPage`, `referrerUrl`, `source`, `sourceType`, `sourceDescription`, `referralInfoHtml`, `utmParameters` and `marketingEvent`. `landingPage` is that session's first page; `sourceType` is a marketing-tactic classification. Privately inspect ad/UTM parameter presence, including `gclid` and `utm_id`; never publish raw click identifiers or token-bearing URLs. [Visit schema](https://shopify.dev/docs/api/admin-graphql/latest/objects/customervisit).
3. Align chronology with the GA4 purchase/session event timestamps and identifiers, accounting for timezone and session boundaries. Intermediate paid markers support an ad-related touch; organic-only captured moments do not prove that no ad touch occurred. Missing event-level evidence keeps the explanation UNKNOWN.

## What still needs Ads access

Read the existing campaign's matching-period clicks/spend and conversion-action source, primary/secondary scope, counting/window/model and values; verify any available click/conversion linkage. Reconcile interaction-date metrics separately from conversion-time columns. [Google conversion reporting](https://support.google.com/google-ads/answer/6270625?hl=en); [import/counting definitions](https://support.google.com/google-ads/answer/2375435?hl=en).

Shopify journeys cannot establish campaign cost, CPA, ROAS or incrementality. Full basket identity, refunds and actual fulfillment/settled costs remain separate requirements. No account, browser or production change was made; root owns the private join.
