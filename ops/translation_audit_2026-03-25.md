# Translation Audit - 2026-03-25

## Scope audited
- Source Shopify translation exports in repo:
  - `/Users/fsuels/Projects/dresslikemommy/Dress_Like_Mommy_translations_Mar-24-2026/`
- Claimed generated Shopify import CSVs outside repo:
  - `/Users/fsuels/project/Dresslikemommy/translations/`
- Theme locale files in repo:
  - `/Users/fsuels/Projects/dresslikemommy/locales/`

## Verified findings

### 1. Source export state
- Found `12` Shopify translation export CSVs in `Dress_Like_Mommy_translations_Mar-24-2026/`.
- Total source rows across all locales: `600,914`.
- Per-locale source rows:
  - `de`: `31,664`
  - all other audited locales: `31,625` each
- Non-empty `Translated content` already present in source exports:
  - `fr`: `14,540 / 31,625` (`45.98%`)
  - `es`: `14,203 / 31,625` (`44.91%`)
  - `de`: `42 / 31,664` (`0.13%`)
  - `id`, `it`, `ja`, `ko`, `nl`, `pl`, `pt-BR`, `ru`, `sv`, `th`, `tr`, `zh-CN`, `zh-TW`: `2 / 31,625`
  - `ar`, `hi`, `vi`: `1 / 31,625`
- Conclusion: the source exports confirm that French and Spanish are partially translated already, while the other added languages are effectively untranslated.

### 2. Claimed import CSVs exist, but only outside the repo
- The earlier agent claimed the generated `import_*.csv` files were in the repo. That is false for this repo path.
- They do exist at `/Users/fsuels/project/Dresslikemommy/translations/`.
- Found `19` import files there:
  - `import_ar.csv`
  - `import_de.csv`
  - `import_es.csv`
  - `import_fr.csv`
  - `import_hi.csv`
  - `import_id.csv`
  - `import_it.csv`
  - `import_ja.csv`
  - `import_ko.csv`
  - `import_nl.csv`
  - `import_pl.csv`
  - `import_pt-BR.csv`
  - `import_ru.csv`
  - `import_sv.csv`
  - `import_th.csv`
  - `import_tr.csv`
  - `import_vi.csv`
  - `import_zh-CN.csv`
  - `import_zh-TW.csv`

### 3. Structural validation of the import CSVs
- Total rows across all import files: `74,361`.
- Every import row matched a real source-export translation key:
  - key shape checked: `(Type, Identification, Field, Locale, Market)`
  - `missing_src = 0` for every import file
- Locale column matched filename locale for every file:
  - `bad_locale = 0` for every import file
- `Translated content` was non-empty on every import row.
- `Translated content` was never identical to `Default content` on any import row.

### 4. Coverage gap in the generated import CSVs
- These files are partial imports, not full-store translations.
- Coverage by locale compared to the source export:
  - `ar`: `2,384 / 31,625` (`7.54%`)
  - `de`: `4,073 / 31,664` (`12.86%`)
  - `es`: `292 / 31,625` (`0.92%`)
  - `fr`: `270 / 31,625` (`0.85%`)
  - `hi`: `2,778 / 31,625` (`8.78%`)
  - `id`: `2,778 / 31,625` (`8.78%`)
  - `it`: `5,084 / 31,625` (`16.08%`)
  - `ja`: `6,169 / 31,625` (`19.51%`)
  - `ko`: `6,169 / 31,625` (`19.51%`)
  - `nl`: `4,065 / 31,625` (`12.85%`)
  - `pl`: `4,117 / 31,625` (`13.02%`)
  - `pt-BR`: `5,065 / 31,625` (`16.02%`)
  - `ru`: `4,117 / 31,625` (`13.02%`)
  - `sv`: `4,100 / 31,625` (`12.96%`)
  - `th`: `2,778 / 31,625` (`8.78%`)
  - `tr`: `5,068 / 31,625` (`16.03%`)
  - `vi`: `2,716 / 31,625` (`8.59%`)
  - `zh-CN`: `6,169 / 31,625` (`19.51%`)
  - `zh-TW`: `6,169 / 31,625` (`19.51%`)
- Conclusion: importing these files would only translate a small subset of the store for each locale.

### 5. Quality problems in the generated import CSVs
- Many translated rows still contain significant English fragments or untranslated English phrases.
- Heuristic check: rows where at least 50% of meaningful English source tokens remained in the translated output:
  - `import_fr.csv`: `77 / 270` (`28.52%`)
  - `import_es.csv`: `74 / 292` (`25.34%`)
  - `import_nl.csv`: `646 / 4,065` (`15.89%`)
  - `import_de.csv`: `636 / 4,073` (`15.62%`)
  - `import_sv.csv`: `577 / 4,100` (`14.07%`)
  - `import_pl.csv`: `528 / 4,117` (`12.82%`)
  - `import_ru.csv`: `519 / 4,117` (`12.61%`)
  - `import_tr.csv`: `455 / 5,068` (`8.98%`)
  - `import_it.csv`: `424 / 5,084` (`8.34%`)
  - `import_pt-BR.csv`: `422 / 5,065` (`8.33%`)
- Representative examples:
  - `import_es.csv`
    - `Matching Family Outfits – Coordinating Looks for Everyone`
    - translated as `Combinados Familia Conjuntos – Coordinating Looks for Everyone`
  - `import_fr.csv`
    - `Matching Family Outfits – Coordinating Looks for Everyone`
    - translated as `Assortis Famille Tenues – Coordinating Looks for Everyone`
  - `import_ja.csv`
    - `Dresslikemommy | Mommy & Me Casual Dresses | Cute & Comfortable Outfits ...`
    - translated with large English fragments still present: `Dresslikemommy | ママ & Me Casual Dresses | Cute & Comfortable ...`
- Conclusion: these imports are not at a publish-ready quality standard.

### 6. Existing FR/ES source gaps that still need real work
- Missing source-export rows for existing French and Spanish are concentrated in:
  - `METAFIELD value`: `16,871`
  - `MEDIA_IMAGE alt`: `13,104`
  - `PRODUCT handle`: `1,408`
  - `PRODUCT_OPTION_VALUE name`: `1,398`
  - `PRODUCT_OPTION name`: `626`
  - `PRODUCT product_type`: `299`
  - `PRODUCT meta_description`: `88`
  - `COLLECTION body_html`: `72`
  - `PRODUCT title`: `54`
  - `PRODUCT body_html`: `54`
- Conclusion: French and Spanish are also incomplete beyond the tiny gap-fill import files.

## Theme locale audit
- Ran `shopify theme check --path . --output json --fail-level error`.
- Result: `33` files with errors.
- Locale-file translation errors:
  - `27` missing translation keys each in many locale files, including `de`, `id`, `it`, `ja`, `ko`, `nl`, `pl`, `pt-BR`, `ru`, `sv`, `th`, `tr`, `vi`, `zh-CN`, `zh-TW`, and more.
  - `es.json`: missing `general.breadcrumbs.home`
  - `fr.json`: missing `general.breadcrumbs.home`
- Additional non-locale repo errors still present:
  - `snippets/cjpod.liquid`
  - `tmp_products.json`
  - `sections/email-signup-banner.liquid`

## Practical conclusion
- The store is not ready for a professional multilingual rollout.
- The generated import CSVs are structurally valid partial imports, but they do not provide full translation coverage and they contain visible quality issues.
- Theme locale files are also incomplete for many languages, so storefront chrome/cart/breadcrumb strings will still break or fall back even if product/content translations are imported.
- Uploading the current `import_*.csv` set to Shopify would create a mixed-language storefront, not a finished multilingual store.

## Recommended next steps
1. Do not import or publish the current `import_*.csv` files to live markets.
2. Fix theme-locale gaps first for every language that will be exposed in the storefront.
3. Build a deterministic translation pipeline against the full Shopify export:
   - complete all required rows per locale, not a small subset
   - preserve HTML safely
   - preserve handles only when intentionally localized
   - run automated QA for blank rows, key mismatches, same-as-source rows, and English-fragment leakage
4. Import first to an unpublished language or non-live market and preview in Shopify Markets.
5. Publish only after storefront QA across:
   - homepage
   - collection pages
   - PDPs
   - cart
   - checkout language
   - menus
   - policy pages
   - blog/pages if included in the export
