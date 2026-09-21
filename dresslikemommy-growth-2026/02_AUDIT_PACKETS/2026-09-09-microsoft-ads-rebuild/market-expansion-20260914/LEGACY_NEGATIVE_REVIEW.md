# Narrow negative review for eight existing dress languages

Prepared 2026-09-14T21:16:03.793852+00:00. **LOCAL PROPOSAL / NO NATIVE CHANGES.** This covers Spanish, French, German, Danish, Dutch, Italian, Czech and Romanian. Spanish is linked to both US-Spanish and Spain-Spanish. Mergeable rows and complete tests are in [legacy-negative-profiles.json](legacy-negative-profiles.json).

Each locale has eight entries: six qualified Phrase negatives for sewing/digital files and two full-query Exact rental exclusions. No bare garment, style, free, cheap, gift, age, size, wholesale or rental word is added. Current native negatives, US/DE IDs and the USD 0.15 cap remain untouched.

## Continuity and scope

The saved CSV dress positives supply the intended shopping language. Identical Spanish sewing-pattern, Czech sewing-instruction and Romanian instruction seeds retain provenance. Broad existing seeds such as rental, wholesale, SVG and printable are not copied wholesale into this profile. The earlier qualified-seed review has no campaign-level review rows for these eight locales; it does not certify these new candidates.

Campaign negatives reach all child groups. The local check therefore also includes the other saved positives in each affected campaign. Held garment negatives and ad-group-only routing exclusions remain excluded.

## Proposed profiles

### Spanish (es)

| Negative text | Match | Rationale |
|---|---|---|
| `patrón de costura` | Phrase | Sewing pattern for making clothing; reused narrow local seed. |
| `patrones de costura` | Phrase | Separate plural sewing-pattern form. |
| `tutorial de costura` | Phrase | Instructional sewing tutorial, not finished-dress shopping. |
| `patrones pdf` | Phrase | Digital PDF pattern request; PDF qualifies the pattern word. |
| `archivo svg` | Phrase | Digital SVG file request. |
| `archivos svg` | Phrase | Separate plural digital SVG-file request. |
| `alquiler de vestidos madre e hija` | Exact | Only this complete mother-daughter dress-rental query. |
| `renta de vestidos mamá e hija` | Exact | Only this complete rental query using wording relevant to some US-Spanish shoppers; demand unknown. |

Keep US-Spanish and Spain-Spanish country applicability distinct. Rental synonyms, accents and tutorial plurals are not fully covered.

### French (fr)

| Negative text | Match | Rationale |
|---|---|---|
| `patron de couture` | Phrase | Qualified sewing pattern, not the bare word patron. |
| `patrons de couture` | Phrase | Separate plural sewing-pattern form. |
| `tutoriel de couture` | Phrase | A sewing tutorial rather than retail dress shopping. |
| `patron pdf` | Phrase | Digital PDF pattern; PDF qualifies the pattern word. |
| `fichier svg` | Phrase | Digital SVG file request. |
| `fichiers svg` | Phrase | Separate plural digital-file form. |
| `location robes mère fille` | Exact | Only this complete mother-daughter dress-rental query. |
| `louer robes mère fille` | Exact | Only this complete query explicitly asking to rent dresses. |

The old packet also has telegraphic patron couture without de. This short list does not cover every preposition, plural or accent variant.

### German (de)

| Negative text | Match | Rationale |
|---|---|---|
| `nähanleitung für kleider` | Phrase | Instructions for sewing dresses. |
| `kleid selber nähen` | Phrase | Explicitly sewing a dress yourself. |
| `kleider selber nähen` | Phrase | Separate plural dress-making form. |
| `schnittmuster pdf` | Phrase | Digital PDF sewing-pattern request; no bare pattern exclusion. |
| `svg datei` | Phrase | Digital SVG file request. |
| `svg dateien` | Phrase | Separate plural digital SVG-file request. |
| `mutter tochter kleider mieten` | Exact | Only this complete query for renting mother-daughter dresses. |
| `mama tochter kleider mieten` | Exact | Only this complete rental query using mama wording. |

Compound and umlaut-transliteration forms need distinct review. Preserve German campaign506254908 and current negatives until an exact native delta is reviewed.

### Danish (da)

| Negative text | Match | Rationale |
|---|---|---|
| `syvejledning til kjole` | Phrase | Sewing instructions for a dress. |
| `syvejledning til kjoler` | Phrase | Sewing instructions with plural dress wording. |
| `symønster pdf` | Phrase | PDF sewing pattern rather than a clothing print. |
| `symønstre pdf` | Phrase | Separate plural PDF sewing-pattern form. |
| `svg fil` | Phrase | Digital SVG file request; spaced spelling. |
| `svg filer` | Phrase | Separate plural digital-file form. |
| `leje af kjoler mor og datter` | Exact | Only this complete mother-daughter dress-rental query. |
| `udlejning af kjoler mor og datter` | Exact | Only this complete dress-hire query. |

Danish compounds, vowel variants and natural query wording remain model-reviewed candidates. No query-frequency or native-speaker certificate is asserted.

### Dutch (nl)

| Negative text | Match | Rationale |
|---|---|---|
| `jurk naaien` | Phrase | Sewing a dress rather than choosing a finished one. |
| `jurken naaien` | Phrase | Separate plural dress-sewing form. |
| `naaipatroon pdf` | Phrase | Digital PDF sewing pattern. |
| `naaipatronen pdf` | Phrase | Separate plural PDF sewing-pattern form. |
| `svg bestand` | Phrase | Digital SVG file request. |
| `svg bestanden` | Phrase | Separate plural digital-file request. |
| `jurken moeder dochter huren` | Exact | Only this complete mother-daughter dress-rental query. |
| `jurken moeder dochter verhuur` | Exact | Only this complete dress-hire query. |

No bare patroon, zelf maken or verhuur is included. Inflections, compounds and different word order need separate query review.

### Italian (it)

| Negative text | Match | Rationale |
|---|---|---|
| `tutorial di cucito` | Phrase | Qualified sewing tutorial. |
| `tutorial cucito` | Phrase | Compact sewing-tutorial wording without di; demand unmeasured. |
| `come cucire` | Phrase | Explicit how-to-sew instructional request. |
| `cartamodello pdf` | Phrase | Digital PDF sewing pattern. |
| `cartamodelli pdf` | Phrase | Separate plural PDF sewing-pattern form. |
| `file svg` | Phrase | Digital SVG file; file is invariant in Italian singular/plural usage. |
| `noleggio abiti mamma e figlia` | Exact | Only this complete mother-daughter dress-rental query. |
| `affitto vestiti mamma e figlia` | Exact | Only this complete rental wording; comparative query frequency is unknown. |

No bare cartamodello, fai da te, da stampare or ingrosso is included. The qualified list is deliberately narrower than every instruction query.

### Czech (cs)

| Negative text | Match | Rationale |
|---|---|---|
| `návod na šití` | Phrase | Sewing instructions; reused narrow local seed. |
| `návody na šití` | Phrase | Separate plural sewing-instruction form. |
| `střih pdf` | Phrase | PDF pattern request; bare střih can also refer to a garment cut. |
| `střihy pdf` | Phrase | Separate plural digital-pattern form. |
| `svg soubor` | Phrase | Digital SVG file request. |
| `svg soubory` | Phrase | Separate plural digital-file request. |
| `půjčovna šatů máma dcera` | Exact | Only this complete mother-daughter dress-hire query. |
| `půjčení šatů pro maminku a dceru` | Exact | Only this complete query requesting rental dresses. |

Czech inflection and diacritic-free queries materially limit a short literal list. This file does not certify native eligibility or phrase demand.

### Romanian (ro)

| Negative text | Match | Rationale |
|---|---|---|
| `tutorial de cusut` | Phrase | Qualified sewing tutorial. |
| `cum să cos` | Phrase | How-to-sew intent; reused local instruction seed. |
| `tipar pdf` | Phrase | Digital PDF pattern; no bare tipar or clothing-print exclusion. |
| `tipare pdf` | Phrase | Separate plural PDF-pattern form. |
| `fișier svg` | Phrase | Digital SVG file request. |
| `fișiere svg` | Phrase | Separate plural digital-file request. |
| `închiriere rochii mamă fiică` | Exact | Only this complete mother-daughter dress-rental query. |
| `inchiriere rochii mama fiica` | Exact | Explicit diacritic-free variant of that complete rental query. |

Only the rental Exact query has an explicit accent-free counterpart here. Other accented words do not imply coverage of unaccented spelling.

## Checks and residual risk

**Local checks passed:** 64 locale/text/type rows: 48 Phrase and 16 Exact. Zero literal conflicts against 126 affected saved positive rows, including 63 dress rows. All 64 ordinary buyer holdouts remain unblocked; all 64 direct negative probes match; 16 deliberately uncovered variant/longer-query probes remain unblocked.

Buyer holdouts cover ordinary dress searches, low-price/free-delivery searches, floral prints, larger sizes, birthday/family photos, T-shirt dresses and gifts/reviews. Testing these intents does not claim any requested item, size or delivery benefit is available.

**Eight plausible mixed-buyer queries still collide.** Each shopper explicitly asks to buy finished dresses instead of using sewing instructions. The excluded phrase still matches, so these are known false-positive risks, not passed holdouts. Native query evidence must decide whether to retain the phrase or use a justified full-query Exact alternative.

| Locale | Buyer query that still matches a negative |
|---|---|
| es | comprar vestidos madre e hija en lugar de un tutorial de costura |
| fr | acheter robes mère fille plutôt que suivre un tutoriel de couture |
| de | mutter tochter kleider kaufen statt kleid selber nähen |
| da | køb kjoler til mor og datter i stedet for syvejledning til kjole |
| nl | moeder dochter jurken kopen in plaats van een jurk naaien |
| it | comprare vestiti mamma e figlia invece di seguire un tutorial di cucito |
| cs | chci koupit šaty pro maminku a dceru ne návod na šití |
| ro | vreau să cumpăr rochii mamă fiică nu un tutorial de cusut |

Negative matching does not automatically include plurals, synonyms, spelling variants or alternate accents. Compounds, case endings and word order create gaps; Exact rental negatives deliberately miss longer queries. The checks preserve accents and use ordered tokens, not Microsoft semantic positive matching, complete punctuation normalization, inherited lists or actual auctions. [Negative rules](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_aboutnegativekeywords), [positive matching](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_matchoptions).

No native-speaker certification, native conflict report, current negative export or query-performance test was obtained. No CPC, CPA, waste-reduction or profit improvement is claimed. The root must rerun conflicts against all new positives in its separate 20-language library and compare country idiom before merging.

## Next exact action

Reconcile this profile with each native account/shared/campaign/group negative list and positive list; preserve duplicate IDs and inspect the mixed-buyer examples before choosing the precise paused delta. Preserve German campaign 506254908 and US campaign 506254907. No numeric budget, activation or live negative modification is supplied by these files.

Continuation: Merge these eight local profiles into the root language library, rerun cross-profile buyer/positive tests, and prepare the exact native paused delta after current inheritance is read back.
