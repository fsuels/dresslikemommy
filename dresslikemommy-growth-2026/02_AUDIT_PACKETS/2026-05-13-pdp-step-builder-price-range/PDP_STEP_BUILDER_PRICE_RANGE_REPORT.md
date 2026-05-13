# PDP step-builder, price-range, and Lavender cache report

Date: 2026-05-13 06:40 EDT

## Scope

- Theme files:
  - `snippets/price.liquid`
  - `sections/main-product.liquid`
  - `assets/product-desktop-ux.js`
  - `assets/product-desktop-ux-20260513.js`
  - `assets/component-product-desktop-ux.css`
- Live theme: `dresslikemommy/main` `#133290917985`.
- Exact product reported by owner:
  - `https://www.dresslikemommy.com/products/lavender-plaid-family-matching-set-tank-dress-shirt-2?variant=44104772943969`
  - Product `gid://shopify/Product/7542447079521`
  - Variant `gid://shopify/ProductVariant/44104772943969`

## What changed

- Matching-set PDP headline prices now render a product price range instead of one selected/first variant price.
- Matching-set PDPs now open with one adult role selected by default, preferring Mother, so the size/options card is visible immediately.
- Switching role buttons, for example Mother to Father, dynamically swaps the visible size/options card without hiding the options step.
- Lavender-style standalone size labels such as `2 Years` now fall back to SKU role inference, so role groups can be built even when the size option does not include `Boy`, `Girl`, `Mother`, or `Father`.
- Redundant builder prices were removed from:
  - role buttons
  - card headers
  - selected-size confirmation line
  - quantity row
- The only builder price after a completed choice is the final ready-to-add chip, for example `Mother - M - $34.99`.
- A fresh asset name, `product-desktop-ux-20260513.js`, was added and referenced by `sections/main-product.liquid` so fresh product renders do not reuse stale cached JS.
- CSS includes a defensive hide rule for old price classes if an intermediate render contains old markup.

## Live Admin/cache cleanup attempts

These were narrow, reversible cache-bust attempts for the exact Lavender product. Final readback confirms the product remains active and unchanged in title, handle, publication, template, SKU, and price.

- Product metafield `ops.pdp_cache_bust_20260513` was set and deleted.
- Variant metafield `ops.pdp_cache_bust_20260513` was set and deleted.
- Variant price was resubmitted as the same value, `24.99`; no user errors; SKU and price unchanged.
- Product template suffix was temporarily set to two identical product templates during cache tests, then reverted to `null`.
- Temporary cache-bust templates were deleted from the live theme and local repo.

Final Admin readback:

- Product title: `Lavender Plaid Family Matching Set — Tank Dress & Shirt`
- Product handle: `lavender-plaid-family-matching-set-tank-dress-shirt-2`
- Product status: `ACTIVE`
- Product `templateSuffix`: `null`
- Product URL: `https://www.dresslikemommy.com/products/lavender-plaid-family-matching-set-tank-dress-shirt-2`
- Variant SKU: `DLM-LVP-BOY-KID2Y-LAVENDER`
- Variant price: `24.99`

## Verification

Commands:

```text
node --check assets/product-desktop-ux.js
node --check assets/product-desktop-ux-20260513.js
git diff --check -- snippets/price.liquid sections/main-product.liquid assets/product-desktop-ux.js assets/product-desktop-ux-20260513.js assets/component-product-desktop-ux.css
shopify theme check --path . --fail-level error --output json
shopify theme push --store dresslikemommy-com.myshopify.com --theme 133290917985 --only snippets/price.liquid --only sections/main-product.liquid --only assets/product-desktop-ux.js --only assets/product-desktop-ux-20260513.js --only assets/component-product-desktop-ux.css --allow-live
shopify theme pull --store dresslikemommy-com.myshopify.com --theme 133290917985 --only sections/main-product.liquid --only assets/product-desktop-ux-20260513.js --only assets/component-product-desktop-ux.css --path /tmp/dlm-live-theme-check --force
shopify theme push --store dresslikemommy-com.myshopify.com --theme 133290917985 --only assets/product-desktop-ux.js --only assets/product-desktop-ux-20260513.js --allow-live
shopify theme pull --store dresslikemommy-com.myshopify.com --theme 133290917985 --only assets/product-desktop-ux-20260513.js --path /tmp/dlm-live-theme-check-20260513-default-role --force
```

Results:

- Both `node --check` runs passed.
- Theme Check returned `[]`.
- Live source pull confirmed `sections/main-product.liquid` references `product-desktop-ux-20260513.js`.
- Live source pull confirmed `product-desktop-ux-20260513.js` contains `inferBaseRoleKeyFromStandaloneSize`.
- Live source pull confirmed `product-desktop-ux-20260513.js` contains `getDefaultGroupForBootstrap` and the immediate-size hint copy.
- Public fresh asset `product-desktop-ux-20260513.js` contains the Lavender SKU/standalone-size fallback and does not contain the removed role/card price render terms.
- Public fresh asset `component-product-desktop-ux.css` contains the defensive price-class hide rule.

Fresh public render readbacks:

- Other Lavender variants, including `44104772845665`, serve:
  - `assets/product-desktop-ux-20260513.js?v=6227657029263901151778668902`
  - `assets/component-product-desktop-ux.css?v=100697688843046080961778667523`
- The same exact Lavender variant with `&view=ajax` serves the fresh assets above.
- Browser readback on the owner-reported exact URL loaded `product-desktop-ux-20260513.js?v=6227657029263901151778668902`, selected Mother by default, rendered one visible size/options card with Mother sizes, and showed the disabled CTA as `Choose a size for Mother`.
- Clicking Father switched the selected role to Father, kept the size/options card visible, showed Father sizes, and changed the disabled CTA to `Choose a size for Father`.
- Selecting Father size `M` enabled the CTA and showed one builder price only in the final ready chip, `Father - M - £22.00`; redundant role/card/selection/quantity price nodes remained absent.
- Earlier public Golden Daisy/Picnic Plaid browser readbacks passed for the focused one-role flow, range price, one active card after role selection, and hidden totals.

## Exact URL cache state

As of 2026-05-13 06:45 EDT, browser-equivalent public reads of the owner-reported exact URL serve the fresh assets:

```text
https://www.dresslikemommy.com/products/lavender-plaid-family-matching-set-tank-dress-shirt-2?variant=44104772943969&country=US
assets/product-desktop-ux-20260513.js?v=6227657029263901151778668902
assets/component-product-desktop-ux.css?v=100697688843046080961778667523
```

Playwright with cookies cleared also passed the US/browser path: `localization=US`, `cart_currency=USD`, fresh `product-desktop-ux-20260513.js`, Mother selected, and one visible card. Plain `curl` with its default `Accept: */*` can still hit an older Shopify page-cache variant that references the old asset query, but browser/customer-style requests read the fresh page.

## Residual risks

- A non-browser `curl` cache variant still returns the old asset query for the exact URL; the customer-browser readback is fresh and functional, but the curl-only edge variant should be rechecked before deleting this tracker note.
- Old immutable CDN asset versions still carry the pre-fix repeated-price builder render terms; final proof should use browser-equivalent page reads that load `product-desktop-ux-20260513.js`.
- No live cart add was clicked during this pass; the existing AJAX cart add path was left intact.

## Next action

- Recheck the exact URL with both browser-equivalent `Accept` headers and plain curl after the Shopify page-cache window.
- Close the tracker only when the plain curl edge variant also serves `product-desktop-ux-20260513.js`, or document that Shopify keeps a harmless `Accept: */*` cache variant while customer-browser reads remain fresh.
