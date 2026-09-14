# Gate B-3 Local Feed Repair Readback

Date: 2026-05-18 04:58 EDT

## Scope

Local-only repair for the Pinterest TSV after Gate B-3 completed with ingestion diagnostics.

This pass did not upload to Cloudflare R2, trigger Pinterest ingestion, change Pinterest settings, click Promote, pause/remove legacy sources, or mutate Shopify/Merchant/Google Ads/GA4/GTM.

## Pinterest Diagnostics Being Repaired

Source: `3041760873378113572`

Completed ingestion showed:

- Successful uploads: `41,056`
- Failed uploads: `758`
- Warnings: `40,998`

Visible diagnostics:

- Warning `126`: shallow `google_product_category` on `41,814` rows.
- Warning `179`: malformed `gtin` on `7,710` rows.
- Warning `1011`: additional image ingestion on `6 + 1` rows.
- Error `1009`: image ingestion on `1` row.

This local repair targets the first two large feed-format issues. The small image-ingest issues may clear on the next ingestion or require item-level diagnostics if they persist.

## Code Change

Updated `ops/scripts/generate_pinterest_feed_grouped.py`:

- Added product-type to deeper `google_product_category` mapping.
- Added GTIN checksum validation for GTIN-8/12/13/14.
- Suppressed non-digit, wrong-length, or bad-checksum GTIN values from the Pinterest-only TSV.
- Added `identifier_exists=yes` only when a checksum-valid GTIN is emitted.
- Added `identifier_exists=no` when GTIN is blank.
- Preserved parent-product `item_group_id`.
- Preserved parent featured image in `image_link`.
- Preserved supplier/source URL blocking.

## Rebuilt Files

Regenerated local feeds with:

```bash
python3.13 ops/scripts/build_pinterest_unified_feed.py
```

Updated outputs:

- `feeds/pinterest_us.tsv`
- `feeds/pinterest_canada.tsv`
- `feeds/pinterest_united-kingdom.tsv`
- `feeds/pinterest_eu.tsv`
- `feeds/pinterest_australia.tsv`
- `feeds/pinterest_international.tsv`
- `feeds/pinterest_unified_all_markets.tsv`
- `feeds/pinterest_unified_all_markets.summary.json`
- `feeds/pinterest_unified_all_markets.sha256`

## Repaired Unified Feed Readback

File:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_unified_all_markets.tsv`

Readback:

- Data rows: `41,814`
- File lines including header: `41,815`
- Size: `145M`
- SHA-256: `809d48e96832ffc4db8a30de685250273412c2988678b5364d48c627699e8863`
- Unique item IDs: `41,814`
- Duplicate item IDs: `0`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Parent groups with multiple `image_link` values: `0`
- Supplier/source host hits: `0`

Category repair:

| Category | Rows |
|---|---:|
| `Apparel & Accessories > Clothing > Outfit Sets` | `22,218` |
| `Apparel & Accessories > Clothing > Swimwear` | `6,732` |
| `Apparel & Accessories > Clothing > Shirts & Tops` | `6,636` |
| `Apparel & Accessories > Clothing > Dresses` | `4,116` |
| `Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas` | `2,004` |
| `Apparel & Accessories > Clothing > Outerwear` | `84` |
| `Apparel & Accessories > Clothing > One-Pieces` | `24` |

Warning-targeted validation:

- Shallow category rows: `0`
- GTIN present: `852`
- GTIN blank/suppressed: `40,962`
- Bad GTIN format/checksum rows remaining: `0`
- `identifier_exists=yes`: `852`
- `identifier_exists=no`: `40,962`

## Guardrail Verification

Command:

```bash
python3.13 ops/scripts/check_pinterest_feed_grouping.py --report-only --strict
```

Result:

- Generated Path B feeds: `7` PASS, including unified feed.
- Upstream/live-equivalent historical snapshots: `3` expected FAIL.
- Summary: `10` snapshots scanned, `3` FAIL, `0` ERROR.

The FAIL snapshots are the old upstream/Merchant/CSV evidence that remains intentionally unresolved until a clean live Pinterest readback exists. The repaired local Path B feed itself passes.

## Upload Status

At the time of this local repair readback, no Cloudflare R2 object replacement had occurred.

After the owner later approved the exact upload/reingestion phrase, automation replaced only Cloudflare R2 object `pinterest/pinterest_unified_all_markets.tsv` with this repaired TSV and triggered Pinterest reingestion for source `3041760873378113572`. See `GATE_B3_PINTEREST_CLOUDFLARE_SOURCE_READBACK.md` for the live upload/reingestion readback.

No Pinterest source edit, campaign launch, Promote action, budget/bid/status, tag/CAPI, billing, legacy-source pause/remove, Shopify, Merchant, Google Ads, GA4/GTM, or product write occurred.

## Approval Required For Next External Step

To upload and test the repaired feed, the next live-gated approval should be exact:

```text
I approve replacing the existing Cloudflare R2 object pinterest/pinterest_unified_all_markets.tsv with the locally verified repaired Pinterest TSV SHA-256 809d48e96832ffc4db8a30de685250273412c2988678b5364d48c627699e8863, keeping the same Worker URL https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv, then triggering or waiting for Pinterest source 3041760873378113572 to reingest and capturing after-state readback. Do not launch, promote, pause/remove legacy feeds, change campaigns/ad groups/ads/audiences/budgets/bids/statuses/tag/CAPI/billing, change Shopify products/theme/app-proxy, or mutate Merchant/Google Ads/GA4/GTM.
```

Expected after-state proof:

- Pinterest source `3041760873378113572` ingestion completed.
- Successful uploads improve from `41,056`.
- Failed uploads decrease from `758`.
- Warning `126` for shallow category materially decreases or clears.
- Warning `179` for malformed GTIN clears or materially decreases.
- `item_group_id` grouping remains visible.
- Parent featured image remains the primary `image_link`.
- Exact product groups become usable without broad fallback.
