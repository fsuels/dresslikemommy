# Pinterest US Paused Draft Field Checklist

Generated: 2026-05-12

Worker: Worker B, local-only Pinterest paused US draft lane.

Mode: local evidence/checklist only. No Pinterest, catalog, campaign, ad group, ad, product group, audience, tag, CAPI, budget, bid, status, spend, Shopify, Merchant, Google Ads, feed, credential, browser, or external-system write was made.

## Current Unblock

The paused US catalog/retargeting draft is already owner-approved in the parent lane, but it remains blocked by authenticated Pinterest Ads Manager access/tooling.

Exact unblock action:

`Authenticate Pinterest Ads Manager for advertiser 549756244483 in the controllable Chrome/CDP session, or fix macOS automation permission for Computer Use; then rerun the non-committal create-flow probe and build only paused US draft objects from the 342-row scope with the 4 exclusions.`

Do not retry this in an unauthenticated public Pinterest Ads page. Do not ask the operator to solve this by changing credentials, billing, catalog source, tag, CAPI, audience, Shopify, Merchant, Google Ads, or feed settings.

## Local Evidence Validated

Primary clean scope:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`
- Rows: `342`
- Unique `shopify_variant_id`: `342`
- SHA256: `ae0c1721cc40e1ca0fbb51f3a15e1fa1bc49095f6226c6f73ef908f4b7a7ab83`

Explicit exclusions:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`
- Rows: `4`
- Excluded Shopify variant IDs: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`
- Overlap with clean scope: `0`
- SHA256: `d3fb918a30a61edb2e9aa618f7bd0582f46d7fc0eb3885619205ab64914de14a`

Clean scope split by `custom_label_2`:

| Product group | Rows |
|---|---:|
| `mommy_me` | `210` |
| `family_matching` | `103` |
| `pajamas` | `29` |

Existing local templates:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/pinterest_scope_manifest.json`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/pinterest_product_group_template.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/pinterest_campaign_adgroup_template.csv`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/pinterest_promoted_pin_copy_template.csv`

Template counts validated:

| Template | Rows | Status |
|---|---:|---|
| `pinterest_product_group_template.csv` | `3` | `REVIEW_ONLY_NOT_UPLOAD` |
| `pinterest_campaign_adgroup_template.csv` | `6` | `REVIEW_ONLY_NOT_UPLOAD` |
| `pinterest_promoted_pin_copy_template.csv` | `6` | `REVIEW_ONLY_NOT_UPLOAD` |

## Required Before-Write Readbacks

Run these readbacks after authenticated Ads Manager access is restored and before clicking any create/save/publish/launch button:

1. Confirm advertiser/account:
   - Advertiser ID: `549756244483`
   - Account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
   - Stop if any other advertiser, business, or domain is selected.

2. Confirm campaign baseline:
   - Campaign count and serving count.
   - Current spend.
   - Any active/promoted campaigns, ad groups, ads, or product groups.
   - Expected preserved baseline from prior evidence: `0` campaigns, `0` currently serving, `$0.00` spend.
   - Stop if there are unexpected live/serving objects and parent has not reconciled them.

3. Confirm catalog/source:
   - Catalog name: `Catalog_Retail`
   - Catalog ID: `3041764155561548387`
   - Allowed EN Shopify source/feed profile: `3041760867124595727`
   - Blocked failed sitemap source: `3041760916127467912`
   - Locale/source must be `en-US`.
   - Stop if the UI selects the failed sitemap source, localized sources, non-US sources, or asks to change catalog/source/feed settings.

4. Confirm local scope still matches:
   - Clean rows: `342`
   - Unique variants: `342`
   - Exclusions: exactly the 4 IDs listed above.
   - Product groups: `210` Mommy & Me, `103` Family Matching, `29` Pajamas.
   - Stop if any count drifts, if any excluded variant appears in the clean scope, or if the clean scope cannot be mapped to the selected source.

5. Confirm Event Quality without trying to repair it:
   - Record overall WEB status, Pinterest Tag status, Conversions API status, last updated date, latest Tag/CAPI timestamps, Verified Merchant Program, Automatic Enhanced Match, Enhanced Match, and top action items.
   - Prior state was `Fair`; owner currently says assume tags are correct for launch-prep.
   - Stop if the UI requests tag/CAPI/customer-data/config changes.

## Field-Level Build Checklist

Use this only after the authenticated account readbacks above pass.

### Campaign 1: Catalog Shopping Shell

| Field | Value / rule |
|---|---|
| Campaign name | `DLM_PIN_US_CATALOG_342_PAUSED_20260512` |
| Objective / campaign type | Catalog sales, Shopping, or closest Pinterest catalog-shopping equivalent |
| Advertiser | `549756244483` |
| Country | United States / `US` |
| Language / source | `en-US` |
| Catalog | `Catalog_Retail` / `3041764155561548387` |
| Feed profile/source | `3041760867124595727` only |
| Status | Paused/draft only |
| Budget | Do not activate. Stop if a budget is required without fresh exact approval naming the budget field. |
| Bid | Do not activate. Stop if a bid is required without fresh exact approval naming the bid field. |
| Audience | Prospecting/catalog shopping only if no new or changed audience is required. |
| URL/landing behavior | Use item URLs from the EN-US Shopify catalog source. |

Ad groups/product groups under Campaign 1:

| Ad group name | Product group object/filter | Rows | Status |
|---|---|---:|---|
| `DLM_PIN_US_CATALOG_MOMMY_ME_PAUSED_20260512` | `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`, `custom_label_2=mommy_me`, `locale=en-US`, availability `IN_STOCK`, excluding the 4 unresolved variants | `210` | Paused/draft only |
| `DLM_PIN_US_CATALOG_FAMILY_MATCHING_PAUSED_20260512` | `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`, `custom_label_2=family_matching`, `locale=en-US`, availability `IN_STOCK`, excluding the 4 unresolved variants | `103` | Paused/draft only |
| `DLM_PIN_US_CATALOG_PAJAMAS_PAUSED_20260512` | `custom_label_0=paid_eligible`, `custom_label_4=us_test_ready`, `custom_label_2=pajamas`, `locale=en-US`, availability `IN_STOCK`, excluding the 4 unresolved variants | `29` | Paused/draft only |

### Campaign 2: Retargeting Shell

Create this only if Pinterest offers an existing platform-native retargeting selector without creating or modifying an audience.

| Field | Value / rule |
|---|---|
| Campaign name | `DLM_PIN_US_RETARGETING_342_PAUSED_20260512` |
| Objective / campaign type | Catalog sales, Shopping retargeting, or closest Pinterest catalog-retargeting equivalent |
| Advertiser | `549756244483` |
| Country | United States / `US` |
| Language / source | `en-US` |
| Catalog | `Catalog_Retail` / `3041764155561548387` |
| Feed profile/source | `3041760867124595727` only |
| Status | Paused/draft only |
| Budget | Do not activate. Stop if a budget is required without fresh exact approval naming the budget field. |
| Bid | Do not activate. Stop if a bid is required without fresh exact approval naming the bid field. |
| Audience | Reuse only an existing platform-native retargeting selector; do not create or change audiences. |

Ad groups/product groups under Campaign 2 mirror Campaign 1:

| Ad group name | Product group object/filter | Rows | Status |
|---|---|---:|---|
| `DLM_PIN_US_RETARGETING_MOMMY_ME_PAUSED_20260512` | Same `mommy_me` clean-scope filter and exclusions | `210` | Paused/draft only |
| `DLM_PIN_US_RETARGETING_FAMILY_MATCHING_PAUSED_20260512` | Same `family_matching` clean-scope filter and exclusions | `103` | Paused/draft only |
| `DLM_PIN_US_RETARGETING_PAJAMAS_PAUSED_20260512` | Same `pajamas` clean-scope filter and exclusions | `29` | Paused/draft only |

## Creative Copy Fields

Use only claim-safe copy from `pinterest_promoted_pin_copy_template.csv`. Acceptable examples:

| Product group | Headline | Description | CTA |
|---|---|---|---|
| Mommy & Me | `Mommy & Me Matching Outfits` | `Coordinated dresses and looks for moms and kids, ready for photos, birthdays, trips, and everyday moments.` | `Shop now` |
| Family Matching | `Family Matching Outfits` | `Find coordinated family outfits for parents and kids across casual looks, vacations, photos, and special days.` | `Shop now` |
| Pajamas | `Matching Family Pajamas` | `Explore coordinated pajama looks for family photos, holidays, lounging, and cozy at-home moments.` | `Shop now` |

Copy stop rules:

- No warehouse, local inventory, owned inventory, in-hand stock, or guaranteed availability claims.
- No delivery-speed, free-shipping, discount, review-count, bestseller, urgency, or limited-time claims unless separately verified and approved.
- Do not imply a physical retail location.

## Required After-Write Readbacks

If an authenticated operator creates the paused draft objects under approval, capture after-readbacks before closing the lane:

1. Campaign/ad group/ad/product group status:
   - Every created campaign reads paused/draft.
   - Every created ad group reads paused/draft.
   - Every ad/ad creative reads paused/draft.
   - Every product group reads paused/draft.
   - Currently serving remains `0`.
   - Spend remains `$0.00`.

2. Scope:
   - Product group scope totals still map to `342` clean rows.
   - Splits still read `210` / `103` / `29`.
   - The 4 excluded variants do not appear in any included product group.

3. Catalog/source:
   - Catalog remains `3041764155561548387`.
   - Source/feed profile remains `3041760867124595727`.
   - Failed sitemap source `3041760916127467912` is not used.
   - No localized/non-US source is used.

4. Guardrails:
   - No live spend.
   - No enabled/serving object.
   - No budget/bid activation.
   - No catalog source, tag, CAPI, audience, Shopify product, Merchant, Google Ads, feed, billing, or credential change.
   - Event Quality status recorded, but not repaired in this lane.

5. Evidence to save:
   - Screenshots or exported text for campaign list/baseline before and after.
   - Screenshots or exported text for each created campaign/ad group/product group detail page.
   - Catalog/source readback screenshot/text.
   - Event Quality readback screenshot/text.
   - A summary JSON or markdown note with URL, timestamp, advertiser ID, object names, statuses, and exact stop/continue decision.

## Stop Conditions

Stop immediately and report to parent/orchestrator if any of these occur:

- Pinterest Ads Manager is not authenticated for advertiser `549756244483`.
- A login, CAPTCHA, billing, payment, permission, account-switcher, unsaved-changes, policy-warning, or publish/launch modal appears.
- The UI does not offer a paused/draft state before save.
- The UI asks to activate, launch, serve, publish, promote, enable, or spend.
- The UI requires budget or bid fields and the current approval does not explicitly name those fields.
- The UI requires creating or editing an audience.
- The UI asks for tag, CAPI, customer-data, pixel, source, feed, catalog, Shopify, Merchant, or Google Ads changes.
- The catalog/source is not `3041764155561548387` / `3041760867124595727`.
- The failed sitemap source `3041760916127467912` or any localized/non-US source is selected.
- Clean scope count, exclusions, or product-group splits do not match local validation.
- Any object would be enabled or serving after creation.

## Operator Handoff

When the unblock is complete, the operator should start with the before-readbacks, then create only the paused objects above, and finally capture after-readbacks. Live Pinterest spend remains a separate approval gate after the paused draft exists and reads back clean.
