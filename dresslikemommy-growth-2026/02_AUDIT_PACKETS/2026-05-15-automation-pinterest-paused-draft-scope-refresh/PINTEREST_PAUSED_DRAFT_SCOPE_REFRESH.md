# Pinterest Paused Draft Scope Refresh

Date: `2026-05-15 04:49 EDT`
Status: `PASS_WITH_HELD_PUBLIC_ROWS`

## Purpose

Refresh the public storefront and image readiness evidence for the already-approved Pinterest US paused draft scope before any future Ads Manager draft creation. This packet is local/read-only and does not create or edit Pinterest objects.

## Inputs

- Clean scope: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`
- Exclusions: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`
- Prior local spec validation: `PASS`

## Result

- Clean rows preserved: `342`
- Unique variants: `342`
- Unique products checked publicly: `32`
- Unique image URLs checked: `32`
- Explicit exclusions preserved: `4`
- Product group variant counts: `{"family_matching": 103, "mommy_me": 210, "pajamas": 29}`
- Product group unique product counts: `{"family_matching": 7, "mommy_me": 28, "pajamas": 1}`
- Public product pages pass/hold: `30` / `2`
- Public images pass/hold: `32` / `0`
- Refreshed clean variant rows after public source holds: `333`
- Refreshed excluded variant rows: `9`
- Refreshed product group variant counts: `{"family_matching": 103, "mommy_me": 201, "pajamas": 29}`

## Decision

The Pinterest scope remains a paused-draft-only candidate. It is still not live-launch authority and it must not create spend, enablement, catalog/source/tag/CAPI changes, or product-group mutations outside the paused spec and current approval gates.

Use `pinterest_paused_draft_refreshed_clean_scope.csv` for the next paused-draft prefill instead of the older full `342` rows unless the held public product rows are repaired and read back clean. The hard blocker found in this refresh is public supplier/source-domain leakage on held product pages, so those rows stay excluded from paid Pinterest use.

Next account-capable step: use the restored advertiser `549756244483` access, create only the paused/draft shell from `PINTEREST_US_PAUSED_DRAFT_BUILD_SPEC.md`, and stop before any budget/bid/enablement/launch/publish/audience/source/feed/tag/CAPI mutation if Pinterest requires it.

## Evidence Files

- `pinterest_paused_draft_public_product_readback.csv`
- `pinterest_paused_draft_image_readback.csv`
- `pinterest_paused_draft_refreshed_clean_scope.csv`
- `pinterest_paused_draft_refreshed_public_exclusions.csv`
- `pinterest_paused_draft_scope_refresh_summary.json`

## Guardrails

- No Pinterest campaign, ad group, ad, product group, catalog, source, tag, CAPI, audience, budget, bid, status, launch, or spend write occurred.
- No Shopify Admin, Merchant, Google Ads, GA4/GTM, billing, credential, product, feed, or live theme write occurred.
- Platform `IN_STOCK` is treated only as a feed diagnostic; no customer-facing copy claims local stock, owned inventory, warehouse inventory, or guaranteed on-hand availability.
