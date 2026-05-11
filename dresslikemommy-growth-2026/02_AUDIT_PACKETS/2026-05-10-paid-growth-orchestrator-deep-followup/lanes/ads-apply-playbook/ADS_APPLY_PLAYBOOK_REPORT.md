# Ads Apply Playbook Report

AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-orchestrator-deep-followup
Lane: A / Ads-Apply-Playbook
Generated: 2026-05-10 (subagent local, read-only audit + this report only; no live writes)
Problem: PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE
Posture: Resume order is fixed (`PL -> CZ -> RO -> PT -> GR -> IT -> FR -> BE`). This file is the per-country paste-execute playbook for the next browser-enabled operator.

Scope: 8 unresolved countries only (PL, CZ, RO, PT, GR, IT, FR, BE). The 9 already-applied countries (GB, CA, AU, CH, DK, DE, NL, SE, ES) are out of scope.

Hard guardrails (apply to every country, every step):
- Paused-only test build. No live spend, no enable, no budget/bid/status edit.
- No PMax / Standard Shopping / Performance Max changes. No Merchant uploads. No edits to any of the 11 protected campaign IDs.
- One country at a time, full preview-then-apply-then-readback cycle. Do not chain uploads.
- USD across the whole MCC (customer_id `220823493`) - no per-country currency switch in the import. Confirmed by `final_validated_summary.json` for AU/SE/CH which all read `"currency": "USD"`.

---

## Source-of-truth parsing (one-shot, do not skip)

All numeric claims below are produced by the following commands. Re-run them before each apply to detect any silent drift in the held CSVs.

```
SPLIT="/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs"

# Per-country line count + budget + language + location
for C in PL CZ RO PT GR IT FR BE; do
  F="$SPLIT/${C}_intl_search_paused_draft_web_bulk.csv"
  echo "=== $C ==="
  echo "data rows: $(($(wc -l < "$F") - 1))"
  awk -F, '$1=="Campaign" {print "Campaign name="$5; print "Budget="$8; print "Language="$15; print "Location="$16}' "$F"
  awk -F, 'NR>1 {print $1}' "$F" | sort | uniq -c
  awk -F, '$1=="Ad group" {cpc=$39} END {print "ad-group default max CPC: "cpc}' "$F"
done
```

Result for all 8 files (consistent):
- 88 data rows = 1 Campaign + 10 Ad group + 30 Keyword + 37 Negative keyword + 10 Ad
- Budget value in CSV column 8 = `1.00` (units = MCC currency = USD)
- Language column 15 = `en` for every campaign
- Location column 16 = country name (Poland / Czechia / Romania / Portugal / Greece / Italy / France / Belgium)
- Default max CPC column 39 = `0.10` for PL/CZ/RO/PT/GR; `0.12` for IT/FR/BE
- The header has no `Currency` column - the import inherits MCC currency (USD), confirmed by every applied country's `<C>_campaign_rpc/initial_summary.json` (`"currency": "USD"`).

Expected preview success readout per country (Google Ads UI strings, Chinese locale): `预览已完成 / 更改 88 / 成功 88 / 错误数 0` (English equivalent: `Preview complete / Changes 88 / Success 88 / Errors 0`). This is the only acceptable preview state to click Apply on.

---

## Per-country playbook

For every country: only the file path, the count gate, the budget/currency, the locale-of-import, the post-apply RPC target, and the per-country preflight differ. Everything else is in the common preflight / postflight blocks below.

### 1. PL (first to resume)

- Split CSV path:
  `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/PL_intl_search_paused_draft_web_bulk.csv`
- Expected preview rows: `88 changes / 88 success / 0 errors` = 1 Campaign + 10 Ad group + 30 Keyword + 37 Negative keyword + 10 Ad. Verify with `awk -F, 'NR>1 {print $1}' "$F" | sort | uniq -c`.
- Currency assumed by import: `USD` (MCC inherited; CSV has no Currency column).
- Budget value (CSV col 8 of Campaign row): `1.00` USD daily.
- Default max CPC (CSV col 39, all ad groups): `0.10` USD.
- Expected RPC readback target (after apply, same shape as `AU_campaign_rpc/final_validated_summary.json`):
  - `campaign_name = "DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"`
  - `campaign_status_interpreted = "PAUSED"` (`campaign_status_code: 5`)
  - `advertising_channel_type_interpreted = "SEARCH"`
  - `budget_micros = "1000000"` -> `budget_usd = 1.0`
  - `currency = "USD"` / `customer_id = "220823493"`
  - `target_google_search = true`
  - `target_search_network = null OR false` (search-partners OFF)
  - `target_content_network = false` (display network OFF)
  - `target_youtube_video = false` (YouTube OFF)
  - `positive_geo_target_type_interpreted = "LOCATION_OF_PRESENCE"`
  - `negative_geo_target_type_interpreted = "LOCATION_OF_PRESENCE"`
  - `geo_target_type_setting_raw = {"16": 18, "17": 18}`
  - `languages = ["英语"]` (zh-CN render of "English")
- Per-country preflight: none specific. PL is the clean restart; use it to reseed the upload cadence.
- Do-not-click list (PL):
  - Do not click Enable on the campaign.
  - Do not change the daily budget from $1.00.
  - Do not add or change conversion goals.
  - Do not edit ad groups, keywords, or RSAs.
  - Do not change geo targeting; leave at the imported `LOCATION_OF_PRESENCE` (run the GB-style narrow presence-only repair only if Locations panel reads "Presence and interest").
  - Do not click Apply unless preview reads `88 / 88 / 0`.

### 2. CZ

- Split CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/CZ_intl_search_paused_draft_web_bulk.csv`
- Expected preview rows: `88 / 88 / 0` (1 + 10 + 30 + 37 + 10).
- Currency: `USD`. Budget: `1.00` USD daily. Max CPC: `0.10` USD.
- RPC target: same shape as PL but `campaign_name = "DLM_CZ_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"`, `budget_micros = "1000000"`.
- Per-country preflight: none specific.
- Do-not-click list (CZ): same as PL with CZ in the campaign-name slot.

### 3. RO

- Split CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/RO_intl_search_paused_draft_web_bulk.csv`
- Expected preview rows: `88 / 88 / 0` (1 + 10 + 30 + 37 + 10).
- Currency: `USD`. Budget: `1.00` USD daily. Max CPC: `0.10` USD.
- RPC target: `campaign_name = "DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"`, `budget_micros = "1000000"`.
- Per-country preflight: RO Final URLs use the localized `/ro/` path prefix (verified: `awk -F, '$1=="Keyword" {print $49; exit}' RO_..csv` returned `https://www.dresslikemommy.com/ro/products/...?country=RO`). If preview rewrites or strips the `/ro/` prefix, stop and update tracker.
- Do-not-click list (RO): same as PL with RO in the campaign-name slot.

### 4. PT

- Split CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/PT_intl_search_paused_draft_web_bulk.csv`
- Expected preview rows: `88 / 88 / 0` (1 + 10 + 30 + 37 + 10).
- Currency: `USD`. Budget: `1.00` USD daily. Max CPC: `0.10` USD.
- RPC target: `campaign_name = "DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"`, `budget_micros = "1000000"`.
- Per-country preflight: PT Final URLs use the localized `/pt/` path prefix (verified: first keyword Final URL = `https://www.dresslikemommy.com/pt/products/...?country=PT`). If preview rewrites the prefix, stop.
- Do-not-click list (PT): same as PL with PT in the campaign-name slot.

### 5. GR

- Split CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/GR_intl_search_paused_draft_web_bulk.csv`
- Expected preview rows: `88 / 88 / 0` (1 + 10 + 30 + 37 + 10).
- Currency: `USD`. Budget: `1.00` USD daily. Max CPC: `0.10` USD.
- RPC target: `campaign_name = "DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"`, `budget_micros = "1000000"`.
- Per-country preflight: none specific. Last clean unattempted before the three throttle/stale-preview risk countries.
- Do-not-click list (GR): same as PL with GR in the campaign-name slot.

### 6. IT (parked: stale `0/0/0` in-progress preview)

- Split CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/IT_intl_search_paused_draft_web_bulk.csv`
- Expected preview rows: `88 / 88 / 0` (1 + 10 + 30 + 37 + 10).
- Currency: `USD`. Budget: `1.00` USD daily. Max CPC: `0.12` USD.
- RPC target: `campaign_name = "DLM_IT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"`, `budget_micros = "1000000"`.
- Per-country preflight (IT) - mandatory order:
  1. Open Tools -> Bulk operations -> Upload spreadsheet history. Confirm whether the prior `IT_intl_search_paused_draft_web_bulk.csv` preview is still in `进行中 / In progress` (per `IT_preview_resume_check_body.txt`: "Your preview is in progress. You can stop the preview or apply the file at any time").
  2. If still in-progress, click `Stop preview` (do NOT click `Apply`) and wait for it to flip to `Cancelled` / `Stopped`. Save a screenshot to `raw/preview/IT_preview_stopped.png`.
  3. Only after the prior preview is cancelled (or vanishes from the visible 30-day batch history), upload the file fresh.
  4. Hard rule: if any IT preview row count reads `0/0/0` or `... / in progress`, do not click Apply. Wait or stop the preview.
- Do-not-click list (IT):
  - All of the PL list, PLUS:
  - Do not click Apply on the previous in-progress preview (any preview row showing `0/0/0` or non-final state).
  - Do not delete the in-progress preview record (cancel/stop only).

### 7. FR (parked: stale completed-with-errors preview from prior session)

- Split CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/FR_intl_search_paused_draft_web_bulk.csv`
- Expected preview rows: `88 / 88 / 0` (1 + 10 + 30 + 37 + 10).
- Currency: `USD`. Budget: `1.00` USD daily. Max CPC: `0.12` USD.
- RPC target: `campaign_name = "DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"`, `budget_micros = "1000000"`.
- Per-country preflight (FR) - mandatory order:
  1. Inspect Bulk operations history: a prior preview record `FR_intl_search_paused_draft_web_bulk.csv` exists. Prior packet describes it as stale completed-with-errors; do not reuse it.
  2. Re-upload the held FR CSV to generate a fresh preview record. Treat any reading of the older record as advisory only.
  3. Confirm the fresh preview reads `88 / 88 / 0` (the tail of `FR_preview_body.txt` shows `更改 88 / 成功 88 / 错误数 0` from the prior run; the new run must also hit this exact triple) before clicking Apply.
  4. If the fresh preview reads anything other than `88 / 88 / 0`, stop and update PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE.
- Do-not-click list (FR):
  - All of the PL list, PLUS:
  - Do not click Apply on the prior stale FR preview record. Apply only on a freshly-generated `88/88/0` preview.

### 8. BE (last; parked from upload throttle)

- Split CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/BE_intl_search_paused_draft_web_bulk.csv`
- Expected preview rows: `88 / 88 / 0` (1 + 10 + 30 + 37 + 10).
- Currency: `USD`. Budget: `1.00` USD daily. Max CPC: `0.12` USD.
- RPC target: `campaign_name = "DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507"`, `budget_micros = "1000000"`.
- Per-country preflight (BE) - mandatory order:
  1. Wait at least 60 minutes from the last upload (the prior BE attempt produced the throttle string from `BE_upload_rate_limit_body.txt`: "You have too many simultaneous uploads, or you have uploaded too many spreadsheets recently. Please wait and try again later.").
  2. Confirm BE is the last apply of the day; do not chain another country after BE.
  3. Upload BE fresh (no resume of the throttled background record). The throttle returned a "running in background" pseudo-state; treat that record as terminated.
  4. If the throttle string returns, abort the day, screenshot the error, and update PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE with the new timestamp. Resume next session no sooner than 24 hours later.
- Do-not-click list (BE):
  - All of the PL list, PLUS:
  - Do not retry on throttle. Wait, do not hammer.
  - Do not run another country apply within the same upload window after BE.

---

## Common preflight (do BEFORE every per-country apply)

Run, in order, for the country whose turn it is:

1. Confirm the resume order remaining is correct (no out-of-order country). The fixed order is `PL -> CZ -> RO -> PT -> GR -> IT -> FR -> BE`.
2. Confirm logged into the correct Google Ads account: customer_id `220823493`. Reject any prompt asking to switch account, log in again, complete 2FA, complete CAPTCHA, complete identity verification, or accept billing changes - stop and update the tracker instead.
3. Confirm Bulk operations -> Upload spreadsheet history shows no duplicate or in-progress record for the target country. If one exists for IT or FR, follow that country's per-country preflight before uploading.
4. Re-parse the held CSV with the source-of-truth block above and confirm:
   - `data rows = 88` and row-type breakdown is `1 / 10 / 30 / 37 / 10`.
   - Campaign `Location` column = the target country name.
   - Campaign `Language` column = `en`.
   - Campaign `Budget` column = `1.00`.
   - Ad-group `Default max. CPC` column = `0.10` (PL/CZ/RO/PT/GR) or `0.12` (IT/FR/BE).
5. Re-confirm SHA-256 of the CSV matches the value in the resume-order report (lane A 2026-05-10-paid-growth-orchestrator-safe-resume). If a hash drift is detected, stop.
6. Upload the file via Tools -> Bulk operations -> Upload spreadsheet -> Upload file. Capture screenshot to `raw/preview/<C>_file_selected_before_preview.png`.
7. Click Preview. Capture rendered DOM body to `raw/preview/<C>_preview_body.txt` and screenshot to `raw/preview/<C>_preview_result.png`.
8. The only acceptable preview result before clicking Apply: `Changes 88 / Success 88 / Errors 0` (or zh-CN equivalent `更改 88 / 成功 88 / 错误数 0`). Anything else (errors > 0, in-progress, 0/0/0, throttle warning) is an immediate stop.

---

## Common postflight (do AFTER every per-country apply click)

Mirror the existing `<C>_campaign_rpc/` structure used by AU/SE/CH/NL/DE/DK/CA/GB/ES.

1. Capture the apply success body and screenshot:
   - `raw/preview/<C>_apply_body.txt` (DOM text including the Chinese strings `成功完成 / 88 处更改成功`)
   - `raw/preview/<C>_apply_result.png`
2. Download the per-country results CSV from the Bulk operations row and place at:
   - `raw/preview/downloads/<C>/<C>_intl_search_paused_draft_web_bulk_RESULTS.csv`
   - Confirm the file has 89 lines (1 header + 88 data rows) and every data row's Results column ends in `# OK`. Generate a `.validation.json` of the same shape as `FR/FR_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json` (fields: `bad_hits`, `country`, `file`, `phase = "preview"`, `result = "PASS"`, `results = {"# OK": 88}`, `row_types = {Campaign:1, "Ad group":10, Keyword:30, "Negative keyword":37, Ad:10}`, `rows: 88`, `statuses` all Paused).
3. Issue the campaign RPC readback (same flow as AU). Save to `raw/after-readbacks/<C>_campaign_rpc/`:
   - `initial_request.json`
   - `initial_response.json`
   - `initial_summary.json`
4. Required RPC fields to capture in `initial_summary.json` (must match the per-country RPC target listed above):
   - `customer_id` = `"220823493"`
   - `campaign_id` = the new ID returned by the import (record it; do not reuse from another country)
   - `campaign_name` = the country-specific `DLM_<CC>_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
   - `campaign_status_code` = `5`, `campaign_status_interpreted` = `"PAUSED"`
   - `advertising_channel_type_code` = `1`, `advertising_channel_type_interpreted` = `"SEARCH"`
   - `budget_micros` = `"1000000"`, `budget_usd` = `1.0`
   - `currency` = `"USD"`
   - `target_google_search` = `true`
   - `target_search_network` = `null` or `false` (search partners OFF)
   - `target_content_network` = `false` (Display Network OFF)
   - `target_youtube_video` = `false` (YouTube OFF)
   - `positive_geo_target_type_interpreted` = `"LOCATION_OF_PRESENCE"`
   - `negative_geo_target_type_interpreted` = `"LOCATION_OF_PRESENCE"`
   - `geo_target_type_setting_raw` = `{"16": 18, "17": 18}`
   - `languages` = `["英语"]` (the MCC's zh-CN rendering of English)
5. If the Locations panel readback reads `Presence and interest` (geo_target_type_setting_raw shows `DONT_CARE` / value other than `18`), run the same narrow presence-only repair used for GB. Save `presence_repair_request.json`, `presence_repair_response.json`, `post_presence_repair_summary.json`, and a `final_validated_summary.json` mirroring the AU shape. Do not skip readback.
6. Update `ops/PROBLEM_TRACKER.md` (`PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE`) row for that country with the new `campaign_id`, the apply timestamp, and the path to `final_validated_summary.json` (or `initial_summary.json` if no presence repair was needed).

Stop criteria (any of these triggers a halt before the next country):
- Preview not equal to `88 / 88 / 0`.
- Apply result not equal to `88 changes succeeded` / `0 errors`.
- RPC readback shows `currency != USD`, `budget_usd != 1.0`, `campaign_status != PAUSED`, `target_content_network != false`, `target_youtube_video != false`, or any geo type other than `LOCATION_OF_PRESENCE` (after a single presence-only repair attempt).
- Any forbidden-surface row in preview/results: PMax, Performance Max, Standard Shopping, Shopping, conversion goal, product scope, feed label, product group, Merchant feed, or any of the 11 protected campaign IDs.
- Any 2FA / CAPTCHA / billing / account-switch / identity-verification modal.
- Upload throttle string returned ("too many simultaneous uploads").

---

## Rollback if mis-applied

A "mis-applied" campaign is any newly created campaign for one of the 8 unresolved countries that, on RPC readback, shows ANY of:
- `campaign_status_interpreted != "PAUSED"` (i.e. status is `ENABLED` (code 2) or any other non-paused state), OR
- `budget_usd != 1.0`, OR
- `currency != "USD"`, OR
- `target_content_network = true` OR `target_youtube_video = true` OR `target_search_network = true` (search partners ON), OR
- positive or negative geo type != `LOCATION_OF_PRESENCE` after one repair attempt, OR
- `campaign_name` does not match `DLM_<CC>_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`.

Identification steps:
1. Pull `customer/220823493/campaigns` via the same RPC used for the after-readback. Filter `campaign_name LIKE 'DLM_<CC>_%'`.
2. If `campaign_status_code` is `2` (ENABLED) for any of PL/CZ/RO/PT/GR/IT/FR/BE - that is the mis-applied campaign.

Rollback action (Pause-only, no delete):
1. In the Ads UI, navigate to the offending campaign by `campaign_id` from the RPC readback.
2. Click the status toggle to `Paused`. Do NOT click Remove / Delete / Archive.
3. Re-issue the campaign RPC and confirm `campaign_status_code = 5` / `campaign_status_interpreted = "PAUSED"`.

Required screenshot evidence (save to `raw/after-readbacks/<C>_campaign_rpc/rollback/`):
- `before_pause.png` - the campaign row in the campaigns table showing `Enabled`.
- `after_pause.png` - same row showing `Paused`.
- `rpc_after_pause_summary.json` - full RPC summary showing `campaign_status_code: 5`.

Problem-tracker update note (append to `PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE`):
- Country code, campaign_id, time of mis-apply, time of pause action, the field that was wrong (`status` / `budget` / `network` / `geo` / `currency` / `name`), absolute path to the rollback evidence folder, and a one-line root cause if known. Do not close the entry; flag for orchestrator review before resuming the queue.

Hard rule: never click Remove/Delete on a mis-applied campaign. Pause-only preserves the campaign_id for forensic readback and matches the test-build approval scope.

---

## Files touched by this lane

Read-only inputs (parsed only, no edits):
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/{PL,CZ,RO,PT,GR,IT,FR,BE}_intl_search_paused_draft_web_bulk.csv`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/raw/after-readbacks/{AU,SE,CH}_campaign_rpc/{initial_summary,final_validated_summary}.json`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/raw/preview/{IT_preview_resume_check,IT_preview_timeout,FR_preview,SE_preview,BE_upload_rate_limit}_body.txt`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/raw/preview/downloads/FR/FR_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/ads-resume-order/ADS_RESUME_ORDER_REPORT.md`

Written outputs (this report only):
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/ads-apply-playbook/ADS_APPLY_PLAYBOOK_REPORT.md`
