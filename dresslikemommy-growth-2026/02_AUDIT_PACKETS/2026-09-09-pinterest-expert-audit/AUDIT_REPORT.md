# Pinterest tracking and growth repairs

Updated September 11, 2026. Confidence: H for the recorded changes and readbacks; M for complete tracking acceptance. **Three live repairs are verified. End-to-end tracking, paid launch readiness, and sales improvement remain unverified.**

## Supplied plan implemented locally — September11

The [owner-plan reconciliation](PLAN_RECONCILIATION_20260911.md) now makes manual Sales/Pins/verified completed Checkout the primary conditional pilot. The old Consideration USD15/72h proposal is archived. One original family-photo P1 checklist graphic is finished, with unchanged existing copy and UTM link; the12-slot capacity register includes the already published Sunshine Pin and two later video concepts. Local production does not mean a new Pin, native campaign or scheduled post was created. Actual costs, native checks and consent approval remain open.

## Implemented and verified

| Change | Result and verification |
|---|---|
| Organic product-detail Pin | [Sunshine Stripe Family Matching T-Shirts](https://www.pinterest.com/pin/343118065387544334/) published once to the existing Mommy & Me Matching Outfits board. Image, saved title, description, alt text, AI disclosure, organic status, destination and four UTMs were verified after reload. The actual Visit site click reached the correct US/English/USD product; child/adult selections worked and cart remained empty. |
| Board description | Removed the unsupported “largest selection … online” claim. The replacement describes the actual clothing categories and directs shoppers to product-specific sizes and included items. One save; exact description verified after reload. |
| Failed sitemap source | Paused future ingestion for source 3041760916127467912 after ten visible September 1–10 runs failed; the inspected error was Error 100. One pause; the exact source's menu still offered Unpause ingestions after reload. Source/history and the other 23 sources were preserved. This contains the failed fetches; it does not establish replacement product coverage. |

The Pin's description appeared populated in the composer but initially saved empty. The same published Pin was corrected using native paste and one Save. A full reload and reopened editor confirmed the exact description. No second Pin was created. The pre-existing Sunshine lifestyle Pin 343118065386636484 remains in place. The public Rich Pin product-description panel is distinct from the saved authored Pin description.

Execution and rollback receipts: [Sunshine publication](SUNSHINE_EXECUTION_20260910.json), [board correction](BOARD_DESCRIPTION_REPAIR_20260910.json), [source pause](FAILED_SOURCE_PAUSE_20260910.json). Independent reviews passed for the board and source pause. A separate parent receipt-to-plan comparison passed 16 checks; it is not an independent native account or creative-audience acceptance test.

Closeout verification passed: independent local review (26 initial and 10 follow-up checks), command integration (25/25; zero risks), strict continuity (10/10; CONTINUITY_OK), scoped whitespace checks, and unchanged paid-control bytes. The generated dashboard marks TA-11 completed and TA-12 open. The stored-feed guard has zero failures and three historical warnings; this is not current catalog certification. [Verification receipts](RESUMED_VERIFICATION_20260910.json).

September11 local closeout also passed: independent evidence/updater review, all10 applied canonical-file hashes, root state/cleanup/authority checks, command integration25/25 with0risks, strict continuity10/10 and scoped git diff --check. These checks validate continuity and recorded evidence, not receiver performance or consent enforcement. [September11 closeout receipt](CANONICAL_CLOSEOUT_20260911.json).

## September 11 supported browser test

Shopify's existing Pinterest app is Connected, Server/Web and Always on. Its privacy declaration requires marketing and analytics permission and excludes collection following sale opt-out. The official helper test ran: page and product events showed green callback dots, and the Sunshine product input contained product/variant IDs and21.99USD. No app setting, permission or production code was changed. Green means successful local callback handling, not provider receipt. [Shopify helper definitions](https://help.shopify.com/en/manual/promoting-marketing/pixels/app-pixels#reviewing-events-received).

Consent acceptance is **CONFLICTED**. After Decline, fresh product navigation initially showed Pixel is awaiting consent. Automatic approval review rejected Give consent; no retry or workaround followed. A later same-tab read showed Loaded and green events without a verified consent transition. Browser control subsequently stopped twice because the user changed Chrome. The test tab remains open, cart0 last verified, stored consent unknown, and cleanup incomplete. Exact Tag14d AddPaymentInfo Product ID coverage remains unread. [September11 native receipt](SHOPIFY_PIXEL_NATIVE_20260911.json), [independent interpretation](PIXEL_HELPER_INTERPRETATION_20260911.md).

Fresh validated theme-role readback confirms MAIN133290917985 and UNPUBLISHED UX137888792673. No theme was changed or published. The next controlled consent test requires explicit temporary test-consent approval and a verified path to restore Decline before granting. The remaining receiver and genuine-order criteria still apply.

## September 10 receiver findings (latest receiver evidence)

The correct advertiser 549756244483 still shows Shopify Connected, merchant Approved, and a verified domain. VMP remains a separate under-review status. The sole visible active tag is 2620007050621, with its latest event at September 10 15:43 UTC. The prior three-route source audit found exactly one expected Shopify Pinterest app configuration per page and no justification for another sender.

The Business Hub's “Good setup” summary is insufficient: detailed **Tag and CAPI Event Quality are Fair** in both inspected windows, updated September 9.

| Receiver evidence | Interpretation and next check |
|---|---|
| Fourteen-day CAPI Product ID: AddPaymentInfo 0%; Checkout/AddToCart/InitiateCheckout 100%; PageVisit 28% | The payment-event discrepancy needs a browser-versus-CAPI comparison. Coverage is not catalog-match proof. Tag AddPaymentInfo's exact percentage remains unread. |
| Fourteen-day CAPI Click ID 0% across seven event types | Determine whether qualifying genuine Pinterest clicks occurred and survived storage/redirects/consent. This organic QA click had no epik, so it cannot validate capture. |
| Email coverage AddToCart 5%, AddPaymentInfo 57% | Automatic enhanced match is already enabled with every displayed option selected. Guest/data/consent availability must be distinguished from failed mapping. |
| Metadata warnings differ between Tag and CAPI | Product quantity, price, brand/category/title and search-query fields need event-specific evaluation. Generic banners do not prove missing configuration. |
| Duplicate-event-ID good health displayed for PageVisit/ViewCategory | This does not prove that a genuine purchase is received once with matching order identity, discounts, value and currency. |

The captured app script already maps payment_info_submitted to AddPaymentInfo, derives product IDs, and contains epik capture logic. Eleven extracted-handler fixture assertions passed. These findings narrow the diagnosis; they do not certify managed CAPI forwarding. [Independent mapping review](TRACKING_MAPPING_REVIEW_20260910.md), [native receiver evidence](NATIVE_HEALTH_20260910.json).

The [partner diagnostic packet](PINTEREST_PARTNER_DIAGNOSTIC_PACKET_20260910.md) is prepared and **not sent**. The September11 Test/permissions/privacy inspection is complete with the limits above; the controlled consent repeat and exact Tag/CAPI comparison remain. Connector pixel/privacy reads lack required scopes; no scope expansion, reinstallation, enhanced-match toggle, extra pixel or fabricated event was attempted.

The consent repair is preserved in the current combined **UNPUBLISHED theme 137888792673**, owned by the UX release integrator; older 137881223265 and consent-only 137880666209 are historical candidates. MAIN 133290917985 was not changed by this task. Prior consent tests and rendered preview checks passed, but this is not live publication or receiver-side consent proof. Managed Arabic privacy-dialog content remains unresolved. [Consent handoff](CONSENT_RELEASE_HANDOFF.json), [prior runtime proof and limits](CONSENT_RUNTIME_QA.json).

## Catalog reconciliation

All 24 primary sources were listed:19 Shopify and 5 URL sources. Their market/variant rows must not be added together as unique products. The distribution view showed 121.26 k approved (99.56%) and 538 not approved (0.44%), with Products out of stock as the only displayed reason. Ten sampled excluded variants independently read availableForSale=false, DENY and inventoryQuantity 0 in Shopify. That sample supports correct exclusion; the full 538 population was not checked.

Four variant IDs from older NL/HE invalid-GTIN warnings now have barcode=null in fresh Shopify reads, consistent with the existing Merchant repair. No second barcode or inventory mutation was needed. A newer Japanese ingestion showed 4,945 successful items and zero failed items, but its 277 warning summary contradicted an empty issue table. This conflict remains open. The isolated 210-item source showed 100% success and zero failed/warning products; its unchanged-source early-completion notice is informational. Current parent grouping, image consistency, actual item matching and complete managed-feed propagation remain unverified. [Catalog and sample receipts](CATALOG_RECONCILIATION_20260910.json).

## Traffic and paid execution

The new Pin is a real organic distribution step, not evidence of acquired traffic or sales. Exclude identifiable QA. September 11 is the first complete reporting date; review the first 7,14 and 30 complete dates on September 18, September 25 and October 11. Measure outbound clicks, tagged landing sessions, carts, distinct orders, CPA and retained contribution. No monitoring automation was created by this task.

The existing [four-week content plan](STRATEGY_AND_ASSET_READINESS.md) tests three useful Pins per week, including this Sunshine Pin. Six later product-copy drafts remain local. Use verified product images, specific shopping questions, relevant boards and matching landing pages; expand only with measured results and source-supported claims.

The current [paid campaign specification](PAID_CAMPAIGN_SPEC.json) remains **NOT_LAUNCH_READY** and now proposes manual Sales/Pins with explicitly selected completed Checkout. USD5fixed-daily is a planning starting point only; total cap, max loss, dates and approved CPA are unset. Native enforcement, overlap, current economics and purchase/consent receipt must be qualified. The previous USD15/72h Consideration and USD0.15in-grid bid are [archived alternatives](PAID_CAMPAIGN_SPEC_20260909_ARCHIVE.json), not Sales spend authority or an outbound-price guarantee. [Pinterest objectives](https://help.pinterest.com/en/business/article/simplified-objectives), [budget modes](https://help.pinterest.com/en/business/article/set-up-campaign-budgets).

The current full-paid control remains NONE. No campaign, budget, bid, billing or spend was changed. The hub's no-active-campaign-in-last 30 days statement is a hub snapshot, not a full campaign-status audit. The earlier Shopify Pinterest referral slice of 3 sessions/1 cart-session/0 checkouts predates this release and remains dated evidence; whole-store orders cannot be attributed to Pinterest from matching event counts.

## Remaining execution boundary

Native Shopify diagnostics resumed September11 after explicit handback and scoped Computer Use recovery. After two later user-changed-app interruptions, native actions stopped and the lease was returned to Merchant once user activity permits. No unsaved edit form exists; the test tab is still open for cleanup. Current stored consent must not be assumed declined.

**Next action: approve one controlled temporary consent test, with a verified restoration path, then finish the same-window Tag/CAPI comparison when Chrome is available.** This comes first because consent and receiving-event accuracy affect whether paid traffic can be measured responsibly. Preserve the completed Pin, board copy and paused failed source. A genuine paid order remains necessary for order/value/currency/deduplication acceptance; this task will not place or pay for one.

Automatic approval review rejected the helper's Give consent action because it would authorize tracking/data transmission without explicit permission for this QA action and destination. It was not retried. The earlier detailed internal status-message rejection is preserved in the September10 record; no support message was sent.

Completed live repair anchor:2026-09-10-pinterest-organic-release-and-source-repair. New diagnostic checkpoint:2026-09-11-pinterest-pixel-callback-and-consent-conflict. Continue through the [canonical paid-growth prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md); this report is evidence and does not grant spend authority.
