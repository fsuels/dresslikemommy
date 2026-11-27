# Collection membership audit 2026-11-27

Source: Admin API read-only, 2026-11-27. Receipts: ops/organic/receipts/2026-11-27/collection-membership/raw.json

## Totals
- Published collections: {len(cols)} ({sum(1 for c in cols if not c["ruleSet"])} manual, {sum(1 for c in cols if c["ruleSet"])} smart; {sum(1 for c in cols if not c["publishedOnPublication"])} not published to Online Store)
- Active products published to Online Store: 328 of 328 active
- (a) Missing from a hub (clear, unambiguous): 0 actionable
- (b) Orphans (no collection, or only catch-alls new-arrivals/matching-outfits/best-sellers/family-bundle-eligible/new-matching-outfits/new-women-outfits/popular-*): 0
- (c) Misplaced: 39 product-in-collection pairs (19 pajama hold, 20 sweatshirts in sweaters hubs)

## Hub collections (all smart except noted)
Manual: new-pajama-drop (18, pajamas: hold), thanksgiving-family-outfits (29). Every other hub is smart (tag/type rules): family-sweaters (Family Matching+Sweaters), christmas-sweaters (Christmas Sweaters), matching-family-sweatshirts (type Family Matching Sweatshirts), maternity (Maternity), swimsuits (Swimsuits or Mommy and Me), couples, daddy-and-me, mother-daughter-matching-dresses (dress tags), family-tops. Rules were not edited.

## (a) Missing
None. Every product whose title clearly names a hub appears in it. Considered and rejected: 8 father-and-son swim trunks are not in swimsuits but are in daddy-and-me and trunks (their home hubs; swimsuits is not their category). If wanted in swimsuits (smart) they would need tag Swimsuits; no rule edit proposed. Thanksgiving (manual): no product is unambiguously Thanksgiving beyond the 29 already in.

## (b) Orphans
None. All 328 active products are in at least one specific collection.

## (c) Misplaced
| handle | title | collection | proposed | reason |
|---|---|---|---|---|
| spooky-skeleton-family-matching-onesie-pajamas | Spooky Skeleton Family Matching Pajamas — Hooded Onesies | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| pumpkin-ghost-family-matching-pajamas | Pumpkin Ghost Family Matching Pajamas — Halloween Two-Piece Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| beanie-ghost-family-matching-pajamas | Beanie Ghost Family Matching Pajamas — Halloween Two-Piece Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| boo-stripe-family-matching-pajamas | Boo Stripe Family Matching Pajamas — Halloween Two-Piece Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| trick-or-treat-family-matching-pajamas | Trick or Treat Family Matching Pajamas — Halloween Two-Piece Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| classic-red-plaid-family-matching-pajamas | Classic Red Plaid Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| evergreen-fair-isle-family-matching-pajamas | Evergreen Fair Isle Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| jolly-crew-family-matching-pajamas | Jolly Crew Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| joyful-merry-blessed-family-matching-pajamas | Joyful Merry Blessed Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| let-it-snow-family-matching-pajamas | Let It Snow Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| lights-out-reindeer-family-matching-pajamas | Lights Out Reindeer Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| plaid-reindeer-family-matching-pajamas | Plaid Reindeer Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| plaid-tree-trio-family-matching-pajamas | Plaid Tree Trio Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| snowy-village-stripes-family-matching-pajamas | Snowy Village Stripes Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| we-are-family-evergreen-family-matching-pajamas | We Are Family Evergreen Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| we-are-family-red-family-matching-pajamas | We Are Family Red Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| blue-plaid-reindeer-family-matching-pajamas | Blue Plaid Reindeer Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| green-plaid-merry-tree-family-matching-pajamas | Green Plaid Merry Tree Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| buffalo-plaid-tree-family-matching-pajamas | Buffalo Plaid Tree Family Matching Pajamas — Christmas Set | couples | none (hold: pajama) [HOLD] | family pajamas inside couples (via tag Father Pajama Set) |
| santa-and-friends-family-matching-sweatshirts | Santa and Friends Family Matching Sweatshirts — Christmas Crewneck | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| santa-and-friends-family-matching-sweatshirts | Santa and Friends Family Matching Sweatshirts — Christmas Crewneck | christmas-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| smiley-heart-family-matching-sweatshirts | Smiley Heart Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| eternal-bliss-hearts-family-matching-sweatshirts | Eternal Bliss Hearts Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| little-heart-family-matching-sweatshirts | Little Heart Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| good-luck-smile-family-matching-sweatshirts | Good Luck Smile Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| moon-and-star-family-matching-sweatshirts | Moon and Star Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| starry-sky-family-matching-sweatshirts | Starry Sky Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| little-lamb-family-matching-sweatshirts | Little Lamb Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| scribble-heart-family-matching-sweatshirts | Scribble Heart Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| hooray-sun-family-matching-sweatshirts | Hooray Sun Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| happy-faces-family-matching-sweatshirts | Happy Faces Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| cute-happy-bunny-bear-family-matching-sweatshirts | Cute Happy Bunny Bear Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| panda-family-matching-sweatshirts | Panda Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| make-life-sweet-family-matching-sweatshirts | Make Life Sweet Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| duck-parade-family-matching-sweatshirts | Duck Parade Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| one-big-star-family-matching-sweatshirts | One Big Star Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| san-francisco-family-matching-sweatshirts | San Francisco Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| sky-blue-stripe-family-matching-sweatshirts | Sky Blue Stripe Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |
| double-heart-family-matching-sweatshirts | Double Heart Family Matching Sweatshirts — Crewneck Tops | family-sweaters | matching-family-sweatshirts (already in) | sweatshirt inside sweaters hub |

Note: removal not performed or proposed as an action; all affected collections are smart, so fixing means changing a tag (sweatshirts carry tag Sweaters; family pajamas carry tag Father Pajama Set that couples rules match). Needs an owner decision on tags/rules.

Borderline (not flagged): sweaters in christmas-sweaters without "Christmas" in title (red/burgundy/nordic/heart sweaters, tagged Christmas Sweaters).

## Pajama cases on hold
All 19 family pajama products in couples (Halloween and Christmas family pajamas) plus new-pajama-drop (manual). No pajama added anywhere.

## Follow-up 2026-11-27: swim trunks into swimsuits (NOT applied)
Re-read of rules: swimsuits = tag Swimsuits AND tag Mommy and Me (appliedDisjunctively=false, all conditions must match). family-swimsuits = Family Matching AND Swimsuits. The father-and-son trunks have neither Mommy and Me nor Family Matching, so adding only "Swimsuits" would NOT put them in swimsuits. Making them enter would require also adding "Mommy and Me" (a mommy tag on dad-and-son items; it would also put them in mommy-and-me/tops-style collections tied to that tag, e.g. new-matching-outfits, popular-mommy-me-1, pajamas rules). Not safe, so no tag was written. Note: most smart rules here are AND, so the earlier rule descriptions above should be read as AND where "tag X + tag Y" is listed. Before-state saved in swim-tag-before.json (9 trunks products, counts per collection).
