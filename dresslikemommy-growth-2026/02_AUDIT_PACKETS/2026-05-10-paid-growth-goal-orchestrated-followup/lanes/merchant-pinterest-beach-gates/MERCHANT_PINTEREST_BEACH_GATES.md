# Merchant, Pinterest, And Beach Gates

Generated: 2026-05-10

Worker: Worker C

Scope: consolidate current approval/readback gates for Merchant US/es age_group, Pinterest Event Quality, and beach SEO/social metadata. This is a local evidence synthesis only. No Merchant Center, Pinterest, Shopify Admin, browser, API, live product data, tracker, worklog, coordination, or other lane files were touched.

## Executive Board

| Gate | Current status | Already solved or mitigated | Next concrete unblock action | Live-spend ready |
|---|---|---|---|---|
| Merchant US/es age_group | `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX` | Original `US/en/United States` paid-cohort Missing age group is solved at `0`; Shopify variant age_group work must not be redone | Get exact owner approval for Path A supplemental age_group-only source joined to source `10627981690`, or Path B source-specific official refresh only if the UI proves it is narrow | No |
| Pinterest Event Quality | `OWNER_APPROVAL_REQUIRED` | Official app pixel path is alive; catalog scope is clean at `342` EN-US rows with `4` exclusions; review-only draft templates exist | Get exact owner approval either for paused US catalog/retargeting draft build, or for narrow Event Quality verification/repair | No |
| Beach SEO/social metadata | `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD__OWNER_APPROVAL_REQUIRED_FOR_SHOPIFY_FIX` | Held Ads CSV and all `17` split CSVs exclude the bad handle and `Vacation Family` rows | Keep using the held `1496`-row CSV for approved paused Search work, or get exact owner approval for narrow Shopify SEO/social-title repair | No |

## Gate 1: Merchant US/es Age_Group

Problem ID: `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`

Current status: `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`.

Current evidence:
- Merchant Center account `124884876`.
- Remaining issue surface is feed label `US`, language `es`, country `United States`, source `10627981690` / `Shopify App API`.
- Exact export showed `625` paid-cohort item IDs / `1,250` rows still have `Missing age group` only on `US/es/United States`, split as `625` Shopping ads rows and `625` Free listings rows.
- The original paid-cohort `US/en/United States` Missing age group count is `0`; that solved gate must not be reopened.
- Shopify-side ProductVariant `mm-google-shopping.age_group` was already fixed for the current paid cohort; repeating Shopify age_group edits is ruled out unless a fresh Shopify readback proves regression.
- Live read-only product-detail RPC confirmed two affected US/es samples on source `10627981690` still lack effective `n:age_group`; one control sample on the same source has effective `n:age_group`.

Already solved and must not be redone:
- Do not redo the US/en repair.
- Do not redo Shopify variant age_group writes.
- Do not treat the removed local-inventory add-on or dropshipping/local-inventory diagnostics as part of this problem.

Next concrete unblock action:
- Preferred Path A: get exact owner approval to preview and create/update one age_group-only Merchant supplemental source joined to source `10627981690`, scoped to the current affected US/es paid-cohort IDs and only columns `id` and `age_group`.
- Fallback Path B: get exact owner approval for one source-specific official Shopify App API / Google & YouTube refresh only if the UI proves it applies narrowly to source `10627981690` / feed label `US` / language `es`.

Approval phrases already present in repo evidence:

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH A ONLY: CREATE OR UPDATE ONE AGE_GROUP-ONLY MERCHANT SUPPLEMENTAL SOURCE JOINED TO SOURCE 10627981690 / SHOPIFY APP API FOR FEED LABEL US, LANGUAGE ES, COUNTRY UNITED STATES, USING ONLY EXACT PREVIEWED PAID-COHORT ITEM IDS CURRENTLY FAILING MISSING AGE_GROUP AND ONLY COLUMNS ID AND AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO PRIMARY SOURCE EDIT, BROAD SOURCE REFRESH, OR NON-AGE_GROUP PRODUCT-DATA CHANGE; PREVIEW ROW SCOPE FIRST, APPLY ONLY IF PREVIEW MATCHES, AND READ BACK SOURCE PROCESSING, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

```text
APPROVE MERCHANT US/ES AGE_GROUP PATH B ONLY: READ BACK SOURCE 10627981690 AND TWO AFFECTED US/ES PRODUCT DETAILS FIRST; THEN CLICK ONE CLEARLY LABELED SOURCE-SPECIFIC OFFICIAL SHOPIFY APP API / GOOGLE & YOUTUBE REFRESH, SYNC, OR UPDATE-PRODUCTS CONTROL ONLY IF THE UI CONTEXT PROVES IT APPLIES TO SOURCE 10627981690 / FEED LABEL US / LANGUAGE ES; NO MERCHANT UPLOAD, SOURCE CREATION, PRIMARY SOURCE EDIT, SHOPIFY PRODUCT-DATA EDIT, GOOGLE ADS, PINTEREST, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; DO NOT USE A BROAD ALL-SOURCES REFRESH; READ BACK SOURCE TIMESTAMP, PRODUCT DETAILS, EXACT EXPORT, AND LABEL/SCOPE INTEGRITY AFTER.
```

Safe local/read-only work that can continue:
- Reconcile existing exports and sample IDs.
- Prepare row-scope preview files locally, marked not-uploadable, if requested by the parent.
- Keep paused Ads, Pinterest, CRO, reporting, and measurement lanes moving without Merchant writes.

Prohibited actions:
- Broad Merchant refresh/sync, Merchant upload without exact approval, primary source edit, source edit without preview, Shopify product-data edit, local-inventory feed/pickup/store-stock work, Standard Shopping change, product-scope/feed-label/product-group/conversion-goal change, Google Ads/Pinterest write, budget/bid/status change, PMax change, campaign enablement, or live spend.

Fixed criteria:
- Fresh exact export or equivalent shows `0` paid-cohort `US/es/United States` Missing age group rows.
- Formerly affected US/es product details show effective `n:age_group`.
- Paid-cohort `US/en/United States` remains `0`.
- Standard Shopping scope, labels, groups, budget, bids, status, and conversion goals remain unchanged.

## Gate 2: Pinterest Event Quality And Paused Drafts

Problem ID: `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`

Current status: `OWNER_APPROVAL_REQUIRED`.

Current evidence:
- Pinterest advertiser `549756244483`.
- Event Quality remains `Fair`.
- Official Shopify Pinterest app path is alive; prior stored activity showed Tag and CAPI timestamps fresh after the app pixel was set to `Always on` / share all events.
- Clean US catalog scope is `342` EN-US in-stock rows with `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready`.
- Exact exclusions are variants `41878208249953`, `41878208479329`, `41878208577633`, and `41878208610401`.
- Review-only paused-draft templates exist and are marked `REVIEW_ONLY_NOT_UPLOAD`.
- Event Quality top gaps are mapped: `product_id__ADD_PAYMENT_INFO`, `hashed_email__ADD_TO_CART`, and `click_id_epik__CHECKOUT`.
- Theme readback found no theme-side Pinterest tag firing code: no `pintrk`, `pinterest_tag`, `tag_id`, or `epik` matches that would indicate an existing custom tag. Pinterest enters via Shopify official app / `content_for_header`.

Already solved and must not be redone:
- Do not reopen the old `337/346` catalog scope; it is superseded by clean `342` rows plus `4` exclusions.
- Do not add a duplicate theme-level Pinterest tag or custom CAPI by inference.
- Do not include the four excluded variants unless a fresh just-in-time proof resolves them.

Next concrete unblock action:
- Option A: get exact owner approval for paused US catalog/retargeting draft objects using only the clean `342` rows and `4` exclusions. This can create infrastructure but must remain paused and non-serving.
- Option B: get exact owner approval for narrow Event Quality verification/repair. Phrase A below is read-only official-app/dashboard reconfirmation and is the recommended first repair step in the existing evidence. Phrase B is reserved for a later Customer Events web pixel addition if reconfirmation and observation do not lift the app-managed gaps.

Approval phrases already present in repo evidence:

```text
APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.
```

```text
APPROVE READ-ONLY PINTEREST EVENT QUALITY VERIFICATION AND OFFICIAL APP RECONFIRMATION FOR ADVERTISER 549756244483: OPEN PINTEREST ADS MANAGER EVENT QUALITY, CONVERSIONS HEALTH, ENHANCED MATCH, VERIFIED MERCHANT, AND AUTOMATIC ENHANCED MATCH VIEWS; OPEN THE OFFICIAL SHOPIFY PINTEREST APP AND THE SHOPIFY CUSTOMER EVENTS LIST PAGE; CONFIRM SHARE-ALL-EVENTS REMAINS ON, ADVERTISER BINDING REMAINS 549756244483, AND NO SECOND PINTEREST PIXEL EXISTS; NO CAMPAIGN, AD GROUP, AD, PRODUCT GROUP, AUDIENCE, BUDGET, BID, STATUS, TAG, CAPI, CATALOG, DATA SOURCE, FEED, MERCHANT, GOOGLE ADS, SHOPIFY PRODUCT, MARKETS, SHIPPING, OR THEME WRITE; READ BACK BEFORE AND AFTER.
```

```text
APPROVE NARROW SHOPIFY CUSTOMER EVENTS WEB PIXEL ADDITION FOR PINTEREST EVENT QUALITY REPAIR ONLY (PRODUCT_ID ON ADD_PAYMENT_INFO AND HASHED_EMAIL ON ADD_TO_CART): IMPLEMENT INSIDE A SINGLE NEW SHOPIFY CUSTOMER EVENT SUBSCRIBER (NOT A LIQUID THEME EDIT), REUSE THE OFFICIAL SHOPIFY PINTEREST APP EVENT_ID FOR DEDUPE, FIRE ONLY ADD_PAYMENT_INFO AND ADD_TO_CART, NO PAGE_VISIT/VIEW_CATEGORY/CHECKOUT/INITIATE_CHECKOUT/SEARCH/SIGNUP/LEAD; NO SECOND BASE TAG, NO PINTRK INSTALL IN LAYOUT/THEME.LIQUID OR ANY SNIPPET; NO SHOPIFY ADMIN PRODUCT DATA, MERCHANT, FEED, CATALOG, MARKETS, SHIPPING, OR CHECKOUT WRITE; NO PINTEREST CAMPAIGN, AD GROUP, AD, PRODUCT GROUP, AUDIENCE, BUDGET, BID, OR STATUS WRITE; NO LIVE SPEND ENABLEMENT; READ BACK BEFORE AND AFTER WITH NETWORK CAPTURE PROVING NO DUPLICATE EMISSION.
```

Gap flag:
- No evidence found in this lane that the owner has already approved any of the three Pinterest phrases above for execution in the current session. Treat them as approval text to request, not as granted approval.

Safe local/read-only work that can continue:
- Revalidate the `342`-row scope and four exclusions from local files.
- Maintain/review local draft templates as review-only artifacts.
- Draft QA checklists and readback plans.
- Continue non-Pinterest reporting, ROAS, localization, Ads paused-infra, and measurement planning that does not write to Pinterest.

Prohibited actions:
- Live Pinterest spend, campaign/ad/ad-group/product-group launch, serving enablement, budget or bid activation, catalog source edit, tag/CAPI/pixel change, custom CAPI/token work, duplicate theme tag, audience changes, Shopify product edit, Merchant write, Google Ads write, feed change, or including the four unresolved variants without fresh proof.

Fixed or enable criteria:
- For draft creation: all objects are paused/draft only, serving remains `0`, spend remains `$0.00`, scope remains the `342` clean rows with `4` exclusions, and no tag/CAPI/catalog/feed/audience/budget/bid/source changes occur outside approval.
- For live spend: Event Quality must be proven good enough in a single readback session, or the owner must explicitly accept the documented `Fair` risk in a separate spend approval. The `click_id_epik` gap is volume-gated and cannot be fully resolved before real Pinterest clicks.

## Gate 3: Beach / Vacation Family SEO And Social Metadata

Problem ID: `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`

Current status: `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD__OWNER_APPROVAL_REQUIRED_FOR_SHOPIFY_FIX`.

Current evidence:
- Shopify product `7227378892897`.
- Handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set`.
- Paid theme in Ads packets: `Vacation Family`.
- Public product URL returned HTTP `200` and showed beach/vacation H1, but `<title>`, `og:title`, and `twitter:title` were `Family Matching Sets - Christmas Print | Dress Like Mommy`.
- Sampled ES, IT, RO, and PT localized routes showed analogous Christmas-themed title metadata over beach/vacation H1s.
- Local Ads mitigation is intact: held CSV `00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv` has `1496` data rows with `0` bad-handle hits and `0` `Vacation Family` hits.
- All `17` per-country split CSVs have `88` rows each and reconcile to `1496` total rows, with `0` bad-handle hits and `0` `Vacation Family` hits.

Already solved or mitigated and must not be redone:
- Do not use the original `1666`-row non-US Search packet as the preferred candidate while this URL remains stale.
- Do not re-add Vacation Family rows to Ads packets until public metadata is repaired and read back, or the URL is swapped for a clean one.
- Do not perform broad product-data cleanup. Evidence supports a narrow SEO/social-title issue on this product unless a later scan proves a wider pattern.

Next concrete unblock action:
- Fastest paused Ads path: keep using the held `1496`-row CSV and per-country split files that exclude the bad handle and `Vacation Family`.
- If the owner wants the Vacation Family theme restored, request exact approval for narrow Shopify SEO/social-title repair on product `7227378892897`, then read back public English plus ES/IT/RO/PT title, OG title, and Twitter title before reintroducing this URL into Ads artifacts.

Approval phrases already present in repo evidence:

```text
APPROVE NARROW SHOPIFY SEO/SOCIAL-TITLE REPAIR FOR PRODUCT 7227378892897 / HANDLE matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set: REPLACE STALE CHRISTMAS TITLE/OG/TWITTER METADATA WITH BEACH/VACATION COPY MATCHING THE H1 IN EN AND IN ES/IT/RO/PT TRANSLATIONS; NO PRODUCT STATUS, PUBLICATION, PRICE, VARIANT, INVENTORY, HANDLE, IMAGE, TAG, BODY, COLLECTION-MEMBERSHIP, OR FEED-LABEL CHANGES; NO MERCHANT/GOOGLE ADS/PINTEREST/GA4/CAMPAIGN/FEED/BUDGET/BID/CONVERSION CHANGES; READ BACK PUBLIC TITLE/OG/TWITTER FOR EN AND THE FOUR LOCALES BEFORE AND AFTER.
```

```text
APPROVE NARROW SHOPIFY PRODUCT SEO TITLE REPAIR ONLY FOR PRODUCT 7227378892897 / HANDLE matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set: READ BACK CURRENT TITLE, SEO TITLE, META DESCRIPTION, OG/TWITTER TITLE SOURCE, AND TRANSLATIONS FIRST; THEN CHANGE ONLY THE STALE CHRISTMAS SEO/SOCIAL TITLE METADATA TO BEACH/VACATION FAMILY OUTFIT WORDING; DO NOT CHANGE PRODUCT STATUS, HANDLE, PRICE, VARIANTS, INVENTORY, TAGS, VENDOR/SOURCE URL FIELDS, PUBLICATIONS, MERCHANT, GOOGLE ADS, PINTEREST, FEED LABELS, PRODUCT SCOPE, PRODUCT GROUPS, CONVERSION GOALS, BUDGETS, BIDS, CAMPAIGN STATUS, THEME, OR LIVE SPEND; READ BACK PUBLIC TITLE/OG/TWITTER TITLE AFTER.
```

Gap flag:
- No evidence found in this lane that the owner has already approved either beach metadata repair phrase for execution in the current session. Treat them as approval text to request, not as granted approval.

Safe local/read-only work that can continue:
- Keep validating that held Ads CSVs exclude the handle, product ID `7227378892897`, `Vacation Family`, `Christmas`, and `Xmas`.
- Prepare public readback URL/checklist for EN, ES, IT, RO, and PT.
- Continue paused Ads build/import work only from the held CSV/splits where already approved by parent and owner, without restoring Vacation Family.

Prohibited actions:
- Shopify live product-data/SEO/social metadata edit without exact approval, handle change, price/variant/inventory/status/publication/tag/vendor/source URL/body/collection/feed-label change, Merchant upload/source edit, Google Ads preview/import/enablement tied to the stale URL, Pinterest write, product-scope/feed-label/product-group/conversion-goal change, budget/bid/status change, PMax, Standard Shopping change, theme edit, or live spend.

Fixed criteria:
- Public EN product URL and sampled ES/IT/RO/PT routes show beach/vacation-specific `<title>`, `og:title`, and `twitter:title`.
- No stale Christmas wording remains in those three metadata fields.
- Product status, handle, price, variants, inventory, tags, vendor/source fields, publications, Merchant/feed/campaign settings, budgets, bids, conversion goals, theme, and live spend remain unchanged.
- A refreshed Ads packet either keeps using the held CSV or explicitly validates re-adding Vacation Family after public metadata passes.

## Cross-Gate Work That Can Continue

- Local/reporting work: ROAS guardrails, scorecards, QA checklists, evidence consolidation, readback scripts, and non-uploadable templates.
- Paused Search infrastructure work that uses already-approved, held, country-split CSVs and does not touch Merchant/Pinterest/Shopify Admin or live spend.
- Measurement pre-enable planning and public/local readback design, provided no payment, order, account write, or live external-system mutation occurs.
- Native-copy review planning and landing-page QA that avoids Shopify product-data edits.

## Cross-Gate Prohibitions Under Current Guardrails

- Do not touch Merchant, Pinterest, Shopify Admin, browser, APIs, live product data, tracker, worklog, coordination, or other lanes from this Worker C task.
- Do not bundle these gates into one approval or one live browser/account action.
- Do not infer approval from prepared approval wording.
- Do not enable live spend, raise budgets, change bids, change campaign status, edit Standard Shopping/PMax/product groups/feed labels/product scopes/conversion goals, or write to Shopify product data.
- Do not write vendor/source URLs into any customer-visible or sales-channel-visible product data.
- Do not create local inventory feeds, pickup claims, warehouse/local-stock claims, or on-hand-stock claims for this dropshipping business.

## Evidence Paths

- `ops/PROBLEM_TRACKER.md`
- `ops/AGENT_WORKLOG.md` anchor references only, not edited by this worker
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/MERCHANT_AGE_GROUP_EXACT_EXPORT_READBACK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-merchant-age-group-exact-export-readback/reconciliation/merchant-product-issues-paid-age-group-context-breakdown.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-readonly-us-es-au-followup/lanes/merchant-us-es-readonly/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/merchant-us-es-repair/MERCHANT_US_ES_AGE_GROUP_REPAIR_APPROVAL_PACKET.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/merchant-pinterest-beach-gates/MERCHANT_PINTEREST_BEACH_APPROVAL_GATES.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/PINTEREST_PAUSED_US_DRAFT_STRUCTURE.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/pinterest-paused-draft/PINTEREST_PAUSED_DRAFT_GATE_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/pinterest-event-quality-fix-plan/PINTEREST_EVENT_QUALITY_FIX_PLAN_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/PAID_GROWTH_URL_HOLD_CHECKOUT_SAFE_ADVANCE_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/landing-url-quality/LANDING_METADATA_QUALITY_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/GOOGLE_ADS_INTL_URL_HOLD_VALIDATION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/GOOGLE_ADS_SPLIT_IMPORT_CONTROL_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/beach-seo-gate/BEACH_SEO_GATE_REPORT.md`

## Files Touched

- Created: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup/lanes/merchant-pinterest-beach-gates/MERCHANT_PINTEREST_BEACH_GATES.md`
