# Storefront UX and PageSpeed audit

Audit date: September 9, 2026 New York / September 10 UTC. Status: all staged theme repairs verified in the preview. Live publication and a correctly bound post-release PageSpeed run remain required.

[Open the isolated preview](https://www.dresslikemommy.com/?preview_theme_id=137888792673)

## September 11 variant-link verification

The current unpublished release already fixes the newly reported Together Heart deep link. Fresh source reconciliation found zero changes across its 527 files, MAIN or the predecessor since V6. Opening the exact 4XL/Green link selected the correct options and USD 26.99; one Add click placed that exact variant in the cart at quantity 1. Only the test item was removed, cart 0 verified, and the browser returned to MAIN before closing the audit tab. Independent source review confirmed this repair predates V6. No new theme patch or upload was needed.

MAIN still requires manual selection; parent independently reproduced both surfaces. Google's account review and five extreme Minimalist Heart source prices are separate owner scopes. See the [dated source and buyer receipt](variant-deep-link-20260911/READBACK.md). Automatic approval review blocked the broader shared-record updates; this owned audit packet contains the result, and shared records were left unchanged.

## Release scope and authority

The owner requested an audit and repairs for conversion and PageSpeed issues. Root preserved the dirty repository and created the separate unpublished theme **DLM UX Performance QA 2026-09-10**, ID **137888792673**, from the current combined Merchant preview **137881223265**. MAIN remains **133290917985**.

The candidate includes the existing Merchant/consent/localization repairs inherited from the combined preview. Publication must select this complete theme after reviewing its full difference from MAIN; publishing the older combined theme afterward would remove these UX repairs. The final manifest lists the exact files and hashes: **16 files changed and511 preserved relative to the combined draft;59 total differences from MAIN, including2 added consent assets inherited from the earlier work.** No claim is made that all inherited changes were reimplemented or exhaustively audited here.

Shopify's connector allows file writes on unpublished themes and blocks publishing and MAIN file writes. Owner publication in Shopify Admin is the remaining release step. No publication attempt was made. A detailed cross-task progress message was rejected by automatic approval review; a minimized general update succeeded, with no retry of the rejected identifiers. This did not block the permitted preview mutation.

## Findings repaired in the preview

| Finding | Repair and observed result |
| --- | --- |
| Mobile cart summary covered product and quantity controls | Removed mobile sticky positioning from the full cart footer. At 390×844, the footer began exactly below the items at 463.875px; overlap was false. Quantity controls remained visible and usable. |
| Desktop color filter navigated to a product | Corrected the open filter stacking order. Clicking Apricot applied the filter and showed 1 of 118 products; removing the chip restored 118. |
| Cart heading retained the old item count | Added the title section to cart refresh rendering. Quantity 1→2 produced heading/header 2 and USD53.98; 2→1 produced heading 1 and USD26.99. The subtotal itself was already correct. |
| Predictive-search async races | Cancelled obsolete requests and guarded response insertion by current query/focus. Ordinary mobile search returned 12 pajama results; Escape closed it. Race and error cases passed automated regression coverage. Native Escape was not falsely reported as a baseline failure. |
| Oversized and duplicate homepage image requests | Added accurate lazy-image sizing and dimensions; preserved coherent server-selected cards; deferred hidden hero slides until needed with safe decode and failure handling. Actual draft images used the expected size selection. Resource samples are diagnostic, not a controlled speed improvement. |
| Contrast, heading order and hero controls | Darkened the spotlight badge, fixed dark-footer text/selectors, made category headings h2, retained an accessible mobile hero h1, and provided 44×44px hero controls. The desktop gradient is rendered, with display:block overriding the global empty-div rule. |
| Internal text in homepage product previews | Filtered source/process captions in initial content and all candidate/fallback paths. Known English default captions are omitted on non-English pages, without replacing intentional localized content. Product source descriptions themselves were not edited. |
| Broken Danish footer headings | Normalized exact malformed aliases, restricted translation instructions to a real t: prefix, and rejected missing-translation output. Only three Danish locale values changed. DA/ES/EN rendered headings and the Danish accordion passed. Custom headings and consent controls remain preserved. |
| Homepage links dropped the selected language | Hero, category, curated collection and editorial links retain locale prefixes. Final real hero clicks landed on /da/collections/daddy-me and /es/collections/daddy-me. Both homepages had zero unprefixed main collection links and no horizontal overflow. |
| Arabic Together Heart child offers were hidden | Recognized the observed Arabic child label and bounded KID SKU without recategorizing other roles. All98 offers retain their IDs, prices and availability; child age2/white reached the cart atUSD24.99. Both7-row fit guides, mobile child/adult selection and the full source table passed. |
| Japanese product descriptions were erased | Preserved native ja/zh/ko text in cleanup while retaining explicit vendor and administrative safeguards. All3 Japanese paragraphs render exactly, survive size/guide interaction and pass mobile inspection; all140 source table cells remain unchanged. |

## Browser and source evidence

Actual in-app browser journeys covered 1280×900 desktop and 390×844 mobile: homepage/hero; menu open and Escape; predictive search; collection filtering/removal; Together Heart Adult S/White variant; add to cart; quantity changes; standard checkout entry; fit guide open/close and cm/in conversion; footer contrast/language selector; Spanish and Danish navigation. Desktop/mobile standard checkout displayed Contact, Delivery, Shipping method and Payment with the expected total. No contact/payment details or order were submitted. Only the auditor's test line was removed and cart0 was verified; the fit guide was returned to cm.

The preview bar identified the exact draft, and its image path used /cdn/shop/t/105/. V5 verified the original14-file scope at02:05:01UTC. V6 then staged the two localized PDP fixes; the independent after-query verified both exact hashes and the other525 preview files, with MAIN and the earlier combined draft unchanged. All527 candidate files exactly match the full V6 checked copy and uploaded source. See localized-pdp-v6/after.json and final-source-validation.json. Independent reviewers inspected each staged payload, exact inverse and scope; their browser evidence review did not constitute a second browser replay.

## PageSpeed

[Owner-supplied report](https://pagespeed.web.dev/analysis/https-dresslikemommy-com/oabgq2puhy?form_factor=desktop), generated September9 20:43:03 EDT:

| Metric | Desktop | Mobile |
| --- | --- | --- |
| Performance | 96 | 82 |
| Accessibility | 95 | 92 |
| Best practices | 92 | 92 |
| SEO | 100 | 100 |
| Laboratory LCP | 1.3s | 4.4s |
| Total blocking time | 0ms | 0ms |

Mobile origin field data passed Core Web Vitals with LCP1.7s and CLS0; INP was unavailable. Desktop field data was unavailable. Field data is historical and is not proof of this repair.

A new PageSpeed run was attempted with the preview URL, but Google's report loaded MAIN's /cdn/shop/t/100/ assets and old template rather than the draft. Its performance71/LCP9.2s **cannot measure this candidate's improvement or regression**. See pagespeed-attempt.json. A post-publication run must verify the actual released source before accepting its scores.

Browser image samples decreased from21 entries/2,060,128 encoded bytes to13/1,105,388, but product selection, timing, autoplay and preview overhead differed. No percentage gain or conversion uplift is claimed. Platform telemetry/client/CSP errors were recorded; consent and security controls were preserved.

## Remaining issues and limits

- **Together Heart source repair completed by its separate owner:** English and20 body translations now show unavailable hip/waist values and corrected buyer copy. The product-specific recurrence path was also repaired;98 variants and80 other translations were preserved. This audit then verified the two remaining theme rendering repairs in V6. Their published acceptance remains pending; do not repeat product-source writes. See the adjacent 2026-09-10-together-heart-source-repair/READBACK.md and localized-pdp-v6/READBACK.md.
- **Amazon Pay:** the button reported it was currently unavailable on both MAIN and preview. Standard checkout worked. The cause and provider acceptance remain unverified; financial configuration was not changed.
- **Localization breadth:** English fallback text remains in portions of localized editorial/trust/footer copy. The tested navigation fixes do not certify all21 languages, all products, accessibility against every criterion, or every device.
- **Publication and outcomes:** source/preview repairs are verified; published behavior, a valid new PageSpeed score, completed payment, sales and conversion uplift are unverified. No finite audit establishes a perfect website.

## Verification artifacts

- baseline-audit.json: supplied PageSpeed and reproduced live failures.
- final-release-manifest.json and final-release-readback.json: staged files, preserved source and release scope.
- final-release-rollback.json: the exact16-file inverse to the combined baseline; each staged revision also has its own narrow inverse.
- regression-tests.txt:20 meaningful homepage/search/cart tests passed. footer-test-results.txt:8 source/locale contract tests passed; these do not execute Shopify Liquid.
- theme-check-v5.json and theme-check-v5-run.json: earlier full527-file Shopify Theme Check, zero diagnostics. V6 reran the complete check with zero diagnostics in localized-pdp-v6/theme-check.json and theme-check-run.json.
- localized-pdp-v6/regression-results.txt:42 production-script regressions pass; browser-after.json records Arabic/Japanese desktop/mobile and EN/FR/KO holdouts. independent-after-review.json distinguishes independent evidence review from root browser actions.
- remaining-findings.md: product-source and payment evidence.
- candidate-source-validation.json: all527 candidate files exactly match the full-theme-check copy;16 modified-file hashes are bound to the exact uploaded release.
- final-checks.json: final continuity and scoped whitespace results.

## Single next owner action

Review and publish **DLM UX Performance QA 2026-09-10 (137888792673)** in Shopify Admin after confirming MAIN has not changed since the final source receipt. This comes first because shoppers receive the fixes only after release. It is the combined release, including the earlier Merchant/consent changes; preserve the old MAIN for rollback.

Continuation prompt: “
