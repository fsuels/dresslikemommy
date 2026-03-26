# SEO Priority Worklist

Date: 2026-03-25

## P0: Repair Broken Live Product Titles

Evidence:
- `ops/seo/product_title_repair_plan.csv` contains `164` planned repairs.
- Live examples still showing broken titles:
  - `/products/battery-themed-matching-family-t-shirt-set-super-tired-parents-energetic-kids`
  - `/products/chic-color-block-one-piece-swimsuit-for-mother-daughter-vibrant-sleek-beachwear`

Why this is first:
- It affects organic CTR, product-page relevance, and Google Merchant Center / free listings quality at the same time.
- These broken titles are already live on indexed product pages.

Execute when Shopify Admin API credentials are available:

```bash
export SHOPIFY_STORE_DOMAIN='dresslikemommy-com.myshopify.com'
export SHOPIFY_ADMIN_ACCESS_TOKEN='...'
python3 ops/scripts/repair_product_titles.py \
  --plan-csv ops/seo/product_title_repair_plan.csv \
  --execute
```

Suggested safe rollout:
1. `--max-updates 25`
2. Verify live titles
3. Run the full execute pass

## P1: Replace Generic Theme Fallbacks With Hand-Written Collection SEO

These collection pages now have theme-level fallback SEO, but they still need custom admin copy for best rankings and CTR.

Highest-priority collection handles:
- `couples`
- `daddy-me`
- `family-swimsuits`
- `family-sets`
- `dresses`
- `maternity`
- `new-arrivals`
- `family-tops`
- `family-sweaters`
- `tops`
- `pajamas`
- `sweaters`
- `daddy-me-t-shirts`
- `christmas-pajamas`
- `christmas-sweaters`

Why these first:
- They are surfaced repeatedly from the homepage navigation and collection cards.
- Several were confirmed to be missing custom collection descriptions/meta before the theme fallback pass.

Admin standard for each priority collection:
- Unique SEO title
- Unique meta description
- 100-200 words of useful intro copy
- Clear audience + occasion intent in the copy

## P2: Fix Product Feed Data Gaps That Limit Merchant Center Quality

Among active published products from `products_export_1 2.csv`:
- Active published products: `283`
- Missing Google product category: `283`
- Missing MPN: `283`
- Missing any barcode across variants: `193`
- Missing type: `90`

Why this matters:
- Google can infer some attributes, but cleaner structured product data improves feed quality, approval stability, and query matching.

## P3: Clean Up Weak Product Meta Snippets

Theme work completed:
- Product pages with blank or junk auto descriptions such as `SPECIFICATIONS ...` now use a cleaner fallback meta description in theme code.

Still worth doing in admin:
- Write custom product SEO descriptions for the highest-conversion SKUs instead of relying on fallback text.

## P4: Reviews on Revenue Pages

Current export signal:
- Missing review count metafield on active published products: `282` of `283`

Why this matters:
- Reviews improve conversion directly.
- Richer review coverage also strengthens product trust signals in search and shopping surfaces.

Best candidates:
- Best sellers
- Mommy and Me hero products
- Family matching pajamas
- Swimwear collections before season peaks

