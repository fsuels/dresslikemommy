# Path B — Primary Fix Plan (Shopify App Proxy + Pinterest Data Feed Source)

Generated: 2026-05-15
Mode: repo-local plan only. No live writes. No Shopify, Pinterest, Merchant, Google Ads, theme, billing, product, feed, source, tag, CAPI, audience, campaign, or budget mutation yet.

## Why this exists

The Shopify Pinterest sales-channel Settings UI does not expose a variant-submission grouping toggle, image-source toggle, or additional-images control (see `PATH_A_NOT_AVAILABLE_FINDING.md`). Path A is not available.

Path B is the only viable fix: generate a properly grouped Pinterest catalog feed (`item_group_id` on every row, `image_link` pinned to the parent product's featured image), host it under our control, and configure Pinterest's catalog to ingest it.

## Owner-confirmed choices (this session)

1. **Feed hosting:** Shopify app proxy. Pinterest will fetch the feed from `https://www.dresslikemommy.com/apps/<proxy_handle>/pinterest-feed.tsv`. No external vendor required.
2. **Legacy 19 feeds (US (en/fr/es/ja/it/nl/de/ar/pl/cs/da/fi/el/he/hi/ko/no/ro/pt-BR)):** leave active until the new feed produces a clean readback, then pause them at Pinterest's catalog manager.
3. **Per-market coverage:** since Pinterest currently treats every entry as `US/USD`, the new feed bundles every active Shopify Market (`us`, `canada`, `united-kingdom`, `eu`, `australia`, `international`) and every product category into one Pinterest catalog source with proper `country` / `language` columns per row.
4. **Save authority:** the human (Francisco) performs every live save in Shopify Admin and Pinterest catalog manager. No AI clicks Save, Publish, Apply, Enable, Disconnect, Reset, Pause, or Create.

## Required components

### 1. Feed generator (already exists)

`ops/scripts/generate_pinterest_feed_grouped.py` reads Shopify Admin GraphQL (read-only) and emits a Pinterest-compatible TSV with `item_group_id` on every row, `image_link` = parent featured image, vendor/supplier-URL leakage blocked, and an internal abort if any row lacks `item_group_id`. The script already supports `--market <handle>` for per-market output; for the unified Pinterest catalog we will call it once per market and concatenate with a `country`/`language` column injected per row.

A new wrapper `ops/scripts/build_pinterest_unified_feed.py` (TBD) will:

- Call the generator for each market in turn.
- Inject `country` and `language` columns appropriate for each market and language.
- Merge into a single TSV at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-pinterest-feed-grouping-all-markets-fix/feeds/pinterest_unified_all_markets.tsv`.
- Generate a SHA-256 checksum and row-count summary JSON.

### 2. Shopify app proxy endpoint (new theme/app component, requires explicit owner approval)

A minimal Shopify private app with one app-proxy route:

- Public URL: `https://www.dresslikemommy.com/apps/<proxy_handle>/pinterest-feed.tsv`
- Handler: streams the latest committed feed TSV with appropriate `Content-Type: text/tab-separated-values` and `Cache-Control: max-age=86400` headers.
- Auth: Pinterest fetches unauthenticated; the proxy MUST refuse any non-GET method and MUST return only the feed file, no other data.

Implementation can be either (a) a tiny Node/Express server hosted on existing infra, or (b) a Liquid/Shopify app that serves the file via the existing storefront. Both are repo-local until owner approves the deploy.

**Stop conditions during proxy setup:**
- The app cannot request scopes beyond `read_products` (and only if not already covered by existing tokens).
- The proxy MUST NOT read or expose any customer, order, billing, credential, or vendor/source URL data.
- The proxy MUST NOT mutate any Shopify data.

### 3. Pinterest catalog source configuration (Pinterest-side, requires explicit owner approval)

In Pinterest Catalogs:

- Add a new data feed source pointing at `https://www.dresslikemommy.com/apps/<proxy_handle>/pinterest-feed.tsv`.
- Schedule daily fetch.
- Map columns explicitly (do not rely on auto-detection).
- Once the new source ingests cleanly and the catalog shows grouped products, pause the 19 legacy auto-emitted feeds at Pinterest's "Product feed status" page.

**Stop conditions during Pinterest config:**
- Do not change ad account, billing, tag, CAPI, audience, campaign, budget, bid, or status.
- Do not click "Disconnect all" on the Shopify channel.
- Do not click "App reset".
- Do not pause the 19 legacy feeds until the new source has a clean readback.

## Sequenced approval gates

This pivot replaces the single Path A master phrase with three smaller gates so each step is independently verifiable:

### Gate B-1 — Generate feed locally

Exact approval phrase:

```
I approve generating the Pinterest unified feed locally for read-back only. Run ops/scripts/generate_pinterest_feed_grouped.py read-only against Shopify Admin GraphQL for every active Shopify Market (us, canada, united-kingdom, eu, australia, international), then build_pinterest_unified_feed.py to merge with country/language columns. No Shopify product, channel, feed, or theme write. No Pinterest write. Output stays in the repo evidence folder only.
```

What this authorizes: read-only Admin GraphQL calls plus local TSV file creation. Nothing leaves the local machine.

### Gate B-2 — Deploy Shopify app proxy

Exact approval phrase to be drafted **after** Gate B-1 produces a verified clean TSV. Will cover: app creation under the operator-managed Shopify integration, proxy route registration, scope `read_products` only, deploy of the file-streaming handler, smoke test that the proxy returns the TSV with correct content-type and only over GET.

### Gate B-3 — Add Pinterest catalog source and pause legacy

Exact approval phrase to be drafted **after** Gate B-2 produces a working proxy URL. Will cover: Pinterest catalog source creation pointing at the proxy URL, scheduled fetch, column mapping, 24h re-sync wait, before/after readback, then pause of the 19 legacy auto-emitted feeds at Pinterest.

### Gate B-4 — Flip continuity guardrail to strict

After Gate B-3 readback confirms grouped products: replace the contents of `FIX_LANDED_FRESHNESS_MARKER.txt` with the attest phrase + per-market readback summaries. From the next session forward, any per-variant regression in any feed snapshot fails the strict continuity gate.

## Acceptance criteria for Path B

- `ops/scripts/check_pinterest_feed_grouping.py --strict` returns PASS against the generated Path B feed AND against any current/future Pinterest catalog snapshot.
- Pinterest catalog shows variants grouped under one parent product per `item_group_id`.
- `image_link` on every row is the parent product's featured image.
- The "Dresses" group entry count in Pinterest drops from the owner-reported 157 to roughly 14-25 parent products.
- All 6 active Shopify Markets covered.
- No live Pinterest campaign, ad, audience, tag, CAPI, conversion, budget, bid, or status was changed in any of the four gates.
- AGENTS.md / CLAUDE.md Non-Negotiable rule preserved byte-identical.
- Automated guardrail wired into `--strict` continuity remains wired.

## What this plan does NOT touch

- No Shopify Admin product / title / price / inventory / vendor / type / policy edit.
- No theme push beyond the optional minimal app-proxy handler (gated by Gate B-2).
- No edits to other sales channels (Google & YouTube, Facebook & Instagram, TikTok).
- No Merchant Center source / feed / language / currency change.
- No Google Ads / Pinterest campaign / ad / audience / billing / scope change.
- No destructive filesystem action, no credential persistence in the repo, no vendor/source URL leakage.

## Current status

- Gate B-1: complete locally as of 2026-05-17 11:42 EDT. Evidence: `GATE_B1_UNIFIED_FEED_READBACK.md`, `feeds/pinterest_unified_all_markets.tsv`, `feeds/pinterest_unified_all_markets.summary.json`, and `feeds/pinterest_unified_all_markets.sha256`.
- Gate B-2: next approval gate. Draft and approve the Shopify app-proxy/file-hosting implementation before any deploy or public URL exposure.
- Gates B-3 and B-4: blocked on B-2 completing cleanly.
