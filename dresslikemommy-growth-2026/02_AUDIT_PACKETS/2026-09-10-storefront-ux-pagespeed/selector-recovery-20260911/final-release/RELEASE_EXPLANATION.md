# Current UX draft and remaining release gate

**Superseded on September 12:** the Couples repair is now saved and its rendered checks passed. Use the [final seven-file release explanation](../couples-grid-repair/RELEASE_EXPLANATION-20260912.md). This document retains the earlier four-file milestone and subsequent discovery chronology; its temporary collection hold is resolved in the draft. Owner Admin publication is still required.

The latest uploaded theme is **DLM UX Performance QA 2026-09-10 (137888792673)**. The name retains September 10, but the current four-file selector repair was uploaded **September 11 at 22:41:33 UTC / 6:41 p.m. New York**. Full source and six-theme inventory were read back at **22:50:06 UTC**. It remains **UNPUBLISHED**; the live theme is **dresslikemommy/main (133290917985)**.

**Publication is temporarily on hold for a separate Couples collection display defect discovered after the nine final product/cart checks.** The historical `PASS_WITH_LIMITS_READY_FOR_OWNER_ADMIN_PUBLICATION` in the 22:50 binding describes the completed product repair before that discovery. The subsequent [Couples rendered receipt](COUPLES_MAIN_READBACK.json) controls the current publication recommendation. No earlier candidate should be published while that essential repair is pending.

## What the draft fixes

The existing combined UX release repairs variant deep links, mobile cart overlap and quantity headings, filter click-through, stale search results, language-preserving links, accessible hero controls and image loading. It also preserves the earlier consent, Merchant landing and localization changes; these inherited changes are included in the complete release comparison.

The latest four-file repair additionally:

- Restores native selection when the custom selector cannot safely classify every size, so child sizes are not silently hidden.
- Keeps explicit Girl/Boy identities separate and adds the selected Trail shirt or shorts variant correctly.
- Preserves exact source size labels, including adult normal versus extended versions, in selectors, guides and the cart.
- Makes valid preselected variant links work with the mobile Add button while keeping the size-selection prompt for URLs without an explicit variant.
- Prevents a missing initial size guide from stopping matching-piece controls from loading.

The changed files are `assets/product-desktop-ux-20260513-ruler-sync.js`, `assets/component-product-desktop-ux-ruler-sync.css`, `assets/size-conversion.js`, and `sections/main-product.liquid`. The [complete source binding](complete-release-binding.json) records every final file and rollback reference.

## Preservation and verification

All **527 draft files** match the verified composite. The latest repair changes four files from the frozen V7 candidate, preserves 523 exactly and deletes none. Across the complete release versus MAIN, 61 files differ and two consent assets are added; **zero files are deleted**. Both configuration files and all 20 templates remain byte-identical to MAIN. All **525 live theme files remain unchanged**.

This UX work did not alter product records, prices, variant availability or source measurements. Native buying forms, genuine review widgets, app hooks and existing navigation remain present. This is scoped preservation evidence, not certification of every app or payment provider.

- Final ordinary desktop/mobile cart checks: **9/9 passed**, matching exact variant IDs, raw sizes and AUD prices. Every test item was removed. See [buyer readback](BUYER_READBACK.json).
- Latest focused regression suites: **20/20 passed**. Full 527-file Shopify Theme Check: **zero diagnostics**.
- Independent source reviews passed for native fallback, source labels, explicit deep links and missing-guide initialization.
- Live Couples acceptance: **failed** in English desktop/mobile, French, Spanish and Arabic. The theme hides the three collection products and displays old generated body text. This is the next repair before publication.

No measured PageSpeed or conversion lift has been established. No payment or order was submitted. Amazon Pay was unavailable in earlier MAIN and preview checks and remains unresolved. Some localized presentation limits remain; the site is not certified perfect.

## Publication and rollback

The owner has explicitly authorized publication; no additional generic approval is required. The Shopify connector states that theme publishing is blocked for safety and that the owner must perform it in Shopify Admin. It also blocks MAIN file writes. No browser, CLI or alternate API workaround will be used.

After the collection repair passes and a fresh full-source check confirms the final binding, the exact owner step is [Shopify Admin → Online Store → Themes](https://admin.shopify.com/store/dresslikemommy-com/themes), publish **DLM UX Performance QA 2026-09-10 (137888792673)**, and keep **dresslikemommy/main (133290917985)** for rollback. Then verify the new MAIN identity, source, shopping paths and PageSpeed.

Continuation: “Finish the Couples display repair in the existing UX draft, verify the final complete theme and preserved settings, then give me the exact Shopify publication step.”
