# Paid Growth CZ/RO/PT/GR Paused Search Build

Session anchor: `2026-05-10-paid-growth-cz-built-ro-preview-pending`

Starting anchor: `2026-05-10-paid-growth-browser-recovery-it-pl-paused-search-built`

Scope:
- Parent/orchestrator continuation of the already owner-approved paused non-US Google Search `TEST BUILD`.
- Countries in scope: `CZ`, `RO`, `PT`, and `GR`, one at a time.
- `FR` stays parked for a fresh non-stale preview/no-duplicate readback.
- `BE` stays last after upload-throttle cooldown.

Guardrails:
- No live spend or campaign enablement.
- No completed-country re-uploads.
- No existing campaign budget, bid, or status changes.
- No PMax, Standard Shopping, US campaign `23827590655`, Merchant, Shopify product-data, Pinterest, theme, product-scope/feed-label/product-group, or conversion-goal changes.
- Parent owns any Google Ads write; subagents are local/read-only only.

Evidence will be collected here plus in the existing approved build packet where the reusable Google Ads helpers write raw output:
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-google-ads-non-us-search-paused-test-build-approved/`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-browser-recovery-and-remaining-search-preflight/`

Closeout:
- `CZ` was created only inside the owner-approved paused TEST BUILD scope and read back clean as paused/Search/`$1/day`/presence-only/content off/YouTube off.
- `RO` preview started but remained in progress after bounded waits; the `RO` campaign still reads absent and no apply was clicked.
- `PT` and `GR` were intentionally not attempted because the one-country-at-a-time guard blocks stacking uploads behind an in-progress preview.
