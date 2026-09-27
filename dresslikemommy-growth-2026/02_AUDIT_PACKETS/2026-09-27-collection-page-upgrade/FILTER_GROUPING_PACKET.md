# Filter value grouping (Search & Discovery): approval packet

Status: READ-ONLY packet, prepared 2026-09-27. No changes were made to Search & Discovery, products, metafields, theme or git. Every step below is for the owner to approve and carry out.

Machine-readable twin: `filter_grouping.json`. It holds every raw value with product counts, its target group and confidence, plus per-collection before/after.

## What the filters actually are

- **Size**: variant option "Size" (param filter.v.option.size)
- **Color**: variant option "Color" (filter.v.option.color)
- **Type**: PRODUCT METAFIELD custom.subcategory (filter.p.m.custom.subcategory), labelled "Type"; NOT product_type
- **Price**: price range

The **Type** filter reads the product metafield `custom.subcategory`, not `product_type`. So the Type duplicates ("Set"/"Sets", "Sweaters"/"Family Sweaters") come from metafield values. Editing them would not touch the Merchant or Pinterest feeds, which read `productType`. It would still change theme behaviour, because `subcategory` drives card analytics, the hub interleave buckets, breadcrumbs and JSON-LD. **Recommendation: group in S&D and edit no product data.** The same applies to `product_type`, which feeds `product_type` in the Merchant feed worker (`ops/cloudflare/merchant-feed-worker/src/generator.js`).

## Headline numbers

| Collection | Size before → after | Color before → after | Type before → after |
|---|---|---|---|
| `mommy-and-me` | 72 (18 grouped) → **26** | 52 (8 grouped) → **13** | 9 (0 grouped) → **7** |
| `matching-outfits` | 77 (18 grouped) → **25** | 15 (8 grouped) → **12** | hidden by theme |
| `daddy-me` | 19 (5 grouped) → **16** | 10 (6 grouped) → **8** | 2 (0 grouped) → **2** |
| `pajamas` | 41 (13 grouped) → **24** | 28 (6 grouped) → **10** | 1 (0 grouped) → **1** |
| `dresses` | 44 (10 grouped) → **18** | 19 (7 grouped) → **12** | 1 (0 grouped) → **1** |
| `swimsuits` | 28 (10 grouped) → **16** | 14 (8 grouped) → **11** | 1 (0 grouped) → **1** |

Store-wide distinct values: Size **196 → 30** groups, Color **81 → 13**, Type (subcategory) **15 → 7**.

The counts come from the live rendered filter markup, where each `gid://shopify/FilterSettingGroup/…` input is an existing group. Collection filter counts also include products that the theme later hides (Packet 1), so they will shrink once Packet 1 is applied.

## Theme interactions (no theme change required)

These were read from the committed theme (HEAD `77f6e2c`) in `/Users/fsuels/Projects/dlm-collection-upgrade`; that worktree also has uncommitted facet edits.

- **type_hidden_on**: snippets/facets.liquid hides the Type filter on new-women-outfits, family-matching-outfits, family-matching, matching-outfits
- **blocked_color_labels**: facets.liquid drops color values overall, short, t-shirt, striped, stripes, tee(s), shirt(s), top(s); grouping them makes those products reachable through a real color group
- **label_dedupe**: facets.liquid drops a value whose handleized label was already rendered (e.g. "Baby 6-9 Months" vs "Baby 6-9 months"): the second value is unreachable today; grouping fixes it
- **color_dot**: snippets/dlm-facet-color-dot.liquid matches words in the label: "Cream & Beige" -> cream swatch, "Multicolor & Print" -> multi swatch; no theme change needed
- **value_order**: theme renders values in S&D order (active first only when operator is AND)

## 1. Size

Group order to set in S&D:
- **Mom / Women**: Mom XS · Mom S · Mom M · Mom L · Mom XL · Mom 2XL · Mom 3XL · Mom 4XL · Mom 5XL · Mom One Size
- **Kids**: Baby 0-12 months · 1-2 years · 2-3 years · 3-4 years · 4-5 years · 5-6 years · 6-7 years · 7-8 years · 8-9 years · 9-10 years · 10-11 years · 11-12 years · 12-14 years
- **Dad / Men**: Dad S · Dad M · Dad L · Dad XL · Dad 2XL · Dad 3XL · Dad 4XL

Mapping rules: a single age N goes to "N-(N+1) years". A range spanning two groups (6-8, 8-10, 10-12) goes to its lower bound. T sizes (2T, 4T, 10T) map by their number. Baby month sizes up to 12 months go to "Baby 0-12 months"; 12-24 months go to "1-2 years". `cm` sizes are mapped by height and marked uncertain. Unisex "Adult" sizes go to the Mom group, because a value can sit in only one group. That fits mommy-and-me; on family pages, "Adult M" shoppers include dads, so consider "Adult / Mom M" as the label.

Existing groups (`Mother S…3XL`, `Father M…3XL`, `2-3 years`, `4-5 years`, `6-7 years`, `8-9 years`, `10-11 years`, `12-14 years`, `Baby 3-6 Months`, `Baby 9-12 Months`) should be **edited and renamed**, not duplicated. Their current membership cannot be read from the storefront, so treat the table below as authoritative and move every listed raw value into its group.

| Raw value | Products | → Group | Note |
|---|---|---|---|
| Adult XS | 7 | Mom XS | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult XXS | 7 | Mom XS | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Mother XS | 2 | Mom XS |  |
| Adult S | 39 | Mom S | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult S - Mother "VE" | 1 | Mom S | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult S-M | 1 | Mom S | range; mapped to lower size; unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult S/M | 1 | Mom S | range; mapped to lower size; unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Mother S | 162 | Mom S |  |
| S | 1 | Mom S | plain/edition-labelled adult size |
| S (Adult Extended Version) | 1 | Mom S | plain/edition-labelled adult size |
| S (Adult Normal Version) | 1 | Mom S | plain/edition-labelled adult size |
| Adult M | 48 | Mom M | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult M - Mother "VE" | 1 | Mom M | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult M-L | 1 | Mom M | range; mapped to lower size; unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult M/L | 1 | Mom M | range; mapped to lower size; unisex "Adult" size placed in Mom group (value can only sit in one group) |
| M | 1 | Mom M | plain/edition-labelled adult size |
| M (Adult Extended Edition) | 1 | Mom M | plain/edition-labelled adult size |
| M (Adult Normal Version) | 1 | Mom M | plain/edition-labelled adult size |
| Mother M | 170 | Mom M |  |
| Adult L | 47 | Mom L | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult L - Mother "VE" | 1 | Mom L | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult L-XL | 1 | Mom L | range; mapped to lower size; unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult L/XL | 1 | Mom L | range; mapped to lower size; unisex "Adult" size placed in Mom group (value can only sit in one group) |
| L | 1 | Mom L | plain/edition-labelled adult size |
| L (Adult Extended Version) | 1 | Mom L | plain/edition-labelled adult size |
| L (Adult Normal Version) | 1 | Mom L | plain/edition-labelled adult size |
| Mother  L | 1 | Mom L |  |
| Mother L | 165 | Mom L |  |
| Mother L-XL | 1 | Mom L | range; mapped to lower size |
| Adult XL | 47 | Mom XL | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult XL - Mother "VE" | 1 | Mom XL | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult XL-2XL | 1 | Mom XL | range; mapped to lower size; unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult XL/2XL | 1 | Mom XL | range; mapped to lower size; unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Mother XL | 138 | Mom XL |  |
| Adult 2XL | 46 | Mom 2XL | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Adult 2XL - Mother "VE" | 1 | Mom 2XL | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Mother 2XL | 68 | Mom 2XL |  |
| Adult 3XL | 45 | Mom 3XL | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Mother 3XL | 31 | Mom 3XL |  |
| Adult 4XL | 21 | Mom 4XL | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Mother 4XL | 7 | Mom 4XL |  |
| Adult 5XL | 11 | Mom 5XL | unisex "Adult" size placed in Mom group (value can only sit in one group) |
| Mother One Size | 3 | Mom One Size |  |
| Baby 0-6 Months | 1 | Baby 0-12 months |  |
| Baby 12 Months | 2 | Baby 0-12 months |  |
| Baby 3 Months | 2 | Baby 0-12 months |  |
| Baby 3-6 Months | 5 | Baby 0-12 months |  |
| Baby 6 Months | 2 | Baby 0-12 months |  |
| Baby 6-12 Months | 1 | Baby 0-12 months |  |
| Baby 6-9 Months | 5 | Baby 0-12 months |  |
| Baby 6-9 months | 14 | Baby 0-12 months |  |
| Baby 9 Months | 2 | Baby 0-12 months |  |
| Baby 9-12 Months | 5 | Baby 0-12 months |  |
| Baby 9-12 months | 14 | Baby 0-12 months |  |
| Baby 1-2 Years | 2 | 1-2 years |  |
| Baby 12-18 Months | 5 | 1-2 years |  |
| Baby 18-24 Months | 2 | 1-2 years |  |
| Boy 1-2 Years | 2 | 1-2 years |  |
| Child 1 Year | 3 | 1-2 years |  |
| Child 1 year | 37 | 1-2 years |  |
| Child 1 years | 2 | 1-2 years |  |
| Child 1-2 Years | 34 | 1-2 years |  |
| Girl 1-2 Years | 2 | 1-2 years |  |
| Girl 1-2T | 4 | 1-2 years |  |
| 90cm | 1 | 2-3 years | uncertain: ≈2-3Y by height; confirm against product size chart |
| Boy 2 Years | 3 | 2-3 years |  |
| Boy 2 years | 1 | 2-3 years |  |
| Boy 2T | 4 | 2-3 years |  |
| Child 2 Years | 115 | 2-3 years |  |
| Child 2 years | 40 | 2-3 years |  |
| Child 2-3 Years | 22 | 2-3 years |  |
| Child 2-3 years | 43 | 2-3 years |  |
| Child 2-3T | 1 | 2-3 years |  |
| Girl 2 Years | 3 | 2-3 years |  |
| Girl 2 years | 1 | 2-3 years |  |
| Girl 2-3 Years | 1 | 2-3 years |  |
| Girl 2-3 years | 2 | 2-3 years |  |
| 100cm | 2 | 3-4 years | uncertain: ≈3-4Y by height; confirm against product size chart |
| Boy 3 Years | 3 | 3-4 years |  |
| Boy 3-4 Years | 3 | 3-4 years |  |
| Boy 3-4 years | 1 | 3-4 years |  |
| Child 3 Years | 110 | 3-4 years |  |
| Child 3 years | 37 | 3-4 years |  |
| Child 3-4 Years | 34 | 3-4 years |  |
| Child 3-4 years | 2 | 3-4 years |  |
| Child 3-4T | 1 | 3-4 years |  |
| Girl 3 Years | 3 | 3-4 years |  |
| Girl 3-4 Years | 5 | 3-4 years |  |
| Girl 3-4 years | 3 | 3-4 years |  |
| Girl 3-4T | 4 | 3-4 years |  |
| 110cm | 2 | 4-5 years | uncertain: ≈4-5Y by height; confirm against product size chart |
| Boy 4 Years | 3 | 4-5 years |  |
| Boy 4-5 Years | 4 | 4-5 years |  |
| Boy 4T | 4 | 4-5 years |  |
| Child 4 -5 Years | 1 | 4-5 years |  |
| Child 4 Years | 129 | 4-5 years |  |
| Child 4 years | 39 | 4-5 years |  |
| Child 4-5 Years | 24 | 4-5 years |  |
| Child 4-5 years | 43 | 4-5 years |  |
| Child 4-5T | 1 | 4-5 years |  |
| Girl 4 Years | 3 | 4-5 years |  |
| Girl 4-5 Years | 6 | 4-5 years |  |
| Girl 4-5 years | 1 | 4-5 years |  |
| Boy 5 Years | 3 | 5-6 years |  |
| Boy 5-6 Years | 4 | 5-6 years |  |
| Boy 5-6 years | 1 | 5-6 years |  |
| Child 5 Years | 130 | 5-6 years |  |
| Child 5-6 Years | 31 | 5-6 years |  |
| Child 5-6 years | 45 | 5-6 years |  |
| Girl 5 Years | 3 | 5-6 years |  |
| Girl 5-6 Years | 6 | 5-6 years |  |
| Girl 5-6 years | 3 | 5-6 years |  |
| Girl 5-6T | 4 | 5-6 years |  |
| 120cm | 2 | 6-7 years | uncertain: ≈6-7Y by height; confirm against product size chart |
| Boy 6-7 Years | 7 | 6-7 years |  |
| Boy 6T | 4 | 6-7 years |  |
| Child 6 Years | 19 | 6-7 years |  |
| Child 6 years | 2 | 6-7 years |  |
| Child 6-7 Years | 140 | 6-7 years |  |
| Child 6-7 years | 1 | 6-7 years |  |
| Child 6-8 Years | 1 | 6-7 years | range 6-8Y spans two groups; mapped to lower bound |
| Child 6-8 years | 42 | 6-7 years | range 6-8Y spans two groups; mapped to lower bound |
| Child 6-8T | 1 | 6-7 years | range 6-8Y spans two groups; mapped to lower bound |
| Girl 6-7 Years | 9 | 6-7 years |  |
| Girl 6-7 years | 2 | 6-7 years |  |
| Boy 7-8 Years | 4 | 7-8 years |  |
| Boy 7-8 years | 1 | 7-8 years |  |
| Child 7 Years | 3 | 7-8 years |  |
| Child 7-8 Years | 27 | 7-8 years |  |
| Child 7-8 years | 39 | 7-8 years |  |
| Girl 7-8 Years | 6 | 7-8 years |  |
| Girl 7-8 years | 3 | 7-8 years |  |
| Girl 7-8T | 4 | 7-8 years |  |
| 130cm | 2 | 8-9 years | uncertain: ≈8-9Y by height; confirm against product size chart |
| 8Y | 1 | 8-9 years |  |
| Boy 8 Years | 3 | 8-9 years |  |
| Boy 8-9 Years | 4 | 8-9 years |  |
| Boy 8T | 4 | 8-9 years |  |
| Child 8 Years | 117 | 8-9 years |  |
| Child 8 years | 2 | 8-9 years |  |
| Child 8-10 Years | 1 | 8-9 years | range 8-10Y spans two groups; mapped to lower bound |
| Child 8-10 years | 42 | 8-9 years | range 8-10Y spans two groups; mapped to lower bound |
| Child 8-10T | 1 | 8-9 years | range 8-10Y spans two groups; mapped to lower bound |
| Child 8-9 Years | 16 | 8-9 years |  |
| Child 8-9 years | 1 | 8-9 years |  |
| Girl 8 Years | 3 | 8-9 years |  |
| Girl 8-9 Years | 6 | 8-9 years |  |
| Girl 8-9 years | 2 | 8-9 years |  |
| 9Y | 1 | 9-10 years |  |
| Boy 9-10 Years | 5 | 9-10 years |  |
| Boy 9-10 years | 1 | 9-10 years |  |
| Child 9 Years | 2 | 9-10 years |  |
| Child 9-10 Years | 116 | 9-10 years |  |
| Child 9-10 years | 38 | 9-10 years |  |
| Girl 9-10 Years | 5 | 9-10 years |  |
| Girl 9-10 years | 2 | 9-10 years |  |
| Girl 9-10T | 4 | 9-10 years |  |
| 10Y | 1 | 10-11 years |  |
| 140cm | 2 | 10-11 years | uncertain: ≈10-11Y by height; confirm against product size chart |
| Boy 10T | 4 | 10-11 years |  |
| Child 10 Years | 16 | 10-11 years |  |
| Child 10 years | 2 | 10-11 years |  |
| Child 10-11 Years | 5 | 10-11 years |  |
| Child 10-12 Years | 9 | 10-11 years | range 10-12Y spans two groups; mapped to lower bound |
| Child 10-12 years | 56 | 10-11 years | range 10-12Y spans two groups; mapped to lower bound |
| Child 10-12T | 1 | 10-11 years | range 10-12Y spans two groups; mapped to lower bound |
| Girl 10-12 years | 1 | 10-11 years | range 10-12Y spans two groups; mapped to lower bound |
| Boy 11-12 years | 1 | 11-12 years |  |
| Child 11 Years | 1 | 11-12 years |  |
| Child 11-12 Years | 5 | 11-12 years |  |
| Child 11-12 years | 1 | 11-12 years |  |
| Girl 11-12T | 4 | 11-12 years |  |
| 12Y | 1 | 12-14 years |  |
| 150cm | 2 | 12-14 years | uncertain: ≈12Y by height; confirm against product size chart |
| 160cm | 1 | 12-14 years | uncertain: ≈13-14Y by height; confirm against product size chart |
| Boy 12T | 4 | 12-14 years |  |
| Boy 13-14 years | 1 | 12-14 years |  |
| Child 12 Years | 34 | 12-14 years |  |
| Child 12 years | 2 | 12-14 years |  |
| Child 13-14 Years | 2 | 12-14 years |  |
| Child 13-14 years | 1 | 12-14 years |  |
| Child 14 Years | 20 | 12-14 years |  |
| Girl 12-14 years | 1 | 12-14 years |  |
| Father S | 44 | Dad S |  |
| Father M | 111 | Dad M |  |
| Adult L - Father "LO" | 1 | Dad L |  |
| Father L | 116 | Dad L |  |
| Adult XL - Father "LO" | 1 | Dad XL |  |
| Father XL | 116 | Dad XL |  |
| Adult 2XL - Father "LO" | 1 | Dad 2XL |  |
| Father 2XL | 112 | Dad 2XL |  |
| Father XXL | 3 | Dad 2XL |  |
| Adult 3XL - Father "LO" | 1 | Dad 3XL |  |
| Father 3XL | 95 | Dad 3XL |  |
| Adult 4XL - Father "LO" | 1 | Dad 4XL |  |
| Father 4XL | 28 | Dad 4XL |  |

## 2. Color

Groups (13): Black · White · Cream & Beige · Grey · Brown · Red · Pink · Orange · Yellow · Green · Blue · Purple · Multicolor & Print. Navy folds into Blue, and Ivory, Beige and Cream into "Cream & Beige".

Print names were mapped by colour words in the name, colour tags, and a visual check of the variant or product image for every print that was not obvious. Confidence: high = name or tag is unambiguous; medium = image-based or dominant colour; low = placeholder, non-colour value, or mixed print. Low rows are the ones to eyeball.

| Raw value | Products | → Group | Confidence | Basis |
|---|---|---|---|---|
| Black | 43 | Black | high | name |
| black | 2 | Black | high | name |
| Black and White | 1 | Black | medium | name |
| Midnight Paint Splash | 1 | Black | medium | image: black shirt with neon splash |
| Ladybug Dots | 1 | White | low | image: white/pale-blue pajamas |
| Monochrome Palm | 1 | White | medium | image: white shirts with black palms |
| White | 32 | White | high | name |
| white | 2 | White | high | name |
| White Graphic | 1 | White | high | name |
| Autumn Woodland Bunny | 1 | Cream & Beige | high | image: cream pajamas; tags Beige/Cream |
| Bamboo Garden Panda Cream | 2 | Cream & Beige | high | name |
| Beige | 2 | Cream & Beige | high | name |
| Bird Chirping Cream | 1 | Cream & Beige | high | name |
| Bunny Garden | 1 | Cream & Beige | high | image: cream pajamas |
| Cream | 3 | Cream & Beige | high | name |
| Eucalyptus Bunny Meadow | 1 | Cream & Beige | high | image: cream pajamas |
| Fairy Tale Messenger Cream | 1 | Cream & Beige | high | name |
| Fluttering Butterflies | 1 | Cream & Beige | medium | image: cream pajamas with pink print |
| Good Night Song of the Sea | 1 | Cream & Beige | medium | image: cream pajamas with blue whales |
| Grape Vineyard Cream | 1 | Cream & Beige | high | name |
| Grapevine Cream | 1 | Cream & Beige | high | name |
| Ivory | 5 | Cream & Beige | high | name |
| Little Pear Cream | 1 | Cream & Beige | high | name |
| Little Sheep Meadow Cream | 1 | Cream & Beige | high | name |
| Meow Star Garden | 1 | Cream & Beige | high | image: cream pajamas |
| Polar Adventure Cream | 1 | Cream & Beige | high | name |
| Red Panda | 1 | Cream & Beige | medium | image: cream pajamas with orange print (name says red) |
| Stripes | 1 | Cream & Beige | low | image: cream cardigans with navy stripes, red trim |
| Summer Puppies | 1 | Cream & Beige | high | image: cream pajamas |
| Vintage Cottage Floral | 1 | Cream & Beige | high | image: cream floral pajamas; tag Cream |
| Welsh Dinosaur Cream | 1 | Cream & Beige | high | name |
| Gray | 3 | Grey | high | name |
| Brown | 3 | Brown | high | name |
| Leopard | 1 | Brown | medium | image: leopard print swimsuit |
| Coral Blossom | 1 | Red | medium | image: red/coral floral dress; name says coral |
| Red | 36 | Red | high | name |
| Red Heart Raglan | 1 | Red | high | name |
| Red Plaid | 1 | Red | high | name |
| Red Stripe | 1 | Red | high | name |
| Red Tropical Leaf | 1 | Red | high | name + tag Red |
| As image | 1 | Pink | low | image: hot-pink bikini; placeholder value, fix product data |
| Blush Floral | 1 | Pink | high | name + tags Pink/White |
| Pastel Watercolor | 1 | Pink | low | image: pink/peach watercolor dress |
| Peach Sweetheart | 1 | Pink | low | image: cream top + pink shorts pajamas |
| Pink | 30 | Pink | high | name |
| Apricot | 1 | Orange | medium | name (apricot = light orange); verify image |
| Orange | 9 | Orange | high | name |
| Yellow | 11 | Yellow | high | name |
| yellow | 1 | Yellow | high | name |
| Green | 29 | Green | high | name |
| green | 1 | Green | high | name |
| Green Botanical | 1 | Green | high | name + tag Green |
| Light Green | 1 | Green | high | name |
| Blue | 35 | Blue | high | name |
| blue | 3 | Blue | high | name |
| Blue Apricot | 1 | Blue | medium | name + tags Blue/Red |
| Blue Daisy | 1 | Blue | high | name + tag Blue |
| Blue Monstera Citrus | 1 | Blue | medium | name; tags Blue/Orange/White |
| Blue Stripe | 1 | Blue | high | name |
| Coastal Banana Leaf | 1 | Blue | medium | image: blue/white tropical shirts |
| Denim Blue | 1 | Blue | high | name |
| Midnight Palm Blossom | 1 | Blue | high | image: navy tropical shirt |
| Navy | 3 | Blue | high | name (navy folded into Blue) |
| Ocean Blue Floral | 1 | Blue | high | name + tag Blue |
| Sky Daisy Doodle | 1 | Blue | medium | image: light-blue floral shirts |
| Striped | 1 | Blue | low | image: navy/grey/white striped hoodies |
| Washed Denim | 1 | Blue | high | name |
| Purple | 8 | Purple | high | name |
| Bright Paint Splash | 1 | Multicolor & Print | high | name + 5 colour tags |
| Main color | 2 | Multicolor & Print | low | placeholder value on 2 products with different prints; fix product data |
| Multi Color | 14 | Multicolor & Print | high | name |
| Multi-Color | 4 | Multicolor & Print | high | name |
| Overall | 1 | Multicolor & Print | low | NOT a colour: garment type stored in Color option; fix product data |
| Pastel Bloom | 1 | Multicolor & Print | high | image: multicolour floral |
| Photo Color | 3 | Multicolor & Print | low | placeholder value on 2 products (black/white animal, blue/white paisley); fix product data |
| Playful Cat Parade | 1 | Multicolor & Print | high | image + Multicolor tag |
| Rainbow | 1 | Multicolor & Print | high | name |
| Short | 1 | Multicolor & Print | low | NOT a colour: garment type stored in Color option; fix product data |
| Sunlit Tropical Bloom | 1 | Multicolor & Print | high | image: multicolour tropical |
| Sunshine Stripe | 1 | Multicolor & Print | high | image: yellow/red/blue stripes |
| T-shirt | 1 | Multicolor & Print | low | NOT a colour: garment type stored in Color option; fix product data |

## 3. Type (metafield `custom.subcategory`)

| Raw value | Published products | → Group |
|---|---|---|
| `Dresses` | 39 | Dresses |
| `Set` | 33 | Sets & Outfits |
| `Sets` | 6 | Sets & Outfits |
| `Family Sets` | 7 | Sets & Outfits |
| `Family Matching Sets` | 2 | Sets & Outfits |
| `Tops` | 18 | Tops & Tees |
| `Family Tops` | 18 | Tops & Tees |
| `Daddy & Me T-Shirts` | 34 | Tops & Tees |
| `Sweaters` | 6 | Sweaters |
| `Family Sweaters` | 18 | Sweaters |
| `Family Sweaters ` | 1 | Sweaters |
| `Pajamas` | 39 | Pajamas |
| `Swimsuits` | 35 | Swimwear |
| `Trunks` | 11 | Swimwear |
| `Skirts` | 1 | Skirts |

Group order: Dresses · Sets & Outfits · Tops & Tees · Sweaters · Pajamas · Swimwear · Skirts. This merges "Set"/"Sets"/"Family Sets"/"Family Matching Sets" and "Sweaters"/"Family Sweaters"/"Family Sweaters " (trailing space).

Fallback: if S&D does not offer "Group values" for this metafield filter, **do not edit `product_type`**. The narrow fallback normalises `custom.subcategory` on 3 + 6 + 1 products (Sets→Set, Sweaters→Family Sweaters, trailing space). That is a product-data write and would need its own approval.

## 4. "Who's matching" filter

- **Recommended source: `product metafield custom.category1 (single_line_text_field, definition gid://shopify/MetafieldDefinition/9244180577)`.**
- category1 coverage: 268 published products, **0 missing**, one value per product: {'Mommy and Me': 107, 'Daddy and Me': 45, 'Family Matching': 116}. Active drafts and unpublished products are also 100% filled.
- Tag coverage: {'Mommy and Me': 140, 'Daddy and Me': 90, 'Family Matching': 116, 'Couples': 0, 'Maternity': 0}. **45 products carry 2-3 audience tags** ({'Mommy and Me': 107, 'Daddy and Me': 45, 'Family Matching': 71, 'Daddy and Me + Family Matching': 12, 'Mommy and Me + Daddy and Me + Family Matching': 33}). A tag filter would list the 33 whole-family Christmas sets under Mommy & Me and Daddy & Me, which contradicts Packet 1. The S&D Tag filter also exposes every tag, and these products carry about 40 each: sizes, colours and styles.
- Couples: 0 published products have category1=Couples or a Couples tag. /collections/couples holds 2 products via title rules, both category1=Family Matching. Maternity: 0. Leave both out until products exist.
- Proposed display labels: {'Mommy and Me': 'Mommy & Me', 'Daddy and Me': 'Daddy & Me', 'Family Matching': 'Whole family', 'Couples': 'Couples (0 products today; value will not appear)'}
- Where it helps: {'family-pajamas': {'Mommy and Me': 21, 'Family Matching': 17}, 'matching-family-vacation-outfits (today)': {'Mommy and Me': 56, 'Family Matching': 48}, 'search and /collections/all': 'all three values'}. After Packet 1 these collections hold a single audience, so the filter would show one value: mommy-and-me, pajamas, dresses, swimsuits, tops, sweaters, matching-outfits, family-sets, family-tops, family-sweaters, daddy-me. S&D filters are store-wide, so it is still worth adding for search, `/collections/all`, family-pajamas and any mixed landing page.
- Localisation: the theme snippet already handles translated category1 values (mami, rodzin, papà…), so the metafield has translations. The filter values should appear translated on /de, /fr and other locales. EXPECTED: verify on one locale after enabling.

## 5. Owner click-by-click (Shopify Admin → Apps → Search & Discovery → Filters)

**Before you start:** take screenshots of the Size, Color and Type filter settings, including each existing group opened. These are the rollback reference.

**Size**
1. Click the **Size** filter. Under the values list, open **Group values** (or **Edit groups**).
2. Rename the existing groups: `Mother S` → `Mom S` (and the rest), `Father M` → `Dad M`, keep `2-3 years`, `4-5 years`, `6-7 years`, `8-9 years`, `10-11 years`, `12-14 years`. Create the missing groups: `Mom XS`, `Mom 4XL`, `Mom 5XL`, `Mom One Size`, `Dad S`, `Dad 4XL`, `Baby 0-12 months`, `1-2 years`, `3-4 years`, `5-6 years`, `7-8 years`, `9-10 years`, `11-12 years`. Merge `Baby 3-6 Months` and `Baby 9-12 Months` into `Baby 0-12 months`.
3. In each group, tick every raw value listed for it in the Size table above. Search inside the value picker, for example for "6-8".
4. Order the groups Mom XS→5XL, One Size, then Baby → 12-14 years, then Dad S→4XL. If S&D offers only automatic sorting, keep this order in the table as the target and note it.
5. Save.

**Color**
1. Click the **Color** filter, then **Group values**.
2. Keep and extend Black, Blue, Green, Grey, Pink, Red, White and Yellow. Rename `Multi-Color` → `Multicolor & Print`. Create `Cream & Beige`, `Brown`, `Orange` and `Purple`.
3. Assign every raw value from the Color table. Eyeball the 11 "low" rows against the product first.
4. Optional: set a swatch colour per group in S&D. The theme already shows a matching dot from the label.
5. Save.

**Type**
1. Click the **Type** filter (Product metafield: SubCategory). If **Group values** is offered, create the 7 groups from the Type table and save. If it is not, stop and report back; do not edit product data under this packet.

**Who's matching**
1. Click **Add filter** → source **Product metafield** → **Category1 (custom.category1)**.
2. Set the label to **Who's matching**.
3. If value grouping or renaming is offered, rename `Mommy and Me` → `Mommy & Me`, `Daddy and Me` → `Daddy & Me`, `Family Matching` → `Whole family`.
4. Drag the filter to sit above Size.
5. Save.
6. Translate the filter label in Translate & Adapt, where filter labels are translatable.

**Verify afterwards (read-only):**
1. On `/collections/mommy-and-me`, Size shows about 26 values, Color 13 and Type 7.
2. Pick `Mom M` and `6-7 years` together; the result count is greater than 0 and matches the cards shown.
3. On `/de/collections/mommy-and-me`, the labels render.
4. The Type filter is still hidden on the family hubs, which is intended by the theme.

## Rollback

- Groups: open the filter → Group values → delete or rename back using the before-screenshots. Raw values return to the list as soon as they leave a group.
- Who's matching: Search & Discovery → Filters → remove the Category1 filter.
- No product, metafield, feed or theme data changes, so nothing else needs rolling back.

## Risks

- **Group support per filter type is EXPECTED, not verified.** Grouping is live on the Size and Color option filters today. Whether S&D offers it for the metafield-based Type and Who's-matching filters must be confirmed in the app; a fallback is given for each.
- **Mapping ranges to the lower bound.** A shopper filtering "7-8 years" misses items sold as "6-8 years". Mitigation: size charts stay on the product page.
- **cm and height-based kids sizes** (11 values, 1-2 products each) are approximate.
- **Adult unisex sizes** are grouped under Mom. On family and daddy pages this may read oddly; the alternative label is given above.
- **Placeholder and non-colour values** ("As image", "Main color", "Photo Color", "Overall/Short/T-shirt") are fixed only cosmetically by grouping. The real fix is product data, which is out of scope.

## Data-quality follow-ups (not part of this approval)

- Color option holds non-colors on vibrant-rainbow-family-matching-outfits-* (Overall/Short/T-shirt)
- Placeholder color values: "As image" (1), "Main color" (2), "Photo Color" (2)
- custom.subcategory "Family Sweaters " has a trailing space (1 product)
- Size value "Mother  L" has a double space (1 product)
- 3 products use option name "size" (lowercase)