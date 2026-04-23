# Shopify Listing From 1688 — Quick Start (Minimal Input)

This is the lightweight request template that pairs with [`ops/prompts/shopify-listing-master-prompt.md`](/Users/fsuels/Projects/dresslikemommy/ops/prompts/shopify-listing-master-prompt.md).

## How To Use It

1. Keep the master prompt as the standing operator prompt.
2. For each new vendor product, attach the vendor size chart and any useful product images.
3. Paste one `LISTING REQUEST` block like the examples below.
4. Leave fields as `auto` unless you want to force a decision.

## Copy-Paste Template

```text
LISTING REQUEST

VENDOR_URL:
SIZE_CHART_SOURCE: attached image
LISTING_MODE: Mommy and Me | Daddy and Me | Family Matching
PRIMARY_CATEGORY: auto
DESIGNS_TO_LIST: auto
EXCLUDE_ITEMS:
NOTES:
PRICE_OVERRIDES:
SHORTCODE_OVERRIDE:
COLOR_TOKEN_OVERRIDE:
FORCE_SPEC_PRICES: true
```

## What The Agent Should Infer By Default

If you leave a field blank or `auto`, the agent should infer:

- roles allowed by `LISTING_MODE`
- the actual roles the vendor sells
- the per-role garment
- category and taxonomy
- title, SEO, tags, body copy, metafields
- handle, shortcode, color token
- pricing from nearby live products, then fallback matrix if needed
- which vendor rows belong in variants

The agent should only stop for real blockers:

- size rows that cannot be mapped honestly
- conflicting garment/category evidence
- ambiguous `EXCLUDE_ITEMS`
- missing credentials/access after fallbacks
- destructive update/delete decisions that cannot be inferred safely

## Example 1 — Mommy and Me Dresses

```text
LISTING REQUEST

VENDOR_URL: https://detail.1688.com/offer/1234567890.html
SIZE_CHART_SOURCE: attached image
LISTING_MODE: Mommy and Me
PRIMARY_CATEGORY: Dresses
DESIGNS_TO_LIST: auto
EXCLUDE_ITEMS:
NOTES: floral mother-daughter listing; use the cleanest summer-facing print name
PRICE_OVERRIDES:
SHORTCODE_OVERRIDE:
COLOR_TOKEN_OVERRIDE:
FORCE_SPEC_PRICES: true
```

## Example 2 — Daddy and Me Shirts

```text
LISTING REQUEST

VENDOR_URL: https://detail.1688.com/offer/1234567890.html
SIZE_CHART_SOURCE: attached image
LISTING_MODE: Daddy and Me
PRIMARY_CATEGORY: Tops
DESIGNS_TO_LIST: auto
EXCLUDE_ITEMS:
NOTES: vendor may show pants too; list shirts only
PRICE_OVERRIDES:
SHORTCODE_OVERRIDE:
COLOR_TOKEN_OVERRIDE:
FORCE_SPEC_PRICES: true
```

## Example 3 — Family Matching Mixed Garments

```text
LISTING REQUEST

VENDOR_URL: https://detail.1688.com/offer/1032088497889.html
SIZE_CHART_SOURCE: attached image
LISTING_MODE: Family Matching
PRIMARY_CATEGORY: FamilySet
DESIGNS_TO_LIST: auto
EXCLUDE_ITEMS: shorts, pants
NOTES: girls + mothers wear dresses; boys + fathers wear shirts; keep the listing family-first and photo-ready
PRICE_OVERRIDES:
SHORTCODE_OVERRIDE: VCF
COLOR_TOKEN_OVERRIDE: CREAM
FORCE_SPEC_PRICES: true
```

## Operator Reminder

The vendor size chart is still the source of truth. The point of this template is not to loosen accuracy. It is to remove repetitive operator work and let the agent infer what can be inferred safely.
