# CRO Parallel Execution Plan

Last updated: 2026-02-25
Owner: CRO Coordinator (Codex)

## 1) Purpose
This file is the source of truth for running multiple AI agents on CRO work in parallel without file conflicts.

Primary goal: increase qualified conversions while preserving trust, accessibility, performance, and compliance.

## 2) Non-negotiable rules for all agents
1. Read these files before coding:
   - `AGENTS.md`
   - `CRO-TASK.MD` (this file)
   - `ops/AGENT_WORKLOG.md` (latest entries at bottom)
2. Work on exactly one task ID only.
3. Edit only the allowed files listed in your task.
4. If you need to edit a file owned by another task, stop and hand off to coordinator.
5. Do not invent runtime facts. If you cannot verify from repo/runtime, mark as `NEEDS_DATA` in your notes.
6. No dark patterns or fake urgency/scarcity.
7. Keep changes surgical and Dawn-compatible.
8. Keep i18n and a11y intact.
9. Log your work in `ops/AGENT_WORKLOG.md` using the template below.

## 3) Worklog template (required)
Append this exact structure at the end of `ops/AGENT_WORKLOG.md`:

```
Patch: <TASK-ID short title>
Date: 2026-02-25
AGENT_CONTINUITY_ANCHOR: 2026-02-25-<task-id>-<short-slug>

Scope completed
- ...

Changes applied (evidence-first)
- file:line-range summary

Validation snapshot
- commands run + result

Open TODOs / NEEDS_DATA
1) ...
```

## 4) Collaboration protocol (how to avoid collisions)
1. Coordinator assigns tasks by ID.
2. One branch per task: `cro/<task-id>-<short-slug>`.
3. Only the coordinator edits `CRO-TASK.MD`.
4. If two tasks must touch the same file, they are not parallel. Use dependency order.
5. Merge order must follow the dependency table in section 6.
6. Agents must include changed-file list in final handoff.

## 5) Global quality gates for every task
Run all unless your task says otherwise:
1. `git diff --check`
2. `shopify theme check --fail-level error --output text`
3. Page-specific manual validation notes (desktop + mobile)

Important: this repo has pre-existing theme-check errors. Your task passes if you do not add new errors and you clearly report any unchanged baseline errors.

## 6) Parallelization matrix

| Task ID | Title | Priority | Can run in parallel? | Depends on | File collision risk |
|---|---|---|---|---|---|
| CRO-02 | Cart conversion resilience | P1 | Yes | None | Low |
| CRO-03 | PDP trust + variant clarity | P1 | Yes | None | Medium (large single file) |
| CRO-04 | Search reliability + intent consistency | P1 | Yes | None | Medium |
| CRO-05 | Breadcrumb and collection-link integrity | P1 | Yes | None | Low |
| CRO-06 | Legal visibility + footer mobile a11y | P1 | Yes | None | Low |
| CRO-07 | Utility recovery pages (404 + list collections) | P1 | Yes | None | Low |
| CRO-08 | Global theme/header performance hygiene | P1 | Yes (merge late) | None | Medium |
| CRO-09 | Home conversion polish | P2 | Yes | None | Low |
| CRO-01 | Telemetry integration pass | P1 | No (run after other tasks) | CRO-02/03/04/06/09 | High (`assets/analytics.js`) |
| CRO-00 | Final integration + QA sweep (coordinator) | P1 | No | All tasks | N/A |

### Recommended execution waves
- Wave A (parallel now): `CRO-02`, `CRO-03`, `CRO-04`, `CRO-05`, `CRO-06`, `CRO-07`, `CRO-08`, `CRO-09`
- Wave B (after Wave A merges): `CRO-01`
- Wave C (final): `CRO-00`

---

## 7) Task instructions (one by one)

## CRO-02 - Cart conversion resilience (P1)
Status: OPEN
Parallel: YES

### Objective
Reduce cart abandonment caused by unclear errors and weak reassurance before checkout.

### Allowed files
- `assets/cart.js`
- `sections/main-cart-footer.liquid`
- `snippets/cart-drawer.liquid`
- Optional for strings only: `locales/*.json`

### Do not edit
- `assets/analytics.js` (reserved for CRO-01)

### Step-by-step
1. In `assets/cart.js`, replace generic cart error fallback with specific message mapping where possible (stock, min/max, network).
2. Keep line-level error rendering in place and improve actionable copy.
3. In cart footer and cart drawer, add concise policy-backed reassurance near checkout CTA (shipping/returns/privacy links only if real pages exist).
4. Do not add fake claims or unverifiable delivery percentages.
5. Preserve existing checkout button behavior and forms.

### Acceptance criteria
- Cart quantity/update failures provide actionable messages.
- Reassurance block appears near checkout CTA in both cart page and drawer.
- No regressions in empty cart or disabled checkout states.

### Validation
1. Update quantity above allowed max -> clear error.
2. Remove item -> cart updates correctly.
3. Empty cart state still renders and checkout is disabled.
4. Cart drawer and cart page both pass keyboard navigation.

### Handoff format
- Changed files list
- Before/after behavior summary
- `NEEDS_DATA` items

### Copy/paste prompt for assigned AI
You are implementing `CRO-02` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. Edit only allowed files. Improve cart error recovery UX and add truthful reassurance near checkout CTA in cart page and drawer. Do not touch `assets/analytics.js`. Run quality gates, then append your worklog entry with evidence.

---

## CRO-03 - PDP trust + variant clarity (P1)
Status: OPEN
Parallel: YES

### Objective
Increase PDP add-to-cart rate by removing risky hardcoded claims, exposing policy context, and improving variant-choice clarity.

### Allowed files
- `sections/main-product.liquid`
- `snippets/product-variant-picker.liquid`
- Optional for strings: `locales/*.json`
- Optional styling support: `assets/component-product-variant-picker.css`

### Step-by-step
1. Remove or neutralize hardcoded trust/urgency statements that are not data-backed.
2. Replace long hardcoded shipping/security text blocks with concise, policy-linked content.
3. Remove inline hiding of the built-in PDP tax/shipping policy area if policy content exists.
4. Replace hardcoded English UI strings in sticky/mobile ATC and size prompts with translation keys.
5. Keep the current size-required logic behavior intact (no regression).

### Acceptance criteria
- No unverifiable hardcoded claims remain in PDP buy area.
- Variant prompt and CTA labels are translation-key based.
- PDP still handles color-first/size-first selection safely.
- No JS errors in sticky mobile ATC flow.

### Validation
1. Product with Size + Color: choose Color first, confirm size guidance appears.
2. Select Size, confirm CTA returns to normal state.
3. Product without Size option still behaves correctly.
4. Mobile sticky ATC syncs with main form state.

### Handoff format
- Exact claims removed/replaced
- New translation keys added
- Any `NEEDS_DATA` remaining for policy content

### Copy/paste prompt for assigned AI
You are implementing `CRO-03` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. Edit only PDP files listed for this task. Remove unverifiable trust/urgency copy, expose truthful policy context, and localize hardcoded variant/CTA prompt strings. Preserve current variant validation behavior. Run quality gates and log evidence.

---

## CRO-04 - Search reliability + intent consistency (P1)
Status: OPEN
Parallel: YES

### Objective
Fix search-page refinement reliability and align search behavior across header/search surfaces.

### Allowed files
- `sections/main-search.liquid`
- `assets/predictive-search.js`
- `snippets/header-search.liquid`
- `snippets/visible-header-search.liquid`
- Optional: `assets/main-search.js`
- Optional strings: `locales/*.json`

### Step-by-step
1. Ensure `/search` page has a visible, functional search form for refinement.
2. Keep behavior consistent between header search and search page.
3. Decide and implement one clear strategy:
   - product-only search (recommended now), or
   - mixed-content search.
4. If product-only, make that explicit in labels/placeholders (do not mislead users).
5. Preserve no-results and filtered-empty recovery states.

### Acceptance criteria
- Users can submit/refine query directly on `/search`.
- Search scope is consistent and explicit.
- Predictive results render without JS errors.
- Keyboard and screen-reader behavior remains valid.

### Validation
1. Query with results.
2. Query with no results.
3. Refinement from existing query.
4. Mobile search interaction.

### Handoff format
- Strategy chosen (product-only or mixed)
- Files changed
- Remaining `NEEDS_DATA`

### Copy/paste prompt for assigned AI
You are implementing `CRO-04` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. Fix `/search` refinement UX, align scope across search components, and preserve accessibility. Use only allowed files. Run quality gates and log evidence.

---

## CRO-05 - Breadcrumb and collection-link integrity (P1)
Status: OPEN
Parallel: YES

### Objective
Prevent dead/mismatched navigation links from PDP and collection breadcrumb systems.

### Allowed files
- `snippets/breadcrumbs.liquid`
- `snippets/collection-breadcrumbs.liquid`

### Step-by-step
1. Stop generating blind `/collections/{{ handleize }}` URLs without existence checks.
2. Prefer `collections[handle].url` when target exists.
3. If target does not exist, gracefully skip link or fall back to current valid parent path.
4. Keep existing visual breadcrumb UI mostly unchanged.
5. Remove brittle logic where possible but do not break current category-pill behavior.

### Acceptance criteria
- Breadcrumb links resolve to existing routes for tested collections/products.
- No empty or broken breadcrumb anchors are rendered.
- Current active-page markers stay correct.

### Validation
1. Test top-level category collections.
2. Test special-handle branches (`daddy-*`, `family-*`, etc.).
3. Test PDP with missing/partial metafields.

### Handoff format
- Link generation rules changed
- Fallback behavior implemented

### Copy/paste prompt for assigned AI
You are implementing `CRO-05` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. Harden breadcrumb link generation to avoid dead routes, with graceful fallbacks. Edit only breadcrumb snippets. Run quality gates and log evidence.

---

## CRO-06 - Legal visibility + footer mobile a11y (P1)
Status: OPEN
Parallel: YES

### Objective
Increase trust/compliance visibility and fix footer mobile keyboard interaction quality.

### Allowed files
- `sections/footer.liquid`
- Optional strings: `locales/*.json`

### Step-by-step
1. Set policy visibility default to enabled (`show_policy` default true).
2. Keep policy list conditional on existing policies.
3. Fix mobile footer accordion key handling:
   - replace generic `keypress` toggling with key-filtered keyboard support (Enter/Space).
4. Preserve existing footer structure and styling.

### Acceptance criteria
- Policy links display by default when policies exist.
- Footer headings are keyboard-accessible without accidental toggles.
- No regression in desktop footer behavior.

### Validation
1. Mobile footer accordion with keyboard.
2. Desktop footer unchanged.
3. Policy links render correctly.

### Handoff format
- Accessibility behavior before/after summary
- Policy visibility defaults changed

### Copy/paste prompt for assigned AI
You are implementing `CRO-06` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. Enable footer policy visibility by default and fix mobile footer keyboard interaction semantics. Edit only footer files. Run quality gates and log evidence.

---

## CRO-07 - Utility recovery pages (404 + list collections) (P1)
Status: OPEN
Parallel: YES

### Objective
Recover lost sessions from broken URLs and stabilize the collections directory template.

### Allowed files
- `sections/main-404.liquid`
- `sections/main-list-collections.liquid`
- `templates/list-collections.json` (only if needed)

### Step-by-step
1. Remove forced redirect from 404 template.
2. Keep a clear recovery UI on 404 (continue shopping + search or top collections).
3. Rebuild `main-list-collections.liquid` into valid, stable Dawn-compatible structure.
4. Preserve existing configurable settings where possible.

### Acceptance criteria
- 404 page renders without auto-redirect.
- `/collections` page renders valid output and pagination/sorting behave correctly.
- No Liquid syntax errors in these templates.

### Validation
1. Visit invalid URL and confirm visible 404 recovery options.
2. Visit `/collections` with multiple collections.
3. Run `shopify theme check` and confirm no new errors from these files.

### Handoff format
- 404 behavior change summary
- List-collections structural fixes summary

### Copy/paste prompt for assigned AI
You are implementing `CRO-07` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. Remove 404 auto-redirect, build a recovery-focused 404 page, and repair list-collections template structure. Edit only task files. Run quality gates and log evidence.

---

## CRO-08 - Global theme/header performance hygiene (P1)
Status: OPEN
Parallel: YES (merge late)

### Objective
Reduce conversion risk from global CSS/script debt in `theme.liquid` and `header.liquid`.

### Allowed files
- `layout/theme.liquid`
- `sections/header.liquid`
- Optional if needed for extraction: `assets/*.css`
- Optional card payload optimization: `snippets/card-product.liquid`

### Step-by-step
1. Remove invalid CSS values (example: `#white`).
2. Clean malformed duplicate script attributes in header script tags.
3. Remove style blocks placed after `</html>`.
4. Move non-critical large inline styles into asset files where safe.
5. Keep visual output stable and avoid broad restyling.

### Acceptance criteria
- No style blocks after `</html>`.
- Header scripts use valid attributes.
- Invalid CSS tokens removed.
- No obvious visual regression on Home, PDP, Collection, Cart.

### Validation
1. Check rendered head/body structure for validity.
2. Spot-check top templates for styling regressions.
3. Run `git diff --check` and `theme check`.

### Handoff format
- Inline CSS moved/removed summary
- Any remaining debt marked `NEEDS_DATA` or follow-up

### Copy/paste prompt for assigned AI
You are implementing `CRO-08` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. Perform safe global cleanup in `theme.liquid` and `header.liquid`: valid markup/CSS/script attributes, remove trailing style blocks, and reduce non-critical inline CSS. Keep layout stable. Run quality gates and log evidence.

---

## CRO-09 - Home conversion polish (P2)
Status: OPEN
Parallel: YES

### Objective
Improve homepage clarity and conversion flow to collections without adding heavy redesign risk.

### Allowed files
- `sections/hero-banner.liquid`
- `sections/collection-list.liquid`
- `templates/index.json` (only if section config adjustments are needed)

### Step-by-step
1. Ensure hero CTA behavior remains reliable with graceful fallback when anchor target is missing.
2. Keep image loading strategy sane (no unnecessary eager/high priority assets beyond first meaningful hero).
3. Preserve collection-list empty-collection safeguards.
4. Add only truthful trust/value copy (if needed).

### Acceptance criteria
- Hero CTA always leads to meaningful destination.
- No broken in-page anchor behavior.
- No regression in collection-list rendering.

### Validation
1. Home desktop/mobile.
2. Hero CTA with and without anchor target.
3. Collection blocks with empty and non-empty collections.

### Handoff format
- Hero CTA reliability summary
- Any loading behavior changes and rationale

### Copy/paste prompt for assigned AI
You are implementing `CRO-09` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. Apply low-risk homepage conversion improvements focused on hero CTA reliability and collection flow. Edit only allowed files. Run quality gates and log evidence.

---

## CRO-01 - Telemetry integration pass (P1, run after other tasks)
Status: BLOCKED (until Wave A merged)
Parallel: NO

### Objective
Create one coherent measurement layer for funnel, errors, and key micro-conversions.

### Allowed files
- `assets/analytics.js`
- `snippets/meta-tags.liquid`
- Optional for hooks if missing: small additions in task-owned templates after coordinator approval
- Optional documentation: `ops/` docs file

### Step-by-step
1. Fix product fallback price meta selector mismatch (`product:price:amount` vs `og:price:amount`).
2. Add/adjust events for:
   - cart update errors
   - search submit/no-results/result click
   - auth submit/error
   - contact form submit/success/error
   - 404 view/recovery click
3. Keep dedupe protections to prevent event spam.
4. Ensure all payloads are non-PII.
5. Keep existing GA4 ecommerce payload conventions consistent.

### Acceptance criteria
- Event schema is documented and consistent.
- No duplicate high-frequency events on simple interactions.
- Existing `view_item`, `add_to_cart`, `view_cart`, `begin_checkout` still work.

### Validation
1. Trigger each event path manually in preview.
2. Confirm payload keys and no PII.
3. Confirm no JS errors.

### Handoff format
- Event list added/changed
- Payload schema table
- `NEEDS_DATA` list for checkout-hosted events outside theme scope

### Copy/paste prompt for assigned AI
You are implementing `CRO-01` in `dresslikemommy`. Follow `AGENTS.md` and `CRO-TASK.MD`. This task runs after Wave A merges. Own all telemetry changes in `assets/analytics.js` and related meta selector fixes. Keep payloads non-PII, deduped, and GA4-compatible. Run quality gates and log evidence.

---

## CRO-00 - Final integration and QA sweep (Coordinator only)
Status: OPEN
Parallel: NO

### Objective
Integrate all task branches safely, resolve conflicts, and produce final release checklist.

### Steps
1. Merge tasks in dependency-safe order.
2. Resolve conflicts with file ownership rules.
3. Run full validation pass:
   - theme check
   - critical page manual sweep
   - telemetry smoke checks
4. Produce final changelog and rollback notes.

### Merge order (recommended)
1. CRO-07
2. CRO-05
3. CRO-06
4. CRO-02
5. CRO-04
6. CRO-03
7. CRO-09
8. CRO-08
9. CRO-01

---

## 8) Quick assignment sheet
Use this when dispatching agents:

- Agent A -> `CRO-02`
- Agent B -> `CRO-03`
- Agent C -> `CRO-04`
- Agent D -> `CRO-05`
- Agent E -> `CRO-06`
- Agent F -> `CRO-07`
- Agent G -> `CRO-08`
- Agent H -> `CRO-09`
- Agent I (after Wave A) -> `CRO-01`
- Coordinator -> `CRO-00`

## 9) Final reminder for every agent
Do not expand scope. Do not edit files outside your task. Log evidence. If blocked, stop and escalate with exact file and reason.
