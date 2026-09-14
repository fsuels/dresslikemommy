# Pin 2 current product source

**PASS — current source facts**, September 6, 2026, **07:55:25 UTC**. Read-only scope: `VC_ORGANIC_02`, product **7533081133153**, shop `dresslikemommy-com.myshopify.com` / Dress Like Mommy.

Current title: **Vintage Cottage Floral Mommy and Me Pajamas — Short-Sleeve Set**. Handle: `vintage-cottage-floral-mommy-and-me-pajama-set`. Status is **ACTIVE**, with the same nonnull Online Store URL as the saved source and the prepared Pin's destination base. Its tracking query remains unchanged and was not opened.

All **11 variants** returned in one complete page, with no GraphQL errors:

| Selection | Listed choices | Default USD price |
|---|---|---:|
| Mother | S, M, L, XL | $34.99 |
| Child | 2, 3, 4, 5, 6–7, 8, 9–10 Years | $31.99 |

Every variant uses **Vintage Cottage Floral** as its Color. The current title, selection/price pairs and currency exactly match `pinterest_organic_product_source.json`. The Pin's **Mother S–XL / Child 2–10 Years** wording matches these listed options. Child ranges include grouped labels; this is not a fit or individual-age-variant guarantee.

Each variant contains exactly one wearer-specific Size choice: Mother or Child. This supports separate-person **selection structure**. The existing Pin's sale-unit disclosure cites earlier rendered PDP wording; this check did not reverify current rendered disclosure, package contents or checkout behavior.

Schema discovery and both validators passed before the structured query. The initial local ID comparison was corrected because the Pin stores numeric `7533081133153`, while GraphQL uses `gid://shopify/Product/7533081133153`; the exact IDs agree. Fifteen final comparison checks pass. The JSON retains variant IDs/options/prices, exact query, validation, pagination, timestamps and both source-file hashes.

No stock, availability, fit, delivery, market-specific pricing, supplier-clean landing quality or profit is inferred. No browser, public HTTP retry, private fields or external mutation occurred. This is not a Pinterest publication or traffic-result receipt.

Next: root integrates this source PASS with its remaining Pin preparation gates. Evidence: `pin2_current_product_readback.json`. Documentation: [ProductVariant prices/options](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/ProductVariant). Continue through the [canonical prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md).
