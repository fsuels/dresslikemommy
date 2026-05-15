# US Active Product Proof Packet

Generated: 2026-05-15T04:06:53

## Scope

Public/read-only proof for US `GREEN` keyword-universe rows that are already routed to clean collection pages and are candidates for future US Search validation.

This packet does not authorize Google Ads, Shopify Admin, Merchant, Pinterest, feed, product, bid, budget, status, conversion, or theme writes.

## Results

- US `GREEN` keyword rows selected: `35`
- Collection routes checked: `5`
- Sampled public product pages: `51`
- Public active-product pass rows: `47`
- Held/review rows: `4`

Route CSV: `us_active_product_route_readback.csv`

Product sample CSV: `us_active_product_sample_rows.csv`

## Decision

The rerouted US keyword lane now has public active-product proof at the route/product sample level. This removes route-cleanliness-only ambiguity for future US Search prep, but the rows remain local-only until authenticated `$0.15` CPC/search feasibility, anti-cannibalization review, and a fresh green action row exist.

## Guardrails Preserved

- No Google Ads upload, apply, keyword, bid, budget, status, negative, or campaign write.
- No Shopify Admin product/vendor/source metadata edit.
- No Merchant, Pinterest, GA4/GTM, billing, feed, product-scope, product-group, conversion, credential, or destructive action.
- No Computer Use permission probing or account-access repair loop.

## Next Action

After the GB/CA/AU P0 CPC gate, build a small US validation packet only from these public-active route/product candidates and run authenticated Google Ads/Keyword Planner validation at max `$0.15` before any live Search use.
