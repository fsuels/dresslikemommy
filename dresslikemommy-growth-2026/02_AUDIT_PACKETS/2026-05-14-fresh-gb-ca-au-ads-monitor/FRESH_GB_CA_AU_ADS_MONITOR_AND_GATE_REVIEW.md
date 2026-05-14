# Fresh GB/CA/AU Ads Monitor And Gate Review

Timestamp: 2026-05-14 08:17 EDT

Mode: read-only Google Ads CDP/RPC/UI monitor plus public storefront source readback. No Google Ads, Merchant, Pinterest, Shopify Admin, GA4/GTM, billing, budget, bid, status, keyword, ad, negative, feed, product, conversion, or live theme write occurred.

## Decision

`BLOCK_LIVE_ADS_ACTION__LANDING_SANITIZER_FAILS__HEAD_TERMS_FAIL_015_CPC_GATE`

Do not upload/apply/add keywords, change bids, change status, add negatives, or execute an auction-entry repair yet. The Ads-side readback is usable, but the live paid landing sanitizer gate failed on all three active final URLs and the current head keywords fail the owner's hard `$0.15` CPC economics.

## Fresh Ads Readback

| Market | Campaign | Ad group | Status/scope | Spend/click/impression state | Search-term filter | Keyword/RSA/final URL |
|---|---|---|---|---|---|---|
| GB | `23838895360` | `194138528537` | Campaign enabled/eligible, `$2/day`, Search only, presence-only, only target ad group enabled, no campaign conversion override | Displayed `0` clicks, `0` impressions, `$0.00` cost, `0.00` conversions/value in current monitor window | Stale `Keyword: "human hair wigs"` filter was present, then removed by clicking only the visible filter-chip delete control; after capture has no stale filter and no search terms | 3 exact keywords enabled; 1 RSA enabled; all final URLs country-qualified with `?country=GB` |
| CA | `23834423669` | `196679079575` | Campaign enabled/eligible, `$2/day`, Search only, presence-only, only target ad group enabled, no campaign conversion override | Displayed `0` clicks, `0` impressions, `$0.00` cost, `0.00` conversions/value in current monitor window | Stale `Keyword: "human hair wigs"` filter was present, then removed by clicking only the visible filter-chip delete control; after capture has no stale filter and no search terms | 3 exact keywords enabled; 1 RSA enabled; all final URLs country-qualified with `?country=CA` |
| AU | `23834424182` | `198852670520` | Campaign enabled/eligible, `$2/day`, Search only, presence-only, only target ad group enabled, no campaign conversion override | Displayed `0` clicks, `0` impressions, `$0.00` cost, `0.00` conversions/value in current monitor window | Stale `Keyword: "human hair wigs"` filter was present, then removed by clicking only the visible filter-chip delete control; after capture has no stale filter and no search terms | 3 exact keywords enabled; 1 RSA enabled; all final URLs country-qualified with `?country=AU` |

## Quality / Auction Diagnosis

- Keyword UI detail pages expose Quality Score, Exp. CTR, Ad relevance, Landing page experience, policy, and final URL columns.
- Every currently active keyword is `Eligible (Limited)` with `Below first page bid`:
  - `[mommy and me dresses]`: first page estimate `$0.68`, top-of-page estimate `$0.80`.
  - `[mom and daughter matching outfits]`: first page estimate `$0.74`, top-of-page estimate `$0.84`.
  - `[mother daughter dresses]`: first page/top-of-page estimate `$0.65`.
- Current max CPC remains `$0.15`, so zero impressions are plausibly auction-entry/CPC-cap constrained, not proof that demand is absent.
- Owner correction: `$0.15` CPC is a hard ceiling. Do not raise bids into the `$0.65-$0.74` head-term auction, and do not treat close variants such as `[mummy and me dresses]`, `[mommy and me dresses canada]`, or `[mummy and me dresses australia]` as real long-tail discovery.
- No search-term negative is justified because search terms are now filter-clean but still empty/no terms.

## Live Landing Sanitizer Readback

All three public final URLs returned HTTP `200` and showed the expected currency signal, but all three still exposed a supplier URL in public source:

| Market | Expected currency | Currency seen | Supplier/source hits | Result |
|---|---|---|---|---|
| GB | GBP | Yes | `1688.com`, `detail.1688.com`, `data-analytics-vendor="http` | `FAIL` |
| CA | CAD | Yes | `1688.com`, `detail.1688.com`, `data-analytics-vendor="http` | `FAIL` |
| AU | AUD | Yes | `1688.com`, `detail.1688.com`, `data-analytics-vendor="http` | `FAIL` |

Representative source snippet pattern: `data-analytics-vendor="https://detail.1688.com/offer/602107180663.html"`.

## Reviewer Verdict

Reviewer verdict: `BLOCK`

Checked:
- Approval boundary: read-only/local evidence only.
- External-write risk: no account/theme write made.
- Spend authority: `APPROVED_ACTIVE`, but green-gate conditions are incomplete.
- Supplier/source URL: failed on all three live final URLs.
- CPC economics: current head terms and close head-term variants fail the `$0.15` cap. No bid-up or close-head-term expansion is reviewer-safe.
- Full quality attention: status, scope, keywords, RSA, final URLs, Quality Score columns, search-term filters, auction-entry estimates, and live landing source were checked.
- Keyword discipline: no negative/upload/bid change from zero search terms.

Required gates/fixes:
- Scoped live theme sanitizer sync/readback must show `0` hits for `1688.com`, `detail.1688.com`, `alibaba.com`, `aliexpress.com`, and URL-like analytics vendor/brand attributes on GB/CA/AU final URLs.
- Then rerun the Ads read-only monitor and reviewer gate before any live keyword action.
- Any keyword addition must pass a `$0.15` CPC validation gate: read-only Keyword Planner or keyword UI must show first-page estimate `<= $0.15`, or no below-first-page warning at max CPC `$0.15`. No bid increase above `$0.15` is allowed.

## Exact-Scope Bounded Packet Status

The bounded action packet is prepared only as `BLOCKED_DO_NOT_UPLOAD_OR_APPLY` in `exact_scope_bounded_action_packet_blocked.csv`.

Correction after owner CPC review: the previous close-head-term rows were rejected. The current packet now separates rejected head/near-head terms from real long-tail validation candidates.

Preferred next Ads action after the landing gate passes: validate product-specific and buyer-moment long-tail exact rows first, not a head-term bid jump and not a head term with only country/local vocabulary attached. Head-term first-page estimates around `$0.65-$0.74` are far above the hard `$0.15` cap and conflict with the `650% ROAS` path.

## Evidence

- Fresh monitor: `raw/monitoring_summary.json`
- Search-term filter clear readback: `raw/search-term-filter-clear/search_term_filter_clear_summary.json`
- Keyword/RSA/final URL RPC readback: `raw/fresh-readonly-rpc/fresh_rpc_summary.json`
- Keyword and ads UI detail captures: `raw/ui-detail-pages/ui_detail_pages_summary.json`
- Public landing source readback: `raw/landing/landing_sanitizer_public_source_summary.json`
- CPC correction: `CPC_015_LONG_TAIL_CORRECTION.md`
