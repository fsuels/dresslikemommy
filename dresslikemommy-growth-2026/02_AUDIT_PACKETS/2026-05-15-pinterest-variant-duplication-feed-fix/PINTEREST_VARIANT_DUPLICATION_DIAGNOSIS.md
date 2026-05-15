# Pinterest Variant Duplication — Feed-Level Diagnosis

Generated: 2026-05-15
Mode: repo-local diagnostic only. No Pinterest, Shopify, Merchant, Google Ads, GA4/GTM, tag, CAPI, catalog, feed, source, product, budget, bid, status, launch, publish, billing, or spend write occurred.

## Owner-Reported Symptom

Pinterest catalog "Dresses" group shows 157 entries that are not 157 distinct products — they are size variants of a much smaller set of parent products. Example given by owner:

- `43831323066465` -> Lavender Mommy and Me Floral Applique Sleeveless Ruffle Dress – 120cm / Purple
- `43831323197537` -> Lavender Mommy and Me Floral Applique Sleeveless Ruffle Dress – S / Purple

Same dress. Different size. Submitted to Pinterest as two separate products with their own images and prices.

## Root Cause

The Shopify -> Pinterest feed (US/en source label `Shopify App API`, advertiser `549756244483`) is submitting one row per **variant**, with no `item_group_id` attribute grouping the variants under their parent product. Pinterest correctly treats each row as its own catalog item, so:

- Size/color variants appear as duplicate listings.
- `image_link` per row is whatever Shopify attached to that variant (often a swatch or a secondary image), not the main product hero image.
- Price shown per row is the variant price, not the lowest "from" price for the product.
- Ad creative pulled from the catalog inherits whichever variant Pinterest picks, producing the mixed-hero-image impression the owner observed.

## Evidence From The Approved Active-Clean Scope

Source CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-exact-product-group-unblock/pinterest_exact_product_group_item_id_import.csv`

Item-ID format used by the feed: `shopify_US_<parent_product_id>_<variant_id>` — confirming the feed already knows the parent product, it simply does not collapse variants under one `item_group_id`.

Parent-product collapse analysis across the 333-variant US active-clean scope:

| Group | Variant rows submitted | Unique parent products | Avg variants per parent | Worst offender |
|---|---:|---:|---:|---|
| Mommy & Me | 201 | 26 | 7.7 | parent `7227270791265` -> 32 rows |
| Family Matching | 103 | 7 | 14.7 | parent `7229259874401` -> 42 rows |
| Pajamas | 29 | 1 | 29.0 | parent `7228788867169` -> 29 rows |
| **Total** | **333** | **30** | **11.1** | — |

If `item_group_id = parent_product_id` were applied, Pinterest would dedupe the catalog from 333 entries to 30 parent products. Extrapolation to the larger "Dresses" group the owner referenced (157 entries) would land in the same ballpark — roughly 14 to 25 real dresses depending on how many sizes each carries.

## Why The "Wrong Image" Symptom Comes With Duplication

Shopify's Pinterest channel feed maps `image_link` per variant, defaulting to either the variant's assigned image (often a small swatch or color-specific shot) or, if none is assigned, the product's primary image. With no parent grouping, every variant ships its own `image_link`, so the most attention-grabbing variant — not the merchandised hero — wins ad placements.

The fix that solves both problems simultaneously is:

1. Set `item_group_id = parent_product_id` on every variant row.
2. Pin `image_link` to the parent product's primary image (`product.image.src`), keeping variant-specific shots under `additional_image_link` only.
3. Optionally suppress secondary size variants from the feed altogether, leaving one primary item per parent.

Either approach (1+2, or 1+2+3) eliminates the visible duplication in Pinterest's catalog UI within one 24-hour feed re-sync.

## Two Viable Fix Paths

### Path A — Native Shopify Pinterest sales-channel setting (fastest, lowest risk)

The Shopify Pinterest sales channel has a setting that controls whether variants are submitted as separate items or grouped under one parent item with `item_group_id`. The exact label varies by channel version but is typically under:

`Shopify Admin -> Sales channels -> Pinterest -> Settings -> Product feed / Variant submission`

Look for an option named one of:
- "Submit one product per variant" (currently ON — that is the bug)
- "Group variants under a single parent product"
- "Use item_group_id"
- "Submit only primary variants"

Toggling to the parent-grouping mode causes the next 24-hour feed re-sync to ship grouped items.

### Path B — Custom feed via Shopify Admin GraphQL (highest control)

If the native channel setting is not exposed or does not behave correctly, the canonical Pinterest catalog data feed (`catalog.txt` / Google-Shopping-style CSV) can be generated directly from `~/.config/dresslikemommy/shopify-admin.env` and uploaded to Pinterest as a separate feed source. In that mode the script:

- Walks `products` via Admin GraphQL.
- Emits one row per parent product (default) with `id = parent_product_id`, `image_link = product.featuredImage.url`, and `additional_image_link` filled from variant images.
- Emits `item_group_id` consistently if multiple-row-per-product mode is preferred.
- Excludes vendor/source URLs, per the repo guardrail.

Path B is more work but does not depend on Pinterest channel UI parity and is reproducible from the repo.

## Recommended Path

Start with Path A because the symptom shows the native channel app is already the active feed source. If Path A's toggle is missing or the next re-sync still shows duplication, fall back to Path B with a separate exact approval gate.

## Before/After Readback Plan

Before owner approves anything live, capture:

- Current Pinterest catalog item count for advertiser `549756244483`.
- Current Pinterest "Dresses" group entry count (owner-reported 157).
- Current item-ID format sample (must look like `shopify_US_<parent>_<variant>`).
- Screenshot/HTML of the relevant Shopify Pinterest channel setting page.

After the toggle (24h re-sync window), capture:

- New Pinterest catalog item count (expected ~30 for the active-clean US scope, materially lower for the full Dresses group).
- New "Dresses" group entry count.
- New item-ID sample (should be one row per parent or rows sharing `item_group_id`).
- Pinterest catalog warnings panel (no new disapprovals or feed errors).

## Stop Conditions

Stop before any save/publish if:

- The Shopify Pinterest channel setting page requires changes outside the feed-grouping toggle (e.g., re-authentication, scope changes, billing edits, currency edits, market mapping).
- The toggle is missing entirely — escalate to Path B before retrying.
- Pinterest catalog shows a new severity-1 disapproval after re-sync — pause and read back.
- Any unrelated Shopify channel (Google & YouTube, Facebook & Instagram, TikTok) shows a setting change as a side effect — stop and read back.

## Approval Required

Exact phrase to unblock the live toggle (owner must paste back verbatim before any save in Shopify Admin):

`I approve toggling the Shopify Pinterest sales-channel feed to group variants under a single parent product via item_group_id for advertiser 549756244483, with no Shopify product/title/price/inventory/vendor/type/policy edits, no Pinterest campaign/budget/bid/status/audience/tag/CAPI/billing changes, and no edits to other sales channels. After the 24-hour Pinterest re-sync, capture the after-state readback and only then consider promoting/launching.`

## Why This Is Sales-Moving

- Pinterest ad creative will pull the merchandised hero image instead of size-swatch variants -> higher CTR.
- Catalog spend is no longer split across duplicate listings -> lower wasted impressions and clearer per-product reporting.
- The active-clean 333-row scope already validated for the paid-growth sprint will collapse to ~30 real products, matching the way Pinterest auctions actually evaluate creative.
- It directly unblocks the existing `PROB-2026-05-08-PINTEREST-EVENT-QUALITY` line because exact product-group product counts will become non-zero on the parent dimension, not the variant dimension.

## What This Does Not Do

- Does not change Pinterest tag, CAPI, conversion settings, event quality directly, budget, bid, campaign status, audience, billing, or account.
- Does not change Shopify product data, titles, prices, vendors, types, policies, inventory, or theme.
- Does not change Merchant Center, Google Ads, Facebook/Instagram catalog, TikTok catalog, or any non-Pinterest feed source.
- Does not retroactively republish historical Pinterest pins; only catalog ingestion changes.
