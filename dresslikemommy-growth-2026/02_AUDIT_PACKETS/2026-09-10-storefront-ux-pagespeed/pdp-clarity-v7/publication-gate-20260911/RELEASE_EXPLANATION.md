# Latest theme and preservation review

Updated September 11, 2026. Current source readback: 20:14:01 UTC.

The recommended release is **DLM UX Performance QA 2026-09-10 (137888792673)**, internal revision V7. Although its name contains September 10, its latest upload was September 11 at 17:40:34 UTC. The current six-theme Shopify inventory confirms it is the most recently updated uploaded theme. It remains **UNPUBLISHED**. The active theme is **dresslikemommy/main (133290917985)**.

The owner has now explicitly requested publication of the better theme while preserving important functionality. No further generic approval is needed. Publication execution is blocked by the Shopify connector's explicit restriction on theme publishing; no browser, CLI, alternate API, or MAIN file-write workaround is permitted.

The V8 localization proposal is separate local work. It has not been uploaded or tested in the storefront, so it is not this release.

## Why V7 is the recommended release

| Area | Concrete repair and buyer benefit |
| --- | --- |
| Product selection | The tested Together Heart 4XL/Green URL now initializes the custom size/color controls and permits adding the exact variant at USD 26.99. Previously the custom controls left Add disabled. |
| Cart | The mobile cart footer no longer covers item controls. Quantity changes refresh the heading count as well as the existing correct subtotal. |
| Filtering and search | Desktop filter clicks no longer open the product underneath. Predictive search guards against outdated responses replacing the current results. |
| Images and accessibility | Responsive image sizing and deferred hidden hero slides reduce unnecessary work. Hero controls, heading structure, contrast and overlays were repaired. A measured PageSpeed gain is not yet established. |
| Language and product information | Homepage links retain the selected language. Danish footer labels, Arabic child-option recognition, Japanese descriptions and product-page collection labels were repaired. The collection-label fix covers 105 templates across 35 locales. |
| Honest review presentation | Removed the automatic zero-review “New arrival” and unsupported “loved by moms” fallback. Genuine review widgets and positive review navigation remain. |

The candidate also retains the earlier combined draft's consent, Merchant landing and localization work. Those inherited changes are included in the full comparison; they were not all newly implemented or exhaustively re-audited in this UX task.

## What was preserved

Fresh full-source comparison confirms **all 527 uploaded files match the verified V7 candidate**. The complete difference from MAIN is 59 modified files plus 2 added consent assets, with **zero theme files deleted** and 466 files identical. Relative to the immediately preceding combined draft, V7 changes 19 files and preserves 508 exactly.

Against MAIN, both configuration files, all 20 templates, header/navigation files, and customer-account/login/order files are byte-identical by checksum and size. Buy-button, price and cart-footer files are also preserved. This retains the saved theme settings, template configuration and account surfaces.

Independent source inspection confirms that modified product and layout files retain Shopify app rendering hooks and the genuine positive-rating branches. Judge.me embed, badge and widget configuration remains. Consent changes expose Shopify's native preference controls without automatically setting consent. These are scoped preservation findings; they do not certify every third-party app or payment provider.

This UX work did not edit catalog product records, prices, variant availability, size-table source data or genuine reviews. Earlier rendered checks exercised actual desktop/mobile add-to-cart, quantity updates, fit-guide controls, menus, language navigation and standard checkout entry. No payment or order was submitted.

Source and existing review evidence: [current comparison](owner-release-2014-comparison.json), [complete V7 manifest](../../final-release-manifest.json), [audit and browser evidence](../../AUDIT.md), [V7 product-page receipt](../READBACK.md).

## Verification and remaining limits

- Current private source comparison: PASS, including unchanged MAIN, candidate and predecessor since 19:49.
- Existing V7 regression receipt: 51/51 pass. Full 527-file Shopify Theme Check: zero diagnostics. These retain their original execution dates; no code changed during this review.
- Public storefront requests remain stopped after HTTP 429. Fresh published buyer checks and a correctly bound desktop/mobile PageSpeed run are still required after actual access clearance.
- Standard checkout entry was tested earlier. Amazon Pay reported unavailable on both MAIN and preview; its cause and payment acceptance remain unresolved.
- Some localized guidance still needs work. V7 is an improvement supported by scoped tests, not a claim that every storefront feature or conversion outcome is perfect.

## Exact action and rollback

In [Shopify Admin → Online Store → Themes](https://admin.shopify.com/store/dresslikemommy-com/themes), under **Draft themes**, publish **DLM UX Performance QA 2026-09-10 (137888792673)**. Preserve **dresslikemommy/main (133290917985)** as the rollback theme. The connector can inspect the store and edit drafts, but explicitly blocks theme publishing and MAIN file writes. No publication was executed in this review.

After the owner publishes, verify the new MAIN identity and all source files privately. Resume buyer and PageSpeed checks only after the public HTTP 429 gate is actually cleared.

Continuation prompt: “I published DLM UX Performance QA 2026-09-10. Verify MAIN 137888792673 and its complete source, then continue the authorized buyer and PageSpeed checks after storefront access clears.”
