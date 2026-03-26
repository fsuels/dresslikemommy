# Internal Linking Structure Audit

Date: 2026-03-26
Site audited: https://www.dresslikemommy.com
Scope: live English storefront crawl of homepage, collection pages, product pages, pages, blog index, and article URLs from the default sitemap set, plus theme-code review for header/footer/article/product templates.

## Method

- Crawled the default-locale sitemap inventory: 225 product URLs, 41 collection URLs, 17 pages, 255 blog/article URLs, plus the homepage.
- Reviewed live navigation and collection directory pages in-browser.
- Cross-checked the theme implementation for the footer blog link, product description rendering, and article internal-link rendering.
- Resolved the initial orphan-page false positives by combining the live `/collections` hub with Storefront API collection-product membership for published resources.

## Verified Broken Internal Links

Direct check: `/blogs/style-journal` returns 404, but no live internal link to that path was found in the crawl or in the theme files. The footer itself is correctly wired to `blogs['news']`.

The verified broken live internal links are concentrated in article body links to discontinued products:

| Source page | Broken destination | Recommended fix |
| --- | --- | --- |
| `https://www.dresslikemommy.com/blogs/news/best-fall-colors-for-family-matching-looks` | `https://www.dresslikemommy.com/products/2016-summer-family-matching-outfits-short-sleeved-cotton-matching-family-clothes-t-shirt-family-look-family-matching-clothes` | Replace with a current family-matching collection or current product. |
| `https://www.dresslikemommy.com/blogs/news/best-fall-colors-for-family-matching-looks` | `https://www.dresslikemommy.com/products/christmas-family-pajamas-set-xmas-parent-child-sleepwear` | Replace with a live Christmas pajamas product or `/collections/christmas-pajamas`. |
| `https://www.dresslikemommy.com/blogs/news/back-to-school-matching-outfits-for-first-day-photos` | `https://www.dresslikemommy.com/products/cute-mother-daughter-matching-stripe-dress` | Replace with a live dress PDP or `/collections/dresses`. |
| `https://www.dresslikemommy.com/blogs/news/back-to-school-daddy-and-me-photo-outfits` | `https://www.dresslikemommy.com/products/family-matching-christmas-t-shirts-festive-reindeer-design` | Replace with a live daddy-and-me or family-shirts target relevant to the article. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2020` | `https://www.dresslikemommy.com/products/family-matching-christmas-t-shirts-santa-reindeer-snowman-festive-design` | Replace with a live Christmas tops PDP or `/collections/christmas-tops`. |
| `https://www.dresslikemommy.com/blogs/news/adorable-matching-valentines-day-looks-for-the-whole-family` | `https://www.dresslikemommy.com/products/family-matching-fashion-colorful-sweater` | Replace with a live Valentine's-appropriate product or `/collections/mommy-and-me` or `/collections/couples`. |
| `https://www.dresslikemommy.com/blogs/news/back-to-school-daddy-and-me-photo-outfits-2022-edition` | `https://www.dresslikemommy.com/products/family-matching-hawaii-summer-set` | Replace with a live back-to-school family set or `/collections/family-sets`. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2020` | `https://www.dresslikemommy.com/products/family-matching-outfits-father-son-mommy-me` | Replace with a live patriotic family set or `/collections/family-sets`. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2024` | `https://www.dresslikemommy.com/products/family-matching-outfits-ruffled-sleeve-dress-t-shirt` | Replace with a live 4th-of-July or family-set PDP. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2020` | `https://www.dresslikemommy.com/products/family-matching-wave-stitching-sweatshirt-pant-set` | Replace with a live winter family set or `/collections/family-sweaters`. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2017` | `https://www.dresslikemommy.com/products/girl-mom-dress-family-clothing-2016-long-sleeve-print-floral-lace-dresses-for-me-and-mommy-mother-and-daugther-clothes-3xl` | Replace with a live mommy-and-me dress PDP or `/collections/dresses`. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2019` | `https://www.dresslikemommy.com/products/high-end-matching-princess-wedding-dress` | Replace with a live formal dress collection link. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2018` | `https://www.dresslikemommy.com/products/matching-dress-for-mom-and-toddler` | Replace with a live mommy-and-me dress PDP or `/collections/dresses`. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2018` | `https://www.dresslikemommy.com/products/matching-floral-summer-beach-dress` | Replace with a live summer dress/family set link. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2017` | `https://www.dresslikemommy.com/products/matching-hearts-yoga-pants-mommy-me` | Replace with a live mommy-and-me casual product or `/collections/mommy-and-me`. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2018` | `https://www.dresslikemommy.com/products/matching-leopard-print-tie-dye-lace-top` | Replace with a live tops or mommy-and-me collection link. |
| `https://www.dresslikemommy.com/blogs/news/apple-picking-matching-outfits-for-the-whole-family` | `https://www.dresslikemommy.com/products/matching-leopard-t-shirt-mommy-me` | Replace with a live mommy-and-me tee or fall collection link. |
| `https://www.dresslikemommy.com/blogs/news/back-to-school-daddy-and-me-photo-outfits` | `https://www.dresslikemommy.com/products/matching-mommy-me-one-piece-swimsuit` | Replace with a relevant daddy-and-me product or collection; the current swim link is both broken and off-topic. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2024` | `https://www.dresslikemommy.com/products/matching-mommy-me-unicorn-t-shirt` | Replace with a live holiday/family tee. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2020` | `https://www.dresslikemommy.com/products/matching-mother-daughter-rainbow-pony-dress` | Replace with a live red-white-blue or summer mommy-and-me dress link. |
| `https://www.dresslikemommy.com/blogs/news/back-to-school-matching-outfits-for-first-day-photos-2023` | `https://www.dresslikemommy.com/products/matching-orange-brown-leggings-mommy-me` | Replace with a live fall leggings or mommy-and-me collection link. |
| `https://www.dresslikemommy.com/blogs/news/adorable-matching-valentines-day-looks-for-the-whole-family` | `https://www.dresslikemommy.com/products/matching-short-sleeve-floral-printed-patchwork-dress` | Replace with a live Valentine's or dresses target. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2016` | `https://www.dresslikemommy.com/products/matching-sunflower-mother-daughter-one-piece-jumpsuits` | Replace with a live jumpsuits or dresses collection link. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2020` | `https://www.dresslikemommy.com/products/matching-t-shirt-heart-puzzle-piece` | Replace with a live family tee or couples tee. |
| `https://www.dresslikemommy.com/blogs/news/best-family-matching-outfits-for-harvest-season-2023-edition` | `https://www.dresslikemommy.com/products/mommy-me-angel-wing-embroidery-t-shirt` | Replace with a live fall mommy-and-me product or collection. |
| `https://www.dresslikemommy.com/blogs/news/back-to-school-daddy-and-me-photo-outfits-2022-edition` | `https://www.dresslikemommy.com/products/mommy-me-checkered-one-piece-swimsuit` | Replace with a relevant daddy-and-me product; current link is broken and off-topic. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2019` | `https://www.dresslikemommy.com/products/mommy-me-matching-plaid-swimsuit` | Replace with a live swim PDP or `/collections/swimsuits`. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2018` | `https://www.dresslikemommy.com/products/mother-and-daughter-africa-pajama` | Replace with a live pajamas or summer collection link. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2017` | `https://www.dresslikemommy.com/products/mother-and-daughter-matching-swimsuit` | Replace with a live swim PDP or `/collections/swimsuits`. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2026` | `https://www.dresslikemommy.com/products/mother-daughter-matching-princess-pajamas` | Replace with a live summer or pajamas target appropriate to the article. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2025` | `https://www.dresslikemommy.com/products/mother-daughter-matching-sundress-outfit` | Replace with a live sundress or mommy-and-me dress link. |
| `https://www.dresslikemommy.com/blogs/news/back-to-school-daddy-and-me-photo-outfits-2022-edition` | `https://www.dresslikemommy.com/products/new-2020-matching-mother-daughter-swimsuit-beachwear` | Replace with a relevant daddy-and-me or back-to-school target. |
| `https://www.dresslikemommy.com/blogs/news/4th-of-july-family-matching-outfits-2025` | `https://www.dresslikemommy.com/products/christmas-family-matching-outfits-t-shirt-short-sleeve` | Replace with a live 4th-of-July/family-tees product or collection. |

## Internal Links That Still Work But Should Be Updated

These are not broken, but they create avoidable redirect hops from editorial content:

| Source page | Current destination | Resolves to | Recommended fix |
| --- | --- | --- | --- |
| `https://www.dresslikemommy.com/blogs/news/autumn-matching-family-style-plaid-flannel-and-more` | `https://www.dresslikemommy.com/products/family-matching-christmas-crew-pajamas-black-and-red-plaid-holiday-pajama-set-for-kids-and-adults` | `https://www.dresslikemommy.com/products/family-matching-pajama-set-red-and-black-buffalo-plaid` | Update the article to the final PDP URL. |
| `https://www.dresslikemommy.com/blogs/news/back-to-school-daddy-and-me-photo-outfits` | `https://www.dresslikemommy.com/products/family-matching-christmas-pajama-set-merry-christmas-tree-print-in-festive-green-and-black-for-holiday-gatherings` | `https://www.dresslikemommy.com/products/family-matching-christmas-pajamas-merry-christmas-tree-festive-green-black` | Update the article to the final PDP URL. |
| `https://www.dresslikemommy.com/blogs/news/best-family-matching-outfits-for-harvest-season` | `https://www.dresslikemommy.com/products/mom-baby-white-lace-matching-swimsuit` | `https://www.dresslikemommy.com/collections/swimsuits` | Replace with a current swim PDP or keep the collection URL directly. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2019` | `https://www.dresslikemommy.com/products/mommy-me-fashion-outfit-sundress` | `https://www.dresslikemommy.com/collections/sundresses` | Link directly to `/collections/sundresses`. |
| `https://www.dresslikemommy.com/blogs/news/best-matching-family-outfits-for-winter-2017` | `https://www.dresslikemommy.com/products/mommy-me-matching-denim-dress` | `https://www.dresslikemommy.com/collections/dresses` | Link directly to `/collections/dresses`. |
| `https://www.dresslikemommy.com/blogs/news/adorable-matching-valentines-day-looks-for-the-whole-family` | `https://www.dresslikemommy.com/products/mother-and-daughter-dresses-dresses-for-girls-family-matching-clothing-girls-sleeveless-summer-beach-party-dress` | `https://www.dresslikemommy.com/collections/dresses` | Link directly to `/collections/dresses`. |

## Navigation SEO

Verified current header structure:

- Top-level collections are reachable in one click from the homepage header: `NEW ARRIVALS`, `MOMMY & ME`, `DADDY & ME`, `COUPLES`, `MATERNITY`, and `FAMILY MATCHING`.
- Sub-collections such as `Swimsuits`, `Pajamas`, `Dresses`, `Family Sets`, `Family Tops`, `Family Pajamas`, `Family Sweaters & Coats`, and `Family Swimsuits` are exposed from the live menu/collection directory.

Primary structural issue:

- `SHOP` points to the homepage (`/`) instead of the collection directory (`/collections`) or another browse hub.
- The live collection directory at `https://www.dresslikemommy.com/collections` contains secondary collection paths that are not clearly surfaced from the homepage header, including:
  - `https://www.dresslikemommy.com/collections/fall-winter`
  - `https://www.dresslikemommy.com/collections/formal-dresses`
  - `https://www.dresslikemommy.com/collections/jumpsuits`
  - `https://www.dresslikemommy.com/collections/maxi-dresses`
  - `https://www.dresslikemommy.com/collections/midi-dresses`
  - `https://www.dresslikemommy.com/collections/mini-dresses`
  - `https://www.dresslikemommy.com/collections/rompers`

Recommended navigation fix:

- Keep the existing mega-menu, but change `SHOP` to link to `/collections` so the collection directory becomes crawlable from the homepage in one click.
- Add at least one direct path from the homepage header to `Dresses`, `Swimsuits`, and `Pajamas` if the merchant wants those to remain high-priority SEO targets independent of hover/mega-menu behavior.

## Cross-Linking Findings

### Product pages

- In the crawl, `0 / 225` live product descriptions contained contextual internal links to related products or collections inside the product-description block.
- The product description block in the theme renders only the optimized product description HTML, with no related-links fallback injected in the product body.

Recommended product-link pattern:

- Swimsuit PDPs: add links to `/collections/swimsuits`, `/collections/family-swimsuits`, and `/collections/trunks`.
- Dress PDPs: add links to `/collections/dresses`, `/collections/mommy-and-me`, and `/collections/family-sets`.
- Pajama PDPs: add links to `/collections/pajamas` and `/collections/family-pajamas`.
- Daddy & Me PDPs: add links to `/collections/daddy-me` and `/collections/daddy-me-t-shirts`.
- Couples PDPs: add links to `/collections/couples` and `/collections/matching-couples-t-shirts`.

### Blog posts

- Only `24 / 254` article pages contained any raw HTML links to products or collections.
- Most seasonal articles have zero product or collection links in the article body, including:
  - `https://www.dresslikemommy.com/blogs/news/mommy-and-me-easter-outfit-ideas-for-2026`
  - `https://www.dresslikemommy.com/blogs/news/mommy-and-me-easter-outfit-ideas-for-2025`
  - `https://www.dresslikemommy.com/blogs/news/matching-family-outfits-for-easter-brunch-2024`
  - `https://www.dresslikemommy.com/blogs/news/best-matching-swimsuits-for-the-whole-family-2026`
  - `https://www.dresslikemommy.com/blogs/news/valentines-day-mommy-and-me-outfits-for-2028`
- One article that does contain merch links, `https://www.dresslikemommy.com/blogs/news/adorable-matching-valentines-day-looks-for-the-whole-family`, currently points to one generic collection URL (`/collections/all`) and multiple retired product URLs, so it still needs cleanup.

Recommended blog-link pattern:

- Easter articles: add links to `/collections/mommy-and-me`, `/collections/dresses`, and one current Easter-appropriate PDP.
- Swimsuit articles: add links to `/collections/swimsuits`, `/collections/family-swimsuits`, and `/collections/trunks`.
- Valentine's articles: add links to `/collections/mommy-and-me`, `/collections/dresses`, and `/collections/couples` or `/collections/matching-couples-t-shirts`.
- Back-to-school Daddy & Me articles: add links to `/collections/daddy-me`, `/collections/daddy-me-t-shirts`, and one current daddy-and-me PDP.

Implementation note:

- The theme already supports article-related internal-link modules, but the inline CTA in the article template is injected with JavaScript after page load. For SEO, important collection/product links should also exist in server-rendered HTML inside `article.content` or in a server-rendered block immediately following the article body.

## Orphan / Underlinked Page Findings

Verified structural issue:

- `/collections` exists and exposes long-tail collections, but `SHOP` does not link to it from the homepage.

Verified orphan collections:

- `https://www.dresslikemommy.com/collections/bottoms`
- `https://www.dresslikemommy.com/collections/christmas-pajamas`
- `https://www.dresslikemommy.com/collections/christmas-sweaters`
- `https://www.dresslikemommy.com/collections/christmas-tops`
- `https://www.dresslikemommy.com/collections/leggings`
- `https://www.dresslikemommy.com/collections/new-matching-outfits`
- `https://www.dresslikemommy.com/collections/pants`
- `https://www.dresslikemommy.com/collections/popular-family-matching`
- `https://www.dresslikemommy.com/collections/popular-mommy-me-1`
- `https://www.dresslikemommy.com/collections/skirts`
- `https://www.dresslikemommy.com/collections/sundresses`
- `https://www.dresslikemommy.com/collections/valentines-day-matching-outfits-1`

Recommended fix for orphan collections:

- If these collections should remain live, add internal links from `/collections`, the homepage nav, or related collection/article hubs.
- If they are legacy or duplicative, redirect or unpublish them instead of leaving them indexable but unlinked.

Verified orphan product:

- `https://www.dresslikemommy.com/products/backless-striped-jumpsuit`

Why this product is a true orphan:

- It appeared in the original sitemap crawl with no inbound internal links.
- It is not assigned to any published collection in the live Storefront collection graph.

Recommended fix for the orphan product:

- Add it to at least one live collection such as `/collections/jumpsuits` or another relevant category.
- Then make sure that collection is linked from `/collections` or another crawlable hub.

## Priority Fix Order

1. Remove or replace the 33 verified broken product links in old blog articles.
2. Update the 6 redirecting article links to their final destinations.
3. Point `SHOP` to `/collections` and keep the category directory crawlable from the homepage.
4. Add server-rendered merch links to seasonal article templates, starting with Easter, swimsuits, Valentine's, and back-to-school clusters.
5. Add contextual related-collection links inside product descriptions by category template or metafield.
6. Resolve the 12 orphan collections and attach the orphan PDP `backless-striped-jumpsuit` to a linked collection or redirect it.
