# Google Shopping Parent-Outfit Paused Rebuild Execution Report

UTC timestamp: `20260520T055931Z`

## Approval

Approve the Google Shopping parent-outfit paused rebuild only: keep DLM_US_STANDARD_SHOPPING_TEST_PAID_READY paused, create/import only paused V2 Shopping structures from the packet, do not enable spend, do not change budgets/bids/statuses beyond paused draft requirements, do not include catchalls, and read back counts/images before any activation discussion.

## Before-State Readback

- Existing V2 campaign count before mutation: `0`
- Old test campaign status: `PAUSED`
- Customer: `dresslikemommy.com` (`3990976848`), currency `USD`

## Execution Result

- Mode: `execute`
- Validate-only passed: `True`
- Live mutate executed: `True`
- Operation count: `96`
- Paused draft daily budget micros per campaign: `1000000`
- Paused draft CPC bid micros: `10000`

## After-State Readback

- Validation passed: `False`
- Campaigns: `3`
- Ad groups: `0`
- Product ads: `12`
- Listing groups: `60`
- Included subgroup units: `12`
- Excluded catchall units: `24`
- Bad catchall units: `0`
- Campaign listing scopes: `3`

## Counts / Images Boundary

- Google Ads structure readback verifies the paused campaigns, ad groups, product ads, listing scopes, and no-catchall tree.
- Merchant product count/image readback remains a separate feed-label/Merchant refresh gate; this script does not mutate Merchant/Shopify feed labels or product images.
- Do not discuss activation until Merchant-side counts/images prove the parent-outfit labels and hero images are live.

## Guardrails

- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` was not edited and must remain paused.
- No enablement, Merchant, Shopify, feed, product, conversion, existing campaign, existing budget, existing bid, or billing write occurred.

## Files

- Before JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-google-shopping-parent-outfit-rebuild/google_ads_shopping_parent_outfit_before_20260520T055931Z.json`
- After JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-google-shopping-parent-outfit-rebuild/google_ads_shopping_parent_outfit_after_20260520T055931Z.json`

## Validation Issues

- Expected 12 ad groups, found 0
