# Earlier marketing work and account access — September 5 reconciliation

Local review completed September 6, 2026 UTC / September 5 EDT. Stage: HANDOFF. This is evidence for the existing `ops/marketing/` command layer, not a replacement strategy or permission to execute historical plans.

**Finding: the earlier AI had real account access and implemented substantial work.** Google Ads API execution receipts, Merchant uploads, Shopify mutation summaries, and the original Pinterest task establish this. The saved history is useful now even though current Google Ads and Merchant access remains unresolved. No account recovery or new live marketing change occurred in this review.

Root integrated two disjoint readers: `/root/historical_google_access_paths` for access implementation and `/root/prior_google_campaign_work` for Google execution/outcomes. Root separately checked the original Pinterest task and Shopify repair summaries. Historical dates below must not be mistaken for current serving, product eligibility, or authority.

## How access actually worked

| Surface | Dated proof of previous access | Current evidence and limit |
|---|---|---|
| Google Ads customer `3990976848`, manager `7001079966` | Official API Basic Access produced 29 historical and 29 forecast rows on May 19. May 20 official API code executed 96 mutations and read back three paused Shopping campaigns, 12 paused ad groups and 12 paused product ads. Earlier browser scripts also used an authenticated Chrome session. | The documented secure YAML still exists with its six documented fields present; the local check says `ready:true`, which means configuration presence only. September 5 refresh failed HTTP400 `invalid_grant`. September 6 00:11:09 UTC manager readback had no linked clients. No authentication retry in this review. |
| Merchant Center `124884876` | Authenticated Chrome/CDP exports and UI uploads worked. May 20 supplemental source `10663204023` reported 4,531 updated and 4,390 matched products. | September 5 exact-account browser access denied. Historical official API alternatives had insufficient-scope/`invalid_scope` failures; no separate working Merchant API grant was established. |
| GA4 property `330266838`, account `88409806` | May 20 browser responses provided 18 transaction IDs after the separate gcloud OAuth path was blocked. | September 5 reporting remains accessible. Its Completed Ads link redirects to the empty Ads manager; Merchant links were empty. A linked Analytics property does not establish current app access. |
| Search Console | Authenticated browser reports and downloaded CSVs exist. | September 5 property reporting was read successfully. No independent GSC API credential implementation was found in the bounded code search. |
| Shopify | April repair records include successful Admin writes and after-state scans, detailed below. | September 5 authenticated reporting and aggregate order reads succeeded. Existing Shopify access is useful for the sales and attribution work that can continue now. |
| Pinterest advertiser `549756244483` | The original task records authenticated reporting, feed/group readbacks, and an owner-approved campaign pause on May 29. | September 5 readback again showed campaign `626758581530` paused and zero recent spend. Site Checkout events are not proof of paid campaign sales. |

Access implementation references:

- `ops/scripts/check_google_ads_api_config.py:66` defines the presence-only check. Credentials remain outside the repo under the documented secure configuration directory; no credential values were copied into this packet.
- `ops/AGENT_WORKLOG.md:40737` records the May 19 API success; `ops/AGENT_WORKLOG.md:42149` records the May 20 GA4 browser transaction export.
- `../2026-05-20-google-shopping-parent-outfit-rebuild/execute_google_shopping_parent_outfit_paused_rebuild.py:26` uses the official Google Ads client and saved YAML; its `GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_LIVE_READBACK.md:9` records executed mutations and after-state.
- `../2026-05-12-google-ads-gb-ca-au-monitoring/monitor_gb_ca_au_readonly_cdp.py:119` documents the old browser-session mechanism. Internal UI `ocid=220823493` refers to the original Ads client, not a different external customer account.
- `ops/scripts/export_merchant_center_source_eligibility_browser_rpc.py:126` documents the authenticated Merchant exporter; the May 20 rebuild packet's `GOOGLE_SHOPPING_PARENT_OUTFIT_MERCHANT_FEED_UPDATE_EXECUTION_READBACK_20260520.md:49` records the upload result.

Three documented temporary Ads Python environments are now absent; `python3.13` is absent from PATH. The system Python can run the configuration checker but lacks the old Google Ads/Google Auth distributions. The bundled runtime remains available for current local work. Recreating a runtime alone would not repair the observed OAuth failure or app-access denial. No installation was needed for this historical review.

There was not one universal, permanent grant for every tool: different surfaces used separate API scopes or authenticated browser sessions. The May 14 `AUTOMATION_CAPABILITY_AND_MERCHANT_CAPACITY_DIAGNOSIS.md` also records tool/runtime limitations despite useful access on other paths. No surviving independent Google grant that resolves today's access problem was found. Why access changed remains UNKNOWN; neither Business Manager linking nor an email notice proves the cause.

## What the earlier plans actually became

| Work | Implemented historical result | Reuse or unresolved issue |
|---|---|---|
| US Standard Shopping | `23802638621`, a controlled cohort of 780 variants across 81 products, was enabled in late April/May after product and source-leak checks. | Later May 20/21 records show it paused. The old May 1 handoff is not the latest status. Original $0.25 CPC settings do not satisfy today's $0.15 ceiling. |
| Brand and US nonbrand Search | Brand `23805046526` had ad, negative and tracking cleanup. May 6 corrected it to $2/day and $0.15 max CPC. US nonbrand `23827590655` was built paused with 12 ad groups, 36 exact/phrase keywords, 37 negatives and 12 RSAs. | May 20 raw export shows both enabled. Reuse the structures and history, then verify current settings and change history. Remarketing `23609373008` was briefly enabled and re-paused for policy limits. |
| International Search | Twelve country shells existed by May 20. GB `23838895360`, CA `23834423669`, AU `23834424182` had three exact keywords and one RSA each enabled May 12, $2/day per country. Italian native `23866684201` launched May 19 with nine exact keywords and four RSAs, $5/day/$0.15 CPC. | GB/CA/AU monitoring on May 14 showed zero impressions, clicks and spend; first-page estimates around $0.65–$0.74 did not support $0.15 viability for those terms. Native long-tail and landing-fit work is reusable; cheaper international conversion costs were not proved. |
| Additional US exact Search | `23866096027` launched May 19 with eight exact keywords and four RSAs, $5/day and a historically approved $0.20 CPC exception. | May 20 export shows `TARGET_SPEND`/learning instead of the initial Manual CPC. The actor responsible for the intervening change is not established. The old exception is not current authority. |
| Parent-outfit Shopping V2 | Mommy `23868645502`, Family `23858920059`, Daddy `23868645508` were created paused, with 12 paused ad groups and ads in total, for a planned 210-parent/4,531-variant hierarchy. | Reduced activation stopped because 22 held rows would still be included. Exact 4,370-item enforcement hit quota during validation; no execution mutation or activation occurred in that attempt. Reuse the enforcement script and held-item lists, not the unfenced label tree. |
| Products with Shopify sales | Retest `23867953136` was created paused May 21: eight products, 19 exact previously sold variants, excluded catchall, $5/day/$0.15 CPC. | This is an existing candidate to refresh, not a paid winner. Organic product sales do not establish paid conversion performance. |
| Pinterest parent catalog campaign | Campaign `626758581530` ran, then was explicitly paused May 29. The later June 1 report for May 18–June 1 records $105.30 spend, 973 outbound clicks, zero Checkout conversions and zero ROAS. | A separate attribution-ready source `3041760890485574219` and groups `4673019914864` / `4673019915037` / `4673019915140` passed June 1 preflight at 210 rows, grouped 99/77/34. The replacement setup and relaunch had not happened. |

Primary Google evidence: `ops/GOOGLE_ADS_CONTINUITY.md:194`; `ops/AGENT_WORKLOG.md:29505`; the May 12 `GB_CA_AU_INNER_ENABLE_EXECUTION_REPORT.md`; May 20 parent-outfit rebuild receipts; May 21 `GOOGLE_SHOPPING_SHOPIFY_SOLD_RETEST_PAUSED_SETUP_FINAL_READBACK_20260521.md`; `ops/AGENT_WORKLOG.md:43503`; and `../2026-05-20-paid-optimization-shopify-ads-truth/google_ads_campaigns_current_status.csv:15`. Use later exact execution/readback records to resolve conflicts with earlier plans.

The original Codex task **Verify Pinterest campaign audit**, ID `019e6ef4-6976-7822-a2b8-327b971dab74`, was read directly through task history. Its final actions agree with the saved May 29 pause, post-pause diagnostics and relaunch packet, and June 1 preflight packets. An external audit pasted into the original user prompt blamed broken tracking; that allegation was not the verified outcome. Checkout receipts from both API and Tag existed, while click-ID quality gaps and missing campaign-source UTMs were documented. Neither proves tracking explains every missing sale.

## Results and completed repairs to preserve

The May 20 Shopify/Ads truth audit covers April 22–May 19: **184 Google clicks and $33.12 spend**, zero Ads conversions and zero Shopify-classified Google paid orders. Shopping supplied 158 clicks/$30.62; Brand supplied 26/$2.50. Of Shopping traffic, 154 clicks/$29.79 went to products with no Shopify sales in that window. GA4 recorded 18 transactions/$1,113.53 versus Shopify's 23/$1,596.06, so channel revenue was not accepted as reliable optimization truth. Source: `../2026-05-20-paid-optimization-shopify-ads-truth/PAID_OPTIMIZATION_FROM_SHOPIFY_ADS_TRUTH_2026-05-20.md:19`.

Pinterest's June 1 report shows inexpensive outbound traffic, approximately $0.108 per click, without reported paid purchases. This is evidence against treating cheap clicks alone as success. Attribution gaps limit diagnosis; they do not justify inventing sales or concluding the pixel is the only cause. Historical results are not September performance estimates.

Root directly checked the four April Shopify JSON receipts under `ops/reports/`:

- `pinterest-catalog-fix-2026-04-29-clear-invalid-live-summary.json`: 3,220 invalid compare-at-price updates across 129 scoped products, 3,220 successes, zero failures. The corresponding `post-price-verification-summary.json` reports zero remaining targeted changes. This is the active Online Store-and-Pinterest scope, not every product in the store.
- `pinterest-description-html-fix-2026-04-29-live-summary.json`: 413 description/translation rows across 28 products applied, zero errors. Its `post-verification-summary.json` reports zero remaining over-limit rows in scope. Preserve the cleanup; do not blindly reapply an old recommendation.

The April 29 vetted Shopify orchestration plan already distinguished implemented repairs from stale suggestions. It also identified the existing official Shopify Pinterest integration; adding a duplicate custom pixel was not established as a solution. Completed feed grouping, parent images, source sanitization, localized storefront work and the current command layer are assets to verify and retain.

The April economics documents used a 50% non-marketing-cost assumption and roughly 6.67x target ROAS. A Shopify cost field populated as price times 0.5 is still an assumption unless reconciled to fulfilled product/country costs. This review does not certify those margins, shipping performance, 30% net profit, or realized growth.

## How this changes the ongoing turnaround

1. Continue from the existing campaign IDs, sold-item joins, country keyword files, feed validators and isolated Pinterest source. Create new structures only when a current gap justifies them.
2. Refresh purchase/source/value reconciliation from currently accessible Shopify and GA4. Combine actual country/product costs and unrecovered returns with the historical sold-product candidate to choose a defensible pilot. Google access recovery remains a dependency for current Google inventory and settings.
3. Reject the demonstrated failure modes: head terms that do not serve at the CPC ceiling, held-product leakage, settings drift, unsupported tracking diagnoses, and traffic-only success claims. Preserve localized organic demand and verified product/checkout strengths.

Current authority remains in `ops/marketing/current_marketing_state.md`: `READ_ONLY_MARKETING_RECONCILIATION`, stale full-account evidence, no campaign or feed write scope. The exact Google support request is separately already approved and still NOT SUBMITTED; its existing form-validation gate and manual owner input are unchanged. No new approval is requested by this historical review.

Continue through `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, the latest relevant worklog anchor, and `LOCAL_VERIFICATION_AND_HANDOFF.md`. The report is indexed in the current digest and handoff so another session can recover what was done without reopening every old task. This review does not claim an exhaustive audit of every historical file or fresh verification of all live accounts.

Verification: independent review PASS after two factual wording corrections; current-anchor compile OK; handoff17/17; integration25/25 with0 risks; strict CONTINUITY_OK; scoped diff PASS. The seven frozen compiler/scorer/prompt/test/holdout sources are unchanged. Final check receipt is `prior_work_reconciliation_checks.json`. No live action or restored Google access is asserted by these local checks.
