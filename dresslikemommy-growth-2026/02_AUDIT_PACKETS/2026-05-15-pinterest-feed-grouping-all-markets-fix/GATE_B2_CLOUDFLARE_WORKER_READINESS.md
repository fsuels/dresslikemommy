# Gate B-2 Cloudflare Worker Readiness

Generated: 2026-05-18

Mode: repo-local implementation only. No Cloudflare resource creation, R2 upload, Worker deploy, Shopify app-proxy configuration, Pinterest catalog/source configuration, campaign change, product/feed mutation, billing action, credential persistence, or external write occurred.

## Decision

The preferred free/low-cost hosting path is Cloudflare R2 plus Cloudflare Workers, with Shopify App Proxy in front of it:

```text
Pinterest -> https://www.dresslikemommy.com/apps/pinterest-feed.tsv -> Shopify App Proxy -> Cloudflare Worker -> Cloudflare R2 TSV object
```

This is preferred over:

- Local Mac hosting, because Pinterest needs a stable public HTTPS URL and the Mac would need to stay online, awake, routable, and secure.
- The existing `agent-backend` deployment path, because no deploy target config exists in the repo and the unified feed is large enough that object storage is a cleaner fit.
- A public Shopify App Store app, because this can be a private/custom app-proxy setup for Dress Like Mommy only.

## What Changed Locally

Added a self-contained Cloudflare Worker package:

- `ops/cloudflare/pinterest-feed-worker/package.json`
- `ops/cloudflare/pinterest-feed-worker/package-lock.json`
- `ops/cloudflare/pinterest-feed-worker/wrangler.toml.example`
- `ops/cloudflare/pinterest-feed-worker/src/worker.js`
- `ops/cloudflare/pinterest-feed-worker/test/worker.test.mjs`
- `ops/cloudflare/pinterest-feed-worker/README.md`

Worker behavior:

- Serves `GET /pinterest-feed.tsv` and any path ending `/pinterest-feed.tsv`.
- Rejects non-GET feed requests with `405` and `Allow: GET`.
- Streams the configured R2 object without calling Shopify, Pinterest, Merchant, Google Ads, GA4/GTM, or any external API.
- Sets `Content-Type: text/tab-separated-values; charset=utf-8`.
- Sets `Cache-Control: public, max-age=86400`.
- Sets `X-DLM-Feed-SHA256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7`.
- Sets `X-DLM-Feed-Rows: 41814`.
- Supports optional Shopify app-proxy signature verification with the secret held only in Cloudflare Worker secrets as `SHOPIFY_APP_PROXY_SECRET`.

## Local Verification

Commands:

```bash
node --check ops/cloudflare/pinterest-feed-worker/src/worker.js
cd ops/cloudflare/pinterest-feed-worker && npm test
cd ops/cloudflare/pinterest-feed-worker && npm audit --audit-level=moderate
```

Results:

```text
node --check: passed
npm test: 4 tests passed
npm audit: 0 vulnerabilities
```

Test coverage:

- Successful TSV response includes the Pinterest audit headers.
- Non-GET request returns `405`.
- Shopify app-proxy signature verification can pass with the expected HMAC.
- Signature-required mode fails closed when the signature is absent.

## Owner/Operator Deployment Steps

These steps are intentionally not run by automation because they write to Cloudflare and require account/billing/session authority:

```bash
cd ops/cloudflare/pinterest-feed-worker
cp wrangler.toml.example wrangler.toml
npx wrangler login
npx wrangler r2 bucket create dlm-pinterest-feeds
npx wrangler r2 object put dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv \
  --file ../../../dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_unified_all_markets.tsv
npx wrangler secret put SHOPIFY_APP_PROXY_SECRET
npx wrangler deploy
```

Then configure the Shopify custom app proxy so:

```text
https://www.dresslikemommy.com/apps/pinterest-feed.tsv
```

proxies to the deployed Worker feed path.

## Required Public Readback Before Gate B-3

The public Shopify URL must prove:

- HTTP `200`.
- `Content-Type: text/tab-separated-values; charset=utf-8`.
- `X-DLM-Feed-SHA256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7`.
- `X-DLM-Feed-Rows: 41814`.
- Body row count: `41,814`.
- Body SHA-256 matches `feeds/pinterest_unified_all_markets.sha256`.
- `0` missing `item_group_id`.
- `0` missing `image_link`.
- `0` supplier/source host hits.
- Non-GET request returns `405` with `Allow: GET`.

Gate B-3 remains closed until that public readback passes.

## Deploy Attempt Status

2026-05-18 owner-approved deploy attempt stopped before live writes because Cloudflare auth is absent, default Wrangler OAuth requests broad unrelated scopes, and this repo has no Shopify app TOML/config for app-proxy configuration.

Evidence: `GATE_B2_DEPLOY_ATTEMPT_BLOCKED_AUTH_READBACK.md`.

2026-05-18 follow-up: after owner enabled R2, the direct Cloudflare Worker URL was deployed and verified. Evidence: `GATE_B2_CLOUDFLARE_DEPLOY_READBACK.md`.

Remaining blocker: Shopify App Proxy is not configured because this repo has no Shopify app TOML/config or identified installed app-proxy owner.
