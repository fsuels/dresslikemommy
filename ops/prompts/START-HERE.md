# START HERE — Shopify Listing Workflow

Use this file as the first stop for any new session that needs to create or update Shopify product listings from vendor pages, size charts, screenshots, or dropship source material.

## Read In This Order

1. [`shopify-listing-master-prompt.md`](/Users/fsuels/Projects/dresslikemommy/ops/prompts/shopify-listing-master-prompt.md)
2. [`shopify-listing-from-1688.md`](/Users/fsuels/Projects/dresslikemommy/ops/prompts/shopify-listing-from-1688.md)

## What Each File Does

- `shopify-listing-master-prompt.md`
  The canonical operator spec. It contains the rules, guardrails, category mapping, size-chart contract, pricing logic, metafield expectations, channel publication steps, and verification requirements.
- `shopify-listing-from-1688.md`
  The minimal-input request template. This is the small block the operator fills in for each new product.

## Default Rule

For new listing work, prefer the `ops/prompts/` workflow over older prompt files under `GPT/` unless the user explicitly asks for a legacy prompt.

Family-matching sanity check: if `Size` labels already encode the shopper role (`Mother S`, `Father M`, `Child 2 Years`), keep `Type` generic to the garment (`Dress`, `Shirt`) instead of repeating the role in the option value.

Colorway sanity check: if `DESIGNS_TO_LIST` names multiple colorways or print colors for the same garment and vendor size chart, keep them in one Shopify product with a `Color` option. Do not create separate products unless the operator explicitly says "separate listings" or the vendor evidence shows materially different garments or size charts.

## Minimal Request Template

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

## Fresh-Session Instruction

If you are starting a new session and the task is listing-related:

- read this file first
- then read the two canonical prompt files above
- then execute the listing workflow from those files
- document any deviation in `ops/AGENT_WORKLOG.md`
