# Google Ads Intl Paused-Build Validation

Source packet validated:
`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/ads-intl/`

Output lane:
`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/google-ads-intl/`

## Result

`PASS_WITH_APPROVAL_GATE_SHARPENING`

The importable non-US Google Search packet remains local-only and structurally ready for a future preview-only import after exact owner approval. I found no Google Ads, Merchant, Shopify, Pinterest, browser-account, import, or live-spend action in this validation lane.

## Count Validation

| Check | Result |
|---|---:|
| Campaigns | `17` |
| Countries | `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `GR`, `PT` |
| Unique ad groups | `204` |
| Positive keywords | `612` |
| Campaign negatives | `629` |
| RSAs | `204` |
| Web bulk rows | `1666` |

Web bulk row types: `17` Campaign, `204` Ad group, `612` Keyword, `629` Negative keyword, and `204` Ad rows.

## Guardrail Validation

| Guardrail | Result | Evidence |
|---|---|---|
| All importable statuses paused | `PASS` | Campaign, ad group, keyword, and ad status fields are `Paused`; negative keyword source rows are marked `Paused import row` and attach to paused campaigns. |
| Max CPC <= `$0.20` | `PASS` | Max CPC seen: `$0.15`. |
| No importable US campaign `23827590655` rows | `PASS` | `0` rows in `campaign_structure.csv`, `keyword_plan.csv`, `negative_keyword_plan.csv`, `rsa_copy_pack.csv`, or web bulk upload reference `23827590655`, `_US_`, or `country=US`. |
| No PMax / Standard Shopping / product-scope / feed-label / product-group / conversion-goal rows | `PASS` | `0` prohibited importable-row hits. |
| ES/IT/RO/PT final URLs country-qualified | `PASS` | Localized routes use `/es`, `/it`, `/ro`, `/pt` product paths with matching `country=ES`, `country=IT`, `country=RO`, `country=PT`. |

Info: non-importable context files still reference the existing US nonbrand campaign as a template/gate, especially `country_tier_plan.csv` and `manifest.json`. That is acceptable for documentation, but future bulk upload/import work should continue to use only the non-US importable files.

## Approval Gate Sharpening

The existing packet gate is close but not exact against the canonical owner-standard approval wording in `ops/prompts/paid-growth-ai-army-continuation-prompt.md`. For any future owner request, use this exact wording:

```text
APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.
```

## Residual Risks

- This is not approval to import, create, enable, preview, or edit anything in Google Ads.
- The source packet still needs action-time Google Ads preview validation before any approved paused import.
- International live spend remains blocked by Merchant/Pinterest/tracking/economics, landing-page, shipping/checkout, and final owner-approval gates.
- GB/CA still need visual checkout UI confirmation before spend; AU has a prior isolated-browser shipping-step pass; ES/IT/RO/PT had prior localized country-qualified landing/checkout evidence.
- English-only non-US shells outside English-first countries may have limited reach and conversion quality until localized landing QA and copy are proven.

## Next Best Action

Parent/orchestrator can use this validation as the local proof packet. If the owner wants live paused campaign creation later, request the exact gate above, run preview-only import validation first, then read back campaigns, ad groups, ads, keywords, locations, networks, CPCs, negatives, and conversion-goal inheritance before applying.
