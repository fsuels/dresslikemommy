# Path B Grouped Feed Generation Readback

Generated: 2026-05-15 10:07 EDT
Mode: read-only Shopify Admin fetch plus local TSV generation. No Shopify, Pinterest, Merchant, Google Ads, GA4/GTM, theme, billing, product, feed-source, tag, CAPI, audience, campaign, budget, bid, status, conversion, or credential write occurred.

## Why

Pinterest launch remains blocked because current catalog evidence submits size/color variants as standalone product rows without `item_group_id`. The channel/UI grouping path still needs owner approval and after-state readback. This pass advanced the approved local fallback lane: generate Path B grouped TSV files so a future exact-approved operator has an executable grouped-feed artifact if the Shopify Pinterest channel does not expose a parent-grouping toggle.

## Local Outputs

Generated with:

```bash
python3.13 ops/scripts/generate_pinterest_feed_grouped.py --market <market> --output dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_<market>.tsv
```

| Market | Rows | Unique parent groups | Missing `item_group_id` | Supplier/source host hits |
|---|---:|---:|---:|---:|
| `us` | 6,969 | 326 | 0 | 0 |
| `canada` | 6,969 | 326 | 0 | 0 |
| `united-kingdom` | 6,969 | 326 | 0 | 0 |
| `eu` | 6,969 | 326 | 0 | 0 |
| `australia` | 6,969 | 326 | 0 | 0 |
| `international` | 6,969 | 326 | 0 | 0 |

Each TSV emits per-variant rows with a shared parent `item_group_id`, parent PDP links, and parent featured image in `image_link`.

## Guardrail Result

Command:

```bash
python3.13 ops/scripts/check_pinterest_feed_grouping.py --report-only --strict
```

Result:

- `6` generated Path B feed snapshots: `PASS`.
- `3` existing upstream/live-equivalent snapshots: expected `FAIL`.
- `0` parser errors.

Expected failing snapshots remain:

- Pinterest exact product-group import CSV: `30` duplicate-parent clusters without `item_group_id`.
- Merchant post-prune sanitized export: `69` market x language buckets with duplicate parents, worst `96x`.
- Merchant source-eligibility sanitized export: `69` market x language buckets with duplicate parents, worst `96x`.

## Decision

Path B is now locally generated and guardrail-clean for every active market. It is not upload authority. The next live step still requires one of:

1. Owner approves and the operator applies the Shopify Pinterest channel grouping setting, if exposed.
2. Owner gives separate exact approval to upload/import the generated Path B grouped TSVs as a Pinterest catalog source, with before/after readbacks and a 24h re-sync check.

Do not attest `FIX_LANDED_FRESHNESS_MARKER.txt` or run strict mode as solved until the live after-state shows grouped rows for every approved market/category.
