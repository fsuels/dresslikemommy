# Collection SEO Agent Prompts

Date: 2026-03-27

## Swimsuits

Collection:
- Handle: `swimsuits`
- URL: `https://www.dresslikemommy.com/collections/swimsuits`

Evidence:
- Shopify Admin GraphQL `collectionByHandle(handle: "swimsuits")` returned the live SEO fields below.
- Live Admin record `updatedAt`: `2026-03-27T03:14:17Z` (`2026-03-26 23:14:17 EDT`).
- Current live SEO title: `Mother Daughter Swimsuits - Matching Swimwear | Dress Like Mommy`
- Current live meta description: `Explore matching bikinis, one-pieces, cover-up skirts, and beach-ready swimwear for moms and daughters. Free shipping + 30-day returns. Shop matching swimwear now.`
- `ops/content/collection-seo-admin-2026-03-26.json` shows the same title and meta description, so the March 26 admin batch and the current live Admin value are aligned.

Prompt for content/SEO agent:

In Shopify Admin -> Collections -> `Swimsuits` -> scroll to the `Search engine listing` / SEO section.

Current live title:
`Mother Daughter Swimsuits - Matching Swimwear | Dress Like Mommy`

Recommendation:
- Preferred title: `Mommy and Me Swimsuits | Mother Daughter Bathing Suits - Dress Like Mommy`
- Alternate title test: `Mommy and Me Swimsuits & Matching Bikinis - Mother Daughter Bathing Suits`

Current live meta description:
`Explore matching bikinis, one-pieces, cover-up skirts, and beach-ready swimwear for moms and daughters. Free shipping + 30-day returns. Shop matching swimwear now.`

Replace the meta description with:
`Shop mommy and me swimsuits, mother daughter matching bikinis, and family bathing suits. Matching one-pieces, two-pieces & cover-ups in sizes for mom and daughter. Free shipping.`

Rationale:
- Adds `family bathing suits` to target broader family swim intent.
- Adds `mother daughter matching bikinis` to cover stronger bikini-specific commercial intent.
- Keeps `mommy and me swimsuits` as the lead phrase while staying readable at collection level.
- This is a title/meta refresh only; do not change the collection handle or description in this pass.
