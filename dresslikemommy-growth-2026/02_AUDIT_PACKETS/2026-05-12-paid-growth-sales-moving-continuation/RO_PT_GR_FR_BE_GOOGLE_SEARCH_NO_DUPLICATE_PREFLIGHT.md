# RO/PT/GR/FR/BE Google Search No-Duplicate Preflight

Worker: `Worker A`
Date: `2026-05-12`
Mode: local-only / read-only evidence. No Google Ads, Merchant, Shopify Admin, Pinterest, checkout, billing, credential, upload, preview, import, apply, or external-system action was taken.

## Purpose

Prepare the next safe Google Ads expansion handoff for the remaining gated paused Search markets: `RO`, `PT`, `GR`, `FR`, and `BE`.

This file does not authorize platform action. It is a no-duplicate/preflight checklist so the next Google Ads operator can move quickly without re-uploading completed countries or stacking countries behind a stale upload.

## Source Files Validated

Source split CSV directory:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/`

| Market | Split CSV | Rows | Row Shape | Import Statuses | Max CPC | URL Rows | Checksum | Local Decision |
|---|---|---:|---|---|---:|---:|---|---|
| `RO` | `RO_intl_search_paused_draft_web_bulk.csv` | 88 | 1 campaign, 10 ad groups, 30 keywords, 37 negatives, 10 ads | all paused | `$0.10` | 40 country-qualified | match | ready only after fresh no-RO/no-preview readback |
| `PT` | `PT_intl_search_paused_draft_web_bulk.csv` | 88 | same | all paused | `$0.10` | 40 country-qualified | match | hold behind RO decision |
| `GR` | `GR_intl_search_paused_draft_web_bulk.csv` | 88 | same | all paused | `$0.10` | 40 country-qualified | match | hold behind RO/PT decision |
| `FR` | `FR_intl_search_paused_draft_web_bulk.csv` | 88 | same | all paused | `$0.12` | 40 country-qualified | match | parked until fresh non-stale preview path |
| `BE` | `BE_intl_search_paused_draft_web_bulk.csv` | 88 | same | all paused | `$0.12` | 40 country-qualified | match | last after throttle/cooldown and no-duplicate readback |

Fresh local validation also found:

- `0` nonblank campaign/ad group/keyword/ad IDs in the five source split CSVs.
- `0` completed-country campaign-name hits for `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, or `CZ`.
- `0` forbidden hits for protected or unrelated surfaces: `23827590655`, `23802638621`, `DLM_US_`, `PMax`, `Performance Max`, `Standard Shopping`, Merchant/feed/product-group/product-scope/conversion-goal terms, supplier domains, product `7227378892897`, stale beach handle, `Vacation Family`, `Christmas`, or `Xmas`.

## Current Gated State

Do not re-upload completed countries. Current completed/created non-US Search countries are `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, and `CZ`. `GB`, `CA`, and `AU` are now live/eligible exact micro-tests under separate exact approvals; that live status does not change the remaining build lane.

Local/readback evidence for the five target markets:

- `RO`: absent in latest local readback; prior preview became not visible after timeout. Next action must recheck no in-progress `RO` upload and no `RO` campaign before any new preview.
- `PT`: absent in latest local readback; not attempted because the one-country guard blocked stacking behind `RO`.
- `GR`: absent in latest local readback; not attempted because the one-country guard blocked stacking behind `RO`.
- `FR`: absent in campaign readback, but prior stale preview/apply recovery produced errors/no changes. Treat the old preview as unsafe for apply. Needs fresh non-stale `88/88 # OK` preview plus no-duplicate readback.
- `BE`: absent in campaign readback, but prior Google Ads upload path hit upload-throttle / too many simultaneous or recent uploads. Keep last until cooldown and no-duplicate readback.

## Required No-Duplicate Checklist Before Any Future Google Ads Action

Run these before touching upload/preview/apply:

1. Confirm no other agent has an active Google Ads international Search write claim in `ops/AGENT_COORDINATION.md`.
2. Confirm fresh exact owner approval for the named country and named action.
3. Confirm the campaign does not already exist with a fresh readback for the exact campaign name:
   - `DLM_RO_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
   - `DLM_PT_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
   - `DLM_GR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
   - `DLM_FR_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
   - `DLM_BE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
4. Confirm no bulk-upload preview/apply row is currently in progress for that country file.
5. Confirm the source file still matches the row shape above and still has no protected-surface or stale bad-handle hits.
6. Preview one country only.
7. Download the preview result and validate `88/88 # OK`; do not apply from a stale, partial, invisible, in-progress, or error preview.
8. Apply only the same single country after a clean preview.
9. Download the apply result and validate `88/88 # OK`.
10. Read back the resulting campaign as paused Search, presence-only, Search-only/content+YouTube off, daily budget unchanged from source file, CPC at or below `$0.20`, and no conversion-goal override.
11. If presence-only is not clean, only use the previously proven narrow presence-only repair path after exact approval/readback; do not bundle that repair with another country.
12. Update `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md`, and `ops/AGENT_WORKLOG.md` before moving to the next country.

## Exact Next Safe Google Ads Action

No platform action is safe from this Worker A lane. The next safe Ads action for a parent/operator with browser access is:

`RO` one-country preview-only retry, and only after fresh owner approval plus fresh readbacks proving no `RO` campaign exists and no `RO` upload/preview/apply is in progress.

Recommended approval wording:

`APPROVE RETRY RO PAUSED GOOGLE SEARCH TEST BUILD ONLY: FIRST CONFIRM NO RO CAMPAIGN EXISTS AND NO RO BULK-UPLOAD PREVIEW/APPLY IS IN PROGRESS; THEN UPLOAD ONLY RO_intl_search_paused_draft_web_bulk.csv, PREVIEW, DOWNLOAD, AND VALIDATE 88/88 # OK; APPLY ONLY IF CLEAN; READ BACK THE RO CAMPAIGN AS PAUSED SEARCH, PRESENCE-ONLY, CONTENT/YOUTUBE OFF, CPC AT OR BELOW $0.20; DO NOT TOUCH PT, GR, FR, BE, COMPLETED COUNTRIES, US CAMPAIGN 23827590655, STANDARD SHOPPING, PMAX, MERCHANT, SHOPIFY PRODUCT DATA, PINTEREST, THEME, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT; NO LIVE SPEND.`

If the owner chooses to park `RO`, the next safest build order is `PT` then `GR`, one at a time, with the same preview/download/validate/apply/readback loop. `FR` should come only after a fresh non-stale preview path is proven. `BE` should remain last after upload-throttle cooldown.

## Local Validation Commands

Commands run in this worker lane:

- `sed -n '1,220p' ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `sed -n '1,220p' ops/AGENT_COORDINATION.md`
- `tail -n 220 ops/AGENT_WORKLOG.md`
- `sed -n '1,220p' ops/GROWTH_NORTH_STAR.md`
- `sed -n '1,220p' ops/PROBLEM_TRACKER.md`
- `sed -n '1,200p' ops/BROWSER_SUBAGENT_COORDINATION.md`
- `sed -n '1,220p' ops/GOOGLE_ADS_CONTINUITY.md`
- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS -type f ...`
- `python3 -m json.tool .../google_ads_split_bulk_apply_state.json`
- `python3 -m json.tool .../local_preflight_validation.json`
- `python3 -m json.tool .../raw/campaign-absent-readbacks/*_campaign_rpc/initial_summary.json`
- `python3 -m json.tool .../raw/preview/downloads/FR/FR_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json`
- `python3 - <<'PY' ...` using `csv`, `hashlib`, `json`, `pathlib`, and local regex checks for the five target split CSVs.

Fresh validation result:

`PASS: RO/PT/GR/FR/BE local split CSV guardrails validated`

## Guardrails

This packet is local-only. It does not change approval status and does not reduce the hard guardrails around live spend, campaign/status/budget/bid edits, Merchant uploads/source edits, Pinterest writes, Shopify product-data writes, product scope/feed label/product group changes, conversion-goal changes, PMax, Standard Shopping, payment/order/refund/cancel, billing/account/credential changes, or destructive actions.
