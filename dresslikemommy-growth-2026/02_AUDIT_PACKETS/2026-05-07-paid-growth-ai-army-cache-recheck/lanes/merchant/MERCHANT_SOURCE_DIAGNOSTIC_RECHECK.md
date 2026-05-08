# Merchant Source Diagnostic Recheck

Generated: 2026-05-07 23:05 EDT / 2026-05-08 UTC

Lane: Merchant / Google & YouTube source refresh and paid-cohort diagnostics.

Mode: read-only/local reconciliation only. No Merchant upload, source sync/refresh click, Shopify product-data edit, Google & YouTube publication toggle, ads/budget/bid/status/conversion change, product-scope change, product-group change, or feed-label change was made.

## Outcome

Status: `NOT_CLEARED`.

The latest safe readbacks still point to Merchant / Google & YouTube source propagation as the blocker, not missing Shopify `age_group` data.

Key current facts:

- Shopify paid-cohort ProductVariant `mm-google-shopping.age_group` remains correct for all `780` paid variants.
- Fresh dry-run planned `0` Shopify updates and skipped `780` rows as `already_correct`.
- Sample product `7227254276193` remains `ACTIVE`, Online Store published, Google & YouTube published, with positive prices in dry-run.
- Merchant US/en sample row `shopify_US_7227254276193_41871113158753` still shows source `Shopify App API`, source ID `10627623003`, and US/en source timestamp `2026-05-07T14:14:02+00:00`.
- The sample US/en Merchant source timestamp is still older than the Shopify variant age_group repair timestamp `2026-05-07T17:12:10Z`.
- Merchant Diagnostics page text captured fresh at `2026-05-07T23:05:20` showed `Last updated at 10:53 PM May 7, 2026` and still included `Missing age group`.
- Full API product-issues export is still blocked by local Google OAuth scopes: Merchant API and Content API both returned `403 PERMISSION_DENIED`.

## Evidence Reconciled

Prior evidence packets reviewed:

- `2026-05-07-merchant-feed-refresh-age-group-recheck/MERCHANT_FEED_REFRESH_AGE_GROUP_RECHECK.md`
- `2026-05-07-merchant-source-refresh-readonly-review/MERCHANT_SOURCE_REFRESH_READONLY_REVIEW.md`
- `2026-05-07-merchant-source-refresh-action/MERCHANT_SOURCE_REFRESH_ACTION_REPORT.md`
- `2026-05-07-paid-growth-parallel-infra-sprint/merchant-source-recheck/MERCHANT_SOURCE_RECHECK_SUBAGENT_REPORT.md`
- `2026-05-07-paid-growth-continuation-readbacks/lanes/merchant/MERCHANT_READBACK.md`
- Current lane board: `2026-05-07-paid-growth-ai-army-cache-recheck/LANE_BOARD.md`

Prior state confirmed:

- Supplemental Merchant age_group upload was accepted on 2026-05-06, but diagnostics did not clear.
- Shopify-side variant age_group repair was completed on 2026-05-07 and verified across `780` paid-cohort variants.
- Merchant diagnostics refreshed at `1:15 PM May 7, 2026`, but paid-cohort US/en `Missing age group` stayed at `754` with `0` improvement.
- Read-only source review found the US `Shopify App API` source still `Needs update`.
- One owner-approved single-product Google & YouTube unpublish/republish probe was already executed for product `7227254276193`; final publication was restored.
- Later readbacks still saw the same old US/en source timestamp `2026-05-07T14:14:02+00:00`.

## Fresh Readbacks In This Lane

### Shopify age_group dry-run

Command:

```bash
python3 ops/scripts/repair_paid_cohort_variant_age_group.py --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/merchant/shopify-age-group-dry-run
```

Artifacts:

- `shopify-age-group-dry-run/summary.json`
- `shopify-age-group-dry-run/planned_variant_age_group_updates.csv`

Result:

- `execute=false`
- Target paid variant rows: `780`
- Planned updates: `0`
- Skipped rows: `780`
- Reason counts: `already_correct=780`

Interpretation: do not redo Shopify ProductVariant age_group edits.

### Google & YouTube publication dry-run

Command:

```bash
python3 ops/scripts/google_publication_republish_probe.py --handle mommy-and-me-matching-yellow-sleeveless-maxi-dress-vibrant-summer-beach-dress-for-mother-daughter --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/merchant/google-publication-sample-dry-run
```

Artifacts:

- `google-publication-sample-dry-run/summary.json`
- `google-publication-sample-dry-run/probe_state.csv`

Result:

- `execute=false`
- Product `7227254276193`
- Product status `ACTIVE`
- Online Store published `true`
- Google & YouTube published `true`
- Storefront URL present `true`
- All prices positive `true`

Interpretation: the prior approved toggle appears restored correctly. Do not repeat the toggle as a blind refresh tactic.

### Merchant browser source timestamp readback

Command:

```bash
python3 ops/scripts/check_merchant_center_clean_labels_live.py --account 124884876 --cdp-port 9222 --sample-offer-id shopify_US_7227254276193_41871113158753 --expected-labels-csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-merchant-clean-label-upload/upload_matched_full_clean_labels_with_age_group.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/merchant/browser-source-readback
```

Artifact:

- `browser-source-readback/merchant_exact_label_readback_refresh_check.json`

Result:

- Gate status: `PASS_CAMPAIGN_FILTER_LABELS_VISIBLE`
- Full label gate: `PASS_ALL_EXPECTED_LABELS_VISIBLE`
- US/en sample source: `Shopify App API`
- Source ID: `10627623003`
- Last updated UTC: `2026-05-07T14:14:02+00:00`
- Paid labels still visible:
  - `custom_label_0=paid_eligible`
  - `custom_label_1=margin_medium`
  - `custom_label_2=swimsuits`
  - `custom_label_3=aov_medium`
  - `custom_label_4=us_test_ready`
- Observed sample label mismatches: none

Important nuance: the sample has newer non-US or localized Merchant rows, but those rows do not carry the paid US labels and do not resolve the US/en paid-cohort age_group propagation issue.

### Merchant diagnostics browser text readback

Command: dedicated read-only CDP text capture of Merchant Diagnostics page for account `124884876`.

Artifacts:

- `diagnostics-browser-readback/diagnostics_page_summary.json`
- `diagnostics-browser-readback/diagnostics_page_text.txt`

Result:

- Capture generated at `2026-05-07T23:05:20`
- Visible diagnostics timestamp: `Last updated at 10:53 PM May 7, 2026`
- Visible page text still included `Missing age group`
- Visible page text also included `Missing local inventory data`

Interpretation: this is not a full item-level product-issues export, so it does not quantify the current paid-cohort count. It does show the diagnostics UI still has the age_group issue after a very fresh platform refresh.

Dropshipping note: `Missing local inventory data` is a Merchant platform diagnostic label for products in physical stores. Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory. The owner explicitly clarified this should be treated as a platform/program mismatch, not a product-data mistake. Do not create local inventory feeds, physical-store/store-pickup claims, warehouse claims, local stock claims, or guaranteed on-hand inventory claims to clear it. If this row matters, the next safe read-only question is whether any Local Inventory Ads / physical-store pickup program or setting is enabled by mistake; changing that would need a separate explicit approval.

### Merchant API product-issues export attempt

Command:

```bash
python3 ops/scripts/export_merchant_center_api_diagnostics.py --merchant-id 124884876 --input-eligibility dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-06-live-visual-qa-merchant-age-group-gate/paid_cohort_age_group_after_patch_rows.csv --output-dir dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-ai-army-cache-recheck/lanes/merchant/api-product-issues
```

Artifacts:

- `api-product-issues/merchant_center_api_diagnostics_summary.json`
- `api-product-issues/merchant_center_api_diagnostics_evidence.csv`
- `api-product-issues/merchant_center_api_diagnostics_raw.jsonl`

Result:

- Current variant rows scanned from input: `780`
- Merchant evidence rows: `0`
- Merchant API `products.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes
- Content API `productstatuses.list`: `403 PERMISSION_DENIED`, insufficient authentication scopes

Interpretation: exact current item-level product-issues count remains blocked by local Google OAuth scopes. The blocker is credential scope, not proof that issues are gone.

## Duplicate Fixes To Avoid

Do not repeat these fixes/actions without fresh evidence and explicit owner approval:

- Do not rerun Shopify ProductVariant age_group writes. Current dry-run still says `780 already_correct`.
- Do not upload another Merchant supplemental age_group file as a blind retry.
- Do not edit Shopify product titles, descriptions, status, publications, prices, inventory, tags, options, images, feed labels, or unrelated metafields for this issue.
- Do not repeat the Google & YouTube unpublish/republish toggle immediately. It was already executed once for product `7227254276193` and final publication state was restored.
- Do not click Merchant source sync/refresh, Shopify Google & YouTube app sync, source update, upload, save, apply, or publish controls from this lane.
- Do not change Google Ads or Pinterest campaigns, budgets, bids, status, product scope, product groups, feed labels, pixels, or conversion goals.

## Exact Next Safe Path

First, continue read-only:

1. Re-run the Merchant browser source timestamp sample for `shopify_US_7227254276193_41871113158753`.
2. Re-run a Merchant diagnostics/product-issues readback if a browser export or properly scoped Google API token is available.
3. Re-run the Shopify publication/age_group dry-runs only as verification, not as writes.

Success gate:

- The US/en source timestamp for source `10627623003` advances beyond `2026-05-07T17:12:10Z`, and/or
- current paid-cohort US/en `Missing age group` materially drops from the prior known `754`.

If the source timestamp remains stale and a safe official app/source refresh control is found, request a new approval gate before any click:

`APPROVE GOOGLE & YOUTUBE US FEED SOURCE REFRESH REVIEW: READ BACK SHOPIFY GOOGLE & YOUTUBE CHANNEL SYNC STATUS, MERCHANT US SHOPIFY APP API SOURCE DETAILS, AND SAMPLE ITEM API TIMESTAMPS FIRST; ATTEMPT ONLY A SAFE OFFICIAL APP RESYNC/REFRESH IF AVAILABLE; NO PRODUCT DATA EDITS, FEED LABEL CHANGES, SUPPLEMENTAL UPLOADS, ADS, CAMPAIGNS, BUDGETS, BIDS, PRODUCT SCOPE, PRODUCT GROUP, PIXEL, OR CONVERSION-GOAL CHANGES.`

If no official refresh exists, do not infer permission to repeat the publication toggle. A second toggle or broader product/source action needs a separate, exact, action-time approval and a just-in-time pre-readback.

## Guardrails Preserved

No changes were made to:

- Merchant Center sources, product data, uploads, feed labels, supplemental feeds, source settings, or sync/refresh state.
- Shopify product data, variant data, publications, pricing, inventory, product status, tags, options, images, or metafields.
- Google & YouTube publication state.
- Google Ads, Pinterest, GA4/GTM, pixels, campaigns, budgets, bids, statuses, conversion goals, product scope, product groups, or PMax/Standard Shopping/Remarketing/Brand Search surfaces.
- Shipping rates, Markets, checkout, payments, or orders.

Because this was a subagent lane with the explicit instruction to write only under `.../lanes/merchant/`, no `ops/AGENT_WORKLOG.md`, `ops/AGENT_COORDINATION.md`, or `AGENTS.md` edits were made by this lane.
