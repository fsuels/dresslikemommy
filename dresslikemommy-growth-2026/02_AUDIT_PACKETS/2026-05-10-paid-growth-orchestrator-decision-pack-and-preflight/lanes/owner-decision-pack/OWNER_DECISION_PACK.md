# Owner Decision Pack - Paid Growth Sprint

**Lane:** A / Owner-Decision-Pack
**AGENT_CONTINUITY_ANCHOR:** 2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight
**Date (Pacific):** 2026-05-10
**Author:** Owner-Decision-Pack subagent (local file write only; no live writes, no browser actions, no Shopify/Ads/Merchant/Pinterest/GA4/theme writes)
**Owner email:** suelsferro@hotmail.com

## 0. Purpose

This pack consolidates EVERY currently parked paid-growth gate so the owner can approve or defer each one in a single pass. Every approval phrase is reproduced verbatim from existing repo evidence; no facts are invented. Where a verbatim phrase does not exist in repo, the gap is flagged explicitly in that section.

Source of truth for the active list: `/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md` Active Summary, plus the lane reports cited per section.

Hard guardrails preserved by producing this pack: no live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads, no Shopify live product-data changes, no Pinterest live writes, no theme edits.

---

## 1. PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE - Per-country apply playbook (PL/CZ/RO/PT/GR/IT/FR/BE)

**Current symptom:** TEST BUILD already approved 2026-05-10 and 9 of 17 countries (`GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`) are created paused with clean readback; the remaining 8 (`FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, `GR`) are absent. FR is parked on a stale completed-with-errors preview, BE is parked on an upload-throttle, IT is parked on an in-progress `0/0/0` preview, and PL/CZ/RO/PT/GR are simply unattempted.

**Business impact:** 8 non-US Search countries remain without paused infrastructure, so any future approved live-enable wave is bounded to the 9 existing markets and the staged sequence stalls before Tier-2 Europe.

**Verbatim approval phrase the owner can paste** (this is the original TEST BUILD phrase that already authorizes paused builds across all 17 listed countries; per `ops/prompts/paid-growth-ai-army-continuation-prompt.md` lines 179-181 and `ops/PROBLEM_TRACKER.md` Active Summary, this same approval continues to govern the per-country apply playbook for the remaining 8):

```
APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.
```

**Exact next safe action if approved (continuation):** Resume the per-country apply playbook in the frozen safest order `PL -> CZ -> RO -> PT -> GR -> IT -> FR -> BE`. One country at a time, full preview-then-apply-then-readback cycle, with stop-criteria enforced (preview must read `Changes 88 / Success 88 / Errors 0`; RPC readback must show `currency=USD`, `budget_usd=1.0`, `campaign_status=PAUSED`, `target_content_network=false`, `target_youtube_video=false`, `LOCATION_OF_PRESENCE` geo). Per-country preflight: IT requires stopping the in-progress preview first; FR requires re-upload to generate a fresh preview (do not Apply on the stale completed-with-errors record); BE requires waiting at least 60 minutes from the last upload and being run last. Do not chain uploads.

**Exact "park" action if deferred:** Leave all 8 remaining countries absent. Keep the 9 already-applied countries paused as-is. Do not start further Ads uploads. Update tracker note that the parked sub-gate is owner-deferred. The held English-only `1496`-row CSV and the 17 per-country split files remain intact and approval-gated for any later resumption.

**Linked evidence (existing files only):**
- `/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md` (Active Summary row for `PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE`)
- `/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md` (lines 179-181, verbatim phrase source)
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/GOOGLE_ADS_NON_US_SEARCH_PAUSED_TEST_BUILD_APPROVED_PARTIAL_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/working/final_campaign_readback_summary_2026-05-10_it_still_in_progress.json`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/ads-resume-order/ADS_RESUME_ORDER_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/ads-apply-playbook/ADS_APPLY_PLAYBOOK_REPORT.md`

---

## 2. PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE - English-first vs localized copy vs staged native build

**Current symptom:** Local native-language copy options exist for 14 locale variants (`es-ES`, `it-IT`, `pt-PT`, `ro-RO`, `de-DE`, `nl-NL`, `fr-FR`, `fr-BE`, `nl-BE`, `sv-SE`, `da-DK`, `pl-PL`, `cs-CZ`, `el-GR`) with `0` forbidden-claim hits, max headline length `24`, max description length `73`, but every locale remains concept-ready only and requires native-speaker review plus landing-language QA before platform use. The first approved paused build is currently English-only.

**Business impact:** Until the owner picks a copy posture, no non-US Search campaign can move toward live spend without language friction risk on conversion rate; Tier-2 Europe is gated behind the chosen path.

**Verbatim approval phrases the owner can paste:**

VERBATIM-PHRASE GAP FLAG: No per-option verbatim approval phrase was found in repo evidence for any of the three options below. The `lanes/native-language-copy-options/NATIVE_LANGUAGE_COPY_OPTIONS_REPORT.md` and `lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md` describe the three postures and the per-locale review/staging procedure but do NOT draft owner-paste-ready APPROVE phrases for the three options. What follows is what does exist in repo, quoted verbatim, with the gap clearly flagged.

What exists in repo (verbatim) describing the decision shape (`ops/PROBLEM_TRACKER.md` Active Summary, current next action for this problem):

> "Decide whether the first approved paused build stays English-first, uses localized/native-language copy after native review, or stages native copy as a second build; do not import or edit Ads without exact approval"

What exists in repo (verbatim) describing the fixed criterion (`ops/PROBLEM_TRACKER.md` Active Summary, fixed criteria for this problem):

> "Native-speaker-reviewed copy and landing-language QA are complete for the chosen markets, or the owner explicitly chooses English-first paused infrastructure with the caveat documented before any spend; any live account build remains separately approval-gated"

The three option descriptions, quoted from `lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md` and the prior options packet:

- **Option A - English-first paused infrastructure (status quo):** First approved paused build remains English-only. The held `1496`-row CSV stays the safer owner-approval-gated paused English-first build candidate. Owner must explicitly accept the English-on-non-English-landing caveat before any spend.
- **Option B - Localized/native-language copy after native review:** Stage native review per locale (recommended order: Tier 2 first batch `pt-PT` -> `es-ES` -> `it-IT` -> `ro-RO`; then mid batch `de-DE`, `fr-FR`, `nl-NL` paired with landing-language QA; then Tier 3 `sv-SE`, `da-DK`, `pl-PL`, `cs-CZ`, `el-GR`; with `fr-BE` / `nl-BE` held until the Belgium FR/NL split decision). Approval is per-locale, not bulk. Replace English ad copy with native copy only after each locale clears review.
- **Option C - Stage native copy as a second build:** Keep the first English-first paused build intact; create a separate paused second build per locale that uses the native copy after each locale clears review. Both builds remain paused-approval-gated.

**Exact next safe action if approved:** No live action - even after the owner picks a posture, the next steps are paused/local: stage native reviewer recruitment per the recommended batches, run landing-language QA on the country-qualified URL pattern per `lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md` section 3, then return for a separate exact-owner-approval phrase before any Ads import or campaign edit.

**Exact "park" action if deferred:** Leave the held `1496`-row English-only CSV and the 14 native-language locale option files intact and approval-gated. Do not run native reviewer recruitment, do not run landing-language QA. The first GB live-enable candidate (`GB / Mommy & Me Dresses - Exact only`, English) is unaffected because it does not depend on this gate.

**Linked evidence (existing files only):**
- `/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md` (Active Summary row for this problem)
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/NATIVE_LANGUAGE_COPY_OPTIONS_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_rsa_options.csv`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_keyword_option_notes.csv`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_copy_options_summary.json`

---

## 3. PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP - Narrow Merchant US/es age_group repair review

**Current symptom:** Merchant Center `124884876`, source `10627981690` / `Shopify App API` has affected `US` / `es` products without effective `n:age_group`. Status `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`.

**Business impact:** US/es paid-cohort items remain at risk of `Missing age group` disapprovals, blocking the Spanish-language US shopping surface from clean Merchant eligibility.

**Verbatim approval phrase the owner can paste** (verbatim from `/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md` lines 187-189):

```
APPROVE MERCHANT US/ES AGE_GROUP REPAIR REVIEW FOR SOURCE 10627981690: READ BACK THE US/ES PRODUCT DETAIL AND SOURCE STATE FIRST; THEN USE ONLY THE NARROWEST SAFE OFFICIAL REPAIR PATH FOR US FEED LABEL / ES LANGUAGE / UNITED STATES MISSING AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO BROAD SOURCE REFRESH, MERCHANT UPLOAD, SOURCE EDIT, OR SHOPIFY DATA EDIT WITHOUT A PREVIEW, EXACT ROW SCOPE, AND POST-READBACK.
```

**Exact next safe action if approved:** Read back the US/es product detail and source state first; preferred Path A is age_group-only supplemental source joined to source `10627981690` after exact preview; Path B only if source-specific refresh UI proves narrow. Capture pre/post readback evidence under the existing `2026-05-08-merchant-age-group-exact-export-readback/` packet pattern.

**Exact "park" action if deferred:** No Merchant write. The US/es Missing age_group surface stays as-is; document that the owner-deferred state continues. US/en age_group remains solved (`0` `Missing age group` rows) and unaffected.

**Linked evidence (existing files only):**
- `/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md` (Active Summary row for `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`)
- `/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md` (lines 187-189, verbatim phrase source)
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/merchant-pinterest-beach-gates/MERCHANT_PINTEREST_BEACH_APPROVAL_GATES.md`

---

## 4. PROB-2026-05-08-PINTEREST-EVENT-QUALITY - Pinterest Event Quality repair (Phrase A and Phrase B)

**Current symptom:** Advertiser `549756244483` Pinterest Event Quality reads `Fair`. Top three named gaps are `product_id__ADD_PAYMENT_INFO` (coverage `0.0% FAIL`), `hashed_email__ADD_TO_CART` (coverage `4.225% FAIL`, match rate `100% PASS`), `click_id_epik__CHECKOUT` (all `0.0`, volume-gated). Theme has zero `pintrk` / `epik` / `event_id` code; pixel is sourced from the official Shopify Pinterest app (`Always on` / share all events). Status `OWNER_APPROVAL_REQUIRED`.

**Business impact:** Pinterest live spend cannot be unblocked while Event Quality reads `Fair`; the clean `342`-row paused US draft also cannot be promoted. Risk of dedupe regression if a second tag is added blindly.

**Verbatim approval phrases the owner can paste** (both reproduced verbatim from `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/pinterest-event-quality-fix-plan/PINTEREST_EVENT_QUALITY_FIX_PLAN_REPORT.md` section 5):

**Phrase A (recommended first step - Event Quality dashboard repair, no theme/CAPI writes):**

```
APPROVE READ-ONLY PINTEREST EVENT QUALITY VERIFICATION AND OFFICIAL APP RECONFIRMATION FOR ADVERTISER 549756244483: OPEN PINTEREST ADS MANAGER EVENT QUALITY, CONVERSIONS HEALTH, ENHANCED MATCH, VERIFIED MERCHANT, AND AUTOMATIC ENHANCED MATCH VIEWS; OPEN THE OFFICIAL SHOPIFY PINTEREST APP AND THE SHOPIFY CUSTOMER EVENTS LIST PAGE; CONFIRM SHARE-ALL-EVENTS REMAINS ON, ADVERTISER BINDING REMAINS 549756244483, AND NO SECOND PINTEREST PIXEL EXISTS; NO CAMPAIGN, AD GROUP, AD, PRODUCT GROUP, AUDIENCE, BUDGET, BID, STATUS, TAG, CAPI, CATALOG, DATA SOURCE, FEED, MERCHANT, GOOGLE ADS, SHOPIFY PRODUCT, MARKETS, SHIPPING, OR THEME WRITE; READ BACK BEFORE AND AFTER.
```

**Phrase B (held in reserve - narrow Customer Events subscriber for product_id on AddPaymentInfo and hashed_email on AddToCart, no theme Liquid edit, no live spend):**

```
APPROVE NARROW SHOPIFY CUSTOMER EVENTS WEB PIXEL ADDITION FOR PINTEREST EVENT QUALITY REPAIR ONLY (PRODUCT_ID ON ADD_PAYMENT_INFO AND HASHED_EMAIL ON ADD_TO_CART): IMPLEMENT INSIDE A SINGLE NEW SHOPIFY CUSTOMER EVENT SUBSCRIBER (NOT A LIQUID THEME EDIT), REUSE THE OFFICIAL SHOPIFY PINTEREST APP EVENT_ID FOR DEDUPE, FIRE ONLY ADD_PAYMENT_INFO AND ADD_TO_CART, NO PAGE_VISIT/VIEW_CATEGORY/CHECKOUT/INITIATE_CHECKOUT/SEARCH/SIGNUP/LEAD; NO SECOND BASE TAG, NO PINTRK INSTALL IN LAYOUT/THEME.LIQUID OR ANY SNIPPET; NO SHOPIFY ADMIN PRODUCT DATA, MERCHANT, FEED, CATALOG, MARKETS, SHIPPING, OR CHECKOUT WRITE; NO PINTEREST CAMPAIGN, AD GROUP, AD, PRODUCT GROUP, AUDIENCE, BUDGET, BID, OR STATUS WRITE; NO LIVE SPEND ENABLEMENT; READ BACK BEFORE AND AFTER WITH NETWORK CAPTURE PROVING NO DUPLICATE EMISSION.
```

**Exact next safe action if approved:** Phrase A first - open the Pinterest dashboard verification flow per the lane C "Concrete action sequence" (Steps 0-7), reconfirm Verified Merchant Program `PASS`, Automatic Enhanced Match `PASS`, Enhanced Match per-event rows match probe baseline, official Shopify Pinterest app `Always on` and advertiser binding intact, and no second Pinterest pixel exists in Customer Events. Re-read Event Quality after a 24-72h observation window. Phrase B only if the 7-14 day Phrase A observation window does not lift `product_id__ADD_PAYMENT_INFO` and `hashed_email__ADD_TO_CART`.

**Exact "park" action if deferred:** No Pinterest dashboard or app actions. Pinterest Event Quality remains `Fair`. The clean `342`-row paused US draft remains review-only and cannot be promoted. No tag, CAPI, catalog source, audience, campaign, ad group, ad, budget, bid, status, or theme write happens.

**Linked evidence (existing files only):**
- `/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md` (Active Summary row for `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`)
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/pinterest-event-quality-fix-plan/PINTEREST_EVENT_QUALITY_FIX_PLAN_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/PINTEREST_PAUSED_US_DRAFT_STRUCTURE.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/event_quality_api_probe.json`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/event_quality.txt`

---

## 5. PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH - Narrow Shopify SEO/social-title repair

**Current symptom:** Public Shopify product `7227378892897` / handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` has stale Christmas title/OG/Twitter metadata on a beach/vacation paid-candidate URL, including sampled ES/IT/RO/PT localized metadata. Status `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD__OWNER_APPROVAL_REQUIRED_FOR_SHOPIFY_FIX`.

**Business impact:** Live paid traffic to this URL would land on Christmas-titled metadata while body/imagery is beach/vacation, hurting CTR-to-CVR and risking Merchant/quality-score penalties; until repaired, all approved paused Ads imports must exclude or swap any Vacation Family rows tied to this handle.

**Verbatim approval phrase the owner can paste** (verbatim from `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/beach-seo-gate/BEACH_SEO_GATE_REPORT.md` section 4):

```
APPROVE NARROW SHOPIFY SEO/SOCIAL-TITLE REPAIR FOR PRODUCT 7227378892897 / HANDLE matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set: REPLACE STALE CHRISTMAS TITLE/OG/TWITTER METADATA WITH BEACH/VACATION COPY MATCHING THE H1 IN EN AND IN ES/IT/RO/PT TRANSLATIONS; NO PRODUCT STATUS, PUBLICATION, PRICE, VARIANT, INVENTORY, HANDLE, IMAGE, TAG, BODY, COLLECTION-MEMBERSHIP, OR FEED-LABEL CHANGES; NO MERCHANT/GOOGLE ADS/PINTEREST/GA4/CAMPAIGN/FEED/BUDGET/BID/CONVERSION CHANGES; READ BACK PUBLIC TITLE/OG/TWITTER FOR EN AND THE FOUR LOCALES BEFORE AND AFTER.
```

**Exact next safe action if approved:** Capture public title/og:title/twitter:title BEFORE at the five EN/ES/IT/RO/PT URLs listed in `BEACH_SEO_GATE_REPORT.md` section 5, perform the narrow SEO/social-title field swap in Shopify Admin (no other field touched), then capture public AFTER readbacks at the same five URLs. Acceptance criterion: each readback shows beach/vacation-themed title/og:title/twitter:title that semantically match the H1 in the same locale, with zero remaining occurrences of `Christmas`, `Navideno`, `Natalizia`, `Craciun`, `Natal`, or any Christmas-equivalent term in those three fields.

**Exact "park" action if deferred:** No Shopify Admin write. The held `1496`-row local Google Ads CSV and the 17 per-country split files remain the local mitigation (each with `0` bad-handle hits and `0` Vacation Family rows tied to the bad handle); any future approved paused non-US Search preview/import must continue to exclude/swap all Vacation Family rows tied to this handle until the title is fixed. Do not send live paid traffic to this URL.

**Linked evidence (existing files only):**
- `/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md` (Active Summary row for `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`)
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/beach-seo-gate/BEACH_SEO_GATE_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/GOOGLE_ADS_SPLIT_IMPORT_CONTROL_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/landing-url-quality/LANDING_METADATA_QUALITY_REPORT.md`

---

## 6. First non-US live enable - GB / Mommy & Me Dresses - Exact only

**Current symptom (paired with PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE):** GB paused Search test campaign `23838895360` (`$2/day`, Manual CPC, `$0.15` cap, presence-only, content/YouTube off, all ad groups paused) is built clean and ready, but the very first non-US live spend action is gated on a fresh exact owner-approval phrase plus a 12-item just-in-time pre-enable gate.

**Business impact:** This is the smallest, safest first step toward proving the goal/landing/checkout chain works in a non-US market. Without it, no non-US revenue can be attributed and Tier-1 English market expansion (CA, AU) cannot start.

**Verbatim approval phrase the owner can paste** (verbatim from `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/first-enable-runbook/FIRST_ENABLE_RUNBOOK_REPORT.md` section 2):

```
APPROVE FIRST NON-US LIVE ENABLE - GB SEARCH ONLY: ENABLE CAMPAIGN 23838895360 (GB PAUSED NON-US SEARCH TEST BUILD) AND ENABLE ONLY THE AD GROUP "Mommy & Me Dresses - Exact only"; LEAVE ALL OTHER AD GROUPS IN CAMPAIGN 23838895360 PAUSED; KEEP DAILY BUDGET AT $2.00/DAY WITH NO BUDGET CHANGE; KEEP MANUAL CPC WITH MAX CPC CAP $0.15 WITH NO BID CHANGE; KEEP PRESENCE-ONLY GB GEO TARGETING; KEEP CONTENT NETWORK AND YOUTUBE OFF; KEEP ACCOUNT-DEFAULT PURCHASES CONVERSION GOAL WITH NO CONVERSION-GOAL CHANGE AND NO CAMPAIGN-LEVEL OVERRIDE; NO US CAMPAIGN 23827590655 CHANGES; NO PMAX, STANDARD SHOPPING, MERCHANT, FEED, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, SHOPIFY PRODUCT-DATA, PINTEREST, GA4/GTM, OR THEME CHANGES; NO ENABLE OF CA, AU, CH, DK, DE, NL, SE, OR ES PAUSED CAMPAIGNS; READ BACK CAMPAIGN STATUS, AD GROUP STATUS, BUDGET, MAX CPC, NETWORK, GEO, AND CONVERSION-GOAL BEFORE AND AFTER; APPLY $8 ZERO-PURCHASE WARNING / $16 ZERO-PURCHASE HARD-PAUSE / $24 ZERO-PURCHASE AD-GROUP-KILL RULE.
```

**Exact next safe action if approved:** Walk the 12-item pre-enable gate (`FIRST_ENABLE_RUNBOOK_REPORT.md` section 1: items 1-7 canonical safety, items 8-12 just-in-time live RPC readbacks). If every item passes, follow the apply-time runbook (section 3): pre-RPC readback -> enable ad group `Mommy & Me Dresses - Exact only` first -> enable campaign `23838895360` second -> capture post-RPC readback within 60 seconds; expected delta is exactly +1 ad group / +1 campaign enabled, everything else byte-identical. Then run the 24h / 72h / 7d review schedule with the `$8` warning / `$16` hard-pause / `$24` kill rules. Win threshold: CVR `>= 1.39%` over 7d with cumulative clicks `>= 50` (target CPA `$10.77` from `$70` AOV / `6.5x` ROAS).

**Exact "park" action if deferred:** No live enable. Campaign `23838895360` stays paused with all ad groups paused. No CA, AU, CH, DK, DE, NL, SE, or ES paused-campaign change. US campaign `23827590655`, Standard Shopping, Brand Search, Merchant, Pinterest, theme, and product/feed/conversion state stay untouched.

**Linked evidence (existing files only):**
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/first-enable-runbook/FIRST_ENABLE_RUNBOOK_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/market-activation/MARKET_ACTIVATION_SCORECARD.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/ads-resume-order/ADS_RESUME_ORDER_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md`

---

## 7. Defer-all default - what stays parked if the owner takes no action

If the owner does not approve any phrase above, the following posture is preserved automatically and no live writes occur in any lane:

1. **Non-US Search per-country apply playbook (Section 1):** 9 of 17 non-US Search countries remain paused/presence-only with clean readback. The remaining 8 (`PL`, `CZ`, `RO`, `PT`, `GR`, `IT`, `FR`, `BE`) stay absent. The held `1496`-row English-only CSV and 17 per-country split files remain intact and approval-gated. No further Ads uploads.
2. **Native-language copy posture (Section 2):** First approved paused build remains English-first. Local native copy options for 14 locale variants stay concept-ready only. No native reviewer recruitment, no landing-language QA, no Ads import or edit.
3. **Merchant US/es age_group (Section 3):** No Merchant Center write. US/es `Missing age group` cohort stays as-is. US/en age_group repair (already solved, `0` Missing rows) is unaffected.
4. **Pinterest Event Quality (Section 4):** No Pinterest dashboard reconfirm, no Customer Events subscriber. Event Quality stays `Fair`. The clean `342`-row paused US draft stays review-only and cannot be promoted. Pinterest live spend stays blocked.
5. **Beach SEO/social-title repair (Section 5):** No Shopify Admin write. The bad-handle metadata stays Christmas-themed on the beach/vacation URL. The held CSV / per-country splits remain the local mitigation; any future approved paused non-US Search preview/import must continue to exclude/swap Vacation Family rows tied to the bad handle.
6. **First non-US live enable - GB (Section 6):** No live enable. Campaign `23838895360` stays paused with all ad groups paused. The 12-item pre-enable gate is not walked. No 24h/72h/7d review schedule is started. No CA/AU/CH/DK/DE/NL/SE/ES enable is contemplated.

Across all six sections, defer-all preserves these standing facts already in repo: live-spend-ready non-US markets remain `0`; US Standard Shopping (`23802638621`) stays Enabled at owner-set budget with no product-scope/feed-label/product-group/conversion-goal change; US Brand Search stays Eligible at `$5/day`; US paused nonbrand Search rebuild (`23827590655`) stays paused; remarketing stays paused; Shopify ProductVariant `mm-google-shopping.age_group` stays fixed for all `780` paid-cohort variants; Pinterest official app pixel stays `Always on`; the prior 6 solved P0/P1/P2 items (localized shipping info link, localized collection grid count, localized size charts, DE/NL checkout QA, Standard Shopping live metrics readback, SE/PL/CZ/GR and FR/BE checkout QA) stay solved.

The only new state from defer-all is: this `OWNER_DECISION_PACK.md` exists in repo as the single-pass artifact for the next session to surface every parked gate.

---

## 8. Verbatim-phrase gap summary

- Section 1 (PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE): no gap. The original TEST BUILD phrase (continuation prompt lines 179-181) governs the parked sub-gate per the tracker's current next action.
- Section 2 (PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE): GAP. Three option postures are described in repo, but no option-specific verbatim APPROVE phrase exists in `lanes/native-language-copy-options/` or `lanes/native-language-review-checklist/`. Gap flagged in Section 2 above.
- Section 3 (PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP): no gap. Verbatim phrase reproduced from `ops/prompts/paid-growth-ai-army-continuation-prompt.md` lines 187-189.
- Section 4 (PROB-2026-05-08-PINTEREST-EVENT-QUALITY): no gap. Phrase A and Phrase B reproduced verbatim from lane C report section 5.
- Section 5 (PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH): no gap. Verbatim phrase reproduced from beach-seo-gate lane report section 4.
- Section 6 (First non-US live enable - GB): no gap. Verbatim phrase reproduced from first-enable-runbook lane report section 2.

---

## 9. Guardrails preserved by this pack

- This pack is local file write only. No live writes, no browser actions, no network requests, no theme edits, no Shopify/Merchant/Pinterest/GA4/Google Ads writes were performed by this lane.
- This pack does NOT make or execute any approval decision; the owner does.
- No new owner approval was requested in this session; only existing repo phrases were reproduced.
- `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, and `ops/AGENT_COORDINATION.md` were not modified by this lane (parent integrates).
- No CSV/JSON file outside this single `.md` was created or modified.
- No customer PII, cookies, request headers, payment data, or credentials are stored.

---

## 10. Files touched

WRITTEN by this subagent (lane report only):
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/owner-decision-pack/OWNER_DECISION_PACK.md`

READ by this subagent (no modifications):
- `/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md`
- `/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/pinterest-event-quality-fix-plan/PINTEREST_EVENT_QUALITY_FIX_PLAN_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/first-enable-runbook/FIRST_ENABLE_RUNBOOK_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/ads-apply-playbook/ADS_APPLY_PLAYBOOK_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/PAID_GROWTH_ORCHESTRATOR_DEEP_FOLLOWUP_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/beach-seo-gate/BEACH_SEO_GATE_REPORT.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/NATIVE_LANGUAGE_COPY_OPTIONS_REPORT.md`
