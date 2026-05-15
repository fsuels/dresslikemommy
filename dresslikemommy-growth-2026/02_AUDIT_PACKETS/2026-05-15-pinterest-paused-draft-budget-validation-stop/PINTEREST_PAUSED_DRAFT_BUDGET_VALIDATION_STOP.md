# Pinterest Paused Draft Budget Validation Stop

Generated: 2026-05-15 05:22 EDT

Mode: current-session approved Pinterest UI attempt, stopped before out-of-scope budget requirement.

Advertiser: `549756244483`

Approval phrase received in current session:

`I approve creating Pinterest paused draft objects for advertiser 549756244483 using the 333-row refreshed scope, with no launch, no enablement, no spend, no budget/bid activation, no catalog/source/tag/CAPI/feed changes, and stop if Pinterest requires any out-of-scope write.`

## Before-State Readback

- Existing authenticated Pinterest Ads Manager tab was used, not a fresh public unauthenticated tab.
- Account/domain readback: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- Reporting dashboard readback before create flow: `0 campaigns`, `0 currently being served`, `$0.00` spend, `0` impressions.
- Existing draft readback from the prior pass: no saved campaign drafts.
- Scope source: refreshed clean `333` variants from `pinterest_paused_draft_refreshed_clean_scope.csv`; the `9` held supplier-leaking variants remain excluded.

## UI Attempt

- Opened Create > Create campaign.
- Selected manual campaign flow after Pinterest initially defaulted to Performance+.
- Selected `Catalog sales`.
- Set campaign name to `DLM_PIN_US_CATALOG_333_PAUSED_20260515`.
- Set campaign status to `Paused`.
- Attempted to keep budget inactive/blank under the current approval boundary.
- Opened `Draft actions`, which exposed `Save as a new draft` and `Load existing draft`.

## Stop Evidence

Pinterest blocked the draft save path with validation errors before any object could be saved:

- `Enter a valid currency value to continue.`
- `Daily budgets must be $1.00 or more.`

Stopped immediately because the current approval explicitly allowed no budget/bid activation and required stopping if Pinterest required an out-of-scope write.

## After-State / Write Boundary

- No `Save as a new draft` click occurred after the validation errors.
- No `Continue`, `Review`, `Publish`, `Launch`, `Enable`, or status-activation action occurred.
- No campaign, ad group, ad, product group, audience, catalog, source, tag, CAPI, feed, budget, bid, launch, spend, or serving object was saved or modified.
- The UI was left in unsaved local builder state with validation errors visible.

## Decision

Status: `UI_ATTEMPT_STOPPED_BUDGET_REQUIRED_NO_SAVED_DRAFT`

Do not retry the no-budget UI save path; Pinterest requires a valid daily budget of at least `$1.00` before saving the paused catalog draft.

## Smallest Next Approval Packet

If the owner wants the paused draft created through this Pinterest UI path, the next approval must explicitly allow entering the minimum budget value only to satisfy paused-draft validation while preserving no launch and no spend:

`I approve entering a $1.00 daily budget only to satisfy Pinterest paused-draft validation for advertiser 549756244483, while keeping the campaign paused/unpublished with no launch, no enablement, no spend, no bid activation, no catalog/source/tag/CAPI/feed/audience changes, and stop if Pinterest requires any additional out-of-scope write.`

Alternative safe path: find a Pinterest API/import/draft route that can save a paused draft shell without a budget value, then read back before any launch decision.
