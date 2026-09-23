# Article chrome localization — implementation handoff

Confidence: H for source changes and local validation. IMPLEMENTED locally; Git, Shopify sync and public verification are root-owned and NOT RUN by this lane.

Changed 37 source files: `sections/main-article.liquid`, `snippets/style-journal-internal-links.liquid`, and all35 storefront locale JSON files. The precise list is `changed_files.json`; the patch against each captured before-state is `exact_source_changes.diff`; before/after SHA256 bindings are in `before_manifest.json` and `check_results.json`.

## Changes

- Added20 `storefront.article` keys with manually authored, complete translations in the20 published non-English locales: ar, cs, da, de, el, es, fi, fr, he, hi, it, ja, ko, nl, no, pl, pt-BR, ro, ru, sv. Default English values match the prior labels. No language-provider/API generation was used.
- Reused seven existing keys/groups for journal title, reading time, shop labels, category labels, and neutral collection descriptions. Article chrome now includes localized breadcrumb accessibility label, editor role, TOC, recommended-products heading, author label and bio, comparison card, collection shopping headings, related articles, collection-guide labels and CTA defaults.
- English case-specific collection titles/captions and selection/routing blocks remain unchanged. Only non-English collection teaser output is replaced after collection resolution using `collection-seo-fallback`'s translated display title and the existing translated `storefront.collection_fallback_description`. All12 selected collection handles have native title keys. Unknown explicit collection overrides continue to use that collection's own title; its resource translation remains a data dependency.
- If a selected collection object is absent, clear its non-English title/caption before deriving the CTA, so an English case-assigned title cannot label the fallback collection index. Blank-object link guards remain in place.
- CTA JavaScript uses `t | json` for translated fallback text and a locale-aware `routes.collections_url` fallback. English fallback wording and English button label retain their exact previous values. Destination handles, metafield selection logic, HTML links and tracking attribute names are preserved.
- Mixed raw/translated shared-snippet values use `escape_once`: Shopify's `t` output is escaped already, so adding `escape` again could display HTML entities. Raw English text still receives HTML escaping.
- Root explicitly expanded ownership to the14 unpublished locale files only to add the same20 exact English defaults: hu, id, nb, th, tr, vi, zh-CN, zh-TW, hr-HR, pt-PT, ro-RO, lt-LT, sk-SK, sl-SI. These are explicit fallback values, not reviewed translations; no published language choice changed.

## Checks actually run

- `python3 .../article-chrome/check_patch.py`: PASS, 2440 assertions. All35 locale dictionaries retain every pre-existing value and every pre-existing byte outside the added article object; exact20-key order, nonempty text and placeholder parity pass. Every referenced/reused key resolves in all21 published/default dictionaries. All20 new keys differ from English in each published non-English language. All12 selected collection titles resolve. Existing English tailored assignments, complete article/collection selection blocks, HTML hrefs and tracking attribute names are preserved.
- Bundled Node running `check_inline_cta.mjs`: PASS for all21 published/default locales. The actual edited inline JavaScript, with its narrowly substituted Liquid literals, parses and executes against DOM fixtures. Tests cover missing-data translated text/label/route, chosen-data precedence, literal quote/ampersand/angle-bracket text via textContent, tracking, insertion point, short/missing content, and English before/after equivalence. This is an actual-script unit check, not a Shopify Liquid render or browser QA.
- `node --check check_inline_cta.mjs` and Python compilation of manual translations, implementation helper and validation script: PASS.
- Installed Shopify CLI `theme check --path /Users/fsuels/Projects/dresslikemommy --output json`: PASS, exit0, zero findings (`theme-check.json` = []). The first run identified280 missing-key findings in14 unpublished locales; these were resolved within root's explicit expanded ownership by the unchanged English fallback values.
- All37 current source SHA256 values match the validation output.

The Shopify Liquid skill's public documentation search ran with instrumentation opted out. Its supplied validation entry point was attempted but could not load its missing `@shopify/theme-check-common` dependency; evidence is `skill-validation.txt`. The installed CLI Theme Check supplied the independent local validation fallback. No dependency installation or skill-file modification was made. System `node` had a missing Homebrew library, so checks used the observed bundled Codex Node runtime.

NOT RUN here: independent translation review by another author, actual Shopify rendering, desktop/mobile/browser checks, Git/index changes, live theme writes or connector calls. Root must integrate the reviewed37-file change to `main` and verify theme sync plus the affected article and collection-guide routes. Full product/article translation completion is not claimed.
