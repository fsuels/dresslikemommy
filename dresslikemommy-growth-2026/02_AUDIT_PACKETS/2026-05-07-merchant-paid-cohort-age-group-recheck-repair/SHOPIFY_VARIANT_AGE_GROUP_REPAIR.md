# Shopify Variant Age Group Repair

Date: 2026-05-07  
Merchant account: `124884876`  
Shopify repair surface: ProductVariant metafield `mm-google-shopping.age_group`  
Scope: current paid cohort only

## Merchant Recheck

Fresh Merchant diagnostics were rechecked before any Shopify write.

Readback:

- Merchant diagnostics last updated: `12:43 PM May 7, 2026`
- `Missing age group` still visible.
- Product issues export rows: `37,033`
- Total `Missing age group` issue rows: `16,222`
- Unique item IDs with `Missing age group`: `4,588`
- Current paid cohort size: `780`
- Current paid cohort item IDs still showing `Missing age group` anywhere in the export: `777`
- Current paid cohort US/en/United States item IDs still showing `Missing age group`: `754`
- Current paid cohort US/en rows by traffic type:
  - Free listings: `754`
  - Shopping ads: `754`

Evidence:

- `merchant-diagnostics-2026-05-07-readback.png`
- `merchant-product-issues-2026-05-07-product_issues_2026-05-07_13-05-58.csv`
- `merchant-product-issues-paid-cohort-age-group-summary-2026-05-07.json`
- `merchant-product-issues-paid-us-en-missing-age-group-ids-2026-05-07.txt`

## Repair Path

The Shopify primary-feed path is variant-level:

- ProductVariant metafield definition exists:
  - namespace: `mm-google-shopping`
  - key: `age_group`
  - owner type: `PRODUCTVARIANT`
  - type: `single_line_text_field`

This matches the Merchant issue shape because Merchant reports the issue by item / variant ID, not just product ID.

## Live Shopify Write

Script:

`ops/scripts/repair_paid_cohort_variant_age_group.py`

Input:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-live-visual-qa-merchant-age-group-gate/paid_cohort_age_group_after_patch_rows.csv`

Dry-run before write:

- Target paid variants: `780`
- Planned updates: `780`
- Skipped rows: `0`
- Reason: `blank_age_group = 780`

Executed write:

- Attempted updates: `780`
- Applied batches: `32`
- Errors: `0`

Values applied:

- `adult`: `347`
- `kids`: `267`
- `toddler`: `164`
- `infant`: `2`

Post-write readback:

- Target paid variants: `780`
- Planned updates remaining: `0`
- Rows already correct: `780`
- Blank age-group values remaining: `0`

Independent sample readback:

- `41871113158753` / `Child 2 Years / Yellow` => `toddler`
- `41871520661601` / `Father XL / blue` => `adult`
- `41871506964577` / `Boy 4-5 Years / yellow` => `toddler`

## Immediate Merchant Check

Merchant still showed the sample product `Missing age group` immediately after the Shopify write. That is expected until the Google & YouTube app / Merchant Center refreshes the primary feed from Shopify.

Important interpretation:

- Shopify primary data repair: complete and read back.
- Merchant diagnostic clear: pending feed refresh.
- No additional Merchant upload was performed.

## Guardrails

No changes were made to:

- Shopify product title, body, status, publications, prices, inventory, tags, options, or images.
- Product-level custom labels / paid feed labels.
- Google Ads campaigns, budgets, bids, product groups, product scope, or conversion goals.
- Pinterest, pixels, GA4/GTM, or Merchant supplemental uploads.
- Non-`age_group` attributes.

## Next

Recheck Merchant diagnostics after the next Google & YouTube / Merchant feed refresh. The expected success condition is that current paid-cohort US/en `Missing age group` rows drop from `754` to `0`, or at minimum materially decrease with refreshed Shopify App API timestamps.

