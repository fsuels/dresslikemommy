# Merchant US/es Source Detail Readback

Generated: 2026-05-14T05:37:54-04:00

Problem: `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`.

Mode: live Merchant Center read-only browser/RPC capture. No uploads, source syncs, edits, saves, product data changes, or Ads/Pinterest/Shopify writes were made.

Decision: `US_ES_SOURCE_10627981690_TARGET_ROWS_VISIBLE_BUT_DETAIL_MISSING_AGE_GROUP_NOT_REPRODUCED`.

## Source 10627981690

- Direct source URL attempted: `https://merchants.google.com/mc/products/sources/joindetails?a=124884876&joinFeedId=10627981690&tab=settings`
- Direct source page title: `- Merchant Center`
- Direct source-detail UI did not expose a clean source settings/processing table in this run; it showed the Merchant shell plus a stale ready-download notification.
- Product-detail RPCs below are therefore the stronger readback for source `10627981690`.

## Product List Readback

- Sample queries: `shopify_US_7227630649441_41872775020641, shopify_US_7227379023969_41871522431073, shopify_US_7227254276193_41871113158753`.
- Target `US` / `es` / source `10627981690` rows visible: `2`.

| Item ID | Last updated UTC | custom_label_0 | custom_label_4 | Source |
| --- | --- | --- | --- | --- |
| `shopify_US_7227630649441_41872775020641` | `2026-05-09T07:21:52+00:00` | `` | `` | `10627981690 / Shopify App API` |
| `shopify_US_7227379023969_41871522431073` | `2026-05-09T07:21:49+00:00` | `` | `` | `10627981690 / Shopify App API` |

## Product Detail Readback

| Item ID | Missing age_group shown | Effective `n:age_group` in detail RPC | Issues |
| --- | --- | --- | --- |
| `shopify_US_7227630649441_41872775020641` | `False` | `True` | `` |
| `shopify_US_7227379023969_41871522431073` | `False` | `True` | `` |
| `shopify_US_7227254276193_41871113158753` | `False` | `True` | `` |

## Interpretation

- The readback preserves the solved US/en age_group state and does not redo Shopify variant age_group work.
- The active US/es source path is source `10627981690` / `Shopify App API`; live detail readback should be treated as the authoritative blocker for Spanish-language US paid use.
- Any actual repair still requires a fresh exact approval gate before source refresh/sync/edit/upload or Shopify product-data changes.

## Evidence

- Summary JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/merchant-us-es-readback/merchant_us_es_source_detail_readback_summary.json`
- Raw captures: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/merchant-us-es-readback/raw`
