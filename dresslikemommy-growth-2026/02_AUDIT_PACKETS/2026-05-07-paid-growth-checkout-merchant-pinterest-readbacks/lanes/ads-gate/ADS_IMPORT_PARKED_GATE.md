# Ads Import Parked Gate

Lane: Ads paused import parked gate
Date: 2026-05-07 EDT / 2026-05-08 UTC
Scope: local documentation only
Status: `PARKED_NOT_APPROVED`

## Result

The paused international Google Search import remains parked. No Google Ads browser, API, import, create, enable, pause, budget, bid, status, conversion, product-scope, product-group, feed-label, Merchant, Shopify, Pinterest, or live spend action was taken in this lane.

Even paused campaign creation is a live Google Ads write. The local packet can only move from parked to preview/import if the parent/orchestrator receives the exact action-time owner approval phrase and completes just-in-time readbacks first.

## Current Approval Status

Approval status: `NOT_APPROVED_IN_THIS_LANE`

Required exact approval phrase from the source packet:

`APPROVE PAUSED INTERNATIONAL GROWTH BUILD: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR US, UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; CREATE PAUSED PINTEREST US CATALOG/RETARGETING DRAFTS ONLY IF TAG/CATALOG GATES PASS; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES.`

If approval arrives with different wording, narrower country scope, or any ambiguity around Google Ads import/create, the parent should pause and clarify before opening Google Ads.

## Latest Local Packet Validation Referenced

Latest validation artifact:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/ads-intl/GOOGLE_ADS_INTL_PACKET_RECHECK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/ads-intl/GOOGLE_ADS_INTL_PACKET_RECHECK_SUMMARY.json`

Source packet:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/`

Prior gate context:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-continuation-readbacks/lanes/ads-gate/GOOGLE_ADS_IMPORT_GATE.md`

Latest validation summary:

| Check | Latest local result |
|---|---:|
| Non-US paused draft campaigns | 17 |
| Countries | GB, CA, AU, CH, DK, DE, NL, SE, FR, BE, ES, IT, PL, CZ, RO, GR, PT |
| New US campaigns | 0 |
| Existing US template | `23827590655` only |
| Ad groups | 204 paused |
| Keywords | 612 paused |
| Positive match types | 306 exact, 306 phrase, 0 broad |
| Campaign negatives | 629 |
| RSAs | 204 paused |
| Web bulk rows | 1666 |
| Bid strategy | Manual CPC |
| Max CPC found | $0.15 |
| CPC values over $0.20 | 0 |
| PMax / Standard Shopping / product-scope / feed-label / product-group / conversion-goal edit rows | 0 |
| Google Ads live action in latest validation | No |

Local readiness therefore remains `PASS_FOR_PAUSED_PACKET_ONLY`, not approval to import and not approval for spend.

## Just-In-Time Pre-Import Readbacks Required If Approval Arrives

Before any future bulk-upload preview or paused import apply, the parent/orchestrator should complete these gates in order:

1. Confirm the current-session owner approval exactly covers paused Google Search campaign creation/import and still includes no live spend, no enable, no PMax, no Standard Shopping changes, no product-scope expansion, no feed-label changes, no product-group changes, and no conversion-goal changes.
2. Re-read `ops/AGENT_COORDINATION.md` and confirm no conflicting Google Ads writer is active. The parent must own any live Google Ads write claim before preview/apply.
3. Read back Google Ads account context and confirm the correct account is open before touching bulk upload.
4. Read back existing US nonbrand Search campaign `23827590655`; it must still exist and remain paused. Do not create a duplicate US nonbrand campaign.
5. Read back that Standard Shopping campaign `23802638621` is not part of the import scope and will not be changed.
6. Read back that PMax and Remarketing campaigns are not part of the import scope and will not be changed.
7. Read back purchase measurement posture before import: no conversion-goal edits, and account-default Purchases remains the inherited goal path.
8. Re-run the local packet validator against the source CSVs and web bulk upload: all campaigns/ad groups/keywords/RSAs paused, Manual CPC, max CPC at or below `$0.20`, exact/phrase only, no broad positives, no prohibited PMax/Standard Shopping/feed/product/conversion rows.
9. Re-scan RSA copy for unsupported claims: no fast/free shipping promises, no return-shipping confusion, no warehouse/store/local-inventory/stocked-inventory claims, no promos/reviews/bestseller claims unless newly verified.
10. Confirm landing-language posture by market: English-only shells are still conservative draft infrastructure; local-language ad copy must not be imported where landing-page quality has not passed QA.
11. Confirm the import file is still the paused-only bulk CSV from the source packet, not an edited or generated replacement.
12. Run Google Ads bulk-upload preview first. Do not apply if preview has errors, creates non-paused entities, changes budget/bid/status outside the packet, adds Search Partners/Display/PMax, creates US duplicates, touches Standard Shopping/PMax/Remarketing, or includes conversion/product/feed edits.
13. Confirm intended targeting in preview/readback where visible: one country per campaign, Google Search only, no Display, no Search Partners, Manual CPC, default max CPC at or below `$0.20`, and paused status throughout.
14. Only after a clean preview and still-current approval, apply the paused-only import. Spend/enable remains separately blocked.

## Post-Import Readbacks Before Any Future Enable Request

If a future approved paused import is applied, it still would not authorize spend. Before any separate enable request, the parent should read back:

- Every imported campaign, ad group, keyword, negative, and RSA is paused.
- One country per campaign and presence-only location setting.
- Google Search only; no Display, Search Partners, broad match, AI Max, or PMax.
- Manual CPC with every CPC cap at or below `$0.20`.
- Campaign negatives present.
- Policy/ad review status is clean enough for a controlled test.
- Country-specific landing, route/currency, no-payment checkout, Merchant/catalog, tracking, and economics gates pass.

## Residual Risks

- No live Google Ads account state was refreshed in this lane.
- Presence-only location targeting may require Google Ads UI/API readback because bulk formats can be limited.
- English-only shells are infrastructure, not local-language launch readiness.
- International live spend remains blocked until checkout, catalog/feed, tracking, and economics gates clear and the owner separately approves enablement.
- This subagent was instructed to write only under this `ads-gate` lane, so no worklog or coordination file was updated here.

## Handoff

Keep the Ads import parked. The next safe parent action is either to maintain the parked state, or, if the exact approval arrives, run the just-in-time readbacks above and start with preview-only bulk upload. Do not apply or enable anything from this lane by inference.
