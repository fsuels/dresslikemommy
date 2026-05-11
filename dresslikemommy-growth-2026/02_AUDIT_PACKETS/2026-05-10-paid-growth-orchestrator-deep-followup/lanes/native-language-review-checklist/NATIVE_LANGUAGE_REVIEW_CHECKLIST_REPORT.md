# Native-Language Review Checklist

**Lane:** D / Native-Language-Review-Checklist
**AGENT_CONTINUITY_ANCHOR:** 2026-05-10-paid-growth-orchestrator-deep-followup
**Date (Pacific):** 2026-05-10
**Author:** Native-Language-Review-Checklist subagent (local file write only; no browser, no network, no Shopify/Ads/Merchant/Pinterest/GA4/theme writes)
**Tracks:** `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE` (currently `PARTIALLY_MITIGATED_LOCAL_OPTIONS_READY__OWNER_DECISION_REQUIRED`)

---

## 0. Scope and guardrails

This lane produces an operator-paste-ready review checklist that can be handed to native speakers (and to QA reviewers walking the live site in their native language) so the gate above can move from `PARTIALLY_MITIGATED` to `SOLVED_READBACK_PASSED` per locale.

This lane:

- Reads from local files only.
- Does not touch the theme, Shopify Admin, Google Ads, Merchant Center, Pinterest, GA4, or any browser surface.
- Does not modify `ops/PROBLEM_TRACKER.md` (parent integrates).
- Does not approve, enable, or import any campaign.
- Does not invent locale-specific copy rows; every quoted row is read from the source CSV.

Source files inspected (cited at every claim below):

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_rsa_options.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_keyword_option_notes.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_copy_options_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/NATIVE_LANGUAGE_COPY_OPTIONS_REPORT.md`
- `ops/GROWTH_NORTH_STAR.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md`
- `AGENTS.md` (country-qualified URL pattern guidance)

Source-of-truth note from the summary JSON: the packet covers **14 locale variants** across **5 themes per locale**, with `length_violations: 0` and `forbidden_claim_hits: 0`. Every locale row is flagged `native_speaker_review_required_for_all_rows: true`.

---

## 1. Inventory of existing native-language copy options (14 locales, 5 themes each)

The block below reproduces every headline option (`H`) and description option (`D`) from `native_language_rsa_options.csv` exactly as written. Each cell in that CSV stores options pipe-delimited; the `Dress Like Mommy` brand-name headline is preserved across all locales as written. Themes per locale: `mommy_me_dresses`, `family_matching`, `matching_pajamas`, `matching_swimwear`, `daddy_me`.

Source: `native_language_rsa_options.csv`. Keyword notes source: `native_language_keyword_option_notes.csv`.

### 1.1 `es-ES` Spanish (Spain)
- **mommy_me_dresses**
  - H: `Vestidos mamá e hija` | `Looks madre e hija` | `Dress Like Mommy`
  - D: `Looks coordinados para fotos, cumpleaños y días en familia.` | `Elige tallas por separado para cada persona en la página del producto.`
- **family_matching**
  - H: `Looks familiares` | `Ropa familiar a juego` | `Dress Like Mommy`
  - D: `Diseña un look coordinado para madres, padres, niñas y niños.` | `Ideas de ropa familiar para fotos y momentos especiales.`
- **matching_pajamas**
  - H: `Pijamas familiares` | `Pijamas a juego` | `Dress Like Mommy`
  - D: `Ideas de pijamas a juego para mañanas tranquilas y fotos familiares.` | `Elige tallas por separado para cada persona.`
- **matching_swimwear**
  - H: `Bañadores familiares` | `Moda playa a juego` | `Dress Like Mommy`
  - D: `Looks de baño coordinados para piscina, playa y fotos familiares.` | `Combina tallas de adultos, niñas y niños en la página del producto.`
- **daddy_me**
  - H: `Looks papá e hijo` | `Padre e hijo a juego` | `Dress Like Mommy`
  - D: `Ideas de looks padre e hijo para fotos y planes familiares.` | `Elige tallas por separado para padre e hijo.`

### 1.2 `it-IT` Italian (Italy)
- **mommy_me_dresses**
  - H: `Abiti mamma e figlia` | `Look madre e figlia` | `Dress Like Mommy`
  - D: `Look coordinati per foto, compleanni e giornate in famiglia.` | `Scegli taglie separate per ogni persona nella pagina prodotto.`
- **family_matching**
  - H: `Look famiglia coordinati` | `Outfit famiglia` | `Dress Like Mommy`
  - D: `Componi un look coordinato per mamme, papà, bambine e bambini.` | `Idee di outfit famiglia per foto e momenti speciali.`
- **matching_pajamas**
  - H: `Pigiami famiglia` | `Pigiami coordinati` | `Dress Like Mommy`
  - D: `Idee di pigiami coordinati per mattine tranquille e foto in famiglia.` | `Scegli taglie separate per ogni persona.`
- **matching_swimwear**
  - H: `Costumi famiglia` | `Moda mare coordinata` | `Dress Like Mommy`
  - D: `Look mare coordinati per piscina, spiaggia e foto in famiglia.` | `Combina taglie per adulti e bambini nella pagina prodotto.`
- **daddy_me**
  - H: `Look papà e figlio` | `Padre figlio coordinati` | `Dress Like Mommy`
  - D: `Idee di look papà e figlio per foto e giornate in famiglia.` | `Scegli taglie separate per papà e bambino.`

### 1.3 `pt-PT` Portuguese (Portugal) — flagged `pt-BR` storefront-behavior risk
- **mommy_me_dresses**
  - H: `Vestidos mãe e filha` | `Looks mãe e filha` | `Dress Like Mommy`
  - D: `Looks coordenados para fotos, aniversários e momentos em família.` | `Escolha tamanhos separados para cada pessoa na página do produto.`
- **family_matching**
  - H: `Looks família` | `Roupa família a combinar` | `Dress Like Mommy`
  - D: `Crie um look coordenado para mães, pais, crianças e bebés.` | `Ideias de roupa familiar para fotos e momentos especiais.`
- **matching_pajamas**
  - H: `Pijamas em família` | `Pijamas a combinar` | `Dress Like Mommy`
  - D: `Ideias de pijamas a combinar para manhãs calmas e fotos em família.` | `Escolha tamanhos separados para cada pessoa.`
- **matching_swimwear**
  - H: `Moda praia a combinar` | `Praia em família` | `Dress Like Mommy`
  - D: `Looks de praia coordenados para piscina, praia e fotos em família.` | `Combine tamanhos de adultos e crianças na página do produto.`
- **daddy_me**
  - H: `Looks pai e filho` | `Pai e filho a combinar` | `Dress Like Mommy`
  - D: `Ideias de looks pai e filho para fotos e planos em família.` | `Escolha tamanhos separados para pai e criança.`

### 1.4 `ro-RO` Romanian (Romania)
- **mommy_me_dresses**
  - H: `Rochii mamă și fiică` | `Ținute mamă fiică` | `Dress Like Mommy`
  - D: `Ținute coordonate pentru poze, aniversări și zile în familie.` | `Alege mărimi separate pentru fiecare persoană pe pagina produsului.`
- **family_matching**
  - H: `Ținute familie` | `Familie asortată` | `Dress Like Mommy`
  - D: `Creează un look coordonat pentru mame, tați și copii.` | `Idei de ținute de familie pentru poze și momente speciale.`
- **matching_pajamas**
  - H: `Pijamale familie` | `Pijamale asortate` | `Dress Like Mommy`
  - D: `Idei de pijamale asortate pentru dimineți liniștite și poze de familie.` | `Alege mărimi separate pentru fiecare persoană.`
- **matching_swimwear**
  - H: `Costume baie familie` | `Costume baie asortate` | `Dress Like Mommy`
  - D: `Lookuri de baie coordonate pentru piscină, plajă și poze de familie.` | `Combină mărimi pentru adulți și copii pe pagina produsului.`
- **daddy_me**
  - H: `Ținute tată copil` | `Tată copil asortat` | `Dress Like Mommy`
  - D: `Idei de ținute tată și copil pentru poze și zile în familie.` | `Alege mărimi separate pentru tată și copil.`

### 1.5 `de-DE` German (Germany)
- **mommy_me_dresses**
  - H: `Mama Tochter Kleider` | `Partnerlook Kleider` | `Dress Like Mommy`
  - D: `Abgestimmte Looks für Fotos, Geburtstage und Familienmomente.` | `Wähle Größen für jede Person separat auf der Produktseite.`
- **family_matching**
  - H: `Familien Outfits` | `Partnerlook Familie` | `Dress Like Mommy`
  - D: `Erstelle einen abgestimmten Look für Mütter, Väter und Kinder.` | `Outfit-Ideen für Familienfotos und besondere Momente.`
- **matching_pajamas**
  - H: `Familien Pyjamas` | `Pyjamas im Partnerlook` | `Dress Like Mommy`
  - D: `Ideen für passende Pyjamas an ruhigen Morgen und für Familienfotos.` | `Wähle Größen für jede Person separat.`
- **matching_swimwear**
  - H: `Bademode Familie` | `Partnerlook Bademode` | `Dress Like Mommy`
  - D: `Abgestimmte Bademode-Looks für Pool, Strand und Familienfotos.` | `Kombiniere Größen für Erwachsene und Kinder auf der Produktseite.`
- **daddy_me**
  - H: `Papa Kind Outfits` | `Vater Kind Looks` | `Dress Like Mommy`
  - D: `Ideen für Vater-Kind-Looks bei Fotos und Familienplänen.` | `Wähle Größen für Vater und Kind separat.`

### 1.6 `nl-NL` Dutch (Netherlands)
- **mommy_me_dresses**
  - H: `Mama Dochter Jurken` | `Moeder Dochter Jurken` | `Dress Like Mommy`
  - D: `Gecoördineerde looks voor foto's, verjaardagen en familiedagen.` | `Kies aparte maten voor elke persoon op de productpagina.`
- **family_matching**
  - H: `Familie Outfits` | `Matching Familie Looks` | `Dress Like Mommy`
  - D: `Maak een gecoördineerde look voor moeders, vaders en kinderen.` | `Outfitideeën voor familiefoto's en bijzondere momenten.`
- **matching_pajamas**
  - H: `Familie Pyjama's` | `Matching Pyjama's` | `Dress Like Mommy`
  - D: `Ideeën voor bijpassende pyjama's voor rustige ochtenden en familiefoto's.` | `Kies aparte maten voor elke persoon.`
- **matching_swimwear**
  - H: `Familie Badmode` | `Matching Badmode` | `Dress Like Mommy`
  - D: `Gecoördineerde badmode voor zwembad, strand en familiefoto's.` | `Combineer maten voor volwassenen en kinderen op de productpagina.`
- **daddy_me**
  - H: `Papa Kind Outfits` | `Vader Kind Looks` | `Dress Like Mommy`
  - D: `Ideeën voor vader-kind looks voor foto's en familiedagen.` | `Kies aparte maten voor vader en kind.`

### 1.7 `fr-FR` French (France)
- **mommy_me_dresses**
  - H: `Robes mère fille` | `Looks mère fille` | `Dress Like Mommy`
  - D: `Looks coordonnés pour photos, anniversaires et moments en famille.` | `Choisissez des tailles séparées pour chaque personne sur la page produit.`
- **family_matching**
  - H: `Tenues famille` | `Looks assortis famille` | `Dress Like Mommy`
  - D: `Créez un look coordonné pour mamans, papas et enfants.` | `Idées de tenues famille pour photos et moments spéciaux.`
- **matching_pajamas**
  - H: `Pyjamas famille` | `Pyjamas assortis` | `Dress Like Mommy`
  - D: `Idées de pyjamas assortis pour matins calmes et photos en famille.` | `Choisissez des tailles séparées pour chaque personne.`
- **matching_swimwear**
  - H: `Maillots famille` | `Maillots assortis` | `Dress Like Mommy`
  - D: `Looks de bain coordonnés pour piscine, plage et photos en famille.` | `Associez les tailles adultes et enfants sur la page produit.`
- **daddy_me**
  - H: `Looks père enfant` | `Tenues papa enfant` | `Dress Like Mommy`
  - D: `Idées de looks père enfant pour photos et journées en famille.` | `Choisissez des tailles séparées pour le père et l'enfant.`

### 1.8 `fr-BE` French for Belgium
Copy rows are **identical to `fr-FR`** as written in the source CSV (every headline and description text matches `fr-FR`). Source row in CSV: market `BE-FR`, locale `fr-BE`. The `review_reason` in that row reads: `Belgium needs French/Dutch split decision, native review, and landing-language QA before use`. The Belgian-French dialect was therefore not separately drafted; reviewer must explicitly accept or rewrite for `fr-BE` register.

### 1.9 `nl-BE` Dutch for Belgium (Flemish)
Copy rows are **identical to `nl-NL`** as written in the source CSV (every headline and description text matches `nl-NL`). Source row in CSV: market `BE-NL`, locale `nl-BE`. The `review_reason` is the same Belgium split note as above. The Flemish/Belgian-Dutch register was not separately drafted; reviewer must explicitly accept or rewrite for `nl-BE`.

### 1.10 `sv-SE` Swedish (Sweden)
- **mommy_me_dresses**
  - H: `Mamma dotter klänning` | `Mor dotter klänning` | `Dress Like Mommy`
  - D: `Samordnade looks för foton, födelsedagar och familjedagar.` | `Välj separata storlekar för varje person på produktsidan.`
- **family_matching**
  - H: `Familjeoutfits` | `Matchande familj` | `Dress Like Mommy`
  - D: `Skapa en samordnad look för mammor, pappor och barn.` | `Outfitidéer för familjefoton och särskilda stunder.`
- **matching_pajamas**
  - H: `Familjepyjamas` | `Matchande pyjamas` | `Dress Like Mommy`
  - D: `Idéer för matchande pyjamas för lugna morgnar och familjefoton.` | `Välj separata storlekar för varje person.`
- **matching_swimwear**
  - H: `Familjebadkläder` | `Matchande badkläder` | `Dress Like Mommy`
  - D: `Samordnade badlooks för pool, strand och familjefoton.` | `Kombinera storlekar för vuxna och barn på produktsidan.`
- **daddy_me**
  - H: `Pappa barn outfits` | `Far barn outfits` | `Dress Like Mommy`
  - D: `Idéer för pappa-barn looks för foton och familjedagar.` | `Välj separata storlekar för pappa och barn.`

### 1.11 `da-DK` Danish (Denmark)
- **mommy_me_dresses**
  - H: `Mor datter kjoler` | `Mamma datter kjoler` | `Dress Like Mommy`
  - D: `Koordinerede looks til billeder, fødselsdage og familiedage.` | `Vælg separate størrelser til hver person på produktsiden.`
- **family_matching**
  - H: `Familie outfits` | `Matchende familie` | `Dress Like Mommy`
  - D: `Skab et koordineret look til mødre, fædre og børn.` | `Outfitidéer til familiebilleder og særlige øjeblikke.`
- **matching_pajamas**
  - H: `Familie pyjamas` | `Matchende pyjamas` | `Dress Like Mommy`
  - D: `Idéer til matchende pyjamas til rolige morgener og familiebilleder.` | `Vælg separate størrelser til hver person.`
- **matching_swimwear**
  - H: `Familie badetøj` | `Matchende badetøj` | `Dress Like Mommy`
  - D: `Koordinerede badelooks til pool, strand og familiebilleder.` | `Kombinér størrelser til voksne og børn på produktsiden.`
- **daddy_me**
  - H: `Far barn outfits` | `Far barn looks` | `Dress Like Mommy`
  - D: `Idéer til far-barn looks til billeder og familiedage.` | `Vælg separate størrelser til far og barn.`

Reviewer note: row 1 headline 2 (`Mamma datter kjoler`) appears to be a Swedish/Norwegian spelling of "mamma" inside a Danish row; flag for native confirmation — the canonical Danish form is `mor` (already present in headline 1) or `mor/mamma` debate.

### 1.12 `pl-PL` Polish (Poland)
- **mommy_me_dresses**
  - H: `Sukienki mama córka` | `Styl mama córka` | `Dress Like Mommy`
  - D: `Dopasowane stylizacje na zdjęcia, urodziny i rodzinne dni.` | `Wybierz osobne rozmiary dla każdej osoby na stronie produktu.`
- **family_matching**
  - H: `Stylizacje rodzinne` | `Ubrania rodzinne` | `Dress Like Mommy`
  - D: `Stwórz spójny look dla mam, ojców i dzieci.` | `Pomysły na rodzinne stylizacje do zdjęć i ważnych chwil.`
- **matching_pajamas**
  - H: `Piżamy rodzinne` | `Piżamy dla rodziny` | `Dress Like Mommy`
  - D: `Pomysły na dopasowane piżamy na spokojne poranki i rodzinne zdjęcia.` | `Wybierz osobne rozmiary dla każdej osoby.`
- **matching_swimwear**
  - H: `Stroje kąpielowe` | `Moda plażowa rodziny` | `Dress Like Mommy`
  - D: `Dopasowane looki kąpielowe na basen, plażę i rodzinne zdjęcia.` | `Połącz rozmiary dorosłych i dzieci na stronie produktu.`
- **daddy_me**
  - H: `Stroje tata dziecko` | `Styl tata dziecko` | `Dress Like Mommy`
  - D: `Pomysły na stylizacje tata-dziecko do zdjęć i rodzinnych dni.` | `Wybierz osobne rozmiary dla taty i dziecka.`

### 1.13 `cs-CZ` Czech (Czechia)
- **mommy_me_dresses**
  - H: `Šaty máma dcera` | `Look máma dcera` | `Dress Like Mommy`
  - D: `Sladěné outfity na fotky, narozeniny a rodinné dny.` | `Vyberte samostatné velikosti pro každou osobu na stránce produktu.`
- **family_matching**
  - H: `Rodinné outfity` | `Sladěné outfity` | `Dress Like Mommy`
  - D: `Vytvořte sladěný look pro maminky, tatínky a děti.` | `Nápady na rodinné outfity pro fotky a zvláštní chvíle.`
- **matching_pajamas**
  - H: `Rodinná pyžama` | `Sladěná pyžama` | `Dress Like Mommy`
  - D: `Nápady na sladěná pyžama pro klidná rána a rodinné fotky.` | `Vyberte samostatné velikosti pro každou osobu.`
- **matching_swimwear**
  - H: `Rodinné plavky` | `Sladěné plavky` | `Dress Like Mommy`
  - D: `Sladěné plavkové looky k bazénu, na pláž a rodinné fotky.` | `Kombinujte velikosti dospělých a dětí na stránce produktu.`
- **daddy_me**
  - H: `Táta dítě outfity` | `Look táta dítě` | `Dress Like Mommy`
  - D: `Nápady na looky táta-dítě pro fotky a rodinné dny.` | `Vyberte samostatné velikosti pro tátu a dítě.`

### 1.14 `el-GR` Greek (Greece)
- **mommy_me_dresses**
  - H: `Φορέματα μαμά κόρη` | `Στυλ μαμά κόρη` | `Dress Like Mommy`
  - D: `Συντονισμένα looks για φωτογραφίες, γενέθλια και οικογενειακές στιγμές.` | `Επιλέξτε ξεχωριστά μεγέθη για κάθε άτομο στη σελίδα προϊόντος.`
- **family_matching**
  - H: `Οικογενειακά σύνολα` | `Ασορτί οικογένεια` | `Dress Like Mommy`
  - D: `Δημιουργήστε συντονισμένο look για μαμάδες, μπαμπάδες και παιδιά.` | `Ιδέες για οικογενειακά σύνολα σε φωτογραφίες και ιδιαίτερες στιγμές.`
- **matching_pajamas**
  - H: `Οικογενειακές πιτζάμες` | `Ασορτί πιτζάμες` | `Dress Like Mommy`
  - D: `Ιδέες για ασορτί πιτζάμες σε ήσυχα πρωινά και οικογενειακές φωτογραφίες.` | `Επιλέξτε ξεχωριστά μεγέθη για κάθε άτομο.`
- **matching_swimwear**
  - H: `Οικογενειακά μαγιό` | `Ασορτί μαγιό` | `Dress Like Mommy`
  - D: `Συντονισμένα looks για πισίνα, παραλία και οικογενειακές φωτογραφίες.` | `Συνδυάστε μεγέθη ενηλίκων και παιδιών στη σελίδα προϊόντος.`
- **daddy_me**
  - H: `Σύνολα μπαμπά παιδί` | `Στυλ μπαμπά παιδί` | `Dress Like Mommy`
  - D: `Ιδέες για looks μπαμπά-παιδί σε φωτογραφίες και οικογενειακές ημέρες.` | `Επιλέξτε ξεχωριστά μεγέθη για μπαμπά και παιδί.`

Validation summary (from `native_language_copy_options_summary.json`): `rsa_option_rows: 14`, `keyword_note_rows: 14`, `themes_per_locale: 5`, `max_headline_length: 24`, `max_description_length: 73`, `length_violations: 0`, `forbidden_claim_hits: 0`. Headline limit `30`, description limit `90`.

---

## 2. Per-locale native-reviewer instruction sheet

Each brief below is operator-paste-ready. Hand the section to a native reviewer with access to the live storefront in their locale. Brand voice (from `ops/GROWTH_NORTH_STAR.md`): coordinated family looks for matching family / mommy-and-me / daddy-and-me / vacation / photo-day / pajama / swimwear; dropshipping business with no physical store, no warehouse, no local stocked inventory, no guaranteed on-hand stock; growth that is "aggressive but intelligent" — controlled, conversion-quality first.

Forbidden-claim rules (apply to ALL locales — these are the "no" answers; if a reviewer's rewrite introduces any of these, reject):

- No fast/rush/same-day/guaranteed-delivery shipping claims.
- No free-shipping promises in ad copy (note: standard shipping is "included in product price" on-site per Phase 1 clarity work — this is a landing-page statement, not an ad-copy claim).
- No bestseller / most popular / top-rated / viral / trending claims.
- No review counts, star ratings, or social-proof volume claims.
- No sale, discount, coupon, promo, free gift, limited-time, or urgency claims unless an active verified promotion exists and is approved.
- No physical store, warehouse, local inventory, stocked inventory, nearby inventory, pickup, or guaranteed-on-hand-stock claims.
- No guaranteed-fit, guaranteed-availability, or no-risk-returns claims.

Per-row review questions the reviewer must answer **YES / NO / REWRITE** for every headline and every description option in the locale (pipe-split each cell):

1. Does the headline mean what it says in fluent native register? (Y/N/REWRITE)
2. Is the tone right for matching-family / mommy-and-me / daddy-and-me apparel sold by a dropshipping ecommerce site? (Y/N/REWRITE)
3. Would a real local shopper read this and click — does it match how locals actually search? (Y/N/REWRITE)
4. Are diacritics, accents, spelling, capitalization, and gender/number agreement correct? (Y/N/REWRITE)
5. Does the copy avoid every forbidden claim listed above? (Y/N/REWRITE)
6. If REWRITE, propose a replacement that fits the original headline limit (30 chars) or description limit (90 chars).

### 2.1 `es-ES` reviewer brief
- **Target:** European Spanish (Spain). Source CSV `landing_locale_evidence`: `/es product URLs with country=ES previously read back as Spain / Spanish / EUR`. Drafted as `es-ES` (Spanish-Spain), NOT `es-MX` / `es-LA`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - Watch for Latin-American Spanish leaks: `bañadores` (Spain) vs `trajes de baño` (LatAm) — copy uses the Spain form `bañadores`; confirm Spain shoppers prefer that.
  - Vosotros vs ustedes register: copy uses imperative `Elige`/`Combina`/`Diseña` (informal `tú`); confirm informal tone is right for the brand (kids/family) in Spain.
  - "mamá" vs "madre" — both used; check naturalness of `Vestidos mamá e hija` vs `Looks madre e hija`.
- **Per-row check:** all 5 themes × 2 description option strings × 3 headline option strings; reviewer answers Q1–Q6.

### 2.2 `it-IT` reviewer brief
- **Target:** Italian (Italy). Source `landing_locale_evidence`: `/it product URLs with country=IT previously read back as Italy / Italian / EUR`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - Imperative tu (`Scegli`, `Combina`, `Componi`) — confirm informal register is right for family apparel.
  - `bambine e bambini` is gender-explicit — check whether locals prefer the masculine plural `bambini` as inclusive or whether the explicit pair reads better.
  - `costumi famiglia` (swimwear) — confirm this reads as swimwear and not as halloween-style "costumes." Italian `costume da bagno` is fully unambiguous; consider whether the shorter `costumi` alone is safe.

### 2.3 `pt-PT` reviewer brief — HIGH RISK
- **Target:** European Portuguese (Portugal). Source `landing_locale_evidence`: `/pt product URLs with country=PT previously read back as Portugal / pt-BR / EUR`. The copy was drafted in `pt-PT`, but the storefront path served `pt-BR` behavior at evidence time.
- **`review_reason`:** `Review European Portuguese wording because storefront path currently serves pt-BR locale behavior`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - PT vs BR: copy uses `bebés` (PT) not `bebês` (BR), `fatos de banho` does not appear (instead uses `Moda praia a combinar`/`Praia em família`) — confirm this is acceptable; in Portugal the actual swimwear word is `fatos de banho`. The keyword notes file does list `fatos de banho família` as a recommended keyword.
  - `pijamas em família` / `pijamas a combinar` — `a combinar` is European Portuguese for "matching"; confirm naturalness.
  - `manhãs calmas` — confirm this is the right register.
  - **CRITICAL:** if the storefront still serves `pt-BR` content when traffic lands, ad copy in `pt-PT` will visibly mismatch the page. Reviewer must do landing QA (section 3) before approving paid use.

### 2.4 `ro-RO` reviewer brief
- **Target:** Romanian (Romania). Source `landing_locale_evidence`: `/ro product URLs with country=RO previously read back as Romania / Romanian / RON`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - Diacritics: `mamă`, `și`, `mărimi`, `dimineți`, `liniștite`, `tată`, `piscină`, `plajă` — confirm correct ș/ț (with comma) vs incorrect ş/ţ (with cedilla).
  - `Lookuri` vs `Look-uri` — copy uses `Lookuri`; confirm acceptable in modern Romanian e-comm copy.
  - `Familie asortată` — confirm this reads as "matching family" rather than "well-stocked family."
  - RON pricing context: ads will appear with RON currency landing — keep ad copy free of currency claims.

### 2.5 `de-DE` reviewer brief
- **Target:** German (Germany). Source `landing_locale_evidence`: `Base English product URLs with country=DE passed product/cart/checkout presentment in EUR; native DE landing not proven`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - **`Sie` vs `du`:** copy uses informal `du` imperative (`Wähle`, `Kombiniere`, `Erstelle`). German e-commerce historically used `Sie`; informal `du` is increasingly common for young/family/lifestyle brands. Confirm which register matches Dress Like Mommy positioning. If `Sie`, then headlines stay (no verbs) but descriptions need rewriting (`Wählen Sie...`, `Kombinieren Sie...`).
  - `Partnerlook` is a German-specific term for matching outfits — confirm appropriate for parent-child contexts (typically used for couples; can read odd for parent-child). The keyword notes use `partnerlook kleider`, `partnerlook familie`, `partnerlook bademode` — flag for native sanity check.
  - Compound nouns: `Familienmomente`, `Familienfotos`, `Familienpläne`, `Bademode-Looks` — confirm casing and hyphenation conventions.
  - Native DE landing/policy quality is **not cleared**; landing QA (section 3) is mandatory before any local-language ad use.

### 2.6 `nl-NL` reviewer brief
- **Target:** Dutch (Netherlands). Source `landing_locale_evidence`: `Base English product URLs with country=NL reached EUR product/cart/rates; native NL landing not proven`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - "Matching" anglicism: copy uses `Matching Familie Looks`, `Matching Pyjama's`, `Matching Badmode`. Common in NL e-comm, but reviewer must confirm acceptability vs full-Dutch alternatives like `bijpassend` / `gecoördineerd`.
  - Apostrophes in `pyjama's`, `foto's` — Dutch plural-with-apostrophe is correct here; confirm not changed by autocorrect.
  - `Gecoördineerde` (with diaeresis on the second `o`) — confirm spelling preserved.
  - Informal `je`/imperative `Kies`/`Combineer`/`Maak` — confirm tone.
  - NL-specific check confirmed in continuity: NL UI checkout passed at `en-NL`/EUR; native NL landing is still not proven.

### 2.7 `fr-FR` reviewer brief
- **Target:** French (France). Source `landing_locale_evidence`: `Base English product URLs with country=FR passed product/cart/checkout presentment in EUR; native FR landing not proven`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - Formal `vous` is used (`Choisissez`, `Associez`). Confirm right for family apparel — many young/lifestyle FR brands use `tu` (`Choisis`, `Associe`). Decide and stay consistent.
  - `Looks` and `assortis` — confirm `looks` (English borrowing) is acceptable in FR e-comm or whether `tenues` should replace it everywhere.
  - `Maillots` is correct (FR for swimwear); confirm not confused with sports jerseys.
  - `Tenues famille` vs `tenues assorties famille` — keyword file lists `tenues famille assorties`; confirm consistency.

### 2.8 `fr-BE` reviewer brief — Belgian French
- **Target:** French for Belgium. Source `landing_locale_evidence`: `Base English product URLs with country=BE passed EUR product/cart/checkout; native BE language split not proven`.
- **`review_reason`:** `Belgium needs French/Dutch split decision, native review, and landing-language QA before use`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - **Copy is literally identical to `fr-FR`** in the source CSV. Reviewer must explicitly accept that fr-FR copy is acceptable for fr-BE shoppers OR rewrite for Belgian register (e.g., possible Belgian-French preferences in everyday vocabulary, though for ad copy at this length the differences are typically minor).
  - Belgium routing/UI: confirm whether the storefront serves an explicitly fr-BE experience or a generic fr fallback, and whether the country selector shows Belgium with EUR.
  - This is a "split decision" gate before any BE local-language structure exists.

### 2.9 `nl-BE` reviewer brief — Flemish (Dutch for Belgium)
- **Target:** Dutch for Belgium. Source `landing_locale_evidence`: same as fr-BE.
- **`review_reason`:** same as fr-BE.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - **Copy is literally identical to `nl-NL`** in the source CSV. Reviewer must explicitly accept nl-NL copy for nl-BE shoppers OR rewrite for Flemish register.
  - Flemish register prefers some different word choices (e.g., `kledij` is common in BE-NL; NL-NL prefers `kleding`). Copy currently uses `kleding`-family; confirm acceptability.
  - `Matching` anglicism is also common in Flemish e-comm; confirm.
  - Belgium split decision is a prerequisite for any nl-BE structure.

### 2.10 `sv-SE` reviewer brief
- **Target:** Swedish (Sweden). Source `landing_locale_evidence`: `Base English product URLs with country=SE passed product/cart/checkout presentment in SEK; native SE landing not proven`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - `klänning` (singular) vs `klänningar` (plural) — copy uses singular `klänning` in headlines (`Mamma dotter klänning`, `Mor dotter klänning`). Confirm singular is intentional and reads right (in Swedish ad copy "dresses" is often plural `klänningar`).
  - `Familjebadkläder` (compound) — confirm correctly compounded.
  - Imperative `Välj`, `Kombinera`, `Skapa` — informal `du` register; confirm right for family apparel.
  - "Anglicism" check: copy uses `looks`, `outfits`, `outfitidéer` — confirm acceptable in modern SE e-comm vs full Swedish alternatives.

### 2.11 `da-DK` reviewer brief
- **Target:** Danish (Denmark). Source `landing_locale_evidence`: `Base English product URLs with country=DK passed product/cart/checkout presentment in DKK; native DK landing not proven`. DK CH/DK no-payment checkout-to-shipping passed in continuity evidence.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - **Likely error to flag:** mommy_me_dresses headline option 2 reads `Mamma datter kjoler`. Danish for "mom" is `mor` (used in headline 1 `Mor datter kjoler`). `Mamma` is Swedish/Norwegian. Reviewer should mark REWRITE — likely intended Danish form is `Mor datter kjoler` (already exists) or `Mor og datter kjoler`.
  - Imperative `Vælg`, `Skab`, `Kombinér` — informal register, confirm.
  - `Familie pyjamas` — Danish is more typically `familie-pyjamas` with a hyphen or compound `familiepyjamas`. Confirm.
  - "Anglicisms" `outfits`, `looks` — confirm acceptability.

### 2.12 `pl-PL` reviewer brief
- **Target:** Polish (Poland). Source `landing_locale_evidence`: `Base English product URLs with country=PL passed product/cart/checkout presentment in PLN; native PL landing not proven`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - Polish diacritics: `ż`, `ż`, `ą`, `ę`, `ó`, `ł`, `ś`, `ć`, `ź` — confirm none stripped or replaced.
  - Genitive/instrumental case agreement: `Dopasowane stylizacje na zdjęcia` (acc. pl. zdjęcia) — confirm cases throughout.
  - `Stroje kąpielowe` (swimwear) is correct; `Moda plażowa rodziny` — confirm naturalness.
  - Imperative `Wybierz`, `Stwórz`, `Połącz` — informal register; confirm.
  - Polish search behavior often uses noun phrases without verbs; check whether the descriptions read as native search-page snippets or like translation.

### 2.13 `cs-CZ` reviewer brief
- **Target:** Czech (Czechia). Source `landing_locale_evidence`: `Base English product URLs with country=CZ passed product/cart/checkout presentment in CZK; native CZ landing not proven`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - Czech diacritics: `š`, `ě`, `é`, `á`, `í`, `ý`, `ž`, `ů`, `ř` — confirm preserved.
  - Imperative formal vs informal: copy uses formal `Vyberte`, `Vytvořte`, `Kombinujte` (2nd person plural / formal). German-style formal register may be right for Czech; confirm vs informal `Vyber`/`Vytvoř` for younger family audience.
  - `máma` vs `maminka` — copy uses both (`máma dcera` and `maminky`); confirm naturalness.
  - `Sladěné` (matching/coordinated) is a strong, native Czech word — confirm strength is right.

### 2.14 `el-GR` reviewer brief
- **Target:** Greek (Greece). Source `landing_locale_evidence`: `Base English product URLs with country=GR passed product/cart/checkout presentment in EUR; native GR landing not proven`.
- **Product type:** matching family / mommy-and-me / daddy-and-me / pajama / swimwear.
- **Locale gotchas:**
  - Greek diacritics/accents (τόνοι): every accented vowel must read correctly (`μαμά`, `κόρη`, `μπαμπά`, `παιδί`, `πιτζάμες`, `μαγιό`, `οικογενειακές`).
  - `looks` (Latin-script English borrowing) is mixed into Greek text — confirm Greek e-comm acceptability vs replacing with `στυλ`/`σύνολα`.
  - `Ασορτί` is a French-derived loanword common in Greek fashion vocabulary — confirm.
  - Formal plural `Επιλέξτε`, `Συνδυάστε`, `Δημιουργήστε` — confirm formal register suits family-apparel customer.
  - Greek search behavior: confirm that `Φορέματα μαμά κόρη` matches how Greeks actually search vs preferring `μαμά και κόρη` or `μαμά-κόρη`.

---

## 3. Landing-language QA checklist (per locale)

For every locale, paid traffic must hit a country-qualified URL pattern (per `AGENTS.md`: bare `/es`, `/it`, `/ro`, `/pt` paths can default to US/USD; the `?country=XX` qualifier is required). The reviewer must walk the live storefront and confirm the listed spot-checks. **No write actions** — read-only walkthrough only.

Canonical URL pattern (replace `<HANDLE>` with the campaign's product handle):

- `es-ES` → `https://dresslikemommy.com/es/products/<HANDLE>?country=ES`
- `it-IT` → `https://dresslikemommy.com/it/products/<HANDLE>?country=IT`
- `pt-PT` → `https://dresslikemommy.com/pt/products/<HANDLE>?country=PT`
- `ro-RO` → `https://dresslikemommy.com/ro/products/<HANDLE>?country=RO`
- `de-DE` → `https://dresslikemommy.com/products/<HANDLE>?country=DE` (no proven `/de` localized path; reviewer must confirm whether `/de/...` or base path serves DE shoppers in DE)
- `nl-NL` → `https://dresslikemommy.com/products/<HANDLE>?country=NL` (no proven `/nl` localized path; confirm)
- `fr-FR` → `https://dresslikemommy.com/products/<HANDLE>?country=FR` (no proven `/fr` localized path; confirm)
- `fr-BE` → `https://dresslikemommy.com/products/<HANDLE>?country=BE` + locale `fr` (BE language split is a prerequisite — reviewer must confirm storefront actually serves fr-BE)
- `nl-BE` → `https://dresslikemommy.com/products/<HANDLE>?country=BE` + locale `nl` (BE language split prerequisite)
- `sv-SE` → `https://dresslikemommy.com/products/<HANDLE>?country=SE` (confirm any `/sv` path)
- `da-DK` → `https://dresslikemommy.com/products/<HANDLE>?country=DK`
- `pl-PL` → `https://dresslikemommy.com/products/<HANDLE>?country=PL`
- `cs-CZ` → `https://dresslikemommy.com/products/<HANDLE>?country=CZ`
- `el-GR` → `https://dresslikemommy.com/products/<HANDLE>?country=GR`

(For ES/IT/RO/PT the localized `/es|/it|/ro|/pt` paths are proven per `AGENTS.md` continuity; for DE/NL/FR/BE/SE/DK/PL/CZ/GR the storefront localization path is not proven and the reviewer must verify language quality on the page that actually loads.)

Per-locale spot-check checklist (reviewer marks PASS / FAIL / NOTE):

1. **Page loads in native language** — primary nav, footer nav, page chrome are in the locale's language (not English).
2. **PDP title** — matches the product handle's intended product type and reads natively (no translation artifacts, no Christmas/seasonal stale title; PT especially must not show `pt-BR` text).
3. **Price + currency** — currency symbol matches the locale's expected currency (ES/IT/PT/DE/NL/FR/BE/GR = EUR; RO = RON; SE = SEK; DK = DKK; PL = PLN; CZ = CZK; CH = CHF where applicable).
4. **ATC button label** — Add-to-cart button text is in native language.
5. **Cart drawer** — line item, subtotal, currency, and CTA labels in native language.
6. **Shipping country list / "Do we ship to my country?" modal** — reviewer's country is present; modal labels are in native language; per Phase 2 work this modal is searchable across `localization.available_countries`.
7. **Checkout language and currency** — opening checkout (without entering payment, without clicking Pay Now / Place Order, without creating an order) shows native language and the right currency. Reviewer must NOT submit payment.
8. **Shipping rates** — at least Standard and Express visible, with native-language labels and locale currency.
9. **Policy / page links** — `/policies/shipping-policy`, `/pages/shipping-info`, `/policies/refund-policy`, `/policies/privacy-policy`, `/policies/terms-of-service` open in native language; no English fallback; no stale "free local stock / warehouse / pickup" claims; PT must not serve `pt-BR`-only content where `pt-PT` is expected.
10. **Forbidden-claim sweep on the landing page** — no fast/rush shipping promises, no inflated review counts, no bestseller stamps, no countdown timers / fake urgency, no warehouse/local-stock claims.
11. **Mobile rendering** — page renders cleanly on mobile (paid traffic skews mobile); no overflow, no untranslated strings.
12. **Country-qualified URL persistence** — clicking from PDP to cart to checkout preserves the `?country=XX` selection and language; opening a fresh tab on the same URL produces the same locale.

PT-specific extra: explicitly confirm whether `/pt` path serves European Portuguese (`pt-PT`) or Brazilian Portuguese (`pt-BR`). If `pt-BR` is served on a Portugal-targeted page, **fail the locale** and report; native review for `pt-PT` ad copy is moot until storefront serves `pt-PT`.

BE-specific extra: the BE storefront must let the reviewer pick / confirm a French-Belgium or Dutch-Belgium experience. If the storefront only serves a generic `fr` or `nl` fallback, that is the BE split decision the owner must take before either `fr-BE` or `nl-BE` ad copy is used.

DE/NL/FR/SE/DK/PL/CZ/GR-specific extra: continuity evidence shows checkout currency/UI passed in `en-DE`, `en-NL`, `en-FR`, `en-SE`, `en-DK`, `en-PL`, `en-CZ`, `en-GR`. Reviewer must confirm whether a native-language landing path exists; if the page still serves English to a country-qualified URL, that is a landing-language gate even if checkout currency is correct.

---

## 4. Reviewer recruitment options (high level)

The owner can stage native review through any combination of the below; this list is high-level and does not endorse a specific brand.

1. **Professional translation/review services.** Pros: vetted native linguists, NDA, turnaround SLA, can deliver the per-locale brief above as a structured workflow. Cons: cost per locale × per word; copy here is short so cost is bounded. Best for: PT (because of pt-PT vs pt-BR risk), DE (Sie/du and Partnerlook calls), GR (script + diacritics + register).
2. **Vetted freelance marketplaces (general translation/copywriting).** Pros: per-locale specialist available within ~24–72h, lower cost. Cons: variance in quality, requires a screening test. Best for: smaller-scale Tier-3 locales (PL, CZ, RO, GR) where dialect risk is low and the copy is short.
3. **Marketing-localization agencies.** Pros: experience with paid-search character constraints and brand-voice handoff; can also do landing-language QA. Cons: highest unit cost. Best for: a one-shot wave covering all 14 locales if speed matters more than budget.
4. **In-network native speakers (community / customer base).** Pros: real customer voice, very low cost, fastest turnaround for early sanity checks. Cons: not formally accountable, no NDA, not appropriate for legal/policy text. Best for: a "smell test" before paying for formal review on Tier-2 locales (ES, IT) where the brand already has shopper signal.
5. **AI-assisted draft + native human review (the cheapest reviewable path).** Pros: keeps cost low while preserving native sign-off as the binding gate. Cons: only works if the human reviewer is empowered to reject the AI rewrite. The 14 locales already exist in this state — they are the "AI-drafted" half; the missing half is the human sign-off.

Operational recommendation: pair option 1 (professional service) for **PT** specifically (because of the storefront `pt-BR` risk) and one mid-tier option (option 2 or option 5) for the other 13 locales, using the per-row Y/N/REWRITE checklist in section 2 as the deliverable contract.

---

## 5. Approval-staging recommendation

Lane D economics from `2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md`:

- Target ROAS 650% → CPA target $10.77.
- Max CPC $0.15 → breakeven CVR 1.39%.
- Per-country smallest-future-spend-unit: $2/day, hard pause at $16 cumulative w/ 0 purchases (~106 clicks at $0.15 CPC, ~8 elapsed days at the daily cap).
- First approved live enable per market activation scorecard is **GB / Mommy & Me Dresses — Exact only**, English; non-US locales remain paused.

CPC discovery vs review-cost trade-off:

- A locale where review costs (say) $200 of human time but the per-country live test cap is only $16 cumulative before hard-pause means review cost can dwarf the discovery spend if review is bought per locale up-front.
- Conversely, batching review into one wave is cheaper per locale, but staging market activation requires review evidence per market before that market's traffic can convert without language friction.
- The first paused→enabled escalation candidates are GB/CA/AU (English-first), so localized review is **not on the critical path** for the first enablement. Localized review unblocks the second wave (Tier-2 and beyond).

**Recommendation: stage native review by tier, in this order, but do all reviews in pre-paid batches to avoid review-cost-per-locale drag while keeping operator decisions sequential.**

- **Tier 2 first batch (highest expected economic value, already had checkout/landing evidence):** `es-ES`, `it-IT`, `ro-RO`, `pt-PT`. Within Tier 2, prioritize `pt-PT` because its review unblocks both ad copy AND a known storefront `pt-BR` risk. Then `es-ES` and `it-IT` (already proven `/es` and `/it` paths and EUR/RO checkout). Then `ro-RO` (RON economics caveat is a separate gate).
- **Tier 2/3 mid batch (checkout passed but native landing not proven; high commercial value):** `de-DE`, `fr-FR`, `nl-NL`. These three move fastest if landing-language QA is run alongside copy review (the QA work doubles for both gates).
- **Tier 3 batch:** `sv-SE`, `da-DK`, `pl-PL`, `cs-CZ`, `el-GR`. Lower expected per-click conversion certainty; review can be lower-cost (community + lightweight professional) because rewrite stakes are lower.
- **Special-case batch:** `fr-BE`, `nl-BE`. Do not commission Belgian-specific review until the owner takes the Belgium FR/NL split decision (per source `review_reason`). Until that decision, fr-BE rides on fr-FR review and nl-BE rides on nl-NL review for "concept-acceptability" only — not for market enablement.

Rationale tied to economics: at $16 cumulative pause-spend per ad group, the live discovery budget is bounded, so review investment must scale to expected lifetime spend per market, not the first-test spend. Tier 2 markets have the highest expected lifetime spend if they convert at the breakeven CVR (1.39% at $0.15 CPC), so they justify deeper review. Tier 3 markets justify lighter, batched review because the path to material spend is longer and more dependent on cheap-CPC discovery economics.

The owner-staged approval should approve **per locale** (not bulk) so a failed review in one locale (e.g., PT pt-BR mismatch) does not contaminate the others' enablement decision.

---

## 6. What "passed native review" looks like — closing criteria per locale

For `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE` to move from `PARTIALLY_MITIGATED_LOCAL_OPTIONS_READY__OWNER_DECISION_REQUIRED` to `SOLVED_READBACK_PASSED` **for a specific locale**, all of the following must be true and evidenced in the lane folder:

1. **Native reviewer sign-off on every row.** A named native reviewer (or named service) has answered Y/N/REWRITE for every headline option and every description option across all 5 themes, has accepted or rewritten each row, and the final accepted set continues to satisfy the existing validation: 0 length violations (≤30 char headlines, ≤90 char descriptions) and 0 forbidden-claim hits.
2. **Landing-language QA passed.** A reviewer walked the live storefront on the locale's country-qualified URL pattern (section 3) and marked PASS on items 1–12 above (with appropriate special-case notes for PT, BE, DE/NL/FR/SE/DK/PL/CZ/GR landing paths). No payment, no Pay Now / Place Order click, no order creation. Slow probes only — no rapid curls per `AGENTS.md` rate-limit guidance.
3. **Belgium split resolved (BE locales only).** For `fr-BE` and `nl-BE`, the owner has explicitly recorded the Belgium FR/NL split decision before sign-off counts.
4. **Portugal storefront resolved (`pt-PT` only).** Either the `/pt` path serves `pt-PT` content (storefront translation work confirmed) OR the owner explicitly accepts using `pt-PT` ad copy against `pt-BR` storefront content; the second option is documented as a known mismatch and re-tested before any spend escalation.
5. **Final-set artifacts written.** A locked, dated CSV per locale (e.g., `native_language_rsa_options_FINAL_<locale>.csv`) is committed under the lane's audit folder, with a short approval log naming the reviewer and date.
6. **No live-write side effects during review.** No campaigns enabled, no Ads import, no Merchant change, no Pinterest write, no Shopify Admin or theme write. The smallest-future-spend-unit (GB / Mommy & Me Dresses — Exact only, English) remains the first enablement candidate; localized enablement is approved separately, per locale, after sign-off.
7. **Tracker updated.** `ops/PROBLEM_TRACKER.md` reflects the locale moving to `SOLVED_READBACK_PASSED` with citation to the final CSV and the landing-QA report. Parent integrates this row.

When all 14 locales meet the above, the umbrella problem moves from `PARTIALLY_MITIGATED` to `SOLVED_READBACK_PASSED`. Until then, individual locales can be marked `SOLVED_READBACK_PASSED` independently (per locale) without unblocking the umbrella state — useful because Tier-2 markets can ship review well before Tier-3.

---

## 7. Files touched

- Created: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md`

No other files modified. No browser, network, Shopify Admin, Google Ads, Merchant Center, Pinterest, GA4, theme, payment, order, feed, or conversion-goal write was performed by this lane.
