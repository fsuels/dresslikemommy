# Live Visual QA + Merchant Age-Group Gate

Date: 2026-05-06

## Scope

- Visually reviewed the live storefront on desktop and mobile for:
  - Homepage
  - Product page: `red-resort-mommy-and-me-set`
  - Collection: `mother-daughter-matching-dresses`
- Moved to the next profit gate: Merchant Center age-group/feed issue review.
- Merchant/feed work in this packet is read-only/proposed only. No Merchant upload was made.

## Live Storefront Findings

### Found and fixed

1. The homepage/product/collection announcement claim could still show `FREE SHIPPING ON ALL ORDERS`, which conflicts with checkout-dependent shipping options.
2. The product page had duplicate matching-set guidance near the purchase controls.
3. `/collections/mother-daughter-matching-dresses` showed product count/pagination but no product cards because the visibility filter treated the collection as `Family Matching` instead of `Mommy and Me`.

### Theme changes pushed to live theme `134923321441`

- `sections/announcement-bar.liquid`
  - Normalizes translated and literal announcement text.
  - Replaces stale English `FREE SHIPPING ON ALL ORDERS | ... | SECURE CHECKOUT` with checkout-safe copy.
- `snippets/collection-grid-product-visible.liquid`
  - Classifies `mother-daughter-matching-dresses` as `Mommy and Me`.
  - Forces the collection expectation to `Mommy and Me` even if collection metafields are stale.
- `snippets/buy-buttons.liquid`
  - Removed the duplicate matching-set note from the buy-button area; kept the existing product-page matching guidance.
- Locale files for the tested paid-growth languages:
  - `locales/en.default.json`
  - `locales/es.json`
  - `locales/fr.json`
  - `locales/de.json`
  - `locales/da.json`

### Visual/readback evidence

Screenshots captured in the repo root:

- `dlm-live-home-desktop-hotfix-1440.png`
- `dlm-live-home-mobile-hotfix-390.png`
- `dlm-live-collection-desktop-hotfix-1440.png`
- `dlm-live-collection-mobile-hotfix-390.png`
- `dlm-live-pdp-mobile-hotfix-atc-390.png`

Readbacks:

- Homepage origin readback: live theme `134923321441`; banner shows `SHIPPING OPTIONS AT CHECKOUT | FAMILY MATCHING MADE EASY | SECURE CHECKOUT`.
- Product page origin readback: live theme `134923321441`; banner shows `SHIPPING OPTIONS AT CHECKOUT | FAMILY MATCHING MADE EASY | SECURE CHECKOUT`; duplicate `product-form__matching-set-clarity` is absent; existing `product-form__matching-set-hint` and `Build your matching set` remain.
- Collection readback: `id="product-grid"` and repeated `class="grid__item"` rows are present again.
- Cache note: one canonical collection URL cURL briefly returned an older cached announcement line after the push, while cache-bypassed/query-variant reads returned the fixed origin output. A later canonical retry returned the fixed copy and visible product cards.

## Merchant Age-Group Gate

### Inputs

- Live Shopify product export, read-only:
  - `shopify_products_readonly.json`
  - `798` products
- Current paid Shopping cohort:
  - `../2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv`
  - `780` paid rows

### Before local validator fix

- Full live export validator:
  - `19,531` variant items
  - `0` required-field errors
  - `13,955` high-confidence age-group supplemental rows
- Paid cohort:
  - `764 / 780` high-confidence age groups
  - `16 / 780` missing high-confidence age groups

The missing paid rows were not random. They were size formats the local age-group parser did not understand:

- `Child 4T`
- `Child 5-6T`
- `Child 2-3T`, `3-4T`, `4-5T`, `6-8T`, `8-10T`, `10-12T`
- `Baby 0-6 Months`
- `Baby 6-12 Months`

### Local validator improvement

- Updated `scripts/validateFeed/ageGroup.js` to classify:
  - Month ranges like `0-6 Months` and `6-12 Months`
  - Toddler/kids `T` sizes like `4T`, `5-6T`, and `10-12T`
- Added lightweight regression coverage:
  - `ops/tests/test_validate_feed_age_group.mjs`

### After local validator fix

- Full live export validator:
  - `19,531` variant items
  - `0` required-field errors
  - `18,493` high-confidence age-group supplemental rows
- Paid cohort:
  - `780 / 780` high-confidence age groups
  - `0 / 780` missing high-confidence age groups
- Newly resolved paid rows:
  - `16`
  - `7` toddler
  - `7` kids
  - `2` infant

### Proposed Merchant file, not uploaded

- `paid_cohort_age_group_supplemental_PROPOSED_DO_NOT_UPLOAD.tsv`
  - Header: `id	age_group`
  - `780` paid rows
  - Uses live Merchant item IDs like `shopify_US_<product_id>_<variant_id>`
- Review CSV:
  - `paid_cohort_age_group_supplemental_PROPOSED_DO_NOT_UPLOAD.csv`
- Newly resolved audit rows:
  - `paid_cohort_age_group_newly_resolved_rows.csv`

## Verification

- `shopify theme check --path .`
  - Passed: `261 files inspected with no offenses found`
- `git diff --check` on touched files
  - Passed
- `node --check scripts/validateFeed/ageGroup.js`
  - Passed
- `node ops/tests/test_validate_feed_age_group.mjs`
  - Passed
- Feed validator after parser fix
  - Passed with `0` required-field errors
- Paid cohort comparison after parser fix
  - Passed with `780 / 780` high-confidence age groups

## Guardrails Kept

- No Shopify product edits.
- No Merchant Center upload.
- No feed sync/upload.
- No Google Ads edits.
- No Pinterest edits.
- No pixel/tag changes.
- No campaign status, budget, bid, product-scope, product-group, feed-label, or conversion-goal changes.

## Next Approval Gate

Recommended next exact approval if the owner wants to repair the Merchant age-group issue live:

`APPROVE MERCHANT AGE_GROUP SUPPLEMENTAL UPLOAD FOR CURRENT PAID COHORT ONLY: UPLOAD THE PROPOSED 780-ROW AGE_GROUP TSV USING EXISTING MERCHANT ITEM IDS; NO PRODUCT, SHOPIFY, FEED LABEL, PRODUCT SCOPE, PRODUCT GROUP, CAMPAIGN, BUDGET, BID, STATUS, OR CONVERSION-GOAL CHANGES.`
