# Pinterest US Paused Draft Build Spec

Date: `2026-05-12`
Status: `LOCAL_BUILD_SPEC_ONLY_NO_PINTEREST_WRITES`

## Purpose

Turn the already validated Pinterest US paused-draft checklist into a machine-readable build spec for the first authenticated Ads Manager session.

This packet does not create or edit Pinterest campaigns, ad groups, ads, product groups, catalogs, sources, audiences, tags, CAPI, feeds, budgets, bids, or statuses.

## Files

- `pinterest_us_paused_draft_build_spec.json`
- `validate_pinterest_us_paused_draft_spec.py`
- `pinterest_us_paused_draft_build_spec_validation_summary.json`
- `PINTEREST_US_PAUSED_DRAFT_FIELD_CHECKLIST.md`
- `pinterest_us_paused_draft_local_validation_summary.json`

## Local Spec Validation

The local verifier passed:

`python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/validate_pinterest_us_paused_draft_spec.py`

Result:

- Status: `PASS`.
- Checks: `21`.
- Failed checks: `0`.
- Verified the clean scope and exclusions exist.
- Verified clean rows `342`, unique variant IDs `342`, no overlap with the 4 exclusions, and matching source SHA256 values.
- Verified product group counts `210` mommy_me / `103` family_matching / `29` pajamas.
- Verified clean rows use `paid_eligible`, `us_test_ready`, `en-US`, `IN_STOCK`, feed profile `3041760867124595727`, market `US`, and review status `CANDIDATE_ONLY_NOT_LAUNCH_APPROVED`.
- Verified spec object names are unique and every planned campaign/ad group requires `paused_or_draft`.

## Auth Recovery Result

Fresh recovery attempt:

- Chrome DevTools MCP `list_pages` still failed because the profile is already running/locked.
- Chrome DevTools MCP `new_page` with isolated context still failed with the same profile lock.
- Computer Use `get_app_state` for Google Chrome still returned Apple event error `-1743`.

No authenticated Pinterest page was controlled and no Pinterest write occurred.

## Validated Scope

- Advertiser: `549756244483`.
- Catalog: `3041764155561548387`.
- Allowed feed profile/source: `3041760867124595727`.
- Blocked failed sitemap source: `3041760916127467912`.
- Clean scope: `342` unique variants.
- Exclusions: `4` variants.
- Product group split: `210` mommy_me / `103` family_matching / `29` pajamas.

## Draft Object Plan

Campaigns:

- `DLM_PIN_US_CATALOG_342_PAUSED_20260512`
- `DLM_PIN_US_RETARGETING_342_PAUSED_20260512`

Ad groups per campaign:

- `MOMMY_ME`: `210` rows.
- `FAMILY_MATCHING`: `103` rows.
- `PAJAMAS`: `29` rows.

All objects must remain paused or draft. If Pinterest requires budget, bid, enablement, launch, publish, audience creation/edit, catalog/source change, tag/CAPI change, billing, or account permission changes, stop and return to the parent.

## Next Exact Unblock

Authenticate Pinterest Ads Manager for advertiser `549756244483` in a controllable browser/CDP session, or fix macOS automation permission for Computer Use. Then run the before-write readbacks in the JSON spec before creating any paused objects.

Live Pinterest spend remains a separate future approval gate.
