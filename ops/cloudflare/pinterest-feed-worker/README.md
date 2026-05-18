# Pinterest feed Worker

This is the local, install-ready Cloudflare path for Gate B-2. It serves the already verified unified Pinterest TSV from R2 through a tiny GET-only Worker.

It does not create Cloudflare resources, upload files, configure Shopify, configure Pinterest, or change live product/catalog/campaign state by itself.

## Files

- `src/worker.js` - feed-only Cloudflare Worker.
- `wrangler.toml.example` - safe template; copy outside the repo or to a local untracked `wrangler.toml` before deployment.
- `test/worker.test.mjs` - Node test coverage for GET, 405, and optional Shopify app-proxy signature verification.

## Intended public path

Pinterest should eventually fetch the Shopify app-proxy URL:

```text
https://www.dresslikemommy.com/apps/pinterest-feed.tsv
```

Shopify should proxy that path to the Cloudflare Worker. The Worker should read this R2 object:

```text
dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv
```

## Local verification

```bash
cd ops/cloudflare/pinterest-feed-worker
npm install
npm test
```

## Deployment checklist

These commands are intentionally owner/operator steps because they write to Cloudflare:

```bash
cd ops/cloudflare/pinterest-feed-worker
cp wrangler.toml.example wrangler.toml
npx wrangler login
npx wrangler r2 bucket create dlm-pinterest-feeds
npx wrangler r2 object put dlm-pinterest-feeds/pinterest/pinterest_unified_all_markets.tsv \
  --remote \
  --file ../../../dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_unified_all_markets.tsv
npx wrangler deploy
```

Only set `SHOPIFY_APP_PROXY_SECRET` and switch `REQUIRE_SHOPIFY_PROXY_SIGNATURE` to `true` after the Shopify app proxy is identified and ready to sign requests.

After deployment, configure the Shopify custom app proxy so the storefront path points to the Worker feed path. Then verify the public Shopify URL before Gate B-3:

```bash
curl -sSL -D /tmp/dlm-pinterest-feed-headers.txt -o /tmp/dlm-pinterest-feed.tsv 'https://www.dresslikemommy.com/apps/pinterest-feed.tsv'
curl -sL 'https://www.dresslikemommy.com/apps/pinterest-feed.tsv' | shasum -a 256
```

Required readback:

- HTTP `200`.
- `Content-Type: text/tab-separated-values; charset=utf-8`.
- `X-DLM-Feed-SHA256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7`.
- `X-DLM-Feed-Rows: 41814`.
- Body SHA-256 matches `feeds/pinterest_unified_all_markets.sha256`.
- Non-GET request returns `405` with `Allow: GET`.

Gate B-3 remains separate. Do not configure Pinterest Catalogs until the hosted Shopify URL passes the readback above.

## Current deployed URL

Gate B-2 Cloudflare deployment currently serves:

```text
https://dlm-pinterest-feed-worker.dresslikemommy.workers.dev/pinterest-feed.tsv
```

Shopify App Proxy is still pending because the repo has no `shopify.app.toml` or identified installed app-proxy owner.
