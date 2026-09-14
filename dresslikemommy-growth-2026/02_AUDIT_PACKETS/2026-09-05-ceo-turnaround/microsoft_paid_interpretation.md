# Microsoft paid-traffic evidence interpretation

The current native readback identifies account477439/customer770182 by two Dress Like Mommy landing URLs. Its11campaigns are paused. The displayed historical window is September6,2023–September6,2026, with Eastern Time shown by Microsoft. This does not establish recent traffic or current campaign profitability.

The source table places36000629 and36005151 in the **Tag ID** column. They are UET tag IDs, not unique conversion-goal IDs. The Smart goal uses36000629; the inspected purchase/checkout goals use36005151. Four goals are included in automatic-bidding optimization, including Smart and three checkout/purchase goals. AddToCart is excluded. None was changed.

The three inspected definitions are Purchases (URL contains `thank_you`, variable value with USD30 fallback), ShopifyCheckoutCompleteTracking (URL contains `thank-you`, variable value with USD1 fallback), and ShopifyCheckoutCompleteEventTracking (event action equals `purchase`, variable value with USD1 fallback). The fallback currency does not establish account reporting currency or prove that all observed revenue was a transmitted order value. Three dialogs were closed with Cancel.

Account reporting currency is still UNKNOWN. Australia’s displayed0.24 historical average CPC therefore cannot be directly compared with the owner’s USD0.15 ceiling. Its667/88.72=7.518x historical reported value/spend and38 conversions do not prove38 paid orders or30% current net profit. Full-account7328.37/3618.22=2.025x likewise does not establish purchase-only or retained-order ROAS.

Next exact evidence: a campaign-by-conversion-goal report for the same historical window, with purchase/checkout versus Smart counts/value separated, plus account reporting currency. Match real retained purchases and current costs before qualifying any capped test. Do not add goal-level rows into impression/click/spend totals when the platform does not allocate those metrics by goal. Inspect goal overlap before summing purchase goals. No new account, re-enablement, goal or budget change follows from this readback.

The root native receipt is microsoft_paid_initial_readback.json. Independent review is microsoft_paid_readback_review.json/md. Earlier helper context is historical integration evidence, not current launch authority. The two official Microsoft Help pages returned an Oops/not-found body on direct open; their search snippets were not treated as proof of this account’s event behavior. No documentation or UI error justifies altering tracking without exact source evidence.
