# Phase 4 Policy Truth Pack

Date: 2026-04-29

Scope: local theme/source truth for paid-traffic conversion blockers. No live Shopify Admin policy, shipping-rate, market, campaign, feed, or checkout setting write is recorded by this packet.

## Current Storefront Truth

| Area | Current local storefront position | Evidence source | Remaining gate |
| --- | --- | --- | --- |
| Shipping cost | Shipping options and costs are confirmed at checkout after address entry. No visible local-theme free-shipping promise should be used for paid traffic. | `locales/en.default.json`, PDP/cart/home/theme scans | Live checkout-rate and policy-page browser verification. |
| Delivery timing | PDP/cart calendar-date estimates are disabled. PDP copy points shoppers to checkout-confirmed timing. | `layout/theme.liquid`, `assets/cart.js`, `sections/main-product.liquid` | Do not re-enable dates until approved shipping ranges exist by market/product. |
| Customs/duties | International orders may be subject to local taxes, duties, or customs fees collected by the carrier or local authority. | `products.additional_info.secure_logistics_line_2` | Owner/legal review before stronger DDP/DAP wording. |
| Returns | 30 days from delivery to request a return or exchange. | `products.additional_info.return_policy_line_1` | Live refund-policy page and return-rule enforcement verification. |
| Swimwear/intimates | Swimwear and intimates are not returnable for hygiene reasons; final sale and personalized items are excluded. | `products.additional_info.return_policy_line_3` | Product tagging/return-rule enforcement after owner review. |
| Return shipping/refund timing | PDP tells shoppers to review the refund policy for eligibility, return shipping, and refund timing before sending anything back. | `products.additional_info.return_policy_line_4` | Live policy page must define actual return routing/cost handling clearly. |
| Reviews/trust | Storewide aggregate rating/social-proof fallback is not used. Product reviews are shown only through product metafields/Judge.me app blocks. | `sections/main-product.liquid`, `templates/product.json`, theme scan | Keep disabled until proof exists. |
| Size guide | FAQ/PDP sizing points to on-page Size Details/size chart behavior; no off-domain size-guide link is required in local theme. | `snippets/product-faq-schema.liquid`, footer size-guide filter | Live FAQ page readback if deploying Admin page content changes. |

## Paid-Traffic Rule

Do not mark pages `READY_FOR_PAID` from this packet alone. A page can only advance after live browser checkout/policy QA confirms shipping rates, return-policy rendering, customs/duties wording, PDP/cart copy, search recovery, collection filters, and product-card price rendering on actual storefront URLs.
