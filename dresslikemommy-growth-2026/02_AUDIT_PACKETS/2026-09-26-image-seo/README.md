# Image SEO — alt text, filenames, captions (2026-09-26)

Owner request: make every storefront image's filename, alt text and caption strong for search engines and AI recommendations; fix current images and keep new listings fixed automatically.

## Baseline (read-only audit, 2026-09-26T18:43Z)

- 261 ACTIVE/DRAFT products, 1,287 images. 1,143 need better alt text: 545 templated (`Alternate image of …`), 536 empty, 126 duplicated within a product, 53 numbered (`… photo 3`), plus title copies and over-length.
- 889 images have generic filenames (on active products: `ChatGPT_Image_…` 401, `pomelli-image_…` 520, supplier `O1CN…` codes 5).
- Blog: 32 published featured images, 25 with empty alt. Collections: 8 images, all with alt.
- 150 active product image files are embedded in blog article bodies.
- Cause for new listings: `poll_shopify_import_autofill.py` processes a product once at creation, before photos exist, so the newest listings went live with empty alt.

Report: `image_seo_audit_20260926T184335Z.csv`.

## Prepared (local, not yet applied)

- `proposed_product_alts.json`: 1,143 image-specific alt texts written by 10 vision reviewers from the actual thumbnails, per `ALT_STYLE_GUIDE.md`. Validator: 0 invalid, 0 missing, each batch file equals its batch's media set, 50–125 chars (avg 93).
- `proposed_article_alts.json`: 25 blog featured-image alt texts.
- `image_flags.json`: 60 product-image flags (title/image mismatches, screenshot artifacts, possible third-party IP).
- Apply path: `python3 ops/scripts/image_seo.py apply --alts <file> [--execute] --receipt <file>`; refuses rows whose live alt changed since the queue; reads back every write.

## Theme

- `snippets/jsonld-seo.liquid`: Product JSON-LD `image` entries become `ImageObject` with `url`, `contentUrl` and `caption` (= media alt, fallback product title).

## Gates

- Live Shopify writes and the persistent automation (launchd guard + daily scheduled vision task) were blocked by the session permission layer and await the owner's explicit approval.
- Renaming existing live filenames is not proposed: it changes image URLs used by Merchant/Pinterest feeds and by 150 blog embeds, for a weak ranking signal.

## Applied (owner approved "Apply alt text", 2026-09-26)

- Products: 1,143/1,143 alt texts written via `fileUpdate` at 19:16Z; 0 user errors, 0 readback mismatches. Receipt with every before/after: `apply_products_receipt.json`.
- Blog featured images: 25/25 written via `articleUpdate` at 19:18Z; 0 errors, 0 mismatches. Receipt: `apply_articles_receipt.json`.
- Independent sample check before apply: `independent_sample_verification.json` (73 PASS, 4 MINOR, 3 FAIL; the FAILs and one MINOR were corrected).
- Post-apply re-audit: product images 1,287/1,287 alt OK; blog featured images 32/32 alt OK.
- Live storefront readback: `/products/jingle-bells-santa-family-matching-sweaters` renders the new gallery and related-card alts.
- Side effect: `articleUpdate` re-uploaded all 25 blog featured images. Pictures are visually identical (24 byte-identical renders; 1 re-encoded JPEG checked by eye). 11 old article-image URLs now 404; no article body or theme file references them. Details: `article_image_url_changes.json`.
- Rollback: re-apply `live_alt_before` from the receipts with `image_seo.py apply --force`.

## Guard installed (owner approved, 2026-09-26)

- LaunchAgent `com.dresslikemommy.image-seo-guard` runs every 15 min. First run 21:35Z renamed 58 new-listing files (`guard_first_run_renames.json`), 0 errors, alt preserved 58/58, new URLs load 58/58; second run 0 planned.
- Old filenames now 404. The only stale reference seen is Judge.me's hidden widget `data-image-url`.

Still not approved: JSON-LD caption deploy, daily vision task.
