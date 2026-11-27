# Greek (el) storefront text review (2026-11-27)

Same method as `collection-copy-review-2-2026-11-27.md`. Greek is published (Admin `shopLocales`: `el` published = true, read earlier today).

## Scope read (EN against EL, every string)

- Collection copy: the 97 rendered `sections.collection_seo` keys (H1/display titles, intro bodies, rich guide parts, meta descriptions, swimsuits guide and FAQ) plus all 44 `display_titles` and 16 `meta_titles` (157 strings).
- Purchase path and most visible UI (505 strings): `products.product`, `products.additional_info`, `products.purchase_confidence`, `products.shipping_card`, `products.shipping_country`, `products.trust`, `products.facets`, `sections.cart` (incl. `item_removed` "Το προϊόν αφαιρέθηκε" / `undo` "Αναίρεση", already fine), `general.cart/search/pagination`, `templates.search/cart/404`, `sections.header/footer/footer_headings/announcements`, `storefront.mega_menu/menu/pdp_steps/privacy_modal`, breadcrumbs and collection navigation, product navigation, localization, customer account/login/register/password/orders, newsletter.
- Not read in this unit: `storefront.callout`, `storefront.journal`, `storefront.article`, `sections.home_category_copy`, `customer.addresses/order`, gift cards, Dawn inventory labels ("Σε απόθεμα"; Dawn keys not used by the theme's PDP).

Category names (category-names.json, el): Οικογενειακά ασορτί / Μαμά και κόρη / Μπαμπάς και παιδί. "Matching" = "ασορτί" throughout (was mixed "ταιριαστά", "που ταιριάζουν", "Ταίριασμα"). Trunks = "μαγιό σορτς" (was "κορμούς", "μπαούλα", "Κοντό πανταλόνι αθλητών"). Register: polite plural (Δείτε, Ανακαλύψτε, Ξεκινήστε), consistent.

## Changes: 134 keys

- 47 UI keys. Most important: `products.product.free_shipping_short` said "Δωρεάν αποστολή" (free shipping) -> "Περιλαμβάνεται τυπική αποστολή". Others: compare-at price ("Συγκρίνετε στο" -> "Αρχική τιμή"), "Δόσεις" (instalments) -> "Ανά", matching-set strings, return-policy lines 2-4, "Ασφαλής Logistics" -> "Υποστήριξη αποστολών", "Ολοι" -> "Όλα", maternity "Μητρότητα" (motherhood) -> "Εγκυμοσύνη", "Νέες αφίξεις" -> "Νέα προϊόντα", "checkout" -> "ταμείο", search placeholder, product navigation phrasing, menu items.
- 87 collection keys: rewritten guide/intro/meta for daddy-me shirts and tees, couples, couples tees, family sets, maxi dresses, family swimwear, swimsuits guide and FAQ, all-outfits meta; broken H1s and tab titles ("Ζευγάρια που ταιριάζουν" = "couples who match", "Ταίριασμα Rompers", "Ταίριασμα κάτω", "Συνδυαστικά ρούχα", "Συντονισμένες αναζητήσεις για αυτόν και αυτήν").
- Truth: no "δωρεάν" left anywhere in el.json; no stock/warehouse/fast-shipping/review/bestseller/date claims added; "weddings" dropped from the dad-and-son shirts intro (as in other locales); maternity title untouched (Experto SEO's photoshoot title).

## Release

(rounds below)

### Round 1: STOPPED, export reverted it

- 09:26Z lock taken (re-read after 5 s). Commit 5761705 (20 UI keys: free_shipping_short, search, compare-at price, return policy lines, etc.). Read-only listing: only `locales/el.json`, 20 keys, all mine. `sync-locales --apply` upserted el.json (backup `ops/organic/receipts/2026-11-27/theme-locale-before-20261127T092656Z`).
- Shopify export d7aa4b6 ("Update from Shopify", within the 3-minute hold) put the 20 OLD Greek values back on main, and `sync-locales` then reported "locales in sync", i.e. the live theme also holds the old values again. 0 of 134 on origin.
- Per rule: not re-applied. Remaining 114 keys not committed. Lock released 09:30Z; work copy colcopy10 finished.
- Likely cause (not verified): Greek has Admin theme-translation content (Translate & Adapt / ONLINE_STORE_THEME locale content) that Shopify writes back over the file, as noted for `standard_delivery_window` in `delivery-statements-2026-11-26.md` ("also the Admin theme-translation copy (ONLINE_STORE_THEME and LOCALE_CONTENT, 20 locales)"). The other languages released today (nl, pl, sv, pt-PT, pt-BR, da, no, fi) held; el did not. Needs a read-only check of `translatableResources(resourceType: ONLINE_STORE_THEME_LOCALE_CONTENT)` for el before any retry.
- Prepared and validated values: scratch `el_all.json` (134 keys: 47 UI + 87 collection).

## Why round 1 did not hold (read-only investigation, 2026-11-27 ~09:40Z)

1. Admin theme translations (`translatableResources`, ONLINE_STORE_THEME and ONLINE_STORE_THEME_LOCALE_CONTENT, theme 133290917985): Greek has 5,389 / 5,298 stored values, the same counts as sv, da and fi. For my keys the Greek store holds exactly the old text that reappeared: `products.product.free_shipping_short` "Δωρεάν αποστολή", `general.search.search` "Αναζήτηση", `products.product.quantity.multiples_of` "Δόσεις {{ quantity }}", `products.product.price.compare_at_price` "Συγκρίνετε στο {{ price }}" (outdated false; the API gives no updatedAt). sv and da hold their current file values ("Standardfrakt ingår", "Ordinarie pris {{ price }}", ...).
2. So there is no extra Greek-only translation layer: every language has the same Admin store, and it is the same content as the theme's locale file. The difference is only that the Greek store went back to the old text.
3. Git: `d7aa4b6` (shopify[bot], 09:27:10Z) touched only `locales/el.json` (20 lines), exactly my 20 keys, back to the old values. It came 30 s after my commit 5761705 (09:26:40Z) and 14 s after my upsert (09:26:56Z). In the whole history of el.json the bot has 5 exports (this one and four in April), the same count as sv.json: no sign of an app rewriting Greek repeatedly.
4. Reading: a delayed export of the pre-change theme (snapshot taken before my upsert landed) was committed to main, and the GitHub-connected theme then pulled that commit back into the live theme. That is why both main and the live theme reverted (this morning, the live theme had kept the new values and only main went back). It is a race between Shopify's pull/export and the upsert, not a translation app.

## What it would take (not done)

- Same retry, with the race avoided (CEO/coordinator decision, no owner step): commit, then wait until the bot's own "Update from Shopify" for that commit has landed and `sync-locales` shows the expected drift, only then `sync-locales --apply`, then hold and confirm; or commit only and let the GitHub pull carry it (no upsert), then check live with `sync-locales`.
- Alternative: write the same 134 values with Admin `translationsRegister` on the ONLINE_STORE_THEME_LOCALE_CONTENT resource for `el` (needs the key digests; it is a production translation write, so it needs explicit approval and must still be followed by a matching commit so main does not overwrite it).
- Owner-only: nothing required by this evidence. If the owner has automatic translation switched on for Greek in Translate & Adapt, turning it off is his setting; the data does not show that it is on.

## Retry with the corrected order (09:32-10:24Z): all 134 keys held

Order per round: lock (write, re-read after 5 s) -> `ceo_worktree.py commit` -> wait 90 s -> fetch, check main still holds the values -> `sync-locales` read-only -> apply ONLY if it lists just my el.json keys (separate call) -> hold 3 min -> fetch, check main and `sync-locales` -> release lock.

| Round | Commit | After 90 s | Apply? | Export during hold | Main after hold |
|---|---|---|---|---|---|
| 1 (test, the 20 UI keys) | e37208a | in sync, no bot export: Shopify had already pulled main into the theme | no | none | 20/20 |
| 2 | 5de582c | 20 keys differ | yes | 008c068 kept values | 40 |
| 3 | e77ce14 | 20 differ | yes | 4106f01 kept | 60 |
| 4 | bfc5866 | 20 differ | yes | ec618b3 kept | 80 |
| 5 | 3106ed2 | 20 differ | yes | 8fac127 kept | 100 |
| 6 | 26fd177 | 20 differ | yes | c08533c kept | 120 |
| 7 | fc6dc22 | 14 differ | yes | 072353a kept | 134 |

Final: main holds all 134 values; `sync-locales` "locales in sync". Each listing showed only `locales/el.json` with my keys. Work copy finished, lock released. (A first attempt at round 3 failed before committing because of a shell argument bug in my helper; the dirty work copy was discarded and rebuilt; nothing reached main.)

Rule that worked (proposed for everyone): never apply in the same minute as the commit. Commit, wait about 90 s for Shopify's GitHub pull/export of that commit, then list read-only and apply only the drift that is still there; then hold 3 minutes and confirm. The earlier failure was the opposite order (apply 16 s after the commit), which let a delayed export of the old theme win.

Live readback (built-in browser, own tab, 3 loads >= 10 s apart, cart emptied, no checkout): `/el/collections/swimsuits` lang el, tab "Ασορτί μαγιό για όλη την οικογένεια | Μαμά και κόρη", guide title and FAQ question 3 new, no "κορμούς"/"μπαούλα", no "Δωρεάν"; `/el/products/heart-button-mommy-and-me-cardigan-dress-sets` shows "Περιλαμβάνεται τυπική αποστολή" and "Επιστροφές 30 ημερών", no "Δωρεάν", no "Συγκρίνετε στο"; `/el/cart` shows "Τυπική, περιλαμβάνεται", "Εκτιμώμενο σύνολο", "Ολοκλήρωση αγοράς", returns line, no "Δωρεάν". Overflow not measured (pane hidden). Not reviewed in this unit: home category copy, callouts, journal, article strings, customer addresses/orders.

## Calidad V131 follow-up (10:29-10:36Z)

- Fixed: `display_titles.valentines` "Ασορτί ρούχα για τη γιορτή του Αγίου Βαλεντίνου"; Greek guide snippets (`collection-guide-daddy-me`, `collection-guide-swimsuits`, 3 places) "μαγιό βερμούδες" -> "μαγιό σορτς", the term el.json uses. Commit 5109f64; same order (commit -> 90 s -> listing showed only my 1 key + 2 snippets -> apply -> 3 min). Export 8e01b5b kept both; `sync-locales` in sync, `sync-theme` 0 differ; lock released, work copy finished.
- "Αποστολή σε Γερμανία" with Spain: not a translation error. The Greek keys use the variable (`Αποστολή σε {{ country }}`, like English). Server HTML of the same PDP in /el, /es and /de with the session country ES (fetched read-only from an existing tab, 10 s apart) shows Spain in all three: "Αποστολή σε Ισπανία", "Envío a España", "Lieferland: Spanien", estimate 19-26 days. Not reproduced. The built-in browser shares one cookie/session across sessions; at that time another session was on /de pages, so the most likely cause is that the shared session country was switched to Germany by another test. No change made.
