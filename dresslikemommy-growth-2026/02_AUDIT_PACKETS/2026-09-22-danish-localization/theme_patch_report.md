# Danish theme patch — local candidate

Confidence: H for source identity, scope preservation and narrow checks; M for model-reviewed Danish prose. Browser rendering, customer-language acceptance and upload are NOT RUN by this worker.

Status: IMPLEMENTED locally; PASS_NARROW_SOURCE_CHECKS_RENDER_NOT_RUN. No external writes, Git writes, root theme edits or shared-canonical edits.

Target prepared for parent review: existing UNPUBLISHED theme `137888792673`. Eleven files only, based exactly on the fresh theme API payloads `theme_137888792673_before.json`, `theme_extra_before.json`, `theme_navigation_before.json`, `theme_blog_before.json`. Every before body matches its API MD5. Parent owns any later claim, upload, refreshed source binding and preview acceptance.

Changes:

- `layout/theme.liquid`: Danish-only homepage title and description; other page types unchanged.
- `sections/footer.liquid`: Danish journal summary and CTA prefix; existing Danish alias/key repairs and Italian proposal unchanged.
- `sections/main-blog.liquid`: 17 Danish branches for spotlight, article labels/read time, about text, newsletter copy, email placeholder/accessibility label and subscribe button. The existing 10% statement and every form attribute/destination remain unchanged. The three platform-translated heading/intro settings and source fallbacks remain unchanged.
- `snippets/home-category-localized-copy.liquid`: 11 Danish spelling/accent repairs inside its existing da branch.
- `snippets/facets.liquid`: only the existing family-collection helper sentence gets a Danish branch. Filter behavior is unchanged.
- `snippets/collection-seo-fallback.liquid`: after existing keyed translations, Danish-only generic meta/body fallback uses the localized display title and neutral buyer guidance. No new fabric, stock, shipping, rating or size claims.
- `snippets/collection-merchandising-callout.liquid`: Danish text for its existing six handle branches, labels and three count/shipping/return items. Same existing collection handles; only Danish secondary/tertiary links add `routes.root_url`. Primary product-grid anchor unchanged.
- `snippets/header-mega-menu.liquid`, `snippets/header-drawer.liquid`, `snippets/header-mega-menu-feature-card.liquid`: Danish overrides for forced Family Matching title, existing feature description, card CTA and labels. Routing/visibility/media selection logic unchanged. Existing marketing claims are translated, not newly verified.
- `locales/da.json`: 38 existing values corrected; 783 keys retained with all interpolation tokens preserved. Includes requested English values, two mixed-English swimsuit paragraphs, exact false translations of trunks/twinning, and breadcrumb/category labels. The already-Danish dresses meta-description remains byte-identical. No new locale keys or other locale files.

Source bindings:

| File | Before/API MD5 | Candidate MD5 |
| --- | --- | --- |
| layout/theme.liquid | 6b2199c45524b6651e468dec73470ce6 | 1d15646c02e32ccc3fb1e888b8d04bc2 |
| locales/da.json | 5e5dde28789c79d5813487647c4dbd72 | 90962b170b6ae87a2bf69a1ac0a0060f |
| sections/footer.liquid | 0975d039b49a52684fd140064e639990 | 30c20bfccb3ddeb6d9cc96bad0ccca39 |
| sections/main-blog.liquid | 5a8145ffa143e7259c2438b75d9b45fe | 699fc5a412763769244b5695669e1429 |
| snippets/collection-merchandising-callout.liquid | 60f695aa01eaa42741e32d5f5391fe49 | b3292116ce2bb4d513bc4161ae356d09 |
| snippets/collection-seo-fallback.liquid | 9ff6ec2d6f0911298e957f9d10bbd49c | f6a18aa44aabe7d850a73f3c5b055c23 |
| snippets/facets.liquid | c34e3d7ed9e2ad597caabe51d64a6338 | ccc20a9fae8c5d72e295a079809fc783 |
| snippets/header-drawer.liquid | ea25b3a082de86b0fd30435c440f76b6 | f98c963f7f29ca56298b307ff979f2ed |
| snippets/header-mega-menu-feature-card.liquid | 51d9f93d1d5b5c33a421c45db9fc3167 | 187bd044fa81b2413e9699c4a7705f95 |
| snippets/header-mega-menu.liquid | 5295b2fa63f21d89c58d0f1129b889dc | d3431b77dab9e94377f44a7aa1a7090a |
| snippets/home-category-localized-copy.liquid | cae2e959cc9cbc48272fb3836b1520b0 | d0c340bdab483c441dcba9084ab483f0 |

Candidate SHA256 values are in `theme_candidate/MANIFEST.json`; current manifest SHA256 `720f1709b2dafb6693ca7a76ae3d77f33487cac5fc5362b7954be65253e54714`. Exact diff: `theme_candidate/changes.diff`. Inverse source: `theme_candidate/before/`. Candidate upload bytes: only the 11 entries under `theme_candidate/theme/`.

Verification actually run:

1. Shopify Liquid skill `scripts/search_docs.mjs` succeeded; results saved in `theme_candidate/search_docs.json`. Official locale documentation: https://shopify.dev/docs/storefronts/themes/architecture/locales/storefront-locale-files .
2. Required skill `scripts/validate.mjs --theme-path ... --files ... --model gpt-6 --client-name codex --client-version desktop --artifact-id danish-theme-95aad16d-61dd-446c-a2bd-34c9f511294e --revision 1` attempted; BLOCKED by installed skill missing `@shopify/theme-check-common`. Original failure saved as `theme_candidate/validate_candidate.txt`. No skill/package files modified and no dependencies installed.
3. System Shopify CLI launcher failed before checking due missing Homebrew `libsimdjson.29.dylib`. Recovered using verified bundled Node `/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node` with existing `/opt/homebrew/lib/node_modules/@shopify/cli/bin/run.js`.
4. Existing official Shopify CLI Theme Check ran on both 11-file snapshots. Each exited 1 with the same **258** findings: 109 missing translation keys, 87 missing templates, 60 missing assets and 2 schema-name findings in these dependency-incomplete snapshots. **Zero new offenses; zero syntax offenses.** Comparison uses file/check/message/severity, ignoring shifted line offsets. Do not call this a clean full-theme lint pass. Raw reports are `theme_check_before.json` and `theme_check_theme.json`.
5. `python3 theme_candidate/check_patch.py` passed: all source/candidate hashes, JSON/schema parsing, identical locale key set, 38 exact value changes, all 783 keys' placeholders preserved, changed HTML href values preserved, destination literals preserved in every Liquid file, and non-Danish source projection unchanged (whitespace-normalized). This is a static branch proof, not a rendered browser test.
6. `git diff --no-index --check before theme`: exit 1 because snapshots differ; no whitespace diagnostics. Captured and classified by the check script.

Residual limitations:

- No browser/preview control was assigned to this worker. Parent must verify Danish desktop/narrow homepage, collection fallback/callouts, header drawer/mega menu, journal/newsletter UI and footer after staging. Do not submit a newsletter or cart/order during this verification.
- Article/product bodies are outside the 11-file patch and may independently remain English. Known untouched mixed-English `sections.collection_seo.meta_descriptions.all` is outside the final scoped list and retains its pre-existing shipping wording.
- Parent observed translated homepage category custom labels can suppress helper captions because current helper matching uses English defaults. This source patch preserves that behavior; no mapping redesign.
- Existing marketing statements (standard shipping, 30-day return period, 10% newsletter incentive, best-selling/trending labels) are preserved from current source. This worker did not validate those business claims.
- Prior theme readiness cannot be reused after these bytes change. Fresh role/checksum comparison, parent acceptance, exact 11-file upload readback and source binding remain required.

Next action: parent independently reviews the frozen candidate and its narrow checks, then performs its authorized staged-theme workflow. No repeated discovery or duplicate platform translation registration is needed.

Continuation prompt: Review the Danish 11-file candidate against its before snapshots and MANIFEST.json, reconcile the assigned authority/claim, stage only those exact bytes to UNPUBLISHED137888792673 when authorized, verify checksums and affected desktop/narrow Danish routes, then renew source binding and acceptance while preserving all narrower routing negatives.
