# Merchant Center Audit — Dress Like Mommy
**Store:** Dress Like Mommy (www.dresslikemommy.com)
**Catalog scanned:** 322 active products (all pages)
**Default policy applied:** brand = Dress Like Mommy · gender = female (adult) · GTIN policy = identifier_exists = false where no GTIN exists

---

## Executive summary

Dress Like Mommy's catalog has **five systemic issues** that are almost certainly driving the bulk of Merchant Center disapprovals. None of them require fixing products one at a time — every single one is a bulk fix. Each is listed below in the order it should be tackled, hardest impact first.

| # | Issue | Products affected | Bulk-fixable? |
|---|---|---:|---|
| 1 | `vendor` field contains a 1688.com / Taobao supplier URL — this is what's being sent as the brand | **70 / 322 (22%)** | Yes |
| 2 | `vendor` is `dresslikemommy.com` instead of `Dress Like Mommy` — Merchant Center treats lowercase domain text as a non-brand string | **213 / 322 (66%)** | Yes |
| 3 | No GTINs / barcodes on any of 489 sampled variants → identifier_exists=false must be set globally | **322 / 322 (100%)** | Yes — feed-side toggle |
| 4 | Variants on 59 products have null SKUs — required for unique offer IDs and item_group_id | **59 / 322 (18%)** | Yes |
| 5 | Mother + Father + Kids matching-set products are sent as one "unisex" feed item — Google can't classify them, must be split per role with shared item_group_id | **286 / 322 (89%)** | Requires a feed rule (not a Shopify edit) |

After those five fixes, the remaining work is small: 22 products have no featured image, 19 products have no color attribute on the product, 1 product has zero inventory but is still active, and 2 products have zero-priced variants.

---

## 1. Brand / vendor — the biggest single fix

The `vendor` field on a Shopify product becomes the `brand` attribute in the Google Merchant feed by default. Right now:

- **70 products** have a `vendor` value like `https://detail.1688.com/offer/553478499954.html`. That's a sourcing supplier link — when Google sees a URL in the brand field it disapproves the listing for "Generic / invalid brand."
- **213 products** have `vendor` = `dresslikemommy.com`. This is your domain name in lowercase, not a brand. Google treats this as inconsistent because your structured-data brand is "Dress Like Mommy" and the feed says "dresslikemommy.com".
- **39 products** already have `vendor` = `Dress Like Mommy`. Those are correct.

**Fix:** Set `vendor = "Dress Like Mommy"` on every active product. This is one bulk update.

A sample of the 70 products with URL-as-vendor (full list in `merchant_center_audit_per_product.csv`):

- Tropical Family Matching Outfits
- Tropical Vibes: Hawaiian Shirt and Floral Dress
- Backless Striped Jumpsuit
- Boho Chic Outfit - Flowy Skirts and Paisley Shirts
- Couple Matching Queen King Hearts T-shirts
- Cute Mother Daughter Matching Swimsuits
- Father and Child "Pilot & Co-Pilot" Matching T-Shirts
- Family Matching Denim Pink Casual Coat
- Mommy & Me Cherries Sweater Cardigan
- Mother & Daughter Matching Wool Sweater
- (… 60 more)

---

## 2. GTIN / MPN — set identifier_exists=false catalog-wide

Of 489 variants sampled across the catalog, **zero** had a barcode value. Dress Like Mommy is a private-label brand, so the correct treatment is:

- Don't fake GTINs.
- In Merchant Center → Diagnostics → "Missing GTIN," apply the rule **identifier_exists = false** for the whole feed.
- Where SKUs exist, they can be sent as `mpn`. (Shopify already maps SKU → mpn in the standard Google channel app feed.)

**Where this is set:**
- If you use the **Google & YouTube channel app** in Shopify → app settings → "Identifier exists" → set to "no" for the brand.
- If you use a **third-party feed** (DataFeedWatch, Simprosys, etc.) → add a feed rule: `identifier_exists = no` for all rows.

This single change clears the most common Merchant Center error message on this catalog.

---

## 3. Variant SKU coverage — 59 products affected

These products have null SKUs on every variant, which prevents item_group_id from working in the feed. A SKU-less variant publishes as an offer with no stable ID, which Google sometimes treats as a duplicate listing.

Top offenders (all have 5/5 variants missing SKUs):

- "Happy Flower" T-Shirts — Colorful Floral Print
- "Love Balloon" T-Shirt Set — Heart & Love Design
- "Love Grows" T-Shirts — Watering Can & Plant Design
- "LOVE" T-Shirt Set — Adorable Family Heart Design
- "Need More" Drink T-Shirt Set — Beer, Coffee, Milk
- "Original, Remix & Encore" T-Shirt Set
- "Plug & Lightbulb" T-Shirt Set
- Battery-Themed T-Shirt Set
- Beautiful Rainbow T-Shirts
- Colorful "I Love Family" Matching T-Shirts Set
- (… 49 more — see CSV)

**Fix:** Generate a SKU for every variant. Recommended pattern:
`DLM-<short-style-code>-<role>-<size>-<color>` (this matches the SKU pattern your newer 2026 products are already using, e.g. `DLM-WWFL-GRL-DRS-KID12Y-SAGE`).

I can generate the SKUs and apply them via update-product, but I want you to confirm you want me to overwrite null SKUs across all 59 products before I do.

---

## 4. Matching-set role splitting — the structural issue

286 of 322 products are matching sets that contain Mother + Father + Kids variants in a single Shopify product. The `target-gender` metaobject is being set to **Unisex** to accommodate this, and `age-group` lists Toddlers + Kids + Adults at once.

**Why this disapproves listings:** Merchant Center applies its policy filters per offer. An offer with "unisex / mixed-age" classification can't be matched to either the Women's or Kids' apparel taxonomy, and many countries (US/UK in particular) require a single gender + single age group for kids' apparel offers.

**Fix (feed-side, not Shopify-side):** In your Google channel app or feed-management tool, add three feed rules that split each matching-set product into separate feed items:

```
For each variant:
  if variant title contains "Mother" / "Mom" / "Women" → gender=female, age_group=adult
  if variant title contains "Father" / "Dad" / "Men"   → gender=male,   age_group=adult
  if variant title contains "Child"/"Kid"/"Boy"/"Girl"/"Baby" → infer gender from title, age_group from years
```

All variants from the same Shopify product share the same `item_group_id` (the product's handle is fine), so Google still understands they're one matching set.

If you want, I can write the Shopify Flow logic or the equivalent rules for Simprosys / DataFeedWatch — tell me which feed tool you use.

---

## 5. Smaller cleanup items

| Issue | Count | Notes |
|---|---:|---|
| `featuredMedia` is null (no main image) | 22 | Feed will fail with `image_link [missing]` until a primary image is set in Shopify |
| Product has no color metafield or color in tags | 19 | Add color via the `shopify.color-pattern` metafield or product tags |
| Variant price = 0.00 | 2 | These will fail "price [invalid]" on submission |
| Active product with totalInventory = 0 | 1 | Backless Striped Jumpsuit — set to draft or change feed availability to `out_of_stock` |
| GPC (google_product_category) missing | 3 | Most of the catalog has this set; only a handful are missing |

Full per-product flags are in `merchant_center_audit_per_product.csv`.

---

## What I can fix automatically vs. what needs you

**Bulk-applyable in Shopify right now (just say go):**
1. Set `vendor = "Dress Like Mommy"` on all 283 products that don't have it.
2. Set product status = `DRAFT` on the 1 zero-inventory product, or whatever you prefer.
3. Generate and apply SKUs for the 59 products with null variant SKUs (using the DLM-… pattern above).

**Needs the feed tool, not Shopify:**
4. Toggle `identifier_exists = no` for the catalog.
5. Apply the role-splitting feed rule for matching sets.

**Needs you to act in Shopify admin:**
6. Add a featured image to the 22 products that are missing one (I can list the specific products and you upload).
7. Replace zero-priced variants on the 2 affected products with real prices.

---

## Files

- `merchant_center_audit.md` — this report
- `merchant_center_audit_per_product.csv` — every product with its flags
- `merchant_center_audit_summary.json` — issue counts in JSON form

Tell me which fix you want me to start with and I'll apply it.
