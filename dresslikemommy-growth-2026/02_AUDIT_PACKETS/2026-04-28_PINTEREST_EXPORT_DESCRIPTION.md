# PINTEREST_EXPORT_DESCRIPTION

Generated: 2026-04-28
Mode: authenticated browser capture, read-only. No Pinterest, Ads, Shopify, feed, campaign, budget, or tracking setting writes.

## Source Evidence

- Authenticated Chrome profile cookies from the local operator browser were used only to render private Pinterest account pages in a temporary DevTools-controlled tab.
- Raw captured text, screenshots, link lists, and network URL/status logs were written under:
  - `dresslikemommy-growth-2026/01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/`
- Existing local Shopify AOV/CAC evidence was read from:
  - `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-28_LOCAL_SHOPIFY_PACKET_v2.md`

## Generated Files

- `2026-04-28_PINTEREST_EXPORT_DESCRIPTION.md`
- `2026-04-28_PINTEREST_PACKET_v1.md`
- `01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/*.txt`
- `01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/*.png`
- `01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/*_links.json`
- `01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/*_network.json`
- `01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/summary.json`
- `01_EXPORTS_RAW/PINTEREST/2026-04-28_authenticated_browser_capture/ads_reporting_ranges_summary.json`

## Capture Coverage

- Catalog distribution diagnostics.
- Catalog ingestion diagnostics.
- Catalog product groups.
- Catalog data sources.
- Conversion events overview.
- Conversion health / event quality.
- Ads reporting campaigns for 30, 90, and 365 complete-day windows ending 2026-04-27.
- Ads reporting ad-level view for 30, 90, and 365 complete-day windows ending 2026-04-27.

## Safety Notes

- No customer PII, passwords, API tokens, or cookies were written into the repo packet.
- Browser session cookies were read from the local Chrome profile to render pages, but were not exported.
- No export/upload buttons were used; reports were captured from rendered account screens.
- Network logs are URL path/status/type evidence only; query strings were redacted after capture to avoid retaining hashed identifiers or account/browser tracking parameters.
- The old unauthenticated 403 blocker is resolved for these pages by using the authenticated browser context.
