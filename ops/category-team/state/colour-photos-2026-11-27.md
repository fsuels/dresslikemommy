# Colour photos audit (2026-11-27, read-only, Admin GraphQL)

Scope: 328 active products. Single-colour or no colour option (out of scope): 248 (202 one colour value, 46 with only Size/Type/Set options). Multi-colour audited: 80. Every colour image was looked at (contact sheets).

## Totals (80 multi-colour products)
- OK: 72 (each colour has its own photo linked; 3 of them, skyfade, picnic-plaid, hooray-sun, link two photos per colour, adult and child garment, deliberately)
- LINK_ONLY: 1 (christmas-knit-family-matching-hats)
- MISSING_PHOTO: 5
- SHARED: 2
- WRONG_LINK: 0 pure (the wrong links below are because no photo of that colour exists, so they are MISSING_PHOTO)

Other colour checks: no product has partially linked variants; all variants of a colour point to the same photo; no gallery image naming a colour is left unlinked, apart from the cases below. Colour names that are print names (swimsuits "Green" for teal) were accepted when the photo matches the name roughly.

## Priority (season first, then 60d sales)
1. happy-faces-family-matching-sweatshirts (fall sweatshirts)
2. christmas-knit-family-matching-hats (Christmas)
3. colorful-i-love-family-matching-t-shirts-set-for-the-whole-family
4. family-matching-original-remix-encore-t-shirt-set-fun-family-outfits-for-all-ages
5. need-more-family-matching-drink-t-shirt-set-beer-coffee-milk-juice-family-outfit
6. dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set (out of season)
7. willow-mist-mommy-and-me-dresses (out of season)
Top sellers by 60d units (Christmas Reindeer 29, Nordic Yoke 27, Santa and Friends 9, Little Heart 7, Cream Heart cardigans 6) have no colour-photo defect: Nordic Yoke Cream/Gray, Santa Red/Green, Little Heart all OK. Christmas Reindeer has no multi-colour option.

## Per product (defects)

### happy-faces-family-matching-sweatshirts , option Color , MISSING_PHOTO
Values: Cream - Mom & Girl, Cream - Dad & Boy, Brown - Mom & Girl, Brown - Dad & Boy. All 60 variants have no image. Gallery (4 photos): 3 family lifestyle shots and one flat lay (media 40707077767265) showing a brown adult and a cream child sweatshirt together. No photo of a single colour. Needed: one flat lay per colour (cream pair, brown pair), then link each. Interim in plan.json: link all four values to the flat lay (group photo, better than blank).

### christmas-knit-family-matching-hats , option Style , LINK_ONLY (shared)
Values Tree Stripe, Garland: 8 variants unlinked. Media 40696718753889 (flat lay) shows both hats (garland top, tree stripe bottom): link both values to it (see plan.json). Better later: one close-up per style.

### colorful-i-love-family-matching-t-shirts-set-for-the-whole-family , option Color
White OK (28160641663073), Blue OK (28160641695841), Black OK (28160641630305), Red OK (28160641597537). Yellow = MISSING_PHOTO: its variants point to the red photo (28160641597537). Gallery has no yellow shirt. (Media 30561299... pink/light-blue lifestyle photos exist unlinked; there is no Pink value.) Needed: yellow flat lay, or remove the Yellow value.

### family-matching-original-remix-encore-t-shirt-set-fun-family-outfits-for-all-ages , option Text
The Original OK in practice; The Remix and The Encore = MISSING_PHOTO: all three designs link to the same photo showing "The Original" shirts. Gallery has 3 photos, all Original. Needed: Remix and Encore photos.

### need-more-family-matching-drink-t-shirt-set-beer-coffee-milk-juice-family-outfit , option Text , SHARED
Milk, Juice, Beer, Coffee all link to one flat lay (30559745704033) showing all four drink shirts. Acceptable group photo; per-design photos would be better.

### vibrant-rainbow-family-matching-outfits-striped-t-shirts-and-yellow-overalls-set-for-family-outings , option Color (actually garment: T-shirt, Short, Overall) , SHARED
T-shirt and Short share the set flat lay; Overall has its own photo. Not colours.

### dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set , option Color
Orange and Pink both link to one flat lay of orange/yellow-teal trunks. Orange OK; Pink = MISSING_PHOTO (no pink trunks in the 3-photo gallery).

### willow-mist-mommy-and-me-dresses , option Color
White OK (31309636239457). Green = MISSING_PHOTO: linked photo 31309636468833 shows the same white dress with blue floral hem; all 4 gallery photos are white. Needed: green dress photo, or rename/remove Green.

### Deliberately split per garment (OK)
skyfade-family-matching-set, picnic-plaid-family-matching-set, hooray-sun-family-matching-sweatshirts: each colour has an adult and a child/garment photo, linked by size group.

## Machine plan
ops/organic/receipts/2026-11-27/colour-photos/plan.json: LINK_ONLY (hats, 8 variants) and interim happy-faces mapping (60 variants) for productVariantAppendMedia. Not run.
