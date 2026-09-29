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

## 5. Christmas guide translations (LIVE_VERIFIED)

The 3 Christmas guides had no translation in ar, cs, el, fi, he, hi, ja, ko, no, pt-BR, ro, ru. ChatGPT-app Codex (Pro plan, no API) translated title, body, summary and meta description per locale (`guide_translations/codex_prompt_example_ar.txt`); logs show no external translation calls.
- Validator `christmas_guide_translation_validate_register.py`: identical tag sequence and hrefs, every source number present, not left in English, title ≤80 / meta ≤170 chars. 12/12 locales OK.
- Registered with `translationsRegister` against current digests: 144 fields, 0 user errors. Arabic was re-registered once because its job rewrote the file after the first registration.
- Independent readback: 144/144 equal the validated files, none outdated. Live: `/ar/` and `/fi/` Christmas collections show translated guide titles; `/pt/blogs/news/family-christmas-photo-outfits-2026` serves the Portuguese H1.
- Rollback: `translationsRemove` for those locales/keys on the 3 article IDs. Files: `guide_translations/<locale>.json`.

## 6. Open

- Recheck Merchant Center after the next full sync for age-group issues and baby/kids query matching.
- Owner: Shopify AI shopping (agentic storefronts) terms; see million-plan README §4.

## 7. Follow-up 2026-09-29 (`followup-2026-09-29/`)

- **Merchant age groups: LIVE_VERIFIED after Google's sync.** 10/10 sampled offers show the right value: Baby 3 Months = Newborn, Baby 6-9 months and 12 Months = Infant, Child 3 Years and Girl 4-5 = Toddler, Girl 7-8, Child 12 and Boy 9-10 = Kids, Mother M = Adult; gender Female/Male on Girl/Boy/Mother; brand "Dress Like Mommy". One sampled offer (archived Red Plaid) no longer exists.
- **Remaining Merchant item issues: no feed action.** Not approved 2.28K = 1,303 shipping-currency mismatch + 654 missing price + 7 Korean business number; the first two are "Found by Google" crawl offers (numeric IDs); the Shopify-app offers for the same products are approved. Korea is not a sold market.
- **Store quality (US/AU "Great").** "Images per offer: 1 image" (Low) and "High resolution images" 21% (US) / 27% (AU) are 30-day trailing scores that contradict current offers (1 + 3–6 extra photos). Shopify photos are 756–941 px wide (5 of 1,456 reach 1,500 px). Recheck after the 30-day window since the Sep 27 source cleanup; if still Low, test Google Product Studio or real (not interpolated) upscaling. Return window/cost "Incomplete" = return policy 9335482178 still in Google review; store rating = Google Customer Reviews (owner).
- **Christmas guide translations: date and unit fix.** Codex had kept "December 8" in English in 10 locales and "12–16 days" / "30-day" in hi/ja/ko. Replaced with local forms (e.g. 12月8日, 8. prosince), re-validated, re-registered; readback 144/144, none outdated. Negated delivery disclaimers ("not a guaranteed arrival date") confirmed in ru/ja/pt-BR/ko/ar.
- **Leaked translation placeholders (`__DLMTOK0___`) fixed on 10 collection translations**: ar titles of family-tops, family-swimsuits, family-sets, family-sweaters, matching-couples-t-shirts; ar meta of swimsuits, new-arrivals; ja titles of best-sellers, popular-mommy-me-1; pl title of daddy-and-me. Rescan: 0 collection hits. Before/after: `collection_token_fix_receipt.json`. 160 more hits sit on 128 products, all ARCHIVED/DRAFT (not visible); list in `archived_product_token_hits.json` for when any is restored.
- **M2 best-sellers wording.** Admin meta description said "top-rated … fan-favorite … proven favorites" (no reviews back it). New EN: "Best-selling mommy and me and family matching outfits, sorted by what customers order most…" (the collection is sorted BEST_SELLING) + 20 translations (Sonnet subagent, parent-checked); readback 20/20. Theme `collection-seo-fallback.liquid` intro phrase "top-rated dresses…" → "dresses…". Before-state: `bestsellers_before.json`. The Black Friday article body has no deal/bestseller claims left (engine repaired it 2026-09-29).
- **BLOCKED (owner login):** Shopify admin is logged out in both the in-app browser and Chrome; enabling AI shopping (agentic storefronts) needs the owner to sign in and accept Shopify's terms.
- **Leaked placeholders, full sweep (`followup-2026-09-29/token-fix/`).** Scan of every translatable resource type in 20 locales found 328 more live fields with `__DLMTOK` placeholders (excluding 16 on archived products): 278 image alt texts, 27 collection metafields, the /collections/all SEO title, the Arabic shop meta description, 1 Arabic menu link ("Family Matching Sets"), and 4 page bodies (ar/hi/ja shipping-and-delivery and wholesale pages; Arabic contact email showed `info@__DLMTOK0___`; Hindi had an `<hr>` translated to `<घंटा>`). ChatGPT-app Codex (Pro plan) re-translated each from the English source; validator: no placeholder, identical HTML tag sequence, emails/URLs/domain kept; 328/328 OK. Arabic shop meta "free shipping on all orders" changed to "standard shipping included" (store convention). Registered 328, 0 errors; readback 328/328 clean and not outdated; rescan of PAGE/LINK/SHOP/COLLECTION: 0 hits; live /ar/ pages show `info@dresslikemommy.com`. Rollback: `items_before.json` (`broken` values, re-register by digest).
- **AI shopping:** Shopify auto-enabled agentic storefronts for eligible stores on 2026-03-24; settings at `admin.shopify.com/agentic`. Owner check only (both browsers logged out of Shopify admin).
