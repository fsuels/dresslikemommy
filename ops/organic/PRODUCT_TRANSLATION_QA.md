# Product Translation QA (2026-09-30)

Read-only sample: 5 live product pages x 5 languages (el, da, no, nl, he) = 25 pages, fetched from `/<lang>/products/<handle>` and compared to the English source (`/products/<handle>.json`). Judged as a strict native editor on title, `<title>`/meta description, body, and size/colour option labels. Nothing was written to Shopify, git, or the theme.

Products: ARGYLE = argyle-wool-mommy-and-me-cardigans, BURG = burgundy-trim-crew-daddy-and-me-sweaters, SWIM = matching-mom-child-one-shoulder-swimsuit, HOOD = pure-joy-heart-family-matching-hoodies, PJ = buffalo-plaid-tree-family-matching-pajamas (the "Christmas pajama" pick from `/collections/christmas-pajamas`).

## Grades (A publishable, B understandable with real errors, C visibly machine-made)

| Product | el | da | no | nl | he |
|---|---|---|---|---|---|
| ARGYLE (knit template) | B | B | B | B- | B |
| BURG (knit template) | B- | B- | B | B- | B |
| SWIM (vendor boilerplate) | C | C+ | C+ | C | C+ |
| HOOD (sweatshirt template) | B | B | B+ | B | B |
| PJ (pajama template) | B | B+ | B+ | B+ | B |
| Language average | B- | B | B | B- | B |

No page is an A. Templated 2026 listings sit at B (body prose is mostly fluent because the wording is a fixed template); the older vendor-copy listing (SWIM) is C in every language. Nothing added stock, shipping, review or bestseller claims. The only overclaims are inherited from the English source (see SWIM).

## Systemic errors (repeat on every page, so one fix covers many listings)

1. **Leftover English in size options.** "6-12 Months" is untranslated in all five languages in the variant picker (and in the el size table): el "Παιδί 6-12 Months", da "Barn 6-12 Months" / "Dreng 6-12 Months", no "Barn 6-12 Months" / "Gutt 6-12 Months", nl "Kind 6-12 Months" / "Jongen 6-12 Months", he "גיל 6-12 Months" / "ילד 6-12 Months". Correct: el "6-12 μηνών", da/no "6-12 måneder", nl "6-12 maanden", he "6-12 חודשים". English source has 20 published products with a "Months" option.
2. **Gender invented in "Child" size labels.** English says "Child 4 Years"; translations pick Girl/Boy per product: ARGYLE el "Κορίτσι 4 ετών", da "Pige 4 år", no "Jente 4 år", nl "Meisje 4 jaar"; BURG "Αγόρι/Dreng/Gutt/Jongen"; and SWIM (a one-shoulder swimsuit shown on girls) labelled "Αγόρι 2-3 ετών", "Dreng 2-3 år", "Gutt 2-3 år", "Jongen 2-3 jaar", he "ילד 2-3 שנים". Correct: neutral "Παιδί", "Barn", "Barn", "Kind", "ילד/ה" or "גיל" as on the PJ/HOOD pages. Misleading on a size picker.
3. **"Soft knit" rendered as "jersey"** in da/no ("Blød jersey: Varm uldstrik…", "Myk jersey: Varm ullstrikk…") and "tricot" in nl ("Zachte tricot: Een warm wollen breisel…"). Jersey/tricot are different fabrics from the chunky wool knit the heading sits above. Correct: da "Blød strik", no "Myk strikk", nl "Zacht breisel". It also appears in the da/no/nl meta ("blød jersey i bomuldsblanding").
4. **"Mommy and Me / Daddy and Me" calques in H1 and `<title>`:** el "Μαμά και Εγώ", da "Mor og mig-striktrøjer", no "Mamma og meg-gensere", nl "Mama en ik-truien", he "לאמא ואני" (ungrammatical: needs "לאמא ולי"). Natural forms: el "για μαμά και παιδί", da "til mor og barn", no "til mamma og barn", nl "voor mama en kind", he "לאמא ולי" / "אמא וילד". Same for "Papa en ik", "Far og mig", "Pappa og meg", "Μπαμπάς και Εγώ", "לאבא ואני".
5. **Word-for-word titles that lose the noun order/keyword:** el "Μαλλί με ρόμβους αργκάιλ Πουλόβερ" (reads "wool with rhombuses"; product is a cardigan, called πουλόβερ in title but ζακέτα in body); el "Μπορντό με στρογγυλή λαιμόκοψη και τελειώματα" ("crew trim" -> "finishings"); el/da/no/nl/he PJ titles "Δέντρο με καρό ξυλοκόπου…", "Juletræ i skovmandstern…", "Juletre i tømmerhoggerruter…", "Kerstboom in houthakkersruit…", "עץ בדוגמת משבצות גדולות…" — the word "Christmas" (the highest-intent keyword) is missing from the `<title>`, and "buffalo plaid" is three different things within one page (he: "משבצות גדולות" in title, "משבצות באפלו" in meta; no: "tømmerhoggerruter" in title, "skogshoggerruter" in meta).
6. **Cardigan called "sweater/trui/genser/striktrøje" in titles and size-chart heading** while the body says cardigan (ζακέτα, cardigan/strikkejakke, vest, קרדיגן): inconsistent in all five languages (source itself says "Sweaters", so needs a garment word decision).
7. **Hebrew colour option values carry niqqud** (SWIM: "צָהוֹב", "וָרוֹד", "יָרוֹק", "כְּחוֹל", ARGYLE "אָדוֹם") while every other value is unpointed; raglan spelled "ראגלן" in body and "רגלן" in the option and "הרגלן" elsewhere on the same page; meta typo "מבד בד כותנה" (doubled word) on HOOD he.
8. **"Family story" heading** is a literal translation in all languages (el "Οικογενειακή ιστορία", da "Familiehistorie", no "Familiehistorie", nl "Familieverhaal", he "סיפור משפחתי"); reads odd for a product spec block. Also "Print/Tryk/Trykk/Opdruk/הדפס" is used for a knitted argyle pattern (not a print).

## Concrete errors by product/language (beyond the systemic list)

**Dutch**
- SWIM (worst page on the sample): "Onze bijpassende moeder & Badpak met één schouder voor kinderen" (broken capitalisation and word order); "Gemakkelijk te dragen & Move" (English "Move" left in a heading, should be "Makkelijk aan te trekken en comfortabel in beweging"); "voelt u zich nooit verstopt" ("verstopt" = constipated/blocked, source meant "not constricted": use "nooit beklemd"); "Luchtdrogen of in de droger laag" (truncated: "Aan de lucht drogen of op lage stand in de droger"); "Kostenefficiënt: Met behulp van het draaggemak en het gebruiksgemak geweldige prestaties, het badpak biedt…" (ungrammatical); switches between "u/uw" and "je"; badpak/zwempak/zwemkleding used interchangeably; title "Mama en Ik Badpakken - Eén Schouder" (Title Case, plural for one product).
- **Colour option "Green" = "Groente"** (vegetables). Must be "Groen". Live on the swimsuit variant picker.
- HOOD: "Maattabel - Sweater" (for a hoodie), "hoeden" for hats (means brimmed hats; should be "mutsen"); ARGYLE "Zachte tricot" (see systemic).

**Danish**
- SWIM: "Luftenørres eller tørretumbles ved lav varme" (typo, should be "Lufttørres"); "Modige farver & teksturer" (calque of "Bold", use "Markante farver"); "Let at have på & bevæge sig i"; meta "Mor og barn matchende one-shoulder badedragt" (English "one-shoulder" left in meta, title uses "Én Skulder" Title Case); title "Klæd Dig Som Mor" Title Case.
- ARGYLE: "Tryk: En strikket cardigan…" vs "striktrøjer" in title; "Uld med argylemønster" title order awkward (better "Argyle-striktrøjer i uld til mor og barn").
- Claims kept from source: "dens flotte farver forbliver intakte for evigt", "passer perfekt til alle kvinder" (see SWIM below).

**Norwegian**
- SWIM: "Vår matchende mamma- og barn-badetøy" (wrong article: "vårt"); "Luften tørkes" (should be "Lufttørkes"); badetøy/badedrakt mixed; "Friske farger" for "Bold colors" (should be "Markante farger"); title "Kle deg som mamma", "Én skulder" (capital É mid-title style).
- PJ: "Pyjamassett" (heading) vs "pysjamas" (body) on the same page; title "tømmerhoggerruter" vs meta "skogshoggerruter".
- ARGYLE: "genser" (title/size heading) vs "strikkejakke/cardigan" (body).

**Greek**
- SWIM: title "Μαγιό Μαμά και Εγώ - Ένας Ώμος" (Title Case, calque); H1/body "μαγιό μιας ώμου" and "μαγιό μιας ώμου" (wrong gender agreement: ώμος is masculine, needs "ενός ώμου"); "Ντύσου σαν τη Μαμά – Dress Like Mommy" (brand doubled in title); "δεν αποτυγχάνει ποτέ να εντυπωσιάσει τους θεατές" (literal "never fails to impress onlookers").
- Size chart: "Πατέρας S" (formal "father") vs "Μπαμπάς" in the body; "Μητέρα M" (formal "mother") vs "Μαμά" elsewhere. Use the same word as the H1.
- PJ: "Μαλακό πλεκτό από μείγμα βαμβακιού με 35% βαμβάκι" (repeats cotton twice, awkward); meta "καρό ξυλοκόπου" then "buffalo" (mixed).
- ARGYLE meta says "για μαμά και κόρη" (source also says daughter; consistent with the English but narrower than the "Παιδί" size labels).

**Hebrew**
- ARGYLE/BURG: "סוודרים לאמא ואני" / "סוודרים לאבא ואני" (should be "ולי"); size label prefix "ילדה" (girl) on argyle vs "ילד" on burgundy (gender fixed by translation, not by source).
- "חג מולד משפחתי ונעים" (Key Features closer, article dropped; should be "חג המולד"); "מפתח צוואר" and "צווארון" both used for neckline on the same page; SWIM "לעולם לא תרגישו צפיפות" (literal "congested"; means "restricted"), "לעולם לא מאכזב את המתבוננים", "נשארים שלמים לנצח", "לכל הנשים שם בחוץ".

**Claims to fix at source (all languages, present in English SWIM copy too):** "colours remain intact forever", "suitable for all women", "never fails to impress the onlookers", "no financial burden". These are unsupported/odd marketing claims inherited from the vendor description, not a translation error, but they are now repeated in 20 languages. About 6 published products match this boilerplate (regex sample; likely more).

## Verdict: worth doing, as a bounded template-and-glossary fix, not a per-page rewrite

- **Scale.** 308 published products. 136 use the 2026 "Family story / Key Features" template (all sampled template pages share errors 1-8 above), 303 carry Child/Mother/Father style option values, 20 have a "Months" option, and at least 6 carry the vendor boilerplate that produced the C-grade swimsuit pages. Roughly 140-170 pages are affected by the systemic defects; the C-grade set is the legacy vendor-copy group (plus any product whose body is not template-generated).
- **Which languages hurt most.** In this sample: Dutch (broken SWIM syntax, "Groente", "verstopt", tricot) and Greek (word-order titles, "μιας ώμου", Πατέρας/Μητέρα mixing) are lowest at B-; Danish, Norwegian and Hebrew sit at B. Danish/Norwegian share the jersey/strik and "Luftenørres" issues; Hebrew has script-level inconsistencies (niqqud, spellings) and the "ואני" grammar error. Expect the same template errors in the other ~15 languages (untested).
- **Why it matters.** About 70% of Google clicks land on translated storefronts, and the defects hit exactly the conversion surface: `<title>` keyword order (missing "Christmas"/"matching"), size pickers with English or wrong-gender words, and one live wrong colour word ("Groente"). No page is unreadable, so this is a lift, not an emergency: ordering = (a) the two shipping-risk items first (nl "Groente", gender labels on the SWIM picker and "6-12 Months"), (b) title/H1 patterns and "jersey/tricot" via the glossary, (c) rewrite the SWIM boilerplate in English source, then re-translate.
- **Recommended fix program.** Fix at the source of truth, not per page: (1) extend `ops/content/translation_glossary.json` (only 17 terms today, e.g. nl "Mama en ik"; no el/da/no/he entries for "Mommy & Me") with per-language Child/Mother/Father/Months, "Soft knit", cardigan vs sweater, buffalo plaid, Christmas pajamas, "Mommy & Me" phrases; (2) fix the template strings in `poll_shopify_product_translations.py` (see below) so title, "6-12 Months", gender-neutral child labels and "Family story" are localised once; (3) rewrite the vendor SWIM-type bodies in English (remove the "forever/onlookers" copy) before re-translating; (4) re-run the writer for only the affected handles, then spot-check 2 pages per language.

## Tools that write product translations (not run)

- `ops/scripts/poll_shopify_product_translations.py`: the main writer. Translates title, body, meta, option names/values and localized size charts (role/age/garment label helpers at ~L1105-1330), engine is Google Translate through `translation_utils.py` (`deep_translator.GoogleTranslator`) plus template/glossary substitution; writes with `translationsRegister`. Google Translate explains the "Groente", "verstopt", "jersey" and boilerplate calques.
- `ops/scripts/finalize_shopify_listing_localization.py --handles a,b --locales el,da,...`: the synchronous closeout gate that wraps the poller/audits for named handles; the right entry point for a handle-scoped re-run.
- `ops/scripts/sync_shopify_translations.py`: bulk export-based writer (`translationsRegister`, `--execute`, `--locales`), uses `ops/content/translation_glossary.json`.
- Per-product polish precedent: `ops/scripts/polish-gdsy-golden-daisy-title-translations.py` (hand-written title/SEO translations, `--execute`), and `ops/scripts/repair_localized_product_size_charts.py` / `apply_localized_shipping_policy_cleanup.py` for size-chart and policy bodies.
- Audits: `ops/scripts/audit_shopify_product_translation_completeness.py` (missing/stale/source-language content) and `audit_localized_pdp_language_leakage.py` (would catch "Months"); neither catches wrong-word errors like "Groente".
- Article precedent: `organic_engine.py translate-apply --execute` was used for the 2026-09-29 article fixes (`ops/organic/TRANSLATION_QA.md`); it is article-scoped, not product-scoped.

## Limitations

Sample of 5 products / 5 languages read by a model acting as native editor, not a paid human review; Greek, Hebrew, Danish, Norwegian and Dutch judged from page text. Counts (136 / 303 / 20 / 6) come from the English `products.json` body/option scan of 308 published products and are estimates of exposure, not confirmed per-language defects. Other 15 languages not checked. Raw pages saved in `/tmp/pqa/`.
