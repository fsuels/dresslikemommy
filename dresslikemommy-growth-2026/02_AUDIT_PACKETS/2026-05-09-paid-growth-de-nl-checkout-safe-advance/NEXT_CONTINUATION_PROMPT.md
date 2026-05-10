# Next Continuation Prompt

Use the canonical prompt in `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.

Latest paid-growth anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-09-paid-growth-de-nl-checkout-safe-advance`

Do not create a competing prompt. Paste the owner-standard prompt from the canonical file and preserve these current facts:

- `DE` passed no-payment checkout-to-shipping for paused infrastructure only.
- `NL` remains checkout-pending / rate-limited after two HTTP `429` verification results on cart/rates; no CAPTCHA or verification bypass was attempted.
- `GB`, `CA`, `AU`, `ES`, `IT`, `RO`, `PT`, `CH`, `DK`, and `DE` have checkout/rate evidence for paused infrastructure only.
- Non-US live-spend-ready markets remain `0`.
- Remaining checkout-pending markets are `NL`, `FR`, `BE`, `SE`, `PL`, `CZ`, and `GR`.
- The held `1496`-row non-US Search CSV remains local-only and approval-gated; DE/NL validation passed with no bad beach URL, US campaign, PMax, Standard Shopping, product/feed/conversion, enablement, or CPC-over-`$0.20` hits.
- `PROB-2026-05-08-STANDARD-SHOPPING-LIVE-METRICS-READBACK` remains `CREDENTIALS_REQUIRED`; next unblock is logged-in Google Ads access, approved read-only export, or read-only Google Ads API credentials for campaign `23802638621`.
- Merchant US/es age_group, Pinterest Event Quality/draft, and beach/Vacation Family metadata remain separate approval-gated problems.

Next safest subagent split:

1. Checkout QA: `FR`, `BE`, `SE`, `PL`, `CZ`, and `GR`, one market at a time, no payment/order/CAPTCHA bypass.
2. NL retry lane: only after longer cooldown or parent-approved browser path; no CAPTCHA/verification bypass.
3. Ads local validation: keep held CSV ready, but no preview/import without exact `TEST BUILD` approval.
4. Standard Shopping metrics gate: recover read-only metrics access/export for campaign `23802638621`; no campaign changes.
