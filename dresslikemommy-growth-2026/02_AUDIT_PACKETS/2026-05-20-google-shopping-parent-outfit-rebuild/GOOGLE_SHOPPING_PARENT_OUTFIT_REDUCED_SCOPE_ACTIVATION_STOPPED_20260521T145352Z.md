# Google Shopping Parent-Outfit Reduced-Scope Activation Stopped

Generated: `20260521T145352Z`

## Approval Received

Owner approved the reduced-scope activation phrase for the passed reduced gate `GOOGLE_SHOPPING_PARENT_OUTFIT_REDUCED_ACTIVATION_REVIEW_GATE_20260521T132011Z.md`, with the explicit requirement to activate only the `4,370` candidate ready-label in-stock rows while keeping the exact `141` unresolved-offer rows and exact `20` out-of-stock rows held out.

## Decision

Activation stopped before any status change.

Reason: `FAIL_CLOSED__CURRENT_V2_LABEL_SUBGROUP_TREE_WOULD_INCLUDE_HELD_ROWS`

## Before-State Readback

- V2 campaigns: `3`
- V2 ad groups: `12`
- V2 product ads: `12`
- V2 campaign status: paused on readback
- Old campaign `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY`: `PAUSED`
- Listing groups: `60`
- Included subgroup units: `12`
- Excluded catchall units: `24`
- Bad catchall units: `0`
- Before-state readback report: `GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_20260521T145352Z.md`

## Leak Preflight

The current live V2 product-group tree is label/subgroup based:

- campaign listing scope uses `custom_label_0=paid_eligible`, parent lane, and `custom_label_4=us_parent_outfit_ready_v20260520`
- ad group listing units include subgroup `custom_label_2`
- catchalls are excluded

That structure is clean for hierarchy and catchalls, but it is not an exact item-ID fence for the reduced `4,370` candidate rows.

Preflight against the exact hold files found:

- Candidate rows: `4,370`
- Exact unresolved-offer hold rows: `141`
- Exact out-of-stock hold rows: `20`
- Held rows already present in the latest ready-label surface: `22`
- Held rows that the current label/subgroup tree would include if active: `22`
- Held in-stock rows that would leak now: `2`
- Held out-of-stock rows that would be inside the active tree and could leak later if inventory changes: `20`

Leak distribution:

- `mommy_and_me / tops_shirts`: `3`
- `family_matching / tops_shirts`: `19`

Sample held rows that would be included by the current tree:

- `shopify_US_7535944368225_44861276684385` - `IN_STOCK` - `mommy_and_me / tops_shirts`
- `shopify_US_7535944368225_44861276782689` - `IN_STOCK` - `mommy_and_me / tops_shirts`
- `shopify_US_7230645239905_41884150530145` - `OUT_OF_STOCK` - `family_matching / tops_shirts`

## Guardrails Preserved

- No campaign, ad group, or product ad was enabled.
- No spend was activated.
- No Merchant feed/source write occurred.
- No Shopify product/publication/inventory/title/price/handle/SEO write occurred.
- No Google & YouTube sync occurred.
- No budget, bid, conversion, billing, campaign product-group, broad sync, source reset, or product recreation write occurred.

## Required Next Step

The next safe action is not simple activation. It is a separate paused exact-scope product-group enforcement step, such as a validate-only and then approved paused product-group rewrite that fences the active tree to the exact `4,370` candidate item IDs or otherwise proves the exact held rows cannot enter delivery.

After that exact-scope structure passes readback, activation can be reconsidered under a fresh owner approval.
