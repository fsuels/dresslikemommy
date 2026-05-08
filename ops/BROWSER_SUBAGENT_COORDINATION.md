# Browser And Subagent Coordination

Purpose: let multiple agents work quickly in the logged-in ChatGPT Atlas / in-app browser without colliding in Shopify Admin, Google Ads, Merchant Center, GA4, Search Console, Pinterest, or other paid-growth surfaces.

This file supplements `ops/AGENT_COORDINATION.md`. It does not replace the one-writer rule.

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

## Atlas Browser Tab Pattern

When logged-in ChatGPT Atlas / in-app browser access exists, use it instead of asking the owner to log in again.

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
5. Leave the tab open at a useful readback page when handing off.
6. Report current URL, account ID, readback state, and any unsaved-change risk.

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
