# Multilingual storefront release — September 22, 2026

Status: IMPLEMENTED and VERIFIED LIVE. Canonical repository is `fsuels/dresslikemommy/main`; the existing published Shopify theme is133290917985 (`dresslikemommy/main`). No alternate live site or new theme was created.

## Released repairs

- Shared header/footer links, collection navigation, journal interface and homepage categories use locale keys and preserve the selected language. Product classification uses stable handles, so translated titles do not alter shirt/T-shirt filtering or counts.
- Repaired867unique Shopify translation fields across20non-English locales and23resources: homepage/collection copy, policy/help pages, journal settings and the first7journal article cards. Every changed field was read back exactly with `outdated=false`. Two English FAQ/About bodies were aligned with existing published policy facts; underlying policy terms were preserved.
- Reviewed28additional apparel-category labels across18languages, including golf/mechanical meanings of tees and incorrect swimwear/button-shirt labels. Source is committed in7f9a05f; all18changed files now byte-match the live theme and all28corrected labels were verified on published pages.

## Acceptance evidence

21published languages: ar,cs,da,de,el,en,es,fi,fr,he,hi,it,ja,ko,nl,no,pl,pt-BR,ro,ru,sv. Portuguese uses `/pt`.

631unique public route checks passed the scoped missing-token, rendered404, language-preservation and footer-key checks:30routes per language plus the Spanish privacy destination. All21locales showed the same23shirts and11T-shirts with localized counts; the parent shirt query retained the same23products. All return pages were revisited after the final17body repairs. Russian/Swedish journal settings and all31supplemental card fields were retested publicly.

Full Theme Check returned zero findings. Twelve filter regressions, all35locale-file key/placeholder parity checks, JavaScript syntax and independent Liquid review passed. Independent content reviews covered meaning, source/before guards and receipts; the final836-field release review passed11checks, followed by a separate31-field journal review/readback.

Representative desktop1366×900 and narrow390×844 checks passed for Swedish journal layout, Danish/Hebrew help accordions, translated mobile footer/shipping panel, and Arabic collection text fit. Viewport emulation was restored. Arabic/Hebrew checks do not constitute a complete RTL design audit.

Shopify finished the final import at19:16:20UTC with processing=false/processingFailed=false. The final528-file manifest matchesmain, and all18changed locale bodies match byte for byte. The public checks confirm all28corrected apparel labels. There are no remaining local-only storefront fixes from this task.

## Preserved limits

`/collections/family-swimsuits` still redirects to the broad family collection while preserving language; this does not prove a dedicated swimwear destination. Narrower routing negatives remain unchanged. This release grants no campaign activation or spend authority.

The existing17TRACK widget has documented native result languages for17non-English locales. Arabic/Hebrew/Hindi page controls are translated, but native carrier-result language support remains unknown and English fallback is retained. No actual carrier lookup, cart/checkout submission or order was created.

First-page journal card copy is repaired; later article pages and all product/article bodies are not comprehensively certified. No product facts/prices/stock, advertising, budgets, tracking configuration, billing, accounts or underlying policy terms were changed. No conversion/profit improvement is claimed.

## Evidence and rollback

Theme commits0dd8c90 and7f9a05f; reviewed content recordb53f438; final evidence commit is recorded in Git history. Main/theme manifests, mutation batches, independent reviews, exact before/after snapshots and `public_acceptance.json` are in this packet. Shopify native same-theme Reset to latest commit recovered stalled GitHub events; manifest metadata may update before body/public propagation, so source checksums alone are insufficient.

Rollback: use the recorded before values/digests for scoped translations and revert the exact theme changes on main, then verify the same existing live theme. Do not reset unrelated work or publish a separate draft.
