# Store search audit (read-only), 2026-11-27

Method: built-in browser, own tab, 24 page loads at 10 s spacing (`/search?q=...&type=product`, `/es/`, `/de/`). No 429, 403 or verification page appeared. Nothing was changed. Result counts are the number in the page title. Queries were not typed into the search box; the results page was loaded directly. Not tested: predictive-search dropdown and the empty-state page (no term returned zero).

Terms come from Search Console demand (organic-demand-hubs-2026-11-27.md) plus obvious product words.

| # | Term | Lang | Results | Relevant? | First results | Note |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | christmas sweater | en | 76 | yes | Christmas Reindeer Family Matching Sweaters; Jingle Bells Santa Family Matching Sweaters | Good. |
| 2 | family pajamas | en | 287 | yes | Jolly Crew Family Matching Pajamas; Buffalo Plaid Tree; Plaid Tree Trio | Count 287 shows OR matching ("family" or "pajamas"); top is fine. |
| 3 | mommy and me dress | en | 328 | yes | Lavender Floral Applique Ruffle Dress; Ivory Dot Mommy and Me Dresses; Watercolor Stripe Maxi | Good. |
| 4 | matching swimsuit | en | 252 | yes | One Shoulder Swimsuit; Sunflower Print Swimsuit; Two-Piece Swimsuits | Good. |
| 5 | maternity dress | en | 190 | yes | Dotted Tulle Off-Shoulder Maternity Photoshoot Gown; Ivory Pleated Rosette Dress | Good (gowns are the whole maternity range). |
| 6 | dad and son shirt | en | 181 | yes | Father & Son Matching Shirts Palm Print; Dad & Son Navy Tropical Shirts | Good ("dad" matches "father" and "daddy"). |
| 7 | couple hoodie | en | 68 | partly | Pure Joy Heart Family Matching Hoodies; Striped Fleece Hoodies; Reindeer Row Sweaters | Family hoodies, not couple items; no couples hoodie exists, so sweaters mix in. |
| 8 | baby | en | 128 | partly | Family Matching Cardigans; Dotted Tulle Maternity Gown; Daddy and Me Shirts (Onesie Set); Cream Heart Cardigans | Maternity gown ranks 2nd for "baby" (matched on "baby bump" text). Hard to say what the shopper wants. |
| 9 | plus size | en | 69 | no | Dotted Tulle Maternity Photoshoot Gown; Pleated Ruffle Tulle Gown; Tiered Tulle Gown; Bloom Fishtail Gown; Floral Tulle Cape Gown | Only maternity gowns, which mention extended sizes. Nothing for mommy-and-me or family sets, and no size info to filter. |
| 10 | red dress | en | 186 | partly | Red Tropical Leaf Mommy and Me Dresses; Dotted Tulle Maternity Gown; Navy Red Floral Family Set; Rainbow Maxi Dresses | Only the 1st is clearly red; rest match "dress" alone. Maternity gown at rank 2 is odd. |
| 11 | matching family christmas sweaters | en | 291 | yes | Christmas Reindeer; Jingle Bells Santa; Nordic Heart Reindeer | Good order; count 291 is OR matching. |
| 12 | mommy & me | en | 307 | yes | Cream Heart Cardigans; Ivory Dot Dresses; Bamboo Garden Panda Pajamas | Works (ampersand handled). Pajamas appear in top 5. |
| 13 | sweter (typo) | en | 67 | yes | Nordic Yoke Family Matching Sweaters; Cable Knit Heart Pullovers; Reindeer Row | Typo tolerated. |
| 14 | pajama (singular) | en | 52 | yes | Jolly Crew Pajamas; Bamboo Garden Panda; Vintage Cottage Floral | Singular works. |
| 15 | suéter navideño | es | 57 | yes | Suéteres navideños a juego para toda la familia (hilera de renos, reno nórdico, renos) | Good, Spanish titles. |
| 16 | vestidos mamá e hija | es | 211 | yes | Vestidos largos de rayas arcoíris; "Vestidos mamá e hija – White Rosette: Vestido sin mangas con gradas"; Vestidos a juego con hojas tropicales rojas | Relevant, but several titles are untranslated English mixed in ("White Rosette", "Ivory Dot"). |
| 17 | pijamas familia | es | 215 | yes | Equipo Alegre Pijamas; Pijamas navideños trío de árboles; Somos Familia Verde Pino | Good. |
| 18 | ropa a juego | es | 232 | yes | Conjunto de camisa y vestido a juego floral; Looks a juego para la familia; Sunshine Daisy | Good. |
| 19 | traje de baño | es | 41 | yes | Traje de baño de un hombro mamá y niño; Trajes de baño mamá y yo paisley azul; con remolinos | Good. |
| 20 | weihnachtspullover | de | 49 | yes | Familien-Partnerlook Weihnachtspullover (Weihnachtsmann, Rentiere, Rentierreihe) | Good. |
| 21 | partnerlook familie | de | 282 | yes | Pullover mit nordischer Passe; Strickjacken Marineblau/Rot; Weihnachtspullover Rentierreihe | Good. |
| 22 | mutter tochter kleid | de | 72 | yes | Set Strickjacke und Kleid Mutter Tochter; Kleider mit roten tropischen Blättern; Ozeanblau | Good. |
| 23 | umstandskleid | de | 31 | yes | Umstandskleid aus gepunktetem Tüll; Elfenbeinfarbenes plissiertes Umstandskleid | Good. |
| 24 | badeanzug | de | 33 | yes | Passende Bademode mit einem Träger; Langarm-Mama-Tochter-Badeanzüge; Bikini-Sets | Good (bikini sets mixed in, acceptable). |

## Summary

- 24 terms tested, 0 returned an empty page. 20 fully relevant, 3 partly (couple hoodie, baby, red dress), 1 not relevant (plus size).
- All three languages return results in the right language; sweaters, pajamas, swimsuits, maternity and dresses are well covered. Typo ("sweter") and singular ("pajama") are tolerated.
- Weakness: search matches any word (OR logic), so counts are inflated (287 for "family pajamas") and generic words pull unrelated products (maternity gowns for "baby", "red dress", "plus size").

## Weak terms by probable cause, with suggested fix (none applied)

1. **plus size (no) - word not in titles/tags.** Results are maternity gowns that happen to mention sizes in their text. Suggested fix: add a "plus size" / "size inclusive" tag only to products whose size chart truly goes above 2XL (owner/sourcing must confirm which; do not claim it otherwise), and add the same in Spanish/German. Otherwise the best answer is a short size-guide page linked from the search page.
2. **baby (partly) - no synonym, text match too loose.** The word appears in descriptions ("baby bump", onesies) so maternity gowns rank 2nd. Fix: tag the real baby/toddler items (onesie sets, baby sizes) "baby" and let Search & Discovery boost them; the boost and any synonym ("baby" = "infant, newborn, onesie") can only be set by the owner in the Search & Discovery app.
3. **couple hoodie (partly) - word not present / no product type.** There are no couples hoodies; family hoodies and knit sweaters show. Fix: add "couple", "his and hers", "couples matching" to the titles/tags of family hoodies and sweatshirts that adults wear (a few products), or a synonym "couple" = "his and hers, matching adults" in Search & Discovery (owner only). Check the couples collection exists before pointing search at it.
4. **red dress (partly) - colour missing from titles/tags.** Only one title says "Red". Fix: add a colour tag (red, burgundy) to the dresses and gowns that are red in any variant, or enable the colour filter in Search & Discovery (owner only) so shoppers can narrow.
5. **Mixed language titles in Spanish (vestidos mamá e hija).** Some titles still carry English names ("White Rosette", "Ivory Dot"). Not a failure but looks unfinished; list of such titles can be pulled with a full es crawl if wanted.
6. **General (typo tolerance is fine; the issue is OR matching).** Multi-word terms return hundreds of results. The relevance order is mostly right, so no change is urgent; optionally ask the owner to check in Search & Discovery whether the "all words must match" option can be enabled, which would cut noise for terms 8, 9, 10.

## Untested / limits

- Predictive dropdown, spelling "did you mean" suggestions, and the empty-result page were not exercised because no term returned zero. A deliberate nonsense term was not tried (outside the 24-term plan).
- Only the first five titles were judged; deeper ranking was not reviewed.
