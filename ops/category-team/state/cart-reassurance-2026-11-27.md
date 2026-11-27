# Cart reassurance next to the total (2026-11-27)

Read-only result: nothing to add. The three facts the unit asked for are already shown in the cart page and in the cart drawer, from existing, translated keys and the same transit logic as the product page. No code, no locale and no theme change; no lock taken; nothing published.

Read first: `cart-dropoff-2026-11-26.md`, `mobile-cart-ux-2026-11-26.md`, `delivery-statements-2026-11-26.md`, `cart-bar-2026-11-27.md`. Code read at origin/main: `sections/main-cart-footer.liquid`, `snippets/cart-drawer.liquid`, `snippets/delivery-estimate-copy.liquid`, `snippets/dlm-transit-map.liquid`, `snippets/christmas-order-by.liquid` (via the 11-26 notes).

## What the cart shows today, in order around the total

Cart page (`main-cart-footer.liquid`, subtotal block) and drawer (`cart-drawer.liquid:784-923`) use the same blocks:

1. Shipping cost: "Shipping — Standard included" (`sections.cart.shipping_label` / `sections.cart.shipping_free`; es "Envío — Estándar incluido", de "Versand — Standard inklusive", ro "Livrare — Standard inclus"). No "free".
2. Delivery estimate for the visitor's country: `snippets/delivery-estimate-copy.liquid` (no `product`), same snippet and same `dlm-transit-map` numbers as the product page: countries in the map (US, CA, GB, DE, FR, IT, ES, CZ, NL, PL, SE) get transit + 5 days, turned into a date range by `assets/dlm-delivery-dates.js`; every other country gets the neutral "delivery times vary by country" line (`dlm-delivery-vary-copy`), no numbers.
3. Christmas order-by line (`christmas-order-by`, US dated only; neutral elsewhere) when a Christmas item is in the cart.
4. "Ships to <country>" (country checker), then Estimated total, then "Taxes calculated at checkout" + "Shipping details" (the shipping policy).
5. Check out button; on mobile the sticky bar (total + Check out).
6. Below the button: wallets, then trust row: "Secure Checkout · SSL Encrypted · Shipping included · 30-day returns" (`sections.cart.trust.*`; es "Devoluciones de 30 días", de "30-tägige Rückgabefrist"). In the drawer the trust strip ("Secure · Shipping included · 30-day returns") sits directly under the payment icons below Check out.

Returns truth: published return policy page says 30 days from delivery (`delivery-statements-2026-11-26.md`, "Pages: return-policy (30 days from delivery...)"), so "30-day returns" is supported.

## Live check (built-in browser, own tab, 2 loads 10 s+ apart, 375 px)

`/cart` with 1 test item (Bamboo Garden Panda, variant 44047096119393), visitor country Spain (EUR):
| Element | Y (px) | Text |
|---|---|---|
| Shipping line | 850 | Shipping STANDARD INCLUDED |
| Delivery note | 894 | Estimated delivery: Wed, Dec 16 – Wed, Dec 23 |
| Country | 921 | Ships to Spain |
| Total | 967 | Estimated total €38,95 |
| Taxes/policy | 990 | Taxes calculated at checkout. Shipping details |
| Check out | 1015 | CHECK OUT |
| Wallets | 1077 | |
| Trust row | 1129 | Secure Checkout SSL Encrypted Shipping included 30-day returns |
| Sticky bar | 743 (fixed) | Estimated total €38,95 Check out |
No horizontal overflow (375). The drawer was not opened (its markup on /cart is empty until it is used); its content above is from the code. Spain check: 14-21 + 5 = 19-26 days from today (Nov 27) = Dec 16 to Dec 23, matches. Test item removed (cart 0), viewport reset, tab closed. No checkout opened.

## Decision

Nothing is missing, so no line was added (adding "30-day returns" a second time beside the total would only duplicate the trust row 114 px lower). No new keys are needed. The only possible tweak, if the CEO wants returns above the button, is moving the existing trust row (or just its returns item) to sit under "Taxes calculated at checkout" on the cart page; that is a layout change, not new text, and I did not make it.

## Where the cart-to-checkout gap more likely is (already documented, owner decisions)

From `mobile-cart-ux-2026-11-26.md`: (1) EU/UK shoppers read "Taxes calculated at checkout" plus a shipping policy saying import VAT/duties are theirs, while checkout shows no tax line: owner choice IOSS/UK VAT collection vs. one honest DDU sentence; (2) mandatory phone at checkout: set to optional; (3) RO and other unmapped countries see only "delivery times vary" while checkout shows "Standard (10 - 14 days)" (stale method names, `delivery-statements` pattern 1). None is a missing cart line.
