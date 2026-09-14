# Pinterest Phase 1 Preapproval Readback - 2026-06-01

## Scope

- Surface: Pinterest advertiser `549756244483`.
- Campaign: `DLM_PIN_US_PARENT_COLLECTIONS_99_77_34_20260520` / `626758581530`.
- Current no-UTM ad group: `DLM_PIN_US_PARENT_COLLECTIONS_ADGROUP_20260520` / `2680090331049`.
- Date range read back in Pinterest reporting: `2026-05-18` through `2026-06-01` UTC.
- This was read-only preapproval verification. The owner did not paste the exact Phase 1 approval phrase in the current turn.

## Decision

Keep campaign `626758581530` paused.

No Phase 1 setup was executed because the exact approval phrase was not supplied in the current turn. No Pinterest, Shopify, Merchant, Google Ads, GA4, tag/CAPI, billing, budget, bid, product-group, source/feed, campaign status, or other campaign change was made.

## Readback

| Surface | Readback |
|---|---|
| Campaign row | `Paused`; `0 currently being served` |
| Campaign metrics | Spend `$105.30`; impressions `75,037`; Pin clicks `1,005`; outbound clicks `973`; Checkout CPA `$0.00`; Checkout ROAS `0`; Checkout conversions `0` |
| Ad group row | `Active` inside paused campaign; `0 currently being served` because the campaign is paused |
| Ad group metrics | Spend `$97.23`; impressions `70,859`; Pin clicks `949`; outbound clicks `917`; Checkout ROAS `0`; Checkout conversions `0`; Checkout value `$0.00` |
| Product groups | 3 active current no-UTM parent groups: Mommy `99`, Family `77`, Daddy `34` |
| Product group metrics | Mommy `$57.93` / `579` Pin clicks / `560` outbound clicks / `0` Checkout; Family `$27.79` / `264` Pin clicks / `251` outbound clicks / `0` Checkout; Daddy `$11.50` / `106` Pin clicks / `106` outbound clicks / `0` Checkout |

## Current Gate

Phase 1 remains approval-gated. If the owner wants the paused replacement setup executed, the next operator must require the exact Phase 1 phrase from:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-29-pinterest-attribution-safe-relaunch-approval/PINTEREST_ATTRIBUTION_SAFE_RELAUNCH_APPROVAL_PACKET_20260529.md`

The required phrase starts:

`APPROVE PINTEREST ATTRIBUTION-SAFE PAUSED REPLACEMENT SETUP ONLY: keep campaign 626758581530 paused; create or duplicate one replacement ad group under campaign 626758581530...`

Do not treat a paraphrase, partial phrase, or general continuation prompt as approval.

## Evidence

- `raw/pinterest_phase1_preapproval_readback_summary.json`
- `raw/campaigns.txt`
- `raw/adgroups.txt`
- `raw/productgroups.txt`
- `raw/campaigns.png`
- `raw/adgroups.png`
- `raw/productgroups.png`
