# Organic feed + Christmas SEO — 2026-09-28

Owner: CEO (Claude Code). Lane: million-plan README §4, items 1–3. All free traffic; no paid media (owner ended paid marketing 2026-09-28).

## 1. Merchant feed photos — premise disproved

The plan listed "only 1 image per offer" as a Google free-listing gap. Readback disproves it:
- Shopify: all 296 active products have 2–13 images (157 have 4).
- Merchant Center 513542500 offer detail: sweater `shopify_US_7227435450465_41871766519905` shows 1 main + 3 extra images; Christmas onesie `shopify_US_9473151696993_47169853915233` 1 + 3; swimsuit `shopify_US_6718945034337_39756755861601` 1 + 6.
- Nothing to fix. Removed from the queue.

## 2. Variant age group + gender for Google (fixed, LIVE_VERIFIED)

Found on the onesie offer: size "Baby 3-6 Months" was sent to Google as Age group **Adult**. 5,564 of 6,371 active variants had no variant age group, so every size inherited the product value (adult) or nothing. No variant had a gender.

The Google & YouTube app reads variant metafields `mm-google-shopping.age_group` / `gender` (proven on the swimsuit: variant `toddler` → MC "Toddler (1–5 years old)").

Mapping from the Size option (`plan.py`): Mother/Father/Adult/S–5XL → adult; Baby ≤3 months → newborn; months ≤12 → infant; 12–18 months, ages ≤5 years, ≤110 cm → toddler; 6+ years, ≥120 cm → kids. Gender: Mother/Girl → female, Father/Boy → male; Child/Baby/Adult keep the product value. 3 existing 13–14-year values (adult) left unchanged. 8 knit-hat variants (no Size option) skipped.

- Applied: 7,539 metafields (5,556 age groups, 1,983 genders) on 5,950 variants; 0 user errors.
- Readback: 5,950/5,950 variants match; 0 mismatches.
- Merchant Center readback (same session, ~10 min later): onesie Baby 3-6 Months now "Infant (3–12 months old)".
- Before-state and every change: `variant_age_gender_changes.csv`. Rollback: `metafieldsDelete` on (variant, `mm-google-shopping`, `age_group`/`gender`) for rows where the before value is empty.

## 3. Brand consistency (fixed, LIVE_VERIFIED)

81 active products had vendor `dresslikemommy.com` (Google brand) vs 215 `Dress Like Mommy`, the May 2026 canonical (`ops/scripts/apply_vendor_backfill.py`). The new listing engine had regressed it.
- Set vendor `Dress Like Mommy` on the 81; readback 296/296 `Dress Like Mommy`. No collection uses a VENDOR rule.
- Fixed the source: `tools/runner_engine.py` `VENDOR` and `tools/accessories/create_xmas_knit_hats.py`.
- Rollback: `vendor_before.json`.

## 4. Christmas collection SEO (theme `5ec1df3`, LIVE_VERIFIED)

Before: the four Christmas collections (`matching-family-christmas-outfits` 38 designs, `christmas-pajamas` 15, `christmas-sweaters` 22, `christmas-tops` 2) did not link to each other, and showed no Christmas guide. The pajama styling-guide section pointed at two deleted articles.

- New `snippets/collection-christmas-cluster.liquid`, rendered in `sections/main-collection-banner.liquid`: link row to the other Christmas collections with ≥4 products (titles are Shopify-translated; eyebrow translated inline for 20 locales). `christmas-tops` (2 products) is linked to but not linked from, to avoid promoting a thin page.
- `templates/collection.json`: new `styling-guide-christmas` section (2026 pajama guide, sweater guide, photo-outfit guide) on the four Christmas collections; `christmas-pajamas` removed from the old pajama guide section.
- Release: GitHub sync dropped the push again; `sync_live_theme_from_main.py --apply` (2 files, MD5-verified) and a themeFilesUpsert of the template after confirming live == pre-change main. Drift after: 0.
- Live readback: EN, `/de/`, `/ja/` show the row and 3 guides with localized URLs; `/collections/pajamas` unchanged. Desktop row visible under the intro. On mobile the theme hides everything under the H1 by design ("products first"); the links stay in the HTML and the guide cards below the grid carry the links there.

## 5. Open

- The 3 Christmas guides have no translation in ar, cs, el, fi, he, hi, ja, ko, no, pt-BR, ro, ru (title, body, summary, meta). Codex translation job running; validate (HTML/href parity, numbers, length) before `translationsRegister`.
- Recheck Merchant Center after the next full sync for "Age group" issues and query matching.
