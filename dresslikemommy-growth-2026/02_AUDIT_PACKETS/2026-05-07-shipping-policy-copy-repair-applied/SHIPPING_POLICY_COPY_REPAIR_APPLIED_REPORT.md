# Shipping/Policy Copy Repair Applied

Generated: 2026-05-07

## Scope

Owner approved applying the shipping/policy copy repair before any international paid import or spend.

Applied only:

- Shopify Admin Shipping Policy body.
- Shopify Admin Terms of Service pricing sentence and section 5 shipping block.
- Shopify Admin page `shipping-info` body.

Not changed:

- No theme edits or theme publish.
- No products, Shopify product data, inventory, markets, shipping rates, feeds, Merchant Center, Pinterest, Google Ads, budgets, bids, campaign statuses, product scope, product groups, feed labels, or conversion goals.
- No checkout payment, no order creation.
- Refund policy was not changed. Return shipping remains customer-paid; "NL returned rates" in prior notes means outbound checkout delivery rates, not return postage.

## Admin Write Result

Script: `ops/scripts/apply_shipping_policy_copy_repair.py`

Mode: `--execute`

Applied:

- `shipping_policy`
- `terms_of_service`
- `shipping_info_page`

Admin/GraphQL readback:

- Shipping Policy updated at `2026-05-07T16:03:22-04:00`; old four-country blocker absent; checkout policy URL shows the new checkout-availability copy.
- Terms of Service updated at `2026-05-07T16:03:23-04:00`; old `All prices are in USD unless otherwise noted` and four-country shipping sentence absent; new currency-at-checkout and online-store shipping text present.
- Refund Policy still contains the customer-paid return-shipping marker.

Artifacts:

- `summary.json`
- `before/`
- `after/`
- `delayed-readbacks/admin_policy_graphql_summary.json`
- `delayed-readbacks/localized_body_policy_scan.json`

## Public Readback

Clean or improved:

- Checkout-hosted Shipping Policy URL is clean and shows the new checkout-availability copy.
- Storefront Terms of Service shows the new currency-at-checkout and online-store shipping text.
- ES, RO, and PT localized Shipping Policy pages now show the new English source copy in the body.

Still blocked:

- Storefront `/policies/shipping-policy` continued to serve the old English body on repeated cache-busted reads during this session.
- Storefront `/pages/shipping-info` continued to serve old English body/metadata on readback.
- Localized Shipping Info pages for ES, IT, RO, and PT still contain old worldwide/four-country translated copy.
- Italian localized Shipping Policy still contains old translated four-country copy.

Interpretation: the approved Admin source write landed, but public storefront/published translation surfaces are not fully clean. This still blocks live international paid spend.

## Checkout QA

Required region/province values found:

- ES: `Comunidad de Madrid`
- IT: `Roma`
- RO: `București`
- PT: `Lisboa`

Earlier same-session no-payment rate probes using these values returned outbound checkout delivery rates for all target countries:

- NL, ES, IT, RO, PT each returned Standard Delivery `0.00 USD` and Express Delivery `12.99 USD`.

The final expanded QA run added localized Shipping Info pages to the URL set and then hit Shopify storefront bot protection / HTTP `429` at the IT product page before cart/rate probes could run. Its JSON artifact therefore records the current stop-rule blocker, not a rate failure.

Artifacts:

- `checkout-region-recheck/CHECKOUT_QA.md`
- `checkout-region-recheck/checkout_probe_raw.json`

## Decision

Do not proceed to international paid import or spend.

Why:

- Admin source copy repair is applied.
- Outbound checkout delivery rates were observed for NL/ES/IT/RO/PT using required regions.
- Public storefront policy/page translation surfaces are still not clean.
- Latest expanded QA hit storefront bot protection after repeated probes.
- Product pages still report `USD` currency meta on localized routes, despite checkout rates being available.
- PT routes remain partially broken (`/pt-BR` 404; `/pt` failures observed in prior and current probes).

## Next Safe Action

Prepare a localized policy/page translation cleanup plan for ES, IT, RO, and PT, plus a storefront cache/readback strategy for `/policies/shipping-policy` and `/pages/shipping-info`. Apply only after fresh approval because this is another live public-copy write.
