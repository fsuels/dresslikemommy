# Cart drawer copy trim — 2026-09-27

Owner request (Claude Code chat, session "Conversion improvements"): move "You may also like" out of the fixed drawer footer, remove "64 countries enabled" and the duplicate "Estimated delivery after address entry" line, release via `main` and verify on iPhone and Android sizes. The drawer claim owner (CEO overnight sprint, session "Website sales improvement") handed off this exact scope in chat.

## Findings at start (LIVE, 2026-09-27 ~13:55 UTC)
- "You may also like" was already out of the fixed footer (commits `d8a472e`/`1c95318` by the claim owner). Nothing left to move.
- "Estimated delivery after address entry": the drawer copy was already hidden by `assets/cart.js`. The `/cart` copy was still visible, because `.cart-page__delivery-estimate { display:flex }` overrode `[hidden]`.
- "64 countries enabled" showed in the "Ships to <country>" box in the drawer and on `/cart`.

## Change — commit `089a1da`
- `snippets/shipping-country-checker-trigger.liquid`: the cart context renders no count line. Other contexts are unchanged.
- `snippets/cart-drawer.liquid`: the hidden delivery-reassurance block is removed. The wallet block and `#CartDrawer-Footer` are untouched.
- `sections/main-cart-footer.liquid`: the `/cart` delivery-estimate block is removed. The dated estimate above the total stays.

## Release
- Before-state: 3/3 live files equalled `089a1da^` (MD5).
- The GitHub→Shopify sync dropped the push; after 6 minutes, 0/3 files were live. Only these 3 files were upserted with `themeFilesUpsert` (userErrors `[]`). Readback: 3/3 equal `089a1da`.

## Live readback (headless Chromium, real add-to-cart, Adult M / Red sweater)

| Device (visible viewport) | Line-items area | Footer | Check out on screen | Wallet buttons |
|---|---|---|---|---|
| iPhone 13 (390×664) | 150 → 161 px | 445 → 434 px | yes | Shop Pay, Amazon Pay, PayPal, G Pay |
| iPhone 14 Pro Max (430×740) | 237 px | 434 px | yes | yes |
| Galaxy S9+ (320×658) | 155 px | 434 px | yes | yes |
| Pixel 7 (412×839) | 336 px | 434 px | yes | yes |
| iPhone SE (320×568) | drawer scrolls | — | after a scroll, clickable | yes |

- On every device and on `/cart`: no "countries enabled", no "after address entry"; "Ships to United States" and the dated "Estimated delivery:" line are still shown.
- 0 page errors.

## Rollback
`git revert 089a1da`, then upsert the three files from `089a1da^`.

## Residual
The express-wallet stack (183 px) is now the largest part of the fixed footer. On a 390×664 iPhone the line item shows its title and price, while the size/colour/quantity rows need a small scroll. The remaining option is a design decision for the drawer claim owner: for example, collapse the wallets to a single row, or show them only after a tap.

## Follow-up: express-wallet stack cap — commit `80576d3`
The drawer claim owner ("Website sales improvement") handed this off in chat. Target: on iPhone 13 (390×664), the first line's title, size and price are fully visible without scrolling, with Check out and at least the first wallet row on screen. Wallets are not hidden behind a tap.

- Cause: `shopify-accelerated-checkout-cart` lays out its buttons inside a closed shadow root. Shopify's CSS forces one column for 4 wallets when the container is ≤430px wide. A page-level grid on the host only creates one grid item, so a two-per-row layout is not possible from theme CSS.
- Change (`assets/component-cart-drawer.css`): only at `max-width:749px` and heights 651–760px, where the footer stays fixed, the wallet block gets `max-height:112px; overflow-y:auto; overscroll-behavior:contain`. That shows two rows plus a peek of the third; the rest scroll inside the block. The 40px button height and 5px gap stay as they were. At ≤650px the whole drawer already scrolls, and taller phones keep the full stack.
- Release: the GitHub sync dropped the push again. Live equalled `80576d3^`, so the one file was upserted (userErrors []). Readback: MD5 equals `80576d3`, and the storefront serves the minified rule.

LIVE readback (real add-to-cart, no injected CSS):

| Device | Items area | Footer | Title / size / price visible | Check out + first 2 wallets on screen | Last wallet reachable |
|---|---|---|---|---|---|
| iPhone 13 (390×664) | 161 → 232 px | 434 → 363 px | yes / yes / yes | yes | yes, by scrolling the block |
| iPhone 14 Pro Max (430×740) | 237 → 308 px | 363 px | yes | yes | yes |
| Galaxy S9+ (320×658) | 155 → 226 px | 363 px | yes | yes | yes |
| Pixel 7 (412×839) | 336 px (unchanged) | 434 px | yes | yes, full stack | — |
| iPhone SE (320×568) | unchanged: whole drawer scrolls | — | yes | Check out is clickable after a scroll | — |

Rollback: `git revert 80576d3` and upsert `assets/component-cart-drawer.css` from `80576d3^`.
