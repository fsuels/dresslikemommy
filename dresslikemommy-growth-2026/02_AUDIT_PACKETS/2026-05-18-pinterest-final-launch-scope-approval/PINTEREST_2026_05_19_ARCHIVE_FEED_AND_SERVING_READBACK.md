# Pinterest Archive Feed And Serving Readback

Timestamp: 2026-05-19 07:25 EDT.

Scope: read-only Shopify Admin feed generation, public Cloudflare Worker readback, and authenticated Pinterest reporting/catalog readback after the owner archived a group of previously active Shopify listings and reported seeing `0` impressions.

## Answer

The Cloudflare/Pinterest feed does not automatically rebuild from Shopify archived-product changes.

Pinterest automatically re-fetches the configured URL every day, but the URL currently serves a static R2 object:

```text
https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv
```

That object remains stale until a current-active TSV is regenerated, verified, uploaded to R2, and Pinterest reingests it.

## Worker And Pinterest Source Readback

Public Worker body readback:

- Body SHA-256: `809d48e96832ffc4db8a30de685250273412c2988678b5364d48c627699e8863`
- Body rows: `41,814` data rows / `41,815` lines including header
- Status: still serving the previously approved repaired feed
- Note: response header still advertises older `X-DLM-Feed-SHA256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7`, but the body hash is the repaired `809d48...` file Pinterest ingests.

Pinterest source `3041760873378113572` readback:

- Source name: `DLM Cloudflare Grouped Feed 2026-05-18`
- Source URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
- Current ingestion: `Completed`
- Product count: `41,814`
- Completed at: `May 19 at 3:03 AM EDT`
- Successful uploads: `41,814`
- Failed: `0`
- Warnings: `0`
- Images: `Completed`
- Next scheduled update: `May 20 at 3:00 AM EDT`

This proves Pinterest reingested the hosted URL today, but it pulled the old static object because R2 was not replaced after the Shopify archive work.

## Current-Active Local Feed Candidate

Read-only Shopify Admin generation after the archive changes:

- Current U.S. generated feed: `4,687` rows / `223` parent products
- Old U.S. hosted feed: `6,969` rows / `326` parent products
- Net current-active difference: `104` old parent products removed and `1` new parent product added relative to the hosted U.S. feed.

Current local all-market replacement candidate in `/tmp`:

- File: `/tmp/dlm_pinterest_unified_current_20260519.tsv`
- SHA-256: `789b85804c01126885fae1ac791d28101b8e04eee39a94f77ce93cd6b1ae5efd`
- Data rows: `28,122`
- Lines including header: `28,123`
- Per market: `4,687` rows and `223` parent groups for `us`, `canada`, `united-kingdom`, `eu`, `australia`, and `international`
- Duplicate item IDs: `0`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Parent image drift groups: `0`
- Supplier/source host hits: `0`

Exact launched product group impact from the archive changes:

| Group | Old selected variant IDs | Current active IDs still present | Missing after archive |
|---|---:|---:|---:|
| `DLM_PIN_US_SHOPPING_MOMMY_ME_333` | 201 | 166 | 35 |
| `DLM_PIN_US_SHOPPING_FAMILY_MATCHING_333` | 103 | 103 | 0 |
| `DLM_PIN_US_SHOPPING_PAJAMAS_333` | 29 | 29 | 0 |

## Pinterest Serving Readback

Authenticated Pinterest reporting readback for campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518` / ID `626758581530`:

For `Today` / `2026-05-19` UTC:

- Campaign status: `Active`
- Currently being served: `1`
- Spend: `$2.67`
- Impressions: `1,272`
- Pin clicks: `19`
- Outbound clicks: `19`
- CTR: `1.49%`
- CPC: `$0.14`
- Actions: `0`

Ad group `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518` / ID `2680090307739` today:

- Status: `Active`
- Currently being served: `1`
- Spend: `$2.67`
- Impressions: `1,272`
- Pin clicks: `19`
- Outbound clicks: `19`
- CTR: `1.49%`
- CPC: `$0.14`
- Bid column: `$0.15`

Ads tab:

- `0 ads`
- `0 currently being served`
- No ad rows

Product groups tab:

- The ad group still lists the three exact groups.
- Product-group reporting returned `0` product-group-level spend/impression/click rows, while campaign/ad-group reporting shows serving. Treat this as a Pinterest reporting-surface inconsistency until a later readback clarifies attribution.

## Assessment

The owner-visible `0 impressions` view was likely a reporting/filter/date-range issue. Current authenticated Pinterest reporting shows delivery has started and is spending.

This is still not an expert-finished state:

- The hosted Cloudflare feed is stale after Shopify archives.
- The campaign is spending before the stale feed is repaired.
- The ad group bid column reads `$0.15`, not the owner-reported `$0.10`.
- The ads tab still shows `0 ads`.
- Product-group reporting does not attribute the visible campaign/ad-group delivery to the exact groups, even though those groups remain attached.
- No purchase actions or ROAS are visible yet.

## Recommended Next Step

Stop guessing from the UI. The cleanest next move is:

1. Replace only the Cloudflare R2 object with the locally verified current-active TSV.
2. Keep the same Worker URL.
3. Trigger or wait for Pinterest source `3041760873378113572` to reingest.
4. Read back the source product count and exact group usability.
5. Then read campaign/ad group/product-group/ad delivery again before changing bids, budgets, ads, keywords, negatives, audiences, or product groups.

## Approval Phrase

Use this exact phrase only if you want the live feed repair executed:

```text
I approve replacing Cloudflare R2 object pinterest/pinterest_unified_all_markets.tsv with the locally verified current-active Pinterest TSV SHA-256 789b85804c01126885fae1ac791d28101b8e04eee39a94f77ce93cd6b1ae5efd, keeping the same Worker URL https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv, then triggering or waiting for Pinterest source 3041760873378113572 to reingest and capturing after-state readback. Do not change Pinterest campaigns/ad groups/ads/product groups/keywords/negative keywords/audiences/budgets/bids/statuses/tag/CAPI/billing, do not pause/remove legacy feeds, and do not mutate Shopify products/theme/app-proxy, Merchant, Google Ads, GA4, or GTM.
```

No external write occurred during this readback.

---

## Approved Execution Readback

Timestamp: 2026-05-19 09:48-10:06 EDT.

Owner instruction in current session approved the exact packet path: replace only the R2 TSV, keep the same Worker URL, trigger/wait for Pinterest reingestion, then read back source + campaign before touching bids, budgets, ads, keywords, negatives, or product groups.

Executed write:

- Replaced Cloudflare R2 object: `dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv`
- Uploaded file: `/tmp/dlm_pinterest_unified_current_20260519.tsv`
- Uploaded SHA-256: `789b85804c01126885fae1ac791d28101b8e04eee39a94f77ce93cd6b1ae5efd`
- Kept Worker URL unchanged: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`

Worker after-state readback:

- HTTP `200`
- `Content-Type: text/tab-separated-values; charset=utf-8`
- `Content-Length: 120341505`
- Body SHA-256: `789b85804c01126885fae1ac791d28101b8e04eee39a94f77ce93cd6b1ae5efd`
- Body lines: `28,123`
- Data rows: `28,122`
- Non-GET guard: POST returned `405` with `Allow: GET`
- Known caveat: Worker metadata headers still show old `X-DLM-Feed-Rows: 41814` and old `X-DLM-Feed-SHA256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7`; the body is correct and is the object Pinterest fetches. This should be repaired in a separate Worker metadata redeploy only if approved.

Pinterest ingestion trigger:

- Source: `3041760873378113572`
- Source URL unchanged: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
- Manual trigger accepted through `Manage ingestion > Trigger ingestion`.
- Pinterest showed confirmation modal `Trigger ingestion?`; confirmed only that expected source action.
- Current source state after trigger:
  - Current ingestion: `Processing`
  - Product count: `-`
  - Images: `Processing`
  - Past ingestion row: `May 19 at 9:48 AM EDT`, status `Processing`, successful uploads `0`, failed `0`, warnings `0`, videos `0`
  - Prior completed row remains `May 19 at 3:03 AM EDT`, `41,814` successful uploads, `0` failed, `0` warnings

Polling performed:

- Multiple source refreshes from approximately 9:49 to 10:06 EDT still showed `Processing`.
- No failed/warning state was visible during polling.
- No second ingestion trigger was attempted.

Campaign readback during source processing:

- Campaign: `DLM_PIN_US_CATALOG_333_EXACT_20260518`
- Campaign ID: `626758581530`
- Date range: Today / `2026-05-19` UTC
- Status: `Active`
- Currently being served: `1`
- Spend: `$4.44`
- Impressions: `2,505`
- Pin clicks: `31`
- Outbound clicks: `31`
- CTR: `1.24%`
- CPC: `$0.14`
- Actions: `0`

Ad group readback during source processing:

- Ad group: `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518`
- Ad group ID: `2680090307739`
- Status: `Active`
- Currently being served: `1`
- Spend: `$4.44`
- Impressions: `2,505`
- Pin clicks: `31`
- Outbound clicks: `31`
- CTR: `1.24%`
- CPC: `$0.14`
- Bid column: `$0.15`

Guardrail confirmation:

- No Pinterest campaign, ad group, ad, product group, keyword, negative keyword, audience, budget, bid, status, tag/CAPI, billing, legacy feed pause/remove, Shopify product/theme/app-proxy, Merchant, Google Ads, GA4, or GTM change occurred.
- The only external write was the approved Cloudflare R2 object replacement plus the approved Pinterest manual ingestion trigger for source `3041760873378113572`.

Next required readback:

1. Poll source `3041760873378113572` until `Completed` or error.
2. Expected clean completion target is approximately `28,122` successful uploads, `0` failed, `0` warnings, images completed.
3. After completion, read back exact product groups and the live campaign/ad group/product-group/ad tabs before making any optimization decision.

### 10:12 EDT Poll Addendum

Source `3041760873378113572` was refreshed again in Pinterest Catalogs:

- Data source URL remains `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`
- Current ingestion: `Processing`
- Product count: `-`
- Images: `Processing`
- Current processing row: `May 19 at 9:48 AM EDT`, status `Processing`, successful uploads `0`, failed `0`, warnings `0`, videos `0`
- Prior completed row remains `May 19 at 3:03 AM EDT`, `41,814` successful uploads, `0` failed, `0` warnings
- Next scheduled update remains `May 20 at 3:00 AM EDT`

Campaign/ad group readback after the 10:12 source poll:

- Campaign `DLM_PIN_US_CATALOG_333_EXACT_20260518` / ID `626758581530`: `Active`, Today UTC spend `$4.44`, `2,505` impressions, `31` Pin clicks, `31 Clicks, 0 Actions`, `$1.772` CPM, `$0.143` CPC, `1.24%` CTR.
- Ad group `DLM_PIN_US_CATALOG_333_EXACT_ADGROUP_20260518` / ID `2680090307739`: `Active`, Today UTC spend `$4.44`, `2,505` impressions, `31` Pin clicks, `$0.143` CPC, `1.24%` CTR.

No Pinterest campaign, ad group, ad, product group, keyword, negative keyword, audience, budget, bid, status, tag/CAPI, billing, legacy feed pause/remove, Shopify product/theme/app-proxy, Merchant, Google Ads, GA4, GTM, or Worker metadata change occurred during this addendum.

Additional 10:15 EDT source refresh still showed the same state: current ingestion `Processing`, product count `-`, images `Processing`, May 19 9:48 AM EDT row `Processing`, successful uploads `0`, failed `0`, warnings `0`, videos `0`.
