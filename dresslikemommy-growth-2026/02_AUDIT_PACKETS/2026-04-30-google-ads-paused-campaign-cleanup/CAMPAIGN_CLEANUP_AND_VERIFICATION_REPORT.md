# 2026-04-30 Google Ads Paused Campaign Cleanup And Verification

Confidence: H for Standard Shopping edits and final paused/budget readback; M for change-history timing because Google Ads did not immediately surface every just-made edit in the visible change-history table.

## Scope

Account: `399-097-6848 dresslikemommy.com`

Measurement prerequisite: paid-value gate passed in `../2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md`.

Operator instruction: proceed with paused campaign-specific cleanup and verification. Standard Shopping is the first controlled test candidate. PMax and Remarketing remain rebuild/repair before launch.

## Non-Negotiable Safety Result

No campaign was enabled.

No budget was increased.

Final campaign-table readback still shows all 5 target campaigns paused, `$1.00/day`, `$0.00` all-time cost, `0` impressions, `0` clicks/interactions, `0.00` conversions, and `0.00` conversion value.

Evidence:
- `raw/all_campaigns_final_pause_budget_readback.txt`
- `screenshots/all_campaigns_final_pause_budget_readback.png`

## Live Edits Applied

Campaign edited: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` (`23802638621`)

All edits were made while the campaign was paused.

1. Maximize clicks CPC guardrail
   - Before: `Maximize clicks`, no visible CPC cap.
   - After: `Maximize clicks` with maximum CPC bid limit checked and value `0.25`.
   - Purpose: prevent uncapped click bidding if the paused draft is later approved for a controlled test.
   - Evidence:
     - `screenshots/standard_shopping_bidding_cpc_025_before_save.png`
     - `screenshots/standard_shopping_bidding_final_reopen_after_save.png`
     - `raw/standard_shopping_bidding_final_inputs_after_save.json`

2. Location option tightened
   - Before: `Presence or interest`.
   - After: `Presence: People in or regularly in your included locations`.
   - Purpose: avoid non-US-interest traffic for the US-only controlled Shopping test.
   - Evidence:
     - `screenshots/standard_shopping_location_options_open.png`
     - `screenshots/standard_shopping_location_presence_final_options_visible.png`

3. Product group catch-all excluded
   - Before: `Everything else in "All products"` was `Automatic`.
   - After: `Everything else in "All products"` is `Excluded`.
   - Purpose: keep spend inside the intended `us_test_ready` cohort.
   - Evidence:
     - `screenshots/standard_shopping_productgroups_before_cleanup_live.png`
     - `screenshots/standard_shopping_productgroups_after_exclude_confirm.png`

## Standard Shopping Final Controlled-Test Posture

`DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` is the only first-test candidate, but still requires explicit owner activation approval before it can run.

Current verified state:
- Status: `Paused`
- Budget: `$1.00/day`
- Campaign type: `Shopping`
- Merchant Center/CSS: `124884876 - Dresslikemommy / CSS: Google Shopping`
- Feed label: `US`
- Network: `Google Search Network`
- Location: United States, with `Presence` include option
- Bidding: `Maximize clicks` with max CPC cap `0.25`
- Product groups:
  - `us_test_ready`: `Automatic`
  - `Everything else in "All products"`: `Excluded`
- All-time cost/impressions/clicks/conversions/value: zero

## Brand Search

`DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` was verified paused at `$1.00/day` with all-time zero spend. No live Brand Search non-budget edits were applied in this pass because Standard Shopping is the first controlled-test candidate.

Still recommended before any Brand Search activation:
- Replace `Maximize conversion value` with a controlled low-CPC strategy.
- Re-open and verify advanced location option is `Presence`.
- Add brand-list enforcement if Google Ads exposes it for this campaign.
- Review campaign negatives for over-blocking brand modifiers.
- Add/verify campaign-level brand assets only after copy/supporting claims are approved.

Evidence:
- `raw/brand_search_settings_tab_live.txt`
- `screenshots/brand_search_settings_tab_live.png`
- `raw/all_campaigns_final_pause_budget_readback.txt`

## PMax And Remarketing Status

PMax and Remarketing were not launch-cleaned in this pass. They remain hold/rebuild/repair campaigns, not activation candidates.

Key launch blockers:
- `PMax: Shopping ads (United States)`: paused, `$1/day`, `No products for any locations`, Merchant Center mismatch risk from prior audit, no launch.
- `PMax: USA Google Shopping T-Shirts`: paused, `$1/day`, all asset groups paused, product scope not T-shirt-only, no launch.
- `Remarketing - Cart Abandoners & Checkout Starters`: paused, `$1/day`, ads limited by policy, audiences not eligible in prior audit, no launch.

## Decision

`STANDARD_SHOPPING_READY_FOR_OWNER_REVIEW_NOT_LAUNCH`

The paid-value gate is passed and the Standard Shopping draft is safer, but no campaign is approved to run until the owner approves the exact activation action and launch budget.
