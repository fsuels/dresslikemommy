# Independent Merchant Center standards review

Date: 2026-09-09. Confidence: H for official requirements; current account compliance requires root's live evidence. Scope: read-only standards research for Merchant 513542500 and the Shopify Google & YouTube integration. No native account access or external writes by this reviewer. Root owns implementation and canonical continuity.

## Required foundation

**Coverage means received and eligible offers in every served, supported destination.** An enabled market, connected account, or free-listing switch does not demonstrate coverage or guarantee impressions. Confirm the existing account's free-listing permission and each source's marketing methods. Shopify-created accounts usually opt in automatically; accounts created elsewhere require verification. [Google's Shopify free-listing guide](https://support.google.com/merchants/answer/13692890)

**Reconcile country, language, currency and source.** Shopify sync needs enabled Markets and General shipping rates for selected countries. Overlapping Markets can become standalone country-code sources, increasing offer counts; old source rules do not transfer, and existing campaign filters may be affected. Inspect automatic sync, country selection, future-country selection and source ownership before changes. [Current Shopify sync guide](https://support.google.com/merchants/answer/13693394)

Supported feed languages can reach speakers in supported countries; local language is an opportunity, not a universal requirement. Feed, product page and purchase navigation must agree on language. A supported foreign currency can use Google's conversion, but the submitted currency must remain on the landing page and checkout. South Korea requires a business registration number; France excludes overseas territories. [Language/currency requirements](https://support.google.com/merchants/answer/160637)

**Shipping must represent checkout.** Only Shopify's General profile automatically syncs reliably; custom profiles and third-party rates require explicit reconciliation. API imports can overwrite manual Merchant edits. Costs must match checkout, or be conservatively overstated when exact matching is impossible. [Shopify shipping integration](https://support.google.com/merchants/answer/14232591) Cover every target country with delivery estimates and shipping in the offer's currency. Country targeting and shipping configuration are separate checks. [Multi-country setup](https://support.google.com/merchants/answer/15404838)

**Apparel fields belong to each actual variant.** Free listings require `age_group`, `gender`, `color`, and clothing/shoe `size`. Age values: `newborn`, `infant`, `toddler`, `kids`, `adult`; gender: `male`, `female`, `unisex`. Adult applies to teen/adult sizing and is unrelated to explicit-content classification. Do not apply one adult or female value across mixed family variants. Sizes must contain the size, with role/demographic information separately represented. [Age](https://support.google.com/merchants/answer/6324463), [gender](https://support.google.com/merchants/answer/6324479), [color](https://support.google.com/merchants/answer/6324487), [size](https://support.google.com/merchants/answer/6324492)

Keep distinct offer IDs and stable shared `item_group_id` for true variants. [Grouping](https://support.google.com/merchants/answer/6324507) Match the received offer's selected piece, price, availability and image to its landing page and checkout; test exact variant URLs and localized desktop/mobile paths. [Landing requirements](https://support.google.com/merchants/answer/4752265) Use only verified identifiers: internal SKUs are not substitutes for manufacturer-assigned GTIN/MPN; missing knowledge does not establish that identifiers do not exist. [Identifiers](https://support.google.com/merchants/answer/160161)

Return window, method, fees and exceptions must agree across Merchant and the accessible website. Do not invent free returns or broaden the business policy to gain annotations. [Return policy requirements](https://support.google.com/merchants/answer/14011730)

## Useful improvements after ingestion works

- Keep price, availability and condition automations enabled when page/structured data are accurate. They correct temporary mismatches, not broken bulk sync. Automatic shipping updates are a separate US-only feature requiring suitable crawl/tracking evidence. [Product automations](https://support.google.com/merchants/answer/12157888), [shipping updates](https://support.google.com/merchants/answer/16371720)
- Add accurate `variant_option` and `item_group_title` where the integration supports them; these 2026 optional fields supplement required apparel attributes. Each group needs consistent option names and unique value combinations. [Variant options](https://support.google.com/merchants/answer/17085214)
- Improve specific product titles, complete descriptions, relevant product types and truthful high-quality images. Plan images at least 500×500 for January 31, 2027 enforcement; 1500×1500 or larger is recommended. [2026 specification update](https://support.google.com/merchants/answer/16989427), [image guidance](https://support.google.com/merchants/answer/6324350)
- Inspect Store Quality's shipping, returns, browsing and purchase signals. Enrollment follows approved products; the badge is conditional and currently offered in AU/CA/GB/IN/JP/NZ/US, not a setting guaranteeing excellence. [Store Quality](https://support.google.com/merchants/answer/14261098)
- Evaluate Organic traffic by country/product, then verified purchases, revenue and actual fulfillment/return costs. Traffic alone does not establish profit. [Merchant reports](https://support.google.com/merchants/answer/14152817)

## 2026 and interpretation cautions

Content API sunset was August 18, 2026; unextended custom integrations face intermittent HTTP 410 failures from September 1. Platform partners manage their own migration. [Current API notice](https://developers.google.com/shopping-content/guides/deprecation-and-sunset) Google explicitly handles Shopify app migration; reinstalling is unnecessary, product IDs remain unchanged, and a lingering Content API source label is expected. [Shopify sync migration FAQ](https://support.google.com/merchants/answer/13693394)

Google's country tables differ in breadth: Shopify sync availability is broader than its free-listing table; beta participation may be restricted. Establish actual per-country eligibility rather than infer universal availability. [Beta conditions](https://support.google.com/google-ads/answer/7101265) Ordinary processing may take 15 minutes; initial free-listing review can take weeks. Record submission, processing and review separately. [Visibility/status](https://support.google.com/merchants/answer/12488713)

Local inventory, store pickup and physical-store programs are inapplicable to this dropshipping business. [Local requirements](https://support.google.com/merchants/answer/3271956) Paid launches, automated discounts, new promotions and changed delivery promises require separate effects review; they are not prerequisites for free-listing eligibility.

## Independent verification checklist

- [ ] Exact Merchant/account/domain and Shopify channel binding freshly matched.
- [ ] Before-state, intended correction, affected countries/offers and rollback captured.
- [ ] Received source IDs, offer counts and update timestamps reconciled to Shopify.
- [ ] Existing Ads implications reviewed before country/source expansion; zero spend effect established.
- [ ] Country × language × currency × shipping × offer eligibility matrix complete, with explicit exceptions.
- [ ] Free-listing account permission, source method, visibility and item exclusions checked.
- [ ] Mixed adult/child/male/female variants verified individually; identifiers and grouping correct.
- [ ] Exact offer URL, selected piece, price, currency, language, availability and checkout agree.
- [ ] Shipping/returns match published policy and checkout; no invented promises.
- [ ] Native after-state readback proves correction; pending processing/review remains clearly pending.
- [ ] Organic country/product baseline captured; profit remains unverified without actual costs.

Independent correction review: NOT RUN. Awaiting root's bounded before/after evidence and proposed or completed corrections.

## Dated superseding review — 2026-09-09

The [readiness review](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/readiness_review.md) records completed independent identifier, image and catalog verification; the historical NOT RUN status above is superseded. Its current verdict is PASS_WITH_GATES for Shopify remediation, with Merchant readiness unverified. The earlier zero-spend-effect checkbox is replaced by an exact paid-setting/scope check with indirect effects left explicit. Shopify app-table matches and Google Ads beta guidance do not establish actual country free-listing eligibility. Current Merchant offer count is unknown; the historical source-zero observation must not be presented as today's receipt.
