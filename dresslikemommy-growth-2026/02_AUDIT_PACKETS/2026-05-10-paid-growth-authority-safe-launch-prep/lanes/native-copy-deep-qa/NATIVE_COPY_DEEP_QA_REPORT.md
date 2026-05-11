# Native-Copy Deep QA Lane

Date: 2026-05-10
Worker: 2
Mode: local-only QA. No Google Ads, Pinterest, Shopify, Merchant, theme, tracking, budget, bid, campaign-status, product, feed, or conversion-goal writes.

## Decision

`LOCAL_NATIVE_COPY_QA_COMPLETE__NO_LOCALE_PLATFORM_READY_WITHOUT_NATIVE_REVIEW`

The existing native-language Google Ads copy options cover all 14 requested locale variants and pass local mechanical checks for Google RSA character limits and known forbidden-claim families. They are not import-ready and not live-spend-ready. The correct operational posture is:

- `CONCEPT_READY_NATIVE_REVIEW_REQUIRED`: ES, IT, RO. These have stronger localized URL/checkout evidence, but still need native speaker review and landing-language QA before platform use.
- `NATIVE_REVIEW_REQUIRED`: DE, NL, FR, SE, PL, CZ, GR. These need native speaker review plus proof that the landing path actually serves native-language storefront content.
- `PLATFORM_USE_BLOCKED`: PT, DA/DK, FR-BE, NL-BE. These have named blockers that must be resolved before local-language platform use.

## Sources Read

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_rsa_options.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_keyword_option_notes.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_copy_options_summary.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/lanes/native-copy-risk-triage/NATIVE_COPY_RISK_TRIAGE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/localization/LOCALIZATION_CONTROLLED_INFRA_READINESS.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-platform-matrix/EXECUTION_MATRIX.md`

## Automated Validation

| Check | Result |
|---|---:|
| Locale rows | 14 |
| Theme rows for review | 70 |
| Themes per locale | 5 |
| Headline options per locale | 15 |
| Description options per locale | 10 |
| Longest headline | 24 chars (`it-IT`: `Look famiglia coordinati`) |
| Headline limit | 30 chars |
| Longest description | 73 chars (`nl-NL`: `Ideeën voor bijpassende pyjama's voor rustige ochtenden en familiefoto's.`) |
| Description limit | 90 chars |
| Length violations | 0 |
| Forbidden-claim hits | 0 |

Automated forbidden-claim scanning looked for unsupported shipping-speed, free-shipping-in-ad-copy, warehouse/local-stock/pickup, social-proof, promotion/discount/urgency, guaranteed-fit, and guaranteed-availability claim families. This does not replace native speaker, legal, platform, or landing-page review.

## Per-Locale Matrix

| Locale | Market | Status | Priority | Max H/D len | Length violations | Claim hits | Manual risk flags |
|---|---|---|---|---:|---:|---:|---|
| `es-ES` | `ES` | `CONCEPT_READY_NATIVE_REVIEW_REQUIRED` | `P1` | 21 / 70 | 0 | 0 | Spain register/accent and mama/madre terminology review |
| `it-IT` | `IT` | `CONCEPT_READY_NATIVE_REVIEW_REQUIRED` | `P1` | 24 / 69 | 0 | 0 | costumi may need costumi da bagno for swimwear clarity |
| `pt-PT` | `PT` | `PLATFORM_USE_BLOCKED` | `P0` | 24 / 67 | 0 | 0 | pt-PT copy vs pt-BR storefront behavior risk |
| `ro-RO` | `RO` | `CONCEPT_READY_NATIVE_REVIEW_REQUIRED` | `P1` | 21 / 71 | 0 | 0 | Diacritics and Lookuri/Look-uri review; RON economics separate gate |
| `de-DE` | `DE` | `NATIVE_REVIEW_REQUIRED` | `P2` | 22 / 67 | 0 | 0 | Register decision needed: du vs Sie; Partnerlook may read awkward for parent-child |
| `nl-NL` | `NL` | `NATIVE_REVIEW_REQUIRED` | `P2` | 22 / 73 | 0 | 0 | Anglicism check: Matching; native landing not proven |
| `fr-FR` | `FR` | `NATIVE_REVIEW_REQUIRED` | `P2` | 22 / 73 | 0 | 0 | vous vs tu register decision; looks vs tenues wording |
| `fr-BE` | `BE-FR` | `PLATFORM_USE_BLOCKED` | `P0` | 22 / 73 | 0 | 0 | fr-BE duplicates fr-FR; Belgium FR/NL split undecided |
| `nl-BE` | `BE-NL` | `PLATFORM_USE_BLOCKED` | `P0` | 22 / 73 | 0 | 0 | nl-BE duplicates nl-NL; Belgium FR/NL split undecided |
| `sv-SE` | `SE` | `NATIVE_REVIEW_REQUIRED` | `P3` | 21 / 63 | 0 | 0 | Singular/plural check: klänning vs klänningar; anglicism check |
| `da-DK` | `DK` | `PLATFORM_USE_BLOCKED` | `P0` | 19 / 67 | 0 | 0 | Likely non-Danish headline option: Mamma datter kjoler |
| `pl-PL` | `PL` | `NATIVE_REVIEW_REQUIRED` | `P3` | 20 / 68 | 0 | 0 | Case/grammar review needed for noun phrases |
| `cs-CZ` | `CZ` | `NATIVE_REVIEW_REQUIRED` | `P3` | 17 / 66 | 0 | 0 | Formal vs informal register review needed |
| `el-GR` | `GR` | `NATIVE_REVIEW_REQUIRED` | `P3` | 22 / 72 | 0 | 0 | Mixed Latin "looks" in Greek copy requires native acceptance or rewrite |

## Status Definitions

- `CONCEPT_READY_NATIVE_REVIEW_REQUIRED`: local copy exists and mechanical checks pass; platform use still blocked until native review, landing QA, Ads preview/readback, and owner approval.
- `NATIVE_REVIEW_REQUIRED`: local copy exists and mechanical checks pass, but native-language landing path/readiness is not proven enough for platform use.
- `PLATFORM_USE_BLOCKED`: a named structural/copy blocker must be resolved before the locale can move to native review as a platform candidate.

## Per-Locale Review Checklist

### `es-ES`
- Status: `CONCEPT_READY_NATIVE_REVIEW_REQUIRED` / priority `P1`.
- Landing evidence: localized URL + checkout evidence exists; country-qualified /es required.
- Current automated validation: max headline 21 chars, max description 70 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Spain register/accent and mama/madre terminology review.
- Platform-use gate: Spain URL and checkout/currency evidence exists; needs Spanish native ad-copy review and landing-language QA before platform use.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `it-IT`
- Status: `CONCEPT_READY_NATIVE_REVIEW_REQUIRED` / priority `P1`.
- Landing evidence: localized URL + checkout evidence exists; country-qualified /it required.
- Current automated validation: max headline 24 chars, max description 69 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: costumi may need costumi da bagno for swimwear clarity.
- Platform-use gate: Italy URL and checkout/currency evidence exists; needs Italian native ad-copy review and landing-language QA before platform use.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `pt-PT`
- Status: `PLATFORM_USE_BLOCKED` / priority `P0`.
- Landing evidence: Portugal checkout evidence exists, but /pt served pt-BR behavior.
- Current automated validation: max headline 24 chars, max description 67 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: pt-PT copy vs pt-BR storefront behavior risk.
- Platform-use gate: Portugal copy is pt-PT but prior storefront evidence served pt-BR behavior; native review plus storefront language decision required before platform use.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `ro-RO`
- Status: `CONCEPT_READY_NATIVE_REVIEW_REQUIRED` / priority `P1`.
- Landing evidence: localized URL + checkout/RON evidence exists; country-qualified /ro required.
- Current automated validation: max headline 21 chars, max description 71 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Diacritics and Lookuri/Look-uri review; RON economics separate gate.
- Platform-use gate: Romania URL and checkout/RON evidence exists; needs Romanian review, landing QA, and RON economics before platform use.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `de-DE`
- Status: `NATIVE_REVIEW_REQUIRED` / priority `P2`.
- Landing evidence: country checkout evidence exists; native /de landing not proven.
- Current automated validation: max headline 22 chars, max description 67 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Register decision needed: du vs Sie; Partnerlook may read awkward for parent-child.
- Platform-use gate: DE checkout evidence exists in country context but native German landing path is not proven; review register and Partnerlook wording.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `nl-NL`
- Status: `NATIVE_REVIEW_REQUIRED` / priority `P2`.
- Landing evidence: country currency/rates evidence exists; native /nl landing not proven.
- Current automated validation: max headline 22 chars, max description 73 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Anglicism check: Matching; native landing not proven.
- Platform-use gate: NL currency/rate evidence exists but native Dutch landing path and UI confirmation remain incomplete; review anglicisms and language QA.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `fr-FR`
- Status: `NATIVE_REVIEW_REQUIRED` / priority `P2`.
- Landing evidence: country checkout evidence exists; native /fr landing not proven.
- Current automated validation: max headline 22 chars, max description 73 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: vous vs tu register decision; looks vs tenues wording.
- Platform-use gate: FR country checkout evidence exists but native French landing path is not proven; review vous/tu and French register.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `fr-BE`
- Status: `PLATFORM_USE_BLOCKED` / priority `P0`.
- Landing evidence: BE checkout evidence exists; fr-BE route/split not proven.
- Current automated validation: max headline 22 chars, max description 73 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: fr-BE duplicates fr-FR; Belgium FR/NL split undecided.
- Platform-use gate: Belgian French copy duplicates fr-FR and Belgium FR/NL structure is undecided; platform use blocked until split decision and BE language QA.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `nl-BE`
- Status: `PLATFORM_USE_BLOCKED` / priority `P0`.
- Landing evidence: BE checkout evidence exists; nl-BE route/split not proven.
- Current automated validation: max headline 22 chars, max description 73 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: nl-BE duplicates nl-NL; Belgium FR/NL split undecided.
- Platform-use gate: Belgian Dutch copy duplicates nl-NL and Belgium FR/NL structure is undecided; platform use blocked until split decision and BE language QA.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `sv-SE`
- Status: `NATIVE_REVIEW_REQUIRED` / priority `P3`.
- Landing evidence: country checkout evidence exists; native /sv landing not proven.
- Current automated validation: max headline 21 chars, max description 63 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Singular/plural check: klänning vs klänningar; anglicism check.
- Platform-use gate: SE checkout evidence exists in country context but native Swedish landing path is not proven; review singular/plural and anglicisms.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `da-DK`
- Status: `PLATFORM_USE_BLOCKED` / priority `P0`.
- Landing evidence: country checkout evidence exists; native /da landing not proven.
- Current automated validation: max headline 19 chars, max description 67 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Likely non-Danish headline option: Mamma datter kjoler.
- Platform-use gate: Danish row contains likely non-Danish option "Mamma datter kjoler"; native rewrite required before platform use.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `pl-PL`
- Status: `NATIVE_REVIEW_REQUIRED` / priority `P3`.
- Landing evidence: country checkout evidence exists; native /pl landing not proven.
- Current automated validation: max headline 20 chars, max description 68 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Case/grammar review needed for noun phrases.
- Platform-use gate: PL checkout evidence exists in country context but native Polish landing path is not proven; review grammar/cases and search phrasing.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `cs-CZ`
- Status: `NATIVE_REVIEW_REQUIRED` / priority `P3`.
- Landing evidence: country checkout evidence exists; native /cs landing not proven.
- Current automated validation: max headline 17 chars, max description 66 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Formal vs informal register review needed.
- Platform-use gate: CZ checkout evidence exists in country context but native Czech landing path is not proven; review formal/informal register and diacritics.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.

### `el-GR`
- Status: `NATIVE_REVIEW_REQUIRED` / priority `P3`.
- Landing evidence: country checkout evidence exists; native /el landing not proven.
- Current automated validation: max headline 22 chars, max description 72 chars, 0 length violations, 0 forbidden-claim hits.
- Manual flags: Mixed Latin "looks" in Greek copy requires native acceptance or rewrite.
- Platform-use gate: GR checkout evidence exists in country context but native Greek landing path is not proven; review Greek phrasing, accents, and mixed Latin "looks" usage.
- Reviewer must mark every option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT, and any rewrite must be revalidated before use.


## Closing Criteria Per Locale

1. Native reviewer marks every headline and description option in `per_locale_theme_review_checklist.csv` as PASS / REWRITE / REJECT.
2. Any rewrite is added to a final dated locale CSV and revalidated for <=30 character headlines, <=90 character descriptions, and zero forbidden-claim hits.
3. Country-qualified landing QA passes for PDP, cart, checkout entry, currency, shipping-rate labels, policy/page links, and mobile rendering. No payment and no order.
4. Special cases close: PT storefront language decision; DK rewrite of `Mamma datter kjoler`; Belgium FR/NL split and route proof.
5. Parent/orchestrator updates the global problem tracker and only then considers a separate paused Ads preview/import approval. This Worker 2 lane does not approve any platform action.

## Files Created

- `native_copy_deep_qa_summary.json`
- `native_copy_qa_matrix.csv`
- `per_locale_theme_review_checklist.csv`
- `NATIVE_COPY_DEEP_QA_REPORT.md`
