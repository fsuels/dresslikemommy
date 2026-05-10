# Google Ads Non-US Search Paused Test Build - Approved Partial

Status: `PARTIAL_9_APPLIED_REMAINING_BLOCKED_BY_FR_STALE_PREVIEW_BE_THROTTLE_IT_STILL_IN_PROGRESS_PREVIEW_NO_LIVE_SPEND`

Created: 2026-05-10 00:33 EDT

## Scope

Owner gave the exact canonical paused non-US Google Search TEST BUILD approval in the current chat. Approved scope was only paused Search campaigns for `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`, with no live spend, no US campaign `23827590655` edits, no PMax, no Standard Shopping changes, no Merchant/Shopify/Pinterest/theme writes, no product/feed/conversion changes, no bid/budget/status increases, and preview/readback before and after.

## What Happened

- Local artifact preflight passed for the held `1496`-row CSV and split manifest:
  - `17` target countries.
  - `17` Campaign rows, `170` Ad group rows, `510` positive Keyword rows, `629` Negative keyword rows, and `170` Ad rows.
  - All rows `Action=Add`.
  - All campaign/ad group/keyword/ad statuses are `Paused`.
  - Positive keywords are exact/phrase only.
  - Max CPC is `$0.15`.
  - `680` final URL rows, `40` country-qualified URLs per country.
  - `0` forbidden hits for US campaign `23827590655`, PMax, Standard Shopping, product/feed/conversion surfaces, Merchant, Shopify, Pinterest, bad beach handle/product, Vacation Family, Christmas, or enablement.
- The DevTools-controlled fresh Chrome tab was credential-gated at Google sign-in.
- Existing logged-in Chrome remote-debugging port `9222` had the correct Ads account context: `dresslikemommy.com - Google Ads`.
- Parent used the Google Ads web bulk upload path for the `GB` split file as a canary.
- `GB_intl_search_paused_draft_web_bulk.csv` preview completed cleanly:
  - UI preview: `88` changes, `88` successes, `0` errors.
  - Downloaded preview result: `88` rows, all `# OK`.
- Parent applied only the `GB` canary.
- `GB` apply completed cleanly:
  - UI apply row: `成功完成` / `88 处更改成功`.
  - Downloaded apply result: `88` rows, all `# OK`.
  - Result file rows remained paused: `1` Campaign, `10` Ad groups, `30` positive Keywords, `37` Negative keywords, `10` Ads; Campaign/Ad group/Keyword/Ad status fields all `Paused`.

## Initial Canary Live Account Writes Made

This section documents only the first `GB` canary stage. The cumulative current state is superseded by the continuation and recheck addenda below.

Only this paused Google Search campaign build was applied:

- `DLM_GB_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`

At this first stage, no other split files were selected, previewed, or applied after `GB`.

No live spend was enabled. No campaign/ad group/ad/keyword enablement was applied. No US campaign `23827590655`, PMax, Standard Shopping, Merchant, Shopify product data, Pinterest, theme, product-scope, feed-label, product-group, conversion-goal, or existing budget/bid/status changes were made by this session.

## Remaining Blocker

After the `GB` canary, the Google Ads bulk upload drawer refreshed into a newer file-picker component:

- Source selection changed from the earlier exposed `input[type=file]` path into a `file-picker` / `local-file-picker` component.
- The component did not expose a safe CDP `input[type=file]` node for `DOM.setFileInputFiles`.
- CDP `Page.setInterceptFileChooserDialog` plus synthetic click, pointer, mouse, Enter, and Space attempts did not emit a `Page.fileChooserOpened` event.
- The helper stopped before selecting any `CA` file; therefore no `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, or `GR` preview/apply action occurred.

Fallback attempt:

- Google Ads Editor was found installed at `/Applications/Google Ads Editor.app`.
- It opened and the menu/account context showed `dresslikemommy.com (399-097-6848)` earlier in the session, but later UI scripting could not access an Editor window (`windows=0`) and no Editor import/post was performed.
- Because Editor posting would be a live Ads write, the session stopped rather than attempt a blind GUI import.

## Evidence

- Local preflight: `working/local_preflight_validation.json`
- GB preview screenshot: `raw/preview/GB_preview_result.png`
- GB preview result CSV: `raw/preview/downloads/GB_intl_search_paused_draft_web_bulk_RESULTS.csv`
- GB apply screenshot: `raw/after-readbacks/GB_apply_result.png`
- GB apply result CSV: `raw/after-readbacks/downloads/GB_intl_search_paused_draft_web_bulk_RESULTS.csv`
- CA file-picker blocker screenshot: `raw/preview/CA_source_dropdown_problem.png`
- Automation/helper state: `working/google_ads_split_bulk_apply_state.json`
- Helper script: `working/google_ads_split_bulk_apply.py`

## Historical Required Next Action - Superseded

This first-stage next action was superseded by the 2026-05-10 continuation and ES resume addenda. Current next action is in the final section below.

1. First read back the newly created `GB` campaign directly in Google Ads:
   - Campaign/ad groups/ads/keywords paused.
   - Google Search only, no Search Partners/Display.
   - Manual CPC and CPC at or below `$0.20`.
   - Final URLs retain `country=GB`.
   - Presence-only location targeting is verified or safely corrected within the already approved paused-build scope.
2. Resume the remaining `16` split files only with a working file-upload path:
   - `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, `GR`.
   - Preview each split file first, download/validate result, then apply only if `88/88 # OK`, all paused, add-only, and no forbidden surfaces.
3. If web bulk upload remains blocked, use Google Ads Editor only after the Editor window/import preview is visibly accessible and after `Get recent changes`/readback ensures the already-created `GB` campaign is not duplicated.

Live-spend-ready non-US markets remain `0`. Any enablement/spend remains separately approval-gated.

## 2026-05-10 Continuation Result

After the partial `GB` build, the parent resumed from the canonical continuation prompt and did not request approval again.

Direct readback and correction:

- `GB` campaign readback found campaign ID `23838895360`, paused Search, budget `US$2/day`, content/YouTube off, and entities paused.
- RPC readback initially found `positiveGeoTargetType=DONT_CARE`; this was outside the approved presence-only requirement.
- A first `UPSERT` mutate attempt failed with `OperatorError.OPERATOR_NOT_SUPPORTED` and made no change.
- A narrow `MERGE_FIELD` repair then set `geo_target_type_setting` to `{positive: LOCATION_OF_PRESENCE, negative: LOCATION_OF_PRESENCE}`. Post-readback passed and the campaign remained paused.

Additional paused split files applied after preview/download validation:

| Country | Campaign ID | Campaign | Budget | Result |
| --- | ---: | --- | ---: | --- |
| `CA` | `23834423669` | `DLM_CA_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `US$2/day` | Preview `88/88 # OK`; apply `88/88 # OK`; final readback paused Search, presence-only |
| `AU` | `23834424182` | `DLM_AU_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `US$2/day` | Preview `88/88 # OK`; apply `88/88 # OK`; final readback paused Search, presence-only |
| `CH` | `23834425358` | `DLM_CH_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `US$1/day` | Preview `88/88 # OK`; apply `88/88 # OK`; final readback paused Search, presence-only |
| `DK` | `23838969244` | `DLM_DK_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `US$1/day` | Preview `88/88 # OK`; apply `88/88 # OK`; final readback paused Search, presence-only |
| `DE` | `23834427575` | `DLM_DE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `US$1/day` | Preview `88/88 # OK`; apply `88/88 # OK`; final readback paused Search, presence-only |
| `NL` | `23829110118` | `DLM_NL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `US$1/day` | Preview `88/88 # OK`; apply `88/88 # OK`; final readback paused Search, presence-only |
| `SE` | `23838970036` | `DLM_SE_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` | `US$1/day` | Preview `88/88 # OK`; apply `88/88 # OK`; final readback paused Search, presence-only |

Including `GB`, `8` paused non-US Search campaigns now exist from the approved build. All final readbacks show:

- Campaign status `Paused`.
- Search campaign type.
- `target_google_search=true`.
- `target_content_network=false`.
- `target_youtube_video=false`.
- Presence-only positive and negative geo targeting.
- Budgets equal to the approved split files.

Blocked/parked lanes:

- `FR`: the first FR preview download validated `88/88 # OK`, but the helper falsely treated older successful history rows as an apply success. A later stale/in-progress FR apply attempt produced a Google Ads row `completed with errors` / `no changes`; final readback confirms no `FR` campaign exists. Fresh FR retry then stuck at preview `0` changes in progress. Parked.
- `BE`: pre-import readback was absent; file selection began but preview was blocked by Google Ads upload throttling: `You have too many simultaneous uploads, or you have uploaded too many spreadsheets recently. Please wait and try again later.` No BE preview/apply occurred.
- `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`: not selected, previewed, or applied in this continuation. Final absent readbacks passed for all.

No live spend was enabled. No campaign/ad group/ad/keyword was enabled. No US campaign `23827590655`, PMax, Standard Shopping, Merchant, Shopify product data, Pinterest, theme, product scope, feed label, product group, conversion goal, product/feed/conversion surface, existing budget/bid/status-enable change, or live-spend change was made.

Additional evidence:

- Final summary: `working/final_campaign_readback_summary_2026-05-10.json`
- Playwright upload helper: `working/google_ads_split_bulk_apply_playwright.js`
- Campaign RPC readback helper: `working/google_ads_campaign_rpc_readback.py`
- GB presence repair: `raw/after-readbacks/gb_presence_rpc_repair/`
- Country readbacks: `raw/after-readbacks/{GB,CA,AU,CH,DK,DE,NL,SE}_campaign_rpc/final_validated_summary.json`
- Country preview/apply result CSVs: `raw/preview/downloads/{CA,AU,CH,DK,DE,NL,SE}/` and `raw/after-readbacks/downloads/{CA,AU,CH,DK,DE,NL,SE}/`
- FR blocked apply/no-change evidence: `raw/after-readbacks/FR_apply_body.txt`
- BE upload throttle evidence: `raw/preview/BE_upload_rate_limit_body.txt` and `raw/preview/BE_upload_rate_limit.png`

## Historical Updated Required Next Action - Superseded By ES Resume

This 8-country next action was superseded after `ES` was applied and read back. Current unresolved countries are `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`.

1. Do not request the same non-US Search `TEST BUILD` approval again.
2. Do not re-upload or duplicate `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, or `ES`.
3. Resume only after Google Ads upload/preview tooling is clean, starting with unresolved countries only: `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`.
4. For `FR` and `IT`, get a fresh preview that completes with `88/88 # OK`; do not apply from a stale, failed, no-change, or `0`-change/in-progress preview.
5. For every remaining country, use one-country controls: absent readback, preview/download/validate, apply/download/validate, then campaign RPC readback for paused/Search/presence-only/approved budget.

## 2026-05-10 Resume Addendum - ES Applied, IT Parked

Parent resumed the same owner-approved paused non-US Search TEST BUILD from the unresolved-country handoff. The owner approval was not requested again and completed countries were not re-uploaded.

Fresh local/read-only controls before live action:

- Sidecar split-file validation passed for unresolved `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`: each split file had `88` rows, all `Action=Add`, all importable statuses paused, max CPC at or below `$0.20`, `40` country-qualified final URLs, manifest checksums intact, and `0` forbidden hits for US campaign `23827590655`, PMax, Standard Shopping, product/feed/conversion surfaces, bad beach handle/product `7227378892897`, Vacation Family, Christmas, or Xmas.
- Fresh campaign RPC absent readback passed for `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR` before the resume attempt.

`ES` result:

- `ES_intl_search_paused_draft_web_bulk.csv` preview completed with `88/88 # OK`; downloaded preview result validation passed.
- Apply was clicked only after the clean preview.
- Google Ads showed the ES upload as successfully completed with `88` successful changes.
- The helper initially failed to find the post-apply download button, so the parent stopped further uploads, read back the live campaign, then recovered the apply-result download manually.
- Recovered apply result validation passed with `88/88 # OK`, same row-type counts, and all campaign/ad group/keyword/ad statuses paused.
- Final campaign RPC readback passed: campaign `23829133584` / `DLM_ES_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`, paused Search, budget `US$1/day`, content/YouTube off, and positive/negative geo targeting both `LOCATION_OF_PRESENCE`.

`IT` result:

- `IT_intl_search_paused_draft_web_bulk.csv` was selected and preview was started, but it did not complete.
- The helper stopped at its 120-second preview guard. A parent follow-up readback after an additional 60 seconds still showed preview in progress with `0` changes, `0` success, and `0` errors.
- No IT apply was clicked. Fresh campaign RPC readback confirmed the IT campaign remained absent.

Current completed paused campaigns from the approved build:

| Country | Campaign ID | Budget | Final state |
| --- | ---: | ---: | --- |
| `GB` | `23838895360` | `US$2/day` | paused Search, presence-only |
| `CA` | `23834423669` | `US$2/day` | paused Search, presence-only |
| `AU` | `23834424182` | `US$2/day` | paused Search, presence-only |
| `CH` | `23834425358` | `US$1/day` | paused Search, presence-only |
| `DK` | `23838969244` | `US$1/day` | paused Search, presence-only |
| `DE` | `23834427575` | `US$1/day` | paused Search, presence-only |
| `NL` | `23829110118` | `US$1/day` | paused Search, presence-only |
| `SE` | `23838970036` | `US$1/day` | paused Search, presence-only |
| `ES` | `23829133584` | `US$1/day` | paused Search, presence-only |

Remaining absent/uncreated countries:

- `FR`: still absent; do not apply without a fresh completed `88/88 # OK` preview because the prior lane had stale/no-change history.
- `BE`: still absent; retry only after upload cooldown and stop if the simultaneous/recent-upload throttle repeats.
- `IT`: still absent; the current preview is in progress at `0` changes and must clear or be superseded by a fresh completed `88/88 # OK` preview before any apply.
- `PL`, `CZ`, `RO`, `PT`, and `GR`: still absent and not attempted in this resume.

No live spend was enabled. No campaign/ad group/ad/keyword was enabled. No US campaign `23827590655`, PMax, Standard Shopping, Merchant, Shopify product data, Pinterest, theme, product scope, feed label, product group, conversion goal, product/feed/conversion surface, existing campaign budget/bid/status-enable change, or live-spend change was made.

Additional evidence:

- ES preview validation: `raw/preview/downloads/ES/ES_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json`
- ES apply validation: `raw/after-readbacks/downloads/ES/ES_intl_search_paused_draft_web_bulk_RESULTS.csv.validation.json`
- ES campaign readback: `raw/after-readbacks/ES_campaign_rpc/final_validated_summary.json`
- IT in-progress evidence: `raw/preview/IT_preview_timeout_body.txt`, `raw/preview/IT_preview_timeout.png`, `raw/preview/IT_preview_timeout_after_60s_body.txt`, `raw/preview/IT_preview_timeout_after_60s.png`
- Updated final readback summary: `working/final_campaign_readback_summary_2026-05-10_resume_es.json`

## Updated Required Next Action After ES Resume

1. Do not request the same non-US Search TEST BUILD approval again.
2. Do not re-upload or duplicate `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, or `ES`.
3. Resume only unresolved countries after the Ads upload/preview lane is clean: `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`.
4. Apply no country from an in-progress, stale, `0`-change, or no-change preview. Require a fresh downloaded preview result with `88/88 # OK`, then an apply download with `88/88 # OK`, then campaign RPC readback.
5. If the IT preview remains in-progress or BE throttles again, stop Ads uploads and move independent local/read-only lanes forward.

## 2026-05-10 Recheck Addendum - IT Still In Progress, Remaining Countries Absent

Parent performed a bounded recheck instead of applying from the stale IT upload state.

Fresh recheck result:

- Browser/CDP readback of the Google Ads upload page still showed `IT_intl_search_paused_draft_web_bulk.csv` preview in progress.
- The IT preview was still at `0` changes / `0` success / `0` errors.
- No IT apply was clicked.
- Fresh campaign RPC absent readback confirmed all unresolved countries remain absent: `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`.

Sidecar findings:

- Local-only Ads gate review confirmed completed countries must not be re-uploaded: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, and `ES`.
- Safest order after the upload/preview lane is clean is clean unattempted files first (`PL`, `CZ`, `RO`, `PT`, `GR`), then `IT` only after the stale preview clears, then `FR` only with a fresh completed preview, then `BE` last because it hit upload throttling.
- Non-Ads lanes remain approval-gated but locally prepared: Merchant `US/es` age_group, Pinterest Event Quality/paused drafts, beach/Vacation Family SEO metadata, and native-language copy review.

Updated evidence:

- IT recheck body: `raw/preview/IT_preview_resume_check_body.txt`
- IT recheck screenshot: `raw/preview/IT_preview_resume_check.png`
- Remaining-country absent recheck: `raw/after-readbacks/remaining_absent_recheck_2026-05-10_0205/remaining_absent_recheck.txt`
- Current final summary: `working/final_campaign_readback_summary_2026-05-10_it_still_in_progress.json`

Updated required next action:

1. Do not request the same non-US Search TEST BUILD approval again.
2. Do not re-upload or duplicate `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, or `ES`.
3. Do not start more Ads uploads while the IT preview remains in-progress at `0` changes.
4. Once the Ads upload/preview lane is clean, resume only unresolved countries one at a time: `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`.
5. Require a fresh downloaded preview result with `88/88 # OK`, then an apply download with `88/88 # OK`, then campaign RPC readback for paused/Search/presence-only/approved budget.
6. Stop on any in-progress/stale/no-change preview, upload throttle, enabled row, budget/bid/status mismatch, US `23827590655`, PMax, Standard Shopping, Merchant, Shopify, Pinterest, theme, product/feed/conversion surface, or unclear readback.
