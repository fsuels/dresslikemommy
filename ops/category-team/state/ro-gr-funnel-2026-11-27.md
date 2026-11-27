# Romania and Greece: cart -> checkout walk (read-only, 2026-11-27)

Method: built-in browser, own tab in front, 375x812, 13 store loads (10 s or more apart, all 200, no 429/403) plus 2 `shipping_rates.json` reads. Country set with `?country=RO` / `?country=GR` (the same `/localization` change the store selector makes). The selector in the mobile menu did not open in the hidden pane, so I used the URL route. Path: /ro (or /el) collection "Christmas sweaters" -> Nordic Yoke family sweater -> builder (Adult, S, Cream) -> drawer -> /ro/cart (/el/cart) -> sticky "Check out" -> checkout first screen. Nothing typed, no method chosen, nothing sent. Cart emptied and country set back to ES (the pane's start state) at the end. Prior studies not repeated: Italy, CZ/CA, country-currency path, cart reassurance, cart drop-off analytics.

Test note: my earlier theme preview left Shopify's preview bar iframe (`PBarNextFrame`) covering the page, and it swallowed the first two Check out clicks. Loading `?preview_theme_id=` (empty) removed it. Real shoppers never get this bar; it is not a store defect.

## Step x country

| Step | Romania (/ro, RO) | Greece (/el, GR) |
|---|---|---|
| Collection | RON. Cards "De la 182,00 RON" (Reindeer), "217,00 RON" (Nordic). No strike-through or badge. Christmas line: delivery times differ by country, order early. | EUR. Cards "Από €34,95", "€40,95", "€39,95". No strike-through. Same Christmas line in Greek. |
| PDP | "Copii de la 217,00 RON · Adulți de la 285,00 RON". Adult S = 285 RON vs US $49.99 x 4.9457 = 247 RON: **+15 %**, compare_at null (US has one). Dated estimate "Livrare estimată: mie., 16 dec. – mie., 23 dec.". The colour must be picked separately ("! Alegeți culoarea"): the first Add press did nothing until colour was chosen. No tax text on the PDP first screen. | "Παιδιά από €40,95 · Ενήλικες από €53,95". Adult S €53.95 vs $49.99 x 0.9258 = €46.28: **+16.6 %**, compare_at null. Same dated estimate "16 Δεκ – 23 Δεκ". "Περιλαμβάνεται τυπική αποστολή", "Αποστολή σε Ελλάδα". |
| Drawer / cart | 285,00 RON. Family tile prices in **"lei"** ("+ Copil 217,00 lei") beside **"RON"** lines: two formats on one screen. "Livrare STANDARD INCLUS" (odd caps). Estimate 16–23 Dec, "Livrare în România", "Taxele sunt calculate la finalizarea comenzii.", trust row (secure, shipping included, 30-day returns). Sticky bar "Total estimat 285,00 RON · Finalizare comandă". DCL 0.76 s. | €53,95 consistent. "Αποστολή ΤΥΠΙΚΗ, ΠΕΡΙΛΑΜΒΑΝΕΤΑΙ" (caps), estimate 16–23 Dec, "Οι φόροι υπολογίζονται στο ταμείο.", same trust row. The product title in the cart ("Σκανδιναβικό μοτίβο στους ώμους – …") differs from the PDP title. DCL 0.59 s. |
| Checkout, first screen | `/checkouts/cn/…/ro-ro`, Romanian, DCL 1.3 s. "285,00 lei" (code "RON" by the total). Subtotal 285,00 lei; Transport "enter the shipping address"; **no tax line**. **Phone required** (`required`, "Telefon"); postal code optional; Județ list present. Payment: Shop Pay express, card ("+5" brands), PayPal, Crypto USDC. **No cash on delivery (ramburs)**. Shipping API for RO: one rate "Free Standard Shipping" 0.00 RON, no delivery days, name in English in the API (checkout label after an address not seen). | `/checkouts/cn/…/el-gr`, Greek, DCL 1.5 s. **Phone required** ("Τηλέφωνο"), postal code optional. Payment: Shop Pay, card (Mastercard, Amex…), PayPal, Crypto USDC; no cash on delivery (αντικαταβολή), no IRIS. Shipping line "Δωρεάν". **Surprise:** this checkout opened with country Romania and **285,00 lei**, not €53.95, and visiting it switched the store back to RO/RON. The same checkout token was kept from the RO run, so Shopify reused the earlier checkout's country. A real Greek shopper on a fresh device would not see this; a shopper who switches country in one browser would. Shipping API for GR: "Free Standard Shipping" 0.00. |

No console errors except the known 401s. No horizontal overflow. No visible English text in the RO/GR path. The aria label "Adult size" / "Ενήλικας size" is screen-reader text only.

## Most likely causes, ranked

### Romania (105 visits, 29 carts, 2 checkouts, 0 orders)
1. **No cash on delivery; card or PayPal only, paid in advance to an unknown foreign shop.** "Plata ramburs" is the default way many Romanians pay online. A shopper who expects it adds to cart, reaches the payment step and stops. This fits an unusually high cart rate with almost no checkout starts. Hypothesis: no Romania-specific payment data here. -> **Owner decision** (offer COD as a manual method, which carries courier and risk cost), set up in **Admin (blocked today)**. No phrase exists in DECISIONES_FRANK.md.
2. **Total cost unclear: "Taxele sunt calculate la finalizarea comenzii" and no tax line at checkout.** Goods ship from outside the EU and Romanian VAT 19 % is not shown. Same as Italy rank 1. -> **Owner decision**, then **theme (you)** for the cart wording. Existing phrases (item 33): «deja el aviso claro en el carrito» (recommended), «el IVA ya va incluido en Europa», «el IVA se cobra aparte al pagar», «incluye IVA en los precios de Europa».
3. **Price about 15 % above the exchange rate with no strike-through, plus a mandatory phone number.** -> **Owner** (item 32): «iguala precios de Europa al cambio» (or «déjalos así»). Phone: **Admin (blocked)** / owner (item 3): «pon el teléfono opcional». Small **theme (you)** fix alongside: one currency format in the cart (the family tile shows "lei", the lines "RON"), and "STANDARD INCLUS" in normal case.

### Greece (60 visits, 7 carts, 1 checkout, 0 orders)
1. **Price about 16.6 % above the exchange rate, no strike-through, against a US price that shows -21 %.** -> **Owner** (item 32): «iguala precios de Europa al cambio».
2. **Payment methods:** no cash on delivery (αντικαταβολή, widely used in Greece), no IRIS, and only card, PayPal and Crypto USDC to a foreign shop. -> **Owner decision** + **Admin (blocked)**. No phrase exists.
3. **Tax doubt and a mandatory phone number** (same evidence as RO 2 and 3). -> Owner item 33 «deja el aviso claro en el carrito» (then theme), and item 3 «pon el teléfono opcional» (Admin).

### Not a cause, but worth a look
- Christmas timing: both countries show "16–23 Dec" and "order early". A range that ends on 23 Dec is a weak promise for Christmas gifts. No delivered RO/GR order exists to prove it.
- Checkout country memory (the GR run above): low frequency, already classed OWNER-watch in `country-currency-path-2026-11-27.md`.
- The builder needs a separate colour tap (first Add press did nothing). This applies to every country; it is a PDP builder matter (owner rule: keep the PDP builder simple), so I am not proposing a change.

## Not verified
Tax and shipping lines after an address is typed (not allowed), the shipping method name shown at checkout for RO, Apple Pay / Google Pay (they depend on the device), and real Romanian or Greek payment-method shares (no analytics on payment-step exits).

# Follow-up: one Romanian currency form ("lei"), 6ce188c (2026-11-27 ~09:44Z)

Source of the mix (theme, not Admin): Shopify's own formats for RON are `money` = "285,00 lei" and `money_with_currency` = "285,00 RON". `snippets/dlm-show-currency-code.liquid` told every non-US, non-EUR market to use `money_with_currency`, through `dlm-cart-money` (cart lines, total, drawer, sticky bar), `price.liquid`, `dlm-price-groups`, `dlm-card-price` and the builder JSON. The family tile (`snippets/dlm-complete-family.liquid` 896/935) always uses plain `money`. Result: "RON" on lines, total and sticky bar, "lei" in the tile. The Romanian checkout shows **"285,00 lei"** (with the ISO code only as the small label by the total).

Change: `dlm-show-currency-code` now leaves the code off for RON, as it already did for EUR (3 lines). Amounts, rounding and conversion untouched.

Test on the copy "gallery-test 2026-11-27" (made equal to the published theme first: 2 files copied, then only this snippet differed; id and role UNPUBLISHED checked). 7 loads:
- RO product page: "Copii de la 217,00 lei · Adulți de la 285,00 lei"; 10 "lei", 0 "RON".
- RO cart and sticky bar: 9 "lei", 0 "RON"; bar "Total estimat 285,00 lei". Drawer HTML (sections render): 7 "lei", 0 "RON".
- CAD, SEK and EUR unchanged. CAD: "$73.00 CAD" on lines and bar. EUR: "€53,95" everywhere.
- Preview bar not in the measures; I left preview mode, emptied the cart and restored ES.

Release with the new order: commit 6ce188c, wait 90 s, read-only list (1 differ), apply (applied 1), re-check 0. Shopify export a1d4b38 keeps the snippet. Lock held 09:43Z to 09:47:40Z. Live: RO product page 10 "lei" / 0 "RON", live drawer 0 "RON".

Found, not changed (same root cause, other currencies, it was already like this): the family tile prints plain `money` while the rest prints the code. CAD shows "$73.00 CAD" lines with "$55.00" in the tile; SEK shows "596,00 SEK" lines with "453,00 kr" in the tile; CZK probably the same. Fix option (theme): give the tile the same `dlm-show-currency-code` rule. That snippet is the one whose earlier change was reverted (16967c1), so it needs its own unit.

# Follow-up 2: one money format for every currency, 300f13d (2026-11-27 ~10:16Z)

Cause: three theme surfaces did not follow `dlm-show-currency-code` like the Liquid prices do.
- `snippets/dlm-complete-family.liquid` (family tile, cart page and drawer) printed plain `money`.
- `snippets/product-desktop-ux.liquid` desktop sticky price printed plain `money` on first paint (the JS then copies the rendered price).
- `assets/product-desktop-ux-20260513-ruler-sync.js` `formatMoney` used `Intl.NumberFormat`, which gives "CA$55.00", "A$70.00", "453,00 kr" and "40,95 €" for the builder's "ready" chip and its sticky total.
The cart page sticky bar already copies the server-rendered total, and the drawer and cart lines use `dlm-cart-money`.

Fix (presentation only):
- The tile captures the same flag and uses `money_with_currency` / `money` like `dlm-cart-money`.
- The desktop sticky price uses the same flag.
- The PDP script learns the store format from the page's own Liquid `price_text` (`parseMoneyFormat`, the same parser the old family builder used). `formatMoney(cents, currency, format)` uses it, with Intl only as a fallback.
No change to amounts, rounding or conversion.

Copy test (made equal to the published theme first, then only these 3 files differed; id and role UNPUBLISHED checked). Per country: PDP price, desktop sticky, builder format, cart lines, tile, sticky bar, drawer lines and tile. Builder output = the script's own `formatMoney` with the learned format.
| Country | One format everywhere | Builder before (Intl) |
|---|---|---|
| CA | $55.00 CAD / $73.00 CAD | CA$55.00 |
| SE | 453,00 SEK / 596,00 SEK | 453,00 kr |
| RO | 217,00 lei / 285,00 lei | 217,00 RON |
| DE | €40,95 / €53,95 | 40,95 € |
| US | $37.99 / $49.99 | same |
| AU | $70.00 AUD / $92.00 AUD | A$70.00 |
| GB | £34.00 GBP / £45.00 GBP | £34.00 |
Console: no errors. Matches the RO checkout ("285,00 lei"). The SE, DE, CA, AU and GB checkouts were not opened this round. Shopify's checkout formats by locale, so SE may show "kr" and DE "53,95 €" there; the store's own format comes from Admin currency formatting, which is outside the theme.

Release order: lock 10:15Z; commit 300f13d; wait 90 s; read-only list (3 differ); apply (3); re-check 0. Shopify export 726b65b keeps all 3 files. Lock released 10:19Z. Live CA and SE: every surface shows "$55.00 CAD / $73.00 CAD" and "453,00 SEK / 596,00 SEK". Cart emptied, country back to ES.
Rollback: `git revert 300f13d` via ceo_worktree, then sync-theme.
