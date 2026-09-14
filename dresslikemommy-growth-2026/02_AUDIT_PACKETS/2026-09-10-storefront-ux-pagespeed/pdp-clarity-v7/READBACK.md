# September 11 product-page clarity repair

Confidence: H for the scoped preview fixes. Status: IMPLEMENTED and VERIFIED in unpublished theme **137888792673, DLM UX Performance QA 2026-09-10**. Published acceptance, PageSpeed improvement and conversion uplift remain unverified.

## Changes

Two buyer-facing defects were reproduced on the Together Heart product page in desktop and mobile views. The heading ended at “Browse more from”, and the accessible similar-styles link ended at “View similar styles in ”. The generated copy map exposed Liquid placeholders to server rendering before the browser could substitute collection names. Exactly 105 templates across 35 locales now preserve the context token; 2,206 unrelated copy values remain identical. Both browser consumers use literal replacement callbacks, preserving punctuation and dollar signs in collection names. The local generator applies the same three-key normalization so regeneration retains the repair.

Products without reviews also received an automatic “New arrival” badge and an unsupported “loved by moms” endorsement. The sole render call for that fallback was removed. Genuine Judge.me preview/full-review blocks and native positive-rating markup are unchanged; no review, product, price or arrival-date data was edited.

The exact three uploaded files are `assets/global.js`, `sections/main-product.liquid`, and `snippets/product-page-copy-map.liquid`. The only additional implementation file is the local `ops/scripts/build_product_page_copy_map.py`. All theme work used the reviewed candidate directory, preserving the dirty root theme.

## Verification

| Check | Observed result |
| --- | --- |
| Source and target | Fresh prewrite guard passed; after-readback matched all 527 candidate files and the complete Theme Check copy. Exactly 3 files changed and 524 remained identical. MAIN and the predecessor are unchanged. |
| Regression suite | 51/51 pass, including frozen original failures, all 35 locales, actual inline/global production functions, literal-dollar names, repeated application, native Arabic/Japanese markup and generic/search labels. |
| Theme validation | Full 527-file Shopify Theme Check: zero diagnostics. `node --check` for global.js and scoped `git diff --check` pass. |
| Generator | Actual generator with its unchanged source-extracted local JSON helpers passes 105 real templates, missing/raw fallback and unrelated-placeholder holdouts. Normal CLI import is blocked by the bundled Python's missing pre-existing deep_translator dependency; that CLI was not certified. |
| Desktop/mobile product | Complete collection headings and accessible names; unsupported fallback absent; selected Adult / 4XL / Green still displays $26.99. No horizontal overflow at 390px. |
| Cart | One real mobile Add click added variant 46512190292065 at quantity 1 and $26.99. Only that item was removed; cart 0 and zero rows verified. |
| Collection navigation | Actual click reached `/collections/family-tops`, titled Family Matching Tops. Product return retained the correct back destination and generic fallback. |
| Genuine review | The leopard-print swimsuit retained its visible 5.00 rating and 1-review badge. Clicking it scrolled to Customer Reviews, 29.8px from the viewport top. |
| Languages | English, Spanish, Japanese and Arabic rendered complete context labels and localized collection links without the removed fallback. Mobile samples had no horizontal overflow; Arabic also passed the desktop check. |
| Browser health/cleanup | Console warning/error samples were empty. Normal Exit preview returned to MAIN `/t/100/`; English, cart 0 and original 1280×720 viewport restored; owned tab closed. |

Independent prewrite review caught the shared-global replacement edge and verified its correction plus exact apply/inverse bodies. The postwrite review inspects source and browser receipts; it is not a second browser replay.

## Release and limits

The combined candidate now differs from its preserved predecessor in **19 files, with 508 unchanged**; the complete difference from MAIN is **61 files**, including inherited work. `../final-release-manifest.json`, `../final-release-readback.json` and `../candidate-source-validation.json` are current V7 summaries. V6 versions are preserved here. The three-file inverse is `inverse-variables.json`; the complete 19-file inverse to the predecessor is `../final-release-rollback.json`. Rollback bytes are checksum-bound, but no rollback was executed.

These results do not certify the entire storefront as perfect. Existing Japanese/Arabic size hints still contain English; Arabic collection translations contain underscore punctuation. Broader localized product/category copy and classification remain open. The prior Amazon Pay finding remains provider acceptance unverified; standard checkout had passed earlier. No checkout/payment/configuration action was repeated here. Positive-review coverage is one product, not review-authenticity or catalog-wide certification.

Shopify's connector blocks publishing and MAIN writes. The single next owner action is to review and publish **DLM UX Performance QA 2026-09-10 (137888792673)** in Shopify Admin after a fresh source-conflict check, preserving the old MAIN for rollback. This goes first because customers only receive the staged repairs after release. Then verify the live buying path and run PageSpeed against the actual published source.

Continuation prompt: “Continue from the September 11 V7 product-page clarity receipt. Verify current theme roles and hashes; preserve the combined 137888792673 release and other owners' changes. After owner Admin publication, test the live purchase path and PageSpeed. Keep remaining localization and Amazon Pay findings explicit; do not repeat product-price repairs or the previously rejected broad-record update.”
