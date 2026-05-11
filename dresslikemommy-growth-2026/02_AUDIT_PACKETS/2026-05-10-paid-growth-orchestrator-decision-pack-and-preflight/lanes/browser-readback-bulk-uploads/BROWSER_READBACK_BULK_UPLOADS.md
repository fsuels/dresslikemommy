# Google Ads Bulk Uploads — Pending Actions Browser Readback (2026-05-10)

Owner-reported browser access became available mid-session via the logged-in `Test Chrome` profile (deviceId `b5330aa5-2634-4673-b353-e2d80c19225c`). This lane is a fresh read-only browser readback of the Google Ads `Pending actions` Bulk Uploads view to determine whether the prior parked previews (FR stale, IT in-progress at `0/0/0`, BE upload throttle) have changed since the prior 2026-05-10 02:05 EDT recheck.

## Account context

- Google Ads UI: `https://ads.google.com/aw/bulk/uploads/pending`
- Customer (CID): `399-097-6848` `dresslikemomm...`
- Logged-in Google account: `testqfinds@gmail.com`
- Session timezone shown: `(GMT-04:00) New York Time`
- Page filter: `Last 7 days` / `May 3 – 9, 2026` (default open). Pending list: `1 - 5 of 5`.
- Tabs: Test Chrome MCP tab `475198700`.

## Pending Actions table — exact readback

| # | User / Date & time | Status | Source | File source | File | Changes | Actions available | Duration (s) |
|---|---|---|---|---|---|---|---|---|
| 1 | `testqfinds@gmail.com` / `May 10, 2026 1:54:33 AM (GMT-04:00) New York Time` | `Preview finished successfully` | `File upload` | `Manual Local File` | `IT_intl_search_paused_dr...` | `88 valid changes` | `Apply` / `Discard` / `Download results` | `8` |
| 2 | `testqfinds@gmail.com` / `May 10, 2026 1:37:26 AM (GMT-04:00) New York Time` | `Preview finished with errors` | `File upload` | `Manual Local File` | `BE_intl_search_paused_dr...` | `Failed` `There are too many concurrent upload requests, please try again after two hours.` | `Apply` / `Discard` (no `Download results`) | `1` |
| 3 | `testqfinds@gmail.com` / `May 10, 2026 1:36:08 AM (GMT-04:00) New York Time` | `Preview finished successfully` | `File upload` | `Manual Local File` | `FR_intl_search_paused_dr...` | `88 valid changes` | `Apply` / `Discard` / `Download results` | `8` |
| 4 | `testqfinds@gmail.com` / `May 10, 2026 1:20:44 AM (GMT-04:00) New York Time` | `Preview finished successfully` | `File upload` | `Manual Local File` | `CA_intl_search_paused_dr...` | `88 valid changes` | `Apply` / `Discard` / `Download results` | `9` |
| 5 | `testqfinds@gmail.com` / `May 6, 2026 6:24:19 AM (GMT-04:00) New York Time` | `Preview finished with errors` | `File upload` | `Manual Local File` | `00_nonbrand_search_pau...` | `98 errors expected` | `Apply` / `Discard` / `Download results` | `7` |

## Material state changes vs prior 2026-05-10 02:05 EDT recheck

1. **IT preview is no longer stuck in-progress.** The IT row now reads `Preview finished successfully` / `88 valid changes`, exactly the validation target named in the canonical playbook (`88/88 # OK`). The earlier `0/0/0` in-progress state recorded in `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/working/final_campaign_readback_summary_2026-05-10_it_still_in_progress.json` has cleared.
2. **FR preview now has a fresh successful result.** FR previously produced `completed with errors` / `no changes` and no FR campaign was created. The current FR row shows `Preview finished successfully` / `88 valid changes`.
3. **BE preview row still shows the throttle error.** The original throttle was hit at `2026-05-10 1:37:26 AM EDT`. The two-hour wait window has elapsed by the time of this readback (`>2 hours later`), but the existing pending row is still in error state. A clean BE retry would require a fresh re-upload, not a re-Apply on this row.
4. **CA preview is a stale duplicate-risk row.** CA campaign `23834423669` already exists and was created in the partial 2026-05-10 build. Re-applying CA from this pending row would attempt to create a duplicate or fail with existing-entity errors. The safest action on the CA row is `Discard`, never `Apply`.
5. **The May 6 `00_nonbrand_search_pau...` row is unrelated to the current non-US Search build.** It pre-dates the 2026-05-10 TEST BUILD approval scope and is a separate US nonbrand artifact with `98 errors expected`.

## What was NOT done

- No `Apply` was clicked on any row.
- No `Discard` was clicked on any row.
- No `Download results` was clicked.
- No new file was uploaded.
- No campaign was enabled, paused, or had budget/bid/status/scope/feed-label/product-group/conversion-goal changed.
- No PMax, Standard Shopping, Merchant, Pinterest, Shopify, theme, or measurement edit was made.
- No `Discard` of the BE/throttle row, the stale CA row, or the unrelated May 6 row was performed — the owner has not given action-time approval to discard either.

## Approval gate (reproduced verbatim from the canonical operating prompt and the prior packet)

The original 2026-05-10 owner approval phrase covered creating paused non-US Search shells. It did not name `Apply` of new previews after the IT/FR previews cleared. The canonical guardrails in this session's operating prompt explicitly require fresh action-time approval for any apply/enable. Recommended action-time phrase the owner can paste:

```
APPROVE APPLY OF THE FRESH IT AND FR PAUSED SEARCH PREVIEWS NOW: APPLY THE 2026-05-10 IT_intl_search_paused_draft AND FR_intl_search_paused_draft 88-VALID-CHANGE PREVIEWS UNDER THE EXISTING 2026-05-10 PAUSED NON-US SEARCH TEST BUILD APPROVAL; DISCARD THE STALE CA_intl_search_paused_draft PREVIEW BECAUSE CA CAMPAIGN 23834423669 ALREADY EXISTS; DO NOT APPLY OR DISCARD THE BE THROTTLED PREVIEW (USE A FRESH BE UPLOAD INSTEAD); DO NOT TOUCH THE MAY 6 00_nonbrand_search_pau ROW; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO ENABLEMENT; NO US CAMPAIGN 23827590655, PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY, PINTEREST, OR THEME CHANGES; READ BACK BEFORE AND AFTER EACH APPLY.
```

If the owner wants to keep the frozen safest order from the prior packet (`PL` first, then `CZ → RO → PT → GR → IT → FR → BE`), the alternate option is to:

1. `Discard` the IT, FR, and CA pending previews (clears the queue safely without creating campaigns).
2. Continue with PL fresh upload using `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/pl-preflight-bundle/PL_PREFLIGHT_BUNDLE.md`.

That alternate also requires fresh action-time approval (e.g.):

```
APPROVE DISCARD OF THE STALE IT, FR, AND CA PAUSED SEARCH PREVIEWS AND CONTINUE WITH PL FRESH UPLOAD ONLY: DISCARD ONLY THE IT, FR, AND CA PENDING ROWS DATED 2026-05-10 1:54, 1:36, AND 1:20 AM EDT; DO NOT APPLY ANY OF THEM; DO NOT TOUCH THE BE THROTTLED ROW OR THE MAY 6 00_nonbrand_search_pau ROW; DO NOT START NEW UPLOADS UNTIL EXPLICITLY APPROVED PER PL PREFLIGHT BUNDLE.
```

## Evidence

- Browser screenshots taken in this session (host-side, attached inline in chat):
  - Pending Actions overview (initial Uploads page).
  - Pending Actions full table (5 of 5 rows visible).
  - Zoomed crop of rows 1–5 with full row text including `Failed: There are too many concurrent upload requests, please try again after two hours.`
- Prior recheck for comparison: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/raw/preview/IT_preview_resume_check_body.txt`, `working/final_campaign_readback_summary_2026-05-10_it_still_in_progress.json`.
- Per-country playbook (drives the next safe action either way): `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/ads-apply-playbook/ADS_APPLY_PLAYBOOK_REPORT.md`.
- PL preflight bundle (alternate path): `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/pl-preflight-bundle/PL_PREFLIGHT_BUNDLE.md`.

## Status

`PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE` is updated:

- IT preview parked-in-progress sub-blocker is **CLEARED** at the upload-page level. Sub-blocker description "IT preview still in progress at 0/0/0" no longer matches reality.
- FR stale preview sub-blocker is **CLEARED** at the upload-page level. A fresh successful 88-valid-change preview now exists.
- BE upload-throttle sub-blocker has elapsed at the wait-window level (`>2 hours since 1:37:26 AM EDT`), but the existing BE pending row is still in error state. A clean BE retry would require a fresh re-upload from `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/BE_intl_search_paused_draft_web_bulk.csv` (sha256 verified clean by `lanes/stale-blocker-checksum-sweep` in this same packet).
- The owner now has a fresh action-time decision: **Apply IT+FR (and Discard stale CA)**, or **Discard IT+FR+CA and continue with PL first** per the frozen safest order.
- Either path requires fresh exact action-time approval; this session does not act without it.
