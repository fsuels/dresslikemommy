# Gate B-2 Cloudflare Deploy Readback

Generated: 2026-05-18

Mode: owner-approved Gate B-2 Cloudflare deployment and readback. Cloudflare R2 bucket creation, remote TSV upload, workers.dev subdomain registration, and Worker deploy occurred. Shopify App Proxy configuration did not occur because this repo has no Shopify app project/config and no identified installed app-proxy owner. Pinterest Gate B-3 remains closed.

## Public Worker URL

```text
https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv
```

Health:

```text
https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/health -> 200 {"ok":true}
```

## Cloudflare Writes Executed

Cloudflare account:

```text
[cloudflare account id redacted]
```

Executed:

```bash
npx wrangler@4.86.0 r2 bucket create dlm-pinterest-feeds
npx wrangler@4.86.0 r2 object put dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv --remote --file ../../../dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_unified_all_markets.tsv
PUT /accounts/[cloudflare account id redacted]/workers/subdomain {"subdomain":"dresslikemommy"}
npx wrangler@4.86.0 deploy --config wrangler.deploy.toml
```

Worker deployment:

```text
Worker: dlm-pinterest-feed-worker
Version ID: 2ea90397-a21e-4d11-89fd-999fac93ab29
workers.dev route: enabled
workers.dev account subdomain: dresslikemommy
R2 bucket: dlm-pinterest-feeds
R2 object: pinterest/pinterest_unified_all_markets.tsv
REQUIRE_SHOPIFY_PROXY_SIGNATURE: false
```

The Worker is public because the Shopify app-proxy owner/config is not yet available. The served file contains product catalog feed rows only and prior guards show no customer/order/payment/credential/vendor-source data.

## Feed Readback

Command shape:

```bash
curl -sSL -D /tmp/dlm-pinterest-feed-headers.txt \
  -o /tmp/dlm-pinterest-feed-readback.tsv \
  'https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv'
```

Response:

```text
HTTP/2 200
Content-Type: text/tab-separated-values; charset=utf-8
Content-Length: 151559047
Cache-Control: public, max-age=86400
X-Content-Type-Options: nosniff
X-DLM-Feed-Rows: 41814
X-DLM-Feed-SHA256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7
```

Body:

```text
SHA-256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7
Lines: 41815 = 1 header + 41814 data rows
Bytes: 151559047
Rows parsed: 41814
Unique IDs: 41814
Duplicate IDs: 0
Missing required columns: 0
Missing item_group_id: 0
Missing image_link: 0
Supplier/source host hits: 0
```

R2 remote object SHA readback:

```text
npx wrangler@4.86.0 r2 object get dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv --remote --pipe | shasum -a 256
8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7
```

Method guard:

```text
POST /pinterest-feed.tsv -> 405
Allow: GET
{"error":"method_not_allowed"}
```

## Not Done

- Shopify App Proxy was not configured.
- `https://www.dresslikemommy.com/apps/pinterest-feed.tsv` does not yet exist from this run.
- Pinterest Catalogs were not configured.
- No legacy Pinterest feeds were paused or removed.
- No Pinterest campaign/ad/ad group/audience/budget/bid/status/tag/CAPI/billing write occurred.
- No Shopify product/variant/inventory/price/collection/market/policy/theme write occurred.
- No Merchant, Google Ads, GA4/GTM, or Google & YouTube write occurred.

## Remaining Gate B-2 Work

Identify the Shopify app that owns or should own the app proxy, then configure:

```toml
[app_proxy]
url = "https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv"
subpath = "pinterest-feed"
prefix = "apps"
```

Shopify app proxy subpaths cannot contain periods, so the storefront URL should likely be:

```text
https://www.dresslikemommy.com/apps/pinterest-feed
```

If Pinterest requires a `.tsv` suffix, use direct Worker URL for Gate B-3 or configure the Shopify app proxy root at `/apps/pinterest-feed` and test whether Shopify forwards child paths such as `/apps/pinterest-feed/pinterest-feed.tsv`.

## Current Gate Decision

The direct Cloudflare hosted feed is live and verified. Shopify App Proxy is still pending. Gate B-3 should stay closed unless the owner explicitly approves using the verified Cloudflare Worker URL directly as the Pinterest catalog source.
