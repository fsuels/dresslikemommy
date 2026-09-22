# Agent Guide — dresslikemommy

Scope: whole repo. Changing state/workflows live in `ops/`, `ops/marketing/`, and `docs/agent-loops/`. Keep this file and `CLAUDE.md` byte-identical; strict continuity enforces it.

## Non-Negotiables

This guide extends the active product-specific global guide: Codex uses `~/.codex/AGENTS.md`; Claude uses `~/.claude/CLAUDE.md`. Current user scope can narrow authority. The stricter safety, freshness, approval, or verification rule wins.

- Preserve unrelated worktree changes. Never use destructive git/filesystem actions unless the current turn explicitly names them.
- Keep credentials, tokens, customer PII, and vendor/source URLs out of repo files, logs, prompts, evidence, theme files, and public fields. Credentials live under `~/.config/dresslikemommy/`.
- Never move money, change billing, or exceed exact paid-media authority.
- No agent UI/backend belongs on the live storefront.
- Never approve/apply Shopify-to-Pinterest per-variant rows without shared parent `item_group_id` and parent featured `image_link` across every active market/category. Keep `check_pinterest_feed_grouping.py` wired into strict continuity.
- Dress Like Mommy is dropshipping: no physical store or owned physical inventory. Never imply a retail location, warehouse, local/stocked/on-hand inventory, or unsupported shipping, return, review, bestseller, or promotion claims.

## Routing

Theme is Dawn-derived; operator systems live under `ops/`, `.codex/agents/`, `pixels/`, `agent-backend/`, and subprojects. Evidence lives in `dresslikemommy-growth-2026/02_AUDIT_PACKETS/`; direction in `VISION.md`. There is no root app package.

1. Read this file and `ops/MEMORY_CONTINUITY_PROTOCOL.md`; read `VISION.md` for product, UX, listing, growth, automation, or trust work.
2. For known issues/failed readbacks, use `ops/PROBLEM_SOLVING_PROTOCOL.md` and the matching `ops/PROBLEM_TRACKER.md` entry.
3. For "continue <channel>", run `python3 ops/scripts/compile_task_context.py --query "continue <channel>" --format brief` and read its sourced brief before acting. Otherwise search the latest relevant worklog anchor and exact IDs. Before shared/external work read `ops/AGENT_COORDINATION.md`; account/browser work also requires the access/browser protocols and a task-owned background surface.
4. Paid growth: follow `ops/marketing/AGENTS.md` `Required First Loop`, the sole detailed retrieval map. For the canonical paid-growth goal, first run `python3.13 ops/scripts/open_marketing_cockpit.py` (local only).
5. Listings/sourcing: follow `ops/prompts/START-HERE.md` and relevant `ops/sourcing/` files.

## Retrieval-First Task-Time Adaptation

Use TTT principles as temporary specialization from retrieved repo evidence—not neural-weight training, self-modification, a second state tree, or external-write authority. Canonical files govern; chat/model memory are hints.

Classify substantive work as `DIAGNOSE`, `BUILD`, `VERIFY`, `HANDOFF`, or `BLOCKED`. Retrieve only: durable rules; owning current-state control; latest relevant (not merely global-latest) anchor; matching problem/claim/decision/outcome; and narrow task evidence/loop. Search exact product, campaign, feed, market, file, error, problem, or decision IDs first. Use `ops/scripts/compile_task_context.py` when semantic continuity matters; avoid whole-ledger reads unless targeted retrieval fails. Use `REPO_KNOWN`, `LIVE_READBACK_REQUIRED`, `LIVE_VERIFIED`, and `STALE_OR_SUPERSEDED`; never promote inference into live truth.

Precedence: hard safety; current user scope/fresh approval; current-session exact-surface readback; authoritative control; latest relevant anchor/problem/claim/decision; historical evidence; inference. Scope may narrow authority, never silently broaden it. Contradictory canonical sources fail closed until reconciled. Never embed changing metrics, approvals, blockers, statuses, or literal latest anchors in permanent instructions.

For ambiguous/cross-surface/material work, build one transient frame: objective, entities, dated evidence, authority, contradictions, hypothesis/falsifier, action/alternative, success/kill criteria, verification, rollback, deadline.

- Routine reversible: one direct path plus narrow verification.
- Significant: test the decision-critical premise and compare one credible alternative.
- Material/costly/live/irreversible/durable-rule: add one adversarial challenge and an independent verifier who did not build/execute it.

If evidence disproves a premise, stop dependent work, return to the last verified premise without unapproved destructive rollback, record the contradiction, and change paths. Stop reflection after one challenge unless evidence changes or verification fails. Parent owns approvals, frame, integration, and external writes; subagents use disjoint scopes.

Persist only durable facts, verified outcomes, unresolved gates, and behavior-changing lessons. Routine recurring learning needs two independent observed-outcome events; one high-severity spend/customer-truth/publication/credential/destructive-action/approval-scope event may qualify. Repeated copies do not.

For prompt/checklist changes, freeze 3–5 failures plus a passing holdout and binary criteria, change one rule, and retain it only if failures improve without weakening safety, approvals, customer truth, or passing behavior. Do not edit evaluator and evaluated prompt together. Promote at most one rule per weekly review; otherwise `NO_CHANGE`.

Close by verifying, updating only owning canonical memory, linking matured decisions to expected-vs-observed outcomes, and naming exactly one owner-facing action with why it goes first. Internal queues may retain several disjoint lanes. Paid-growth handoffs must include the existing authority, uncertainty-branch, and independent-verifier machine fields defined by the canonical prompt.

## Execution Rules

- Use the smallest effective change, existing scripts/conventions, and narrow checks. No live data, infrastructure, deployment, auth, or production-config changes unless explicitly required and currently approved.
- One writer per campaign/feed/product cohort/theme/account surface. Parallel read-only work is allowed; writes need a narrow claim.
- GitHub `fsuels/dresslikemommy` branch `main` is the canonical storefront. For requested fixes, review/test, commit/push to `main`, then verify Shopify sync and affected published routes. Local or unpublished fixes are incomplete; previews are temporary test/rollback copies. Maintain one site version. Report actual release blockers precisely; a tool capability limit alone is not a deployment ban.
- Before external Save/Apply/Publish/Upload/Enable/Pause/Remove/Delete/Sync/Submit, confirm claim, exact authority, before-state, after-state plan, rollback. Stop on login, CAPTCHA, account switch, billing, permission, policy, or unexpected destructive prompts.
- A fresh login page is not proof of no access; complete the recovery ladder. Absent env vars mean “credentials not loaded in this shell”; stored-token `401` means regeneration/reinstall is needed.
- Keep theme work Dawn-compatible/minimal; Liquid presentation-focused and JS vanilla/ES-module. Follow `docs/agent-loops/ui-browser-verification-loop.md` and verify affected desktop/mobile plus relevant country/language routes. Use the canonical listing/localized-size-chart workflow.
- Paid-growth North Star: maximize profitable Google/Pinterest conversions at about `650% ROAS`. Judge purchases, revenue/value, CPA, ROAS; treat traffic/quality metrics diagnostically.
- Monitoring must end with `fix now`, `execute approved bounded action`, `prepare exact approval packet`, `reroute to another safe sales-moving lane`, or `hold with evidence because no action is currently valid`. Zero impressions after 24 hours triggers same-day serving/auction and high-intent long-tail action.
- Follow `ops/marketing/expert_growth_playbook_2026.md`; high-intent/low-waste, landing fit, economics, measurement, and anti-cannibalization beat cheap traffic. One blocked lane must not freeze independent work.
- Standing spend authority is usable only when every current command-layer gate agrees. Historical `GREEN`, readiness, approval, or `LIVE_VERIFIED` text is not present authority. Otherwise no spend/enablement/upload/import/budget/bid/status/PMax/remarketing/Shopping/product/feed/conversion or Merchant/Shopify/Pinterest/GA4/GTM production write.

## Validation And Continuity

Run matching checks only: `git diff --check`, theme checks, `node --check`, focused Python tests, Worker `node --test`, and as applicable:

```bash
python3.13 ops/scripts/check_continuity_integrity.py --strict
python3.13 ops/scripts/audit_marketing_command_integration.py --write-report --fail-on-risk
python3.13 ops/scripts/check_pinterest_feed_grouping.py --strict
```

Strict continuity is required after continuity, command-layer, prompt, cockpit, authority, worklog, or handoff changes. Do not deploy without explicit approval.

`ops/AGENT_WORKLOG.md` is the canonical chronology; add an anchor after code/theme/prompt/script/external-state/durable-strategy changes. Problems remain in `PROBLEM_TRACKER.md` until fixed, disproven, safely superseded, or exactly gated. Claims live in `AGENT_COORDINATION.md`; never clear another owner’s claim. `ops/marketing/` is the only paid-growth command layer.

## Final Response

Start `Confidence: H|M|L`; report changes, files, commands/results, residual risks, the single next action and why first, and one continuation prompt. Use direct file links.
