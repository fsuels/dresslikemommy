# DLM Google Remediation Master Change Log

Created: 2026-03-27 15:43:21 EDT
Objective: Create a pre-edit Google measurement inventory and backup before any production remediation work.

## Scope

- Repo scanned locally for:
  - `G-N4EQNK0MMB`
  - `GT-PJ5D7RB`
  - `GTM-5QVH4W3`
  - `AW-853411529`
  - `G-3VR0TDX4ZK`
  - `google-analytics.com`
  - `googletagmanager.com`
  - `googleadservices.com`
  - `gtag(`
- Active code/deployment files with hits:
  - `layout/theme.liquid`
  - `ops/customer-events/ga4-checkout-ecommerce-pixel.js`
- Documentation-only references were also found in:
  - `DressLikeMommy-Master-Implementation-Plan.md`
  - `ops/AGENT_WORKLOG.md`
  - `ops/AGENT_WORKLOG_utf8.md`

## Active Findings Summary

- Active code/deployment hit count: 13 lines across 2 files.
- Storefront GTM container `GTM-5QVH4W3` is hardcoded in `layout/theme.liquid` and referenced again in the checkout custom pixel helper under `ops/customer-events/ga4-checkout-ecommerce-pixel.js`.
- Storefront GA4 measurement `G-N4EQNK0MMB` is hardcoded in `layout/theme.liquid` and used by a fallback `gtag(...)` configuration block.
- No active local code/deployment hits were found for:
  - `GT-PJ5D7RB`
  - `AW-853411529`
  - `G-3VR0TDX4ZK`
  - `google-analytics.com`
  - `googleadservices.com`
- No local repo script references to `123LegalDoc` were found. The only `123LegalDoc` / `G-3VR0TDX4ZK` mentions were documentation references inside `DressLikeMommy-Master-Implementation-Plan.md`.

## Suspect / Watchlist

- No repo-local 123LegalDoc runtime script was found.
- Any Shopify Admin app embeds, Google & YouTube sales-channel tags, GTM workspace tags, or Web Pixels that are configured outside this repo remain out of scope for a file-only local scan.

## Backup

- Local backup zip created:
  - `dlm-google-remediation-2026-03-27/dresslikemommy-theme-backup-2026-03-27.zip`
- Backup size at creation:
  - `33M`

## Blockers

- None for local theme/code availability; the theme repository is present and scannable.
- Remaining blocker for full Google remediation attribution: admin-side and third-party app configurations cannot be proven or cleared from repo files alone.

## Phase 1 Repo Execution

Updated: 2026-03-27 16:42:14 EDT

- Removed the storefront GTM snippet from `layout/theme.liquid`.
- Removed the storefront GTM noscript iframe from `layout/theme.liquid`.
- Removed the theme-level GA4 fallback `gtag(...)` path from `layout/theme.liquid`.
- Kept `window.dataLayer` and `window.dlmAnalyticsContext.site_language` so theme-side ecommerce payloads can still push non-Google events into `dataLayer`.
- Replaced `ops/customer-events/ga4-checkout-ecommerce-pixel.js` with a deprecation stub so the repo no longer carries a ready-to-deploy Google custom pixel implementation.

## Phase 1 Remaining Browser-Only Actions

- Shopify Admin:
  - disconnect or delete the active `GA4 Checkout Events` custom pixel
  - remove deprecated checkout Additional Scripts entries for:
    - `UA-88409806-1`
    - `AW-853411529`
    - `AW-853411529/LeL6CMiLmYcBEMmN-JYD`
- Google & YouTube:
  - confirm the supported Google measurement path remains connected and healthy
  - confirm only store-owned Google tags remain linked
- GTM:
  - export the current GTM container version
  - remove the GA4 configuration tag for `G-N4EQNK0MMB`
  - remove the Conversion Linker if GTM is no longer serving Google Ads tags
- Google tag account cleanup:
  - investigate and remove the rogue `123LegalDoc` Google tag path for `G-3VR0TDX4ZK` / `GT-M6XFPGSK` if confirmed unused
