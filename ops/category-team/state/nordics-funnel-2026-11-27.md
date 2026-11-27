# Sweden, Norway, Denmark: collection -> cart -> checkout walk (read-only, 2026-11-27)

Why: Sweden + Norway brought 200 organic visits in 14 days and 0 checkout starts. Denmark brought 72 visits, 8 carts and 1 order (`_DATA.md`: SE 117/6/0/0, NO 83/2/0/0, DK 72/8/1/1).

Method: built-in browser, own tab in front, 375x812, 13 store loads at 10 s or more apart, all fine (no 429/403, no verification page). Model: `ro-gr-funnel-2026-11-27.md`.
- Sweden was set with the store's country selector (mobile menu). Norway and Denmark used `?country=NO` / `?country=DK`, the same `/localization` change, to stay under the load limit.
- Path in each country: /sv, /no, /da collection "family-sweaters" -> Nordic Yoke family sweater -> builder (Adult, S, Cream) -> add to cart -> cart page.
- Nothing was typed in any field and no payment method was chosen.
- The cart was emptied after each country. The country was set back to Spain (ES/EUR, the start state) and the cart is empty (read back).

**Checkout was reached only once** (Sweden, first run). The second Swedish attempt was **refused by the session's permission check**. I did not try another way, so the NO and DK checkouts are **NOT RUN**.

Exchange rate = the rate the store applies today (`Shopify.currency.rate`): 1 USD = 10.3608 SEK = 6.9191 DKK. US reference: Nordic Yoke adult S $49.99 (kids from $37.99), shown in the US with a struck "regular" price (-21%).

## Step x country

| Step | Sweden (/sv) | Norway (/no) | Denmark (/da) |
|---|---|---|---|
| Collection | **SEK**. "Barn från 453,00 SEK · Vuxna från 596,00 SEK". No strike-through. Bar "STANDARDFRAKT TILL SVERIGE INGÅR". Christmas text without a date: "check the estimated date on each product and order early". | **SEK (Swedish kronor) on the collection page**, then USD from the product page on (see note 1). Same card prices as Sweden. Bar "STANDARDFRAKT TIL NORGE INKLUDERT". A line "FÅ 10 % RABATT PÅ DIN FØRSTE BESTILLING" (10% off the first order) is in the page; source not checked. | **DKK**. "Børn fra 303,00 DKK · Voksne fra 398,00 DKK". No strike-through. |
| Product page | Adult S 596 SEK vs $49.99 x 10.36 = 518 SEK: **+15.1%**. Kids +15.1%. "Pris per plagg". Delivery "mån 14–lör 19 dec." Christmas line has no date: "Leveranstiderna varierar mellan länder, så beställ så tidigt som möjligt". No tax text. Builder fully translated. | **USD**: "Barn fra $43.69 USD · Voksne fra $57.49 USD" = **+15.0%** over the US price. Delivery "ons. 16.–ons. 23. des." (2-4 days later than SE/DK). Same Christmas line without a date. No customs or VAT text. | Adult S 398 DKK vs $49.99 x 6.92 = 346 DKK: **+15.1%**. Delivery "man. 14.–lør. 19. dec.". Same Christmas line without a date. No tax text. |
| Payment icons (product page and cart, same list everywhere) | Amazon, Amex, Apple Pay, Bancontact, Diners, Discover, Google Pay, iDEAL Wero, Mastercard, MB WAY, PayPal, Satispay, Shop Pay, USDC, Visa. **No Klarna, no Swish.** | Same. **No Vipps, no Klarna.** | Same. **No MobilePay, no Klarna.** |
| Drawer / cart page | 596,00 SEK everywhere. "Frakt STANDARD INGÅR" (odd capitals). "Beräknad leverans: mån 14–lör 19 dec.", "Frakt till Sverige", "Beräknad totalsumma 596,00 SEK", "**Skatter beräknas i kassan.**" Trust row: secure payment, shipping included, 30-day returns. | $57.49 USD everywhere. **Cart page title in English: "Your Shopping Cart – Dress Like Mommy"** (SE and DK are translated). "Frakt STANDARD INKLUDERT", "Frakt til Norge", "Anslått total $57.49 USD", "**Skatter beregnes ved betaling.**" **No word about customs, import VAT or fees.** | 398,00 DKK everywhere. "Forsendelse STANDARD INKLUDERET", "Forsendelse til Danmark", "Estimeret totalbeløb 398,00 DKK", "Skatter beregnes ved betaling." |
| Checkout, first screen | `/checkouts/cn/[token]/sv-se`, Swedish. **Surprise: it opened with country Greece and "53,95 €", not 596 SEK** (note 2). **Phone required** ("Telefon … Om vi behöver kontakta dig"), postal code required. Shipping "Fri standardfrakt – GRATIS", no delivery days. **No tax line.** Payment: express block (Snabbkassa), card (+5 brands), PayPal, Crypto USDC. **No Klarna, no Swish.** The country list includes Sverige, Norge and Danmark. | NOT RUN (permission refused) | NOT RUN (permission refused) |

Notes
1. Norway currency. NOK cannot be enabled in this store, so Norway gets USD. On my run, the Norwegian collection page still showed SEK: the cart-currency cookie from the Swedish run was still set. From the product page on, everything was in USD. A Norwegian on a fresh phone most likely sees USD on every step. Not verified on a clean browser.
2. Checkout country memory. This is the same effect the RO/GR walk recorded, and it may be made worse by other agents changing the country in this same browser at the same time. When I started, the store's localization cookie read ES while the checkout showed GR. A real Swedish shopper on their own phone would not see this. I cleared the cart and the cart cookie afterwards.
3. No visible English except the Norwegian cart page title. No broken layout. The builder needs the colour tapped separately, as in RO/GR, and is not proposed for change (owner rule: keep the product-page builder simple).

## Denmark (buys) vs Sweden and Norway (do not)

- **Denmark vs Sweden.** The store path is almost the same: local currency, the same +15% markup, the same dates (14–19 Dec), the same payment list, the same "taxes at checkout" line. The difference between them (SE 6 carts / 0 checkouts, DK 8 carts / 1 order) is small numbers. With 6 carts, zero checkouts can happen by chance. **The store does not explain why Sweden sells less than Denmark.** The most likely gap is how Swedes pay: Swish and Klarna are the usual ways, and neither is offered.
- **Denmark vs Norway.** These two do differ:
  - Norway sees **US dollars**; Denmark sees its own currency.
  - Norway is **outside the EU** and nothing is said about import VAT or fees, so a Norwegian expects a charge on delivery.
  - Norway's delivery is 2-4 days later (16–23 Dec).
  - Norway has an untranslated cart title.
  - Norway's usual way to pay (Vipps) is missing.

## Three most likely causes per country

### Sweden (117 visits, 6 carts, 0 checkouts)
1. **Missing the usual ways to pay: Swish and Klarna.** Only card, PayPal, express wallets and USDC are offered, paid in advance to a foreign shop. -> **Owner decision**, then **Admin (blocked today)** (Shopify Payments / Klarna app). No existing phrase in DECISIONES_FRANK.md.
2. **Total cost unclear.** "Skatter beräknas i kassan", no tax line at checkout, goods from outside the EU. -> **Owner decision**, then **theme (me)** for the cart wording. Existing phrases (item 33): «deja el aviso claro en el carrito» (recommended), «el IVA ya va incluido en Europa», «el IVA se cobra aparte al pagar», «incluye IVA en los precios de Europa».
3. **Price +15% over the exchange rate with no strike-through (the US shows -21%), and a mandatory phone number.** -> **Owner**: item 32 «iguala precios de Europa al cambio» (or «déjalos así»); phone, item 3 «pon el teléfono opcional» (one click in **Admin**). Small **theme (me)** fix alongside: give Nordic markets an order-by date instead of the generic "order early" line, if the per-country window can be parsed (it shows 14–19 Dec, so an order-by line would be truthful).

### Norway (83 visits, 2 carts, 0 checkouts)
1. **Prices in US dollars** (NOK cannot be enabled; memory note "markets currency availability"). A Norwegian sees "$57.49 USD" from the product page to the cart, which feels foreign and leaves the bank's exchange cost unknown. -> **Owner** (decide whether to keep selling to Norway in USD or show prices in EUR) / **Admin (blocked)**. No existing phrase.
2. **No word on customs or import VAT outside the EU.** Under Norway's VOEC scheme, if the shop does not collect Norwegian VAT, the carrier usually charges 25% plus a fee on delivery. I could not check whether this store collects it (checkout not run, no Admin read). The cart only says "Skatter beregnes ved betaling". -> **Owner decision** (collect VAT or say that the buyer pays it) + **theme (me)** for one truthful cart line once decided. Closest existing phrase: item 33 «deja el aviso claro en el carrito».
3. **Missing local ways to pay (Vipps, Klarna), +15% price, phone required, later delivery (16–23 Dec), English cart title.**
   - Payments and price -> **owner**, item 32 «iguala precios de Europa al cambio».
   - Phone -> item 3 «pon el teléfono opcional».
   - Cart title -> **theme (me)**: the `no` locale shows Shopify's English page title "Your Shopping Cart". The theme can set the cart page title from its own translated string ("Handlekurven din", already in `locales/nb.json`).

### Denmark (72 visits, 8 carts, 1 order): what works
Local currency (DKK), a dated delivery estimate (14–19 Dec), a fully translated path. The same gaps remain and could hold back more orders:
- no MobilePay or Klarna (**owner + Admin**, no phrase);
- +15% price (item 32);
- "taxes at checkout" (item 33);
- phone required (item 3).

## What I can do now (theme, no owner needed)
1. Norwegian cart page title from the theme's own translation (`no` shows "Your Shopping Cart").
2. Normal capitals for "STANDARD INGÅR / INKLUDERT / INKLUDERET" in the cart (same fix family as RO "STANDARD INCLUS").
3. A dated order-by line for SE and DK, which show a 14–19 Dec window: today they get only "order as early as possible". Check the Christmas order-by script for why these markets get the generic line before changing it.

## Not verified
- Norwegian and Danish checkouts (permission refused).
- The Swedish checkout in its own currency (it opened as Greece/EUR).
- Tax and shipping lines after an address is typed.
- Whether Norwegian VAT is collected (VOEC).
- Real payment-method shares.
- Whether the "10% off the first order" line on the Norwegian page is a live, honoured offer.
