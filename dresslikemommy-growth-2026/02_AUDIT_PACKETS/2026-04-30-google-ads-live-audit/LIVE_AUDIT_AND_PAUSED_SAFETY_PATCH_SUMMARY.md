# 2026-04-30 Google Ads Live Audit And Paused Safety Patch

Confidence: H for status/budget/spend readback; M for advanced location options because Google Ads did not expose those collapsed controls in the captured settings drawers.

## Scope

Account audited: `399-097-6848 dresslikemommy.com`

Operator visible in UI: `testhqfinds@gmail.com`

Audit packet folder:
`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-live-audit/`

Prompt source:
`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-campaign-readiness-orchestration/safe_live_audit_prompts.md`

## Non-Negotiable Result

`LAUNCH_BLOCKED` remains in force.

All five visible campaigns are paused and cannot spend right now. All-time campaign-level rows for these five campaigns showed `0` impressions, `0` clicks/interactions, `$0.00` cost, `0.00` conversions, and `0.00` conversion value.

The account-level all-time total shows historical account activity outside these five visible target campaigns; do not use account total rows as campaign spend evidence.

## Owner-Approved Paused Safety Patch Applied

Only one edit class was applied: daily budgets were reduced to `$1.00/day` placeholders while campaigns stayed paused.

| Campaign | Before | After | Status After |
|---|---:|---:|---|
| `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` | `$10.00/day` | `$1.00/day` | Paused |
| `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` | `$25.00/day` | `$1.00/day` | Paused |
| `PMax: Shopping ads (United States)` | `$2.00/day` | `$1.00/day` | Paused |
| `PMax: USA Google Shopping T-Shirts` | `$10.00/day` | `$1.00/day` | Paused |
| `Remarketing - Cart Abandoners & Checkout Starters` | `$5.00/day` | `$1.00/day` | Paused |

Final readback evidence:
- `raw/paused_budget_safety_patch_verified_current_dom.txt`
- `screenshots/budget_edit_corrected_remarketing_after_save.png`
- `screenshots/paused_budget_safety_patch_verified_current_dom.png`

No campaigns were enabled. No bidding strategies, conversion goals, product groups, audience rules, assets, ads, final URL expansion controls, negatives, or location targeting controls were changed.

## Campaign Audit Summary

| Campaign | Type | Final Budget | Bid Strategy | Key Live Findings |
|---|---|---:|---|---|
| `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` | Search | `$1.00/day` | Maximize conversion value | Google Search Network only; account-default Purchases captured in settings; 2 ad groups; 2 RSAs pending; 253 negatives shown in change history; all-time metrics are zero. |
| `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` | Shopping | `$1.00/day` | Maximize clicks | Merchant Center `124884876 - Dresslikemommy`; feed label `US`; inventory filter present; product groups show `All products`, `us_test_ready`, and `Everything else in "All products"` on Automatic CPC; URL tracking options present; all-time metrics are zero. |
| `PMax: Shopping ads (United States)` | Performance Max | `$1.00/day` | Maximize conversion value | Paused with `No products for any locations`; Merchant Center captured as `513542500 - truehairwigs`, which is a major mismatch risk; All languages; final URL expansion/text customization on; no URL options; no brand exclusions; all-time metrics are zero. |
| `PMax: USA Google Shopping T-Shirts` | Performance Max | `$1.00/day` | Maximize conversion value | Paused with all asset groups paused; Merchant Center `124884876 - Dresslikemommy`; All languages; final URL expansion/text customization on; no URL options; no brand exclusions; product view showed non-T-shirt products, so product isolation is not launch-ready; all-time metrics are zero. |
| `Remarketing - Cart Abandoners & Checkout Starters` | Display | `$1.00/day` | Maximize conversions | Account-default conversion goals; English; five responsive display ads captured as `Not eligible` / `Policy (Clickbait), Campaign is paused`; `Cart abandoners` and `Checkout starters` audiences captured as not eligible; all-time metrics are zero. |

## Change History Exports

Pre-patch and post-patch change-history screenshots/text were exported under:
- `change-history/`
- `screenshots/*changehistory*.png`

Observed April 30 and April 29 rows include campaign creation/import, pauses, keywords, negatives, inventory filter, product groups, ads, locations, and older budget changes. Google Ads did not surface the just-applied `$1/day` budget changes in campaign change history during this session, likely due UI/change-history latency. The current campaign-table DOM and screenshots are the authoritative immediate readback for the safety patch.

## Still Blocked Before Activation

- Prove purchase conversion value, currency, transaction ID, and deduplication are correct.
- Decide campaign-level conversion goals only after measurement proof.
- Verify advanced location option is `Presence` only; this was not exposed in the captured settings drawers.
- Keep PMax campaigns paused until product eligibility, product filters, final URL expansion rules, brand exclusions, audience signals, asset quality, and economics pass.
- Keep Remarketing paused until ad policy, audience eligibility, purchaser exclusions, and dynamic remarketing/feed setup are fixed.
- Keep Standard Shopping paused until `Everything else` handling, product groups, product economics/margins, and CPC control are approved.
- Keep Brand Search paused until brand keyword/negative/ad/asset strategy and controlled bidding are approved.
