# Phase 2 Remediation Report

Date: 2026-04-30

## Scope

Order followed:

1. PDP CLS/media behavior
2. Homepage image/LCP behavior
3. Search/collection CLS
4. Global render-blocking resources

## Theme Changes

- PDP: reserved product gallery dimensions from first paint by computing the tallest product media ratio in Liquid and applying critical gallery aspect-ratio CSS before the media carousel paints.
- Homepage: delayed hero autoplay until after initial load/idle, made below-hero category and curated-grid images lazy/low-priority, and preserved responsive `srcset` data after homepage image rotation.
- Collection/search: changed collection cards from `adapt` to `portrait`, removed a conflicting `850px` collection image rule, removed a global predictive-search positioning override, and added critical search-page predictive-search positioning.
- Global: gated `customer.css` to customer templates instead of loading it on every storefront page.

## Verification Summary

Theme Check:

- `shopify theme check --path .`
- Result: `252 files inspected with no offenses found.`

Local browser QA artifacts:

- Directory: `ops/reports/pagespeed-remediation-2026-04-30T103901-0400/browser/`
- Captured mobile and desktop screenshots, CLS/LCP observer data, image loading attributes, visible broken-image checks, horizontal overflow checks, and predictive-search interaction checks.

Local Lighthouse artifacts:

- Directory: `ops/reports/pagespeed-remediation-2026-04-30T103901-0400/lighthouse/raw/`
- Captured JSON and HTML reports for PDP, homepage, search, and best-sellers collection after remediation.

Key local after results:

| Surface | Check | Mobile | Desktop |
| --- | --- | ---: | ---: |
| PDP | Browser CLS | `0.0006` | `0.2602` local browser run, with desktop residual from header/product option timing |
| PDP | Lighthouse CLS | `0.003` | `0.083` |
| PDP | Lighthouse performance | `55` | `70` |
| Homepage | Browser LCP | `1.9s`, first hero image | `1.4s`, first hero image |
| Homepage | Browser CLS | `0.0003` | `0.039` |
| Search | Browser CLS after critical predictive CSS | `0.0003` | `0.054`, residual header/cookie banner |
| Search | Lighthouse CLS | `0.043` | `0.040` |
| Best-sellers collection | Browser CLS | `0.0002` | `0.038` |
| Best-sellers collection | Lighthouse CLS | `0.042` | `0.058` |

Notes:

- Local Lighthouse mobile can report simulated LCP much higher than observed LCP on the Shopify dev server because the local root document can be very large and slow under throttling. LCP discovery for the homepage hero passes: first hero image is eager, high priority, and discoverable in the initial document.
- Homepage curated-grid images appear as lazy placeholders in non-scrolled full-page screenshots, so a separate scroll-through check was captured. Visible lazy images loaded successfully with `0` broken visible images after scrolling.
- Local preview console/network noise is dominated by Shopify/app/analytics behavior on `127.0.0.1`, including CORS and aborted analytics requests; these were present in baseline-style captures and are not from the theme changes.

## Residual Risks / Next Targets

- Desktop CLS residuals are mostly header/logo/font/cookie-banner movement and some product option/card timing. Header critical sizing and announcement rotation should be handled in the next pass.
- Global CSS remains heavy: `theme-inline-body-static-01.css` through `09.css` still load as normal stylesheets. They need a careful page-by-page dependency audit before deferring or scoping to avoid FOUC/CLS.
- Full official PageSpeed API reruns for all canonical URLs were not part of this remediation pass. Use the existing resumable PSI runner once ready for a long batch.
