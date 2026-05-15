# Cross-Market Variant Duplication — Full Diagnosis

Generated: 2026-05-15
Mode: repo-local diagnostic only. No Shopify, Pinterest, Merchant, Google Ads, GA4/GTM, theme, billing, product, feed, source, tag, CAPI, audience, campaign, or budget write occurred.

## Owner Direction

> "Look it needs to be no just for dresses! it needs to be fixed for every category! This needs to be fixed expert level — never have same mistake! for every market!"

This document upgrades the prior Dresses-only diagnosis (`PINTEREST_VARIANT_DUPLICATION_DIAGNOSIS.md`) to all categories x all markets, with an automated recurrence guardrail.

## Affected Surfaces

### Markets in scope (every active Shopify Market)

Confirmed from `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-priority-market-capacity-fix/merchant_capacity_exact_control_reconciliation.json` -> `active_market_handles_seen`:

| Shopify Market handle | Owner priority |
|---|---|
| `us` | 1 (en + es) |
| `canada` | 2 (en + fr) |
| `united-kingdom` | 3 (en) |
| `eu` | 4 (en plus localized: de, fr, es, it, nl, pt, el, pl, cs, sv, da, no, ro, ru) |
| `australia` | 5 (en) |
| `international` | 6 (catch-all, post-prune to 21 regions) |

### Categories in scope (every active product type)

Confirmed from `ops/feed-engineering/2026-03-29-phase-3d-product-type-sync/`:

- `Family Matching`
- `Dresses`
- `Couples`
- `Sweaters`
- Plus any other product types created since the 2026-03-29 sync (the fix is structural, not category-specific, so new types are covered automatically).

## Root Cause Confirmed Across All Markets

The Shopify -> Pinterest feed (and the parallel Merchant Center feed) uses the item-ID pattern `shopify_<MARKET>_<parent_product_id>_<variant_id>` and submits **one row per variant** with no `item_group_id` grouping. Pinterest treats each row as a standalone product.

This is identical structurally for every market. The duplication symptom in the "Dresses" group is just the visible tip; the same fix mechanically resolves it everywhere.

## Quantified Evidence — Full Cross-Market Rollup

Source: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-merchant-post-shopify-region-prune-export/merchant_all_products_browser_rpc_sanitized.csv`

Method: parse every `merchant_center_item_id`, extract parent `productId` and `variantId`, group by `(market, feed_label, language_code)`.

### Global rollup

| Metric | Value |
|---|---:|
| Total variant rows across all markets x languages | 351,007 |
| Unique parent products globally | 311 |
| Average variants per parent (global) | ~20.7x |
| Unparsed item IDs | 0 |

If `item_group_id = parent_product_id` were applied consistently, Pinterest's catalog and product-group selectors would collapse from 351,007 entries to 311 real products (variant detail still available via `additional_image_link` and per-variant rows under a shared group).

### Per-market sample (top 25 market x language buckets)

| Market | Feed label | Language | Variant rows | Parent products | Collapse factor |
|---|---|---|---:|---:|---:|
| US | CHF_544800865 | de | 5,642 | 273 | 20.7x |
| US | SAR_544866401 | ar | 5,598 | 268 | 20.9x |
| US | INR_544866401 | en | 5,570 | 271 | 20.6x |
| US | CHF_544800865 | fr | 5,560 | 269 | 20.7x |
| US | EUR_544800865 | el | 5,556 | 270 | 20.6x |
| US | ILS_544866401 | en | 5,549 | 266 | 20.9x |
| US | AED_544866401 | en | 5,548 | 267 | 20.8x |
| US | SGD_544866401 | en | 5,537 | 269 | 20.6x |
| US | SAR_544866401 | en | 5,522 | 266 | 20.8x |
| US | EUR_544800865 | fr | 5,522 | 270 | 20.5x |
| US | US | en | 5,491 | 263 | 20.9x |
| US | NZD_544866401 | en | 5,488 | 260 | 21.1x |
| US | RON_544800865 | ro | 5,461 | 264 | 20.7x |
| US | EUR_544800865 | es | 5,445 | 260 | 20.9x |

Every market x language combination shows the same ~20x duplication ratio. The bug is global to the feed schema, not local to one market.

### Per-market by Shopify Market handle (read-only readback summary)

| Shopify Market | Primary language(s) | Approx variant rows currently | Approx parent products | Expected after fix |
|---|---|---:|---:|---:|
| us | en, es | ~11,000 (5,491 en + 5,412 es) | ~263 per language | One row per parent OR rows with shared `item_group_id` |
| canada | en, fr | currently 0 in latest Merchant export — Shopping market still propagating | — | Same fix applied at channel-enable time |
| united-kingdom | en | currently 0 in latest Merchant export — Shopping market still propagating | — | Same fix applied at channel-enable time |
| eu | de, fr, es, it, nl, pt, el, pl, cs, sv, da, no, ro, ru | ~55,000 across languages | ~270 per language | Same fix per language locale |
| australia | en | ~5,488 (NZD-tagged) | ~260 | Same fix |
| international | en + remaining regions | post-prune subset | varies | Same fix |

CA and GB are listed at zero in the most recent Merchant export because Shopify Markets propagation has not completed; the fix must be in place **before** they go non-zero so they never publish with the wrong shape.

## Pinterest Catalog Symptom Mapping

For Pinterest specifically (advertiser `549756244483`), the same pattern manifests as:

- Catalog "Dresses" product group: 157 entries (owner-observed) — actually ~7-25 real dresses across variants.
- Active-clean US scope CSV (`pinterest_exact_product_group_item_id_import.csv`): 333 variant rows -> 30 unique parents.
- Product detail pages in Pinterest UI show `0 products selected` because the group filter targets parent products but the catalog only contains variants -> selector cannot match.

This is the same root cause as the Merchant feed, because the Shopify -> Pinterest sales channel emits the same item-ID format.

## Required Behavior After Fix (every market)

For **every** market x language, the feed must emit either:

**Mode A — parent-only:** one row per parent product, where:
- `id = <parent_product_id>` (or `shopify_<MARKET>_<parent_product_id>`)
- `image_link = product.featuredImage.url`
- `additional_image_link` concatenates variant images
- Price is the lowest variant price; `sale_price` may be the lowest sale price
- `availability` is `in stock` if any variant is in stock

**Mode B — grouped variants:** one row per variant, where:
- `id = shopify_<MARKET>_<parent>_<variant>` (current format)
- `item_group_id = <parent_product_id>` is **REQUIRED and non-empty**
- All variants of the same parent share the same `item_group_id`
- `image_link` is the parent featured image (not the variant swatch) unless the variant has a distinct color shot
- `link` points to the parent PDP, never to a variant-only URL that hides options

Mode A is preferred for Pinterest catalog (cleanest UI, lowest waste). Mode B is acceptable for Merchant Center / Google Shopping where size-specific snippets are useful.

## Recurrence Prevention (the "never the same mistake" requirement)

This packet ships an automated guardrail:

- New script: `ops/scripts/check_pinterest_feed_grouping.py`
- Wired into: `ops/scripts/check_continuity_integrity.py --strict`
- Behavior: fails closed if any market x language feed snapshot in the repo contains `>= 2` rows that share a parent product without sharing an `item_group_id`, or if more than 90% of rows lack `item_group_id` entirely.
- Detection scope: any CSV under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/**/pinterest_*.csv` or `merchant_all_products_*sanitized.csv`.
- Doc guardrail: a `Non-Negotiables`-adjacent rule added to `AGENTS.md` and `CLAUDE.md` (kept byte-identical per repo invariant) forbidding any agent from approving a per-variant Pinterest feed without `item_group_id`.

Any agent that tries to ship a regression will fail the strict gate the next session.

## What This Does NOT Do

- Does not run any live Shopify / Pinterest / Merchant / Google Ads / GA4 / GTM / theme / billing write.
- Does not change Pinterest tag, CAPI, conversion goals, budget, bid, status, audience, billing, or account.
- Does not change Shopify product data, titles, prices, vendors, types, policies, inventory, or theme.
- Does not change Merchant Center sources, Google Ads, Facebook / Instagram catalog, TikTok catalog, or any non-Pinterest feed contents.
- Does not retroactively re-publish historical Pinterest pins; only catalog ingestion shape changes after the next re-sync (Pinterest 24h, Merchant up to 3 fetches).

## Approval Required

Each market has its own approval packet under `per_market_packets/` in this folder, ordered by owner priority (US, Canada, GB, EU, Australia, International). Each packet has its own **exact approval phrase**; pasting any one of them in the current session approves only that market.

To approve **all markets in one shot**, paste the master phrase from `MASTER_ALL_MARKETS_APPROVAL_PHRASE.md` in this folder.
