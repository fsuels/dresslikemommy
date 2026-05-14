# Current Marketing State

Last reconciled: 2026-05-14 06:05 EDT
Source level: repo-known evidence plus 2026-05-14 read-only live reconciliation and public/local paid landing readbacks.

## State Labels

- `REPO_KNOWN`: historical repo evidence says this was true at the cited time.
- `LIVE_READBACK_REQUIRED`: current live state must be checked before any decision or claim.
- `LIVE_VERIFIED`: current-session live readback proves the state for the named evidence scope.
- `STALE_OR_SUPERSEDED`: historical evidence exists but should not drive current action without reconciliation.

## Executive State

- Goal: grow profitable Dress Like Mommy sales through controlled Google Ads and Pinterest execution, targeting about `650% ROAS`.
- Execution issue being fixed: the repo had durable memory but lacked a compact daily command layer for active campaign decisions.
- Current authority: bounded paid-media authority is `APPROVED_ACTIVE` in `spend_authorization.md`: total cap `$80/day`, new/test campaign cap `$5/day`, green-gated quality-checked proactive actions only. Fresh approval is still required for excluded surfaces.
- Growth urgency: starting 2026-05-14, each day without sales growth, usable learning, or a sales-moving improvement is a failure signal; zero impressions after 24 hours requires same-day serving diagnosis and high-buyer-intent long-tail or auction-entry action planning.
- Latest live task: read-only reconciliation completed for GB/CA/AU exact Search, Standard Shopping, Pinterest access, Merchant US/es samples, Merchant prioritized fixes, and current paid landing public-source safety.
- Active-products rule: paid campaigns must advertise only currently active, public, purchasable products with clean landing readbacks. Draft, inactive, stale, excluded, supplier-leaking, seasonally mismatched, or unresolved product URLs cannot enter live traffic.
- Category strategy rule: campaign/category planning must match real shopper intent and the calendar. For example, Father's Day tests should bias toward Daddy-and-Me, father-inclusive family matching products, and broader family matching categories instead of unrelated or stale seasonal pages.

## Repo-Known Paid-Growth State

| Surface | Evidence class | Repo-known state | Current live state | Next action |
|---|---|---|---|---|
| Google Ads GB Search | `LIVE_VERIFIED` | Campaign `23838895360`, exact ad group `Mommy & Me Dresses - Exact`, 3 exact keywords and 1 RSA were previously enabled under exact 2026-05-12 approval | `LIVE_VERIFIED`: 2026-05-14 monitor passed. Campaign `Enabled` / `Eligible`, `$2.00/day`, Search only, presence-only, no campaign conversion override, only exact ad group `194138528537` enabled, `9` other ad groups paused. Yesterday `2026-05-13`: `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions/value | `ACTION_DUE_NOW`: T+24 zero-impression rule triggered; run same-day serving diagnosis and high-buyer-intent long-tail/auction-entry planning |
| Google Ads CA Search | `LIVE_VERIFIED` | Campaign `23834423669`, same approved exact micro-cohort | `LIVE_VERIFIED`: 2026-05-14 monitor passed. Campaign `Enabled` / `Eligible`, `$2.00/day`, Search only, presence-only, no campaign conversion override, only exact ad group `196679079575` enabled, `9` other ad groups paused. Yesterday: `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions/value | `ACTION_DUE_NOW`: T+24 zero-impression rule triggered; run serving diagnosis, clear/avoid stale unrelated search-term filter, and evaluate long-tail/auction-entry options |
| Google Ads AU Search | `LIVE_VERIFIED` | Campaign `23834424182`, same approved exact micro-cohort | `LIVE_VERIFIED`: 2026-05-14 monitor passed. Campaign `Enabled` / `Eligible`, `$2.00/day`, Search only, presence-only, no campaign conversion override, only exact ad group `198852670520` enabled, `9` other ad groups paused. Yesterday: `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions/value | `ACTION_DUE_NOW`: T+24 zero-impression rule triggered; run serving diagnosis, clear/avoid stale unrelated search-term filter, and evaluate long-tail/auction-entry options |
| Standard Shopping US | `LIVE_VERIFIED` | Repo memory says live/eligible with tight paid cohort, Standard Shopping constraints, and no permission for status/budget/scope/conversion changes | `LIVE_VERIFIED`: campaign `23802638621` / `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` is `Enabled` / `Eligible`, Shopping, `$20.00/day`; yesterday `2026-05-13` shows `17` impressions, `0` clicks, `$0.00` cost, `0.00` conversions/value; included `us_test_ready` child groups remain `$0.04`; `Everything else in "All products"` remains `Excluded` | `HOLD_MONITOR_NO_WRITE`; no Standard Shopping status/budget/bid/product-scope change justified |
| GB/CA/AU optimization | `LIVE_VERIFIED` | Prior evaluator decision was `HOLD_MONITOR_NO_OPTIMIZATION_WRITE` because zero data and search terms were not actionable | `LIVE_VERIFIED`: still no spend/click/conversion data on 2026-05-14; GB search terms readable but empty; CA/AU stale filter remains | Do not add negatives, pause, scale, change bids/budgets, or infer ROAS from stale data; do run same-day zero-impression diagnosis and high-intent long-tail candidate work inside green gates |
| GB/CA/AU active Search landing PDP | `LIVE_VERIFIED_LOCAL_FIX_READY` | Final URLs point to the beige chiffon family matching PDP with `?country=GB`, `?country=CA`, and `?country=AU` | Public source readback returned `200`, correct country/currency/shipping signals, no Christmas/local-inventory/warehouse/retail-store copy, but exposed a supplier URL in a related product `data-analytics-vendor`. Local theme sanitizer patch now removes `1688.com`/supplier URL hits from the same local paid landing paths | Do not expand paid traffic from this landing state until scoped theme sanitizer is synced live and public readback passes; no Shopify product/vendor data edit without approval |
| Google Ads RO/PT/GR/FR/BE builds | `REPO_KNOWN` | RO absent/preview path blocked, PT/GR absent, FR stale/no-change, BE upload-throttle; completed countries must not be re-uploaded | `LIVE_READBACK_REQUIRED` | One-country-at-a-time no-duplicate readback before any preview/apply path |
| ES/IT Golden Daisy Search | `REPO_KNOWN` | Local review-only microtest and native signoff bundle exist; `platform_use_ready=false` pending native review and exact owner approval | `LIVE_READBACK_REQUIRED` before platform use | Native review, validator, then exact approval |
| Pinterest US | `LIVE_VERIFIED` | Clean local US scope: `342` rows, `4` exclusions, validated paused-draft spec. Owner had approved a paused build, but authenticated controllable Pinterest access was blocked. No Pinterest write occurred | `LIVE_VERIFIED`: 2026-05-14 Pinterest Ads URL lands on public login/sign-up page, Create control not found, login blocker true, and no object saved/created | Restore authenticated controllable Ads Manager access before any paused draft write |
| Pinterest Event Quality | `REPO_KNOWN` | Repo-known status `Fair`; owner later said assume tags are correct for launch-prep, but writes remain gated. Event quality should not block local/paused prep | `LIVE_READBACK_REQUIRED` | Read-only check if relevant, do not add duplicate tag/CAPI by inference |
| Merchant US/en age_group | `REPO_KNOWN` | Solved in repo evidence; do not redo broad Shopify age_group work | `STALE_OR_SUPERSEDED` for new decisions | Verify only if a fresh diagnostic reopens it |
| Merchant US/es age_group | `LIVE_VERIFIED` / `STALE_OR_SUPERSEDED` | Source `10627981690`, feed label `US`, language `es`, country `United States`; old exact export showed `625` paid item IDs / `1,250` rows | `LIVE_VERIFIED`: 2026-05-14 sampled target rows are visible and sampled detail RPCs show effective `n:age_group` with no Missing age_group issue reproduced. Current Merchant prioritized page does not show Missing age group. `STALE_OR_SUPERSEDED`: downloaded CSV is still named `product_issues_2026-05-08_02-52-49.csv` and must not be treated as today's exact export | Do not request/perform repair from stale export alone; obtain current exact US/es export or authoritative all-row readback before reclassifying solved or repair-needed |
| Merchant Shopping capacity | `LIVE_VERIFIED` | Not part of the prior command-layer seed | `LIVE_VERIFIED`: Merchant prioritized fixes page updated `3:09 AM May 14, 2026` shows `Over capacity for Shopping ads (outside of CSS program)` affecting `73.3K products (21%)` | Diagnose paid-cohort/serving impact read-only; no product removals, source changes, or capacity request without owner decision |
| Non-US purchase proof | `STALE_OR_SUPERSEDED` | Order-level non-US purchase event currency/value proof remained unclosed in repo evidence; owner later said stop using tags/Event Quality/GA4 proof as launch-prep blocker, but do not overclaim measurement | `LIVE_READBACK_REQUIRED` for reporting claims | Reconcile with owner directive and fresh reporting evidence |
| Beach/Vacation URL | `REPO_KNOWN` | Stale Christmas SEO/social metadata on paid-candidate beach URL is locally mitigated by held Ads CSV excluding that handle; Shopify repair requires exact approval | `LIVE_READBACK_REQUIRED` before traffic | Keep URL excluded or request exact Shopify metadata repair approval |

## Live Readback Status

2026-05-14 read-only reconciliation confirmed, without writes:

- GB/CA/AU exact Search are enabled/eligible at the approved exact micro-cohort scope, with zero spend/click/impression/conversion data for yesterday.
- Standard Shopping is enabled/eligible, with `17` impressions, `0` clicks, `$0.00` cost, and `0.00` conversions/value for yesterday.
- Pinterest Ads Manager is not authenticated in the current controllable browser session.
- Merchant US/es age_group should be treated as sample-cleared but exact-export-pending, because the downloaded CSV is stale May 8 evidence.
- ROAS decision state from the saved readback does not justify scale, pause, negative, or bid/budget live action yet; bounded authority is active, and GB/CA/AU zero-impression state now requires same-day diagnosis and high-intent long-tail/auction-entry planning before any green-gated action.
- GB/CA/AU active Search landing public source has correct country/currency/shipping and no stale Christmas/local-inventory copy, but the live page still needs a scoped theme sync/readback because a supplier URL was found in a related-card analytics vendor attribute. Local sanitizer readback passed.

Still needed:

- Current exact Merchant all-row export/readback for `US` / `es` / source `10627981690`, avoiding stale ready-download artifacts.
- Read-only Merchant capacity impact diagnosis for current paid cohort and Standard Shopping serving.
- Authenticated Pinterest Ads Manager access and before-write readbacks for the paused US draft path.
- Next GB/CA/AU monitor and serving diagnosis now, not after impressions appear: check sales/ROAS, serving, eligibility, Quality Score gaps, auction entry/CPC cap, exact keyword competitiveness, long-tail alternatives, and CA/AU stale filter absence before any live action.
- Scoped live theme sync/push of the paid-landing vendor/source sanitizer remains outside paid-media spend authority unless separately approved or covered by an explicit safe theme-write path, followed by public source/DOM readback on GB/CA/AU final URLs.
- Full current Admin/Merchant/Pinterest active-product intersection before advertising all active products; the first prep map is saved, but upload/apply decisions still require exact approval and clean readbacks.

## Do Not Infer

- Do not infer live eligibility, spend, ROAS, or blockers from this file.
- Do not infer approval for out-of-bounds actions from bounded spend authority.
- Do not treat local review-only files as platform-ready.
- Do not create a second command layer under `AI_Team/`.
