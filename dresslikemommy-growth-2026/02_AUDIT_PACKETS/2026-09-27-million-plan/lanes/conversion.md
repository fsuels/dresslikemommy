# Conversion Lane: Million Plan (2026-09-27)

Status: `LOCAL_AUDIT_ONLY`. Nothing live was changed: no Shopify or theme write, no commit, no cart add (adding to cart would fire ATC pixels into the paid-growth data), and no checkout. Evidence comes from:
- public storefront reads made on 2026-09-27 between 00:20 and 00:45 EDT (curl, plus the built-in browser at 375×812, US/USD/English);
- theme files at `HEAD f000ab6`;
- the existing packets cited inline.

Evidence labels:
- `LIVE_VERIFIED`: read from the public storefront in this session.
- `REPO_KNOWN`: read from repo files or dated packets. These are not re-read live.
- `INFERENCE`: reasoning or a prediction that has not been measured.

## 0. Baseline this lane optimizes against (REPO_KNOWN)

| Fact | Value | Source |
|---|---|---|
| Shopify 30-day CVR | 0.21%, polluted by bot days. Exclude 2026-08-08, 08-09, 08-24, 09-16 and 09-25 from numerator and denominator. The adjusted rate is `UNKNOWN` | `ops/marketing/current_marketing_state.md` (DEC-20260926-SPIKE-DAY-EXCLUSIONS) |
| Mobile funnel, 90 days | 5,756 sessions → 362 cart → 101 checkout → 28 orders. Cart→checkout is 27.9% | `2026-09-24-cart-to-checkout/README.md` |
| Google search, 30 days | 1,413 sessions → 69 cart → 11 checkout → 4 orders. **58 of 69 carts never reach checkout** | same packet, §5 |
| Non-US checkout completion | 20% (14/70), vs 45% for the US. No local EU payment methods | same packet, plus `2026-09-26-europe-payment-delivery-review/README.md` |
| Basket economics | Landed cost is 65% of revenue on 1-item orders ($24), 52% on 2 items ($46), 48% on 3, 45% on 4, and 43% on 5+ ($157). 48% of orders have 2 pieces | `2026-09-27-buckydrop-profit-study/README.md` |
| Reprice | 55 products / 980 variants raised on 2026-09-27. Compare-at = new price + $10 wherever a compare-at existed | `ops/AGENT_WORKLOG.md` anchor `2026-09-27-price-floor-reprice-55-products` |

The profit study shows that a larger basket is the profit lever. Every fix below is judged on two things: sessions → orders, and pieces per order.

---

## 1. Findings

### 1.1 PDP above the fold (mobile 375×812)

| # | Finding | Label | Evidence |
|---|---|---|---|
| P1 | **Only the photo is above the fold.** Media runs from y=102 to 773 (671 px tall). The H1 sits at y=783 and the price at y=849, below the 812 px fold. The owner rule "mobile photo full size, no crop" (memory) explains this. So nothing identifies price, delivery or trust until the shopper scrolls. | LIVE_VERIFIED | JS layout read on `/products/snowflake-reindeer-family-matching-onesie-pajamas` and `/products/santa-hat-reindeer-family-matching-sweaters` |
| P2 | The price shows as a range, `$33.99 USD - $36.99 USD` (`price--range`, `data-price-on-sale="false"`). A deep link (`?variant=47170208039009`) correctly preselects Adult · M and shows `$35.99 USD`. | LIVE_VERIFIED | price markup; variant deep-link test |
| P3 | **The PDP and the collection cards disagree on "sale".** Home and collection cards show `Sale -13%` / `-14%`. The same product's PDP shows only `Regular price`, with no compare-at, even when a single variant with a compare-at (e.g. $41.99 vs $35.99) is selected. 140 of 261 live products carry a compare-at. After today's reprice the compare-at is formula-set (price + $10), so it may not be a price the item ever sold at. | LIVE_VERIFIED (display) / INFERENCE (reference-price risk) | home HTML cards; PDP price block; `products.json` pages 1–2 |
| P4 | **Delivery promise is 750–900 px below the fold.** `Estimated delivery: Fri, Oct 9 – Tue, Oct 13` sits at y≈1561–1683. "Standard shipping included" is just above it, and "Returns" / "Secure checkout" are below it. The copy is accurate and localized. It is just late. | LIVE_VERIFIED | layout read |
| P5 | **Zero reviews.** 35 of 35 sampled live PDPs return `data-number-of-reviews='0'` (5 more were rate-limited). Judge.me is installed and loads `loader.js` plus a 30 KB `jdgmSettings` block. `hide_badge_preview_if_no_reviews: true` hides the stars, so **no stars render anywhere**. `snippets/pdp-review-social-proof.liquid` (the "New arrival" pill fallback) does not render in the main product info. | LIVE_VERIFIED | in-browser fetch of every 6th product; Judge.me settings JSON |
| P6 | No express-pay button (Shop Pay / Apple Pay / PayPal) on the PDP. There is no `shopify-payment-button` in the HTML, even though `templates/product.json` has `show_dynamic_checkout: true`. The matching-set builder replaces the Dawn buy form. | LIVE_VERIFIED / REPO_KNOWN | HTML grep; matches 09-24 packet finding 1 |
| P7 | Christmas "order-by" line: `assets/dlm-holiday-order-by.js` has `LEAD_DAYS = 60`, so the "Order by Tue, Dec 8 for estimated Christmas arrival" line stays hidden until about Oct 9. Christmas-tagged PDPs show nothing about Christmas timing today. | REPO_KNOWN + LIVE_VERIFIED (absent on the Santa Hat PDP) | `assets/dlm-holiday-order-by.js` lines 17–28 |

### 1.2 Size-chart discoverability

| # | Finding | Label |
|---|---|---|
| S1 | In the mobile builder, the only size-guide entry is a **44 px icon-only ruler button** (`.product-matching-set__fit-icon`, aria-label "Find Adult's fit"), next to the size pills. There is no visible "Size chart" text anywhere in the purchase area. The copy map has the strings (`single_size_guide_label` "Size guide & fit", `compare_size_guide_label`), but they are not shown on mobile. | LIVE_VERIFIED |
| S2 | The product description says "see the size chart for measurements", but no size table is visible on the rendered mobile PDP (`main table` count = 0). The per-pill measurement tooltips (cm/in) exist, but only after a size is tapped. | LIVE_VERIFIED |

### 1.3 Mobile weight and speed

| # | Finding | Label |
|---|---|---|
| W1 | PDP HTML is **1.12 MB raw / ~196 KB brotli**. Inline JS is 481 KB. The largest single block is `window.DLM_PRODUCT_PAGE_COPY`, **177.5 KB**, holding all ~35 locales on every PDP. Every consumer (`assets/global.js` `getProductPageCopy`, `assets/product-description.js`, `sections/main-product.liquid` l.1915/2622) picks only the current locale or its root. | LIVE_VERIFIED + REPO_KNOWN |
| W2 | 28 theme JS files: 585 KB raw / 147 KB gzip, measured on repo copies of the live asset list. `product-desktop-ux-20260513-ruler-sync.js` alone is 203 KB. Third-party scripts come on top: Shopify WPM (87 KB inline), Judge.me, Facebook `fbevents.js` (415 KB decoded). | LIVE_VERIFIED (asset list) / REPO_KNOWN (sizes) |
| W3 | 57 unique theme CSS files: 570 KB raw / 119 KB gzip. **27 render-blocking stylesheets in `<head>`** and 49 non-deferred stylesheet links in the body. There are duplicate tags: `component-loading-spinner.css` ×6, `component-price.css` ×5, `component-card.css` ×4, plus several `section-footer` / `component-list-*` duplicates. | LIVE_VERIFIED |
| W4 | Homepage HTML is 764 KB raw / 109 KB gzip; theme JS 42 KB gzip; theme CSS 79 KB gzip. | LIVE_VERIFIED |
| W5 | A PageSpeed Insights run was **BLOCKED** by the anonymous API daily quota. The last recorded mobile trace failed on performance with CLS 0.058 at 390 px (worklog, 2026-09-15). | BLOCKED / REPO_KNOWN |

### 1.4 Homepage seasonal message

| # | Finding | Label |
|---|---|---|
| H1 | The hero is "THE HALLOWEEN & WINTER EDIT / Spooky nights. Snowy mornings. Matching families.", with CTAs Halloween Pajamas / Cozy Sweaters / Family Matching Outfits. **Christmas pajamas are not named in the hero or the announcement bar.** "Shop by Occasion" does lead with Christmas → `matching-family-christmas-outfits`. | LIVE_VERIFIED |
| H2 | `christmas-pajamas` has **1 live product** (Snowflake Reindeer onesie). `matching-family-christmas-outfits` has 14 (13 sweaters + 1 onesie). The 11 Christmas 2026 pajama drafts are still pending. | LIVE_VERIFIED (counts) / REPO_KNOWN (drafts) |
| H3 | The announcement bar rotates `STANDARD SHIPPING INCLUDED TO United States | EXPRESS OPTIONS AT CHECKOUT | SECURE CHECKOUT`. Two of the three slots are low-value. There is no returns line, no Christmas timing and no "free". | LIVE_VERIFIED |
| H4 | Halloween's last estimated order date is **Oct 15** (12–16 day window). After that date the hero's lead CTA sells a product that can no longer arrive in time. `snippets/hero-seasonal-copy.liquid` has only a static `halloween_winter` edition and no date switch. | REPO_KNOWN + INFERENCE |

### 1.5 Collection sort and filters

| # | Finding | Label |
|---|---|---|
| C1 | Filters are Price, Color, Size and `custom.subcategory`. `mommy-and-me` exposes **144 Size values**, e.g. "Mother M", "Child 6-7 Years", "Baby 9-12 Months", each listed separately. There is no "Who is it for" filter (Mom / Dad / Girl / Boy / Baby). | LIVE_VERIFIED |
| C2 | Sort options are the standard Dawn set. `mommy-and-me` defaults to Featured (manual). `pajamas` leads with 5 Halloween sets, then the Christmas onesie. `new-arrivals` leads with the Christmas onesie. This is reasonable for now, but it needs to flip after Oct 15 (see H4). | LIVE_VERIFIED |
| C3 | `/collections/family-christmas-pajamas` returns **404**. The live handle is `christmas-pajamas`. Any ad or email that uses the intuitive handle breaks. | LIVE_VERIFIED |

### 1.6 Cart and upsell

| # | Finding | Label |
|---|---|---|
| U1 | **`dlm-family-builder` exists and is live** (`snippets/dlm-family-builder.liquid`, `assets/dlm-family-builder.js` 962 lines, `.css`, with node tests in `ops/tests/test_family_builder.mjs`; commit `5847163`). On Mother · M it shows "+ Add another family member". After a tap, the list shows `Mother · M × 1 $36.99` and the CTA becomes `ADD ALL TO BAG (1) · $36.99 USD` (the sticky bar mirrors it). It uses real variant prices only and sends one `/cart/add.js` request with `items[]` plus the drawer sections. | LIVE_VERIFIED (UI; no add submitted) / REPO_KNOWN |
| U2 | It is **PDP-only and same-product-only**. When a shopper adds just one piece with the normal "ADD THIS PIECE TO BAG" button, the cart does nothing to recover the other family members for that design. | REPO_KNOWN |
| U3 | The cart drawer's non-empty upsell, "You may also like" (`snippets/cart-drawer.liquid` l.717–761), shows **other products** from the first line's first collections. It sits **below the checkout button and trust strip**, in the fixed footer. The cart page's "Complete the look" (`sections/main-cart-footer.liquid` l.217–260) does the same and **does not skip unavailable products**. | REPO_KNOWN |
| U4 | Empty-cart picks come from New Arrivals (3 in the drawer, 4 on `/cart`) plus Recently Viewed. | LIVE_VERIFIED |

### 1.7 Free-shipping messaging

| # | Finding | Label |
|---|---|---|
| F1 | Every storefront surface says **"Standard shipping included"** (announcement, PDP, drawer `Shipping: Standard included`, trust strip). Checkout says **"Free Standard Shipping — FREE"**. The delivery profile charges $0 standard in both zones. The storefront wording was chosen on 2026-05-09 after a Denmark confusion, with the owner stating that shipping is included in prices. | LIVE_VERIFIED (storefront) / REPO_KNOWN (checkout, profile, decision) |
| F2 | There is no free-shipping threshold. Every order ships free, so a "spend $X for free shipping" bar would be dishonest. The honest basket lever is per-piece value, not a threshold. | REPO_KNOWN |

### 1.8 Checkout friction visible from the storefront

| # | Finding | Label |
|---|---|---|
| K1 | There are no wallets before checkout: none in the drawer, none on the PDP. Wallets appear only on `/cart`, and the drawer is the default cart. The 09-24 packet measured the layout conflict: adding the 248 px wallet stack shrinks the item list to 12 px, because "You may also like" (191 px) sits in the fixed footer. | REPO_KNOWN |
| K2 | There is no local EU payment method (iDEAL, Klarna, Bancontact, BLIK, MobilePay). Non-US checkout completion is 20% vs 45% for the US. | REPO_KNOWN |
| K3 | Abandoned-checkout email status is **UNKNOWN / BLOCKED**. Indirect data: 29 abandoned checkouts with contact info since 2026-06-26, and 0 email-referred orders in 365 days. | REPO_KNOWN |
| K4 | The pre-ticked marketing consent was fixed on 2026-09-26 (region set to Shopify-recommended / US). | REPO_KNOWN (`ops/PROBLEM_TRACKER.md` l.191) |
| K5 | The drawer's checkout-reassurance block (`cart-drawer.liquid` l.693) is still `hidden`. The estimate now shows under the shipping line instead (`Estimated delivery: 12-16 days` is visible in the empty-drawer markup). | LIVE_VERIFIED |
| K6 | Currency code on every price (`$33.99 USD`) adds noise for US shoppers. `currency_code_enabled: true` is set in `config/settings_data.json`. | LIVE_VERIFIED / REPO_KNOWN |

---

## 2. Top 15 fixes, ranked by expected revenue impact

"Owner yes" means the change touches money, customer messaging, a claims decision or an Admin setting that needs explicit approval. Theme-code items ship through the normal `main` → Shopify sync after review, with desktop and mobile verification per `docs/agent-loops/ui-browser-verification-loop.md`. Impact estimates are `INFERENCE` unless marked.

| Rank | Fix | Why it moves revenue | Exact files / settings | Risk |
|---:|---|---|---|---|
| 1 | **Activate the 11 Christmas 2026 pajama designs and make Christmas pajamas the Q4 lead.** Add a `christmas` edition to the hero, lead with pajamas, and switch from `halloween_winter` automatically on Oct 16 (the day after the Halloween cutoff). Point the lead CTA at `/collections/christmas-pajamas`. Add a 301 redirect from `family-christmas-pajamas` to `christmas-pajamas`. | Family pajamas are the category most likely to produce 3–5 piece baskets (43–48% landed). Today there is 1 live SKU for the season's main search intent. | Product status in Admin (listing workflow, owner yes). `snippets/hero-seasonal-copy.liquid` (new `christmas` edition, all languages). `sections/hero-banner.liquid` (date-based edition pick via `'now' \| date: '%Y%m%d'`, which is cached, so it needs a daily re-render or a JS swap). `templates/index.json` hero CTA links. Admin → Navigation → URL redirects. | Medium. Images, size charts and translations must be ready per the canonical listing workflow. Liquid `now` is cache-bound, so verify on the live route. `templates/index.json` has uncommitted peer edits, so coordinate before touching it. |
| 2 | **"Complete the family" in the cart drawer and `/cart`** (spec in §3). Same design, missing family roles, real prices, one-tap add, placed **inside the scrolling item list**. | Moves 1–2 piece baskets toward 3–4 pieces. A 1→2 piece step cuts landed cost from 65% to 52%, and 2→4 cuts it from 52% to 45%. It also frees the fixed footer for fix 5. | New `snippets/dlm-complete-family.liquid`. New `assets/dlm-complete-family.js` built on `assets/dlm-family-builder.js` exports. `snippets/cart-drawer.liquid` (render inside `#CartDrawer-CartItems`, remove l.717–761). `sections/main-cart-items.liquid`. `sections/main-cart-footer.liquid` (remove l.217–260). `assets/dlm-family-builder.css`. `ops/tests/test_family_builder.mjs`. | Low–medium. Drawer re-render must keep lines visible at 375×812. Must never show fake scarcity or unreal discounts. |
| 3 | **Start collecting real reviews.** Turn on Judge.me review requests for fulfilled orders, including the past-order import (608 orders in the profit-study window). Enable photo-review requests. Once reviews exist, show real stars under the H1 and on cards (`hide_badge_preview_if_no_reviews` stays true until then). Any incentive must be disclosed, must not depend on a positive rating, and must use Judge.me's transparency badge. | For a 12–16 day, unknown-brand dropship store, zero social proof is the biggest trust gap. Google Seller Ratings and product ratings in Shopping also need a review feed. | Judge.me app → Requests (past orders, timing about 5 days after delivery), Widgets → star badge. Theme: `snippets/pdp-review-social-proof.liquid` is already written; render it under `product__title` in `sections/main-product.liquid` when the count is above 0. | Low (owner yes, because it emails customers). Never seed, import or invent reviews. |
| 4 | **Honest one-line value strip under the price on the mobile PDP**, as the first thing after the photo: `From $32.99 · Arrives Oct 9–13 · Free standard shipping · 30-day returns`. Use the existing `dlm-delivery-dates.js` window and the existing strings. Also make the sticky bar visible from the first scroll pixel with price plus arrival date. | Price, delivery and returns are the questions Google-search mobile shoppers answer before adding to cart. Today they sit 750–900 px down. Keeps the full-size photo rule. | `sections/main-product.liquid` (block order: title → price → new strip → builder). `snippets/pdp-purchase-confidence.liquid` (reuse `[data-dlm-delivery-window]`). `assets/dlm-delivery-dates.js` (also target the new strip). Sticky script in `sections/main-product.liquid` (`StickyMobileATC`). `snippets/price.liquid` ("From" for ranges). | Low. The strip must use the same computed window. No guarantee wording ("estimated"). |
| 5 | **Express wallets in the cart drawer**, after fix 2 moves the upsell out of the fixed footer. Add `{{ content_for_additional_checkout_buttons }}` under Check out. | 58 of 69 Google-search carts never reach checkout, and mobile cart→checkout is 27.9%. One-tap Shop Pay / Apple Pay / PayPal is the standard remedy. The 09-24 build already passed theme check. | `snippets/cart-drawer.liquid` (checkout CTA block l.676–700). `assets/component-cart-drawer.css` (compact wallet row, max 2 visible). Theme setting: keep `cart_type: drawer`. | Low–medium. Layout must keep at least 1 full cart line visible at 375×812. Re-measure as in the 09-24 packet. |
| 6 | **Visible "Size chart" text link** next to the size row in the builder, one per role ("Size chart · Mother"), opening the existing full chart. Also render the chart inline in a collapsible "Size chart" block. | Size doubt is the top apparel hesitation, and for a family set it applies to every person. Better fit also reduces paid-return friction. | `assets/product-desktop-ux-20260513-ruler-sync.js` (builder markup near `.product-matching-set__fit-icon`). `snippets/product-desktop-ux.liquid`. `assets/component-product-desktop-ux-ruler-sync.css`. Existing copy-map keys `single_size_guide_label` / `compare_size_guide_label`. | Low. Must keep the localized size-chart workflow and per-product chart accuracy. |
| 7 | **Show the Christmas order-by date now**, not from Oct 9. Use a per-holiday lead: Christmas 90 days, Halloween 60. Add the same computed line to the cart drawer shipping block and the Christmas hero subheading. | Gift buyers plan early. A true, computed "Order by Dec 8 for estimated Christmas arrival" is honest urgency backed by a real carrier window. | `assets/dlm-holiday-order-by.js` (`LEAD_DAYS` → per-holiday map; add a drawer target). `snippets/cart-drawer.liquid` (shipping note l.630). Node test for `orderByFor`. | Low. Estimate language only. Keep the Sunday roll and hide the line after the cutoff (already coded). |
| 8 | **Say "Free standard shipping"** where checkout already shows FREE (every current zone): announcement slot 1, PDP strip, drawer `Shipping: Free`, trust strip. Keep "Express options at checkout" as secondary text. Drop the "SECURE CHECKOUT" slot in favour of "30-day returns on eligible items" and, from fix 7, the Christmas order-by date. | "Free shipping" is the most-recognized purchase trigger. The current "included" wording reads as a caveat. | `locales/*.json` keys `sections.cart.shipping_free`, `sections.cart.trust.free_ship`, `sections.announcements.default_promo`. `snippets/pdp-purchase-confidence.liquid`. `snippets/product-page-copy-map.liquid` (regenerate with `ops/scripts/build_product_page_copy_map.py`). `sections/header-group.json`. | **Owner yes.** This reverses the 2026-05-09 wording decision. It must stay true per country: gate on `localization.country` having a $0 standard rate. It must match Merchant Center shipping settings. `locales/*.json` currently have uncommitted peer edits, so coordinate. |
| 9 | **Cut PDP weight:** emit only the current locale plus `en` from `DLM_PRODUCT_PAGE_COPY`, dedupe repeated `stylesheet_tag`s, and defer non-critical component CSS (`media="print" onload`). | About 170 KB less inline JS to parse on every PDP, and fewer render-blocking requests on mid-range phones. Paid traffic lands on PDPs. | `sections/main-product.liquid` l.940. `snippets/product-page-copy-map.liquid` / `ops/scripts/build_product_page_copy_map.py` (key by locale and let Liquid pick the right key). The Dawn sections that each emit `component-card/price/loading-spinner` (search `stylesheet_tag` in `sections/*.liquid` and `snippets/card-product.liquid`). | Medium. Every copy-map consumer needs regression checks in 3+ locales. CSS deferral can cause CLS, so re-measure CLS at 390 px. |
| 10 | **Fix the "Sale" mismatch and review the compare-at policy.** Either show compare-at consistently on the PDP for the selected variant, or remove sale badges. Keep compare-at only where it was a real recent selling price. | The mismatch looks like bait at the moment of decision. A formula compare-at (price + $10) is a reference-price legal risk: the FTC Guides Against Deceptive Pricing and state laws in the US, and EU Omnibus (EU already shows none). | Admin pricing (owner yes). `snippets/price.liquid`, `snippets/card-product.liquid` (badge logic). `sections/main-product.liquid` (`data-pdp-sale-percent`). | **Owner yes.** Removing badges may lower CTR. Compliance and trust win. The rollback file `reprice_before.json` exists. |
| 11 | **"Who is it for" filter** (Mom, Dad, Girl, Boy, Baby, Adult) plus a grouped size filter. Default Christmas collections to pajamas-first manual or best-selling order once the new designs are live. | Shoppers filter by family member first. 144 raw size chips are unusable on mobile. | Product metafield `custom.family_roles` (list, derived from the Size option prefix with a script). Search & Discovery app → Filters (add metafield filter, hide raw Size or keep it collapsed). `snippets/facets.liquid` only if label mapping is needed. | Low. Metafield backfill needs a dry run and readback (Admin write, owner yes). |
| 12 | **Rebuild the PDP builder flow around the family.** Before any selection, show a one-line prompt "Shopping for the family? Pick each person, then add all at once." After a single-piece add, auto-select the next missing role (`nextRoleKey` already exists). | Makes the existing family list the default path instead of a hidden option, which grows pieces per order. | `assets/dlm-family-builder.js` (`STRINGS` + `sync()`). `assets/dlm-family-builder.css`. `ops/tests/test_family_builder.mjs`. | Low. Must not change single-piece behaviour for shoppers who want one piece. |
| 13 | **EU local payment methods** (iDEAL, Klarna, Bancontact, BLIK, MobilePay) in Shopify Payments. | Non-US checkout completion is 20% vs 45% for the US, and Italy had 8 checkouts → 0. EU is a large share of Google/Microsoft paid traffic. | Admin → Settings → Payments (owner yes). Next action `OWNER_ENABLE_EU_LOCAL_PAYMENT_METHODS` already exists. | Low technical risk. Fees and settlement terms are an owner money decision. |
| 14 | **Turn on abandoned-checkout and abandoned-cart automations** (Shopify Messaging) with honest copy, as drafted in the email lane (`lanes/email.md`). | 29+ contactable abandoned checkouts and 0 email-referred orders in 365 days. This is the cheapest recovery lever. | Admin → Marketing → Automations (owner yes, customer messaging). | Low. Consent rules per the email lane. No fake urgency. |
| 15 | **Price-display cleanup:** turn off the currency code for single-currency markets (show `$32.99`), show "From $32.99" on range prices, and fix the 5 products still under $19.99 (e.g. `matching-mom-child-one-shoulder-swimsuit` $17.99) that the reprice plan did not cover. | Less visual noise at the decision point. The sub-$20 items lose money on a 2-piece basket (profit study). | Theme settings → Currency format (`currency_code_enabled`). `snippets/price.liquid`. Admin pricing for the 5 handles (owner yes). | Low. The currency code may need to stay on for multi-currency clarity in EU markets. Test per market. |

---

## 3. Spec: "Complete the family" (cart drawer, `/cart`, and PDP handoff)

### 3.1 Goal and rules

- **Goal:** raise pieces per order on the same design. Success means: the share of 1-piece orders goes down, the share of 3+ piece orders goes up, AOV goes up, and cart→checkout rate does not go down. Measure over dates that exclude the spike days.
- **Build on** `assets/dlm-family-builder.js`. Reuse its exported pure helpers: `mergeLine`, `buildItems`, `buildRequestBody`, `formatMoney`, `parseMoneyFormat`, `cartAddJsUrl`, `translate`/`STRINGS`. Reuse its drawer re-render pattern (`drawer.getSectionsToRender()` → `/cart/add.js` with `sections` → `drawer.renderContents(parsed)` → `publish('cartUpdate')`). Reuse its "no markup edits to other components" discipline. ES5, no build step, vanilla, Dawn-compatible.
- **Honesty rules** (fail closed):
  - Real variant prices only.
  - No "bundle price", "save X%" or "customers also bought" unless a real Shopify automatic discount exists and the cart shows it.
  - No stock counts, "selling fast" or timers.
  - Always state "each piece sold separately".
  - Delivery wording is always "estimated".

### 3.2 Data (server-side, Liquid)

New `snippets/dlm-complete-family.liquid`, rendered once inside `#CartDrawer-CartItems` (after the line items) and once in `sections/main-cart-items.liquid`. Because it sits inside the sections Dawn already re-renders, it refreshes on every add, remove or quantity change with no extra fetch.

For up to 2 distinct cart products, ordered by line price descending:
1. Find the size option index: the option whose name downcased is `size`. If there is none, skip the product.
2. `role` of a variant = the first word of its size value, lowercased (`Mother S` → `mother`, `Child 6-7 Years` → `child`, `Adult M` → `adult`, `Baby 3-6 Months` → `baby`). Accept only the known keys `mother, father, girl, boy, child, baby, adult`. The same keys and order are used by `ROLE_DEFINITIONS` in `assets/product-desktop-ux-20260513-ruler-sync.js` l.803.
3. `rolesInCart` = roles of this product's variants in the cart.
4. Candidate variants = `product.variants` where `available`, `role ∉ rolesInCart`, and every non-size option equals the cart line's value for that option (same Color, so the look matches). For products with a `Type` option (40 live products), accept a variant when its Type differs from the cart line's only if its role differs. Otherwise skip the product. Version 1 may skip Type products entirely and show a link "Add another family member →" to the PDP.
5. If there are no candidate roles, render nothing for that product.

The snippet emits one `<script type="application/json" data-dlm-complete-family>` containing `{currency, products:[{id, title, url, image(width 160), color, rolesInCart, roles:[{key, label, variants:[{id, size, price, price_text}]}]}]}`. It also emits server-rendered fallback markup: role chips as links to `product.url?variant=<first candidate>`, so the block still works without JS. Role labels come from locale keys `products.product.roles.<key>`. Add them if they are missing, with the existing `ROLE_DEFINITIONS.labels` as the source for es/fr/ar.

Size: at most 2 products × about 60 variants, roughly 6–8 KB of JSON. Only the cart section renders it.

### 3.3 UI (drawer at 375 px; `/cart` uses the same component in a wider grid)

```
┌ Complete the family ─────────────────────────────┐
│ [thumb] Snowflake Reindeer Family Pajamas         │
│ You have: Mother · Add the matching pieces:       │
│ ( + Father ) ( + Child ) ( + Baby )               │
│  ↓ tap "+ Child"                                  │
│ Child size [ 6 Years ▾ ]   $33.99   [ Add ]       │
│ Each piece is sold separately.                    │
└───────────────────────────────────────────────────┘
```

- Chips are real `<button>`s, at least 44 px tall. Tapping one expands an inline native `<select>` of that role's available sizes (localized size labels), showing the price of the selected variant and an **Add** button. Only one role is open at a time.
- **Size memory:** after any family-builder or complete-family add, store the last chosen size per role in `sessionStorage` (`dlm:lastSize:<role>`). Preselect it when it exists for this product. Wrap every storage read and write in try/catch. Nothing leaves the browser.
- **Add** sends `POST /cart/add.js` with `{items:[{id, quantity:1}], sections, sections_url}` via `buildRequestBody`, then calls `drawer.renderContents(parsed)` and `publish(PUB_SUB_EVENTS.cartUpdate, {source:'dlm-complete-family'})`. On error, show the inline `role="alert"` message from `STRINGS.error` and do not re-render.
- An `aria-live="polite"` announcer says "Added Child · 6 Years".
- **Placement:** inside the scrolling item list, directly under the lines. This removes the old "You may also like" block from the fixed footer, which is the precondition for wallets (fix 5). On an empty cart, keep the existing New Arrivals / Recently Viewed picks.
- **Adult/Child products** (e.g. sweaters): the chip reads "+ Adult (Mom or Dad)". Allow the same role twice ("+ Another child") using a secondary chip once the role is already in the cart.
- **Styling:** `assets/dlm-family-builder.css` tokens (same pill style as the PDP builder). No new fonts. CLS-safe: the block has reserved min-height only when the JSON has candidates.

### 3.4 PDP handoff

- After a single "ADD THIS PIECE TO BAG", the drawer opens with the complete-the-family block already showing the remaining roles of that product. The shopper never has to find the PDP list.
- In `assets/dlm-family-builder.js`:
  - show a one-line intro above the roles before the first selection (new `STRINGS.intro`);
  - after a successful add, call `nextRoleKey()` to preselect the next missing role, so a second add is one tap.

### 3.5 Measurement (no PII)

- Push `window.dataLayer.push({event:'dlm_complete_family', action:'open_role'|'add', product_id, role, surface:'drawer'|'cart'})`. Existing GA4/GTM tags can read it, and no tag changes are needed to ship.
- Shopify-side KPI: order line-count distribution (1 / 2 / 3 / 4 / 5+) and AOV, compared to the profit-study table. Wait for a minimum of 30 post-launch orders before judging.

### 3.6 Tests and QA

- `ops/tests/test_family_builder.mjs`, or a sibling `test_complete_family.mjs`, with new pure helpers exported from `assets/dlm-complete-family.js`:
  - `roleFromSize(label)`, covering Mother/Father/Child/Baby/Adult and unknown input;
  - `missingRoles(product, cartVariantIds)`;
  - `variantsForRole(product, role, matchOptions)` for Color match, the Type skip, and sold-out exclusion;
  - `requestBodyFor(variantId, sections)`.
  - Run with `node --test`.
- Run `node --check` on the new JS and `shopify theme check --path . --fail-level error`.
- Browser checks: 375×812 and 1440×900; US/USD plus one EU locale (fr or de) and one RTL locale (ar).
  - Drawer with 1 line: the block is visible and the Check out button is still reachable.
  - Drawer with 4 lines: the block collapses to chips only.
  - Sold-out variant never offered.
  - Removing a line re-renders the block.
- **Do not submit test adds on the live store without owner approval.** ATC pixels feed the paid-growth data. Use the preview theme and the `ops/BROWSER_SUBAGENT_COORDINATION.md` shared-cart rule.
- **Rollback:** remove the one `render` line in `cart-drawer.liquid` / `main-cart-items.liquid` and restore l.717–761 / l.217–260 from git.

### 3.7 Optional phase 2 (owner money decision, not part of v1)

A real Shopify automatic discount for 4+ pieces of the same product, e.g. 10%. At 4 pieces, landed cost goes from 45% to about 50% after a 10% discount. That is still far better than a 1-piece order at 65%. Show it only if the discount really exists and applies at checkout.

---

## 4. Limits and what was not checked

- No add-to-cart or checkout was run live, because it would pollute ATC/purchase signals. Checkout observations come from the 2026-09-24 and 2026-09-26 packets.
- The PageSpeed/Lighthouse run was BLOCKED by quota. Weights are byte counts, not field Core Web Vitals.
- Asset byte sizes use repo copies at `HEAD`. Live assets may differ slightly (a peer's theme edits are uncommitted in the worktree).
- Review counts are sampled (35 of 261 products). The zero result is consistent, but it is not a full census.
- Revenue impact is ranked by mechanism and basket economics, not by an A/B test. Treat ranks 1–15 as `INFERENCE` until post-launch orders confirm them.

## 5. Next action (one)

Activate the 11 Christmas pajama designs as their images land, and ship fix 2 (complete the family) with the drawer restructure on the preview theme. Christmas demand is time-boxed (the last estimated US order date is Dec 8 per `dlm-holiday-order-by.js`; the worklog's safer figure is about Dec 5). Every piece added to a Christmas pajama basket lands in the 43–48% cost band instead of 52–65%.
