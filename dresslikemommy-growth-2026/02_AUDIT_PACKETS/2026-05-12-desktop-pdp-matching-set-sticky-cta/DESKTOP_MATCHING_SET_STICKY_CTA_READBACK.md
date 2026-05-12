# Desktop Matching-Set Sticky CTA Readback

Date: 2026-05-12 06:24-06:30 EDT

Scope:
- Live theme `dresslikemommy/main` `#133290917985`.
- Product: `picnic-plaid-family-matching-set`.
- Public URL: `https://www.dresslikemommy.com/products/picnic-plaid-family-matching-set`.
- Desktop viewport: `1280x720`.

Issue:
- Desktop sticky ATC was still tied to the hidden standalone product form and showed a single-product price plus `ADD TO CART`.
- On matching-set PDPs, the sticky CTA needs to be the out-of-view continuation of the green matching-set CTA, with the already selected pieces and total.

Fix:
- `assets/product-desktop-ux.js`
  - Desktop sticky now detects matching-set PDPs.
  - It observes the real `[data-matching-set-add-button]`, not the hidden standalone submit button.
  - It consumes `DLMMatchingSetStickyState` / `dlm:matching-set-summary`.
  - It scrolls back to the matching-set builder if no pieces are selected.
  - It forwards ready clicks to the real matching-set add button.
- `assets/component-product-desktop-ux.css`
  - Matching-set desktop sticky uses the green CTA styling.

Validation commands:
- `node --check assets/product-desktop-ux.js`
- `git diff --check -- assets/product-desktop-ux.js assets/component-product-desktop-ux.css ops/AGENT_COORDINATION.md`
- `shopify theme check --path . --fail-level error --output json`
- `shopify theme push --theme 133290917985 --only assets/product-desktop-ux.js --only assets/component-product-desktop-ux.css --allow-live`

Live asset readback:

```json
{
  "productUxScript": "https://www.dresslikemommy.com/cdn/shop/t/100/assets/product-desktop-ux.js?v=84777925448218368241778581590",
  "desktopUxCss": "https://www.dresslikemommy.com/cdn/shop/t/100/assets/component-product-desktop-ux.css?v=136782400840342921741778581590",
  "jsHasDesktopMatchingSet": true,
  "cssHasDesktopMatchingSet": true
}
```

Live behavior readback:

```json
{
  "visibleCheck": {
    "ctaInViewport": true,
    "stickyVisible": false,
    "stickyText": "2 Matching Pieces Total $60.98 ADD MATCHING PIECES",
    "stickyClasses": "sticky-desktop-atc sticky-desktop-atc--matching-set"
  },
  "outOfViewCheck": {
    "ctaInViewport": false,
    "stickyVisible": true,
    "stickyText": "2 Matching Pieces Total $60.98 ADD MATCHING PIECES",
    "stickyClasses": "sticky-desktop-atc sticky-desktop-atc--matching-set is-visible",
    "buttonBg": "rgb(29, 134, 86)"
  },
  "passed": true
}
```

Evidence files:
- `live_desktop_picnic_sticky_cta_readback.json`
- `live_desktop_picnic_sticky_cta_visibility_readback.json`
- `live_desktop_picnic_cart_drawer_after_fix_readback.json`
- `live_desktop_picnic_sticky_cart_drawer_after_fix_retry_readback.json`
- `live_desktop_picnic_sticky_drawer_after_fix_attempt_2.png`

Conclusion:
- `PASSED`: On the live Picnic Plaid PDP, desktop sticky now hides while the green matching-set CTA is visible and appears only after that CTA scrolls out of view, mirroring the selected matching pieces and total with green CTA styling.

## Cart Drawer Follow-Up

Date: 2026-05-12 06:38-06:43 EDT

Owner follow-up:
- Sticky CTA click opened the cart drawer in an ugly state: the page looked mostly gray, the drawer top was blank, and checkout/upsells appeared before the cart title and line items.
- The regular green matching-set button opened the drawer correctly with `Your cart` and line items visible at the top.

Root cause:
- The matching-set AJAX add path called `cartDrawer.renderContents(parsed)` directly.
- Unlike the standard `product-form` add path, it did not remove stale `is-empty` from the outer `<cart-drawer>` after adding from an empty cart.
- The stale `is-empty` class triggered drawer CSS that hid the header and item rows, making the footer appear first.

Fix:
- `assets/cart-drawer.js`
  - `renderContents` now removes stale `is-empty` from the outer cart drawer before opening.
  - It resets `.drawer__inner` and `cart-drawer-items` scroll positions to top before calling `open()`.
- Pushed only `assets/cart-drawer.js` to live theme `dresslikemommy/main` `#133290917985`.

Validation commands:
- `node --check assets/cart-drawer.js`
- `git diff --check -- assets/cart-drawer.js assets/product-desktop-ux.js assets/component-product-desktop-ux.css`
- `shopify theme check --path . --fail-level error --output json`
- `shopify theme push --theme 133290917985 --only assets/cart-drawer.js --allow-live`

Live drawer readback:

```json
{
  "sticky": {
    "before": {
      "stickyText": "2 Matching Pieces Total $60.98 ADD MATCHING PIECES",
      "cartDrawerAsset": "https://www.dresslikemommy.com/cdn/shop/t/100/assets/cart-drawer.js?v=138855533694470059091778582391",
      "hasResetFunction": true
    },
    "after": {
      "drawerClass": "drawer animate active",
      "title": "Your cart (2)",
      "innerScrollTop": 0,
      "itemsScrollTop": 0,
      "headerRect": { "height": 71 },
      "firstItemRect": { "height": 204 },
      "visibleStart": "Your cart (2) PRODUCT IMAGE PRODUCT TOTAL QUANTITY Picnic Plaid Family Matching Set - Dress & Shirt..."
    }
  }
}
```

Conclusion:
- `PASSED`: Sticky click now opens the live cart drawer in the same top-of-cart state as the regular green matching-set button.
