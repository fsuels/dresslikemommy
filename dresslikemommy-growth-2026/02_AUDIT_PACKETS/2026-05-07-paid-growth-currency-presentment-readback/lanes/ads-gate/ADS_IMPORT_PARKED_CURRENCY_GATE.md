# Ads Import Parked Currency Gate

Lane: Ads parked-gate subagent  
Scope: local artifact revalidation only  
Status: `PARKED_NOT_APPROVED_CURRENCY_GATE_BLOCKED`

## Result

The international Google Search import remains explicitly parked. I did not access Google Ads, Merchant Center, Shopify Admin, Pinterest, or any live account surface. I did not import, create, enable, pause, change budgets, change bids, change status, edit conversion goals, alter product scope, edit feed labels, edit product groups, touch PMax, touch Standard Shopping, or authorize spend.

Even paused campaign creation is a live Google Ads write. This lane confirms only that the existing local packet is still parked and still requires exact action-time owner approval before any preview/import workflow.

## Local Packet Status

Source packet rechecked:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/`

Referenced latest local validation:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/ads-intl/GOOGLE_ADS_INTL_PACKET_RECHECK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/ads-intl/GOOGLE_ADS_INTL_PACKET_RECHECK_SUMMARY.json`

Local status remains:

| Check | Local readback |
|---|---:|
| Manifest status | Local draft only; paused-only if approved for import |
| Owner approval required before import | true |
| Latest validation result | pass |
| Latest approval status | not approved in that lane |
| Google Ads browser/API used in validation | false |
| Import/create authorized | false |
| Non-US draft campaigns | 17 |
| Countries | GB, CA, AU, CH, DK, DE, NL, SE, FR, BE, ES, IT, PL, CZ, RO, GR, PT |
| Ad groups | 204 |
| Keywords | 612 |
| Positive match types | 306 exact, 306 phrase, 0 broad |
| Campaign negatives | 629 |
| RSAs | 204 |
| Web bulk rows | 1666 |
| Distinct status values in bulk CSV | Paused only |
| Max CPC found | $0.15 |
| CPC values over $0.20 | 0 |
| PMax / Performance Max bulk rows | 0 |
| Standard Shopping / campaign `23802638621` bulk rows | 0 |
| Product-scope bulk rows | 0 |
| Feed-label bulk rows | 0 |
| Product-group bulk rows | 0 |
| Conversion-goal bulk rows | 0 |

Evidence file written in this lane:

- `ADS_IMPORT_PARKED_CURRENCY_GATE_EVIDENCE.json`

## Currency Gate

The Ads import is also parked behind the current international currency/presentment blocker. Prior checkout QA showed ES, IT, RO, and PT routes and outbound rates passing no-payment checks, but product currency meta / Shopify currency signal and cart shipping-rate currency still read `USD` where `EUR` was expected.

That means international live spend remains blocked even if the paused packet itself is internally consistent. The next safe work is read-only currency/presentment investigation and, if needed, a browser walkthrough to the shipping step only with no payment and no order.

## Exact Approval Gate

Required exact action-time owner approval from the source packet:

`APPROVE PAUSED INTERNATIONAL GROWTH BUILD: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR US, UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; USE TIGHT EXACT/PHRASE KEYWORDS, LOCAL LANGUAGE ONLY WHERE LANDING PAGE QUALITY IS ACCEPTABLE, ENGLISH ONLY WHERE LOCALIZATION IS NOT READY, CPC CAPS AT OR BELOW $0.20, NO LIVE SPEND; CREATE PAUSED PINTEREST US CATALOG/RETARGETING DRAFTS ONLY IF TAG/CATALOG GATES PASS; READ BACK BEFORE AND AFTER; NO ENABLE, NO PMAX, NO STANDARD SHOPPING CHANGES, NO PRODUCT SCOPE EXPANSION, NO FEED LABEL CHANGES, NO PRODUCT GROUP CHANGES, NO CONVERSION-GOAL CHANGES.`

If the owner gives different wording, a narrower country scope, or any ambiguous instruction, the parent/orchestrator should clarify before opening Google Ads or previewing a bulk upload.

## Blockers

- Exact owner approval has not been given in this lane.
- Currency/presentment is not cleared for ES/IT/RO/PT; prior readbacks still showed `USD` where `EUR` was expected.
- Merchant paid-cohort age-group diagnostics remain partially improved but not cleared.
- Pinterest Event Quality and full item proof remain blocked/partial.
- No live Google Ads state was refreshed here by instruction.

## Next Safe Action

Keep Ads import parked. The next safe parent action is read-only currency/presentment investigation for ES/IT/RO/PT, then continued Merchant/Pinterest read-only gates. If exact Ads approval later arrives, the parent should run just-in-time readbacks and a preview-only bulk upload first; applying a paused import still must preserve no live spend, no enable, no PMax, no Standard Shopping, no product/feed scope changes, and no conversion-goal changes.

## Commands Run

- `pwd && rg --files -g 'AGENTS.md' -g 'ops/AGENT_COORDINATION.md' -g 'ops/GOOGLE_ADS_CONTINUITY.md' -g 'ops/AGENT_WORKLOG.md' -g 'ops/GROWTH_NORTH_STAR.md' -g 'ops/prompts/paid-growth-ai-army-continuation-prompt.md'`
- `tail -n 220 ops/AGENT_WORKLOG.md`
- `sed -n '1,260p' ops/AGENT_COORDINATION.md`
- `sed -n '1,260p' ops/GOOGLE_ADS_CONTINUITY.md`
- `rg -n "Google Ads international|intl|paused international|Ads gate|ADS_IMPORT|exact owner approval|currency|presentment|international Search|PARKED" AGENTS.md ops/AGENT_WORKLOG.md ops/AGENT_COORDINATION.md ops/GOOGLE_ADS_CONTINUITY.md`
- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS -path '*google-ads-intl-search*' -o -path '*ads-gate*' | sort`
- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search -maxdepth 3 -type f | sort`
- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/ads-intl dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-checkout-merchant-pinterest-readbacks/lanes/ads-gate -maxdepth 2 -type f | sort`
- `sed -n '1,220p' .../google-ads-intl-search/manifest.json`
- `sed -n '1,240p' .../google-ads-intl-search/manual_qa/approval_gate.md`
- `sed -n '1,240p' .../lanes/ads-intl/GOOGLE_ADS_INTL_PACKET_RECHECK.md && sed -n '1,220p' .../lanes/ads-intl/GOOGLE_ADS_INTL_PACKET_RECHECK_SUMMARY.json`
- `sed -n '1,220p' .../lanes/ads-gate/ADS_IMPORT_PARKED_GATE.md`
- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/ads-gate -maxdepth 2 -type f -print`
- Inline `python3` CSV/JSON revalidator for manifest status, approval status, bulk row count, paused statuses, CPC checks, match types, prohibited row scans, and approval-gate presence.
- `python3 -m json.tool dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/ads-gate/ADS_IMPORT_PARKED_CURRENCY_GATE_EVIDENCE.json >/dev/null`
- `git diff --check -- dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/ads-gate`
- `git diff --stat -- dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/ads-gate && git status --short -- dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/ads-gate AGENTS.md ops/AGENT_WORKLOG.md ops/AGENT_COORDINATION.md ops/GOOGLE_ADS_CONTINUITY.md`
- `sed -n '1,260p' dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-currency-presentment-readback/lanes/ads-gate/ADS_IMPORT_PARKED_CURRENCY_GATE.md`
