# Italy funnel, 2026-11-26 (read-only, curl + Admin API reads)

Method: curl with cookie jars (mobile UA), IT shopper (`?country=IT`, `/it/...`) vs US shopper. Walk: `/it/collections/mommy-and-me` and `/matching-outfits` -> PDP `/it/products/nordic-yoke-family-matching-sweaters` -> `POST /it/cart/add.js` (Adult S Crema) -> `/it/cart`, `/it/cart.js`, drawer HTML -> `/cart/shipping_rates.json` -> `POST /it/cart` (checkout=) first page load only; nothing typed. Cart never left in a shared state (own jar). Admin token scopes have no `read_markets` and no delivery profiles, so market price adjustment, rounding, duties and delivery-profile zones could NOT be read (ACCESS_DENIED). Not repeated from `conversion-audit-2026-11-26.md` (PDP price/photo/seller/date items), only cross-referenced.

## What works (no cause here)
- Currency chain is consistent in EUR: card `€40,95 EUR` -> PDP `Bambini da €40,95 EUR · Adulti da €53,95 EUR` -> cart.js `EUR 5395` -> `/it/cart` `€53,95 EUR` -> checkout `53,95 €`. No price change between steps.
- Cart, drawer, PDP and checkout are fully Italian (`lang="it"`, `/checkouts/cn/.../it-it`, "Spedizione gratuita", "Tasse calcolate al momento del pagamento"). No English strings found in cart, drawer or checkout. Checkout button = `<button name="checkout" form="cart">` posting to `/it/cart`; it loads (HTTP 200).
- Shipping: `shipping_rates.json` IT 00100 RM = one rate "Free Standard Shipping" 0.00 EUR; US 10001 = same, 0.00 USD. No IT-only shipping block or surcharge.
- Stock: all 30 sampled IT products have every variant available (e.g. Nordic Yoke 32/32). Size charts are in cm, kg, height. Titles are Italian.

## Ranked causes

1. **Hidden import VAT / duties at the door (probable biggest cause).** FIX_THEME + OWNER.
   - Evidence: shop `taxesIncluded:false`; checkout JSON for IT has `"dutiesIncluded":false`, `"taxesIncluded":false`, `totalTaxAmount 0.0` (range 0.0 to 4.56 EUR) on a 53,95 EUR basket, i.e. no 22 % Italian VAT is charged at checkout. The product ships from outside the EU (cart policy: "molti dei quali situati al di fuori degli Stati Uniti", 12-16 days). The only warning is buried in the PDP shipping accordion: "Gli ordini internazionali possono essere soggetti a tasse locali, dazi o spese doganali riscosse dal corriere o dall'autorità locale." The cart says only "Tasse calcolate al momento del pagamento", which an Italian reads as "all-in at checkout", then the checkout shows no tax line.
   - Why it kills carts: the shopper sees the price, cannot tell whether VAT/customs/courier fee arrive later, and has no seller credibility signal (1 review). Unexpected-fee doubt is the classic EU abandon trigger.
   - FIX_THEME: for IT/EU visitors replace the cart/drawer line with an honest one, e.g. "Spedizione gratuita. IVA e dazi non sono riscossi al checkout: possono essere richiesti dal corriere alla consegna." only after the owner confirms what actually happens (OWNER). Show it in the PDP shipping box (first screen of box), not only in the accordion.
   - OWNER: decide DDP/IOSS (collect VAT at checkout; needs IOSS registration and price/margin change) vs keep DDU and say so plainly. Check Shopify Settings > Taxes and duties > European Union / Italy, and Markets > Italy "Duties and import taxes". Also confirm what the EU courier really charges on a 54 EUR parcel; if it is a handling fee, that is the real shock.

2. **Italian prices carry no sale signal and are higher than the US number.** OWNER + FIX_ADMIN.
   - Evidence: every sampled product has `compare_at_price` set in US (e.g. Nordic Yoke 37.99 vs 47.99, Cream Heart 24.99 vs 34.99) and `null` in IT (`/it/products/*.js`). US cards show "-21%"; IT cards show a bare `€40,95`. IT/US nominal ratio 1.066 to 1.098 (typically 1.078: 3799 -> 4095, 4999 -> 5395, 2499 -> 2695, 3199 -> 3495). `Shopify.currency` rate on IT page = 0.925, so 40,95 EUR is about +16.5 % over the market rate (not the 25 % reported; could not read the market adjustment setting). The higher base price is shown without the discount story US shoppers get, and the "Compra 2, il 3° capo è scontato del 20%" line is the only offer.
   - FIX_ADMIN: if the owner confirms the compare-at is a genuine former price (see audit item 11), add the matching EUR compare-at to the Italy market price list (Markets > Italy > Catalogs/Price lists) so card, PDP, cart agree with the US treatment. If not genuine, do the opposite and remove the US strike-throughs. Do not add one without the other.
   - OWNER: price adjustment for Italy (currently about +16 to +17 % beyond FX); a lower adjustment is a margin decision.

3. **Checkout asks for a mandatory phone number.** FIX_ADMIN.
   - Evidence: IT checkout HTML `name="phone" placeholder="Telefono" required type="tel" aria-required="true"` and `addressFormSettings.phone.mode":"REQUIRED"`, first name REQUIRED, company IGNORED. Same in US. First field group for a guest also lists Telefono. Italians are reluctant to give a phone number to an unknown shop with a new site.
   - FIX_ADMIN (reversible): Settings > Checkout > "Shipping address phone number" -> Optional (carrier tracking still works via email). Keep a note of the previous value.

4. **Collection pages: 116-plus products, no occasion entry, filters polluted by design names.** FIX_THEME.
   - Evidence: `/it/collections/mommy-and-me` (123 organic sessions) = 35 cards rendered, 133 colour filter values of which about 34 distinct; the Colore filter lists design names as if they were colours: "Avventura polare – color crema", "Miao: giardino di stelle", "Buonanotte Canzone del mare", "Cottage vintage floreale", "Dinosauro gallese – color crema", plus "Multi-Color"; "Nero" sorted before "Blu navy" and "Verde" (English sort order of translated names). `/it/collections/matching-outfits` same pattern (45 distinct). The first four cards of both are family Christmas sweaters (Nordic Yoke, Double Heart, Vintage Argyle), not mother-and-child items, so a Google visitor for "mamma e figlia coordinati" sees family sweaters first.
   - FIX_THEME: hide colour values that are not real colours (use only the product-option colour list, or the filter's `custom.color_family`), and keep Mommy and Me first cards as mother-daughter pieces (collection sort/pin; check `SORT_ORDER_PACKET.md` with Merchandising). Add the "Shop by who" chips already recommended in audit item 10.

5. **Mixed-language labels and copy reduce trust.** FIX_THEME (translations).
   - "Mamma e Me", "Papà e Me" (collection chips, breadcrumbs, some titles: "Abiti rosa con volant Mamma e Me", "Gonne in tulle rosa e blu Mamma e Me"): half English. Natural Italian: "Mamma e figlia" / "Mamma e bimbo", "Papà e figlio".
   - Sort option "Best seller" untranslated (the `value=best-selling` option label).
   - Cart and PDP show `€53,95 EUR` (symbol plus code); the Italian norm is `53,95 €`. The same price in checkout reads `53,95 €`, so the two formats collide.
   - PDP text: empty labels "Prezzo unitario /  per ", dangling "Consegna stimata:" at the end of details, label "Prezzo di listino" (regular price) shown with no strike-through price.
   - Size chart: decimals with dot ("7.5 kg", "17.5 kg") instead of comma; columns "Pantaloni/Shorts", "Fianchi", "Vita" are all "-" for a sweater (clutter on a phone).
   - FIX_THEME: in `locales/it.json` and the size-chart snippet; no schema change.

6. **Cart page in Italian lacks the family tile and the "each piece sold separately" line the US cart has.** FIX_THEME (low).
   - Evidence: `/cart` (US) text includes "Complete the family ... Each piece is sold separately."; `/it/cart` text goes straight from the line item to "Hai un codice sconto?" (the block is in the markup, 4 matches vs 6, but renders no visible text for IT). Delivery line says "Consegna stimata: 12-16 giorni" with no date (US shows dates), fine but less reassuring.
   - FIX_THEME: check why `dlm-complete-family` prints nothing on `/it/cart` (page cart only; drawer shows "+ Aggiungi una taglia per un altro familiare").

## Not found / cleared
- No broken add-to-cart, no cart error, no missing checkout button, no English strings in cart or checkout, no sold-out variants, no currency flip between steps, no IT-only shipping charge.
- Not verifiable here: real Italian courier VAT/handling fee, Markets Italy settings (price adjustment, rounding, "duties and import taxes" toggle), delivery profile zones (need `read_markets` / delivery scopes), and the interactive checkout after the address (tax and total after typing an address). Cookieless curl from a US IP on `/it/...` shows `Shopify.country = "US"`, USD (Italian text, `$` prices); a real Italian IP would be geolocated by Shopify, but that was not tested from Italy. Someone on a US VPN or a first-visit with no country cookie would see Italian text with dollar prices.

## Verdict
The Italian walk works mechanically: EUR prices are identical on card, PDP, cart and checkout, the page is fully Italian, shipping is free, nothing is sold out, and the checkout opens in Italian. The leak is trust and total-cost doubt, not a bug. A shopper who adds a 54 EUR sweater from a new shop with one review is told only "Tasse calcolate al momento del pagamento" and then sees no tax line, while a buried paragraph says local taxes, duties and customs may be collected by the courier; Italy also gets prices about 16 % above the market rate with no strike-through (US gets -21 %), a mandatory phone number, and a collection page whose filters and chips are half-English. Rank 1 (VAT/duty honesty or IOSS) is an owner decision and the likeliest driver; ranks 3 to 6 are small reversible changes that can ship now.
