# Google Ads turnaround audit — 2026-09-05

Confidence: M. Status: PARTIAL. Current operating-account access is BLOCKED; historical analysis and a local campaign build sheet are complete. No campaign, spend, credential or conversion settings changed.

## What the evidence actually proves

The assigned Chrome test tab `475224108` is manager `700-107-9966`, not operating customer `399-097-6848`. Accounts > Performance, Aug 8–Sep 4, all account statuses and Level All, returned zero linked accounts. This is not evidence of zero store-account spend. The manager reports Eastern time; the historical operating account reports America/Los_Angeles.

The secure config checker passed presence checks. `python3.13` and the documented temporary Google Ads runtimes are absent. A bounded standard-library REST probe followed official [Google API reporting](https://developers.google.com/google-ads/api/rest/common/search) and [authentication](https://developers.google.com/google-ads/api/rest/auth) documentation. Sandbox DNS initially failed; the approved network escalation reached Google OAuth and returned HTTP400 `invalid_grant` at **2026-09-05 22:42:10 UTC**. No Ads query was sent after that authentication failure. See `google_api_access_readback.json` and `google_readonly_probe.py`.

After the owner asked us to recover account information from project files, one navigation used the documented operating-account URL (`ocid=220823493`, GB campaign `23838895360`). It redirected to manager `700-107-9966`; the operating account was not reached. No Google identity switch or authentication bypass occurred.

Current operating-account 28d/90d spend, enabled entities, conversions/value, keyword Quality Score, RSA status, search terms, bid strategy, conversion goals/counting and product/feed health are UNKNOWN. No current winner or market affordability claim is defensible.

## Keep, fix, retire

**Keep:** the existing canonical command layer; the $0.15 cap; exact product fences and excluded Shopping catchalls; separate country/language lanes; purchase/value reconciliation; public landing checks; small hypotheses instead of bulk activation. The work is not starting from zero.

**Fix:** restore the correct account read; bind campaigns to current product-country contribution margins and an explicit maximum daily exposure plus total test loss; refresh the existing enabled/paused inventory and overlap before building more. Campaign names containing PAUSED were historically enabled, so names are not status evidence. The historical $0.20 US test cannot be reused as permission above the current $0.15 limit.

**Retire as decision rules:** cheap traffic implies profit; translated pages imply viable paid markets; historical GREEN means launch-ready; zero visible search terms means no waste. Google exact match includes same-intent variants, and redundant keywords do not make an advertiser bid against itself in a single Search auction. Our overlap discipline protects routing and learning. [Google matching guidance](https://support.google.com/google-ads/answer/7478529?hl=en)

## Historical performance — stale, not current

The Apr 22–May 19 export has **135 campaign rows, 184 clicks and $33.12 cost**. Standard Shopping `23802638621` produced **158 clicks/$30.62**; Brand `23805046526` produced **26 clicks/$2.50**. The saved Shopify attribution join found **0 Google-paid orders/value**. That is a historical attribution result, not proof that attribution was complete. Ads conversion columns are explicitly labeled untrusted.

The top200 search-term export contains only two brand terms; it cannot justify new negatives. Brand Exact ad group `198796260409` has keyword IDs `447393692138` (dress like mommy) and `548385971753` (dresslikemommy). Small brand spend proves neither profitability nor incremental acquisition. Current negative upload rows: **zero**. [Google search-term guidance](https://support.google.com/google-ads/answer/7102466?hl=en)

Historical GB `23838895360`, CA `23834423669`, AU `23834424182`, and US nonbrand `23827590655` had zero impressions in that window. These require same-day serving/auction diagnosis after access returns. The May19-created US `23866096027` and Italy `23866684201` rows alone do not prove a full 24h failure.

The May21 Shopify-sold Shopping retest already exists historically: campaign `23867953136`, ad group `197311220552`, product ad `809575752934`; all were paused, 19 exact item-ID units, $0.15 Manual CPC, $5 average daily budget, one excluded catchall. Its 8-product cohort is worth refreshing before a broad rebuild. Do not duplicate or enable it from old evidence. Older Standard Shopping ad group/ad IDs are `196252589739` / `807076785262`.

## Concrete next test candidate

`google_campaign_buildsheet.json` contains one US English mother-daughter photo-dress campaign hypothesis: six exact candidate keywords, three held phrase alternatives, eight headlines, three descriptions, CPC/network/geo controls, overlap gates and stop/scale criteria. All headlines pass 30 characters and descriptions pass 90. No entities were created; candidate campaign/ad-group/ad/keyword IDs are null.

The current CRO peer observed `/collections/mommy-and-me` rendering in US/USD, but dress cohort purchasability, role/style availability and source-cleanliness are still pending. Final URL remains unset until those checks pass. Copy makes no unsupported shipping, inventory, promotion, material or review promises. Overseas selection stays open pending current CPC, native-language, delivery, duties and product-country margin evidence. [Presence targeting](https://support.google.com/google-ads/answer/1722038?hl=en) limits the geographic hypothesis; it is not perfectly accurate.

The owner subsequently answered $50; parent limits initial aggregate paid-test exposure to **$50 total**, with no recurring interpretation. This is an initial test allocation, not a permanent ceiling: the owner wants $500 or more available when results justify it. Each higher stage needs a recorded amount/window and reconciled profitable purchases. Google campaign allocation and daily exposure remain unset. Google's usual daily billed limit is 2× average daily budget, so a stated $5 daily loss ceiling cannot automatically become a $5 average daily budget. Bid adjustments also affect effective bids. [Budget limits](https://support.google.com/google-ads/faq/10286469?hl=en), [bid adjustments](https://support.google.com/google-ads/answer/2732132?hl=en)

The owner clarified that 50% of sale covers all costs except marketing and returns. A 30% final-profit goal therefore leaves at most 20% for marketing plus return losses. 650% ROAS consumes 15.38%, leaving 4.62% for return losses. It does not guarantee 30% net profit. At $50 AOV and 650% ROAS, CPA allowance is $7.69 and $0.15 CPC requires 1.95% conversion; these are conditional arithmetic, not a forecast.

## Handoff

Decision: prepare exact approval packet; hold account writes because no action is currently valid. Next action: restore read access to `399-097-6848` or explicitly identify its replacement, because actual account state controls every paid decision. Parent owns canonical updates and independent verification. Continue with `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, linking this packet; no separate operating system is needed.

Checks: CSV aggregation; API configuration presence; OAuth probe; local RSA lengths; Python AST; owned-file diff whitespace check. Source aggregates and exact historical rows are retained in `google_evidence_summary.json`. Historical source packet: `2026-05-20-paid-optimization-shopify-ads-truth`; retest source: `2026-05-21-shopify-sold-product-paid-retest`.
