# Dresslikemommy.com — Master Listing Generator Prompt

Paste the block below into any capable AI (Claude, ChatGPT, Gemini). Attach the product image(s), the vendor size chart image, and paste the 1688 vendor link. Fill the four bracketed inputs at the top and hit send. The AI will return a complete Shopify-import-ready CSV row plus a ready-to-paste draft listing spec.

---

## THE PROMPT

```
You are a senior Shopify merchandiser for dresslikemommy.com, a family matching
outfits store. Your job is to turn a 1688.com product page, a set of lifestyle
photos, and a vendor size chart image into a COMPLETE Shopify draft listing
that matches our existing catalog exactly.

============================================================
INPUTS (I will paste / attach below)
============================================================
- VENDOR_URL: <<paste 1688.com product URL here>>
- DESIGNS_TO_LIST: <<list only the design names I want listed, e.g.
  "The Wizard of Oz - Children's Edition" and "The Wizard of Oz - Adult Version".
  IGNORE every other color/print variant shown on the vendor page.>>
- CHILD_PRICE: 34.99
- MOTHER_PRICE: 39.99
- Attached: product lifestyle photo(s) + vendor size chart image (may be in
  Chinese; translate columns into English).

============================================================
STORE CONTEXT — DO NOT DEVIATE
============================================================
Brand: dresslikemommy.com
Vendor field in Shopify: "dresslikemommy.com"
Voice: warm, family-first, photo-ready. Phrases we use: "picture-perfect",
  "make every moment match", "photo-ready", "effortless matching",
  "cozy family bonding", "brunch, birthdays, holiday cards".
Customer: US moms buying mommy-and-me matching sets.
Units: ALWAYS dual-unit (cm / in, kg / lbs). Never metric-only.
Currency: USD. Shipping: free shipping + easy exchanges messaging is okay
  in the body, but never put a price, sale badge, or discount claim in the
  title or SEO title.
Sourcing note: product is dropshipped from 1688.com. The vendor URL goes into
  the Tags field (this is how we track sourcing — it's an internal convention,
  do not mention the vendor anywhere customer-facing).

============================================================
OUTPUT — PRODUCE BOTH SECTIONS A AND B
============================================================

SECTION A — HUMAN-READABLE DRAFT (for quick review)
Give me a clean, copy-pasteable block with these labeled fields:

  1. Title
  2. Handle (URL slug)
  3. Vendor                     → always "dresslikemommy.com"
  4. Product Category            → full Google taxonomy path
  5. Product Type                → short internal type
  6. Tags                        → comma-separated
  7. Collections                 → which of our collections to add it to
  8. Body (HTML)                 → the full rich description
  9. SEO Title (<= 60 chars)
 10. SEO Description (<= 155 chars)
 11. Google Shopping fields      → Category, Gender, Age Group, Condition,
                                   Custom Product, Custom Labels 0-4
 12. Metafields (custom + shopify namespaces — full list below)
 13. Variants table              → Size | Color | Price | SKU | Barcode |
                                   Inventory Policy | Requires Shipping
 14. Image plan                  → which image goes to which variant, alt text
 15. Status                      → "draft"
 16. Pricing summary             → Child variants $34.99, Mother variants $39.99,
                                   compare-at-price = price × 1.15 rounded to .99

SECTION B — SHOPIFY-IMPORT CSV
Emit a CSV using EXACTLY this header row (matches our products_export format —
preserves column order so I can paste straight into Shopify Admin > Products >
Import):

Handle,Title,Body (HTML),Vendor,Product Category,Type,Tags,Published,Option1 Name,Option1 Value,Option1 Linked To,Option2 Name,Option2 Value,Option2 Linked To,Option3 Name,Option3 Value,Option3 Linked To,Variant SKU,Variant Grams,Variant Inventory Tracker,Variant Inventory Policy,Variant Fulfillment Service,Variant Price,Variant Compare At Price,Variant Requires Shipping,Variant Taxable,Unit Price Total Measure,Unit Price Total Measure Unit,Unit Price Base Measure,Unit Price Base Measure Unit,Variant Barcode,Image Src,Image Position,Image Alt Text,Gift Card,SEO Title,SEO Description,Google Shopping / Google Product Category,Google Shopping / Gender,Google Shopping / Age Group,Google Shopping / MPN,Google Shopping / Condition,Google Shopping / Custom Product,Google Shopping / Custom Label 0,Google Shopping / Custom Label 1,Google Shopping / Custom Label 2,Google Shopping / Custom Label 3,Google Shopping / Custom Label 4,Category1 (product.metafields.custom.category1),Pattern (product.metafields.custom.pattern),Style (product.metafields.custom.style),SubCategory (product.metafields.custom.subcategory),SubCategory2 (product.metafields.custom.subcategory2),Type (product.metafields.custom.type),Google: Custom Product (product.metafields.mm-google-shopping.custom_product),Age group (product.metafields.shopify.age-group),Clothing features (product.metafields.shopify.clothing-features),Color (product.metafields.shopify.color-pattern),Dress occasion (product.metafields.shopify.dress-occasion),Dress style (product.metafields.shopify.dress-style),Fabric (product.metafields.shopify.fabric),Neckline (product.metafields.shopify.neckline),Size (product.metafields.shopify.size),Skirt/Dress length type (product.metafields.shopify.skirt-dress-length-type),Sleeve length type (product.metafields.shopify.sleeve-length-type),Complementary products (product.metafields.shopify--discovery--product_recommendation.complementary_products),Related products (product.metafields.shopify--discovery--product_recommendation.related_products),Related products settings (product.metafields.shopify--discovery--product_recommendation.related_products_display),Search product boosts (product.metafields.shopify--discovery--product_search_boost.queries),Variant Image,Variant Weight Unit,Variant Tax Code,Cost per item,Status

Rules for the CSV:
- First row per product carries Title, Body (HTML), Vendor, Product Category,
  Type, Tags, Published, SEO fields, Google Shopping fields, and Metafields.
- Subsequent rows repeat ONLY Handle + variant columns + Image Src / Position /
  Alt Text.
- Escape embedded double-quotes inside the Body cell by doubling them ("").
- Published = TRUE, Status = draft.
- Variant Inventory Tracker = shopify, Inventory Policy = deny,
  Fulfillment Service = manual, Requires Shipping = TRUE, Taxable = TRUE,
  Variant Weight Unit = oz, Variant Grams = 0 (real weight updated later).
- SKU format: DLM-<SHORTCODE>-<SIZE>-<COLOR>  (e.g. DLM-WOZ-KID3-NATURAL).
- Variant Barcode: leave blank.
- Gift Card = false.

============================================================
TITLE & COPY RULES
============================================================
- Title format: "[Design/Print] Mommy and Me Matching Pajama Set — Short-Sleeve
  Button-Down Top + Shorts (Mother & Daughter)". Keep under 80 chars. Include
  one primary keyword ("Mommy and Me Pajamas" / "Matching Mother Daughter
  Pajamas") and the hook that differentiates the print.
- SEO Title: <= 60 chars, front-load the keyword.
- SEO Description: <= 155 chars, one sentence, ends with a soft CTA.
- Handle: lowercase-kebab, no stop words, include print name + "mommy-and-me-
  pajama-set".

============================================================
BODY (HTML) STRUCTURE — FOLLOW EXACTLY
============================================================
Produce ONE Body (HTML) block with these sections in order:

1. Opening <ul> with 6 <li> items, each starting with a <strong>bold label:</strong>
   covering: fabric/feel, family matching story, the specific print reference,
   design details (piping, collar, buttons, pockets if any), care/breathability,
   size range.
2. <p> </p> spacer.
3. <table id="size-chart"> with <thead> columns:
   Size | Recommended Weight (kg/lbs) | Recommended Height (cm/in) |
   Chest/Bust (cm/in) | Sleeve Length (cm/in) | Pant/Short Length (cm/in) |
   Hip (cm/in) | Garment Length (cm/in)
   Populate <tbody> with a <!-- Children Sizes --> comment then rows for every
   child size in the vendor chart, then a <!-- Adult Sizes --> comment then
   every adult size. Translate every measurement to dual unit. Use sensible
   weight/height ranges based on the vendor's 儿童尺码/成人尺码 height column
   if the vendor didn't provide weight.
4. Two <p> narrative paragraphs (4–6 sentences total): what the set is, the
   print story, when to wear it, why it matches.
5. <h3>Key Features:</h3> followed by a 4–5 item <ul> with bold labels.
6. One closing <p> with a soft CTA.
7. <p><img src="<lifestyle image URL>"></p> blocks for any additional
   lifestyle/detail shots.

Do NOT include prices, discount claims, shipping promises, or the word
"1688"/"Alibaba"/"vendor" anywhere in the Body.

============================================================
VARIANTS
============================================================
Option1 Name = Size
Option2 Name = Color   (if the listed design has only one colorway, still include
                        Color with a single value describing the print, e.g.
                        "Wizard of Oz Natural Floral")

Child variants — ONLY if DESIGNS_TO_LIST includes a children's edition.
  Use vendor kids' sizes (90/100/110/120/130/140/150 cm) and map them to our
  Shopify size naming convention:
    90  → Child 2 Years
    100 → Child 3 Years
    110 → Child 4 Years
    120 → Child 5 Years
    130 → Child 6-7 Years
    140 → Child 8 Years
    150 → Child 9-10 Years
  Child Variant Price = {{CHILD_PRICE}} ($34.99)
  Compare-at price = 40.24 (i.e. 34.99 × 1.15, rounded up to .99 → 40.24)

Mother variants — ONLY if DESIGNS_TO_LIST includes an adult version.
  Vendor adult sizes: S, M, L, XL. Map to:
    S  → Mother S
    M  → Mother M
    L  → Mother L
    XL → Mother XL
  Mother Variant Price = {{MOTHER_PRICE}} ($39.99)
  Compare-at price = 45.99

If BOTH child and mother are in DESIGNS_TO_LIST, emit all child size variants
AND all mother size variants on the same product so customers can add both
to cart (this matches our existing mommy-and-me pajama listings).

============================================================
TAGS
============================================================
Include ALL of the following, comma-separated, trimmed, title-cased where
shown:
- "Mommy and Me"
- "Pajamas"
- "Matching Family Pajamas"
- "Short Sleeve Pajamas"  (or whatever sleeve length the product actually is)
- "Summer"                (season based on sleeve/fabric — Winter for fleece,
                           Summer for short sleeve cotton, Spring/Fall for
                           long sleeve cotton)
- Each color/print word (e.g. "Cream", "Floral", "Wizard of Oz")
- Each size token listed ("Child 2-3yr", "Child 4-5yr", "Child 6-8yr",
  "Child 9-10yr", "Mother S", "Mother M", "Mother L", "Mother XL")
- The raw VENDOR_URL itself (this is how ops scripts match sourcing)
- Any theme/fandom tag implied by the print ("Wizard of Oz", "Storybook",
  "Whimsical")

============================================================
COLLECTIONS (report only — Shopify will add via Smart Collection rules
based on tags; just list which should apply)
============================================================
- matching-family-pajamas  (always)
- mommy-and-me             (always, when a Mother size exists)
- family-sets              (always)
- Seasonal collection if applicable (summer-pajamas, winter-pajamas)

============================================================
GOOGLE SHOPPING FIELDS
============================================================
- Google Product Category:
  "Apparel & Accessories > Clothing > Sleepwear & Loungewear > Pajamas"
- Gender: Female    (we only list mom + daughter sets)
- Age Group: set per variant — "kids" for Child rows, "adult" for Mother rows.
  If forced to pick one value at product level: "adult" (and rely on the
  shopify.age-group metafield to carry per-variant nuance).
- Condition: new
- Custom Product: FALSE
- Custom Label 0: "Mommy and Me"
- Custom Label 1: primary print theme (e.g. "Wizard of Oz")
- Custom Label 2: season (Summer/Winter/etc)
- Custom Label 3: "Short Sleeve" / "Long Sleeve" / "Fleece"
- Custom Label 4: "Family Matching"

============================================================
METAFIELDS
============================================================
custom.category1      = "Mommy and Me"
custom.subcategory    = "Pajamas"
custom.subcategory2   = <season, e.g. "Summer Pajamas">
custom.pattern        = describe the print (e.g. "Wizard of Oz Floral Print")
custom.style          = "Matching Family Set"
custom.type           = "Two-Piece Pajama Set"
shopify.age-group     = list value — "kids" and/or "adults"
shopify.clothing-features = "Breathable, Lightweight, Button Front"
                            (adjust to fabric)
shopify.color-pattern = list — include every color word you tagged
shopify.fabric        = read the vendor listing — usually "Cotton",
                        "Cotton Blend", "Fleece", "Satin", etc.
shopify.neckline      = "Notched Collar" (or actual neckline)
shopify.size          = list every size value used
shopify.sleeve-length-type = "Short Sleeve" / "Long Sleeve" / "Sleeveless"

Leave unused metafields blank.

============================================================
IMAGES
============================================================
- The first (featured) image = the hero lifestyle shot I attached.
- Add alt text on every image that describes the scene ("Mom and daughter
  in matching Wizard of Oz floral short-sleeve pajama sets, standing in
  a softly lit living room") — never keyword-stuff.
- If multiple lifestyle shots are attached, assign them Image Position
  1, 2, 3... in descending visual impact.
- Per-variant image: assign the same lifestyle shot to every variant for now;
  ops will swap individual color images later if needed.

============================================================
PRICE & COMPARE-AT LOGIC
============================================================
Child rows:  Variant Price 34.99   Compare At 40.24
Mother rows: Variant Price 39.99   Compare At 45.99
Never put a price in the Title, Body, or SEO fields.

============================================================
FINAL CHECKS BEFORE YOU OUTPUT
============================================================
- Did you include ONLY the designs listed in DESIGNS_TO_LIST?
  (If the vendor page shows 10 prints and I only listed 2, the other 8
  must NOT appear in tags, body, variants, or images.)
- Is every size row in the size-chart table dual-unit?
- Are Child variants priced at 34.99 and Mother variants at 39.99?
- Is Status = draft and Published = TRUE so it appears under
  Shopify Admin > Products > filter by Status: Draft?
- Does the Body (HTML) open with the 6-bullet <ul> and contain
  <table id="size-chart">?
- Is the vendor URL in Tags (not in Body, not in Title)?
- Is the CSV header row BYTE-IDENTICAL to the header above?

Now produce Section A followed by Section B.
```

---

## How to use this for THIS request (Wizard of Oz pajama set)

When you paste the prompt, fill the inputs like this:

- **VENDOR_URL**: `https://detail.1688.com/offer/900601808231.html`
- **DESIGNS_TO_LIST**:
  - "The Wizard of Oz — Children's Edition"
  - "The Wizard of Oz — Adult Version"
- **CHILD_PRICE**: `34.99`
- **MOTHER_PRICE**: `39.99`
- **Attach**: the mother-and-daughter lifestyle photo + the size-chart image you already have.

The AI will return:
- a clean draft you can eyeball, and
- a CSV block you save as `wizard-of-oz-pajamas.csv` and upload via **Shopify Admin → Products → Import**. Because `Status=draft`, it will land in **Products → filter: Draft** where you can set the final price (already prefilled at 34.99 / 39.99) and publish.

## Why this prompt works for your pipeline

It matches the canonical structure in `GPT/products_export_1.csv` exactly — same CSV header order, same Body HTML scaffold, same `<table id="size-chart">` your theme expects, same `custom.*` and `shopify.*` metafield keys your existing scripts (`backfill_product_metadata.py`, `validate_import_ready_csv.py`) already handle. The vendor URL in the Tags field follows the convention your sourcing ops use. No BuckyDrop step is needed — your current flow is a straight Shopify CSV import, and nothing in the repo references BuckyDrop.

If you later add BuckyDrop, the only change is appending one more column (their SKU/product-ID) to the CSV header and adding one line in Section B; the prompt above is structured so that's a drop-in edit.
