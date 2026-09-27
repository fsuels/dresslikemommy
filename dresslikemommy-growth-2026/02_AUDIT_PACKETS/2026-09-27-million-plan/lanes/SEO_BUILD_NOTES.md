# SEO build notes: theme fixes #3, #4, #8, #9, #10 and #11

- Date: 2026-09-27
- Source audit: `lanes/seo.md`, sections 3 and 4.
- Scope: local theme-code edits only. Nothing was committed, pushed or written to Shopify.
- Files left alone on purpose: `locales/*.json`, `snippets/cart-drawer.liquid`, the cart sections, `assets/dlm-family-builder*`, and every file another session had already modified.
- Status: `IMPLEMENTED`, with the local checks `VERIFIED`. Every live effect is `EXPECTED` until release and `LIVE_READBACK_REQUIRED`.

## 1. Changes per item

### #3 Head-term collection copy, and removing SEO-speak

**New snippets.** Each snippet holds the copy inline, with a `case` on the locale. It covers es, fr, de, it, nl, pt, da, sv, no/nb, pl, cs, ja, ko, ru, ar, he, hi, el, ro and fi. English is the `else` branch.

- `snippets/collection-guide-mommy-and-me.liquid`: fields `heading`, `lead` and `guide` (section 4.1).
- `snippets/collection-guide-christmas-pajamas.liquid`: fields `heading`, `lead` and `guide` (section 4.2).
  - It takes a `show_styles` flag. The print-examples paragraph (plaid, reindeer, Fair Isle, snowflake) renders only when the collection has at least 6 products.
  - Reason: the audit notes the page holds 1 product today, so describing those prints would be false.
- `snippets/collection-guide-daddy-me.liquid`: section 4.4. It also serves the `daddy-and-me` duplicate.
- `snippets/collection-guide-swimsuits.liquid`: fields `lead` and `guide` (section 4.5). The swimsuits section keeps its own title, related-links aside and FAQ.
- `snippets/collection-guide-family-pajamas.liquid`: section 4.6.
- `snippets/collection-guide-generic.liquid`: a short sizing and delivery block, "Before you order". It replaces the templated "Collection Note / A closer look at …" block on all other collections.

**`snippets/collection-seo-fallback.liquid`**

- New variables: `seo_lang`, `head_guide`, `head_show_styles` and `head_meta_description`. `daddy-and-me` is mapped to the `daddy-me` guide.
- English display titles, i.e. the H1 (section 4):
  - `swimsuits`: "Mommy and Me Swimsuits"
  - `christmas-pajamas`: "Matching Family Christmas Pajamas"
  - `new-women-outfits`: "Matching Family Outfits"
- English meta titles and descriptions for all 6 head collections come from section 4. Every description is 155 characters or fewer, so the existing `truncate: 155` never cuts one.
  - The christmas-pajamas description drops the print list while the page has fewer than 6 products.
- `christmas-pajamas` now forces the theme SEO fields, in English only. Localized titles stay as they were.
- Body and hero:
  - The 5 guide handles now use `<p>lead</p>` plus the guide HTML. The hero gets the lead sentence exactly.
  - For `new-women-outfits` in English, the lead is the section 4.3 paragraph. Its existing translated rich parts are already buyer guidance, so they stay.
- `matching-couples-t-shirts` and `daddy-me-shirts`: the translated body strings for these open with "for shoppers searching …", so the hero now uses the meta description instead.
- English fallback branches: I rewrote every "strongest dress styles", "landing page built around … search intent", "this page is built around", "for shoppers searching" and "for shoppers looking specifically" sentence.
- I also removed the templated "These styles are selected for … soft fabrics, easy sizing …" paragraph, along with the `audience_long` assignments that only it used.
- Honesty fix beyond the brief: the `/collections/all` description said "fast shipping", in English and in every translation.
  - English now reads "Standard shipping included".
  - Other languages now use the neutral `storefront.collection_fallback_description`.

**`snippets/collection-seo-content.liquid`**

- `mommy-and-me` and `daddy-me`/`daddy-and-me` now render the translated guides instead of the old `rich_parts`. The old `daddy_me` rich parts contained "Search demand around this category…".
- `christmas-pajamas` and `family-pajamas` gained guide blocks.
- These rich-part pieces are no longer rendered, because they talk about searches or "this page":
  - `daddy_me_tshirts` 2–4
  - `daddy_me_shirts` 1–2
  - `couples` 2–3
  - `couples_tshirts` 2
  - `spring_matching` 2
  - `family_swimsuits` 2–4
- All rich output is now captured, and the "Collection Note" eyebrow `<p class="collection-seo-rich__eyebrow">…</p>` is stripped in every language. This covers dresses, maxi-dresses, matching-outfits and family-sets.

**`sections/main-collection-seo.liquid`**

- In the swimsuits branch, `copy_1`/`copy_2` (page-talk) are replaced by the swimsuits guide.
- The generic branch no longer shows "Collection Note" or "A closer look at {title}". It renders the translated "Before you order" guide instead.
- I dropped the `display_title` and `hero_summary` renders and the variables that nothing uses any more, which saves 2 fallback renders per collection page.

**`snippets/style-journal-internal-links.liquid`**

- Two English captions said "landing page". I rewrote them.

### #4 Canonical consolidation (`layout/theme.liquid`)

- I followed the existing `popular-family-matching` pattern:
  - `daddy-and-me` now has its canonical at `collections['daddy-me'].url`.
  - `popular-mommy-me-1` now has its canonical at `collections['mommy-and-me'].url`.
- Both are guarded by `!= blank`.

### #8 One hreflang set (`snippets/meta-tags.liquid`)

- A single public GET of `https://www.dresslikemommy.com/` on 2026-09-27 returned HTTP 200 with 44 alternates:
  - Theme set: `pt-br` for `/pt` and `x-default` last, placed between `og:*` and `twitter:*`.
  - Shopify's set: in `content_for_header` next to `rel="ucp"`, with `x-default` first and `pt` for `/pt`.
- Shopify's set is therefore confirmed live. I deleted the theme's hreflang computation and loop and left a comment explaining why.

### #9 No noindex on `?variant=` product URLs

- `layout/theme.liquid`: removed the `parameterized_product_noindex` assignment and the render argument. The query-stripped product canonical is unchanged.
- `snippets/meta-tags.liquid`: removed the `if parameterized_product_noindex` block.

### #10 Homepage: one H1 and a head-term title

- `layout/theme.liquid`: in English, the homepage `<title>` is now "Mommy and Me Outfits & Matching Family Clothes | Dress Like Mommy". Localized homepages keep their translated `storefront.home_title`.
- `snippets/meta-tags.liquid`: the index `og:title` matches it in English. In other languages, `og:title` and `og:description` now use the translated home strings; before, English was hard-coded for every locale.
- `sections/header.liquid`: removed the index-only `<h1 class="header__heading">` wrapper around the logo in both logo positions. The homepage logo markup now matches every other page, and `.header__heading-link` already carries the grid area.
- `sections/hero-banner.liquid`:
  - On the index page, first section only, it now renders `<h1 class="visually-hidden">` with stable text from the new `snippets/home-seo-heading.liquid`. That text is "Mommy and Me and Family Matching Outfits", translated into the 20 languages.
  - The seasonal headline ("Spooky nights. …") is now always an `h2`.

### #11 Empty-collection guard (`snippets/meta-tags.liquid`)

- A collection with `all_products_count < 3` now gets `noindex, follow`.
- Handles on the whitelist never get it:
  - The seasonal hubs `christmas-pajamas`, `halloween-family-pajamas`, `swimsuits` and `family-swimsuits`.
  - The head-term pages `mommy-and-me`, `new-women-outfits`, `daddy-me` and `family-pajamas`.
  - `all`.
  - The canonicalized duplicates `daddy-and-me`, `popular-mommy-me-1` and `popular-family-matching`, so none of them combines noindex with a cross-URL canonical.

## 2. Deviations from the audit text, and why

1. **The homepage H1 is visually hidden, not a visible replacement headline.**
   - The audit asks for a visible stable H1, with the seasonal line as a `<p>`. That would redesign the hero, and I cannot preview it here, since `shopify theme dev` would write a dev theme.
   - The H1 carries the head terms without any change to the layout. The seasonal line is an `h2` rather than a `<p>`, so it keeps the heading font; `.hero-banner__heading` sets size and weight but not the font family.
   - If a visible H1 is wanted, that is a design follow-up for the hero owner.
2. **In other languages, titles, meta titles and meta descriptions stay the existing locale translations.**
   - Only the visible guide copy (lead and guide) is newly translated.
   - Native localized head-term titles are fix #13, which also touches `locales/*.json`.
3. **Copy was softened where a claim could be false for a dropship catalog.**
   - "Every look" became "Styles come in…".
   - "Each set is sold by person" became "Most sets…".
   - "Adult shirts are cut to standard men's sizing" was dropped.
   - "Tankinis" was dropped from swim, and "many with trunks" became "some".
   - Nothing mentions UPF, stock, warehouses, fast shipping, reviews or bestsellers. Delivery always points to the estimate on the product page.
4. **The empty `family-swimsuits` collection is not linked from the new copy.**
   - The swimsuits guide links `trunks` and `family-sets`.
   - Christmas links `family-sweaters`, which is live from the homepage hero, instead of an unverified "Christmas outfits" collection.
   - Family pajamas links `mommy-and-me` instead of `pajamas`, whose H1 is also "Matching Family Pajamas".

## 3. Verification

- `perl -e 'alarm 300; exec @ARGV' shopify theme check --output json` returned `[]`: 0 errors and 0 warnings across the whole theme (`VERIFIED`).
  - The first run flagged one warning I had introduced (`UnusedAssign audience_long`). I fixed it and re-ran.
- `git diff --check` on all touched files: clean. The new files end with a newline and have no trailing whitespace (`VERIFIED`).
- One live GET of the homepage confirmed the duplicate hreflang and the two H1s. There were no further requests, because of the rate limit.
- No Liquid engine is available locally and `theme dev` is a Shopify write, so there is no rendered preview (`NOT RUN`). The head output below is reasoned from the code.
  - **Product** `/products/x?variant=123` (en): canonical `/products/x` with no query. No robots meta, unless it is a search, utility or archived page. One Shopify hreflang set of 22. `og:type` is `product`.
  - **Collection** `/collections/daddy-and-me` (en):
    - Canonical: `/collections/daddy-me`.
    - `<title>`: "Daddy and Me Outfits – Matching Dad and Kid Shirts & Tees", with no shop suffix because the theme SEO fields are forced.
    - Meta description: the section 4.4 text. No robots meta, since the handle is whitelisted.
    - H1: "Daddy and Me Outfits". The hero `<p>` is the lead sentence, and the guide block sits below the product grid.
  - **Collection** `/collections/christmas-pajamas` (en, 1 product): title "Matching Family Christmas Pajamas for Adults, Kids & Baby", with the description that has no print list. It stays indexable (whitelisted), and the guide has no print paragraph.
  - **Collection** `/de/collections/mommy-and-me`: title and meta are unchanged (translated keys). The German lead and guide render, with no "Collection Note".
  - **Homepage** (en):
    - Title "Mommy and Me Outfits & Matching Family Clothes | Dress Like Mommy", with a matching `og:title`.
    - Description unchanged. Exactly one `<h1>` (the hidden stable H1); the seasonal headline is an `h2` and the logo is not a heading.
    - One Shopify hreflang set.
- Strict continuity: `NOT RUN`, because no continuity, prompt or worklog files were touched. The parent should add the `ops/AGENT_WORKLOG.md` anchor when committing.

## 4. Exact file list for the parent to commit (15 files)

Modified (the hunks in these files are mine only; none of them had changes from another session before this work started):

```
layout/theme.liquid
sections/header.liquid
sections/hero-banner.liquid
sections/main-collection-seo.liquid
snippets/collection-seo-content.liquid
snippets/collection-seo-fallback.liquid
snippets/meta-tags.liquid
snippets/style-journal-internal-links.liquid
```

New:

```
snippets/collection-guide-christmas-pajamas.liquid
snippets/collection-guide-daddy-me.liquid
snippets/collection-guide-family-pajamas.liquid
snippets/collection-guide-generic.liquid
snippets/collection-guide-mommy-and-me.liquid
snippets/collection-guide-swimsuits.liquid
snippets/home-seo-heading.liquid
```

Plus this notes file: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-27-million-plan/lanes/SEO_BUILD_NOTES.md`.

Commit with explicit paths only, for example `git add <paths above>`. Never use `git add -A`, because `locales/*.json` and other files carry peer edits.

## 5. Post-release live checks (after the main → Shopify sync)

Space the requests out: the site returns 429 after about 17 fast fetches.

1. **Homepage `/`:**
   - `<title>` is the new title.
   - Exactly 1 `<h1>`, the stable text; the seasonal line is an `h2`; the logo is not inside an `h1`.
   - Exactly 22 `hreflang` alternates, with one `x-default` and no `pt-br`.
   - Also check `/de` for the German H1 and German `og:title`.
2. **Collections:**
   - `/collections/daddy-and-me`: canonical is `…/collections/daddy-me`.
   - `/collections/popular-mommy-me-1`: canonical is `…/collections/mommy-and-me`.
   - `/collections/popular-family-matching`: still canonical to `new-women-outfits`.
3. **The 6 head URLs** (`mommy-and-me`, `christmas-pajamas`, `new-women-outfits`, `daddy-me`, `swimsuits`, `family-pajamas`):
   - The section 4 title and meta, and one H1.
   - No "Collection Note", "search demand", "strongest" or "this page is built" anywhere in the HTML.
   - The guide block renders below the grid.
   - 22 alternates each, and no robots meta.
4. **Thin collection:** `/collections/family-swimsuits` (0 products, whitelisted) has no robots meta. Pick any non-whitelisted collection with fewer than 3 products and confirm `noindex, follow`, and confirm every head collection is unaffected.
5. **Product with `?variant=<id>`:** no `<meta name="robots">`, canonical without the query, 22 alternates.
6. **Localized spot check** on `/es`, `/de`, `/ja` and `/he` for `collections/mommy-and-me` and `collections/swimsuits`:
   - The lead and guide are in the page language, with no English left in them.
   - The Hebrew and Arabic guides render right-to-left.
7. **Mobile at 375 px and desktop:**
   - The homepage header and logo alignment are unchanged, now that the `h1` wrapper is gone.
   - The collection guide block and the swimsuits panel copy lay out correctly (`docs/agent-loops/ui-browser-verification-loop.md`).
8. **Google Search Console:**
   - URL Inspection on the 6 head URLs and one `?variant=` URL.
   - After 28 days, check the "Excluded by noindex" count, which should fall, and "Duplicate, Google chose different canonical".

## 6. Follow-ups outside this build (Shopify admin, `S`)

- Mirror the section 4 titles and descriptions into each head collection's Shopify SEO fields, so the admin and the theme agree. Five of them already have the theme SEO fields forced in English.
- Point the navigation and footer links to the survivor collections only (`daddy-me`, `mommy-and-me`).
- `popular-mommy-me-1` still shows the H1 "Popular Mommy and Me". It is canonicalized now, but the "Popular" wording should go unless real sales data supports it.
- Remaining low-grade copy in non-head translated rich parts: `family_matching` part 2 and `family_sets` part 2 say "strongest … styles". These belong to the #13 locale lane.
