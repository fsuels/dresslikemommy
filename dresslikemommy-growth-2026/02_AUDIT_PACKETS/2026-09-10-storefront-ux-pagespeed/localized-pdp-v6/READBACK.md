# Localized product-page repair — V6

Status: IMPLEMENTED and VERIFIED in the existing unpublished UX preview. Published acceptance remains pending.

The coordinating owner completed the Together Heart source repair separately. This continuation changes only two theme files; product descriptions, translations, variants, prices, publications and source-chart records were not written here. The shared canonical interval was explicitly handed back before this closeout.

## Repairs and evidence

- Arabic role parsing now recognizes the observed للأولاد label and token-bounded KID SKU. A generic child fallback preserves already recognized boy/girl/baby/adult roles. The prior code exposed only 49 adult offers. The repaired production-script fixtures expose all98 original offers, two7-row guides and the same original values across all20 other locale holdouts.
- Japanese cleanup preserves native ja/zh/ko text while retaining explicit vendor-credit and administrative-artifact cleanup. The three Japanese paragraphs previously rendered as Together。。 /11。。。 /、、、。。. All three now render exactly, remain intact after size/fit-guide interaction, and match on390px mobile. The140 source table cells are unchanged.
- Actual Arabic shopper checks reached the cart with child age2/white, variant46512187113569 atUSD24.99, quantity1. Only that test item was removed and cart0 verified. Mobile age9–10/green selected correctly; child measurements74/29/39 through98/47/57 were preserved. Switching to adultS/white gaveUSD26.99. A fresh390px recheck reads only the visible highlighted S guide row:102/52/64, separate from the other six adult rows (selected-guide-recheck.json). The earlier parent-container text included every row and was not a selected-tooltip-only capture. Missing hip/waist measurements stayed unavailable.
- English/French/Korean buyer-copy holdouts passed in the rendered preview. French retains its existing benign space normalization before the semicolon. Japanese/Arabic390px pages had no page-width overflow. Screenshots were visually inspected in the tool transcript. Viewport returned to1280px, language toEnglish, cart0; units remainedcm.

## Exact release

Theme137888792673, DLM UX Performance QA 2026-09-10, remains UNPUBLISHED. The staged two-file mutation returned no user errors. The independent after-query verified both exact checksums and the other525 unchanged preview files. MAIN133290917985 and the preserved predecessor137881223265 remained unchanged.

All527 candidate files match the uploaded source and the full checked temporary copy. V6 totals16 changed/511 preserved relative to the predecessor; the full combined release differs fromMAIN in59 files, including two inherited consent assets. V5 receipts are archived here. Do not publish an older clone after this release.

| File | SHA256 |
| --- | --- |
| assets/product-desktop-ux-20260513-ruler-sync.js | e5a16e0cc2e9dca6cd5b40fce603b1cee54daa023943b1b5cd5033b401842438 |
| snippets/pdp-description-copy-cleanup.liquid | 04997bf4d29704d478115fac5e6588772e460e04eccffa0f6cd3e712d80e2219 |

The exact two-file apply and rollback payloads are apply.json and rollback.json. Their hashes are recorded in payload-summary.json. The cumulative16-file inverse is in the parent final-release-rollback.json. The large ruler asset had no inline API body; its inverse uses the preserved V5 checked copy bound to the fresh API MD5 and size. No rollback has been applied.

## Verification and limits

Root ran42 production-script regressions:28 Arabic and14 cleanup tests, all passing. The Japanese frozen fixture changed from6fail/8pass to14pass. The full527-file Shopify Theme Check returned zero diagnostics. Source/payload validation passed. Independent prewrite review passed; final independent source/evidence review is recorded separately in independent-after-review.json and .md.

The independent reviewer did not build or execute these repairs. Root performed the browser actions; reviewing those receipts is not a second browser replay. All98 offer mappings are exercised by the production-script fixture and exact embedded variant comparison, with one real cart addition and representative child/adult mobile selections. This is not an exhaustive physical-device or catalog-wide certification.

An early mobile click immediately after reload was superseded while the selector initialized. Fresh state showed the default adult role; after initialization, the same child action succeeded. No duplicate cart addition or repeated stage occurred. Current English-page console read contained no error entries.

One detailed cross-task status message was rejected by automatic approval review for exporting nonpublic identifiers. A minimized general status succeeded; the detailed rejected message was not retried. This did not block the two-file theme mutation or local evidence. Shopify's separate connector restriction on publishing and MAIN writes remains in force.

No publication, completed order, payment, new PageSpeed result, conversion lift or profit result is claimed. Earlier Amazon Pay unavailability and broader localization fallbacks remain separate findings.

Next action for this release: owner review and Admin publication of the current combined preview after a fresh MAIN conflict check, then exact published Arabic/Japanese buyer verification and source-bound desktop/mobile PageSpeed.

Continuation: use ops/prompts/paid-growth-ai-army-continuation-prompt.md with anchor2026-09-10-storefront-localized-pdp-v6-preview-verified, TA-22/TA-06 and this packet. Preserve product-source completion and every other owner's gates.
