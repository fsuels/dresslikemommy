# Style Journal Custom Data

Use Shopify Admin custom data to override the default Style Journal internal-link
mapping without editing theme code.

The theme now checks these metafields first and falls back to the repo-side
handle mapping only when the metafields are blank.

## Article metafields

Create these article metafields in Shopify Admin:

| Namespace/key | Type | Example | Purpose |
| --- | --- | --- | --- |
| `custom.primary_collection_handle` | Single line text | `mommy-and-me` | Replaces the article's primary collection CTA and inline CTA target. |
| `custom.supporting_collection_handles` | Single line text | `dresses,matching-outfits` | Replaces the article end-cap supporting collection links. Use comma-separated collection handles. |
| `custom.related_article_handles` | Single line text | `what-to-wear-for-family-photos-matching-outfit-ideas,the-complete-guide-to-family-matching-outfits` | Replaces the explicit “Continue reading” article list. Use comma-separated article handles. |

## Collection metafields

Create this collection metafield in Shopify Admin:

| Namespace/key | Type | Example | Purpose |
| --- | --- | --- | --- |
| `custom.style_journal_article_handles` | Single line text | `how-to-choose-mommy-and-me-matching-outfits-for-family-photos,mommy-and-me-summer-dresses-for-vacations-and-photos` | Replaces the collection hero “Read the guide before you shop” links. Use comma-separated article handles. |

## Behavior notes

- The theme resolves collection handles through `collections[handle]`.
- The theme resolves article handles through `blogs['news'].articles`.
- If a handle is missing or the target article is not published yet, the theme
  silently skips that link instead of rendering a dead destination.
- If you only set the primary article collection handle and leave the supporting
  or related metafields blank, the theme still falls back to the repo-side
  defaults for the missing slots.

## Recommended setup order

1. Fill `custom.primary_collection_handle` on every published Style Journal article.
2. Fill `custom.related_article_handles` on the pillar articles first.
3. Add `custom.style_journal_article_handles` on the main commercial collections:
   - `matching-outfits`
   - `mommy-and-me`
   - `daddy-me`
   - `dresses`
   - `swimsuits`
   - `family-swimsuits`
4. Backfill supporting collection handles only where the default mapping is not
   good enough.
