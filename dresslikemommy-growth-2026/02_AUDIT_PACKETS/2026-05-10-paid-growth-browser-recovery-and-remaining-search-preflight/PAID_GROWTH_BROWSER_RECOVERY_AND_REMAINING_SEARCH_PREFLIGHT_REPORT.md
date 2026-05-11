# Paid Growth Browser Recovery And Remaining Search Preflight

Date: 2026-05-10

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-browser-recovery-it-pl-paused-search-built`

## Scope

Continue the paid-growth sprint as parent/orchestrator from the prior state where 9 paused non-US Search campaigns existed and the `IT` bulk-upload preview was still in progress.

Allowed by existing owner-approved TEST BUILD scope:
- Resume only unresolved non-US paused Search countries.
- Apply only after a fresh completed `88/88` preview result and downloaded result validation.
- Keep all new entities paused.
- Read back each applied campaign and repair only the known positive geo-targeting mode to presence-only if Google Ads defaulted it to broad.

Blocked:
- Live spend or campaign enablement.
- Existing campaign budget/bid/status changes.
- Standard Shopping, PMax, US campaign `23827590655`, conversion goals, Merchant, Shopify product data, Pinterest, product/feed/product-group/feed-label/product-scope, theme, account/billing, credential, checkout payment, or order changes.

## Parent Actions

1. Read the canonical paid-growth prompt and required continuity files.
2. Claimed the browser recovery + unresolved Search lane in `ops/AGENT_COORDINATION.md`.
3. Spawned three disjoint sidecars:
   - Ads CSV revalidation.
   - Public measurement preflight.
   - Native-copy risk triage.
4. Recovered browser access after direct Browser/Playwright MCP launch paths hit a locked Chrome profile by using the already-authenticated Chrome remote-debugging session on port `9222`.
5. Rechecked the Google Ads bulk-upload history and found the stale `IT` preview had completed cleanly.
6. Applied `IT` and `PL` one at a time from validated `88/88` previews, downloaded and validated the apply result files, then read back campaigns through the Google Ads RPC path.
7. Repaired the known Google Ads geo-targeting default on both new campaigns from positive `DONT_CARE` to `LOCATION_OF_PRESENCE`.

## Google Ads Results

New paused Search campaigns now exist and final readback passed:

| Country | Campaign ID | Campaign Name | Budget | Final Status | Final Geo | Notes |
|---|---:|---|---:|---|---|---|
| `IT` | `23829232530` | `DLM_IT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1/day` | Paused Search | Positive and negative `LOCATION_OF_PRESENCE` | Preview/apply both `88/88 # OK`; needed narrow presence-only repair |
| `PL` | `23829238698` | `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `$1/day` | Paused Search | Positive and negative `LOCATION_OF_PRESENCE` | Preview/apply both `88/88 # OK`; needed narrow presence-only repair |

Final campaign readbacks for both show:
- `campaign_status_interpreted`: `PAUSED`
- `advertising_channel_type_interpreted`: `SEARCH`
- `target_google_search`: `true`
- `target_content_network`: `false`
- `target_youtube_video`: `false`
- `budget_usd`: `1.0`
- positive and negative geo target type: `LOCATION_OF_PRESENCE`

The approved paused non-US Search build is now at 11 of 17 campaigns applied and read back clean:
- Existing clean before this packet: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`.
- Newly completed in this packet: `IT`, `PL`.
- Remaining unresolved: `CZ`, `RO`, `PT`, `GR`, `FR`, `BE`.

## Lane Results

### Ads CSV Revalidation

`PASS_LOCAL_ONLY`.

All unresolved split CSVs revalidated locally:
- `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, `GR`
- 88 rows each.
- Row counts per file: 1 Campaign, 10 Ad groups, 30 Keywords, 37 Negative keywords, 10 Ads.
- All importable statuses paused.
- Checksums match the existing manifest.
- No stale beach/Vacation Family URL hits.

Report: `lanes/ads-csv-revalidation/ADS_CSV_REVALIDATION_REPORT.md`

### Public Measurement Preflight

`BLOCKED_BY_PUBLIC_429_AND_PURCHASE_EVENT_GAP_NOT_CLOSED`.

Low-volume public probes for `PL`, `CZ`, `RO`, `PT`, and `GR` all returned Shopify `429`, so the lane stopped without retrying. This did not affect Ads account work and did not close the larger non-US purchase-event currency proof gap.

Report: `lanes/public-measurement-preflight/PUBLIC_MEASUREMENT_PREFLIGHT_REPORT.md`

### Native Copy Risk Triage

`PASS_LOCAL_ONLY_STATUS_UNCHANGED`.

The lane confirmed English-first paused infrastructure is a build-control choice, not native-language launch readiness. Main copy risks remain:
- `pt-PT` Ads copy while storefront serves `pt-BR`.
- `da-DK` row with `Mamma datter kjoler` needs native rewrite.
- `fr-BE`/`nl-BE` need a Belgium language-split decision.

Report: `lanes/native-copy-risk-triage/NATIVE_COPY_RISK_TRIAGE.md`

## Evidence

IT:
- `raw/it-preview/bulk_upload_history_recheck_body.txt`
- `raw/it-preview/downloads/preview/IT_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json`
- `raw/it-preview/downloads/apply/IT_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json`
- `raw/after-readbacks/IT_campaign_rpc/post_apply_summary.json`
- `raw/after-readbacks/IT_campaign_rpc/post_presence_repair_summary.json`
- `raw/remaining-readback/IT_campaign_rpc/final_validated_summary.json`

PL:
- `raw/pl-apply/PL_preview_detail_body_before_apply.txt`
- `raw/pl-apply/downloads/preview/PL_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json`
- `raw/pl-apply/downloads/apply/PL_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json`
- `raw/after-readbacks/PL_campaign_rpc/post_apply_summary.json`
- `raw/after-readbacks/PL_campaign_rpc/post_presence_repair_summary.json`
- `raw/remaining-readback/PL_campaign_rpc/final_validated_summary.json`

## Problems Updated

- `PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE`: moved from 9 applied to 11 applied; `IT` no longer in-progress/absent, and `PL` no longer absent.
- `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE`: no status change; added the native-copy risk triage attempt.
- `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`: opened/updated because non-US purchase-event currency remains unproven and the public preflight was blocked by 429.

## Current State

Do not redo:
- Do not re-upload or re-apply `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, or `PL`.
- Do not request the same paused non-US Search TEST BUILD approval again.

Next safest Ads order:
1. `CZ`
2. `RO`
3. `PT`
4. `GR`
5. `FR` only after a fresh non-stale completed `88/88 # OK` preview and careful no-duplicate readback.
6. `BE` last after upload-throttle cooldown.

Stop criteria:
- Any in-progress/stale preview.
- Any preview/apply result other than `88` rows and all `# OK`.
- Any account/login/CAPTCHA/billing/account-switch interrupt.
- Any unexpected existing campaign duplicate.
- Any row touching protected surfaces or existing campaigns.
- Any final readback that is not paused Search, expected budget, content/YouTube off, and presence-only.
