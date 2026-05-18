# Gate B-2 Local Endpoint Readback

Generated: 2026-05-17

Mode: local implementation and local verification only. No Shopify app-proxy deploy, Shopify Admin save, Pinterest catalog/source configuration, legacy-feed pause, campaign change, product/feed mutation, billing action, credential persistence, or external write occurred.

## What Was Approved / Executed

The owner said "Do it" for the next live-gated step after Gate B-1. This run advanced Gate B-2 as far as the repo can safely support without an identified hosting/deployment target:

- Implement the GET-only TSV endpoint in the existing `agent-backend` Express app.
- Verify it locally against the Gate B-1 unified feed.
- Stop before deploy/public URL exposure because this repo has no deployment target config for `agent-backend`.

## Repo Discovery

Found existing app-proxy-capable backend:

- `agent-backend/src/index.js`
- `agent-backend/package.json`
- `agent-backend/README.md`

No deployment target config was found under `agent-backend` for Render, Vercel, Cloud Run, Fly, Docker, Procfile, or similar deployment automation.

## What Changed Locally

Added a Pinterest feed endpoint to `agent-backend/src/index.js`:

- `GET /apps/pinterest-feed.tsv`
- `GET /apps/:proxyHandle/pinterest-feed.tsv`
- `GET /pinterest-feed.tsv`

Behavior:

- Streams the verified unified TSV from `feeds/pinterest_unified_all_markets.tsv`.
- Uses `Content-Type: text/tab-separated-values; charset=utf-8`.
- Uses `Cache-Control: public, max-age=86400`.
- Adds `X-DLM-Feed-SHA256`.
- Rejects non-GET methods with `405 Method Not Allowed` and `Allow: GET`.
- Uses existing app-proxy signature verification in production; local development bypass remains unchanged.
- Does not call Shopify, Pinterest, Merchant, Google Ads, GA4/GTM, or any external API when serving the feed.

Updated `agent-backend/README.md` with the new feed env vars and app-proxy path guidance.

## Local Verification

Command:

```bash
PORT=3127 NODE_ENV=development node src/index.js
```

Readback:

```text
GET /apps/pinterest-feed.tsv -> 200 OK
Content-Type: text/tab-separated-values; charset=utf-8
Cache-Control: public, max-age=86400
Content-Length: 151559047
X-DLM-Feed-SHA256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7
Rows: 41814
SHA-256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7
```

Method guard:

```text
POST /apps/pinterest-feed.tsv -> 405 Method Not Allowed
Allow: GET
{"error":"method_not_allowed"}
```

Health check:

```text
GET /health -> {"ok":true}
```

Static checks:

```bash
node --check agent-backend/src/index.js
```

Result: passed.

## Current Status

Gate B-2 is locally implemented and locally verified. It is not deployed and not publicly reachable yet.

Follow-up on 2026-05-18: after the owner asked which option is free and whether this should be local computer, Shopify app, or another app, the preferred deployment path is now Cloudflare R2 plus Cloudflare Worker with Shopify App Proxy in front. See `GATE_B2_CLOUDFLARE_WORKER_READINESS.md` and `ops/cloudflare/pinterest-feed-worker/`.

Blocked live step:

- A specific public hosting/deployment target is required before the public Shopify app-proxy URL can exist. The current recommended target is Cloudflare R2/Worker, not the local Mac.
- After deployment, the operator must configure the Shopify app proxy path in the app/admin surface and capture before/after readback.
- Gate B-3 remains separate and closed until the hosted URL returns a verified `200` TSV response with the Gate B-1 SHA-256.

## Next Exact Gate

Deploy/readback Gate B-2 only after the hosting target is identified:

```text
I approve deploying the existing agent-backend Pinterest feed endpoint to the selected hosting target and configuring the Shopify app-proxy path to the deployed GET-only endpoint. Do not change Pinterest catalog/source/feed/product-group/campaign/budget/bid/status/tag/CAPI/audience/billing. Do not change Shopify products, variants, inventory, prices, collections, markets, policies, theme, Merchant, Google Ads, GA4/GTM, or Google & YouTube settings. Capture the public URL, status code, content type, row count, item_group_id count, image_link count, supplier/source host scan, SHA-256, and method-guard readback.
```
