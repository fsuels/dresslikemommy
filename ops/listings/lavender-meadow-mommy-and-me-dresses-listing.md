# Lavender Meadow Mommy and Me Dresses - Soft Twirl Style

## Links
- **Admin:** https://admin.shopify.com/store/dresslikemommy/products/7541032779873
- **Live:** not published
- **Vendor:** https://detail.1688.com/offer/780646169756.html
- **Product GID:** `gid://shopify/Product/7541032779873`
- **Handle:** `lavender-meadow-mommy-and-me-dresses`

## Inputs (resolved)
| Field | Value |
|---|---|
| VENDOR_URL | https://detail.1688.com/offer/780646169756.html |
| SIZE_CHART_SOURCE | attached image |
| LISTING_MODE | auto evidence -> Mommy and Me |
| PRIMARY_CATEGORY | auto -> Dresses |
| DESIGNS_TO_LIST | auto -> one Lavender dress colorway |
| EXCLUDE_ITEMS | none |
| SHORTCODE | auto -> `LVMD` |
| COLOR_TOKEN | auto -> `LAV` |
| FORCE_SPEC_PRICES | true |

## Vendor Fetch Status
A direct request to the 1688 page returned Alibaba punish/CAPTCHA markup during this run. Per the canonical workflow, the attached size chart and supplied product image were used as authoritative evidence.

## Pricing Source
Nearby live Mommy and Me dress products were queried through Shopify Admin. The prevailing role-level pattern is child `31.99` and adult `34.99`, so those prices were used with `FORCE_SPEC_PRICES=true`; Cost per item is exactly 50% of selling price.

## Title & SEO
| Field | Value | Chars |
|---|---|---|
| Product title | `Lavender Meadow Mommy and Me Dresses - Soft Twirl Style` | 55 |
| SEO title | `Lavender Mommy and Me Dresses | Dress Like Mommy` | 48 |
| SEO description | `Soft lavender mommy-and-me dresses in lightweight woven-look fabric for mom + daughter. Sizes Child 2Y-10Y and Mother S-2XL.` | 124 |

## SIZE_CHART / Variant Recap
| Role | Vendor row | Picker label | Color | SKU | Price | Cost | shopify.size GID |
|---|---|---|---|---|---|---|---|
| Girl Dress | 90 | Child 2 Years | Lavender | `DLM-LVMD-GRL-KID2Y-LAV` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972863073` (2-3 years) |
| Girl Dress | 100 | Child 3 Years | Lavender | `DLM-LVMD-GRL-KID3Y-LAV` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972895841` (3-4 years) |
| Girl Dress | 110 | Child 4 Years | Lavender | `DLM-LVMD-GRL-KID4Y-LAV` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972928609` (4-5 years) |
| Girl Dress | 120 | Child 5 Years | Lavender | `DLM-LVMD-GRL-KID5Y-LAV` | 31.99 | 16.00 | `gid://shopify/Metaobject/129972961377` (5-6 years) |
| Girl Dress | 130 | Child 6-7 Years | Lavender | `DLM-LVMD-GRL-KID67Y-LAV` | 31.99 | 16.00 | `gid://shopify/Metaobject/139840323681` (6-7 years) |
| Girl Dress | 140 | Child 8 Years | Lavender | `DLM-LVMD-GRL-KID8Y-LAV` | 31.99 | 16.00 | `gid://shopify/Metaobject/129973026913` (8) |
| Girl Dress | 150 | Child 9-10 Years | Lavender | `DLM-LVMD-GRL-KID910Y-LAV` | 31.99 | 16.00 | `gid://shopify/Metaobject/129971552353` (10) |
| Mother Dress | S | Mother S | Lavender | `DLM-LVMD-MOM-S-LAV` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975255137` (S) |
| Mother Dress | M | Mother M | Lavender | `DLM-LVMD-MOM-M-LAV` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975222369` (M) |
| Mother Dress | L | Mother L | Lavender | `DLM-LVMD-MOM-L-LAV` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975189601` (L) |
| Mother Dress | XL | Mother XL | Lavender | `DLM-LVMD-MOM-XL-LAV` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975287905` (XL) |
| Mother Dress | 2XL | Mother 2XL | Lavender | `DLM-LVMD-MOM-2XL-LAV` | 34.99 | 17.50 | `gid://shopify/Metaobject/129975156833` (2XL) |

## Derivations
- Vendor weight guidance was listed in jin in the screenshot and converted to kg/lbs for the shopper-facing table.
- Child hip = chest + 4 cm and child waist = chest because the girl chart omits hip and waist.
- Mother hip = bust + 6 cm because the adult chart omits hip; adult waist uses the vendor-published waist values.
- Shoulder values were transcribed for evidence but not surfaced as a separate storefront column because the canonical table has one dress secondary-measurement column.

## Verification
| Check | Result | Detail |
|---|---|---|
| Product status is DRAFT | PASS | DRAFT |
| publishedAt is null | PASS | None |
| No sales-channel publication is live | PASS | [] |
| Variant count matches SIZE_CHART | PASS | 12 vs 12 |
| Option axes are Size / Color | PASS | ['Size', 'Color'] |
| Size table rows match picker labels | PASS | Child 2 Years | Child 3 Years | Child 4 Years | Child 5 Years | Child 6-7 Years | Child 8 Years | Child 9-10 Years | Mother S | Mother M | Mother L | Mother XL | Mother 2XL |
| Each size table has 10 headers | PASS | 10 |
| Waist populated for every row | PASS | yes |
| Taxonomy fullName matches | PASS | Apparel & Accessories > Clothing > Dresses |
| Price and cost parity | PASS | FORCE_SPEC_PRICES=true and cost=50% |

## Price and Cost Parity
| SKU | Live Price | Live Compare-at | Live Cost | Spec Price | Spec Compare-at | Spec Cost | Match |
|---|---|---|---|---|---|---|---|
| `DLM-LVMD-GRL-KID2Y-LAV` | 31.99 | 36.99 | 16.00 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-LVMD-GRL-KID3Y-LAV` | 31.99 | 36.99 | 16.00 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-LVMD-GRL-KID4Y-LAV` | 31.99 | 36.99 | 16.00 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-LVMD-GRL-KID5Y-LAV` | 31.99 | 36.99 | 16.00 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-LVMD-GRL-KID67Y-LAV` | 31.99 | 36.99 | 16.00 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-LVMD-GRL-KID8Y-LAV` | 31.99 | 36.99 | 16.00 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-LVMD-GRL-KID910Y-LAV` | 31.99 | 36.99 | 16.00 | 31.99 | 36.99 | 16.00 | yes |
| `DLM-LVMD-MOM-S-LAV` | 34.99 | 40.99 | 17.50 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-LVMD-MOM-M-LAV` | 34.99 | 40.99 | 17.50 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-LVMD-MOM-L-LAV` | 34.99 | 40.99 | 17.50 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-LVMD-MOM-XL-LAV` | 34.99 | 40.99 | 17.50 | 34.99 | 40.99 | 17.50 | yes |
| `DLM-LVMD-MOM-2XL-LAV` | 34.99 | 40.99 | 17.50 | 34.99 | 40.99 | 17.50 | yes |

## Metafields Written
| Namespace.Key | Type | Value |
|---|---|---|
| `global.title_tag` | single_line_text_field | `Lavender Mommy and Me Dresses | Dress Like Mommy` |
| `global.description_tag` | single_line_text_field | `Soft lavender mommy-and-me dresses in lightweight woven-look fabric for mom + daughter. Sizes Child 2Y-10Y and Mother S-...` |
| `mc-facebook.google_product_category` | string | `2271` |
| `custom.category1` | single_line_text_field | `Mommy and Me` |
| `custom.subcategory` | single_line_text_field | `Dresses` |
| `custom.subcategory2` | single_line_text_field | `Summer Dresses` |
| `custom.pattern` | single_line_text_field | `Solid Lavender` |
| `custom.style` | single_line_text_field | `Soft Twirl Dress` |
| `custom.type` | single_line_text_field | `Dress` |
| `mm-google-shopping.custom_product` | boolean | `false` |
| `mm-google-shopping.gender` | single_line_text_field | `female` |
| `mm-google-shopping.age_group` | single_line_text_field | `adult` |
| `mm-google-shopping.condition` | single_line_text_field | `new` |
| `mm-google-shopping.custom_label_0` | single_line_text_field | `Mommy and Me` |
| `mm-google-shopping.custom_label_1` | single_line_text_field | `Lavender Meadow` |
| `mm-google-shopping.custom_label_2` | single_line_text_field | `Summer` |
| `mm-google-shopping.custom_label_3` | single_line_text_field | `Short Sleeve Dress` |
| `mm-google-shopping.custom_label_4` | single_line_text_field | `Two-Role Matching` |
| `shopify.age-group` | list.metaobject_reference | `["gid://shopify/Metaobject/128116523105","gid://shopify/Metaobject/128116490337"]` |
| `shopify.care-instructions` | list.metaobject_reference | `["gid://shopify/Metaobject/130283503713"]` |
| `shopify.color-pattern` | list.metaobject_reference | `["gid://shopify/Metaobject/130284126305"]` |
| `shopify.dress-occasion` | list.metaobject_reference | `["gid://shopify/Metaobject/69622169697","gid://shopify/Metaobject/69622202465"]` |
| `shopify.dress-style` | list.metaobject_reference | `["gid://shopify/Metaobject/130282520673"]` |
| `shopify.neckline` | list.metaobject_reference | `["gid://shopify/Metaobject/129972469857"]` |
| `shopify.size` | list.metaobject_reference | `["gid://shopify/Metaobject/129972863073","gid://shopify/Metaobject/129972895841","gid://shopify/Metaobject/129972928609"...` |
| `shopify.skirt-dress-length-type` | list.metaobject_reference | `["gid://shopify/Metaobject/130282487905"]` |
| `shopify.sleeve-length-type` | list.metaobject_reference | `["gid://shopify/Metaobject/129971486817"]` |
| `shopify.target-gender` | list.metaobject_reference | `["gid://shopify/Metaobject/129971617889"]` |

## Metafields Skipped
| Namespace.Key | Reason |
|---|---|
| `shopify.fabric` | The 1688 page returned Alibaba punish/CAPTCHA markup and the attached chart/image do not confirm exact fiber composition. |
| `shopify.top-length-type` | Does not apply to a dress listing. |
| `shopify.pants-length-type` | No pants or shorts garment is sold in this listing. |
| `shopify.waist-rise` | No pants or shorts garment is sold in this listing. |

## Tags Written
`A-Line Dress, Child 2 Years, Child 3 Years, Child 4 Years, Child 5 Years, Child 6-7 Years, Child 8 Years, Child 9-10 Years, Dresses, Garden, Girl Dress, https://detail.1688.com/offer/780646169756.html, Lavender, Lavender Meadow, Lilac, Matching Family Dress, Matching Family Dresses, Midi Dress, Mommy and Me, Mother 2XL, Mother Dress, Mother L, Mother M, Mother S, Mother XL, Purple, Resort, Round Neck Dress, Short Sleeve Dress, Solid Lavender, Spring, Summer, Sundress, Vacation`

## Smart Collections
- New Arrivals (`/new-arrivals`)
- New Mommy & Me (`/new-matching-outfits`)
- Popular Mommy & Me (`/popular-mommy-me-1`)
- Mommy and Me Matching Outfits for Mother and Daughter (`/mommy-and-me`)
- Matching Family Vacation Outfits (`/matching-family-vacation-outfits`)

## Publication
- Product remains DRAFT.
- Live URL: not published.
- Sales-channel publication check: no live publications.

## Manual Follow-ups
- Replace or retouch the supplied source image before publication if the top-right mark is visible.
- Confirm exact fabric composition if the vendor page becomes readable later; `shopify.fabric` was intentionally skipped.
- Inventory quantities and per-variant grams still need operator stock values.

## Files Saved
- `/Users/fsuels/Projects/dresslikemommy/ops/scripts/create-lvmd-lavender-meadow-mommy-and-me-dresses.sh`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/lavender-meadow-mommy-and-me-dresses-listing.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/lavender-meadow-mommy-and-me-dresses-shopify-import.csv`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/size-chart-lavender-meadow-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/body-lavender-meadow-mommy-and-me-dresses.html`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/verify-lavender-meadow-mommy-and-me-dresses.json`
- `/Users/fsuels/Projects/dresslikemommy/ops/listings/source-size-chart-lavender-meadow-mommy-and-me-dresses.png`
- `/Users/fsuels/Projects/dresslikemommy/uploads/lavender-meadow-mommy-and-me-dresses`

## Sources
- Attached size chart image from operator request.
- Attached product image from operator request.
- Shopify Admin query of nearby live Mommy and Me dress products for pricing.