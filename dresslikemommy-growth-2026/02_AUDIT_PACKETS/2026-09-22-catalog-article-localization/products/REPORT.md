# Product localization audit

Status: VERIFIED exhaustive inventory and field audit; localization defects remain. No live writes, provider requests, Git changes, or canonical-state edits were made in this lane.

Read window: 2026-09-22T21:46:12.951642+00:00 to 2026-09-22T21:51:07.177305+00:00. Before and after published counts are EXACT 238.

- 238 ACTIVE online-store products; 238 non-null onlineStoreUrl values; all five cursor pages, terminal hasNextPage=false.
- 21 published locales: English source and 20 translated locales.
- 477 options and 3,458 option values inventoried without array truncation; 4,925 variants counted EXACT. Variant display text is represented by options/values; combinations, SKUs, prices and inventory were not fetched.
- All 4,173 identified resources returned in 105 translation query pages; no missing resource IDs. 93,831 existing rows retained with explicit locale and market provenance; zero unexpected alias-locale or market rows.
- 5,054 available source fields and 101,080 nonempty field/locale checks. Vendor and handle translations excluded; title, body_html, product_type, available meta_title/meta_description and nested name fields included.
- 67 active option values are linked-value backed and return no translatableContent. All 67 linkedMetafieldValue references were read back; no digest was invented. See linked_option_values_before.json and resources_without_translatable_source.json.

## Flagged records

8,890 field/locale rows across 196 products: name 6,574, title 398, body_html 508, product_type 298, meta_title 450, meta_description 662.

Reasons overlap: missing 7,487, source_english_paragraph 377, outdated 925, source_english 103. Outdated flags indicate a source change, not proof the existing translation is wrong.

The 337 offline language-review candidates remain separate from deterministic flags. Apple NaturalLanguage ran on device; no remote language or translation service was used. This is not a complete manual semantic review or native-speaker certification.

Identical legitimate labels and standard size codes were manually excluded (including Spanish Color, Romanian Adult + size, French/Nordic Type, and common apparel loanwords). See audit_catalog.py for the exact allowlists.

## Exact cached workload

713 distinct source strings; 3012 source/locale pairs; 78,837 unique source words (329,387 when repeated per target locale).

Historical caches contain a different exact-match candidate for 5,455 rows; 3,363 rows have no exact cache; 72 have only source-equal cache values. Caches are untrusted candidates and require meaning/structure review; no automatic reuse is approved.

## Priority Danish case

All three homepage-observed wrong-language product titles have correct current global Danish title records, with outdated=false and no Danish override in any of six active markets. Parent isolated the homepage symptom to recently-viewed cart history. The valid product title records are preserved. See priority_danish_before.json.

## Evidence and limits

Raw product inventory and translation batches contain source values, opaque Shopify digests, exact current translations, locale and market IDs. defects.jsonl binds each flagged field to its source digest, before hash and raw batch. grouped_source_workload.jsonl records exact cache provenance. No mutation payload has been executed.

Global translations are exhaustive within the specified fields. Market-specific values were checked only for the three reported Danish cases. Arbitrary metafields, image alt text, media, handle/vendor text, full variant combinations and rendered PDP/checkout behavior are outside this read-only pass.

Subsequent candidate preparation is separate from this frozen audit; option_cohort_candidate.json remains pending independent review and parent freshness checks.
