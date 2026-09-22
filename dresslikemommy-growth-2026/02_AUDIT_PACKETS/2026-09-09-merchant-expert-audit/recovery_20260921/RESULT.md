# September 21 Merchant source maintenance

Existing US and Australia source maintenance is **implemented and verified with limits**. Merchant Center account **513542500** accepted **4,741 updated offers and zero new offers per market**, recognized all attributes, and reported no product-file issues.

- **US source 10727274744:** complete Shopify source at 21:22:35.148 UTC; one verified pointer renewal and one native Update. Google receipt at 21:33:16.289 UTC cleared the previous scheduled connection failure. Six protected native offers were approved, in stock, correctly priced in USD, and assigned to US free listings.
- **AU source 10727245667:** complete Shopify source at 21:30:52.149 UTC; one manual upload. Google receipt at 21:41:47.697 UTC accepted 186 source-backed AUD price changes: 93 offers A$37→38, 50 offers A$47→48, and 43 offers A$57→58. All nine samples across the three changed price groups and six protected offers showed the correct prices, approved status, in-stock availability, and Australia free listings.

Each complete source contained 238 active parents and 4,925 variants. Each released feed contains 232 eligible parents and 4,741 offers. The existing six holds exclude 162 available offers; 22 unavailable variants also remain excluded. Neither feed added or removed offer identities. Shopify prices and product state were not changed.

Independent before-release reviews passed 39,022 US and 48,740 AU checks. Independent after-reviews passed 66 US and 139 AU checks. Root validation parsed 69 JSON artifacts without error; the owned-checkpoint whitespace check and all 10 strict-continuity groups passed. Both feed generators/configurations remained pinned and unchanged.

This is receiving and sample evidence, not proof that every offer is approved, every buyer route works, or traffic and sales increased. AU still uses its existing manual source. The US public-client 403 remains qualified; no access protection was bypassed, and native Google receipt succeeded separately. Canada, the UK, other languages, and the broader all-market goal remain incomplete.

The reviewed project sync is closed: GitHub main was pushed to `731de115a9f2ba94fe24cef95218332a15b685ee`, and local main was reconciled at `096224cdb5ceb71f40b7e1014a5dc2f4fb445249`. Its 4,484 project-path updates preserved 528 guarded theme/config/workflow entries. Private exclusions, local theme work, and post-cutoff work remain local. This maintenance packet was created after that sync cutoff and was not part of its push.

Next: resume fresh Canada/UK country and buyer-route qualification under current authority. Preserve existing-source freshness targets: US September 22 at 21:22:35.148 UTC and AU September 22 at 21:30:52.149 UTC; the unchanged US 48-hour guard expires September 23 at 21:22:35.148 UTC. Do not repeat either completed submission.

Evidence: `us_au_maintenance_handoff.json`, the US and AU execution handoffs it binds, and `standard_checks.json`. Parent task `01a08223` retains shared canonical integration ownership. Continue through `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.
