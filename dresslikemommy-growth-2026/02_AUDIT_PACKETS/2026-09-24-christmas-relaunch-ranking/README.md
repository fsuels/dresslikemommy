# Archived Christmas products ranked by past sales — read-only readback 2026-09-24

State: `LIVE_VERIFIED` Shopify Admin reads on 2026-09-24. No Shopify, Google or Merchant write happened.

## Method
- Catalog: Admin GraphQL `products(query:"status:archived OR status:draft")` = 577 products. Christmas = title/handle/type match on christmas, xmas, santa, reindeer, grinch, elf, gnome, snowman, fair isle, nordic, "let it snow", merry, "ho ho" and similar. 91 matched. Two were excluded as not Christmas: `3880452161633` Stripe Holiday Dress (23% of sales Oct–Jan) and `748259115105` antler floral dress (0% Oct–Jan). They stay in the CSV with a `note`. Result: **89 archived Christmas products, 0 drafts, 0 active.**
- Sales: a bulk export of every order line since 2017 (31,951 objects, 8,572 orders), excluding cancelled and test orders. `revenue` is line revenue after line-level discounts and before refunds. Season columns run Jul–Jun, so `rev_2025_26` is the 2025 Christmas season.
- Cross-check: lifetime totals match ShopifyQL `net_sales` exactly for `7230717886561` (933.29), `4814804418657` (922.41) and `4360391721057` (832.59). `6677481652321` is 762.03 here vs 759.28 net; the gap is a refund.
- `in_christmas_pajamas_collection`: product has the tag `Christmas Pajamas`, which is the smart-collection rule of `christmas-pajamas` (41 products, all archived). The Oct 15–Dec 25 homepage/menu gate (commit 94d538f) shows nothing until that collection has storefront products.

## Totals
- 41 of the 89 have sales: $8,436.44 lifetime. 27 of them sold in the 2024 or 2025 season. 48 never sold.
- Lines whose product was deleted (not archived) also carry Christmas titles: 538 units and $11,365.69 across 34 titles. They can't be reactivated and would need to be listed again.
