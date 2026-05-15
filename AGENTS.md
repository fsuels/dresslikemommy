# Agent Guide - dresslikemommy

Scope: this file applies to the whole repository. It is the short agent bootstrap. Detailed, changing state lives in `ops/` and `ops/marketing/`, not here.

This same bootstrap lives in both `AGENTS.md` and `CLAUDE.md`. Keep the two files byte-for-byte identical; do not maintain separate Claude-only or Codex-only instructions. The continuity check `python3.13 ops/scripts/check_continuity_integrity.py --strict` enforces this.

## Global Guides

This project file extends two user-scope global guides — read them first if available:

- `~/.codex/AGENTS.md` — Codex global (autonomy posture plus shared 18-section agent guide).
- `~/.claude/CLAUDE.md` — Claude global (shared 18-section agent guide).

Global guides carry: verification mandate, secrets/PII discipline, destructive-command guardrails, financial-actions hard stop, adversarial-input handling, citations format, determinism preferences, output discipline, and the self-eval checklist. This file carries only dresslikemommy-specific rules plus a short non-negotiables block so an agent without home-directory access still sees the most dangerous rules.

## Non-Negotiables

Even if the global guides are not loaded, these three rules always apply on this repo:

- Never run destructive git commands (`git reset --hard`, `git clean -fd`, `git checkout --`, `git push --force`, `git push -f`) unless the current turn explicitly requests them by name. Preserve unrelated worktree changes.
- Never write credentials, tokens, or vendor/source URLs into any repo file, commit, log, worklog, theme file, prompt, evidence snippet, or external-system-visible field. Credentials live only in `~/.config/dresslikemommy/`.
- Never execute trades, place orders, send money, charge cards, initiate transfers, or change billing on the user's behalf. Prepare the action and ask the user to perform it.

## Start Here

1. Read this file.
2. Read `ops/MEMORY_CONTINUITY_PROTOCOL.md`.
3. If the task involves a known issue, failed readback, blocker, or repeated uncertainty, read `ops/PROBLEM_SOLVING_PROTOCOL.md` and `ops/PROBLEM_TRACKER.md`.
4. Read the latest entries at the bottom of `ops/AGENT_WORKLOG.md`; search `AGENT_CONTINUITY_ANCHOR` when context is tight.
5. Before touching external systems, theme files, live product data, paid feeds, campaign artifacts, or shared surfaces, read `ops/AGENT_COORDINATION.md`.
6. For account access, logged-in browser/account work, subagents on account surfaces, or any login/account blocker, read `ops/ACCOUNT_ACCESS_PROTOCOL.md` and `ops/BROWSER_SUBAGENT_COORDINATION.md`.
7. For paid-growth work, read `ops/marketing/AGENTS.md`, `ops/marketing/expert_growth_playbook_2026.md`, `ops/marketing/current_marketing_state.md`, `ops/GROWTH_NORTH_STAR.md`, `ops/GOOGLE_ADS_CONTINUITY.md`, and `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.
8. For listing or sourcing work, read `ops/prompts/START-HERE.md` and the relevant files under `ops/sourcing/`.

## Paid-Growth Session Start

When a session starts with `/goal Continue the Dress Like Mommy paid-growth command layer from the latest AGENT_CONTINUITY_ANCHOR`, first render and open the human cockpit:

```bash
python3.13 ops/scripts/open_marketing_cockpit.py
```

This opens `ops/marketing/operator_cockpit.html` locally for the human. It is a local dashboard action only; it does not create live external writes.

## Project Operating Model

The general operating model (evidence-first, smallest effective change, prefer existing scripts, verify before declaring done) lives in the global guides. The dresslikemommy-specific additions are:

- No AI UI or backend agent surface belongs on the live Shopify storefront. Agent tooling is developer/operator-side only.
- Do not modify secrets, credentials, billing, auth providers, deployment config, infrastructure, production data, or destructive filesystem state unless the task explicitly requires it and the current session has the needed approval. (This restates the global rule because external-write approval gating is core to how this repo operates.)

## Memory And Continuity

- `ops/AGENT_WORKLOG.md` is the chronological session log and must receive an `AGENT_CONTINUITY_ANCHOR` after any session that changes code, theme files, prompts, scripts, external-system state, or durable strategy.
- `ops/PROBLEM_TRACKER.md` is the active problem ledger. A real issue stays live until fixed, disproven, superseded by a safer path, or gated with the exact next unblock action.
- `ops/AGENT_COORDINATION.md` is the active write-claim and lock registry. Do not clear or override another agent's claim unless the owner explicitly transfers or clears it.
- `ops/marketing/` is the paid-growth daily command layer. Treat it as the compact execution state for marketing decisions; keep older `ops/` files as historical memory and evidence.
- Do not rely on Codex or Claude chat history as authority when checked-in repo docs can answer the question.
- For paid-growth handoffs, use the single canonical prompt in `ops/prompts/paid-growth-ai-army-continuation-prompt.md`; packet prompts may point back to it but must not become competing operating prompts.
- Run `python3.13 ops/scripts/check_continuity_integrity.py --strict` before closing continuity, paid-growth command-layer, prompt, cockpit, spend-authority, worklog, or handoff changes. The check must pass; if it fails, fix the canonical files rather than creating another side document.

## Problem Handling (project-specific tempo)

The general problem-handling stance (don't write passive "blocked" notes; try the safest direct path then a grounded alternate; document evidence and next unblock action; continue independent work) lives in the global guides under stop conditions. The dresslikemommy-specific additions:

- Every touched problem entry in `ops/PROBLEM_TRACKER.md` needs status, owner/session, surface, symptom, business impact, fixed criteria, attempt log, failed paths, gates, next action, and parallel work to continue.
- Results/action mandate: when you see a mistake, broken state, underperforming path, or clear improvement, take proactive action immediately. If it is local/read-only or inside current approval, fix it and verify. If it requires unapproved live external writes, prepare the smallest exact approval packet and keep other safe sales-moving work going. Monitoring is only useful when it produces a fix, bounded action, optimization decision, or exact unblock step.

## Coordination And External Systems (project-specific)

- One writer per campaign/feed/product cohort/theme area/account surface.
- Read-only audits may run in parallel. Writes require a narrow active claim in `ops/AGENT_COORDINATION.md`.
- A fresh login page in one new tab is not proof that account access is blocked. Before declaring Google Ads, Merchant Center, GA4/GTM, Search Console, Shopify Admin, Pinterest, GitHub, or business email inaccessible, complete `ops/ACCOUNT_ACCESS_PROTOCOL.md`: check existing authenticated tabs/sessions, local secure credential paths or connectors, direct account URLs from the authenticated session, and current-session owner-provided credentials when safe. Do not persist credentials.
- Before clicking Save, Apply, Publish, Upload, Enable, Pause, Remove, Delete, Sync, or Submit in an external system, confirm the claim, approval phrase, before-state readback, and after-state readback plan.
- Parent/orchestrator owns approvals, live writes, final integration, and the final report. Subagents must use disjoint scopes and separate tabs/sessions.
- Stop and report if an external account shows login, CAPTCHA, account switcher, billing, permission, policy, unsaved-change, or destructive-action prompts.

## Paid-Growth Guardrails

- North Star: build and run a profitable paid-growth machine for Dress Like Mommy across Google Ads and Pinterest, aiming for as many profitable conversions as possible at about `650% ROAS`.
- Progress must be sales-moving: approved live tests enabled/monitored, paused-ready campaigns or drafts built, keywords/negatives/copy/assets improved, landing/feed/catalog blockers fixed, performance decisions made from evidence, or exact unblock actions prepared.
- Results over loops: do not run monitor/readback cycles as the deliverable. Every monitor must end by choosing and recording one of `fix now`, `execute approved bounded action`, `prepare exact approval packet`, `reroute to another safe sales-moving lane`, or `hold with evidence because no action is currently valid`.
- Starting 2026-05-14, paid-growth agents must treat each day without sales growth, usable learning, or a sales-moving improvement as a failure signal requiring same-day action. Tomorrow's check must answer paid-growth sales, revenue, CPA, ROAS, and what changed.
- Zero impressions after 24 hours is a same-day action trigger. Diagnose serving and evaluate high-buyer-intent long-tail exact/phrase or auction-entry actions instead of waiting passively.
- Use `ops/marketing/expert_growth_playbook_2026.md` for source-backed 2026 strategy: high-intent/low-waste keywords, anti-cannibalization, channel roles, daily optimization clocks, and specialist agent personas.
- Audits, packets, and readbacks are support work only. They count when they produce action, approval packets, blocker removal, or optimization decisions.
- Default to parent/orchestrator plus parallel subagents for paid-growth when tooling supports it.
- Do not let one blocked lane freeze the sprint. Record the gate and keep independent safe lanes moving.
- Current command-layer files are under `ops/marketing/`; project-scoped Codex agents are under `.codex/agents/`.
- Standing bounded spend authority is not active unless `ops/marketing/spend_authorization.md` says it is approved. Until then, live spend/status/budget/bid/feed/product/conversion writes still require fresh explicit action-time approval.
- Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory. Do not write policy, ad, listing, feed, or report copy that implies a retail location, warehouse, local inventory, stocked inventory, or guaranteed on-hand stock. Platform inventory/salability labels are diagnostics only.

## Paid-Growth Write Boundaries

Unless fresh explicit action-time approval exists in the current session, do not:

- Enable spend, upload/apply/import campaign changes, change budgets/bids/statuses, alter product/feed/conversion scope, or mutate Merchant/Shopify/Pinterest/GA4/GTM production data.
- Enable PMax or unresolved remarketing.
- Change Standard Shopping status, budget, product groups, feed labels, product scope, bids, or conversion goals.
- Change billing, credentials, account access, conversion goals, Shopify products/prices/discounts/policies, Merchant feeds/sources, Pinterest catalog/source/product groups, or native-language ads that are not signed off.

Read-only monitoring, local packet creation, paused/review-only artifacts, and storefront public readbacks are allowed when they stay inside the repo and approved safety bounds.

## Shopify And Credentials

- Shopify Admin API access exists through the operator-managed `n8n Integration` app. Canonical local credential sources are `~/.config/dresslikemommy/shopify-admin.env`, `~/.config/dresslikemommy/admin-api-token.json`, and `~/.config/dresslikemommy/translation-helper-token.json`.
- Credentials must stay outside the repo, worklog, theme files, prompts, and evidence snippets.
- If env vars are unset, say "credentials not loaded in this shell", not "no API access exists".
- If a stored token returns `401`, treat it as stored token regeneration/reinstall needed, not proof the store lacks API access.
- Never write vendor/source URLs into Shopify tags, title, SEO, body copy, product type, customer-visible metafields, feed-visible metafields, or sales-channel-visible product data. Source URLs belong only in local operator evidence.

## Shopify Theme And GitHub Sync

- Theme work should be minimal and Dawn-compatible. Avoid server code in Liquid; use app proxies for backend needs.
- Run narrow JS/Liquid/theme checks for touched areas and review the diff for scope creep.
- `AGENTS.md` and `CLAUDE.md` intentionally mirror each other. Follow current user instructions for sync/push requests and preserve unrelated worktree changes.

## Sourcing And Listing

- For 1688 sourcing, use the existing local sourcing dashboard and files under `ops/sourcing/`; do not restart the pipeline from scratch.
- Keep source credentials and CAPTCHA/login handling outside the repo.
- Rejected 1688 offer IDs should stay rejected unless the user restores them.
- For Shopify listing workflows, use `ops/prompts/START-HERE.md`, `ops/prompts/shopify-listing-master-prompt.md`, and `ops/prompts/shopify-listing-from-1688.md`.
- New listings with size charts must follow the localized size-chart repair and audit workflow before being considered complete.

## Final Response Format

Start with `Confidence: H|M|L`, then report:

- what changed
- files touched
- commands run
- results
- residual risks
- next best action
