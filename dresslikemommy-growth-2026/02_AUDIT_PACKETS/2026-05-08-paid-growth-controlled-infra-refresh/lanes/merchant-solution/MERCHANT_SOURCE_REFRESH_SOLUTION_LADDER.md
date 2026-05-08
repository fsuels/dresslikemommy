# Merchant Source Refresh Solution Ladder

Date: 2026-05-08
Mode: local solution plan only, no Merchant/Shopify account write

## Decision

`MERCHANT_FIX_PATH_IS_SOURCE_REFRESH_NOT_MORE_PRODUCT_DATA`

The current Merchant blocker is not unsolved Shopify product data. The Shopify-side paid cohort has already been fixed and verified: `780` target variants, `0` planned age_group updates, `780 already_correct`. The sample variant's `mm-google-shopping.age_group` is correct in Shopify, but Merchant still shows the US/en `Shopify App API` row timestamp `2026-05-07T14:14:02+00:00`, older than the Shopify repair.

The solution is to make the Google & YouTube / Merchant API source ingest the corrected data, not to keep editing products.

## Root Cause

Evidence points to stale source propagation:

- Shopify source data is fixed.
- Merchant exact issue count improved from `754` to `623`, proving some processing happened.
- The sample source timestamp did not advance beyond the Shopify write timestamp.
- The US source still shows `Needs update` evidence in prior UI captures.
- Local API diagnostics are blocked by insufficient OAuth scopes, making browser exports brittle.

## Ranked Solution Path

### 1. Read Back First

Run a just-in-time readback before any live action:

- Merchant account `124884876`.
- Sample item `shopify_US_7227254276193_41871113158753`.
- Current product-issues export count for paid-cohort US/en `Missing age group`.
- Shopify Google & YouTube product publication state for sample product.
- Visible source/app status and exact label of any official refresh/sync control.

This is not the endpoint. It is the preflight for the source-refresh action.

### 2. Execute One Official Source Refresh / App Sync If Visible And Approved

Smallest live fix candidate:

- Use the Shopify Google & YouTube app/channel or Merchant source UI.
- Click only a clearly labeled official refresh/sync/update-products control.
- Do not click upload, add product source, found-by-Google add products, local inventory, Fix, View fix, broad product publication toggles, or product-data editors.

Expected result:

- Sample source timestamp advances beyond `2026-05-07T17:12:10Z`.
- Paid-cohort US/en `Missing age group` drops materially from `623`, ideally to `0`, after processing.

### 3. Repair Read-Only API Credentials

Parallel operator fix:

- The local API path is blocked by `403 PERMISSION_DENIED`.
- Regenerate/load credentials with read-only Merchant/Product Status scopes so the next agent can query product/source/issue state directly instead of relying on fragile browser downloads.
- Credentials must stay outside the repo.

This is a solution because it removes the current instrumentation blocker and lets the source-refresh result be measured precisely.

### 4. Stop Repeating The Product Toggle

The prior approved single-product Google & YouTube unpublish/republish probe restored publication but did not advance the Merchant timestamp in the immediate readback. Repeating that blindly adds product-publication risk without evidence that it fixes the source pipeline.

Only repeat any publication toggle if the owner explicitly approves that exact action again after the official refresh path is unavailable or fails.

## Exact Approval Gate For The Live Fix

`APPROVE GOOGLE & YOUTUBE US FEED SOURCE REFRESH ACTION: READ BACK SHOPIFY GOOGLE & YOUTUBE CHANNEL SYNC STATUS, MERCHANT US SHOPIFY APP API SOURCE DETAILS, SAMPLE ITEM TIMESTAMP, AND PAID-COHORT MISSING AGE_GROUP COUNT FIRST; THEN CLICK ONLY ONE CLEARLY LABELED OFFICIAL GOOGLE & YOUTUBE OR MERCHANT SOURCE REFRESH/SYNC/UPDATE-PRODUCTS CONTROL IF AVAILABLE; NO PRODUCT DATA EDITS, NO FEED LABEL CHANGES, NO SUPPLEMENTAL UPLOADS, NO LOCAL INVENTORY FEEDS OR CLAIMS, NO ADS, NO CAMPAIGNS, NO BUDGETS, NO BIDS, NO PRODUCT SCOPE, NO PRODUCT GROUP, NO PIXEL, NO CONVERSION-GOAL CHANGES, AND NO PRODUCT PUBLICATION TOGGLE; READ BACK AFTER.`

## Success Criteria

- Sample source timestamp advances beyond the Shopify age_group repair timestamp.
- Paid-cohort US/en `Missing age group` count drops from `623`.
- No paid labels are lost: `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`.
- No product count/product scope/feed label/product group/campaign change occurs.
- `Missing local inventory data` remains ignored as a non-fix target for this dropshipping business.

## Stop Rules

Stop immediately if the UI shows:

- Login, CAPTCHA, permission, billing, or account-switch prompt.
- Upload/feed/source replacement flow.
- Local inventory, pickup, physical store, or stock-location flow.
- Product editor or publication state change.
- Any control whose label does not clearly mean refresh/sync/update existing product source.

## Post-Action Watch

After an approved official refresh/sync:

1. Recheck after 30 minutes.
2. Recheck after 2 hours.
3. Recheck after the next Merchant visible source update time.

If no movement after the next source update, escalate as a Google & YouTube app / Merchant source pipeline issue. Do not continue making product-data edits that have already read back correct in Shopify.
