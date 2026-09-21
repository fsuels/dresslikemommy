# Czech collection heading correction and local main sync

One supported save updated the existing unpublished theme137888792673 on2026-09-15 at05:07:39UTC. The only changed locale value is `sections.collection_seo.display_titles.dresses`: “Šaty pro mámu a já” becomes “Šaty pro maminku a dceru”.

The exact saved Czech file was copied to local `main`. The other782 locale values, longer metadata title,526 other draft files, and all525 MAIN file records and metadata are preserved. The seven additional committed local files listed in SEVEN_ADDITIONAL_LOCAL_FILES.json remain intact and are not part of the accepted draft.

Source verification passed:39 root before checks,49 independent action-state checks, an immediate exact fresh-state match before the single save, and40 root after checks. The fresh actual527-file source binding is ACTUAL_527_SOURCE_BINDING.json. Independent final after-review is recorded separately.

Both exact Czech collection paths were checked at1280×720 and390×844. Desktop headings are readable. At phone width the heading exists in source but an existing `.collection-hero { display: none !important; }` rule hides it on both routes. The two source CSS files are identical in live MAIN and draft, so the one-string correction did not introduce this gap. **Mobile visible-heading acceptance FAILED.**

The observed Coral Blossom product-card click retained the Czech product path, with both localized purchase instructions visible and cart0 preserved. That result applies to the existing preview session; it does not resolve the separately observed cookie-independent direct-arrival redirect to English.

All temporary browser tabs were closed and the viewport reset. No country/language controls, cart, checkout, products, collection data, tracking, feed, paid settings, MAIN files, publication or Git push were changed.

GitHub `main` remains at e077c69e06bbc729da121533a480c55456b079ba. Pushing is held while it is connected to the current MAIN theme and source/publication acceptance is unresolved. This packet records a completed exact source correction and a remaining mobile acceptance gap; it does not claim complete GitHub sync, publication, a fresh PageSpeed result or conversion lift.

Next: prepare and independently review the smallest mobile heading-only correction, preserving image suppression and unrelated local files. Parent task01a08223 owns canonical integration and the exact next external scope; no new user approval question is needed for preparation.
