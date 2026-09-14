# Coral Blossom copy repair — independent preflight

Reviewed 2026-09-09. Reviewer did not build or execute the repair. Confidence: high for structural preservation and source-image interpretation; medium for multilingual editorial quality.

**Verdict: PASS — scoped copy repair, subject to fresh-state and readback conditions below.**

Final review is bound to `coral_copy_plan.json` SHA-256 `2815b91dc274ae26aa975430eca224cc92a3becf2fb201d700ab7c0f3e46cefb`, resource `gid://shopify/Product/7607764287585`, and its 21 body changes. No external writes were made during this review.

Both required corrections are now verified, each with a count-one builder guard:

1. pt-BR design text: `para mãe e filho` → `para mãe e filha`, correcting son to daughter.
2. fi design text: `joustava hame` → `laskeutuva hame`, preserving flowing-skirt meaning without asserting stretch.

The bounded delta pass passed 166 checks. Reversing just these two after-body edits, their hashes, and their two count metadata entries reproduces the entire previously reviewed plan exactly (SHA-256 `5fbf5ab68b40191ef96a252f2cb531222e7232946b03e05b5cedbef7535f33af`). The other 19 after-bodies, complete before snapshot, replacement paragraphs, preservation scope and rollback are unchanged. Reversing the corresponding builder additions also reproduces its prior hash. The reviewer edited only this review file.

**Passed:** 300 independent checks verified before/after hashes, exactly one unchanged size table per locale, permitted retained list items, removal of fabric/care and internal draft/chart/source paragraphs, insertion and uniqueness of the replacement paragraphs, Spanish correction counts, and unchanged image/link targets. The 20 translated buying-choice and measurement-note pairs reasonably preserve the English meaning: one dress per selection, mother/daughter dresses sold separately, all hip and Mother XL dimensions explicitly estimated, and comparison of bust, waist and dress length. The three Spanish corrections are appropriate.

The original `source-size-chart.png` provides adult S/M/L and five child sizes, with bust, waist and dress length. It supplies neither hip nor Mother XL dimensions. `source-selector-mother-xl.png` offers XL but proves no dimensions. The new notices disclose this limitation; they do not validate the estimates or the existing age/height labels.

**Execution conditions:** fresh before-state hashes must match all 21 bodies. Allow only English `descriptionHtml` plus the 20 existing `body_html` translations. Preserve all 21 table byte strings, nine complete variant records and prices, product title/handle/status/URL/SEO, and all 80 non-body translation values and flags. Stop on concurrent drift. After writing, independently compare every body with the reviewed payload and all preserved fields with the frozen baseline; expected product update timestamps may change.

**Rollback:** restore the exact English before-body, read its fresh translation digest, then restore the exact original translated bodies using that digest. For partial completion, identify actual changed locales before recovery. Do not rewrite unrelated fields.

Legacy literal wording and stray leading letters in some locales remain editorial work. This preflight does not certify native-language polish, rendered checkout, shipping, purchase tracking, or qualification for paid traffic.

## Independent post-write verification

**PASS — 295 independent checks**, completed 2026-09-09 18:25:35 UTC against the saved Shopify readbacks recorded at 18:23:24 UTC. No defect was found within the reviewed scope. Evidence: `coral_copy_after.json`, SHA-256 `d610685bba72ad38c2f4fc0839880a01a973dab0730bdf6c65eca7df7ab858d4`. The original before snapshot and final reviewed plan hashes still match their preflight bindings.

Checks were recomputed from raw before, plan and after values, independently of the executor's pass flags:

- All 21 actual bodies match the reviewed after-values and hashes exactly. All 21 size tables retain their exact original bytes and hashes; body URL targets are unchanged.
- All 20 translated bodies are current (`outdated=false`). All 80 non-body translation rows, including values, locales, keys and outdated flags, are deeply identical to the baseline.
- All nine complete variant records and prices, SEO, product identity/title/handle/status/URL, shop identity and 21 shop-locale settings are unchanged. Only the captured product `descriptionHtml` and expected `updatedAt` changed.
- The five non-body source translation-content records, including digests, are unchanged. The English body digest matches its new content. Both after-state source-content readbacks and the duplicate Spanish translation readbacks agree.
- Spanish, Portuguese and Finnish corrections are present. Both saved GraphQL readback envelopes contain no errors; the evidence records empty source and translation mutation `userErrors` arrays.

The reviewer performed no external writes and edited only this review file. **Rendered validation: NOT RUN.** These API readbacks do not prove public rendering, checkout/shipping, purchase-event delivery, native-language polish or paid-landing qualification. The measurement-estimate limitation and exact rollback method above still apply.
