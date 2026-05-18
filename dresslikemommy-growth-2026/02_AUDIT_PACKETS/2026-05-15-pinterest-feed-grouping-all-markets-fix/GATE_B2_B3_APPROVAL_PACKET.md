# Gate B-2 / B-3 Approval Packet — Pinterest Unified Feed Hosting And Catalog Source

Generated: 2026-05-17

Mode: approval packet only. No live writes authorized by this document itself.

## Current Prerequisite State

Gate B-1 is complete locally:

- Unified feed: `feeds/pinterest_unified_all_markets.tsv`
- Summary: `feeds/pinterest_unified_all_markets.summary.json`
- Checksum: `feeds/pinterest_unified_all_markets.sha256`
- Rows: `41,814`
- Unique item IDs: `41,814`
- Missing `item_group_id`: `0`
- Missing `image_link`: `0`
- Parent-image drift groups: `0`
- Supplier/source host hits: `0`
- SHA-256: `8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7`

This does **not** mean Pinterest is fixed live. The old upstream/live-equivalent snapshots still fail until a hosted grouped feed is ingested and read back clean.

## Gate B-2 — Shopify App-Proxy / File Hosting

Goal: make the verified unified TSV available at a stable Dress Like Mommy URL for Pinterest fetches, without exposing customer/order/payment/credential/vendor-source data and without mutating product data.

Recommended implementation after owner hosting question: Cloudflare R2 plus a Cloudflare Worker, with Shopify App Proxy in front of the Worker. Repo-local readiness lives at `GATE_B2_CLOUDFLARE_WORKER_READINESS.md` and `ops/cloudflare/pinterest-feed-worker/`.

2026-05-18 update: the direct Cloudflare Worker URL is deployed and verified in `GATE_B2_CLOUDFLARE_DEPLOY_READBACK.md`. Shopify App Proxy is still pending because no Shopify app config/app owner exists in this repo.

Proposed public URL:

```text
https://www.dresslikemommy.com/apps/<proxy_handle>/pinterest-feed.tsv
```

Minimum implementation requirements:

- Serve only `GET` requests.
- Return only the unified TSV bytes, with no customer/order/admin data.
- If using Cloudflare, store the TSV in R2 and keep `SHOPIFY_APP_PROXY_SECRET` only as a Cloudflare Worker secret.
- Set `Content-Type: text/tab-separated-values; charset=utf-8`.
- Set a cache policy no longer than one day.
- Verify SHA-256 after deploy matches `8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7`.
- If any Shopify app scope is needed, it must be no broader than `read_products`; do not request order/customer/payment/billing scopes.
- Do not change Shopify products, variants, inventory, prices, collections, markets, policies, theme, Google & YouTube, Pinterest channel settings, or Merchant feeds as part of this gate.

Exact Gate B-2 approval phrase:

```text
I approve Gate B-2 only: prepare and deploy the minimal Shopify app-proxy or equivalent Dress Like Mommy hosted file endpoint for the already verified local file feeds/pinterest_unified_all_markets.tsv, available as a GET-only TSV URL for Pinterest. The endpoint must serve only that feed, expose no customer/order/payment/credential/vendor-source data, request no scope broader than read_products if a scope is required, and must not change Shopify products, variants, inventory, prices, collections, markets, policies, theme, Pinterest catalog/source/feed/product-group/campaign/budget/bid/status/tag/CAPI/audience/billing, Merchant, Google Ads, GA4/GTM, or Google & YouTube settings. Capture before/after readback including URL, content type, status code, row count, item_group_id count, image_link count, supplier/source host scan, and SHA-256.
```

Stop conditions:

- Any prompt asks to create billing, change subscription, approve charges, broaden scopes, disconnect/reset apps, publish theme changes, or alter products/feed/source settings. If Cloudflare requires a payment method or plan decision, stop for owner action.
- The hosted URL returns anything except the intended TSV.
- The deployed file checksum differs from Gate B-1 unless a fresh local readback explains and verifies the change.

## Gate B-3 — Pinterest Catalog Source Configuration

Goal: configure Pinterest Catalogs to ingest the hosted grouped TSV and only later pause legacy auto-emitted feeds after clean readback.

Eligible hosted URL options:

- Preferred final storefront URL after Shopify App Proxy exists: `https://www.dresslikemommy.com/apps/<proxy_handle>`.
- Currently verified direct Cloudflare URL: `https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv`.

Use the direct Cloudflare URL for Gate B-3 only if the owner explicitly approves that URL as the catalog source.

Required before-state readback:

- Pinterest advertiser/account: `549756244483`.
- Current legacy feed/source list and statuses.
- Current product counts and grouped/duplicated product evidence.
- Confirm no campaign/budget/bid/status/tag/CAPI/audience/billing action is in scope.

Exact Gate B-3 approval phrase:

```text
I approve Gate B-3 only: in Pinterest Catalogs for advertiser 549756244483, add or configure a catalog data feed source pointing to the verified Dress Like Mommy hosted TSV URL from Gate B-2, map the required columns explicitly including id, item_group_id, title, description, link, image_link, availability, price, brand, condition, product_type, market_handle, country, and language, schedule the feed fetch, and capture before/after readbacks. Do not launch, save, enable, pause, or edit any Pinterest campaign/ad/ad group/audience/budget/bid/status/tag/CAPI/billing. Do not pause or remove the 19 legacy Shopify/Pinterest feeds until the new source has ingested cleanly and the grouped catalog readback passes after sync.
```

Stop conditions:

- Pinterest requests billing, campaign launch, tag/CAPI setup, audience changes, or account changes.
- The source preview shows `0` products after the expected fetch/update window without an explainable transient status.
- The feed parser rejects `item_group_id` or drops parent `image_link`.
- Pinterest tries to auto-map columns in a way that omits `item_group_id`; stop and require an explicit mapping readback.

## Gate B-4 — Freshness Marker Attest

Only after Gate B-3 has synced and after-state readback proves grouped products:

1. Capture catalog row/product counts.
2. Confirm `item_group_id` exists on every ingested row.
3. Confirm parent featured image is used as `image_link`.
4. Confirm no new severe disapprovals.
5. Replace `FIX_LANDED_FRESHNESS_MARKER.txt` with the required attest phrase and readback summary.
6. Run:

```bash
python3.13 ops/scripts/check_pinterest_feed_grouping.py --strict
python3.13 ops/scripts/check_continuity_integrity.py --strict
```

Until Gate B-4 passes, the live blocker remains open.
