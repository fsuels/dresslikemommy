# Pinterest Exact Product Group Import Readback

Date: 2026-05-15 07:14 EDT

## Scope

- Advertiser: `549756244483`
- Catalog: `3041764155561548387`
- Feed profile: `3041760867124595727`
- Imported CSV: `pinterest_exact_product_group_item_id_import.csv`
- Allowed by current-session approval: exact active-clean product-group import only, then launch only after final review confirms max `$5/day`, max `$0.15` CPC, exact scope, and no source/feed/tag/CAPI/billing/Shopify changes.

## Import Result

- Used an upload-capable authenticated Chrome DevTools path.
- Uploaded and imported the exact CSV.
- Pinterest returned to the product group table after the import.
- Exact groups now exist:
  - `DLM_PIN_US_SHOPPING_MOMMY_ME_333`
  - `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333`
  - `DLM_PIN_US_SHOPPING_PAJAMAS_333`

## Readback

The imported filter payloads read back as exact item-ID filters:

| Product group | Imported item IDs read back | Pinterest selected/products readback |
|---|---:|---:|
| `DLM_PIN_US_SHOPPING_MOMMY_ME_333` | `201` | `0` |
| `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` | `103` | `0` |
| `DLM_PIN_US_SHOPPING_PAJAMAS_333` | `29` | `0` |

Additional Pinterest UI readback:

- Detail pages show `This product group updates every 24 hours`.
- Product previews are empty.
- `Promote` is disabled on the exact groups.
- Mommy & Me also displays the Pinterest warning `Product groups must contain 200 items or fewer to be published to boards.`

## Decision

No launch, publish, save, enable, campaign creation, ad group creation, ad creation, budget activation, bid activation, or spend was executed.

The item-ID import succeeded enough to expose exact filter payloads, but the launch gate did not pass because Pinterest has not resolved the product groups to usable product counts and the Promote action is disabled.

## Guardrails

- No broad product groups were selected.
- No source/feed/tag/CAPI/billing/Shopify changes were made.
- No Merchant, Google Ads, GA4/GTM, conversion, credential, theme, or billing mutation occurred.
- Do not launch until a fresh readback shows Pinterest usable product counts for the exact groups and final review confirms max `$5/day`, max `$0.15` CPC, exact active-clean scope, and no excluded changes.
