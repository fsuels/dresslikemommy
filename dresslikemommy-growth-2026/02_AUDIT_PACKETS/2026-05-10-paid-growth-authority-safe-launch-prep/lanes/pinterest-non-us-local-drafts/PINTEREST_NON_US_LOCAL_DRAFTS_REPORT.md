# Pinterest Non-US Local Drafts Report

Generated: 2026-05-10

Worker: Worker 1 / Pinterest non-US local drafts

Write scope: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/lanes/pinterest-non-us-local-drafts/`

Mode: local-only documentation and review-only templates. No live account action was taken.

## Executive Verdict

`NON_US_PINTEREST_NOT_ACCOUNT_READY__LOCAL_OPERATOR_TEMPLATES_CREATED__US_AND_GOOGLE_FIRST_REMAIN_THE SAFE PATH`

The current repo evidence supports a clean Pinterest path only for US `en-US`. It does not support treating any of the 17 non-US markets as Pinterest account-ready. This lane therefore creates operator-ready local prep files for future non-US Pinterest setup, but every non-US Pinterest market remains gated by missing country-specific catalog/source proof, missing product-group readback, missing localized/country copy approval, missing account readback, and the unresolved `Fair` Event Quality gate.

## Current Pinterest Truth

Read-only sources agree on this baseline:

- Advertiser: `549756244483`.
- Account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- Catalog: `Catalog_Retail`.
- Catalog ID: `3041764155561548387`.
- Allowed US EN Shopify source/feed profile: `3041760867124595727`.
- Blocked failed sitemap source: `3041760916127467912`.
- Clean launchable-local US scope: `342` EN-US rows.
- Clean US scope split: `210` Mommy & Me, `103` Family Matching, `29` Pajamas.
- US exclusions: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`.
- Baseline campaign state from prior readback: `0` Pinterest campaigns, `0` currently serving, `$0.00` spend.
- Official Pinterest app pixel/CAPI path: Always on / share all events in prior evidence.
- Event Quality: `Fair`, with top gaps `product_id__ADD_PAYMENT_INFO`, `hashed_email__ADD_TO_CART`, and `click_id_epik__CHECKOUT`.

The US paused-draft templates from 2026-05-09 are review-only operator files. They are not Pinterest bulk uploads and are not evidence of a live Pinterest draft.

## What Is Missing For Non-US Pinterest

No current evidence proves any of the following for `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, or `GR`:

- Pinterest country-specific catalog/source/feed profile.
- Country or locale-specific product item readback.
- Clean in-stock diagnostic scope by country/locale.
- Product-group filter readback.
- Exclusion set equivalent to the US 4-row exclusion.
- Localized promoted-pin copy approved for platform use.
- Country targeting UI path.
- Paused draft account object readback.
- Event Quality readback after selecting a non-US setup path.

Therefore Google Ads artifacts, Shopify localization evidence, and checkout evidence cannot be used as substitutes for Pinterest catalog/account readiness.

## Recommended Market Posture

### Keep Pinterest US-only until the US gate is clean

Pinterest should remain US-only at the account-object level until the parent either:

1. Builds and reads back the approved paused US Pinterest drafts from the clean `342` scope, or
2. Reconfirms Event Quality and official app state, then explicitly decides that non-US local prep should proceed anyway.

### First future non-US Pinterest packet candidates

If the parent chooses non-US Pinterest local prep before US live spend, build one local packet at a time in this order:

1. `GB / en-GB`: strongest English-first Pinterest candidate after US because checkout/presentment evidence exists and no native copy dependency is required.
2. `CA / en-CA`: English-first candidate; French-Canada remains a later copy decision, not a default.
3. `AU / en-AU`: English-first candidate; good checkout evidence, but no Pinterest source proof yet.

These three are local-packet candidates only. They are not account-ready.

### Google-first or US-only for now

The following should stay Google-first, not Pinterest-account-first, until country-specific Pinterest source proof and copy gates exist:

- `CH`: language split decision needed (`de`, `fr`, `it`, or English-first).
- `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, `GR`: native review and localized landing/copy gates remain before local-language Pinterest use.
- `FR`: Google Ads branch is parked and no Pinterest country scope exists.
- `BE`: Google Ads branch is throttled/parked and Belgium needs French/Dutch split decision.

## Per-Market Readiness Summary

The CSV `pinterest_non_us_market_readiness_matrix.csv` is the machine-readable matrix. Summary:

| Market | Locale posture | Pinterest readiness | Future path |
|---|---|---|---|
| `GB` | `en-GB` | Not built | First non-US local packet candidate after US/Event Quality gate |
| `CA` | `en-CA`; French-Canada later decision | Not built | Second local packet candidate |
| `AU` | `en-AU` | Not built | Third local packet candidate |
| `CH` | English-first only until split decision | Not built | Google-first; decide language split before Pinterest |
| `DK` | `da-DK` needs native review | Not built | Google-first; native copy and source proof first |
| `DE` | `de-DE` needs native review | Not built | Google-first; native copy and source proof first |
| `NL` | `nl-NL` needs native review | Not built | Google-first; native copy and source proof first |
| `SE` | `sv-SE` needs native review | Not built | Google-first; native copy and source proof first |
| `FR` | `fr-FR` needs native review | Not built | Park Pinterest until Google FR branch and source proof are clean |
| `BE` | `fr-BE`/`nl-BE` split needed | Not built | Park Pinterest until Belgium split and source proof are clean |
| `ES` | `es-ES` needs native review | Not built | Google-first; local Pinterest only after source/copy proof |
| `IT` | `it-IT` needs native review | Not built | Google-first; local Pinterest only after source/copy proof |
| `PL` | `pl-PL` needs native review | Not built | Google-first; local Pinterest only after source/copy proof |
| `CZ` | `cs-CZ` needs native review | Not built | Google-first; local Pinterest only after source/copy proof |
| `RO` | `ro-RO` needs native review | Not built | Google-first; RON economics and source proof first |
| `PT` | `pt-PT` conflicts with current `pt-BR` storefront behavior | Not built | Google-first; resolve language behavior before Pinterest |
| `GR` | `el-GR` needs native review | Not built | Google-first; source and Greek copy proof first |

## Draft Object Naming Conventions

Do not create these objects without parent approval and live readbacks. These are review-only names for future paused drafts:

- Catalog campaign: `DLM_PIN_{MARKET}_CATALOG_{SCOPE_ROWS}_PAUSED_{YYYYMMDD}`.
- Retargeting campaign: `DLM_PIN_{MARKET}_RETARGETING_{SCOPE_ROWS}_PAUSED_{YYYYMMDD}`.
- Prospecting ad group: `DLM_PIN_{MARKET}_CATALOG_{GROUP_KEY}_PAUSED_{YYYYMMDD}`.
- Retargeting ad group: `DLM_PIN_{MARKET}_RETARGETING_{GROUP_KEY}_PAUSED_{YYYYMMDD}`.
- Product group: `DLM_PIN_{MARKET}_SHOPPING_{GROUP_KEY}`.

Allowed `GROUP_KEY` values remain aligned with the proven US product groups unless a future readback proves a different safe scope:

- `MOMMY_ME`
- `FAMILY_MATCHING`
- `PAJAMAS`

Do not put row counts in an object name until the country-specific clean scope file exists and has been counted. Use `{SCOPE_ROWS}` as a placeholder until then.

## Product-Group Template Assumptions

The file `pinterest_non_us_product_group_template.csv` defines review-only assumptions. It deliberately does not name a real non-US feed profile ID because none is proven.

Future product groups may be considered only if all conditions are true:

- Pinterest catalog/source readback proves the selected country/locale source exists.
- Item-level metadata proves a clean row scope for that market.
- The source exposes labels or attributes that can filter to the same safe paid cohort without changing feed labels.
- The source does not require Merchant, Shopify product-data, feed-label, or catalog-source mutation.
- The UI can keep every campaign, ad group, ad, and product group paused/draft only.
- The UI does not require budget/bid/status actions outside the exact approval phrase.

Use `IN_STOCK` only as a platform diagnostic, never as customer-facing stock, warehouse, local inventory, or guaranteed availability copy.

## Localized Copy And Country Gates

The file `pinterest_non_us_copy_country_gate_template.csv` maps each market to its copy gate.

Rules:

- English-first markets (`GB`, `CA`, `AU`) may reuse the claim-safe English copy style only after the country source and URL readbacks pass.
- `CA` must remain English-first unless the parent explicitly creates a French-Canada copy/source packet.
- `CH` must remain English-first until the parent chooses German, French, Italian, or split-country setup.
- `BE` must not be launched as one ambiguous language. Decide `fr-BE`, `nl-BE`, or separate objects first.
- `PT` must not use `pt-PT` copy until the existing `pt-BR` storefront behavior is resolved or explicitly accepted.
- Native-language copy for `da-DK`, `de-DE`, `nl-NL`, `sv-SE`, `fr-FR`, `fr-BE`, `nl-BE`, `es-ES`, `it-IT`, `pl-PL`, `cs-CZ`, `ro-RO`, `pt-PT`, and `el-GR` remains concept-ready only until native review and landing-language QA pass.

Do not use claims about discounts, fast shipping, guaranteed delivery, stock, warehouse, local inventory, physical store, bestseller status, reviews, or limited-time urgency unless a future evidence packet proves the claim.

## Exact Stop Conditions

The full stop list is in `STOP_CONDITIONS.md`. The highest-risk stops are:

- Any Pinterest account write is required.
- Any budget, bid, status, campaign, ad group, ad, product group, audience, catalog source, tag, CAPI, feed, or spend action is required.
- No country-specific catalog/source/feed profile can be selected and read back.
- The UI selects the failed sitemap source `3041760916127467912` or an unproven localized source.
- The UI requires creating or changing an audience.
- Event Quality is still `Fair` and the operator is attempting live spend.
- A native-language market has no native copy review or landing-language proof.
- A country setup would require Shopify product-data, feed-label, Merchant, Google Ads, or theme changes.

## Files Created

- `README.md`
- `PINTEREST_NON_US_LOCAL_DRAFTS_REPORT.md`
- `pinterest_non_us_market_readiness_matrix.csv`
- `pinterest_non_us_object_naming_template.csv`
- `pinterest_non_us_product_group_template.csv`
- `pinterest_non_us_copy_country_gate_template.csv`
- `STOP_CONDITIONS.md`

## Guardrails Preserved

- No Pinterest account write.
- No campaign, draft, ad group, ad, product group, audience, catalog source, feed, budget, bid, status, tag/CAPI, or spend write.
- No Shopify Admin, product-data, Merchant, Google Ads, GA4/GTM, theme, payment, order, refund, or credential action.
- No claim that non-US Pinterest is account-ready.
- No edits outside the assigned worker lane.
