# Google Ads Purchase Attribution Readback

Generated: 2026-05-15 10:24 EDT

Mode: read-only Google Ads existing authenticated Chrome/CDP readback plus read-only Shopify Admin GraphQL order-attribution summary. No external writes.

Verdict: `PURCHASE_TRACKING_HEALTHY__NO_PAID_GOOGLE_CPC_ORDERS_FOUND__DO_NOT_CHANGE_CONVERSION_GOALS`

## Why This Packet Exists

The owner pasted an outside critique that diagnosed the live Standard Shopping campaign as having broken or missing purchase conversion tracking, then a second diagnosis that claimed the root cause was a removed or misrouted Purchase action.

Current evidence does not support either live-fix conclusion. The campaign has zero primary purchase conversions/value, but the current Google Ads purchase action is still primary/included and has received a recent purchase request. The stronger current conclusion is that Standard Shopping has no paid-attributed purchase orders in the checked window, not that the purchase action should be recreated or repaired.

## Google Ads Current Purchase Action Readback

Account surface: Google Ads client `399-097-6848`, existing authenticated session for `dresslikemommy.com`.

| Conversion action | Category | Primary | Included | Current readback |
|---|---|---:|---:|---|
| `Google Shopping App Purchase` | Purchase | Yes | Yes | Current conversion-action data shows all-conversions `5.0`, value `193.9`, and last received request `2026-05-11T21:47:18Z`. |
| `Purchases from google Adwords` | Purchase | No | No | Secondary/excluded; older last-request evidence only. |
| `Purchases from google analytics data` | Purchase | No | No | Secondary/excluded. |
| `dresslikemommy.com - GA4 (web) purchase` | Purchase | No | No | Secondary/excluded. |

Readback interpretation:

- The current account-default purchase goal names `Google Shopping App Purchase` as the primary/included purchase action.
- A removed historical purchase action visible in Google Ads is not current proof that the active purchase action is removed.
- Add-to-cart/begin-checkout rows and historical `All conv. value` are not ROAS proof and should not drive Shopping optimization.

## Shopify Order Attribution Readback

Window checked: Shopify Admin orders processed from `2026-04-29` through the current readback.

Sanitized order-attribution summary:

| Metric | Count |
|---|---:|
| Total orders returned | `18` |
| Non-cancelled, non-test orders | `13` |
| Orders with Google paid/CPC signals | `0` |
| Orders with Google organic/product-sync signals | `4` |

One sanitized order around `2026-05-11T21:47Z` aligned with the Google Ads purchase-action last-request timestamp within seconds, but its attribution signals were organic/product-sync, not paid CPC. That supports the conversion tag receiving real purchase requests while also supporting the campaign report's zero paid-attributed purchase value.

No customer PII, order IDs, customer names, emails, addresses, payment data, or source/vendor URLs were written to this packet.

## Decision

- Do not restore, recreate, or switch the active Google Ads purchase conversion action from this pasted diagnosis.
- Do not change campaign conversion goals, GA4/GTM setup, Shopify conversion integration, or account-default goals without a separate exact approval and fresh before/after measurement plan.
- Do not raise Shopping bids to benchmark levels because of a false tracking diagnosis. The owner hard CPC constraint and current zero paid-attributed purchase evidence still require tight economics.
- Do not read `All conv. value` or micro-conversion value as purchase revenue.
- Treat the Standard Shopping result as currently unprofitable/learning-poor: spend and clicks exist, but no paid-attributed purchases were found.

## Sales-Moving Next Action

The safest current Standard Shopping action is not conversion-action surgery. It is:

1. Keep the current purchase action unchanged.
2. Continue judging Shopping by primary purchases and conversion value.
3. Use the clicked-title cleanup packet if the owner approves the exact no-feed/no-campaign Shopify title/display-title cleanup for clicked PDPs with literal ellipses.
4. Continue Merchant/feed eligibility work for `US/es`, Canada English/French, and GB English before any multilingual Shopping build.
5. If the owner wants an end-to-end attribution proof, prepare a separate controlled paid-test-purchase approval packet. Do not create a payment/order/test purchase from automation without explicit owner action.

## Guardrails

- No Google Ads bid, budget, status, product-group, product-scope, conversion-goal, campaign, upload/import/apply, or account-goal write occurred.
- No Shopify product/order/customer/payment mutation occurred.
- No Merchant, Pinterest, GA4, GTM, billing, credential, feed, source, product data, theme, or catalog write occurred.
- This readback supersedes the outside claim that the current live issue is a broken/missing purchase action.
