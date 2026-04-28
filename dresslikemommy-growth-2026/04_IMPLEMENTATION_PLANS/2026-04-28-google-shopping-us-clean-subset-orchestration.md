# Google Shopping US Clean Subset Orchestration

Date: 2026-04-28
Mode: planning and orchestration only. No Shopify, Merchant Center, Google Ads, or campaign write is approved by this document.

## Goal

Create a small US-only Standard Shopping clean subset for Dress Like Mommy.

The clean subset, not the campaign, decides what Google is allowed to advertise:

- `paid_eligible = true`
- `market = US`
- `campaign_type = Standard Shopping`
- `campaign_status = PAUSED`
- Products only from known-margin, Merchant Center approved, clean-PDP, high-AOV candidates.

Explicitly excluded:

- Performance Max
- broad Search
- Display
- Dynamic Search Ads
- all-products Shopping
- international paid campaigns
- any enabled/live campaign
- any feed upload before owner review of the CSV

## Current Local State

Latest fresh post-cost-sync Shopify export:

- Summary: `dresslikemommy-growth-2026/03_LOCAL_ANALYSIS/2026-04-28-variant-cost-50pct-post-sync_PAID_LABEL_FRESH_SHOPIFY_summary.json`
- Eligibility table: `dresslikemommy-growth-2026/03_LOCAL_ANALYSIS/2026-04-28-variant-cost-50pct-post-sync_PAID_LABEL_FRESH_SHOPIFY_product_eligibility.csv`
- Active variants: `7,324`
- Missing Shopify Cost per item rows: `0`
- Reliable cost basis rows: `7,324`
- Current local `paid_eligible` rows from cost/inventory gate only: `7,227`
- Current local excluded rows: `97`, all `OUT_OF_STOCK`
- Missing SKU rows still present: `1,604`
- Missing barcode/GTIN rows still present: `5,897`

Important interpretation:

- The cost blocker was fixed locally/live in Shopify, but the current local `paid_eligible` value is not final Google Shopping eligibility.
- The current local gate does not yet include Merchant Center approval, item diagnostics, PDP pass/fail, US shipping/return policy verification, GTIN/SKU hard fails, or low-AOV/multi-item prioritization.
- Therefore `7,227` is a preliminary economics/inventory pass, not an ad-ready count.

## Current Label Conflict

The existing local paid-label export diverges from the requested Shopping test schema.

Current post-cost-sync export:

- `custom_label_4 = FIX_BEFORE_PAID` or `EXCLUDE_PAID`
- `custom_label_0..3` still carry older meanings from Shopify/marketing labels.

Requested schema:

- `custom_label_0`: paid eligibility group, for example `paid_eligible`, `exclude_unknown_margin`, `exclude_feed_issue`, `exclude_pdp_issue`
- `custom_label_1`: margin tier, for example `margin_high`, `margin_medium`, `margin_low`, `margin_unknown`
- `custom_label_2`: product family, for example `mommy_me`, `family_matching`, `swimsuits`, `dresses`, `pajamas`, `daddy_me`
- `custom_label_3`: AOV tier, for example `aov_high`, `aov_medium`, `aov_low`
- `custom_label_4`: market/test status, for example `us_test_ready`, `us_fix_before_paid`, `international_exclude`

Required conclusion:

- Do not upload the existing paid-status-only file as the final clean-subset label plan.
- Generate a new full-label, owner-reviewed clean-subset file that implements the requested schema.

## Merchant Center Source Caution

Known historical source:

- Merchant Center account: `124884876`
- Supplemental source name: `supplemental_feed_pilot.txt`
- Supplemental join/source id observed historically: `10626787326`
- Historical join key: `shopify_US_<product_id>_<variant_id>`

During the previous upload task, the source page was reached in an authenticated browser and a tab-delimited paid-status-only `.txt` was uploaded. Merchant Center reported:

- Last updated: April 28, 2026 2:06 PM
- `Your products are updated`
- `No issues found`
- `Total updated products = 0`
- `Matched products = 0`

This strongly suggests the upload did not change product labels, but it did update the source file state. No further Merchant Center upload should be attempted until the owner reviews and approves the corrected clean-subset CSV and upload format.

## Data Contract

The clean-subset builder must output these files:

1. `google_shopping_us_clean_subset_paid_eligible.csv`
2. `google_shopping_excluded_products_with_reasons.csv`
3. `google_shopping_fix_before_paid.csv`
4. `google_ads_paused_standard_shopping_build_plan.md`

Canonical columns for the master eligibility table:

```text
shopify_product_id,
shopify_variant_id,
sku,
gtin_or_barcode,
merchant_center_item_id,
title,
product_url,
price,
cost,
gross_margin_amount,
gross_margin_percent,
max_marketing_allowed,
max_cac,
collection,
product_family,
image_url,
merchant_center_status,
merchant_center_destination,
merchant_center_issue_count,
merchant_center_issues,
image_status,
price_status,
availability_status,
shipping_policy_status,
return_policy_status,
pdp_status,
market,
custom_label_0,
custom_label_1,
custom_label_2,
custom_label_3,
custom_label_4,
paid_eligible,
fix_before_paid,
exclusion_reason
```

Use `NEEDS_DATA` for missing evidence. Missing evidence fails paid eligibility.

## Hard Gates

Set `paid_eligible = false` if any are true:

- cost is missing
- gross margin is unknown
- SKU is missing
- GTIN/barcode is missing, unless valid identifier handling is documented for that exact item
- Merchant Center status is `Limited`, `Not approved`, `Disapproved`, or `Under review`
- Merchant Center has any unresolved issue bucket for the item
- image is missing, too small, unsupported, unprocessed, or invalid
- price does not match the landing page
- availability does not match the landing page
- US shipping policy is missing or invalid
- return policy is missing or invalid
- product is not available in the US market
- PDP has recurring/subscription/deferred-payment confusion
- PDP has unsupported trust/review claims
- PDP has blank or contradictory delivery estimate
- PDP has conflicting shipping/customs/returns language
- PDP has broken size guide, broken add-to-cart, or unclear variant selection
- product is low-AOV and unlikely to support a profitable multi-item order
- product belongs to weak/empty first-test collections such as Maternity or Couples
- product is international/localized-only

## Prioritization

Among products that pass hard gates, prioritize:

- high-AOV matching-set products
- Mommy & Me sets
- Family Matching sets
- pajama sets
- swimsuit sets
- dresses only when margin and PDP are clean
- products likely to produce multi-item orders

Use the guardrail:

- Current AOV baseline: `$63.25`
- Max CAC: `$9.49`
- Required ROAS: `6.67`
- Product-level max marketing spend: `price * 0.15`

## Orchestration Plan

### Phase 0 - Freeze Writes

Status: active.

- No further Merchant Center upload.
- No Shopify feed-label/metafield write.
- No Google Ads campaign creation.
- No Google Ads recommendations.
- No Google Ads budget or campaign status changes.

### Phase 1 - Build Read-Only Candidate Workspace

Owner: local data agent.

Implemented local generator:

- `ops/scripts/build_google_shopping_us_clean_subset.py`
- Test: `ops/tests/test_google_shopping_us_clean_subset.py`
- Default output directory: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28-google-shopping-us-clean-subset_REVIEW_ONLY/`

Implemented local evidence converter:

- `ops/scripts/build_google_shopping_local_evidence.py`
- Test: `ops/tests/test_google_shopping_local_evidence.py`
- Outputs:
  - `merchant_center_diagnostics_evidence.csv`
  - `pdp_evidence.csv`
  - `local_evidence_build_summary.json`
- Source limits:
  - Merchant Center source is an issue reconciliation export, not a full approval diagnostics export.
  - Products absent from that export remain `NEEDS_DATA`, not approved.
  - PDP source is an accessibility audit only; accessible pages remain `NEEDS_DATA` until full PDP Shopping QA is complete.

Implemented current API/PDP QA tooling:

- `ops/scripts/export_merchant_center_api_diagnostics.py`
- `ops/scripts/audit_google_shopping_pdp_readiness.py`
- Tests:
  - `ops/tests/test_merchant_center_api_diagnostics.py`
  - `ops/tests/test_google_shopping_pdp_readiness.py`
- Merchant Center API attempt:
  - Merchant API `products.list`: blocked by `403 PERMISSION_DENIED` / insufficient authentication scopes.
  - Content API `productstatuses.list`: blocked by `403 PERMISSION_DENIED` / insufficient authentication scopes.
  - Evidence rows from current API pull: `0`.
- Browser-context PDP QA:
  - Candidate products audited: `83`.
  - Candidate variant rows covered: `1,383`.
  - PDP pass products: `0`.
  - PDP fail products: `83`.
  - Top blockers: checkout-only/blank delivery estimate, recurring/deferred purchase text, unsupported guarantee/trust text, plus two 404 product pages.

Inputs:

- Fresh Shopify active variant export with cost, SKU, barcode, inventory, URL, image, product family, and market availability.
- Merchant Center item diagnostics export or browser/API readback for US Shopping ads eligibility.
- Public PDP browser checks for candidate products.

Required local builder behavior:

- Work at variant level.
- Generate `merchant_center_item_id = shopify_US_<product_id>_<variant_id>`.
- Treat `NEEDS_DATA` as not eligible.
- Preserve every exclusion reason.
- Split outputs into paid-eligible, fix-before-paid, and excluded files.
- Fail closed when Merchant Center or PDP evidence files are absent.

### Phase 2 - Merchant Center Verification

Owner: browser/Merchant Center agent.

Read-only checks:

- Confirm supplemental source parser/format before upload.
- Confirm current item IDs and US feed label.
- Export or capture Merchant Center status, destination, issues, image status, price status, availability status, US shipping, and return policy.
- Confirm whether the April 28 zero-match upload needs rollback/correction. Any rollback is also a write and needs explicit owner approval.

Required output:

- Merchant Center evidence table joined to `merchant_center_item_id`.
- No upload.

### Phase 3 - PDP Verification

Owner: browser/storefront agent.

For each proposed candidate:

- Open the public US product URL.
- Verify image visibility, price clarity, variant clarity, add-to-cart, no subscription/deferred-payment confusion, no trust/legal conflicts, no blank/contradictory delivery estimate, and no shipping/returns conflict.
- Record `pdp_status = PASS`, `FAIL`, or `NEEDS_DATA`.
- Record concrete failure reasons.

Required output:

- PDP evidence columns joined to the eligibility table.
- Screenshots for any product marked `PASS`, or a text/DOM proof bundle that can be reviewed.

### Phase 4 - Owner Review

Owner: operator.

Review these files before any write:

- `google_shopping_us_clean_subset_paid_eligible.csv`
- `google_shopping_excluded_products_with_reasons.csv`
- `google_shopping_fix_before_paid.csv`
- `google_ads_paused_standard_shopping_build_plan.md`

Approval must explicitly say whether to:

- upload full-label supplemental feed;
- create a new supplemental source vs replace `supplemental_feed_pilot.txt`;
- create the paused Google Ads Standard Shopping campaign;
- leave all ads/campaigns uncreated and use the build plan only.

### Phase 5 - Feed Label Upload, Only After Approval

Preferred upload:

- Google Merchant Center supplemental source.
- Match by `id`.
- Update only `custom_label_0..custom_label_4`.
- Do not overwrite title, price, image, availability, shipping, or other core data.

Format validation before upload:

- Confirm parser expectations against the existing source.
- Confirm header names exactly: `id,custom_label_0,custom_label_1,custom_label_2,custom_label_3,custom_label_4`.
- Confirm row count equals owner-approved clean-subset label table.
- Confirm sampled IDs exist in Merchant Center before upload.

### Phase 6 - Paused Campaign Build, Only After Approval

Campaign draft:

- Name: `US | Standard Shopping | Clean Subset | Paid Eligible | Test`
- Type: Shopping
- Subtype: Standard Shopping only
- Merchant Center: Dresslikemommy / `124884876`
- Country: United States
- Inventory filter:
  - `custom_label_0 = paid_eligible`
  - `custom_label_4 = us_test_ready`
- Status: Paused
- Budget: tiny test placeholder only, campaign remains paused
- Bidding: conservative Manual CPC or equivalent low-risk bidding
- Product groups:
  - subdivide by `custom_label_2`
  - then subdivide by `custom_label_1`
  - exclude all other products

Proof required:

- campaign name
- paused status
- United States only
- Shopping / Standard Shopping
- inventory filter
- included product groups
- excluded product groups
- budget
- bidding
- conversion goal selected
- confirmation that no campaign is enabled

## Launch Decision Rules

- If fewer than 20 clean products pass: `LAUNCH_BLOCKED`.
- If products pass but campaign/tracking/PDP fixes still need review: `READY_FOR_PAUSED_BUILDOUT`.
- Only use `READY_FOR_LIMITED_TEST` if measurement, feed status, margin, PDP, shipping, and return policy all pass.

Current decision from local evidence only:

`LAUNCH_BLOCKED`

Reason:

- Current Merchant Center API diagnostics are blocked by insufficient Google OAuth scopes, so all current Merchant Center approval/destination/policy evidence remains `NEEDS_DATA`.
- Full browser-context PDP QA was joined for `1,383` locally viable candidate variant rows, and all failed at least one PDP hard gate.
- SKU and barcode/GTIN gaps remain large.
- The label schema must be rebuilt before any correct feed upload.
- The April 28 supplemental source state needs read-only review before any further feed action.

## Subagent Workstreams

1. Shopify/export agent:
   - verify local cost, SKU, GTIN, inventory, family, URL, and image fields;
   - build the first candidate table;
   - never write to Shopify.

2. Merchant Center/browser agent:
   - read item diagnostics and supplemental-source state;
   - verify item IDs and parser format;
   - never upload without owner approval.

3. PDP/browser agent:
   - verify landing pages for candidate products;
   - record hard PDP blocker reasons;
   - never modify theme/product data.

4. Google Ads agent:
   - draft or create only a paused Standard Shopping campaign after owner approval;
   - never create PMax or all-products Shopping;
   - never enable a campaign.

## Subagent Review Consensus

Three read-only subagents audited the repo evidence before this plan was finalized.

Shopify/export audit:

- Existing scripts already generate cost sync, paid eligibility, and supplemental feed files.
- The current post-sync `7,227` count is cost/inventory eligible only, not Google Shopping ready.
- Current label output diverges from the requested schema:
  - current `custom_label_0` is margin tier;
  - current `custom_label_4` is paid status;
  - requested `custom_label_0` must become paid eligibility and `custom_label_4` must become US test status.
- A new read-only clean-subset generator is required before any upload.

Merchant Center/feed-history audit:

- Historical supplemental feed source `10626787326` / `supplemental_feed_pilot.txt` previously matched Shopify-style IDs.
- Prior full March upload succeeded with `3,348` submitted rows, `2,722` matched rows, and `626` stale/unmatched rows.
- Later refresh evidence reduced the known unmatched set to about `343`.
- The April 28 tab-delimited paid-status-only upload attempt reported `0` updated and `0` matched products, so it must not be treated as a successful label update.
- Safest next step is owner-reviewed corrected CSV first. Any rollback or correction upload is also a write and needs explicit approval.

PDP/readiness audit:

- No repo artifact proves a final `READY_FOR_PAID` product set.
- Existing storefront and accessibility checks are useful, but they are not a per-product PDP pass/fail join against Merchant Center diagnostics.
- Missing local piece: a product/variant PDP verifier that records subscription/deferred-payment confusion, trust claims, shipping/returns/customs conflicts, delivery estimate, size guide, variant clarity, and add-to-cart/cart behavior.
- The current campaign gate remains `LAUNCH_BLOCKED` until Merchant Center item status and PDP evidence are joined into the clean-subset table.
