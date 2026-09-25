# Desktop checkout test — 2026-09-24 (~22:45 EDT)

Surface: Claude desktop built-in browser, viewport 1440x900, public storefront www.dresslikemommy.com, US/USD/English.

| Step | Result |
|---|---|
| PDP `/products/little-pear-mommy-and-me-pajamas`, select Mother M, "Add this piece to bag" | `/cart.js`: 1 item, variant 44046788395105, $32.99 USD |
| `/cart` → Check out | Shopify one-page checkout loaded, correct line item and total |
| Placeholder contact/address (checkout-test@example.com, "Test Checkout", 123 Test Street, Miami FL 33101) | Address-validation suggestions shown; shipping rates loaded: Free Standard Shipping FREE, Priority Shipping $12.99; total $32.99 |
| Payment section | Credit card fields, Shop Pay, PayPal, Crypto USDC; express buttons PayPal / Amazon Pay / Google Pay / Venmo rendered; "Pay now" enabled |
| Console / network | One 401 on `/private_access_tokens` (standard Shopify Private Access Token probe, benign). All checkout `Proposal` GraphQL calls 200. |

Stopped before "Pay now": no card data entered, no order placed, no payment/gateway setting changed. Cart cleared afterwards (`/cart/clear.js` → 0 items). A checkout session with placeholder email may appear as an abandoned checkout in Shopify admin.

Not verified: payment authorization, order creation, thank-you page, purchase pixel. Requires an owner-performed real (then refunded) order or Shopify test/Bogus gateway, which would be a payment-settings change.

Observation: "Email me with news and offers" appeared checked in checkout although the test never clicked it (likely a pre-checked store marketing-consent setting; unconfirmed). Not changed.

## Funnel context (ShopifyQL sessions, last 30 days, read 2026-09-24)

| Device | Bot flag | Sessions | Cart adds | Reached checkout | Completed |
|---|---|---:|---:|---:|---:|
| mobile | human | 2,133 | 99 | 23 | 10 |
| desktop | bot | 1,781 | 13 | 15 | 0 |
| desktop | human | 1,625 | 22 | 8 | 0 |
| mobile | bot | 95 | 0 | 0 | 0 |
| tablet | human | 19 | 0 | 0 | 0 |

Desktop bot-flagged sessions reach checkout more often than they add to cart (15 vs 13), consistent with scripted probing. Human desktop 0/8 vs mobile 10/23 (~43%): 0 of 8 at 43% has ~1% chance, so a desktop payment-step problem is not ruled out. The QA above proves desktop checkout works through shipping and payment-method rendering; it does not test payment submission.

Conclusion: UI/checkout-flow defect ruled out up to "Pay now". Remaining unknown is payment submission on desktop. One owner-performed desktop order (then cancel/refund) closes it.
