# Pinterest Attribution-Safe Relaunch Approval Packet - 2026-05-29

## Scope

- Packet type: local approval packet only.
- Current live status to preserve: Pinterest campaign `626758581530` / `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520` remains `Paused`.
- Advertiser: `549756244483`.
- Current no-UTM ad group: `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049`.
- Current no-UTM source: `DLM US Paid Parent Collection Intent 2026-05-20` / `3041760889836768751`.
- Recommended UTM-bearing source: `DLM US Paid Parent Isolated 2026-05-21` / `3041760890485574219`.
- This packet does not approve any live external write by itself.

Do not relaunch or change budget, bid, product groups, source/feed, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, or any other campaign unless the owner pastes an exact approval phrase from this packet or a later narrower packet.

## Why This Packet Exists

The spend-safety pause stopped a zero-return Pinterest campaign. The post-pause diagnostic then narrowed the relaunch blocker:

- Campaign `626758581530` still read `Paused`.
- Refreshed reporting row for `2026-05-18` through `2026-05-29` UTC read `$105.30`, `75,021` impressions, and `1,005` Pin clicks.
- Pinterest Events Manager receives `Checkout` from `Api + Tag`, but Event Quality is `Fair` and flags `Click ID` gaps on Checkout/AddToCart.
- Ten sampled catalog PDP links loaded with add-to-cart surfaces.
- Current parent source has `0/210` UTM or `dlm_pg` links.
- Shopify preserved manual UTM probes `10/10`, so Shopify is not stripping attribution parameters when present.

Conclusion: do not restart the old no-UTM ad group. The next safe sales-moving path is to replace the active spend path with the already-verified isolated UTM-bearing source while the campaign remains paused, then read back everything before a separate relaunch decision.

## Recommended Path

Use the existing verified isolated source and product groups. This is better than editing the old source because it already avoids the prior Pinterest catalog collision problem and already carries UTM/`dlm_pg` links.

Verified isolated source:

| Item | Readback |
|---|---|
| Source name | `DLM US Paid Parent Isolated 2026-05-21` |
| Source ID | `3041760890485574219` |
| Feed route | `pinterest-paid-parent-isolated-feed.tsv` |
| Rows | `210` |
| Successful uploads | `210 of 210` |
| Failed uploads | `0` |
| Warnings | `0` |
| Images | `Completed` |
| UTM rows | `210/210` |
| `dlm_pg` rows | `210/210` |

Verified isolated product groups:

| Lane | Product group | ID | Count |
|---|---|---:|---:|
| Mommy & Me | `DLM_PIN_US_ISOLATED_PARENT_MOMMY_AND_ME_99_20260521` | `4673019914864` | `99` |
| Family Matching | `DLM_PIN_US_ISOLATED_PARENT_FAMILY_MATCHING_77_20260521` | `4673019915037` | `77` |
| Daddy & Me | `DLM_PIN_US_ISOLATED_PARENT_DADDY_AND_ME_34_20260521` | `4673019915140` | `34` |

## Phase 1: Paused Replacement Setup Only

Goal: create a spend-safe replacement path inside the paused campaign using only the UTM-bearing isolated source and product groups. Stop before relaunch.

Allowed if approved:

- Keep campaign `626758581530` paused.
- In campaign `626758581530`, create or duplicate one replacement ad group using source `3041760890485574219`.
- Attach only isolated product groups `4673019914864`, `4673019915037`, and `4673019915140`.
- Copy delivery, targeting, destination, CTA, tracking, and bid fields from current ad group `2680090331049` only after before-state readback.
- Neutralize the old no-UTM ad group `2680090331049` only if needed so a later campaign relaunch cannot spend through the no-UTM source.
- Capture before/after readbacks of campaign paused status, ad group statuses, source, product groups, URL tracking, bid, and cost.

Not allowed in Phase 1:

- Do not relaunch the campaign.
- Do not change campaign budget.
- Do not increase or otherwise alter bid economics beyond copying the current readback if Pinterest requires a bid field on the new paused ad group.
- Do not change tag/CAPI, Shopify, Merchant, Google Ads, GA4, billing, product data, or any other campaign.
- Do not attach broad `All Products` or old no-UTM product groups.

### Exact Approval Phrase: Phase 1

`APPROVE PINTEREST ATTRIBUTION-SAFE PAUSED REPLACEMENT SETUP ONLY: keep campaign 626758581530 paused; create or duplicate one replacement ad group under campaign 626758581530 using only Pinterest source 3041760890485574219 / DLM US Paid Parent Isolated 2026-05-21 and product groups 4673019914864 / 4673019915037 / 4673019915140; copy current delivery, targeting, destination, CTA, tracking, and bid fields from ad group 2680090331049 only after before-state readback; neutralize old no-UTM ad group 2680090331049 only if needed to prevent future no-UTM spend; do not relaunch, do not change campaign budget, do not change bid economics except copying the current readback if required, do not change tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, product data, sources beyond this isolated source, or any other campaign; stop after before/after readbacks of campaign paused status, ad groups, source, product groups, URL tracking, bid, and cost.`

## Phase 2: Event Quality Click-ID Repair/Readback

Goal: address the Pinterest Event Quality click-ID gaps without changing campaigns or spend.

Recommended sequence:

1. Read back Event Quality details for both Conversions API and Pinterest Tag before any repair.
2. Inspect only the relevant Pinterest/Shopify integration surfaces needed to identify why Checkout/AddToCart click ID quality is weak.
3. If the fix is a clearly bounded setting in the Pinterest app or Pinterest integration, prepare and execute only that exact approved repair.
4. If the fix requires custom code, custom pixel/CAPI changes, checkout changes, or app reinstall/reconnect, stop and prepare a narrower implementation packet first.
5. Read back Tag Manager and Events Manager after the fix. Because Event Quality can lag, record both immediate readback and the next-day readback requirement.

### Exact Approval Phrase: Phase 2 Read-Only Root Cause

`APPROVE PINTEREST EVENT QUALITY CLICK-ID ROOT-CAUSE READBACK ONLY: inspect Pinterest Events Manager/Event Quality details, Tag Manager, and Shopify/Pinterest integration surfaces only to identify why Checkout/AddToCart Click ID quality is weak; do not save, publish, reconnect, reinstall, edit code, change tag/CAPI, change Shopify, change campaign settings, change sources, or change billing; stop with the smallest exact repair packet and before-state readbacks.`

### Exact Approval Phrase: Phase 2 Bounded Repair

Use this only after a specific setting-level repair is identified:

`APPROVE PINTEREST EVENT QUALITY CLICK-ID BOUNDED REPAIR ONLY: after before-state readback, change only the specific Pinterest/Shopify integration setting identified in the root-cause packet to improve Checkout/AddToCart Click ID quality; do not change campaign status, budget, bid, product groups, sources/feed, billing, Shopify product data, Merchant, Google Ads, GA4, or any other campaign; do not edit custom code, custom pixel/CAPI code, checkout code, reconnect apps, or reinstall apps unless separately approved in a narrower phrase; capture immediate Tag Manager/Event Quality readback and record the next-day Event Quality reread requirement.`

## Phase 3: Relaunch Only After Phase 1 And Phase 2 Gates Pass

Goal: turn spend back on only after the old no-UTM route cannot spend and the attribution readbacks are acceptable.

Preconditions:

- Phase 1 readback shows campaign `626758581530` still paused.
- Exactly one intended UTM-bearing replacement ad group is spend-eligible for relaunch.
- Old no-UTM ad group `2680090331049` cannot spend after relaunch, or the operator stops and asks for a narrower neutralization approval.
- Product groups are exactly `99/77/34` from source `3041760890485574219`.
- No broad product groups are attached.
- Event Quality root-cause readback is complete, and any owner-approved repair/readback is recorded.
- Before-state campaign spend/status is captured immediately before relaunch.

### Exact Approval Phrase: Phase 3

`APPROVE PINTEREST ATTRIBUTION-SAFE RELAUNCH ONLY: after Phase 1 paused replacement setup readback passes and Event Quality click-ID readback/repair status is documented, change only campaign 626758581530 from Paused to Active; relaunch only if the old no-UTM ad group 2680090331049 cannot spend and the active spend path uses source 3041760890485574219 with product groups 4673019914864 / 4673019915037 / 4673019915140; do not change budget, bid, product groups, source/feed, tag/CAPI, billing, Shopify, Merchant, Google Ads, GA4, product data, targeting, or any other campaign; capture before/after campaign/ad group/product-group status and spend readbacks immediately.`

## Stop Conditions

Stop immediately and report if any of these happen:

- Pinterest requires a budget, bid, tracking, product-group, source, or campaign setting change outside the approval phrase.
- The old no-UTM ad group cannot be neutralized before relaunch.
- The isolated source or product groups no longer read back as `210`, `99/77/34`, `0` failed, and `0` warnings.
- Event Quality repair requires app reconnection, code edits, custom CAPI/tag implementation, checkout changes, or Shopify Admin changes not named in the approval phrase.
- A login, MFA, CAPTCHA, permission, billing, policy, destructive-confirmation, or account-switch prompt appears.

## Evidence

- Post-pause diagnostic: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-29-pinterest-post-pause-tracking-landing-diagnostics/PINTEREST_POST_PAUSE_TRACKING_LANDING_DIAGNOSTICS_20260529.md`
- Isolated source/product groups: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-21-pinterest-isolated-catalog-diagnosis/PINTEREST_EXACT_LABEL_INDEX_DIAGNOSIS_20260521.md`
- Current parent ad group setup: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-pinterest-shopify-collection-mapping/PINTEREST_PARENT_PAID_SOURCE_EXECUTION_READBACK.md`

## Recommendation

Ask for Phase 1 only first. It is the safest next action because it builds the attribution-safe route while spend remains off. Do not request Phase 3 relaunch until Phase 1 readback proves the no-UTM path cannot spend and Phase 2 Event Quality status is documented.
