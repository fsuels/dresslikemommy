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

Shopify safety default:

- create or update a Shopify draft only
- do not set the product `ACTIVE`
- do not call `publishablePublish`
- do not publish to any sales channel unless the operator explicitly asks for a separate publish-live action

The agent should only stop for real blockers:

- size rows that cannot be mapped honestly
- conflicting garment/category evidence
- ambiguous `EXCLUDE_ITEMS`
- missing credentials/access after fallbacks
- destructive update/delete decisions that cannot be inferred safely

Family-matching default:

- if sizes already encode role/audience, collapse `Type` to the honest garment labels only, e.g. `Dress` and `Shirt`, instead of `Mother Dress`, `Father Shirt`, `Girl Dress`, `Boy Shirt`
- if the vendor selector lists separate garment choices such as `白色上衣` and `红色格子裤`, treat them as item Types, not Colors; expected options are `Type` x `Size` with values such as `Top` and `Pants`

Multi-color default:

- if `DESIGNS_TO_LIST` names multiple colors or colorways for the same garment and same size chart, create one Shopify product with a `Color` option containing those colorways
- do not split colorways into separate products unless the request explicitly says `separate listings` or `separate products`
- keep one size table per garment; multiply Shopify variants by `SIZE_CHART` rows x colorways
- do not use `Color` for separate purchasable garments, even when the vendor labels them under a translated "Color" selector

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

Expected option model for Example 3:

- `Type`: `Dress`, `Shirt`
- `Size`: role-bearing labels such as `Mother S`, `Father M`, `Child 2 Years`

## Example 4 — Two Dress Colors, One Product

```text
LISTING REQUEST

VENDOR_URL: https://detail.1688.com/offer/1234567890.html
SIZE_CHART_SOURCE: attached image
LISTING_MODE: Mommy and Me
PRIMARY_CATEGORY: Dresses
DESIGNS_TO_LIST: pink, white
EXCLUDE_ITEMS:
NOTES: same dress and same size chart in both colorways
PRICE_OVERRIDES:
SHORTCODE_OVERRIDE:
COLOR_TOKEN_OVERRIDE:
FORCE_SPEC_PRICES: true
```

Cost rule for every generated or updated Shopify variant:

- Cost per item is automatic and equals 50% of the current final Shopify variant price.
- The operator may manually set final prices in Shopify. Treat those manual prices as the source of truth.
- On create, use the generated/override price as the final price and set `inventoryItem.cost` to `price * 0.50`, rounded to cents.
- On update, rerun, or verification, first read the current live/draft variant price. Preserve that price unless the current request explicitly changes prices, then set Cost per item to `current price * 0.50`.
- In Shopify CSV backups, populate `Cost per item` from the row's final `Variant Price`.
- If any variant is missing stale Cost per item after verification, fix cost to 50% of the current price; do not reset the operator's manual price just to match an earlier generated spec.

Expected option model for Example 4:

- one Shopify product
- `Size`: role-bearing labels such as `Child 4 Years`, `Mother S`
- `Color`: `Pink`, `White`
- variants = every intended `Size x Color` combination

## Operator Reminder

The vendor size chart is still the source of truth. The point of this template is not to loosen accuracy. It is to remove repetitive operator work and let the agent infer what can be inferred safely.
