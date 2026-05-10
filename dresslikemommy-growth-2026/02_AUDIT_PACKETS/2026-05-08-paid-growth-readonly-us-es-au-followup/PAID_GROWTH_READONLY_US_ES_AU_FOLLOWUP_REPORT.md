# Paid Growth Read-Only US/es + AU Follow-Up Report

Generated: 2026-05-08 03:31 EDT

Owner request: run read-only Merchant US/es source/detail readback for likely source `10627981690`, then AU isolated-browser checkout-to-shipping QA. Only after that, use separate exact approval gates for paused Google Search or paused Pinterest drafts.

## Results

| Workstream | Result | Evidence |
| --- | --- | --- |
| Merchant US/es age_group | Read-only product-detail RPC confirms the blocker. Two affected `US` / `es` items on source `10627981690` still show `Missing age group` and lack effective `n:age_group`; one control sample on the same source has `n:age_group` and no Missing age group. Direct source-detail UI did not expose a clean source settings table. | `lanes/merchant-us-es-readonly/MERCHANT_US_ES_SOURCE_DETAIL_READBACK.md` |
| AU checkout | Passed after isolated-browser retry. Product/cart/rates/checkout reached AU/AUD shipping methods without `429` or verification page. Standard: `0.00 AUD`; Express API: `18.24 AUD`; checkout UI displayed Standard/Express/AUD and `en-AU`. No payment data entered, no Pay Now click, no order confirmation. | `lanes/au-checkout-readonly/AU_ISOLATED_CHECKOUT_TO_SHIPPING.md` |

## Problem Tracker

- `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`: moved to `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`. The next safe action is exact owner approval for a narrow US/es source `10627981690` age_group repair path, with pre/post readbacks.
- `PROB-2026-05-08-AU-CHECKOUT-429`: moved to `SOLVED_READBACK_PASSED`. AU is no longer blocked by the prior `429` for paused English-first infrastructure, but live spend still requires all paid-growth gates.
- `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`: unchanged as `OWNER_APPROVAL_REQUIRED`.

## Approval Gates

Merchant US/es live repair approval gate:

`APPROVE MERCHANT US/ES AGE_GROUP REPAIR REVIEW FOR SOURCE 10627981690: READ BACK THE US/ES PRODUCT DETAIL AND SOURCE STATE FIRST; THEN USE ONLY THE NARROWEST SAFE OFFICIAL REPAIR PATH FOR US FEED LABEL / ES LANGUAGE / UNITED STATES MISSING AGE_GROUP; NO GOOGLE ADS, PINTEREST, SHOPIFY PRODUCT-DATA, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, BUDGET, BID, STATUS, PMAX, STANDARD SHOPPING, OR LIVE-SPEND CHANGES; NO BROAD SOURCE REFRESH, MERCHANT UPLOAD, SOURCE EDIT, OR SHOPIFY DATA EDIT WITHOUT A PREVIEW, EXACT ROW SCOPE, AND POST-READBACK.`

Paused non-US Google Search build approval gate:

`APPROVE PAUSED NON-US GOOGLE SEARCH TEST BUILD ONLY: CREATE PAUSED GOOGLE SEARCH TEST CAMPAIGNS FOR UK, CANADA, AUSTRALIA, SWITZERLAND, DENMARK, GERMANY, NETHERLANDS, SWEDEN, FRANCE, BELGIUM, SPAIN, ITALY, POLAND, CZECHIA, ROMANIA, PORTUGAL, AND GREECE; DO NOT CREATE OR EDIT US CAMPAIGN 23827590655; USE TIGHT EXACT/PHRASE KEYWORDS, PRESENCE-ONLY LOCATION TARGETING, CPC CAPS AT OR BELOW $0.20, AND KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND KEYWORDS PAUSED; NO LIVE SPEND; NO PMAX, STANDARD SHOPPING, PRODUCT-SCOPE, FEED-LABEL, PRODUCT-GROUP, CONVERSION-GOAL, MERCHANT, SHOPIFY PRODUCT-DATA, PINTEREST, THEME, BUDGET-INCREASE, BID-INCREASE, OR ENABLEMENT CHANGES; PREVIEW AND READ BACK BEFORE AND AFTER.`

Paused US Pinterest draft approval gate:

`APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.`

## Guardrails

No external account writes were made. No live spend, campaign enablement, campaign/budget/bid/status changes, PMax enable, Standard Shopping changes, product-scope/feed-label/product-group changes, conversion-goal changes, Merchant uploads/source syncs/source edits, Shopify live product-data changes, Pinterest draft/campaign/tag/CAPI/product-group/audience/budget/bid writes, checkout payment/order, theme publish, or credential changes.
