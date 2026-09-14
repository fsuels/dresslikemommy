# Google Shopping Parent-Outfit Missing Offers Repair Approval Packet

Mode: approval packet only. No additional Shopify Admin, Merchant primary-source, Google & YouTube publication, Google Ads, budget, bid, status, product-group, conversion, billing, or activation write is authorized by this document.

## Why This Packet Exists

The parent-outfit supplemental file was uploaded to Merchant source `10663204023`, and Merchant Center recognized the file attributes. Merchant processed `4,531` rows but matched only `4,390` rows. It reported `141` affected products with `Offer does not exist`.

The supplemental file can update labels, `item_group_id`, and hero images only for offers already present in Merchant. It cannot create primary product offers that the Google/Merchant source does not currently have.

## Affected Scope

All currently diagnosed missing rows are Mommy & Me:

| Parent product ID | Shopify title | Subgroup | Missing rows | Full parent missing |
|---|---|---:|---:|---|
| `6718948147297` | Matching Mom & Child One Shoulder Swimsuit | `swimwear` | `40` | `true` |
| `7562834215009` | Crochet Mommy and Me Set - Beach Coverup | `sets` | `35` | `true` |
| `6718945034337` | Mom & Child Matching Two Piece Swimsuit | `swimwear` | `20` | `true` |
| `6719764463713` | Matching Mommy And Me Hollow Out Bikini | `swimwear` | `10` | `true` |
| `6719774720097` | Matching Mommy & Me Orange Print Swimsuit | `swimwear` | `10` | `true` |
| `6719792873569` | Matching Mommy & Me Sunflower Print Swimsuit | `swimwear` | `10` | `true` |
| `7535944368225` | Powder Blue Mommy and Me Set — Flutter Top & Eyelet Pants | `tops_shirts` | `8` | `false` |
| `7227254276193` | Matching Yellow Sleeveless Maxi Dress Vibrant Summe... \| DLM | `dresses` | `6` | `false` |

Shopify Admin readback showed these parent products are `ACTIVE` and online-store published. Some whole missing parents did not read back as published to `Google & YouTube`, while the two partial parents did.

## Proposed Next Action

1. Read the exact Google & YouTube / Merchant publication state for the 8 parent products and their missing variants.
2. If the UI/API exposes a narrow product-level Google & YouTube publication or sync action, apply it only to those 8 parent products or their missing variants.
3. Do not change title, handle, price, inventory, body copy, SEO, vendor, theme, campaign, product group, budget, bid, conversion goal, billing, or Shopping campaign status.
4. Wait for Google/Merchant primary-source processing.
5. Rerun the parent-outfit Merchant/feed gate.
6. Keep all V2 Shopping campaigns paused.

## Exact Approval Phrase

Use this exact phrase only if you want the primary-source repair attempted:

> Approve the Google Shopping missing-offer primary-source repair only: keep all Shopping V2 campaigns paused, keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused, read back and repair only the Google & YouTube / Merchant publication or sync state for the 8 diagnosed Mommy & Me parent products, do not change titles/prices/handles/body/SEO/inventory/campaigns/budgets/bids/statuses/product groups/conversions/billing, wait for processing, and rerun the counts/images/no-catchall gate before any activation discussion.

## Activation Gate

Activation discussion remains blocked until after-state readback proves:

- V2 campaigns remain paused until separately approved.
- Old test campaign remains paused.
- No catchall leakage.
- Live ready-label rows match the expected included scope.
- Images match the parent/hero image contract.
- Missing Merchant offers are resolved or explicitly excluded from the eligible scope with updated parent counts.
