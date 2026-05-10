# GB / CA / AU Checkout Readiness QA

Generated: 2026-05-08 03:06 EDT

Lane: GB/CA/AU storefront checkout readiness QA.

Mode: public/read-only storefront and cart probes only. No payment data was entered, no pay/place-order button was clicked, no order was created, and no Ads/Merchant/Pinterest/Shopify/Admin/theme/campaign/budget/bid/status/product-scope/feed/conversion changes were made.

## Summary

| Country | Landing | Cart carry-through | Delivery-rate readback | Checkout UI shipping step | Status |
| --- | --- | --- | --- | --- | --- |
| GB - United Kingdom | PASS: HTTP 200, `html lang=en`, `og:price:currency=GBP` | PASS: `/cart.js` returned `GBP`, 1 item | PASS: Standard `0.00 GBP`; Express `9.71 GBP` | Not browser-verified; browser tools locked | PASS with UI residual risk |
| CA - Canada | PASS: HTTP 200, `html lang=en`, `og:price:currency=CAD` | PASS: `/cart.js` returned `CAD`, 1 item | PASS: Standard `0.00 CAD`; Express `18.00 CAD` | Not browser-verified; browser tools locked | PASS with UI residual risk |
| AU - Australia | Initial PASS: HTTP 200, `html lang=en`, `og:price:currency=AUD` | BLOCKED: `/cart/add.js` and `/cart.js` returned HTTP 429 | BLOCKED: shipping-rate endpoint returned HTTP 429 | Not verified; blocked before cart/rates after 429 | BLOCKED by storefront verification |

Decision: `GB_CA_SUPPORT_PAUSED_ENGLISH_FIRST_INFRA_AFTER_PARENT_INTEGRATION__AU_CHECKOUT_REMAINS_BLOCKED_BY_STOREFRONT_429__NO_INTERNATIONAL_LIVE_SPEND_READY`.

## URLs Checked

Product/country URLs:

- GB: `https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601&country=GB`
- CA: `https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601&country=CA`
- AU: `https://www.dresslikemommy.com/products/matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set?variant=41871520661601&country=AU`

Public cart/rate endpoints used in fresh anonymous sessions:

- `/cart/clear.js`
- `/cart/add.js` with variant `41871520661601`, quantity `1`
- `/cart.js`
- `/cart/shipping_rates.json` with country-specific address params

Policy URLs attempted after the AU blocker:

- `https://www.dresslikemommy.com/pages/shipping-info`
- `https://www.dresslikemommy.com/policies/shipping-policy`
- `https://www.dresslikemommy.com/policies/refund-policy`

Those policy URLs all returned HTTP 429 verification pages in this run, so this lane falls back to prior paid-growth continuity evidence that English public Shipping Policy and Shipping Info were clean after cooldown.

## Country Results

### GB - United Kingdom

Test address: London, England, `SW1A 1AA`.

Readback:

- Product landing: HTTP `200`, final URL retained `country=GB`, `html lang=en`, currency meta `GBP`.
- Cart clear: HTTP `200`.
- Cart add: HTTP `200`, item title `Beach Outfits Holiday Palm Tree Print Summer Dresse... | DLM - Father XL / blue`.
- Cart readback: HTTP `200`, currency `GBP`, item count `1`, total price minor units `2100`.
- Shipping-rate readback: HTTP `200`.
- Rates: `Standard Delivery (10 - 14 Days)` at `0.00 GBP`; `Express Delivery (7 - 11 Days)` at `9.71 GBP`.

Status: pass for product/cart/rate evidence. A real browser checkout UI pass is still needed before enablement because this run could not open an isolated browser tab.

### CA - Canada

Test address: Toronto, Ontario, `M5V 2T6`.

Readback:

- Product landing: HTTP `200`, final URL retained `country=CA`, `html lang=en`, currency meta `CAD`.
- Cart clear: HTTP `200`.
- Cart add: HTTP `200`, item title `Beach Outfits Holiday Palm Tree Print Summer Dresse... | DLM - Father XL / blue`.
- Cart readback: HTTP `200`, currency `CAD`, item count `1`, total price minor units `3900`.
- Shipping-rate readback: HTTP `200`.
- Rates: `Standard Delivery (10 - 14 Days)` at `0.00 CAD`; `Express Delivery (7 - 11 Days)` at `18.00 CAD`.

Status: pass for product/cart/rate evidence. A real browser checkout UI pass is still needed before enablement because this run could not open an isolated browser tab.

### AU - Australia

Test address: Sydney, New South Wales, `2000`.

Initial readback:

- Product landing: HTTP `200`, final URL retained `country=AU`, `html lang=en`, currency meta `AUD`.
- Cart clear: HTTP `200`.
- Cart add: HTTP `429`.
- Cart readback: HTTP `429`.
- Shipping-rate readback: HTTP `429`.
- Blocker body title/text: `Verifying your connection...`.

Recovery attempts:

- MCP Playwright browser tab: blocked because the Playwright MCP browser profile was already in use and requested an isolated instance.
- MCP Chrome DevTools isolated context: blocked because the Chrome DevTools MCP profile was already running and requested a different user-data-dir or stopping the running browser.
- Slow AU-only retry after a 65 second cooldown with fresh cookies and Shopify cart permalink: blocked at product landing with HTTP `429` and `Verifying your connection...`.

Status: AU is not cleared by this lane. Product presentment initially showed AUD, but cart carry-through and checkout/rate reachability remain blocked by storefront bot protection.

## Commands / Tools Used

- `sed`, `find`, and `rg` to inspect prior continuation, checkout, localization, and final-URL artifacts.
- Inline `python3` public storefront probe with `urllib` and fresh `CookieJar` sessions per country.
- `mcp__playwright__.browser_tabs` attempted for an isolated AU browser tab; unavailable due locked profile.
- `mcp__chrome_devtools__.new_page` attempted for an isolated AU browser tab; unavailable due locked profile.
- Inline `python3` AU-only cooldown retry with fresh cookies and cart permalink.
- Inline `python3` policy URL readback attempt after AU blocker.

## Residual Risk

- GB and CA have strong public cart/rate evidence, but not a visual Shopify one-page checkout shipping-step screenshot or browser DOM readback from this run.
- AU must be retested after cooldown in a real isolated browser/profile because repeated public probes hit Shopify verification.
- Policy page freshness could not be refreshed after the rate-limit event; use prior clean English policy evidence until a cooldown public/browser recheck succeeds.
- This lane does not clear live spend. Merchant/Pinterest catalog health, tracking, economics, final URL readbacks, and exact owner approval still gate any enablement.

## Next Action

Run a cooldown, one-country-at-a-time browser walkthrough for GB, CA, and AU in a truly isolated profile or human browser tab. Start from the same country-qualified product URL, add variant `41871520661601`, proceed only until shipping rates are visible, confirm country/currency/order-summary/rates, and stop before entering payment or creating an order.
