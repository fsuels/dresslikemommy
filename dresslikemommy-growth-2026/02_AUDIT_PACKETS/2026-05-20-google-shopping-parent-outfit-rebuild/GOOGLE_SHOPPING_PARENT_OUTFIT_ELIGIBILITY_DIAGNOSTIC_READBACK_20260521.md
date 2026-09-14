# Google Shopping Parent-Outfit Eligibility Diagnostic Readback

Date: 2026-05-21

Mode: read-only diagnostic. No Merchant feed/source upload, source reset, broad sync, Shopify product/publication edit, Google & YouTube setting edit, Google Ads campaign/product-group/budget/bid/status/conversion/billing change, or activation occurred.

## Scope

- Exact expected parent-outfit offer IDs checked: `4,531`.
- Latest gate evidence used: `google_shopping_parent_outfit_merchant_feed_gate_20260521T095240Z.json`.
- Expected-offer input: `google_shopping_parent_outfit_expected_offer_ids_for_eligibility_diagnostic_20260521.csv`.
- Diagnostic output folder: `eligibility_diagnostic_20260521/`.

## Current Gate State

- Gate passed: `false`.
- Expected included rows: `4,531`.
- Live ready-label rows: `4,390`.
- Missing expected rows: `141`.
- Label mismatches: `0`.
- Image mismatches: `0`.
- Missing live images: `0`.
- Bad catchall units: `0`.
- All V2 Shopping campaigns remained paused.
- Old `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` remained paused.

## What The Eligibility Diagnostic Proved

The `NOT_ELIGIBLE` status on the live labeled rows is not, by itself, proof of bad labels or bad images. Google Ads reports `not_eligible_in_any_campaign` / `No campaigns advertising this product` for every found expected item. That is consistent with the required safety state: all parent-outfit V2 Shopping campaigns remain paused.

The remaining product-scope blockers are:

- `71` expected offer IDs are absent from the Google Ads Shopping-product surface.
- `20` unique expected offer IDs have the non-campaign error `not_eligible_out_of_stock`.
- Merchant API and Content API item/status diagnostics still cannot provide strict Merchant-side `item_group_id` or item-status proof because the current local Google token lacks Merchant/Content API scopes.

## Google Ads Surface Summary

- Expected rows: `4,531`.
- Google Ads surface rows found: `8,852`.
- Unique expected item IDs found on the Ads surface: `4,460`.
- Expected item IDs absent from the Ads surface: `71`.
- Unique status distribution: `4,460` `NOT_ELIGIBLE`.
- Unique availability distribution: `4,440` `IN_STOCK`, `20` `OUT_OF_STOCK`.
- Unique issue code counts:
  - `not_eligible_in_any_campaign`: `4,460`.
  - `missing_item_attribute_for_product_type`: `4,580`.
  - `not_eligible_out_of_stock`: `20`.

Interpretation:

- `not_eligible_in_any_campaign` is expected while all Shopping V2 campaigns stay paused.
- `missing_item_attribute_for_product_type` is warning-level in this Ads diagnostic and is not the current counts/images/no-catchall blocker.
- `not_eligible_out_of_stock` is a real non-campaign error for `20` offer IDs and should be handled before any strict eligibility gate can pass.

## Absent Offer IDs

These `71` offer IDs are expected by the parent-outfit spec but absent from the Google Ads Shopping-product surface:

| Parent product ID | Handle | Lane | Subgroup | Absent offer IDs |
|---|---|---|---|---:|
| `7562834215009` | `white-crochet-mommy-and-me-set` | `mommy_and_me` | `sets` | `35` |
| `6718945034337` | `mom-child-matching-two-piece-swimsuit` | `mommy_and_me` | `swimwear` | `20` |
| `6719774720097` | `matching-mommy-me-orange-print-swimsuit` | `mommy_and_me` | `swimwear` | `10` |
| `7227254276193` | `mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter` | `mommy_and_me` | `dresses` | `6` |

Existing Shopify readback evidence for these four products showed they are `ACTIVE`, online-store present, Google & YouTube published, and their missing expected variants are present in Shopify. That points away from a Shopify variant-existence problem and toward Merchant/Google & YouTube indexing or Ads-surface availability.

## Out-Of-Stock Offer IDs

These `20` offer IDs are found on the Ads surface but have `not_eligible_out_of_stock`:

| Parent product ID | Handle | Lane | Subgroup | Out-of-stock offer IDs |
|---|---|---|---|---:|
| `7230645239905` | `eternal-love-family-matching-t-shirts-colorful-heart-design` | `family_matching` | `tops_shirts` | `15` |
| `7537367679073` | `playful-graphic-family-matching-tops` | `family_matching` | `tops_shirts` | `3` |
| `7537367384161` | `red-plaid-family-matching-tops` | `family_matching` | `tops_shirts` | `1` |
| `7546613530721` | `golden-daisy-mommy-and-me-set` | `mommy_and_me` | `tops_shirts` | `1` |

## Evidence Files

- `eligibility_diagnostic_20260521/google_ads_expected_offer_issue_diagnostic_summary_20260521.json`
- `eligibility_diagnostic_20260521/google_ads_expected_offer_issue_diagnostic_unique_20260521.csv`
- `eligibility_diagnostic_20260521/google_ads_expected_offer_absent_from_ads_surface_20260521.csv`
- `eligibility_diagnostic_20260521/google_ads_expected_offer_parent_presence_summary_20260521.csv`
- `eligibility_diagnostic_20260521/merchant_center_api_diagnostics_summary.json`
- `google_shopping_parent_outfit_expected_offer_ids_for_eligibility_diagnostic_20260521.csv`
- `google_shopping_parent_outfit_merchant_feed_gate_20260521T095240Z.json`

## Decision

Do not repeat the same TSV upload, Shopify publication resync, or attribute repair. The gate is still blocked, but the diagnostic changed the blocker shape:

1. The paused-campaign `not_eligible_in_any_campaign` status is expected under the current no-spend safety state.
2. The exact live product-scope cleanup is now limited to:
   - `71` absent offer IDs across four Mommy & Me parents;
   - `20` out-of-stock offer IDs across four parents.
3. Any next repair/exclusion must be separately approved and must still keep all Shopping campaigns paused.

