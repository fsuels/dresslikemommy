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

- Latest durable paid-growth family anchor in memory: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-es-it-native-signoff-bundle`; later paid-growth monitors also exist, but current repo state must be reconciled from worklog and command layer.
- GB/CA/AU exact Search micro-cohort was enabled under exact owner approval on 2026-05-12 and later saved monitors showed zero data.
- Pinterest US paused draft path has a validated local spec, but controllable authenticated Ads Manager access was blocked.
- Merchant US/en age_group is solved; Merchant US/es source `10627981690` remains approval-gated.
- ES/IT Golden Daisy microtest is local/review-only until native signoff and owner approval.
- 2026-05-14: Active GB/CA/AU Search landing public source exposed a supplier URL in `data-analytics-vendor`; local theme sanitizer is ready and locally verified, but live theme sync/readback is still approval-gated.
- 2026-05-14 owner directive: advertise only active, public, purchasable products; never expose supplier/source URLs; build smarter category/event strategy from current active catalog readbacks, such as Father's Day using Daddy-and-Me and father-inclusive family matching products.
- 2026-05-14 keyword correction: active GB/CA/AU keyword campaigns must not rely only on copied generic exact head terms. A local review-only market/language intent map now exists for GB English-UK, CA English-Canada with French-Canada gated separately, and AU English-Australia at `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-gb-ca-au-keyword-strategy-repair/`.
- 2026-05-14 fresh GB/CA/AU Ads monitor: campaigns/ad groups/keywords/RSA/final URLs passed read-only scope checks and stale search-term filters were cleared, but live final URLs still expose `detail.1688.com` in `data-analytics-vendor`. Owner then clarified a hard `$0.15` CPC cap; current head terms with `$0.65-$0.74` first-page estimates and close variants are rejected. Exact-scope bounded Ads action packet is `BLOCKED_DO_NOT_UPLOAD_OR_APPLY` until scoped live sanitizer sync/readback and `$0.15` long-tail validation pass.
- 2026-05-14 keyword factory criteria: build the high-intent long-tail universe as large as possible locally, but promote only validated market/language/landing/economics-safe batches into live packets. Current reference: `ops/marketing/keyword_factory_015_cpc_criteria.md`.
- 2026-05-14 US primary correction: US is the biggest market and must be explicit in keyword planning. Current reference: `ops/marketing/us_primary_keyword_lane.md`.
- 2026-05-14 proactive action mandate: results over monitor loops. If a mistake, broken state, underperforming path, or clear improvement is visible, fix it when safe/approved; if live approval is missing, prepare the smallest exact approval packet and keep another safe lane moving.
- 2026-05-14 action-biased keyword universe: created `ops/marketing/keyword_strategy.md`, `ops/marketing/keyword_scoring_rubric.md`, and `ops/marketing/keyword_universe.csv` with `105` local rows (`60` US, `15` GB, `15` CA, `15` AU; `77` `GREEN`, `20` `YELLOW`, `8` `RED`). It is for validation and controlled promotion, not live upload.
- 2026-05-14 command-layer integration guard: created `ops/scripts/audit_marketing_command_integration.py` and generated `ops/marketing/command_layer_integration_audit.md`. Initial audit found `4` side-document risks; current audit covers `25` tracked files and reports `0` risks. New `ops/marketing/` artifacts must be registered, action-linked, continuity-logged, or marked generated/archive before they count as complete.

## Maintenance Rule

After any meaningful paid-growth session, update this digest only with durable compressed facts. Put detailed evidence in packets, worklog, tracker, and the specific command-layer files.
