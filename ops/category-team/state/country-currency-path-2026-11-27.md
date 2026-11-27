# Country / currency path, store vs checkout (read-only test, 2026-11-27)

Method: built-in browser pane, 375x812, shared cookie jar, 10 page loads. Switching done with the same POST `/localization` the country selector form sends (`assets/localization-form.js` onItemClick -> `form.submit()`) plus real `/?country=` loads. Cart emptied, viewport reset, country back to US at the end. Start state: US/USD, empty cart.

## Code (origin/main)
- `snippets/auto-localization.liquid` + `assets/auto-localization.js`: once per browser (flag `dlm_auto_country` in localStorage + cookie). Asks `/browsing_context_suggestions.json` (IP), and only if the visitor is still on US and the detected country is enabled, POSTs `/localization` (js:154-167). Any `?country=` load sets the flag first (js:135). Bots/design mode skipped. It never reads `cart_currency`.
- Currency is not decided by theme code: Shopify derives it from the `localization` cookie (Basic plan, no auto geo). The theme only submits `/localization`.
- Cart is not frozen to a currency: Shopify reprices the same cart on the next request after `/localization`.

## Results (same cart token throughout)
| # | Action | cookies `localization` / `cart_currency` | `/cart.js` | Checkout first screen |
|---|---|---|---|---|
| a1 | `/?country=GB`, add item | GB / GBP | GBP 50.00 | `/checkouts/cn/<t>/en-gb`, GBP 50.00 |
| a2 | Selector POST US (then `/?country=US`) | US / USD | USD 54.99 | `/en-us`, USD 54.99 |
| a3 | Stale `.../en-gb` URL opened while US | US / USD | USD | page shows USD 54.99 (URL language only) |
| b | US -> DE selector | DE / EUR | EUR 58.95 | `/en-de`, EUR 58.95 |
| c | `/de/products/...` with US cookie | US / USD | USD | PDP "$54.99"; `/de` does not change country |
| d | Geo script after add-to-cart | see below | | |

Store and checkout agreed in every controlled test. I could NOT reproduce GB checkout with a US store.

## Scenarios
1. **Switch country with items in cart (a, b): NO_ISSUE.** Cart and checkout reprice to the chosen country on the next request. Evidence above.
2. **Stale tab / shared cookies (the reviewer's case): plausible, cause unconfirmed.** `localization` is one cookie for the whole browser. If a second tab or session sets GB, an older tab still paints US prices, while any cart call from it (add, drawer refresh, checkout button) runs under GB, so checkout is GBP. The quality note said another session was active in the same browser, which fits. A real shopper needs two tabs or a UK-then-US switch in another tab: rare. Tag OWNER-watch / NO_ISSUE; fix only if analytics show it.
3. **Geo script after add-to-cart (d): possible, narrow.** Script fires on first page load after an async fetch, then POSTs `/localization` and reloads. A shopper who adds to cart within that window on first visit gets the cart repriced (USD -> CAD/EUR/GBP) and the page reloads. One-shot per browser (flag set before the submit, js:155). Reprices consistently, so no store/checkout mismatch, only a surprise total. Tag FIX_THEME (low priority): skip the auto switch when `cart.item_count > 0` (cart count is available server side in the config JSON).
4. **Localized path with US geo (c): NO_ISSUE.** `/de/` changes language only; country stays US/USD until the visitor or the geo script picks a country. German-speaking visitors on a US IP see USD in German, by design.
5. **Odd finding: duplicate `localization` cookies.** Language-path POSTs (`/de/localization`) leave a cookie scoped to path `/de` (seen `/de=GB` or `/de=US`) beside the root one. Test: the server ignored the stale `/de` value (pages, cart and checkout followed the root cookie). Harmless today, but it makes cookie-based debugging misleading. Tag NO_ISSUE.
6. **Checkout URL language segment (`en-gb`, `en-us`)** is cosmetic; the checkout currency follows the cart's current country. A shared or saved old checkout link opens in the cart's current currency. NO_ISSUE.

## Plausible frequency
Mismatch needs two simultaneous country changes in one browser (two tabs, or a family sharing a device with UK and US visits). Under 1% of carts by reasoning; no measurement. Geo race (3): first-visit visitors outside the US who add to cart within roughly one second.

## Minimal action
Nothing to change now. Optional FIX_THEME: do not run the auto country switch when the cart already has items. If the owner wants proof of the mismatch, replay with two real tabs: tab A on `/?country=GB`, tab B on `/?country=US`, then press Checkout in tab A (not run; shared-cookie limits).
