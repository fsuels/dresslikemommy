# Paid Growth Active Campaign Activation Push

Anchor target: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-paid-growth-active-campaign-coverage-push`

Purpose:
- Reframe the sprint around the owner-stated goal: working active Google Ads and Pinterest campaigns for every viable language/market.
- Preserve hard approval gates around live spend, campaign enablement, budget/bid/status changes, product/feed/conversion changes, Merchant/Pinterest/Shopify production writes, and payment/order creation.
- Make the remaining path explicit enough that the next action is not another audit loop.

Files:
- `ACTIVE_CAMPAIGN_COVERAGE_MATRIX.md` - current active/paused/absent/gated state by platform and market/language.
- `APPROVAL_LADDER.md` - exact approval language needed for the next live/account actions.
- `ga4_scope_retry/GA4_SCOPE_RETRY.md` - safe read-only GA4 scope recovery attempt and result.

Current conclusion:
- The actual goal is not complete. Google Ads has some active US coverage and paused international infrastructure. Pinterest has no active campaigns yet.
- The next hard blocker before any new non-US Google activation is still order-level GA4 non-US purchase currency/value proof, unless the owner explicitly approves a controlled non-US test purchase/refund/cancel.
- The next Pinterest account action is an owner-approved paused US EN draft build from the clean 342-row scope, not live spend.
