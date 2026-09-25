# Read-only article chrome patch route

Confidence: H for source cause and file/key route; no runtime or live verification performed in this lane.

The article-body translation API does not control the reported English chrome. It is literal text in `sections/main-article.liquid` and `snippets/style-journal-internal-links.liquid`. Existing translated theme keys are available for all 20 published non-English languages.

## Smallest cohesive patch

Edit exactly those two Liquid files plus `locales/en.default.json` and the 20 published storefront locale files: `ar`, `cs`, `da`, `de`, `el`, `es`, `fi`, `fr`, `he`, `hi`, `it`, `ja`, `ko`, `nl`, `no`, `pl`, `pt-BR`, `ro`, `ru`, `sv` (all `.json`). This is 23 files; schema locale files need no change. The observed Shopify locale identifiers are `no` and `ro`, not the separate existing `nb` and `ro-RO` files.

Use the existing native Liquid `t` convention. Reuse these existing keys, which are present in all 20 published locales:

- `storefront.journal.title` — replace news-only hardcoded Style Journal at main-article:8 and collection-guide label at internal-links:900.
- `storefront.journal.read_time` — main-article:128, matching the implementation already in main-blog:155.
- `storefront.menu.shop_now` — main-article:241.
- `storefront.menu.shop_edit` — main-article:253.
- `sections.breadcrumbs.cat_mommy_me` and `.cat_family_matching` — main-article:296–297 buttons.
- `storefront.collection_fallback_description` (`title` parameter) — reusable fully translated neutral collection teaser if selecting the compact teaser approach below.

Add the following 20 keys under `storefront.article` in the default and all 20 published locale JSON files. These are suggested exact new key names; they do not exist yet:

| Key | English source value / use |
| --- | --- |
| breadcrumbs_label | Breadcrumbs (main-article nav aria-label) |
| author_credential | Family Fashion Editor |
| contents_label | In this article |
| contents_aria_label | Table of contents |
| recommended_products | Recommended products from this guide |
| written_by | Written by |
| author_bio | Dress Like Mommy's editorial team builds practical shopping guides for family matching outfits, mommy and me looks, daddy and me outfits, swimwear, pajamas, and photo-ready seasonal styles. |
| shop_look | Shop the look |
| compare_title | Ready to compare matching outfits? |
| compare_body | Browse the core collections for mommy and me outfits, daddy and me styles, family matching sets, and vacation-ready swimwear. |
| continue_reading | Continue reading |
| more_from | More from {{ journal }} |
| inline_cta_text | Ready to shop the looks from this guide? |
| inline_cta_label | Shop matching collections |
| shop_collection | Shop the collection |
| shop_collections | Shop the collections |
| build_look | Build the look from this guide |
| guide_caption | Read {{ title }} before you shop. |
| read_before_shop | Read the guide before you shop |
| view_all_guides | View all guides |

Main article affected regions: lines 8, 13, 123–139, 166–168, 241, 253–254, 281–297, 314–315. Shared snippet affected fixed-string regions: 399–426, 696–718, 736, 758–759, 822–823, 900–904.

For JS fallback text (main-article:166–167), inject `| t | json` into the JS expression rather than surrounding translated text with handwritten quotes. Use the same translated CTA text and label as the data attributes. Its current fallback URL `/collections/matching-outfits` should use `routes.collections_url | append: '/matching-outfits' | json` so a missing data element does not drop the active language. Normal selected collection URLs already come from the collection objects; preserve those, handles, metafield routing overrides and tracking attributes.

## Collection teasers: precise cause and compact repair

The snippet contains 80 nonempty title assignments (23 unique strings) and 80 distinct nonempty English captions in article-handle/context branches. At internal-links:371–396, `collection_link_n_object.title` and `.description` only run if the earlier English value is blank. Hence a fully translated collection still displays an English card.

Smallest compact fix: preserve the existing collection-handle selection logic and actual collection-object URLs, but after each nonblank collection object is resolved, always derive its visible title with the existing `collection-seo-fallback` snippet, `field: 'display_title'`. This is the same display-title mechanism used by `sections/main-collection-banner.liquid:7`; it maps all 12 hardcoded target handles to existing translated `sections.collection_seo.display_titles.*` keys. Unknown explicit metafield handles retain the collection object's title through that snippet. Set its caption using existing `storefront.collection_fallback_description | t: title: collection_link_n_title`. Do this before `inline_cta_label` is assigned at line425, so CTA and cards use the same localized title. Preserve blank-object guards and do not invent destinations.

This compact choice deliberately replaces context-specific teaser prose with the existing neutral collection comparison copy (also for English if applied uniformly). It avoids adding 103 branch-specific translation strings per locale. If retaining every original teaser sentence is required, each of the 23 unique title and 80 unique caption strings must instead become a stable locale key; that is a larger copy-preserving alternative. Do not merely empty assignments: an untranslated `.description` fallback or the concatenated English fallback sentences can recreate leakage.

Guide titles and captions in collection-guide mode already come from localized article title/excerpt/content at lines650–680; only the empty-caption concatenations at696–718 need `guide_caption | t: title: ...`. Related cards already render the shared article-card with localized article resources, so no additional article-card edit is required for the reported labels.

## Verification boundary

NOT RUN: Liquid/theme checks, rendered QA, Git sync or live checks for this proposal. This lane made no theme/source changes. Root should validate all 21 files' JSON/key/placeholder parity, render both article CTA branches and related-article fallback, check one narrow/desktop article and collection-guide view, verify no `translation missing` output and preserve active-locale links. Root owns `main` sync and Shopify/public readback.
