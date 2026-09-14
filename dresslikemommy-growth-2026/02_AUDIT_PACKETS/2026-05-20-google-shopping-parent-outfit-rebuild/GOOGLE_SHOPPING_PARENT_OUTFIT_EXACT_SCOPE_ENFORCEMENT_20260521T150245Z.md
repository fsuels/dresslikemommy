# Google Shopping Parent-Outfit Exact-Scope Product-Group Enforcement

UTC timestamp: `20260521T150245Z`

## Mode

- Mode: `validate_only`
- Validate-only passed: `False`
- Executed: `False`

## Scope

- Candidate rows: `4370`
- Held unresolved rows: `141`
- Held out-of-stock rows: `20`

## Operation Plan

- Operation count: `4406`
- Removed subgroup units: `12`
- Created subgroup subdivisions: `12`
- Created exact item units: `4370`
- Created item catchall exclusions: `12`

## Readback

- Validation passed: `False`
- Campaigns: `3`
- Old campaign status: `PAUSED`
- Ad groups: `12`
- Product ads: `12`
- Listing groups: `60`
- Included exact item units: `0`
- Unique included item IDs: `0`
- Item catchall exclusions: `0`
- Included subgroup units remaining: `12`
- Missing candidate IDs: `4370`
- Extra item IDs: `0`
- Held item IDs included: `0`

## Guardrails

- All V2 campaigns, ad groups, and product ads must remain paused.
- The old test campaign must remain paused.
- No activation, budget, bid, conversion, billing, Merchant, Shopify, Google & YouTube, feed/source, broad sync, source reset, or product recreation write is authorized by this script.

## Files

- Before JSON: `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-20-google-shopping-parent-outfit-rebuild/google_ads_shopping_parent_outfit_exact_scope_before_20260521T150245Z.json`
- After JSON: `None`

## Issues

- Missing candidate item units: ['shopify_US_7108953604193_41496508432481', 'shopify_US_7108953604193_41496508465249', 'shopify_US_7108953604193_41496508498017', 'shopify_US_7108953604193_41496508530785', 'shopify_US_7108953604193_41496508563553']
- Included subgroup units remain: 12
