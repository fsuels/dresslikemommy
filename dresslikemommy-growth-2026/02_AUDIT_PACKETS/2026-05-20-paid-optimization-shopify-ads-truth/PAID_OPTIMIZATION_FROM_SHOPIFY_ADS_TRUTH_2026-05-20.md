# Paid Optimization From Shopify + Google Ads Truth

Date: 2026-05-20

Window: 2026-04-22 to 2026-05-19

Mode: read-only. No Google Ads, Shopify, Merchant, GA4, GTM, billing, campaign, budget, bid, status, keyword, negative, product group, conversion-goal, feed, or product write occurred.

## Decision

GA4 channel revenue and the GA4-derived "0 purchases after checkout" funnel are not trusted optimization inputs until GA4 purchase parity is repaired to about +/-5% against Shopify paid-order truth.

Optimize Google paid traffic from:

- Shopify paid/non-cancelled orders and order line items.
- Google Ads cost, click, campaign, search-term, keyword, and Shopping product readbacks.
- Product-level Shopify sold-item truth joined to Google Ads Shopping clicked item IDs.

## Readback Summary

Shopify paid-order truth:

- `23` paid/non-cancelled Shopify orders.
- `$1,596.06` Shopify revenue.
- Shopify-classified `google_paid_candidate`: `0` orders / `$0.00`.

GA4 parity state:

- GA4 extracted `18` transaction IDs / `$1,113.53`.
- GA4 under-counts Shopify truth by `21.74%` on order count and `30.23%` on revenue.
- GA4 is outside the repo target of about `+/-5%`.

Google Ads readback:

- Apr 22-May 19 total: `184` clicks / `$33.12` cost.
- Today, May 20: `0` clicks / `$0.00` cost.
- Search terms with clicks were brand-only: `dress like mommy` and `dresslikemommy`.
- Standard Shopping campaign `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` was the main paid-cost source: `158` clicks / `$30.62` cost / `0` Ads conversions and `0` Shopify Google-paid orders.

## Shopping Product Join

The product-level join compared Google Ads clicked Shopping item IDs against Shopify paid order line items for the same window.

Results:

| Classification | Rows | Impressions | Clicks | Cost | Shopify sold qty | Shopify sold revenue |
|---|---:|---:|---:|---:|---:|---:|
| Clicked item/product had no matching Shopify sale | 44 | 5,482 | 154 | $29.79 | 0 | $0.00 |
| Clicked product sold, but a different variant sold | 3 | 94 | 3 | $0.63 | 9 | $140.91 |
| Clicked exact variant sold | 1 | 26 | 1 | $0.20 | 1 | $14.99 |

Interpretation:

- Standard Shopping is spending mostly on variants/products that did not sell in Shopify during the window.
- There is not enough proof to scale the current Shopping setup.
- The only exact clicked-variant sale was `Daddy and Me Swim Trunks - Blue Yellow`, 1 click / `$0.20` cost / `$14.99` sold revenue.
- The `Family Matching Swimsuits - Long Sleeve` product had 3 paid clicks across variants and one Shopify order for different variants, so it is a weak product-level signal, not a clean variant-level winner.
- `65` sold variants had no matching Ads click in the clicked Shopping rows, so the next test should start from Shopify-sold products, not from the old clicked-but-unsold Shopping distribution.

## Campaign Actions

These are decision recommendations only; they are not live writes.

| Surface | Decision | Why | Valid next step |
|---|---|---|---|
| Standard Shopping `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` | Hold paused / do not scale current scope | `$30.62` cost, `158` clicks, `0` Shopify Google-paid orders, and `154/158` clicks landed on no-sale item/product rows | Build a narrower Shopify-sold-product retest packet or product-group repair; owner approval required before any Shopping scope/status/bid/budget write |
| Brand Search `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` | Keep capped; do not scale | `$2.50` cost, `26` clicks, brand-only queries, `0` Shopify Google-paid orders; small defensive spend, not growth proof | Monitor from Shopify order truth; keep exact-brand only and capped unless evidence changes |
| Enabled zero-spend Search tests | Serving repair or hold, not budget/bid escalation | Window readback shows no material clicks/cost; May 20 readback shows `0` cost / `0` clicks | Diagnose serving and auction entry only for high-intent rows; do not raise from GA4 channel revenue |
| GA4 channel reports | Exclude from optimization truth | Purchase parity is off by `21.74%` orders / `30.23%` revenue | Repair GA4 parity separately, then reintroduce GA4 if within about `+/-5%` |

## Next Best Action

Create a small, approval-gated Google paid retest from Shopify order truth:

1. Use the Shopify-sold variants/products that did not receive paid Shopping clicks as the candidate pool.
2. Prioritize products with real Shopify revenue, clean public landing pages, active availability, correct market/currency, and clear parent/child variant merchandising.
3. Exclude the clicked/no-sale Shopping rows from any scaled scope unless a landing, title, image, stock, sizing, or price issue is repaired and verified.
4. Keep the test capped and read it from Shopify paid orders plus Google Ads cost/clicks until GA4 parity is fixed.

## Evidence Files

- `paid_optimization_summary.json`
- `paid_optimization_product_join_summary.json`
- `paid_optimization_campaign_decisions_2026-04-22_to_2026-05-19.csv`
- `google_ads_campaigns_2026-04-22_to_2026-05-19.csv`
- `google_ads_campaigns_2026-05-20_today.csv`
- `google_ads_search_terms_2026-04-22_to_2026-05-19_top200.csv`
- `google_ads_shopping_products_2026-04-22_to_2026-05-19_clicked.csv`
- `shopify_paid_orders_truth_classified_2026-04-22_to_2026-05-19.csv`
- `shopify_paid_order_line_items_2026-04-22_to_2026-05-19.csv`
- `shopping_clicks_vs_shopify_sold_items_2026-04-22_to_2026-05-19.csv`
- `shopify_sold_items_not_clicked_in_ads_2026-04-22_to_2026-05-19.csv`
