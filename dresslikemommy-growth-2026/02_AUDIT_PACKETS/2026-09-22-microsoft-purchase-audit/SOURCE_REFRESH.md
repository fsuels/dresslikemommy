# Public Microsoft publisher refresh — September 22, 2026

Confidence: H for public source identity and mapping; attribution remains unverified.

At **2026-09-22 14:02:51 UTC**, unauthenticated public HTTP GETs returned HTTP200 for the homepage and its configured Microsoft APP bundle. No cookie jar, credentials, JavaScript execution, simulated clicks, cart/checkout actions, or tracking events were used. No reusable standalone source-refresh script was found in the targeted existing scripts/packet search; a bounded Python standard-library read performed the refresh. Full homepage and response headers were not saved.

## Verified source

- MAIN theme **133290917985**; APP **931561569**, client **2997493**, STRICT; UET **36005151**.
- Installed version **5ee93563fe31b11d2d65e2f09a5229dc**. The **8,917-byte** retrieved app source is byte-identical to the September9 audited bundle; SHA256 **bdf85b114cb9d9ef5c790dee198f38dd8032c46bc13bdf7ca9f4ee034abc7f29**.
- Privacy declarations remain ANALYTICS, MARKETING and SALE_OF_DATA; dataSharingState optimized.
- `checkout_completed` invokes `completePurchase`, which sends `ea=purchase`, `pagetype=purchase`, `gc=checkout.subtotalPrice.currencyCode`, `gv=checkout.subtotalPrice.amount`, and deduplicated composite product_variant IDs. Subtotal is not full order total.
- The source still calls `e.set(`msclkid; expires=${r.toUTCString()}`,i)` and separately retains a90-day localStorage fallback. The previously reproduced malformed cookie-setting expression remains installed. Actual click-ID loss is not established by source identity.
- Existing source limitations remain: no explicit purchase transaction/event ID and no explicit `asc`/`ad_storage` implementation in the audited bundle. These do not independently prove production duplication or app-purchase consent failure.

Evidence: [sanitized receipt](public_source_refresh.json); historical independent source analysis: `../2026-09-09-microsoft-ads-rebuild/microsoft_tracking_independent_review.md`, lines3–13. No extra copy of the byte-identical bundle was written.

## Existing support path and authority

Latest exact diagnostic addendum: `../2026-09-09-microsoft-ads-rebuild/receiver-and-day-20260922/support-addendum.md`. Status LOCAL_NOT_SENT; same case **7108824779**, acknowledged September14. It asks for investigation status, supported publisher correction, exact purchase/consent/deduplication diagnostics and confirmed escalation/update timing.

The latest explicit follow-up authority source found is `../2026-09-09-microsoft-ads-rebuild/support-followup-20260921/preflight.json`: the existing owner heartbeat authorizes **EXISTING_CASE_ROUTINE_STATUS_REQUEST_ONLY**, with **EXACT_SCOPE_ONLY_NO_BUSINESS_WRITE**. This is source-owner authorization, not transferable subagent send authority. This subtask's authority is read-only and no message was sent.

September21 READBACK lines33–37 record a sent375-character routine status request but two failed human connections and no acknowledgment. The mailbox searched was not established as the support recipient. September22 addendum line3 and handoff line49 preserve the existing authenticated-channel dependency and forbid retrying unchanged failed routes or duplicating the case. No supported correction, response or engineering escalation has been verified.

## Result and limits

Source refresh VERIFIED; installed code remains unchanged. Four local assertions passed: both HTTP200 receipts, exact byte match, exact cookie expression and exact purchase subtotal/currency mapping. This is not a receiver, consent-runtime, order reconciliation or paid-click attribution test. No production fix was applied. Parent retains live verification, exact change authority and shared canonical integration.
