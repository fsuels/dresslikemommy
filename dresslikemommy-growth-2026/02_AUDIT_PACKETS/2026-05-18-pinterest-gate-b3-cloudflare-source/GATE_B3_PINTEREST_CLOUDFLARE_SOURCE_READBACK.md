# Gate B-3 Pinterest Cloudflare Source Readback

Date: 2026-05-18 02:39 EDT

## Approval

Owner approved Gate B-3 with the exact current-session instruction:

`Approve Gate B-3 using the verified Cloudflare Worker URL.`

Approved scope:

- Add/configure a Pinterest catalog data source for advertiser `549756244483`.
- Use verified URL `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`.
- Keep Gate B-3 separate from campaign/ad group/ad/audience/budget/bid/status/tag/CAPI/billing work.
- Do not pause/remove legacy sources until the new source ingests cleanly and grouped readback passes.

## Input Feed Verification

Gate B-2 public feed readback had already passed before this approval:

- URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
- HTTP: `200`
- Content type: `text/tab-separated-values; charset=utf-8`
- Content length: `151559047`
- Rows: `41,814`
- SHA-256: `8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7`
- Duplicate item IDs: `0`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Supplier/source host hits: `0`
- POST guard: `405`

## Before-State Readback

Pinterest authenticated access was confirmed for:

- Advertiser: `549756244483`
- Catalog: `3041764155561548387`
- Business/account surface: `Dress Like Mommy | Matching Family Outfits`

Before adding the new source, the catalog data-source page showed existing Shopify and URL sources, including the previous URL source `https://www.dresslikemommy.com/sitemap_collections_1.xml` in failed state and existing Shopify feed profiles.

Evidence:

- `raw/before-data-sources.png`

## Gate B-3 Action

Configured a new Pinterest catalog data source:

- Name: `DLM Cloudflare Grouped Feed 2026-05-18`
- Source URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
- Format: `TSV`
- Country/region: `United States`
- Language: `English (US)`
- Currency: `USD`
- Schedule: enabled, every 24 hours
- Scheduled time: `03:00`
- Timezone: `America/New_York`

Pinterest validation completed before submission. The UI showed: file validation complete and continue-to-submit.

Evidence:

- `raw/pre-submit-add-source.png`
- `raw/validation-complete-before-continue.png`

## After-State Readback

The source was submitted and Pinterest showed:

- New data source name: `DLM Cloudflare Grouped Feed 2026-05-18`
- Data source ID: `3041760873378113572`
- List status: `New Processing`
- Latest ingestion: `May 18 at 2:33 AM EDT`
- Source: `URL pinterest-feed.tsv`
- Country: `United States`
- Language: `English (US)`

Detail URL:

`https://www.pinterest.com/business/catalogs/3041764155561548387/data-sources/3041760873378113572/detail/?subjectBusinessId=343118202768859516`

Detail page readback:

- Data source ID: `3041760873378113572`
- Data source URL exactly matched the verified Cloudflare Worker URL.
- Current ingestion product count: `-`
- Current ingestion status: `Processing`
- Images: `Processing`
- Feed ingested daily.
- Next scheduled update: `May 18 at 3:00 AM EDT`
- Past ingestions: `May 18 at 2:33 AM EDT`, status `Processing`
- Successful uploads: `0`
- Failed: `0`
- Warnings: `0`
- Videos: `0`
- Data source file download: disabled while processing

Two repolls during the session still showed `Processing`, which is consistent with Pinterest's stated "up to 24 hours" processing window.

Evidence:

- `raw/after-data-source-submitted.png`
- `raw/after-detail-processing.png`
- `raw/after-detail-processing-repoll.png`

## Product-Group Count Readback

At 2026-05-18 03:12 EDT, the owner observed the new feed profile on the Pinterest Product groups page:

- Page URL included `feedProfileId=3041760873378113572`.
- Selected feed profile: `DLM Cloudflare Grouped Feed 2026-05-18`
- Auto-created product group: `All Products`
- Product group ID: `4673019439386`
- Products: `41,126`
- Last updated: `5/18/2026`
- Promote control visible.

This is a positive catalog-population signal, but it is not a launch-ready proof yet. The verified feed has `41,814` rows, so Pinterest is currently showing `688` fewer products than the submitted TSV rows. The source detail page still showed current ingestion `Processing` and product count `-` during the same follow-up readback window.

Evidence:

- `raw/product-groups-owner-screenshot-2026-05-18-0312.png`
- `raw/current-detail-processing-after-product-group-count.png`

## Completed Ingestion Readback

At 2026-05-18 04:24 EDT, the owner observed the source detail page after ingestion completed. Automation read back the same authenticated Pinterest page and captured evidence.

Current ingestion:

- Product count: `41,056`
- Status: `Completed`
- Completion line: `41,056 of 41,056`
- Ingestion timestamp: `May 18 at 2:33 AM EDT`
- Images: `Completed`
- Next scheduled update: `May 19 at 3:00 AM EDT`

Past ingestion row:

- Date: `May 18 at 2:33 AM EDT`
- Status: `Completed`
- Successful uploads: `41,056`
- Failed to upload: `758`
- Warnings: `40,998`
- Videos: `0`

The submitted TSV had `41,814` data rows. The exact delta between submitted rows and successful uploads is `758`, matching Pinterest's failed-upload count. Gate B-3 therefore completed, but the ingestion is not clean.

Evidence:

- `raw/owner-source-detail-completed-2026-05-18-0424.png`
- `raw/owner-source-detail-completed-2026-05-18-0424.snapshot.txt`
- `raw/source-detail-completed-41056-758-failed-40998-warnings.png`
- `raw/source-detail-completed-41056-758-failed-40998-warnings.snapshot.txt`

## Diagnostics Readback

Automation opened the Pinterest diagnostics page for data source `3041760873378113572` and captured the visible ingestion-issue summary.

Summary:

- Successful uploads: `41.06k`, `98.19%` of total data source
- Failed to upload: `758`, `1.81%` of total data source
- Warnings: `41k`, `98.05%` of total data source
- Latest ingestion: `May 18 at 2:33 AM EDT`
- Export details button: disabled in the visible page state

Visible issues from latest ingestion:

| Type | Code | Description | What Pinterest says to do | Occurrences |
|---|---:|---|---|---:|
| Warning | `126` | Some items only have 1 or 2 levels of `google_product_category` values listed, which may limit visibility in recommendations, search results and shopping experiences | Enter all applicable levels of `google_product_category` values for each item | `41,814` |
| Warning | `179` | `gtin` is formatted incorrectly | Make sure `gtin` is all digits with length `8`, `12`, `13`, or `14`, excluding dashes | `7,710` |
| Warning | `1011` | Pinterest could not ingest some additional images in the feed | Wait 24 hours for the next ingestion; contact support if it persists | `6` |
| Error | `1009` | Pinterest could not ingest some images in the feed | Wait 24 hours for the next ingestion; contact support if it persists | `1` |
| Warning | `1011` | Pinterest could not ingest some additional images in the feed | Wait 24 hours for the next ingestion; contact support if it persists | `1` |

Local feed inspection supports the first two visible diagnostics:

- Current generated feed emits `google_product_category = Apparel & Accessories > Clothing` on all `41,814` rows, which is too shallow.
- Current generated feed includes non-empty `gtin` values on `8,562` rows; at least `264` are locally malformed because they contain non-digit SKU-like values. Pinterest reports a broader GTIN warning count of `7,710`, so the safer Pinterest-only repair is to avoid emitting uncertain GTINs unless they are known valid product identifiers.

Evidence:

- `raw/diagnostics-ingestion-issues-summary.png`
- `raw/diagnostics-ingestion-issues-summary.snapshot.txt`

## Local Repair Prepared

After diagnostics, automation repaired the Pinterest-only TSV locally without uploading it.

Repair readback:

- Repaired unified TSV rows: `41,814`
- Repaired unified TSV SHA-256: `809d48e96832ffc4db8a30de685250273412c2988678b5364d48c627699e8863`
- Shallow `google_product_category` rows: `0`
- Bad GTIN format/checksum rows remaining: `0`
- GTIN present after validation: `852`
- GTIN suppressed/blank: `40,962`
- `identifier_exists=yes`: `852`
- `identifier_exists=no`: `40,962`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Parent image drift groups: `0`

Evidence:

- `GATE_B3_LOCAL_FEED_REPAIR_READBACK.md`

## Approved Repaired R2 Upload And Manual Reingestion

At 2026-05-18 05:18 EDT, the owner approved the exact repaired-feed upload/reingestion scope:

```text
I approve replacing the existing Cloudflare R2 object pinterest/pinterest_unified_all_markets.tsv with the locally verified repaired Pinterest TSV SHA-256 809d48e96832ffc4db8a30de685250273412c2988678b5364d48c627699e8863, keeping the same Worker URL https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv, then triggering or waiting for Pinterest source 3041760873378113572 to reingest and capturing after-state readback. Do not launch, promote, pause/remove legacy feeds, change campaigns/ad groups/ads/audiences/budgets/bids/statuses/tag/CAPI/billing, change Shopify products/theme/app-proxy, or mutate Merchant/Google Ads/GA4/GTM.
```

Executed action:

- Replaced Cloudflare R2 object `dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv`.
- Kept the same Worker URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`.
- Triggered Pinterest manual ingestion from the existing source detail page.

Worker URL readback after upload:

- HTTP: `200`
- Content type: `text/tab-separated-values; charset=utf-8`
- Body SHA-256: `809d48e96832ffc4db8a30de685250273412c2988678b5364d48c627699e8863`
- Body line count: `41,815`
- Parsed data rows: `41,814`
- Duplicate item IDs: `0`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Parent image drift groups: `0`
- Shallow `google_product_category` rows: `0`
- Bad GTIN format/checksum rows: `0`
- `identifier_exists=yes`: `852`
- `identifier_exists=no`: `40,962`
- POST guard: `405`

Readback note: the Worker body is repaired and correct. The custom response header `X-DLM-Feed-SHA256` still advertises the previous SHA because that value is stored in Worker deployment config, not the R2 object body. Automation did not redeploy Worker config because the owner approved replacing the R2 object and keeping the same URL, not a Worker metadata redeploy. Pinterest fetches the TSV body from the URL.

Pinterest manual ingestion:

- Manage ingestion exposed `Trigger ingestion`.
- Confirmation modal said the source is eligible for one manually triggered ingestion every `2` hours.
- Automation confirmed `Trigger ingestion` under the owner-approved scope.
- Toast readback: `DLM Cloudflare Grouped Feed 2026-05-18 has been successfully queued for ingestion.`

Pinterest after-state poll:

- Current ingestion status: `Processing`
- Current product count: `-`
- Images: `Processing`
- Past ingestion row timestamp: `May 18 at 5:24 AM EDT`
- Past ingestion row status: `Processing`
- Successful uploads visible while processing: `41,087`
- Failed to upload visible while processing: `0`
- Warnings visible while processing: `0`
- Videos: `0`

This is a materially improved in-progress readback versus the prior completed row (`41,056` successful / `758` failed / `40,998` warnings), but it is not final launch proof until Pinterest marks the 5:24 AM ingestion `Completed` and diagnostics are refreshed.

Evidence:

- `raw/worker-repaired-r2-readback.headers.txt`
- `raw/worker-repaired-r2-readback.summary.txt`
- `raw/source-detail-before-reingest-after-r2-upload.png`
- `raw/source-detail-before-reingest-after-r2-upload.snapshot.txt`
- `raw/trigger-ingestion-confirm-modal.png`
- `raw/source-detail-reingest-queued-0524.png`
- `raw/source-detail-reingest-queued-0524.snapshot.txt`
- `raw/source-detail-reingest-processing-41087.png`
- `raw/source-detail-reingest-processing-41087.snapshot.txt`
- `raw/source-detail-reingest-processing-41087-second-poll.png`
- `raw/source-detail-reingest-processing-41087-second-poll.snapshot.txt`
- `raw/source-detail-reingest-processing-41087-final-poll.png`
- `raw/source-detail-reingest-processing-41087-final-poll.snapshot.txt`

## Completed Repaired Ingestion Readback

After the owner reported completion, automation refreshed the Pinterest source detail page and diagnostics.

Current ingestion:

- Product count: `41,814`
- Status: `Completed`
- Completion line: `41,814 of 41,814`
- Ingestion timestamp: `May 18 at 5:24 AM EDT`
- Images: `Completed`
- Next scheduled update: `May 19 at 3:00 AM EDT`

Past ingestion row:

- Date: `May 18 at 5:24 AM EDT`
- Status: `Completed`
- Successful uploads: `41,814`
- Failed to upload: `0`
- Warnings: `0`
- Videos: `0`

This confirms the repaired feed fixed the failed-upload and warning counts from the prior completed ingestion:

| Metric | Before repair | After repair |
|---|---:|---:|
| Successful uploads | `41,056` | `41,814` |
| Failed uploads | `758` | `0` |
| Warnings | `40,998` | `0` |
| Images | `Completed` | `Completed` |

Diagnostics readback:

- Successful uploads: `41.81k`, `100%` of total data source
- Failed to upload: `0`, `0%` of total data source
- Warnings: `0`, `0%` of total data source
- Latest ingestion: `May 18 at 5:24 AM EDT`
- Issues from last ingestion: `There are no ingestion issues for this data source`

Product-group readback:

- Feed profile: `DLM Cloudflare Grouped Feed 2026-05-18`
- Auto-created product group: `All Products`
- Product group ID: `4673019439386`
- Product group product count: `41,694`
- Product preview table loads real products with item IDs from the new source.
- `Promote` button is visible on the product group detail page.
- `Save to board` is disabled because Pinterest says product groups must contain `200` items or fewer to be published to boards; this does not block catalog-sales product-group usability.

Product-group count note: the product-group count (`41,694`) is `120` lower than the successful upload count (`41,814`). Pinterest diagnostics still reports `100%` successful uploads, `0` failed, and `0` warnings, so this is not an ingestion failure. Treat the `120` difference as Pinterest product-group eligibility/display filtering unless a later item-level export proves otherwise.

Evidence:

- `raw/source-detail-reingest-completed-41814-0-0.png`
- `raw/source-detail-reingest-completed-41814-0-0.snapshot.txt`
- `raw/diagnostics-reingest-clean-41814-0-0.png`
- `raw/diagnostics-reingest-clean-41814-0-0.snapshot.txt`
- `raw/product-groups-reingest-completed-all-products-41694.png`
- `raw/product-groups-reingest-completed-all-products-41694.snapshot.txt`
- `raw/product-group-detail-all-products-41694-preview.png`
- `raw/product-group-detail-all-products-41694-preview.snapshot.txt`

## Guardrails Confirmed

No action was taken on:

- Pinterest campaign/ad group/ad/audience/budget/bid/status
- Pinterest tag/CAPI
- Pinterest billing
- Legacy Pinterest source pause/remove
- Shopify product/source/theme/app-proxy configuration
- Merchant Center feeds/sources/products
- Google Ads campaigns/conversions/budgets/bids/statuses
- GA4/GTM

## Current State

The repaired R2 object is live at the same Worker URL and Pinterest repaired ingestion is completed cleanly.

Current status:

`REPAIRED_INGESTION_COMPLETED_CLEAN__PRODUCT_GROUP_USABLE__NO_LAUNCH`

## Next Required Gate

Before any launch or legacy-source cleanup:

- Treat Gate B-3 feed-source repair as clean for the primary data source `3041760873378113572`.
- Prepare a separate final Pinterest launch/review approval packet if campaign activation is desired.
- Do not use broad `All Products` as the launch scope without a separate exact owner decision; product-group/category scope still needs sales-safe review.
- Decide separately whether the stale Worker SHA header should be updated through a tiny Worker metadata redeploy; do not do that without fresh approval.

Do not launch Pinterest campaigns and do not pause/remove legacy sources without a fresh explicit action-time approval.
