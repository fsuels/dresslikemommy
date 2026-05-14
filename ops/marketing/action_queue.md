# Marketing Action Queue

Last reconciled: 2026-05-14 07:52 EDT

Legend:
- `GREEN`: safe to execute now inside current repo/local/read-only scope.
- `YELLOW`: prepare or read back, but do not write externally.
- `RED`: do not execute until the named gate is cleared.
- `DONE`: completed in this command-layer pass.

| Priority | Status | Action | Owner agent | Gate | Evidence/source |
|---|---|---|---|---|---|
| P0 | DONE | Run read-only live reconciliation goal for Google Ads GB/CA/AU, Standard Shopping, Pinterest access, Merchant/Pinterest blockers, and ROAS decision state | `head_of_growth` with operators | Completed with no external writes | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/LIVE_RECONCILIATION_REPORT.md` |
| P0 | GREEN | Run Day 1 sales/ROAS monitor and GB/CA/AU same-day zero-impression diagnosis; because T+24 already showed zero impressions in saved evidence, evaluate high-buyer-intent long-tail exact/phrase candidates, auction-entry constraints, ad/RSA status, Quality Score gaps, and landing/product fit now | `google_ads_operator` + `analytics_roas_operator` + `head_of_growth` | `spend_authorization.md` is `APPROVED_ACTIVE`, but no bid/budget/status/keyword/ad write until fresh readback, reviewer pass, exact row scope, caps, expert playbook, high-intent/low-waste economics, and anti-cannibalization checks are satisfied; CA/AU search-term pages must be free of stale `human hair wigs` filter before negative decisions | `current_marketing_state.md`; `campaign_explorer.json`; `spend_authorization.md`; `expert_growth_playbook_2026.md` |
| P0 | GREEN | Build a GB/CA/AU high-buyer-intent long-tail candidate map for immediate bounded testing: role + product, occasion + buyer intent, style + role, country vocabulary, negatives, expected CPC/CPA risk, landing fit, and no-cannibalization owner | `google_ads_operator` + `landing_cro_operator` | Repo-local/read-only candidate work is allowed now; live keyword/ad/bid/status changes require green-gated bounded authority, fresh readback, reviewer pass, and after-state readback | `expert_growth_playbook_2026.md`; `campaign_explorer.json` |
| P0 | RED | Restore controllable authenticated Pinterest Ads Manager access and perform before-write readbacks for approved paused US draft path | `pinterest_operator` | Current controllable browser is unauthenticated; stop on login/CAPTCHA/account/billing/policy prompts; no writes until access and approval/readbacks are clean | `PROB-2026-05-08-PINTEREST-EVENT-QUALITY` |
| P1 | DONE | Reconcile Standard Shopping live state, spend, product scope, and conversion data | `google_ads_operator` + `analytics_roas_operator` | Completed read-only; no Standard Shopping write justified | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/standard-shopping-readback/raw/` |
| P1 | DONE | Refresh compact daily scorecard after live readbacks | `analytics_roas_operator` | Completed from saved Ads/Merchant/Pinterest evidence plus public/local landing readbacks; no platform writes | `daily_scorecard.md` |
| P1 | DONE | Activate bounded spend authority | `head_of_growth` | Owner approved bounded spend within set limits and `650% ROAS` goal; `spend_authorization.md` now `APPROVED_ACTIVE` | `spend_authorization.md` |
| P1 | YELLOW | Obtain current exact Merchant US/es age_group export/readback before any repair decision | `merchant_feed_operator` | Read-only only; stale May 8 CSV is not enough to justify repair | `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP` |
| P1 | YELLOW | Diagnose Merchant `Over capacity for Shopping ads` impact on current paid cohort and Standard Shopping serving | `merchant_feed_operator` + `google_ads_operator` | Read-only only; no product removals/source changes/capacity request without owner decision | `PROB-2026-05-14-MERCHANT-SHOPPING-ADS-CAPACITY` |
| P1 | DONE | Build active-product advertising/category map prep from public storefront/catalog readbacks and existing paid cohort, including event layers such as Father's Day using Daddy-and-Me and father-inclusive family matching products | `head_of_growth` + `merchant_feed_operator` + `google_ads_operator` | Completed read-only/local prep only; full current Admin/Merchant/Pinterest intersection remains a future readback before uploads/applies | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/ACTIVE_PRODUCT_CATEGORY_ADVERTISING_MAP_PREP.md` |
| P1 | RED | Publish scoped paid-landing vendor/source analytics sanitizer to live theme and read back GB/CA/AU paid landing source | `landing_cro_operator` / Shopify theme operator | External Shopify theme sync/push is not covered by paid-media spend authority; do not edit Shopify product/vendor data under paid-growth guardrails | `PROB-2026-05-14-PAID-LANDING-VENDOR-SOURCE-URL-LEAK` |
| P1 | RED | Repair Merchant US/es age_group source `10627981690` if a current exact readback proves it is still live | `merchant_feed_operator` | Fresh exact owner approval and before/after readbacks | `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP` |
| P1 | RED | Use ES/IT Golden Daisy rows in Google Ads | `google_ads_operator` | Native review signoff plus exact owner action-time approval | ES/IT signoff bundle |
| P2 | DONE | Review paid landing/CRO blockers from current active campaign landing URLs | `landing_cro_operator` | Public/read-only and theme-local only; no external write occurred | `blocker_board.md`; `PROB-2026-05-14-PAID-LANDING-VENDOR-SOURCE-URL-LEAK` |

## Green-Gate Requirements For Future Live Actions

A row can be treated as green for live marketing writes only when all are true:

- `spend_authorization.md` says `APPROVED_ACTIVE` or the current session contains exact action-time approval.
- The row names the exact campaign/ad group/ad/keyword/feed/source/product/surface.
- Before-state live readback is saved or summarized.
- The action is inside caps and excludes billing, conversion-goal, PMax, unresolved remarketing, Merchant feed/source/product-scope, Shopify product/price/discount/policy, and unreviewed native-language changes.
- Bid strategy, keyword quality/Quality Score or quality-column gap, ad/creative quality, landing page, product/photo fit, measurement, and sales/ROAS impact are checked where relevant.
- High-intent/low-waste economics, anti-cannibalization owner, and `expert_growth_playbook_2026.md` standard are checked where relevant.
- If an active campaign has zero impressions after 24 hours, same-day diagnosis and long-tail/auction-entry action planning are mandatory.
- After-state readback and worklog update are part of the task.
