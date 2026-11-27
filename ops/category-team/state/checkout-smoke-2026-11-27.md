# Checkout smoke test, 2026-11-27

Scope: read-only purchase-path check, built-in browser pane, ship-to Spain / EUR (auto geo). No form field filled, nothing submitted; cart emptied after each route. No 429/403 seen.

Result: PASS on all 5 runs. No real break found.

| Route | Viewport | Product | Console errors | Cart | Checkout |
|---|---|---|---|---|---|
| EN `/` | desktop | /products/cream-heart-mommy-and-me-cardigans (Mother S) | only 401 on `/sf_private_access_tokens` (Shopify platform, benign) | drawer shows item, EUR 35,95, Check out visible | /checkouts/cn/.../en-es, contact/delivery form rendered, EUR 35.95, about 2 s |
| EN `/` | mobile 375 | same | same | drawer OK, Check out visible, total EUR 35,95 | /checkouts/.../en-es OK, EUR 35.95, about 3 s |
| SV `/sv` | mobile | /sv/products/argyle-wool-mommy-and-me-cardigans (Mamma M, colour Gra required) | same 401 only | drawer in Swedish, 63,95 EUR | /checkouts/.../sv-es in Swedish, 63,95 EUR, about 3 s |
| DE `/de` | mobile | /de/products/beanie-ghost-family-matching-pajamas (Mama S) | same 401 only | drawer in German, 38,95 EUR | /checkouts/.../de-es in German, 38,95 EUR, about 3 s |
| ES `/es` | mobile | /es/products/bamboo-garden-panda-cotton-mommy-and-me-pajamas (Mama S) | same 401 only | drawer in Spanish, 42,95 EUR | /checkouts/.../es-es in Spanish, 42,95 EUR, about 4 s |

Times are approximate (click to rendered form, polled by screenshot).

## Minor observations (not blockers)
- Mobile sticky bar: appears about 1 to 3 s after size selection / page load; before that the bottom of the screen shows nothing. Once visible it is not covered, and its Add button works with live total.
- Mobile sticky "Select size" button scrolls to the builder; the first click sometimes needed a second click (smooth scroll lag), one transient blank frame seen while the cart drawer opened (SV).
- ES cart drawer: variant line "Color: Panda en el jardin de bambu - c..." is truncated; a grey loading placeholder bar shows briefly above "Completa la familia".
- DE: `beanie-ghost-family-matching-pajamas` is a Halloween product still sold on 27 Nov (seasonal relevance, not a bug).
- Checkout shows EN-style price format `EUR 35.95` in en-es by design (Shopify checkout locale); SV/DE/ES use comma format.
- Browser pane had a pre-existing cart (2 x cream cardigan) at start; cleared it before testing. Cart is 0 at the end.
- Pane viewport emulation resets on navigation, so mobile was re-applied per route.

## Conclusion
Product page to checkout works in EN/SV/DE/ES on mobile and EN on desktop. The 9 carts / 0 checkouts signal is not explained by a theme break in this path; look at the shopper side (shipping cost reveal, express-pay only, trust) or tracking instead.
