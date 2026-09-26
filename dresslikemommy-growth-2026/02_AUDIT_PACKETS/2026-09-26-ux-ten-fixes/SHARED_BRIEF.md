# UX ten-fix program — shared brief for all lanes (2026-09-26)

Repo: `/Users/fsuels/Projects/dresslikemommy` (Dawn-derived Shopify theme; GitHub `main` syncs to live theme MAIN `133290917985`). Live site: https://www.dresslikemommy.com. 21 storefront languages. Parent session: "Website UX recommendations" (Claude Code root). The parent is the only committer and the only editor of `layout/theme.liquid`.

## Why

The owner asked to fix 10 UX issues from a live audit on 2026-09-26. A peer session ("Website design recommendations", claim `Storefront visual polish (16-issue audit)` in `ops/AGENT_COORDINATION.md`) already holds an ACTIVE_WRITE_CLAIM on the homepage, hero, category tiles, product cards/price, PDP (`sections/main-product.liquid`, `snippets/pdp-*.liquid`, `snippets/buy-buttons.liquid`, `snippets/product-media-gallery.liquid`, `assets/section-main-product.css`) and footer files. Its lanes cover issues 2, 6, 7, 8, 9 and the PDP half of 10. **Never write any file in that claim.** This program takes the remaining work in new or unclaimed files.

## Lanes (write ONLY your own files; read anything)

- **H — Halloween/holiday order-by**: new `assets/dlm-holiday-order-by.js`, new `ops/tests/test_holiday_order_by.mjs`, packet folder `lanes/holiday/`.
- **F — Family builder (add several family members at once)**: new `assets/dlm-family-builder.js`, new `assets/dlm-family-builder.css`, new `snippets/dlm-family-builder.liquid` (optional), new `ops/tests/test_family_builder.mjs`, packet folder `lanes/family-builder/`.
- **C — Cart recommendations truthfulness**: `sections/main-cart-items.liquid`, `snippets/cart-drawer.liquid` (recommendation block only), packet folder `lanes/cart/`.
- **D — Description cleanup and sort-order packets (read-only)**: packet folder `lanes/descriptions/` only. No theme files.

If you need a change in `layout/theme.liquid` or in a peer-claimed file, write the exact patch (file, anchor line, inserted text) into your lane's `INTEGRATION.md`. The parent applies it after the peer releases its claim.

## Hard rules

- Never edit `locales/*.json`, `ops/AGENT_WORKLOG.md`, `ops/AGENT_COORDINATION.md`, `ops/PROBLEM_TRACKER.md`, `snippets/jsonld-seo.liquid`, or any peer-claimed file. Never run `git add/commit/push/stash/reset/checkout/restore`.
- No external writes: no Shopify Admin mutations, theme push/upload, product/collection/menu/translation/feed/ad changes, and no live add-to-cart (it fires ad pixels and pollutes conversion data). Read-only Storefront JSON (`/products/<h>.js`, `/collections/<h>/products.json`) and read-only Admin GraphQL queries are fine. The token is in `~/.config/dresslikemommy/admin-api-token.json`; never print, log or copy it.
- Customer truth: dropshipping store with no physical store or stocked inventory. No unsupported claims about stock, warehouses, reviews, ratings, bestsellers, popularity or discounts. Delivery timing is always an **estimate** from the storefront's own 12–16 day window.
- Translations: any new customer-visible text must work in all 21 storefront languages (en, es, fr, de, it, nl, pt, da, sv, no/nb, pl, fi, cs, ro, el, hu, ja, ko, zh, tr, and the rest listed in `snippets/hero-seasonal-copy.liquid`). Prefer no new text or existing translated locale keys. When new text is unavoidable, inline translations keyed by language (see `snippets/hero-seasonal-copy.liquid` for Liquid and `assets/dlm-delivery-dates.js` for JS locale handling). Unknown language falls back to English.
- Dawn conventions: presentation-only Liquid, vanilla ES5-safe JS (no build step), CSS scoped to your component, progressive enhancement (the page must still work if your JS fails).
- Accessibility: real buttons/labels, visible focus, `aria-live` for dynamic totals/messages, 44px touch targets, no horizontal scroll at 320–1440px.

## Tooling

- Node: Homebrew node is broken. Use `source ~/.nvm/nvm.sh && nvm use 20` (or 22 via nvm).
- `shopify theme check` from the repo root: 0 new offenses in your files. `git diff --check` clean. `node --check` every JS file you touch. Node tests with `node --test`.
- Local render harness precedent: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-25-seasonal-homepage-hero/tools/`. You may inject your script into a saved copy of a live page in the built-in or headless browser for a visual check.

## Report back (under ~300 words)

Files changed; what you changed and how you verified it (IMPLEMENTED / VERIFIED / FAILED / BLOCKED / SKIPPED / NOT RUN); exact integration patches or admin approval packets needed; residual risks.
