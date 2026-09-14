# Italian GA4 campaign-cost review

Confidence: H for receipt consistency and arithmetic. **PASS; no required correction.** Reviewed 2026-09-06 using the [cost receipt](italian_ga4_campaign_cost_readback.json), [native receipt](italian_ga4_native_readback.json) and [prior review](italian_ga4_native_postreview.md). Browser observations remain operator-supplied; no browser/API read was repeated.

The property, Ads account, campaign name and fixed June 7–September 4 dates agree. Both advertising-report views identify Google Ads campaign `23866684201` with identical metrics under account `3990976848` and purchase-only key-event selection. This supplies an explicit advertising-report `googleAdsCampaignId`; it does not retroactively supply the unavailable session-scoped numeric field or an independent transaction-to-click join. Total revenue remains the report’s metric, not verified profit.

Recomputed from displayed USD values:

| Scope | Result |
| --- | --- |
| Italian campaign | $127.34 / 855 clicks = $0.148936 average CPC; one purchase key event gives $127.34 cost/event. |
| Italian efficiency | $151.46 / $127.34 = 1.189414×, or 118.94% ROAS; purchase key events/click = 0.116959%. |
| Other brand campaign | 40 clicks, $3.02 cost, zero purchase key events/revenue. |
| Two returned rows | 895 clicks, $130.36 cost, one purchase key event, $151.46 revenue; 1.161859× rounds to 1.16×. |

All supplied conditional planning calculations reconcile, including −$51.715 contribution under the owner’s 50% non-ad-cost assumption. That estimate is not an actual loss determination. Actual costs, returns, missing purchases, Shopify attribution disagreement and Google Ads conversion accounting remain unresolved. Average CPC does not establish a maximum CPC or successful economics.

September 5: provisionally 11 clicks/$1.65/zero purchase key events/$0 revenue/0× ROAS; CPA is undefined. The completed calendar date still uses intraday data. Neither its unsampled flag nor the 90-day daily-data flag proves complete capture or matured conversions. September 6 serving status and full-account spend remain unknown; a stored “PAUSED” name proves no current status.

**Priority accepted:** HOLD Italian scaling. Owner correction of the existing support contact for original Ads control goes before four-file Shopify release review because recent spend is now evidenced. Preserve existing send approval, unresolved validation/no-retry restriction and every release/control gate. Root’s next safe action is exact-campaign keyword/query diagnosis through GA4; no campaign or measurement mutation is authorized by these results.

Receipt SHA256: `c3a12cec7d333669bd11f8bcefb373b2ff44094daaa5cbba47aa34d6b6bd645a`
