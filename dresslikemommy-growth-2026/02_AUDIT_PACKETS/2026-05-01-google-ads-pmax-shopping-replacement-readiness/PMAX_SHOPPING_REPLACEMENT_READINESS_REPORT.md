# 2026-05-01 PMax Shopping Replacement Readiness

Confidence: H for current blocker diagnosis from repo readbacks; M for final activation timing because live Google Ads/Merchant writes still require owner approval and fresh readbacks.

## Scope

Owner request: fix all issues with `PMax: Shopping ads (United States)` so it can eventually be activated.

Coordination result:
- `ops/AGENT_COORDINATION.md` was checked before work.
- Work was limited to local planning and handoff files.
- No Google Ads, Merchant Center, Shopify Admin, GA4/GTM, Pinterest, feed, product data, budget, conversion-goal, product-scope, asset, or campaign-status edits were made.

## Campaign Decision

Decision: `REPLACE_NOT_REPAIR_IN_PLACE`.

The existing live campaign `PMax: Shopping ads (United States)` / `18154132278` should not be activated or repaired in place.

Known live blockers from prior readback:
- Status included `No products for any locations`.
- Asset group text referenced products from `truehairwigs`.
- Prior settings readback recorded Merchant Center `513542500 - truehairwigs`.
- Campaign is paused at `$1.00/day` with `$0.00` cost, `0` impressions, `0` clicks, and `0.00` conversions.

Activating that object would risk sending Dress Like Mommy spend through the wrong Merchant/product source. The safe fix is to keep it paused, archive/rename it only after owner approval, and build a replacement PMax shell using the Dress Like Mommy Merchant Center account.

## Replacement Build Spec

Replacement campaign name:
`DLM_US_PMAX_PAID_READY_REPLACEMENT_DRAFT`

Initial status:
`Paused`

Merchant Center:
`124884876 - Dresslikemommy`

Initial budget:
`$1.00/day` draft/safety budget unless the owner approves another amount at action time.

Targeting:
- United States.
- Presence-only where Google Ads exposes the setting.
- English.

Product scope:
- Must use only Dress Like Mommy products.
- Must use only eligible Merchant rows with `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready`.
- Current local paid cohort evidence: `780` rows across `81` products, all `in_stock`, all `margin_medium`, all `aov_medium`.
- Category split in the verified local cohort: `345` swimsuits, `214` mommy_me, `103` family_matching, `89` daddy_me, `29` pajamas.
- Must not run concurrently against the same product scope as active Standard Shopping unless the owner approves a deliberate overlap/cannibalization test or Standard Shopping is paused/its scope is changed after its review.

URL controls:
- Final URL expansion off, or restricted to approved Dress Like Mommy `/products/` and `/collections/` URLs only.
- No supplier/source URLs in titles, descriptions, tags, metafields, feed-visible fields, or landing pages.

Brand control:
- Do not use PMax as a brand-protection vehicle while Brand Search is live at `$5/day`.
- Add or document brand exclusion / brand traffic posture before activation so PMax does not quietly consume branded demand.

Measurement:
- Use account-default purchase goal only after final readback confirms the primary purchase action remains the value-verified `Google Shopping App Purchase`.
- Do not change conversion goals without explicit owner approval.

## Activation State

Current state: `LOCAL_REPLACEMENT_BLUEPRINT_READY__LIVE_ACTIVATION_BLOCKED`.

All known issues with the existing campaign are resolved only by replacement:
- wrong Merchant source: replacement must use `124884876 - Dresslikemommy`;
- no-products blocker: replacement must attach verified paid-ready products;
- unsafe product overlap: replacement must wait for a Standard Shopping owner decision or use a separately approved non-overlapping cohort;
- final URL risk: replacement must lock URL expansion/allowlist;
- brand cannibalization risk: replacement must document brand exclusion posture;
- activation risk: replacement must remain paused until a fresh gate passes.

## Required Live Fix Sequence

1. Run a fresh read-only Google Ads readback for `PMax: Shopping ads (United States)` and confirm it remains paused.
2. Run a fresh Merchant supplier-domain gate and paid-cohort readback.
3. Get owner approval to rename/archive the bad existing PMax campaign or leave it paused with a clear `DO_NOT_USE` note.
4. Get owner approval to create a paused replacement PMax shell.
5. Build replacement shell with correct Merchant account `124884876 - Dresslikemommy`.
6. Attach only the approved product cohort.
7. Keep replacement paused and run final readbacks for Merchant, product count, conversion goal, location, URL expansion, brand posture, assets, and audience signals.
8. Only after owner approval, run activation at the owner-approved budget and rollback threshold.

## What Was Not Done

- Did not enable PMax.
- Did not create a replacement campaign.
- Did not rename or archive the existing PMax campaign.
- Did not touch Merchant Center, feeds, product labels, Standard Shopping, Brand Search, Remarketing, conversion goals, or budgets.

## Next Owner Decision

The next safe action is not activation. It is approval to prepare a paused replacement shell and leave all spend off.

Suggested exact phrase:

`APPROVE CREATE PAUSED PMAX SHOPPING REPLACEMENT DRAFT ONLY; USE MERCHANT 124884876; KEEP ALL PMAX CAMPAIGNS PAUSED; DO NOT CHANGE STANDARD SHOPPING, BUDGETS, PRODUCT SCOPE, OR CONVERSION GOALS`

