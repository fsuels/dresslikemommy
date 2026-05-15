# Pinterest Live Launch Attempt - CPC And 333-Scope Blocker

Generated: 2026-05-15 05:30 EDT

## Owner Approval Received

Owner approved live Pinterest launch:

`I approve creating and launching Pinterest catalog sales ads for advertiser 549756244483 using the 333-row refreshed scope, max $5/day test budget, no catalog/source/tag/CAPI/feed changes, no billing changes, and stop if Pinterest requires anything outside this scope.`

Owner then clarified an additional hard rule:

- Do not pay more than `$0.15` CPC.
- Use the refreshed `333` scope intelligently, not a lazy broad setup.
- Advertise only active products sold by Dress Like Mommy.

## Live UI Readback

Pinterest Ads Manager advertiser:

- Advertiser: `549756244483`
- Account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Create URL: `https://ads.pinterest.com/advertiser/549756244483/ads/create/?enter_from=Ad_reporting_create_campaign`

Campaign setup reached:

- Objective: `Catalog sales`
- Campaign name: `DLM_PIN_US_CATALOG_333_PAUSED_20260515`
- Budget type: `Daily`
- Budget amount entered: `$5.00`
- Initial ROAS optimization forced `Pinterest Performance+ bidding`; `Custom` was disabled.
- Switching optimization to `Pin clicks` enabled `Custom` bidding.
- Maximum CPC bid entered: `$0.15`

## Stop Reason

Launch was stopped before publish because the live product-group selector did not expose the exact `333` clean scope as selectable catalog groups.

The selector exposed broad existing groups instead, including:

- `All Products` with `5,664` products.
- `Family Matching Sets` with `1,011` products.
- `Family Matching Outfits` with `1,067` products.
- `Pajamas` with `252` products.
- `Mommy & Me Dresses` with `445` products.
- `Popular Mommy & Me` with `1,011` products.

Searches for exact scope/group labels did not find selectable exact groups:

- `DLM_PIN_US_SHOPPING`
- `DLM_PIN_US_SHOPPING_MOMMY_AND_ME`
- `DLM_PIN_US_SHOPPING_FAMILY_MATCHING`
- `DLM_PIN_US_SHOPPING_PAJAMAS`
- `mommy_me`
- `family_matching`

The data-source selector did include the scope feed profile `3041760867124595727`, but that source still exposed only broad groups, not the exact `333` clean split.

## 333-Scope Criteria

The intended `333` rows are a row-level whitelist, not a broad Shopify collection selection.

Required gates:

- `custom_label_0 = paid_eligible`
- `custom_label_4 = us_test_ready`
- `custom_label_2` in `mommy_me`, `family_matching`, or `pajamas`
- Pinterest EN-US item found and `IN_STOCK`
- Merchant approved / Shopping ads eligible
- image, price, availability, shipping policy, return policy, and PDP checks passed
- public PDP source-clean readback passed
- no supplier/source-domain leakage

The prior `342` scope was cut to `333` by excluding `9` variants across `2` public PDPs that exposed supplier/source domains.

Current intended split:

- `mommy_me`: `201` variants
- `family_matching`: `103` variants
- `pajamas`: `29` variants

## Decision

Do not publish a broad product-group campaign.

Publishing with `All Products`, broad `Family Matching`, broad `Mommy & Me`, or broad `Pajamas` would violate:

- the refreshed `333` scope,
- the public source-clean exclusion gate,
- the active/sellable paid-product rule,
- and the owner's requirement for a smart non-lazy setup.

## Smart Category Strategy

Yes, the launch should be divided by buyer category. The smart version is not one broad `All Products` ad set, and it is not the broad Shopify collection groups Pinterest exposed in the UI.

The launch should use exact product groups that match the clean active whitelist:

- Mommy & Me: `201` variants from `custom_label_2 = mommy_me`.
- Family Matching: `103` variants from `custom_label_2 = family_matching`.
- Pajamas: `29` variants from `custom_label_2 = pajamas`.
- Daddy & Me / father-inclusive: add only if current feed rows are active, paid-eligible, source-clean, in stock, and selectable as an exact group or explicitly approved to create as a new exact product group.

At `$5/day`, do not over-split into too many tiny ad groups unless the groups are exact and reportable. The practical first launch should prioritize the highest-intent category groups that can spend without violating the `$0.15` CPC cap or the 333-row active-product whitelist. Broad `Family Matching`, broad `Mommy & Me`, broad `Daddy & Me`, or broad `Pajamas` groups are acceptable only after a current readback proves every included item is active, sellable, source-clean, and inside the approved scope.

## Required Next Approval / Unblock

To launch exactly, the next safe path is to create or expose exact Pinterest product groups from current feed attributes, without changing catalog source, feed source, tag, CAPI, billing, or Shopify product data.

Minimum live target groups:

- `custom_label_0 = paid_eligible`
- `custom_label_4 = us_test_ready`
- `custom_label_2 = mommy_me`
- `custom_label_2 = family_matching`
- `custom_label_2 = pajamas`
- optional Daddy & Me / father-inclusive group only after exact active clean feed proof
- availability is in stock / active in Pinterest feed
- exclude the `9` held variants until repaired and read back clean

The operator should not proceed unless the approval explicitly allows creating the needed Pinterest product-group objects or the existing catalog surface already exposes exact equivalent groups.

## Guardrails Preserved

- No Publish click occurred.
- No Pinterest campaign was launched.
- No spend was enabled.
- No catalog source, feed source, tag, CAPI, billing, Shopify Admin, Merchant, Google Ads, or product data mutation occurred.
- No broad `All Products` campaign was launched.
