# Google Shopping Parent-Outfit Unresolved Offer Exclusion Approval Packet

Generated: `2026-05-21T09:59:11Z`

Mode: approval packet only. No Merchant, Shopify, Google & YouTube, Google Ads, campaign, product group, budget, bid, status, conversion, billing, feed, product-data, inventory, or activation write is authorized by this document.

## Why This Packet Exists

The approved Merchant TSV refresh succeeded at the source level, but the parent-outfit gate still fails closed.

Latest read-only gate:

- Gate timestamp: `20260521T095116Z`.
- Expected rows: `4,531`.
- Ready-label rows: `4,390`.
- Missing expected rows from the gate: `141`.
- Label mismatches: `0`.
- Image mismatches: `0`.
- Missing live images: `0`.
- Bad catchall units: `0`.
- V2 Shopping campaigns paused: `true`.
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused: `true`.

Read-only eligibility diagnostic:

- Diagnostic timestamp: `20260521T095911Z`.
- Google Ads expected offer IDs present: `4,460`.
- Google Ads expected offer IDs absent: `71`.
- Present expected offer IDs without approved ready label: `70`.
- Current ready-label rows: `4,390`.
- Merchant source `10663204023`: `4,531` total updated products, `4,392` matched products, all attributes recognized, `139` `Offer does not exist` rows.
- Merchant Content API strict product/item_group readback remains unavailable because the token returns `invalid_scope`.

The unresolved scope is not caused by a Shopify active/publication flag. All `8` diagnostic parent products read back `ACTIVE`, Google & YouTube published, and no Shopify product feedback messages.

## Exact Exclusion Scope

Use this exact local CSV as the exclusion scope:

- `google_shopping_parent_outfit_unresolved_offer_exclusion_scope_20260521T095911Z.csv`

It contains exactly `141` unresolved Mommy & Me offer IDs:

- `71` absent from Google Ads `shopping_product`.
- `70` present in Google Ads but without `custom_label_4=us_parent_outfit_ready_v20260520`.

Breakdown:

| Status | Parent product | Handle | Rows |
|---|---:|---|---:|
| Absent | `7562834215009` | `white-crochet-mommy-and-me-set` | `35` |
| Absent | `6718945034337` | `mom-child-matching-two-piece-swimsuit` | `20` |
| Absent | `6719774720097` | `matching-mommy-me-orange-print-swimsuit` | `10` |
| Absent | `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `6` |
| Present without ready label | `6718948147297` | `matching-mom-child-one-shoulder-swimsuit` | `40` |
| Present without ready label | `6719764463713` | `matching-mommy-and-me-hollow-out-bikini` | `10` |
| Present without ready label | `6719792873569` | `matching-mommy-me-sunflower-print-swimsuit` | `10` |
| Present without ready label | `7535944368225` | `powder-blue-mommy-and-me-set` | `8` |
| Present without ready label | `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `2` |

## Separate Out-Of-Stock Hold

The diagnostic also found `20` ready-label rows with `not_eligible_out_of_stock`.

Use this local CSV as a separate out-of-stock hold:

- `google_shopping_parent_outfit_eligibility_out_of_stock_rows_20260521T095911Z.csv`

Breakdown:

- `15` rows: `eternal-love-family-matching-t-shirts-colorful-heart-design`.
- `3` rows: `playful-graphic-family-matching-tops`.
- `1` row: `red-plaid-family-matching-tops`.
- `1` row: `golden-daisy-mommy-and-me-set`.

This packet does not approve inventory edits. If those variants later become in stock naturally or by separate owner-approved product operation, they can be rechecked read-only.

## Recommended Approval Path

Recommended next action: approve exclusion-gate preparation first, not another upload/resync.

Why this is better first:

- The unresolved `141` rows already resisted the narrow publication resync, attribute repair, and approved Merchant TSV refresh.
- The current `4,390` ready-label rows have clean labels/images and `0` bad catchalls.
- The main Ads hard error on present rows is `not_eligible_in_any_campaign`, which is expected while the campaigns are intentionally paused.
- Repeating uploads or broad syncs risks another loop; accepting a reduced, explicit eligible scope lets the sprint move toward a clear activation-review packet while preserving the unresolved rows as a separate repair lane.

## Approval Phrase

If approved, paste this exact phrase:

```text
Approve Google Shopping parent-outfit unresolved-offer exclusion gate only: use the exact 141-row exclusion scope in google_shopping_parent_outfit_unresolved_offer_exclusion_scope_20260521T095911Z.csv and the exact 20-row out-of-stock hold in google_shopping_parent_outfit_eligibility_out_of_stock_rows_20260521T095911Z.csv to prepare a reduced read-only activation-review gate for the current ready-label parent-outfit scope. Do not activate, unpause, change Merchant feeds/sources, trigger Google & YouTube sync, change Shopify products/publications/inventory/prices/titles/handles/SEO, change Google Ads campaigns/product groups/budgets/bids/statuses/conversions/billing, or broaden scope. Stop with an evidence packet and a separate activation approval packet only if the reduced gate passes.
```

## Allowed If Approved

- Build a local reduced-scope read-only gate using current ready-label rows minus the `20` out-of-stock hold.
- Report updated candidate counts and parent counts.
- Prepare a separate activation approval packet only if the reduced read-only gate passes labels/images/catchalls/campaign-paused safety.
- Keep the `141` unresolved rows and `20` out-of-stock rows out of the activation-review scope until separately repaired and read back clean.

## Still Blocked Without Separate Approval

- No Shopping campaign activation or unpause.
- No budget, bid, status, product group, campaign, conversion, or billing changes.
- No Merchant feed/source upload, source reset, fetch trigger, or broad sync.
- No Shopify product title, price, body, handle, SEO, inventory, publication, variant, image, or Google & YouTube setting changes.
- No live write to remove or alter products. This packet is for gate preparation and activation-review scope only.

## Evidence

- `google_shopping_parent_outfit_merchant_feed_gate_20260521T095116Z.json`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_20260521T095116Z.md`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_ELIGIBILITY_DIAGNOSTIC_20260521T095911Z.md`
- `google_shopping_parent_outfit_eligibility_diagnostic_20260521T095911Z.json`
- `google_shopping_parent_outfit_eligibility_missing_rows_20260521T095911Z.csv`
- `google_shopping_parent_outfit_eligibility_present_rows_20260521T095911Z.csv`
- `google_shopping_parent_outfit_unresolved_offer_exclusion_scope_20260521T095911Z.csv`
- `google_shopping_parent_outfit_eligibility_out_of_stock_rows_20260521T095911Z.csv`
