# Portuguese landing readback

Confidence: H for HTTP, canonical, language metadata and nonempty source grids; M for language quality from the server-rendered main text. Browser execution and Brazil/Portugal purchase paths were not verified.

Fresh public GET window: 2026-09-22 18:42:34–18:42:37 UTC. All eight supplied URLs returned HTTP 200 without redirects. Each has `html lang="pt-BR"`, the exact requested `/pt/collections/…` canonical, and both `hreflang="pt-br"` and `hreflang="pt"` pointing to the same `/pt` URL. **Keep `/pt`; do not replace it with an assumed `/pt-br` path.**

| Group | Collection path below `/pt/collections/` | Main H1 | First-page unique product links |
|---|---|---|---:|
| 1 | dresses | Vestidos Mamãe e eu | 36 |
| 2 | new-women-outfits | Roupas combinando para a família | 36 |
| 3 | family-tops | Correspondência Familiar Tops | 36 |
| 4 | pajamas | Família correspondente Pijamas | 22 |
| 5 | daddy-me-shirts | Camisetas pai e filho | 23 |
| 6 | mommy-and-me | Roupas Mamãe e eu | 36 |
| 7 | swimsuits | Correspondência Familiar Maiôs e biquínis | 35 |
| 8 | family-sweaters | Suéteres e jaquetas familiares | 7 |

The main introductions, navigation and numerous product titles are Portuguese. Some product-name descriptors remain English, including “Crewneck Tops”, “Family Matching Tops” and “Matching Swimwear”. These pages are not established as entirely Portuguese or free of translation defects.

**Specific landing-copy inconsistency:** group 5's H1 says “Camisetas pai e filho”, while its introduction explicitly describes camisas de botão/camisa social/Hawaiian styles and its product titles describe camisas. The proposed ad label “Camisas pai e filho” fits those descriptions better. Do not reinterpret this heading as evidence that the button-down category should receive T-shirt keywords. No storefront repair was attempted under this campaign worker scope.

All grids are nonempty in server-rendered source, including the three destinations the attachment could not recover. Counts deduplicate product URLs by handle on the first collection page. They are neither total collection counts nor proof of availability, matching adult/child sizes, inventory, delivery or checkout. Repeated card H3 elements are retained in the evidence, with a separate unique-title list. Facet product counters were excluded from count conclusions.

Browser limitation: the subagent's `cua.getState` inventory exposed Chrome only; creating a hidden IAB tab returned `Browser is not available: iab`. This limitation and the public HTTP fallback were communicated to the parent. No existing browser tab was selected or changed. GET requests used fresh urllib openers without CookieJar, Cookie headers, authentication, country/language selectors, forms, cart or checkout. Root's Microsoft tab was untouched.

Evidence: `landing_readback.json` preserves request/final/canonical URLs, timestamps, HTTP status, redirect traces, full-source SHA256, H1, product headings, unique product handles and main-text excerpts. `landing_group_1_main.txt` through `landing_group_8_main.txt` preserve parsed main text. `landing_check.py` reproduces the independent public reads. Local validation passed for all eight exact routes, language/alternate metadata and positive product-link counts.

Next action: root can use the verified `/pt` paths for target ads and sitelinks, while retaining campaign status and the separate native eligibility, market/shipping and tracking gates. This source check does not satisfy the attachment's requirement that receiving ad groups be active and eligible before conditional routing exclusions take effect.
