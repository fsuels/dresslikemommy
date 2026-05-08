# Pinterest Event Quality / Catalog / Item Readback

Generated: 2026-05-07 14:45 EDT

Scope: read-only Pinterest Ads/Catalog browser readback using existing logged-in session artifacts. No Pinterest campaign, ad group, product group, catalog, item, pixel, tag, CAPI, budget, bid, audience, or spend writes were made. No Shopify or Google Ads changes were made.

## Decision

`PINTEREST_US_DRAFTS_STILL_BLOCKED_PENDING_APPROVAL_AND_ITEM_LEVEL_SCOPE.`

Pinterest measurement is healthier than the stale packet suggested because Events Overview now shows fresh Checkout and AddPaymentInfo activity from both `Api · Tag`, but Event Quality itself still reads `Fair` and updated `5/6/2026`. Catalog EN ingestion looks clean in the visible UI, but any paid draft still needs explicit approval and exact included item/product-group scope.

## Event Quality

- Event Quality page readback: `event_quality_readback.txt` / `event_quality_screenshot.png`.
- Score update timestamp: `Updated 5/6/2026`.
- Event quality score: `Fair`.
- Top visible action items remain: Product ID in Add Payment Info, Email in Add to Cart, and Click ID in Checkout.
- Event-parameter gaps still mention Product ID and Order Value for Add Payment Info, and Click ID across Checkout/AddToCart/InitiateCheckout/AddPaymentInfo/PageVisit/Search/ViewCategory.

## Events Overview

- Fresh Events Overview artifact: `events_overview_fresh_readback.txt`.
- Source path visible for all standard events: `Api · Tag`.

| Event | Total events | Last received |
|---|---:|---|
| PageVisit | 19,913 | 5/7/2026 06:38pm (UTC) |
| ViewCategory | 4,224 | 5/7/2026 03:18pm (UTC) |
| AddToCart | 703 | 5/7/2026 02:29pm (UTC) |
| InitiateCheckout | 124 | 5/7/2026 01:21pm (UTC) |
| Search | 40 | 5/2/2026 07:07am (UTC) |
| Checkout | 25 | 5/7/2026 01:22pm (UTC) |
| AddPaymentInfo | 24 | 5/7/2026 01:22pm (UTC) |

Interpretation: Checkout and AddPaymentInfo are now visibly receiving after the 2026-05-06 official Pinterest app pixel fix, but Event Quality has not yet advanced past `Fair`.

## Catalog Readback

- Catalog surface: `Catalog_Retail`.
- Data sources artifact: `catalog_data_sources_fresh_readback.txt`.
- EN Shopify data source: `3041760867124595727`, latest ingestion `May 7 at 1:14 PM EDT`; detail readback says `Completed`, `5,663 of 5,663`, `0` failed, and `152` warnings.
- A separate sitemap data source `3041760916127467912` still shows `Failed` at `May 7 at 3:31 AM EDT`; treat this as non-launch-clean until it is understood, even if the Shopify EN source is clean.
- Other localized Shopify feeds show some warning/fail counts, e.g. cs `5,577 / 86`, German `5,611 / 52`, ro `5,645 / 18`, hi `5,661 / 2`. Pinterest international expansion should wait.

## EN Ingestion And Product Groups

- EN ingestion diagnostics artifact: `catalog_en_ingestion_fresh_readback.txt`.
- The visible ingestion issue table for data source `3041760867124595727` shows blank issue rows; no concrete EN ingestion issue text was captured.
- Product groups artifact: `catalog_en_product_groups_fresh_readback.txt`.
- Visible product groups include `All Products`, `Top Sellers`, `Midi Dresses`, `Dresses`, `Tops`, `Best Deals`, `New Arrivals`, `Back In Stock`, `Matching Hawaiian Outfits for Family`, `Family Matching Tops`, and `Family Matching Outfits`.
- Product-group UI contains Promote actions; no Promote/create/save action was clicked.

## Dropshipping/Inventory Interpretation

- Owner correction: Dress Like Mommy is dropshipping, with no physical store and no owned physical inventory. Pinterest catalog availability terms such as item availability or product groups must be interpreted as platform/catalog salability only, not a physical-stock promise.
- Avoid customer-facing copy that implies local inventory, a warehouse, or guaranteed on-hand stock.

## Blockers

- Event Quality still reads `Fair`, with unresolved parameter action items.
- Exact item-level paid candidate readback was not refreshed in this pass; the visible product-groups page is not enough to prove each candidate row.
- Sitemap data source failure and localized feed warning/fail counts need follow-up before Pinterest international catalog testing.
- Paused Pinterest draft creation still needs explicit action-time approval and USA-only targeting readback.

## Next Safe Action

Keep Pinterest draft creation parked. Next read-only step is exact US candidate item-level readback for the intended paid-ready rows, plus another Event Quality check after Pinterest refreshes beyond `5/6/2026`. Draft creation requires the existing exact approval gate and must remain paused/draft-only with no spend.

## Artifacts

- `event_quality_readback.txt`
- `event_quality_screenshot.png`
- `events_overview_fresh_readback.txt`
- `catalog_data_sources_fresh_readback.txt`
- `catalog_en_ingestion_fresh_readback.txt`
- `catalog_en_product_groups_fresh_readback.txt`
- `fresh_visible_readback_summary.json`
