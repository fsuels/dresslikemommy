# Pinterest account audit — September 9, 2026

> Historical September 9 readbacks follow. The September 10 checkpoint at the end supersedes their pending Pin/access steps. Use AUDIT_REPORT.md and the dated 20260910 receipts for current status.


Evidence grade: LIVE_VERIFIED for the explicit UI observations below; incomplete audit, no production changes.
Surface: existing Pinterest tab in Chrome profile test, selected from the user-provided Business Hub. Account dresslikemommy; advertiser 549756244483; business 343118202768859516; catalog 3041764155561548387. Observations completed before the explicit clock check at 16:38:52 UTC; individual tool observations did not record wall-clock timestamps. Sources are native accessibility-tree observations in the current task; no private event/customer payload exported.

## Business Hub

URL: https://www.pinterest.com/business/hub/

- Profile: Dress Like Mommy | Matching Family Outfits; https://www.pinterest.com/dresslikemommy/.
- Merchant status Approved. Shopify Connected. Verified domain link dresslikemommy.com. VMP under review is a separate status from merchant approval.
- Hub Event Quality Score link says Good setup. This is not certification of individual event fields or purchase accounting.
- Last 30 days preview: one total campaign; no active campaigns in the last 30 days. Detailed campaign status, settings and historical performance remain unread.
- Catalog preview says Data sources 3 of 24; all three visible Shopify rows show Completed, ingestion September 8, 4,897 products each. This is a preview, not a complete source reconciliation or unique product count. Do not sum the rows.
- Organic top-Pin preview: 5 Ways to Style Mommy & Me Matching Dresses for Spring 108 impressions / 2 engagements; Matching Family Pajamas 48 / 5; Mother and daughter beach floral maxi dress 46 / 2. Total organic impressions, outbound clicks, sessions and attributed purchases remain unknown.

## Conversion receipt

URL: https://ads.pinterest.com/advertiser/549756244483/conversions/events-overview/
Filter: Last 30 days; All events overview. UI explicitly says totals are after duplicate events are removed. All listed event types show Api · Tag.

| Event | Total | Last received, UTC |
|---|---:|---|
| PageVisit | 14,883 | September 9 16:36 |
| ViewCategory | 4,625 | September 9 16:25 |
| AddToCart | 326 | September 9 15:54 |
| InitiateCheckout | 49 | September 6 21:30 |
| AddPaymentInfo | 21 | September 5 15:18 |
| Search | 18 | September 7 11:08 |
| Checkout | 10 | September 6 21:31 |

These are store event receipts, not Pinterest-attributed sales, unique shoppers, or certified Shopify paid orders. The post-deduplication display does not independently prove correct event-ID overlap or rule out extra emitters. No synthetic Checkout event or purchase was generated.

## Event quality

URL: https://ads.pinterest.com/advertiser/549756244483/conversions/health/
Header updated September 8, 2026. Web events: Needs attention. Selected source: Conversions API. Selected window: Last 14 days. The page's detailed components had not yet rendered in the last Pinterest observation. Exact warning, coverage, product-ID match, value/currency and overlap details remain LIVE_READBACK_REQUIRED.

The hub Good setup label and detailed Needs attention label may refer to different dimensions/windows. They are a discrepancy to investigate, not proof that the entire installation is broken.

## Browser coordination boundary

A following read returned Google Tag Assistant instead of Pinterest. The two separate active tasks Audit Microsoft Ads tracking and Migrate Shopify Google tags also control native Chrome. Pinterest actions stopped at that unexpected surface change; no controls in their tabs were touched. The user was asked whether the tasks may coordinate uninterrupted browser turns. This is a concurrent-control dependency, not a current login or Mac-lock failure. Existing Google and Microsoft claims remain intact.

The Google migration task subsequently sent an explicit five-minute native Chrome lease request while its already-saved migration proceeds through duplicate cleanup. Pinterest acknowledged and continues only local/connector work during that lease. The Google task will send release; no Google tag, custom pixel, migration wizard or Tag Assistant control is touched by Pinterest.

### Final access checkpoint

Google released to Merchant, Merchant released to Microsoft, and Microsoft released to Pinterest. The other tasks reported title-only Chrome, empty accessibility output and unavailable screenshots despite fresh app selection and normal recovery; Finder remained readable. Root read their exact recovery evidence and the Computer Use recovery skill, and did not repeat those attempts or change permissions, helpers or browser state.

A materially different exact-site fallback used Codex In-app Browser1, tab1, https://www.pinterest.com/business/hub/. Its rendered header identifies **Santo Ruidos** and profile santoruidos, not Dress Like Mommy. Root stopped at this wrong-account boundary without opening its reporting or account switcher. The tab is marked for handoff; open_in_codex returned queued, not confirmed visible. An asynchronous owner request asks them to switch this tab to Dress Like Mommy and confirm. The native lease has been released. Current gate is ACCOUNT_SWITCH_REQUIRED for the isolated browser plus degraded native Chrome, not Mac locked or missing global permissions.

## Next checks

### Subsequent public buyer-route check

After the account gate, a separate temporary isolated tab opened the exact existing Sunshine organic URL with all four UTMs intact. Initial session country was Spain/EUR. Normal storefront country selection changed only this shopping session to United States/USD, then restored Spain/EUR before closing the temporary tab. No account/production setting changed.

Observed: correct Sunshine Stripe product; USD21.99–24.99 range; explicit each-selection-sold-separately and one-T-shirt disclosure; seven child options from2Years through9–10Years and seven adult optionsS–4XL. Selecting AdultM enabled Add this piece to bag. Switching toChild reset the button toPick a size; selectingChild2Years enabled it and showed Ready to add Child2Years–USD21.99. Desktop screenshot and390x844mobile screenshots showed readable selections, selected-shirt price and purchase button. Temporary viewport override reset. Cart remained0, no add-to-cart/checkout/purchase action. This is rendered product/selection proof, not a full cart/checkout, consent or event-receipt test.

The observed footer had Privacy policy but no visible cookie-preferences control in this existing session. This does not identify the session's consent state or prove the source-level reopening hypothesis; fresh consent/reject/reopen/revoke testing remains unresolved. QA visits may appear in later analytics and must not be reported as newly acquired Pinterest shoppers.

Publisher profile/board/duplicate/preview checks remain pending in the correct DLM session. Reuse this product-route result instead of repeating it without changed evidence; the actual publishing clickthrough still needs an after-state.

1. Obtain the correct Dress Like Mommy session in the isolated browser, then read source-specific event quality, tag manager ID, checkout value/currency/order/event IDs and overlap.
2. Reconcile actual Shopify paid orders to Pinterest Checkout receipts for the same period using only required aggregate/sanitized data; respect the separate Google migration's tracking ownership.
3. Read the existing one campaign, full source health (especially source 3041760916127467912 versus isolated 3041760890485574219), source/item-ID grouping and eligible product groups.
4. Finish exact profile/board/duplicate/buyer checks for the already reviewed Sunshine product-detail Pin, publish once under saved authority and verify the public Pin and clickthrough.

Live changes: zero. New campaign, upload, publication, tag/CAPI/catalog changes, spend, billing and account changes: zero.

## September 9 evening continuation — selected-tab gate

The later owner supplied the exact advertiser549756244483 health URL. Native Chrome profile test became readable, superseding the earlier locked-Mac barrier for this scoped read. Both fresh attempts to select the existing Pinterest tab were interrupted by user-driven tab changes. The final visible surface was unrelated to Pinterest; root stopped, took no further action there and retained no unrelated private content in this packet. Current Pinterest diagnostics were not read.

Only the in-app browser adapter was available. One disclosed direct attempt to open the exact advertiser health URL there was rejected by automatic approval review as an unauthorized workaround around the private-account access-control gate. No content was read, no new tab result was returned, and no retry or indirect account request followed. Current pending owner action is to select Pinterest Event Quality in Chrome test and leave Chrome unused10minutes, then reply Ready. Native leases remain suspended until changed readiness.

Public source and product checks continued independently and passed; two validated Shopify reads stopped on missing read_pixels/read_privacy_settings. Full evidence and scope: EVENING_CHECKPOINT_20260909.json; source and product receipts; TRACKING_ACCEPTANCE_REVIEW_20260909_EVENING.md. No new Pin, campaign, spend, settings, catalog or theme write occurred. Anchor2026-09-09-pinterest-source-refresh-and-selected-tab-gate.


## September 10 — completed organic and source repairs; detailed receiver findings

Correct Dress Like Mommy advertiser549756244483 and tag2620007050621 were read in the original native Chrome path. Shopify is Connected, merchant Approved and domain verified; VMP is separately under review. Actual enhanced-match options are already enabled with all displayed options selected. One-day and fourteen-day Tag/CAPI views are Fair, updated September9; the hub Good setup label is insufficient. Exact event-level percentages and interpretation limits are saved in NATIVE_HEALTH_20260910.json.

The authorized Sunshine product-detail Pin343118065387544334 was uploaded and published exactly once. Its composer description initially failed to persist; native paste plus one Save corrected the same Pin. Full reload and reopened editor verified all saved fields. The public Pin image/identity and actual Visit site URL/UTMs, US/English/USD and child/adult selections passed. Cart remained0; no order was made. The pre-existing lifestyle Pin343118065386636484 remains preserved. SUNSHINE_EXECUTION_20260910.json records the receipt and metadata correction separately.

Board343118134050368248 had its unsupported largest-selection claim replaced with factual category guidance. One save and full-reload exact text readback passed. Failed source3041760916127467912 was paused once after ten visible failed runs; Error100 was the inspected error. The exact source retained history and offered Unpause ingestions after full reload. No deletion or replacement was made. Both narrow repairs passed independent pre-write review and have before/after/rollback receipts.

All24 catalog sources were listed. Four older invalid-GTIN examples now have barcode=null in fresh Shopify reads; ten sampled stock exclusions independently show availableForSale=false/DENY/0. Preserve correct existing repairs and stock suppression. The newer Japanese warning summary versus empty detail table remains a conflict. CATALOG_RECONCILIATION_20260910.json contains the bounded sample evidence; it does not certify all products or actual catalog matching.

After these completed checks, coordinate clicks failed twice with noWindowsAvailable despite readable Pinterest accessibility state. A later System Settings read succeeded after a long tool delay. No TCC reset, helper restart, alternate private Pinterest session or configuration workaround followed. Chrome and the shared-file interval were explicitly released to the Merchant task at17:59UTC; no unsaved Pinterest form remained. Its selected surface and all old coordinates are stale for this task. The previous10-minute/Ready question is superseded, not still pending here.

Next supported step after normal Chrome handback is Shopify Customer events → Pinterest Test/permissions/privacy and an exact Tag/CAPI comparison, including Tag AddPaymentInfo Product ID. No purchase, CAPI mapping, catalog-match, receiver consent or acquisition result is certified. A redacted diagnostic packet is prepared but not sent. No pixel/privacy/theme/campaign/budget/billing/spend write occurred in this September10 continuation.


## September 11 — Shopify native pixel diagnosis

Correct store and Pinterest app verified through Customer events: Connected, Server/Web, Always on. Privacy requires marketing and analytics and excludes collection after sale opt-out. These are declarations; Always on is an optimization setting and does not override consent. App installation date remains August 25, 2022. No app setting or permission was changed.

The official Test opened Shopify Pixel Helper for pixel 22577249. Real page/search events appeared; the Sunshine product later showed green page_viewed and product_viewed callback dots. Non-personal product data contained IDs7545279512673/44116031373409, amount21.99 and USD. These are local callback/input checks, not Pinterest receipt, transmitted-payload validation, catalog matching, purchase value or deduplication proof.

A real Decline choice at12:22:31PM removed the banner. Fresh product navigation initially displayed Waiting to load / Pixel is awaiting consent. Automatic approval review rejected the requested Give consent action because it would change a privacy choice and authorize Pinterest data transmission without explicit test-specific approval. No retry or workaround occurred. Later the same helper showed Loaded and two green events dated12:22:48PM; the consent transition has no verified cause or SDK readback. Refusal/revocation acceptance is CONFLICTED, not passed.

A stale native menu was recovered by restarting only the observed Computer Use helper after one session reset failed; System Settings AX/screenshot worked, so no Mac-lock or TCC cause was inferred. Later two user-changed-app interruptions stopped further native actions. The existing test tab remains open, cart last verified0, stored consent unknown, and cleanup incomplete. Native lease returned to Merchant once user activity permits. No production theme/pixel/campaign, cart, order or payment mutation occurred. MAIN133290917985 and UNPUBLISHED UX137888792673 roles were independently refreshed by validated Shopify query.

Exact Tag14d AddPaymentInfo Product ID coverage and a new Pinterest receiver comparison remain unread. September10 receiver metrics remain dated evidence. [Structured receipt](SHOPIFY_PIXEL_NATIVE_20260911.json); [independent helper meanings](PIXEL_HELPER_INTERPRETATION_20260911.md).
