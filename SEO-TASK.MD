# SEO Multi-Agent Execution Playbook (Shopify Theme)

This repository is a **Shopify Liquid theme** (not Next.js).  
All agents must follow this file exactly so tasks can run in parallel safely.

## 0) Mission
Ship SEO fixes from the audited backlog with minimal merge conflicts, clear ownership, and fast validation.

## 1) Mandatory Rules For Every Agent
1. Take exactly **one** task ID.
2. Edit only files listed in that task’s "Allowed files".
3. Do not touch unrelated existing local changes.
4. Keep changes surgical. No refactors outside task scope.
5. Add a short entry to `ops/AGENT_WORKLOG.md` when done.
6. Return: summary, changed files, verification output, and diff.

## 2) Recommended Parallel Workflow
Use a separate git worktree per task.

```bash
# from repo root
mkdir -p ../seo-worktrees

# example for task TSEO-001
git worktree add ../seo-worktrees/tseo-001 -b seo/tseo-001 main
cd ../seo-worktrees/tseo-001
```

If worktrees are not available, run tasks sequentially.

## 3) Delivery Contract (every agent)
Each agent must return:
1. What changed (3-8 bullets)
2. Exact file list
3. Verification commands run + result
4. Risks / follow-up notes
5. Unified diff

## 4) File Lock Map (conflict prevention)
- `sections/main-404.liquid` -> TSEO-001 only
- `snippets/jsonld-seo.liquid` -> TSEO-002 only
- `snippets/meta-tags.liquid` -> TSEO-003, TSEO-005, TSEO-012 (SEQUENTIAL)
- `templates/gift_card.liquid` -> TSEO-003 only
- `sections/main-list-collections.liquid` -> TSEO-004 (and optionally TSEO-010) (SEQUENTIAL)
- `layout/theme.liquid` -> TSEO-006, TSEO-008, TSEO-012 (SEQUENTIAL)
- `snippets/card-product.liquid` + product-card parent sections -> TSEO-007 only
- `snippets/breadcrumbs.liquid` -> TSEO-009 only
- `snippets/card-collection.liquid` + collection-list callers -> TSEO-010
- `sections/main-collection-banner.liquid` -> TSEO-011 only
- `sections/main-article.liquid` -> TSEO-012 only

## 5) Parallel Execution Plan

### Wave A (safe parallel now)
- TSEO-001
- TSEO-002
- TSEO-004
- TSEO-009
- TSEO-011

### Wave B (parallel after Wave A)
- TSEO-007
- TSEO-010 (only after TSEO-004 if it needs `main-list-collections.liquid`)
- TSEO-006

### Wave C (must be sequential due shared files)
1. TSEO-003
2. TSEO-005
3. TSEO-012
4. TSEO-008 (data-gated, and touches `layout/theme.liquid`)

## 6) Task Cards

---

## TASK TSEO-001 — Remove 404 Homepage Redirect
**Priority:** Critical  
**Goal:** Keep true 404 behavior; remove soft-404 redirect.

**Allowed files:**
- `sections/main-404.liquid`
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. Open `sections/main-404.liquid`.
2. Remove the `<script>` block that calls `window.location.replace('/')`.
3. Keep existing 404 content and CTA links.
4. Do not add any redirect/meta refresh.

**Verification:**
```bash
rg -n "window\.location\.replace\('/'\)" sections/main-404.liquid
```
Expected: no matches.

**Parallel status:**
- Can run with: TSEO-002, TSEO-004, TSEO-009, TSEO-011, TSEO-007, TSEO-006
- Cannot run with: none (file-isolated)

**Done output must include:**
- Confirmation redirect code is removed
- Diff for `sections/main-404.liquid`

---

## TASK TSEO-002 — Fix Product/Breadcrumb JSON-LD URL Composition
**Priority:** Critical  
**Goal:** Prevent duplicated product paths in schema URLs.

**Allowed files:**
- `snippets/jsonld-seo.liquid`
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. Find assignments using `canonical_url | default: shop.url | append: product.url`.
2. Replace with safe logic:
   - If `canonical_url` is present, use it directly.
   - Else use `shop.url` + `product.url`.
3. Apply same fix to both `product_breadcrumb_url` and `product_url`.
4. Keep schema structure unchanged.

**Verification:**
```bash
rg -n "canonical_url \| default: shop.url \| append: product.url" snippets/jsonld-seo.liquid
```
Expected: no matches.

**Parallel status:**
- Can run with: all tasks except none (file-isolated)
- Cannot run with: none

**Done output must include:**
- Final URL logic snippet
- Diff for `snippets/jsonld-seo.liquid`

---

## TASK TSEO-003 — Expand Noindex Coverage For Private Routes
**Priority:** Critical  
**Goal:** Ensure private/auth/password/gift-card routes are noindexed.

**Allowed files:**
- `snippets/meta-tags.liquid`
- `templates/gift_card.liquid`
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. In `snippets/meta-tags.liquid`, expand `should_noindex` rules to include:
   - password pages
   - customer/account templates
2. Keep current noindex rules for search/cart/404.
3. In `templates/gift_card.liquid`, add explicit robots noindex tag in `<head>`.
4. Do not noindex product/collection/home/blog/article/page routes.

**Implementation hint:**
- Customer route detection can use `template` checks (e.g., contains `customers`) if `request.page_type` is inconsistent.

**Verification:**
```bash
rg -n "should_noindex|robots" snippets/meta-tags.liquid templates/gift_card.liquid
```

**Parallel status:**
- Can run with: Wave A tasks, TSEO-006, TSEO-007, TSEO-009, TSEO-010, TSEO-011
- Cannot run with: TSEO-005, TSEO-012 (shared `snippets/meta-tags.liquid`)

**Done output must include:**
- Exact noindex conditions added
- Diff for both files

---

## TASK TSEO-004 — Repair `main-list-collections` Syntax/Structure
**Priority:** High  
**Goal:** Remove Liquid/HTML syntax errors and keep list-collections page renderable.

**Allowed files:**
- `sections/main-list-collections.liquid`
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. Fix broken Liquid flow around sorting logic and closing tags.
2. Ensure valid structure:
   - page wrapper
   - sorting/pagination logic
   - collection list loop
   - pagination render
3. Preserve existing settings schema and sort options.
4. Prefer Dawn-consistent structure if uncertain.

**Verification:**
```bash
shopify theme check --fail-level error --output text > /tmp/themecheck.txt || true
rg -n "main-list-collections\.liquid|\[error\]" /tmp/themecheck.txt
```
Expected: no syntax error for `main-list-collections.liquid`.

**Parallel status:**
- Can run with: TSEO-001, TSEO-002, TSEO-009, TSEO-011, TSEO-007, TSEO-006
- Cannot run with: TSEO-010 if TSEO-010 edits `main-list-collections.liquid`

**Done output must include:**
- Confirmation that syntax error is gone
- Diff for `sections/main-list-collections.liquid`

---

## TASK TSEO-005 — Implement Faceted/Tagged URL Indexation Policy
**Priority:** High  
**Goal:** Prevent index bloat from filter/sort/tag variants.

**Allowed files:**
- `snippets/meta-tags.liquid`
- (optional) `layout/theme.liquid` only if absolutely needed
- `ops/AGENT_WORKLOG.md`

**Default policy to implement (unless owner overrides):**
1. Keep indexable:
   - Base collection URLs
   - Collection pagination URLs where only `page` is present
2. Noindex:
   - Collection tag URLs (`current_tags`)
   - Collection URLs with filter params (`filter.`)
   - Collection URLs with sorting params (`sort_by=`)

**Steps:**
1. Add collection-specific logic in `meta-tags`.
2. Compute `should_noindex` for filter/sort/tag states.
3. Avoid changing behavior for search/cart/404/private noindex logic.
4. Keep implementation readable and comment the policy.

**Verification:**
```bash
rg -n "current_tags|filter\.|sort_by|should_noindex" snippets/meta-tags.liquid
```

**Parallel status:**
- Can run with: TSEO-001, TSEO-002, TSEO-004, TSEO-006, TSEO-007, TSEO-009, TSEO-010, TSEO-011
- Cannot run with: TSEO-003, TSEO-012 (shared `snippets/meta-tags.liquid`)

**Done output must include:**
- Final policy logic and examples of URLs affected
- Diff for touched files

---

## TASK TSEO-006 — Reduce Head Inline CSS Payload
**Priority:** High  
**Goal:** Reduce HTML/CSS inline weight while preserving layout.

**Allowed files:**
- `layout/theme.liquid`
- `assets/*` (new/extracted CSS files)
- `ops/AGENT_WORKLOG.md`

**Important scope guard:**
- Focus on extracting **static** inline CSS from `layout/theme.liquid`.
- Do not change dynamic Liquid-dependent styles unless necessary.

**Steps:**
1. Identify long static style blocks in `layout/theme.liquid`.
2. Move them to one or more asset CSS files (e.g., `assets/theme-inline-extracted.css`).
3. Include extracted CSS via `stylesheet_tag` in `layout/theme.liquid`.
4. Keep minimal critical inline CSS only.
5. Verify no visual selector breakage.

**Verification:**
```bash
rg -n "<style>|</style>" layout/theme.liquid
ls -1 assets | rg "theme-inline-extracted|theme-.*overrides"
```

**Parallel status:**
- Can run with: TSEO-001, TSEO-002, TSEO-003, TSEO-004, TSEO-005, TSEO-007, TSEO-009, TSEO-010, TSEO-011
- Cannot run with: TSEO-008, TSEO-012 (shared `layout/theme.liquid`)

**Done output must include:**
- Estimated before/after reduction (line count or bytes)
- Diff for `layout/theme.liquid` + new assets

---

## TASK TSEO-007 — Remove Per-Card Stylesheet Duplication (`card-product`)
**Priority:** High  
**Goal:** Load shared CSS once per section/page, not once per card render.

**Allowed files:**
- `snippets/card-product.liquid`
- `sections/main-collection-product-grid.liquid`
- `sections/main-search.liquid`
- `sections/featured-collection.liquid`
- `sections/related-products.liquid`
- (optional) other direct parent sections that render `card-product`
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. Remove CSS includes from top of `snippets/card-product.liquid`.
2. Add needed CSS includes in parent sections (once per page/section), conditionally when possible.
3. Ensure features still work:
   - price/rating styles
   - quick add / quantity popover paths where enabled
4. Avoid editing `sections/main-product.liquid` unless strictly necessary (conflict reduction).

**Verification:**
```bash
rg -n "component-rating\.css|component-volume-pricing\.css|quick-order-list\.css|quantity-popover\.css" snippets/card-product.liquid
rg -n "component-rating\.css|quick-order-list\.css|quantity-popover\.css" sections/main-collection-product-grid.liquid sections/main-search.liquid sections/featured-collection.liquid sections/related-products.liquid
```
Expected: no such includes in `card-product`, present appropriately in parent sections.

**Parallel status:**
- Can run with: TSEO-001, TSEO-002, TSEO-003, TSEO-004, TSEO-005, TSEO-006, TSEO-009, TSEO-011
- Cannot run with: avoid overlap with TSEO-010 if both edit same section file

**Done output must include:**
- List of parent sections updated
- Diff for all touched files

---

## TASK TSEO-008 — Hreflang Head Implementation (Data-Gated)
**Priority:** Medium  
**Goal:** Ensure correct `<link rel="alternate" hreflang>` tags if missing.

**Allowed files:**
- `layout/theme.liquid`
- (optional) new snippet like `snippets/hreflang-tags.liquid`
- `ops/AGENT_WORKLOG.md`

**NEEDS_DATA (required before final implementation):**
1. Actual published locale URL structure (subfolder/domain/market)
2. List of enabled storefront locales
3. Sample rendered head from live/preview storefront

**Steps:**
1. First verify whether Shopify/platform already emits correct alternates.
2. If missing/incomplete, add deterministic hreflang output for all enabled locales plus self and `x-default`.
3. Keep locale URLs canonical and consistent.
4. If data unavailable, stop and return a blocker report only.

**Verification:**
- Requires rendered HTML inspection on live/preview locale URLs.

**Parallel status:**
- Can run with: file-isolated tasks not touching `layout/theme.liquid`
- Cannot run with: TSEO-006, TSEO-012 (shared `layout/theme.liquid`)

**Done output must include:**
- Either implemented hreflang diff, or explicit blocker report listing missing data

---

## TASK TSEO-009 — Validate Product Breadcrumb Collection Links
**Priority:** Medium  
**Goal:** Avoid breadcrumb links pointing to non-existent collections.

**Allowed files:**
- `snippets/breadcrumbs.liquid`
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. For each breadcrumb handle (category1/subcategory/subcategory2), resolve with `collections[handle]`.
2. Render clickable link only when target collection exists (and optionally has products).
3. Render plain text label when target does not exist.
4. Keep separators, labels, and accessibility attributes.
5. Replace hardcoded home path `/` with `routes.root_url` where practical.

**Verification:**
```bash
rg -n "collections\[|routes\.root_url|/collections/" snippets/breadcrumbs.liquid
```

**Parallel status:**
- Can run with: all tasks except none (file-isolated)
- Cannot run with: none

**Done output must include:**
- Example before/after breadcrumb behavior for missing collection handle
- Diff for `snippets/breadcrumbs.liquid`

---

## TASK TSEO-010 — Improve Collection Card LCP Loading Strategy
**Priority:** Medium  
**Goal:** Stop lazy-loading above-the-fold collection cards.

**Allowed files:**
- `snippets/card-collection.liquid`
- `sections/collection-list.liquid`
- `sections/main-list-collections.liquid` (only if not locked by TSEO-004)
- (optional) `snippets/cart-drawer.liquid` if needed for explicit lazy behavior
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. Add optional snippet parameter (e.g., `lazy_load`) to `card-collection` with default `true`.
2. Use `loading="eager"` (and optional `fetchpriority="high"`) for first visible cards in homepage collection-list section.
3. Keep `loading="lazy"` for non-critical cards.
4. If `main-list-collections.liquid` is locked by TSEO-004, skip that caller and document it.

**Verification:**
```bash
rg -n "loading=\"(lazy|eager)\"|fetchpriority" snippets/card-collection.liquid sections/collection-list.liquid sections/main-list-collections.liquid 2>/dev/null || true
```

**Parallel status:**
- Can run with: most tasks
- Cannot run with: TSEO-004 if both need `sections/main-list-collections.liquid`

**Done output must include:**
- Which callers now pass eager for first viewport items
- Diff for touched files

---

## TASK TSEO-011 — Re-enable Collection Intro Content On Suppressed Handles
**Priority:** Medium  
**Goal:** Restore top-of-page descriptive content for key collection handles.

**Allowed files:**
- `sections/main-collection-banner.liquid`
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. Remove or replace logic that suppresses description for:
   - `new-women-outfits`
   - `family-matching-outfits`
2. Keep existing behavior for all other collections.
3. Do not alter collection title logic.

**Verification:**
```bash
rg -n "new-women-outfits|family-matching-outfits|collection-hero__description" sections/main-collection-banner.liquid
```

**Parallel status:**
- Can run with: all tasks except none (file-isolated)
- Cannot run with: none

**Done output must include:**
- Final logic for those two handles
- Diff for `sections/main-collection-banner.liquid`

---

## TASK TSEO-012 — Metadata Hygiene Cleanup
**Priority:** Low  
**Goal:** Normalize metadata protocol and placeholder values.

**Allowed files:**
- `sections/main-article.liquid`
- `snippets/meta-tags.liquid`
- `layout/theme.liquid`
- `ops/AGENT_WORKLOG.md`

**Steps:**
1. In `main-article.liquid`, change schema context to `https://schema.org`.
2. In `meta-tags.liquid`, change `og:image` protocol to `https:` for consistency.
3. In `layout/theme.liquid`, replace placeholder author content with store-derived value (e.g., `{{ shop.name | escape }}`).
4. Keep all output escaped and valid.

**Verification:**
```bash
rg -n "http://schema\.org|og:image\" content=\"http:|Your Store Name" sections/main-article.liquid snippets/meta-tags.liquid layout/theme.liquid
```
Expected: no matches.

**Parallel status:**
- Can run with: file-isolated tasks only
- Cannot run with: TSEO-003, TSEO-005 (`meta-tags`), TSEO-006, TSEO-008 (`layout/theme`)

**Done output must include:**
- Final metadata values
- Diff for touched files

---

## 7) Final Integration Order (recommended)
1. Merge Wave A task branches.
2. Merge Wave B task branches.
3. Merge Wave C sequentially in this exact order: TSEO-003 -> TSEO-005 -> TSEO-012 -> TSEO-008.
4. Resolve conflicts only in locked files listed above.
5. Run final smoke checks on:
   - Home
   - Collection page with filters
   - Product page
   - Blog article
   - 404 page
   - Account/login route
   - Password route
   - Gift card route

## 8) Worklog Entry Template (mandatory)
Append this to `ops/AGENT_WORKLOG.md`:

```md
Task: TSEO-XXX
Date: YYYY-MM-DD
AGENT_CONTINUITY_ANCHOR: YYYY-MM-DD-tseo-xxx
Changes:
- ...
Verification:
- ...
Open items:
- ...
```

