# Pinterest 342-Scope Draft Gate

Date: 2026-05-08
Mode: local/read-only; no Pinterest write

Problem: `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`

## Result

The older Pinterest draft solution with `337` resolved rows and `9` excluded rows is superseded by the later clean scope:

- Clean scope: `342` EN-US in-stock rows.
- Product-group split:
  - `210` Mommy & Me.
  - `103` Family Matching.
  - `29` Pajamas.
- Exclude exactly `4` unresolved variants:
  - `41878208249953`.
  - `41878208479329`.
  - `41878208577633`.
  - `41878208610401`.

The old local solution file now has a supersession notice. Future paused-draft work should use:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`

and:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`

## Event Quality Handling

Event Quality remains `Fair`, while Tag and CAPI are alive. This should not block owner-approved paused draft creation, but it should continue to block live spend/enablement unless the owner separately accepts the risk or approves a narrow tracking repair.

Do not add duplicate theme-level Pinterest tag, custom CAPI, catalog source, or audience changes without exact owner approval.

## Exact Approval Gate

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

## Residual Risk

Paused drafts are still live account writes and require exact owner approval. Live Pinterest spend remains separately gated by Event Quality, catalog/source readback, targeting proof, economics, and owner approval.

