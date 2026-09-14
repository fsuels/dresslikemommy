# International landing check — 11 September 2026

Confidence: H for Shopify configuration and contextual prices; public landing/checkout currency **UNKNOWN**.

The frozen 4,923-row US file contains variant **39756755861601** once: *Mom & Child Matching Two Piece Swimsuit*, Child 2–3 years / Black, **17.99 USD**. A schema-discovered, validated Shopify read at **14:57:07–14:57:08 UTC** confirmed shop 15571635, the active product and `availableForSale=true`.

| Country | Fresh Admin contextual price | Candidate query, in addition to variant |
|---|---:|---|
| Australia | 26.00 AUD | `country=AU&currency=AUD` |
| Canada | 26.00 CAD | `country=CA&currency=CAD` |
| United Kingdom | 14.00 GBP | `country=GB&currency=GBP` |

All three resolved web presences return the same English root, **https://www.dresslikemommy.com/**, with 21 locale roots and complete pagination. Thus the candidate `landingBaseUrl` is `https://www.dresslikemommy.com`; no distinct `/en-au`, `/en-ca` or `/en-gb` route is established. Shopify advises deriving URLs from actual market configuration. [Shopify Markets](https://shopify.dev/docs/apps/build/markets)

Exact candidate product URLs:

- [Australia](https://www.dresslikemommy.com/products/mom-child-matching-two-piece-swimsuit?variant=39756755861601&country=AU&currency=AUD)
- [Canada](https://www.dresslikemommy.com/products/mom-child-matching-two-piece-swimsuit?variant=39756755861601&country=CA&currency=CAD)
- [United Kingdom](https://www.dresslikemommy.com/products/mom-child-matching-two-piece-swimsuit?variant=39756755861601&country=GB&currency=GBP)

**These query parameters are candidates, not verified export settings.** The public web tool rejected all three URLs and the exact frozen US URL as “not safe to open (non-retryable error).” No storefront content or HTTP response was obtained; this does not prove a storefront defect. No alternate transport or browser workaround was attempted.

Local exports may be prepared using the verified Admin prices. Submission still needs root's native check of each candidate's selected variant/country, visible price/currency, structured Offer, and persistence into cart/checkout. Admin `availableForSale` and contextual pricing do not establish country-specific purchasability or what a shopper sees. No order, external write or native control occurred in this lane.

Next: root verifies these three exact candidate journeys; the US submission remains independent.
