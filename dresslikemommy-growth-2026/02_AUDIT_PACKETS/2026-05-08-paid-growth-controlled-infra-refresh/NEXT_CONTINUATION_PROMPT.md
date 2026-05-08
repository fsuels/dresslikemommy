# Next Continuation Prompt

Continue the Dress Like Mommy paid-growth sprint in `/Users/fsuels/Projects/dresslikemommy`.

Use `ops/prompts/paid-growth-ai-army-continuation-prompt.md` as the canonical operating prompt. Read it first, then read `AGENTS.md`, `ops/GROWTH_NORTH_STAR.md`, `ops/MEMORY_CONTINUITY_PROTOCOL.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, `ops/GOOGLE_ADS_CONTINUITY.md`, and the latest entries in `ops/AGENT_WORKLOG.md`.

Latest anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-08-paid-growth-controlled-infra-refresh`

What is already done and should not be repeated blindly:

- A new local-only controlled infrastructure packet exists at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/`.
- The international Google Search local packet was refreshed in `lanes/ads-intl/`: `17` campaigns, `204` ad groups, `612` exact/phrase keywords, `629` negatives, `204` RSAs, `1666` web-bulk rows, all paused, max CPC `$0.15`, and final URLs now include `country=<ISO>`.
- ES/IT/RO/PT use localized product paths plus `country=<ISO>`; other non-US paused shells use base product paths plus `country=<ISO>`.
- Merchant did not clear: latest exact completed count remains `623` paid-cohort US/en `Missing age group` IDs, sample source timestamp remains `2026-05-07T14:14:02+00:00`, and API paths remain blocked by insufficient scopes.
- Pinterest remains parked: Event Quality `Fair`, EN source completed with `152` warnings, failed sitemap source remains failed, and item proof is `337/346` with `9` unresolved variants.
- A concrete Pinterest local paused US draft package exists in `lanes/pinterest-solution/`: `resolved_337_product_scope.csv`, `excluded_unresolved_9.csv`, `product_group_scope.csv`, `paused_campaign_draft_plan.csv`, and `creative_draft_rows.csv`.
- A concrete Merchant source-refresh solution ladder exists in `lanes/merchant-solution/MERCHANT_SOURCE_REFRESH_SOLUTION_LADDER.md`; the fix path is one official source refresh/sync/update-products action after just-in-time readbacks and exact approval, not more Shopify product edits.
- Localization matrix is written: ES/IT/RO/PT are the strongest localized paused candidates; GB/CA/AU are English-first paused-only; broader countries need QA before spend.
- ROAS guardrails are refreshed: at `$70` AOV max CPA is `$10.77`; `$0.15` CPC needs about `1.39%` CVR; RO presents RON and needs currency-normalized reporting.
- Creative copy packs are local-only and validated; do not upload them without approval and platform readbacks.

Unresolved blockers:

- No live Google Ads import/create/enable/spend approval exists.
- Merchant age_group/source propagation is not cleared; do not repeat the Google & YouTube toggle or click refresh/sync/upload without exact approval.
- Pinterest drafts/spend remain blocked by Event Quality, catalog warnings/failed sitemap source, and `9` unresolved candidate rows.
- Non-ES/IT/RO/PT markets still need country/currency/shipping/language QA before live spend.

Closest next path to the North Star:

1. If the owner wants paused account-side infrastructure now, request and receive the exact paused international growth approval gate from `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.
2. After approval, run just-in-time readbacks, preview-only import the refreshed Ads packet from `lanes/ads-intl/`, confirm all entities remain paused, then apply only the approved paused build.
3. For Merchant, request the exact approval phrase in `lanes/merchant-solution/MERCHANT_SOURCE_REFRESH_SOLUTION_LADDER.md`; if granted, run pre-readbacks, execute only one clearly labeled official source refresh/sync/update-products control, and read back the sample timestamp and issue count.
4. For Pinterest, request the exact paused US draft approval phrase in `lanes/pinterest-solution/PINTEREST_US_PAUSED_DRAFT_SOLUTION.md`; if granted, build paused-only US drafts using `resolved_337_product_scope.csv` and excluding `excluded_unresolved_9.csv`.
5. Run country-level storefront/currency/checkout QA for GB/CA/AU and any broader markets before any spend discussion.

Required subagent lanes next:

- Parent control: approvals, coordination, final integration.
- Google Ads intl Search: preview-only import validation if exact approval exists.
- Merchant: read-only source timestamp and product-issues export.
- Pinterest: read-only Event Quality/catalog/item proof; optional paused US draft using the `lanes/pinterest-solution/` package only after exact approval.
- Localization: country-level storefront/currency/no-payment checkout QA for next candidate markets.
- ROAS/measurement: just-in-time reporting and kill-rule board.

Guardrails:

No live spend, no campaign enablement, no budget/bid/status changes, no PMax enable, no Standard Shopping changes, no product-scope/feed-label/product-group changes, no conversion-goal changes, no Merchant uploads, no source refresh/sync/toggle, no Shopify live product-data changes, no Pinterest drafts/spend, no shipping/Markets changes, no theme publish, no payment, and no order creation unless the owner gives fresh explicit action-time approval.
