# PDP Collection Image Parity Report

Date: 2026-05-13

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-13-pdp-collection-image-parity-live`

## Problem

Collection cards render the product image from `product.featured_media`, but the PDP gallery started from `product.selected_or_first_available_variant.featured_media`. On products where the first available variant has its own image, a normal collection-card click could land on a different first PDP image than the shopper just clicked.

## Change

Updated `snippets/product-media-gallery.liquid` so normal product-page loads start with `product.featured_media`, matching `snippets/card-product.liquid`.

Explicit variant URLs still honor the selected variant image:

- `?variant=...` with variant media uses `product.selected_variant.featured_media`.
- Products without product-level featured media still fall back to the selected-or-first available variant media.

No Shopify Admin product images, product data, checkout settings, Ads, Merchant, Pinterest, or GA4/GTM actions were changed.

## Verification

Commands run:

- `git diff --check -- snippets/product-media-gallery.liquid ops/AGENT_COORDINATION.md ops/PROBLEM_TRACKER.md`
- `shopify theme check --path . --fail-level error --output json`
- `shopify theme dev --host 127.0.0.1 --port 9292 --live-reload off`
- `shopify theme push --theme 133290917985 --only snippets/product-media-gallery.liquid --allow-live`
- Local Nokogiri readback against `http://127.0.0.1:9292/collections/mommy-and-me`
- Live curl/Nokogiri readback against `https://www.dresslikemommy.com/collections/mommy-and-me`

Results:

- Theme Check returned `[]`.
- Scoped `git diff --check` returned no whitespace errors.
- Local collection-to-PDP readback checked the first five `mommy-and-me` product cards and all passed.
- Scoped live push to theme `dresslikemommy/main` `#133290917985` succeeded for only `snippets/product-media-gallery.liquid`.
- Live collection-to-PDP readback checked the first five `mommy-and-me` product cards and all passed.
- Variant deep-link guard passed locally and live on `golden-daisy-mommy-and-me-set?variant=44197959270497`.

Collection-to-PDP readback:

| # | Result | Product | Collection card image | PDP first image |
|---|---|---|---|---|
| 1 | PASS | Golden Daisy Mommy & Me Matching Separates | `ChatGPT_Image_May_8_2026_01_07_21_AM.png` | `ChatGPT_Image_May_8_2026_01_07_21_AM.png` |
| 2 | PASS | Scarlet Ruffle Mommy and Me Tank Top - Breezy Beach Top | `ChatGPT_Image_May_6_2026_03_15_05_AM.png` | `ChatGPT_Image_May_6_2026_03_15_05_AM.png` |
| 3 | PASS | Pastel Watercolor Mommy and Me Dresses - Airy Layered Look | `ChatGPT_Image_Apr_27_2026_11_55_56_AM.png` | `ChatGPT_Image_Apr_27_2026_11_55_56_AM.png` |
| 4 | PASS | Fairy Tale Messenger Mommy and Me Pajamas — Short-Sleeve Set | `ChatGPTImageApr22_2026_04_03_25PM.png` | `ChatGPTImageApr22_2026_04_03_25PM.png` |
| 5 | PASS | Red Resort Mommy and Me Set - Tee and Skirt | `ChatGPT_Image_May_6_2026_02_42_13_AM.png` | `ChatGPT_Image_May_6_2026_02_42_13_AM.png` |

## Residual Risk

Browser automation MCPs were blocked by profile locks, so the customer-path verification used live HTML readbacks with browser-like request headers instead of an interactive screenshot. The first active PDP gallery media and collection-card media matched in the rendered live HTML.
