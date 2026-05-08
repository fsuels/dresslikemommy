# Merchant Dedicated Age Group Repair

Generated: 2026-05-08

## Problem

Merchant Center still has a paid-cohort `Missing age group` blocker:

- Latest exact completed count: `623` paid-cohort US/en item IDs.
- Sample item: `shopify_US_7227254276193_41871113158753`.
- Sample source: `10627623003` / `Shopify App API`, US/en timestamp `2026-05-07T14:14:02+00:00`.

Shopify is not the remaining data problem:

- ProductVariant `mm-google-shopping.age_group` has already been set/read back for all `780` paid-cohort variants.
- The sample Shopify variant has `age_group=toddler`.

Merchant product-detail RPC still shows the processed US/en item lacks effective `n:age_group`, while paid labels are visible. That means the existing supplemental/source path is not applying `age_group` into processed product data, even though labels are present.

## Fix Packet

Prepared a new dedicated supplemental upload that contains only:

- `id`
- `age_group`

Files:

- `upload_paid_cohort_age_group_only.txt`
- `upload_paid_cohort_age_group_only.csv`
- `age_group_only_upload_review.csv`
- `summary.json`

Rows:

- Upload rows: `780`
- Blocked rows: `0`
- `adult`: `347`
- `kids`: `267`
- `toddler`: `164`
- `infant`: `2`

## Guardrails

- No `custom_label_0..4` columns, so paid targeting labels are not overwritten.
- No Shopify product edits.
- No Google & YouTube publication toggle or sync click.
- No existing supplemental source deletion/edit.
- No local inventory feeds, store-stock claims, or pickup claims.
- No Google Ads/Pinterest/GA4/budget/bid/status/product-scope/product-group/feed-label/conversion-goal changes.

## Verification Gates

After upload/source creation, verify:

1. The new supplemental source is linked to `Shopify App API (US, English)`.
2. Source processing accepts `780` rows and recognizes `age_group`.
3. Sample product detail no longer lists `Missing age group`.
4. Sample processed product data contains effective `n:age_group`.
5. Sample paid labels still read `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready`.
6. Next diagnostics/product-issues export count drops from `623`.

## Rollback

If the new source causes unexpected behavior, delete only the newly created dedicated supplemental source. Existing `supplemental_feed_pilot.txt` remains untouched.
