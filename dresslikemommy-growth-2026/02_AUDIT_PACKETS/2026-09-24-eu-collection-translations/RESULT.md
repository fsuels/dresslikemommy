# Danish, Norwegian, Dutch and Greek collection translations — 2026-09-24

Owner request: "Make sure the Danish, Norwegian, Dutch and Greek versions of your store have translated collection titles and descriptions."

Shop locales: `da`, `no` (Norwegian; `nb.json` in the theme is not a published shop locale), `nl`, `el`. Public routes: `/da/`, `/no/`, `/nl/`, `/el/`.

## Two layers

Collection pages get their text from two places:
1. Shopify translation records (COLLECTION `title`, `body_html`, `meta_title`, `meta_description`). These drive most page titles and descriptions.
2. Theme locale keys (`sections.collection_seo.*`), which override the heading, meta and buying-guide copy for about 40 handles.

## Before

- Shopify: all 46 collections had a translation for every field, but 59 values were outdated (English changed): `matching-outfits` and `christmas-pajamas` in all four languages, plus 26 older Dutch meta/body values. Some of those old Dutch values made claims that are not in the English (for example "fabrieksprijs", "gratis wereldwijde levering", "Bestel vóór 10 februari").
- Shopify: 127 up-to-date values still had English collection names in them ("Mommy and Me Dresses", "Mother Daughter Swimsuits" and similar). About 150 meta titles translated the brand literally ("Klæd dig som mor", "Kle deg som mamma", "Kleed je als mama", "Ντύσου σαν τη μαμά").
- Theme: 20 English keys changed on September 24 (family matching outfits target page, retitled `matching-outfits`, related links) and had old wording in the four languages. Other collection keys in `da`, `no` and `el` still had English phrases.
- Public: in the 172 page checks (43 published collections × 4 languages), 114 titles, 17 H1s and 4 meta descriptions had English or a translated brand name.

## Changes

- Shopify `translationsRegister`, global locale scope: 317 values in 166 mutations, with 0 userErrors.
  - 59 outdated values were retranslated from the current English.
  - 127 values had their English leftovers fixed with minimal edits.
  - 131 meta titles had the brand name restored to "Dress Like Mommy".
- Theme commits on `main`:
  - `a2517b6`: 123 keys across the 4 locale files.
  - `86a4223`: season-tip links matching peer commit `cb6f0ea`.
  - `73a43fa`: consistent H1 wording for `new-women-outfits` in no/nl/el.
- The GitHub→Shopify sync did not apply in over 10 minutes. Live was also missing several other `main` commits. So `themeFilesUpsert` wrote files byte-identical to `main` to MAIN theme `133290917985`:
  - the 4 locale files;
  - `snippets/collection-seo-content.liquid` and `locales/en.default.json`, both from peer commit `cb6f0ea`. These were needed because the new tip links use `family_sweaters_url` and `family_pajamas_url`.
  - A follow-up upsert wrote no/nl/el again after `73a43fa`.

Translations were drafted by per-language subagents from the current English and checked mechanically by the root. The checks compared HTML tag and Liquid placeholder sequences, numbers and brand, looked for English leftovers and compared lengths; the root also reviewed a sample of each language. No English source, product, article, redirect, feed, ad or spend change was made.

## Verification

- Shopify readback: 317/317 exact. English source digests are unchanged, with 0 unplanned changes. Across 46 collections × 4 locales × 4 keys: 0 missing, 0 outdated, 0 English leftovers and 0 translated brand names.
- Live theme: all 6 upserted files parse identically to `main` HEAD, and the snippet is byte-identical. Shopify sync-back commit `e8aed27` echoed the upsert with no content change.
- Public: 172/172 pages return HTTP 200 with the correct `lang`. In titles, H1s and meta descriptions, 0 have English or a translated brand (before: 114/17/4).

## Residual notes

- The English source keeps "Free shipping + 30-day returns" in older copy and "one of our most popular categories" in `christmas-pajamas`, which has 0 active products. The translations are faithful to the English. Whether those claims are supported is an English-copy question.
- Some older translated bodies are serviceable machine-style prose. They have no English left in them, but they have not had a human native review.
- `aria-label` values in the related-link blocks are still English in these locales, as they were before.
- `locales/nb.json` is unused because `no` is the published locale, and it has 2 English fallback strings.

## Rollback

- Shopify: re-register values from `shopify_collection_translations_before.json`.
- Theme: revert commits `73a43fa`, `86a4223` and `a2517b6` on `main` and upsert the prior file contents. `live_theme_before_upsert_checksums.json` records the before checksums.
