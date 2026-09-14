# Merchant landing candidate — frozen for independent review

Confidence: H for source parity and automated checks; rendered draft acceptance remains NOT RUN.

IMPLEMENTED locally from MAIN theme **133290917985**, `dresslikemommy/main`, updated `2026-07-02T16:47:21Z`. The 92-file baseline is a targeted set of actual MAIN files and their referenced validation dependencies. Every saved file matches Shopify's reported size and MD5. The active JS source MD5 is `61ded53111ee5002eb5c37b42a2c4b3f`; Shopify's public CDN response is minified, so the exact source came from Shopify's read-only download. One schema read adds a 366-byte generated comment prefix; stripping only that prefix reproduced the reported source size/MD5, recorded separately.

The **40-file** candidate changes only:

- Active `product-desktop-ux-20260513-ruler-sync.js`: initialize an explicit valid linked variant once, with exact role, size, axes and quantity one. Missing/invalid links retain the empty adult default. Unavailable variants remain visible but cannot enter the cart. Subsequent shopper choices are preserved.
- `main-product.liquid` and `product-desktop-ux.liquid`: explicit linked prices use Shopify's selected variant; the matching builder updates prices from server-formatted presentment amounts and restores the generic range when incomplete. An idempotent observer repairs later stale price replacements. Existing matching products' compare-at promotions remain suppressed.
- Two policy snippets and 21 published locale files: qualified item-eligibility copy, definite policy exclusions, localized policy links and existing damaged/defective guidance. Four existing return keys are revised; `returns_damaged` and `returns_shipping` are added. No product eligibility classification, title heuristic, delivery claim, measurement or policy data is invented.
- Fourteen inactive locale files receive only those two new keys, translated for locale parity. Their existing values and publication status are unchanged. All 35 locale JSON files now contain both keys.
- Reviewed Microsoft selector dictionary: **98 missing labels added**, two Spanish values preserved, zero existing-value conflicts. No layout/footer or Pinterest clone changes.

VERIFIED: **18/18 synthetic DOM journeys** pass, including cart identity, unavailable rejection, shopper changes, stale-price recovery, currencies and locale parity. Revision 3 fixes the independently reproduced literal money-entity display in headline and unit prices. It decodes once through an inert, angle-bracket-escaped textarea, inserts plain text, and clones prepared DOM without reparsing decoded text. Cases cover named/decimal/hex entities, nonbreaking/narrow spaces, ampersands, controls and markup-shaped text without created elements. The other 39 payload files are unchanged.

JavaScript syntax and whitespace pass. The unchanged Shopify validator uses telemetry opt-out and private temporary dependencies. Baseline/revision 2 passed all 40 files; revision 3's sole revised asset separately passes with zero diagnostics. Initial missing-context diagnostics were resolved by exact dependency reads. Policy wording remains unchanged after the root reported independent current-policy grounding PASS.

Review artifacts are in `theme_candidate/`: `candidate.patch`, `candidate_files.json` revision 3, its SHA-256 receipt, file manifest, validation logs, `revision3_price_entity.patch`, `revision3_validation.json` and exact baseline rollback files. The payload is **FROZEN_FOR_INDEPENDENT_REVIEW_NOT_UPLOADED**. Intended root-created preview **137881223265** must remain UNPUBLISHED, ready, and baseline-matched before writing only the 40 listed files. Earlier payload revisions are superseded.

Remaining: independently review code and return translations; then root verifies the draft on desktop/mobile, EN/ES plus another locale, exact linked variant **41498026442849**, currency/cart parity and summary/modal/full-policy agreement. No browser action, live edit, draft upload or publication was performed by this worker. Root owns any further write and publication decision.
