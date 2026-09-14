# Independent Merchant landing code verification

2026-09-09 — Confidence H for inspected local code; rendered Shopify behavior remains unverified. Reviewer did not build the candidate or perform any external write. Only this report is reviewer-owned.

## Verdict and binding

**PASS for the frozen revision 3 local code payload.** No unresolved code defect remains in the inspected scope. The prior revision 2 payload is superseded because its price-entity defect was reproduced independently. Its receipt must not authorize uploading revised files under the old hash. Policy review and rendered preview remain separate gates.

Complete payload SHA-256: `1ac332a2a99ce5ae66dc9f0485f476631457acd52b594b73134f086c433d8a6b`; revision 3, 40 files, 4,213,677 bytes. Independently recalculated receipt, embedded-content, changed-file-set and all 92 baseline/candidate manifest checks PASS.

Reviewed revision 3 active JS SHA-256: `360798ed8a6f859369ba4526bed0242e38fdf5f951a58f4aaf2d83a46a7c9cb7`. Exact delta SHA-256: `e45a3f41b0ba9d5f958bb59d876ed063c54668a40d588d42ade43823f473cc33`.

## Findings

The actual saved MAIN section loads `assets/product-desktop-ux-20260513-ruler-sync.js` at `sections/main-product.liquid:933`. All 92 baseline file hashes match recorded Shopify metadata; the JS separately matches `theme_staging_before.json` MD5 `61ded53111ee5002eb5c37b42a2c4b3f`. Candidate payload scope is 35 locale JSONs and five intended runtime/Liquid files; no alternate JS copies, footer, layout, tracking, catalog or root dirty-file changes enter the payload. Source MAIN is `133290917985`; intended target is unpublished preview `137881223265`. This is source binding, not a current rendered or upload readback.

`theme/snippets/product-desktop-ux.liquid:182` uses nullable `product.selected_variant.id`, avoiding implicit first-available selection. The runtime validates membership and initializes the exact role, size, every captured option axis, and quantity one only once (`theme/assets/product-desktop-ux-20260513-ruler-sync.js:3615`). Missing/invalid IDs preserve generic selection. Unavailable selections retain visible options and price but receive no purchasable instance ID; the independent cart-item availability guard blocks a synthetic click too. Later role, quantity and option changes retain their existing semantics without reseeding.

`theme/sections/main-product.liquid:1064` distinguishes explicit selected prices from generic ranges. Current variant amounts come from Shopify presentment formatting rather than a browser currency conversion. Matching-product compare-at promotions remain suppressed as intended; other product price rendering is preserved. `updateMatchingPrice` refreshes the headline and data attributes, unit-price reference, and incomplete-selection range; the observer restores a stale inner price replacement without a repeat-mutation loop.

**Resolved defect:** revision 2 rendered `22,00&nbsp;€` literally because `strip_html` does not decode entities. Revision 3’s detached decoder and text-only assignments (`JS:2839`) fix named/numeric entities while preserving literal text; prepared DOM cloning avoids reparsing decoded text. No image, script or emphasis node is created by the adversarial encoded-markup fixture. Final policy wording and translation meaning remain the separate standards reviewer’s responsibility.

## Checks and limits

Independently replayed **18/18** candidate tests and JS syntax: PASS. Additional reviewer probes passed reordered option records, a hidden single-value axis, and unit-reference formatting. A recorded 27-variant swimsuit matrix passed exact initial variant, price, quantity-one and synthetic cart payload checks. Initial cross-realm assertion failures were reviewer harness artifacts, corrected by comparing serialized payload values. The recorded availability/price fixture is not fresh inventory or checkout evidence.

Tests execute the real runtime and assert shopper-visible state/cart payloads, so they are stronger than matching source strings. However, the harness manually calls the builder, supplies synthetic price markup/data, stubs cart/network behavior and does not render Liquid, real CSS or Dawn section events. Its EUR/JPY cases verify formatting preservation, not exchange-rate truth. An initial multi-Type probe expected the wrong legacy global-picker behavior; source inspection confirms existing implicit per-card Type handling, so that expectation was discarded rather than labeled a candidate defect.

Root must still verify the frozen payload against the unpublished target and exercise desktop/mobile, EN/ES plus another locale, exact variant `41498026442849`, price/image/cart/currency parity, unavailable recovery and returns summary/modal/full policy. No production-readiness or publication verdict is implied.
