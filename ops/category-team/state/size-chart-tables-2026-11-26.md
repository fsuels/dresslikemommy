# Size-chart tables, translated vs English: whole-catalog measurement (2026-11-26)

Read-only audit (Admin GraphQL reads only, no public requests). Script: `ops/scripts/check_size_chart_tables.py`; tests: `ops/tests/test_check_size_chart_tables.py` (23 pass). Machine file: `ops/organic/receipts/2026-11-26/size-chart-tables/findings.json` (all findings with handle, locale, row, column, English and translated value, plus the aggregated non-glossary table). Rerun: `python3 ops/scripts/check_size_chart_tables.py --out <path>`.

Scope: 328 active products x 20 locales, body_html tables matched by id, else by position. Glossary: `retranslate-short/table-glossary.json`; it already contains the V25-2 corrections (fi, fr, de, cs, pl, ru, sv, da, he), so the in-memory patch was a no-op (`glossary_v25_applied_in_memory=False`). Year words per locale (ja 歳/才, ko 세/살, ...) and the calendar-year-wrong list (ja 年, ko 연도/년/해) are defined in the script. Decimal comma is info only in cs/de/es/fr/it/nl/pl/pt-BR/ru/sv/da/no/fi/ro/el (69698 cells), no unlisted-locale case found.

## Totals by problem type (cell-level findings)

| Type | Count | Meaning |
|---|---|---|
| numeric_dropped | 9456 | translated cell lacks numbers English has (imperial values omitted) |
| english_residue | 2468 | English header/label word left in a translated cell |
| numeric_rounded | 1729 | same value, precision changed (22.05 -> 22.0462) |
| duplicated_header | 577 | same term used for two English headers, or "X/X" in one header |
| size_code_mismatch | 245 | size code differs from English (converted/transliterated/dropped) |
| age_unit_wrong | 14 | age written as calendar year |
| numeric_mismatch | 7 | a different number from English (serious) |
| numeric_reordered | 5 | same numbers, different order |

Not findings (info): decimal comma in allowed locales 69698; ar/he number written as a word for 1 or 2 years 189; outdated body translations by locale: none.

## By locale

| Locale | numeric_dropped | english_residue | numeric_rounded | duplicated_header | size_code_mismatch | age_unit_wrong | numeric_mismatch | numeric_reordered |
|---|---|---|---|---|---|---|---|---|
| ar | 557 | 22 | 91 | 70 | 142 | 0 | 0 | 5 |
| cs | 361 | 147 | 91 | 0 | 0 | 0 | 0 | 0 |
| da | 0 | 101 | 91 | 54 | 0 | 0 | 0 | 0 |
| de | 557 | 176 | 91 | 81 | 0 | 0 | 0 | 0 |
| el | 557 | 116 | 91 | 0 | 0 | 0 | 0 | 0 |
| es | 557 | 23 | 91 | 0 | 0 | 0 | 0 | 0 |
| fi | 557 | 129 | 91 | 76 | 0 | 0 | 0 | 0 |
| fr | 557 | 28 | 0 | 189 | 0 | 0 | 0 | 0 |
| he | 557 | 286 | 91 | 52 | 0 | 0 | 0 | 0 |
| hi | 557 | 195 | 91 | 0 | 68 | 0 | 0 | 0 |
| it | 557 | 158 | 91 | 0 | 0 | 0 | 0 | 0 |
| ja | 557 | 65 | 91 | 0 | 1 | 13 | 0 | 0 |
| ko | 557 | 277 | 91 | 53 | 0 | 1 | 7 | 0 |
| nl | 740 | 77 | 91 | 2 | 0 | 0 | 0 | 0 |
| no | 0 | 111 | 91 | 0 | 0 | 0 | 0 | 0 |
| pl | 557 | 202 | 91 | 0 | 0 | 0 | 0 | 0 |
| pt-BR | 557 | 144 | 91 | 0 | 0 | 0 | 0 | 0 |
| ro | 557 | 150 | 91 | 0 | 0 | 0 | 0 | 0 |
| ru | 557 | 22 | 91 | 0 | 34 | 0 | 0 | 0 |
| sv | 0 | 39 | 91 | 0 | 0 | 0 | 0 | 0 |

(Locales absent from the table have zero findings.)

## Numeric mismatches (wrong or reordered number in a size chart): most serious

12 cells in 6 products. Format: handle | locale | row | column | English | translated.

- `matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi` | ko | Child 1 year | Size | `Child 1 year` | `Child 1 year|어린이 1세` (numeric_mismatch)
- `matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi` | ko | Child 2 years | Size | `Child 2 years` | `Child 2 years|어린이 2세` (numeric_mismatch)
- `matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi` | ko | Child 3 years | Size | `Child 3 years` | `Child 3 years|어린이 3세` (numeric_mismatch)
- `matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi` | ko | Child 4 years | Size | `Child 4 years` | `Child 4 years|어린이 4세` (numeric_mismatch)
- `matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi` | ko | Child 5-6 years | Size | `Child 5-6 years` | `Child 5-6 years|어린이 5-6세` (numeric_mismatch)
- `matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi` | ko | Child 7-8 years | Size | `Child 7-8 years` | `Child 7-8 years|어린이 7-8세` (numeric_mismatch)
- `matching-men-s-and-boys-100-cotton-floral-short-sleeve-button-up-shirt-navy-multi` | ko | Child 9-10 years | Size | `Child 9-10 years` | `Child 9-10 years|어린이 9-10세` (numeric_mismatch)
- `vintage-cottage-floral-mommy-and-me-pajama-set` | ar | Child 2 Years | Recommended Weight (kg/lbs) | `11–13 kg / 24–29 lbs` | `13–11 كجم / 24–29 رطلاً` (numeric_reordered)
- `bird-chirping-mommy-and-me-pajamas` | ar | Child 2 Years | Recommended Weight (kg/lbs) | `11–13 kg / 24–29 lbs` | `13–11 كجم / 24–29 رطلاً` (numeric_reordered)
- `good-night-song-of-the-sea-mommy-and-me-pajamas` | ar | Child 2 Years | Recommended Weight (kg/lbs) | `11–13 kg / 24–29 lbs` | `13–11 كجم / 24–29 رطلاً` (numeric_reordered)
- `summer-puppies-mommy-and-me-pajamas` | ar | Child 2 Years | Recommended Weight (kg/lbs) | `11–13 kg / 24–29 lbs` | `13–11 كجم / 24–29 رطلاً` (numeric_reordered)
- `grapevine-mommy-and-me-pajamas` | ar | Child 1-2 Years | Recommended Weight (kg/lbs) | `10–13 kg / 22–29 lbs` | `13–10 كجم / 22–29 رطلاً` (numeric_reordered)

The seven ko rows are one defect: the cell contains the English label, a pipe and the Korean label (`Child 1 year|어린이 1세`), so the digit appears twice. The one ar row prints a weight range backwards (`13–11` for `11–13`).

## Imperial values dropped (numeric_dropped)

9456 cells in 46 products. Three products account for 9273 of them in all 20 locales: the translated cells keep only the metric value, English shows metric / imperial.

- `safari-caravan-family-matching-set`: 3162 cells, 17 locales, e.g. ar | Weight (kg/lbs) | `9-11.5 kg / 19.8-25.4 lbs` -> `9-11.5 كجم`
- `pink-horizon-family-matching-set`: 3136 cells, 16 locales, e.g. ar | Weight (kg/lbs) | `12-14 kg / 26.5-30.9 lbs` -> `12-14 كجم`
- `fresh-blue-plaid-family-matching-set`: 2975 cells, 17 locales, e.g. ar | Weight (kg/lbs) | `9-11.5 kg / 19.8-25.4 lbs` -> `9-11.5 كجم`
- `elegant-matching-family-outfits-light-blue-halter-dresses-casual-t-shirt-set-for-summer`: 11 cells, 1 locales, e.g. nl | Suggested Weight (kg/lbs) | `55-60 kg / 121-132 lbs` -> `55-60 kg`
- `matching-family-striped-cardigans-navy-and-red-heart-embroidery-knit-sweaters-for-mom-dad-and-kids`: 10 cells, 1 locales, e.g. nl | Suggested Weight (kg/lbs) | `3.5-7 kg / 8-15 lbs` -> `3.5-7 kg`
- `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`: 9 cells, 1 locales, e.g. nl | Suggested Weight (kg/lbs) | `55-60 kg / 121-132 lbs` -> `55-60 kg`
- `matching-family-striped-fleece-hoodies-cozy-winter-pullover-for-parents-and-kids`: 7 cells, 1 locales, e.g. nl | Recommended Weight (kg / lbs) | `20.5-22.5 kg / 45-50 lbs` -> `20,5-22,5 kg`
- `matching-family-love-t-shirt-set-adorable-family-heart-design`: 7 cells, 1 locales, e.g. nl | Recommended Weight (kg / lbs) | `55-62.5 kg / 121-137.5 lbs` -> `55-62,5 kg`
- `matching-family-denim-button-up-shirts-casual-unisex-jean-jackets-for-parents-and-kids`: 6 cells, 1 locales, e.g. nl | Recommended Weight (kg / lbs) | `20.5-22.5 kg / 45-50 lbs` -> `20,5-22,5 kg`
- `family-matching-t-shirt-set-with-colorful-heart-brushstroke-design`: 6 cells, 1 locales, e.g. nl | Recommended Weight (kg / lbs) | `45-57.5 kg / 99-126.8 lbs` -> `45-57,5 kg`
- `matching-family-love-balloon-t-shirt-set-heart-love-design-in-4-colors`: 6 cells, 1 locales, e.g. nl | Recommended Weight (kg / lbs) | `45-57.5 kg / 99-126.5 lbs` -> `45-57,5 kg`
- `matching-family-minimalist-heart-t-shirt-set-simple-love-design-in-4-colors`: 6 cells, 1 locales, e.g. nl | Recommended Weight (kg / lbs) | `45-57.5 kg / 99-126.5 lbs` -> `45-57,5 kg`
- Remaining 34 products: see findings.json (type numeric_dropped), mostly 1-3 cells each (translated cell shorter than English).

## Precision changed (numeric_rounded)

- `cable-horse-family-matching-tops`: 1729 cells, 19 locales, e.g. ar | `10-13.5 kg / 22.05-29.76 lbs` -> `10-13.5 كجم / 22.0462-29.7624 رطل`

## Age-unit errors (age_unit_wrong)

- `good-night-song-of-the-sea-mommy-and-me-pajamas` | ja | Child 6-7 Years | `Child 6-7 Years` -> `子供 6-7年`
- `good-night-song-of-the-sea-mommy-and-me-pajamas` | ko | Child 6-7 Years | `Child 6-7 Years` -> `어린이 6-7연도`
- `teddy-bear-siblings-christmas-sweaters` | ja | 3-4 Years | `3-4 Years` -> `3～4 年`
- `teddy-bear-siblings-christmas-sweaters` | ja | 4-5 Years | `4-5 Years` -> `4～5 年`
- `teddy-bear-siblings-christmas-sweaters` | ja | 6 Years | `6 Years` -> `6 年`
- `teddy-bear-siblings-christmas-sweaters` | ja | 7-8 Years | `7-8 Years` -> `7-8 年`
- `red-truck-siblings-christmas-sweaters` | ja | 3-4 Years | `3-4 Years` -> `3～4 年`
- `red-truck-siblings-christmas-sweaters` | ja | 4-5 Years | `4-5 Years` -> `4～5 年`
- `red-truck-siblings-christmas-sweaters` | ja | 6 Years | `6 Years` -> `6 年`
- `red-truck-siblings-christmas-sweaters` | ja | 7-8 Years | `7-8 Years` -> `7-8 年`
- `nordic-hearts-siblings-christmas-sweaters` | ja | 3-4 Years | `3-4 Years` -> `3～4 年`
- `nordic-hearts-siblings-christmas-sweaters` | ja | 4-5 Years | `4-5 Years` -> `4～5 年`
- `nordic-hearts-siblings-christmas-sweaters` | ja | 6 Years | `6 Years` -> `6 年`
- `nordic-hearts-siblings-christmas-sweaters` | ja | 7-8 Years | `7-8 Years` -> `7-8 年`

Other age words are not judged wrong; unrecognised ones are in the non-glossary list under `age_unit`.

## Size codes (size_code_mismatch)

245 cells in 55 products: ar mismatch 142, hi converted 68, ja mismatch 1, ru converted 34. No pt-BR P/G/GG conversion occurs inside tables (it is only in bodies, V25-1).
- `gradient-ombre-family-matching-outfits-pink-blue-t-shirts-with-white-shorts-set`: 32 cells, e.g. ar `Father S` -> `الأب س`
- `matching-family-love-t-shirt-set-adorable-family-heart-design`: 22 cells, e.g. ar `Mother S` -> `الأم س`
- `elegant-matching-family-outfits-light-blue-halter-dresses-casual-t-shirt-set-for-summer`: 19 cells, e.g. ar `Father M` -> `الأب م`
- `matching-family-striped-cardigans-navy-and-red-heart-embroidery-knit-sweaters-for-mom-dad-and-kids`: 19 cells, e.g. ar `Mother S` -> `الأم س`
- `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`: 18 cells, e.g. ar `Father M` -> `الأب م`
- `matching-family-beach-outfits-with-floral-dresses-and-shorts`: 16 cells, e.g. ar `Father L` -> `الأب لام`
- `battery-themed-matching-family-t-shirt-set-super-tired-parents-energetic-kids`: 6 cells, e.g. ar `Father M` -> `الأب م`
- `matching-family-plug-lightbulb-t-shirt-set-unique-family-connection-design`: 5 cells, e.g. ar `Father M` -> `الأب م`
- `family-matching-red-cable-knit-cardigans-elegant-heart-button-design`: 5 cells, e.g. ar `Adult M` -> `م بالغ`
- `family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style`: 5 cells, e.g. ar `Adult M` -> `م بالغ`

## English left in cells (english_residue)

Top locale/word pairs: he father 180; ko mother 119; pl father 115; hi father 114; ko father 110; ro mother 101; de mother 99; cs mother 95; el mother 92; pt-BR mother 92; fi mother 91; he mother 82; it father 80; no mother 76; pl mother 71; da mother 66; it mother 62; hi child 62; de father 61; nl mother 49; pt-BR father 40; ja mother 33; cs father 28; ko child 28; ro father 25.

## Duplicated headers

By locale: fr 189, de 81, fi 76, ar 70, da 54, ko 53, he 52, nl 2. Examples:
- de | `Size | Height (cm / in)` -> `Größe (cm / in)`
- fr | `Size | Waist (cm / in)` -> `Taille (cm / po)`
- fr | `Size | Waist (cm/in)` -> `Taille (cm/po)`
- he | `Chest/Bust (cm/in)` -> `חזה/חזה (ס"מ/אינץ')`
- ar | `Chest/Bust (cm/in)` -> `الصدر/الصدر (سم/بوصة)`
- ko | `Chest/Bust (cm/in)` -> `가슴/가슴(cm/인치)`
- ar | `Length (cm) | Height (cm)` -> `الطول (سم)`
- de | `Size | Height (cm)` -> `Größe (cm)`
- fi | `Length (cm) | Height (cm)` -> `Pituus (cm)`
- fr | `Size | Waist (cm)` -> `Taille (cm)`
- fr | `Size | Height (cm)` -> `Taille (cm)`
- ar | `Length (cm/in) | Height (cm/in)` -> `الطول (سم/بوصة)`

## Non-glossary values per locale, for accept/reject in one pass

Value = what the translation uses where the glossary has a different term. count = cells, prod = products. `label:*` is the row-label stem (numbers, size code and age word removed); `header:*` the header without the unit; `age_unit` the leftover text where no accepted year word was found. Top 10 per locale; the full list is in findings.json under `nonglossary`.

### ar (54 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | طفل | للأطفال عمر | 684 | 95 |
| label:child | طفل | للبنات عمر | 404 | 58 |
| label:adult | بالغ | للكبار | 383 | 71 |
| label:child | طفل | للأولاد عمر | 160 | 19 |
| header:size | المقاس | الحجم | 132 | 126 |
| header:garment | طول القطعة | طول الملابس | 85 | 79 |
| label:adult | بالغ | الكبار | 63 | 13 |
| header:garment | طول القطعة | الطول | 50 | 50 |
| header:shoulder | عرض الكتفين | عرض الكتف | 39 | 39 |
| label:girl | بنت | فتاة | 38 | 6 |

### cs (47 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:mother | Máma | Maminka | 464 | 103 |
| label:child | Dítě | Dívka | 390 | 56 |
| label:father | Táta | Tatínek | 337 | 53 |
| label:father | Táta | Otec | 235 | 51 |
| label:child | Dítě | Chlapec | 169 | 20 |
| label:mother | Máma | Matka | 151 | 37 |
| label:mother | Máma | Mother | 95 | 24 |
| header:garment | Délka oděvu | Délka | 52 | 52 |
| label:father | Táta | Father | 28 | 6 |
| header:garment | Délka oděvu | Délka kabátu | 23 | 23 |

### da (43 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Barn | Pige | 378 | 54 |
| label:child | Barn | Dreng | 169 | 20 |
| header:garment | Tøjets længde | Længde | 121 | 121 |
| header:garment | Tøjets længde | Beklædningslængde | 78 | 73 |
| label:mother | Mor | Mother | 64 | 16 |
| label:mother | Mor | Moder | 58 | 15 |
| header:garment | Tøjets længde | Tøjlængde | 47 | 32 |
| header:skirt | Nederdelslængde | Ærme eller nederdel | 22 | 18 |
| header:pants | Buksernes længde | Bukselængde | 21 | 21 |
| header:shoulder | Skulderbredde | Skulder | 19 | 19 |

### de (39 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Kind | Mädchen | 430 | 62 |
| label:father | Papa | Vater | 215 | 46 |
| label:child | Kind | Junge | 169 | 20 |
| label:mother | Mama | Mutter | 167 | 40 |
| label:mother | Mama | Mother | 98 | 25 |
| header:garment | Gesamtlänge | Kleidungsstücklänge | 98 | 80 |
| header:height | Körpergröße | Größe | 81 | 58 |
| label:father | Papa | Father | 61 | 13 |
| header:garment | Gesamtlänge | Länge | 50 | 50 |
| header:garment | Gesamtlänge | Kleidungslänge | 35 | 28 |

### el (52 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:mother | Μαμά | Μητέρα | 586 | 135 |
| label:father | Μπαμπάς | Πατέρας | 586 | 106 |
| label:child | Παιδί | Κορίτσι | 386 | 55 |
| label:child | Παιδί | Αγόρι | 173 | 21 |
| label:mother | Μαμά | Mother | 90 | 22 |
| label:child | Παιδί | Παιδικό | 76 | 6 |
| header:sleeve | Μανίκι | Μήκος Μανικιού | 54 | 54 |
| header:garment | Μήκος ρούχου | Μήκος ενδύματος | 51 | 45 |
| header:garment | Μήκος ρούχου | Μήκος | 50 | 50 |
| header:garment | Μήκος ρούχου | Μήκος Παλτό | 23 | 23 |

### es (52 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Niño/a | Infantil | 712 | 98 |
| label:child | Niño/a | Niño | 682 | 97 |
| label:child | Niño/a | Niña | 417 | 60 |
| label:father | Papá | Padre | 269 | 57 |
| label:mother | Mamá | Madre | 263 | 65 |
| label:child | Niño/a | Niño de a | 223 | 41 |
| header:size | Talla | Tamaño | 116 | 111 |
| header:chest | Pecho | Busto | 80 | 80 |
| header:garment | Largo de la prenda | Longitud de la prenda | 76 | 70 |
| label:child | Niño/a | Niño Años | 57 | 17 |

### fi (49 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Lapsi | Tyttö | 401 | 57 |
| header:hip | Lantionympärys | Lantio | 217 | 194 |
| label:child | Lapsi | Poika | 168 | 20 |
| header:chest | Rinnanympärys | Rinta | 131 | 110 |
| label:mother | Äiti | Mother | 91 | 23 |
| header:chest | Rinnanympärys | Rinta/rinta | 71 | 65 |
| label:adult | Aikuinen | Aikuisten | 59 | 8 |
| header:garment | Vaatteen pituus | Pituus | 50 | 50 |
| age_unit | v/vuotta/vuotias | vuosi | 42 | 42 |
| header:shoulder | Hartialeveys | Olkapään leveys | 35 | 35 |

### fr (50 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Enfant | Fille | 415 | 60 |
| label:father | Papa | Père | 258 | 54 |
| label:mother | Maman | Mère | 246 | 63 |
| label:child | Enfant | Garçon | 161 | 19 |
| header:waist | Tour de taille | Taille | 143 | 124 |
| header:height | Stature | Hauteur | 87 | 87 |
| header:waist | Tour de taille | Taille de ceinture | 69 | 69 |
| header:garment | Longueur du vêtement | Longueur | 50 | 50 |
| header:height | Stature | Taille | 46 | 27 |
| header:garment | Longueur du vêtement | Longueur du manteau | 23 | 23 |

### he (63 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | ילד/ה | ילד | 837 | 121 |
| label:child | ילד/ה | גיל | 620 | 85 |
| label:child | ילד/ה | ילדה | 398 | 57 |
| header:hip | היקף ירכיים | ירכיים | 204 | 182 |
| label:father | אבא | Father | 180 | 38 |
| header:waist | מותניים | מותן | 108 | 90 |
| label:child | ילד/ה | ילדים | 86 | 12 |
| label:mother | אמא | Mother | 80 | 20 |
| header:garment | אורך הבגד | אורך בגד | 67 | 61 |
| label:mother | אמא | אם | 51 | 12 |

### hi (76 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | बच्चा | बच्चों के लिए | 677 | 94 |
| label:father | पापा | पिता | 460 | 84 |
| label:child | बच्चा | लड़की | 389 | 56 |
| header:size | साइज़ | आकार | 231 | 205 |
| label:child | बच्चा | लड़का | 152 | 18 |
| header:weight | वज़न | वजन | 137 | 109 |
| label:father | पापा | Father | 114 | 24 |
| header:height | ऊँचाई | ऊंचाई | 103 | 97 |
| label:mother | माँ | मदर | 95 | 27 |
| header:garment | कपड़े की लंबाई | परिधान की लंबाई | 89 | 81 |

### it (67 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Bambino/a | Bambino | 892 | 137 |
| label:child | Bambino/a | Bimbi | 691 | 96 |
| label:child | Bambino/a | Bambina | 423 | 61 |
| label:mother | Mamma | Madre | 209 | 50 |
| label:father | Papà | Padre | 195 | 42 |
| label:child | Bambino/a | Bambino Anni | 117 | 20 |
| header:garment | Lunghezza del capo | Lunghezza capo | 88 | 69 |
| header:chest | Torace | Petto/Busto | 80 | 76 |
| label:father | Papà | Father | 80 | 16 |
| header:chest | Torace | Busto | 66 | 66 |

### ja (72 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | 子ども | 子供 | 1394 | 201 |
| label:child | 子ども | 女の子 | 356 | 51 |
| label:father | パパ | 父 | 142 | 40 |
| label:mother | ママ | マザー | 138 | 55 |
| label:child | 子ども | 男の子 | 137 | 16 |
| label:mother | ママ | 母 | 99 | 47 |
| header:chest | 胸囲 | バスト | 97 | 97 |
| header:chest | 胸囲 | 胸/バスト | 95 | 71 |
| label:child | 子ども | キッズ | 76 | 6 |
| label:father | パパ | 父親 | 68 | 15 |

### ko (77 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | 아동 | 어린이 | 627 | 110 |
| label:child | 아동 | 여아 | 339 | 48 |
| header:waist | 허리둘레 | 허리 | 187 | 168 |
| label:father | 아빠 | 아버지 | 142 | 30 |
| label:child | 아동 | 남아 | 137 | 16 |
| label:mother | 엄마 | Mother | 119 | 30 |
| label:father | 아빠 | Father | 110 | 23 |
| header:hip | 엉덩이둘레 | 엉덩이 | 104 | 103 |
| label:mother | 엄마 | 어머니 | 97 | 27 |
| header:garment | 총장 | 의류 길이 | 82 | 62 |

### nl (41 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Kind | Meisje | 397 | 57 |
| label:father | Papa | Vader | 273 | 58 |
| label:mother | Mama | Moeder | 238 | 59 |
| label:child | Kind | Jongen | 169 | 20 |
| header:garment | Lengte kledingstuk | Kledinglengte | 119 | 107 |
| label:adult | Volwassene | Volwassen | 103 | 14 |
| header:garment | Lengte kledingstuk | Kledingstuklengte | 87 | 77 |
| header:chest | Borst | Buste | 66 | 66 |
| header:garment | Lengte kledingstuk | Lengte | 52 | 52 |
| label:mother | Mama | Mother | 49 | 12 |

### no (40 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:mother | Mor | Mamma | 461 | 99 |
| label:child | Barn | Jente | 381 | 55 |
| label:father | Far | Pappa | 346 | 53 |
| label:child | Barn | Gutt | 169 | 20 |
| header:garment | Plaggets lengde | Plagglengde | 121 | 101 |
| label:mother | Mor | Mother | 75 | 29 |
| header:garment | Plaggets lengde | Lengde | 52 | 52 |
| header:chest | Bryst | Byste | 47 | 47 |
| header:skirt | Skjørtlengde | Erme eller skjørt | 27 | 23 |
| header:garment | Plaggets lengde | Jakkelengde | 23 | 23 |

### pl (52 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Dziecko | Dziewczynka | 404 | 58 |
| label:child | Dziecko | Chłopiec | 169 | 20 |
| label:mother | Mama | Matka | 164 | 42 |
| label:father | Tata | Ojciec | 133 | 29 |
| label:father | Tata | Father | 115 | 23 |
| header:chest | Klatka piersiowa | Biust | 82 | 82 |
| header:chest | Klatka piersiowa | Klatka/Biust | 76 | 70 |
| label:mother | Mama | Mother | 71 | 18 |
| header:hip | Biodra | Biodro | 53 | 50 |
| header:garment | Długość odzieży | Długość | 52 | 52 |

### pt-BR (46 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Criança | Infantil | 685 | 95 |
| label:mother | Mamãe | Mãe | 622 | 142 |
| label:father | Papai | Pai | 560 | 101 |
| label:child | Criança | Menina | 396 | 57 |
| label:child | Criança | Menino | 152 | 18 |
| label:mother | Mamãe | Mother | 92 | 23 |
| header:garment | Comprimento da peça | Comprimento | 50 | 50 |
| label:father | Papai | Father | 40 | 8 |
| header:garment | Comprimento da peça | Comprimento do Casaco | 23 | 23 |
| header:shoulder | Largura dos ombros | Ombro | 20 | 19 |

### ro (61 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:father | Tata | Tată | 582 | 105 |
| label:mother | Mama | Mamă | 557 | 125 |
| label:child | Copil | Fată | 404 | 58 |
| label:child | Copil | Băiat | 169 | 20 |
| label:mother | Mama | Mother | 101 | 26 |
| header:chest | Piept | Bust | 85 | 85 |
| header:garment | Lungimea articolului | Lungimea îmbrăcămintei | 73 | 67 |
| header:chest | Piept | Torace/bust | 66 | 59 |
| header:garment | Lungimea articolului | Lungime | 52 | 52 |
| header:garment | Lungimea articolului | Lungime articol | 36 | 25 |

### ru (49 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Ребёнок | Дети | 818 | 114 |
| label:child | Ребёнок | Девочка | 523 | 80 |
| label:child | Ребёнок | Мальчик | 378 | 54 |
| label:child | Ребёнок | Детский | 137 | 27 |
| label:mother | Мама | Мать | 97 | 23 |
| label:child | Ребёнок | Ребенок | 95 | 20 |
| header:garment | Длина изделия | Длина одежды | 76 | 70 |
| header:garment | Длина изделия | Длина | 50 | 50 |
| header:chest | Грудь | Обхват груди | 39 | 39 |
| label:father | Папа | Отец | 35 | 6 |

### sv (36 distinct values)

| Key | Glossary | Found | Cells | Prod |
|---|---|---|---|---|
| label:child | Barn | Flicka | 493 | 76 |
| label:child | Barn | Pojke | 387 | 55 |
| header:garment | Plaggets längd | Plagglängd | 181 | 159 |
| header:chest | Bröst | Bystmått | 84 | 84 |
| label:mother | Mamma | Moder | 58 | 15 |
| header:skirt | Kjollängd | Ärm eller kjol | 27 | 23 |
| header:garment | Plaggets längd | Längd | 25 | 25 |
| header:shoulder | Axelbredd | Axel | 19 | 19 |
| header:chest | Bröst | Byst | 15 | 15 |
| header:pants | Byxlängd | Byx-/shortslängd | 8 | 8 |

## Limits

- Mother/father/child swap is detected only when the translated label contains a glossary term of another role, or two roles share one stem; other synonyms (Mutter, Vater) count as non-glossary, not as swaps. Zero swaps found.
- Word-level translation quality outside table cells and the HTML comments inside tables is not checked.
- Row matching is positional, so a table with different row counts is reported once as row_count and compared over the common rows.
