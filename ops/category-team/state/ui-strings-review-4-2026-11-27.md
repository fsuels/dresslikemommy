# Interface strings review 4: Swedish, Dutch, Polish, full interface (2026-11-27)

This unit wrote changes and released them; it was not read-only. I hand-read each of the 802 in-scope leaves (the 1005 English keys minus the 203 `sections.collection_seo.*`) in `locales/sv.json`, `nl.json` and `pl.json` against `locales/en.default.json` at origin/main 07ba1d6. Polish also has 24 extra plural leaves (`few`/`many`). I used the same method as reviews 1–3.

Changed keys: sv 87, nl 87, pl 113 (287 in total), released in 6 rounds of at most 20 keys per file.

The product-page copy map (`snippets/product-page-copy-map.liquid`) was refreshed for the sv, nl and pl blocks only. Running `build_product_page_copy_map.py` in full would have reverted hand edits that other locales (de, es, fr, hr, hu, id, it, lt, pt, ro) have in the map, so I used a partial rebuild that reads the map, replaces the three locales and writes it back.

## Scope and rules

- **Not touched:** all `sections.collection_seo.*` keys (collection H1s, intros, guides and meta, which belong to the Experto SEO session); the category-name keys (`cat_mommy_me`, `cat_daddy_me`, `home_category_copy.mommy_me/daddy_me`, `within_mommy_me/daddy_me`); `storefront.home_title` and `home_description` (head meta); pt-BR and pt-PT; and the unused `breadcrumbs.prefix_*` keys.
- **Register:** sv uses du and nl uses je throughout. pl uses Ty imperatives (the file's existing style), and I removed one gendered form (`złożyłeś(-aś)`).
- **Truth:** every "free" claim became "included". Warehouse and stock wording became neutral: pl "W magazynie" is now "Dostępny" and "Niski poziom zapasów" is now "Ostatnie sztuki"; sv "Låg lagernivå" is now "Få i lager". I removed newness claims the English no longer makes ("Nyaste ankomsterna", "Najnowsze przybycia" where the English says "Mommy and Me pajama sets"). Nothing was added that the English does not say.
- **Placeholders and HTML:** a script confirmed that `{{ }}` variables, tags and `[code]` are identical to the English for all 287 values. `ceo_worktree check` passed in every round.

## Swedish (sv): 87 keys

By area: product page 31, cart 3, search/filter 10, header/menu/home/collection UI 25, journal/article 9, account 4, aria/blog/forms 5.

| Key | Before | After |
|---|---|---|
| `products.product.free_shipping_short` | Fri frakt | Standardfrakt ingår |
| `products.additional_info.return_policy_line_3` | …badkläder och närbesvär… slutförsäljning och personliga föremål… | …badkläder och underkläder…; varor som sålts utan returrätt och personligt anpassade varor är också undantagna. |
| `products.additional_info.return_policy_line_1` | Du har 30 dagar på dig från leverans på dig att… | Du har 30 dagar på dig från leveransen att begära retur eller byte. |
| `products.additional_info.secure_logistics_title` | Säker logistik | Hjälp med frakt |
| `sections.product_navigation.back_to_family_sets` | Tillbaka till familjen Set | Tillbaka till familjeset |
| `storefront.journal.shop_family_swim` | Shoppa familjen simma | Handla familjebadkläder |
| `storefront.callout.new_matching_outfits.callout_eyebrow` | Färska ankomster | Nyheter |
| `templates.search.results_with_count_and_term.one` | hittat {{ count }} resultat för "{{ terms }}" | {{ count }} resultat hittades för ”{{ terms }}” |

Also changed: SKU "Lagerhållningsenhet" is now "Artikelnummer"; "Skatt ingår" is now "Moms ingår"; height uses "Längd"; "kvantitet" and "samling/produktserie" are now "antal" and "kollektion"; "nyanlända" (which reads as newly arrived people) is now "nyheter"; "Plocka för kallt väder" is now "Utvalt för kallt väder"; "mamma och mig" is now "mamma och barn"; maternity uses "Gravidkläder" (it was "Moderskap", motherhood); and the order status "Distributionsstatus" is now "Leveransstatus".

## Dutch (nl): 87 keys

By area: product page 34, cart 2, search/filter 5, header/menu/home/collection UI 29, journal/article 6, account 4, aria/blog/forms 7.

| Key | Before | After |
|---|---|---|
| `products.facets.product_count.other` | {{ product_count }} korting op {{ count }} producten | {{ product_count }} van {{ count }} producten |
| `products.product.free_shipping_short` | Gratis verzending | Standaardverzending inbegrepen |
| `products.additional_info.return_policy_line_1` | Vanaf de levering heeft u 30 dagen… een ​​retour (zero-width chars) | Je hebt vanaf de levering 30 dagen de tijd om een retour of omruiling aan te vragen. |
| `products.additional_info.return_policy_line_3` | …badkleding en intimi… definitieve verkoop… | …badkleding en ondergoed…; artikelen zonder retourrecht en gepersonaliseerde artikelen zijn ook uitgesloten. |
| `products.additional_info.shopping_security_title` | Winkelbeveiliging | Veilig winkelen |
| `customer.order.fulfilled_at_html` | Voldaan {{ date }} (means "paid") | Verzonden {{ date }} |
| `storefront.journal.shop_family_swim` | Familiezwemmen kopen | Familiebadkleding kopen |
| `storefront.callout.pajamas.secondary_label` | Nieuwste aankomsten | Pyjamasets voor moeder en kind |

Also changed: "gallery-weergave" is now "galerijweergave"; "Shop op categorie" is now "Shop per categorie"; "Winkel sneller" is now "Sneller shoppen"; "matchende" is now "bijpassende"; the remaining u-forms became je; "Inloggegevens" (the login page title) is now "Inloggen"; "Moederschap" and "Paren" are now "Zwangerschapskleding" and "Koppels"; "nieuwkomers" is now "nieuwe items" or "nieuw binnen"; and "Dit artikelen delen" is now "Dit artikel delen".

## Polish (pl): 113 keys

By area: product page 33, cart 2, search/filter 24, header/menu/home/collection UI 30, journal/article 10, account 3, aria/blog/forms 11.

| Key | Before | After |
|---|---|---|
| `products.additional_info.return_policy_line_3` | …również nie są objęte promocją (= not covered by the promotion) | …; wyłączone są również produkty sprzedawane bez możliwości zwrotu oraz produkty personalizowane. |
| `products.product.free_shipping_short` | Darmowa wysyłka | Standardowa wysyłka w cenie |
| `products.product.inventory_in_stock` | W magazynie | Dostępny |
| `products.facets.product_count_simple.few` | {{ count }} produkty(-ów) | {{ count }} produkty (many: produktów, other: produktu) |
| `sections.home_category_copy.matching_dresses` | Dopasowane sukienki (= fitted dresses) | Pasujące sukienki |
| `storefront.journal.shop_family_swim` | Kupuj rodzinne kąpiele (= family baths) | Kupuj rodzinne stroje kąpielowe |
| `storefront.callout.new_matching_outfits.callout_eyebrow` | Świeże przyjazdy | Nowości |
| `templates.search.no_results` | …dla “{{ terms }}”… | …dla „{{ terms }}”… |

Also changed: complete one/few/many/other forms for the search results, search results with term, products, pages, suggestions and blog comments, which replaces the `(-ów)` / `(y)` placeholder text; "Dopasowane" in the sense of matching is now "Pasujące" on home, menu, callouts and article; "Bezpieczna logistyka" is now "Pomoc w sprawie wysyłki"; "Nazwa" (name field) is now "Imię"; the password button "Enter" is now "Wejdź"; and "Macierzyństwo" is now "Odzież ciążowa".

## Commits and release

| Round | Commit | Keys |
|---|---|---|
| 1 | 34827ee | sv 20, nl 20, pl 20 |
| 2 | e915b05 | sv 20, nl 20, pl 20 |
| 3 | 9d6517d | sv 20, nl 20, pl 20 |
| 4 | c69335d | sv 20, nl 20, pl 20 |
| 5 | a69b329 | sv 7, nl 7, pl 20 |
| 6 | d75d46b | pl 13 |

Every commit went through `ceo_worktree.py commit`, followed by `sync-locales --apply`. In rounds 1 and 2, `sync-theme --apply` also pushed the copy-map snippet, which the GitHub sync had not delivered.

After each round I waited 60 s (from round 3 on, held the lock for 3 minutes), fetched, and compared every value with origin/main. The result was 0 mismatches after every Shopify "Update from Shopify" commit. The final check at origin/main 296f857 found all 287 values present, `sync-locales` in sync and `sync-theme` showing 0 files different. No value was reverted.

**THEME_LOCK incidents:**
- At 07:04Z and 07:16Z, collection-copy-4 overwrote my lock while I held it. My values survived both times, and I did not delete their lock.
- At 07:10Z my write raced with pdp-perf's. I backed off.
- In round 4, `sync-locales --apply` also upserted da, fi, no and pt-BR (1–2 collection keys each). That made live equal to origin/main, where collection-copy-4 had restored those values in 49fe1ff.

## Live readback (built-in browser, 6 loads after 07:32Z, at least 10 s apart, no 429 or 403)

- **`/sv/products/nordic-yoke-family-matching-sweaters` and `/sv/cart`:** "Standardfrakt ingår" is shown, and the new titles are present in the page and copy map ("Hjälp med frakt", "Trygg handel", "Tillbaka till familjeset"). No "Fri frakt", "Låg lagernivå" or missing translations.
- **`/nl/...` and `/nl/cart`:** "Standaardverzending inbegrepen" and "Maatgids en pasvorm" are shown. No "Gratis", "intimi", "heeft u" or "gallery-weergave". The only "korting op" left is the real promo line.
- **`/pl/...` and `/pl/cart`:** "Standardowa wysyłka w cenie" and "30 dni na zwrot" are shown. No "Darmowa", "W magazynie", "nie są objęte promocją" or plural placeholders.

**Still wrong on live, outside the theme locale files:** the top menu is translated in Shopify Admin. nl shows "WINKEL", "NIEUWE AANKOMSTEN", "PAREN" and "MOEDERSCHAP"; pl shows "SKLEP", "NOWE PRZYJAZDY" (a calque that reads as arrivals of people) and "MACIERZYŃSTWO". Better wording would be: nl "Nieuw binnen", "Koppels", "Zwangerschapskleding"; pl "Nowości", "Odzież ciążowa". The owner of the menu translations needs to fix these.

## English defects found (English not edited)

1. `products.product.inventory_in_stock`, `inventory_low_stock(_show_count)` ("In stock", "Low stock: N left") are stock claims for a dropshipping store. Check whether the theme ever shows them.
2. `gift_cards.issued.how_to_use_gift_card` says "QR code in-store", which implies a physical store. This is Dawn's default text.
3. `products.product.review_thanks_note` ("10% thank-you code with their order") is a promotional claim. Confirm it is still true.
4. `products.additional_info.safe_payment_description` ("never shared with our partners", "manage your saved cards anytime") makes payment claims. Card data is shared with the payment processor, and saved-card management may not exist.
5. The newness wording "Fresh arrivals", "New arrivals" and "New pajama drop" (callout and menu) is true only while those collections hold recent pieces.
6. `storefront.callout.pajamas.callout_title` and `secondary_label` changed meaning in English (now Mommy and Me pajama sets); the three translations still said "newest arrivals" (fixed).
7. `sections.breadcrumbs.prefix_*` keys are not used by any snippet (dead keys); the sv/nl/pl values ("Motsvarande", "Dopasowanie") are wrong but harmless.
