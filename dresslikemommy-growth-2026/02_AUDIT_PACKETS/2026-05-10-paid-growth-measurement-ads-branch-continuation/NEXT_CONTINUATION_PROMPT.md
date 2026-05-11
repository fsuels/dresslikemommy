# Next Continuation Prompt

Use the canonical operating prompt at:

`ops/prompts/paid-growth-ai-army-continuation-prompt.md`

Latest anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-measurement-prepurchase-branch-gated`

Start by reading:

1. `AGENTS.md`
2. `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
3. `ops/MEMORY_CONTINUITY_PROTOCOL.md`
4. `ops/PROBLEM_SOLVING_PROTOCOL.md`
5. `ops/PROBLEM_TRACKER.md`
6. `ops/AGENT_COORDINATION.md`
7. `ops/BROWSER_SUBAGENT_COORDINATION.md`
8. `ops/GROWTH_NORTH_STAR.md`
9. the latest `ops/AGENT_WORKLOG.md` entry for the anchor above

Current state:

- Measurement gate has a partial browser pass only: `GB`/`GBP` and `DE`/`EUR` pre-purchase events through checkout entry carried correct currency/value into Google/GA requests.
- Google Ads `Google Shopping App Purchase` readback is clean as the single Primary account-level purchase action with dynamic value settings and recent request evidence.
- The official Shopify Google & YouTube app's non-US `purchase` event remains unproven. No payment/order/refund/cancel occurred.
- Non-US live spend remains blocked.
- Ads build state is `12 built / 3 absent / 2 parked`: built paused campaigns are `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, and `CZ`; absent are `RO`, `PT`, `GR`; parked are `FR`, `BE`.

Next exact gates:

1. Measurement gate: prove a non-US `purchase` event without creating a new order if a genuine order exists; otherwise get exact owner approval for a controlled non-US test purchase/refund/cancel procedure.
2. Ads branch: get exact owner direction to retry `RO` or skip/park `RO` and continue one country at a time with `PT`, then `GR`.

Do not re-upload completed countries. Do not enable campaigns. Do not change budgets, bids, statuses, conversion goals, product scope, feed labels, product groups, Merchant sources, Shopify live product data, Pinterest settings, PMax, or Standard Shopping without fresh exact owner action-time approval.

Useful exact approval wording for the measurement gate:

`APPROVE CONTROLLED NON-US PURCHASE MEASUREMENT PROOF ONLY: RUN ONE LOW-VALUE NON-US TEST PURCHASE FOR DRESSLIKEMOMMY USING A COUNTRY-QUALIFIED STOREFRONT SESSION, CAPTURE TAG ASSISTANT/DEVTOOLS/GA4 DEBUGVIEW EVIDENCE FOR THE OFFICIAL GOOGLE & YOUTUBE APP PURCHASE EVENT CURRENCY, VALUE, TRANSACTION_ID, AND GOOGLE ADS CONVERSION REQUEST, THEN IMMEDIATELY REFUND AND CANCEL THE TEST ORDER IF THE PLATFORM ALLOWS; DO NOT ENABLE ANY CAMPAIGN, DO NOT CHANGE BUDGETS/BIDS/STATUSES, DO NOT CHANGE CONVERSION GOALS/ACTIONS, DO NOT EDIT SHOPIFY PRODUCTS/THEME/CUSTOMER EVENTS, DO NOT EDIT MERCHANT/PINTEREST/ADS SETTINGS, DO NOT CREATE INVENTORY OR LOCAL-PICKUP CLAIMS, AND STORE ONLY SANITIZED EVIDENCE.`

Useful exact approval wording for Ads branch option A:

`APPROVE RETRY RO PAUSED GOOGLE SEARCH TEST BUILD ONLY: FIRST CONFIRM NO RO CAMPAIGN EXISTS AND NO RO BULK-UPLOAD PREVIEW/APPLY IS IN PROGRESS; THEN UPLOAD ONLY RO_intl_search_paused_draft_web_bulk.csv, PREVIEW, DOWNLOAD, AND VALIDATE 88/88 # OK; APPLY ONLY IF CLEAN; READ BACK THE RO CAMPAIGN AS PAUSED SEARCH, PRESENCE-ONLY, CONTENT/YOUTUBE OFF, CPC AT OR BELOW $0.20; DO NOT TOUCH PT, GR, FR, BE, US CAMPAIGN 23827590655, STANDARD SHOPPING, PMAX, MERCHANT, SHOPIFY PRODUCT DATA, PINTEREST, THEME, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT; NO LIVE SPEND.`

Useful exact approval wording for Ads branch option B:

`APPROVE SKIP RO FOR NOW AND CONTINUE PAUSED GOOGLE SEARCH TEST BUILD WITH PT THEN GR ONLY: KEEP RO ABSENT/PARKED; FIRST CONFIRM NO PT/GR CAMPAIGN EXISTS AND NO BULK-UPLOAD PREVIEW/APPLY IS IN PROGRESS; THEN PROCESS PT ONE COUNTRY AT A TIME, AND ONLY AFTER PT READBACK PASSES PROCESS GR; PREVIEW, DOWNLOAD, VALIDATE 88/88 # OK BEFORE APPLYING EACH; KEEP ALL NEW CAMPAIGNS/AD GROUPS/KEYWORDS/ADS PAUSED, PRESENCE-ONLY, CONTENT/YOUTUBE OFF, CPC AT OR BELOW $0.20; DO NOT TOUCH FR, BE, US CAMPAIGN 23827590655, STANDARD SHOPPING, PMAX, MERCHANT, SHOPIFY PRODUCT DATA, PINTEREST, THEME, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT; NO LIVE SPEND.`
