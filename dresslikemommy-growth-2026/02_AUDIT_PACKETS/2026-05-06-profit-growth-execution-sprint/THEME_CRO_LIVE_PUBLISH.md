# Theme CRO Live Publish - 2026-05-06

## Scope Approved

Owner approval phrase:

`APPROVE PUBLISH THEME CRO PREVIEW 134923321441 LIVE; NO SHOPIFY PRODUCT, FEED, ADS, PIXEL, CAMPAIGN, BUDGET, BID, PRODUCT SCOPE, OR CONVERSION-GOAL CHANGES.`

## Result

- Published theme `134923321441` live.
- Live theme is now: `134923321441 | DLM CRO Preview 2026-05-06 | live`
- Previous live theme is now: `133290917985 | dresslikemommy/main | unpublished`
- Live storefront: `https://dresslikemommy-com.myshopify.com`
- Public storefront verified: `https://www.dresslikemommy.com`

## Commands

- `shopify theme list --json`
- `shopify theme publish --theme 134923321441 --force --no-color`
- `shopify theme list --json`
- `curl -L -s --max-time 20 'https://www.dresslikemommy.com/' | rg -n 'Matching looks for the moments families remember most|Shipping options shown at checkout|Mommy & Me|Mother-daughter favorites' | head -50`
- `curl -L -s --max-time 20 'https://www.dresslikemommy.com/products/red-resort-mommy-and-me-set' | rg -n 'Build your matching set|Optional: choose one size|Shipping options shown at checkout|Shipping Options' | head -50`

## Pre-Publish Readback

- `133290917985 | dresslikemommy/main | live`
- `134923321441 | DLM CRO Preview 2026-05-06 | unpublished`

## Publish Output

Shopify CLI reported:

`The theme 'DLM CRO Preview 2026-05-06' (#134923321441) is now live at https://dresslikemommy-com.myshopify.com.`

## Post-Publish Readback

- `134923321441 | DLM CRO Preview 2026-05-06 | live`
- `133290917985 | dresslikemommy/main | unpublished`

## Live Storefront Verification

Homepage live readback found:

- `Matching looks for the moments families remember most`
- `Shop Mommy & Me`
- `Shipping options shown at checkout`
- `Mother-daughter favorites`

PDP live readback for `/products/red-resort-mommy-and-me-set` found:

- `Build your matching set`
- `Optional: choose one size for each family member you want to include. Each selection adds one separate piece to cart.`
- `Shipping options shown at checkout`

## Guardrails Preserved

- No Shopify product edits.
- No feed or Merchant Center edits.
- No Google Ads edits.
- No Pinterest Ads edits.
- No pixel/tag edits.
- No campaign status, budget, bid, product-scope, product-group, feed-label, or conversion-goal changes.

## Rollback Note

The previous live theme remains available as unpublished theme `133290917985 | dresslikemommy/main`.
