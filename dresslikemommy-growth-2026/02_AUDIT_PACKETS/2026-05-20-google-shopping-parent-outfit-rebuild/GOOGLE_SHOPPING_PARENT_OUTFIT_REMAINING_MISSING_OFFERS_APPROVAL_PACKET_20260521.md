# Google Shopping Parent-Outfit Remaining Missing Offers Approval Packet

Mode: approval packet only. This document authorizes no Shopify Admin, Merchant Center, Google & YouTube, Google Ads, budget, bid, status, product-group, conversion, billing, or activation write by itself.

## Why This Packet Exists

The prior approved repairs did their jobs, but the full live gate is still closed:

- Merchant source `10663204023` processed the parent-outfit supplemental file with `4,531` total rows and `4,390` matched offers.
- The missing-offer publication repair published the 8 diagnosed Mommy & Me parent products to Google & YouTube.
- The label-precedence repair updated older source `10626787326` so parent-outfit rows now win the ready labels.
- The fresh read-only propagation rerun on `2026-05-21T08:50:30Z` still reads `4,390 / 4,531` ready rows, leaving `141` expected rows missing from the Google Ads Shopping-product surface.

This is no longer a label-precedence, image, catchall, or campaign-structure issue. It is a remaining primary-source/live-offer presence issue for the missing expected offer IDs.

Follow-up read-only diagnosis on `2026-05-21T09:00:20Z` split the blocker:

- All `8` diagnosed products are `ACTIVE`, Online Store published, Google & YouTube published, and all `141` missing variant IDs still exist in Shopify.
- `72` Google Ads Shopping-product rows / `70` unique missing item IDs now exist in Google Ads but have blank `custom_label_0..4`; those need the approved supplemental labels/images to rematch.
- `71` item IDs are still absent from the Google Ads Shopping-product surface; those need a narrow Google & YouTube / Merchant primary-source presence repair.

Diagnosis evidence:

- `GOOGLE_SHOPPING_PARENT_OUTFIT_REMAINING_MISSING_OFFERS_DIAGNOSIS_20260521.md`
- `google_shopping_remaining_missing_offers_shopify_readback_20260521T085916Z.json`
- `google_ads_missing_offer_item_id_presence_probe_20260521T090020Z.json`

## Current Gate Evidence

Fresh gate file: `google_shopping_parent_outfit_merchant_feed_gate_20260521T085030Z.json`

- Gate passed: `false`
- Expected rows: `4,531`
- Ready rows: `4,390`
- Missing expected rows: `141`
- Unexpected ready rows: `0`
- Label mismatches on ready rows: `0`
- Image mismatches on ready rows: `0`
- Missing live images: `0`
- Bad catchall units: `0`
- V2 campaigns paused: `true`
- Old test campaign paused: `true`
- Activation discussion allowed: `false`

Current missing-row artifacts from the same stable `141`-row blocker:

- `google_shopping_parent_outfit_missing_expected_rows_20260521T070231Z.csv`
- `google_shopping_parent_outfit_missing_expected_parent_summary_20260521T070231Z.csv`

## Affected Scope

All current missing rows are still Mommy & Me:

| Parent product ID | Handle | Subgroup | Missing rows | Full parent missing |
|---|---|---:|---:|---|
| `6718948147297` | `matching-mom-child-one-shoulder-swimsuit` | `swimwear` | `40` | `true` |
| `7562834215009` | `white-crochet-mommy-and-me-set` | `sets` | `35` | `true` |
| `6718945034337` | `mom-child-matching-two-piece-swimsuit` | `swimwear` | `20` | `true` |
| `6719764463713` | `matching-mommy-and-me-hollow-out-bikini` | `swimwear` | `10` | `true` |
| `6719774720097` | `matching-mommy-me-orange-print-swimsuit` | `swimwear` | `10` | `true` |
| `6719792873569` | `matching-mommy-me-sunflower-print-swimsuit` | `swimwear` | `10` | `true` |
| `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `dresses` | `8` | `true` |
| `7535944368225` | `powder-blue-mommy-and-me-set` | `tops_shirts` | `8` | `false` |

## Proposed Smallest Next Repair

With fresh exact approval only:

1. Refresh only the existing approved parent-outfit supplemental sources needed to rematch the `70` unique now-visible blank-label item IDs.
2. Repair only the Google & YouTube / Merchant primary-source presence for the `71` item IDs still absent from Google Ads, scoped to the affected parent products.
3. If the only available control is a broad Google & YouTube account sync, broad Merchant source reset, product deletion/recreation, or campaign/feed-scope rewrite, stop and report instead of applying it.
4. Do not change title, handle, price, inventory, body copy, SEO, vendor, product type, theme, campaign, product group, budget, bid, conversion goal, billing, or Shopping campaign status.
5. Wait for Google & YouTube / Merchant / Google Ads processing.
6. Rerun the parent-outfit counts/images/no-catchall gate.
7. Keep all Shopping campaigns paused until the gate passes and the owner gives separate activation approval.

## Exact Approval Phrase

Use this exact phrase only if you want the remaining missing-offer primary-source repair attempted:

> Approve the Google Shopping remaining missing-offer primary-source repair only: keep all Shopping V2 campaigns paused, keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused, refresh only the existing approved parent-outfit supplemental sources needed to rematch the 70 unique now-visible blank-label offer IDs, repair only the Google & YouTube / Merchant primary-source or sync state for the 71 still-absent offer IDs from the diagnosed Mommy & Me parent products, do not change titles/prices/handles/body/SEO/inventory/publications outside that narrow Google & YouTube/Merchant presence repair, do not change campaigns/budgets/bids/statuses/product groups/conversions/billing, stop if only a broad account sync/source reset/product recreation path is available, wait for processing, and rerun the counts/images/no-catchall gate before any activation discussion.

## Activation Gate

Activation discussion remains blocked until after-state readback proves:

- V2 campaigns remain paused until separately approved.
- Old test campaign remains paused.
- No catchall leakage.
- Live ready-label rows match the expected included scope or the eligible scope is explicitly updated with owner approval.
- Images match the parent/hero image contract.
- Missing Merchant/Shopping offers are resolved or explicitly excluded from the eligible scope with updated parent counts.
