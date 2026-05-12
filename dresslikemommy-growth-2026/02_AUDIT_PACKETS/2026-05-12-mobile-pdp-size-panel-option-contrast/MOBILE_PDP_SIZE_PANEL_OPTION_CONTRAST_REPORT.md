# Mobile PDP Size Panel + Option Contrast

Date: 2026-05-12

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-mobile-pdp-size-panel-option-contrast`

## Scope

- Local theme/front-end repair only.
- Files changed: `assets/product-desktop-ux.js`, `assets/component-product-desktop-ux.css`, `sections/main-product.liquid`.
- No live theme push/publish, Shopify Admin write, checkout edit, ads/feed/analytics write, payment/order action, or credential/account/billing edit.

## What Changed

- Mobile selected-size measurements now render as an inline panel inside the matching-set card instead of a fixed floating tooltip.
- The old pinned floating tooltip is hidden on mobile so it cannot cover Type, Color, or Quantity controls.
- A meaningful vertical scroll on mobile closes any open selected-size panel the same way the panel X close does.
- Quantity/add/remove/add-role interactions close open size panels once the shopper moves past sizing.
- Selected per-card Type/axis buttons keep white text in hover/focus/active selected states.
- Selected global pill options inside the PDP reference UI keep dark readable text on a white selected pill.

## Verification

- `node --check assets/product-desktop-ux.js` passed.
- `git diff --check` passed.
- `shopify theme check --path . --fail-level error --output json` returned `[]`.
- Isolated mobile Chrome/CDP browser readback used viewport `390x844` on public Golden Daisy PDP with local patched JS/CSS injected, without pushing the theme live.

Browser readback highlights from `mobile_size_panel_browser_readback.json`:

- Matching-set builder visible: `true`; card count: `2`.
- After `Size=S` and `Type=Top`, inline size panel visible: `true`.
- Old floating pinned tooltip display: `none`.
- Panel overlap with Type axis button: `false`.
- Panel overlap with Quantity button: `false`.
- Selected Type button computed text color: `rgb(255, 255, 255)`.
- Selected Type button computed background: `rgb(29, 134, 86)`.
- After mobile scroll: inline panel count `0`, visible panel count `0`, pinned tooltip count `0`.
- Quantity `+` remained clickable and incremented value to `2`.
- Global checked pill computed text color: `rgb(21, 26, 32)`, background `rgb(255, 255, 255)`, border `rgb(26, 26, 26)`.

Screenshots:

- `mobile-inline-size-panel-after-type.png`
- `mobile-size-panel-after-size.png`

## Residual Risk

- The live theme was not pushed in this session. Deployment/sync and live post-deploy mobile QA remain separate.
- Golden Daisy needs Type after Size before a measurement row is available, so the inline panel appears after Size + Type on that PDP. Products whose chart maps directly from Size may show the panel immediately after Size.
