# Date-sensitive storefront text (2026-11-27)

Read-only result: every date-dependent element in the theme already switches itself off or to a neutral, true variant. Nothing would become false between 28 Nov and 20 Jan with nobody touching the store, so no theme change, no lock, nothing published. The owner's 2 Dec cutoff and the pajama hold are untouched.

Scope read at origin/main: every `'now' | date` in Liquid and every `new Date()` in theme JS (`git grep`), templates/index.json, locales (no "2025/2026/2027", "Black Friday" or "Cyber Monday" in any locale or theme file).

## How each element is decided

| # | Element (file) | Where | Decided by |
|---|---|---|---|
| A | US dated Christmas line "Estimate: order by {order} to arrive by {arrive}. Not a guarantee." (`snippets/christmas-order-by.liquid` + `assets/dlm-delivery-dates.js` renderChristmasOrderBy) | PDP value strip, cart page, cart drawer | Liquid renders a HIDDEN node only 1 Nov-7 Dec (shop time) and only for country US; JS fills and shows it only while order day + 21 days (7 handling + US transit max 14) <= 23 Dec, i.e. through Wed 2 Dec; otherwise keeps it hidden. No JS = stays hidden. |
| B | Non-US neutral line "Ordering for Christmas? Delivery times vary by country, so order as early as you can." (same snippet) | PDP, cart, drawer | Liquid, 1 Nov-7 Dec, non-US. No date, no promise. |
| C | Christmas banner (`snippets/christmas-cutoff-banner.liquid` + `assets/dlm-holiday-order-by.js`) "Order by {date} for estimated Christmas arrival" | Top of home and Christmas collections | Liquid reserves the slot 1 Nov-3 Dec; JS (US only) shows it while cutoff (23 Dec - 21 days, Sunday roll) >= today and within 14-day lead: 19 Nov-2 Dec. Row is `visibility:hidden` unless JS fills it. Non-US: neutral line B, 1 Nov-3 Dec. |
| D | PDP holiday slot (`snippets/dlm-pdp-value-strip.liquid`) | PDP | Liquid reserves space only while 16 <= days to 23 Dec <= 30 (about 23 Nov-7 Dec); JS collapses it when A is hidden. |
| E | Delivery estimate "Estimated delivery: <date> – <date>" (`delivery-estimate-copy` + JS) | PDP, cart, drawer | Today + (transit + 5) days for mapped countries; neutral "delivery times vary" elsewhere. Never mentions Christmas. True every day. |
| F | Home hero (`sections/hero-banner.liquid`, `snippets/hero-season-window.liquid`, `hero-seasonal-copy.liquid`; index.json `seasonal_copy: halloween_winter`) | Home | Shop date: Christmas edition 16 Oct-2 Dec ("Matching Christmas outfits for the whole family"), winter_photos 3-25 Dec ("Matching family outfits for winter photos"), new_year 26 Dec-10 Jan ("Matching winter outfits for the whole family"), valentines 11 Jan-14 Feb, everyday 15 Feb-31 Aug. Christmas product photos only to 25 Dec. All editions translated; none promises arrival. |
| G | Home seasonal collection (`sections/seasonal-collection.liquid` + `christmas-season-collection.liquid`) | Home | Christmas hub collection 1 Oct-25 Dec (heading = collection title); pajamas fallback only 1 Sep-31 Oct; after 25 Dec the section renders nothing. |
| H | Collection pill row (`snippets/collection-breadcrumbs.liquid`) | Collections | "Christmas" pill 16 Oct-25 Dec, "Valentine's Day" 11 Jan-14 Feb. |
| I | Mega menu (`snippets/dlm-mega-panel.liquid`) | Header | Halloween items 1 Sep-31 Oct; Valentine's items 1 Nov-15 Feb. Christmas items are menu data (no date gate). |
| J | PDP Christmas cross-links (`pdp-purchase-confidence.liquid`) | Christmas PDPs | 1 Nov-24 Dec: links to Christmas sweaters/pajamas collections (titles only). |
| K | "Shopping for the holidays? See ..." (`collection-seo-fallback.liquid`) | Some collections | Whole of Nov and Dec. Link only, no date or promise. |
| L | Thanksgiving links/articles (`collection-guide-english-terms`, `collection-related-guides`) | Collections | 1 Oct-26 Nov; already off. |
| M | Footer © year | All | `'now' | date: '%Y'`, auto. |
| N | Christmas guide/FAQ text (`collection-guide-christmas-*`, `christmas-hubs`) | Christmas collections | Static: "check the estimated delivery date on each product page... order early". No date, no promise; still true after Christmas (the collections stay up). |

## Date x element (US visitor unless noted)

| Date | A US cart/PDP dated line | B non-US neutral | C banner | E estimate | F hero | G home seasonal | H/I/J/K |
|---|---|---|---|---|---|---|---|
| 28 Nov | "order by Wed, Dec 2 to arrive by Wed, Dec 23" | shown | "Order by Wed, Dec 2 for estimated Christmas arrival" | today+12-19 | Christmas | Christmas hub | Christmas pill/links on |
| 3 Dec | hidden (JS) | shown (to 7 Dec) | hidden (US); non-US neutral 3 Dec only | today+... | Winter photos | Christmas hub | on |
| 20 Dec | not rendered | not rendered | not rendered | today+... | Winter photos | Christmas hub | on (J to 24, H to 25) |
| 26 Dec | not rendered | not rendered | not rendered | today+... | New Year | empty | H off, J off, K on (no promise) |
| 2 Jan | not rendered | not rendered | not rendered | today+... | New Year | empty | K off; Valentine menu item on |
| 20 Jan | not rendered | not rendered | not rendered | today+... | Valentine's | empty | Valentine pill + menu |

Nothing in this table is false or stale on its date: no Christmas arrival promise after 2 Dec, no "order by 2 Dec" on 3 Dec, no Christmas hero in January, no wrong year.

## Evidence

- Node simulation of the live JS (origin/main copies of `dlm-holiday-order-by.js` and `dlm-delivery-dates.js`, clock forced): banner/PDP order-by shows "Wed, Dec 2" on 27 Nov, 28 Nov and 2 Dec, hidden on 3 Dec, 20 Dec, 26 Dec, 2 Jan, 20 Jan. The cart/PDP line A shows on 27 Nov-2 Dec and is hidden 3-26 Dec. Note: on 2 Jan and 20 Jan the JS function alone would compute next December (order by 2 Dec 2027), but Liquid does not render the node outside 1 Nov-7 Dec, so nothing shows (latent only; not changed).
- Live, built-in browser, own tab, 1 load of `/` (visitor country ES): banner is the neutral non-US line; calling the live `DLMHolidayOrderBy.orderByFor` with country forced to US for 28 Nov, 2 Dec, 3 Dec, 20 Dec, 26 Dec, 2 Jan, 20 Jan gave "Order by Wed, Dec 2 for estimated Christmas arrival" for the first two and hidden for the rest. Country restored, tab closed, cart not touched.
- Existing tests `ops/tests/test_holiday_order_by.mjs` and `test_delivery_dates.mjs` pass.
- Liquid gates (F-M) cannot be forced from the browser; reasoned from the code above (shop timezone America/New_York; MMDD comparisons inclusive).

## Residual risks (not fixed, not false)

1. Time zone: JS uses the visitor's own clock; a US shopper whose device is behind ET still sees "order by Dec 2" until their local midnight; no zone in the US is behind by more than a few hours, and visitors east of the US lose the line earlier (safe side).
2. Page cache: Liquid date switches (hero, pills) can lag a cached page by minutes; the switches only move between true texts.
3. Blog articles (store content, not theme) still carry the arrival-style sentence flagged in `delivery-statements-2026-11-26.md` pattern 6 ("order early ... so everything arrives before your photo day or Christmas morning"); it has no date, but after 2 Dec it reads as advice that can no longer be met for Christmas morning. Owner/CEO decision; not a theme change.
4. Neutral line B stays until 7 Dec for non-US shoppers: "order as early as you can" with no date; true, but the CEO may prefer it to stop on 3 Dec like the US line (one-number change in `christmas-order-by.liquid`, `1207` -> `1202`).

## Addendum: published blog articles (Admin API, read-only, 2026-11-27)

Read with `oe.Admin().gql` (token not printed, nothing written, no storefront request): 313 articles, 121 published; English source plus es, de, fr, it, cs, ro translations (title, body, summary, meta title/description). Every sentence that pairs a Christmas/holiday word with an ordering, delivery or arrival word was read (129 sentences: en 16, es 21, de 21, fr 22, it 18, cs 19, ro 12). No translation of the Christmas guides is marked outdated.

Result: no sentence in any of the 7 languages promises arrival for Christmas or gives an order-by date. Ordering advice is general ("order early", "check the estimated delivery window on each product page", "Christmas does not move, so the outfits need to be in your hands with time to try everything on") and stays true after 3 Dec. The "12–19 days" figures are labelled "for the United States; Canada about 19–29 days; other countries check the product page" in every language. The earlier flagged sentence ("...so everything arrives before your photo day or Christmas morning", delivery-statements pattern 6) is no longer in the English or the six translations.

Only borderline wording (suggests, does not promise):

| Article | Lang | Field | Sentence (short) | Current English of the same sentence | False from 3 Dec? |
|---|---|---|---|---|---|
| matching-family-christmas-pajamas-guide-2026 | en | summary, meta description | "...per-person sizing, baby onesie options and estimated holiday delivery." | (source) | No date or promise; after 2 Dec a US order no longer has an estimate before Christmas, so "estimated holiday delivery" reads as outdated advice. Borderline. |
| same | es | summary, meta | "...plazos estimados de entrega para Navidad" | "estimated holiday delivery" | Same, slightly stronger ("for Christmas"). Borderline. |
| same | de | summary, meta | "...geschätzte Lieferzeiten zum Fest" | same | Borderline. |
| same | fr | summary, meta | "...livraison estimée pour les fêtes" | same | Borderline. |
| same | it | summary, meta | "...consegne stimate per le feste" | same | Borderline. |
| same | cs | summary / meta | "...odhadovaným doručením před svátky" / "...odhadované doručení před Vánocemi" | same | Stronger than English ("delivery before Christmas"). Most likely to read as false after 2 Dec. |
| same | ro | summary / meta | "...livrarea estimată de sărbători" / "...livrare estimată" | same | Borderline / neutral. |

Count of promises or dates per language: en 0, es 0, de 0, fr 0, it 0, cs 0, ro 0. Borderline (one article, summary + meta): en 2, es 2, de 2, fr 2, it 2, cs 2, ro 1.

Not counted (read and judged general or not about Christmas arrival): christmas-eve-box, christmas-morning, christmas-dinner, christmas-eve-evening, concert, newborn-holiday, maternity-christmas, cold-weather, New Year's Day ("order before the holiday rush"), Valentine's ("easiest to enjoy when they arrive before the day itself"), Thanksgiving-and-Christmas ("Thanksgiving falls on 26 November this year", true for 2026).

If the CEO wants it cleaner after 2 Dec: change the English summary/meta of the pajamas guide from "estimated holiday delivery" to "estimated delivery" and the cs/es equivalents (Admin translation writes; not done here).
