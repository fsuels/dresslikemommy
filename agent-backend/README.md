Agent Backend (App Proxy) – Product Finder L1→L2

What this is
- A minimal Express server to back the theme’s product-finder widget (`assets/agent.js`).
- Safe for Shopify: no secrets in theme; cart remains client-side; LM/tools run here.

Env vars
- PORT (default 3000)
- SHOPIFY_STORE_DOMAIN (e.g., myshop.myshopify.com)
- SHOPIFY_STOREFRONT_TOKEN (Storefront API public token)
- SHOPIFY_APP_PROXY_SECRET (App secret for verifying App Proxy signatures) – TODO wire verify
- PINTEREST_FEED_TSV_PATH (optional; defaults to the repo-local unified Pinterest TSV)
- PINTEREST_FEED_SHA256 (optional; defaults to the current Gate B-1 verified checksum)

Run locally
1) `cd agent-backend && npm i`
2) Create `.env` with the vars above.
3) `npm run dev`

Deploy
- Host on your platform of choice (Render/Vercel/Cloud Run/etc.).
- Configure Shopify App Proxy in your custom app to point to `/apps/agent/chat`.
- For the Pinterest grouped feed, configure a separate Shopify App Proxy path that maps to `/apps/<proxy_handle>/pinterest-feed.tsv`.
- Preferred Pinterest hosting path as of Gate B-2 follow-up: use `ops/cloudflare/pinterest-feed-worker/` with Cloudflare R2 plus a Worker, then put Shopify App Proxy in front of the Worker URL. Keep this Express endpoint as the local fallback/readback implementation unless `agent-backend` gets a real deployment target.
- Do not configure the Pinterest catalog source until the hosted URL returns `200`, `Content-Type: text/tab-separated-values; charset=utf-8`, the expected row count, and the Gate B-1 SHA-256.
- Current repo status: this endpoint is implemented and verified locally, but no deployment target config is checked in for `agent-backend`.

Contract
- See ops/AGENT_PROXY_SPEC.md
