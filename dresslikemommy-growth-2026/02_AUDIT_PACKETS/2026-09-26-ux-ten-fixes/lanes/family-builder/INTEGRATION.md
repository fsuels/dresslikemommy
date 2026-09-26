# Lane F: family builder integration (for the parent session)

Status: the lane files are IMPLEMENTED and VERIFIED locally. They are not live until the parent applies the one-line patch below and releases through the normal commit, push to `main` and Shopify sync.

## Files (all new; nothing existing was edited)

| File | Purpose |
|---|---|
| `assets/dlm-family-builder.js` | The enhancement itself, plus pure helpers exported for node |
| `assets/dlm-family-builder.css` | Styles scoped to `.dlm-family-builder` and `[data-dlm-family-list]` |
| `snippets/dlm-family-builder.liquid` | Outputs the CSS tag and the deferred script tag |
| `ops/tests/test_family_builder.mjs` | Node tests (10) |

## Patch 1 (required): `layout/theme.liquid`, one line

The anchor is the product-only block in `<head>` that already loads `dlm-holiday-order-by.js` (around line 329 in the current working tree):

```liquid
  {%- if request.page_type == 'product' -%}
    <script defer src="{{ 'dlm-holiday-order-by.js' | asset_url }}"></script>
    {%- render 'dlm-family-builder' -%}
  {%- endif -%}
```

Insert only the `{%- render 'dlm-family-builder' -%}` line. It must come after `pubsub.js` and `global.js`, because the module uses `fetchConfig`, `publish` and `PUB_SUB_EVENTS` when they are available. This anchor already satisfies that. If the holiday block is not present when you apply this, wrap the line in its own `{%- if request.page_type == 'product' -%} … {%- endif -%}` directly after the `dlm-delivery-dates.js` line.

## Patch 2: `sections/main-product.liquid` (peer-claimed)

No change is needed. The module mounts on the existing `[data-product-desktop-ux]`, `[data-matching-set-builder]`, `[data-matching-set-roles]`, `[data-matching-set-add-button]` and `#ProductMatchingSetData-<section id>` hooks from `snippets/product-desktop-ux.liquid`. It also reads the price node `#price-<section id> .price[data-price-variant-id]`. All of these are live today.

Coupling to keep in mind if the peer or anyone else later edits the builder (`snippets/product-desktop-ux.liquid` or `assets/product-desktop-ux-20260513-ruler-sync.js`):

- The step UI must keep `[data-select-role-group]` role buttons with `aria-pressed`, one `[data-instance-card]`, pills `[data-instance-pill][aria-pressed][data-size-label]`, `[data-qty-value]` and `[data-qty-action="dec"]`.
- `updateMatchingPrice()` must keep setting `data-price-variant-id` to the resolved variant id.
- The builder must keep writing its button with `textContent =` and `setAttribute/removeAttribute('disabled')`. The module holds back those writes while the list has lines and replays them afterwards.
- The `dlm:matching-set-summary` event and `window.DLMMatchingSetStickyState` contract must stay as it is. The module publishes a list-aware state with `source: 'dlm-family-builder'` that both sticky bars already understand.

If any of these hooks goes missing, the module does not mount or does nothing. The original single-add flow keeps working.

## Behaviour summary

- With an empty list nothing changes. The builder's "Add this piece to bag" posts its own single `/cart/add` exactly as before (verified).
- Once a size is chosen, "+ Add another family member" appears. It keeps the choice as a line (person · size · extra options, × quantity, real line price, Remove) and moves the picker to the next person not yet in the list (Mother → Father → Child). When everyone is already in the list, it stays on the current person and clears the size, which covers a second child.
- With one or more lines, the builder's own button (and the desktop and mobile sticky bars that mirror it) reads `Add all to bag (N) · $total`. N and the total include a fully chosen selection still in the picker, so what is selected on screen is what gets added. One `POST <locale>/cart/add.js` sends JSON `{items:[{id,quantity}…], sections:"cart-drawer,cart-icon-bubble", sections_url}`. On success it clears the list, clears the picker size, shows the builder's existing localized success text, publishes `cartUpdate` and calls `cart-drawer.renderContents()`. Without a cart drawer it goes to `/cart`.
- If the request fails (HTTP error or `status` in the response), the list is kept and Shopify's localized `description` (or the translated fallback) is shown in a `role="alert"` box. A line whose variant is marked unavailable in the page data is blocked before the request is sent. Double submits are blocked with a busy flag and the button's `disabled`/`aria-busy` state (a triple click sends one request).
- Prices are the variants' own `price` values from `ProductMatchingSetData`, formatted with the shop's own money format learned from a rendered `price_text`. There is no bundle pricing and no discount.
- The module does nothing on products with fewer than two "who" choices (verified on `lavender-mommy-and-me-floral-applique-sleeveless-ruffle-dress`). It works on Mother/Child-only products (verified on `bamboo-garden-panda-mommy-and-me-pajamas`).
- There are 7 new strings, translated inline for en, es, fr, de, it, nl, pt, da, sv, no/nb, pl, cs, fi, ro, el, hu, tr, ru, ja, ko, zh, ar, he and hi. Other languages fall back to English.

## Owner live test script (run once after release, as a real shopper)

Agents must not do this, because a real add-to-cart fires ad pixels. Do it in a normal browser window, then empty the cart afterwards.

1. Open https://www.dresslikemommy.com/products/beanie-ghost-family-matching-pajamas on a phone.
2. Under "Choose who this piece is for", keep **Mother** and tap size **M**. Check that "+ Add another family member" appears under the size card. Tap it.
3. Expected: "Your family list" shows `Mother · M × 1 $35.99 USD Remove`, the picker switches to **Father**, and the green button reads `ADD ALL TO BAG (1) · $35.99 USD`.
4. Tap **L**, then "+ Add another family member". The picker should switch to **Child**.
5. Tap **4-5 Years**, tap **+** once (quantity 2), then tap "+ Add another family member". The list should show 3 lines and the button should read `ADD ALL TO BAG (4) · $137.96 USD`. Prices can differ if they have changed; the total must equal the sum of the lines.
6. Tap **Remove** on the Father line. The button should read `ADD ALL TO BAG (3) · $101.97 USD`.
7. Scroll down until the bottom sticky bar appears. It should show "Your family list (3)", "$101.97 USD" and the same button text.
8. Tap the green button once. Expected: one cart drawer opens with Mother M × 1 and Child 4-5 Years × 2. The cart count bubble updates, the family list disappears and the builder is back to "Pick a size".
9. Open the cart page and confirm the line items and prices match the page. Then **remove the items from the cart** so the test does not affect anything.
10. Single-add regression: pick **Mother · S** only and tap "Add this piece to bag". Exactly one item should be added, as before. Remove it.
11. Optional: repeat steps 2–8 on `/es/products/beanie-ghost-family-matching-pajamas`. Expect Spanish text ("+ Añadir otro familiar", "Añadir todo al carrito (3) · …").

If step 8 opens the drawer with only some items, or shows an error with valid sizes, remove the render line from `layout/theme.liquid`. That is the full rollback. Then report the drawer content and any error text.

## Rollback

Remove the single `{%- render 'dlm-family-builder' -%}` line. The asset and snippet files are then inert.
