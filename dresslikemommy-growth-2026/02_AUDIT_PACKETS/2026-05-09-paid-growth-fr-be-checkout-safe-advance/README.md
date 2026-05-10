# 2026-05-09 Paid Growth FR/BE Checkout Safe Advance

Parent/orchestrator: Codex current session, 2026-05-09.

Canonical prompt: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.

## Scope

Safe read-only/local continuation of the paid-growth sprint. This packet is intended to advance France (`FR`) and Belgium (`BE`) from checkout-pending into paused-infrastructure approval-gated status if no-payment checkout, landing, and CSV guardrails pass.

## Guardrails

- No live spend.
- No campaign enablement, import, preview, upload, budget, bid, or status changes.
- No PMax enablement.
- No Standard Shopping changes.
- No product-scope, feed-label, product-group, or conversion-goal changes.
- No Merchant uploads, source syncs, source edits, or product-data changes.
- No Shopify live product-data changes.
- No theme edit or theme publish.
- No checkout payment submission or order creation.
- No CAPTCHA or verification bypass.
- No rapid repeated endpoint probing after `429`/verification.

## Lanes

| Lane | Owner | Status | Output |
|---|---|---|---|
| `checkout-fr-be` | Worker A | `DONE_PASS_READONLY_NO_PAYMENT_NO_ORDER` | FR and BE reached checkout-to-shipping with EUR, Standard/Express visible, no verification wall, no payment, and no order |
| `remaining-landing-policy` | Worker B | `DONE_PASS_PUBLIC_LANDING_POLICY_ONLY` | `NL`, `FR`, `BE`, `SE`, `PL`, `CZ`, and `GR` public product/policy/page surfaces returned `200`, correct currency/language behavior, and no visible blocker phrases/leaks |
| `ads-held-csv-remaining` | Worker C | `DONE_PASS_LOCAL_ONLY_APPROVAL_GATED` | Held `1496`-row Ads CSV validated for `NL`, `FR`, `BE`, `SE`, `PL`, `CZ`, and `GR`: all importable entities paused, no forbidden rows, no bad beach URL |
| `market-readiness-controls` | Worker D | `DONE_MATRIX_UPDATED` | FR/BE moved to paused-infrastructure approval-gated only; `NL`, `SE`, `PL`, `CZ`, `GR` remain checkout-pending; live-spend-ready non-US markets remain `0` |

## Problem Links

- `PROB-2026-05-09-FR-BE-CHECKOUT-QA` closed as `SOLVED_READBACK_PASSED`
- `PROB-2026-05-09-DE-NL-CHECKOUT-QA` remains partial: `DE` solved; `NL` still `429` blocked.
- `PROB-2026-05-08-STANDARD-SHOPPING-LIVE-METRICS-READBACK` remains `CREDENTIALS_REQUIRED`.

## Parent Decision Rules

- FR/BE can become paused-infrastructure approval-gated only if public country/currency/landing checks and no-payment checkout-to-shipping checks pass without verification/CAPTCHA/payment/order.
- If either country hits HTTP `429`, CAPTCHA, or verification, stop that country after one safe retry at most and keep it checkout-pending with the exact next unblock action.
- Live-spend-ready non-US markets remain `0` unless Merchant/Pinterest/tracking/economics and exact owner approval gates clear.
