# Purchase capture: confirmed defect, local correction, live gates

2026-09-06. Anchor: `2026-09-06-ceo-turnaround-purchase-capture`.
Tasks: `TA-02`, `PROB-2026-05-20-GA4-SHOPIFY-PURCHASE-PARITY`.

**IMPLEMENTED and independently VERIFIED locally:** preserve the complete `_ga` cookie value in `pixels/ga4-custom-pixel.js`. The installed Shopify GA4 pixel contains the same truncating expression as the original template. **No installed code or tracking setting was changed. The cause of the three missing purchases remains UNKNOWN.**

## What the current evidence establishes

Root read the existing Chrome Test Shopify Customer events and Analytics stream screens between 11:11:59 and 11:40:19 UTC. Exact per-call timestamps were not retained. The current readback is `purchase_capture_current_readback.json`.

- Shopify custom pixel `111181921`, DLM GA4 Measurement Protocol, has a Disconnect button and requires Analytics permission. Its visible code subscribes to `checkout_completed`, checks consent, and sends purchase value, tax, shipping, currency and items. It uses order ID with checkout-token fallback.
- Its measurement ID `G-N4EQNK0MMB` matches the current GA4 account `88409806`, property `330266838`, stream `4030905738`. GA4 reports collection active in the past 48 hours. A wrong current measurement ID does not explain this gap; activity does not prove purchase completeness or sender identity.
- The installed visible parser uses `parts.slice(2, parts.length - 1).join(".")`. For the synthetic cookie `GA1.1.123456789.1700000000`, the original local helper returns only `123456789`.
- The existing private reconciliation, without another order export, still contains eight retained paid web orders and three missing from GA4, totaling USD302.44 merchandise. The captured data has no individual consent decision, browser callback, sender or transport/ingestion receipt. These fields remain null in `purchase_capture_missing_cohort.json`; source names do not supply that evidence.

Selected installed source fragments were inspected, not a complete installed-code fingerprint. No customer-level root cause is established.

## Smallest local correction

Google's current Measurement Protocol reference accepts the complete client-ID cookie value. The helper now stores and returns the nonempty cookie string intact. It retains the existing stored/generated fallback and changes no consent, session, transaction, value, subscription or transport code. [Google Measurement Protocol reference](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference?client_type=gtag).

The frozen original is `purchase_capture_ga4_template_before.js`; the exact diff is `purchase_capture_ga4_client_id.patch`. The seven-case test extracts the actual helper into an isolated VM and cannot initialize a pixel or send requests. Four synthetic cookie cases fail against the original; the three fallback holdouts pass. All seven pass against the correction. Syntax and scoped whitespace checks pass. The independent reviewer repeated both versions and verified every byte outside the helper is unchanged: `purchase_capture_client_id_review.md`.

The correction prevents this local truncation. It does not prove the sandbox exposes this cookie, its identity matches another sender, or Analytics ingests the event. If no cookie is available, an already truncated stored ID remains unchanged. Malformed-cookie validation and other inventory findings are outside this patch.

## Competing explanations and preserved safeguards

The purchase event depends on the relevant completion page loading; Shopify documents that failure to load that page prevents the event. Consent and transport/ingestion evidence for the missing orders are absent. These remain possible explanations, not diagnosed causes. [Shopify checkout_completed](https://shopify.dev/docs/api/web-pixels-api/standard-events/checkout_completed).

The native Ads pixel `111214689` is also connected. Its visible code permits Analytics=true after Marketing=false, while Shopify requires both purposes at the pixel level. No receipt shows a send against a customer's permission. Record this as a separate source-review risk; do not weaken the platform gate or modify Ads tracking within this repair. Google & YouTube app pixel details show Server Web and Optimized data access, but no explicit connection status was captured. Old claims that only the app pixel runs, that it caused the gap, or that deduplication has a universal 24-hour guarantee are unsupported by this readback. Existing README/runbook files remain unchanged; use the current inventory and primary-platform review before any installation change.

Alternatives considered: leave the demonstrable helper defect untouched; or replace/migrate the complete tracking stack. The bounded helper correction preserves working behavior and avoids choosing a migration from incomplete sender evidence. Neither a new pixel nor a historical-purchase replay is proposed.

## Deployment and verification gate

This is a reviewed **local candidate**, not an executable full-template installation packet. Before proposing an installed save, bind the exact current installed helper and a private, credential-safe full-code comparison; preserve current configuration and all unrelated live code. Never paste the repository template over the installed pixel. If current source differs, stop and revise the candidate/review.

Any production tracking change needs exact current authority under the command layer, one root-owned claim, a secure before-state and after-state comparison, and an approved validation scope. No additional approval was requested here. Existing public 429 challenge and test-purchase/financial gates remain. Future consent-respecting validation must establish callback, sender, identifier/session and ingestion behavior without contaminating sales reporting or replaying the three historical orders. A successful HTTP receipt alone is not ingestion proof.

Local rollback is the frozen original helper after checking for intervening changes. A live rollback, if later needed, restores only the exact captured installed before-state under the applicable authority; none was executed. Success for this turn is the seven-case local contract and preservation proof. Live effectiveness, purchase reconciliation and profitable-growth outcomes remain unverified. Keep Shopify retained sales and verified platform cost separate from GA4 attribution while parity is unresolved.

## Continuation

Do not repeat the completed order join, pixel inventory or stream mapping. The tracking lane next needs deployment binding and permitted event evidence, not another aggregate audit. Reuse the existing Sunshine quantity/expense work and prepared organic releases when their specific gates change.

The single owner action remains the pending Italian paid/unfulfilled-item resolution: confirm any external replacement/refund for the two Ivory Meadow dresses totaling EUR60.90 and resolve any outstanding obligation. The owner performs any financial remedy. This customer issue precedes support-form recovery. Root sent no customer message or financial action. All nine paid-control fields, saved support-send approval, prior publication/access gates and the ACTIVE goal/heartbeat are preserved.

Evidence index: current readback; missing-cohort receipt; frozen original; exact patch; before/after test outputs; implementation inventory; primary-platform requirements; independent client-ID review; `purchase_capture_checks.json`. Resume through `ops/prompts/paid-growth-ai-army-continuation-prompt.md` and the current command-layer digest.
