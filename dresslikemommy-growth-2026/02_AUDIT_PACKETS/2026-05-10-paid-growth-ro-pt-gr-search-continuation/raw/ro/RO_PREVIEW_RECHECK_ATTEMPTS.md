# RO Preview Recheck Attempts

Generated: 2026-05-10

Scope: parent/orchestrator Google Ads control lane, existing Chrome CDP session `9222`, no new upload, no apply click, no live spend.

## Attempt 1: Existing Page, No Reload

Command:

`NODE_PATH=/opt/homebrew/lib/node_modules node dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/working/google_ads_existing_preview_recheck.js RO`

Terminal result:

```json
{
  "country": "RO",
  "status": "PREVIEW_IN_PROGRESS_ERROR_0",
  "statusPath": "dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/raw/ro/existing_preview_recheck_status.json"
}
```

Interpretation: the existing `RO` preview was not a clean completed `88/88 # OK` preview and could not be applied.

Note: the helper writes `existing_preview_recheck_status.json` to a stable path. Attempt 2 intentionally refreshed the same path, so this note preserves Attempt 1 terminal output.

## Attempt 2: Reload And 90-Second Poll

Command:

`NODE_PATH=/opt/homebrew/lib/node_modules node dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/working/google_ads_existing_preview_recheck.js RO --reload --wait-ms=90000`

Saved status: `existing_preview_recheck_status.json`

Result:

```json
{
  "country": "RO",
  "filename": "RO_intl_search_paused_draft_web_bulk.csv",
  "status": "PREVIEW_FILE_NOT_VISIBLE",
  "checkedAt": "2026-05-10T07:58:06.035Z",
  "applyRequested": false,
  "reload": true,
  "waitMs": 90000
}
```

Interpretation: after a refreshed upload-history readback, the prior `RO` preview was no longer visible as a completed preview row; visible history showed other upload rows, but no `RO_intl_search_paused_draft_web_bulk.csv` or `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`.

## Campaign Absent Readbacks

Post-recheck RPC readbacks confirmed:

- `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`: `found=false`
- `DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`: `found=false`
- `DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`: `found=false`

Evidence: `raw/campaign-absent-readbacks/*_campaign_rpc/initial_summary.json`.

## Decision

`RO` is parked as stale/not-visible rather than applied. `PT` and `GR` were not attempted because the one-country-at-a-time guard forbids stacking more uploads behind an unresolved `RO` preview path.
