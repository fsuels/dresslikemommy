# Google Shopping Parent-Outfit Exact-Scope Enforcement Validate Blocked

Generated: `2026-05-21 10:59 EDT`

## Decision

Paused exact-scope product-group enforcement was built locally, but not executed.

Reason: `STOPPED__GOOGLE_ADS_API_BASIC_ACCESS_OPERATION_QUOTA_EXHAUSTED`

## Intended Enforcement Shape

The local script `execute_google_shopping_parent_outfit_exact_scope_enforcement.py` builds the safer paused structure needed before activation:

- keep all V2 campaigns paused
- keep all V2 ad groups paused
- keep all V2 product ads paused
- keep old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused
- preserve the parent/subgroup hierarchy
- replace each included subgroup unit with a subgroup subdivision
- add exact `product_item_id` units for the `4,370` reduced-scope candidate rows
- add an excluded item-level catchall under each subgroup subdivision
- keep the exact `141` unresolved-offer rows and exact `20` out-of-stock rows out of included item units

Expected operation plan:

- remove included subgroup units: `12`
- create subgroup subdivisions: `12`
- create exact item units: `4,370`
- create item-level catchall exclusions: `12`
- total operations: `4,406`
- batches: `12` Shopping ad groups

## Validate-Only Attempt

The first validate-only shape check failed because Google Ads required an explicit item-level `others` case below each item-ID subdivision. The script was patched to create explicit product-item-ID catchalls.

The second validate-only shape check then reached Google Ads API Basic Access quota limits:

- Error: `429 RESOURCE_EXHAUSTED`
- API message: `Too many requests. Retry in 62513 seconds.`
- Request ID: `dQSB-3UevUPdukZ_RQEPIw`
- Quota note: `Number of operations for basic access`

## Guardrails Preserved

- No execute mutation was sent.
- No campaign, ad group, or product ad was enabled.
- No spend was activated.
- No budget, bid, conversion, or billing change occurred.
- No Merchant feed/source write occurred.
- No Shopify product/publication/inventory/title/price/handle/SEO write occurred.
- No Google & YouTube sync occurred.
- No broad sync, source reset, or product recreation occurred.

## Current State

The current V2 label/subgroup tree must remain paused because prior preflight proved it would include `22` held rows if activated.

The next valid step is to retry validate-only after the Google Ads API quota window clears, then execute only if every batch validates and read back:

- `4,370` exact included item units
- `0` held item IDs included
- item-level catchall exclusions present
- all campaigns/ad groups/product ads still paused
- old test campaign still paused

Activation must remain separate.
