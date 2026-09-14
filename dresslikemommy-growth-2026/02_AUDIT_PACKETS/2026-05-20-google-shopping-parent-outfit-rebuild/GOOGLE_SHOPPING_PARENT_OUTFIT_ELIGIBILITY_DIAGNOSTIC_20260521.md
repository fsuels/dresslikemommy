# Google Shopping Parent-Outfit Eligibility Diagnostic

Generated: `2026-05-21T10:12:00Z`

Mode: read-only diagnostic closeout. No Merchant feed/source, Shopify product/publication, Google & YouTube setting, Google Ads campaign/product-group/budget/bid/status/conversion/billing, product data, label, inventory, price, handle, SEO, broad sync, or activation change occurred.

## Approval Boundary Used

Owner approved only the diagnostic phrase in `GOOGLE_SHOPPING_PARENT_OUTFIT_ELIGIBILITY_CONTROL_SURFACE_APPROVAL_PACKET_20260521.md`.

The work stayed inside that boundary:

- Existing authenticated Merchant Center source page was read only.
- Google Ads Shopping-product issue diagnostics were read only.
- Local gate and diagnostic CSV/JSON artifacts were derived from saved readbacks.
- No activation discussion is opened by this packet.

## Current Gate State

Latest current gate evidence:

- `google_shopping_parent_outfit_merchant_feed_gate_20260521T095240Z.json`
- `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_GATE_READBACK_20260521T095240Z.md`
- `google_shopping_parent_outfit_ready_products_20260521T095240Z.csv`

Readback:

| Check | Result |
|---|---:|
| Expected parent-outfit rows | `4,531` |
| Ready rows | `4,390` |
| Missing expected rows | `141` |
| Label mismatches on ready rows | `0` |
| Image mismatches on ready rows | `0` |
| Missing live images | `0` |
| Bad catchall included units | `0` |
| V2 Shopping campaigns paused | `true` |
| Old test campaign paused | `true` |
| Activation discussion allowed | `false` |

Merchant source `10663204023` still reads as refreshed from the approved TSV:

- `4,531` total updated products
- `4,392` matched products
- `139` `Offer does not exist`
- all attributes recognized
- last updated `May 21, 2026 5:35 AM`

Evidence: `merchant_source_10663204023_after_approved_tsv_refresh_20260521T093710Z.json`.

## Merchant API Scope Result

The local API diagnostic attempted read-only Merchant and Content API product/status exports for Merchant account `124884876`.

Result: blocked by OAuth scope, not by a product-data finding.

Evidence:

- `eligibility_diagnostic_20260521/merchant_center_api_diagnostics_summary.json`
- `eligibility_diagnostic_20260521/merchant_center_api_diagnostics_evidence.csv`

Errors captured:

- Merchant API `products.list`: HTTP `403`, `PERMISSION_DENIED`, insufficient authentication scopes.
- Content API `productstatuses.list`: HTTP `403`, `PERMISSION_DENIED`, insufficient authentication scopes.

Because of this, strict live Merchant API proof for `item_group_id` and approval/source fields remains unavailable from the local token. The authenticated Merchant browser source page did confirm the source-level processing numbers above.

## Google Ads Issue Diagnostic

Read-only Google Ads Shopping-product diagnostics were run against the exact `4,531` expected parent-outfit offer IDs.

Primary evidence:

- `eligibility_diagnostic_20260521/google_ads_expected_offer_issue_diagnostic_summary_20260521.json`
- `eligibility_diagnostic_20260521/google_ads_expected_offer_issue_diagnostic_unique_20260521.csv`
- `eligibility_diagnostic_20260521/google_ads_expected_offer_issue_diagnostic_20260521.csv`
- `eligibility_diagnostic_20260521/google_ads_expected_offer_absent_from_ads_surface_20260521.csv`
- `eligibility_diagnostic_20260521/google_ads_expected_offer_parent_presence_summary_unique_20260521.csv`

Unique-item summary:

| Diagnostic | Count |
|---|---:|
| Expected offer IDs | `4,531` |
| Unique expected IDs found on Ads Shopping-product surface | `4,460` |
| Expected IDs absent from Ads Shopping-product surface | `71` |
| Unique status `NOT_ELIGIBLE` | `4,460` |
| Unique `IN_STOCK` | `4,440` |
| Unique `OUT_OF_STOCK` | `20` |
| Unique items with `not_eligible_in_any_campaign` | `4,460` |
| Unique items with warning `missing_item_attribute_for_product_type` | `4,580` issue instances across found items |
| Unique items with non-campaign error `not_eligible_out_of_stock` | `20` |

Important interpretation:

- `not_eligible_in_any_campaign` appears on every Ads-visible expected item. Under this diagnostic scope, that is consistent with all parent-outfit Shopping campaigns remaining paused and no approved active Shopping campaign advertising this scope. It is not an instruction to activate spend.
- `missing_item_attribute_for_product_type` is warning-level evidence. It is not the current counts/images/no-catchall blocker.
- `not_eligible_out_of_stock` is a real non-campaign eligibility error on `20` expected offer IDs. Because inventory changes were not approved, the next safe handling is exclusion from strict paid-ready eligibility until stock state changes, or a separate exact inventory/source decision.

## Remaining Blocker Split

Derived split evidence:

- `eligibility_diagnostic_20260521/google_shopping_parent_outfit_remaining_blocker_split_20260521.json`
- `eligibility_diagnostic_20260521/google_shopping_parent_outfit_gate_missing_ads_visible_blank_or_not_ready_20260521.csv`
- `eligibility_diagnostic_20260521/google_shopping_parent_outfit_gate_missing_ads_absent_20260521.csv`
- `eligibility_diagnostic_20260521/google_shopping_parent_outfit_out_of_stock_expected_items_20260521.csv`

The `141` gate-missing rows split cleanly:

| Split | Rows | Meaning |
|---|---:|---|
| Ads-visible but blank/not-ready labels | `70` | Offer IDs exist in Ads Shopping-product readback but do not have the ready label set that the gate requires. |
| Ads-surface absent | `71` | Offer IDs are in the expected spec but absent from Ads Shopping-product readback. |
| Total missing | `141` | Matches the latest gate failure. |

Parent summary for the `70` Ads-visible blank/not-ready rows:

| Parent product | Handle | Rows |
|---:|---|---:|
| `6718948147297` | `matching-mom-child-one-shoulder-swimsuit` | `40` |
| `6719764463713` | `matching-mommy-and-me-hollow-out-bikini` | `10` |
| `6719792873569` | `matching-mommy-me-sunflower-print-swimsuit` | `10` |
| `7535944368225` | `powder-blue-mommy-and-me-set` | `8` |
| `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `2` |

Parent summary for the `71` Ads-absent rows:

| Parent product | Handle | Rows |
|---:|---|---:|
| `7562834215009` | `white-crochet-mommy-and-me-set` | `35` |
| `6718945034337` | `mom-child-matching-two-piece-swimsuit` | `20` |
| `6719774720097` | `matching-mommy-me-orange-print-swimsuit` | `10` |
| `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `6` |

Parent summary for the `20` out-of-stock expected rows:

| Parent product | Handle | Rows |
|---:|---|---:|
| `7230645239905` | `eternal-love-family-matching-t-shirts-colorful-heart-design` | `15` |
| `7537367679073` | `playful-graphic-family-matching-tops` | `3` |
| `7546613530721` | `golden-daisy-mommy-and-me-set` | `1` |
| `7537367384161` | `red-plaid-family-matching-tops` | `1` |

## Decision

The initial parent-outfit Shopping gate is still not fixed.

What is fixed:

- Label precedence is no longer the dominant blocker.
- Ready rows are stable at `4,390`.
- Ready-row labels and images have `0` mismatches.
- Product group catchalls remain clean with `0` bad included catchalls.
- All required Shopping campaigns remain paused.

What remains:

- `70` expected offer IDs exist in Ads but are blank/not-ready for the gate.
- `71` expected offer IDs are absent from the Ads Shopping-product surface.
- `20` expected offer IDs are out of stock and carry a non-campaign eligibility error.
- Strict live Merchant API `item_group_id` proof is still blocked by OAuth scope; spec-side `item_group_id` remains clean.

## Smallest Next Approval Packet

Use `GOOGLE_SHOPPING_PARENT_OUTFIT_REMAINING_ELIGIBILITY_REPAIR_OR_EXCLUSION_APPROVAL_PACKET_20260521.md` if the owner wants the next live repair/exclusion step.

No activation, campaign status change, budget, bid, product-group, conversion, billing, broad sync, product data rewrite, Shopify title/price/handle/body/SEO/inventory/publication change, or Merchant source reset is authorized by this diagnostic.
