# Pinterest Draft QA Checklist

Generated: 2026-05-09

Mode: local checklist only. This file does not authorize any Pinterest write.

## Approval Gate

Paused draft approval required before any Pinterest account write:

```text
APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.
```

Separate Event Quality repair approval, only if that path is chosen:

```text
APPROVE NARROW PINTEREST EVENT QUALITY REPAIR ONLY: INVESTIGATE OFFICIAL SHOPIFY/PINTEREST APP AND CUSTOMER EVENTS CONFIGURATION FOR PRODUCT ID, EMAIL, AND CLICK ID GAPS; NO CAMPAIGN, DRAFT, PRODUCT GROUP, CATALOG SOURCE, AUDIENCE, BUDGET, BID, STATUS, OR SPEND CHANGES; NO DUPLICATE THEME TAG; NO CUSTOM CAPI DEPLOYMENT OR CUSTOMER-DATA CHANGE WITHOUT A SEPARATE READBACK AND APPROVAL; READ BACK BEFORE AND AFTER.
```

## Pre-Write Readbacks

- Confirm one parent-owned Pinterest writer claim exists in coordination before opening the live Pinterest account surface.
- Read back advertiser `549756244483`: campaign count, currently serving count, spend, active/promoted objects, login/CAPTCHA/billing/unsaved prompts.
- Read back Event Quality: overall WEB status, Pinterest Tag status, Conversions API status, updated date, latest Tag/CAPI timestamps, Verified Merchant Program, Automatic Enhanced Match, Enhanced Match, and top action items.
- Revalidate the local clean scope file: `342` clean rows, `342` unique variant IDs, all `en-US`, all platform availability diagnostic `IN_STOCK`, all `FOUND_EN_US_IN_STOCK`.
- Revalidate exclusions: exactly `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`, with `0` overlap against clean scope.
- Verify product-group splits: `210` Mommy & Me, `103` Family Matching, `29` Pajamas.
- Verify catalog/source selection: `Catalog_Retail`, catalog ID `3041764155561548387`, EN Shopify source/feed profile `3041760867124595727`.
- Confirm the failed sitemap source `3041760916127467912` and localized sources are not selected.
- Confirm no live spend, budget activation, bid activation, or campaign/ad/ad-group/product-group enablement is implied by the UI flow.

## Build Rules If Approval Exists

- Create paused/draft-only objects from `pinterest_campaign_adgroup_template.csv` and `pinterest_product_group_template.csv`.
- Keep all campaigns, ad groups, ads, and product groups paused.
- Use only claim-safe copy from `pinterest_promoted_pin_copy_template.csv`.
- Do not add customer-facing claims about stock, warehouse, local inventory, guaranteed availability, free shipping, delivery speed, discounts, reviews, or bestseller status.
- Do not create or modify audiences. If retargeting requires a new or changed audience, stop.
- Do not change tag, CAPI, catalog source, feed, Shopify products, Merchant, Google Ads, budget, bid, status, or live spend.
- If the Pinterest UI requires a budget or bid field even for paused drafts, stop and ask parent for exact action-time approval naming that field.

## Post-Write Readbacks If Approval Exists

- Every created campaign, ad group, ad, and product group reads paused/draft only.
- Currently serving remains `0`.
- Spend remains `$0.00`.
- Product scope reads as the clean `342` rows, split `210` / `103` / `29`, with the four unresolved variants excluded.
- Catalog/source remains `3041764155561548387` / `3041760867124595727`.
- Event Quality is recorded again; live spend remains blocked if status is still `Fair`.
- Confirm no tag/CAPI/audience/catalog/feed/source/Shopify/Merchant/Google Ads/budget/bid/status change occurred outside the approval text.

## Stop Conditions

- Owner approval is absent or does not exactly authorize the paused Pinterest US draft.
- Approval bundles live spend, campaign enablement, budget activation, bid activation, Event Quality repair, Shopify changes, Merchant changes, Google Ads changes, or feed changes.
- Fresh clean scope no longer reads `342` rows with the same four exclusions.
- The UI selects or asks to use a failed sitemap source, localized source, or non-US source.
- The UI requires a new/changed audience for retargeting.
- The UI asks to publish, launch, promote, enable, or serve.
- The UI requires budget/bid/status changes not named in a fresh exact approval.
- Any prompt asks for tag, CAPI, customer data, pixel, catalog source, Shopify product, Merchant, Google Ads, or feed changes.

## What This Checklist Does Not Solve

- Event Quality remains `Fair`.
- Live spend remains blocked unless the owner separately accepts the measurement risk.
- This does not create Pinterest drafts.
- This does not upload or change any catalog product group.
- This does not repair Enhanced Match, AddPaymentInfo product ID, AddToCart hashed email, or Checkout click ID gaps.
