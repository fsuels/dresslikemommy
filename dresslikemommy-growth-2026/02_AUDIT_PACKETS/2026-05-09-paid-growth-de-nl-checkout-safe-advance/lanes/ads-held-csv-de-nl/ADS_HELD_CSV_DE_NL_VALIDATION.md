# Worker C - Held Google Ads CSV DE/NL Validation

Date: 2026-05-09

Status: `PASS_LOCAL_ONLY_APPROVAL_GATED`

## Scope

Validated the held non-US Google Ads Search web-bulk CSV locally, focused on Germany (`DE`), Netherlands (`NL`), and forbidden-change detection.

Source CSV:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`

No Google Ads account was opened. No preview/import/upload was attempted. No live changes were made.

## Output Files

- `validation_summary.json` - full validation summary and check booleans.
- `campaign_summary.csv` - one row per campaign in the held CSV.
- `de_nl_campaign_summary.csv` - focused DE/NL row counts, status, CPC, URL, and ID summary.
- `forbidden_findings.csv` - forbidden finding log; header-only because no findings were detected.

## Full CSV Summary

| Metric | Result |
|---|---:|
| Data rows | 1496 |
| Campaigns | 17 |
| Campaign rows | 17 |
| Ad group rows | 170 |
| Positive keyword rows | 510 |
| Negative keyword rows | 629 |
| Ad rows | 170 |
| Actions | 1496 `Add` |
| CPC values | `0.10`, `0.12`, `0.15` |

## DE/NL Coverage

| Country | Campaign | Rows | Ad Groups | Keywords | Negatives | Ads | Location | Language | CPC | Final URLs |
|---|---|---:|---:|---:|---:|---:|---|---|---|---:|
| DE | `DLM_DE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 10 | 30 | 37 | 10 | Germany | `en` | `0.12` | 40 |
| NL | `DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | 88 | 10 | 30 | 37 | 10 | Netherlands | `en` | `0.12` | 40 |

DE final URLs all contain `country=DE`. NL final URLs all contain `country=NL`.

## Guardrail Checks

| Check | Result |
|---|---|
| All actions are `Add` | Pass |
| Row types limited to `Campaign`, `Ad group`, `Keyword`, `Negative keyword`, `Ad` | Pass |
| Campaigns, ad groups, keywords, and ads are paused | Pass |
| Campaign type is Search and network is Google Search | Pass |
| Bid strategy is Manual CPC | Pass |
| CPC values are at or below `$0.20` | Pass |
| DE/NL campaigns are present | Pass |
| All final URLs have matching country parameters | Pass |
| No existing IDs or edit rows detected | Pass |
| No `Vacation Family` rows detected | Pass |
| No bad beach handle or product `7227378892897` detected | Pass |
| No US campaign `23827590655` detected | Pass |
| No PMax or Standard Shopping rows detected | Pass |
| No product-scope, feed-label, product-group, conversion-goal, or Merchant write terms detected | Pass |

## Interpretation

The held CSV remains a local-only paused Search infrastructure candidate. DE and NL are covered with country-qualified URLs and paused-only entities, and the forbidden-change scan found no rows that would touch the existing US nonbrand campaign, PMax, Standard Shopping, Merchant/feed/product surfaces, conversion goals, or the held Vacation Family/beach URL.

This validation does not authorize import, preview, upload, enablement, spend, budget changes, bid changes, campaign status changes, or any Merchant/Pinterest/Shopify writes.

## Residual Gates

- Any Google Ads preview/import requires fresh exact owner approval using the canonical paused non-US Google Search `TEST BUILD` gate.
- DE/NL remain paused-infrastructure candidates only until the parent integrates checkout, landing/policy, tracking, Merchant/Pinterest, and economics gates.
- Live-spend-ready non-US markets remain `0`.
