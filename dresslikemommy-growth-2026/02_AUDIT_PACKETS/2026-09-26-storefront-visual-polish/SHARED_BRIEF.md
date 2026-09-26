# Storefront visual polish — shared brief for all lanes (2026-09-26)

Repo: `/Users/fsuels/Projects/dresslikemommy` (Shopify Dawn-derived theme; GitHub `main` syncs to the live theme MAIN `133290917985`). Live site: https://www.dresslikemommy.com. 21 storefront languages.

## The 16 audit issues (owner asked for all to be fixed)

1. Home "Most-Loved Matching Sets" renders 1 of 4 cards: 3 product handles return 404 (`mommy-daughter-matching-tie-dye-dress`, `family-matching-hawaiian-shirt-and-floral-dress`, `family-matching-shirt-and-dress-set-yellow-floral-for-a-springtime-look`). Only `ladybug-dots-mommy-and-me-pajamas` works.
2. Home "Shop by Occasion": 4 tiles in a 3-column grid leave "Beach Days" orphaned on its own row.
3. Home section `seasonal_christmas` (type `seasonal-collection`) renders empty (0px).
4. Double outline on buttons ("See all family sets", "Shop new pajamas": square border drawn around the rounded pill) and on the footer email field.
5. Category tiles mix seasons (Christmas sweater on hanger, beach swimwear, shirtless dad) in autumn; the Mommy & Me tile says "Mother-daughter favorites" but shows a sweater on a hanger, not a mom and daughter.
6. Trust message repeated 4+ times; on mobile the 4 stacked trust pills below the hero eat ~220px before any product.
7. Hero: 3 equal-weight CTAs compete; the arch art loads after the text, so the hero's right half is briefly empty.
8. Every collection card shows "SALE" and a red price; badge loses meaning and the grid looks loud.
9. Product card titles truncate at 2 lines ("Jingle Bells Santa Family Matching…").
10. `/collections/mommy-and-me` opens with whole-family (dad-inclusive) sweaters instead of mom-and-child items.
11. Mobile PDP: gallery fills the whole first screen; title/price/size picker below the fold; no clear sign of more photos.
12. PDP: price is visually heavier than the small bold product title.
13. PDP: disabled "Pick a size" button is a faded pale green that reads as broken.
14. PDP: "Why You'll Love It" is 6+ stacked cards with orange checks — too much scroll.
15. Inconsistent section headings ("Shop by Category" small bold with a rule vs "Most-Loved Matching Sets" large light); Arial and Assistant mixed.
16. Footer unbalanced: "Customer Care" has one link ("Contact US"), Style Journal and newsletter blocks float out of alignment.

## Hard rules (every lane)

- Write ONLY the files in your lane. Read anything. Another lane owns every other file; if you need a change outside your lane, describe it exactly in your report instead.
- Never edit `locales/*.json`, `ops/AGENT_WORKLOG.md`, `ops/AGENT_COORDINATION.md`, `ops/PROBLEM_TRACKER.md`, or `snippets/jsonld-seo.liquid` (a peer's uncommitted work). Never `git add/commit/push/stash/reset/checkout`. The parent commits.
- No external writes of any kind: no Shopify Admin mutations, no theme push/upload, no product/collection/menu/translation/feed changes. Read-only Storefront (`/products/<h>.js`, `/collections/<h>/products.json`) and read-only Admin GraphQL queries are fine (token: `~/.config/dresslikemommy/admin-api-token.json`; never print, log, or copy it).
- Customer truth: dropshipping store, no physical store or stocked inventory. Never add claims about stock, warehouses, reviews, ratings, bestsellers, or discounts that aren't backed by data. Do not invent reviews or social proof.
- Translations: any new customer-visible text must work in all 21 languages. Prefer no new text. Editing an existing section setting's text in `templates/index.json` leaves Translate & Adapt serving the OLD translation on 20 locales; new block IDs get English-only fallback. If new text is unavoidable, follow the `snippets/hero-seasonal-copy.liquid` pattern (all 21 languages inline in a lane-owned snippet) or report the string to the parent.
- Images: use only published product photos from this store's own Shopify CDN (no stock, no AI-generated people). Keep new assets small (WebP, responsive widths) and provide alt text.
- Keep Dawn conventions: Liquid for presentation, vanilla JS, CSS scoped to your section/component. Backward-compatible settings with defaults equal to the prior behavior where practical. Smallest effective change.

## Shared design standards (so lanes stay consistent)

- Section headings (#15): homepage section titles use the theme's `h2` class/typography (`var(--font-heading-family)`, weight `var(--font-heading-weight)`), left-aligned, no decorative rule line, no local font-family/size overrides. L4 owns the global heading font weight in `config/settings_data.json`/`base.css`; other lanes only remove local heading overrides in their own files.
- Fonts: never use `Arial`/hard-coded font stacks; use `var(--font-body-family)` or `var(--font-heading-family)`.
- Buttons: primary = solid brand fill; secondary = outline; tertiary = text link with arrow. One outline only (no box-shadow ring plus border).
- Prices: regular price in the normal text color; only a real discount (compare-at > price) may show the sale color and badge.
- Spacing: prefer existing Dawn spacing vars; mobile side gutter 16px; no horizontal page scroll at 320–1440px.

## Tooling

- Node: Homebrew `node@22` is broken. Use `source ~/.nvm/nvm.sh && nvm use 20`.
- `shopify theme check` (run from repo root) must show 0 new offenses in your files. `git diff --check` clean. `node --check` any extracted inline JS you changed.
- Local render harness precedent: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-25-seasonal-homepage-hero/tools/render_hero_harness.js` (liquidjs bundled in the Shopify CLI, rendering into script-free copies of live pages). Adapt a copy into your lane folder if you need a visual check; headless Chromium/Playwright may be available in that packet's tooling.
- Put all notes, screenshots and scripts under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-storefront-visual-polish/lanes/<your-lane>/`.

## Report back (keep under ~300 words)

Files changed; per issue: what you changed and how you verified it (status words IMPLEMENTED / VERIFIED / FAILED / BLOCKED / SKIPPED); exact out-of-lane changes or admin approval packets you need; residual risks.
