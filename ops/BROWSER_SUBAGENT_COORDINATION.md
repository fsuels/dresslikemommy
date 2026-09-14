# Browser And Subagent Coordination

Purpose: let multiple agents work quickly in the logged-in ChatGPT Atlas / in-app browser without colliding in Shopify Admin, Google Ads, Merchant Center, GA4, Search Console, Pinterest, or other paid-growth surfaces.

This file supplements `ops/AGENT_COORDINATION.md`. It applies to separate Codex tasks as well as child agents and does not replace the one-writer rule.

## Background Routing And Personal Computer Use

Use a structured connector/API for supported data and actions. When rendered UI is needed, create or reuse a task-owned background browser surface and address that exact tab handle. With the currently exposed CUA API, a new in-app page can be requested with `cua.createBrowserTab("iab", exactUrl, {visible:false})`; check the tool's current documentation and actual availability before relying on it. Other tasks need their own supported surface, not the same selected tab.

The owner's personal browser/desktop is not a shared automation pool. Do not inventory unrelated personal tabs, select the foreground browser, or fall back to native keyboard/mouse, clipboard paste, account switching or browser-wide settings to recover an unavailable background surface. If the exact necessary action requires an interactive surface, record the blocked action and request that specific handoff only when current authorization does not cover it. Keep other connector, research and local work moving. This routing never bypasses authentication, tool restrictions or automatic approval review.

Tab IDs are handles scoped to their tool/browser session, not globally unique identities. Record the owning Codex task, browser/session identity when exposed, exact URL and business entity together. Read back that identity at startup and after reconnecting; never copy another task's bare tab ID into a new session. Tabs can share login/cookie state: a separate tab is not proof of an isolated browser profile or virtual computer.

Check lifetime and concurrency empirically. A handoff marker does not guarantee that a browser survives another agent turn. If a surface disappears, one supported targeted recovery is reasonable; persistent unavailability is a lane blocker, not permission to control the owner's desktop. Close only the task's disposable test tabs after verification; retain a business handoff tab only when the runtime supports it and the handoff is intentional.

This is a cooperative routing contract, not an OS lock or a cloud runtime. It cannot force already-running tasks to reread instructions, guarantee simultaneous authenticated browser capacity, or keep local agents running while the Mac sleeps. Record actual test results separately from expected capability. Full desktop isolation or an always-on remote worker requires separately configured infrastructure.

## Standing Owner Preference

For paid-growth and revenue/profit work, the owner has explicitly stated that time is money and future agents should not default to a single-agent workflow when a parent/orchestrator plus subagents can move faster. After reading this file and `ops/AGENT_COORDINATION.md`, the parent agent should assign disjoint subagent lanes by default whenever subagent tooling is available.

If subagent tooling or browser-session tooling is unavailable in a session, the parent must say so clearly and execute the same lane plan with the fastest safe sequential/local workflow. Do not silently collapse the plan into a slow one-agent audit.

Non-blocking lane rule: a blocked browser/account lane must not stall unrelated paid-growth lanes. If Merchant Center is waiting on processing, Shopify Google & YouTube is blocked by login, Pinterest is waiting on event-quality refresh, or Google Ads needs approval before a live write, the parent should record that blocker and keep other safe read-only/local/paused-build lanes moving. Only pause all work when the blocked lane is a true prerequisite for every remaining safe task.

## Core Rules

- Parent agent owns orchestration, approvals, live writes, final integration, and the final report.
- Subagents may work in parallel only on disjoint scopes assigned by the parent.
- Every subagent must know which other workstreams are active before touching external systems.
- Each subagent must use its own browser tab or browser session for its assigned surface.
- Never share a tab for two different workstreams.
- Never use another agent's tab unless the parent explicitly transfers that tab/workstream.
- Read-only browser audits may run in parallel.
- Writes require a narrow active claim in `ops/AGENT_COORDINATION.md`.
- Only one writer may touch a platform/surface at a time. Examples:
  - one Google Ads campaign writer
  - one Merchant feed/source writer
  - one Shopify product/cohort writer
  - one Shopify theme writer
  - one Pinterest campaign writer
- If a subagent sees an unexpected modal, unsaved changes banner, account switcher, approval prompt, billing prompt, permission prompt, login, CAPTCHA, or policy warning, it must stop and report to the parent.
- Do not sign out, switch Google accounts, switch Merchant/Ads accounts, save passwords, enter credentials, solve CAPTCHA, accept payment/billing prompts, or grant browser permissions unless the owner has explicitly approved that exact action.
- If one subagent stops on a modal, login, CAPTCHA, policy warning, or missing approval, the parent should leave that lane stopped and reallocate work to other independent lanes rather than asking all agents to wait.

## Account Access Recovery

Read `ops/ACCOUNT_ACCESS_PROTOCOL.md` before declaring any Google Ads, Merchant Center, GA4/GTM, Search Console, Shopify Admin, Pinterest, GitHub, or business-email access blocker.

A login screen in a fresh tab is not enough evidence for a blocker. The parent or surface owner must first:

1. Check configured connectors and the task's assigned background session without exposing secrets or inspecting unrelated personal tabs.
2. Claim an available task-owned surface; reuse authenticated access only within the assigned boundary. A new dedicated tab is allowed when required for isolation.
3. Navigate from an authenticated surface to the exact account, advertiser, property, store, repository, or mailbox.
4. Use owner-provided current-session credentials only transiently when the target site and account are clear.
5. Stop only for CAPTCHA, MFA/2FA, account chooser ambiguity, permission denial, billing/payment prompts, policy prompts, destructive-change prompts, or no available credential/session after the ladder is complete.

Record the result as `ACCESS_RECOVERY_REQUIRED`, `MFA_OR_CAPTCHA_REQUIRED`, `PERMISSION_REQUIRED`, or `ACCOUNT_SWITCH_REQUIRED` unless the failed access is a true prerequisite for the next approved action. Do not call it a generic P0 blocker while other safe lanes can continue.

## Atlas Browser Tab Pattern

When authenticated access exists in the assigned background browser, reuse it within that boundary. A logged-in personal Chrome tab is not automatically assigned to an agent.

Preferred tab naming/session naming pattern:

```text
DLM-PARENT-Control
DLM-MERCHANT-US-SourceRefresh
DLM-SHOPIFY-GoogleYouTube
DLM-GOOGLEADS-IntlSearch
DLM-PINTEREST-EventCatalog
DLM-GA4-GSC-Measurement
DLM-QA-LandingLocalization
```

If the browser tool supports session naming, name the browser session with the same workstream. If it does not support visible tab naming, keep a written tab map in the evidence packet and include screenshots with URL/time.

Each subagent should:

1. Open or reuse only its assigned tab.
2. Confirm the account/store/advertiser before reading or editing.
3. Save screenshots/downloads to its own evidence packet.
4. Avoid navigating away from another agent's page.
5. Leave a business tab at a useful readback page only if the runtime supports the intended handoff; close disposable tests.
6. Report owning task and browser identity, current URL, account ID, readback state and any unsaved-change risk. The receiving task must verify availability rather than trust an old handle.

## Suggested Parallel Paid-Growth Lanes

Use these as disjoint scopes when the owner authorizes subagents:

| Lane | Browser Tab | Primary Surface | Default Mode | Write Owner |
|---|---|---|---|---|
| Parent control | `DLM-PARENT-Control` | coordination, approvals, final readbacks | orchestration | parent only |
| Merchant source refresh | `DLM-MERCHANT-US-SourceRefresh` | Merchant Center US `Shopify App API` source, diagnostics, sample items | read-only first | one Merchant writer only after approval |
| Shopify Google channel | `DLM-SHOPIFY-GoogleYouTube` | Shopify Admin Google & YouTube channel/app sync status | read-only first | one Shopify channel writer only after approval |
| Google Ads international Search | `DLM-GOOGLEADS-IntlSearch` | paused Search campaign shells, RSAs, keywords, negatives | build only after approval | one Google Ads writer |
| Pinterest growth | `DLM-PINTEREST-EventCatalog` | Pinterest tag/event health, catalog, paused campaign drafts | read-only first | one Pinterest writer |
| Measurement | `DLM-GA4-GSC-Measurement` | GA4, Google Tag, Search Console readbacks | read-only unless approved | measurement writer only after approval |
| Landing/localization QA | `DLM-QA-LandingLocalization` | storefront language/shipping/landing-page checks | read-only/theme-local unless approved | theme writer only after approval |

## Browser Write Checklist

Before clicking Save, Apply, Publish, Upload, Enable, Pause, Remove, Delete, Sync, or Submit:

1. Confirm the workstream has an active write claim in `ops/AGENT_COORDINATION.md`.
2. Confirm the exact owner approval phrase covers the action.
3. Read back current state before editing.
4. State the specific button/action and surface in the subagent handoff.
5. Make the smallest approved change.
6. Read back the resulting state.
7. Save screenshot/download evidence.
8. Update worklog and coordination row.

## Conflict Recovery

If two agents collide on the same surface:

1. Stop both workstreams.
2. Parent reviews `ops/AGENT_COORDINATION.md`, browser tab URLs, screenshots, and any unsaved changes.
3. Parent chooses one writer and one read-only observer, or closes one lane.
4. Do not discard unsaved changes unless the owner or parent explicitly approves.

## Evidence Requirements

Every browser workstream must leave:

- Evidence packet path under `dresslikemommy-growth-2026/02_AUDIT_PACKETS/`.
- Screenshots or downloaded reports for important readbacks.
- Current URL and account/store/advertiser ID.
- Exact actions taken.
- Exact actions intentionally not taken.
- Residual risk and next action.
