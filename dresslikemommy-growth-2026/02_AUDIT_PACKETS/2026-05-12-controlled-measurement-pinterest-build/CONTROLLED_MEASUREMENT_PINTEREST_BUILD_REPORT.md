# Controlled Measurement + Pinterest/Ads Build Push

Generated: 2026-05-12

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-controlled-measurement-pinterest-build`

## Owner Direction

- Owner approved one controlled low-risk non-US checkout test purchase, then refund/cancel/void through the safest Shopify path.
- Owner approved paused Pinterest US catalog/retargeting draft build from the clean 342-row EN-US scope with 4 excluded variants.
- Owner later instructed: stop spending time checking tags; assume tags are correct and solve everything else.

## Controlled Non-US Checkout Test

Selected lowest-practical visible exposure:

- Country/currency: `GB` / `GBP`
- Cart URL: `https://www.dresslikemommy.com/cart/41497061916769:1?country=GB`
- Product: `Chic Pink Mermaid Scales Tankini Set for Mother and Daughter`
- Variant: `41497061916769`, `Child 2-3 years / Multi-Color`
- Checkout total after shipping precheck: `GBP £12.00`
- Shipping: `Standard Delivery (10 - 14 Days) FREE`
- Payment methods shown: Credit card, Shop Pay, PayPal, Crypto: USDC

Result:

- Stopped before payment.
- Synthetic contact/address data was entered only to expose shipping/total.
- No payment data was entered.
- `Pay now` was not clicked.
- No order, refund, cancel, void, Ads edit, Merchant edit, Pinterest edit, product/feed/conversion/budget/bid/status change, or campaign enablement occurred.

Reason stopped:

- Checkout requires a real payment method or external payment flow.
- No safe test payment instrument/path was available inside the session.
- Owner approval allowed a low-risk purchase, but it did not provide a safe payment credential/instrument, and the precheck says to stop if payment/order risk exceeds the precheck.

Evidence:

- `measurement/checkout_precheck_summary.json`
- `measurement/checkout_shipping_precheck_summary.json`
- `measurement/checkout_precheck_cart.png`
- `measurement/checkout_precheck_after_checkout_click.png`
- `measurement/checkout_shipping_precheck_after_address.png`

## Pinterest Paused US Draft Build

Approved scope preserved:

- Advertiser: `549756244483`
- Catalog: `3041764155561548387`
- EN Shopify feed profile: `3041760867124595727`
- Scope: clean `342` EN-US in-stock rows
- Exclusions: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`
- Planned templates: US catalog shell and retargeting shell, paused only.

Attempts:

1. CDP opened Pinterest Ads URL in the currently available Chrome remote-debugging session.
2. Instead of the authenticated campaign manager, Pinterest redirected to the public `Pinterest Ads` landing/login page.
3. Chrome DevTools MCP recovery failed because its profile is already running/locked.
4. Playwright MCP recovery failed because its profile is already running/locked.
5. Computer Use recovery failed with Apple event error `-1743`.

Result:

- No Pinterest campaign, ad group, ad, product group, catalog source, tag, CAPI, audience, budget, bid, status, or spend write occurred.
- The paused draft build is blocked by missing authenticated Pinterest browser/session access in the currently controllable tools.

Evidence:

- `pinterest/pinterest_create_flow_probe_summary.json`
- `pinterest/pinterest_before_campaign_manager.json`
- `pinterest/pinterest_before_campaign_manager.txt`
- `pinterest/pinterest_before_campaign_manager.png`
- `pinterest/pinterest_create_menu_probe.*`
- `pinterest/pinterest_create_wizard_probe.*`

## Google Ads Remaining Paused Search Build

Owner told us to assume tags are correct, so the focus moved to campaign infrastructure.

RO recovery:

- Read-only bulk upload page probe passed: no visible `RO`, `PT`, `GR`, `FR`, or `BE` upload row; no throttle hint; logged-in Ads account visible.
- RPC readback confirmed `RO` campaign is absent before import.
- Existing Node/Playwright RO recheck helper failed because the repo shell does not have the `playwright` module.
- CDP-only helper reached the Google Ads Uploads page and then the upload form.
- Patched helper for current UI labels:
  - `Uploads` page text
  - `New Upload` case
  - `Upload a file`
  - native custom file picker
  - ad-blocker overlay UI recovery
  - CDP file chooser intercept / trusted mouse click path
- Final result: file picker remained inaccessible to CDP automation. The RO CSV was not selected, preview was not clicked, apply was not clicked, and no Ads write occurred.

Result:

- RO remains absent.
- The exact next unblock is browser access that can operate the Google Ads native file chooser, Google Ads Editor with posting permission, or another approved upload path. Do not re-upload completed countries.

Evidence:

- `raw/google_ads_bulk_upload_readonly_probe.json`
- `raw/google_ads_bulk_upload_readonly_probe.txt`
- `raw/google_ads_bulk_upload_readonly_probe.png`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/working/google_ads_split_bulk_apply_state.json`
- Patched helper: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/working/google_ads_split_bulk_apply.py`

## Current Launch Position

- Tags/tracking should be treated as owner-assumed-good for launch-prep decisions.
- Live enablement still requires exact action-time approval naming the specific campaign/ad group/status action.
- Pinterest paused US draft creation is approved but blocked by Pinterest authenticated session/tool access.
- Google Ads RO paused build is approved but blocked by the Google Ads native file picker in the currently controlled browser.
- The controlled non-US purchase is approved but blocked by lack of a safe payment/test instrument/path.

## Next Best Action

1. For Google Ads: use an interactive browser/file-picker-capable session or Google Ads Editor to upload only `RO_intl_search_paused_draft_web_bulk.csv`, preview `88/88 # OK`, apply only if clean, then read back paused Search/presence-only/content off/YouTube off/CPC <= `$0.20`.
2. For Pinterest: restore authenticated Pinterest Ads Manager access, then create only paused US catalog/retargeting drafts from the 342-row scope and read back before/after.
3. For first live traffic: if owner wants to proceed with tags assumed-good, give exact action-time approval for the first named Google Ads enablement; start with GB campaign `23838895360` and ad group `Mommy & Me Dresses - Exact`, preserving budget/bid and all other guardrails.
