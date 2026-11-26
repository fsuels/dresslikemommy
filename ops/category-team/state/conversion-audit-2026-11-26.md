# Conversion audit, 2026-11-26 (read-only)

Method: own tab in the Claude browser pane, live site, US/English at 375x812 first, then 1440x900; Canada (CAD) and Czechia (Czech) at desktop width; country and language switched with the store's own selectors and put back to United States / English (checked: cart 0, USD, `en`). Nothing typed into checkout. Cart cleared with `/cart/clear.js` after each leg (0 items at the end). Pages: both sweater PDPs, `/collections/christmas-sweaters`, `/collections/mommy-and-me`, home, cart drawer, `/cart`, first checkout step. Evidence is page text and measured positions (document Y in px) read from the live DOM; PDP data from `/products/<handle>.js`.

## 1. The path as observed

### Home (mobile)
- First screen: black bar "BUY 2, GET A 3RD PIECE 20% OFF", header, green line "Order by Wed, Dec 2 for estimated Christmas arrival", then a hero (pajama photo) with buttons CHRISTMAS SWEATERS / SHOP CHRISTMAS PAJAMAS. The hero photo is pajamas but the primary button is sweaters (the two products that actually sell). Page is 7,810 px long.
- "Standard shipping included", "Helpful sizing support" sit in a strip far below the fold (after the first product grid). No reviews, no seller line.
- Product cards show strike-through prices and -% badges (e.g. Nordic Yoke -21%, From $37.99, was $47.99).

### Collections (mobile)
- `/collections/christmas-sweaters`: order-by line, H1, six "Main collections" chips, Filter/Sort buttons, first product card at Y=412 (inside the first screen). 25 products, 9,460 px. Cards: badge, price, strike-through. Good.
- `/collections/mommy-and-me`: first card at Y=402, 116 products, 11,398 px, 35 cards rendered before any pagination marker found; sub-type chips (All, Sets, Pajamas, Dresses...). Long list, no pagination element: a first-time visitor must scroll a lot to compare. Search-visitors who land here are not asked their occasion.
- Desktop: filters Price/Color/Size/Type are shown as dropdowns; mobile has one Filter button. Size filter exists on desktop.

### Product page, Nordic Yoke (mobile, US)
- Main photo takes the full first screen (812 px). The H1 starts at Y=783, so on arrival the visitor sees only the photo and a slice of the title: no price, no delivery, no returns without scrolling about one screen.
- After one scroll: "From $37.99", "Estimated delivery: Tue, Dec 8 - Sat, Dec 12", "Standard shipping included", "30-day returns", "Order by Wed, Dec 2 for estimated Christmas arrival", then "Build your matching set" with "Buy 2, get the 3rd 20% off. No code needed."
- Builder: step 1 who (Child / Adult, Adult preselected), step 2 size buttons + size-guide link + colour, then quantity and the green button "ADD THIS PIECE TO BAG" at Y=1585 (about 2 screens down on mobile; at Y=1173 on a 900 px desktop screen, i.e. also below the fold). A sticky bottom bar exists on mobile ("From $37.99 / CHOOSE OPTIONS", turning into "$49.99 TOTAL $49.99 ADD THIS PIECE TO BAG" once size and colour are chosen): good.
- Validation is clear and inline ("Pick a size", "Pick a color"). Adult sizes S-4XL plus colour = 14 adult variants; child has 9 age sizes: 3 decisions per person (who, size, colour) plus a repeat for each family member.
- Price: headline "From $37.99" is the CHILD price. The adult S the visitor probably wants is $49.99 (shown only after choosing). The same product on the card shows "-21%, was $47.99"; on the PDP there is no strike-through and no "Save %" pill at all (the theme sets `pdp_show_compare_at_price = false` for matching-set products). Data: child 37.99 vs compare-at 47.99, adult 49.99 vs 59.99 (every size).
- Below the buy box: "Standard shipping included / Estimated delivery / order-by" repeated a second time (the same three facts appear twice within about 700 px), "Ships to United States - USD - Change", "Returns on eligible items: Request a return or exchange within 30 days of delivery", "Secure checkout: Encrypted payment. Available payment methods are shown at checkout." No payment icons, no seller name, no contact address, no reviews, no "who ships this".
- Details block: fabric "Thick, soft knit", chart (inches and cm both on this product), "Imported". Page height 5,302 px; "Compare family sizes" accordion; SIMILAR STYLES grid then "Complete the family look".
- The Christmas Reindeer PDP: same layout (add button Y=1475, page 6,162 px), adult sizes "S-M, M-L, L-XL, XL-2XL" with the explanation "S-M covers sizes S and M" deep in the text (a buyer must choose between two sizes in one button), and two different dates on one page: "Estimated delivery Dec 8 - Dec 12" at the top and "Estimate: order by Wed, Dec 2 to arrive by Wed, Dec 23. Not a guarantee." in the shipping box. Honest, but a hesitant buyer will wonder which is real. The Nordic PDP shows only the Dec 8-12 line.

### Cart drawer (mobile)
- Opens after Add. One piece: shows the item, "+ Add another family member's size", a "Complete the family" tile ("Only 1 piece in your bag. It's for one person. To match, add family members below.", buttons Kid $37.99 / Another adult $49.99), then a block "Buy 2, get the 3rd piece 20% off. Applied automatically in your cart." even though with one piece nothing is applied. Then Shipping STANDARD INCLUDED, delivery estimate, "Estimated total $49.99, Taxes calculated at checkout", "Check out", Shop/Amazon Pay/PayPal/G Pay buttons, trust line "Secure - Shipping included - 30-day returns".
- With two pieces the message becomes "Add 1 more piece and get 20% off. Applied automatically to your lowest-priced piece." Good and truthful. But on a 375x812 screen the item list shrinks to a window of about 1.3 items because the footer (message, shipping, total, buttons) takes most of the height; the second item is cut off in the screenshot.

### Cart page
- `/cart` with two pieces (child 5-6 gray $37.99, adult S cream $49.99): items (no link to the product, no way to change size), "Complete the family" chips, "Have a discount code?", message, Shipping STANDARD INCLUDED, delivery estimate, total $87.98, "Taxes calculated at checkout", "Shipping details" which opens the FULL shipping policy (about 4,000 characters, including "most orders ship in about 3 days", the 5 business day rule, Express wording), CHECK OUT button at Y=1166 (1.4 screens), "WE ACCEPT" icons, "Complete the look". Page 3,058 px.
- No ordered price reduction shown for the strike-through prices seen on the collection.

### Checkout (first step, mobile and desktop, US)
- Shopify standard one page: Order summary collapsed with "$87.98", Express checkout (wallet buttons loading), Contact (email/phone), Delivery with a full Country list (starts United States, Canada, Czechia, Italy, Belgium), Shipping method "Enter your shipping address to view available shipping methods", Submit. Nothing about delivery dates, returns, seller or support on the visible part; shipping cost and tax stay unknown until an address is entered (the visitor cannot confirm "shipping included" at this step). Not editable from the theme (checkout extensibility depends on plan; see section 3).

### Canada (desktop)
- Banner: "STANDARD SHIPPING INCLUDED TO CANADA". PDP price "From $55.00 CAD"; adult S $73.00 CAD (USD 49.99; about 1.46). On the PDP the suffix CAD appears only on the adult price and total, line items in the drawer show "$73.00" with no currency, the total "$73.00 CAD". Same delivery dates (Dec 8-12) as the US. "Taxes calculated at checkout" with no mention of import duties or GST/HST. Checkout shows Subtotal $73.00, Shipping "Enter shipping address", Total CAD.

### Czechia (Czech, desktop)
- Banner "STANDARDNÍ DOPRAVA V CENĚ (ČESKO)". Price "Od 989,00 CZK" child; adult S 1.301,00 Kč. Two different formats in the same cart ("1.301,00 Kč" per line, "1.301,00 CZK" total, and 1 301,00 Kč in checkout); "Daně se vypočítají při pokladně" (taxes at checkout). Same Dec 8-12 estimate as the US, fully translated page, size chart in cm. The trust line in the drawer reads "Zajistit" (a verb: "to secure/ensure") where it should be an adjective like "Zabezpečeno". The PDP carries a stray "BARVA Krémová Šedá" colour block before the builder in the text order (duplicate colour selector in the page source, to check visually).
- Prices for EU visitors: owner already knows the EU tax display question (`_OWNER.md`).

## 2. Ranked recommendations (by likely effect on orders)

1. Make the PDP price tell the truth about the buyer's piece and show the same saving the card promised.
   - Problem: card says "-21%, From $37.99, was $47.99"; PDP shows "From $37.99" (the child price) with no strike-through and no saving; the adult S costs $49.99 "regular price" while the data says compare-at $59.99. A Google visitor sees a discount on a collection, loses it on the PDP, and the headline price is not the price of the adult piece. This is the biggest information gap above the buy button.
   - Change: (a) show, above the builder, one line with both prices: "Child from $37.99 - Adult from $49.99 (each piece priced separately)". (b) The strike-through: only if the owner confirms the compare-at is a genuine previous price (see item 11); then show it consistently on card, PDP, drawer and cart, else remove it from the cards.
   - Effect: removes the "which price is real" doubt, anchors the family total, lowers bounces between card and page. Effort: small (theme Liquid in `sections/main-product.liquid`, price block). Who: theme change (CEO can release) for (a); owner decision for the compare-at question.

2. Bring price, delivery, shipping-included and returns into the first screen of the PDP on mobile (and the buy action closer).
   - Problem: the photo takes 812 px of an 812 px screen; the title starts at Y=783; price, delivery and returns appear only after one scroll; the real buy button is at Y=1585 on mobile and Y=1173 on a 900 px desktop. The sticky bar on mobile says only "CHOOSE OPTIONS" until the shopper picks (which needs two screens).
   - Change: do NOT shrink or crop the photo (owner rule: full width, natural ratio). Instead remove the "Back to Tops / View similar styles" row above it (about 40 px) and make the sticky bottom bar show from the first screen as "From $37.99 - Standard shipping included - Choose size", opening the builder on tap. That puts price and shipping on screen one without touching the photo.
   - Effect: a Google visitor decides to stay or leave in the first second; price + "included shipping" + dates visible without scrolling raises the share who reach the builder. Effort: medium. Who: theme change (CEO can release), after checking the mobile-photo rule.

3. Reduce decisions in the builder for the first piece.
   - Problem: three choices before the first add (who, size, colour), then the drawer asks again for each family member; Christmas Reindeer has combined sizes "S-M / M-L" with the explanation buried in the text; size help is a link, plus a ruler icon inside the size row that is not labelled.
   - Change: (a) preselect nothing wrong, but when the product has one colour (Christmas Reindeer red) hide the colour step (already hidden there, keep); (b) next to the first size row add one line: "Not sure? Choose by height: chest, sleeve and length in inches and cm are in the size guide." (c) For combined sizes add under the buttons "S-M fits sizes S and M; choose the larger if between sizes" ONLY if the supplier chart supports that rule (otherwise: "S-M covers sizes S and M. Compare the chart below."). (d) Label the ruler icon "Size chart".
   - Effect: fewer abandoned builders on mobile; fewer wrong sizes (returns). Effort: small to medium. Who: theme change; copy (c) needs product data check.

4. Show who the seller is and how to reach them next to the buy box and in the cart.
   - Problem: PDP, drawer and cart show no store name, no support address, no operator; "FKG Trading LLC", "info@dresslikemommy.com" and the "We usually reply within 1 business day" line exist only in the policies. The store has one review, so trust must come from visible, checkable facts.
   - Change: add one line under "Secure checkout" in the shipping box on PDP, drawer and cart: "Sold by Dress Like Mommy (FKG Trading LLC), an online-only store. Questions before you order? info@dresslikemommy.com" (the policy already says we usually reply within 1 business day: add only if the owner keeps that line). No phone number, no address, until the owner provides one.
   - Effect: moderate; first-time buyers from Google look for a real contact. Effort: small. Who: theme change; the exact line needs owner OK because it names the legal entity and promises a reply.

5. Explain the dates once, plainly, and reconcile the two dates on the same page.
   - Problem: Nordic shows "Estimated delivery Dec 8-12" + "Order by Dec 2"; Christmas Reindeer also shows "arrive by Dec 23. Not a guarantee". The shopper cannot tell whether order-by Dec 2 means Dec 8-12 or Dec 23. The delivery window itself comes from a 12-16 day estimate; the policy says dispatch within 5 business days and the Dec 23 case is the worst case.
   - Change: one block: "Estimated delivery Dec 8-12. Christmas: order by Wed, Dec 2 and the estimate is before Dec 24 (estimate, not a guarantee)." Show it once on the PDP (remove the duplicate under the buy box) and the same words in drawer and cart. Remove the line after Dec 2 (already done by the theme).
   - Effect: lowers doubt for the biggest seasonal group of buyers; removes a duplicate. Effort: small. Who: theme change (CEO can release), wording agreed with the dates decision of 11-26.

6. Say what is included in one set, per person, with the real price total.
   - Problem: the buyer cannot see what a family of four costs. The "Buy 2, get the 3rd 20% off" is shown, but nobody can see the total: Nordic family of four is about $177 (child 37.99 x2 + adult 49.99 x2, less 20% on the lowest piece) and the first number they see is $37.99. The owner decided no computed bundle totals on the PDP (memory: promo copy simple), so do not print totals.
   - Change: in the "Complete the family" tile in the cart/drawer, show the running total only (the cart already does); on the PDP just keep "Each piece is sold separately; the sweater only, trousers not included" in the first block (it is now at the bottom of the details).
   - Effect: avoids "I thought the family set was one price" surprises. Effort: small. Who: theme change (move one existing sentence up).

7. Drawer and cart on mobile: show the item list and the total in one screen; stop saying "Applied automatically" with one piece.
   - Problem: with two pieces the drawer shows 1.3 items and the second is cut off; the check-out button is reachable, but the visitor cannot confirm what is in the bag; with one piece the line "Buy 2, get the 3rd piece 20% off - Applied automatically in your cart" reads as applied while nothing is.
   - Change: with one piece show "Add one more piece to see the family discount"? NO: the rule is 3rd piece 20% off: with 1 piece: "Buy 2, get the 3rd piece 20% off. Add pieces for your family." and move "Complete the family" below the totals, collapse it to one line. Add a link on each item to its product.
   - Effect: fewer drawer exits, fewer wrong sizes in the bag. Effort: medium. Who: theme change (CEO can release).

8. Payment methods: show them where the doubt happens.
   - Problem: PDP says "Available payment methods are shown at checkout" (no icons); the cart shows icons only after the CHECK OUT button (WE ACCEPT, loaded below); the first checkout step shows only a wallet row loading.
   - Change: the drawer already shows Shop/Amazon Pay/PayPal/G Pay; add the card icons (the shop's enabled methods, read from `shop.enabled_payment_types`) under the PDP "Secure checkout" text. No claim about a specific security product.
   - Effect: small-moderate. Effort: small. Who: theme change.

9. Canada and Czechia: currency and tax wording.
   - Problem: Canadian line prices show "$73.00" with CAD only in the total; no word on duties or GST/HST (the cart only says "Taxes calculated at checkout"); Czech shows two number formats ("1.301,00 Kč" and "1.301,00 CZK" and "1 301,00 Kč") and the drawer trust label "Zajistit" (a verb).
   - Change: show "CAD" on every price on Canadian pages (or "CA$"); in the shipping box for Canada and EU/CZ add "Taxes and import fees, if any, are shown at checkout" ONLY after the owner confirms what the Shopify tax settings actually do for these countries (open owner item: EU tax display). Czech: unify format to "1 301 Kč" and replace "Zajistit" with "Zabezpečeno".
   - Effect: Canada 9 and Czechia 6 orders in 60 days; small absolute, protective for the next markets. Effort: small. Who: theme change for formats and the Czech word; owner decision/step for the tax sentence.

10. Collections: stop making the visitor scroll 116 products to find a match.
   - Problem: `/collections/mommy-and-me` is 11,398 px with 116 products and no pagination on mobile; the top shows a sub-type chip row but no occasion or "who is it for" entry; the Christmas collection works (25 products, first card inside the first screen).
   - Change: a "Shop by who" chip row on mobile at the top of the biggest collections (Mommy & Daughter, Family of 4, Dad & Son, Baby), plus the existing Type chips; cap the first load at 24 cards with a "Show more" button.
   - Effect: lower exit on the biggest landing pages (Italy mommy-and-me has 123 sessions per 14d with zero checkouts). Effort: medium. Who: theme change; the groups need product data tags (`custom.subcategory`).

11. Compare-at prices need a documented real previous price (not a conversion change by itself, but a risk to every number above).
   - Problem: the ceo notes record compare-at set "price + $10" on older Mommy & Me sweaters and re-set several times; one product carries a compare-at of $37.82 (Santa and Friends), an odd value. Strike-through prices that are not genuine former prices can read as an unsupported promotion claim, and can be challenged by Google/Merchant or a regulator.
   - Change: owner to confirm per product that the compare-at was the price actually charged recently; otherwise lower the strike-through or remove it everywhere. Do not add new strike-throughs.
   - Effect: protects the store; decides whether recommendation 1(b) can ship. Effort: owner decision. Who: owner decision/step (prices).

12. Reviews: keep the honest gap, but fix the request loop.
   - Problem: one real review in total; Judge.me requests are not going out (already recorded as an owner step). The PDP correctly shows nothing; the visitor has no social proof.
   - Change: none on the site until real reviews exist. After that turn on card stars (`show_rating`). Do not seed or import reviews, and do not write "loved by families" or similar.
   - Effect: long-term; this is the largest trust gap but not something a theme change can close. Effort: owner (app login + customer messaging). Who: owner decision/step.

## 3. What I could not check
- Whether the 3rd-piece 20% discount applies correctly at 3 pieces (I added only 2 pieces; a 3rd would also show whether "Applied automatically" appears right).
- The checkout steps after the address: actual shipping line, tax/duty lines for Canada and Czechia, payment method list, express upgrade price, total. I typed no email, address or card.
- Real page speed on a phone (only the PageSpeed file of today was used: LCP about 5 s on the PDPs, CLS 0.10); the browser pane's size is fixed and its screenshots are small, so layout judgments on jumpiness rely on measured positions, not on video.
- Czech and Canadian pages at 375 px (I walked them at desktop width as the pane allows one size per leg).
- The "BARVA Krémová Šedá" block in the Czech PDP text (maybe a hidden duplicate; not seen visually).
- Whether the footer "GET 10% OFF YOUR FIRST ORDER" is a working offer and what it gives (not submitted; if it works it is a conversion lever to show once, near the cart, and if it does not it is an unsupported promotion).
- Whether the mobile-photo owner rule (full width, natural ratio, no crop or shrink) allows recommendation 2 as worded: the safe version moves text up and leaves the photo as is.
- Which compare-at prices are genuine former prices (needs the owner).
- Google-style entry: I loaded the pages directly, not from a search result, so cookie banners or consent layers by region were not seen (none appeared).
