# Catalog and article translation release

Confidence: H for the released values and checks below. Overall status: PARTIAL — the qualified translation repairs are live; source-content decisions remain.

Audited all 238 active online-store products and 67 published articles across all 21 published languages, including the English source. The audit covered 4,760 product-title and 1,340 article-title comparisons, product option/metadata/body fields, size charts, article bodies and storefront article labels.

13,220 distinct product/option fields and 531 distinct article fields now have verified repaired values. The 15,645 successful field writes include refinements to fields already repaired. The final batches corrected native size-chart terminology and replaced 154 outdated descriptions with complete translations of the current source. Source measurements, units, blank cells, garment facts and explicit uncertainty were preserved. The translation-token fix and its regression checks were included in main at 4296ae9.

Each write used a fresh publication check, source value/digest check and exact prior translation check, followed by an exact current-value readback. Independent reviewers checked language meaning, chart dimensions and source preservation. The final review reconciles every recent intent with a successful receipt; no recent mutation is pending. Frozen inputs retain 28 superseded planning-hash annotations, documented in a sidecar; their authoritative before-values, runtime guards and released values all match.

Public checks covered all 20 non-English languages for product descriptions, native size-chart labels and article labels. The fully refreshed crochet product was checked in every language; final Russian, Swedish and Finnish repairs were checked on their affected routes. Narrow-screen checks covered product prose, right-to-left/article layouts and the Swedish fit guide, including cm/in conversion. These are representative rendered checks, not a claim that every catalog URL was manually browsed. The complete released fields have exact API readback evidence.

The existing live theme remains dresslikemommy/main (133290917985). All 37 changed theme files match the reviewed source; processing and processingFailed are false. Theme changes use GitHub main synchronization. Product/article resource translations also require the guarded Shopify Admin API; their canonical verified values and receipts are versioned in this same repository.

Remaining source decisions:

- 443 product-language fields: 276 descriptions for search engines, 129 titles for search engines, 34 product descriptions and 4 titles. They involve conflicting garment/material/design or bundle facts, return-policy claims, or measurement evidence. Of these, 20 lack measurement provenance; they are unknown, not proven false.
- 142 article-language fields: 132 shipping-related bodies, 8 sun-protection bodies and 2 obsolete-threshold metadata fields. The exact proposed English policy/claim corrections remain unapplied pending the source decision.
- 80 title watches across four products remain source-fact watches, with four overlapping the 443 above; they are not 80 additional proven translation defects.
- Three precise Danish article-linked product destinations returned 404. Their seven source links appear in four English articles. No replacement product was guessed, and no all-language routing failure is inferred.

The known native-header, outdated-header and broken-placeholder findings are resolved. Narrower routing observations and ads negatives are preserved. English editorial workflow wording remains faithfully translated where present; editing that source copy is a separate content task.

Evidence: RELEASE_PROGRESS.json; verified_translation_values/; releases/; release_review_archives/manifest.json; review/final_independent_release_review.json; review/final_remaining_dispositions.json; review/full_source_public_20locales_final.json; review/theme_final_settled_readback.json. GitHub main and the existing live theme were read back after release commit 15d4d20100351d9a87990b3423acbd5803ea946b. The verified sync receipt is review/main_sync_receipt.json.
