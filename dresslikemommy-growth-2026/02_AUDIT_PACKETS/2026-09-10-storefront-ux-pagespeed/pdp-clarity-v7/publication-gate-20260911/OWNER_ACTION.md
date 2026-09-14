# Publish the verified existing V7 theme

Confidence: H for the current source and exact publication target. **The live UX outcome remains unfinished.**

The required owner action is to open [Shopify Admin themes](https://dresslikemommy-com.myshopify.com/admin/themes) and publish **DLM UX Performance QA 2026-09-10 — theme 137888792673**. Keep the previous MAIN theme **133290917985, dresslikemommy/main**, in the theme library for rollback.

This publishes the already reviewed V7 theme. No new theme or repeated file upload is needed. The separate seven-file V8 local proposal is not part of this release.

## Current source check

Private Shopify Admin readback at **September 11, 2026, 19:30:09 UTC** verified:

- Store **Dress Like Mommy, 15571635**, domain `dresslikemommy-com.myshopify.com`.
- The only published MAIN is **133290917985**, with 525 files.
- The exact target **137888792673** is **UNPUBLISHED**, processing=false, with 527 files. It was last changed at 17:40:34 UTC.
- All 527 candidate hashes and sizes match the uploaded theme; MAIN, candidate and predecessor have no changes since the previous complete readback. Five protected V7 release files remain unchanged.
- The reviewed V7 release has 19 differences from its preserved predecessor and 61 differences from MAIN, including inherited work. Existing V7 test, full-theme and browser receipts retain their original dates; this follow-up changed no code.

## Why owner action is required

The currently available `shopify_graphql_mutation` connector explicitly lists **theme publishing** among blocked operations. It also states:

> Theme file writes (themeFilesCopy, themeFilesUpsert) are allowed on unpublished themes only — writes that target the live/MAIN theme are blocked.

Its supported instruction is to inform the user and have them perform the action in Shopify Admin. The exact tool description is saved in [publication-restriction.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/pdp-clarity-v7/publication-gate-20260911/publication-restriction.json). No publication mutation was attempted or rejected in this follow-up; the restriction was observed before execution. No browser, CLI or alternate API was used to work around it. The owner's request to reach the live destination is understood; the outstanding requirement is execution of this specific Admin action.

## Buyer acceptance after publication

The existing preview repair selected Together Heart variant **46512190292065, Adult / 4XL / Green**, displayed USD 26.99 and added exactly that variant at quantity 1. The test line was removed and cart 0 verified. MAIN previously failed to initialize the custom size/color selection and left Add disabled. The current MAIN source still lacks the selected-variant field supplied by the candidate.

The five Minimalist Heart AU variant links have **not** been individually rendered by this UX task. Corrected source/feed prices do not establish correct landing selection or checkout behavior. After publication, first verify the new MAIN role and complete source privately. Public verification must wait until the actual HTTP 429 access gate is cleared, then test the exact five links in the intended AU/currency context, selected variant, displayed price and cart behavior before Merchant's production AU submission. Merchant owns feed writes.

If the source or target changes before the owner acts, recheck those exact changes. If an accepted release needs rollback, the owner can republish the preserved old MAIN theme; no deletion or file overwrite is required. Published acceptance, fresh desktop/mobile PageSpeed, payment acceptance and conversion impact remain unverified.

Continuation prompt: “Check whether the owner published existing V7 theme 137888792673. Verify exact MAIN identity and source; after actual HTTP 429 clearance, complete the AU variant buyer checks and published PageSpeed tests. Keep V8 separate and preserve Merchant ownership.”
