# Lane C — empty-cart picks row (2026-09-26)

## Before
`sections/main-cart-items.liquid` (4 items) and `snippets/cart-drawer.liquid` (3 items, empty-cart branch) rendered
`sections.cart.popular_with_families` over `collections.all.products`. `collections.all` returns the default A–Z order,
so the row showed Autumn Woodland Bunny, Bamboo Garden Panda ×2, Beanie Ghost. Nothing about popularity supported the heading.

## Evidence (read-only, 2026-09-26)
- Admin GraphQL `collections.sortOrder`: `best-sellers` = BEST_SELLING, `fall-winter` = BEST_SELLING, `new-arrivals` = CREATED_DESC.
- Order line items (non-test, not cancelled; ~2,040 most recent orders; 172 orders in the last 365 days):
  - `best-sellers` storefront top 4 are summer/beach items with 12/9/8/7 lifetime units (6/9/6/5 in 365 days), so its
    order does track sales, but its rules (TYPE EQUALS Dresses/Bottoms/Pajamas/Tops/Swimsuits/Family Matching) miss the
    active types `Swimwear`, `Matching Family Sets`, `Matching Family *`, `Sets`, `Sweaters`. Active top sellers such as
    skyfade-family-matching-set (11), chic-family-tides swimsuit (11), green-tropical-leaf swim shorts (10) are excluded.
  - Every in-season top seller in the last 365 days (safari and elf Christmas pajamas, cable-knit sweaters) is ARCHIVED.
  - `fall-winter` (BEST_SELLING) storefront top 10 are 2026-09-25 Christmas sweaters with 0 units sold, so "popular" would be false there.
- Conclusion: a popularity heading can be supported today only with summer/beach products. That is truthful but fails the
  "seasonal, useful" goal in late September, so Option B was chosen.

## Change (Option B) — IMPLEMENTED
- Source: `collections['new-arrivals']` (the header menu's NEW ARRIVALS link; sort CREATED_DESC, so the rows show the newest products).
- Heading: existing key `sections.breadcrumbs.label_new_arrivals`, which is already live as this collection's breadcrumb label and
  has a non-English value in all 35 locale files. No new text; no locale edits.
- Skips `product.available == false` and any product already in the cart; counts only rendered cards (4 page / 3 drawer).
- Wrapped in `products_count > 0` so an empty or missing collection hides the whole block instead of leaving a bare heading.
- Drawer "You may also like" upsell (non-empty cart) now also skips unavailable products.
- Markup, classes, section IDs and the drawer section-render path are unchanged.

## Verification
- `shopify theme check`: 0 offenses in both lane files. VERIFIED. (The only offense in the theme is `sections/footer.liquid:331`
  LiquidHTMLSyntaxError, which comes from the peer's uncommitted footer edit, not this lane.)
- `git diff --check` on both files: clean. VERIFIED.
- `tools/cart_picks_readback.py` → `readback-2026-09-26.json`: shows the picks as they stand today, the live label in all 21 storefront
  languages, and no missing or English-only locale values. VERIFIED (selection simulated from Storefront JSON, not a Liquid render).
- Liquid render on a preview theme: NOT RUN (no external writes allowed). This is the first check to run after the parent's push.

## Picks today
Cart page: Snowflake Reindeer Hooded Onesie Pajamas, Trick or Treat Pajamas, Boo Stripe Pajamas, Beanie Ghost Pajamas.
Drawer: the first three.

## Residual
- Some live translations of the label are clumsy (nl "Nieuwkomers", fi "Uusia tulokkaita", ko "새로운 도착", sv/da/no "ankomster").
  They are already live in breadcrumbs. Fixing them needs a locale/translation edit that belongs to the parent.
- `new-arrivals` rules also omit `Swimwear`, `Matching Family Sets`, `Sets`, `Sweaters`, `Matching Family Sweaters`, so the
  2026-09-25 Christmas sweaters are not in it. The row is still truthful because every item it shows is newly added.
- `sections/main-product.liquid:2713` still maps "Popular with Families" in the PDP copy map (peer-claimed file). Check whether any PDP surface renders that heading.
