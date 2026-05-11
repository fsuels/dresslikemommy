# PL Preflight Bundle — Paused Search Apply (PL only)

Lane: `pl-preflight-bundle` (decision-pack-and-preflight packet, 2026-05-10)
Scope: Paper preflight only. NO live writes, NO clicks, NO uploads in this session.
Operator action: This bundle is the single paste-ready packet for the next browser-enabled session to apply ONLY the PL paused Search campaign. PL is the next country in the frozen safest resume order: PL -> CZ -> RO -> PT -> GR -> IT -> FR -> BE.

---

## 1. Header

- Country: **PL (Poland)**
- Campaign name (held CSV): `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
- Source CSV path:
  `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/PL_intl_search_paused_draft_web_bulk.csv`
- Source CSV SHA256 (from `SHA256SUMS.txt` in the same lane folder):
  `3ce7a8df5fc7a5e8c248d2441c57154d8e9e1aee575a6dd826a76906bb00bd76`
- Manifest path:
  `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/manifest.json`
- Header field count (manifest): 95
- Expected row totals (data rows, excluding header):
  - Campaign: **1**
  - Ad group: **10**
  - Keyword: **30**
  - Negative keyword: **37**
  - Ad (Responsive search ad): **10**
  - **Total: 88**
- Budget (read directly from PL CSV row 2, `Budget` column): **1.00 USD daily** (Budget type: Daily, Delivery: Standard)
- Bid strategy: Manual CPC, default Max CPC `0.10` per ad group (manifest `max_default_cpc` = 0.10 for PL)
- Language: en
- Location: Poland
- Networks: Google search (no search partners, no display)
- Campaign status, all ad groups, all keywords, all negatives, all ads: `Paused`

---

## 2. Pre-upload absent-readback (zero existing PL entities)

In Google Ads UI before opening Bulk Uploads:

- Navigate: Campaigns view, scope = All campaigns (All time, include removed disabled).
- Search filter (campaign name contains): `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
- Expected result: **zero rows**.
- Secondary readback (Google Ads Search at top bar): paste the literal string `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507` and confirm zero matches under Campaigns / Ad groups / Ads / Keywords.
- STOP if any matching entity already exists. Do not upload — file an exception in the orchestrator before proceeding.

---

## 3. Upload steps (preview only — DO NOT click Apply yet)

1. Open Google Ads -> Tools -> Bulk Actions -> Uploads.
2. Click "New upload" -> "Upload a file".
3. Select file:
   `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/PL_intl_search_paused_draft_web_bulk.csv`
4. Re-verify SHA256 locally before upload (optional but recommended). Expected:
   `3ce7a8df5fc7a5e8c248d2441c57154d8e9e1aee575a6dd826a76906bb00bd76`
5. Choose "Preview" (not "Apply").
6. Wait for the preview to fully process. Do NOT start any other upload while this preview is in-progress.
7. Expected preview banner: **`88 / 88 # OK`** (88 OK, 0 errors, 0 warnings).

> **STOP rule:** If the preview is anything other than exactly **88 / 88 # OK**, do not click Apply. Cancel the preview, capture a screenshot, and halt the lane. Re-run the absent-readback in Section 2 before any retry.

---

## 4. Pre-apply gate (preview must show ALL of the following)

Confirm every item before clicking Apply:

- [ ] Preview shows `88` total changes, `88` OK.
- [ ] Errors: **0**.
- [ ] Warnings: **0** (in particular, zero "entity already exists" warnings).
- [ ] Ignored rows: **0**.
- [ ] Currency on the new campaign preview: **USD** (account currency).
- [ ] Campaign status: **Paused**.
- [ ] All 10 ad groups: **Paused**.
- [ ] All 30 keywords: **Paused**.
- [ ] All 10 RSAs: **Paused**.
- [ ] Negative keywords (37): added at Campaign level.
- [ ] Campaign type: **Search**, Networks: **Google search** only.
- [ ] No "default ad group" or "auto-created" surprise rows in the preview diff.

If any checkbox above fails, STOP. Do not Apply.

---

## 5. Apply step (only if Section 4 is fully green)

1. Click **Apply changes** in the preview view.
2. Wait for processing to complete. Expected result banner: **`88 / 88 # OK`** (`0` errors, `0` warnings, `0` ignored).
3. Click **Download results** -> save the result CSV.
4. Recommended evidence save path (DO NOT create this directory in the preflight session — create it during the apply session):
   `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/pl-preflight-bundle/apply_evidence/PL_apply_result_<UTC_TIMESTAMP>.csv`
5. After download, compute SHA256 of the result CSV and record it in the orchestrator log.

> **STOP rule:** If the apply result is anything other than `88 / 88 # OK`, do not start the post-apply readback or any subsequent country. Begin Section 8 (Rollback).

---

## 6. Post-apply RPC / Google Ads readback

In the Google Ads UI (or Google Ads Query Language via the official report builder — read-only), confirm each of the following on the newly created campaign:

- Campaign name: `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`
- Campaign ID lookup: present, single match, retain the numeric ID.
- Status: **Paused**
- Advertising channel type: **Search**
- Advertising channel sub-type: **Standard / (none)** (no Smart, no PMax, no Shopping)
- Networks:
  - Google search: **ON**
  - Search partners: **OFF**
  - Display network (content network): **OFF**
  - YouTube: **OFF (N/A for Search)**
- Locations: includes only **Poland** with **Presence** option = "People in or regularly in your targeted locations" (presence-only). Confirm by opening Campaign settings -> Locations -> Location options.
- Languages: **en** only.
- Budget: **$1.00 USD daily**, Standard delivery, Budget type Daily.
- Bid strategy: **Manual CPC** (no eCPC enhancement enabled unless explicitly intended).
- Ad group default Max CPC: **$0.10** on each of the 10 ad groups.
- Ad group count: **10**, names match CSV (Mommy & Me Dresses Exact/Phrase, Family Matching Exact/Phrase, Matching Pajamas Exact/Phrase, Matching Swimwear Exact/Phrase, Daddy & Me Exact/Phrase).
- Keyword count: **30** (3 per ad group), all Paused, match types per CSV (Exact / Phrase).
- Negative keyword count at campaign level: **37**, match types per CSV.
- Responsive search ads: **10**, all Paused, Final URLs all carry `?country=PL`.
- Ad strength / policy: capture status; do not enable.
- EU political ads declaration: blank/No (CSV: `No`).

If any readback drifts from the above, mark FAIL and proceed to Section 7.

---

## 7. Stop-criteria (halt rules)

Halt the lane immediately and notify the orchestrator if ANY of the following occur:

- Pre-upload absent-readback (Section 2) returns any matching campaign / ad group / keyword.
- Preview banner is anything other than `88 / 88 # OK`.
- Any error, warning, or ignored row in the preview.
- Currency is not USD; budget is not $1.00; any status is not Paused.
- Apply result is not exactly `88 / 88 # OK`.
- Post-apply readback (Section 6) shows any drift: wrong channel, search partners ON, display ON, location not Poland, presence not "People in or regularly in", non-paused entity, missing or extra ad groups / keywords / ads / negatives, default Max CPC not $0.10, budget not $1.00 USD.
- **Concurrency rule:** No further uploads (CZ, RO, PT, GR, IT, FR, BE, or any other lane) start while any preview or apply is still in-progress in Bulk Actions. One country at a time, end-to-end (preview -> apply -> post-apply readback -> evidence saved -> orchestrator confirms green) before the next country's preflight is opened.

---

## 8. Rollback (only if apply produced unexpected entities)

1. In Google Ads, open Campaigns and filter by name `DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`.
2. Confirm the campaign is **Paused** (it should be — this is the safety net).
3. If the campaign was created but readback drifted (e.g., extra entities, wrong settings):
   - Preferred: leave **Paused** and open a fresh Bulk Upload that REMOVES the campaign:
     - Build a one-row CSV: `Row Type=Campaign, Action=Remove, Campaign=DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507`.
     - Preview must show `1 / 1 # OK`. Apply.
   - Fallback: from the Campaigns UI, select the campaign and choose **Remove** (do not "Pause" only — it is already paused).
4. If apply created partial / orphaned entities (ad groups without parent campaign, etc.), use Bulk Actions to Remove them by name; verify zero rows remain on a fresh search.
5. Record rollback SHA + UI screenshots in `apply_evidence/`.
6. Do NOT retry PL until the orchestrator approves a re-attempt.

---

## 9. Forward chain

- Next country in safest resume order: **CZ (Czechia)**
  - Held CSV: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/CZ_intl_search_paused_draft_web_bulk.csv`
  - Manifest SHA256: `a2e20892564494d10aacf42792be1310df55c473054be456ab16cefa1fd05b55`
- CZ preflight should be authored at:
  `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/cz-preflight-bundle/CZ_PREFLIGHT_BUNDLE.md`
- Preconditions to author CZ preflight: PL apply is `88 / 88 # OK`, post-apply readback fully green, evidence saved, orchestrator marks PL DONE.
- Frozen full chain after CZ: RO -> PT -> GR -> IT -> FR -> BE.

---

## Appendix A — CSV evidence (sample rows verified during preflight)

- Row 2 (Campaign): `Campaign,Add,Paused,,DLM_PL_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260507,Search,Google search,1.00,Standard,Daily,Manual CPC,...,en,Poland,...`
- Rows 3-12: 10 Ad group rows, all `Paused`, default Max CPC `0.10`.
- Rows 13-42: 30 Keyword rows, all `Paused`, Exact / Phrase, Final URLs include `?country=PL`.
- Rows 43-79: 37 Negative keyword rows at Campaign level (Broad / Phrase / Exact mix).
- Rows 80-89: 10 Responsive search ad rows, all `Paused`, Final URLs include `?country=PL`.

## Appendix B — Constraints reaffirmed

- No live spend authorized by this bundle.
- No edits to any existing CSV / manifest / report.
- Only one new file created by the preflight session: this `.md`.
- No curl, no API calls, no theme / Shopify / Ads / Merchant / Pinterest writes.
