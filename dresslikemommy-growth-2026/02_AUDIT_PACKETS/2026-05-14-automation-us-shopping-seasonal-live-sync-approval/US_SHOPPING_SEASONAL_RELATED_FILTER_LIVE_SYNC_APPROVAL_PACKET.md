# US Shopping Seasonal Related-Product Filter Live Sync Approval Packet

Generated: `2026-05-14T18:17:30Z`

## Scope

- Surface: live Shopify theme snippet `snippets/buy-box-similar-styles.liquid`.
- Product/readback URL: `https://www.dresslikemommy.com/products/dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set?country=US`.
- Related problem: `PROB-2026-05-14-US-SHOPPING-QUERY-TITLE-FIT`.
- Existing local fix evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-seasonal-related-filter/US_SHOPPING_SEASONAL_RELATED_FILTER_LOCAL_FIX.md`.
- Candidate paid rows affected: the two held US Shopping swim-trunks rows from the held-PDP packet.

## Why This Packet Exists

The local theme fix is already implemented and Theme Check passed, but the fix is not live. The affected US Shopping rows must remain excluded from paid export/use until a scoped live theme sync is approved, pushed, and publicly read back with `0` stale seasonal hits.

This packet turns the blocker into one exact owner approval and one exact readback plan. It does not authorize Shopify Admin product data, Merchant, Google Ads, product/feed/title, bid, budget, status, or conversion changes.

## Exact Approval To Request

`APPROVE LIVE THEME SYNC FOR US SHOPPING SEASONAL RELATED-PRODUCT FILTER ONLY: push the local related-product recommendation filter in snippets/buy-box-similar-styles.liquid so non-seasonal PDPs do not render Christmas/Santa/Xmas related-product metadata; no Shopify Admin product data, Merchant, Google Ads, Pinterest, budget, bid, status, conversion, feed, product-scope, price, discount, or policy changes; read back the dynamic swim-trunks PDP public source before and after and keep it out of paid export/use unless stale seasonal hits are zero.`

## Execution Plan After Approval

1. Confirm the worktree still contains only the intended snippet diff plus current automation documentation updates.
2. Run a before-state public source readback for the swim-trunks PDP with both `Accept: text/html` and `Accept: */*`.
3. Push only `snippets/buy-box-similar-styles.liquid` to the active live Shopify theme.
4. Pull or source-read the live theme/snippet after push if the CLI path supports it.
5. Run the after-state public source readback for the same PDP and headers.
6. Keep the two swim-trunks rows excluded unless the after-state source has `0` hits for `Christmas`, `Santa`, and `Xmas` in related-card metadata contexts.

## Pass Criteria

- Live public PDP returns `200`.
- Supplier/source-domain hits remain `0` for `detail.1688.com`, `1688.com`, `alibaba.com`, and `aliexpress.com`.
- Stale seasonal hits are `0` for `Christmas`, `Santa`, and `Xmas` in rendered source.
- No live Shopify Admin product/vendor/source metadata edit occurs.
- No Google Ads, Merchant, Pinterest, GA4/GTM, billing, budget, bid, status, feed, product-scope, product-group, title/feed, conversion, price, discount, or policy write occurs.

## Rollback Boundary

If the after-state readback fails, revert only the live snippet to the prior committed version or re-push the pre-change snippet source. Do not compensate by editing Shopify product data, Merchant feeds, Google Ads product groups, or paid campaign settings in the same action.

## Current Status

`OWNER_APPROVAL_REQUIRED_FOR_SCOPED_LIVE_THEME_SYNC`

No live theme sync was performed in this automation run.
