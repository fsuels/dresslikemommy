# Google Search TEST BUILD Approval Packet

Generated: 2026-05-09

Worker: Google Search TEST BUILD approval lane

Decision: `PASS_LOCAL_ONLY_APPROVAL_GATED`

Scope: local approval packaging only. No Google Ads, Merchant Center, Shopify, Pinterest, feed, campaign, budget, bid, status, preview/import/upload, product-scope, feed-label, product-group, conversion-goal, PMax, Standard Shopping, or live-spend action was opened or changed.

## Candidate CSV

Use this held CSV for any future owner-approved paused non-US Search preview/import:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`

Do not use the earlier `1666`-row CSV while `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` remains unrepaired. The held file removes all `Vacation Family` rows tied to the stale beach/Christmas metadata URL.

## Fresh Local Validation

Validator: `validate_test_build_candidate.py`

Artifacts:

- `validation_summary.json`
- `country_matrix.csv`

Result: `PASS`

| Check | Result |
|---|---:|
| Data rows | `1496` |
| Header columns | `95` |
| Actions | `1496 Add` |
| Campaign rows | `17` |
| Ad group rows | `170` |
| Positive keyword rows | `510` |
| Campaign negative keyword rows | `629` |
| Responsive search ad rows | `170` |
| Final URL rows | `680` |
| Final URL country params | `40` per country |
| Existing entity ID fields populated | `0` |
| Importable non-paused entity rows | `0` |
| Languages | `en` |
| Networks | `Google search` |
| Bid strategy type | `Manual CPC` |
| Budget values in paused shell rows | `$1.00`, `$2.00` |
| CPC values observed | `$0.10`, `$0.12`, `$0.15` |
| Max CPC observed | `$0.15` |

Status readback from the CSV:

| Entity | Paused rows |
|---|---:|
| Campaigns | `17` |
| Ad groups | `170` |
| Keywords | `510` |
| Ads | `170` |

Negative keyword rows are counted separately because this web-bulk export does not expose a negative-keyword status field.

## Country Matrix

Each country has `1` paused campaign, `10` ad groups, `30` positive keywords, `37` campaign negatives, `10` paused RSAs, and `40` country-qualified final URL rows.

| ISO | Location | Campaign | Budget |
|---|---|---|---:|
| AU | Australia | `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$2.00` |
| BE | Belgium | `DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| CA | Canada | `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$2.00` |
| CH | Switzerland | `DLM_CH_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| CZ | Czechia | `DLM_CZ_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| DE | Germany | `DLM_DE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| DK | Denmark | `DLM_DK_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| ES | Spain | `DLM_ES_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| FR | France | `DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| GB | United Kingdom | `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$2.00` |
| GR | Greece | `DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| IT | Italy | `DLM_IT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| NL | Netherlands | `DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| PL | Poland | `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| PT | Portugal | `DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| RO | Romania | `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |
| SE | Sweden | `DLM_SE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1.00` |

## Forbidden-Surface Scan

Fresh validator result: `0` hits for all forbidden patterns:

- Existing US nonbrand campaign `23827590655`
- `DLM_US_` campaign names or `United States` location rows
- Bad beach handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`
- Product `7227378892897`
- `Vacation Family`
- `PMax` / `Performance Max`
- `Standard Shopping` / `Shopping ads`
- `product scope`
- `feed label`
- `product group`
- `conversion goal`
- `Merchant Center`

## Approval Phrase

Any Google Ads preview/import/create step is blocked until the owner gives this exact action-time approval:

```text
APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.
```

## Preview-Only Checklist

Only after the exact approval phrase above:

1. Confirm the account and customer context before loading the CSV.
2. Use the held `1496`-row CSV, not the original `1666`-row CSV.
3. Preview only first. Do not import if preview changes are broader than `17` new paused non-US Search campaigns and their paused ad groups, paused ads, paused keywords, and campaign negatives.
4. Confirm preview shows no edits to existing entities and no row touching campaign `23827590655`.
5. Confirm preview shows no PMax, Standard Shopping, product/feed, Merchant, Pinterest, Shopify, conversion-goal, product-scope, feed-label, or product-group changes.
6. Confirm all campaigns, ad groups, ads, and keywords remain paused in preview.
7. Confirm CPC caps are at or below `$0.20`, with local file max `$0.15`.
8. Confirm final URLs remain country-qualified and contain the expected `country=<ISO>` parameter.
9. Confirm location targeting method is presence-only. The CSV contains target locations, but presence-only behavior must be verified in Google Ads preview/readback because the web-bulk file does not prove the location option by itself.
10. Stop before import if any preview row is unclear, merged into an existing campaign, eligible/enabled, missing country params, or asks for a Save/Apply that cannot be read back safely.

## Post-Import Readback Checklist

Only if preview passes and the owner approval still applies:

1. Read back all `17` campaign names and confirm status `Paused`.
2. Read back ad group, keyword, and ad status for samples from every country; all must be `Paused`.
3. Read back campaign locations and confirm no United States targeting.
4. Read back location option and confirm presence-only targeting.
5. Read back bidding and CPC values; no CPC above `$0.20`, expected local max `$0.15`.
6. Read back campaign budgets as paused shell budgets only; no live spend, no budget increase to existing campaigns, and no enablement.
7. Read back final URLs for each country and confirm `country=<ISO>` remains present.
8. Read back there were no changes to Standard Shopping, PMax, campaign `23827590655`, product groups, feed labels, product scope, conversion goals, Merchant, Shopify, or Pinterest.
9. Save screenshots/exports into the parent evidence packet and update the problem tracker and worklog.

## Stop Conditions

Stop and do not import if any of these appear:

- Any live entity status is `Enabled`, `Eligible`, or otherwise serving.
- Any existing campaign/entity ID is populated in preview.
- Any row touches campaign `23827590655` or a US campaign/location.
- Any PMax, Standard Shopping, Merchant, Shopping feed, product-scope, feed-label, product-group, conversion-goal, Shopify, Pinterest, or theme surface appears.
- Any CPC exceeds `$0.20`.
- Any final URL lacks a country parameter or contains the held beach/Vacation Family product.
- Location option cannot be verified as presence-only.
- Google Ads asks for an account switch, sign-in, permission acceptance, CAPTCHA, or irreversible action outside the exact approval.

## Do Not Repeat

- Do not reintroduce the `Vacation Family`/beach handle rows until the Shopify SEO/social metadata repair is separately approved and publicly read back.
- Do not redo the Merchant US/en age_group fix; it is already solved.
- Do not bundle this Google Search approval with Merchant US/es, Pinterest, Standard Shopping, PMax, Shopify metadata, theme, or conversion-goal work.
- Do not change Standard Shopping status, budget, product groups, feed labels, product scope, or conversion goals.
- Do not create live spend. This packet is for paused non-US Search infrastructure only.

## Verification Commands

```bash
python3 -m py_compile dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/google-search-test-build-approval/validate_test_build_candidate.py
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/google-search-test-build-approval/validate_test_build_candidate.py
```
