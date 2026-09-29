# Translation QA (2026-09-29)

Independent native-editor review of live translations: 5 articles x 6 languages (el, da, no, nl, he, de) = 30 samples.
Read from the live storefront pages plus the stored field values (title, body_html, summary_html, meta_title, meta_description).
Grades are before fix, with the post-fix grade after the arrow. A = publishable, B = understandable with real errors, C = visibly machine-made.
Fixes went through `organic_engine.py translate-apply --execute` (verified true). Receipts: `ops/organic/receipts/2026-09-29/tqa-<handle>.json`.

Honesty check (all 30): no added stock, fast-shipping, discount, review or bestseller claims. Pajamas-guide delivery (12-16 days estimate, "not guaranteed"), standard shipping and 30-day returns lines match the English source. Brand kept as "Dress Like Mommy" everywhere. No leftover English in bodies beyond product names and accepted loanwords.

Articles: COUPLES = matching-couples-christmas-pajamas-and-sweaters, CARD = family-christmas-card-photo-ideas, MOMMY = mommy-and-me-matching-outfit-ideas, DADDY = daddy-and-me-matching-outfits-the-ultimate-guide, PJ = matching-family-christmas-pajamas-guide-2026.

| Article | Lang | Grade | Issues found / fixed |
|---|---|---|---|
| COUPLES | el | A | None. |
| COUPLES | da | A | None (minor: "jule-pyjamas" hyphenation, left). |
| COUPLES | no | A | None. |
| COUPLES | nl | B -> A | "dezelfde kleurenpalet" (het-word) fixed to "hetzelfde". |
| COUPLES | he | B -> A | "האזיקים" (handcuffs) for sleeve cuffs fixed to "החפתים"; "הקציפו בקיטור" (whip with steam) fixed to "אדו"; typo "הלבוקים" fixed to "הלוקים". |
| COUPLES | de | A | "schlaffreundlichen Schnitt" reworded to a natural phrase. |
| CARD | el | B -> A | "ο ... οδηγό" wrong case in 3 links, fixed to "οδηγός". |
| CARD | da | B -> A | Missing "vores" before a guide link (grammar); meta title was keyword-stacked ("Julekortfoto Familie: ...") fixed. |
| CARD | no | B -> A | "bilder på høyde" (nonsense for portrait) fixed to "stående/liggende"; missing "vår" before guide link; "pyjamaser" fixed to "pysjamas"; keyword-stacked meta title fixed. |
| CARD | nl | B+ -> A | Meta title, meta description and summary were keyword-stacked ("Kerstkaart familiefoto ideeën") fixed to natural Dutch. |
| CARD | he | B+ -> A | "מצלם עצמי" (not a term) fixed to "טיימר". |
| CARD | de | B -> A | Ungrammatical H1/meta ("Familien-Weihnachtskarte Foto Ideen", "Weihnachtskarte Familienfoto Ideen") rewritten as "Ideen für das Familienfoto auf der Weihnachtskarte"; summary and meta description updated. |
| MOMMY | el | B -> A | H1 said "Μαμά και Κόρη" (daughter only) vs "Μαμά και Παιδί"; "θα το προλάβουν" (will make it in time) fixed to "θα το γεμίσουν σύντομα"; broken clause "από ... ιδέα οικογενειακή παράδοση" fixed. |
| MOMMY | da | B -> A | "modeforvent" (not a word) fixed to "moderigtigt"; meta title inconsistent with H1 and keyword-stacked, fixed. |
| MOMMY | no | C -> A | "Juleplyjamas" typo, "ferimiddager" typo, "feriekle" (not a noun), "motefremmende", "helstøpte badedrakter" (wrong sense), "Proffe tips", "samstemt(e)" for "coordinated", "utfyllende" for "complementary": all fixed. |
| MOMMY | nl | B -> A | "dezelfde kleurenpalet"; H1 "Mama en ik Bijpassende outfits" awkward; meta title had English "Matching"; meta description said "vakanties, vakanties" and "informele dagen": all fixed. |
| MOMMY | he | B+ -> A | Meta description mixed masculine "גלה" and feminine "קני", fixed to plural "גלו/קנו"; meta title "אאוטפיטים" changed to "תלבושות" to match H1. |
| MOMMY | de | A | None (du/ihr register mixed in CTAs, style only). |
| DADDY | el | B+ -> A | H1 "Πανομοιότυπα" (identical) vs "Ασορτί" everywhere else, fixed to "Ασορτί Ρούχα για Μπαμπά και Παιδί". |
| DADDY | da | B+ -> A | Meta title lacked "til" ("Matchende tøj far og søn"), fixed. |
| DADDY | no | A | None. |
| DADDY | nl | B -> A | "boven hen uit torenen" and "kan dochter" (missing article) fixed; H1 "Papa en ik Bijpassende outfits" and meta title with English "matching" fixed. |
| DADDY | he | B -> A | "גוני חמים" (ungrammatical) fixed to "גוונים חמים"; meta description ended in a stray fragment, fixed; meta title aligned with H1 wording. |
| DADDY | de | A | None. |
| PJ | el | A | None. |
| PJ | da | B+ -> A | Stuttering after product-name links ("pyjamas med tre juletræer tre juletræer", "... rensdyr rensdyrører") fixed by using the product names as link text. |
| PJ | no | A- -> A | Meta title used "julepysjamaser" (non-idiomatic plural), fixed. |
| PJ | nl | A | None. |
| PJ | he | A- | None needed. |
| PJ | de | A- -> A | Meta title keyword-stacked ("Weihnachtsschlafanzüge Partnerlook Familie 2026"), fixed. |

## Verdict per language

- **el (Greek)**: Strong. Body text fluent; errors were limited to one recurring case-ending slip and two H1 wording mismatches. Fixed.
- **da (Danish)**: Good. Body reads natively; weak spots were meta titles (keyword stacking) and product-link stutter. Fixed.
- **no (Norwegian)**: Weakest of the set on the older "mommy" article (word-choice errors, typos); newer engine articles are clean. Fixed. Recommend a spot check of other older Norwegian articles for "samstemt", "utfyllende", "feriekle".
- **nl (Dutch)**: Good body text; recurring "dezelfde kleurenpalet" gender slip, English "matching" leftovers and awkward capitalised H1s in older articles. Fixed.
- **he (Hebrew)**: Good, but had three real word errors (handcuffs for cuffs, whip-with-steam for steam, "מצלם עצמי") and mixed gender in meta. Fixed.
- **de (German)**: Best overall. Only defect was the card article's ungrammatical title and meta; fixed. Register mixes du/ihr/Sie across articles (style, not changed).

## Findings outside the reviewed fields (not changed)

- Theme-level strings on translated pages: Norwegian "Kobling" for "Link"; Greek "εμφανίσεις" for "looks" in CTAs and a wrong collection card name "Ταίριασμα μπλουζάκια και μπλουζάκια"; Dutch article tag "Paren bijpassende outfits"; Danish author blurb "pyjamasser". These live in theme locale files or collection/tag translations, not article fields.
- Older articles (2025, by "Jessica Martinez") use Title Case headings in da/no/nl/el, an English convention; left as style.

## Method limits

Sampled 30 of roughly 75 articles x many languages; the sample favours the top-traffic languages. Findings suggest the older non-engine articles (MOMMY, DADDY) carry more errors than the newer engine-built ones. Italian and the remaining languages were not read.

## Hebrew sweep

Full read of 15 live `/he/blogs/news/` articles (title, meta title, meta description, summary, body) against the stored `he` translations and the English source. Grades are before fix, with the post-fix grade after the arrow. 13 articles were corrected through `organic_engine.py translate-apply --execute` (verified true, `unresolved_after` empty). Receipts: `ops/organic/receipts/2026-09-29/heqa-<handle>.json`. Honesty check: no stock, shipping-speed, discount or review claims added; brand kept as "Dress Like Mommy".

| Article (handle) | Grade | Issues found / fixed |
|---|---|---|
| mommy-and-me-outfits-for-every-budget | B -> A | Mixed gender (feminine singular "את מחפשת/שאת רוצה/לך" against plural imperatives) made consistently feminine plural; "הציצו ב <a>" spacing fixed so the prefix attaches. |
| mommy-and-me-matching-outfit-ideas | B -> A | Title and meta used literal "אמא ולי", now "אמא ולילד" like the meta title; "בללבוש" fixed to "בלבישת"; "שום דבר לא עובר" (nothing passes) fixed to "מנצח"; masculine/feminine mix ("אתם" vs "אתן") aligned; "ימי פנאי" in meta fixed. |
| best-matching-swimsuits-for-the-whole-family | A- -> A | "לאחרי החוף" fixed. |
| mother-daughter-matching-swimsuits-complete-guide-for-summer | B -> A | "תחתונים" (underwear) for swim bottoms fixed to "תחתוני ביקיני" / "מכנסי שחייה"; "אשרו" (approve) for confirm fixed to "ודאו"; "התחלפו" fixed to "החליפו"; title "לאם ובת" aligned to "לאמא ולבת". |
| fall-family-matching-outfits | A- -> A | "שכבו בחוכמה" (lie down wisely) fixed to "לבשו שכבות בחוכמה". |
| the-complete-guide-to-family-matching-outfits | A- -> A | Infinitive link text with feminine predicate ("להתלבש ... היא") fixed to a noun. |
| what-to-wear-for-family-photos-matching-outfit-ideas | B -> A | Untranslated English link labels ("Mommy and Me", "Daddy and Me") localized; "טיפים מצלמי" missing prefix fixed; "זמינו לעצמכם זיכרונות" (invite yourselves memories) fixed. |
| holiday-family-matching-outfits-complete-guide | B -> A | Six English image alt texts translated; "כמוך" (singular) fixed to "כמוכם"; "שכבו בחוכמה" fixed. |
| christmas-matching-family-pajamas | B -> A | "שחייבים" (must-have) heading fixed to "שחובה שיהיו לכם"; "תואמות בדיוק" fixed to "בצורה מושלמת"; "שכבו בחוכמה" fixed. |
| matching-family-christmas-sweaters-guide-2026 | A- -> A | "מתייחסות לעניין" fixed to "לנושא"; product label "סנטה מביא עץ" fixed; "וגם" list join and "להתנסות" fixed. |
| family-christmas-photo-outfits-2026 | A | None. |
| daddy-and-me-christmas-outfits | A | None. |
| matching-family-christmas-shirts | A- -> A | "להיראות שונה" agreement, stray space before comma, "סמוך למועד יעד" fixed. |
| matching-family-shirts-for-pictures | B -> A | "הקציפו בקיטור" (whip with steam) fixed to "אדו"; same error class as the earlier COUPLES/he fix. |
| family-matching-pajamas-our-top-picks-for-cozy-nights | B -> A | Meta description ended in a broken fragment and mixed a feminine singular; rewritten. "אשרו" (approve) used for confirm in seven places, fixed to "ודאו". |

Left alone (source-level, not translation): product-title clutter in headings ("... | DLM", truncated "Little Tr...") in the swimsuit and Christmas pajamas articles and a stray `</h3>` in the pajamas article come from the English source; product names such as "Mommy and Me" inside product link labels kept as brand/product naming.

## Norwegian sweep

Date 2026-09-29. Scope: 15 live Norwegian (Bokmål, `no`) blog articles, read as a strict native editor against the stored Admin translations (same text as the live page; two pages re-fetched live after the write to confirm). Fixes registered with `organic_engine.py translate-apply --execute`; every write read back `verified: true`. Receipts: `ops/organic/receipts/2026-09-29/noqa-<handle>.json`. English, other languages, products and theme untouched.

| Article | Grade | Main problems fixed |
|---|---|---|
| what-to-wear-for-family-photos-matching-outfit-ideas | C -> A | "samstemt/samstem/samstemme" (means "in agreement") used 8 times for "coordinated"; "Travle mønstre" calque; "syns"; Title Case meta title; H2 "Familiefoto-antrekk"; "begge looker". |
| winter-family-photo-outfits-matching-looks-for-cold-weather | B -> A | Wrong plural "toppe" (x5) for "topper"; "like som mamma og pappa"; unnatural title "Vinterfamiliebilder"; Title Case meta title; "mommy & me jumpsuits" in alt text. |
| thanksgiving-family-matching-outfit-ideas | B -> A | 7 image alt texts left in English; "Shop looksene"; non-word "bildevakker"; "pyneste"; missing comma; Title Case meta title. |
| holiday-family-matching-outfits-complete-guide | B -> A | 6 image alt texts in English; "er lik deg" (for "kledd likt"); "vrengt"; Title Case meta title. |
| christmas-matching-family-pajamas | B -> A | "slår ingenting gleden ved" (garbled); "uvanlige minner"; "hjortemønster" for reindeer; stray double `</h3></h3>`; plural "julepyjamaser" in title. |
| daddy-and-me-christmas-outfits | B -> A | Keyword-stacked title and meta title ("Pappa og barn juleantrekk ... pappaer og barn"); "Koblingen er fargen"; "ryggtur"; "følge en pakke"; plural "pyjamaser". |
| matching-family-shirts-for-pictures | B -> A | English Title Case in title, meta title and 8 H2s; "jeansen ... leggingsen"; "tilgivende" (calque); "Et trykk som det"; "travle mønstre". |
| mommy-and-me-outfits-for-every-budget | B -> A | "legg inn et lager" (x2, calque of "stock up"); "Kjøp under salg"; "nedsatte priser ... er store"; "ideelle punktet"; plural "pysjamaser". |
| fall-family-matching-outfits | B -> A | Title "Høstfamilie matchende antrekk"; "ingenting som gleden ved" (garbled); "størrelse opp til barna"; "pyjamaser". |
| family-matching-pajamas-our-top-picks-for-cozy-nights | B -> A | Calque title "Familie-matching pysjamas"; "samstemt bilde"; "hver valgt variant"; "listing under pajamas" mistranslated as "plassering"; "som plass til vekst". |
| best-matching-family-outfits-for-winter | B -> A | "Shop familiegensere" left in English; "ankerplagget" (anchor calque); "De sterkeste anbefalingene"; "Handle smartere ..." summary; Title Case meta title; "overdrevet". |
| the-complete-guide-to-family-matching-outfits | B+ -> A | "utfyllende stiler" (complementary calque); "julebordet"; "sweet spot"; "se fantastisk ut på"; "unnskyldning til"; Title Case meta title. |
| matching-family-christmas-shirts | B+ -> A | "samstemt"; "varmt hus"; missing space before "hvis" and stray space before comma; "til å sammenligne"; meta description ended mid-thought. |
| matching-family-christmas-sweaters-guide-2026 | A- -> A | "kremfargede tilbehør" (gender); "vil like et dyretema"; "produktside til plaggets mål"; plural "julepysjamaser". |
| family-christmas-photo-outfits-2026 | A -> A | "border" (English) for "bord"; plural "pysjamaser" in meta and summary. |

Result: 1 C, 12 B/B+, 2 A-/A before; all 15 A after edits. Recurring cause: the older non-engine articles were machine-translated with English word order and Title Case; the newer engine articles were near-clean.

Remaining, not changed:
- Product-link headings such as "Tropiske strandantrekk ... | DLM" are truncated source product titles, kept as translated.
- "skjorter" is used for t-shirts and sweatshirts in matching-family-shirts-for-pictures (source term "shirts"); understandable, left as-is.
- Older articles still carry Title Case headings in other Norwegian articles not in this sweep; the theme-level "Kobling" for "Link" noted in the earlier sweep is unchanged.

## Dutch sweep

Date 2026-09-29. Scope: 15 live Dutch (`nl`) blog articles, read as a strict native editor against the stored Admin translations (same text the live `/nl/blogs/news/` pages render). 14 corrected through `organic_engine.py translate-apply --execute` (`verified` true, `unresolved_after` empty); receipts `ops/organic/receipts/2026-09-29/nlqa-<handle>.json`. No stock, shipping-speed, discount or review claims added; "Dress Like Mommy" kept; "matchende/matching outfits" kept where it is the natural search term.

| Article (handle) | Grade | Main problems fixed |
|---|---|---|
| mommy-and-me-matching-outfit-ideas | B -> A | Title Case headings; "matchmoment", "matchlook", "buitenshoots" and "Klaar om te gaan matchen?" reworded. |
| mommy-and-me-outfits-for-every-budget | B -> A | Calque title "Mama en ik Outfit voor elk budget"; "dezelfde kleur top" reworded. |
| daddy-and-me-matching-outfits-the-ultimate-guide | B -> A | Untranslated filler "gezinsmatching-momenten"; "de helft van de outfit voor dochter"; "Bijpassend in de feestdagen is helemaal je ding". |
| fall-family-matching-outfits | B -> A | Calque title "Herfst Familie Matchende Outfits"; "layeren"; "op koud water ... met kleuren die erbij passen". |
| best-matching-family-outfits-for-winter | B -> A | Title Case meta title; clumsy summary ("familie-outfits"); "layeren"; "om om te kleden"; "Klaar om te beginnen met matchen". |
| the-complete-guide-to-family-matching-outfits | B -> A | Meta description grammatically broken; "familiekleding zijn" (agreement); "Bijpassend zijn kent niveaus"; "De setting negeren"; Title Case meta title. |
| what-to-wear-for-family-photos-matching-outfit-ideas | B -> A | Title Case meta title; "moeder-dochter jurklooks" spelling; "op te tuigen"; "layeren"; English link labels "Mommy and Me / Daddy and Me". |
| holiday-family-matching-outfits-complete-guide | B -> A | Six English image alt texts translated; Title Case meta title; "Laag slim" imperative. |
| christmas-matching-family-pajamas | B -> A | Calque title "Kerstmatchende Familiepyjama's"; wash-care phrase "koud te wassen met kleuren die erbij passen". |
| matching-family-christmas-sweaters-guide-2026 | A | None; not changed. |
| family-christmas-photo-outfits-2026 | B -> A | "om om te kleden"; garbled "Kies voor pyjamafoto's binnen ..." and "combineer broeken ... dan"; "Combineer je verschillende truien"; "bij elke setting". |
| daddy-and-me-christmas-outfits | B -> A | Keyword-stacked title and meta title ("Vader en kind kerstoutfits ... matchende ideeën"); "vader en kind look/collectie/shirts" as separate words; "een felle accessoire" (het-word); "kun je december genieten". |
| matching-family-christmas-shirts | B -> A | "een felle accessoire"; stray spaces before "." and "," and missing space after a link; "kun je december genieten"; "een vader en kind". |
| matching-family-shirts-for-pictures | B -> A | English Title Case in title, meta title and 8 H2s; "familie shirts" split compound (title, meta, summary); "layeren"; link texts "familie kerstshirts/kerstoutfits". |
| family-christmas-card-photo-ideas | B -> A | Title Case title and 6 H2s; "tee" and "kersttruien-gids"; "makkelijk in maat te kiezen". |

Result: 14 B, 1 A before; all 15 A after edits (post-edit grades are the editor's own; no independent re-read yet).

Remaining, not changed: product-name headings and link labels in English or truncated ("... | DLM", "Vibrant Rainbow Mommy and Me", "Jingle Bells") come from source product titles; stray `</h3></h3>` in christmas-matching-family-pajamas comes from the English source; "Mama en ik / Papa en ik / Papa & Ik" collection-style labels kept as brand naming; "Vader en zoon matching outfits" kept in the daddy-and-me meta description as the natural search term. The "dezelfde kleurenpalet" slip from the earlier sample was not present in these 15 articles.

## Danish sweep

Full read of the stored `da` values (title, meta title, meta description, summary, body) for 15 live `/da/blogs/news/` articles, cross-checked against the English source. Grades are before fix, with the post-fix grade after the arrow. Fixes went through `organic_engine.py translate-apply --execute`, all 15 verified true. Receipts: `ops/organic/receipts/2026-09-29/daqa-<handle>.json`. No stock, shipping-speed, discount or review claims were added.

| Article (handle) | Grade | Issues found / fixed |
|---|---|---|
| mommy-and-me-matching-outfit-ideas | B -> A | H1 and meta description used the calque "Mor og mig / mor-og-mig outfits", now "mor og barn"; "feriestøj" fixed to "ferietøj"; "overtræk" for cover-ups fixed to "strandkjoler"; clumsy family-tradition sentence reworded; English-style Title Case headings set to Danish sentence case. |
| mommy-and-me-outfits-for-every-budget | B -> A | H1 "Mor og mig outfits" fixed to "Mor og datter-outfits"; "god stof" to "godt stof"; "Mellemklasse" (middle class) to "Mellemprisklassen"; "gætværk" to "gætteriet"; "det perfekte sted" (sweet-spot calque) to "valg"; "prisen af" to "prisen for"; "overkommeligt matchende tøj" fixed. |
| daddy-and-me-matching-outfits-the-ultimate-guide | B -> A | H1 "Far og mig" calque fixed; meta title narrowed to "far og søn" fixed to "far og barn"; meta description missing "til" fixed; "stjæler billedet" to "stjæler showet"; "klar til fotos" (plural) to "klare"; "holdt-shirts" to "holdets t-shirts"; "juletøj er hvor det sker" reworded. |
| fall-family-matching-outfits | B -> A | H1 "Efterårs matchende familieoutfits" (ungrammatical) fixed; "lettere plejekrævende" (means the opposite) to "plejelette". |
| best-matching-family-outfits-for-winter | B -> A | H1 lacked "De"; Title Case meta title fixed; summary "vinterfamilie-matchesæt" rewritten; "ankerstykke" calque to "hovedstykke"; "vinter-sæt", "ferie-fotos", "Fleece-finishen" fixed. |
| the-complete-guide-to-family-matching-outfits | B -> A | "samstemt(e)" (in agreement) used 10 times for "coordinated", now "koordineret/koordinerede"; "Mor og mig / Far og mig" labels to "mor og barn / far og barn"; "ideelt terræn", "fuld tvillingetilstand", "en chance til", "til der, hvor" fixed; Title Case meta title fixed. |
| what-to-wear-for-family-photos-matching-outfit-ideas | B -> A | Title Case meta title fixed; English leftovers in link labels ("Mommy and Me matchende outfits", "Daddy and Me-outfits", "Mommy and Me-kjoler") localized; "mulighed til at matche" to "for at matche". |
| holiday-family-matching-outfits-complete-guide | B -> A | Six English image alt texts translated; Title Case meta title fixed; "er ens med dig" to "klædt ens som dig". |
| christmas-matching-family-pajamas | B -> A | H1 "Julematchende familiepyjamas" (non-word compound) to "Matchende julepyjamas til hele familien"; "stak ud for os" (calque) reworded; "neutral juleholdning" (mistranslated palette) fixed. |
| matching-family-christmas-sweaters-guide-2026 | B -> A | Nonstandard "sweatre/julesweatre" standardized to "sweatere" (also meta title "julesweaters"); "størrelsesmærkatet" (sticker) to "størrelsesmærket"; missing comma; "juledag morgen" to "julemorgen"; "så der ikke er lovet nogen ankomstdato" and "inkluderet i ordrer" reworded. |
| family-christmas-photo-outfits-2026 | B+ -> A | "sweatre/sweatrene" standardized to "sweatere/sweaterne"; "møde omklædt op" (mistranslation of "arrive dressed") fixed; "juledag morgen" to "julemorgen". |
| daddy-and-me-christmas-outfits | C -> A | H1 "Far og barn julesæt" and meta title/description/summary split compounds ("jul outfits") fixed to "juleoutfits"; keyword-stacked meta title rewritten; "velpudsede" (polished) to "pæneste/pænest"; "Ét fælles accent" gender fix; "træfarver" to "trætoner"; "rygridning" to "ridetur på ryggen"; garbled "nyde højtiden i at følge en pakke" fixed. |
| matching-family-christmas-shirts | B -> A | 88-character title shortened; "lette at have med at gøre på børn" reworded; "cirka-mål" to "omtrentlige"; "træfarver" to "trætoner"; missing space before "for" and stray space before comma; du/I mix in the ordering paragraph fixed. |
| matching-family-shirts-for-pictures | B -> A | Title Case H1, meta title and headings set to sentence case; "samstemte" to "koordineret"; "cirkamål" to "omtrentlige"; "plagets" to "plaggets"; "med i matchet" (calque) to "med i det matchende look". |
| family-christmas-card-photo-ideas | B -> A | Title Case H1 and headings set to sentence case; "julet-shirts" to "jule-t-shirts"; "sammenkneben" to "sammenknebne"; "matchende julesæt" to "juleoutfits". |

Danish verdict: body copy was mostly natural. Recurring defects were the "Mor og mig / Far og mig" calque in titles, wrong or non-word compounds ("Julematchende", "jul outfits", "feriestøj"), "samstemt" for "coordinated", English Title Case in titles, meta titles and headings, and leftover English in link labels and alt texts. These fixes are the editor's own; no independent re-read yet.

Not changed: product-name link text that comes from English source product titles ("Jingle Bells", "Ho Ho", "We Are Family", "Isbjørn jul"); the stray `</h3></h3>` and product-title headings in christmas-matching-family-pajamas, which come from the English source; the "Barn 2 år" size labels; "Godt tip" style choices; non-localized `/policies/refund-policy` hrefs (identical to source).

## Greek sweep

Date 2026-09-29. Scope: 15 live Greek (`el`) blog articles, read as a strict native editor against the stored Admin translations (same text as the live page). Fixes registered with `organic_engine.py translate-apply --execute`; every write read back `verified: true`. Receipts: `ops/organic/receipts/2026-09-29/elqa-<handle>.json`. English, other languages, products and theme untouched. No Greek case-ending errors were found in link labels (the "οδηγό" forms sit correctly after "τον").

| Article | Grade | Main problems fixed |
|---|---|---|
| mommy-and-me-matching-outfit-ideas | A- -> A | Title and meta title kept (10% CTR). Only bare "Αγίου Βαλεντίνου:" label and "φορέματα καλοκαιρινά" word order. |
| mommy-and-me-outfits-for-every-budget | B+ -> A | "Αγίου Βαλεντίνου" without "του"; calque H2 "συμβουλές αγορών για να εξοικονομήσετε". |
| daddy-and-me-matching-outfits-the-ultimate-guide | B -> A | Meta title/description said "μπαμπάς και γιος" only (article covers daughters) and stacked keywords; "ψαγμένο" for "cool"; "στοχαστικό" for "thoughtful"; "layers ... φίλοι" gender mismatch; "Ψωνίστε" heading. |
| fall-family-matching-outfits | B+ -> A | "ελαστικά κοψίματα"; "αμέτρητες φορές και πλύσεις". |
| best-matching-family-outfits-for-winter | B -> A | Title lacked the article ("Καλύτερα ..."); "Αγοράστε πιο έξυπνα" summary (Shop smarter calque); "κρατήστε ... στο παιχνίδι" (in play calque). |
| the-complete-guide-to-family-matching-outfits | B+ -> A | "μόδα-κίνημα"; "Μην πηδήξετε κατευθείαν". |
| what-to-wear-for-family-photos-matching-outfit-ideas | A- -> A | "κολοκυθιές" (plants) for pumpkin patches. |
| holiday-family-matching-outfits-complete-guide | B -> A | 6 image alt texts left in English; fragment intro; "δεν μετριούνται"; "Δείτε ... να δείτε"; "και οι δύο"; repetitive title. |
| christmas-matching-family-pajamas | B -> A | Title "για Συντονισμό"; "τίποτα δεν έχουν ... από τη χαρά"; "ίδιοι" (children are neuter); "ασορτάρετε" non-standard; "στρατηγικά αξεσουάρ" calque; stray double `</h3></h3>`. |
| matching-family-christmas-sweaters-guide-2026 | B+ -> A | "ίδια" for "matching" in meta and summary; "Ασορτί" dropped from title; "γλειφιτζούρι" (lollipop) for candy cane; "να περάσετε τα μεγέθη"; "κάθε χρήστη"; "κόψιμο" for cropping. |
| family-christmas-photo-outfits-2026 | A- -> A | "ίδιες πιτζάμες" (identical) for "matching pajamas" in meta description and summary. |
| daddy-and-me-christmas-outfits | B -> A | Keyword-stacked title, meta title, meta description and summary ("μπαμπάς και παιδί ... μπαμπάδες και παιδιά"); "ψήσιμο" for baking; "γάρνισμα"/"ένα κρεμ γιακά"; "πλάτη με καβάλα"; "Η αστεία". |
| matching-family-christmas-shirts | B -> A | 126-char title; "Αν το πρόγραμμα είναι ζεστό σπίτι"; "εύκολα στα παιδιά"; "κοντά σε προθεσμία"; "ψήσιμο" for baking; stray space before comma. |
| matching-family-shirts-for-pictures | B -> A | Title repeated "φωτογραφίες" three times; Title Case in meta title and 8 headings; "του καθενού"; "επιεική" (forgiving calque). |
| family-christmas-card-photo-ideas | B+ -> A | Title Case in title and 6 headings; "πλατιές λήψεις ... κόβονται"; "στο γοφό"; "Μπλε ναυτικό". |

Result: 0 C, 12 B/B+, 3 A- before; all 15 A after edits. Recurring cause: engine-written articles are mostly clean; older articles carry English word order, Title Case and a few wrong-word calques.

Remaining, not changed:
- Product-link headings such as "Τροπικά σύνολα ... | DLM" in christmas-matching-family-pajamas are truncated source product titles, kept as translated.
- "outfit", "look", "layers" stay as Greek-usage loanwords across the articles; `/policies/refund-policy` links in two articles carry no `/el/` prefix (source structure kept).
- Title Case remains in the titles and meta titles of some articles not flagged as errors (for example what-to-wear-for-family-photos-matching-outfit-ideas, best-matching-family-outfits-for-winter, christmas-matching-family-pajamas).
