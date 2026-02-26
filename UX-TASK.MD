# UX Multi-Agent Execution Plan (dresslikemommy)

Last updated: 2026-02-26  
Scope: Theme UX/CRO implementation tasks only (repo-evidence based)

This document is the handoff playbook for parallel AI agents. Each agent must take one task, keep changes scoped, and avoid merge conflicts.

## 0) How agents cooperate (must read first)

1. One task per agent. Do not expand scope.
2. Claim a task before editing by adding your agent name + branch in the Task Claim Board section below.
3. Edit only files listed in your task's `Allowed files` section.
4. If your task requires touching a file owned by another task, stop and comment in your handoff instead of editing.
5. Keep commits small and descriptive.
6. Run `shopify theme check --fail-level error --output text` before handoff.
7. Provide screenshot/video evidence for mobile + desktop states of the affected page.
8. Do not rewrite unrelated styles/scripts while "already in the file".

## 1) Git and merge protocol

1. Create branch: `agent/<TASK-ID>-<short-name>`
2. Commit format: `<TASK-ID>: <what changed>`
3. Open PR with:
   - Summary
   - Files changed
   - Before/after notes
   - Validation evidence
4. Merge order should follow section 4 (to reduce integration conflicts).

## 2) Task Claim Board

- `UX-00` Owner: Codex (completed) | Branch: n/a
- `UX-01` Owner: unassigned | Branch: 
- `UX-02` Owner: unassigned | Branch: 
- `UX-03` Owner: unassigned | Branch: 
- `UX-04` Owner: unassigned | Branch: 
- `UX-05` Owner: unassigned | Branch: 
- `UX-06` Owner: unassigned | Branch: 
- `UX-07` Owner: unassigned | Branch: 
- `UX-08` Owner: unassigned | Branch: 
- `UX-09` Owner: unassigned | Branch: 
- `UX-10` Owner: unassigned | Branch: 

## 3) Parallelization matrix

| Task | Can run in parallel? | Depends on | Notes |
|---|---|---|---|
| `UX-01` Search page form restoration | Yes | None | Isolated to `sections/main-search.liquid` |
| `UX-02` Header syntax + script tag cleanup | Yes | None | Isolated to header stack files |
| `UX-03` List collections syntax repair | Yes | None | Single file |
| `UX-04` 404 redirect removal + recovery UX | Yes | None | Single file |
| `UX-05` Breadcrumb link robustness | Yes | None | Breadcrumb snippets only |
| `UX-06` Cart + drawer trust clarity near checkout CTA | Yes | None | Cart footer + drawer + locale keys |
| `UX-07` PDP trust/urgency + collapsible accessibility cleanup | Yes | None | `sections/main-product.liquid` (+ optional locale keys) |
| `UX-08` Theme layout CSS debt cleanup + mobile title legibility | Yes | None | `layout/theme.liquid` only; no one else should touch this file |
| `UX-09` Analytics/meta price fallback alignment | Yes | None | `assets/analytics.js` + `snippets/meta-tags.liquid` |
| `UX-10` Integration QA and defect sweep | No (last) | UX-01..UX-09 merged | Final QA sweep task |

## 4) Recommended merge order

1. `UX-03` (syntax blocker)
2. `UX-02` (syntax blocker)
3. `UX-01`
4. `UX-04`
5. `UX-05`
6. `UX-06`
7. `UX-09`
8. `UX-07`
9. `UX-08`
10. `UX-10` (final verification)

---

## TASK DETAILS

### UX-00 (taken): Orchestration and parallel execution guide

Status: Completed by Codex in this file.  
Outcome: Defined parallel-safe task boundaries, ownership, merge order, and validation requirements.

---

### UX-01: Restore functional search input on `/search`

Parallel: Yes

Evidence:
- `sections/main-search.liquid` -> `template-search__search` block -> predictive-search wrapper opens/closes with no actual `<form>` markup between lines 77-85.
- `snippets/visible-header-search.liquid` has a complete, working search form pattern that can be mirrored.

Goal:
- Make `/search` page always show a working search field and submit button.

Allowed files:
- `sections/main-search.liquid`
- Optional: locale keys only if new text is introduced

Do not touch:
- `sections/header.liquid`
- `layout/theme.liquid`

Implementation steps:
1. In `main-search.liquid`, insert a proper search form in the `template-search__search` region.
2. Keep compatibility for both predictive search enabled/disabled.
3. Ensure hidden `options[prefix]=last` exists.
4. Ensure accessible label and proper `role="search"`.
5. Keep existing filter/sort/result rendering unchanged.

Acceptance criteria:
- `/search` displays an input and submit control on mobile and desktop.
- Submitting updates URL with `?q=` and renders results.
- Input has an associated label and keyboard focus works.
- No Liquid syntax errors from this file.

Validation:
- `shopify theme check --fail-level error --output text`
- Manual: `/search`, empty query, valid query, no-results query.

---

### UX-02: Fix header syntax and malformed script tags

Parallel: Yes

Evidence:
- `sections/header.liquid` line ~169 uses dynamic tag syntax that triggers theme-check parse error (`LiquidHTMLSyntaxError`).
- `sections/header.liquid` lines ~136-143 include duplicated `defer` attributes (`defer defer ... defer="defer"`).

Goal:
- Resolve header parsing risk and clean script tag markup so header renders consistently.

Allowed files:
- `sections/header.liquid`
- `snippets/visible-header-search.liquid` (only if required by header structure fix)

Do not touch:
- `layout/theme.liquid`
- `sections/main-search.liquid`

Implementation steps:
1. Replace dynamic open/close HTML tag pattern with valid Liquid branching that renders either `<sticky-header ...>` or `<div ...>` explicitly.
2. Normalize all script tags to single valid `defer` usage.
3. Keep existing behavior (sticky logic and loaded assets) unchanged.
4. Re-run theme check and confirm header syntax error is gone.

Acceptance criteria:
- No Liquid parser error from `sections/header.liquid`.
- Header still supports sticky behavior modes.
- All script tags are valid HTML attributes.
- Mobile and desktop header interactions still work.

Validation:
- `shopify theme check --fail-level error --output text`
- Manual: home page, scroll behavior, mobile menu open/close, search open/close.

---

### UX-03: Repair `main-list-collections` section syntax/structure

Parallel: Yes

Evidence:
- `sections/main-list-collections.liquid` line ~15 closes liquid block with `%}` incorrectly.
- `sections/main-list-collections.liquid` has misplaced `if`/`endif` block outside liquid wrapper and mismatched `<div>` close (theme-check error reports close-before-open at line ~53).

Goal:
- Make list-collections template syntactically valid and renderable.

Allowed files:
- `sections/main-list-collections.liquid`

Do not touch:
- Any other section/snippet

Implementation steps:
1. Rebuild top Liquid logic block (`case`, reverse sort logic, pagination vars) into one coherent `{%- liquid -%}` block.
2. Ensure HTML wrappers open/close correctly.
3. Keep existing sorting/pagination intent.
4. Ensure schema remains valid.

Acceptance criteria:
- No LiquidHTMLSyntaxError in `sections/main-list-collections.liquid`.
- `/collections` list page renders with pagination and cards.
- Sort and reverse logic still respected.

Validation:
- `shopify theme check --fail-level error --output text`
- Manual: list-collections route with at least 2 pages if possible.

---

### UX-04: Remove forced 404 redirect and restore recovery UX

Parallel: Yes

Evidence:
- `sections/main-404.liquid` lines 1-4 force immediate `window.location.replace('/')`.

Goal:
- Keep users on a proper 404 page with recovery options, rather than silent redirect.

Allowed files:
- `sections/main-404.liquid`

Do not touch:
- Routing config

Implementation steps:
1. Remove forced redirect script.
2. Keep/upgrade existing 404 content with clear CTA(s) (continue shopping, search, or featured collections link).
3. Ensure page is accessible and translated through existing keys where possible.

Acceptance criteria:
- Invalid URL remains on 404 template (no automatic redirect).
- 404 page includes at least one primary recovery CTA.
- No JS required for 404 rendering.

Validation:
- Manual: visit a fake URL path and verify 404 remains visible.

---

### UX-05: Harden breadcrumb links against dead handles

Parallel: Yes

Evidence:
- `snippets/breadcrumbs.liquid` uses `product.metafields.custom.category1 | handleize` and `subcategory | handleize` directly for links.
- `snippets/breadcrumbs.liquid` loops `subcategory2` values and links all by handleized text without checking collection existence.
- `snippets/collection-breadcrumbs.liquid` uses parent handle fallback link at line ~199 and constructed URLs even when collection object may be missing.

Goal:
- Prevent breadcrumb links from pointing to non-existent collections.

Allowed files:
- `snippets/breadcrumbs.liquid`
- `snippets/collection-breadcrumbs.liquid`

Do not touch:
- `sections/main-product.liquid`
- `layout/theme.liquid`

Implementation steps:
1. Resolve each breadcrumb target via `collections[handle]` before linking.
2. If missing, render plain text (non-link) for that crumb.
3. Keep current visual breadcrumb structure.
4. Preserve custom cases (`daddy-me`, cross-category logic) but avoid dead URLs.

Acceptance criteria:
- Breadcrumbs never output a link when the target collection is blank.
- Existing valid breadcrumb links still work.
- Product and collection breadcrumb rendering both remain intact.

Validation:
- Manual: test with products/collections having missing or unusual metafield values.

---

### UX-06: Add trust/risk-reversal content near checkout CTA in cart and drawer

Parallel: Yes

Evidence:
- `sections/main-cart-footer.liquid` shows subtotal + tax note + checkout button, but no explicit shipping/returns/security reassurance near CTA.
- `snippets/cart-drawer.liquid` mirrors same pattern in drawer footer.

Goal:
- Reduce pre-checkout hesitation by adding concise trust microcopy adjacent to checkout CTA.

Allowed files:
- `sections/main-cart-footer.liquid`
- `snippets/cart-drawer.liquid`
- `locales/*.json` (only for new translatable strings)

Do not touch:
- Payment logic
- Checkout flow behavior

Implementation steps:
1. Add a compact trust-info block above or below checkout CTA in both cart and drawer.
2. Keep claims factual and generic unless backed by policy links (`shipping_policy`, `refund policy` page link if available).
3. Make text translatable via locale keys.
4. Maintain current layout rhythm on mobile.

Acceptance criteria:
- Trust copy visible near checkout button on cart page and cart drawer.
- Copy is i18n-backed (no hardcoded English unless matching existing pattern requirement).
- No overlap or spacing regressions on mobile.

Validation:
- Manual: `/cart`, cart drawer open state, empty and non-empty cart.

---

### UX-07: Clean PDP trust/urgency claims and improve collapsible accessibility

Parallel: Yes

Evidence:
- `sections/main-product.liquid` lines ~1084-1101 include hardcoded trust claims (`5,000+ Happy Families`, `Quality Guarantee`) without data source.
- Lines ~1128-1130 include specific shipping performance percentages and courier claims (`75.4% within 11 days`) hardcoded.
- Additional info accordion uses custom toggles with static symbols and inline display toggles around lines ~1115+, requiring a11y cleanup.

Goal:
- Keep PDP trust section persuasive but truthful, maintainable, and accessible.

Allowed files:
- `sections/main-product.liquid`
- Optional: `locales/*.json` for any new strings

Do not touch:
- Variant logic that was recently patched unless directly required
- `assets/component-product-variant-picker.css` unless necessary for a11y state

Implementation steps:
1. Replace unverifiable hardcoded claims with configurable or policy-backed statements.
2. Convert custom collapsible blocks to accessible pattern (`button` with `aria-expanded` + controlled panel IDs), or align to Dawn accordion component.
3. Remove hardcoded percentages unless sourced from settings/metafields.
4. Ensure visual hierarchy remains compact on mobile.

Acceptance criteria:
- No unverifiable numeric trust claims hardcoded in PDP trust content.
- Accordion/collapsible elements are keyboard accessible and announce state changes.
- PDP still contains clear shipping/returns/security info with truthful wording.

Validation:
- Manual: PDP mobile and desktop; keyboard-only traversal through trust/collapsible region.

---

### UX-08: Refactor `layout/theme.liquid` CSS debt and fix mobile card title legibility

Parallel: Yes (exclusive ownership of `layout/theme.liquid`)

Evidence:
- `layout/theme.liquid` contains many large inline `<style>` blocks and even `<style>` tags after `</html>` (e.g., around lines ~3866 onward), creating invalid structure risk.
- Mobile title text is forced to tiny size (`font-size: 10px !important`) around line ~1095 and repeated in other blocks, harming readability.

Goal:
- Reduce global layout fragility and restore readable mobile product/card typography.

Allowed files:
- `layout/theme.liquid`
- Optional: `assets/*.css` only if styles are extracted from layout (document exactly what moved)

Do not touch:
- Header/search/PDP/cart section files

Implementation steps:
1. Ensure no styles/scripts are emitted after closing `</html>`.
2. Consolidate the most harmful global inline overrides (especially repeated mobile 10px title rules).
3. Keep behavior unchanged except readability and structure improvements.
4. If extracting CSS to assets, include only moved rules and preserve load order.

Acceptance criteria:
- No `<style>` blocks after `</html>`.
- Mobile product/card titles are readable (target >= 13px equivalent).
- No regressions in homepage/PLP/PDP basic layout.

Validation:
- Manual: home, collection, product on mobile viewport.
- `shopify theme check --fail-level error --output text`

---

### UX-09: Align analytics fallback price selector with emitted meta tags

Parallel: Yes

Evidence:
- `assets/analytics.js` line ~187 reads `meta[property="product:price:amount"]` in fallback.
- `snippets/meta-tags.liquid` outputs `meta property="og:price:amount"` (not `product:price:amount`) around line ~43.

Goal:
- Prevent missing/incorrect fallback price in analytics events when JSON payload is unavailable.

Allowed files:
- `assets/analytics.js`
- Optional: `snippets/meta-tags.liquid` if dual-tag strategy is chosen

Do not touch:
- Event taxonomy logic unrelated to fallback selector

Implementation steps:
1. Update fallback selector to support existing emitted tag(s), preferably both `product:price:amount` and `og:price:amount` for resilience.
2. Keep parsing behavior unchanged.
3. Add minimal inline comment explaining fallback precedence.

Acceptance criteria:
- Analytics fallback successfully reads price on PDP when structured script payload is absent.
- No JS errors in console from analytics initialization.

Validation:
- Manual on PDP with devtools: confirm derived fallback value exists.

---

### UX-10: Final integration QA (post-merge)

Parallel: No (must run after UX-01..UX-09 merged)

Goal:
- Validate that parallel workstreams did not create regressions.

Allowed files:
- QA notes only (`ops/`), unless critical hotfix is required.

Implementation steps:
1. Pull merged branch.
2. Run `shopify theme check --fail-level error --output text` and compare against baseline.
3. Manual QA matrix:
   - Home
   - Collection (with filters/sort)
   - Search
   - PDP (variant select + trust/accordion)
   - Cart page
   - Cart drawer
   - 404
4. Capture defects by severity and assign follow-up tickets.

Acceptance criteria:
- No new critical rendering regressions.
- All touched journeys complete on mobile and desktop.
- All task acceptance criteria verified or logged with blockers.

---

## 5) Handoff template (every agent must include)

Copy this into your PR description:

1. Task ID:  
2. Files changed:  
3. What changed (bullet list):  
4. What did not change (scope control):  
5. Validation performed (commands + manual paths):  
6. Remaining risks/edge cases:  
7. Screenshots (mobile + desktop):  
