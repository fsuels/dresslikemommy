# PMax Shopping Replacement Activation Gate

Gate result today: `BLOCKED_FOR_LIVE_ACTIVATION`.

This file defines the checks required before a replacement PMax Shopping campaign can be activated. It does not approve activation.

## Pre-Build Checks

- `ops/AGENT_COORDINATION.md` checked and a narrow PMax write claim is active.
- Existing bad campaign `PMax: Shopping ads (United States)` remains paused.
- Owner explicitly approves either leaving the bad campaign paused or renaming/archiving it as do-not-use.
- Owner explicitly approves creating a paused replacement shell.

## Merchant And Product Checks

- Merchant Center account reads `124884876 - Dresslikemommy`.
- Supplier-domain gate returns `0` rows for `1688.com`, `detail.1688.com`, `alibaba.com`, and `aliexpress.com`.
- Product scope readback confirms only `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready`.
- Exact product count and variant/item count are captured after the replacement shell is built.
- Product scope is non-overlapping with active Standard Shopping, or owner explicitly approves overlap after the Standard Shopping 48-hour review.
- Catch-all/unknown product inclusion is excluded or impossible under the selected product filter.

## Campaign Controls

- Campaign status remains paused before final gate.
- Budget reads the owner-approved value.
- Location is United States with presence-only where exposed.
- Language is English.
- Final URL expansion is off or URL allowlist is captured.
- Brand traffic posture is documented so PMax does not replace Brand Search accidentally.
- URL suffix/tracking is present or intentionally documented.

## Measurement Checks

- Purchase conversion action readback confirms a primary value-tracked purchase action.
- No conversion-goal change is made unless explicitly approved.
- Enhanced conversion / transaction ID / value evidence remains available from the paid measurement packet.

## Creative And Audience Checks

- Asset groups use Dress Like Mommy assets only.
- No unsupported claims such as largest selection, top quality, free delivery, 100K+ customers, ratings, or unverified promotions.
- Audience signals are present and relevant.
- Search themes are present where useful.
- Ad/asset strength is not `Poor`.

## Activation Approval

Activation requires a fresh exact owner phrase after the gate packet is complete. Suggested phrase:

`APPROVE ENABLE DLM_US_PMAX_PAID_READY_REPLACEMENT_DRAFT AT [BUDGET]/DAY NOW; KEEP STANDARD SHOPPING DECISION AS DOCUMENTED; DO NOT CHANGE CONVERSION GOALS`

## Rollback Triggers

- Spend appears outside the approved product cohort.
- Supplier/source URL text appears in any paid surface.
- Non-US traffic appears despite location controls.
- Final URL expansion sends traffic outside approved URLs.
- Brand terms are consumed contrary to the documented brand posture.
- Purchase value/currency/transaction ID tracking fails.
- Cost reaches the owner-approved cap without qualified traffic or useful product/search insight.

