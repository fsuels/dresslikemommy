# First GB Non-US Search Enable Execution Report

Date: 2026-05-12

## Approval

Owner approved:

`APPROVE ENABLE GB SEARCH CAMPAIGN 23838895360, AD GROUP Mommy & Me Dresses - Exact, WITH NO BUDGET, BID, PRODUCT SCOPE, FEED, MERCHANT, PINTEREST, OR CONVERSION GOAL CHANGES.`

## Action Taken

Enabled only:

- Campaign `23838895360` / `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
- Ad group `194138528537` / `Mommy & Me Dresses - Exact`

No other Google Ads campaign, ad group, keyword, ad, budget, bid, conversion goal, Merchant/feed/product scope, Pinterest, Shopify, PMax, Standard Shopping, or product-group change was made.

## Pre-Enable Guard

Pre-readback passed before the live action:

- Campaign was `PAUSED`.
- Channel was Search.
- Budget was unchanged at `US$2/day` (`2000000` micros).
- Google Search was on.
- Content network was off.
- YouTube was off.
- GB geo target type was presence-only for positive and negative settings (`LOCATION_OF_PRESENCE` / `LOCATION_OF_PRESENCE`).
- Target ad group `Mommy & Me Dresses - Exact` was paused.
- All other GB ad groups were paused.
- Split CSV target ad group had 3 exact-match high-intent keywords:
  - `mommy and me dresses`
  - `mother daughter dresses`
  - `mom and daughter matching outfits`
- Target final URLs were country-qualified with `?country=GB`.
- Campaign-level conversion goal override readback showed `has_campaign_override_goals=false`.

## Execution Notes

First scalar status RPC attempt used the old message-field merge operator and was rejected by Google Ads with `FieldMutateError.MERGE_USED_ON_NON_MESSAGE_FIELD`; post-readback still showed all entities paused, so no spend started.

The corrected scalar `UPDATE` operator was then used for exactly two status changes:

1. `AdGroupService.Mutate`: ad group `194138528537` status `PAUSED` -> `ENABLED`.
2. `CampaignService.Mutate`: campaign `23838895360` status `PAUSED` -> `ENABLED`.

## Post-Enable Readback

Final RPC readback passed:

- Campaign `23838895360`: `ENABLED`.
- Budget: still `US$2/day`.
- Channel: still Search.
- Google Search: still on.
- Content network: still off.
- YouTube: still off.
- Geo target type: still presence-only.
- Enabled ad groups: exactly one, `194138528537` / `Mommy & Me Dresses - Exact`.
- All other GB ad groups remained paused.

Final normalized summary:

- `raw/post-enable-readback/final_success_summary.json`

## Monitoring Rules

Apply the existing 650% ROAS guardrails:

- `$8` zero-purchase warning.
- `$16` zero-purchase hard-pause.
- `$24` zero-purchase ad-group kill/restructure.
- Pause immediately if non-GB traffic, policy disapproval, unexpected conversion-goal override, budget/bid drift, or any unintended ad group enablement appears.

## Next Growth Queue

Fastest smart next enables after GB:

1. `CA` campaign `23834423669`, ad group `Mommy & Me Dresses - Exact`, existing `$2/day`, `$0.15` max CPC, Canada presence-only, English-first.
2. `AU` campaign `23834424182`, ad group `Mommy & Me Dresses - Exact`, existing `$2/day`, `$0.15` max CPC, Australia presence-only, English-first.

Both still require fresh exact action-time approval before enablement.
