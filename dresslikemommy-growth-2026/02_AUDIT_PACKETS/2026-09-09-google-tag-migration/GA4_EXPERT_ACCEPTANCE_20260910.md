# GA4 expert acceptance — September 9 local / September 10 UTC

Recorded: 2026-09-10 00:44:01 UTC. Owner: root Google migration task. Status: **STOREFRONT TRANSPORT PARTIAL PASS; receiver and theme release remain gated**.

The saved Google & YouTube configuration and selective disconnection of custom pixel111181921 remain complete. No new tag, reconnection, production setting change, customer information entry, payment or purchase occurred in this checkpoint.

## What passed

- **MAIN133290917985** was bound from rendered Shopify.theme JSON after using the normal Exit preview control. The initial plain URL retained **UNPUBLISHED137881223265**; initial consent findings apply to that preview, not MAIN.
- Published Bamboo Garden Panda PDP sent page_view and view_item to retained **G-N4EQNK0MMB**, both HTTP204.
- One real UI add of MotherS/variant44047096348769 sent exactly one add_to_cart in its complete capture: **USD39.99, quantity1**, correct item and variant, HTTP204.
- Normal Check out opened the checkout page and sent begin_checkout with the same **USD39.99/quantity1/variant**, HTTP204. No contact/address/card field was filled and Pay now was not clicked.
- Preview cookie preferences persisted and changed optional categories from all off to all on, then back to all off with reopened readback.
- After restoring denial and exiting preview, a complete bounded MAIN reload captured488 network events with no truncation and zero Google requests.
- The exact test variant was removed once through the cart UI. Final fresh MAIN readback: cart0, zero preview frames. Temporary tab closed and network inspection disabled.

The app's non-purchase item payload includes sku and variant_id. This does not establish equivalence with the legacy item_sku/session_number fields or purchase value semantics.

## Findings and limits

MAIN currently has no Cookie preferences footer control. The tested consent repair remains in the combined unpublished theme owned by the Merchant task. This checkpoint did not publish or change themes.

Back from checkout briefly showed an empty cart; a fresh page then showed the same test line. The item was subsequently removed and empty state confirmed after a fresh MAIN reload. This repeats the recorded symptom in PROB-2026-09-06-CART-RETURN-DISPLAY; a browser-history cache cause remains a hypothesis. Merchant received the exact finding and owns the combined draft that already includes the reviewed cart correction. This checkpoint does not verify that correction on a return-from-checkout journey.

Product and checkout event buffers were truncated. Their observed requests and HTTP204 responses are positive evidence; they do not prove exactly-once delivery for those journeys. The add-to-cart and final denied-load windows were complete. No remove_from_cart request was observed during removal; support for that event was not assumed.

**HTTP204 is not proof of GA4 report ingestion.** The read-only Shopify cutoff query returned0 orders after2026-09-09T18:05:00Z, including the final00:44:40UTC recheck. No genuine new purchase is available to reconcile. No unsupported API grant or native access workaround was attempted. Peer native selection is now paused following user interruption; the earlier Mac-lock automatic-review denial is historical, not proof of a current lock.

The prior wizard1/3 versus “No tags to migrate” conflict is unchanged. Do not reinstall or reconnect the legacy pixel to change that counter.

## Method and continuity

Root observed UI and supported CDP network events; only whitelisted event fields, status, product identifiers and aggregate counts are retained in [the receipt](GA4_EXPERT_ACCEPTANCE_20260910.json). Raw cookies, client IDs, request headers, checkout token, customer data and full payloads were not persisted. These were QA visits and checkout initiation, not customer acquisition or revenue.

Independent review: **PASS for scoped transport findings**, after correcting the receipt's SKU field labels to the observed app key, sku. The reviewer did not execute the UI journey or test the GA4 receiver. See [the independent review](EXPERT_ACCEPTANCE_REVIEW.md). Owning canonical tracking sections are updated at anchor2026-09-09-ga4-storefront-acceptance-verified after the Pinterest and Microsoft writer intervals; the full-paid control was preserved byte-for-byte.

Next action: complete retained GA4 receiver evidence when the exact native account can be held stable, then reconcile the first genuine Shopify purchase. The Merchant task retains the separately reviewed theme release.

Continuation uses [the canonical prompt](/Users/fsuels/Projects/dresslikemommy/ops/prompts/paid-growth-ai-army-continuation-prompt.md) with anchor2026-09-09-ga4-storefront-acceptance-verified and TA-02; do not repeat the completed migration. Final local checks are recorded in GA4_ACCEPTANCE_CANONICAL_CLOSEOUT_20260910.json.
