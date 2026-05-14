# Automation Capability And Merchant Capacity Diagnosis

Generated: 2026-05-14 10:38 EDT

Mode: repo-local plus read-only tool capability checks. No Google Ads, Merchant, Pinterest, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme writes were made.

## Capability Inventory

| Capability | Result | Notes |
|---|---|---|
| Shell | `USABLE` | Repo commands, scripts, and validators run normally. |
| Repo writes | `USABLE` | Create/remove write test in repo passed. |
| Network | `USABLE` | Direct outbound fetch returned `200` from `https://example.com`. |
| Browser / Playwright MCP | `USABLE` | Playwright MCP opened a fresh tab and loaded `https://example.com`. |
| Shell-side Playwright | `UNAVAILABLE` | `playwright` package is not installed for local `node` or `python3.13`. |
| Chrome DevTools MCP | `VISIBLE_BUT_UNUSABLE` | Tool is visible, but the profile is already locked by another running browser instance, so no new authenticated readback page could be opened in this runtime. |
| Computer Use | `VISIBLE_BUT_UNUSABLE` | `list_apps` worked, but `get_app_state` returned `Computer Use permissions are not granted`. |
| GitHub app / MCP | `USABLE` | GitHub tool discovery succeeded; no GitHub write was needed for this lane. |
| OpenAI docs MCP | `USABLE` | Search returned current Codex docs successfully. |

Decision: `AUTOMATION_CAPABILITY_MISMATCH` applies to authenticated Chrome/account-surface readbacks needed for Merchant/Pinterest follow-up in this run. The missing practical capability is authenticated browser/account inspection through a usable Chrome DevTools or Computer Use path. Continue safe repo-local/read-only lanes; do not claim manual-session parity for those account surfaces.

## Merchant Shopping Capacity Read-Only Diagnosis

### Fresh evidence

- Merchant prioritized fixes page text shows `Over capacity for Shopping ads (outside of CSS program)`.
- Affected count on the visible page: `73.3K products (21%)`.
- Page timestamp on the visible page: `Last updated at 3:09 AM May 14, 2026`.
- Current live US Standard Shopping campaign `23802638621` still served `17` impressions on `2026-05-13`.
- Current visible product groups remain tightly scoped:
  - `All products > us_test_ready`
  - child groups `daddy_me`, `family_matching`, `mommy_me`, `pajamas`, `swimsuits`
  - `Everything else in "All products"` remains `Excluded`
- Existing paid cohort remains `780` rows / `81` products, all with `custom_label_4=us_test_ready` and `custom_label_0=paid_eligible`.

### What this proves

- The capacity warning is real and current at the account level.
- It is not yet proven to block the active paid cohort or the current Standard Shopping campaign.
- Standard Shopping is not in a total-serve outage, because yesterday still showed `17` impressions.

### What this does not prove

- It does not prove whether any `us_test_ready` / `paid_eligible` products are inside the `73.3K` affected set.
- It does not prove whether the warning is reducing impressions for current paid products versus being broad account/catalog noise.
- It does not justify removing products, changing source/feed scope, changing Shopping product groups, or requesting capacity.

### Next exact unblock

Run an authenticated read-only Merchant Center product-level intersection check in account `124884876`:

1. Open the current capacity warning product list.
2. Filter or sample against the active paid cohort identifiers.
3. Confirm whether current `us_test_ready` / `paid_eligible` products are affected.
4. Save before-state evidence.

Preferred evidence to intersect:

- current paid cohort item IDs from `paid_cohort_exact_780_rows.csv`
- current Standard Shopping scope from the product-group readback
- current Merchant capacity product list or export, but only if the download is proven fresh

## Guardrails Preserved

- No Merchant product removals.
- No Merchant source/feed edits.
- No capacity request.
- No Google Ads Shopping product-group, scope, status, bid, or budget change.
- No Shopify product/theme/Admin change.

## Evidence

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/merchant-product-issues-export/raw/product-issues-browser-export/diagnostics_page_text_before_download_priority.txt`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-14-marketing-command-layer-live-reconciliation/standard-shopping-readback/raw/01_productgroups_initial.txt`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv`
