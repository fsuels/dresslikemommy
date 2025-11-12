Agent Backend (App Proxy) – Product Finder L1→L2

What this is
- A minimal Express server to back the theme’s product-finder widget (`assets/agent.js`).
- Safe for Shopify: no secrets in theme; cart remains client-side; LM/tools run here.

Env vars
- PORT (default 3000)
- SHOPIFY_STORE_DOMAIN (e.g., myshop.myshopify.com)
- SHOPIFY_STOREFRONT_TOKEN (Storefront API public token)
- SHOPIFY_APP_PROXY_SECRET (App secret for verifying App Proxy signatures) – TODO wire verify

Run locally
1) `cd agent-backend && npm i`
2) Create `.env` with the vars above.
3) `npm run dev`

Deploy
- Host on your platform of choice (Render/Vercel/Cloud Run/etc.).
- Configure Shopify App Proxy in your custom app to point to `/apps/agent/chat`.

Contract
- See ops/AGENT_PROXY_SPEC.md

