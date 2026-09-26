# Image SEO Loop

Keeps every storefront product image findable by Google Images, Google Shopping and AI assistants: image-specific alt text, clean filenames on new listings, and alt text exposed as `caption` in product structured data (`snippets/jsonld-seo.liquid`).

Tool: `ops/scripts/image_seo.py` (stdlib only, runs under `/usr/bin/python3`). Tests: `python3 -m unittest ops/tests/test_image_seo.py`.

## Layers

1. **Guard (every 15 min, LaunchAgent `com.dresslikemommy.image-seo-guard`, template `ops/shopify/com.dresslikemommy.image-seo-guard.plist`, log `~/Library/Logs/dresslikemommy/image-seo-guard.jsonl`, no vision).** `image_seo.py guard --execute` scans ACTIVE and DRAFT products.
   - Empty or one-word alt text gets a product-grounded baseline (title, plus the single color option when present), so no image is ever blank.
   - Generic uploads (`ChatGPT_Image_…`, `pomelli-image_…`, `O1CN…` supplier codes, `IMG_…`, hashes) are renamed to `<handle>-NN.ext`, but only on products created inside `--rename-window-hours` (default 72) and never when a blog article embeds that file.
   - It never overwrites descriptive alt text and never renames older products.
   - Renamed files get new URLs and the old ones 404; Merchant/Pinterest feeds pick up the new `image_link` on regeneration.
2. **Vision review (daily, scheduled Claude task).** Replaces baseline, templated, numbered, duplicate, title-copy and over-length alt text with a description of what the image actually shows.
3. **Structured data.** Product JSON-LD emits each image as an `ImageObject` whose `caption` is the image's alt text.

## Vision review procedure

1. `python3 ops/scripts/image_seo.py queue --output <scratch>/image_seo_queue.json` (read-only). Stop if `count` is 0.
2. Download each `thumbnail_url` and view every image of each queued product, including images whose alt is already fine.
3. Write one row per queued image: `{media_id, product_id, handle, expected_current_alt (copy current_alt exactly), alt, flag}` following the style rules below.
4. Dry-run: `python3 ops/scripts/image_seo.py apply --alts <file> --receipt <scratch>/dry.json`. Fix every rejected row.
5. Apply: add `--execute --receipt dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-26-image-seo/apply_<UTC>.json`. The tool refuses rows whose live alt changed since the queue, then reads every written alt back. Non-zero exit means user errors or readback mismatches.
6. Report counts and any `flag` rows (wrong image on a product, supplier watermark, Chinese text, other brand logo).

## Alt text style rules

- Describe what is visible. 60–125 characters (validator: 15–125), one sentence.
- Lead with people and garment, then color, print, one or two details, and the view or setting.
- Use one natural shopping phrase when true: matching, mommy and me, family matching, daddy and me, matching couples. Use the product's print name when it matches the image.
- Unique within a product. Size charts: `Size chart for the <short name> with adult and child measurements`.
- Never: `Image of`/`Photo of`/`Picture of`; brand or domain; price, sale, shipping, stock, bestseller or quality claims; fabric unless the title states it; AI, ChatGPT, suppliers, 1688; a word repeated more than twice; numbering. Dropshipping: never imply a store, warehouse or stock.

## Known side effect

Setting a blog featured image's alt via `articleUpdate` makes Shopify re-upload the image. On 2026-09-26 all 25 updated images kept identical pictures, but 11 old article-image URLs stopped resolving. Pages pick up the new URL automatically; external caches refresh on recrawl.

## Out of scope / gated

- Renaming files of existing live products changes image URLs used by Merchant/Pinterest feeds and by blog posts; it needs an explicit owner decision per run.
- Translated alt text for other locales (`MEDIA_IMAGE` translations) is a separate translation-pipeline task.
