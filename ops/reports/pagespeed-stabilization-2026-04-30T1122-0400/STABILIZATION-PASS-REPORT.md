# PageSpeed Stabilization Pass - Header, PDP, Cookie, Static CSS

Date: 2026-04-30
Preview theme: `134593970273`
Validated preview asset theme: `/cdn/shop/t/111/`

## Scope

- Ran live PageSpeed Insights API captures against preview URLs.
- Stabilized header/logo/font/cookie-banner CLS.
- Audited and gated global static CSS bundles by template.
- Reworked PDP description/size-guide timing after Lighthouse identified remaining CLS from late description and size-guide mutations.

## PSI API Artifacts

- Full preview inventory: `ops/reports/pagespeed-api-preview-2026-04-30T111322-0400/psi-targets-preview-theme-134593970273.csv`
  - `424` live preview URLs plus CSV header.
- Preview probe: `ops/reports/pagespeed-api-preview-2026-04-30T111322-0400/probe/psi-api-summary.csv`
  - Homepage mobile: performance `48`, CLS `0.192`.
  - Homepage desktop: performance `71`, CLS `0.116`.
- Critical after-stabilization batch: `ops/reports/pagespeed-stabilization-2026-04-30T1122-0400/psi/critical-after-stabilization/psi-api-summary.csv`
  - Homepage mobile: performance `37`, CLS `0.000`.
  - Homepage desktop: performance `67`, CLS `0.072`.
  - Collection desktop: performance `45`, CLS `0.006`.
  - Search desktop: performance `85`, CLS `0.032`.
  - Mobile collection/product and desktop product/search had PSI service 500 or request timeout rows; the runner now records those instead of crashing.
- Final desktop CLS mini-batch: `ops/reports/pagespeed-stabilization-2026-04-30T1122-0400/psi/final-desktop-cls-check/psi-api-summary.csv`
  - Homepage desktop: performance `74`, CLS `0.008`.
  - Search desktop: performance `72`, CLS `0.001`.
- Final PDP PSI retry: `ops/reports/pagespeed-stabilization-2026-04-30T1122-0400/psi/product-after-sizeguide-reserve/psi-api-summary.csv`
  - Product desktop: performance `63`, CLS `0.034`.

## Browser And Lighthouse Results

- Direct browser PDP observer after final size-guide reserve: CLS about `0.005`.
- Final PDP local Lighthouse desktop:
  - Report: `ops/reports/pagespeed-stabilization-2026-04-30T1122-0400/lighthouse/raw/desktop_product_final_after_defer_sizeguide_reserve.report.json`
  - Performance `75`, CLS `0.026`, LCP `2434ms`, TBT `0ms`.
- Prior final local Lighthouse desktop checks:
  - Homepage: performance `79`, CLS `0.000`, LCP `2521ms`, TBT `0ms`.
  - Search: performance `78`, CLS `0.000`, LCP `2515ms`, TBT `3ms`.

## Changes Made

- Header and announcement bar now reserve logo, nav, icon, and announcement dimensions before late CSS/font swaps.
- Body bold font is preloaded when distinct from existing regular/header fonts.
- Shopify privacy/cookie banner gets a visible-state height guard and is removed when not needed.
- Homepage hero CTA final styling is emitted early to prevent a late button restyle.
- Product description CSS moved into the PDP section flow, and `product-description.js` can initialize immediately when the description markup already exists.
- PDP matching-size guide now reserves the final snapshot/details space in initial markup when the product has a size-table source.
- Hidden PDP share controls are hidden in the critical PDP CSS before they can take space.
- Body static CSS bundles are template-gated:
  - `01`: collection/search.
  - `02`: product.
  - `03`: product/collection.
  - `04`: product.
  - `05`, `06`, `08`: global for now.
  - `07`: collection.
  - `09`: product.
- PSI runner now catches request timeouts/URL errors and writes failed rows.

## Verification

- `shopify theme check --path .`: pass, `252 files inspected with no offenses found`.
- `node --check assets/product-description.js`: pass.
- `python3 -m py_compile ops/scripts/run_pagespeed_api_batch.py`: pass.
- `git diff --check`: pass.
- Browser screenshots saved in `ops/reports/pagespeed-stabilization-2026-04-30T1122-0400/browser/screenshots/`.

## Residual Risks

- Live PSI preview URLs include Shopify preview/debug behavior and can differ from a published live run.
- PSI mobile requests were intermittently unstable, returning Google Lighthouse service `500` or socket timeout rows.
- Product desktop CLS is now good (`0.034` PSI, `0.026` local Lighthouse), but not literally `0.000`; the remaining local Lighthouse culprit is the color-image fieldset near the viewport edge.
- `theme-inline-head-static-02.css` and the remaining global body statics `05`, `06`, and `08` are still audit candidates for later scoping, but were left global where cart/header/footer risk was higher.
