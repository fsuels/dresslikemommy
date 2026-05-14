# Marketing Memory Digest

Last seeded: 2026-05-14

## What This Layer Exists To Fix

The repo already has memory. The recurring failure mode was not "no AI team"; it was too much scattered evidence and not enough compact daily execution state for paid marketing decisions.

This layer should answer quickly:

- What is live?
- What is spending?
- What converted?
- What is blocked?
- What can be safely done today?
- What exact approval is needed?

## Durable Rules

- Root `AGENTS.md` stays short.
- `ops/marketing/` carries daily marketing command state.
- Existing `ops/` files remain historical memory and detailed evidence.
- `.codex/agents/` carries real Codex custom agents.
- `AI_Team/` is not an operational source of truth.
- Codex memories help recall context, but checked-in repo files govern execution.

## Current High-Signal Facts

- Latest anchor must be resolved from `ops/AGENT_WORKLOG.md`, then reconciled against this command layer. Do not treat old memory, packet prompts, or historical digests as the practical latest state when the canonical worklog has newer anchors.
- GB/CA/AU exact Search micro-cohort was enabled under exact owner approval on 2026-05-12 and later saved monitors showed zero data.
- Pinterest US paused draft path has a validated local spec, but controllable authenticated Ads Manager access was blocked.
- Merchant US/en age_group is solved; Merchant US/es source `10627981690` remains approval-gated.
- ES/IT Golden Daisy microtest is local/review-only until native signoff and owner approval.
- 2026-05-14: Active GB/CA/AU Search PDP final URL source now passes public supplier/source sanitizer readback across two header/cache variants: `0` supplier-domain hits and `0` URL-like brand attributes. This clears the current PDP final URL gate, not all future collection routes.
- 2026-05-14 owner directive: advertise only active, public, purchasable products; never expose supplier/source URLs; build smarter category/event strategy from current active catalog readbacks, such as Father's Day using Daddy-and-Me and father-inclusive family matching products.
- 2026-05-14 keyword correction: active GB/CA/AU keyword campaigns must not rely only on copied generic exact head terms. A local review-only market/language intent map now exists for GB English-UK, CA English-Canada with French-Canada gated separately, and AU English-Australia at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-gb-ca-au-keyword-strategy-repair/`.
- 2026-05-14 fresh GB/CA/AU Ads monitor: campaigns/ad groups/keywords/RSA/final URLs passed read-only scope checks and stale search-term filters were cleared. Owner clarified a hard `$0.15` CPC cap; current head terms with `$0.65-$0.74` first-page estimates and close variants are rejected. Later public source readback cleared the current active PDP final URL sanitizer gate, but exact-scope bounded Ads action remains blocked until clean-route long-tail rows validate at `$0.15` and reviewer/after-state gates pass.
- 2026-05-14 keyword factory criteria: build the high-intent long-tail universe as large as possible locally, but promote only validated market/language/landing/economics-safe batches into live packets. Current reference: `ops/marketing/keyword_factory_015_cpc_criteria.md`.
- 2026-05-14 US primary correction: US is the biggest market and must be explicit in keyword planning. Current reference: `ops/marketing/us_primary_keyword_lane.md`.
- 2026-05-14 proactive action mandate: results over monitor loops. If a mistake, broken state, underperforming path, or clear improvement is visible, fix it when safe/approved; if live approval is missing, prepare the smallest exact approval packet and keep another safe lane moving.
- 2026-05-14 action-biased keyword universe: created `ops/marketing/keyword_strategy.md`, `ops/marketing/keyword_scoring_rubric.md`, and `ops/marketing/keyword_universe.csv` with `105` local rows (`60` US, `15` GB, `15` CA, `15` AU; `77` `GREEN`, `20` `YELLOW`, `8` `RED`). It is for validation and controlled promotion, not live upload.
- 2026-05-14 collection-route reroute: `mommy-and-me`, `family-matching`, `pajamas`, and `family-swimsuits` passed public source checks for GB/CA/AU. The dirty-route leak source is Shopify automatic `window.ShopifyAnalytics.meta` product JSON, not the sanitized theme `data-analytics-*` attributes. GB/CA/AU matching-dress, vacation, daddy, and swimwear keyword rows were locally rerouted to clean product-relevant routes; `36` GB/CA/AU `GREEN` rows now need authenticated `$0.15` CPC validation. `/collections/swimsuits` still leaks supplier vendors and remains excluded.
- 2026-05-14 command-layer integration guard: created `ops/scripts/audit_marketing_command_integration.py` and generated `ops/marketing/command_layer_integration_audit.md`. Initial audit found `4` side-document risks; current audit covers `25` tracked files and reports `0` risks. New `ops/marketing/` artifacts must be registered, action-linked, continuity-logged, or marked generated/archive before they count as complete.
- 2026-05-14 broad continuity integrity guard: `ops/scripts/check_continuity_integrity.py --strict` now fails if the canonical worklog is missing anchors, alternate worklogs are not quarantined, the canonical prompt hard-codes a stale latest anchor in First actions, spend-authority state disagrees across the command layer, the cockpit HTML is stale, the marketing integration audit has risks, or `AGENTS.md` and `CLAUDE.md` diverge. `ops/AGENT_WORKLOG_utf8.md` is preserved only as `HISTORICAL_DO_NOT_USE`; its unique historical session titles are summarized in the canonical worklog.

- 2026-05-14 CPC validation packet: because authenticated Google Ads/Keyword Planner is unavailable in this automation runtime, the exact next validation scope is packetized at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/GB_CA_AU_SWIM_ROUTE_UNBLOCK_AND_36_ROW_CPC_PACKET.md` and `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-swim-route-unblock/gb_ca_au_36_clean_route_cpc_validation_rows.csv`: `36` clean-route GB/CA/AU `GREEN` rows (`GB=12`, `CA=12`, `AU=12`), the added `family-swimsuits` route passed `6/6` public readbacks with `200` and `0` supplier/url-brand hits, and no upload/add/bid/status action is authorized until authenticated `$0.15` validation passes.
- 2026-05-14 US Shopping query/title diagnosis: Standard Shopping campaign `23802638621` had `17` impressions, `0` clicks/cost/conversions yesterday. Visible terms `family pictures outfits`, `family same outfit`, and `mommy and me wedding guest dresses` do not justify negatives or product-group changes. The local packet at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-automation-us-shopping-query-title-diagnosis/US_STANDARD_SHOPPING_QUERY_TITLE_DIAGNOSIS.md` maps those terms to paid-cohort candidate handles and defines the next authenticated read-only item-level export before any title/feed approval packet. US public route checks keep `/collections/vacation` and `/collections/matching-dresses` held.

## Maintenance Rule

After any meaningful paid-growth session, update this digest only with durable compressed facts. Put detailed evidence in packets, worklog, tracker, and the specific command-layer files.
