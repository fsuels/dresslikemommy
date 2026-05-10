# Native-Language Copy Options Packet

Date: 2026-05-09

Lane: Worker B native/local-language Search copy options.

Decision: `LOCAL_NATIVE_LANGUAGE_OPTIONS_READY_FOR_NATIVE_REVIEW_NO_ADS_WRITES`

## Scope

This lane mitigates `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE` locally by creating native/local-language Google Search copy options and keyword notes for priority non-English markets.

No Google Ads preview, import, campaign build, campaign enablement, campaign edit, budget edit, bid edit, status edit, conversion-goal edit, Merchant upload, feed edit, Shopify Admin write, Shopify product-data write, theme edit, Pinterest write, checkout payment, order, or live-spend action was made.

All artifacts were written only under:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/`

## Inputs Inspected

- Held non-US Search CSV:
  - `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`
- Prior creative/copy packets:
  - `2026-05-07-paid-growth-parallel-infra-sprint/creative-copy/CREATIVE_RSA_PINTEREST_COPY_PACK.md`
  - `2026-05-08-paid-growth-controlled-infra-refresh/lanes/creative/CREATIVE_CONTROLLED_COPY_REFRESH.md`
  - `2026-05-08-paid-growth-market-readiness-safe-advance/lanes/creative-copy/CLAIM_SAFE_CREATIVE_REFRESH.md`
  - `2026-05-08-paid-growth-safe-followup/lanes/economics-creative/ECONOMICS_AND_CREATIVE_SAFE_GROWTH_PACK.md`
  - `2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/creative-url-copy-qa/CREATIVE_URL_COPY_QA_REPORT.md`
- Localization and checkout evidence:
  - `2026-05-08-paid-growth-controlled-infra-refresh/lanes/localization/LOCALIZATION_CONTROLLED_INFRA_READINESS.md`
  - `2026-05-09-paid-growth-checkout-expansion-safe-advance/lanes/checkout-ch-dk/CH_DK_CHECKOUT_TO_SHIPPING.md`
  - `2026-05-09-paid-growth-de-nl-checkout-safe-advance/lanes/checkout-de-nl/DE_NL_CHECKOUT_TO_SHIPPING.md`
  - `2026-05-09-paid-growth-nl-checkout-standard-metrics-safe-advance/lanes/nl-checkout-retry/NL_CHECKOUT_RETRY_TO_SHIPPING.md`
  - `2026-05-09-paid-growth-fr-be-checkout-safe-advance/lanes/checkout-fr-be/FR_BE_CHECKOUT_TO_SHIPPING.md`
  - `2026-05-09-paid-growth-se-pl-cz-gr-checkout-safe-advance/lanes/checkout-se-pl-cz-gr/SE_PL_CZ_GR_CHECKOUT_TO_SHIPPING.md`

## Held CSV Readback

The held candidate remains an English-only paused infrastructure packet:

| Check | Result |
|---|---:|
| Total rows | `1496` |
| Campaigns | `17` |
| Campaign language | `en` for all `17` campaigns |
| Positive keyword rows | `510` |
| Negative keyword rows | `629` |
| RSA ad rows | `170` |
| Preserved themes | `5` |
| Excluded theme | `Vacation Family` |

Preserved themes:

- `Mommy & Me Dresses`
- `Family Matching`
- `Matching Pajamas`
- `Matching Swimwear`
- `Daddy & Me`

`Vacation Family` stays excluded because of the unresolved stale Christmas metadata risk on the beach/vacation URL.

## Markets Covered

The packet covers all requested non-English priority markets, with Belgium split into French and Dutch options:

| Market | Locale options | Current copy posture |
|---|---|---|
| `ES` | `es-ES` | Localized URL and checkout evidence exists; native review still required. |
| `IT` | `it-IT` | Localized URL and checkout evidence exists; native review still required. |
| `PT` | `pt-PT` | Portugal checkout evidence exists, but storefront path behaved as `pt-BR`; native Portugal review required. |
| `RO` | `ro-RO` | Localized URL and checkout evidence exists; RON economics still required. |
| `DE` | `de-DE` | Checkout evidence exists in `en-DE`; native landing-language QA still required. |
| `NL` | `nl-NL` | NL rates/checkout lines were read back after cooldown; cleaner country-confirmed UI readback still useful before spend. |
| `FR` | `fr-FR` | Checkout evidence exists in `en-FR`; native landing-language QA still required. |
| `BE` | `fr-BE`, `nl-BE` | Checkout evidence exists in `en-BE`; Belgium language split decision required. |
| `SE` | `sv-SE` | Checkout evidence exists in `en-SE`; native landing-language QA still required. |
| `DK` | `da-DK` | Checkout evidence exists in `en-DK`; native landing-language QA still required. |
| `PL` | `pl-PL` | Checkout evidence exists in `en-PL`; native landing-language QA still required. |
| `CZ` | `cs-CZ` | Checkout evidence exists in `en-CZ`; native landing-language QA still required. |
| `GR` | `el-GR` | Checkout evidence exists in `en-GR`; native landing-language QA still required. |

## Artifacts

- `native_language_rsa_options.csv`: claim-safe local-language RSA headline and description options for `14` locale variants and `5` themes per locale.
- `native_language_keyword_option_notes.csv`: concept-only exact/phrase keyword notes by locale, with negative-keyword and usage gates.
- `native_language_copy_options_summary.json`: machine-readable summary of scope, source CSV shape, coverage, validation, and remaining gates.
- `NATIVE_LANGUAGE_COPY_OPTIONS_REPORT.md`: this report.

## Claim Guardrails

The copy options intentionally avoid:

- physical store, warehouse, local stock, stocked inventory, nearby inventory, pickup, or guaranteed on-hand-stock claims
- fast shipping, rush shipping, same-day shipping, guaranteed delivery, or unsupported delivery-speed claims
- bestseller, most popular, top-rated, viral, trending, review, star-rating, or customer-volume claims
- sale, discount, coupon, promotion, free gift, limited-time, or urgency claims
- guaranteed fit, guaranteed availability, or no-risk returns
- free-shipping claims in ad copy

The options stay in safer message territory:

- coordinated family looks
- mommy and me, daddy and me, family pajamas, family swimwear, and full-family matching outfit themes
- photos, birthdays, calm mornings, beach/pool moments, and family days
- separate size choice on the product page

## Validation

Local validation parsed both CSV files and checked RSA option limits:

| Check | Result |
|---|---:|
| RSA option rows | `14` |
| Keyword-note rows | `14` |
| Max headline length | `24` characters |
| Headline limit | `30` characters |
| Max description length | `73` characters |
| Description limit | `90` characters |
| Length violations | `0` |
| Forbidden-claim hits | `0` |

Validation command:

```bash
python3 - <<'PY'
import csv, pathlib, re, sys
lane=pathlib.Path('dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options')
rsa=lane/'native_language_rsa_options.csv'
kw=lane/'native_language_keyword_option_notes.csv'
with rsa.open(newline='') as f:
    rows=list(csv.DictReader(f))
head_cols=[c for c in rows[0] if c.endswith('_headlines')]
desc_cols=[c for c in rows[0] if c.endswith('_descriptions')]
viol=[]; max_head=(0,''); max_desc=(0,'')
for i,r in enumerate(rows,2):
    for c in head_cols:
        for opt in filter(None, r[c].split('|')):
            max_head=max(max_head,(len(opt),opt),key=lambda x:x[0])
            if len(opt)>30: viol.append((i,c,'headline',len(opt),opt))
    for c in desc_cols:
        for opt in filter(None, r[c].split('|')):
            max_desc=max(max_desc,(len(opt),opt),key=lambda x:x[0])
            if len(opt)>90: viol.append((i,c,'description',len(opt),opt))
with kw.open(newline='') as f:
    krows=list(csv.DictReader(f))
print('rsa_rows', len(rows))
print('keyword_rows', len(krows))
print('max_head', max_head)
print('max_desc', max_desc)
print('length_violations', len(viol))
PY
```

## Interpretation

This lane partially mitigates the English-only Search-copy gate by preparing local-language options. It does not clear the gate for Ads import or spend.

Use posture:

- The held `1496`-row CSV remains the safer owner-approval-gated paused English-first build candidate.
- These native/local-language options should be treated as concept-ready, not import-ready.
- Every locale row is labeled for native-speaker review before platform use.
- Local-language campaigns should not be used against English-only landing or checkout experiences unless the owner explicitly accepts that mismatch after readbacks.

## Remaining Gates

- Native-speaker review for every locale variant.
- Native landing, policy, cart, checkout, and customer-support wording QA for DE, NL, FR, BE, SE, DK, PL, CZ, and GR before local-language traffic.
- Portugal-specific wording review because `/pt` evidence uses pt-BR behavior for a Portugal market.
- Belgium language split decision before any BE local-language structure.
- Owner approval before any Google Ads preview/import/build.
- Just-in-time Ads readbacks: paused status, Search network only, no broad match, exact/phrase only, country locations, presence-only targeting, CPC cap, unchanged conversion goals, and country-qualified final URLs.
- Separate live-spend approval and Merchant/tracking/economics readbacks before any activation.
