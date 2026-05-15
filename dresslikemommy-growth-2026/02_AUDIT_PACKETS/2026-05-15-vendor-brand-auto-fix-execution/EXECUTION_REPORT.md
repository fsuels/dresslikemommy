# Vendor / Brand Auto-Fix — Execution Report

Date: 2026-05-15
Operator: Claude current session
Store: Dress Like Mommy (`www.dresslikemommy.com`)
Merchant Center account: `124884876`

## Owner approval phrase (received in current session)

> I approve, in this session, against Merchant Center account 124884876 and the Dress Like Mommy Shopify store: (a) bulk Shopify Admin productUpdate setting vendor = "Dress Like Mommy" on every active product where it is not already that exact value, (b) creation of a Shopify Flow workflow triggered on Product created, Product updated, and Product duplicated that sets vendor = "Dress Like Mommy" whenever vendor is not already that value, and (c) creation of Merchant Center feed rules on the Shopify Google & YouTube source feed: Rule A force brand = "Dress Like Mommy" for all rows, Rule B matching-set gender/age split as specified, and Rule C identifier_exists = no for all rows. No other Shopify product, feed, source, billing, status, budget, bid, conversion, Pinterest, or Google Ads mutation is authorized.

## Action (a) — Bulk Shopify Admin `productUpdate` — DONE LIVE

- Search query used: `status:active AND NOT vendor:"Dress Like Mommy"`
- Candidates collected via Admin API: **287 products**
- Mutations executed via Shopify Admin GraphQL `productUpdate`: **287**
- userErrors: **0**
- Transient connector retries: **1** (one product re-issued successfully)
- After-state re-query (identical filter): **0 products returned**. Catalog is now 100% `vendor = "Dress Like Mommy"`.

The repo-side script that performed the same logic (idempotent, re-runnable) is at:

- `ops/scripts/apply_vendor_backfill.py`

It can be re-run at any time to assert compliance; on a compliant store it finds zero targets.

## Action (b) — Shopify Flow auto-vendor workflow — FILE DELIVERED

The workflow file is `auto-vendor-dress-like-mommy.flow` in this folder. Owner imports it once. See `APPLY_ME.md` for click-by-click steps.

Why this part needs an owner click: there is no Shopify Admin GraphQL mutation that creates a Flow workflow programmatically; Flow workflows are created either through the Flow UI or via the Flow import feature. The `.flow` file is the import-ready artifact.

## Action (c) — Merchant Center feed rules A + B + C — SPECS DELIVERED

The exact rule definitions (rule name, condition, action) are in `MERCHANT_CENTER_FEED_RULES.md` in this folder. Owner applies them once on MC account `124884876` against the **Shopify Google & YouTube** primary source feed.

Why this part needs an owner click: no Merchant Center API is connected to this session. The rule specs are precise enough to paste into MC's feed-rule editor directly.

## Verification

- Live Shopify Admin re-query (this session): `0` non-compliant products.
- Automation read-only verifier, 2026-05-15 10:18 EDT: `326` active products checked, `0` non-compliant products, verdict `PASS`.
- Re-runnable verification: `python3.13 ops/scripts/verify_vendor_compliance.py`
- Latest verifier output: `vendor_compliance_report.json`.
- Future Merchant Center after-state readback: pending Rule A apply; expect `brand = Dress Like Mommy` on every offer row.

## Compliance

- Per `CLAUDE.md`: no supplier/source URLs were written to any repo file, worklog, or evidence file. Pre-mutation vendor classes were recorded as `URL_SUPPLIER_REDACTED` or `LOWERCASE_DOMAIN`.
- Per `CLAUDE.md`: only the named scope (product `vendor` field) was touched. No title, description, price, image, tag, SEO, metafield, status, or other product field was modified.
- Per `CLAUDE.md`: write lane was claimed in `ops/AGENT_COORDINATION.md` before any mutation.
- Continuity integrity check is to be run before closing the session: `python3.13 ops/scripts/check_continuity_integrity.py --strict`.

## Files in this packet

| File | Purpose |
|---|---|
| `EXECUTION_REPORT.md` | This document. |
| `APPLY_ME.md` | Owner action checklist for (b) and (c). |
| `auto-vendor-dress-like-mommy.flow` | Shopify Flow workflow import file for (b). |
| `MERCHANT_CENTER_FEED_RULES.md` | Exact rule specs for (c). |
| `vendor_compliance_report.json` | Read-only Shopify Admin verification output from `ops/scripts/verify_vendor_compliance.py`. |
