# Perfect Before Advertising Checklist

Date: 2026-05-10

Mode: launch-readiness prep only. This document records the owner's broad authority to get everything ready and start advertising only when the setup is clean. It does not execute a live enable.

## Owner Authority Interpretation

The owner wants the operator to keep building until the paid-growth machine is ready, and to start advertising when everything is perfect enough to protect profit. The safe interpretation is:

- Continue all local, read-only, paused, draft, evidence, and verification work without stopping at old planning gates.
- Treat live spend and enablement as allowed only after every launch gate below passes for the exact named campaign/ad group.
- Do not launch broad country sets. The first possible spend unit remains one Google Search ad group: campaign `23838895360`, ad group `Mommy & Me Dresses - Exact`.
- Do not make product/feed/conversion/PMax/Shopping/Pinterest/Shopify product-data changes as part of first enable.

## Hard Pass Gates Before Any New Spend

| Gate | Pass condition | Current state | If fail |
|---|---|---|---|
| Measurement | Non-US `purchase` event proves correct currency/value/transaction id into GA4/Google Ads, or owner explicitly accepts a controlled test-purchase result | Not passed; only pre-purchase GB/DE evidence exists | Do not enable spend |
| Campaign identity | Just-in-time readback confirms campaign `23838895360`, Search, paused, budget `$2/day`, Manual CPC, max CPC `$0.15`, GB presence-only | Prior readback passed; must be repeated at action time | Do not enable |
| Ad group identity | Just-in-time readback confirms ad group name exactly `Mommy & Me Dresses - Exact`, paused, exact keywords only, final URLs country-qualified for GB | Local bug fixed in docs; must be repeated live | Do not enable |
| Landing page | Browser readback confirms the GB final URL is visible, no 403/verification wall, GBP/GB presentment, no stale beach/Christmas metadata, cart/checkout entry works without payment | Passed later in packet; repeat at action time | Do not enable if it fails |
| Search-only guard | Content network and YouTube off; no PMax, Shopping, feed label, Merchant feed, or product group binding | Prior readback passed; must be repeated | Do not enable |
| Conversion goal | Account-default purchase action only; no campaign-level conversion goal override | Prior readback passed; must be repeated | Do not enable |
| Existing live campaigns | Standard Shopping and Brand Search read back unchanged and not regressed | Prior evidence passed; must be repeated if action is same session | Do not enable |
| Problem tracker | No active P1 gate blocks first enable; all blockers have exact next action | Measurement gate still blocks | Do not enable |
| Coordination | No active conflicting Google Ads writer claim | Must be checked at action time | Do not enable |
| Monitoring | 24h/72h/7d scorecard and rollback procedure ready before the click | Local template ready in this packet | Do not enable |

## First Spend Unit If Gates Pass

- Platform: Google Ads Search
- Campaign: `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
- Campaign ID: `23838895360`
- Market: `GB`
- Ad group: `Mommy & Me Dresses - Exact`
- Daily budget: existing `$2/day`; no budget change
- Max CPC: existing `$0.15`; no bid change
- Activation scope: enable only this one ad group and the containing campaign if both are still paused and all other ad groups remain paused

## Stop Conditions

Stop before any enable if:

- Any readback names `Mommy & Me Dresses - Exact only` instead of the actual ad group `Mommy & Me Dresses - Exact`.
- Any readback shows campaign/ad group already enabled, wrong campaign ID, wrong market, wrong budget, wrong CPC, wrong network, wrong geo, or conversion-goal override.
- The final URL shows verification wall, wrong country/currency, stale metadata, or broken cart/checkout entry.
- Measurement still lacks non-US purchase currency/value proof.
- The operator would need to change budget, bid, product scope, product groups, Merchant feed, conversion goals, PMax, Standard Shopping, Pinterest, or Shopify product data to proceed.

## Current Verdict

`NOT_READY_FOR_LIVE_SPEND` because the non-US purchase-event currency/value gate is still open. The GB final URL browser readback passed later in this packet, but it still must be repeated at action time before any enable.
