# Google Ads 2026: Dress Like Mommy implementation playbook

Research checked: **2026-09-11**. Status: **measurement configuration repaired and installation verified; campaign strategy remains a proposal**. Confidence: high in the bounded repair and platform mechanics; medium in campaign selection until actual economics and purchase acceptance are verified. The root operator owns live evidence and changes.

Labels: **Requirement** = platform/policy; **Practice** = evidence-supported operation; **Judgment** = context-dependent recommendation; **Experiment** = unproved business hypothesis. Sources were checked on the research date; undated Help pages have no established publication date.

## 1. Executive recommendation

**Judgment, updated for live findings:** reconcile the **existing Performance Max campaign first** and complete purchase verification. A temporary pause is proposed but awaits the owner's exact approval; it is not reported completed. Do not create or relaunch a campaign from this report. The current command layer preserves a **USD0.15 CPC ceiling**, approximately **6.5× ROAS**, and **30% all-in profit** objective. No qualifying hard CPC control has been verified for the existing PMax campaign. After economics and measurement pass, one tightly scoped Manual CPC Search test is the provisional candidate; Standard Shopping is a credible alternative after Merchant approval and equivalent cost controls. Product photographs and visible prices support Shopping's candidacy, not a guaranteed profit advantage. PMax retention requires resolving its actual controls against the owner's constraints or a separately approved change to those constraints. [Manual CPC mechanics](https://support.google.com/google-ads/answer/2390250?hl=en), [Shopping mechanics](https://support.google.com/google-ads/answer/2454022?hl=en_us_us)

Dress Like Mommy is a dropshipper without a physical store or owned inventory. Verify supplier fulfillment capacity. Existing Shopify sales may inform product choice despite Google Ads' cold start. [Project direction](/Users/fsuels/Projects/dresslikemommy/VISION.md)

Largest threats: selecting the wrong Ads account, replacing established tag settings, double-counting purchases, weak contribution after returns and shipping, and paying for existing brand demand. The repository's approximately 650% ROAS ambition is a business objective, not an evidence-based initial bid setting or present spend authority.

## 2. Essential questions and explicit assumptions

Resolve these six grouped inputs through authorized read-only evidence before asking the owner for unavailable facts:

1. Which country, language and currency should be first, and which additional markets are essential?
2. What are the approved total advertising budget, maximum testing loss and tolerable single-day exposure?
3. Which products have confirmed supplier availability, landed costs and defensible delivery promises?
4. What does existing Shopify order history show by product, market, new customer, cancellation and mature return cohort?
5. What are discounts, shipping collected/paid, payment fees, refund losses, return handling and desired contribution after ads?
6. What are the visible Ads customer ID, Merchant account/domain claim, GA4 property, tag destinations, campaign statuses and consent implementation?

Known URL: `dresslikemommy.com`. Provisional assumptions: a small approved cohort and one market will be selected; no budget, conversion rate or margin is assumed. The supplied URL's `ocid=8520129103` is **not a Google Ads customer ID**; current native readback establishes customer650-997-2886. Standing paid control remains `STALE_READBACK_REQUIRED`, approved scope `NONE`; purchase receiver acceptance remains unresolved after earlier GA4 cleanup. The separate [September11 research packet](../2026-09-11-google-ads-cold-start-research/REPORT.md) has already verified useful Shopify aggregate order/product/customer history. Reuse its dated results and the existing cost pilot; do not treat the store as having no sales or reclassify report totals as verified paid acquisition.

**Current execution note — root native readback through 2026-09-11 18:11 UTC; no independent native replay:** the visible Ads account is **650-997-2886**. Existing **Campaign #1 / 24247604341** remains **ENABLED**, Performance Max, configured **$5/day**. Its latest settled status is **Pending — All asset groups under review**, superseding the earlier Eligible (Learning) observation. Its September6–11 report showed zero impressions, clicks, purchases and spend; this is a dated report, not proof it cannot begin spending. Present budget/loss authorization remains unknown. The owner question about a temporary pause is pending; no relaunch or alternative-campaign creation is authorized.

Before repair, the detector did not find `AW-18433316477`; the Shopify app showed GA4 and Merchant tags only. Root saved the separate AW tag and mapped only **Checkout completed** to existing Purchase **7760272273**, label `DTaoCJG3sfQcEP2s2NVE`. Full reloads verified both changes and all preserved destinations. Google then detected the installed tag and signup completed. A fresh Purchase settings reload still shows **Primary / Every / dynamic values / USD1 fallback / Enhanced Conversions Not configured**. The older pixel configured for `AW-853411529` is preserved. **Configuration and base-tag installation are verified; genuine Purchase receipt, dynamic payload, consent and deduplication remain open.** [Execution evidence](READBACK.md)

## 3. Research findings

| Capability | What is established as of this research | Simplest useful decision |
|---|---|---|
| Campaign total budgets | **2026 expansion:** Google says it expanded these to Search, Shopping and Performance Max earlier this year. Current Help confirms new campaigns only, 3–90-day durations, no daily spending limit, and an unchangeable budget type. [Announcement](https://blog.google/products/ads-commerce/bidding-budgeting-google-marketing-live-2026/), [current requirements](https://support.google.com/google-ads/answer/10486938?hl=en-GB) | **Judgment:** useful for an approved total-loss envelope only if rapid exhaustion is acceptable. Verify the option in this account. |
| AI Max for Shopping | Announced April 30, 2026: text customization, final URL expansion and format selection. Announcement does not establish this account's availability. [Google](https://blog.google/products/ads-commerce/ai-max-for-shopping/) | **Experiment later:** preserve a baseline; preview product truth and destination changes first. |
| AI Brief and Search experiments | April 30 announcement described an English rollout over coming months. August 20 announced multi-campaign budget/ROI experiments rolling out in September. [AI Brief](https://blog.google/products/ads-commerce/ai-max-new-features/), [experiments](https://blog.google/products/ads-commerce/ai-max-testing-planning-tools/) | **Experiment later:** confirm account, language and campaign eligibility. Guidance is not a guarantee against false claims. |
| Asset Studio improvements | May 20 announcement described global English rollout during summer, including multimodal creation/testing. Full availability here is unverified. [Google](https://blog.google/products/ads-commerce/asset-studio-updates/) | **Judgment:** draft previews only; reject invented fabric, fit, package contents or altered garments. Real product imagery comes first. |
| AI Mode formats / Direct Offers | May 20 article calls new formats tests and Direct Offers a pilot; several additions were forthcoming. [Google](https://blog.google/products/ads-commerce/google-marketing-live-search-ads/) | **Not a launch dependency.** No assumption of country eligibility, access or native-checkout availability. |
| Performance Max visibility | Channel reporting and campaign negative-keyword controls were already developing in **2025**; they are not wholly new 2026 inventions. [August 7, 2025 update](https://support.google.com/google-ads/answer/16451273), [current reporting](https://support.google.com/google-ads/answer/16260130?hl=en) | **Practice:** use these if PMax is tested; channel reporting does not provide independent channel budget control. |

Established practices remain: accurate products, purchase-only goals, coherent landing pages and conservative economics. No researched source proves a universal best campaign, achievable 650% ROAS, compulsory conversion count for every automation, or fixed learning spend. Google's aggregate uplifts do not establish this store's profit.

Independent original evidence supports caution about attribution: eBay field experiments found brand advertising could receive credit without measurable short-term lift. This is a mature marketplace study, not a 2026 apparel forecast; use its experimental logic, not its estimated effect size. [Blake, Nosko and Tadelis, May 2014 working paper; published 2015](https://www.nber.org/papers/w20171)

## 4. Profitability model

**Judgment; accounting definitions:** use original-order cohorts, retain cancelled/refunded orders in the denominator, and measure after the return window or apply an explicit provisional return reserve. Exclude collected sales taxes/VAT; account for nonrecoverable duties/taxes as costs. Never subtract discounts or refunds twice.

For a cohort:

- `R = merchandise receipts after discounts − merchandise refunds + shipping collected − shipping refunded`, excluding taxes.
- `V = product/fulfillment/outbound shipping/payment/return costs − realized supplier credits or recoverable product-cost credits`.
- `CM = R − V`; contribution margin rate `m = CM / R`.
- Break-even advertising CPA per original order `= CM / N`.
- Target advertising CPA `= (CM − desired contribution after ads) / N`.
- Break-even business ROAS `= R / CM = 1/m`; target business ROAS `= R / permitted ad spend`.
- Contribution after ads `= CM − ad spend`. Fixed overhead and income taxes remain outside this contribution measure.

For acquisition CAC, use a cohort of **new customers' first orders** and divide by those acquired customers. Do not divide all-order contribution by only new customers. Count a recovered product or supplier credit once, only when realizable; an unsupported resale assumption has zero credit.

**Project constraint:** 30% all-in profit is stricter than an arbitrary positive contribution target. On a common retained-revenue basis, let `H` be allocated overhead and other costs excluded from V. Permitted advertising is at most `min(R/6.5, CM − H − 0.30R)`, and must also fit the approved cash/loss envelope. A nonpositive or unknown result means no economically qualified amount. Platform ROAS may use a different revenue basis; do not compare those numbers without the conversion below. [Current project constraints](/Users/fsuels/Projects/dresslikemommy/ops/marketing/operator_cockpit.md)

**Hypothetical first-order example:** per customer, $80 merchandise less $8 discount, $12 expected merchandise refunds, plus $5 shipping collected less $1 refunded gives **$64 R**. Product cost $28 less $3 realized recovery, outbound fulfillment/shipping $8, fees $2.40 and return handling $1.60 gives **$37 V**. Thus CM is **$27**, or **42.19%**. A $10 desired contribution leaves **$17 target CAC**; break-even business ROAS is **2.37×**, target **3.76×**. For 100 such customers, $1,700 advertising leaves $1,000 contribution before overhead.

Google's Shopify purchase value includes discounts but excludes shipping/taxes; the documented change dates to April 24, 2025. It does not establish automatic refund correction. The example's original Ads value could therefore be **$72**, producing platform thresholds of **2.67× break-even** and **4.24× target**, if attribution and counts matched. Actual targets need the observed value basis and adjustments. [Shopify event parameters, updated July 28, 2026](https://developers.google.com/tag-platform/gtagjs/reference/shopify-event-parameters)

The generic $17 CAC example does **not** meet this project's 30% target. Even with hypothetical H=0, the 30% constraint leaves at most `27 − 0.30×64 = $7.80` for ads, implying **8.21× business ROAS** or **9.23× platform ROAS** at $72 reported value. Actual overhead or additional costs lower that allowance further. None of these hypothetical amounts authorizes spending.

`Maximum test spend ≤ min(cash remaining after obligations, approved loss limit − setup costs − variable-loss reserve)`. Do not credit predicted sales against this protection. Hypothetically, a $500 loss limit and $100 reserve permits at most $400 advertising, not a recommended budget.

Attributed ROAS credits interactions; blended results compare all-store retained contribution with all marketing costs; incremental results estimate what advertising caused beyond the counterfactual. None substitutes for the others. Observed repeat-purchase contribution may later inform acquisition limits; speculative lifetime value cannot justify initial losses.

## 5. Recommended account blueprint

**Current account first:** audit Campaign #1's purchase goals, Merchant cohort, assets, geography, destinations and budget exposure. Complete the approved tracking repair and resolve the pending pause decision before campaign changes. The configured $5/day is not a supplied budget authorization. Compare retain/repair versus replacement in a reviewable packet; do not run overlapping campaigns to resolve uncertainty.

**Judgment:** choose the smallest cohort with positive conservative contribution, clear purchase intent, usable sizes, low fulfillment uncertainty and relevant seasonal timing. Use existing retained sales where available. Exclude unpublished drafts, poor size availability, unverifiable claims, unusually costly shipping and loss-making variants. Separate products only when economics or a decision needs a separate budget.

**Shopping replacement candidate, only after separate authorization:** one campaign, a few product groups for contribution bands, a deliberate inclusion label and “everything else” excluded. Prefer Manual CPC when the existing USD0.15 ceiling remains binding; verify all modifiers and features that can increase bids. A supported capped Maximize Clicks configuration is only an alternative after exact control review. The ceiling is the lower of USD0.15 and target CPA × a conservative, explicitly uncertain conversion-rate scenario. These are spending controls, not a profit guarantee. If relevant auctions cannot be reached within the limit, document infeasibility rather than silently increasing it. [Available Shopping bidding options](https://support.google.com/google-ads/answer/10486938?hl=en-GB), [Manual CPC qualifications](https://support.google.com/google-ads/answer/2390250?hl=en)

**Provisional Search candidate:** after measurement, economics, authority and buying intent pass, prepare one small non-brand Manual CPC Search campaign within the existing ceiling. This path can be considered while Merchant approval is unavailable. Use tightly related exact/phrase keywords such as verified family-photo clothing intent, a matching collection/PDP, one strong responsive ad per ad group and truthful sitelinks. Exclude demonstrably irrelevant intents such as sewing patterns or wholesale where unsupplied. Exact/phrase matching still requires search-term review. Initially exclude Search partners and Display expansion where offered. [Search setup](https://support.google.com/google-ads/answer/9510373?hl=en_AU7)

Use approved shipping destinations and presence-based targeting where offered; review actual geography because targeting is imperfect. Language, feed currency and checkout must agree. Report brand separately and exclude it from non-brand tests using supported controls. Defer competitor conquest and international expansion until economics justify them. [Location controls](https://support.google.com/google-ads/answer/1722038?hl=en)

**Later bidding:** verified purchase values make Maximize Conversion Value a candidate; it has no profit-floor guarantee. Set tROAS only when eligibility and sufficiently stable mature results support it. Current generic Help specifies at least 15 conversions in 30 days for Search/Shopping; Shopping-specific Help applies the criterion per Merchant Center ID. This is an eligibility condition, not adequate statistical evidence or a universal rule for all bidding. [General requirements](https://support.google.com/google-ads/answer/6268637?hl=en), [Shopping-specific requirements](https://support.google.com/google-ads/answer/6309035?hl=en-GB)

**Existing PMax review / future comparison:** inspect accurate assets, own-brand exclusions, query/placement controls and final URLs before deciding to retain it. Later comparisons need a disjoint product cohort or supported experiment and separate approval. URL exclusions have exceptions, including the campaign final URL itself. [Brand controls](https://support.google.com/google-ads/answer/13721847?hl=en), [URL limitations](https://support.google.com/google-ads/answer/14337773?hl=en)

Customer lists and remarketing require eligible size, consent and data-transfer authority. PMax audience signals are not targeting restrictions. New Customer Only supports Search/PMax/Shopping/Demand Gen; validate identification first. Do not invent a new-customer value bonus. [Customer Match](https://support.google.com/google-ads/answer/6379332?hl=en), [lifecycle goals](https://support.google.com/google-ads/answer/12080169?hl=en)

## 6. Ordered implementation checklist

1. **Practice:** record visible Ads customer ID, existing campaign status/budget, destination IDs and ownership. Resolve any identity conflict before edits. User handles billing/payment steps.
2. **Practice:** snapshot both tags' settings, destinations and users before addressing the signup warning. Combining affects connected destinations and is not a simple reversible install. Prefer the existing supported Shopify integration after comparing configurations; do not accept “use detected tag” blindly. [Tag management](https://support.google.com/tagmanager/answer/12329709?hl=en)
3. **Practice:** inspect Shopify **Sales channels → Google & YouTube**. Ads conversion setup can be connected without Merchant Center; avoid unnecessary domain transfers or duplicate accounts. Verify the exact account before linking. [Shopify setup](https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/getting-setup/connect)
4. **Practice:** map checkout completion to the verified canonical Ads Purchase action. The current account has one primary Purchase; this repair changed no goal. If a later fresh audit finds competing GA4 purchase imports, prepare the exact separately authorized primary/secondary/custom-goal correction before changing them. Audit automatic account-default actions, including cart/checkout events. Preserve diagnostic funnels without buying toward them. [Integration workflow](https://support.google.com/google-ads/answer/16030792?hl=en), [primary/secondary exception](https://support.google.com/google-ads/answer/10993988?hl=en)
5. **Requirement/Practice:** validate applicable consent behavior through the supported app with controlled denied, granted and revoked traces. EEA requirements are explicit; other jurisdictions need market-specific review. **Enhanced conversions is optional and remains Not configured here**; enabling it needs a separate reviewed data-use decision and exact authorization. Its status alone does not prove whether any customer-data field was transmitted; payload evidence is required. [Google consent requirements](https://support.google.com/google-ads/answer/13695607?hl=en), [Shopify privacy integration](https://help.shopify.com/en/manual/privacy-and-security/privacy/customer-privacy-settings/understanding-customer-privacy-settings)
6. **Requirement:** reconcile Merchant domain ownership, Ads link, policy diagnostics, market, shipping and returns. Check every advertised variant's stable ID, title, image, price and availability. Supply real brand/GTIN/MPN when applicable, never fabricated identifiers. Validate apparel size/color/age/gender and shared parent `item_group_id` against destination-country requirements. [Product specification](https://support.google.com/merchants/answer/7052112?hl=en)
7. **Practice:** test mobile/desktop product → selected variant → cart → checkout; reconcile final shipping cost and delivery/return promises. Free listings can provide eligible visibility without campaign spend; neither listing approval nor impressions prove sales. Promotions require real terms and supported market eligibility. [Shopify channel setup](https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/getting-setup/connect)
8. **Judgment:** prepare the single-campaign settings, economics, exact budget/loss ceiling, start/end conditions and rollback. Launch only after current QA and exact authority agree. Set any automated recommendations to require review where supported; never accept automated budget, bidding or expansion changes solely for an optimization score.

## 7. Prelaunch QA and acceptance checklist

All account-specific checks below are **NOT RUN by this research lane**. Root live evidence may supersede them individually; no blanket pass is implied.

| Check / method | Expected evidence | Launch blocker |
|---|---|---|
| Identity and serving: read Ads header, campaign table, tag destination and links | Matching visible IDs; dated campaign status/budget screenshots | Wrong/unknown account or unauthorized serving |
| Purchase: controlled checkout trace and receiver readback | Correct destination/action, one unique transaction ID, actual currency, discounted value and product identifiers | Missing/wrong/duplicate purchase or receiver unknown |
| Reload/deduplication: revisit confirmation in a controlled test | Same transaction ID; one counted conversion per selected action | New ID on reload or double bidding actions |
| Goals: inspect each campaign's selected goals | Only canonical Purchase contributes to sales bidding | Cart/page view goals or duplicate primary purchases |
| Consent: inspect denied/granted/revoked traces | Actual choices propagate; user data only as permitted | Consent contradiction or unexpected disclosure |
| Feed: compare selected variants in source, Merchant and PDP | Eligible products, matching price/currency/availability, required attributes | Disapproval or customer-truth mismatch |
| Mobile checkout: smallest supported viewport and representative market | Fit/size usable, correct variant, clear total costs and payment flow | Cannot buy intended item or misleading promise |
| Economics and pacing: independently recompute packet | Costs/refund reserve, approved loss ceiling, campaign cap | Unknown economics or unapproved exposure |

**Testing method:** begin with non-purchase diagnostics and existing legitimate order reconciliation. If checkout testing is necessary, use an appropriate isolated test environment first. Owner performs any authorized live transaction; no live-ad click, fabricated conversion, payment by an agent, or simulated production purchase. Record redacted evidence, not customer data. A successful sandbox test proves only that environment; an organic order can prove collection but not paid attribution.

Transaction IDs deduplicate within the **same action**, not separate Google Ads and GA4 purchase actions. [Google deduplication](https://support.google.com/google-ads/answer/6386790?hl=en) Typical published processing windows are 3/15 hours for native Ads and 12/24 hours for GA imports, depending on attribution; buyer conversion lag is additional. [Data freshness](https://support.google.com/google-ads/answer/2544985?hl=en-GB)

Refunds need separate verification: native website conversions can be restated/retracted with matching order ID and action. Retractions can be irreversible; first reconcile locally, verify support/time windows for that action, and read back approved adjustments. GA4 refund recording is not proof of Ads correction. [Adjustment procedure](https://support.google.com/google-ads/answer/7686280?hl=en)

## 8. 30/60/90-day operating plan

**Readiness before an authorized test:** Campaign #1 is already enabled; resolve its exposure and pending pause decision first. The phases below start after current purchase, policy, economics and authority gates pass. Allocate the approved test envelope to one chosen campaign; reserves remain unspent.

**Days 1–14, after authorization:** daily check spend, serving, feed, checkout and purchase integrity. Most campaigns with daily budgets permit charges up to 2× daily and 30.4× monthly; total budgets cap the flight without a daily limit. Alerts are not instant safeguards. [Spending limits](https://support.google.com/google-ads/answer/10486637?hl=en-IE) Stop new spend when realized loss plus conservative unresolved exposure reaches the approved loss ceiling. Zero impressions after 24 hours requires serving/policy/auction diagnosis.

**Days 15–30:** weekly reconcile click cohorts after observed conversion lag, and order cohorts after returns mature. Remove clearly irrelevant queries immediately; pause items for supplier failure, negative contribution or broken pages. Ordinary poor performance needs spend, lag and uncertainty analysis, not “three clicks and no sale.” Test one hypothesis at a time: first product-title/landing relevance, then fit clarity, then bidding. Primary success metric is retained contribution after ads; diagnostics are qualified purchase rate and CPC.

**Days 31–60:** proceed only if collection is reliable, mature contribution meets target and additional risk fits the loss envelope. Test value bidding or a disjoint PMax cohort; do not simultaneously change product mix, creative, bidding and budget. Freeze ordinary edits through a predeclared evaluation window covering conversion lag. Change immediately for technical or financial failures. No positive result from a tiny sample establishes scalable profit.

**Days 61–90:** scale only when marginal cohorts meet the target after return reserves, fulfillment remains reliable and reconciliation holds. Increase one approved budget/cohort at a time; define the next spend checkpoint and rollback before the increase. Hold if only platform ROAS improves, brand share rises or returns erase margin. With sufficient volume, design a powered geographic/control experiment; a simple before/after comparison cannot separate seasonality, promotion and organic demand. [Geo-experiment method](https://research.google/pubs/measuring-ad-effectiveness-using-geo-experiments/)

**Operating dashboard:** spend/cap remaining; original/new-customer orders; retained revenue; contribution before/after ads; mature/new-customer CAC; native Ads value/ROAS alongside business ROAS; return reserve; branded share; purchase/consent/feed health; attribution/return maturity; dated evidence; next decision. Monthly reassess supplier costs, product mix, returns and observed repeat orders. Stop immediately for wrong account, runaway/unapproved exposure, broken purchase tracking or customer-truth failures; otherwise distinguish uncertainty from a proven loss.

## 9. Prioritized strategy matrix

| Priority | Recommendation / rationale | Evidence strength | Effort/cost | Prerequisite / main risk |
|---|---|---|---|---|
| Required before launch | Resolve tag/account identity; one purchase bidding action | Strong platform mechanics | Low–medium | Snapshots; overwrite/duplicates |
| Required before launch | Retained contribution and supplier/checkout QA | Accounting + operational practice | Medium | Real costs; returns/availability |
| Required before Shopping | Eligible, truthful variant feed | Strong requirements | Medium | Merchant claim/source; mismatches |
| Required before controlled test | Reconcile existing enabled PMax and pause decision | Root-reported live status | Low | Owner authority; present spend exposure |
| Worth preparing after audit | One narrow Manual CPC Search test | Context-dependent judgment | Separately approved media | USD0.15 ceiling, measurement/PDP/economics; auction feasibility |
| Worth testing instead | Standard Shopping with qualified offers and equivalent controls | Context-dependent judgment | Separately approved media | Merchant approval and cost control; no overlapping launch |
| After sufficient data | Value bidding / PMax comparison | Verified mechanics; local effect unproved | Medium + test budget | Mature values; brand attribution |
| After sufficient data | AI Max, creative, new-customer and incrementality tests | Availability varies; experimental | Medium–high | Eligibility/consent/power; false claims |
| Not recommended now | All channels, speculative LTV bonuses, paid tracking stack, aggressive expansion | No sufficient case-specific benefit | High complexity/risk | Fragments learning and conceals loss |

## 10. Immediate next actions and source register

**One next owner-facing action:** answer the pending exact temporary-pause request for Campaign #1, because it is already enabled while purchase verification and spend authority remain unresolved. The authorized tracking configuration repair is complete; genuine transaction reconciliation and economics preparation remain separate work.

Continuation: use the [canonical paid-growth prompt](/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md), anchor `2026-09-11-google-ads-tag-repair-verified`, and [the repair handoff](READBACK.md). Preserve the pending pause decision, genuine Purchase gate and exact current authority; this report is not a competing operating prompt.

Sources above checked **2026-09-11**. Help pages are **undated unless noted**; crawl dates are not publication dates.

| Source family | Publication/update provenance | Use / limitation |
|---|---|---|
| Google tag management; Shopify channel setup; migration; conversion goals; consent; deduplication | Undated current documentation | Implementation mechanics; not account readback |
| Google Shopify event-parameters reference | Updated **2026-07-28**; value change **2025-04-24** | Revenue/ID mapping; verify actual payload |
| Merchant product specification; Shopping/Search creation; tROAS; budgets | Undated current documentation | Requirements and controls; interface may vary |
| AI Max Shopping / AI Brief | **2026-04-30** | Announcement; account rollout unverified |
| AI Max testing/planning | **2026-08-20** | September rollout; not universal availability |
| Asset Studio / AI Search formats | **2026-05-20** | English rollout / tests / pilot limits |
| PMax visibility update | **2025-08-07** | Established controls, not invented 2026 novelty |
| Bidding/budgeting announcement | Visible publication date not established | 2026 expansion stated; current Help corroborates mechanics |
| Blake/Nosko/Tadelis original experiment | **2014** working paper; **2015** publication | Attribution caution; mature eBay external validity limited |
| Google geo-experiment research | **2011** | Experimental method; no store-specific power/result |

Review: no invented economics, feature availability or live completion.
