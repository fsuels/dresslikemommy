# Listing claims check, after claims-fix-4 (2026-11-26)

Run: `python3 ops/scripts/check_listing_claims.py --all-locales --json` (328 ACTIVE products, en + 20 locales). Baseline: `claims-check-baseline-2026-11-26.md`.

| category | baseline | after |
|---|---|---|
| craft | 1 | 0 |
| english_leftover | 6 | 0 |
| health_skin | 1 | 0 |
| internal_leak | 3 | 0 |
| performance | 17 | 0 |
| translated_claim | 141 | 0 |
| translation_defect | 327 | 327 (untouched, waits for owner approval) |
| total | 496 | 327 |

Outside translation_defect: 0 remaining.

## What changed (fields body_html / descriptionHtml only; no title or meta_title key written)
- 44 products, one at a time. Before-state (EN + 20 locales of the touched fields): `ops/organic/receipts/2026-11-26/claims-fix-4/<handle>-before.json`; per-product after check: `<handle>-after.json`.
- English sentence rewrites (EN + 20 locales re-registered, 0 outdated): perfect-fit and ensure-fit wording (swimsuits, trunks, father-baby sets), "wrinkles low / keeps airflow" removed (3 pajama sets), hand-dyed removed (blue tie-dye, 3 places), "gentle against skin" removed (French halter dress), "quick to dry" removed (summer plaid), "lasting quality" removed (geometric swimsuits), spooky skeleton "measurements are not available" replaced by "compare chest, sleeve, and length with a garment that fits well" (chart has those columns).
- Vendor image host: 3 supplier image tags removed from he body (yellow beach outfits) and 1 from el body (tropical beach outfits); English has no image at those spots.
- Translation-only rewrites (English already clean): es/de/it/nl/pl/pt-BR/fr/cs guarantee and perfect-fit renderings, ro "durabil" style line, 4 small extras found on re-run.
- matching-dad-and-son-pink-black fr: whole description was a stale translation of an older English body (quick-dry, chlorine-resistant); retranslated from current English, size table byte-identical.
- Also fixed inside touched sentences: de and pl truncated last clause of one blue tie-dye sentence; el "umbrella" and it "eyeshadow" mistranslations of "ombre".
- Glued-letter defects (327) were not touched; per-product counts unchanged before/after.

## Round 2 (Calidad V22)
- spooky-skeleton: advice now "compare chest, hip, sleeve, and length" (EN + 20).
- Script: new rule performance/ensures (ensure/ensures/ensured/ensuring), removed the "find your perfect fit" allowlist, cs terms (zajišťuje, perfektní střih/padnutí); 2 test cases added (22 tests pass).
- tie-shoulder and oversized-heart: EN + 20 rewritten. 22 more products with EN "ensures/ensuring" surfaced: EN fixed and cs fixed; the other locales were already rewritten earlier in 8 languages, but ar/da/el/fi/he/hi/ja/ko/no/ro/ru/sv still carry the older "ensures" wording on those extra sentences (not detected by the script, not re-translated).
- matching-dad-and-son-pink-black: body images were an orange leaf-print dad-son pair and 5 mother-daughter swimsuit thumbnails with links to other products (viewed): not this product. All body image/link tags after the size table removed in EN + 20 (gallery untouched; before-state `*-before-images.json`).
- Final: 0 outside translation_defect. translation_defect = 327 glued-letter (unchanged) + 188 table-id (new rule added by another agent, pre-existing dropped table ids in translations, not from these edits).
