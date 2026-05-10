# Pinterest Paused US Draft Structure

Generated: 2026-05-09

Worker: Worker D, local-only Pinterest structure lane.

Mode: local artifact generation only. No Pinterest account, campaign, draft, product group, tag, CAPI, audience, catalog source, budget, bid, status, or spend write was made.

## Verdict

`LOCAL_TEMPLATES_READY__OWNER_APPROVAL_REQUIRED_FOR_ANY_PINTEREST_WRITE__LIVE_SPEND_BLOCKED_BY_EVENT_QUALITY_FAIR`

The proven clean Pinterest US scope can be converted into paused-draft structure templates, but not into live account objects in this lane. The templates in this folder are operator templates, not upload files and not evidence of any Pinterest write.

## Evidence Used

Primary source packet:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`
- Clean scope CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv`
- Exclusions CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv`
- Summary JSON: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_scope_summary.json`

Latest gate refreshes used:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/pinterest-gate/PINTEREST_PAUSED_US_DRAFT_EVENT_QUALITY_GATE_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/merchant-pinterest-beach-gates/MERCHANT_PINTEREST_BEACH_APPROVAL_GATES.md`

Stored Pinterest facts:

- Advertiser: `549756244483`
- Account/domain: `Dress Like Mommy | Matching Family Outfits` / `dresslikemommy.com`
- Catalog: `Catalog_Retail`
- Catalog ID: `3041764155561548387`
- EN Shopify source/feed profile: `3041760867124595727`
- Clean scope: `342` EN-US rows with Pinterest availability diagnostic `IN_STOCK`
- Clean scope split: `210` Mommy & Me, `103` Family Matching, `29` Pajamas
- Explicit exclusions: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`
- Prior campaign baseline: `0` campaigns, `0` currently serving, `$0.00` spend
- Official Pinterest app pixel/CAPI path: Always on / share all events, with fresh stored Tag and CAPI activity
- Event Quality: `Fair`; Verified Merchant Program `PASS`; Automatic Enhanced Match `PASS`; Enhanced Match `ERROR`

## Draft Architecture

Recommended paused-only account shape after exact owner approval:

| Layer | Draft object | Purpose | Status |
|---|---|---|---|
| Campaign | `DLM_PIN_US_CATALOG_342_PAUSED_20260509` | US catalog shopping shell using the clean EN-US Shopify source | Paused only |
| Campaign | `DLM_PIN_US_RETARGETING_342_PAUSED_20260509` | US catalog retargeting shell, only if existing platform-native retargeting can be selected without creating/changing audiences | Paused only |
| Product groups | Three clean groups by `custom_label_2` | Keep product proof and reporting aligned: Mommy & Me, Family Matching, Pajamas | Paused only |
| Ads | Claim-safe copy variants by group | Preserve a ready creative shell without inventory, warehouse, guaranteed-stock, or unsupported discount claims | Paused only |

Important setup constraints:

- Use only catalog `3041764155561548387` and EN Shopify source/feed profile `3041760867124595727`.
- Do not use the failed sitemap source `3041760916127467912`.
- Do not use localized Pinterest catalog sources.
- Keep all campaign, ad group, ad, and product group statuses paused.
- Do not activate budget or bids. If the UI requires budget or bid fields even for paused drafts, stop and ask the parent for fresh exact approval naming those fields.
- Do not create or modify audiences. For retargeting, reuse only an existing eligible platform-native retargeting selector if the UI clearly supports it without audience creation/change; otherwise stop.
- Live spend remains blocked while Event Quality is `Fair` unless the owner gives a separate explicit spend-risk approval.

## Local Templates

Files created in this lane:

- `pinterest_scope_manifest.json`: machine-readable summary of source evidence and guardrails.
- `pinterest_product_group_template.csv`: local product-group definitions and filters.
- `pinterest_campaign_adgroup_template.csv`: local campaign/ad-group object template.
- `pinterest_promoted_pin_copy_template.csv`: claim-safe copy options by product group.
- `PINTEREST_DRAFT_QA_CHECKLIST.md`: approval wording, pre-readbacks, post-readbacks, and stop conditions.

The CSV files are review-only operator templates. They are not Pinterest bulk upload files and should not be uploaded blindly.

## Exact Approval Gate

No Pinterest write is authorized unless the owner gives this exact paused-draft approval:

```text
APPROVE PAUSED PINTEREST US CATALOG/RETARGETING DRAFT BUILD ONLY: USE THE 2026-05-08 CLEAN 342-ROW EN-US IN-STOCK SCOPE AND EXCLUDE THE 4 UNRESOLVED VARIANTS; KEEP ALL CAMPAIGNS, AD GROUPS, ADS, AND PRODUCT GROUPS PAUSED; NO LIVE SPEND; NO BUDGET OR BID ACTIVATION; NO CATALOG SOURCE, TAG, CAPI, AUDIENCE, SHOPIFY PRODUCT, MERCHANT, GOOGLE ADS, OR FEED CHANGES; READ BACK BEFORE AND AFTER.
```

Separate optional Event Quality repair approval, if the owner chooses tracking repair instead of paused drafts:

```text
APPROVE NARROW PINTEREST EVENT QUALITY REPAIR ONLY: INVESTIGATE OFFICIAL SHOPIFY/PINTEREST APP AND CUSTOMER EVENTS CONFIGURATION FOR PRODUCT ID, EMAIL, AND CLICK ID GAPS; NO CAMPAIGN, DRAFT, PRODUCT GROUP, CATALOG SOURCE, AUDIENCE, BUDGET, BID, STATUS, OR SPEND CHANGES; NO DUPLICATE THEME TAG; NO CUSTOM CAPI DEPLOYMENT OR CUSTOMER-DATA CHANGE WITHOUT A SEPARATE READBACK AND APPROVAL; READ BACK BEFORE AND AFTER.
```

## Live-Spend Position

This lane does not make Pinterest live-spend-ready. Event Quality remains `Fair`, and that remains a live-spend gate. The templates only reduce setup friction after an owner-approved paused-draft build.

## Worker Boundary

This worker changed only files inside:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/`

Parent/orchestrator should update `ops/PROBLEM_TRACKER.md`, `ops/AGENT_WORKLOG.md`, and coordination files if integrating this lane into the broader sprint.
