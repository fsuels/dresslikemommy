# Style Journal Strategy

## Goal

Use the blog to capture search demand that is close to buying intent, then move
readers into collections with clear, relevant internal links.

The blog should support ecommerce, not compete with it.

## Current problems

- The store already has indexed articles, but too many of them read like broad AI
  listicles instead of firsthand shopping guides.
- Several visible publish dates cluster together, which makes the journal feel
  mass-produced instead of editorial.
- The strongest current opportunity is not "more posts at any cost." It is
  better topic selection, stronger article quality, and cleaner conversion paths.
- The current draft set already covers travel, swim, family-photo, mommy-and-me,
  and daddy-and-me themes, but couples-specific coverage is still thin, so new
  SEO work should add net-new intent or tighten an existing draft. Do not
  create sibling articles that solve the same query in slightly different
  words.

## Best-practice rules

- Publish one article per week, not a large batch on one date.
- Each article should target one primary search intent and one primary shopping CTA.
- Every article should link to:
  - 1 primary collection
  - 2 supporting collections
  - 1 related article
- Use original photos or product-led imagery that actually matches the advice.
- Keep introductions short and useful. Start answering the search intent in the
  first two paragraphs.
- Add bylines, keep visible breadcrumbs, and keep article structure clean with
  real headings and scannable lists.
- Search `ops/content/style-journal/articles/` before drafting. If a strong
  near-match already exists, retune that draft instead of creating a duplicate.
- Do not publish thin "ideas for every occasion" articles unless they contain
  concrete styling advice, fit guidance, and product selection logic.
- Until the article template supports article-specific product merchandising,
  put the primary collection links directly in the body copy. The current theme
  still falls back to a generic inline CTA and a generic collection end-cap.

## Query-backed opportunity

- User-provided Search Console notes show informational demand already surfacing
  in French (`comment harmoniser tenues famille sans memes motifs`) and Spanish
  (`traje de bano familiar`).
- The repo already contains Spanish and French locale files
  (`locales/es.json`, `locales/fr.json`) and the blog template is already set up
  as the `Family Style Journal` in `templates/blog.json`.
- The immediate opportunity is not a new content system. It is:
  - publish stronger English long-tail articles that map cleanly to collection CTAs
  - avoid cannibalizing existing swim and family-photo drafts
  - localize the best-performing English winners into French and Spanish after
    they show click-through and collection-click traction

## Priority keyword map

- `how to choose mommy and me matching outfits for family photos`
  - action: add a new narrow article
  - reason: `what-to-wear-for-family-photos-matching-outfit-ideas` is the broad
    family-photo pillar, but it does not own the mom-and-daughter variant tightly enough
  - primary CTA: `/collections/mommy-and-me`
  - supporting CTAs: `/collections/dresses`, `/collections/matching-outfits`
- `best matching family swimsuits for summer 2026`
  - action: retune the existing `best-family-swimsuits-for-beach-vacations-and-pool-days`
    draft instead of creating a second swim pillar
  - reason: the current draft already covers the core intent, and a second
    near-duplicate swim article would split authority
  - primary CTA: `/collections/family-swimsuits`
  - supporting CTAs: `/collections/swimsuits`, `/collections/trunks`
- `daddy and me outfit ideas for Father's Day`
  - action: add a new seasonal article
  - reason: Father's Day is a clear purchase moment that sits inside an existing
    high-converting daddy-and-me category
  - primary CTA: `/collections/daddy-me`
  - supporting CTAs: `/collections/tops`, `/collections/family-sets`
- `mother daughter matching dresses for Easter`
  - action: add a new seasonal article
  - reason: the store already has Easter ranking momentum, so a seasonal blog
    asset can support the commercial collection pages before and during spring demand
  - primary CTA: `/collections/dresses`
  - supporting CTAs: `/collections/mommy-and-me`, `/collections/matching-outfits`
- `mommy and me outfits for every season: a complete guide`
  - action: add a new mommy-and-me pillar
  - reason: the repo has a broad family-matching guide, but not a year-round
    mommy-and-me guide that can accumulate seasonal internal links
  - primary CTA: `/collections/mommy-and-me`
  - supporting CTAs: `/collections/dresses`, `/collections/swimsuits`, `/collections/family-pajamas`

## Journal placement

- Do not keep the blog in the primary conversion navigation.
- Surface the journal from:
  - the homepage featured-blog section
  - related articles below each post
  - article-to-collection links
  - footer or support navigation
- This keeps the main header focused on shopping while still giving Google and
  shoppers clear paths into content.

## Topic clusters

### Cluster 1: Vacation and travel

- Best for: immediate commercial intent
- Collections to push:
  - `/collections/matching-outfits`
  - `/collections/family-sets`
  - `/collections/family-swimsuits`
  - `/collections/trunks`
  - `/collections/dresses`

### Cluster 2: Mommy and Me and Daddy and Me

- Best for: high-converting long-tail searches
- Collections to push:
  - `/collections/mommy-and-me`
  - `/collections/daddy-me`
  - `/collections/trunks`
  - `/collections/dresses`
  - `/collections/tops`

### Cluster 3: Event and photo planning

- Best for: family photos, reunions, trips, birthdays, and seasonal moments
- Collections to push:
  - `/collections/matching-outfits`
  - `/collections/family-sets`
  - `/collections/dresses`
  - `/collections/tops`

### Cluster 4: Couples and gifting

- Best for: pair-focused shopping intent tied to date nights, trips, holidays,
  anniversaries, and gifts
- Collections to push:
  - `/collections/couples`
  - `/collections/tops`
  - `/collections/pajamas`
  - `/collections/sweaters`

## Conversion framework for every article

- Above the fold:
  - clear headline
  - honest summary
  - no hard sell
- Mid-article:
  - contextual collection links that match the section topic
- End of article:
  - one short "shop the look" section
  - one related article link
- Below article:
  - theme-level related posts and collection CTA block already added in repo

## Localization rollout

- Do not localize every draft immediately. Translate only the English articles
  that prove they can drive collection visits.
- First French candidates:
  - `how-to-choose-mommy-and-me-matching-outfits-for-family-photos`
  - `the-complete-guide-to-family-matching-outfits`
- First Spanish candidates:
  - `best-family-swimsuits-for-beach-vacations-and-pool-days`
  - `mother-daughter-matching-swimsuits-complete-guide-for-summer-2026`
- Localize titles, summaries, body copy, and in-body anchor text together so
  the localized article still points to the most relevant collection path.

## Measurement

- Watch these weekly:
  - non-brand clicks and impressions to `/blogs/news/` in Google Search Console
  - sessions that view an article and then a collection
  - assisted revenue from article-entry sessions in GA4 or your analytics stack
  - top internal links clicked from article pages
  - clicks and impressions split by language/locale once French and Spanish
    article translations go live
- Keep publishing only where the topic produces both search demand and
  downstream collection visits. Traffic without collection clicks is low-value
  traffic for this store.

## Existing content actions

- Keep as pillars after rewrite:
  - `the-complete-guide-to-family-matching-outfits`
  - `what-to-wear-for-family-photos-matching-outfit-ideas`
  - `daddy-and-me-matching-outfits-the-ultimate-guide`
  - `mother-daughter-matching-swimsuits-complete-guide-for-summer-2026`
- New drafts ready to publish:
  - `daddy-and-me-button-down-shirts-vacation-dinners-photos`
  - `daddy-and-me-beach-outfits-shirts-trunks-family-travel`
  - `matching-couple-outfits-date-night-travel-gifts`
  - `couple-matching-pajamas-holidays-anniversaries-gifts`
- Priority gap-fill drafts ready to publish:
  - `mother-daughter-matching-dresses-for-easter`
  - `how-to-choose-mommy-and-me-matching-outfits-for-family-photos`
  - `daddy-and-me-outfit-ideas-for-fathers-day`
  - `mommy-and-me-outfits-for-every-season-complete-guide`
- Retune instead of duplicating:
  - `best-family-swimsuits-for-beach-vacations-and-pool-days` -> target
    `best matching family swimsuits for summer 2026`
- Rewrite or tighten next:
  - `mommy-and-me-matching-outfit-ideas`
  - `mommy-and-me-outfits-for-every-budget`
  - `mommy-and-me-valentines-day-outfits`
  - `mommy-and-me-easter-dresses-2026`

## Why this direction

- Google recommends creating helpful, reliable, people-first content rather than
  search-engine-first pages.
- Google also recommends crawlable HTML links and clear internal linking so pages
  can be discovered and understood.
- Google image guidance still favors high-quality, relevant images with useful
  surrounding context and descriptive alt text.

Sources:

- Google Search Central, helpful content:
  https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search Central, crawlable links:
  https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google Search Central, image SEO best practices:
  https://developers.google.com/search/docs/appearance/google-images
- Shopify Admin GraphQL `articleCreate`:
  https://shopify.dev/docs/api/admin-graphql/latest/mutations/articleCreate
- Shopify Admin GraphQL `articleUpdate`:
  https://shopify.dev/docs/api/admin-graphql/latest/mutations/articleUpdate
