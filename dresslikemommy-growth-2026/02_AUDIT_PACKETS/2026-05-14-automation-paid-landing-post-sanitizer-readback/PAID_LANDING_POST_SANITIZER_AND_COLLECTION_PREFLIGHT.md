# Paid Landing Post-Sanitizer And Collection Preflight

Timestamp: 2026-05-14 11:19 EDT

Scope: public/read-only storefront source readback for active GB/CA/AU Search final URLs and the top GB/CA/AU keyword-universe collection routes. No Shopify, Google Ads, Merchant, Pinterest, GA4/GTM, billing, feed, product, campaign, budget, bid, status, or conversion write occurred.

## Result

The active GB/CA/AU exact Search PDP final URL now passes a public source readback for the supplier/source sanitizer gate.

Checked URL:

- `/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=GB`
- `/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=CA`
- `/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=AU`

Two header/cache variants were checked:

- `Accept: text/html,application/xhtml+xml`
- `Accept: */*` with cache-busting query

Both variants returned `200` for all three markets and showed:

- `detail.1688.com`: `0`
- `1688.com`: `0`
- `alibaba.com`: `0`
- `aliexpress.com`: `0`
- `data-analytics-vendor="https://`: `0`
- `data-item-brand="https://`: `0`
- `Christmas`: `0`
- `local inventory`: `0`
- `warehouse`: `0`
- `retail store`: `0`
- `Ships to`: present
- `priceCurrency`: present

## Collection Route Preflight

Because `keyword_universe.csv` routes the next GB/CA/AU long-tail candidates to collection pages, I checked the top collection route set before any live keyword action:

| Route | GB | CA | AU | Decision |
|---|---|---|---|---|
| `/collections/mommy-and-me` | clean | clean | clean | Safe for next CPC/auction validation only; not upload approval |
| `/collections/family-matching` | clean | clean | clean | Safe for next CPC/auction validation only; not upload approval |
| `/collections/pajamas` | clean | clean | clean | Safe for next CPC/auction validation only; not upload approval |
| `/collections/swimsuits` | supplier leak | supplier leak | supplier leak | Block from live Search rows until fixed/excluded |
| `/collections/matching-dresses` | supplier leak | supplier leak | supplier leak | Block from live Search rows until fixed/excluded |
| `/collections/vacation` | `404` | `404` | `404` | Block from live Search rows until rerouted/fixed |
| `/collections/daddy-and-me` | Christmas analytics pattern hits | Christmas analytics pattern hits | Christmas analytics pattern hits | Hold from live Search rows until metadata/product-fit reviewed |

The `/collections/matching-dresses` and `/collections/swimsuits` leaks are not the prior card attribute leak. Public source showed Shopify product JSON with a raw supplier URL:

```text
"vendor":"https:\/\/detail.1688.com\/offer\/602107180663.html"
```

The `/collections/daddy-and-me` hits came from `data-analytics-pattern="Christmas"` on swim-trunks product cards, so this needs a product-fit/metadata review before using the Daddy-and-Me holiday-shirt keyword rows.

## Keyword Action Implication

Active GB/CA/AU paid Search expansion is no longer blocked by the current PDP final URL supplier/source sanitizer gate.

It is still blocked by the hard `$0.15` CPC validation gate and by collection-route cleanliness for any row that does not use a currently clean route.

Allowed next validation set, read-only/authenticated Google Ads or Keyword Planner only:

- GB/CA/AU rows routed to `/collections/mommy-and-me`
- GB/CA/AU rows routed to `/collections/family-matching`
- GB/CA/AU rows routed to `/collections/pajamas`

Held rows until repair/reroute:

- Rows routed to `/collections/matching-dresses`
- Rows routed to `/collections/vacation`
- Rows routed to `/collections/daddy-and-me`

## Guardrails

- No live keyword, ad, bid, budget, campaign, status, negative, or upload action is authorized by this packet.
- Do not bid above `$0.15`.
- Do not upload head/near-head variants that already failed the `$0.15` gate.
- Do not edit Shopify product/vendor/source data without fresh explicit action-time approval.
- Do not treat the collection preflight as product/feed scope approval.

## Next Best Action

Run an authenticated read-only Google Ads/Keyword Planner validation for only the clean-route GB/CA/AU `GREEN` rows, using max CPC `$0.15`, then prepare an exact bounded action row if and only if auction-entry/CPC feasibility passes and the Marketing Safety Reviewer gate passes.
