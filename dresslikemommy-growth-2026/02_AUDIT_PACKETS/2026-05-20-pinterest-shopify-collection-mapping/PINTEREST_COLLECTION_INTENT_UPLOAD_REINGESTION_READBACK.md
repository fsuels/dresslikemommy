# Pinterest Collection Intent Upload And Reingestion Readback

Date: 2026-05-20

## Approved Scope

Owner approved this bounded sequence:

1. Upload/reingest the regenerated collection-intent feed.
2. Wait for Pinterest source processing.
3. Create product groups from `custom_label_2` plus `custom_label_4`.
4. Verify selector counts `99/77/34`.
5. Review budget/CPC/optimization/status before any restart.

No restart/enablement approval was given.

## Local Feed Rebuild

Command:

```bash
python3.13 ops/scripts/build_pinterest_unified_feed.py
```

Unified feed:

- Path: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_unified_all_markets.tsv`
- SHA-256: `b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0`
- Rows: `28,122`
- Unique item IDs: `28,122`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Duplicate item IDs: `0`
- Parent image drift groups: `0`
- Supplier/source host hits: `0`

US label readback from the regenerated unified feed:

| `custom_label_2` | Unique US parent products |
|---|---:|
| `mommy_and_me` | 99 |
| `family_matching` | 77 |
| `daddy_and_me` | 34 |
| `unassigned` | 13 |

All rows carry `custom_label_4=collection_intent_v20260520`.

## Cloudflare R2 Upload

Target:

- Bucket/object: `dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv`
- Worker URL kept unchanged: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`

Note: the first Wrangler object put defaulted to local resource mode and did not affect the live Worker/R2 body. This was detected by remote R2 and Worker SHA readback before any Pinterest action. The corrected upload used `--remote`.

Correct live write:

```bash
set -a; source ~/.config/dresslikemommy/cloudflare.env; set +a
npx wrangler@4.86.0 r2 object put dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv \
  --file dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_unified_all_markets.tsv \
  --remote
```

Remote R2 readback:

- SHA-256: `b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0`
- Lines including header: `28,123`

Worker body readback:

- HTTP: `200`
- Content type: `text/tab-separated-values; charset=utf-8`
- Body SHA-256: `b76539eb641fede467bd6a572f90689c5b1bbff12edd8707fc202c87b4f1b1c0`
- Lines including header: `28,123`
- Data rows: `28,122`
- US parent counts by `custom_label_2`: Mommy & Me `99`, Family Matching `77`, Daddy & Me `34`, unassigned `13`

Known caveat: Worker metadata headers still show the older static `X-DLM-Feed-Rows` and `X-DLM-Feed-SHA256`. The response body is correct. No Worker deploy/metadata change occurred because the approval was feed-object/reingestion scoped.

## Pinterest Ingestion Trigger

Source:

- Catalog: `3041764155561548387`
- Source: `3041760873378113572`
- Name: `DLM Cloudflare Grouped Feed 2026-05-18`
- URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`

Before trigger:

- Current ingestion: `Completed`
- Product count: `27,555`
- Successful uploads: `27,555`
- Failed to upload: `567`
- Warnings: `0`
- Latest ingestion: `May 19 at 9:48 AM EDT`

Action:

- Used `Manage ingestion > Trigger ingestion`.
- Confirmed the expected `Trigger ingestion?` modal for source `3041760873378113572`.

After trigger:

- New ingestion row: `May 20 at 12:53 AM EDT`
- Status: `Processing`
- Current ingestion product count: `-`
- Images: `Processing`
- Successful uploads: `0`
- Failed to upload: `0`
- Warnings: `0`
- Videos: `0`

Polls after trigger continued to show `Processing`. No product groups were created because selector counts would still be stale until ingestion completes.

## Automation Follow-Up

Created heartbeat automation `pinterest-ingestion-readback` to wake this thread and continue from the exact gate.

Next valid action when ingestion completes:

1. Create product groups:
   - `DLM_PIN_US_PAID_MOMMY_AND_ME_99_20260520`
   - `DLM_PIN_US_PAID_FAMILY_MATCHING_77_20260520`
   - `DLM_PIN_US_PAID_DADDY_AND_ME_34_20260520`
2. Filters:
   - `custom_label_0 = us`
   - `custom_label_2 = <lane>`
   - `custom_label_4 = collection_intent_v20260520`
3. Verify selector counts `99/77/34`.
4. Review campaign budget/CPC/optimization/status.
5. Stop before restart unless the owner gives fresh restart approval on the then-current screen.

## Heartbeat Source Completion Readback

Heartbeat poll at `2026-05-20 01:30 EDT` found the Pinterest source no longer processing.

Source detail readback:

- Current ingestion: `Completed`
- Product count: `28,122`
- Current ingestion row: `28,122 of 28,122`
- Latest ingestion: `May 20 at 12:53 AM EDT`
- Images: `Completed`
- Past ingestion row `May 20 at 12:53 AM EDT`: `28,122` successful uploads, `0` failed, `0` warnings, `0` videos

This clears the ingestion gate.

## Product Group Selector Count Gate

Attempted the approved label-filter path in the Pinterest product group builder and stopped before saving because the selector count did not match the approved parent-listing inventory.

Approved filters tested:

- `custom_label_0 is us`
- `custom_label_2 is mommy_and_me`
- `custom_label_4 is collection_intent_v20260520`

Pinterest selector preview result:

- `1,419 products selected`
- Availability preview: `1,418` in stock, `1` out of stock

Expected gate:

- Mommy & Me parent products: `99`
- Family Matching parent products: `77`
- Daddy & Me parent products: `34`

Local feed verification explains the mismatch:

| `custom_label_2` | Pinterest row / variant count | Parent listing count |
|---|---:|---:|
| `mommy_and_me` | 1,419 | 99 |
| `family_matching` | 2,590 | 77 |
| `daddy_and_me` | 522 | 34 |
| `unassigned` | 156 | 13 |

Conclusion: Pinterest's product group selector is counting catalog item rows / variants, not unique parent listings, even though the feed correctly carries `item_group_id` and parent images. Because the required selector counts `99/77/34` did not appear, no new collection-intent product groups were created.

Existing label groups visible in Pinterest after ingestion are not the approved collection-intent groups and should not be attached to the campaign:

| Existing group | Visible count | Reason not approved |
|---|---:|---|
| `DLM_PIN_US_LABEL_MOMMY_ME_20260520` | 1,524 | Old `custom_label_1` category/variant group, not collection intent |
| `DLM_PIN_US_LABEL_FAMILY_MATCHING_20260520` | 2,893 | Old `custom_label_1` category/variant group, not collection intent |
| `DLM_PIN_US_LABEL_PAJAMAS_20260520` | 252 | Old category group and no longer part of the requested three-lane structure |

The unsaved product-group draft was dismissed.

## Campaign Read-Only Review After Gate Failure

No restart was attempted. Read-only reporting/edit readback after dismissing the unsaved product-group draft:

- Campaign: `DLM_PIN_US_CATALOG_333_EXACT_20260518`
- Campaign ID: `626758581530`
- Reporting status: `Paused`
- Reporting header: `0 currently being served`
- Objective: `Catalog sales`
- Today UTC reporting at readback: `$2.79` spend, `1,433` impressions, `19` Pin clicks, `19` outbound clicks, `1.33%` CTR, `$0.15` CPC, `0` actions
- Ad group: `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518`
- Ad group ID: `2680090307739`
- Ad group reporting status: `Active`, but not serving because the campaign is paused
- Bid column: `$0.15`
- Selected product groups in the edit readback are still the old item-ID groups:
  - `DLM_PIN_US_SHOPPING_PAJAMAS_333` / `4673019468480` / `29 Products in stock`
  - `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` / `4673019468479` / `103 Products in stock`
  - `DLM_PIN_US_SHOPPING_MOMMY_ME_333` / `4673019468477` / `166 Products in stock`
- Format details: Shopping ad, website destination, `Shop now`, Pinterest Performance+ creative optimization off, generate backgrounds off, image resizing off
- Targeting: All U.S., placement Browse and search
- Optimization and delivery panel shows custom bid field `Maximum CPC bid (in USD)` and recommendation to use Pinterest Performance+ bidding; no setting was changed

## Revised Next Gate

Do not restart this campaign and do not attach the old product groups.

The corrected next action is no longer another ingestion poll. The feed and source are clean; the remaining blocker is product-group semantics:

1. Decide whether Pinterest campaign product groups should be allowed to show variant-row counts while the paid lane is validated by unique `item_group_id` parent counts, or whether a parent-only ad feed/source is needed for selector counts to display `99/77/34`.
2. If parent-count selector parity is mandatory, create a separate Pinterest ads source/feed with one representative row per parent product for the paid lanes, then ingest and verify selectors against `99/77/34`.
3. Only after the count semantics are approved, replace campaign product groups and review budget/CPC/optimization/status again.
4. Restart still requires fresh action-time owner approval.

## Guardrails

No Pinterest product group creation, campaign/ad group/ad restart, publish, enable, budget, bid, status, tag/CAPI, billing, Shopify product/theme/app-proxy, Merchant, Google Ads, GA4, or GTM write occurred during the heartbeat follow-up.
