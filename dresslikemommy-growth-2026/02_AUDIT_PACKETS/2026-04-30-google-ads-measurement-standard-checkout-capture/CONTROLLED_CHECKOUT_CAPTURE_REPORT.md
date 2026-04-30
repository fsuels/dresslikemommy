# Controlled Checkout / Tag Capture Attempt

Generated: 2026-04-30T20:18:43.734743+00:00

## Decision

`BLOCK_NON_BUDGET_CAMPAIGN_EDITS__PURCHASE_RUNTIME_PROOF_BLOCKED_BY_CHECKOUT_CAPTCHA`

Launch status: `LAUNCH_BLOCKED`

No campaign edits, launch actions, Google Ads settings changes, Shopify settings changes, or completed orders were made by this capture.

## What Happened

- Added one live product to cart: `Fruit Green Family Matching Set - Polo Dresses & Shirts - Dress / Child 1-2 Years`.
- Cart total was `USD 29.99`.
- Checkout showed free standard shipping after the controlled test address.
- Test-card fields were filled successfully in Playwright (`number`, `expiry`, `CVV`, `name` lengths confirmed; no card data saved in artifacts).
- After attempting checkout, Shopify required: `Solve the captcha to complete your purchase.`
- Because CAPTCHA solving requires human handoff, the agent stopped. No thank-you page and no `purchase` measurement event were captured.

## Measurement Events Observed Before Blocker

- `add_to_cart`: `4` request(s), including `value=29.99` and `currency_code=USD`.
- `begin_checkout`: `4` request(s), including `value=29.99` and `currency_code=USD`.
- `add_payment_info`: `5` request(s), including `currency_code=USD`.
- `purchase`: `0` request(s).

## Strict Purchase Requirements

- Purchase value: `NOT_PROVEN`
- Purchase currency: `NOT_PROVEN`
- Transaction ID / order ID: `NOT_PROVEN`
- Deduplication: `NOT_PROVEN`

The capture proves that pre-purchase Google/GA events can carry USD and value, but it does not prove the actual purchase event. Non-budget campaign edits and launch work remain blocked.

## Evidence

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-playwright-capture/`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-30-google-ads-measurement-standard-checkout-capture/`
- Standard checkout blocker screenshot: `screenshots/attempt1_after_submit.png`
- Parsed summary: `raw/controlled_checkout_capture_summary.json`

## Required Next Action

A human must complete the CAPTCHA and controlled test order while capture is running, or provide an equivalent Tag Assistant purchase recording. The agent cannot solve CAPTCHA.
