# Shop by occasion — 2026-09-26

Owner request (chat): "do this — Be the specialist… Organize the store by occasion". Owner choices: "Deep ones only" and "Build, check, then ask me".

## Inventory basis (live Admin read, 2026-09-26, 257 active products)

| Occasion | Active products | Decision |
|---|---|---|
| Christmas (tags Christmas / Christmas Sweaters / Family Christmas Sweaters / Christmas Pajamas / Christmas Tops) | 14 (`christmas-pajamas` alone: 1 active, 41 archived) | New hub `matching-family-christmas-outfits` |
| Family photos (tags Family Photos / Photo Ready / family photo outfit) | 52 | New `family-photo-outfits` |
| Halloween (`halloween-family-pajamas`) | 5 | Keep; homepage tile Sep 1–Oct 31 only |
| Beach vacation (`matching-family-vacation-outfits`) | 104 | Keep |
| Fall & winter (`fall-winter`) | 26 | Menu only (it overlaps the Christmas hub) |
| Easter 2, Birthday 2, Valentine's 3, Maternity 0 | — | Held until sourced |

## Shopify Admin writes (done, reversible)

- `collectionCreate` (UNPUBLISHED, no publications):
  - `gid://shopify/Collection/363955388513` `matching-family-christmas-outfits`: OR of the 5 Christmas tags, sorted `CREATED_DESC`.
  - `gid://shopify/Collection/363955421281` `family-photo-outfits`: OR of the 3 photo tags, sorted `CREATED_DESC`.
  - Titles, descriptions and SEO fields are in `build_collection_translations.py`. The only delivery claim is the existing "Delivery times are estimates" sentence.
- `translationsRegister`: title, body_html, meta_title and meta_description for the 20 published locales. That is 160 values from `collection_translations.json`. Readback: 160/160 exact, `outdated: false`.
- Rollback: `collectionDelete` both IDs. This also removes their translations.

## Theme change (local + preview only)

- Preview theme `156132933729` "DLM shop by occasion preview 2026-09-26" was duplicated from MAIN `133290917985`. Before the upload, the 41 changed files on the preview were byte-equal to `HEAD` `7ec0a83`. The 47 release files were uploaded with `--only`. After the upload, all 47 were byte-equal to the working copy.
- `templates/index.json`: the occasion tiles are now Christmas, Halloween, Photo Days (`family-photo-outfits`) and Vacation. Birthdays (which opened the general Dresses page) and Beach Days are removed.
- `sections/category-icons.liquid`:
  - Occasion tiles need 4 products, not 10.
  - Halloween occasion tiles show only from 0901 to 1031.
  - Curated tile photos for the Christmas and Halloween hubs.
  - Occasion captions are keyed by collection handle. Stored Translate & Adapt label overrides otherwise hid captions on translated homepages.
- `snippets/home-category-card-caption.liquid`: accepts an optional `collection_handle`.
- `snippets/home-category-localized-copy.liquid`: adds the christmas, halloween and caption keys.
- `snippets/dlm-mega-panel.liquid`:
  - Occasion columns are Christmas, Halloween, Family photos, Fall & winter and Vacation (plus Hawaiian in Family Matching).
  - The Family Matching card is now the Christmas hub.
  - Halloween menu links are hidden outside 0901–1031.
- `snippets/christmas-season-collection.liquid`: the Oct 15–Dec 25 header "Christmas" link and the homepage seasonal section now use the hub, not `christmas-pajamas` (1 active product).
- `locales/*.json` (35 files):
  - New keys `home_category_copy.halloween`, `caption_christmas`, `caption_halloween`, `mega_menu.halloween` and `mega_menu.family_photos`.
  - "Photo Days" is now translated where it was still English (14 locales), and accents are fixed (de/es/fr).
- `assets/category-tile-{christmas,halloween}-{360,600,900}.webp`: from the main images of `christmas-reindeer-family-matching-sweaters` and `trick-or-treat-family-matching-pajamas`.

## Verification

- `shopify theme check`: 283 files, 0 offenses. `git diff --check` is clean.
- Preview (in-app browser):
  - EN desktop at 1440 and FR mobile at 375: no Liquid errors and no horizontal scroll.
  - The Halloween and Vacation tiles render with captions in EN and FR.
  - The mega menu Occasion columns render.
  - The two new collections are unpublished, so their tiles and links are correctly hidden on the preview. A 4-tile desktop view was simulated in the browser from the real uploaded assets and strings.
- Known limit: stored theme translations override locale files for the 20 published locales. The de/es/fr accent fixes for the existing Photo Days keys will show only after those three stored values are updated on MAIN.

## Release plan (needs owner approval)

1. Publish both collections to the Online Store (`publishablePublish`). Read back the storefront URLs.
2. Commit the 47 theme files to `main` and push. Verify MAIN byte-equality. If the GitHub sync drops it, re-trigger through `main`.
3. Verify live: EN, FR and DE homepages, the tiles, the mega menu, the two collection pages (title, H1, products), and mobile at 375.

Rollback: `git revert` the release commit, and unpublish or delete the two collections.
