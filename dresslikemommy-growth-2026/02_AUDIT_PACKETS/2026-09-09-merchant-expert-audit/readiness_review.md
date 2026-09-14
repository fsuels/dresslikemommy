# Independent readiness review — 2026-09-09

Confidence: H for verified Shopify repairs; M for the broader readiness assessment because current Merchant receipts are missing. **PASS_WITH_GATES for completed Shopify remediation. Merchant account readiness remains UNVERIFIED.** This is not all-market approval, serving or profitability certification. The reviewer did not execute corrections, repeat the independently completed API scans, or use native account controls in this synthesis.

## Verified corrections

| Correction | Independent evidence | Result |
|---|---|---|
| Invalid identifiers | Complete post-scan: 4,945 variants, 240 ACTIVE parents, 24 checks, zero failures | Exactly 1,108 invalid values cleared across 70 products; 3,712 original empty and 125 populated checksum-passing values preserved |
| Description images | Ordered hosted assets plus private before/after body comparison | Six replacements in each of 21 source/locale bodies: 126 exact substitutions; other body bytes and translation fields preserved |
| Market catalogs | Fresh five-node Shopify readback at 18:14:25 UTC | Six parent joins true; each existing catalog now contains 240 active products, EXACT; both products' 48 variants and nine app publications each preserved |

The later [identifier verification](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/identifier_post_verification.md) supersedes the execution manifest's FULL_SCAN_PENDING label. Final identifiers are **4,820 null, zero malformed/checksum-failing, 125 manufacturer-unverified**. Two remaining barcode values occur across four variants; provenance is required before deciding which assignment, if any, to change. Missing identifiers do not establish that none were assigned.

[Market verification](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/market_post_verification.md) proves parent publication, not variant-level publication; the inspected connector lacks those variant fields. Image fidelity for four direct originals remains limited by blocked source comparisons; the independent image reviewer accepted ordered upload provenance and visible product consistency. The first expanded barcode receipt preserves description length rather than a persisted full-body equality result. The full identifier scan does not independently verify every non-barcode field across all 70 products.

## Country coverage is still a verification queue

The [country matrix](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/market_inventory.json) contains **65 unique active-market countries**, with 68 memberships because AU/CA/GB overlap markets. **36 match Google's Shopify-app support table; 29 are unlisted.** Neither count is a free-listing eligibility result. Unlisted does not mean unsupported in every Google program; listed does not prove destination selection, receipt, approval or serving. [Official Shopify integration table](https://support.google.com/merchants/answer/13693394)

Configured General shipping covers all 65 countries; 21 published locales and 20 presentment currencies exist. These are configuration facts, not delivery or checkout proof. The 237 shipping destinations enumerated by Shopify are not the active-market denominator. English covers the 36 table matches; optional local languages are opportunities. The integration's `pt-BR`/`pt` normalization is unverified. Currency conversion cannot replace matching submitted currency, landing price and checkout. [Language/currency requirements](https://support.google.com/merchants/answer/160637)

## Merchant evidence and remaining actions

Root reports the exact account **513542500** showed “Adding products to Google” around 18:26 UTC, without an offer count. Data Sources opened but its contents were not read before owner-focus interruption. Therefore current receipt/count/status is **UNKNOWN, not zero**. Source `10014302986`'s zero count is September 8 history only. Google-app feedback identifies App1780363, not the Merchant account; its pending/unclaimed and missing-attribute messages cannot be called current Merchant513 disapprovals.

1. **Read the selected account's current source and receipt details when owner focus is available.** Bind Merchant ID, domain claim, Shopify link, source owner/ID, latest update, received offers, feed label, language and target countries. Capture free-listing opt-in and source marketing methods. This distinguishes ingestion failure, processing, review and stale feedback without guessing.
2. Build the actual country/offer matrix: selected destination, source, received count, free-listing eligible/pending/disapproved counts and reason. Reconcile intended coverage against Shopify while allowing legitimate offer multiplication by country/language. Document exceptions for the 29 table-unlisted countries; do not silently create replacement feeds or remove markets.
3. Resolve current account-bound product issues. Verify age, gender, color, size and grouping against each actual offered piece, especially mixed adult/child families. Retained checksum-valid values remain uncertain; do not manufacture GTIN/MPN or blanket identifier flags. [Identifier requirements](https://support.google.com/merchants/answer/160161)
4. Complete localized exact-variant buyer paths and shipping/returns reconciliation. Compare sale unit, image, price, currency, availability and checkout delivery with received offers. General-rate configuration does not establish transit capability; swimwear and other return exclusions must remain accurate. Root owns the separate landing candidate and rendered verification.
5. After receipt/eligibility is established, verify price/availability automations, Store Quality and organic country/product reporting. Judge orders and retained profit using actual fulfillment, fees and returns, not traffic alone.

## Standards amendments and 2026 opportunities

The original checklist's “zero spend effect established” is overbroad: verify unchanged paid settings and exact scope while acknowledging possible indirect effects on connected consumers. Its NOT RUN correction-review status and the original catalog HOLD are superseded by today's receipts. Google Ads beta guidance must not be used as a universal free-listing eligibility classification.

Google manages the Shopify app's Merchant API migration; an old Content API label alone does not justify reinstalling or replacing the integration. Optional 2026 `variant_option`/`item_group_title` fields are relevant only after this integration exposes a supported mapping; that capability has not been verified. [Migration guidance](https://support.google.com/merchants/answer/13693394), [variant fields](https://support.google.com/merchants/answer/17085214) Prepare for the 500×500 image minimum enforced January 31, 2027; the six new 800×800 images satisfy that dimensional threshold, not a catalog-wide image audit. [Specification update](https://support.google.com/merchants/answer/16989427) Physical-store/local-inventory programs remain inapplicable.

**One next action:** obtain the current exact-account source/receipt readback. Existing nonspend correction authorization persists; owner-focus availability is an operational dependency, not a reason to repeat authorization. Continuation: “Read Merchant513 source receipt and build actual country-level free-listing eligibility from current account evidence.”
