BukitDrop import autofill handoff

Recommended browser-side setup:

1. Create a trigger for newly imported Shopify products.
   - Preferred: Shopify Flow `Product created`
   - Filter if needed to only BukitDrop imports using vendor, tag, or another import marker.

2. Pass the created product id into the repo-side autofill script.
   - Script:
     `/Users/fsuels/Projects/dresslikemommy/ops/scripts/autofill_shopify_import_product.py`
   - Command:
     `python3 /Users/fsuels/Projects/dresslikemommy/ops/scripts/autofill_shopify_import_product.py --product-id <SHOPIFY_PRODUCT_ID> --execute`

3. If the browser-side automation cannot execute shell commands directly:
   - send the product id to the operator automation layer that can run the command above
   - or tag the product for queue processing and run the same script from that queue

What the script does:

- reads one live Shopify product by id or handle
- infers missing custom taxonomy fields:
  - `custom.category1`
  - `custom.subcategory`
  - `custom.subcategory2`
  - `custom.type`
  - `custom.style`
  - `custom.pattern`
- fills blank `productType`
- fills blank/generic Shopify category from live peer products in the store
- fills missing Shopify apparel metafields:
  - `shopify.target-gender`
  - `shopify.age-group`
  - `shopify.size`
  - `shopify.color-pattern`

Important behavior:

- dry-run is default; `--execute` is required for live writes
- existing populated fields are left alone
- category/product type/custom taxonomy updates run before apparel metafields
- apparel writes only run when a valid Shopify metaobject mapping exists

Dry-run example:

`python3 /Users/fsuels/Projects/dresslikemommy/ops/scripts/autofill_shopify_import_product.py --product-id <SHOPIFY_PRODUCT_ID>`
