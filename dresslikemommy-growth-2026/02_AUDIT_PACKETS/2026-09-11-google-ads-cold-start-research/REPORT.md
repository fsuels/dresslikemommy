# Google Ads for Dress Like Mommy in 2026

## 1. Executive recommendation

**Prepare one small, non-brand Search experiment for one product occasion and one market, provisionally US/English. Launch only after contribution economics, purchase measurement, account identity, and the exact buying journey pass acceptance.**

Use a compact set of exact and phrase keywords, one or two tightly related ad groups, verified product-page destinations, and Manual CPC (cost per click) initially if the existing $0.15 CPC constraint remains binding. Allocate the first paid tranche to this one experiment. Standard Shopping is the credible alternative when the intended offers are approved, their images and prices accurately represent individual pieces, and a CPC feasibility check favors Shopping. This is a **context-dependent recommendation**, not evidence that Search universally outperforms Shopping or Performance Max.

The rationale is specific to this business: matching outfits need clear explanations of who each piece is for, each piece's price, sizing, delivery, and what is included. Search allows a narrow intent-to-page test while Merchant review is unresolved. Feed approval is required for Shopping, but a Merchant feed is not inherently required for ordinary Search. Search still needs an acceptable website, truthful products, working purchase measurement, and economic approval. [Shopify account connections][1], [Shopping campaign comparison][2].

The main threats to profit are:

- Unknown delivered contribution margin and return costs.
- Bidding toward an old, duplicated, wrong-account, or unverified purchase action.
- Family imagery suggesting a complete outfit bundle when the advertised price buys one piece.
- Weak supplier availability, delivery reliability, or fit information.
- Buying existing brand demand and treating attributed revenue as additional sales.
- Spreading a small learning budget across markets, categories, or automation features.

**Research cutoff: September 11, 2026.** Platform mechanics below were checked against live official documentation and dated announcements. Reported feature availability is distinct from availability in this account.

**Current execution verdict: HOLD paid activation.** This report is a research and implementation artifact. No advertising configuration, campaign, feed, theme publication, payment, or customer-data upload was performed. A temporary product/cart/checkout-entry smoke test was completed and its cart item removed.

## 2. Essential questions and explicit assumptions

Three grouped inputs remain necessary:

1. **Market:** Is the first paid market US/English, or another country/language/currency?
2. **Exposure:** What are the current monthly media ceiling and maximum cumulative testing loss? Does the earlier $0.15 maximum CPC still apply? Which emergency pause actions will be authorized as part of launch?
3. **Economics:** Where are actual supplier costs, outbound shipping, transaction fees, return/refund costs, and supplier recoveries for the proposed cohort? What contribution profit should remain after advertising?

No budget, margin, conversion rate, or future repeat-purchase value is assumed to be a business fact. US/English is a provisional scenario. Current repository controls retain a 30% all-in profit target, approximately 650% ROAS, and the $0.15 CPC ceiling. These are targets/constraints, not measured results or new spending authority. Reconcile their accounting bases before setting bids; the hypothetical 15% contribution example below does not replace the 30% target, which also requires fixed-overhead allocation.

### What was established

| Evidence class | Finding | Decision implication |
|---|---|---|
| LIVE_VERIFIED: Shopify connector | The connected business is Dress Like Mommy. Aggregate sales, product-sales, and new/returning-customer reports for June 13–September 10, 2026 returned existing order history. | A cold-start Ads plan can use store merchandising evidence. It must not describe the store as having no customers. |
| LIVE_VERIFIED: report quality | Skyfade, Sunshine Stripe, and other matching products appear in product-sales history. A blank product-title bucket is also present. Repeat-customer evidence is sparse. | Join candidate sales to stable product/variant IDs and costs. Do not label small-sample sellers “proven winners” or justify losses with lifetime value. |
| LIVE_VERIFIED: access attempt | The supplied Ads route reached a signed-out account chooser in the isolated browser. The configured API refresh returned HTTP 400, invalid_grant, before the Ads query could run. | Current Ads campaigns, spend, goals, links, billing readiness, and account eligibility are unverified. This is an authentication result, not proof of account suspension or an empty account. |
| REPO_KNOWN: newer owning-task live receipt | During this review, the separate signup-tag operator recorded visible customer 650-997-2886 at approximately 17:45–17:52 UTC. Its Ads tag installation detector failed; the guided tag merge was not confirmed. | Reuse that operator's exact-account access. Detector failure is not proof GA4 is absent. Current campaign spending and genuine purchase ingestion still need acceptance. Manager 700-107-9966 and historical 399-097-6848 remain separate identities. |
| REPO_KNOWN, requires live confirmation | Merchant records identify account 513542500 and scheduled source 10727274744, with a reported US/en receiving cohort of 4,923 offers and a pending website review. | Preserve the existing Merchant owner and publisher. Received offers are not the same as approved offers, serving, or sales. Older zero-receipt notes are superseded leads. |
| LIVE_VERIFIED, bounded storefront sample | After exiting the visibly identified draft preview, the Skyfade product page supported Mother / S / Blue selection and a cart line for variant 44083478528097 at $29.99. | This adult US/en route passed a limited buying check; it does not certify the catalog. |
| LIMITATION: checkout | Checkout opened, but retained a draft-preview parameter. Address-dependent shipping, payment completion, and purchase ingestion were not tested. An Amazon Pay control reported unavailable. | Repeat final acceptance in a clean, preview-free context; test only payment methods the store actually intends to offer. |
| REPO_KNOWN: authority | Authoritative paid control is STALE_READBACK_REQUIRED, autonomous action readiness false, external scope NONE. | Research and local preparation may proceed. Current spend authority cannot be inferred from historical campaign approvals. |

The underlying aggregate queries, returned data, access result, and sanitized QA observations are in [EVIDENCE.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-cold-start-research/EVIDENCE.json). The Shopify reports are not a reconciled export of paid, non-test, non-cancelled orders, and do not prove advertising attribution or contribution profit. The older “two orders” operational notes use different windows/cohorts and should not be compared directly with a 90-day sales report.

The newer [signup-tag owner receipt](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/READBACK.md) supersedes a broad claim that normal Ads access is unavailable everywhere. It does not change this research session's failed authentication result or establish a working purchase conversion. Preserve the existing signup-tag, Merchant, GA4 and UX owners; do not start another tag repair from this report.

## 3. Research findings

Classification used throughout:

- **R — Official requirement:** a documented platform or integration rule.
- **P — Evidence-supported practice:** supported by mechanics or assessable evidence, with stated limits.
- **J — Context-dependent judgment:** the proposed choice for this business.
- **H — Experimental hypothesis:** a benefit that must be tested here.

### Established practices that remain useful

Accurate purchase values, consistent item identities, an understandable mobile buying journey, and product-specific economics remain the foundation. They matter more than a platform optimization score. Automation can optimize the information and objectives it receives; it cannot establish an unknown supplier cost or repair an inaccurate product promise.

Search, Standard Shopping, and Performance Max remain viable campaign options. Standard Shopping still supports manual and automated bidding. Performance Max serves across multiple Google channels with automated bidding. It is not inherently restricted to advertisers with mature history, but its broad reach and optimization are a poor first fit when measurement, allowed loss, or product eligibility is unresolved. [Campaign comparison][2].

Enhanced CPC is **not a current Search launch strategy**: Google states it ceased being available for Search and Display during the week of March 31, 2025. Older instructions lower on the same Help page still describe its historical setup; the dated deprecation notice takes precedence. [Enhanced CPC notice][3].

### What actually changed in 2026

| Capability | Verified status and timing | Simplest useful response for this account |
|---|---|---|
| Campaign total budgets | Expanded to Search, Shopping, and PMax in an open-beta announcement on January 15, 2026. Current Google Ads Help supports new campaigns running 3–90 days. Existing campaigns cannot switch budget type. There is a total charging cap and no daily spending limit. | **J:** Consider for a finite pilot only if the owner accepts the possibility of concentrated daily spend. Do not confuse a total cap with daily pacing protection. Check the actual creation screen. [Announcement][4], [current rules][5]. |
| Budget-constrained target bidding | The August 17–27, 2026 rollout changed behavior for affected target-based campaigns. Achieved efficiency can move closer to the entered target; old overachievement is not guaranteed. Target fields and budgets are not automatically changed. | **R/P:** Audit any existing budget-limited tCPA/tROAS settings before resuming them. A permissive target can now be more consequential. [Mechanics][6], [rollout FAQ][7]. |
| Smart Bidding labels | Starting June 2026, target-bearing strategy names were shortened to Target CPA and Target ROAS. The naming change itself did not change bidding behavior. | **P:** Compare actual target, goal, and budget settings, not labels alone. Keep this separate from the August behavior change. [Target ROAS documentation][8]. |
| AI Max for Search | Announced May 6, 2025; 2026 announcements expanded controls and access. It combines broader/keywordless matching, generated text, and optional URL expansion. It is an enhancement layer for Search. | **J:** Start with approved keywords and destinations. Test AI Max later as a distinct expansion experiment after purchase/value and URL controls are reliable. [2025 origin][9], [current mechanics][10]. |
| September AI Max migration | The August 12, 2026 developer notice says campaign-level broad match and standalone automatically created assets migrate during September 1–30. Search-term matching becomes enabled; final URL expansion remains off. Text customization is on for the ACA migration and off for campaign-level broad match. DSA migration is February 1–28, 2027. | **R/P:** Review change history and actual settings. Do not repeat obsolete claims that DSA must migrate in September 2026. [Current migration notice][11]. |
| AI Brief and AI Max for Shopping | April 30, 2026 announcements introduced additional natural-language controls and Shopping expansion. Shopping Help still labels AI Max beta. Text customization can be used without final URL expansion; expansion requires customization and can broaden into text ads/different pages. | **H:** Later test on a fully verified product cohort. Do not assume English rollout announcements prove account access. [AI Brief announcement][12], [Shopping beta mechanics][13]. |
| PMax controls and reporting | Campaign negatives, expanded search-term reporting, and several controls were already 2025 developments. New 2026 SPN reporting/quality changes include January segmentation, February 10 removal of parked domains, and April invalid-activity-credit reporting. | **P:** Use reports to diagnose placement, query, and billed-cost quality. Search/Shopping negatives do not constrain every PMax channel. These controls do not establish incrementality. [2025 controls][14], [2026 SPN chronology][15]. |
| Asset Studio | May 20, 2026 announcements describe improved brief-based editing, video creation, and testing, with global English rollout during summer. | **H:** Use to prepare drafts after confirming availability. Review actual garments, colors, proportions, and set contents before approving any asset. No need for new paid creative infrastructure. [Asset Studio announcement][16]. |
| AI Overviews and AI Mode | Current Help lists English AI Overview ad availability in specified countries including the US. There is no dedicated AI Overview-only targeting, opt-out, or separate performance report. Several AI Mode formats and Direct Offers remain tests/pilots in the May announcement. | **J:** Do not create a separate “AI search” budget or report invented AI Overview ROAS. Ordinary eligible campaigns may participate; special pilots require verified eligibility. [AI Overview rules][17], [GML Search announcement][18]. |
| Shopify native checkout on Google | Rolling out to eligible US stores/US buyers; direct checkout is active by default for eligible stores. Required Merchant, policy and terms conditions apply. Browser GA4/custom pixels do not fire there; server-to-server checkout coverage differs. | **R/J:** Inspect current activation now. Accept any active route separately before relying on purchase totals. Delaying a new test does not mean the route is currently absent. [Shopify Google agentic storefront][19]. |
| Search language targeting | An August 13 announcement schedules removal of campaign-level Search/AI Max language targeting for late September 2026. Search matching follows ad language. PMax follows this on Search; other PMax channels retain campaign language settings. | **R/P:** Align English ad/page content and verify the launch-date UI. An old language field returned by an API will not prove it still restricts Search delivery. This is announced, not verified in this account. [Language transition notice][54]. |

A further useful feed change is **prospective**: current Merchant image documentation announces a minimum of 500 × 500 pixels with enforcement beginning January 31, 2027. Prepare suitable original-quality images, but do not mislabel the future enforcement date as a September 2026 failure. AI-generated images must retain required origin metadata; generated feed titles/descriptions have structured-field requirements. [Product specification][20], [image requirements][21], [structured titles][22].

Journey-aware bidding in the reviewed GML announcement is a **Search lead-generation beta using tCPA**, not a general apparel-purchase recommendation. Smart Bidding Exploration also assumes conditions and risk tolerance that are weak fits here: it seeks expansion and can lower effective ROAS. Do not activate either simply because purchase volume is low. [GML bidding announcement][23], [Exploration FAQ][24].

### What the performance evidence does—and does not—support

**No reviewed evidence establishes a universal winning campaign type for a zero-history Shopify apparel advertiser with this store's constraints.** Official documentation establishes mechanics and availability; it does not establish profit maximization.

Google's AI Max uplift figures are aggregate internal-study claims. Some Search headline study footnotes exclude retail; the Shopping beta evidence is more relevant by category but still does not account for this store's fulfillment costs, returns, or incremental profit. They support testing a hypothesis, not forecasting a guaranteed uplift. [AI Max announcements][9], [2026 controls announcement][12].

A useful independent causal caution comes from Blake, Nosko, and Tadelis's eBay research. The January 17, 2014 Berkeley account describes a 60-day comparison across 68 US markets and substantial substitution toward unpaid channels when paid search stopped. It is old research on a very large established marketplace, so its measured effects cannot be transferred to Dress Like Mommy. Its durable implication is narrower: paid-search attribution can overstate causal sales, particularly around existing demand. The full NBER PDF was inaccessible during this review; the institution's direct research summary was readable. [Berkeley research summary][25].

The Q2 2026 Tinuiti benchmark landing page was inspected, but its accessible page did not provide enough methodology or a cold-start apparel comparison to justify importing its CPC, ROAS, or campaign-type benchmarks into this plan. No benchmark-derived performance promise is used. [Tinuiti report landing page][26].

Unsupported shortcuts to reject include “PMax needs exactly 30 purchases,” “all new accounts should use Maximize Clicks,” “a $0.15 click is profitable,” “650% ROAS guarantees profit,” and “wait two weeks regardless of technical faults or losses.”

## 4. Profitability model

### Define the accounting basis first

Use an order cohort and a consistent currency. For each order define:

- **R:** retained merchandise revenue after discounts and merchandise refunds, plus retained shipping income. Exclude sales tax/VAT collected for remittance.
- **V:** all variable non-ad costs: supplier product charges, outbound freight, fulfillment/handling, duties absorbed by the merchant, payment/FX fees actually retained by processors, return labels, replacements, and variable service costs, less realized supplier credits or economically recoverable product value.
- **C = R − V:** contribution before advertising.
- **A:** advertising cost allocated to that cohort on a consistent tax/credit basis.
- **P = C − A:** contribution profit after advertising, before fixed overhead.

For VAT-inclusive prices, remove the tax liability before computing retained revenue. Include nonrecoverable ad taxes or FX costs in advertising cost; keep recoverable taxes out of both sides. Do not count a cancelled order as revenue. Keep any nonrefundable processing, supplier, or shipping cost associated with cancellation.

A customer refund reduces R. It is not also a second expense in V. Return freight and unrecovered merchandise cost are separate real expenses. If a supplier reimburses a returned product, reduce V once; do not also add the same credit to R. A dropshipped return has **no assumed inventory recovery**: use actual supplier credit or a supportable net recovery value after handling and resale risk.

For immature cohorts, show realized figures and an explicit reserve for expected future refunds/costs. Replace the reserve with realized outcomes as the cohort matures; never subtract both.

### Decision formulas

| Quantity | Formula and interpretation |
|---|---|
| Contribution margin before ads | m = C / R, when R > 0 |
| Break-even cost per order | C / number of distinct eligible orders |
| Break-even acquisition cost | Contribution from the acquired-customer cohort / distinct new customers; for a first-order-only model, use their first-order contribution |
| Practical target CPA | Average contribution per order minus required remaining contribution and a justified uncertainty reserve |
| Practical target CAC | First-order contribution per new customer minus required remaining contribution and uncertainty reserve |
| Break-even business ROAS | R / C = 1 / m, when C > 0 |
| Target business ROAS | R / affordable advertising cost; if required after-ad margin is p, then 1 / (m − p), provided m > p |
| Contribution profit after ads | R − V − A |
| Maximum CPC supported by economics | Affordable CPA × expected purchase probability per paid click |
| Maximum first test exposure | Minimum of explicit media authorization, available cash after operating obligations, and affordable loss allowance after test setup costs/contingency |

CPA and CAC are not interchangeable. A repeat purchase can improve cost per order without acquiring another customer. Do not assign all store revenue to new-customer acquisition or use projected repeat orders to make a losing first order appear affordable.

A target is not a platform guarantee. If the observed conversion rate or auction price cannot support the affordable CPA, reduce cost, improve the offer/journey, select another qualified cohort, or hold the paid lane. Changing a target field does not change the underlying unit economics.

### Clearly hypothetical apparel example

This example is not Dress Like Mommy's margin, price, refund rate, fee contract, or performance forecast.

| Per-order cohort average | Hypothetical USD |
|---|---:|
| Merchandise at list price | 100.00 |
| Discount | −10.00 |
| Shipping charged | +5.00 |
| Tax collected, excluded from revenue | 8.00 |
| Cash initially paid by customer | 103.00 |
| Expected/realized merchandise refunds | −9.00 |
| Shipping-income refunds | −0.50 |
| **Retained revenue R** | **85.50** |
| Supplier product cost | 33.00 |
| Outbound shipping | 12.00 |
| Retained payment/FX fees | 3.20 |
| Return labels/replacement logistics | 3.00 |
| Variable handling/support | 1.30 |
| Realized supplier recovery | −2.00 |
| **Variable cost V** | **50.50** |
| **Contribution before ads C** | **35.00** |

Contribution margin is 40.94%; break-even first-order CPA is $35.00; break-even business ROAS is 2.44×, or 244%.

If the desired contribution after ads is 15% of retained revenue, $12.825 must remain. Affordable CPA is $22.175, about **$22.18**, and target business ROAS is **3.86×**. At an $18 CPA, contribution after ads is $17, or 19.88% of retained revenue. These figures still exclude fixed overhead.

If Google receives $90 of merchandise value before refunds, its displayed break-even ROAS for the same $35 cost is 2.57×. Its target corresponding to the $22.175 affordable CPA is 4.06×. **The same economics produces different ROAS ratios when the revenue bases differ.** Verify the actual integration payload before translating a business target into a bidding target.

If the separate 650% goal remains binding on retained revenue, the example's allowable CPA becomes at most $85.50 / 6.5 = **$13.15**, which is more restrictive than $22.18. If 650% instead refers to Google's unadjusted value, the threshold differs. Resolve that definition; do not silently enter 650% into a new bidding strategy.

Applying the repository's **30% all-in profit target** to the same hypothetical retained revenue is stricter still: $35 − (0.30 × $85.50) = **$9.35 maximum CPA before fixed overhead**, and less after allocating overhead or an uncertainty reserve. That implies at least 9.14× business ROAS before overhead. Neither $22.18 nor $13.15 is an approved launch CPA. Apply all retained constraints on an agreed basis and use the lowest affordable ceiling.

At a hypothetical $0.15 CPC, purchase rates of 0.5%, 1%, and 2% imply CPAs of $30, $15, and $7.50 respectively. A cheap click can therefore be uneconomic.

### Affordable learning and attribution

Suppose, hypothetically, monthly media authorization is $500, cash headroom is $180, total acceptable testing loss is $150, setup costs are $20, and contingency is $30. The first media exposure must be no more than **min(500, 180, 150 − 20 − 30) = $100**. Assume the entire tranche could be lost. Do not release another tranche because the first ran out.

**Attributed revenue** is credit assigned by a reporting model. **Blended business performance** combines all channels' retained revenue, variable costs, and total marketing costs. **Incremental revenue** is the revenue caused by advertising relative to what would have occurred without it. These answer different questions. Keep brand and non-brand results separate, and reconcile customer/order records before judging acquisition. A high brand ROAS alone is weak evidence of incremental profit. [Causal caution][25].

## 5. Recommended account blueprint

Everything in this section is a **provisional local blueprint**, not a change applied to Google Ads.

| Element | Simplest effective first version | Rationale and limits |
|---|---|---|
| Campaign role | One non-brand Search campaign for one verified occasion/product cohort. | **J:** Narrow intent and controlled destination selection suit unresolved feed approval and strict CPC constraints. |
| Market | US presence targeting, English ads and landing pages, USD economics, verified US shipping. | **J:** One coherent market reduces ambiguity. Location targeting is best-effort. Verify the late-September language-setting transition at launch. [Location options][27], [language notice][54]. |
| Products | Start with roughly 3–5 coherent parent products, fewer if only one passes. This is a working shortlist size, not a platform requirement. | **J:** Review sales-history candidates such as Skyfade and Sunshine Stripe, then select on contribution, supplier availability, fit/return risk, and current occasion demand. Do not bundle unrelated categories merely to fill the list. |
| Ad groups/keywords | One or two intent groups; approximately 6–12 tightly relevant exact/phrase candidates overall. | **J:** Avoid fragmentation. These are preparation sizes, not minimums or verified search-volume claims. |
| Initial bidding | Manual CPC where available, no positive bid modifiers, and the approved CPC ceiling. | **J:** Fits a hard per-click constraint and finite discovery. Manual bidding does not optimize profit automatically. Google's supported-strategy table includes Manual CPC for Search. [Bidding reference][55]. |
| Alternative bidding | Capped Maximize Clicks only as an explicitly bounded discovery test when reduced manual work is useful. | **J:** It optimizes clicks, not purchases. Verify the cap, adjustments, and effective bids. [Maximize Clicks][28]. |
| Conversion objective | One verified purchase action for bidding; transaction-specific values and unique order identifiers. Funnel events are observational. | **P:** Scarce purchases are not a reason to bid toward page views or cart events. Review custom goals because secondary actions inside them can still be bid toward. [Goal rules][29], [transaction IDs][30]. |
| Networks | Google Search initially; exclude Search partners and Display expansion where those controls are offered. | **J:** Reduce uncontrolled traffic sources in the first diagnostic tranche. Reconsider using evidence, not an assumption that all partner traffic is poor. |
| Destinations | Exact, approved product/collection URLs; no draft-preview, cart, internal-search, sold-out-only, or irrelevant policy/blog destinations. | **J:** Keep final URL expansion and generated text off for the initial controlled comparison. AI Max can expand beyond the reviewed route. [AI Max mechanics][10]. |
| Brand | Exclude own-brand demand from the non-brand experiment. A separate exact-brand campaign waits for a clear defensive/incremental purpose and its own budget. | **J/P:** Do not blend brand recovery with prospecting performance. This is a proposal, not authority to alter an existing brand campaign. [Causal caution][25]. |
| Audiences | No standalone remarketing launch. Optional observation segments only after eligibility/privacy review. | **J:** Small audiences and sparse repeat behavior do not justify a separate budget or speculative value uplift. |
| Demographics | Do not exclude fathers, grandparents, gifts, or unknown categories based on stereotypes about who buys family clothing. | **J:** Product imagery is not evidence for audience exclusions. Review mature purchase economics before narrowing. |
| Assets | One coherent responsive search ad per ad group initially, with accurate sitelinks and truthful benefit statements. | **J:** Provide meaningful alternatives without filling asset slots with unsupported promises. Add actual-product images only when eligible and approved. |
| Automated recommendations | Review individually; do not auto-apply budget, bid, broad-match, goal, or asset expansion recommendations. | **J:** Account optimization scores are not business-profit tests. |
| Expansion | Test one additional lever at a time using the same economics and reconciled purchase goal. | **J:** Attribute learning to a clear change; do not launch Search, Shopping, PMax, remarketing, and video together. |

**Candidate keyword themes, not validated upload rows:** “matching family photo outfits,” “matching family vacation outfits,” “mother daughter ombre dresses,” and closely related garment/occasion terms that exactly fit the selected landing pages. Validate demand, query meaning, auction feasibility, and current product scope before promotion.

**Negative watchlist:** clearly irrelevant employment, wholesale, rental, sewing-pattern, or download intent when the business does not offer it. Avoid blanket exclusions such as “cheap,” “ideas,” or broad garment words without query evidence. Negative matching can accidentally remove valuable traffic, and search-term reporting is incomplete; assess both disclosed queries and aggregate spend. [Search-term review][31].

**Illustrative ad draft—copy to review, not uploaded:**

- Matching Family Outfits
- Build Your Family Look
- Choose Each Piece & Size
- Skyfade Dresses & Shirts
- Outfits for Family Photos
- Shop Dress Like Mommy

Descriptions:

“Choose coordinated dresses and shirts. Each piece is sold separately.”

“Select each family member's size and color, then build your matching look.”

Use product-specific copy only in its matching ad group. Do not add shipping deadlines, material claims, discounts, reviews, or bestseller language until verified. The actual supplier-backed product appearance should govern images, even when AI helps produce assets.

### When to switch to Shopping or automated value bidding

**Choose Standard Shopping as the first alternative** if the exact offers are approved, stable, and visually unambiguous; their landing variants match; and the auction/economic case is stronger than Search. Use one campaign and simple product groups. Exclude the catch-all outside the explicitly approved cohort. Shopping matching depends on feed information rather than a manually supplied Search keyword list. [Shopping comparison][2], [apparel feed guidance][32].

For value bidding, purchase values must be correct and meaningful. Current general Target ROAS Help specifies at least 15 conversions in the preceding 30 days at conversion-tracking level for Search/Shopping; the Shopping-specific page specifies at least 15 per Merchant Center ID. Confirm the applicable eligibility rule and UI. These are eligibility requirements, not proof of statistically stable economics, and ordinary Shopify orders are not automatically qualifying Ads conversions. [Target ROAS requirements][8], [Shopping-specific rule][33].

Google's preparation guidance is not uniform: the Maximize conversion value page describes 1–2 conversion cycles after value changes; the general activation guide says 3 weeks or 1–2 cycles, whichever is longer; Target ROAS setup tips say 4 weeks or 1–2 cycles, whichever is longer. For this proposed transition, use the conservative **4-week-or-longer lag-adjusted review**, confirm the strategy-specific guidance again, and still require correct values, qualifying volume, plausible economics and approval. This is a planning judgment, not a universal four-week eligibility rule. [Maximize conversion value][51], [general activation][34], [Target ROAS setup][8].

Maximize conversion value without a target aims to use the full available budget and can materially increase spending versus an underdelivering campaign. [Budget behavior][51].

If a hard $0.15 individual CPC limit remains mandatory, do not assume ordinary automated value bidding or PMax satisfies it. A ROAS target is not a CPC ceiling. Verify any supported portfolio controls and their limitations before considering that route.

Customer Match has policy and account eligibility distinctions: unrestricted targeting should not be assumed for a new advertiser. The current policy distinguishes broadly available observation/exclusions from additional capabilities tied to account history and spend. New-customer modes have further mode-specific requirements and imperfect recognition. Use real new/returning reporting first; do not upload customer lists or add arbitrary lifetime-value bonuses. [Customer Match policy][35], [customer lifecycle goals][36].

### Free listings and promotions

**P/J:** Have the existing Merchant owner verify the Free listings card, intended-country eligibility and exact selected offers alongside paid preparation. Free listings may already be enabled; permission or approval does not guarantee display. Track their orders separately from paid clicks and preserve the existing receiving source. Google documents Marketing → Marketing methods → Free listings, but this account's screen was not inspected. [Free listings requirements][52].

**J:** Promotions are optional. Test only a genuine, owner-approved offer that still meets contribution targets after discounts, exclusions and redemption costs. Confirm account/country eligibility, accurate dates and eligible products, and Google's policy/SKU review. Do not invent a sale or describe standard shipping already included in the price as a new incentive. No promotion was created. [Promotions rules][53].

## 6. Ordered implementation checklist

1. **Establish account identity and present exposure.** Verify the operating Ads customer, manager relationship, currency, timezone, campaign inventory, current spending, change history, and linked Merchant/GA4 accounts. Inspect September AI Max migration and budget-limited target bidding. Keep historical account exports as evidence; do not recreate an account or reset historical data. **Output:** dated read-only account map and current settings export.

2. **Confirm permissions and billing readiness.** Check advertiser verification, account policy notices, billing status, and the ability of the named owner to administer the intended account. The owner handles payment/billing changes. Shopify's integration requires appropriate Google account administrative access. **Output:** pass/fail account readiness, without storing payment or authentication details. [Shopify setup][1].

3. **Freeze the economic launch contract.** Calculate retained revenue, disjoint costs, affordable CPA/CAC, monthly ceiling, tranche exposure, and stop criteria. Define revenue basis and attribution windows. **Output:** candidate-level cost sheet and explicit finite launch authorization. Unknown costs remain unknown.

4. **Select and qualify the product cohort.** Join recent sales to stable IDs. Verify source-backed sizing, garment/role options, honest images, sustainable supply, expected dispatch and delivery, return exclusions, and seasonality. Model several pieces in one order without assuming all buyers purchase a whole family set. **Output:** exact parent/variant allowlist and exclusion reasons.

5. **Reconcile Merchant identity and the existing publisher.** Confirm domain verification/claim, business information, ownership, destination eligibility, and shipping/return settings. Preserve the already selected direct-feed route unless a separate reviewed decision changes it. Google & YouTube can handle measurement without replacing the current feed. **Output:** source ID, refresh time, offer counts and selected offer receipts—not just “connected.” [Domain requirements][37], [Shopify connections][1].

6. **Validate feed truth for each selected offer.** Maintain stable item IDs and group genuine variants under a consistent parent item_group_id. Submit applicable size, color, age group, gender, size system/type, identifiers, title, image, price, availability, and correct market/language/currency. Use actual assigned GTINs/brand/MPN; do not fabricate identifiers or use identifier_exists falsely. Confirm the selected variant on the landing URL. **Output:** exact received-offer-to-Shopify-variant join and clean diagnostics for intended destinations. [Product specification][20], [apparel guidance][32].

   Google imagery should accurately show the advertised variant and what its price buys. Do not blindly transfer Pinterest's shared-parent-image convention into Google if it would misrepresent a garment/color. Use additional coordinated-family imagery as context, while making per-piece price and contents explicit. Verify generated-image metadata and structured generated-text fields; do not assume the feed producer preserves them. [Image requirements][21], [title requirements][22].

7. **Reconcile policies and storefront claims.** Align the product page, cart, checkout, policy pages, and Merchant settings. The observed return page excludes swimwear, intimates, final-sale items, and gift cards; a generic “30-day returns” message must not override those exceptions. The shipping page defers exact methods/estimates to checkout. This verifies published wording, not fulfillment reliability or legal validity in every market. **Output:** offer-specific shipping/returns matrix, including customer cost responsibility. [Merchant return requirements][38], [store returns][39], [store shipping][40].

8. **Audit the existing measurement implementation before adding anything.** Inventory Google & YouTube, customer-event pixels, GTM/theme tags, GA4 properties, Ads conversion IDs/labels, and any server sender. Verify the existing migration and duplicate cleanup rather than repeating them. Prefer the supported Shopify/Google integration if it meets requirements. A second generic GTM/GA4 implementation can duplicate tracking. Also inspect Agentic → Google AI Mode and Gemini activation without changing it; include every active checkout route in the map. **Output:** sender-to-destination-to-event map with one chosen purchase source for bidding. [Google migration verification][41], [Shopify GTM guidance][42], [direct checkout][19].

9. **Accept purchase/value/consent behavior.** Check unique transaction IDs, values, currency, items, destination account, primary/secondary goals, consent decisions, and receiver ingestion. Enhanced conversions require correct implementation, customer-data terms, and appropriate consent; an enabled toggle is not acceptance. For EEA/UK/Swiss users, follow Google's current consent requirements and verify defaults, updates, refusal, and withdrawal. US targeting does not prove every visitor is outside those jurisdictions. **Output:** sanitized transaction-level reconciliation and consent evidence. [Google verification][41], [goal rules][29], [transaction IDs][30], [Google consent policy][43], [Shopify privacy integration][44].

10. **Build locally, then review a finite launch packet.** Freeze exact campaigns, ad groups, keywords/negatives, assets, product IDs, URLs, goals, CPC/budget settings, start/end dates, emergency pause authority, and rollback. Validate text lengths and current account settings. The final approval must cover the actual account and numbers. **Output:** a reviewable proposal; no implied permission from the report.

For steps 5–7, fix launch-blocking defects in the chosen cohort first. A minor issue on an excluded product does not justify delaying a qualified Search test indefinitely. An account-wide website restriction, unsafe buying journey, or unreliable purchase goal does.

### Measurement testing method

Start with a no-payment public smoke test for product selection, cart integrity, and checkout entry. Use Shopify's pixel-testing facilities and Google diagnostics for transport/consent inspection. Prefer a separate development/test environment for synthetic event testing. Do not fabricate click IDs, click live ads, replay genuine purchases into primary reporting, or create artificial conversion history.

For production acceptance, reconcile a legitimate order observed after the current tracking cutover. The owner performs any necessary genuine payment; preserve only sanitized order evidence. A controlled test order, if separately authorized and supported, must be identified and excluded from profit/performance analysis and bidding contamination.

Distinguish two gates: **prelaunch functional purchase acceptance** and **postlaunch paid-attribution acceptance**. An organic order can help verify the genuine purchase payload and GA4 ingestion, but does not prove Google Ads credit from an ad interaction. Google Ads does not expose a simple transaction-ID report for ordinary web conversions, so preserve event/destination evidence and use supported diagnostics, upload receipts where applicable, and controlled reconciliation rather than inventing such a screen. [Transaction ID limitations][30].

For refunds, GA4 refund events use the corresponding transaction_id and item information. Google Ads has separate restatement/retraction mechanics for supported conversion actions; verify support for the chosen source and the applicable time window before promising automation. Do not assume a Shopify refund or GA4 refund automatically reduces the primary Ads conversion value. Keep the financial ledger authoritative even where platform adjustments are limited. [GA4 refunds][45], [Ads adjustments][46].

## 7. Prelaunch QA and acceptance checklist

“Verified” below refers only to the stated observation. No full launch acceptance has been granted.

| Critical check | How to test | Expected result and retained evidence | Launch blocker | Status in this review |
|---|---|---|---|---|
| Operating account and current spend | Read customer identity, campaigns, budgets, cost, change history and links. | Dated account-specific export; correct customer, currency/timezone and known exposure. | Wrong/unknown account or uncontrolled current spend. | Own session BLOCKED. Newer owner receipt binds customer650-997-2886; current spend/complete settings remain NOT TESTED here. |
| Billing/advertiser readiness | Inspect owner-visible billing and verification notices without editing. | Eligible account; no unresolved serving/payment restriction. | Restriction or unknown ability to serve. | NOT TESTED. |
| Purchase goal ownership | Inspect all standard/custom campaign goals and sources. | Exactly one intended purchase source drives bidding; auxiliary events do not. | Wrong destination, duplicated goal, or microconversion bidding. | NOT TESTED live; historical setup is not acceptance. |
| Transaction and amount | Reconcile a legitimate post-cutover order to payload and receiver. | Unique non-PII transaction ID, correct tax/shipping/discount basis, ISO currency and item totals. | Missing, static, duplicate, or materially incorrect values/IDs. | NOT TESTED. |
| Duplicate prevention | Review all senders; test supported repeat-delivery behavior in controlled conditions. | Same order is not counted twice for bidding; new legitimate orders remain countable. | Duplicate primary actions or hardcoded ID. | NOT TESTED. |
| Purchase counting | Inspect the chosen purchase action's Count setting and identifier behavior. | Count = Every for purchases, with order-ID deduplication preserving different genuine orders. | One-per-click counting unintentionally discards repeat purchases, or duplicate senders inflate results. | NOT TESTED. |
| Consent/enhanced conversions | Inspect applicable regional defaults, accept/refuse/withdraw paths and diagnostics. | Actual signals follow documented consent choices; no unauthorized personal-data transfer. | Incorrect consent or unknown behavior for target users. | NOT TESTED. |
| Google direct-checkout coverage | Read current Agentic channel activation and trace any active route separately. | Known status and supported purchase/value/consent coverage; storefront GA4 is not substituted. | Unknown active path that undermines purchase/value acceptance. | NOT TESTED; default eligibility does not prove this store's status. |
| Merchant source receipt | Inspect current source timestamp/count and exact selected offer IDs. | Correct receiving source and variant/market/destination join. | Missing or stale selected offers for Shopping. | REPO_KNOWN only; current-session Merchant readback not performed. |
| Shopping eligibility | Inspect diagnostics per selected offer and account-level issues. | Selected destination approved and campaign can use the offers. | Account/offer restriction for Shopping. | NOT TESTED; pending website review reported in repo. |
| Feed/PDP consistency | Open exact feed links, compare selected size/color/image/price/availability. | Every intended offer matches a buyable variant; parent grouping and identifiers are correct. | Misleading price, wrong variant, unavailable item, false identifier. | One product/cart variant checked; full feed join NOT TESTED. |
| Mobile selection/cart | Choose one adult and one child variant; add/remove separate pieces at narrow viewport. | Accurate per-piece amounts, distinguishable roles/sizes, correct cart IDs, usable controls. | Broken selection or wrong item/price. | VERIFIED for one adult Skyfade variant at 390 × 844; child/all-variant coverage NOT TESTED. |
| Desktop presentation | Inspect product image/title/price, controls and sticky UI. | Readable presentation and clear piece-versus-set wording. | Obscured or misleading purchase controls. | LIMITED PASS on one Skyfade page; full desktop flow NOT TESTED. |
| Clean checkout and shipping | Repeat outside all previews; use owner-approved valid test address through appropriate test method. | Correct country/currency, final shipping/tax/total and supported payment path before payment. | Unclear costs, unsupported destination, unavailable required payment method. | PARTIAL: checkout entry only; preview parameter remained. No address or payment supplied. |
| Policy/fulfillment truth | Compare PDP, policies, Merchant and actual supplier/carrier evidence. | Clear return exceptions and realistic supported delivery claims. | Material contradiction or unsupported promised service. | Published wording sampled; operational reliability NOT TESTED. |
| Speed and accessibility | Test selected pages with PageSpeed/field data and keyboard/mobile use. | No functional blocker; track LCP, INP, CLS where reliable data exists, not an arbitrary score alone. | Page cannot load/interact reliably. | Screenshots sampled; formal speed/keyboard evaluation NOT RUN. |
| Refund handling | Reconcile actual refunds to ledger, GA4 and supported Ads adjustments. | Net revenue/costs correct and platform differences explained. | Unknown economics; adjustment gaps must be reserved and explicit. | NOT TESTED. |
| Finite budget and stop control | Review effective budget type, limits, dates, bids, modifiers and named owner. | Worst-case exposure fits cash/loss authorization; pause procedure is executable. | No explicit finite budget/loss authorization. | NOT SET; awaiting essential inputs. |
| Preview and QA cleanup | Verify cart contents and restore temporary viewport/context. | QA cart empty; no order/payment; temporary tabs closed. | Residual test items or contaminated launch evidence. | VERIFIED: zero items/$0.00; viewport reset and prior draft context restored. |
| Real paid attribution | After authorized launch, reconcile genuine paid-click purchases and lagged reports. | Correct campaign/goal/value, explained differences from Shopify. | Block scaling if attribution remains unreliable. | NOT RUN; postlaunch gate. |

Documentation-supported paths, **not live UI verification**: Shopify Admin → Sales channels → Google & YouTube; Google Ads → Goals → Conversions → Summary; Merchant Center's current Help describes Products & store → Shipping and returns. Labels can vary with account and rollout. Use the page search or current navigation when labels differ. No specific Ads screen was inspected in this session. [Shopify setup][1], [conversion-goal navigation][47], [Merchant returns][38].

Reporting delay is not tracking failure. Google's current data-freshness table lists typical Ads-native versus Analytics-import timings of 3 versus 12 hours for last-click and 15 versus 24 hours for other attribution models. GA4 daily processing may take 24–48 hours. Allow for actual conversion delay as well as processing; timestamps, attribution models, cross-device/modelled data, currency and click-date versus conversion-date reporting can all differ. [Ads freshness][48], [GA4 freshness][49].

## 8. 30/60/90-day operating plan

Day counts begin at the **approved launch**, not at account creation or this report. Calendar dates schedule reviews; readiness and evidence determine progression.

### Prelaunch

Close critical gates in dependency order. Leave current account authority unchanged until a concrete launch packet is approved. Use existing purchase history and supplier evidence to choose the cohort. Resolve current serving/spend first once access returns. If another owner's feed or theme work is active, use its receipt and handoff rather than starting a duplicate repair.

### Days 1–14

**Allocation:** one paid campaign receives 100% of the released media tranche. Other paid campaign types receive zero from that tranche. Cash held for future tests is a reserve, not another campaign budget.

**Pacing:** average daily budgets may bill up to twice the daily amount on a day and generally up to 30.4 times the unchanged daily budget in a full month. Budget changes, partial months and campaign types have specific rules. A daily budget is not a fixed test-total cap. [Spending limits][50].

If using a new campaign total budget, verify the 3–90-day window, campaign eligibility, and total charging limit, and accept that there is no daily spending limit. Do not duplicate an existing campaign merely to access this feature before resolving overlap. [Total-budget rules][5].

For a very conservative average-daily test across T days, a planning bound is D ≤ B / (2T), where B is the maximum media exposure, assuming that the documented daily limit applies and the budget is unchanged. This can underdeliver substantially; it is a cash-protection calculation, not a recommended performance budget. Reconcile billed cost and allow for reporting latency.

**Daily:** check spend versus remaining authorization, tracking/consent faults, rejected offers, broken destinations, missing supply, and clearly irrelevant disclosed search terms. Check whether yesterday's data is mature enough to interpret. Log each meaningful change and its reason.

If impressions remain zero after 24 hours, diagnose account/payment/policy status, keyword volume, auction eligibility, feed requirements, bid cap and landing quality that day. Prepare a narrow long-tail or alternative-cohort proposal if justified. Do not automatically raise bids above the approved ceiling or enable broad expansion.

Complete postlaunch paid-attribution acceptance using genuine customer activity. Do not create purchases for the purpose of satisfying an automated-bidding threshold.

### Days 15–30

Review matured click/order cohorts after their relevant conversion delay. Compare actual contribution per acquired order/customer with the target. Inspect query-to-page mismatch, per-piece versus bundle misunderstanding, mobile abandonment, supplier issues and product-specific refunds.

Make one economically motivated change at a time: exclude an irrelevant query, remove an unfulfillable product, clarify an inaccurate asset, improve a landing mismatch, or change a bid within authority. Technical defects can justify immediate action; normal performance uncertainty usually cannot identify which feature should change.

Do not pause a valid campaign solely because an arbitrary number of days elapsed. Conversely, do not exceed the agreed loss budget because the algorithm is still “learning.” With a hypothetical 1% purchase probability, zero orders after 200 independent clicks has probability about 13.4%; it is disappointing but not proof the true rate is zero. The financial stop rule can still require stopping.

### Days 31–60

If measurement, supplier performance and contribution support it, test **one** next step:

- Standard Shopping on the same approved cohort.
- A more appropriate bidding strategy supported by actual value/conversion eligibility.
- One landing/creative proposition that improves buyer understanding.
- One tightly scoped AI Max expansion, with approved URLs and query controls.
- A small, separately measured brand-defense experiment when there is evidence of a business need.

Choose based on the diagnosed bottleneck. Do not run all five. Where an experiment feature can split traffic and there is enough volume, use it; otherwise label sequential comparisons as confounded by seasonality, auction changes and promotions.

### Days 61–90

Scale only if there is reproducible evidence of positive contribution after ads, the accounting basis matches the bidding value interpretation, results are not dominated by one anomalous order or brand demand, fulfillment is dependable, and downside sensitivity remains tolerable.

Release another bounded tranche or expand one dimension—cohort, geography, campaign type, or bid reach. Do not widen all of them together. Verify local shipping, currency, language, consent and returns before adding a market. Use actual fulfilled-order economics rather than speculative lifetime value.

Where volume permits, use a randomized campaign/geo holdout or another credible controlled design to test incrementality. Define the counterfactual, primary retained-contribution outcome, minimum detectable effect, sample/power needs, and interference risks before launch. An underpowered test should end “inconclusive,” not “no effect.” [Causal measurement rationale][25].

### Stop, hold, improve, or scale

| Situation | Decision rule |
|---|---|
| Wrong value/currency, duplicated purchase bidding, broken checkout, major policy defect, unavailable supply, or budget outside authorization | **Immediate protection:** pause affected activity under the exact preauthorized contingency, or have the owner act. Preserve evidence and fix the cause before restart. |
| Cash/loss envelope reached | Stop further exposure even if statistical uncertainty is high. Releasing more money is a new decision. |
| A few expensive clicks or a few quiet days | Diagnose and use lag-aware data; avoid constant changes that obscure cause. |
| Confirmed irrelevant intent or inaccurate product promise | Exclude or correct narrowly within approved scope; no need to wait for statistical significance on a clearly wrong match. |
| Product's retained contribution is persistently negative after costs/returns | Remove or reprice/rework through the appropriate approval path. Increasing sales volume does not fix negative unit economics. |
| Positive platform ROAS but unexplained refunds, brand mix or unknown fulfillment cost | Hold scale. Platform revenue alone does not close the profit gate. |
| Positive contribution in reconciled cohorts, stable tracking/supply, and acceptable downside | Consider a bounded scale test, preserving a comparable baseline and independent review. |

**Leave a campaign alone** when it is technically correct, inside its loss envelope, receiving relevant traffic, and new performance information is still within the normal conversion/return delay. There is no universal safe “20% budget change” rule or universally sufficient learning duration.

### Prioritized experiment backlog

| Priority | Hypothesis | Primary success measure | Prerequisite / reason to stop |
|---|---|---|---|
| 1 | A verified matching-occasion cohort acquires profitable first orders at the allowed CPC. | Retained first-order contribution after ads; acquired-customer CPA. | Measurement, product truth and finite exposure pass. Stop at loss limit or material fault. |
| 2 | Clearer per-piece/fit/shipping information improves qualified buying. | Contribution per paid click and qualified order completion, with return reserve. | Accurate source facts; comparable traffic. Reject a gain that increases returns or misleading expectations. |
| 3 | Better query/product-title fit reduces wasted Shopping traffic. | Retained contribution and relevant-query spend share. | Approved feed and reliable product-level IDs. Do not treat CTR improvement alone as success. |
| 4 | Value bidding improves contribution versus the current strategy. | Contribution after ads at comparable scope; lag-adjusted CPA/ROAS. | Verified values, eligibility, plausible target and changed CPC authority if required. |
| 5 | AI expansion adds valuable non-brand demand. | Additional retained contribution, query/URL quality, new-customer mix. | Reliable baseline, controls, sufficient budget/volume, explicit risk acceptance. |
| 6 | Brand defense or another market adds incremental profit. | Controlled incremental contribution where measurable. | Baseline brand/organic evidence or full localized buying readiness. |

### Compact operating dashboard

Keep one dated operating view with:

- Released media budget, billed/estimated spend, cash exposure and remaining loss allowance.
- Distinct eligible orders and new customers, separated from test/cancelled orders.
- Retained merchandise and shipping revenue, refunds/reserve, actual variable costs.
- Contribution before ads, contribution after ads, CPA per order and CAC per new customer.
- Platform conversion value/ROAS alongside business-basis ROAS; no blended denominator confusion.
- Brand/non-brand mix, attribution confidence, unjoined orders and reporting lag.
- Selected-offer eligibility, purchase-event health, fulfillment/return incidents.
- One next decision, owner and review date.

Use CPC, impressions, CTR, search terms, devices and landing performance as explanations underneath those outcomes. Weekly reviews reconcile cohorts and change logs; monthly reviews mature refunds, fees and cash, reforecast allowable acquisition cost, and reconsider channel allocation.

## 9. Prioritized strategy matrix

Effort is relative operator effort; no new paid app or infrastructure is assumed.

| Priority class | Recommendation | Rationale / evidence strength | Effort or cost | Prerequisites | Major risk |
|---|---|---|---|---|---|
| Required before launch | Account identity/current exposure readback | R/P; correct account and present state are necessary. [Setup][1] | Low after access | Normal authenticated read access | Copying old account settings or missing live spend |
| Required before launch | Actual contribution and loss contract | J; arithmetic is strong, actual cost inputs missing | Medium | Supplier/fulfillment/fee/refund data | Gross revenue mistaken for profit |
| Required before launch | One purchase goal/value/dedup path | R/P; documented goal and transaction mechanics. [Goals][29], [IDs][30] | Medium | Sender/destination map and legitimate order evidence | Duplicated or wrong-account bidding |
| Required before launch | Consent and enhanced-conversion acceptance | R; policy/integration requirements. [Consent][43], [Shopify privacy][44] | Medium | Applicable regional behavior and permissions | Inappropriate data use or signal loss |
| Required before launch | Exact buyer-path truth | R/P; website and return requirements. [Website][37], [Returns][38] | Medium | Approved product facts, clean published checkout | Misleading set price or unsupported delivery |
| Required before Shopping launch | Received and approved exact offer cohort | R; product/destination requirements. [Feed][20], [Apparel][32] | Medium | Existing Merchant owner/source, verified links | Treating receipt or discovery as approval |
| Worth testing at launch | One narrow non-brand Search campaign | J/H; fits present constraints, no universal superiority claim | Finite approved media | All common launch gates, feasible bids | Low volume at hard CPC ceiling |
| Worth testing at launch | Standard Shopping as alternative | J/H; visual discovery can qualify shoppers. [Campaign types][2] | Finite approved media | Additional feed gates | Family image/individual-piece price confusion |
| Worth testing at launch | Campaign total budget for a finite tranche | R mechanics; J use. [Budget rules][5] | Low | New eligible campaign, 3–90 days, approved total | Entire exposure may concentrate early |
| Appropriate after sufficient data | Automated value bidding | R eligibility; H profit gain. [tROAS][8], [Shopping rule][33] | Medium | Reliable values and acceptable target/risk | Restrictive target starves delivery; loose target loses profit |
| Appropriate after sufficient data | PMax or AI Max expansion | Documented controls; H incremental profit. [AI Max][10], [PMax][14] | Medium plus test media | Clean feed/journey, stable economics, exact authority | Broad reach, brand credit, URL/creative drift |
| Appropriate after sufficient data | Remarketing/Customer Match/new-customer modes | R eligibility; J timing. [Policy][35], [Lifecycle][36] | Medium | Consent, eligible lists/modes, adequate audience | Too small or misclassified audiences; inflated value |
| Appropriate after sufficient data | Agentic/direct Google checkout | R path-specific limits; H additional profit. [Shopify][19] | Medium/high QA | Actual store availability and separate measurement | Browser pixels absent; attribution divergence |
| Required before launch | Existing direct-checkout activation check | R default-on behavior; inspect now even if expansion waits. [Shopify][19] | Low after access | Read-only channel status | Assuming an already active buying route is absent |
| Worth testing at launch | Free listings | R eligibility; J low-overhead parallel route. [Free listings][52] | Low/medium | Exact offers, policies and receiving source | Approval mistaken for guaranteed display or sales |
| Worth testing at launch | Genuine promotion, only if justified | R policy/SKU acceptance; H additional contribution. [Promotions][53] | Discount cost plus review | Positive margin after redemption and owner approval | Discount consumes profit without additional demand |
| Not recommended for this situation | Launch every campaign/market; broad Display/video prospecting | J; fragmentation and measurement burden | High relative exposure | No current justification | Little interpretable learning per dollar |
| Not recommended for this situation | Speculative LTV bonuses, page-view bidding, fake conversion history | Weak/invalid support for profitable acquisition | Potentially high loss | None justifies the shortcut | Learns the wrong objective or contaminates data |
| Not recommended for this situation | New paid tracking stack or server-side build by default | J; supported integration should be tested first. [Shopify guidance][42] | Avoidable overhead | Demonstrated native limitation required | Duplicate events, maintenance and data risk |
| Not recommended for this situation | Local-inventory/physical-store campaign strategy | Inapplicable business model | Unnecessary | No physical store/owned inventory | False business claims |

## 10. Immediate next actions and source register

**One owner-facing action goes first: continue through the operator already handling account 650-997-2886's signup-tag setup, and obtain its current-spend and purchase-destination readback.** That task has now recorded exact-account access and a failed Ads tag detector. Reusing its work avoids another sign-in or duplicate tag installation, and identifies existing exposure before any new launch proposal. No passwords or tokens are needed in chat. The source is its dated owner receipt, not a fresh account inspection by this research task.

Then use the existing owners to complete purchase/value acceptance and qualify one costed product cohort. The next paid proposal should specify the exact campaign, audience/keywords or offer IDs, destinations, goals, CPC/budget type, maximum loss, dates and emergency pause authority. The unanswered market/budget/cost questions should be resolved before that proposal is approved. No generic launch approval is requested here because the numerical and account-specific packet is not yet complete.

Continue through the existing [paid-growth continuation prompt](/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md), using this report as research input and preserving the authoritative control, current signup-tag/Merchant/GA4/UX ownership and any newer verified evidence. This report does not replace the marketing command layer or its global One Owner Action; the Ads readback action above is scoped to completing this research handoff.

### Decision and verification record

- Decision ID: DLM-RESEARCH-2026-09-11-GOOGLE-COLD-START.
- Decision status: FROZEN_UNRESOLVED recommendation; no campaign outcome exists.
- Options: proposed narrow non-brand Search; status quo while common launch gates remain unmet; Standard Shopping when feed eligibility and economics favor it.
- Hypothesis: a coherent matching-occasion cohort can acquire first orders whose retained contribution exceeds ad cost within the approved loss envelope.
- Main falsifier: current auction costs and achievable purchase rate cannot meet affordable CPA after actual fulfillment/returns.
- Success: reliable purchase attribution plus positive first-order contribution after ads and the owner's required residual contribution; no material buyer-truth or fulfillment issue.
- Kill: financial exposure reaches the approved bound, technical/consent/policy fault, or credible economics no longer support the test.
- Window/exposure: no active test window or media amount; these require the concrete launch contract.
- Rollback: no live campaign change to reverse. For a future test, a preauthorized pause of the exact campaign ends new exposure while preserving data; incurred spend is not recoverable by “rollback.”
- source_live_evidence_as_of: canonical paid control remains 2026-06-01; scoped Shopify/browser/research observations are September 11, 2026.
- live_state_mode: STALE_READBACK_REQUIRED for paid execution.
- effective_approval_policy: FRESH_ACTION_TIME_APPROVAL_REQUIRED.
- approved_external_scope: NONE for paid execution.
- decision_depends_on_uncertain_state: true.
- decision_changing_evidence: current Ads state, selected-offer approval, real costs/returns, purchase/value/consent acceptance, and CPC feasibility.
- if_evidence_supports_recommendation: prepare the exact finite Search launch packet for approval.
- if_evidence_opposes_recommendation: retain the hold, fix the specific premise, or choose the qualified Shopping/other-product alternative through a new bounded decision.
- material_decision: true.
- independent_verifier: /root/report_verifier; PASS_WITH_LIMITS; see [independent review](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-cold-start-research/INDEPENDENT_REVIEW.md).
- verifier_independence: DID_NOT_BUILD_OR_EXECUTE.
- Outcomes: no incremental traffic, advertising purchases, CPA, ROAS or contribution improvement is claimed from this research or QA visit.

### Source register

All sources below were checked on **September 11, 2026**. “Undated” means no publication/update date was verified; retrieval/crawl dates were not substituted for publication dates. Announcements establish the stated announcement, while current Help and account readback determine practical availability. Source links appear beside the relevant claims.

| # | Publisher and source | Publication/update date verified | Use / limitation |
|---|---|---|---|
| 1 | Shopify — [Set up Google & YouTube][1] | Undated | Account relationships, optional connections, admin path; not account-specific proof |
| 2 | Google Ads — [Shopping and Performance Max comparison][2] | Undated | Campaign reach and supported bidding |
| 3 | Google Ads — [Enhanced CPC][3] | Undated; effective week of Mar 31, 2025 stated | Deprecation overrides historical setup text |
| 4 | Google — [Campaign total budgets announcement][4] | Jan 15, 2026 | Open-beta release; not universal account readback |
| 5 | Google Ads — [Campaign total budgets][5] | Undated | Current supported types, 3–90 days, total/no-daily limit |
| 6 | Google Ads — [Changes to target-based strategies][6] | Undated | August behavior change |
| 7 | Google Ads — [Target-based bidding FAQ][7] | Undated; Aug 17–27, 2026 rollout stated | Rollout completion and affected behavior |
| 8 | Google Ads — [Target ROAS][8] | Undated | Eligibility, naming and value prerequisites |
| 9 | Google — [AI Max for Search announcement][9] | May 6, 2025 | Origin and vendor-study limitations |
| 10 | Google Ads — [How AI Max for Search works][10] | Undated | Matching/text/URL controls |
| 11 | Google Ads Developer Blog — [AI Max migration notice][11] | Aug 12, 2026 | September ACA/broad migration; DSA February 2027 |
| 12 | Google — [AI Max new features][12] | Apr 30, 2026 | AI Brief and rollout qualifications |
| 13 | Google Ads — [AI Max for Shopping][13] | Undated | Beta, text/URL expansion mechanics |
| 14 | Google Ads — [PMax controls announcement][14] | Aug 7, 2025 | Avoid relabeling 2025 controls as new in 2026 |
| 15 | Google Ads — [Search Partner Network updates][15] | Undated; dated 2026 milestones | Reporting/parked domains/invalid activity |
| 16 | Google — [Asset Studio updates][16] | May 20, 2026 | Creative rollout announcement |
| 17 | Google Ads — [Ads and AI Overviews][17] | Undated | Countries, placement/reporting restrictions |
| 18 | Google — [GML Search ads announcements][18] | May 20, 2026 | Tests, pilots, AI Mode and offers |
| 19 | Shopify — [Google agentic storefront][19] | Undated | US eligibility, default activation and native-checkout pixel limitations |
| 20 | Merchant Center — [Product data specification][20] | Undated | Data/identifier/market requirements and prospective image enforcement |
| 21 | Merchant Center — [Image link][21] | Undated | Actual-product imagery and generated-origin metadata |
| 22 | Merchant Center — [Title and structured title][22] | Undated | Variant-specific and AI-generated title rules |
| 23 | Google — [GML bidding and budgeting][23] | No visible publication date verified | Beta/restricted applicability; not general retail eligibility |
| 24 | Google Ads — [Exploration FAQ][24] | Undated | Risk/prerequisite challenge to immediate expansion |
| 25 | UC Berkeley Haas — [Paid-search field-experiment summary][25] | Jan 17, 2014 | Original research team's institutional explanation; mature eBay, not cold-start apparel |
| 26 | Tinuiti — [Q2 2026 Digital Ads Benchmark landing page][26] | Q2 2026 edition; exact release date unverified | Reviewed but not used for performance assumptions; accessible methodology insufficient |
| 27 | Google Ads — [Advanced location options][27] | Undated | Presence versus interest; best-effort targeting |
| 28 | Google Ads — [Maximize Clicks definition][28] | Undated | Click objective and bid-limit control |
| 29 | Google Ads — [Primary/secondary actions][29] | Undated | Bidding treatment and custom-goal exception |
| 30 | Google Ads — [Transaction IDs][30] | Undated | Deduplication scope, count setting, reporting limitations |
| 31 | Google Ads — [Search terms and negative ideas][31] | Undated | Query review; no guarantee every query is disclosed |
| 32 | Merchant Center — [Apparel best practices][32] | Undated | Genuine variants, grouping, size/color attributes |
| 33 | Google Ads — [Shopping Target ROAS setup][33] | Undated | Shopping-specific Merchant-ID conversion requirement |
| 34 | Google Ads — [Value bidding for Search and Shopping][34] | Undated | Conversion values, delays and adoption prerequisites |
| 35 | Google Ads — [Customer Match policy][35] | Undated | Capability-specific account eligibility |
| 36 | Google Ads — [Customer lifecycle goals][36] | Undated | Mode/campaign/bid-strategy prerequisites |
| 37 | Merchant Center — [Online store domain requirements][37] | Undated | Buyable fixed-price products, secure checkout and policies |
| 38 | Merchant Center — [Return policies][38] | Undated | Consistency, disclosure and documented navigation |
| 39 | Dress Like Mommy — [Return policy][39] | Page says Jan 2026 | Published terms only; legal/operational implementation not certified |
| 40 | Dress Like Mommy — [Shipping information][40] | Undated | Published wording; actual delivery performance not verified |
| 41 | Google Analytics — [Verify Google & YouTube upgrade][41] | Undated | Native migration/enhanced-conversion verification |
| 42 | Shopify — [Google Tag Manager][42] | Undated; Jan 2026 auto-upgrade milestone stated | Native integration preference and duplicate tracking risk |
| 43 | Google — [EU user consent policy][43] | Help identifies Jul 31, 2024 Switzerland update | Platform consent duties for EEA/UK/Swiss users; not complete jurisdictional legal advice |
| 44 | Shopify — [Customer privacy settings][44] | Undated | Consent-mode integration and third-party banner compatibility |
| 45 | Google Analytics — [Ecommerce setup Q&A][45] | Undated | Refund transaction/item mechanics |
| 46 | Google Ads — [Conversion adjustments][46] | Undated | Restatement/retraction; selected-source support still needs verification |
| 47 | Google Ads — [Manage conversion goals][47] | Undated | Documentation-level UI path |
| 48 | Google Ads — [Data freshness][48] | Undated | Typical attribution/import delays, not guaranteed per-event SLA |
| 49 | Google Analytics — [GA4 data freshness][49] | Undated | Processing and changing daily reports |
| 50 | Google Ads — [Spending limits][50] | Undated | Average daily and monthly charging limits |
| 51 | Google Ads — [Maximize conversion value][51] | Undated | Full-budget behavior and value-change preparation guidance |
| 52 | Merchant Center — [Free listings][52] | Undated | Official page returned through search; direct open failed; eligibility is not guaranteed display |
| 53 | Merchant Center — [Promotions][53] | Undated | Country/account eligibility and policy/SKU review |
| 54 | Google Ads Developer Blog — [Language targeting transition][54] | Aug 13, 2026 | Announced late-September behavior; actual account transition unverified |
| 55 | Google Ads — [Bidding reference][55] | Undated | Current supported-strategy table; dated deprecations override stale historical ECPC wording |

Private/live sources: the supplied client brief; Shopify shop information and three aggregate ShopifyQL queries preserved in EVIDENCE.json; the bounded browser QA described there; and the current project control/coordination records. No customer records, account credentials, private checkout links, or supplier URLs are included.

[1]: https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/getting-setup/connect
[2]: https://support.google.com/google-ads/answer/2454022?hl=en
[3]: https://support.google.com/google-ads/answer/2464964?hl=en
[4]: https://blog.google/products/ads-commerce/campaign-total-budgets/
[5]: https://support.google.com/google-ads/answer/10486938?hl=en
[6]: https://support.google.com/google-ads/answer/17061251
[7]: https://support.google.com/google-ads/answer/17125145?hl=en
[8]: https://support.google.com/google-ads/answer/6268637?hl=en
[9]: https://blog.google/products/ads-commerce/google-ai-max-for-search-campaigns/
[10]: https://support.google.com/google-ads/answer/15910187?hl=en
[11]: https://ads-developers.googleblog.com/2026/08/migrate-campaign-level-broad-match-and.html
[12]: https://blog.google/products/ads-commerce/ai-max-new-features/
[13]: https://support.google.com/google-ads/answer/17091277?hl=en
[14]: https://support.google.com/google-ads/answer/16451273
[15]: https://support.google.com/google-ads/answer/16286960?hl=en-GB
[16]: https://blog.google/products/ads-commerce/asset-studio-updates/
[17]: https://support.google.com/google-ads/answer/16297775?hl=en-GB
[18]: https://blog.google/products/ads-commerce/google-marketing-live-search-ads/
[19]: https://help.shopify.com/en/manual/online-sales-channels/agentic-storefronts/google
[20]: https://support.google.com/merchants/answer/7052112?hl=en
[21]: https://support.google.com/merchants/answer/6324350?hl=en
[22]: https://support.google.com/merchants/answer/6324415?hl=en
[23]: https://blog.google/products/ads-commerce/bidding-budgeting-google-marketing-live-2026/
[24]: https://support.google.com/google-ads/answer/16294223?hl=en
[25]: https://newsroom.haas.berkeley.edu/research/study-finds-paid-search-ads-dont-always-pay-4/
[26]: https://tinuiti.com/research-insights/research/digital-ads-benchmark-report/
[27]: https://support.google.com/google-ads/answer/1722038?hl=en
[28]: https://support.google.com/google-ads/answer/6336101?hl=en
[29]: https://support.google.com/google-ads/answer/11461796?hl=en
[30]: https://support.google.com/google-ads/answer/6386790?hl=en
[31]: https://support.google.com/google-ads/answer/7102466?hl=en
[32]: https://support.google.com/merchants/answer/7348545?hl=en
[33]: https://support.google.com/google-ads/answer/6309035?hl=en-GB
[34]: https://support.google.com/google-ads/answer/15099424?hl=en
[35]: https://support.google.com/google-ads/answer/6299717?hl=en-GB
[36]: https://support.google.com/google-ads/answer/12080169?hl=en
[37]: https://support.google.com/merchants/answer/12160471?hl=en
[38]: https://support.google.com/merchants/answer/14011730?hl=en
[39]: https://www.dresslikemommy.com/pages/return-policy
[40]: https://www.dresslikemommy.com/pages/shipping-info
[41]: https://support.google.com/analytics/answer/16138144?hl=en
[42]: https://help.shopify.com/en/manual/reports-and-analytics/google-analytics/google-tag-manager
[43]: https://www.google.com/about/company/user-consent-policy/
[44]: https://help.shopify.com/en/manual/privacy-and-security/privacy/consent
[45]: https://support.google.com/analytics/answer/14143583?hl=en
[46]: https://support.google.com/google-ads/answer/7686447?hl=en
[47]: https://support.google.com/google-ads/answer/10993988?hl=en
[48]: https://support.google.com/google-ads/answer/2544985?hl=en
[49]: https://support.google.com/analytics/answer/11198161?hl=en
[50]: https://support.google.com/google-ads/answer/10486637/about-spending-limits?hl=en-GB
[51]: https://support.google.com/google-ads/answer/7684216?hl=en
[52]: https://support.google.com/merchants/answer/13889434?hl=en
[53]: https://support.google.com/merchants/answer/13422697?hl=en
[54]: https://ads-developers.googleblog.com/2026/08/google-ads-language-targeting-changes.html?m=0
[55]: https://support.google.com/google-ads/faq/10286469?hl=en
