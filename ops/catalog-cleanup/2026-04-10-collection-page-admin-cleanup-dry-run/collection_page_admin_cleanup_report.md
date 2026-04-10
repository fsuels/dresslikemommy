# Collection Page Admin Cleanup Dry-Run

Input CSV: `GPT/products_export_1.csv`
Generated: `2026-04-10 04:56:45`

## Summary

- Total rows scanned: `16831`
- Size variant groups flagged: `55`
- Color values flagged: `20`
- Collection plan items: `5`

## Findings

### Dirty size labels

These are case or phrasing variants that should be normalized in source product data before Search & Discovery is rebuilt.

- `xl`: `Adult XL, Boy XL, Boy XL (8-9Y), Child XL, Dad XL, Father XL, father XL, Girl XL, Girl XL (8-9Y), Mom XL, mom XL, Mother XL, mother XL, Women XL, XL`
  Handles: 2016-family-matching-outfits-summer-family-look-clothing-mother-daughter-dresses-clothes-chiffon-dress-korean-fashion, 2016-summer-family-matching-outfits-short-sleeved-cotton-matching-family-clothes-t-shirt-family-look-family-matching-clothes, 2016-summer-style-mother-daughter-dresses-family-cotton-flower-print-sleeveless-clothes-family-matching-outfit-family-look, 2018-brand-new-family-matching-swimwear-mother-daughter-women-kids-baby-girls-swimsuit-bikini-one-piece-cute-cat-romper-swimwear, authentic-mother-daughter-dresses-wave-pattern-family-matching-clothes-summer-cotton-t-shirt-family-look-beach-wear-2016
- `2xl`: `Adult 2XL, Adult 2XL-3XL, Boy 2XL (10-11Y), Child XXL, Dad 2XL, Dad XXL, Father 2XL, Father XXL, father XXL, Girl 2XL (10-11Y), Mom 2XL, Mom XXL, Mother 2XL, Mother XXL, XXL`
  Handles: 2016-family-matching-outfits-summer-family-look-clothing-mother-daughter-dresses-clothes-chiffon-dress-korean-fashion, 2016-summer-family-matching-outfits-short-sleeved-cotton-matching-family-clothes-t-shirt-family-look-family-matching-clothes, authentic-mother-daughter-dresses-wave-pattern-family-matching-clothes-summer-cotton-t-shirt-family-look-beach-wear-2016, baby-mother-matching-outfits-summer, battery-themed-matching-family-t-shirt-set-super-tired-parents-energetic-kids
- `3xl`: `Adult 3XL, Dad 3XL, Dad XXXL, Father 3XL, Father XXXL, father XXXL, Mom XXXL, Mother 3XL, Mother XXXL, XXXL`
  Handles: 2016-family-matching-outfits-summer-family-look-clothing-mother-daughter-dresses-clothes-chiffon-dress-korean-fashion, 2016-summer-family-matching-outfits-short-sleeved-cotton-matching-family-clothes-t-shirt-family-look-family-matching-clothes, baby-mother-matching-outfits-summer, bear-wool-matching-family-sweater, beautiful-rainbow-family-matching-t-shirts-colorful-sunshine-design
- `4-5 years`: `Boy 4-5 Years, Child 4-5 Years, Child 4-5 years, Girl 4-5 Years, Girl 4-5 years`
  Handles: chic-color-block-one-piece-swimsuit-for-mother-daughter-vibrant-sleek-beachwear, chic-family-bonding-mother-daughter-matching-swimsuit-set-with-long-sleeved-cover-up, chic-family-tides-mother-daughter-matching-two-piece-swimsuit-with-skirt-vibrant-versatile-swimwear-collection, chic-floral-ruffle-one-shoulder-swimsuit-for-women-and-girls-elegant-asymmetrical-swimwear-set-in-vibrant-tropics-print, chic-leopard-print-one-piece-swimsuit-with-ruffle-accent-timeless-mother-daughter-beachwear
- `4t`: `4T, Boy 4T, Child 4T, Girl 4T`
  Handles: 2016-family-matching-outfits-summer-family-look-clothing-mother-daughter-dresses-clothes-chiffon-dress-korean-fashion, 2016-mother-daughter-clothes-summer-family-mommy-me-girl-fashion-matching-solid-sleeveless-chiffon-dresses-robe-maman-fille, 2016-summer-family-matching-outfits-short-sleeved-cotton-matching-family-clothes-t-shirt-family-look-family-matching-clothes, 2016-summer-style-mother-daughter-dresses-family-cotton-flower-print-sleeveless-clothes-family-matching-outfit-family-look, 2018-brand-new-family-matching-swimwear-mother-daughter-women-kids-baby-girls-swimsuit-bikini-one-piece-cute-cat-romper-swimwear
- `5-6t`: `5-6T, Boy 5-6T, Child 5-6T, child 5-6T, Girl 5-6T`
  Handles: 2016-mother-and-daughter-summer-clothes-family-matching-outfits-mum-girl-beach-bohemian-sleeveless-floral-chiffon-maxi-dresses, beach-party-summer-dress-mommy-me, bear-wool-matching-family-sweater, bohemian-beach-cover-up-mommy-me, boho-chic-family-matching-outfit-flowy-skirts-and-paisley-shirts
- `2t`: `2T, Boy 2T, Child 2T, Girl 2T`
  Handles: 2016-family-matching-outfits-summer-family-look-clothing-mother-daughter-dresses-clothes-chiffon-dress-korean-fashion, 2016-mother-daughter-clothes-summer-family-mommy-me-girl-fashion-matching-solid-sleeveless-chiffon-dresses-robe-maman-fille, 2016-summer-family-matching-outfits-short-sleeved-cotton-matching-family-clothes-t-shirt-family-look-family-matching-clothes, 2018-brand-new-family-matching-swimwear-mother-daughter-women-kids-baby-girls-swimsuit-bikini-one-piece-cute-cat-romper-swimwear, authentic-mother-daughter-dresses-wave-pattern-family-matching-clothes-summer-cotton-t-shirt-family-look-beach-wear-2016
- `5-6 years`: `Boy 5-6 Years, Boy 5-6 years, Child 5-6 Years, Child 5-6 years, Girl 5-6 Years, Girl 5-6 years`
  Handles: battery-themed-matching-family-t-shirt-set-super-tired-parents-energetic-kids, beautiful-rainbow-family-matching-t-shirts-colorful-sunshine-design, chic-family-matching-sleeveless-dresses-ruffled-hem-mother-daughter-summer-outfit, chic-floral-ruffle-one-shoulder-swimsuit-for-women-and-girls-elegant-asymmetrical-swimwear-set-in-vibrant-tropics-print, chic-mother-daughter-one-shoulder-swimsuit-with-playful-ruffles-and-contrasting-stripes-nylon-polyester-blend
- `7-8t`: `7-8T, Boy 7-8T, Child 7-8T, child 7-8T, Girl 7-8T`
  Handles: 2016-mother-and-daughter-summer-clothes-family-matching-outfits-mum-girl-beach-bohemian-sleeveless-floral-chiffon-maxi-dresses, beach-party-summer-dress-mommy-me, bear-wool-matching-family-sweater, bohemian-beach-cover-up-mommy-me, boho-chic-family-matching-outfit-flowy-skirts-and-paisley-shirts
- `2-3 years`: `Child 2-3 Years, Child 2-3 years, Girl 2-3 Years, Girl 2-3 years`
  Handles: beautiful-rainbow-family-matching-t-shirts-colorful-sunshine-design, chic-color-block-one-piece-swimsuit-for-mother-daughter-vibrant-sleek-beachwear, chic-family-bonding-mother-daughter-matching-swimsuit-set-with-long-sleeved-cover-up, chic-family-tides-mother-daughter-matching-two-piece-swimsuit-with-skirt-vibrant-versatile-swimwear-collection, chic-floral-ruffle-one-shoulder-swimsuit-for-women-and-girls-elegant-asymmetrical-swimwear-set-in-vibrant-tropics-print
- ... 45 more groups in the CSV artifact

### Suspicious color values

The exported Color metafield contains composite or non-plain labels. That should be treated as a filter hygiene issue until Search & Discovery is rebuilt around a clean Color-only source.

- `black; white` (multi_color_combo)
  Handles: daddy-me-beer-monster-milk-monster-matching-t-shirt-set, daddy-me-matching-family-t-shirt-set-heartfelt-father-child-bond-outfit, father-and-baby-matching-pizza-slice-t-shirts-whole-pizza-slice-set, father-baby-matching-big-trouble-and-little-trouble-t-shirt-onesie-set-playful-family-outfit, father-baby-player-1-and-player-2-matching-t-shirt-onesie-set-perfect-gamer-dad-gift
- `black; red; white; blue; pink` (multi_color_combo)
  Handles: family-matching-christmas-t-shirts-adorable-reindeer-design, family-matching-christmas-t-shirts-dad-mom-baby-santa-hat-design, family-matching-christmas-t-shirts-festive-reindeer-design, family-matching-christmas-t-shirts-peek-a-boo-reindeer-design, family-matching-christmas-t-shirts-plaid-leopard-tree-design
- `white; blue; pink; black; red` (multi_color_combo)
  Handles: colorful-family-matching-love-t-shirts-fun-bold-lettering-design-in-multiple-colors, cute-family-matching-cartoon-t-shirts-sun-cloud-plant-design-in-5-colors, love-grows-family-matching-t-shirts-watering-can-plant-design, matching-family-minimalist-heart-t-shirt-set-simple-love-design-in-4-colors
- `black; pink; red; white; blue` (multi_color_combo)
  Handles: matching-family-christmas-t-shirts-adorable-reindeer-print-with-holiday-wishes, merry-christmas-matching-family-t-shirts-festive-holiday-outfit-in-multiple-colors, merry-christmas-matching-family-t-shirts-festive-snowman-santa-and-elf-holiday-tops
- `white; blue; black; red; pink` (multi_color_combo)
  Handles: beautiful-rainbow-family-matching-t-shirts-colorful-sunshine-design, cute-dinosaur-family-matching-t-shirts-what-are-you-doing-hug-design
- `white; blue; black; red; yellow` (multi_color_combo)
  Handles: colorful-i-love-family-matching-t-shirts-set-for-the-whole-family, happy-flower-family-matching-t-shirts-colorful-floral-print-for-parents-kids
- `black; green; pink; red; gray; white` (multi_color_combo)
  Handles: dabbing-santa-matching-family-christmas-t-shirts-fun-holiday-outfits-for-all
- `black; red; white; blue; gray` (multi_color_combo)
  Handles: matching-family-christmas-t-shirts-santa-snowman-festive-holiday-design
- `blue; white; red` (multi_color_combo)
  Handles: matching-color-block-knit-sweaters-vibrant-family-pullover-for-mom-and-kids
- `red; black` (multi_color_combo)
  Handles: family-matching-christmas-tree-fair-isle-pajamas-red-black-holiday-pajama-set-for-kids-and-adults
- ... 10 more color values in the CSV artifact

## Collection taxonomy plan

- `new-women-outfits` -> `family-matching-outfits`: Family Matching Outfits (high)
  Current breadcrumb hint: Home > Sets
  Action: Rename handle only after redirects and internal links are mapped; update title/SEO first.
  Reason: Broad family-matching umbrella matches the keyword research and the existing theme-side SEO fallback language.
- `family-sets` -> `family-vacation-outfits`: Family Vacation Outfits (high)
  Current breadcrumb hint: Home > Sets
  Action: Keep the existing handle until redirects are staged, then rename and update breadcrumbs/nav labels in Admin.
  Reason: Keyword research already maps matching family vacation intent to this collection; 'Sets' is too generic for shoppers.
- `family-swimsuits` -> `family-swimsuits`: Family Matching Swimsuits (high)
  Current breadcrumb hint: Home > Mommy and Me
  Action: Keep handle, but align collection title and search listing copy to the exact-match swim intent.
  Reason: This already owns the strongest exact-match swim intent and should stay canonical.
- `mommy-and-me` -> `mommy-and-me`: Mommy and Me (medium)
  Current breadcrumb hint: Home > Mommy and Me
  Action: Preserve as the legacy brand hub unless a deliberate consolidation plan is approved.
  Reason: This is the broad parent hub; it should not be used as the breadcrumb label for Hawaiian or vacation-specific subclusters.
- `daddy-me` -> `daddy-me-t-shirts`: Daddy and Me T-Shirts (medium)
  Current breadcrumb hint: Home > Daddy and Me
  Action: Consolidate the duplicate Daddy-and-Me family collection only after confirming the canonical handle and redirect target.
  Reason: Repo SEO research shows both `daddy-me` and `daddy-and-me` are live; taxonomy is cleaner if one canonical handle owns the intent.

## Safety notes

- This pass is dry-run only. No live Shopify writes were attempted.
- The repository does not currently have Shopify credentials loaded in this shell, so live Admin reads were not performed.

## Remaining operator steps

1. Normalize the dirty size labels in source product data, then re-import or resync the catalog export.
2. Rebuild the Search & Discovery filter configuration after the source data is clean.
3. Decide whether the Color filter should point at a true color-only source or whether pattern-like entries need their own filter.
4. In Shopify Admin, rename collection titles and handles in the order in this plan, staging redirects before any live handle change.
5. Re-verify the collection breadcrumbs and nav labels after the Admin changes land, then QA the live collection pages again.
