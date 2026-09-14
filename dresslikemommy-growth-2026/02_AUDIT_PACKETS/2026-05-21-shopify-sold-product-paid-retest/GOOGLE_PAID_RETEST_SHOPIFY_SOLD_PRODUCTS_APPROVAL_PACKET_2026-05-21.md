# Google Paid Retest Approval Packet - Shopify-Sold Products

Date: 2026-05-21

Mode: local approval packet only. No live Google Ads, Shopify, Merchant, GA4, GTM, billing, campaign, budget, bid, status, keyword, negative, product group, feed, product, or conversion-goal write occurred.

## Why This Exists

GA4 channel revenue remains excluded from paid optimization until purchase parity is repaired to about +/-5% against Shopify paid-order truth. The retest therefore starts from Shopify-sold products and Google Ads cost/click readbacks, not from GA4 channel revenue and not from the old clicked/no-sale Shopping distribution.

The prior paid audit showed current Standard Shopping spent mostly on item/product rows that did not sell. This packet flips the source: start from products that actually sold in Shopify and had no matching paid Shopping click in the audit window, then require clean live landing proof before any ad retest.

## Recommended Test Structure

- Create a new paused-ready Google Shopping retest, or a paused ad-group/product-group structure under an existing safe test shell, using only the item IDs in `google_ads_retest_candidate_item_scope_2026-05-21.csv`.
- Include exact sold variant item IDs only; exclude all other products/items from this retest scope.
- Manual/ceiling-controlled economics: max CPC `$0.15`, shared daily test cap `$5.00`, 72-hour initial window or `$15.00` spend, whichever comes first.
- Do not use Performance Max, broad Shopping catchalls, Search Partners, Display, AI Max, remarketing, GA4 channel revenue, or the old clicked/no-sale Shopping rows.
- Read results from Shopify paid orders plus Google Ads cost/clicks. GA4 remains diagnostic only until parity is fixed.

## Economics Gate

- Target ROAS: `650%`.
- Max CPC: `$0.15`.
- Required revenue per click at 650% ROAS and $0.15 CPC: about `$0.975`.
- With candidate prices around `$28-$35`, the retest needs roughly one order every `30-36` clicks before fulfillment/product margin review.
- If CPC or product economics cannot stay inside this envelope, do not launch or keep spending.

## Candidate Scope

| Rank | Product | Sold qty | Sold revenue | Min available price | Item IDs |
|---:|---|---:|---:|---:|---|
| 1 | [Lavender Mommy and Me Floral Applique Sleeveless Ruffle Dress](https://dresslikemommy.com/products/lavender-mommy-and-me-floral-applique-sleeveless-ruffle-dress) | 3 | $94.97 | $29.99 | 2 exact sold variant IDs |
| 2 | [Green Tropical Leaf Daddy and Me Matching Swim Shorts for Pool Days](https://dresslikemommy.com/products/green-tropical-leaf-daddy-and-me-matching-swim-shorts-for-pool-days) | 5 | $78.42 | $21.99 | 5 exact sold variant IDs |
| 3 | [Ivory Dot Mommy and Me Dresses - Puff Sleeve Sundress](https://dresslikemommy.com/products/ivory-dot-mommy-and-me-dresses) | 2 | $68.12 | $31.99 | 2 exact sold variant IDs |
| 4 | [Pink Lace Garden Mommy and Me Dresses - Puff Sleeve Sundress](https://dresslikemommy.com/products/pink-lace-garden-mommy-and-me-dresses) | 2 | $66.98 | $31.99 | 2 exact sold variant IDs |
| 5 | [Polka Dot Mommy and Me Dresses - Puff Sleeve Sundress](https://dresslikemommy.com/products/polka-dot-mommy-and-me-dresses) | 2 | $66.98 | $31.99 | 2 exact sold variant IDs |
| 6 | [Blue Tie-Dye Butterfly Mommy and Me Dresses — Tiered Sleeveless Dress](https://dresslikemommy.com/products/blue-tie-dye-butterfly-mommy-and-me-dresses) | 2 | $61.98 | $27.99 | 2 exact sold variant IDs |
| 7 | [Powder Blue Mommy and Me Set — Flutter Top & Eyelet Pants](https://dresslikemommy.com/products/powder-blue-mommy-and-me-set) | 2 | $60.98 | $31.99 | 2 exact sold variant IDs |
| 8 | [Ivory Cascade Mommy and Me Set - Sleeveless Top & Maxi Skirt](https://dresslikemommy.com/products/ivory-cascade-mommy-and-me-set) | 2 | $60.98 | $28.99 | 2 exact sold variant IDs |

Full item-ID scope is in `google_ads_retest_candidate_item_scope_2026-05-21.csv`.

## Landing Proof Gate

Top 8 candidates passed all of these checks from live public readbacks on 2026-05-21:

- Product page HTTP `200`.
- `/products/{handle}.js` HTTP `200`.
- Product JSON available.
- At least one sold variant is currently available.
- Add-to-cart or size-selection flow detected.
- No supplier/source host hit in the scanned page/product JSON (`1688`, Alibaba/AliExpress/Alicdn, Taobao/Tmall, DHGate, Made-in-China, Temu, Shein, CJ/Yiwu patterns).
- Current public title does not contain literal ellipses or old `| DLM` suffix.

Held rows are preserved in `shopify_sold_product_retest_candidates_2026-05-21.csv`. Main hold reasons: old/404 handles, unavailable sold variants, supplier/source-host hits, and old truncated/DLM titles.

## Stop Rules

- Stop if Shopify Google-paid orders remain 0 after $15 spend.
- Stop any product/ad group if average CPC exceeds $0.15 after 20 clicks.
- Stop any row if live QA finds checkout/PDP/source issues.
- Do not optimize from GA4 channel revenue until parity returns to +/-5%.
- Stop if Shopify checkout/PDP QA finds mobile friction before spend produces a sale.
- Stop before any budget, bid, status, product group, feed, product, conversion, or billing change outside this exact scope.

## Exact Owner Approval Phrase

To authorize only the paused-ready setup/readback, use this exact phrase:

`I approve creating the paused-ready Google Shopping Shopify-sold-products retest from the 2026-05-21 packet only: exact item IDs in google_ads_retest_candidate_item_scope_2026-05-21.csv, max CPC $0.15, daily cap $5, no PMax, no broad catchall, no Search Partners, no Display, no GA4 optimization, no Merchant/Shopify product/feed changes, and stop for readback before enabling spend.`

A separate fresh approval is still required to enable spend after paused setup readback.

## Files

- `shopify_sold_product_retest_candidates_2026-05-21.csv`
- `google_ads_retest_candidate_item_scope_2026-05-21.csv`
- `shopify_sold_product_retest_plan_summary.json`
