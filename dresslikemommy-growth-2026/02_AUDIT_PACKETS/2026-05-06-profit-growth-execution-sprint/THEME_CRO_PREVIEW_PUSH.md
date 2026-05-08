# Theme CRO Preview Push - 2026-05-06

## Scope Approved

Owner approval phrase:

`APPROVE THEME CRO PUSH ONLY: PUSH THE LOCAL CRO/SHIPPING-CLARITY/COLLECTION-SEO CHANGES TO A THEME PREVIEW FIRST; DO NOT PUBLISH LIVE UNTIL I REVIEW THE PREVIEW; NO SHOPIFY PRODUCT, FEED, ADS, PIXEL, OR CAMPAIGN CHANGES.`

## Result

- Created unpublished Shopify preview theme: `DLM CRO Preview 2026-05-06`
- Theme ID: `134923321441`
- Role: `unpublished`
- Preview URL: `https://dresslikemommy-com.myshopify.com?preview_theme_id=134923321441`
- Theme editor URL: `https://dresslikemommy-com.myshopify.com/admin/themes/134923321441/editor`
- Live theme remains: `133290917985 | dresslikemommy/main | live`

## Method

To avoid uploading unrelated dirty local theme work, I:

1. Pulled the current live theme into a temporary staging directory.
2. Copied only the approved CRO/shipping-clarity/collection-SEO files into that staging directory.
3. Ran theme validation on the staged theme.
4. Pushed the staged theme as a new unpublished preview theme.
5. Pulled the preview theme back from Shopify and compared the approved files byte-for-byte against the local files.

## Files Included In Preview

- `assets/section-main-product.css`
- `locales/da.json`
- `locales/de.json`
- `locales/en.default.json`
- `locales/es.json`
- `locales/fr.json`
- `sections/category-icons.liquid`
- `sections/hero-banner.liquid`
- `sections/home-conversion-hero.liquid`
- `sections/main-product.liquid`
- `snippets/buy-buttons.liquid`
- `snippets/collection-merchandising-callout.liquid`
- `snippets/collection-seo-content.liquid`
- `snippets/collection-seo-fallback.liquid`
- `snippets/home-category-card-caption.liquid`
- `snippets/home-category-localized-copy.liquid`
- `snippets/home-spotlight-card.liquid`
- `snippets/product-faq-schema.liquid`
- `snippets/product-page-copy-map.liquid`
- `templates/index.json`

## Verification

- `shopify theme check --path "$tmpdir"` passed: `252 files inspected with no offenses found`.
- `shopify theme push --unpublished --theme "DLM CRO Preview 2026-05-06" --path "$tmpdir" --json` succeeded.
- `shopify theme list --json` confirmed:
  - `133290917985 | dresslikemommy/main | live`
  - `134923321441 | DLM CRO Preview 2026-05-06 | unpublished`
- Remote pullback comparison passed for all `20` approved files.
- Preview PDP readback for `/products/red-resort-mommy-and-me-set?preview_theme_id=134923321441` found:
  - `Build your matching set`
  - `Optional: choose one size for each family member you want to include. Each selection adds one separate piece to cart.`
  - `Shipping options shown at checkout`
- Preview homepage readback confirmed the preview renders and includes the updated paid-facing hero/category copy.

## Guardrails Preserved

- No live theme publish.
- No Shopify product edits.
- No feed, Merchant Center, Google Ads, Pinterest Ads, pixel, campaign, budget, bid, product-scope, product-group, feed-label, or conversion-goal changes.

## Next Approval Gate

If the preview is approved after owner review, the publish step should require a fresh exact approval phrase, for example:

`APPROVE PUBLISH THEME CRO PREVIEW 134923321441 LIVE; NO SHOPIFY PRODUCT, FEED, ADS, PIXEL, CAMPAIGN, BUDGET, BID, PRODUCT SCOPE, OR CONVERSION-GOAL CHANGES.`
