Confidence: H for exact contract comparison. **PASS — four fields on three existing goals only.** This is preflight approval of the bounded technical change, not evidence of completed execution or purchase accuracy.

The reviewed [contract](purchase_goal_repair_contract.json) is SHA256 `a5b8b398e04fb3755e85304c711f81c32bed21e8495df00f82c508c1997cb1b7`; [before-state](live_before.json) is `0c33c837f9d5802148ea81c181ab31fe23e3b5020825d622883e4a817b6f48e6`. The [decision amendment](decision_challenge_amendment.json) is `03dbb0269f79dc3a99a3db09025cb3c48d3e9aad829e9a21c80daaeaa49848e8`.

Approved technical delta:

- ShopifyCheckoutCompleteEventTracking: Count **Unique→All**; variable-revenue fallback **USD1.00→USD0.00**.
- ShopifyCheckoutCompleteTracking: automated-bidding/Include in Conversions **Yes→No**.
- Purchases: automated-bidding/Include in Conversions **Yes→No**.

**21 independent checks passed.** Applying that local delta changes exactly four leaf fields; the specified inverse restores the complete before-state. Account477439/customer770182/UET36005151 and unique goal names/criteria agree. MSCLKID tagging is already on. All five Active goals, two existing secondary exclusions, variable revenue/currency, windows, attribution, account options and eleven paused campaigns remain preserved. No extra live fields are permitted.

All is appropriate for multiple sales after a click; it is not order deduplication. Zero fallback avoids fictional positive revenue when the real value is absent. Goal exclusion retains All reporting while affecting standard Conversions/Revenue/ROAS and bidding; “preserve reporting/history” cannot mean those derived numbers remain unchanged. [Microsoft counting](https://learn.microsoft.com/en-us/advertising/campaign-management-service/conversiongoalcounttype?view=bingads-13), [revenue](https://learn.microsoft.com/en-us/advertising/campaign-management-service/conversiongoalrevenue?view=bingads-13), [goal exclusion](https://learn.microsoft.com/en-us/advertising/campaign-management-service/eventgoal?view=bingads-13).

The amendment correctly rejects adding another goal and preserves uncertain order/value/consent evidence. No additional sender, CAPI or consent patch is justified by this contract.

Root may execute after the final native target/staged-state guard, then reopen each goal and verify all intended/preserved fields, account settings and paused campaigns. Stop on drift or error. I did not operate the browser, execute a Save, or build root's contract. Current values, order deduplication, full consent, paid attribution and profit remain unverified. [Full check receipt](exact_goal_preflight_review.json).
