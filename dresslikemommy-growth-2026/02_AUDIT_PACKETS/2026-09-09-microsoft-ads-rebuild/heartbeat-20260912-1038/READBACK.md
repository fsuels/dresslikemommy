# Microsoft consent test — September 12, 10:38 UTC continuation

**VERIFIED:** the native UET receiver accepted normal collection page views without a consent signal. A controlled reload emitted the standard UET pageLoad for the exact test URL while Shopify's effective analytics and marketing permissions were denied before and after the reload. **Supported production repair remains incomplete.**

This is a fresh runtime finding, beyond the older seven-day consent warning. The direct event request had no `asc`. The app's public wrapper loaded standard `bat.js` and queued pageLoad without an explicit Shopify privacy check. The request's final initiator stack was unavailable, so the sender attribution uses the observed loading chain and request shape. The network buffer was truncated; no claim is made that another stream was absent. The receiver's three rows match the unique test URL but provide minute-level ages, not a per-hit request-ID join.

The controlled session was in USFL. It does not certify EEA/UK/Swiss behavior or purchase consent. No visitor identifiers were persisted. The current STRICT app pixel still declares analytics, marketing and sale-of-data requirements and retains its previously inspected version. It was not modified.

The U.S. and German campaigns were reused. No imports, goal changes, campaign settings, spend, cart changes, checkout, synthetic purchases, consent changes, production script edits or app-loading retries occurred. The starting native ad view confirmed the saved U.S. ad remains Paused and the account banner still reports paused campaigns.

**Next action:** obtain a supported Microsoft app repair using the [prepared redacted support request](support_request_ready.md). Sending it requires explicit permission to contact Microsoft support; it has not been sent. Preserve the existing parent owner action for theme publication and all peer ownership. A source fix must be independently reviewed and tested before any live application.

Evidence: [trace](receiver_consent_trace.json), [observed wrapper](standard_publisher_observed.js), [independent guidance](review/uet_consent_interpretation.md). The broader purchase, attribution, actual cost, paid authority and profit gates remain open.

Continue with [the canonical paid-growth prompt](../../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md), TA-15 / Microsoft 477439, the completed September 12 paused-build anchor, and this new consent evidence. Reuse the existing objects. Resume the supported repair when the publisher path or exact required authorization changes; do not repeat this unchanged test on every wake.
