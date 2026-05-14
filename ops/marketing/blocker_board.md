# Marketing Blocker Board

Last reconciled: 2026-05-14 06:05 EDT
Detailed source of truth remains `ops/PROBLEM_TRACKER.md`.

| Priority | Blocker | Current compact status | Next unblock action |
|---|---|---|---|
| P0 | Pinterest Ads Manager controllable access | `LIVE_VERIFIED`: current controllable browser lands on public Pinterest Ads login/sign-up page; Create control not found; no Pinterest write occurred | Restore authenticated controllable Pinterest Ads Manager access for advertiser `549756244483`, then read back before any paused draft write |
| P0 | Fresh GB/CA/AU performance and search terms | `LIVE_VERIFIED`: GB/CA/AU are enabled/eligible at approved scope but yesterday still has `0` cost/clicks/impressions/conversions/value. GB search-term route is readable but empty; CA/AU are blocked by stale `Keyword: "human hair wigs"` filter | Continue monitor after data appears; make no negative/pause/scale/write decision from current data |
| P1 | Standing bounded spend authority | Proposed but not approved | Owner approval required; keep status `PENDING_OWNER_APPROVAL` until explicit approval |
| P1 | Merchant US/es age_group | `LIVE_VERIFIED` samples no longer reproduce Missing age_group; old May 8 CSV still shows the old `625` IDs but is stale/superseded for current action | Obtain current exact US/es export/readback before deciding solved vs repair-needed; do not request repair approval from stale export alone |
| P1 | Merchant Shopping Ads capacity | `LIVE_VERIFIED`: Merchant prioritized fixes page updated `3:09 AM May 14, 2026` shows `Over capacity for Shopping ads (outside of CSS program)` / `73.3K products (21%)` | Diagnose current paid-cohort and Standard Shopping impact read-only; no product removals/source changes/capacity request without owner decision |
| P1 | Active paid Search landing supplier/source URL leak | `LIVE_VERIFIED_LOCAL_FIX_READY`: public GB/CA/AU paid landing source exposed `detail.1688.com` in a related product `data-analytics-vendor`; local theme sanitizer now emits `dresslikemommy.com` and local GB/CA/AU readback has `0` supplier-domain/source-url hits | Get fresh explicit approval for scoped live theme sync/push of sanitizer files, then repeat public source/DOM readback; do not edit Shopify product/vendor data unless separately approved |
| P1 | ES/IT native review | Golden Daisy microtest is review-only; `platform_use_ready=false` | Get native review signoff, rerun validator, then request exact platform-use approval |
| P1 | RO/PT/GR/FR/BE Google Search build continuation | RO absent/blocked, PT/GR absent, FR stale, BE throttle; completed countries must not be re-uploaded | One-country-at-a-time preview/readback after cooldown and no-duplicate checks |
| P2 | Beach/Vacation stale SEO/social metadata | Paid traffic to stale URL is locally held/excluded | Keep held CSV path or request exact Shopify SEO/social repair approval |

## Board Rules

- Every blocker here must map to a `PROB-*` entry or a named worklog anchor.
- Do not close a blocker here unless the detailed tracker is solved, disproven, superseded, or explicitly gated.
- A blocker in one lane is a routing signal; keep independent lanes moving.
