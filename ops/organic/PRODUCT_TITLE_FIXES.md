# Product title native-editor QA (el, da, no, nl, he)

Scope: 73 products listed this month; live titles read 2026-09-30 from `/<locale>/products/<handle>.js`. Not written to Shopify; the listing session registers them from `PRODUCT_TITLE_FIXES.json` (`{handle: {locale: title}}`).

Counts: 72 of 73 products changed, each in all 5 locales (el 72, da 72, no 72, nl 72, he 72). Unchanged: `christmas-knit-family-matching-hats` (already natural in all 5).

## Top recurring issues
1. Title Case leftovers in da/no/nl/el (Matchende, Bijpassende, Ασορτί, Todelt, Tweedelige, Με ...) against the sentence-case rule.
2. Design name run into the product phrase with no separator ("Smilende hjerte Matchende sweatshirts...").
3. Literal or wrong design names: nl "bies" (trim), "Kerstman en de Piek", "Kersttruien van Red Truck Siblings"; da/no "polkagris" (Swedish) for candy cane; da "Hurra og sol"; no "Julenissens stjerne" for a tree topper; el "Αρκουδάκι πάντα" (reads "always"); he "פסים של כפר מושלג", "סריגת".
4. Glossary drift: el "ταιριαστές" instead of "ασορτί"; nl "gezinstruien"; en-dash before the descriptor instead of em dash; he "אייל" (deer) instead of "אייל צפוני" (reindeer); inconsistent geresh in פיג'מות.
5. Invented detail: "round" collar added to Blue Gingham Collar (removed); Danish/Norwegian "Julesweatshirt" duplicating the product noun.
6. Halloween/Christmas set descriptors varied per title; unified per language.

## Conventions chosen
- Template: `{design} – {product + audience} — {descriptor}` (en dash after the design, em dash before the descriptor), same in all 5 locales including he. Siblings titles keep the design inside the phrase.
- Translate descriptive design names idiomatically. Kept in English: Together Heart, Pure Joy (slogan-style), Jingle Bells, We Are Family, Fair Isle. Ho Ho kept as "Ho Ho".
- Colours: navy = el μπλε μαρέν, da/no marineblå, nl marineblauw, he כחול נייבי; evergreen = grangrøn / skoggrønn / dennengroen; buffalo plaid via glossary; burgundy = el μπορντό, da/nl bordeaux, no burgunder.
- Burgundy Trim Crew = "burgundy with round neck and contrast trim" (da "kontrastkant", nl "contrastrand"); "bies" dropped.
- Reindeer = el τάρανδος, da rensdyr, no reinsdyr, nl rendier, he אייל צפוני.
- Sentence case for el/da/no/nl.

## Flags for the listing session
- `red-cable-cardigan-mommy-and-me-sweaters` and `argyle-wool-mommy-and-me-cardigans`: English titles say "Sweaters" (argyle handle says cardigans). Translations use the Cardigans glossary value. If the garments are pullovers, swap to the sweater phrase, or fix the English title.
- Greek titles often exceed the ~70 character target (max 110); shorten by dropping the descriptor if a length limit bites.
- Halloween pajamas: he spelled "האלווין" and Greek/Latin "Halloween" kept as-is.
- Native-editor review by model, not a paid human review.
