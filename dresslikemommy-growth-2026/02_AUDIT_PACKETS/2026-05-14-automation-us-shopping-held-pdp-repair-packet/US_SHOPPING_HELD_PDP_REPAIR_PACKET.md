# US Shopping Held PDP Repair Packet

Generated: `2026-05-14T17:23:11+00:00`

## Scope

- Started from the held/review rows in the US Shopping public PDP fit preflight.
- Rows checked: `6` across `3` unique handles.
- Re-fetched each affected public PDP with browser-like and generic headers.
- No external account, Shopify Admin, Merchant, feed, Ads, product, campaign, budget, bid, status, or theme write occurred.

## Result

- `AUTH_EXPORT_ALLOWED_ONLY_IF_ITEM_LEVEL_IMPRESSIONS_PROVE_RELEVANCE`: `1` rows
- `EXCLUDE_FROM_AUTH_EXPORT_UNTIL_SOURCE_CLEAN`: `3` rows
- `EXCLUDE_FROM_AUTH_EXPORT_UNTIL_STALE_COPY_CLEAN`: `2` rows

## Row Actions

### `chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit`

- Search term: `family pictures outfits`
- Landing URL: `https://www.dresslikemommy.com/products/chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit?country=US`
- Public title: `Family Matching Sets - Ruffle Sleeve | Dress Like Mommy`
- Public H1: `Matching Sequin Lace Tulle Dresses with Crisscross ...`
- Preflight decision: `HOLD_PUBLIC_LANDING_STATUS_OR_SOURCE`
- Repair packet action: `EXCLUDE_FROM_AUTH_EXPORT_UNTIL_SOURCE_CLEAN`
- Reason: Public source still contains supplier/source domain hits.
- Next unblock action: Owner-approved Shopify/product-data or theme-safe repair, then public source readback shows zero supplier hits before any paid export/use.

### `chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit`

- Search term: `family same outfit`
- Landing URL: `https://www.dresslikemommy.com/products/chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit?country=US`
- Public title: `Family Matching Sets - Ruffle Sleeve | Dress Like Mommy`
- Public H1: `Matching Sequin Lace Tulle Dresses with Crisscross ...`
- Preflight decision: `HOLD_PUBLIC_LANDING_STATUS_OR_SOURCE`
- Repair packet action: `EXCLUDE_FROM_AUTH_EXPORT_UNTIL_SOURCE_CLEAN`
- Reason: Public source still contains supplier/source domain hits.
- Next unblock action: Owner-approved Shopify/product-data or theme-safe repair, then public source readback shows zero supplier hits before any paid export/use.

### `chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit`

- Search term: `mommy and me wedding guest dresses`
- Landing URL: `https://www.dresslikemommy.com/products/chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit?country=US`
- Public title: `Family Matching Sets - Ruffle Sleeve | Dress Like Mommy`
- Public H1: `Matching Sequin Lace Tulle Dresses with Crisscross ...`
- Preflight decision: `HOLD_PUBLIC_LANDING_STATUS_OR_SOURCE`
- Repair packet action: `EXCLUDE_FROM_AUTH_EXPORT_UNTIL_SOURCE_CLEAN`
- Reason: Public source still contains supplier/source domain hits.
- Next unblock action: Owner-approved Shopify/product-data or theme-safe repair, then public source readback shows zero supplier hits before any paid export/use.

### `dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set`

- Search term: `family pictures outfits`
- Landing URL: `https://www.dresslikemommy.com/products/dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set?country=US`
- Public title: `Family Matching Swim Trunks - Matching Style | Dress Like Mommy`
- Public H1: `Dynamic Duo" Father and Son Matching Swim Trunks - ...`
- Preflight decision: `HOLD_PUBLIC_LANDING_STATUS_OR_SOURCE`
- Repair packet action: `EXCLUDE_FROM_AUTH_EXPORT_UNTIL_STALE_COPY_CLEAN`
- Reason: Public source contains stale seasonal copy that mismatches current swim/family query intent.
- Next unblock action: Owner-approved narrow SEO/social/card metadata repair, or keep handle excluded from paid Shopping/Search traffic.

### `dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set`

- Search term: `family same outfit`
- Landing URL: `https://www.dresslikemommy.com/products/dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set?country=US`
- Public title: `Family Matching Swim Trunks - Matching Style | Dress Like Mommy`
- Public H1: `Dynamic Duo" Father and Son Matching Swim Trunks - ...`
- Preflight decision: `HOLD_PUBLIC_LANDING_STATUS_OR_SOURCE`
- Repair packet action: `EXCLUDE_FROM_AUTH_EXPORT_UNTIL_STALE_COPY_CLEAN`
- Reason: Public source contains stale seasonal copy that mismatches current swim/family query intent.
- Next unblock action: Owner-approved narrow SEO/social/card metadata repair, or keep handle excluded from paid Shopping/Search traffic.

### `green-and-white-matching-family-outfits-stylish-floral-print-family-set-for-parents-and-kids`

- Search term: `mommy and me wedding guest dresses`
- Landing URL: `https://www.dresslikemommy.com/products/green-and-white-matching-family-outfits-stylish-floral-print-family-set-for-parents-and-kids?country=US`
- Public title: `Family Matching Sets - Green Floral Print | Dress Like Mommy`
- Public H1: `Green and White Outfits Stylish Floral Print Family...`
- Preflight decision: `PUBLIC_LANDING_REVIEW_BEFORE_TITLE_PACKET`
- Repair packet action: `AUTH_EXPORT_ALLOWED_ONLY_IF_ITEM_LEVEL_IMPRESSIONS_PROVE_RELEVANCE`
- Reason: Public page is source-clean but weak for the observed query intent.
- Next unblock action: Run authenticated item export first; only consider title/feed repair if this exact item received meaningful impressions for the query.

## Approval Packet If Repair Is Desired

Use this only after deciding to repair the excluded public PDPs instead of keeping them out of paid traffic:

`APPROVE NARROW US SHOPPING HELD PDP PUBLIC-LANDING REPAIR ONLY: review and repair only the specific handles named in the 2026-05-14 US Shopping held PDP repair packet so public source has zero supplier/source-domain hits and no stale seasonal mismatch before paid export/use; no Google Ads, Merchant feed/source/product-scope/product-group, budget, bid, status, conversion-goal, Pinterest, billing, discount, price, inventory, or unrelated Shopify product changes; read back public source before and after.`

## Files

- Rows: `us_shopping_held_pdp_repair_rows.csv`
- Summary: `us_shopping_held_pdp_repair_summary.json`
