# Interface strings review: product page to checkout link, six languages (2026-11-27)

Read-only unit (Experto SEO). Theme read from `origin/main` (86e7de6). Counts: locale-file rows de 43, es 28, fr 38, cs 28, ro 65, it 23 = 225; inline rows (strings hard-coded in liquid/JS, not in locale files) de 7, es 3, fr 0, cs 3, ro 21, it 3 = 37.

Files: machine file `ops/organic/receipts/2026-11-27/ui-strings/proposed.json` ({locale: {key: new_value}}, locale files only; `it` is gated, see below); `proposed-inline.json` (same folder, keys are `file::variable`, for the strings that live in liquid/JS). Nothing was applied.

## What was checked

- Key list: the closure of snippets rendered by `main-product`, `cart-drawer`, `main-cart-items`, `main-cart-footer`, header, announcement bar, buy buttons, variant picker, size-guide, delivery/Christmas, purchase-confidence, policy modals and shipping-country modal gave 273 locale leaves actually referenced (178 on the purchase path after dropping social links, slider/slideshow, quick-order, gift-card, media a11y, volume pricing, journal). Dynamic keys: none found (`cart_count` is the only plural; `few`/`many` matter for cs and ro). Strings that do NOT come from locale files: per-language tables inside `dlm-complete-family`, `cart-item-add-member`, `automatic-discount-promo`, `discount-title`, `dlm-delivery-vary-copy`, `main-cart-footer`/`cart-drawer` tax and shipping-details lines, and the PDP builder tables in `assets/product-desktop-ux-20260513-ruler-sync.js`. These were reviewed too (inline rows).
- Rendered check, 24 of 24 storefront requests used, no 429: `/{de,es,fr,cs,ro,it}/products/nordic-yoke-family-matching-sweaters` (x6), `/{locale}/cart/add.js` (x6, one item), `/{locale}/cart` (x6) and `/{locale}/products/...?sections=cart-drawer` (x6). All six languages render the cart page, cart drawer, sticky checkout bar markup, trust rows, announcement bar, delivery lines, size-guide labels and the "Complete the family" module in the target language.
- Raw keys: none seen. English on a translated page: none in the rendered sample. Two latent cases: (1) `it.json` has no `products.additional_info.christmas_order_by_other`, so the Italian page falls back to the English sentence wherever the Christmas banner shows for non-US countries (the sample was a US-geo session so it did not show); (2) the English source mixes "cart" and "bag" in inline strings ("Only 1 piece in your bag", "Add this piece to bag", "Could not add to bag"), while all six translations say cart, so no translation fix is needed, only an English-side note.
- Caveats: the sample ran as a US session (USD, "Standard shipping included (United States)"), so country-specific copy for DE/ES/FR/CZ/RO/IT markets (EUR, other `shipping_country` lines) was judged from the locale files, not rendered. The first drawer fetch via `add.js` without `sections_url` came back in English; that is a test artefact (theme JS always passes `sections_url`, and the later `?sections=cart-drawer` fetch rendered every language correctly). The long shipping-policy text printed inside the cart page is the legal policy page, not interface, and was not reviewed.
- Judgment standard: native shopper reading the English next to it; one register per language, matching the hand-written descriptions of this week (de Sie, es tú, fr vous, cs vykání, ro polite plural, it tu). Claims: where a translation says "free/gratis/zdarma/kostenlos" and the English says "included", it was reverted to "included" (the shop does not claim free shipping, shipping is in the price).

Order inside each table: most visible first (rank 1 = buttons and primary labels, 2 = cart lines, promos and delivery, 3 = trust rows, 4 = size chart and modals, 5 = rare errors and accessibility text). Rank is in the first column.

## German (de)

Rows: 43 locale-file + 7 inline.

### Locale-file keys (`locales/de.json`)

| Rank | Key | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 1 | `general.continue_shopping` | Continue shopping | Weiter shoppen | "shoppen" is slang | Weiter einkaufen |
| 1 | `products.product.matching_set.add` | Add matching pieces | Ausgewählte Stücke in den Warenkorb legen | "Stücke" vs "Teile" elsewhere | Ausgewählte Teile in den Warenkorb legen |
| 1 | `products.product.matching_set.copy` | Pick a size for each person. Priced per piece. | Wähle für jede Person eine Größe. Preis pro Teil. | du-form | Wählen Sie für jede Person eine Größe. Preis pro Teil. |
| 1 | `products.product.matching_set.copy_person` | Pick a size for each person. | Wähle für jede Person eine Größe. | du-form | Wählen Sie für jede Person eine Größe. |
| 1 | `products.product.matching_set.heading` | Build your matching set | Stelle dein passendes Set zusammen | du-form | Stellen Sie Ihr passendes Set zusammen |
| 1 | `products.product.size_required_message` | Please select a size before adding to cart. | Bitte wählen Sie eine Größe aus, bevor Sie sie in den Warenkorb legen. | "sie" is ambiguous (the size? the item?) | Bitte wählen Sie eine Größe, bevor Sie den Artikel in den Warenkorb legen. |
| 1 | `sections.cart.checkout` | Check out | Auschecken | "Auschecken" is not a German shopping term (literal "check out"); main cart and sticky-bar button | Zur Kasse |
| 1 | `sections.cart.empty` | Your cart is empty | Dein Warenkorb ist leer | du-form | Ihr Warenkorb ist leer |
| 1 | `sections.cart.title` | Your cart | Dein Warenkorb | du-form; descriptions and most policy text use Sie | Ihr Warenkorb |
| 2 | `customer.log_in` | Log in | Einloggen | "Einloggen" is colloquial; "Anmelden" is the standard shop term | Anmelden |
| 2 | `products.additional_info.christmas_order_by` | Estimate: order by {{ order_date }} to arrive by {{ arrive_date }}. Not a guarantee. | Schätzung: bestelle bis {{ order_date }}, damit es bis {{ arrive_date }} ankommt. Keine Garantie. | du-form | Schätzung: Bestellen Sie bis {{ order_date }}, damit die Lieferung bis {{ arrive_date }} ankommt. Keine Garantie. |
| 2 | `products.additional_info.christmas_order_by_other` | Ordering for Christmas? Delivery times vary by country, so order as early as you can. | Bestellung für Weihnachten? Die Lieferzeiten unterscheiden sich je nach Land, bestellen Sie daher so früh wie möglich. | comma splice, "Bestellung für Weihnachten?" is a noun phrase | Bestellen Sie für Weihnachten? Die Lieferzeiten unterscheiden sich je nach Land – bestellen Sie daher so früh wie möglich. |
| 2 | `products.additional_info.free_shipping_label` | Standard shipping included | Kostenloser Standardversand inklusive | "Kostenloser ... inklusive" is redundant and adds "free", which the English avoids | Standardversand inklusive |
| 2 | `products.product.quantity.decrease` | Decrease quantity for {{ product }} | Verringere die Menge für {{ product }} | du-form | Menge für {{ product }} verringern |
| 2 | `products.product.quantity.increase` | Increase quantity for {{ product }} | Erhöhe die Menge für {{ product }} | du-form | Menge für {{ product }} erhöhen |
| 2 | `sections.announcements.default_promo` | BUY 2, GET A 3RD PIECE 20% OFF \| STANDARD SHIPPING INCLUDED \| SECURE CHECKOUT | KAUFE 2, ERHALTE 20 % RABATT AUF DAS 3. TEIL \| STANDARDVERSAND INKLUSIVE \| SICHERER CHECKOUT | du-imperative in caps; cart says "2 kaufen, 3. Teil 20 % günstiger" | 2 KAUFEN, 3. TEIL 20 % GÜNSTIGER \| STANDARDVERSAND INKLUSIVE \| SICHERER CHECKOUT |
| 2 | `sections.announcements.shipping_country_promo` | BUY 2, GET A 3RD PIECE 20% OFF \| STANDARD SHIPPING INCLUDED TO {{ country }} \| SECURE CHECKOUT | KAUFE 2, ERHALTE 20 % RABATT AUF DAS 3. TEIL \| STANDARDVERSAND INKLUSIVE ({{ country }}) \| SICHERER CHECKOUT | same | 2 KAUFEN, 3. TEIL 20 % GÜNSTIGER \| STANDARDVERSAND INKLUSIVE ({{ country }}) \| SICHERER CHECKOUT |
| 2 | `sections.cart.estimated_total` | Estimated total | Geschätzte Gesamtkosten | "Gesamtkosten" reads as cost to the shop; standard is Gesamtsumme | Geschätzte Gesamtsumme |
| 2 | `sections.cart.login.paragraph_html` | <a href="{{ link }}" class="link underlined-link">Log in</a> to check out faster. | <a href="{{ link }}" class="link underlined-link">Logge dich ein</a>, damit es beim Checkout schneller geht. | du-form, "Checkout" as a loanword next to the "Zur Kasse" button | <a href="{{ link }}" class="link underlined-link">Melden Sie sich an</a>, um schneller zur Kasse zu gehen. |
| 2 | `sections.cart.login.title` | Have an account? | Hast du ein Konto? | du-form | Haben Sie ein Konto? |
| 2 | `sections.cart.new_estimated_total` | New estimated total | Neuer geschätzter Gesamtbetrag | same term fix | Neue geschätzte Gesamtsumme |
| 2 | `sections.cart.note` | Order special instructions | Spezielle Bestellanweisungen | "Spezielle Bestellanweisungen" is a calque | Anmerkungen zur Bestellung |
| 2 | `sections.home_category_copy.heading_category` | Shop by Category | Nach Kategorie shoppen | "shoppen" slang, matches the fix to continue_shopping | Nach Kategorie stöbern |
| 3 | `products.purchase_confidence.shipping_headline` | Standard shipping included | Kostenloser Standardversand | adds "Kostenloser" (free); English says included | Standardversand inklusive |
| 3 | `products.purchase_confidence.ships_to_default` | Ships to your country | Versand in dein Land | du-form | Versand in Ihr Land |
| 3 | `products.trust.free_shipping` | Standard shipping included | Kostenloser Standardversand inklusive | same: "Kostenloser ... inklusive" | Standardversand inklusive |
| 3 | `sections.cart.trust.secure` | Secure | Sicher | one word "Sicher" alone is unclear in the drawer trust row | Sicher bezahlen |
| 4 | `products.additional_info.flat_chest_note` | Chest/bust numbers in this size chart are measured flat across the garment. Double them to get the measurement all the way around. | Die Brustmaße in dieser Größentabelle sind flach über das Kleidungsstück gemessen. Verdopple sie, um den vollen Umfang zu erhalten. | du-form "Verdopple sie" | Die Brustmaße in dieser Größentabelle sind flach über das Kleidungsstück gemessen. Verdoppeln Sie die Werte, um den vollen Umfang zu erhalten. |
| 4 | `products.additional_info.secure_logistics_line_2` | Use your order tracking link for the latest carrier updates. International orders may be subject to local taxes, duties, or customs fees collected by the carrier or local authority. | Verwenden Sie Ihren Bestellverfolgungslink, um die neuesten Updates zu den Versanddienstleistern zu erhalten. Für internationale Bestellungen können lokale Steuern, Zölle oder Zollgebühren anfallen, die vom Spediteur oder der örtlichen Behörde erhoben werden. | "Updates zu den Versanddienstleistern", "Spediteur", "Zölle oder Zollgebühren" duplicated | Nutzen Sie den Sendungsverfolgungslink Ihrer Bestellung für aktuelle Informationen des Versanddienstleisters. Bei internationalen Bestellungen können lokale Steuern, Zölle oder Zollgebühren anfallen, die vom Versanddienstleister oder der örtlichen Behörde erhoben werden. |
| 4 | `products.product.size_guide.chart_units` | Size chart units | Größentabelle-Einheiten | "Größentabelle-Einheiten" is a hyphen compound calque | Einheiten der Größentabelle |
| 4 | `products.purchase_confidence.returns_eligible` | Eligible items must be unworn, unwashed, and returned with tags attached. | Berechtigte Artikel müssen ungetragen, ungewaschen und mit befestigten Etiketten zurückgegeben werden. | "befestigten Etiketten" (fastened) unnatural | Berechtigte Artikel müssen ungetragen, ungewaschen und mit angebrachten Etiketten zurückgegeben werden. |
| 4 | `products.purchase_confidence.returns_exclusions` | Swimwear, intimate items, final-sale items, and gift cards are excluded. See the full return policy for eligibility and exceptions. | Bademode, Unterwäsche, als vom Umtausch ausgeschlossen verkaufte Artikel und Geschenkkarten sind ausgeschlossen. Bedingungen und Ausnahmen finden Sie in der vollständigen Rückgaberichtlinie. | "als vom Umtausch ausgeschlossen verkaufte Artikel ... ausgeschlossen" is garbled (final-sale) and repeats "ausgeschlossen" | Bademode, Unterwäsche, als „Final Sale“ gekennzeichnete Artikel und Geschenkkarten sind ausgeschlossen. Bedingungen und Ausnahmen finden Sie in der vollständigen Rückgaberichtlinie. |
| 4 | `products.purchase_confidence.security_details_body` | Payments are encrypted and processed securely by our payment providers. We do not store your full card number. | Zahlungen sind verschlüsselt und werden sicher von unseren Zahlungsanbietern verarbeitet. Wir speichern deine vollständige Kartennummer nicht. | du-form "deine" among Sie lines | Zahlungen sind verschlüsselt und werden sicher von unseren Zahlungsanbietern verarbeitet. Wir speichern Ihre vollständige Kartennummer nicht. |
| 4 | `products.shipping_country.checker_current_country` | Your current country selection is {{ country }}. | Deine aktuelle Länderauswahl ist {{ country }}. | du-form | Ihre aktuelle Länderauswahl ist {{ country }}. |
| 4 | `products.shipping_country.checker_no_results` | No matching country found in the current checkout list. Try another spelling or email us before ordering. | Kein passendes Land in der aktuellen Checkout-Liste gefunden. Versuche eine andere Schreibweise oder schreibe uns vor der Bestellung. | du-form | Kein passendes Land in der aktuellen Checkout-Liste gefunden. Versuchen Sie eine andere Schreibweise oder schreiben Sie uns vor der Bestellung. |
| 4 | `products.shipping_country.checker_summary` | Yes if your country appears below. These {{ count }} countries and regions are enabled in checkout right now. | Ja, wenn dein Land unten angezeigt wird. Diese {{ count }} Länder und Regionen sind derzeit im Checkout aktiviert. | du-form | Ja, wenn Ihr Land unten angezeigt wird. Diese {{ count }} Länder und Regionen sind derzeit im Checkout aktiviert. |
| 4 | `storefront.privacy_modal.line_3_html` | Dress Like Mommy <strong>does not store your full card number</strong>. | Dress Like Mommy <strong>speichert nicht Ihre vollständige Kartennummer</strong>. | word order: "speichert nicht Ihre ..." | Dress Like Mommy <strong>speichert Ihre vollständige Kartennummer nicht</strong>. |
| 5 | `products.product.inventory_low_stock` | Low stock | Niedriger Lagerbestand | "Niedriger Lagerbestand" is a warehouse term | Nur noch wenige verfügbar |
| 5 | `products.product.inventory_low_stock_show_count` | Low stock: {{ quantity }} left | Niedriger Lagerbestand: {{ quantity }} verbleibend | same plus "verbleibend" | Nur noch {{ quantity }} verfügbar |
| 5 | `products.product.matching_set.empty` | Choose at least one size to add your set. | Wählen Sie für jedes Familienmitglied, das Sie hinzufügen möchten, eine Größe aus. | does not match English (at least one size); long | Wählen Sie mindestens eine Größe, um Ihr Set hinzuzufügen. |
| 5 | `products.product.matching_set.success` | Matching set added to cart. | Passendes Set zum Warenkorb hinzugefügt. | "zum Warenkorb hinzugefügt" mixes with "in den Warenkorb legen" | Passendes Set in den Warenkorb gelegt. |
| 5 | `sections.cart.cart_error` | There was an error while updating your cart. Please try again. | Beim Aktualisieren deines Warenkorbs ist ein Fehler aufgetreten. Bitte versuche es erneut. | du-form, stiff | Ihr Warenkorb konnte nicht aktualisiert werden. Bitte versuchen Sie es erneut. |
| 5 | `sections.cart.cart_quantity_error_html` | You can only add {{ quantity }} of this item to your cart. | Du kannst deinem Warenkorb nur {{ quantity }} Stück dieses Artikels hinzufügen. | du-form, clumsy | Sie können nur {{ quantity }} Stück dieses Artikels in den Warenkorb legen. |

### Inline strings (not in locale files)

| Rank | Where | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.addCurrentPiece` | Add this piece to bag | Dieses Teil in den Warenkorb | button lacks the verb ("legen") | Dieses Teil in den Warenkorb legen |
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.chooseOptionsStep` | Choose size and options | Wähle Größe und Optionen | du-form | Wählen Sie Größe und Optionen |
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.chooseRoleCta` | Choose a family member | Wähle ein Familienmitglied | du-form | Familienmitglied wählen |
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.chooseRoleStep` | Choose who this piece is for | Wähle, für wen dieses Teil ist | du-form | Wählen Sie, für wen dieses Teil ist |
| 2 | `snippets/dlm-complete-family.liquid::t_error` | Could not add to bag. Please try again. | Konnte nicht in den Warenkorb gelegt werden. Bitte versuche es erneut. | tu-form "versuche" in a Sie context | Konnte nicht in den Warenkorb gelegt werden. Bitte versuchen Sie es erneut. |
| 2 | `snippets/dlm-complete-family.liquid::t_single` | Only 1 piece in your bag. | Nur 1 Teil in deinem Warenkorb. | du-form "deinem" | Nur 1 Teil in Ihrem Warenkorb. |
| 2 | `snippets/dlm-complete-family.liquid::t_single_hint` | It's for one person. To match, add family members below. | Es ist für eine Person. Für den Familienlook unten weitere hinzufügen. | telegraphic infinitive, unclear what "Es" refers to | Dieses Teil ist für eine Person. Für den Partnerlook fügen Sie unten weitere Familienmitglieder hinzu. |

### Terms to standardise

| Term | Recommendation |
|---|---|
| Register | Sie everywhere (descriptions, policies and the purchase-confidence lines already use Sie). Remove every du-form: Dein/Wähle/Logge dich ein/Hast du. |
| cart | Warenkorb (keep). Possessive: "Ihr Warenkorb". |
| checkout (button) | Zur Kasse. "Checkout" stays only in the trust label "Sicherer Checkout". Never "Auschecken". |
| size | Größe; table = Größentabelle. |
| add to cart | In den Warenkorb legen (keep). |
| sold out | Ausverkauft (keep). |
| free shipping | "Standardversand inklusive" (matches English "included"); do not add "Kostenloser". |
| total | Gesamtsumme (not Gesamtkosten/Gesamtbetrag). |
| piece | Teil (not Stück/Stücke). |

## Spanish (es)

Rows: 28 locale-file + 3 inline.

### Locale-file keys (`locales/es.json`)

| Rank | Key | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 1 | `products.product.add_to_cart` | Add to cart | Agregar al carrito | "Agregar" (Latin America) while the cart, builder and promos use "Añadir" | Añadir al carrito |
| 1 | `products.product.size_required_message` | Please select a size before adding to cart. | Por favor selecciona una talla antes de añadir al carrito. | "Por favor" calque | Selecciona una talla antes de añadir al carrito. |
| 1 | `sections.cart.checkout` | Check out | Pagar pedido | "Pagar pedido" differs from "al finalizar la compra" used in the tax line; unify on one term | Finalizar compra |
| 1 | `sections.cart.empty` | Your cart is empty | Tu carrito esta vacío | typo: "esta" without accent | Tu carrito está vacío |
| 2 | `general.cart.item_added` | Item added to your cart | Artículo agregado a tu carrito | "agregado" vs "Añadir" elsewhere | Artículo añadido a tu carrito |
| 2 | `products.additional_info.free_shipping_label` | Standard shipping included | Envío estándar gratuito incluido | "gratuito incluido" redundant; adds "free" | Envío estándar incluido |
| 2 | `products.product.include_taxes` | Tax included. | Impuesto incluido. | singular; cart line says "Impuestos incluidos." | Impuestos incluidos. |
| 2 | `sections.cart.recently_viewed` | Recently Viewed | Visto recientemente | singular for a list of items | Vistos recientemente |
| 2 | `sections.cart.savings_html` | You're saving <strong>{{ amount }}</strong> | Estas guardando <strong>{{ amount }}</strong> | "Estas guardando" means storing, not saving money | Estás ahorrando <strong>{{ amount }}</strong> |
| 3 | `products.purchase_confidence.shipping_headline` | Standard shipping included | Envío estándar gratis | "gratis" adds a claim the English avoids | Envío estándar incluido |
| 3 | `products.trust.free_shipping` | Standard shipping included | Envío estándar gratuito incluido | same | Envío estándar incluido |
| 3 | `sections.cart.trust.secure` | Secure | Seguro | "Seguro" alone also means insurance | Pago seguro |
| 3 | `sections.cart.trust.ssl_encrypted` | SSL Encrypted | SSL cifrado | English word order "SSL cifrado" | Cifrado SSL |
| 4 | `products.additional_info.secure_logistics_line_1` | If a package is damaged or lost in transit, contact us so we can help review the shipment. | Si un paquete se daña o se pierde durante el transporte, contáctenos para que podamos ayudarlo a revisar el envío. | usted-form "contáctenos", "ayudarlo" | Si un paquete se daña o se pierde durante el transporte, contáctanos para que podamos ayudarte a revisar el envío. |
| 4 | `products.additional_info.secure_logistics_line_2` | Use your order tracking link for the latest carrier updates. International orders may be subject to local taxes, duties, or customs fees collected by the carrier or local authority. | Utilice el enlace de seguimiento de su pedido para obtener las últimas actualizaciones del operador. Los pedidos internacionales pueden estar sujetos a impuestos, aranceles o tasas aduaneras locales cobrados por el transportista o la autoridad local. | usted-form "Utilice ... su pedido" | Usa el enlace de seguimiento de tu pedido para ver las últimas novedades del transportista. Los pedidos internacionales pueden estar sujetos a impuestos, aranceles o tasas aduaneras locales cobrados por el transportista o la autoridad local. |
| 4 | `products.product.size_guide.chart_units` | Size chart units | Unidades de tabla de tallas | missing article | Unidades de la tabla de tallas |
| 4 | `products.product.size_guide.compare_all_sizes` | Compare all sizes | Comparar todos los tamaños | "tamaños" for clothing sizes; the shop term is "tallas" | Comparar todas las tallas |
| 4 | `products.product.size_guide.compare_family_sizes` | Compare family sizes | Comparar tamaños de familia | "tamaños de familia" unnatural | Comparar las tallas de la familia |
| 4 | `products.product.size_guide.compare_hint` | Open the full chart below to compare nearby sizes. | Abra el cuadro completo a continuación para comparar tamaños cercanos. | usted-form "Abra", "cuadro completo a continuación" | Abre la tabla completa más abajo para comparar tallas cercanas. |
| 4 | `products.shipping_country.checker_no_results` | No matching country found in the current checkout list. Try another spelling or email us before ordering. | No encontramos ese país en la lista actual del checkout. Prueba otra forma de escribirlo o escríbenos antes de comprar. | "checkout" loanword | No encontramos ese país en la lista actual de países disponibles al finalizar la compra. Prueba otra forma de escribirlo o escríbenos antes de comprar. |
| 4 | `products.shipping_country.checker_summary` | Yes if your country appears below. These {{ count }} countries and regions are enabled in checkout right now. | Sí, si tu país aparece abajo. Estos {{ count }} países y regiones están activados ahora mismo en el checkout. | English loanword "checkout"; "ahora mismo" filler | Sí, si tu país aparece abajo. Estos {{ count }} países y regiones están disponibles ahora al finalizar la compra. |
| 5 | `products.product.inventory_low_stock` | Low stock | Bajas existencias | "Bajas existencias" calque | Pocas unidades |
| 5 | `products.product.inventory_low_stock_show_count` | Low stock: {{ quantity }} left | Bajas existencias: quedan {{ quantity }} | same | Pocas unidades: quedan {{ quantity }} |
| 5 | `products.product.matching_set.empty` | Choose at least one size to add your set. | Seleccione una talla para cada miembro de la familia que desee agregar. | usted-form ("Seleccione", "desee") among tú lines; does not match English (at least one size) | Elige al menos una talla para añadir tu conjunto. |
| 5 | `products.product.matching_set.error` | Unable to add the selected pieces. Please try again. | No se pueden agregar las piezas seleccionadas. Por favor inténtalo de nuevo. | "agregar" and "Por favor inténtalo" calque | No se pudieron añadir las piezas seleccionadas. Inténtalo de nuevo. |
| 5 | `products.product.matching_set.success` | Matching set added to cart. | Conjunto a juego agregado al carrito. | "agregado" vs "Añadir" | Conjunto a juego añadido al carrito. |
| 5 | `sections.cart.cart_error` | There was an error while updating your cart. Please try again. | Hubo un error al actualizar tu carrito de compra. Inténtalo de nuevo. | "carrito de compra" stiff | No pudimos actualizar tu carrito. Inténtalo de nuevo. |
| 5 | `sections.cart.cart_quantity_error_html` | You can only add {{ quantity }} of this item to your cart. | Solo puedes agregar {{ quantity }} de este artículo a tu carrito. | "agregar" while the page uses "Añadir" | Solo puedes añadir {{ quantity }} de este artículo a tu carrito. |

### Inline strings (not in locale files)

| Rank | Where | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::ROLE_LABELS_BY_LOCALE.child` | Child | Infantil | same adjective used as a noun on the PDP builder | Niño/a |
| 2 | `snippets/dlm-complete-family.liquid::t_another_child` | Another kid | Otro infantil | "Otro infantil" is not natural Spanish | Otro niño/a |
| 2 | `snippets/dlm-complete-family.liquid::t_child` | Kid | Infantil | "Infantil" is an adjective, not a noun for a child | Niño/a |

### Terms to standardise

| Term | Recommendation |
|---|---|
| Register | tú (descriptions use "Elige"). Remove usted-forms (Seleccione, Abra, Utilice, contáctenos). |
| cart | carrito (keep). |
| checkout (button) | Finalizar compra; "al finalizar la compra" in text. No loanword "checkout". |
| size | talla (never "tamaño" for clothing); table = tabla de tallas. |
| add to cart | Añadir al carrito (one verb everywhere; drop "Agregar"). |
| sold out | Agotado (keep). |
| free shipping | "Envío estándar incluido" (no "gratis/gratuito"). |
| secure | Pago seguro (not "Seguro" alone). |
| child | niño/a (not "infantil" as a noun). |

## French (fr)

Rows: 16 locale-file + 22 typography-only + 0 inline.

### Locale-file keys (`locales/fr.json`)

| Rank | Key | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 1 | `products.product.on_sale` | Sale | En vente | "En vente" means "for sale", not on sale; the badge sits on discounted items | Promo |
| 2 | `products.additional_info.free_shipping_label` | Standard shipping included | Livraison standard gratuite incluse | "gratuite incluse" redundant; adds "free" | Livraison standard incluse |
| 2 | `sections.cart.login.title` | Have an account? | Vous possédez un compte⍽? | "Vous possédez un compte ?" stiff; regular space before ? | Vous avez un compte⍽? |
| 2 | `sections.home_category_copy.heading_category` | Shop by Category | Magasiner par catégorie | "Magasiner" is Québécois; the store serves France first | Acheter par catégorie |
| 3 | `products.purchase_confidence.returns_headline` | Returns on eligible items | Retours des articles admissibles | "admissibles" here, "éligibles" elsewhere | Retours des articles éligibles |
| 3 | `products.purchase_confidence.returns_summary` | Request a return or exchange within 30 days of delivery for eligible items. | Demandez le retour ou l’échange des articles admissibles dans les 30 jours suivant la livraison. | "admissibles" vs "éligibles" | Demandez le retour ou l’échange des articles éligibles dans les 30 jours suivant la livraison. |
| 3 | `products.purchase_confidence.shipping_headline` | Standard shipping included | Livraison standard gratuite | "gratuite" adds a claim the English avoids | Livraison standard incluse |
| 3 | `products.trust.free_shipping` | Standard shipping included | Livraison standard gratuite incluse | same | Livraison standard incluse |
| 3 | `sections.cart.trust.secure` | Secure | Sécurisé | "Sécurisé" alone is unclear | Paiement sécurisé |
| 3 | `sections.cart.trust.ssl_encrypted` | SSL Encrypted | SSL crypté | English word order "SSL crypté" | Chiffrement SSL |
| 4 | `products.product.size_guide.compare_family_sizes` | Compare family sizes | Comparez la taille des familles | "la taille des familles" wrong meaning | Comparez les tailles de la famille |
| 4 | `products.product.size_guide.your_size_details` | Your size details | Vos détails de taille | "Vos détails de taille" calque | Détails de votre taille |
| 4 | `products.purchase_confidence.returns_eligible` | Eligible items must be unworn, unwashed, and returned with tags attached. | Les articles admissibles doivent être non portés, non lavés et retournés avec leurs étiquettes attachées. | same term unification, plus "attachées" | Les articles éligibles doivent être non portés, non lavés et retournés avec leurs étiquettes. |
| 4 | `products.shipping_country.checker_no_results` | No matching country found in the current checkout list. Try another spelling or email us before ordering. | Aucun pays correspondant dans la liste actuelle du checkout. Essayez une autre orthographe ou contactez-nous avant de commander. | "checkout" loanword | Aucun pays correspondant dans la liste actuelle des pays disponibles au paiement. Essayez une autre orthographe ou contactez-nous avant de commander. |
| 4 | `products.shipping_country.checker_summary` | Yes if your country appears below. These {{ count }} countries and regions are enabled in checkout right now. | Oui si votre pays apparaît ci-dessous. Ces {{ count }} pays et régions sont actuellement activés au checkout. | "checkout" loanword (button/trust rows say "paiement") | Oui si votre pays apparaît ci-dessous. Ces {{ count }} pays et régions sont actuellement disponibles au paiement. |
| 5 | `products.product.inventory_low_stock_show_count` | Low stock: {{ quantity }} left | Stock bas⍽: {{ quantity }} restant(s) | "restant(s)" placeholder-style plural | Stock bas⍽: plus que {{ quantity }} |

Typography only (no-break space before `: ; ! ?`; corrected values are in `proposed.json`, visible as ⍽ here): `storefront.pdp_steps.option`, `storefront.pdp_steps.who`, `products.additional_info.christmas_order_by`, `products.additional_info.christmas_order_by_other`, `products.additional_info.estimated_delivery`, `sections.cart.discount_applied`, `sections.cart.discount_code_toggle`, `products.purchase_confidence.ships_to_country`, `products.shipping_country.checker_title`, `products.shipping_country.checker_trigger`, `products.shipping_country.trust_ships_to`, `products.trust.assistance_note`, `products.additional_info.premium_delivery_window`, `products.purchase_confidence.returns_damaged`, `products.purchase_confidence.shipping_details_body`, `products.shipping_card.details_body`, `products.shipping_country.checker_note_html`, `products.shipping_country.product_country`, `products.shipping_country.product_country_with_currency`, `products.shipping_country.product_note_html`, `products.additional_info.faster_shipping_prefix`, `products.product.shipping_policy_html`.

### Terms to standardise

| Term | Recommendation |
|---|---|
| Register | vous (already consistent). |
| cart | panier (keep). |
| checkout (button) | Procéder au paiement (keep); "au paiement" in text, no loanword "checkout". |
| size | taille (keep). |
| add to cart | Ajouter au panier (keep). |
| sold out | Épuisé (keep). |
| free shipping | "Livraison standard incluse" (no "gratuite"). |
| eligible | éligibles everywhere (not admissibles). |
| typography | no-break space before : ; ! ? in every string. |

## Czech (cs)

Rows: 28 locale-file + 3 inline.

### Locale-file keys (`locales/cs.json`)

| Rank | Key | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 1 | `products.product.matching_set.copy` | Pick a size for each person. Priced per piece. | Vyberte velikost pro každého. Cena je za kus. | "každého" is masculine; the people may be women or girls | Vyberte velikost pro každou osobu. Cena je za kus. |
| 1 | `products.product.matching_set.copy_person` | Pick a size for each person. | Vyberte velikost pro každého. | same | Vyberte velikost pro každou osobu. |
| 1 | `products.product.matching_set.heading` | Build your matching set | Sestavte si odpovídající sadu | "odpovídající" (corresponding) calque; the shop says "sladěný" | Sestavte si sladěnou sadu |
| 1 | `products.product.on_sale` | Sale | Výprodej | "Výprodej" means clearance sale; the badge marks a discounted item | Sleva |
| 1 | `products.product.size_required_message` | Please select a size before adding to cart. | Prosím, vyberte velikost před přidáním do košíku. | "Prosím," calque and long | Před přidáním do košíku vyberte velikost. |
| 2 | `products.additional_info.free_shipping_label` | Standard shipping included | Doprava zdarma – standardní doprava v ceně | "Doprava zdarma – standardní doprava v ceně" repeats itself and adds "free" | Standardní doprava v ceně |
| 2 | `sections.cart.complete_the_look` | Complete the Look | Dokončete vzhled | "Dokončete vzhled" literal calque | Doplňte svůj outfit |
| 2 | `sections.cart.estimated_total` | Estimated total | Odhadovaný součet | "součet" is a sum of numbers, not a price total | Odhadovaná celková cena |
| 2 | `sections.cart.new_estimated_total` | New estimated total | Nový odhadovaný součet | same | Nová odhadovaná celková cena |
| 2 | `sections.cart.savings_html` | You're saving <strong>{{ amount }}</strong> | Ukládáte <strong>{{ amount }}</strong> | "Ukládáte" means storing/saving a file, not saving money | Ušetříte <strong>{{ amount }}</strong> |
| 2 | `sections.header.cart_count.few` | {{ count }} items | (missing in file) | NEW KEY: cs needs the "few" form (2-4); without it "3 položek" shows | {{ count }} položky |
| 2 | `sections.header.cart_count.many` | {{ count }} items | (missing in file) | NEW KEY: cs "many" form | {{ count }} položky |
| 3 | `products.purchase_confidence.security_headline` | Secure checkout | Zabezpečená pokladna | "Zabezpečená pokladna" vs "Bezpečná pokladna" in the trust rows | Bezpečná pokladna |
| 3 | `products.purchase_confidence.shipping_headline` | Standard shipping included | Standardní doprava zdarma | "zdarma" adds a claim the English avoids | Standardní doprava v ceně |
| 3 | `products.purchase_confidence.ships_to_default` | Ships to your country | Doručení do tvé země | tykání "tvé země" | Doručení do vaší země |
| 3 | `products.trust.free_shipping` | Standard shipping included | Doprava zdarma – standardní doprava v ceně | same | Standardní doprava v ceně |
| 3 | `sections.cart.trust.returns` | 30-day returns | 30denní vrácení | "30denní vrácení" clipped | Vrácení do 30 dnů |
| 3 | `sections.cart.trust.ssl_encrypted` | SSL Encrypted | SSL šifrováno | English word order | Šifrování SSL |
| 4 | `products.product.size_guide.compare_family_sizes` | Compare family sizes | Porovnejte velikosti rodiny | "velikosti rodiny" unnatural | Porovnejte velikosti pro celou rodinu |
| 4 | `products.product.size_guide.guide_and_fit` | Size guide & fit | Průvodce velikostí a přizpůsobení | "přizpůsobení" means adaptation, not garment fit | Průvodce velikostmi a padnutí |
| 4 | `products.purchase_confidence.security_details_body` | Payments are encrypted and processed securely by our payment providers. We do not store your full card number. | Platby jsou šifrované a bezpečně zpracovávané našimi poskytovateli plateb. Neukládáme úplné číslo tvé karty. | tykání "tvé karty" among vykání lines | Platby jsou šifrované a bezpečně zpracovávané našimi poskytovateli plateb. Neukládáme úplné číslo vaší karty. |
| 4 | `products.shipping_country.checker_no_results` | No matching country found in the current checkout list. Try another spelling or email us before ordering. | V aktuálním seznamu checkoutu nebyla nalezena odpovídající země. Zkuste jiný zápis nebo nám před objednáním napište. | "checkoutu" loanword | V aktuálním seznamu zemí dostupných v pokladně nebyla nalezena odpovídající země. Zkuste jiný zápis nebo nám před objednáním napište. |
| 4 | `products.shipping_country.checker_summary` | Yes if your country appears below. These {{ count }} countries and regions are enabled in checkout right now. | Ano, pokud je vaše země níže. Těchto {{ count }} zemí a regionů je právě aktivních v checkoutu. | "checkoutu" loanword; "je vaše země níže" incomplete | Ano, pokud je vaše země uvedena níže. Těchto {{ count }} zemí a regionů je právě k dispozici v pokladně. |
| 5 | `products.product.inventory_low_stock` | Low stock | Nízký stav zásob | "Nízký stav zásob" warehouse wording | Poslední kusy |
| 5 | `products.product.inventory_low_stock_show_count` | Low stock: {{ quantity }} left | Nízký stav: {{ quantity }} zbývá | "zbývá" wrong number agreement | Skladem pouze {{ quantity }} ks |
| 5 | `products.product.matching_set.success` | Matching set added to cart. | Odpovídající sada přidána do košíku. | "odpovídající sada" calque | Sladěná sada byla přidána do košíku. |
| 5 | `products.product.value_unavailable` | {{ option_value }} - Unavailable | {{ option_value }} - Nedostupné | capital "Nedostupné" after a size/colour | {{ option_value }} – nedostupné |
| 5 | `sections.cart.cart_quantity_error_html` | You can only add {{ quantity }} of this item to your cart. | Do košíku můžete přidat pouze {{ quantity }} tohoto produktu. | missing unit "ks" | Do košíku můžete přidat pouze {{ quantity }} ks tohoto produktu. |

### Inline strings (not in locale files)

| Rank | Where | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.pieceMany` | {count} Matching Pieces | {count} ladících kusů | same; wrong plural form after a number | Sladěné kusy: {count} |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.pieceOne` | 1 Matching Piece | 1 ladící kus | "ladící" means tuning/harmonising, not matching | 1 sladěný kus |
| 2 | `sections/main-cart-footer.liquid::dlm_cart_taxes_checkout` | Taxes calculated at checkout. | Daně se vypočítají při pokladně. | "při pokladně" (at the cashier) instead of "v pokladně" | Daně se vypočítají v pokladně. |

### Terms to standardise

| Term | Recommendation |
|---|---|
| Register | vykání (vy). Remove tykání: tvé/tvá. |
| cart | košík (keep). |
| checkout (button) | Přejít k pokladně (keep); trust label "Bezpečná pokladna" (not Zabezpečená). |
| size | velikost (keep); guide = Průvodce velikostmi. |
| add to cart | Přidat do košíku (keep). |
| sold out | Vyprodáno (keep). |
| free shipping | "Standardní doprava v ceně" (no "zdarma"). |
| matching | sladěný (not odpovídající/ladící). |
| plurals | add "few" and "many" to every counted key (cart_count). |

## Romanian (ro)

Rows: 65 locale-file + 21 inline.

### Locale-file keys (`locales/ro.json`)

| Rank | Key | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 1 | `general.cart.view` | View cart ({{ count }}) | Vezi coșul ({{ count }}) | tu-form | Vedeți coșul ({{ count }}) |
| 1 | `general.cart.view_empty_cart` | View cart | Vezi coșul | tu-form | Vedeți coșul |
| 1 | `general.continue_shopping` | Continue shopping | Continuă cumpărăturile | tu-form | Continuați cumpărăturile |
| 1 | `products.product.add_to_cart` | Add to cart | Adaugă în coș | tu-form imperative; descriptions use polite plural (STYLE_RULES_RO) | Adăugați în coș |
| 1 | `products.product.choose_options` | Choose options | Alege opțiuni | tu-form | Alegeți opțiunile |
| 1 | `products.product.matching_set.add` | Add matching pieces | Adaugă piese asortate | tu-form | Adăugați piesele selectate |
| 1 | `products.product.matching_set.copy` | Pick a size for each person. Priced per piece. | Alege o mărime pentru fiecare persoană. Preț per piesă. | tu-form | Alegeți o mărime pentru fiecare persoană. Preț per piesă. |
| 1 | `products.product.matching_set.copy_person` | Pick a size for each person. | Alege o mărime pentru fiecare persoană. | tu-form | Alegeți o mărime pentru fiecare persoană. |
| 1 | `products.product.matching_set.heading` | Build your matching set | Construiește-ți setul potrivit | tu-form; "potrivit" calque | Creați-vă setul asortat |
| 1 | `sections.cart.empty` | Your cart is empty | Coșul tău este gol | tu-form | Coșul dvs. este gol |
| 1 | `sections.cart.title` | Your cart | Coșul tău | tu-form "tău" | Coșul dvs. |
| 1 | `storefront.pdp_steps.color` | Choose color | Alege culoarea | tu-form | Alegeți culoarea |
| 1 | `storefront.pdp_steps.option` | Choose {{ option }} | Alege: {{ option }} | tu-form | Alegeți: {{ option }} |
| 1 | `storefront.pdp_steps.piece` | Choose piece | Alege articolul | tu-form; "articolul" vs "piesă" used in the cart | Alegeți piesa |
| 1 | `storefront.pdp_steps.size` | Choose size | Alege mărimea | tu-form | Alegeți mărimea |
| 2 | `general.cart.item_added` | Item added to your cart | Produs adăugat în coșul tău | tu-form "coșul tău" | Produs adăugat în coș |
| 2 | `products.additional_info.christmas_order_by` | Estimate: order by {{ order_date }} to arrive by {{ arrive_date }}. Not a guarantee. | Estimare: comandă până la {{ order_date }} pentru a primi până la {{ arrive_date }}. Nu este o garanție. | "comandă" (noun/tu) instead of polite plural | Estimare: comandați până la {{ order_date }} pentru a primi până la {{ arrive_date }}. Nu este o garanție. |
| 2 | `products.additional_info.christmas_order_by_other` | Ordering for Christmas? Delivery times vary by country, so order as early as you can. | Comanzi pentru Crăciun? Timpii de livrare diferă de la o țară la alta, așa că comandă cât mai devreme. | tu-form; "Timpii de livrare" calque (use "Termenele") | Comandați pentru Crăciun? Termenele de livrare diferă de la o țară la alta, așa că comandați cât mai devreme. |
| 2 | `products.product.include_taxes` | Tax included. | Taxa inclusă. | singular "Taxa" | Taxe incluse. |
| 2 | `products.product.quantity.decrease` | Decrease quantity for {{ product }} | Scade cantitatea pentru {{ product }} | tu-form; "Scade" reads as a noun/verb of subtracting | Reduceți cantitatea pentru {{ product }} |
| 2 | `products.product.quantity.increase` | Increase quantity for {{ product }} | Mărește cantitatea pentru {{ product }} | tu-form | Măriți cantitatea pentru {{ product }} |
| 2 | `sections.announcements.default_promo` | BUY 2, GET A 3RD PIECE 20% OFF \| STANDARD SHIPPING INCLUDED \| SECURE CHECKOUT | CUMPĂRĂ 2, PRIMEȘTI 20% REDUCERE LA AL 3-LEA ARTICOL \| LIVRARE STANDARD INCLUSĂ \| PLATĂ SECURIZATĂ | tu-form caps; "al 3-lea articol" vs cart "a 3-a piesă" | CUMPĂRAȚI 2, PRIMIȚI 20% REDUCERE LA A 3-A PIESĂ \| LIVRARE STANDARD INCLUSĂ \| PLATĂ SECURIZATĂ |
| 2 | `sections.announcements.shipping_country_promo` | BUY 2, GET A 3RD PIECE 20% OFF \| STANDARD SHIPPING INCLUDED TO {{ country }} \| SECURE CHECKOUT | CUMPĂRĂ 2, PRIMEȘTI 20% REDUCERE LA AL 3-LEA ARTICOL \| LIVRARE STANDARD INCLUSĂ CĂTRE {{ country }} \| PLATĂ SECURIZATĂ | same | CUMPĂRAȚI 2, PRIMIȚI 20% REDUCERE LA A 3-A PIESĂ \| LIVRARE STANDARD INCLUSĂ CĂTRE {{ country }} \| PLATĂ SECURIZATĂ |
| 2 | `sections.cart.complete_the_look` | Complete the Look | Completează Look-ul | "Look-ul" English with capital L; the shop says "ținută" | Completați ținuta |
| 2 | `sections.cart.discount_apply` | Apply | Aplică | tu-form | Aplicați |
| 2 | `sections.cart.discount_code_toggle` | Have a discount code? | Ai un cod de reducere? | tu-form | Aveți un cod de reducere? |
| 2 | `sections.cart.login.paragraph_html` | <a href="{{ link }}" class="link underlined-link">Log in</a> to check out faster. | <a href="{{ link }}" class="link underlined-link">Conectează-te</a> pentru a finaliza cumpărăturile mai rapid. | tu-form | <a href="{{ link }}" class="link underlined-link">Conectați-vă</a> pentru a finaliza cumpărăturile mai rapid. |
| 2 | `sections.cart.login.title` | Have an account? | Ai un cont? | tu-form | Aveți un cont? |
| 2 | `sections.cart.new_estimated_total` | New estimated total | Total estimat nou | word order "Total estimat nou" | Noul total estimat |
| 2 | `sections.cart.remove_title` | Remove {{ title }} | Elimină {{ title }} | tu-form | Eliminați {{ title }} |
| 2 | `sections.cart.savings_html` | You're saving <strong>{{ amount }}</strong> | Salvați <strong>{{ amount }}</strong> | "Salvați" means save a file, not save money | Economisiți <strong>{{ amount }}</strong> |
| 2 | `sections.cart.you_may_also_like` | You may also like | S-ar putea să-ți placă și | tu-form | S-ar putea să vă placă și |
| 2 | `sections.header.cart_count.few` | {{ count }} items | (missing in file) | NEW KEY: ro "few" (0, 2-19) | {{ count }} articole |
| 2 | `sections.header.cart_count.other` | {{ count }} items | {{ count }} articole | ro "other" (20+) needs "de": "25 articole" is wrong | {{ count }} de articole |
| 2 | `sections.home_category_copy.heading_category` | Shop by Category | Cumpără după categorie | tu-form | Cumpărați după categorie |
| 3 | `products.purchase_confidence.change_short` | Change | Schimbă | tu-form | Schimbați |
| 3 | `products.purchase_confidence.security_headline` | Secure checkout | Finalizare securizată a comenzii | "Finalizare securizată a comenzii" long, differs from trust row | Plată securizată |
| 3 | `products.purchase_confidence.ships_to_default` | Ships to your country | Livrăm în țara ta | tu-form | Livrăm în țara dvs. |
| 3 | `products.trust.assistance_note` | Need help? We typically reply within one business day. | Ai nevoie de ajutor? De obicei, răspundem în termen de o zi lucrătoare. | tu-form | Aveți nevoie de ajutor? De obicei vă răspundem în termen de o zi lucrătoare. |
| 3 | `products.trust.returns` | 30-day return window | Fereastră de retur de 30 de zile | "Fereastră de retur" is an English calque ("return window") | Retur în 30 de zile |
| 3 | `products.trust.secure_checkout` | Secure Checkout | Checkout securizat | unify secure-checkout term | Plată securizată |
| 3 | `sections.cart.trust.returns` | 30-day returns | Retururi de 30 de zile | "Retururi de 30 de zile" calque | Retur în 30 de zile |
| 3 | `sections.cart.trust.secure_checkout` | Secure Checkout | Checkout securizat | three terms for secure checkout (Checkout securizat, Finalizare securizată, Plată securizată); unify | Plată securizată |
| 3 | `sections.cart.trust.ssl_encrypted` | SSL Encrypted | SSL criptat | English word order | Criptare SSL |
| 4 | `products.product.size_guide.chart_units` | Size chart units | Tabel de mărimi unități | "Tabel de mărimi unități" ungrammatical | Unitățile tabelului de mărimi |
| 4 | `products.product.size_guide.compare_all_sizes` | Compare all sizes | Comparați toate dimensiunile | "dimensiunile" (dimensions) for sizes | Comparați toate mărimile |
| 4 | `products.product.size_guide.compare_family_sizes` | Compare family sizes | Comparați dimensiunile familiei | "dimensiunile familiei" wrong meaning | Comparați mărimile pentru întreaga familie |
| 4 | `products.product.size_guide.compare_hint` | Open the full chart below to compare nearby sizes. | Deschideți tabelul complet de mai jos pentru a compara dimensiunile din apropiere. | "dimensiunile din apropiere" calque | Deschideți tabelul complet de mai jos pentru a compara mărimile apropiate. |
| 4 | `products.product.size_guide.your_size_details` | Your size details | Detaliile tale marimii | typo "marimii", "tale" does not agree | Detaliile mărimii dvs. |
| 4 | `products.purchase_confidence.privacy_link_label` | View privacy policy | Vezi politica de confidențialitate | tu-form | Vedeți politica de confidențialitate |
| 4 | `products.purchase_confidence.returns_full_link_label` | View full return policy | Vezi politica completă de retur | tu-form | Vedeți politica completă de retur |
| 4 | `products.purchase_confidence.security_details_body` | Payments are encrypted and processed securely by our payment providers. We do not store your full card number. | Plățile sunt criptate și procesate în siguranță de furnizorii noștri de servicii de plată. Nu stocăm numărul complet al cardului. | tu-form "cardului tău" | Plățile sunt criptate și procesate în siguranță de furnizorii noștri de servicii de plată. Nu stocăm numărul complet al cardului dvs. |
| 4 | `products.shipping_card.change_country` | Change country | Schimbă țara | tu-form | Schimbați țara |
| 4 | `products.shipping_card.see_countries` | See shipping countries | Vezi țările de livrare | tu-form | Vedeți țările de livrare |
| 4 | `products.shipping_country.checker_close` | Close country checker | Închide verificarea țării | tu-form | Închideți verificarea țării |
| 4 | `products.shipping_country.checker_no_results` | No matching country found in the current checkout list. Try another spelling or email us before ordering. | Nu am găsit o țară potrivită în lista actuală din checkout. Încearcă o altă scriere sau contactează-ne înainte de comandă. | tu-form; "checkout" loanword | Nu am găsit o țară potrivită în lista actuală de țări disponibile la finalizarea comenzii. Încercați o altă scriere sau contactați-ne înainte de comandă. |
| 4 | `products.shipping_country.checker_search_label` | Search country or region | Caută țară sau regiune | tu-form | Căutați țara sau regiunea |
| 4 | `products.shipping_country.checker_search_placeholder` | Type a country name, code, or currency | Scrie țara, codul sau moneda | tu-form | Introduceți țara, codul sau moneda |
| 4 | `products.shipping_country.checker_summary` | Yes if your country appears below. These {{ count }} countries and regions are enabled in checkout right now. | Da, dacă țara ta apare mai jos. Aceste {{ count }} țări și regiuni sunt active acum în checkout. | tu-form; "checkout" loanword | Da, dacă țara dvs. apare mai jos. Aceste {{ count }} țări și regiuni sunt disponibile acum la finalizarea comenzii. |
| 4 | `storefront.privacy_modal.full_link` | Open full privacy policy in a new tab | Deschide politica de confidențialitate completă într-o filă nouă | tu-form | Deschideți politica de confidențialitate completă într-o filă nouă |
| 4 | `storefront.privacy_modal.line_3_html` | Dress Like Mommy <strong>does not store your full card number</strong>. | Dress Like Mommy <strong>nu stochează numărul complet al cardului tău</strong>. | tu-form "cardului tău" | Dress Like Mommy <strong>nu stochează numărul complet al cardului dvs.</strong>. |
| 4 | `storefront.privacy_modal.line_5_html` | We <strong>do not sell</strong> your personal information. | <strong>Nu vindem</strong> informațiile tale personale. | tu-form | <strong>Nu vindem</strong> informațiile dvs. personale. |
| 5 | `products.product.matching_set.empty` | Choose at least one size to add your set. | Selectați o dimensiune pentru fiecare membru al familiei pe care doriți să-l adăugați. | "dimensiune" for size; the shop term is "mărime"; does not match English (at least one size) | Alegeți cel puțin o mărime pentru a adăuga setul. |
| 5 | `products.product.matching_set.success` | Matching set added to cart. | Setul potrivit a fost adăugat în coș. | "setul potrivit" calque | Setul asortat a fost adăugat în coș. |
| 5 | `sections.cart.cart_quantity_error_html` | You can only add {{ quantity }} of this item to your cart. | Poți adăuga în coș doar {{ quantity }} din acest articol. | tu-form "Poți" | Puteți adăuga în coș doar {{ quantity }} din acest articol. |

### Inline strings (not in locale files)

| Rank | Where | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.addCurrentPiece` | Add this piece to bag | Adaugă această piesă în coș | tu-form | Adăugați această piesă în coș |
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.chooseOptionsStep` | Choose size and options | Alege mărimea și opțiunile | tu-form | Alegeți mărimea și opțiunile |
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.chooseRoleCta` | Choose a family member | Alege un membru al familiei | tu-form | Alegeți un membru al familiei |
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.chooseRoleStep` | Choose who this piece is for | Alege pentru cine este această piesă | tu-form | Alegeți pentru cine este această piesă |
| 1 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.pickSize` | Pick a size | Alege o mărime | tu-form | Alegeți o mărime |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::FAMILY_BUNDLE_COPY_BY_LOCALE.line` | Buy 2, get the 3rd 20% off. | Cumpără 2, a 3-a cu 20% reducere. | tu-form | Cumpărați 2, a 3-a cu 20% reducere. |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.addAnotherFamilyMember` | Add another family member | Adaugă un alt membru al familiei | tu-form | Adăugați un alt membru al familiei |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.addRole` | + Add {role} | + Adaugă {role} | tu-form | + Adăugați {role} |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.closeSizeDetails` | Close size details | Închide detaliile mărimii | tu-form | Închideți detaliile mărimii |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.decreaseQuantity` | Decrease quantity | Scade cantitatea | tu-form | Reduceți cantitatea |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.findFit` | Find {role}'s fit | Găsește potrivirea pentru {role} | tu-form; "potrivirea" calque of "fit" | Găsiți mărimea potrivită pentru {role} |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.increaseQuantity` | Increase quantity | Crește cantitatea | tu-form | Măriți cantitatea |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.pickAxis` | Pick a {axis} | Alege {axis} | tu-form | Alegeți {axis} |
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::UI_LABELS_BY_LOCALE.removeRole` | Remove {role} | Elimină {role} | tu-form | Eliminați {role} |
| 2 | `snippets/automatic-discount-promo.liquid::promo_next_title` | Add 1 more piece and get 20% off the lowest-priced piece | Adaugă încă 1 piesă și primești 20% reducere la piesa cu cel mai mic preț | tu-form | Adăugați încă 1 piesă și primiți 20% reducere la piesa cu cel mai mic preț |
| 2 | `snippets/automatic-discount-promo.liquid::promo_offer` | Buy 2, get the 3rd piece 20% off | Cumpără 2 și primești 20% reducere la a 3-a piesă | tu-form "Cumpără ... primești" | Cumpărați 2 și primiți 20% reducere la a 3-a piesă |
| 2 | `snippets/cart-item-add-member.liquid::cam_text` | Añadir talla para otro familiar | Adaugă o mărime pentru alt membru al familiei | tu-form | Adăugați o mărime pentru alt membru al familiei |
| 2 | `snippets/dlm-complete-family.liquid::t_add` | Add | Adaugă | tu-form button | Adăugați |
| 2 | `snippets/dlm-complete-family.liquid::t_error` | Could not add to bag. Please try again. | Nu s-a putut adăuga în coș. Încearcă din nou. | tu-form | Nu s-a putut adăuga în coș. Încercați din nou. |
| 2 | `snippets/dlm-complete-family.liquid::t_heading` | Complete the family | Completează familia | tu-form; the same module uses polite plural in the hint | Completați familia |
| 3 | `snippets/dlm-delivery-vary-copy.liquid::echo` | Delivery times vary by country. | Timpii de livrare diferă în funcție de țară. | "Timpii" calque | Termenele de livrare diferă în funcție de țară. |

### Terms to standardise

| Term | Recommendation |
|---|---|
| Register | polite plural (dvs./dumneavoastră), as in STYLE_RULES_RO and the descriptions. Remove tu-forms: tău/Alege/Adaugă/Vezi/Poți/Ai. |
| cart | coș (keep): "Coșul dvs.". |
| checkout (button) | Finalizare comandă (keep). |
| size | mărime (never "dimensiune" for clothing). |
| add to cart | Adăugați în coș. |
| sold out | Epuizat (keep). |
| free shipping | "Livrare standard inclusă" (keep). |
| secure | Plată securizată (one term for all three places). |
| piece | piesă (not articol) for garments in promo/trust lines. |
| plurals | ro needs "few" (2-19) and "other" with "de" (20+). |

## Italian (it): gated (`locales/it.json` has a pending owner-gated release)

Reviewed against `origin/main` `locales/it.json`, not the locally modified copy (the working tree it.json differs by 131 added / 195 removed lines and was not read). Do not apply until the pending it.json release is decided; re-diff these keys against that release first. They are listed separately for that reason, and they are in `proposed.json` under `it`.

Rows: 23 locale-file + 3 inline.

### Locale-file keys (`locales/it.json`)

| Rank | Key | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 1 | `products.product.choose_options` | Choose options | Scegli opzioni | missing article | Scegli le opzioni |
| 1 | `products.product.matching_set.add` | Add matching pieces | Aggiungi i pezzi selezionati al carrello | "pezzi" vs "capi" elsewhere | Aggiungi i capi selezionati al carrello |
| 1 | `sections.cart.checkout` | Check out | Check-out | "Check-out" with a hyphen is the hotel word; trust rows say "Pagamento" | Procedi al pagamento |
| 2 | `products.additional_info.christmas_order_by_other` | Ordering for Christmas? Delivery times vary by country, so order as early as you can. | (missing in file) | KEY MISSING in it.json: the English sentence shows on Italian pages | Ordini per Natale? I tempi di consegna variano a seconda del paese, quindi ordina il prima possibile. |
| 2 | `products.additional_info.free_shipping_label` | Standard shipping included | Spedizione standard gratuita inclusa | "gratuita inclusa" redundant; adds "free" | Spedizione standard inclusa |
| 2 | `products.product.include_taxes` | Tax included. | Imposte incluse. | "Imposte" here, "Tasse" in the cart | Tasse incluse. |
| 2 | `products.product.quantity.decrease` | Decrease quantity for {{ product }} | Diminuisci quantità per {{ product }} | missing article | Riduci la quantità di {{ product }} |
| 2 | `products.product.quantity.increase` | Increase quantity for {{ product }} | Aumenta quantità per {{ product }} | missing article | Aumenta la quantità di {{ product }} |
| 2 | `sections.announcements.default_promo` | BUY 2, GET A 3RD PIECE 20% OFF \| STANDARD SHIPPING INCLUDED \| SECURE CHECKOUT | COMPRANE 2, IL 3° CAPO È SCONTATO DEL 20% \| SPEDIZIONE STANDARD INCLUSA \| PAGAMENTO SICURO | "COMPRANE 2" is awkward; cart says "Compra 2, il 3° capo è scontato del 20%" | COMPRA 2, IL 3° CAPO È SCONTATO DEL 20% \| SPEDIZIONE STANDARD INCLUSA \| PAGAMENTO SICURO |
| 2 | `sections.announcements.shipping_country_promo` | BUY 2, GET A 3RD PIECE 20% OFF \| STANDARD SHIPPING INCLUDED TO {{ country }} \| SECURE CHECKOUT | COMPRANE 2, IL 3° CAPO È SCONTATO DEL 20% \| SPEDIZIONE STANDARD INCLUSA ({{ country }}) \| PAGAMENTO SICURO | same | COMPRA 2, IL 3° CAPO È SCONTATO DEL 20% \| SPEDIZIONE STANDARD INCLUSA ({{ country }}) \| PAGAMENTO SICURO |
| 2 | `sections.cart.login.paragraph_html` | <a href="{{ link }}" class="link underlined-link">Log in</a> to check out faster. | <a href="{{ link }}" class="link underlined-link">Accedi</a> per un check-out più veloce. | "check-out" again | <a href="{{ link }}" class="link underlined-link">Accedi</a> per pagare più velocemente. |
| 2 | `sections.home_category_copy.daddy_me` | Daddy & Me | Papà e figlio | "Papà e figlio" narrows to sons | Papà e io |
| 2 | `sections.home_category_copy.mommy_me` | Mommy & Me | Mamma e figlia | "Mamma e figlia" narrows the English "Mommy & Me" to daughters | Mamma e io |
| 3 | `products.purchase_confidence.security_headline` | Secure checkout | Checkout sicuro | "Checkout sicuro" vs "Pagamento sicuro" in the trust rows | Pagamento sicuro |
| 3 | `products.purchase_confidence.shipping_headline` | Standard shipping included | Spedizione standard gratuita | "gratuita" adds a claim the English avoids | Spedizione standard inclusa |
| 3 | `products.trust.free_shipping` | Standard shipping included | Spedizione standard gratuita inclusa | same | Spedizione standard inclusa |
| 3 | `products.trust.returns` | 30-day return window | Finestra di reso di 30 giorni | "Finestra di reso" is an English calque | Reso entro 30 giorni |
| 3 | `sections.cart.trust.secure` | Secure | Sicuro | "Sicuro" alone is unclear | Pagamento sicuro |
| 3 | `sections.cart.trust.ssl_encrypted` | SSL Encrypted | SSL crittografato | English word order | Crittografia SSL |
| 4 | `products.product.size_guide.compare_family_sizes` | Compare family sizes | Confronta le dimensioni della famiglia | "dimensioni" for sizes; shop term is "taglie" | Confronta le taglie della famiglia |
| 5 | `products.product.inventory_in_stock_show_count` | {{ quantity }} in stock | {{ quantity }} disponibile/i | "disponibile/i" placeholder-style plural | {{ quantity }} disponibili |
| 5 | `products.product.matching_set.error` | Unable to add the selected pieces. Please try again. | Impossibile aggiungere i pezzi selezionati. Per favore riprova. | "pezzi" and "Per favore riprova" calque | Impossibile aggiungere i capi selezionati. Riprova. |
| 5 | `sections.cart.cart_error` | There was an error while updating your cart. Please try again. | Si è verificato un errore durante l'aggiornamento del carrello. Riprova più tardi. | adds "più tardi" (later) that the English does not say | Si è verificato un errore durante l’aggiornamento del carrello. Riprova. |

### Inline strings (not in locale files)

| Rank | Where | English | Current | Problem | Corrected |
|---|---|---|---|---|---|
| 2 | `assets/product-desktop-ux-20260513-ruler-sync.js::ROLE_LABELS_BY_LOCALE.child` | Child | Bimbi | "Bimbi" is plural and slangy; shows in "+ Aggiungi Bimbi" | Bambino/a |
| 2 | `snippets/dlm-complete-family.liquid::t_another_child` | Another kid | Un altro bimbo/a | same | Un altro bambino/a |
| 2 | `snippets/dlm-complete-family.liquid::t_child` | Kid | Bimbo/a | "Bimbo/a" is a slangy/pejorative-sounding word in Italian | Bambino/a |

### Terms to standardise

| Term | Recommendation |
|---|---|
| Register | tu (descriptions use "Scegli"). Keep. |
| cart | carrello (keep). |
| checkout (button) | Procedi al pagamento; trust label "Pagamento sicuro" (not "Checkout sicuro", not hyphenated "Check-out"). |
| size | taglia (never "dimensioni"). |
| add to cart | Aggiungi al carrello (keep). |
| sold out | Esaurito (keep). |
| free shipping | "Spedizione standard inclusa" (no "gratuita"). |
| tax | Tasse (not Imposte). |
| child | bambino/a (not bimbo/Bimbi). |

## How to apply (later)

1. Locale rows: merge `proposed.json[locale]` into `locales/<locale>.json` key by key (keys use dotted paths; `sections.header.cart_count.few|many` are new keys in cs and ro, `few` new in ro). Keep placeholders and HTML as given. Release the non-Italian locales through the normal main sync; hold `it` until the owner-gated it.json release is resolved.
2. Inline rows: edit the named snippet/JS table (`proposed-inline.json`); they are theme-code edits, not locale edits, and need the normal UI browser verification (cart drawer, cart page, PDP builder) per language.
3. After release, re-render one PDP and one cart per language (4 requests each) and compare to this file. The register change (de to Sie, ro to polite plural, es usted lines to tú, cs tvé to vaše) should be applied as one batch per language so no page mixes forms.

Limits: the 178 purchase-path keys were each read in all six languages; strings outside that set (collection copy, blog, account pages, checkout hosted by Shopify) were not reviewed. Native-speaker sign-off was not available: corrections are reviewer judgment, to be spot-checked by the Calidad expert before release.
