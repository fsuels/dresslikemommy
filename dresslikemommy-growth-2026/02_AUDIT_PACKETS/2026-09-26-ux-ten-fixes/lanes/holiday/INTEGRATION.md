# Lane H — Holiday order-by line: integration notes (2026-09-26)

Lane files (new, uncommitted): `assets/dlm-holiday-order-by.js`, `ops/tests/test_holiday_order_by.mjs`, this folder.
No external writes were made. Admin access was read-only GraphQL `products` / `collections` / `collectionByHandle` queries.

## What the script does

- It runs only when the page has `[data-pdp-purchase-confidence] [data-dlm-delivery-window]` and the URL path contains `/products/<handle>`. It also needs a Halloween or Christmas cutoff inside its 60-day lead window for the window shown on the page. Otherwise it makes no network request.
- It makes one same-origin `GET {Shopify.routes.root}products/<handle>.js` and reads `tags`. There is no add-to-cart and no other network call.
- Holiday detection uses a case-insensitive tag match of `^(family )?halloween\b` or `^(family )?christmas\b`. This matches `Halloween`, `Halloween Pajamas`, `Christmas`, `Christmas Sweaters`, `Family Christmas Sweaters` and `Christmas Pajamas`. The ambiguous `Holiday` / `beach holiday outfit` tags and motif tags (`Ghost`, `Winter`, `Fall`) are ignored.
- The cutoff is the latest day D where `D + max` (the upper bound parsed from the same `data-dlm-delivery-window` value, with the same Sunday→Monday roll as `dlm-delivery-dates.js`) is on or before the holiday. Targets are Oct 31 for Halloween and Dec 24 for Christmas, because many storefront markets celebrate on Christmas Eve.
- The line is hidden in these cases: after the cutoff day, more than 60 days before the cutoff, when the window can't be parsed, for non-holiday products, and when JS or fetch fails. If a product has both holidays, the earlier open cutoff wins.
- Output is one `<p class="dlm-pc-row__summary dlm-holiday-order-by" data-dlm-holiday-order-by="halloween|christmas">`, inserted right after the `.dlm-pc-row__estimate` paragraph. It reuses the card's existing summary style and adds no CSS file. The date is formatted like `dlm-delivery-dates.js` (`Intl` `weekday/month/day: short`, `Shopify.locale`, then `<html lang>`, then en-US).
- Copy is inline for all 21 published storefront languages (en es fr de it nl pt da sv no pl cs fi ro el ja ko ru ar he hi), plus hu, tr, zh and zh-Hant. `nb`/`nn` map to `no`, `pt-BR` maps to `pt`, and unknown languages fall back to English. Every sentence says "estimated" (or the local equivalent) and none says "guarantee".

## a. `layout/theme.liquid` include (parent applies)

Anchor, currently line 328:

```liquid
  <script defer src="{{ 'dlm-delivery-dates.js' | asset_url }}"></script>
```

Insert immediately after it:

```liquid
  {%- if request.page_type == 'product' -%}
    <script defer src="{{ 'dlm-holiday-order-by.js' | asset_url }}"></script>
  {%- endif -%}
```

The script doesn't depend on `dlm-delivery-dates.js` because it reads the `data-dlm-delivery-window` attribute, not the rewritten text. Load order between the two doesn't matter.

## b. ADMIN APPROVAL PACKET — new automated collection (NOT applied)

Evidence (read-only Admin GraphQL, 2026-09-26): `tag:Halloween` returns 7 products. The `title/tag/product_type *halloween*` query and a ghost/pumpkin/skeleton/boo/spooky/witch/trick title query found no untagged Halloween products. There are 0 Halloween drafts; the 3 drafts in the store are unrelated. No collection with a `halloween` handle or title exists. The handles `halloween`, `halloween-family-pajamas`, `halloween-pajamas` and `family-halloween-pajamas` are all free. All 6 ACTIVE products use product type `Matching Family Pajamas` and carry both `Halloween` and `Halloween Pajamas`.

| Field | Proposed value |
|---|---|
| Title | `Halloween Family Pajamas & Outfits` |
| Handle | `halloween-family-pajamas` (matches the hero CTA "Shop Halloween Pajamas" and the main search intent; all current items are pajamas) |
| Type | Automated (smart) collection |
| Rules | 1 rule: `TAG` `EQUALS` `Halloween` (with a single rule, `appliedDisjunctively` makes no difference). Future Halloween outfits and tops join automatically when tagged `Halloween`. |
| Sort order | `BEST_SELLING` |
| SEO title | `Matching Family Halloween Pajamas & Outfits \| Dress Like Mommy` |
| SEO description | `Matching family Halloween pajamas: ghosts, pumpkins, skeletons and Boo stripes in adult and kids sizes. Shipping included. Order early for Halloween.` |
| Description (body) | `<p>Matching Halloween pajamas for the whole family, from ghost and pumpkin prints to Boo stripes and skeleton onesies, in adult and kids sizes. Delivery times are estimates; see the estimated arrival date on each product page.</p>` |
| Sales channel | Online Store (publish only after translations are in place, or accept English fallback for a short window) |

Products the rule matches today:

- ACTIVE (6, all visible on the storefront):
  - `beanie-ghost-family-matching-pajamas`
  - `boo-stripe-family-matching-pajamas`
  - `trick-or-treat-family-matching-pajamas`
  - `pumpkin-ghost-family-matching-pajamas`
  - `spooky-skeleton-family-matching-onesie-pajamas`
  - `monster-bloom-family-matching-onesie-pajamas`
- DRAFT (0): none.
- ARCHIVED (1, matched by the rule but not shown on the storefront): `matching-halloween-pumpkin-long-sleeve-t-shirt`.

Translations: the other 20 published languages (es fr de it nl pt da sv no pl cs fi ro el ja ko ru ar he hi) need COLLECTION `title`, `body_html`, `meta_title` and `meta_description` through `translationsRegister`. Keep the brand name "Dress Like Mommy" untranslated. Precedent and checks: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-24-eu-collection-translations/RESULT.md`. That packet also covers the optional theme-locale layer `sections.collection_seo.*`.

Rollback: delete the collection, or unpublish it from Online Store, and revert the hero link below.

### Follow-up hero retarget (peer-claimed files, describe only)

The link is set in `templates/index.json`, not in `snippets/hero-seasonal-copy.liquid`, which only holds the labels (its `cta_primary` already reads "Shop Halloween Pajamas" in all languages). Change both values together:

- `sections.hero_banner_main.settings.button_link`: `"/collections/family-pajamas"` → `"/collections/halloween-family-pajamas"`
- `sections.hero_banner_main.blocks.slide_halloween_arches.settings.link`: `"/collections/family-pajamas"` → `"/collections/halloween-family-pajamas"`

Why both: `sections/hero-banner.liquid` (about lines 951–962) pairs a slide with a CTA by exact link equality, and it localizes `/collections` with `routes.collections_url`, so no per-language URL is needed. Preconditions: the collection exists and is published to Online Store. Before editing, pull the live `templates/index.json` because the theme editor may have changed it. After the change, check that `/`, `/es/` and `/de/` hero buttons return 200 and show the 6 products. Do this only after the peer claim `Storefront visual polish (16-issue audit)` is released.

## c. Cutoff dates computed by the code (window "12-16 days", upper bound 16)

| Holiday | Target date | Order-by cutoff | Line visible |
|---|---|---|---|
| Halloween 2026 | Sat Oct 31 | **Thu Oct 15, 2026** | Aug 16 – Oct 15 (so visible now) |
| Christmas 2026 | Thu Dec 24 (Christmas Eve) | **Tue Dec 8, 2026** | Oct 9 – Dec 8 (hidden today, Sep 26) |
| Halloween 2027 | Sun Oct 31 | Thu Oct 14, 2027 (Sunday roll moves it back one day) | Aug 15 – Oct 14 |
| Christmas 2027 | Fri Dec 24 | Wed Dec 8, 2027 | Oct 9 – Dec 8 |

If the store window changes (for example `10-20 days`), the cutoff moves with it automatically.

## Verification

- `node --check assets/dlm-holiday-order-by.js`: pass.
- `node --test ops/tests/test_holiday_order_by.mjs ops/tests/test_delivery_dates.mjs`: 16/16 pass (11 new tests).
- `shopify theme check`: 278 files, 1 offense. It is the existing `BlockIdUsage` warning in `sections/footer.liquid`; the new file has 0.
- `git diff --check` and `--no-index --check` on the two new files: clean.
- Visual check on the live site: headless Playwright with the real file injected (`addScriptTag`), ad and analytics pixels blocked, no cart actions. Script: `shoot_holiday_order_by.js`; output in `screenshots/` and `screenshots/results.json`.
  - EN desktop 1440 and mobile 375: "Order by Thu, Oct 15 for estimated Halloween arrival", 1 line, no horizontal scroll (scrollWidth equals clientWidth).
  - ES mobile: "Pide a más tardar el jue, 15 oct para una llegada estimada antes de Halloween".
  - DE desktop: "Bis Do., 15. Okt. bestellen für die voraussichtliche Lieferung vor Halloween".
  - Christmas sweater (`nordic-reindeer-family-matching-sweaters`) today: no line, as expected. With a faked date of 2026-10-20: "Order by Tue, Dec 8 for estimated Christmas arrival".
  - Beanie Ghost with a faked date of 2026-10-16: no line, because the page window then ends Mon, Nov 2.
- Built-in browser pane: the Beanie Ghost PDP was checked at pane width and at the 375 mobile preset, then reset to desktop. The line rendered under the estimate with no horizontal scroll. The injection there was a trimmed copy of the same logic (en/es copy only). Full-file fidelity comes from the Playwright run.

## Observation outside this lane

The live German PDP card headline reads "Kostenloser Standardversand" ("free standard shipping"). The snippet deliberately avoids "free" wording. The source is the `de` locale value `products.purchase_confidence.shipping_headline`, which belongs to the peer/locale owner.
