# Ads Import Parked PT / URL Gate

Lane: Ads import parked gate
Scope: local artifacts only; no Google Ads account access
Status: `PARKED_NOT_APPROVED`

## Result

The international Search import remains parked. I did not open Google Ads, Merchant Center, Shopify Admin, Pinterest, or any live account surface. I did not import, create, enable, pause, upload, change budgets, change bids, change statuses, edit conversion goals, alter product scope, edit feed labels, edit product groups, touch PMax, touch Standard Shopping, or authorize spend.

Even paused Google Ads campaign creation is a live write. This lane only revalidates that the local packet is still a paused-only draft and that exact owner approval is still required before any preview/import workflow.

## Source Artifacts Rechecked

Primary source packet:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/`

Latest prior validator referenced:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/ads-intl/GOOGLE_ADS_INTL_PACKET_RECHECK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/ads-intl/GOOGLE_ADS_INTL_PACKET_RECHECK_SUMMARY.json`

Latest prior parked-gate context referenced:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-checkout-merchant-pinterest-readbacks/lanes/ads-gate/ADS_IMPORT_PARKED_GATE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/ads-gate/ADS_IMPORT_PARKED_CURRENCY_GATE.md`

## Current Local Validation

| Check | Current local readback |
|---|---:|
| Manifest status | Local draft only; paused-only if approved for import |
| Owner approval required before import | true |
| Approval given in this lane | false |
| Google Ads browser/API used | false |
| Import/create authorized | false |
| Non-US draft campaigns | 17 |
| Countries | GB, CA, AU, CH, DK, DE, NL, SE, FR, BE, ES, IT, PL, CZ, RO, GR, PT |
| Campaign rows in web bulk CSV | 17 |
| Ad group rows | 204 |
| Positive keyword rows | 612 |
| Positive match types | 306 exact, 306 phrase, 0 broad |
| Campaign negative rows | 629 |
| RSA/ad rows | 204 |
| Web bulk data rows | 1666 |
| Bulk actions | 1666 `Add` rows |
| Non-paused importable rows found | 0 |
| Campaign type/network | Search / Google search |
| Bid strategy | Manual CPC |
| Campaign budgets in local draft | $1.00 and $2.00 daily paused shells |
| Max default CPC found | $0.15 |
| CPC values over $0.20 | 0 |
| PMax / Performance Max rows | 0 |
| Standard Shopping / campaign `23802638621` rows | 0 |
| Product-scope rows | 0 |
| Feed-label rows | 0 |
| Product-group rows | 0 |
| Conversion-goal edit rows | 0 |

Note: negative keyword rows include broad/phrase/exact negative match types, which is expected for campaign negatives. The positive keyword rows are exact/phrase only.

## Approval Gate

The source packet approval gate remains the required action-time gate:

`APPROVE PAUSED INTERNATIONAL GROWTH BUILD: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR US, UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; CREATE PAUSED PINTEREST US CATALOG/RETARGETING DRAFTS ONLY IF TAG/CATALOG GATES PASS; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES.`

Approval status for this lane: `NOT_APPROVED_IN_THIS_LANE`.

If the owner later gives different wording, a narrower country scope, or an ambiguous instruction, the parent/orchestrator should clarify before opening Google Ads or previewing a bulk upload.

## Current PT / URL Gate Implication

The Ads packet remains internally valid as parked infrastructure, but it is not launch-ready and not import-approved. The parent lane is still resolving PT checkout-to-shipping and market-localized ad URL behavior so fresh ad traffic does not start in the wrong market/currency.

Until the parent clears those gates, this lane should remain parked even if the local Ads CSV continues to validate.

## Residual Risks

- No live Google Ads account state was refreshed here by instruction.
- Presence-only location targeting may need action-time Google Ads UI/API readback because bulk formats can be limited.
- English-only shells are infrastructure, not local-language launch readiness.
- PT checkout, market-localized ad URL behavior, Merchant age-group processing, Pinterest event/catalog quality, tracking, and economics gates remain outside this lane and can still block any future import or enablement.
- Future bulk upload must start as preview-only and must not apply if any preview error, non-paused entity, PMax, Shopping, feed/product, conversion-goal, or unauthorized budget/bid/status change appears.

## Commands Run

- `sed` / `tail` reads for required memory, coordination, paid-growth, and Google Ads continuity files.
- `rg --files` over the prior Ads source packet and prior Ads gate reports.
- `sed` reads for `manifest.json`, prior validator summaries, parked-gate reports, and `manual_qa/approval_gate.md`.
- Inline `python3` CSV/JSON validators for source-packet counts, bulk row types, paused statuses, positive match types, CPC caps, prohibited row scans, and approval-gate flags.

## Handoff

Keep Ads import parked. The next safe Ads-lane action is no action unless the parent/orchestrator receives exact owner approval. If exact approval is later given, the parent should claim the live Google Ads write lane, rerun local validation, perform just-in-time account readbacks, run a preview-only bulk upload, and apply only if the preview is clean and all imported entities remain paused. No spend or enablement is authorized by this packet.
