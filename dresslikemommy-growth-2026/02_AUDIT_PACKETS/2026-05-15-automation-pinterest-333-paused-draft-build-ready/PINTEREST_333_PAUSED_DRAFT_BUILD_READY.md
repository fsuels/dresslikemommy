# Pinterest 333 Paused Draft Build-Ready Packet

Generated: 2026-05-15 05:12 EDT
Mode: repo-local build packet only. No Pinterest, Shopify, Merchant, Google Ads, GA4/GTM, tag, CAPI, catalog, feed, budget, bid, status, launch, or spend write occurred.

## Decision

The old Pinterest `342`-row packet is superseded for any new paused draft prefill. Use the refreshed `333`-variant public-clean scope:

- Scope CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-paused-draft-scope-refresh/pinterest_paused_draft_refreshed_clean_scope.csv`
- Public-source exclusions: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-paused-draft-scope-refresh/pinterest_paused_draft_public_source_exclusions.csv`
- Scope refresh report: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-15-automation-pinterest-paused-draft-scope-refresh/PINTEREST_PAUSED_DRAFT_SCOPE_REFRESH.md`

## Draft Objects To Create If Approved

| Object | Exact draft name | Scope | Status |
|---|---|---:|---|
| Campaign shell | `DLM_PIN_US_CATALOG_333_PAUSED_20260515` | 333 variants | Draft/paused only |
| Product group / ad group | `DLM_PIN_US_CATALOG_MOMMY_ME_201_PAUSED_20260515` | 201 variants / 26 products | Draft/paused only |
| Product group / ad group | `DLM_PIN_US_CATALOG_FAMILY_MATCHING_103_PAUSED_20260515` | 103 variants / 7 products | Draft/paused only |
| Product group / ad group | `DLM_PIN_US_CATALOG_PAJAMAS_29_PAUSED_20260515` | 29 variants / 1 product | Draft/paused only |
| Optional remarketing shell | `DLM_PIN_US_RETARGETING_333_PAUSED_20260515` | Only if Pinterest offers an existing safe audience selector without creating/editing audiences | Draft/paused only |

## Top Product Proof For Prefill

| Product group | Variants | Products | Highest-coverage products |
|---|---:|---:|---|
| Mommy & Me | 201 | 26 | Smocked Sundresses `32`, Summer Dresses `22`, Sunflower Maxi Dresses `11`, Star Knit Sweater Dress `10` |
| Family Matching | 103 | 7 | Colorful Heart Brushstroke T-Shirt Set `42`, Rainbow Outfits `16`, Green/White Floral Set `13`, Striped Fleece Hoodies `10` |
| Pajamas | 29 | 1 | Cute Matching Cartoon Pajama Set `29` |

## Required Before-State Readback

Before any Pinterest UI object creation, read back and save/summarize:

- Advertiser ID remains `549756244483`.
- Account/domain remains `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`.
- Current reporting still shows no active serving campaign or spend unless a new human action changed it.
- Existing draft view still has no conflicting saved draft, or the existing draft is explicitly selected for update by owner approval.
- No billing, policy, CAPTCHA, account switcher, permission, publish/launch, tag, CAPI, catalog source, feed source, audience creation/edit, budget activation, or bid activation prompt appears.

## Current-Session Approval Phrase Required

Because the current session says no external writes unless explicitly approved, do not create these Pinterest draft objects until the owner gives this exact approval:

`I approve creating Pinterest paused draft objects for advertiser 549756244483 using the 333-row refreshed scope, with no launch, no enablement, no spend, no budget/bid activation, no catalog/source/tag/CAPI/feed changes, and stop if Pinterest requires any out-of-scope write.`

## Stop Conditions

Stop and report before saving/submitting if Pinterest requires or reveals any of these:

- Launch, publish, enablement, campaign serving, budget activation, or bid activation.
- New catalog source, feed source, tag, CAPI, domain verification, or audience creation/edit.
- Billing, policy, CAPTCHA, account switcher, permission, or destructive prompt.
- Any attempt to include the `9` held public-source exclusion variants before repair and clean readback.

## After-State Readback If Approved Later

If the exact approval is given and the draft can be created without stop conditions, record:

- Created draft object names and IDs.
- Draft/paused status proof.
- Product-group counts.
- Spend remains `$0.00`.
- No currently serving campaign was created.
- No catalog/feed/source/tag/CAPI or audience mutation occurred.
