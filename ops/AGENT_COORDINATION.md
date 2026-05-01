# Agent Coordination Registry

Purpose: prevent multiple agents from overwriting, enabling, pausing, or otherwise changing the same campaign, feed, product cohort, theme area, or external system at the same time.

Every new session must read this file after `AGENTS.md` and before touching Google Ads, Merchant Center, Shopify Admin, GA4/GTM, Pinterest, theme files, live product data, or paid-feed artifacts.

## Coordination Rules

- Treat this file as the current active-work registry.
- One writer per workstream. A workstream is a specific campaign, feed cohort, product set, theme area, prompt/script, or external-system surface.
- Read-only auditing can happen in parallel, but read-only agents must not click Save, Apply, Enable, Pause, Upload, Publish, Sync, or Edit unless they first claim a write lane here.
- If a row says `LOCKED_BY_OTHER_AGENT`, do not edit that surface. Gather read-only evidence only if it cannot affect the other agent's work.
- If a row says `OWNER_APPROVAL_REQUIRED`, ask the owner before changing status, budget, conversion goals, product scope, live feed data, or anything hard to reverse.
- Before making changes, add or update a row with your workstream, owner/session label, scope, allowed actions, blocked actions, and expected handoff.
- After finishing, update the row to `DONE`, `HANDOFF`, or `BLOCKED`, and add the latest worklog anchor/evidence path.
- Do not clear another agent's lock unless the owner explicitly says that workstream is transferred, abandoned, or complete.

## Active Workstreams

| Workstream | Surface | Status | Owner / Agent | Allowed Actions | Blocked Actions | Last Evidence / Handoff | Notes |
|---|---|---|---|---|---|---|---|
| Standard Shopping re-enable after clean supplier readbacks | Google Ads campaign `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` / campaign `23802638621` | `DONE_REENABLED_NO_SCOPE_CHANGE` | Codex current session, 2026-05-01; owner approved exact re-enable phrase | Completed: Merchant supplier-domain gate rerun, Shopify active paid-cohort readback, Google Ads clean/enabled readback | Do not change budget, product groups, feed labels, feeds, product scope, conversion goals, PMax, Remarketing, Brand Search, or any other campaign without fresh explicit owner approval | `AGENT_CONTINUITY_ANCHOR: 2026-05-01-standard-shopping-approved-reenabled`; packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-standard-shopping-reenable-approved/` | Owner approval phrase received: `APPROVE RE-ENABLE DLM_US_STANDARD_SHOPPING_TEST_PAID_READY NOW WITH NO BUDGET, PRODUCT SCOPE, OR CONVERSION GOAL CHANGES`. Re-enabled only Standard Shopping; no budget/product-scope/conversion-goal changes. |
| Brand Search expert optimization pass | Google Ads campaign `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` / campaign `23805046526` | `DONE_NO_LIVE_EDITS` | Codex current session, 2026-05-01; owner requested implementation of agreed expert-level fixes from external review | Read-only audit completed; keep monitoring budget/status, first impressions/clicks, search terms, ad review, Quality Score, Search Impression Share | Do not raise above `$5/day`, change conversion goals, change bid strategy, upload customer lists, change targeting from Observation to Targeting, touch Standard Shopping/Merchant/feed/PMax/Remarketing, or use unsupported promo/review/volume claims | `AGENT_CONTINUITY_ANCHOR: 2026-05-01-google-ads-brand-search-expert-pass-no-live-edits`; packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-expert-pass/` | External review was reconciled against live readback. No additional live edits were safe/needed in this pass; conversion-goal work requires separate explicit approval. |
| Brand Search fresh premium asset live upload | Google Ads campaign `DLM_US_SEARCH_BRAND_PROTECT_PAUSED_20260429` / campaign `23805046526` | `ACTIVE_WRITE_CLAIM` | Codex current session, 2026-05-01; owner gave exact approval phrase `APPROVE UPLOAD BRAND SEARCH FRESH IMAGE LOGO AND PRICE ASSETS ONLY; KEEP BUDGET AT $5/DAY; NO PROMOTION ASSET` | Upload/associate only approved fresh image, official logo, and proof-backed price assets from `2026-05-01-google-ads-brand-search-fresh-premium-assets`; keep campaign at existing `$5/day` | Do not add promotion asset; do not raise above `$5/day`, change conversion goals, change bid strategy, upload customer lists, change audience targeting, touch Standard Shopping/Merchant/feed/PMax/Remarketing, or use unsupported promo/review/volume claims | Upload in progress; source packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-brand-search-fresh-premium-assets/` | Prior reused-image recommendation packet is superseded. Promotion asset deferred because no current storefront-visible promo code/offer was verified. |
| PMax Shopping replacement readiness packet | `PMax: Shopping ads (United States)` / campaign `18154132278`; local packet only | `DONE_LOCAL_BLUEPRINT_OWNER_APPROVAL_REQUIRED` | Codex current session, 2026-05-01; owner asked to fix PMax Shopping issues | Completed local-only replacement/archive blueprint, issue matrix, gate checklist, and handoff notes; keep live campaigns paused | Do not enable, pause/unpause, archive/rename live campaign, create replacement campaign, raise budget, expand product scope, upload assets, change conversion goals, or touch locked Standard Shopping/Merchant/feed surfaces | `AGENT_CONTINUITY_ANCHOR: 2026-05-01-google-ads-pmax-shopping-replacement-readiness`; packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-shopping-replacement-readiness/` | Existing live `PMax: Shopping ads (United States)` should not be repaired in place because of wrong Merchant/no-products risk. Next live step requires fresh exact owner approval to create a paused replacement shell or rename/archive the bad campaign. |
| PMax USA T-Shirts local readiness repair | `PMax: USA Google Shopping T-Shirts` / campaign `18154132284`; local packet only | `HANDOFF_LOCAL_PACKET_READY_OWNER_APPROVAL_REQUIRED` | Codex current session, 2026-05-01; owner asked to fix all PMax T-Shirts issues within guardrails | Completed local-only T-shirt cohort/economics proof, claim-safe copy, audience/search-theme plan, activation checklist, and owner handoff; keep live campaign paused | Do not enable, pause/unpause, create/rename/archive campaigns, raise budget, expand live product scope, upload assets, change conversion goals, edit Merchant Center/feed data, edit Shopify live product data, or touch locked Standard Shopping surfaces | `AGENT_CONTINUITY_ANCHOR: 2026-05-01-google-ads-pmax-tshirts-local-readiness-repair`; packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-pmax-tshirts-readiness-repair/` | Old draft URL `/collections/matching-t-shirts` returned 404. New local packet uses one clean paid-ready T-shirt product / 42 variants as a micro-test candidate; live upload/enable still requires owner approval and just-in-time readbacks. |
| Remarketing launch-control repair | `Remarketing - Cart Abandoners & Checkout Starters` / campaign `23609373008` | `DONE_PAUSED_WARM_REMARKETING_READY_FOR_ENABLE_GATE` | Codex current session, 2026-05-01; owner requested all controllable Remarketing blockers fixed before activation | Completed: kept campaign paused, added eligible warm `Product viewers (Retail)` target, kept cart/checkout targets, kept `All Converters` excluded, kept optimized targeting off, rewrote active RDA to generic warm policy-safe copy, verified location/frequency/dynamic-feed controls | Do not enable campaign, raise budget, upload customer PII/Customer Match, edit Standard Shopping/Merchant/feed surfaces, clear another agent's lock, or make unrelated Brand/PMax changes without fresh explicit owner approval | `AGENT_CONTINUITY_ANCHOR: 2026-05-01-google-ads-remarketing-warm-launch-control-ready`; packet `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-01-google-ads-remarketing-launch-control-repair/` | Launch-gate ready as warm remarketing, not pure cart/checkout only. Exact cart list is still Display size 8 and checkout is 0, so product viewers are the required serving bridge. Campaign remains paused at `$1/day`; enable requires fresh exact approval. |

## How To Claim A Workstream

Add a row or update an unclaimed row before editing:

```text
| Short task name | Exact surface/campaign/files | ACTIVE_WRITE_CLAIM | agent/session + timestamp | Allowed actions | Blocked actions | worklog anchor/evidence path | Notes |
```

Keep the claim narrow. Examples:

- Good: `Brand Search search-term readback only`
- Good: `Remarketing policy-safe RDA copy draft, no upload`
- Bad: `Fix Google Ads`
- Bad: `All campaigns`

## Handoff Requirements

Every write claim must end with:

- Live readback or test result.
- Evidence packet path if external systems were touched.
- `ops/AGENT_WORKLOG.md` entry with an `AGENT_CONTINUITY_ANCHOR`.
- Updated status in this file.
- Clear next action and blocked actions.
