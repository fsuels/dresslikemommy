# Google Ads Continuation Prompt

Use this prompt when starting a new session that needs to continue the Google Ads / Merchant Center / paid-launch work.

`AGENTS.md` is the automatic bootstrap memory. This prompt is a convenience copy only; if it conflicts with `AGENTS.md`, `ops/AGENT_COORDINATION.md`, or `ops/GOOGLE_ADS_CONTINUITY.md`, the live files win. The old prompt/anchor `AGENT_CONTINUITY_ANCHOR: 2026-04-30-google-ads-continuity-memory` is stale and must not be used as current state.

```text
You are continuing Google Ads and paid-launch work for Dress Like Mommy in `/Users/fsuels/Projects/dresslikemommy`.

First read:
1. `AGENTS.md`
2. `ops/AGENT_COORDINATION.md`
3. `ops/GOOGLE_ADS_CONTINUITY.md`
4. The latest entries at the bottom of `ops/AGENT_WORKLOG.md`

Search the worklog for this latest anchor:
`AGENT_CONTINUITY_ANCHOR: 2026-05-01-google-ads-pmax-tshirts-local-readiness-repair`

Current known state as of the latest anchor:
- This is a combined memory-refresh anchor after the Remarketing warm launch-control repair. It summarizes the latest known state across Standard Shopping, Brand Search, PMax, Remarketing, Merchant Center, and Shopify paid-cohort safety after the individual workstream anchors.
- Owner reported pausing `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` after finding an unacceptable supplier/source URL exposure risk.
- Owner later gave the exact approval phrase `APPROVE RE-ENABLE DLM_US_STANDARD_SHOPPING_TEST_PAID_READY NOW WITH NO BUDGET, PRODUCT SCOPE, OR CONVERSION GOAL CHANGES`.
- Standard Shopping supplier/source-url repair is completed and handed off in `ops/AGENT_COORDINATION.md`. The campaign was re-enabled on 2026-05-01 only after just-in-time clean Merchant, Google Ads, and Shopify paid-cohort readbacks. Do not pause/disable/re-enable it again, or edit `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`, Merchant Center product/feed data, product groups, feed labels, budgets, conversion goals, or activation gates unless the owner gives a new narrow approval.
- Latest live gates: Merchant Center supplier-domain searches returned `0` rows for `1688.com`, `detail.1688.com`, `alibaba.com`, and `aliexpress.com` before and after enable; Google Ads row readback showed status icon `Enabled`, `$20.00/day`, campaign ID `23802638621`, and no supplier-domain text; Shopify active paid-cohort readback showed `780` paid rows across `81` active Online Store products and `780` available variants with `0` inactive/unavailable rows.
- The original 48-hour review/rollback deadline is still 2026-05-02 19:09 EDT.
- Max CPC cap remains `0.25`.
- Product scope is only `custom_label_4=us_test_ready` AND `custom_label_0=paid_eligible`.
- Product group `Everything else in "All products"` is excluded.
- Location is United States with presence-only targeting.
- Brand Search is now enabled as a controlled `$5.00/day` test after the owner manually changed the budget from the original `$1.00/day` approval. Campaign `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` reads `Eligible`, `$5.00/day`, `$0.00` cost, `0` clicks, `0` impressions, `0.00` conversions, and `Maximize clicks`.
- Brand Search paused cleanup/gate and quality cleanup are complete: max CPC `0.20`, presence-only location, Google Search Network only, campaign URL suffix added, 8 campaign-level callouts eligible, 6 high-quality campaign-level sitelinks with verified collection URLs eligible, 6 older weak/redundant campaign sitelinks paused, and campaign business name `Dress Like Mommy` pending review.
- Brand Search RSA/keyword repair is complete: the Poor Phrase RSA is paused; the clean Phrase RSA and clean Exact RSA read `Eligible / Pending`; six core exact-match brand keywords and two phrase-match brand keywords read `Eligible`; two low-search-volume exact keywords (`[dress like mommy shop]`, `[dlm dresses]`) remain paused.
- Brand Search brand-list enforcement is not active because the live Google Ads UI requires turning on AI Max to use brand inclusions/exclusions. AI Max remains off.
- Brand Search negative pruning was audited, not applied: `253` campaign negatives, `0` broad negatives, and `0` evidence-supported prune candidates.
- Brand Search business logo was prepared and uploaded into Google Ads Asset Library, but not associated to the campaign because the business-logo picker would not attach it cleanly. Do not claim a logo asset is live until Google Ads readback shows it.
- Brand Search external-review expert pass is complete. No additional live edits were applied: the Poor RSA was already paused, low-search-volume keywords were already paused, negative removals were not evidence-supported, unsupported promo/review/social-proof claims were not used, and conversion-primary changes remain a separate account-level measurement workstream requiring explicit approval.
- Brand Search fresh premium asset pass is upload-ready but not live. The owner clarified they want new creative from scratch, so the prior reused-image recommendation set is superseded. Use packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-fresh-premium-assets/`: 5 new image assets, 1 official-logo export, proof-backed price rows, and promotion deferred because no current storefront-visible promo code/offer was verified. Upload/association requires owner action-time approval.
- Account-level asset cleanup is complete before Brand enable: conservative account-level callouts were added (`Official Store`, `Matching Outfits`, `Family Matching`, `Mommy And Me`) and unsupported account-level claims were paused (`Quality Fabrics`, `200+ Styles`, `New Arrivals` with weekly-new-styles claim, `Best Sellers` with top-rated claim, and `Matching Dresses` with `200+ styles for every occasion`).
- Do not add duplicate account-level sitelinks just to mirror Brand Search; Brand already has campaign-level, brand-specific sitelinks, and account-level sitelinks can spill into other campaigns.
- Brand Search was enabled only after the exact approval phrase `APPROVE ENABLE BRAND SEARCH AT $1.00/DAY NOW` was provided in the owner request, then the owner manually changed budget to `$5/day`; this was read back live. Do not raise Brand Search above `$5.00/day`, change conversion goals, or make broader non-budget changes without fresh explicit approval.
- Both PMax campaigns remain paused at `$1.00/day` and blocked pending structural repair.
- A PMax/Remarketing repair packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-remarketing-repair-pass/`.
- `PMax: Shopping ads (United States)` should not be repaired in place for launch because of wrong Merchant/no-products risk. A local replacement-readiness packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-shopping-replacement-readiness/`; no live PMax edits were made and any paused replacement shell requires fresh exact owner approval.
- `PMax: USA Google Shopping T-Shirts` now has a local-only readiness repair packet at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-tshirts-readiness-repair/`. It supersedes the old `/collections/matching-t-shirts` draft URL because that URL returned 404, and it narrows the candidate to one clean paid-ready T-shirt product / 42 variants with claim-safe copy, search-theme/audience plan, URL controls, and activation checklist. No live upload, unpause, enable, budget, product-scope, Merchant/feed, Shopify product, or conversion-goal edit was made.
- Remarketing launch-control repair later completed as warm remarketing, not pure cart/checkout-only. It remains paused at `$1.00/day`, `$0.00` cost, `0` impressions/clicks/conversions. `Product viewers (Retail) (AdWords)` was added as the eligible warm serving bridge because cart/checkout lists are still too small; `Cart abandoners` and `Checkout starters` remain targeted; `All Converters` remains excluded; optimized targeting remains off; location remains United States presence-only; frequency cap remains `3/day/user`; dynamic ads remain connected to Merchant feed `Dresslikemommy | ID: 124884876`; feed product filter remains `Labels is us_test_ready` AND `Labels is paid_eligible`; the active RDA was rewritten to generic warm policy-safe copy and read `Excellent` before save. Evidence packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-launch-control-repair/`.
- Remarketing is launch-gate ready only as warm remarketing and still requires fresh exact owner enable approval. Do not enable it by inference.
- Shopify vendor URL leak cleanup removed exact supplier URL tags from `263` live products and post-cleanup scans found `0` vendor URL tags/title/body/SEO/metafield leaks across `803` products.
- Final 2026-05-01 Shopify vendor URL rescan also found `0` leaks across `803` products.
- Canonical listing prompts now forbid vendor/source URLs in Shopify customer/feed-visible fields.

Important safety rules:
- Before external-system work, check `ops/AGENT_COORDINATION.md`; one writer per campaign/feed/product cohort/surface.
- If a campaign or feed surface is locked by another agent, stay read-only unless the owner explicitly transfers or clears that lock.
- Do not assume Claude/ChatGPT campaign recommendations were fully implemented. They were evaluated and folded into the plan, but only Standard Shopping and Brand Search have completed their current safety cleanup/gate paths.
- Do not enable PMax or Remarketing; do not pause/disable/re-enable Standard Shopping again; do not raise Brand Search above `$5.00/day`; and do not increase budgets, expand product scope, or change conversion goals without fresh explicit owner approval in this session.
- Never write vendor/source URLs into Shopify tags, title, SEO, body copy, product type, customer-visible metafields, feed-visible metafields, or any sales-channel-visible product data.
- If current time is after 2026-05-02 19:09 EDT and there is no newer owner approval, immediately run the 48-hour Standard Shopping review. If the owner is unavailable and spend should not continue by inertia, follow the documented rollback procedure and update the worklog.
- Use live Google Ads / Merchant Center readbacks before edits.
- Do not write cookies, auth headers, payment data, or customer PII to files.

Key evidence packets:
- Measurement pass: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-paid-order-live-capture-3/`
- Paused cleanup: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-paused-campaign-cleanup/`
- Activation gate/execution: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-standard-shopping-activation-gate/`
- $20/day test: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-standard-shopping-20usd-budget-test/`
- Brand Search cleanup/gate: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-brand-search-paused-cleanup/`
- Brand Search quality cleanup: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-brand-search-quality-cleanup/`
- Brand Search asset quality pass: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-brand-search-asset-quality-pass/`
- Account-level asset cleanup: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-account-level-asset-cleanup/`
- Final Brand Search live readback: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-final-readback/`
- Brand Search RSA repair/enable: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-rsa-repair-enable/`
- Brand Search `$5/day` readback: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-5usd-readback/`
- Brand Search external-review expert pass: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-expert-pass/`
- Brand Search fresh premium assets: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-fresh-premium-assets/`
- PMax/Remarketing repair pass: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-remarketing-repair-pass/`
- PMax Shopping replacement-readiness packet: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-shopping-replacement-readiness/`
- PMax T-Shirts local readiness repair: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-tshirts-readiness-repair/`
- Remarketing policy-safe RDA repair: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-expert-repair-audit/`
- Remarketing warm launch-control repair: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-launch-control-repair/`
- Shopify vendor URL cleanup: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-203731-shopify-vendor-url-leak-cleanup/`
- Standard Shopping supplier-domain cleanup/readback: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-standard-shopping-reactivation-readback/`
- Standard Shopping approved re-enable readback: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-standard-shopping-reenable-approved/`

Your immediate first task:
1. Read `ops/AGENT_COORDINATION.md` and confirm there is no active lock conflict for the work you intend to do.
2. Determine whether the 48-hour Standard Shopping review deadline has passed relative to the current date/time.
3. If it has passed, run the Standard Shopping review read-only while the lock remains active. Escalate for owner lock clearance/transfer before any rollback, budget, pause/unpause, product-group, Merchant Center, feed, or conversion-goal edit.
4. If it has not passed, confirm Standard Shopping remains enabled only at the approved `$20.00/day` test settings and that no supplier-domain or inactive-product exposure has reappeared. Any further paid action still requires fresh owner approval.
5. Monitor Brand Search at `$5.00/day` for first impressions/clicks/search terms/ad-review status, without raising budget or changing goals.
6. Update `ops/AGENT_WORKLOG.md` and create evidence packets for any action or deferral.
```
