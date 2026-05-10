# 2026-05-09 Paid Growth NL Checkout + Standard Metrics Safe Advance

Parent/orchestrator: Codex current session, 2026-05-09.

Canonical prompt: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.

## Scope

Safe read-only/local continuation of the paid-growth sprint with two independent lanes:

- `nl-checkout-retry`: public Netherlands no-payment/no-order/no-bypass checkout-to-shipping retry after cooldown.
- `standard-shopping-metrics-readback`: read-only recovery/readback path for Google Ads Standard Shopping campaign `23802638621`.

## Guardrails

- No live spend.
- No campaign enablement, import, preview, upload, budget, bid, or status changes.
- No PMax enablement.
- No Standard Shopping changes.
- No product-scope, feed-label, product-group, or conversion-goal changes.
- No Merchant uploads, source syncs, source edits, or product-data changes.
- No Shopify Admin product-data changes.
- No theme edit or theme publish.
- No Pinterest write.
- No checkout payment data, Pay Now/Place Order click, or order.
- No CAPTCHA or verification bypass.
- No sign-in, account switch, credential change, or acceptance of Google prompts.

## Lanes

| Lane | Owner | Status | Output |
|---|---|---|---|
| `nl-checkout-retry` | Worker Pascal | `DONE_PARTIAL_PASS_NO_429_NO_PAYMENT_NO_ORDER` | NL product/cart/rates cleared prior `429`; checkout entry reached with `en-NL`, EUR, Standard/Express visible; selected Netherlands checkout UI confirmation remains pending because the runner stopped before address-fill confirmation |
| `standard-shopping-metrics-readback` | Worker Volta | `DONE_ALL_TIME_READBACK_PASSED_NO_ADS_WRITES` | Campaign `23802638621` all-time Google Ads metrics, product groups, products, and search terms captured read-only through existing logged-in browser/CDP path |

## Parent Decision Rules

- NL is cleared only if product/cart/rates and checkout UI reach visible Standard/Express rates with EUR and selected Netherlands, with no `429`, CAPTCHA/verification, payment data, Pay Now/Place Order click, or order.
- Standard Shopping metrics are cleared only if fresh read-only Ads evidence for campaign `23802638621` is captured with no account/campaign writes.
- Passing NL does not make non-US markets live-spend-ready; it only moves NL to paused-infrastructure approval-gated status.
- Any Ads metric finding may inform a decision packet, but no Standard Shopping edit is allowed without fresh exact owner approval.

## Parent Integration

- NL is no longer cart/rates `429` blocked in the latest retry: cart add/read/rates returned `200`, cart currency was `EUR`, Standard was `0.00 EUR`, Express API was `11.19 EUR`, checkout URL was `en-nl`, and checkout visible text showed Standard/Express/EUR. NL is still not fully checkout-UI-cleared because selected Netherlands was not confirmed in the checkout UI before the payment/action guardrail stopped the run.
- Standard Shopping metrics readback is no longer blocked by credentials for the all-time view: campaign `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` / `23802638621` was visible as Enabled / Eligible, Shopping, budget `US$20.00/day`, all-time `82` clicks, `3,962` impressions, `US$18.60` cost, avg CPC `US$0.23`, and `0.00` conversions/value. The custom post-May-6-only range still needs an approved export or safe custom-date readback before any continue/rollback/scale decision.
