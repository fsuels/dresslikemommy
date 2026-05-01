# Google Ads Continuity - Dress Like Mommy

Last updated: 2026-05-01 - Combined paid-media memory refresh for future agents

This file is the durable handoff for Google Ads, Merchant Center, conversion tracking, and paid-launch work. Read it before touching Google Ads in any new session.

Before any Google Ads or Merchant Center work, also read `ops/AGENT_COORDINATION.md` and honor active locks. The Standard Shopping supplier/source-url repair workstream was completed on 2026-05-01 after owner-directed continuation. The campaign was re-enabled on 2026-05-01 only after fresh explicit owner approval and clean just-in-time readbacks; do not pause/disable/re-enable or change `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` again without fresh explicit owner approval.

`AGENTS.md` is the automatic bootstrap memory. If a user provides an older continuation prompt, reconcile it against this file and `ops/AGENT_COORDINATION.md` before acting. The old Google Ads anchor `AGENT_CONTINUITY_ANCHOR: 2026-04-30-google-ads-continuity-memory` is stale and superseded by the latest worklog anchor, currently `AGENT_CONTINUITY_ANCHOR: 2026-05-01-paid-media-combined-memory-refresh`.

## Current State

Decision: `STANDARD_SHOPPING_REENABLED_AFTER_OWNER_APPROVAL_AND_CLEAN_SUPPLIER_ACTIVE_COHORT_READBACKS__BRAND_SEARCH_ENABLED_5USD_TEST__REMARKETING_WARM_REPAIRED_PAUSED_AWAITING_ENABLE_APPROVAL`

Latest combined handoff on 2026-05-01: `PAID_MEDIA_COMBINED_MEMORY_REFRESH`. This anchor adds no live edits. It exists so the next AI starts from the combined state after the individual Standard Shopping re-enable, Brand Search fresh premium asset, and Remarketing warm launch-control repair anchors.

Owner reported pausing the only previously approved campaign after finding an unacceptable supplier/source URL exposure risk. On 2026-05-01 the owner then gave the exact approval phrase `APPROVE RE-ENABLE DLM_US_STANDARD_SHOPPING_TEST_PAID_READY NOW WITH NO BUDGET, PRODUCT SCOPE, OR CONVERSION GOAL CHANGES`.

Owner reaffirmed on 2026-05-01: keep `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` paused until Merchant Center and Google Ads live readbacks confirm no supplier/source URL exposure after refresh; require fresh explicit owner approval before any re-enable. That condition was later satisfied in the same session before the approved re-enable.

Owner later continued the repair request in this session, so the Standard Shopping supplier/source-url workstream was completed and handed off in `ops/AGENT_COORDINATION.md`. After approval, the campaign was re-enabled with no budget, product-scope, product-group, feed-label, feed, or conversion-goal changes.

Latest Standard Shopping re-enable readback on 2026-05-01: `STANDARD_SHOPPING_REENABLED_AFTER_CLEAN_READBACKS`. Shopify final rescan found `0` vendor URL leaks across `803` products. Just-in-time Merchant Center supplier-domain readbacks returned `0` rows for `1688.com`, `detail.1688.com`, `alibaba.com`, and `aliexpress.com` before and after enable. Shopify active paid-cohort readback found `780` paid rows across `81` active Online Store products and `780` available variants, with `0` missing, inactive, unpublished, no-online-url, or unavailable rows. Google Ads row readback showed `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`, status icon `Enabled`, `$20.00/day`, campaign ID `23802638621`, and no supplier-domain text.

Latest Brand/Search state on 2026-05-01: `BRAND_SEARCH_OWNER_SET_5_USD_PER_DAY_READBACK`. The owner manually changed Brand Search to `$5.00/day`. Read-only live readback shows Brand Search `Eligible`, `$5.00/day`, `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions, and `Maximize clicks`. The Poor Phrase RSA was already paused; the visible enabled Exact and Phrase RSAs read `Eligible / Pending`, so actual serving/ad-strength outcome may still depend on Google review.

Latest Brand Search external-review reconciliation on 2026-05-01: `BRAND_SEARCH_EXPERT_PASS_NO_ADDITIONAL_LIVE_EDITS`. Packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-expert-pass/`. No Google Ads, Merchant Center, Shopify Admin, GA4/GTM, Pinterest, feed, budget, bid-strategy, conversion-goal, keyword, negative, audience, asset, PMax, Remarketing, or Standard Shopping edits were applied. Findings: the external review's Poor RSA and low-search-volume keyword fixes were already handled; negative pruning was not evidence-supported; unsupported promo/review/social-proof claims were not used; conversion primary changes remain a separate account-level measurement workstream requiring explicit approval.

Latest Brand Search fresh premium asset pass on 2026-05-01: `FRESH_PREMIUM_ASSETS_UPLOAD_READY_PENDING_OWNER_APPROVAL`. Packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-fresh-premium-assets/`. The prior reused-image recommendation set was superseded after the owner clarified they wanted new assets from scratch. Packet contains 5 new AI-generated image assets, 1 fresh export of the official logo, proof-backed price rows, and a promotion deferral because no current storefront-visible promo code or percent/amount-off offer was verified. No live Google Ads upload/association was made; upload requires owner action-time approval. Exact approval phrase is in `FRESH_PREMIUM_ASSET_PASS_REPORT.md`.

Latest Remarketing repair on 2026-05-01: `REMARKETING_WARM_REMARKETING_REPAIRED_PAUSED_AWAITING_EXPLICIT_ENABLE_APPROVAL`. Packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-launch-control-repair/`. Campaign stayed paused at `$1.00/day`, `$0.00` cost, `0` impressions/clicks/conversions. Controllable launch controls were repaired: `Product viewers (Retail) (AdWords)` was added as the eligible warm serving bridge, `Cart abandoners` and `Checkout starters` remained targeted, `All Converters` remained excluded, optimized targeting remained off, location remained United States presence-only, frequency cap remained `3/day/user`, dynamic ads remained connected to Merchant feed `Dresslikemommy | ID: 124884876`, and the dynamic-feed product filter remained `Labels is us_test_ready` AND `Labels is paid_eligible`. The active RDA was rewritten away from cart-only wording to generic warm-remarketing copy and still read `Ad strength: Excellent` before save; old clickbait RDAs remain paused. It is launch-gate ready as warm remarketing, not pure cart/checkout-only, because `Cart abandoners` Display size is still 8 and `Checkout starters` is still 0.

Previously approved campaign:

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`
- Type: Standard Shopping
- Status after last Google Ads readback: `Eligible`
- Status after owner approval/readback: `Enabled`
- Budget after last readback: `$20.00/day`
- 48-hour test start: 2026-04-30 19:09 EDT
- Review / rollback due: 2026-05-02 19:09 EDT
- Google Ads account-time equivalent: approximately 2026-05-02 16:09 PDT

Current target campaign statuses:

- `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` - `Eligible`, `$5.00/day`, Brand Search controlled test active after owner budget change.
- `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` - enabled after 2026-05-01 owner approval and clean supplier-domain / active-Shopify paid-cohort readbacks; keep at `$20.00/day` until the 48-hour review deadline unless the owner gives a newer decision or rollback criteria are met.
- `PMax: Shopping ads (United States)` - paused/blocked.
- `PMax: USA Google Shopping T-Shirts` - paused/blocked.
- `Remarketing - Cart Abandoners & Checkout Starters` - paused at `$1.00/day`; launch-gate ready as warm remarketing after Product viewers bridge + generic `Excellent` RDA repair, but still requires fresh explicit owner enable approval.

Latest PMax/Remarketing repair pass on 2026-05-01: `PMAX_REMARKETING_REPAIR_PASS_BLOCKED_NOT_READY`. Evidence packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-remarketing-repair-pass/`. No live Google Ads edits were applied during that earlier pass. Findings: `PMax: Shopping ads (United States)` remains a replace/archive candidate because of wrong Merchant/no-products risk. A later local-only replacement-readiness packet for `PMax: Shopping ads (United States)` exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-shopping-replacement-readiness/`; it confirms `REPLACE_NOT_REPAIR_IN_PLACE` and defines the paused replacement-shell gate, with no live PMax/Google Ads/Merchant/feed edits. A later local-only readiness repair packet for `PMax: USA Google Shopping T-Shirts` exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-tshirts-readiness-repair/`; it supersedes the broken `/collections/matching-t-shirts` draft URL, narrows the candidate to one clean paid-ready T-shirt product / 42 variants, and provides claim-safe copy plus activation gates. No live PMax upload/enable/product-scope/budget/Merchant/feed/Shopify/conversion-goal edit was made. Remarketing was later repaired in a separate paused launch-control pass and now has a warm Product-viewers bridge plus generic policy-safe RDA, but remains paused pending exact owner enable approval.

## Do Not Forget

- This is a controlled test, not a scale launch.
- Owner had paused Standard Shopping because supplier/source URLs must never appear in paid surfaces. It was re-enabled only after clean Merchant Center / Google Ads / Shopify paid-cohort readbacks and exact owner approval.
- Standard Shopping supplier/source-url repair is completed and handed off. No further campaign/feed/Merchant writes without a new narrow workstream claim and fresh owner approval.
- Do not let `$20/day` continue past the 48-hour deadline without a new owner decision.
- Google Ads can overdeliver against average daily budgets. Treat `$20/day` as a monitored test budget, not a hard one-day ceiling.
- Do not assume the Claude/ChatGPT recommendation lists were fully implemented. They were used to shape the plan, but only Standard Shopping and Brand Search have completed their current safety cleanup/gate paths.
- Never enable PMax or Remarketing without a new explicit approval and a fresh gate/readback. Never pause/disable/re-enable Standard Shopping again without a new explicit approval and fresh gate/readback.
- Never raise Brand Search above `$5/day`, increase any active budget, expand product scope, or change conversion goals without a new explicit approval.
- Do not store credentials, cookies, request headers, card data, customer PII, or payment payloads in repo files.
- Never write vendor/source URLs into Shopify product tags, title, SEO, body copy, product type, customer-visible metafields, feed-visible metafields, or any channel-visible product data. Source URLs belong only in local operator evidence files.

## Vendor URL Leak Cleanup

Latest cleanup packet:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-203731-shopify-vendor-url-leak-cleanup/`
- Final Standard Shopping supplier-domain cleanup/readback packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-standard-shopping-reactivation-readback/`

Findings:

- Root cause: the canonical listing prompt previously instructed agents to put `VENDOR_URL` in Shopify tags.
- Live Shopify audit scanned `803` products and found `263` products with vendor/source URL tags.
- Cleanup removed those exact leaking tags.
- Post-cleanup live Shopify re-scan found `0` vendor URL tags and `0` title/body/SEO/metafield vendor URL leaks.
- Paid/feed artifact checks found `0` vendor URL rows in the existing paid cohort and supplemental-label files.
- Final 2026-05-01 Shopify rescan found `0` vendor URL leaks across `803` products.
- Final 2026-05-01 Merchant Center supplier-domain gate found `0` rows for `1688.com`, `detail.1688.com`, `alibaba.com`, and `aliexpress.com`.
- Final 2026-05-01 pre-approval Google Ads readback found the Standard Shopping campaign paused and no supplier-domain text in the campaign-table capture.
- Post-approval 2026-05-01 Google Ads readback found the Standard Shopping campaign status icon `Enabled`, budget `$20.00/day`, campaign ID `23802638621`, and no supplier-domain text.
- Post-approval 2026-05-01 Shopify active paid-cohort readback found `780` paid rows across `81` active Online Store products and `780` available variants, with `0` inactive or unavailable rows.

Guardrails added:

- `ops/prompts/shopify-listing-master-prompt.md` now forbids vendor/source URLs in Shopify customer/feed-visible fields.
- `ops/scripts/audit_and_remove_vendor_url_leaks.py` audits/removes live supplier URL tags.
- `ops/tests/test_vendor_url_leak_guard.py` protects the prompt/script guard.

Required before any future pause/disable/re-enable or launch-safety edit:

1. Confirm live Standard Shopping is enabled only if still safely budget-limited, or paused if a rollback already happened.
2. Force/await Merchant Center refresh if needed.
3. Read back Merchant Center item/product data for the paid cohort and confirm no supplier/source URL exposure.
4. Read back Google Ads product/destination surfaces for `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`.
5. Get fresh explicit owner approval before re-enabling or increasing budget.

## Recommendation Implementation Status

Implemented:

- Paid-value measurement gate: passed.
- Standard Shopping paused cleanup:
  - Added max CPC guardrail `0.25`.
  - Changed location option to `Presence`.
  - Excluded `Everything else in "All products"`.
  - Verified inventory filter for `custom_label_4=us_test_ready` AND `custom_label_0=paid_eligible`.
- Standard Shopping activation:
  - Enabled only `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`.
  - Raised only this campaign to `$20.00/day` for the approved 48-hour test.
- Brand Search paused cleanup and activation gate:
  - Changed `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` from `Maximize conversion value` to `Maximize clicks`.
  - Added max CPC guardrail `0.20`.
  - Changed location option to `Presence`.
  - Left campaign paused at `$1.00/day`.
  - Gate decision: `BRAND_SEARCH_ACTIVATION_GATE_PASSED_AWAITING_EXPLICIT_OWNER_ENABLE_APPROVAL_AT_1_USD_PER_DAY`.
- Brand Search quality cleanup:
  - Added one extra RSA to `Brand - Exact` and one extra RSA to `Brand - Phrase`; ads now read back as `4` RSAs.
  - Added campaign URL suffix `utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}&utm_matchtype={matchtype}`.
  - Added four campaign-level callouts: `Official Store`, `Family Matching`, `Mommy And Me`, `Daddy And Me`.
  - Asset readback now shows `18` visible assets in scope.
  - Audited `253` campaign negatives and found `0` evidence-supported prune candidates.
  - Verified Brand list enforcement is blocked unless AI Max is enabled; AI Max remains off.
- Brand/Search account-level asset cleanup before enable:
  - Added conservative account-level callouts: `Official Store`, `Matching Outfits`, `Family Matching`, `Mommy And Me`.
  - Paused unsupported account-level assets: `Quality Fabrics`, `200+ Styles`, `New Arrivals` with weekly-new-styles claim, `Best Sellers` with top-rated claim, and `Matching Dresses` with `200+ styles for every occasion`.
  - Kept account-level `Matching Swimsuits`, `Family Sets`, and `Types` structured snippet.
  - Did not create duplicate account-level sitelinks because Brand Search already has campaign-level, brand-specific sitelinks and account-level sitelinks can spill into other campaigns.
- Brand Search final RSA/keyword repair and enable:
  - Paused the enabled `Brand - Phrase` RSA that read `Poor` ad strength.
  - Enabled the clean/pending `Brand - Phrase` RSA.
  - Enabled six core exact-match brand keywords and left two low-search-volume exact keywords paused.
  - Enabled only `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` at `$1.00/day`.
  - Post-enable row reads `Eligible`, `$1.00/day`, `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions, `Maximize clicks`.

Still not implemented / still blocked:

- Brand Search brand-list enforcement was not applied because Google Ads requires turning on AI Max before using brand inclusions/exclusions in this campaign. AI Max stays off for the controlled brand-protection posture.
- PMax recommendations were not applied live. A repair packet/draft was created on 2026-05-01, but both PMax campaigns still need rebuild/repair work before activation, including Merchant/feed eligibility, product scope, final URL controls, brand exclusions, creative assets, audience signals, and conversion/value verification readbacks.
- Remarketing launch-control repair:
  - Product-viewer warm audience bridge was added because the pure cart/checkout Display lists are too small by themselves.
  - Active RDA was rewritten to generic warm-remarketing copy and read `Excellent` in the editor before save.
  - Old clickbait-limited responsive display ads remain paused.
  - `All Converters` is excluded, optimized targeting is off, dynamic feed is connected and label-filtered, location is presence-only, content/frequency controls are in place.
  - Campaign remains paused at `$1.00/day`, with `$0.00` cost, `0` impressions/clicks/conversions.
  - Remarketing is launch-gate ready only as warm remarketing and still requires fresh exact owner enable approval before spend.

Reason:

- The paid-value gate cleared the measurement blocker, but it did not automatically approve every campaign edit or launch.
- Standard Shopping was intentionally chosen as the first controlled test candidate because it has the verified 780-product paid cohort and the safest product-scope guardrails.
- PMax has structural blockers that make it unsafe to enable as-is. Remarketing has been repaired into a paused warm-remarketing test candidate but must not be enabled without fresh exact owner approval.

## Measurement Gate

Paid-value measurement gate passed.

Evidence packet:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/FINAL_PAID_VALUE_MEASUREMENT_GATE_PASS_REPORT.md`

Key proof:

- Shopify paid order `#9476`
- Shopify order id `6575644803169`
- Confirmation `5QU2KJ7DN`
- Paid total `19.99 USD`
- Google Ads purchase request captured with:
  - endpoint `www.googleadservices.com/pagead/conversion/853411529/`
  - label `UbkpCN-fhogBEMmN-JYD`
  - event `purchase`
  - value `19.99`
  - currency `USD`
  - dedupe/order id `6575644803169`
  - enhanced conversion hash present
- GA4/Google measurement purchase request captured with:
  - measurement id `G-N4EQNK0MMB`
  - event `purchase`
  - value `19.99`
  - currency `USD`
  - transaction id `6575644803169`

Meaning:

- The paid-value blocker for non-budget cleanup and controlled launch was cleared.
- This does not automatically approve new campaign launches or budget increases.

## Feed And Merchant Center Gate

The Standard Shopping test depends on a verified paid cohort:

- Merchant Center account: `124884876 - Dresslikemommy`
- Feed label: `US`
- Cohort filter: `custom_label_4=us_test_ready` AND `custom_label_0=paid_eligible`
- Matching products in Google Ads inventory filter: `780`
- Local proof: `780` paid rows, `81` Shopify products, `780` available-for-sale variants, `0` product issues, `0` variant issues

Evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-merchant-clean-label-upload/paid_label_active_status_live_shopify_check.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-standard-shopping-activation-gate/raw/merchant_exact_label_readback_refresh_check.json`

Important:

- The broader Merchant Center catalog still has issues.
- The test is safe only because the verified paid cohort is filtered and the catch-all product group is excluded.

## Standard Shopping Final Configuration

As of the latest readback:

- Campaign: `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`
- Campaign ID: `23802638621`
- Status: `Eligible`
- Budget: `$20.00/day`
- Bid strategy: `Maximize clicks`
- Maximum CPC bid cap: `0.25`
- Conversion goals: `Account-default`
- Primary purchase action verified separately: `Google Shopping App Purchase`, `Purchases, Primary action`, dynamic value enabled, enhanced conversions enabled
- Location: `United States`
- Location option: `Presence: People in or regularly in your included locations`
- Network: `Google Search Network`
- Merchant Center/CSS: `124884876 - Dresslikemommy / CSS: Google Shopping (google.com/shopping)`
- Feed: `US (feed label)`
- Inventory filter: `custom_label_4=us_test_ready` AND `custom_label_0=paid_eligible`
- Product groups:
  - `us_test_ready`: `Automatic`
  - `Everything else in "All products"`: `Excluded`

Activation and budget evidence:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-standard-shopping-activation-gate/STANDARD_SHOPPING_ACTIVATION_EXECUTION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-standard-shopping-20usd-budget-test/STANDARD_SHOPPING_20USD_48H_BUDGET_TEST_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-standard-shopping-20usd-budget-test/ROLLBACK_AND_MONITORING_48H.md`

## 48-Hour Review Procedure

If current time is before 2026-05-02 19:09 EDT:

1. Open/read live Google Ads.
2. Check spend, impressions, clicks, search terms, conversions, conversion value, and product-group spend.
3. Confirm max CPC still `0.25`.
4. Confirm product group `Everything else in "All products"` remains excluded.
5. Confirm location remains United States and presence-only.
6. Confirm Merchant Center paid cohort remains eligible.
7. Document findings in `ops/AGENT_WORKLOG.md` and an audit packet.

If current time is at or after 2026-05-02 19:09 EDT and no newer owner decision exists:

1. Immediately run the review above.
2. Check `ops/AGENT_COORDINATION.md` before any edit.
3. If the Standard Shopping lock is still active, keep the review read-only and document the needed owner decision; do not edit the campaign, budget, product groups, Merchant Center, feed labels, or conversion goals unless the owner explicitly clears or transfers the lock.
4. If the owner clears/transfers the lock and the user is available, present results and get a decision: restore to `$1/day`, pause, continue `$20/day`, or set a different budget.
5. If the owner clears/transfers the lock and the user is not available, safest rollback is to reduce Standard Shopping to `$1.00/day`, keep the campaign otherwise unchanged, then document the rollback and evidence.

Immediate rollback triggers before the deadline:

- Spend appears outside `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible`.
- `Everything else in "All products"` becomes enabled or receives impressions/clicks.
- Merchant Center paid cohort materially worsens.
- Purchase conversion tracking misses value, currency, or transaction id.
- Duplicate purchase counting appears for one order id.
- Clearly irrelevant Shopping search terms appear and cannot be controlled quickly.
- Non-US traffic appears despite presence-only targeting.
- Cost reaches `$20` with no qualified traffic or useful search-term data.
- The owner asks to stop.

## Other Campaign Status And Required Work

Brand Search:

- Campaign: `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429`
- Status: `Eligible` at `$5.00/day` after owner manually changed the budget from the original `$1.00/day` test.
- Cleanup: completed on 2026-04-30.
- Bid strategy: `Maximize clicks`
- Max CPC cap: `0.20`
- Location option: `Presence: People in or regularly in your included locations`
- Network: Google Search Network only
- Conversion goal: Account-default `Purchases`
- Ads/assets: `4` RSAs, campaign-level URL suffix added, 8 campaign-level callouts now eligible, 6 high-quality campaign-level sitelinks with verified collection URLs now eligible, 6 older weak/redundant campaign sitelinks paused, and campaign business name `Dress Like Mommy` pending review
- Negative audit: `253` campaign negatives, `0` broad negatives, `0` evidence-supported prune candidates
- Brand list: not applied because the live UI requires AI Max for brand inclusions/exclusions; AI Max remains off
- Account-level asset cleanup: completed on 2026-05-01. Unsupported account-level claims were paused (`Quality Fabrics`, `200+ Styles`, weekly-new-styles, top-rated, and `200+ styles for every occasion`), and conservative account-level callouts were added. Do not duplicate Brand Search sitelinks at account level unless a future account-wide asset plan explicitly approves the spillover risk.
- Final live readback before enable: completed on 2026-05-01. Campaign was paused at `$1.00/day`, bid strategy read `Maximize clicks`, settings read back `Google Search Network`, `Account-default: Purchases`, `United States`, `English`, `Text customization and Final URL expansion turned off`, `Automatically created assets` off, `Broad match keywords` off, and `Campaign URL options` using URL tracking options.
- RSA repair and enable: completed on 2026-05-01. Poor Phrase RSA is paused; clean Exact and Phrase RSAs read `Eligible / Pending`; six core exact-match keywords and two phrase keywords read `Eligible`; two low-search-volume exact keywords remain paused.
- Owner-set `$5/day` readback: completed on 2026-05-01. Campaign reads `Eligible`, `$5.00/day`, `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions, `Maximize clicks`; visible enabled Exact/Phrase RSAs read `Eligible / Pending`.
- External-review expert pass: completed on 2026-05-01. No additional live edits were applied. Fresh readbacks confirmed the Poor Phrase RSA was not enabled, the low-search-volume exact keywords were already paused, and the conversion-value gate still showed exactly one primary account-level purchase action. Do not implement the external review's negative removals, unsupported promo/social-proof claims, customer-acquisition switch, tROAS switch, or conversion-primary changes without fresh evidence and the approvals required by `ops/AGENT_COORDINATION.md`.
- Gate: `BRAND_SEARCH_OWNER_SET_5_USD_PER_DAY_READBACK`
- Do not raise budget above `$5/day`, change conversion goals, or make broader non-budget changes without fresh explicit approval.
- Evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-brand-search-paused-cleanup/`
- Quality evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-brand-search-quality-cleanup/`
- Asset quality pass evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-brand-search-asset-quality-pass/`
- Account-level asset cleanup evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-account-level-asset-cleanup/`
- Final Brand Search live readback evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-final-readback/`
- RSA repair/enable evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-rsa-repair-enable/`
- `$5/day` readback evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-5usd-readback/`

PMax:

- `PMax: Shopping ads (United States)`: paused at `$1.00/day`, prior blocker `No products for any locations` / Merchant mismatch risk.
- `PMax: USA Google Shopping T-Shirts`: paused at `$1.00/day`, all asset groups paused, scope/creative not launch-clean.
- Latest repair packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-remarketing-repair-pass/`
- `PMax: Shopping ads (United States)` should not be repaired in place for launch; replacement/archive is safer because the campaign still carries wrong Merchant/no-products risk. Local replacement-readiness packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-shopping-replacement-readiness/`.
- `PMax: USA Google Shopping T-Shirts` now has a local-only readiness packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-tshirts-readiness-repair/`.
- PMax T-Shirts packet result: `PMAX_TSHIRTS_LOCAL_REPAIR_PACKET_READY_LIVE_CHANGES_BLOCKED_PENDING_OWNER_APPROVAL`.
- PMax T-Shirts local proof found one strict clean paid-ready T-shirt product (`7229259874401`) with `42` variants, price `$17.99` to `$21.99`, unit cost `$9.00` to `$11.00`, all rows `paid_eligible` and `us_test_ready`, Online Store + Google/YouTube published, in stock, and no supplier-domain text on the public landing-page check.
- The old PMax T-Shirts draft final URL `https://www.dresslikemommy.com/collections/matching-t-shirts` returned HTTP 404 on 2026-05-01; use the repaired product URL from the new packet only after owner approval and just-in-time readback.
- The repaired T-Shirts packet is a micro-test candidate only; it may be too narrow for PMax learning and may overlap Standard Shopping. Do not upload assets, change live product scope, unpause asset groups, enable campaign, or change budget/conversion goals without fresh explicit owner approval.
- Do not enable either PMax until feed, conversion, landing-page, product-label, final URL, brand-exclusion, creative, and audience-signal work is separately approved and verified.

Remarketing:

- `Remarketing - Cart Abandoners & Checkout Starters`: paused at `$1.00/day`.
- Campaign ID: `23609373008`
- Latest warm launch-control repair packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-launch-control-repair/`
- Status: paused warm-remarketing launch gate ready, pending fresh exact enable approval.
- Targeted audiences: `Product viewers (Retail) (AdWords)`, `Cart abandoners`, and `Checkout starters`.
- Serving bridge: `Product viewers (Retail) (AdWords)` read back `Not eligible - Campaign is paused`, without the `Audience not eligible` reason. The pure cart/checkout lists are still too small by themselves: `Cart abandoners` Display size 8, `Checkout starters` Display size 0.
- Exclusion: `All Converters` at ad-group level.
- Optimized targeting: `Off`.
- Creative: active RDA is generic warm copy, not cart-only pressure copy. It read `Ad strength: Excellent` before save and final Ads table shows `Dress Like Mommy Styles` / `Matching Family Styles From Dress Like Mommy`.
- Old five clickbait RDAs remain `Paused` with historical `Policy (Clickbait), Campaign is paused` notes.
- Dynamic ads: feed `Dresslikemommy | ID: 124884876`, filtered to `Labels is us_test_ready` AND `Labels is paid_eligible`.
- Controls: United States presence-only, English, frequency cap `3/day/user`, content exclusions present, URL tracking options present.
- Final campaign readback: paused, `$1.00/day`, Display, `Maximize conversions`, `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions.
- Do not enable until a fresh owner approval phrase is given after final just-in-time readback.

## Key Packets

Use these first:

- Measurement pass: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/`
- Paused cleanup: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-paused-campaign-cleanup/`
- Activation gate/execution: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-standard-shopping-activation-gate/`
- $20/day 48-hour test: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-standard-shopping-20usd-budget-test/`
- Brand Search cleanup/gate: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-brand-search-paused-cleanup/`
- Brand Search quality cleanup: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-brand-search-quality-cleanup/`
- Brand Search RSA repair/enable: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-rsa-repair-enable/`
- Brand Search `$5/day` readback: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-5usd-readback/`
- Brand Search external-review expert pass: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-expert-pass/`
- Brand Search fresh premium assets: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-fresh-premium-assets/`
- Standard Shopping approved re-enable readback: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-standard-shopping-reenable-approved/`
- PMax/Remarketing repair pass: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-remarketing-repair-pass/`
- PMax T-Shirts local readiness repair: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-tshirts-readiness-repair/`
- Remarketing policy-safe RDA repair: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-expert-repair-audit/`
- Remarketing warm launch-control repair: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-launch-control-repair/`
- Launch readiness control: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-launch-readiness-control/`
- Campaign readiness orchestration: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-campaign-readiness-orchestration/`

Relevant worklog anchors:

- `2026-04-30-google-ads-paid-value-gate-pass`
- `2026-04-30-google-ads-paused-campaign-cleanup`
- `2026-04-30-google-ads-standard-shopping-activation-gate`
- `2026-04-30-google-ads-standard-shopping-enabled`
- `2026-04-30-google-ads-standard-shopping-20usd-48h-budget-test`
- `2026-04-30-google-ads-brand-search-paused-cleanup-gate`
- `2026-04-30-google-ads-brand-search-quality-cleanup`
- `2026-04-30-google-ads-brand-search-asset-quality-pass`
- `2026-05-01-google-ads-brand-search-rsa-repair-enabled`
- `2026-05-01-google-ads-brand-search-5usd-readback`
- `2026-05-01-google-ads-memory-files-refreshed-brand-5usd`
- `2026-05-01-google-ads-auto-bootstrap-coordination-hardening`
- `2026-05-01-google-ads-pmax-remarketing-repair-pass`
- `2026-05-01-google-ads-brand-search-expert-pass-no-live-edits`
- `2026-05-01-google-ads-remarketing-policy-safe-rda-upload`
- `2026-05-01-standard-shopping-approved-reenabled`
- `2026-05-01-google-ads-brand-search-fresh-premium-assets`
- `2026-05-01-google-ads-remarketing-warm-launch-control-ready`
- `2026-05-01-paid-media-combined-memory-refresh`

## Browser / Tooling Notes

- Existing Google Ads work used Chrome DevTools Protocol on port `9222`.
- Prefer live UI readbacks before any paid edit.
- For browser capture, reuse the CDP helper patterns in `ops/scripts/run_google_ads_paid_checkout_capture.py`.
- If Chrome or Google Ads is not logged in, say the browser session needs login instead of assuming access is gone.
- Do not write cookies, auth headers, payment data, or customer PII into evidence packets.

## New Session Prompt

The reusable prompt for starting a new session is:

- `ops/prompts/google-ads-continuation-prompt.md`
