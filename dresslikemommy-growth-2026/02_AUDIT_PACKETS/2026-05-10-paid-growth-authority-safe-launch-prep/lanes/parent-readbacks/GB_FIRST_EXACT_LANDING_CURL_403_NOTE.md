# GB First Exact Landing Curl Readback Note

Date: 2026-05-10

A single low-volume public `curl` request to the first-enable GB final URL returned HTTP `403` and saved the response to `gb_first_exact_landing.html`. This is not treated as a storefront failure because Shopify/public bot protection can block raw terminal probes while browser readbacks pass.

URL checked:

`https://www.dresslikemommy.com/products/elegant-beige-chiffon-family-matching-dresses-mother-daughter-summer-outfits?country=GB`

Result:

- HTTP: `403`
- Effective URL: same as requested
- Account/platform writes: none
- Checkout/payment/order: none

Follow-up browser readback:

Completed later in the same session. See `GB_FIRST_EXACT_BROWSER_READBACK.md`.

The browser-style readback loaded the exact URL, confirmed GB/GBP product presentment, found no visible `403`/verification wall/stale Christmas metadata, added one item to cart, and reached checkout entry with no payment data, no Pay Now / Place Order click, and no order.

Residual action:

The raw-curl uncertainty is solved. The separate non-US purchase-event currency/value proof remains open before any new live spend.
