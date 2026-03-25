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
- Do not publish thin "ideas for every occasion" articles unless they contain
  concrete styling advice, fit guidance, and product selection logic.

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
  - `/collections/dresses`
  - `/collections/tops`

### Cluster 3: Event and photo planning

- Best for: family photos, reunions, trips, birthdays
- Collections to push:
  - `/collections/matching-outfits`
  - `/collections/family-sets`
  - `/collections/dresses`
  - `/collections/tops`

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

## Measurement

- Watch these weekly:
  - non-brand clicks and impressions to `/blogs/news/` in Google Search Console
  - sessions that view an article and then a collection
  - assisted revenue from article-entry sessions in GA4 or your analytics stack
  - top internal links clicked from article pages
- Keep publishing only where the topic produces both search demand and
  downstream collection visits. Traffic without collection clicks is low-value
  traffic for this store.

## Existing content actions

- Keep as pillars after rewrite:
  - `the-complete-guide-to-family-matching-outfits`
  - `what-to-wear-for-family-photos-matching-outfit-ideas`
  - `daddy-and-me-matching-outfits-the-ultimate-guide`
  - `mother-daughter-matching-swimsuits-complete-guide-for-summer-2026`
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
