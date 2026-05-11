# Ads Resume Order Report

AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-orchestrator-safe-resume
Lane: A / Ads-Resume-Order
Generated: 2026-05-10 (subagent local, read-only audit; no live writes)
Problem: PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE
Posture: 9 of 17 paused non-US Search shells already created and final-readback passed (`GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`). Remaining 8 (`FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, `GR`) are unbuilt or stale-preview parked. This report verifies the held split CSVs and proposes the safest resume sequence.

## Files audited

Source manifest packet:
`/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/`

Split CSVs reviewed (one row = one Google Ads importable entity, plus 1 header line, hence file lines = 89 / data rows = 88):

| Country | File path | Data rows | SHA-256 |
|---|---|---|---|
| FR | `.../split_csvs/FR_intl_search_paused_draft_web_bulk.csv` | 88 | `02025e1c1c2cfb42abac7f5138b773b0843afcfc28bcfda0ef0d289b371f5aa8` |
| BE | `.../split_csvs/BE_intl_search_paused_draft_web_bulk.csv` | 88 | `273fb256f44b084520f2d8bc1bdfddafa26b0a823b62282371719bf79003327d` |
| IT | `.../split_csvs/IT_intl_search_paused_draft_web_bulk.csv` | 88 | `adfbf9aedd13ec2d92c2a57737672e476332328b00cb2ce2a01dc71c30597377` |
| PL | `.../split_csvs/PL_intl_search_paused_draft_web_bulk.csv` | 88 | `3ce7a8df5fc7a5e8c248d2441c57154d8e9e1aee575a6dd826a76906bb00bd76` |
| CZ | `.../split_csvs/CZ_intl_search_paused_draft_web_bulk.csv` | 88 | `a2e20892564494d10aacf42792be1310df55c473054be456ab16cefa1fd05b55` |
| RO | `.../split_csvs/RO_intl_search_paused_draft_web_bulk.csv` | 88 | `b3e9eac7c59d06813c3c2b7089c4d46d21c6e92f0d0c5459eab71b5c73a43001` |
| PT | `.../split_csvs/PT_intl_search_paused_draft_web_bulk.csv` | 88 | `5a02a1cff436d7de6444b3462c8017c37742a87bb0fb85f2a0a071e08cdb47a7` |
| GR | `.../split_csvs/GR_intl_search_paused_draft_web_bulk.csv` | 88 | `48c88f4b5f2e9fb44b85e5bb27eb79539707075a7ba622ef530d9cb1a9b2fc8f` |

All 8 SHA-256s match the lane's `SHA256SUMS.txt` and `manifest.json` exactly. Files are unmodified since the 2026-05-09 generation pass.

## Per-country audit results

Row-type breakdown is identical across all 8 files: 1 Campaign + 10 Ad group + 30 Keyword + 37 Negative keyword + 10 Ad = 88 data rows. Every status field for Campaign/Ad group/Keyword/Ad rows is `Paused`; Negative keyword rows have blank status (Google Ads import-correct). Campaign-row `Location` is set to the target country name and `Location Goal for Target IS` is blank. No file contains the strings `DONT_CARE`, `Presence and interest`, `PMax`, `Performance Max`, `Standard Shopping`, `Shopping`, `conversion goal`, `product scope`, `feed label`, `product group`, `Merchant feed`, or the bad URL handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`. No row references any of the 11 protected campaign IDs.

| Country | File present | Total rows | Paused rows | Presence-only (no DONT_CARE / no "Presence and interest") | Max CPC observed | Forbidden-surface hits | Bad-handle hits | Forbidden campaign-ID hits | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| FR | yes | 88 | 88/88 | yes | $0.12 | 0 | 0 | 0 | PASS |
| BE | yes | 88 | 88/88 | yes | $0.12 | 0 | 0 | 0 | PASS |
| IT | yes | 88 | 88/88 | yes | $0.12 | 0 | 0 | 0 | PASS |
| PL | yes | 88 | 88/88 | yes | $0.10 | 0 | 0 | 0 | PASS |
| CZ | yes | 88 | 88/88 | yes | $0.10 | 0 | 0 | 0 | PASS |
| RO | yes | 88 | 88/88 | yes | $0.10 | 0 | 0 | 0 | PASS |
| PT | yes | 88 | 88/88 | yes | $0.10 | 0 | 0 | 0 | PASS |
| GR | yes | 88 | 88/88 | yes | $0.10 | 0 | 0 | 0 | PASS |

Note on presence-only: web-bulk CSV cannot itself encode the Google Ads location-targeting option (`People in or regularly in your included locations`). The CSVs do NOT contain the positive `DONT_CARE` pattern that produced the GB pre-repair failure, so they are safe for upload, but the operator must still readback the campaign Location options panel after preview/apply for each country and run the same narrow presence-only repair if the default lands at "Presence and interest". Max CPC across all 8 files is at or below the project local cap of $0.15 (FR/BE/IT at $0.12; PL/CZ/RO/PT/GR at $0.10).

## Safest resume order with rationale

1. PL  - unattempted, lowest CPC ($0.10), no prior throttle/preview baggage, smallest blast radius for re-establishing a clean upload cadence.
2. CZ  - unattempted, $0.10, parallel structure to PL.
3. RO  - unattempted, $0.10, lower-CPC discovery tier.
4. PT  - unattempted, $0.10, lower-CPC discovery tier.
5. GR  - unattempted, $0.10, lower-CPC discovery tier; finishes the clean unattempted block.
6. IT  - prior preview was stuck at `0/0/0 in progress`; only resume after that stale preview clears or is cancelled in the Ads UI. Do not click Apply on a still-in-progress preview.
7. FR  - prior preview produced "completed with errors / no changes" with no FR campaign created; resume only after a fresh `88/88 # OK` preview is generated and read back.
8. BE  - resume last; Google Ads returned a multi-spreadsheet upload throttle on the prior attempt. Spacing it last gives the throttle the longest cool-down window and lets the 5 unattempted, then IT, then FR, soak the upload pipeline first.

Per-country pacing rule: one country at a time, full preview-then-readback cycle (`88/88 # OK` preview, apply, then read back campaign + first ad group + first keyword + first ad + Locations panel + Networks panel). Do not chain uploads.

## Stop criteria for the next operator

Stop immediately and update `ops/PROBLEM_TRACKER.md` (`PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE`) before continuing if any of the following occur:

- Preview row count, ad-group count, keyword count, or ad count does not equal `88 / 10 / 30 / 10` or shows any error/warning row.
- Preview remains in progress (`0/0/0` or any non-final `success/error/in progress` state) after a bounded wait (3 minutes is the prior precedent for IT staleness).
- Google Ads returns any upload throttle / "too many simultaneous uploads" / "too many recent spreadsheets" message.
- Any account, login, two-factor, CAPTCHA, identity-verification, or billing modal interrupts the flow.
- Preview or applied campaign exposes Locations option = "Presence and interest" / `DONT_CARE` (run the same narrow approved presence-only repair used for GB; do not skip readback).
- Any forbidden-surface row appears in preview output: PMax, Performance Max, Standard Shopping, Shopping, conversion goal, product scope, feed label, product group, Merchant feed, or any reference to one of the 11 protected campaign IDs.
- Any row attempts to enable, change budget, change bid, change status to anything other than Paused, or modify the US campaign `23827590655`.

## Guardrails preserved

- No live spend, no campaign enablement, no budget/bid/status changes.
- No PMax enable, no Standard Shopping changes.
- No product-scope / feed-label / product-group / conversion-goal changes.
- No Merchant uploads, no Shopify product-data writes.
- No edits to any of the 11 existing campaign IDs.
- No browser or account writes performed by this subagent. This audit was local read-only.

## Files touched

WRITTEN by this subagent (lane report only):
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/ads-resume-order/ADS_RESUME_ORDER_REPORT.md`

READ by this subagent (no modifications):
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/AGENT_WORKLOG.md` (anchor lookup only)
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/SHA256SUMS.txt`
- `.../google-ads-split-manifest/campaign_row_counts.csv`
- `.../google-ads-split-manifest/manifest.json`
- `.../google-ads-split-manifest/split_csvs/{FR,BE,IT,PL,CZ,RO,PT,GR}_intl_search_paused_draft_web_bulk.csv`
