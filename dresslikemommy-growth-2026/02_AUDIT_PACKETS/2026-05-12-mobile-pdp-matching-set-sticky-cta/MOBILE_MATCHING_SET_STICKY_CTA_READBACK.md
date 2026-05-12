# Mobile Matching-Set Sticky CTA Readback

Date: 2026-05-12 06:01-06:16 EDT

Scope:
- Local theme only.
- Product: `golden-daisy-mommy-and-me-set`.
- Mobile viewport: `390x844`.
- Local preview: `http://127.0.0.1:9292/products/golden-daisy-mommy-and-me-set?sticky_matching_set_readback=1`.

What changed:
- The matching-set builder now publishes selected-piece state for the sticky bar.
- On matching-set PDPs, the mobile sticky bar no longer behaves like a standalone single-variant add-to-cart.
- With no selected pieces, the sticky bar shows the matching-set context and keeps the button clickable so it can scroll the shopper to the builder.
- With selected pieces, the sticky bar mirrors the selected bundle: piece count, total, selected summary, and the real matching-set CTA label.

Verification commands:
- `node --check assets/product-desktop-ux.js`
- `git diff --check -- sections/main-product.liquid assets/product-desktop-ux.js assets/theme-inline-body-static-04.css ops/AGENT_COORDINATION.md`
- `shopify theme check --path . --fail-level error --output json`
- Isolated headless Chromium readback via global Playwright package with `NODE_PATH=/opt/homebrew/lib/node_modules`.

Readback result:

```json
{
  "initial": {
    "stickyVisible": true,
    "price": "Build your matching set",
    "detail": "",
    "button": "Choose options",
    "disabled": false,
    "state": {
      "template--17601278443617__main": {
        "sectionId": "template--17601278443617__main",
        "pieceCount": 0,
        "pieceCountLabel": "",
        "totalText": "",
        "summaryText": "",
        "isReady": false
      }
    }
  },
  "after": {
    "stickyVisible": true,
    "stickyClasses": "sticky-mobile-atc visible",
    "price": "2 Matching Pieces",
    "detail": "Total $52.98",
    "detailTitle": "Mother S, Girl 2 Years",
    "shippingHidden": true,
    "button": "Add matching pieces",
    "disabled": false,
    "bundleButtonDisabled": false,
    "bundleTotal": "Total $52.98",
    "bundleChips": "2 Matching Pieces",
    "state": {
      "template--17601278443617__main": {
        "sectionId": "template--17601278443617__main",
        "pieceCount": 2,
        "pieceCountLabel": "2 Matching Pieces",
        "totalText": "Total $52.98",
        "summaryText": "Mother S, Girl 2 Years",
        "isReady": true
      }
    }
  }
}
```

Click-forward readback:

```json
{
  "forwardedClicks": 1,
  "stickyText": "2 Matching Pieces TOTAL $52.98 ADD MATCHING PIECES"
}
```

Notes:
- The default Playwright/Chrome DevTools MCP browser profiles were locked, so verification used an isolated headless Chromium run from the installed global Playwright package.
- No live theme push/publish or Shopify Admin write was made.

## Live Deploy and Readback

Date: 2026-05-12 06:14-06:16 EDT

Deploy command:
- `shopify theme push --theme 133290917985 --only assets/product-desktop-ux.js --only sections/main-product.liquid --allow-live`

Deploy result:
- Shopify CLI reported: `The theme 'dresslikemommy/main' (#133290917985) was pushed successfully.`
- Only the two scoped theme files were included in the live push.

Live hard-refresh readback:
- URL: `https://www.dresslikemommy.com/products/golden-daisy-mommy-and-me-set?sticky_live_readback=1778580888656`
- Mobile viewport: `390x844`
- Fresh context headers: `Cache-Control: no-cache`, `Pragma: no-cache`
- Follow-up reload was executed before interaction.
- Evidence JSON: `live_mobile_matching_set_sticky_cta_readback.json`

Live asset readback:

```json
{
  "productUxScript": "https://www.dresslikemommy.com/cdn/shop/t/100/assets/product-desktop-ux.js?v=56127774210270559611778580822",
  "containsStickyStateEmitter": true
}
```

Live behavior readback:

```json
{
  "initial": {
    "stickyVisible": true,
    "price": "Build your matching set",
    "detail": "",
    "button": "Choose options",
    "disabled": false
  },
  "after": {
    "stickyVisible": true,
    "price": "2 Matching Pieces",
    "detail": "Total $52.98",
    "detailTitle": "Mother S, Girl 2 Years",
    "shippingHidden": true,
    "button": "Add matching pieces",
    "disabled": false,
    "bundleButtonDisabled": false,
    "bundleTotal": "Total $52.98",
    "bundleChips": "2 Matching Pieces"
  },
  "clickForward": {
    "forwardedClicks": 1,
    "stickyText": "2 Matching Pieces TOTAL $52.98 ADD MATCHING PIECES"
  },
  "passed": true
}
```

Live conclusion:
- `PASSED`: live mobile sticky CTA now reflects the selected matching pieces and forwards to the real matching-set add button.
