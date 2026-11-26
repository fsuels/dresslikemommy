# PageSpeed mobile, 2026-11-26 (PSI API, mobile strategy; after = best of 2 runs)

Raw: `ops/organic/receipts/2026-11-26/pagespeed-before.json` and `pagespeed-after.json`.

| URL | Score | LCP | CLS | TBT | Page weight |
|---|---|---|---|---|---|
| / | 85 -> 87 | 4.2 -> 4.1 s | 0.007 -> 0.007 | 0 -> 0 ms | 2.87 -> 3.05 MB |
| /collections/christmas-sweaters | 78 -> 77 | 5.9 -> 6.3 s | 0.004 -> 0.003 | 10 -> 0 ms | 3.83 -> 3.77 MB |
| /collections/mommy-and-me | 60 -> 83 | 5.5 -> 4.6 s | 0.000 -> 0.000 | 739 -> 20 ms | 3.10 -> 3.32 MB |
| /products/nordic-yoke-family-matching-sweaters | 68 -> 62 | 5.5 -> 5.1 s | 0.097 -> 0.102 | 216 -> 428 ms | 2.78 -> 2.76 MB |
| /products/christmas-reindeer-family-matching-sweaters | 71 -> 76 | 5.0 -> 5.1 s | 0.090 -> 0.102 | 202 -> 96 ms | 2.56 -> 2.63 MB |
| /es/collections/mommy-and-me | 62 -> 82 | 4.4 -> 4.9 s | 0.003 -> 0.030 | 652 -> 0 ms | 3.12 -> 3.23 MB |

## Measured before (what drives the score)
- LCP: home = hero image (already eager + fetchpriority high + preloaded); collections = first product card image (no priority hint); product pages = main photo (already preloaded, high priority).
- Render-blocking CSS: about 1 s estimated on every page, from ~15 small stylesheets (base.css, static head files, dlm-header, cart drawer, localization form, ...), each its own request.
- Images: 260-850 KiB estimated savings per page (PNG product photos at card size).
- Product pages: CLS 0.09 (product info column shifts while page scripts run in the throttled lab; not reproducible in a normal browser), main-thread script time 2.4 s, of which Shopify's event-observer-collector 0.94 s (not ours) and inline/page script 0.93 s.

## Changed
1. 2aae907 `snippets/card-product.liquid`: eager (first two) card images get fetchpriority high. `sections/header.liquid`: cart drawer CSS made non-blocking.
2. 68fb285 `assets/dlm-delivery-dates.js`, `assets/dlm-holiday-order-by.js`: page watchers coalesce DOM changes (one pass per burst); dates unchanged.
3. de3a366 REVERT of the drawer CSS part of (1): PSI measured CLS 1.007 on home and christmas-sweaters (score 55/50) because the hidden drawer showed unstyled until its CSS arrived. The card image priority stays.

## Left alone
- Hero/product LCP images: already preloaded and high priority.
- Combining or deferring the ~15 head stylesheets: large risk of unstyled flashes (see the revert); needs a visual test per template.
- PNG photos: Shopify serves WebP/AVIF by negotiation; the remaining saving is the source compression (photo workflow, not theme).
- Shopify event-observer-collector, Judge.me, Bing Ads: third-party/platform, not to be removed.
- Product CLS 0.10: cannot be reproduced outside the throttled lab; borderline "good".

## Reading the after numbers
PSI run-to-run noise is large (TBT swung 739 -> 20 ms on a page whose scripts did not change; LCP moves by 0.4-0.5 s between identical runs). Only mommy-and-me (60 -> 83) and es mommy-and-me (62 -> 82) improved beyond that noise, mostly through TBT; LCP changes are inside the noise band. No reliable LCP gain is claimed.
