# Pinterest Corrected Label Product Groups Readback

Date: 2026-05-20

## Scope

Owner requested corrected Pinterest product groups created from category/feed labels, with count verification before any restart. This packet records only catalog product-group writes and readbacks.

No campaign/ad group/ad restart, budget, bid, status, source, feed, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or GTM write was made.

## Before State

Pinterest catalog source:

- Catalog: `3041764155561548387`
- Feed profile/source: `3041760873378113572`
- Source name: `DLM Cloudflare Grouped Feed 2026-05-18`

Broken item-ID groups in the catalog list before this correction:

| Product group | ID | Products |
|---|---:|---:|
| `DLM_PIN_US_SHOPPING_MOMMY_ME_333` | `4673019468477` | `1` |
| `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` | `4673019468479` | `0` |
| `DLM_PIN_US_SHOPPING_PAJAMAS_333` | `4673019468480` | `0` |

## New Label-Based Groups Created

All three new groups use `Match products for All filters below` with:

- `Custom label 0 is us`
- `Custom label 1 is ...` using the category/feed label values listed below

| New product group | ID | Feed label values | Preview count before save | After-save list count |
|---|---:|---|---:|---:|
| `DLM_PIN_US_LABEL_MOMMY_ME_20260520` | `4673019642205` | `Dresses`, `Sets`, `Swimwear`, `Sweaters`, `Tops` | `22` | `22` |
| `DLM_PIN_US_LABEL_FAMILY_MATCHING_20260520` | `4673019642201` | `Family Matching`, `Matching Family Sets`, `Matching Family Dresses`, `Matching Family Tops`, `Matching Family Outerwear`, `Matching Family Sweaters`, `Matching Family Swimwear` | `73` | `73` |
| `DLM_PIN_US_LABEL_PAJAMAS_20260520` | `4673019642195` | `Pajamas`, `Matching Family Pajamas` | `6` | `6` |

## Launch Gate

Do not restart or reattach the Pinterest catalog campaign until a fresh approval names these corrected groups and the final selector/readback confirms:

- only the corrected label-based groups above are selected, not broad `All Products`;
- the selected group counts still read back as `22`, `73`, and `6`;
- campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518` remains intentionally paused until the owner approves restart;
- max CPC, budget, optimization, source, and product-group scope are explicitly reviewed again before publish/enable.

## Campaign Status Readback After Group Creation

Pinterest Ads reporting on 2026-05-20 showed:

- `2 campaigns`
- `0 currently being served`
- `DLM_PIN_US_CATALOG_333_EXACT_20260518` / ID `626758581530`: `Paused`
- No restart, publish, launch, enable, budget, bid, or status action was taken.
