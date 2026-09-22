# Danish follow-up patch

Confidence: H for source identity and narrow preservation checks; M for the zero-count cause until rendered readback.

Status: IMPLEMENTED locally, PASS_NARROW_CHECKS_RENDER_NOT_RUN. No external, root theme, Git or shared-canonical writes. Phase 1 packet is unchanged.

Three upload candidates under `theme_candidate_followup/theme/`:

- `layout/theme.liquid`: Danish news blog title `Stiljournal`. Danish generic meta-description on the untagged news index; existing nonblank tagged metadata preserved. The existing blank-description blog fallback is also translated when Danish. Tag/pagination suffix bytes, article metadata and other locales remain unchanged.
- `snippets/article-card.liquid`: Danish-only `min. læsetid` and `Læs artiklen`. The abbreviation works for both one and multiple minutes. Existing reading-time calculation, excerpt/title/body, image logic and all destinations remain unchanged.
- `locales/da.json`: adds `products.facets.product_count_simple.zero` and `products.facets.product_count.zero`, exactly mirroring their existing Danish `other` values and placeholders. No existing values changed; the 38 Phase 1 corrections are preserved.

| File | Before/API MD5 | Candidate MD5 |
| --- | --- | --- |
| layout/theme.liquid | 1d15646c02e32ccc3fb1e888b8d04bc2 | 8a1dd2bb52bde9f4d8803b55ebcd7c5f |
| locales/da.json | 90962b170b6ae87a2bf69a1ac0a0060f | 3ad0181cb1165661d4841d350b9dbf30 |
| snippets/article-card.liquid | 652cfa42e9e253269b716528206adf25 | 43dd4963c36e28bd9db253399976f3ad |

Full hashes and exact upload filenames: `MANIFEST.json`, SHA256 `0cbed925ef5fcd349d8d9c3c3d40863b526af7d0210e0eb9241d2b54de6dcd83`. Combined final local 12-file source list: `COMBINED_12_FILE_MANIFEST.json`. It merges the immutable Phase 1 candidate with these three replacements; it is not a fresh full remote source binding.

Evidence and checks:

- Before layout/da bytes match the Phase 1 upload after-state manifest on UNPUBLISHED137888792673. Article-card matches fresh `theme_article_card_before.json` MD5. Fresh English locale body matches `theme_english_locale_before.json`, MD5 `849b154af867761fd4682fbd2b3fcddd`.
- `search_docs.mjs` succeeded before changes. Shopify explicitly supports zero/one/other and other locale-aware forms through `t: count:`: https://shopify.dev/docs/storefronts/themes/architecture/locales/storefront-locale-files . Both fresh English and Danish source files lacked a zero form. This supports the candidate mechanism but does not prove missing zero caused the observed English label.
- Required skill `validate.mjs` attempted and BLOCKED by missing installed package `@shopify/theme-check-common`; preserved failure in `validate_candidate.txt`. No dependency/package changes.
- Existing official Shopify CLI Theme Check executed via bundled Node on both three-file snapshots. Both have 86 identical pre-existing dependency-incomplete findings, zero new findings and zero syntax findings. Exit status 1 for both; not a clean full-theme validation pass. Raw reports in `theme_check_before.json` and `theme_check_theme.json`.
- `check_patch.py` passed: hashes, zero-only locale additions, unchanged existing locale values/placeholders, byte-identical non-Danish Liquid projection, unchanged tag/pagination suffixes, unchanged href values and valid combined 12-file final source hashes.
- `git diff --no-index --check before theme`: expected exit 1 for different trees with zero whitespace diagnostics.

Residuals and next action:

- Parent must review/stage only the three current follow-up bytes, verify returned MD5s, then recheck Danish blog cards, blog title/meta and empty collection counts. Specifically test the observed `daddy-me-shirts` Danish/Denmark empty collection to determine whether explicit zero keys work. Do not declare that mechanism fixed without rendering.
- The empty collection remains an availability observation. No inventory, product publication, market availability or target-qualification claim is made or changed.
- Tagged pages retain their existing nonblank metadata and title suffix behavior. This does not certify translated article content or all tag destinations.

Continuation prompt: Review and stage only the three Danish follow-up files to the same authorized unpublished theme, verify MD5 readback, confirm the remaining blog/zero-count labels in preview, preserve empty-collection routing negatives, then renew the combined 12-file source binding and acceptance.
