# Pinterest US Paused Draft Solution

Date: 2026-05-08
Mode: local build package only, no Pinterest account write

## Supersession Notice

This `337` resolved / `9` excluded package is superseded by the later read-only unblock packet:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/`

Future paused Pinterest draft work should use:

- Clean scope: `lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`.
- Exclusions: `lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`.
- Exact approval gate: `APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

Do not use the older `resolved_337_product_scope.csv` / `excluded_unresolved_9.csv` files unless a future just-in-time readback proves the newer 342/4 scope regressed.

## Decision

`LOCAL_PAUSED_US_PINTEREST_DRAFT_PACKAGE_READY_WITH_337_RESOLVED_ROWS`

This is the concrete fix path for the Pinterest lane: stop treating the `9` unresolved rows as a total blocker. Build the first US-only paused draft scope from the `337` rows that already resolved as EN-US and `IN_STOCK`, and explicitly exclude the `9` unresolved Mommy & Me variants unless they re-resolve immediately before account-side build.

No Pinterest campaign, draft, product group, budget, bid, catalog, tag, CAPI, audience, Shopify, Merchant, Google Ads, or feed write was made.

## Product Scope

Source file:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-pt-presentment-url-readback/lanes/pinterest/raw/full_item_metadata_rows.csv`

Output files:

- `resolved_337_product_scope.csv`: all rows with `status=FOUND_EN_US_IN_STOCK`.
- `excluded_unresolved_9.csv`: all rows with `status=NOT_FOUND_BY_PIN_METADATA`.
- `product_group_scope.csv`: product-group-level inclusion and exclusion rules.

Counts:

| Product group | Resolved rows | Rule |
|---|---:|---|
| `DLM_PIN_US_SHOPPING_MOMMY_AND_ME` | `205` | Include resolved rows only; exclude 9 unresolved variants from product `7229026304097`. |
| `DLM_PIN_US_SHOPPING_FAMILY_MATCHING` | `103` | Include resolved rows only. |
| `DLM_PIN_US_SHOPPING_PAJAMAS` | `29` | Include resolved rows only. |
| Total | `337` | US / EN Shopify source only. |

Excluded rows:

- Shopify product `7229026304097`.
- Variants:
  - `41878208249953`
  - `41878208282721`
  - `41878208315489`
  - `41878208446561`
  - `41878208479329`
  - `41878208512097`
  - `41878208577633`
  - `41878208610401`
  - `41878208643169`

## Paused Draft Structure

Draft plan file: `paused_campaign_draft_plan.csv`.

Proposed structure after exact approval:

- One US-only paused campaign:
  - `DLM_PIN_US_CATALOG_RETARGETING_PAUSED_20260508`
  - status `Paused`
  - starting budget placeholder `$1/day`
  - no spend because campaign remains paused
- Three paused product/ad groups:
  - `DLM_PIN_US_MOMMY_ME_RESOLVED_205`
  - `DLM_PIN_US_FAMILY_MATCHING_RESOLVED_103`
  - `DLM_PIN_US_PAJAMAS_RESOLVED_29`

Creative copy file: `creative_draft_rows.csv`, sourced from the claim-safe creative lane. It contains only local paused draft copy and carries no shipping-speed, promo, review, bestseller, local inventory, physical-store, warehouse, stocked inventory, or guaranteed-stock claims.

## Just-In-Time Readback Before Any Pinterest Account Write

1. Confirm advertiser `549756244483` and domain `dresslikemommy.com`.
2. Confirm campaign baseline is still `0 campaigns`, `0 currently serving`, `$0.00` spend, unless the owner created something outside this lane.
3. Confirm Event Quality current state and updated date.
4. Confirm Tag and CAPI are still receiving recent events.
5. Confirm EN Shopify source `3041760867124595727` is still completed with `0` failed uploads.
6. Re-run item proof for the exact rows in `resolved_337_product_scope.csv`.
7. Keep the `9` rows in `excluded_unresolved_9.csv` excluded unless they re-resolve as EN-US and `IN_STOCK`.
8. Confirm no failed sitemap or localized source is used for this US draft.

## Exact Approval Gate

Before any Pinterest account-side draft creation:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE ONLY RESOLVED EN-US IN-STOCK ROWS OR EXCLUDE UNRESOLVED ROWS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

## Why This Is A Solution

The previous blocker was not that Pinterest had zero usable catalog proof. It was that `9` rows did not resolve. This package changes the execution path from "wait for perfect" to "build a scoped paused draft from proven rows, exclude the failures, and keep spend off until readbacks and approval clear."

The remaining Event Quality `Fair` state is still a risk for live spend, but it does not prevent preparing an approval-gated paused US draft if the owner accepts that the first draft will remain paused and read back before activation.
