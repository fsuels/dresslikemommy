# Microsoft tracking repair contract — September 14, 2026

**LOCAL CANDIDATE / NOT DEPLOYABLE.** This subordinate evidence packet implements and tests a purchase contract. It neither repairs nor disconnects the installed Microsoft publisher. No Shopify pixel, Microsoft tag, campaign, goal, customer record or account setting was changed. No SDK was loaded and no event was sent to Microsoft. The owning task remains TA-15 in `ops/marketing/`; this packet is not a command layer or approval.

Target for any future authorized repair: Dress Like Mommy, Microsoft account **477439**, customer **770182**, existing UET **36005151**. The test suite uses a reserved example domain, a dummy tag and synthetic orders.

## Decision and observed limits

The September 12 evidence demonstrates a **standard storefront pageLoad request** without the expected consent signal while Shopify reported analytics and marketing denied. It does not prove a defect in the isolated purchase sandbox. The September 14 UET receiver view reports a purchase and parameter names, but does not identify the actual order, value, currency or consent state. See the preserved [publisher issue](../heartbeat-20260912-1038/support_message.txt) and [receiver addendum](../heartbeat-20260914-1044/support_addendum.md).

The primary route remains a supported publisher correction. The alternative examined here is a custom browser purchase sender. Its local tests demonstrate that ordinary asynchronous browser storage cannot make its read/reserve/write sequence atomic across tabs. Two instances can queue one order twice; concurrent distinct orders can overwrite each other's reservation. These are reproduced limitations, not hypothetically passing safeguards.

**Decision: do not install this draft.** A custom replacement would require an independently validated single-sender cutover and an authoritative deduplication design, plus consent and delivery evidence. Stable IDs alone do not supply that guarantee. Microsoft documents browser `event_id` for matching JavaScript and CAPI copies, not a browser-only repeat guarantee. [CAPI integration guide, updated August 4, 2026](https://learn.microsoft.com/en-us/advertising/guides/uet-conversion-api-integration?view=bingads-13).

## Implemented local contract

Files: [purchase-contract.mjs](purchase-contract.mjs) and [purchase-contract.test.mjs](purchase-contract.test.mjs).

| Concern | Implemented behavior | Limit |
| --- | --- | --- |
| Initial consent | Requires explicit `true` for analytics, marketing and sale-of-data processing, plus a successfully registered privacy source | Conservative design preserves the installed app's declared purposes; this is not a legal determination |
| Consent transitions | Invalidates pending work when a required permission changes; checks after asynchronous identity/storage operations and before enqueue | Cannot cancel an in-flight storage operation, SDK timer or already-dispatched request |
| Denied events | Discards without reading storage or buffering for a later grant | Some legitimate purchases will be unmeasurable; never invent a conversion |
| Purchase identity | SHA-256 of a versioned JSON tuple containing shop, environment, tag, action and Shopify order ID | Browser support and receiver acceptance require live verification; hashing is pseudonymization, not anonymity |
| Transaction/event fields | `transaction_id` is the stable digest; `event_id` is `purchase_` plus that digest | Distinct field meanings; neither is a Microsoft receipt or proven browser replay lock |
| Revenue | Uses the actual checkout total and its currency without a default, second discount subtraction or assumed cents conversion | Checkout total differs from retained merchandise revenue and contribution profit |
| Validation | Rejects missing order identity, invalid money/currency and conflicting checkout currencies | A three-letter currency format check does not prove Microsoft supports that currency |
| Duplicate attempts | Serializes one instance and suppresses existing persistent records after reload | Does not serialize other tabs, devices, deleted browser data or another sender |
| Changed order payload | Holds the same order with a different value/currency for reconciliation | Does not implement refunds, edits or restatements automatically |
| Delivery | Distinguishes reservation, definite non-dispatch, queued/unconfirmed and uncertainty | Does not expose a “received” setter; receipt requires independent evidence |
| Storage | Refuses corruption, clock rollback, capacity overflow and expired records; never silently evicts unresolved records | Failure favors undercounting over an uncontrolled resend; storage policy remains provisional |
| Pending work | Admits at most eight outstanding purchase calls and uses a five-second deadline including queue wait; timeout invalidates the attempt and holds the instance | These are provisional engineering limits; timers cannot preempt synchronous SDK code or a suspended browser |
| Personal fields | Copies only event name, order ID and checkout total/currency into working memory; diagnostics contain only status/reason | Hashed identity remains order-related data; avoid logging payloads in a real adapter |

The Shopify purchase source is `event.data.checkout.order.id`, distinct from the customer event's `event.id`. Shopify describes `checkout_completed` on the thank-you page or first upsell page, with possible absence if the triggering page fails to load. The schema provides numeric `MoneyV2.amount` and currency. These platform facts do not prove Microsoft receipt. [Shopify checkout_completed](https://shopify.dev/docs/api/web-pixels-api/standard-events/checkout_completed), accessed September 14, 2026.

The candidate omits feed product IDs, `items`, click-ID handling and automatic page views. Actual Microsoft offer mappings and full attribution continuity must be verified before these are implemented; Shopify product IDs must not simply be assumed to equal Merchant Center IDs. Microsoft separately documents transaction identity and feed matching. [UET parameter table, updated June 26, 2026](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_uet_parameters_table).

## Publisher consent requirements

The installed standard sender and the isolated purchase sender are separate paths. A helper in a new custom pixel cannot control either existing sender merely by using the same tag ID.

1. Capture the current publisher/version and both loading paths before correction. Preserve a rollback route that does not recreate the observed consent problem.
2. Obtain the effective Shopify privacy state before any dependent SDK initialization or event. A missing snapshot is not permission.
3. Register the documented privacy-change subscription before allowing events. Failure or lost access invalidates the permission source. Do not replay events collected while permission was absent.
4. Recheck permission after each asynchronous initialization stage and immediately before dispatch. If a basic consent design is selected, do not initialize a marketing SDK before permission. A denied-consent signal to an already-running SDK and complete suppression of every SDK request are different behaviors and require separate observation.
5. Handle grant, refusal, revocation and a revoke/regrant during an outstanding operation. Verify both standard UET and the isolated app stream, not merely the visible theme queue.
6. Verify SDK defaults, automatic page views, SPA navigation, delayed requests and storage behavior in the actual runtime. `canInitializeTransport()` in this candidate is only a current local predicate; it does not initialize, shut down or audit an SDK.

Shopify documents `init.customerPrivacy` and `api.customerPrivacy.subscribe('visitorConsentCollected', callback)` for custom pixels; app pixels receive their API through the registered callback instead. Do not substitute email-marketing opt-in or an undocumented event name. [Customer privacy API](https://shopify.dev/docs/api/web-pixels-api/standard-api/customerprivacy), [pixel privacy](https://shopify.dev/docs/api/web-pixels-api/pixel-privacy), accessed September 14, 2026.

This candidate is not packaged for pasting into Shopify. It has no SDK loader or production adapter. An integration must register and maintain the privacy source, map the documented APIs and prove its transport behavior separately. The synchronous `enqueue` adapter returns `queued` only for accepted queueing, `not_queued` only when non-dispatch is certain; thrown, asynchronous or unknown results mean delivery uncertainty. Native `uetq.push` return values cannot be used directly as that contract without an adapter and review.

## Storage and recovery semantics

The one local ledger is scoped to shop/environment/tag. It contains only digests, state and timestamps. The provisional offline limits are **100 records** and a **90-day review horizon**. These are engineering placeholders, not an approved data-retention policy, conversion window or permission to store data for that period. Capacity blocks additional orders; any expired record holds all orders in this ledger. Neither condition deletes data. A live design still needs a consent-aware retention/deletion procedure and protection against replay after deletion.

Shopify exposes asynchronous storage `getItem` and `setItem`; the documented interface supplies no atomic compare-and-swap operation. [Shopify browser API](https://shopify.dev/docs/api/web-pixels-api/standard-api/browser), accessed September 14, 2026.

| Durable state | What it means | Automatic retry |
| --- | --- | --- |
| `reserved` | Stored before the queue attempt; a crash or consent change may leave its later outcome unknown | No |
| `definitely_unsent` | The adapter explicitly confirmed it did not queue or dispatch | No; reconcile and design a controlled retry first |
| `queued_unconfirmed` | The local adapter accepted the queue call | No; this is not receiver confirmation |
| `delivery_uncertain` | Queue execution threw or returned an unsupported/ambiguous result | No; it may already have dispatched |

If permission changes after reservation, the immediate result can prove that this instance never called the adapter, while durable state remains `reserved`. The contract makes no additional marketing storage write after detecting that revocation. A storage operation already started cannot be canceled. A failed final state write also leaves a reservation; the instance holds all later sends because persistence is uncertain.

A timeout also invalidates the attempt and holds further sends. A late storage read cannot reserve or queue; a previously started write may still finish and is not blindly deleted. A timeout before the adapter is definitely unsent by this instance, while a timeout after invoking it remains delivery-uncertain. The admission cap prevents an unresolved dependency from accumulating unlimited purchase callbacks. The deadline settles the local promise when the event loop can run; it does not cancel the external storage operation or guarantee wall-clock completion while the browser is suspended.

No local API upgrades a record to “received.” A separate receiver/order reconciliation must establish that. Order adjustments require a consistent transaction identity, independently verified account eligibility and their own authorized implementation; this draft does not implement them.

## Verification and release boundary

Root's revised offline run: **28 tests passed, 0 failed**. Twenty-six exercise the local contract; two deliberately reproduce cross-tab limitations. A passing test that reproduces a race does not turn the design into a production pass. Independent review found and prompted corrections to malformed ledger types, unbounded pending work and ledger-wide expiry behavior. The initial and final independent verdicts are recorded separately.

| Check | Result / requirement |
| --- | --- |
| Denied, unknown, malformed consent | Local test PASS; no storage/queue calls |
| Privacy-source readiness and revocation during storage | Local test PASS; stale work discarded |
| Revenue, zero amounts, currencies and field minimization | Local test PASS; synthetic fixtures only |
| Same-instance concurrency, reload, stable IDs and value conflicts | Local test PASS within the stated scope |
| Storage failures, clock rollback, capacity, expiry and ambiguous dispatch | Local test PASS; holds exposed |
| Malformed stored key/fingerprint, stalled storage, admission cap and late completion | Local regression tests PASS; no late dispatch and no blind reservation deletion |
| Cross-tab same-order duplicate guarantee | **FAILED by reproduced counterexample** |
| Cross-tab preservation of distinct-order reservations | **FAILED by reproduced counterexample** |
| Installed standard pageLoad correction | **NOT IMPLEMENTED** |
| Installed purchase sender defect | **UNPROVED** |
| Real SDK behavior after refusal/revocation, desktop/mobile and navigation | **NOT RUN for this draft** |
| Native purchase value/currency/identity and delivery reconciliation | **BLOCKED by missing exact receiver evidence** |
| One purchase sender after a proposed cutover | **NOT VERIFIED** |
| Accelerated checkout, upsell and browser reload with receiver identity | **NOT RUN for this draft** |
| Copilot/server-only checkout compatibility | **NOT IMPLEMENTED; do not assume a browser pixel covers it** |
| Live cutover, campaign launch or spending | **NOT AUTHORIZED** |

A future release must first identify the supported publisher fix or an architecture that resolves the demonstrated races. Then prepare an exact before/after change, independent review, single-sender plan, consent/runtime tests, receiver reconciliation and a rollback that preserves privacy. Do not disable the native app or alter its catalog connection just to make this local candidate appear usable.

## Continuation

The next operator action is to obtain and verify a supported correction for the installed standard sender through the already-prepared publisher support route when the pending contact authorization arrives. This goes first because it addresses the observed defect without introducing a second purchase sender. The contact question is already pending; no repeat was sent.

Independent preparation can qualify actual product-country economics using the previously requested costs and cash/loss limits when supplied. Existing U.S. and Germany campaigns remain subject to current authority and measurement gates; configured daily budgets are not authorization.

Continue through `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, TA-15, the latest relevant Microsoft anchor and this evidence packet. Do not introduce a separate task-state system or install the candidate based on its local test count.
