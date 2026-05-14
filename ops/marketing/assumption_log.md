# Marketing Assumption Log

Last updated: 2026-05-14

Use this file for important assumptions that affect paid-growth decisions, especially when evidence is repo-known, stale, sampled, or gated by approval/access.

| Date | Assumption | Evidence | Risk if wrong | How to verify or retire |
|---|---|---|---|---|
| 2026-05-14 | Bounded paid-media authority is active only inside the explicit caps and quality gates. | `ops/marketing/spend_authorization.md` status is `APPROVED_ACTIVE`; owner authorized spend within limits as long as goals are respected. | An agent could treat bounded authority as blanket approval for excluded surfaces or low-quality changes. | Re-check `spend_authorization.md`, `action_queue.md`, reviewer checklist, and before/after readbacks before any live paid action. |
| 2026-05-14 | Existing stopped-session supplier/source URL sanitizer changes are intentional local fixes. | Dirty diff touches public brand/vendor analytics surfaces and latest worklog anchor `2026-05-14-paid-landing-vendor-source-sanitizer-local` documents the local handoff. | Rewriting or reverting could reintroduce supplier URL leaks or lose a prepared fix. | Preserve changes; verify with diff checks and, before live sync, local/public source readbacks. |
| 2026-05-14 | Merchant US/es age_group old May 8 CSV should not drive repair decisions by itself. | Current marketing state says sampled 2026-05-14 detail readbacks did not reproduce Missing age_group, while the CSV download is stale May 8 evidence. | A needless Merchant or Shopify repair could mutate product/feed data. | Obtain current exact all-row readback/export for source `10627981690`, `US` / `es` / `United States`. |
| 2026-05-14 | Active-product advertising expansion needs a fresh public/Admin/Merchant/Pinterest intersection before uploads/applies. | Current state says the prep map is local/read-only and not approval to advertise all products. | Draft, inactive, supplier-leaking, stale, or unavailable products could enter paid traffic. | Build/read back current active, public, purchasable product scope and exclude unresolved products before any platform action. |
| 2026-05-14 | Father's Day or event-layer planning should prioritize Daddy-and-Me and father-inclusive family matching intent. | Current marketing state and decision log record the category strategy rule. | Seasonal ads may send shoppers to irrelevant or stale categories. | Review current collections/products and route event traffic only to intent-matched active products. |
| 2026-05-14 | 2026 expert strategy should favor high-intent, low-waste, non-cannibalizing traffic until data proves broader automation or scale. | `ops/marketing/expert_growth_playbook_2026.md` and official Google/Pinterest/OpenAI/Anthropic sources listed there. | Agents could buy cheap but low-intent traffic, duplicate query ownership, or broaden too early. | Daily search-term, Quality Score, ad, landing, product, purchase value, CPA, and ROAS readbacks decide expansion, negatives, bid changes, and scale. |
| 2026-05-14 | The growth system now treats zero impressions after 24 hours as an action trigger, not normal waiting. | Owner message: each day without growing sales is a failure; if after one day a campaign has 0 impressions, something needs to be done. | Agents could move too slowly and leave active campaigns with no learning. | Daily scorecard must show sales/ROAS and same-day diagnosis or long-tail/auction-entry action for zero-impression lanes. |

## Add New Assumptions Like This

| Date | Assumption | Evidence | Risk if wrong | How to verify or retire |
|---|---|---|---|---|
| YYYY-MM-DD |  |  |  |  |
