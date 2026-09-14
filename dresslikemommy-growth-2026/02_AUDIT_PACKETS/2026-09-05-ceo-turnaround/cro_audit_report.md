# Storefront / CRO / technical SEO audit

Confidence: H for the named observations; M for their business impact. `DIAGNOSE / HANDOFF`, 2026-09-05 UTC. No theme or Shopify Admin changes.

## Scope and evidence

Chrome test tab `475224132`, browser ID `1` in this agent. Public DOM identifies theme `133290917985`, `dresslikemommy/main`, role `main`, Dawn `14.0.0`. A Shopify preview toolbar was visible; its existence alone was not treated as evidence of an alternate theme.

Rendered journey: homepage → Mommy & Me collection → Golden Daisy product → cart → hosted checkout; English/US/USD. Narrow homepage and Spanish homepage were also rendered. Requested viewport `390×844`; actual DOM viewport was `433×937`, so evidence is labeled narrow rather than an exact 390-pixel certification. Viewport reset; tab left at English homepage, US/USD, empty cart.

Public HTTP readback: **16 successful pages out of 17 attempts** plus robots, sitemap index and four default-language sitemap inventories. `/de` returned `429`; bulk requests stopped. This is a sample, not a full site or locale audit. Evidence: `cro_public_readback.json`, `cro_cart_after_quantity.txt`, `cro_spanish_dom.txt`, `cro_mobile_home.png`, `cro_spanish_mobile.png`.

One synthetic add-to-cart, one quantity increase, and one hosted-checkout opening occurred during approximately `22:35–22:43 UTC`; exact event timestamps were not captured. No customer data entered, payment submitted, or order placed. Only this audit's item was removed; `Cart 0 items` and `Your cart is empty` verified. Analytics should exclude this known QA activity from decisions.

## Keep

- Clear relationship/occasion navigation and a usable collection-to-product route. The first Mommy & Me page visibly contained 36 products, including dresses, family tops, separates, pajamas and swimwear.
- Golden Daisy clearly explains top and pants are separate, asks who the piece is for, shows size measurements with cm/in choices, and shows a precise selected-piece total. Mother S Top added at **$26.99**; quantity two produced **$53.98** line, subtotal, and hosted-checkout total. This disproves a blanket claim that checkout is broken.
- Standard shipping inclusion is visible near purchase controls. Shipping/returns pages are accessible and describe processing, return costs, exclusions and possible international import charges. Their operational accuracy still needs owner evidence.
- All 16 successful HTTP samples returned `200`, self-canonicals, and zero matches for the source-domain/URL-brand patterns tested. Former dirty dress/swim collection routes currently passed that limited source scan.
- Sitemap index has 85 children covering English plus 20 other language prefixes. Default inventories contain 239 product-sitemap URLs **including the homepage**, 45 collection URLs, 17 page URLs and 68 blog URLs **including the blog index**. Three sampled PDPs expose parseable Product/Offer, shipping and return-policy objects. This is a useful base; do not rebuild SEO infrastructure blindly.

## Fix first

| Priority | Verified finding | Smallest next change |
|---|---|---|
| P1 | Homepage rotating pajama caption visibly includes “The vendor calls this a 四层纱布…”. Same issue already tracked as `PROB-2026-06-22-HOMEPAGE-SPOTLIGHT-VENDOR-CAPTION`. | Use the existing local caption guard in `snippets/home-spotlight-card.liquid:79`; do not recreate it. Review underlying PDP customer copy separately. |
| P1 | Spanish/French cookie-free homepage HTML retains claims about thousands of happy families and trust since 2016, unlike current English trust copy. Both mix in English CTA/trust/caption sentences. Spanish uses `Comprar Juegos Familiares`/`Ver todos los juegos familiares`, ambiguous game-oriented wording for clothing sets. | Product-owned/theme translation inventory and native-language review of these exact strings. Retain numerical/history claims only with owner evidence. Do not assume translated-page existence means market readiness. |
| P2 | Cart quantity increases update line/subtotal correctly, but heading remains `Your cart (1)` with two items; reloading changes it to `(2)`. | Existing local fix already covers exact section targets in `assets/cart.js:109`, `sections/main-cart-items.liquid:30`, and `sections/main-cart-footer.liquid:93`. June tracker should be narrowed to the count defect; stale subtotal was not reproduced. |
| P2 | Narrow homepage hero H1 is `display:none` and absent from the accessible heading tree. CTAs remain visible. | Existing local accessible-heading correction in `sections/hero-banner.liquid:363`; do not claim it visually restores the headline. |
| P2 | Amazon Pay is prominently rendered while its accessible label says it is currently unavailable. | Verify payment-provider configuration with owner; do not test payment or change billing. Avoid promising unavailable methods. |
| P2 | `/es` and `/fr` retain the English homepage SEO title. Homepage outputs two hreflang sets (44 tags), with Portuguese represented as `pt-br` and `pt` for the same path. Meow Star PDP title still says “Cat Meadow”. | Audit exact translated SEO records and template-generated versus Shopify-generated hreflang. Deduplicate only after confirming current source ownership; no demonstrated indexing penalty claimed. |

Spanish footer headings now render human labels. Do not blindly repeat the June footer fix.

## Reviewable release package

`cro_existing_theme_fixes.patch` contains the **existing** five-file local diff, inspected here; no theme source was edited. `cro_existing_patch_manifest.json` records file SHA256 values and patch SHA256 `b9876c88e6a6bd2d2fdbe5a491a9a2629a0c230e873e29266ca33e69dd04514e`.

Safe release path: obtain a fresh snapshot of live theme `133290917985`; transplant only these hunks into an isolated copy; run theme/JS checks; create an approval-scoped unpublished preview; independently verify desktop/narrow captions, heading, quantity 1→2→1, totals and checkout entry; then obtain exact live-release authorization and retain the live baseline for rollback. **These local hashes do not authorize or validate a whole-theme deployment.** The working tree contains unrelated changes.

## Organic and paid decision

Prioritize existing collection/PDP demand from GSC and conversion data. Useful organic content should answer real sizing, piece-count and destination-specific delivery questions with product links. Do not generate more generic pages simply because 20 languages exist. Google describes hreflang as a localization signal and product markup as eligibility for richer product information, not a ranking or revenue guarantee: [localized pages](https://developers.google.com/search/docs/specialty/international/localized-versions), [merchant listings](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing).

No new traffic recommendation is cleared by this sample. Missing gates include actual landed costs and return losses by market, delivery-time distribution, mobile PDP/cart checkout verification, exact sale/compare-at history, real photo-to-product match, native-language PDP completeness, full country/currency matrix, and Core Web Vitals. Cheap CPC cannot compensate for misleading or unprofitable fulfillment promises.

Owner facts needed: (1) actual typical and slow-end delivery by destination, (2) return destination/cost and refund treatment when shipping is included, (3) evidence for numerical trust claims and sale reference prices.

Checks run: script syntax compilation, JSON parse/readback, five-file diff inspection, scoped `git diff --check` all passed. Initial title extractor inadvertently included SVG payment-icon titles; saved evidence documents a deterministic removal of that exact suffix, and the script now restricts titles to `<head>`. No broad refetch after `429`. Theme checks and post-deploy tests were not run because no theme implementation/deployment occurred.

Single next action: **prepare and verify the isolated five-file preview**, because it converts already-written fixes into shopper evidence without rebuilding them. Root owns canonical problem/worklog/cockpit integration. Continue through `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, referencing this packet and current root anchor.
