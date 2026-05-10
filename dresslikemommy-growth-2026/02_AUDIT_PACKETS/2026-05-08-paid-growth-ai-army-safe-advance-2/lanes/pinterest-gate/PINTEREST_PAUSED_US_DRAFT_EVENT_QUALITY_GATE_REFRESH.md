# Pinterest Paused US Draft / Event Quality Gate Refresh

Generated: 2026-05-08 local/read-only subagent pass.

Mode: local/read-only evidence refresh only. No Pinterest account, campaign, draft, product group, catalog source, audience, tag, CAPI, budget, bid, account setting, or spend write was made.

## Verdict

`PASS_FOR_EXACT_OWNER_APPROVED_PAUSED_US_DRAFT__FAIL_FOR_LIVE_SPEND_UNTIL_EVENT_QUALITY_ACCEPTED_OR_REPAIRED`

The clean Pinterest US launch scope remains valid for a future exact-owner-approved paused draft:

- Clean scope CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`
- Clean rows: `342`
- Unique Shopify variant IDs: `342`
- Locale: `342` rows `en-US`
- Availability: `342` rows `IN_STOCK`
- Pinterest item status: `342` rows `FOUND_EN_US_IN_STOCK`
- Paid labels: `342` rows `custom_label_0=paid_eligible`, `342` rows `custom_label_4=us_test_ready`
- Market and Merchant status: `342` rows `US`, `342` rows `Approved`
- Review status: `342` rows `CANDIDATE_ONLY_NOT_LAUNCH_APPROVED`
- Product split: `210` Mommy & Me, `103` Family Matching, `29` Pajamas

The four unresolved variants remain correctly excluded:

- Exclusions CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`
- Excluded variant IDs: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`
- Exclusion status: `4` rows `NOT_RERESOLVED`
- Pinterest item status: `4` rows `NOT_CURRENTLY_RESOLVED_EN_US`
- Review status: `4` rows `EXCLUDED_FROM_CURRENT_PINTEREST_SCOPE`
- Clean/exclusion overlap: `0`

The old `337/346` blocker remains superseded by the later `342` clean scope with `4` explicit exclusions. Do not reuse the older `337` resolved / `9` excluded plan unless a fresh just-in-time proof changes the row state again.

## Event Quality Gate

Freshest stored Event Quality evidence used:

- Probe generated: `2026-05-08T05:55:17.164Z`
- Advertiser: `549756244483`
- Event Quality updated date: `2026-05-06`
- Pinterest Tag status: `FAIR`
- Conversions API status: `FAIR`
- Pinterest Tag latest raw timestamp in API proof: `1778219456502890000`
- Conversions API latest raw timestamp in API proof: `1778219473760287700`
- Verified Merchant Program: `PASS`
- Automatic Enhanced Match: `PASS`
- Enhanced Match: `ERROR`
- Top action items: `product_id__ADD_PAYMENT_INFO`, `hashed_email__ADD_TO_CART`, `click_id_epik__CHECKOUT`

Interpretation:

- The official Pinterest app path is alive because both Tag and CAPI have fresh stored activity.
- `Fair` Event Quality is not a blocker to creating paused draft objects after exact owner approval and just-in-time readbacks.
- `Fair` Event Quality remains a live-spend blocker unless the owner explicitly accepts the risk or approves a narrow tracking repair.
- The `click_id_epik` gap may remain weak until Pinterest has real serving/click traffic, but that does not justify duplicate tags or custom CAPI without approval.

## Account / Campaign Baseline

Latest stored read-only campaign baseline:

- Advertiser: `549756244483`
- Account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Campaign baseline date range: `2026-04-08` through `2026-05-07`
- Campaigns: `0`
- Currently serving: `0`
- Spend: `$0.00`
- Login/CAPTCHA/unsaved/billing blocker hints in stored baseline: all `false`

No fresh Pinterest browser/API readback was run in this subagent pass; the task was local/read-only validation from stored evidence packets.

## Safe Source Gate

Use only the EN-US Shopify source for any future US paused draft:

- Catalog: `Catalog_Retail`
- Catalog ID: `3041764155561548387`
- Helper Merchant ID: `3041760832963738705`
- EN Shopify source/feed profile: `3041760867124595727`
- Prior source readback: `Completed`, `5,663/5,663` uploaded, `0` failed, `152` warnings
- Known warning: `description_html` too long; Pinterest indicates affected items publish without `description_html`

Do not use:

- Failed sitemap source `3041760916127467912`
- Localized Pinterest catalog sources
- Any international Pinterest expansion before US measurement is cleaner

## Paused-Draft Approval Checklist

Before any approved paused Pinterest draft write:

1. Confirm the owner gives the exact paused US Pinterest approval phrase below.
2. Re-read `ops/AGENT_COORDINATION.md` and ensure one Pinterest writer owns the live account surface.
3. Run just-in-time read-only campaign baseline for advertiser `549756244483`: campaign count, currently serving count, spend, active/promoted objects, login/CAPTCHA/billing/unsaved prompts.
4. Run just-in-time read-only Event Quality readback: overall WEB, Tag, CAPI, updated date, latest Tag/CAPI timestamps, top action items.
5. Revalidate the clean scope CSV row count and exclusions: `342` clean rows, `4` exclusions, no overlap, all clean rows `en-US` / `IN_STOCK`.
6. Verify the draft source is the EN-US Shopify source `3041760867124595727`, not the failed sitemap or localized feeds.
7. Build only US paused catalog/retargeting draft objects; keep all campaign/ad group/ad/product group objects paused.
8. Do not activate budget or bids for serving; do not enable, launch, promote, or set anything live.
9. Do not change tag/CAPI, catalog source, feed, product group source, Shopify products, Merchant, Google Ads, conversion goals, budgets, bids, audiences, or live spend.
10. Save before/after readbacks in the evidence packet, then hand control back to the parent/orchestrator for tracker/worklog/coordination updates.

Exact approval gate:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

## Event Quality Repair Checklist

If the owner chooses tracking repair before drafts:

1. Treat this as a separate approval lane from paused draft creation.
2. Investigate official Shopify/Pinterest app and customer events configuration for the three top gaps only: Product ID in AddPaymentInfo, hashed email in AddToCart, click ID in Checkout.
3. Avoid duplicate Pinterest tags, duplicate CAPI, or theme-level tracking unless a separate implementation and privacy-safe credential plan is approved.
4. Keep all campaign/draft/product group/catalog source/audience/budget/bid/status/spend objects untouched.
5. Read back Event Quality before and after, including latest Tag/CAPI timestamps and top action items.

Suggested approval gate:

`APPROVE NARROW PINTEREST EVENT QUALITY REPAIR ONLY: INVESTIGATE OFFICIAL SHOPIFY/PINTEREST APP AND CUSTOMER EVENTS CONFIGURATION FOR PRODUCT ID, EMAIL, AND CLICK ID GAPS; NO CAMPAIGN, DRAFT, PRODUCT GROUP, CATALOG SOURCE, AUDIENCE, BUDGET, BID, STATUS, OR SPEND CHANGES; NO DUPLICATE THEME TAG; NO CUSTOM CAPI DEPLOYMENT OR CUSTOMER-DATA CHANGE WITHOUT A SEPARATE READBACK AND APPROVAL; READ BACK BEFORE AND AFTER.`

## Readback Plan

Pre-write readback for paused draft approval:

- Pinterest Ads Manager campaign table: advertiser `549756244483`, `0` campaigns or exact current count, `0` currently serving, spend total, no active/serving surprises.
- Pinterest Event Quality: WEB overall, Tag status, CAPI status, updated date, latest Tag/CAPI timestamps, Verified Merchant Program, Automatic Enhanced Match, Enhanced Match, top action items.
- Pinterest catalog source: EN Shopify source `3041760867124595727` is completed and usable; failed sitemap and localized sources are not selected.
- Local CSV guard: clean `342` rows and four exact excluded variant IDs still match.

Post-write readback if owner approval is granted:

- Campaign/ad group/ad/product group objects created only as paused/draft, with no currently serving objects.
- Spend remains `$0.00` after creation.
- Product group/scope uses the 342-row clean set and excludes `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`.
- No tag/CAPI/catalog/feed/audience/budget/bid/source changes were made outside the approval text.
- Event Quality status is recorded again; live spend stays blocked if still `Fair`.

## Ruled-Out Paths

- Creating paused Pinterest objects now: not allowed in this subagent pass and no action-time owner approval was present.
- Live spend or enablement: blocked by `Fair` Event Quality and no live-spend approval.
- Including the 4 unresolved variants: blocked until they re-resolve in fresh just-in-time proof.
- Using sitemap/localized sources: blocked by stored source health and US-only scope.
- Adding duplicate theme tag or custom CAPI: blocked without separate exact approval because it risks duplicate events, PII/credential handling, and measurement drift.

## Parent Integration Note

This subagent wrote only this lane folder per scope. Parent/orchestrator should update `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, and `ops/AGENT_COORDINATION.md` if this lane is integrated into the broader sprint handoff.
