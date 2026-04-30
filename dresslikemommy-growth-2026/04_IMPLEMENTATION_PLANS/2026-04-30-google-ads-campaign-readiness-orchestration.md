# Google Ads Campaign Readiness Orchestration

Date: 2026-04-30

Decision: `LAUNCH_BLOCKED`

Purpose: organize the April 30 Google Ads campaign critiques into an agent-ready implementation plan that can make every draft campaign safer while keeping all spend disabled until the final launch gates pass.

## Source Evidence

- April 30 campaign packets in `/Users/fsuels/Downloads/2026-04-30_GOOGLE_ADS_*_EVAL_PACKET_v1.md`.
- Master packet rule: audit all paused campaigns and change history before implementation; do not enable anything.
- Existing growth rules: `dresslikemommy-growth-2026/00_MASTER/MASTER_RULES.md`.
- Google Ads purchase value gate: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-ads-conversion-value-gate/google_ads_conversion_value_gate_report.md`.
- Google Shopping campaign gate: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate/campaign_gate_report.md`.
- Final launch gate: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-final-launch-gate/phase7_final_launch_gate_report.md`.
- Worklog anchor: `2026-04-29-google-ads-editor-paused-brand-search-post-shopping-negatives`.

## Evidence Reconciliation

The April 30 handoff packets are intentionally conservative and say to verify before trusting any screenshot. They also include older shared blockers such as missing paid labels and unclear purchase tracking.

The repo/worklog has newer April 29 evidence that must be treated as current unless a fresh live audit disproves it:

- `Google Shopping App Purchase` is the single primary account-level purchase action, has dynamic value evidence, and had a recent received request. This supports paused build/readback work, not activation.
- The live Merchant Center label gate passed for the clean cohort. The Shopping campaign gate read back `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible` with `780` products.
- Standard Shopping `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` was live-read as paused with `$25/day`, `Maximize clicks`, Merchant Center `124884876`, feed label `US`, and the paid-ready inventory filter.
- Brand Search `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` was posted through Google Ads Editor as paused with `$10/day`, Google Search only, Search Partners off, Display off, US/English, 2 ad groups, 12 paused brand keywords, 2 paused RSAs, and 253 campaign negatives.
- The old `Search - Brand` campaign remains removed and must not be restored.
- Final launch remains blocked: Phase 7 says only 1 of 8 gates is `YES`; website, localization, country economics, paid efficiency, and blended spend are not ready.

## Global Rules

- Do not enable, publish, restart, or unpause any campaign.
- Do not raise budgets.
- Do not switch a campaign into broad automated spend until the final launch gate passes.
- Do not use PMax for launch until Standard Shopping, measurement, feed, landing pages, product economics, and brand cannibalization controls are proven.
- Do not use unsupported ad claims: no unverified ratings, family counts, founding-year trust proof, free returns, no-customs promises, guaranteed delivery, or unsupported discounts.
- Keep Google purchase measurement aligned to the supported architecture: Shopify Google & YouTube app / `Google Shopping App Purchase` as the bidding purchase path. Do not add GTM/theme/custom-pixel Google purchase tracking.
- Every live-account edit requires before/after screenshot or export, change-history capture, and rollback note.

## Agent Orchestration

### Agent 0 - Controller

Role: own sequencing, evidence reconciliation, and final approval gates.

Inputs:
- This plan.
- `campaign_action_matrix.csv`.
- `agent_workstream_board.csv`.
- The current Google Ads safe audit exports.

Outputs:
- Updated launch gate packet.
- Exact owner approval request for one limited activation, if and only if all gates pass.

### Agent 1 - Read-Only Google Ads Audit

Role: audit the live Google Ads account without changes.

Tasks:
- Verify status, budget, bid strategy, networks, locations, location options, conversion goal, cost today, cost since creation, clicks, impressions, conversions, conversion value, ROAS, CPA/CAC, and spend ability for all five campaigns.
- Export change history from 2026-04-29 through 2026-04-30.
- Capture screenshots/exports for campaign settings, product/listing groups, ads/assets, audiences, brand exclusions, URL options, and policy diagnostics.

Stop condition:
- If any campaign can spend now, stop and escalate before doing anything else.

### Agent 2 - Paused Safety Patch

Role: make only owner-approved paused-draft safety edits after Agent 1 verifies current settings.

Allowed edits while paused:
- Reduce draft budgets to `$1/day` placeholders where the operator approves.
- Set Search campaigns to Google Search only, Search Partners off, Display off.
- Set US location option to Presence only where verified as `Presence or interest`.
- Add or verify safe URL suffixes only after confirming they do not duplicate UTMs.
- Turn PMax final URL expansion off unless an approved URL map exists.
- Add brand exclusions to PMax only after verifying the brand entity/list is correct.
- Keep or add purchaser exclusions to remarketing if missing.

Forbidden edits:
- Any enable/unpause/publish action.
- Any budget increase.
- Any conversion-goal mutation without a separate measurement approval.
- Any bulk negative deletion.
- Any broad/product-expanding PMax edit.

### Agent 3 - Feed, Product, and Economics Gate

Role: prove the product set is actually paid-ready.

Tasks:
- Confirm Merchant Center account/domain and label readback for the Standard Shopping cohort.
- Export the exact included offer IDs/item groups for Standard Shopping and any PMax campaigns.
- Verify every included product is approved, in stock, US eligible, known-margin, and not `FIX_BEFORE_PAID`, `EXCLUDE_PAID`, limited, not approved, or unknown margin.
- Produce a T-shirt-specific AOV/margin report before allowing the T-shirt PMax campaign to remain in any launch plan.

Decision rule:
- Standard Shopping can stay as the first paid structure only if the exact 780-row cohort still reads back clean.
- PMax T-Shirts remains `REJECT_FOR_LAUNCH` unless T-shirt economics independently prove ROAS >= 6.67 and CAC <= AOV x 0.15.

### Agent 4 - Website and Landing-Page Gate

Role: build a paid-traffic landing-page allowlist.

Tasks:
- Audit the homepage and every landing page used by ads, sitelinks, product groups, and final URL expansion.
- Mark each URL `READY_FOR_PAID`, `FIX_BEFORE_PAID`, or `EXCLUDE_FROM_PAID`.
- Confirm pages are fast enough, policy-safe, and do not contain unsupported claims.

Decision rule:
- Brand Search may use homepage only until sitelinks pass.
- Shopping may send traffic only to product/collection pages that pass.
- PMax final URL expansion remains off until the allowlist exists.

### Agent 5 - Measurement and Attribution Gate

Role: prove conversion value and attribution are usable for bidding.

Tasks:
- Re-run the Google Ads conversion-value gate.
- Capture an end-to-end purchase/payment proof showing value, currency, and transaction ID behavior without duplicate purchase values.
- Verify `Google Shopping App Purchase` remains the only primary account-level purchase action.
- Confirm add-to-cart and begin-checkout are diagnostic only, not bidding goals.
- Document enhanced conversions state and consent implications for Customer Match/remarketing.

Decision rule:
- Tracking health can allow paused buildout.
- Activation still requires final gate proof and explicit owner approval.

### Agent 6 - Creative and Asset Buildout

Role: create compliant assets that can be applied while paused.

Tasks:
- Brand Search: keep compliant brand-only RSA copy; do not add unsupported proof claims. Add only READY_FOR_PAID sitelinks.
- Standard Shopping: no ad copy, but verify merchant promotions/price assets only when margins and offer accuracy are proven.
- PMax US Shopping: draft asset groups only for approved product cohorts; include brand exclusion and final URL guardrails.
- PMax T-Shirts: draft assets only after T-shirt economics pass.
- Remarketing: replace clickbait RDAs with literal, product-led cart/checkout reminder copy; submit for policy review only while campaign remains paused.

Decision rule:
- Ads can be fixed for eligibility while paused.
- Creative approval is not launch approval.

### Agent 7 - Final Gate and Limited Activation Proposal

Role: decide whether a small owner-approved launch test is possible.

Tasks:
- Rebuild the Phase 7 launch gate after Agents 1-6 finish.
- If all gates pass, propose exactly one limited test:
  - Preferred first test: Standard Shopping clean cohort or Brand Search, not PMax.
  - Daily budget must fit the 15% revenue cap after all other platform spend.
  - Bid strategy must be controlled and rollback-ready.
- Create rollback steps and monitor thresholds before asking for activation approval.

Decision rule:
- If any gate is not `YES`, keep `LAUNCH_BLOCKED`.

## Campaign Decisions

### Brand Search

Current best posture: keep paused, improve safety/readback, do not enable.

Recommended paused-draft configuration:
- Campaign: `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`.
- Status: paused.
- Budget: `$1/day` placeholder after audit and owner approval; current posted budget is `$10/day`.
- Network: Google Search only; Search Partners off; Display off.
- Location: United States, Presence only.
- Language: English.
- Keywords: exact/phrase brand variants only.
- Bid strategy before data: Manual CPC or Max clicks with strict CPC cap; avoid Maximize conversion value/tROAS until launch gates pass.
- Final URL: homepage only until sitelinks are `READY_FOR_PAID`.
- Negatives: export and audit; do not bulk-delete. Verify match types before accepting claims about overblocking.

Reject:
- Non-brand terms, broad match, competitor conquesting, coupon/support keywords, unsupported ad claims, and renaming that removes the `PAUSED` safety signal.

### Standard Shopping

Current best posture: highest-priority paid draft, still paused.

Recommended paused-draft configuration:
- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`.
- Status: paused.
- Budget: `$1/day` placeholder after audit and owner approval; current live-read budget was `$25/day`.
- Type: Standard Shopping only.
- Merchant Center: Dress Like Mommy account `124884876` unless fresh audit disproves.
- Inventory filter: `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible`.
- Product groups: no All Products catch-all serving; subdivide by paid-ready label, product family, margin tier, AOV tier, or item group after readback.
- Bidding: no uncapped Maximize clicks at launch. Use controlled CPC until value data supports smarter bidding.
- Networks: if Search Partners is exposed and enabled, disable only after live audit confirms the setting and rollback path.

Reject:
- Running the `$25/day` draft as-is, All Products inclusion, unknown-margin products, broad product expansion, and budget increases.

### PMax Shopping Ads United States

Current best posture: hold out of launch sequence.

Recommended paused-draft configuration:
- Status: paused.
- Budget: `$1/day` placeholder after audit and owner approval; current visible budget in packet was `$2/day`.
- Final URL expansion: off unless a paid URL allowlist exists.
- Product scope: no all-products listing group; only approved, known-margin, paid-ready products after feed and landing gates.
- Brand controls: exclude Dress Like Mommy brand demand once Brand Search is safe.
- Audience signals/assets: build only after product scope and consent-safe lists are verified.

Reject:
- Any launch now, any broad/all-products PMax, any budget increase for learning, and any tROAS/Maximize conversion value launch without final measurement and product gates.

### PMax USA Google Shopping T-Shirts

Current best posture: reject from launch plan unless T-shirt economics pass.

Recommended paused-draft configuration:
- Status: paused.
- Budget: `$1/day` placeholder after audit and owner approval; current visible budget in packet was `$10/day`.
- Product scope: T-shirts only, but only if exact item IDs, margins, AOV, landing pages, and feed status pass.
- Asset copy: T-shirt-specific only; no generic dress/matching-outfit copy.
- Overlap: must not overlap Standard Shopping or PMax US Shopping.

Reject:
- Launching at `$10/day`, launching on assumed T-shirt margin, generic mixed product groups, and using PMax before the main clean Shopping cohort proves paid traffic can work.

### Remarketing

Current best posture: policy/audience repair only; no launch.

Recommended paused-draft configuration:
- Campaign: `Remarketing - Cart Abandoners & Checkout Starters`.
- Status: paused.
- Budget: `$1/day` placeholder after audit and owner approval, or keep `$5/day` maximum while paused.
- Ads: rewrite all clickbait-limited RDAs into literal, product-led reminders.
- Audiences: audit source, size, membership duration, consent, and exclusions before changing list logic.
- Exclusions: past purchasers/recent converters must be excluded before launch.
- Location: US Presence only.
- Delivery controls: frequency caps and content/placement exclusions where supported.

Reject:
- Enabling with policy-limited ads, optimized targeting/audience expansion as launch default, EU/UK remarketing without consent review, raising budget, and using account-default goals if they include non-purchase bidding signals.

## Final Launch Gates

All must be `YES` before activation:

1. Live Google Ads audit proves every campaign is paused, has expected settings, and has `$0` spend/cost since creation.
2. Change history from 2026-04-29 through 2026-04-30 is exported and reconciled.
3. Purchase conversion records value, currency, and transaction ID without duplicate bidding values.
4. `Google Shopping App Purchase` remains the only primary account-level purchase action.
5. Exact campaign landing pages are `READY_FOR_PAID`.
6. Exact included offer IDs are approved, in stock, US eligible, known-margin, and paid-ready.
7. Actual all-platform spend is known, and the planned budget fits the 15% revenue cap.
8. Country economics and paid efficiency can support ROAS >= 6.67 and CAC <= AOV x 0.15.
9. No campaign includes unsupported claims, broad products, or unapproved URL expansion.
10. Owner approves the exact campaign, budget, bid strategy, date/time, monitor plan, and rollback.

## Activation Preference

If every gate passes, the safest first activation is not PMax.

Preferred sequence:

1. Brand Search limited test or Standard Shopping clean cohort.
2. Standard Shopping clean cohort if Brand Search remains too cannibalization-sensitive.
3. Remarketing only after policy, audience eligibility, exclusions, and consent pass.
4. PMax only after Standard Shopping proves product economics and tracking.
5. T-shirt PMax last, and only if T-shirt unit economics beat the CAC/ROAS rules.

## Rollback Standard

Before any activation:

- Export current settings and change history.
- Record campaign IDs, budget, bid strategy, location option, networks, product filters, URL options, and conversion goal.
- Define stop-loss thresholds:
  - any spend outside expected campaign,
  - any campaign cost above approved daily cap,
  - any non-US traffic,
  - any disapproved/limited ads becoming the only serving ads,
  - any conversion value anomaly or duplicate purchase event.
- Rollback action: pause the campaign, revert changed settings from the export, and append a dated note to `ops/AGENT_WORKLOG.md`.
