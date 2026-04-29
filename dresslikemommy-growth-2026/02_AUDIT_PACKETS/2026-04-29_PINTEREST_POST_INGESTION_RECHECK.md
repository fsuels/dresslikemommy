# Pinterest Post-Ingestion Recheck - 2026-04-29

Read-only recheck through the authenticated Chrome/CDP Pinterest session on Apr 28, 2026 around 10:41-11:03 PM EDT.

## Evidence

- Raw captures: `dresslikemommy-growth-2026/01_EXPORTS_RAW/PINTEREST/2026-04-29_post_ingestion_catalog_recheck/`
- Current Admin price readback: `ops/reports/pinterest-catalog-fix-2026-04-29-post-ingestion-recheck-current-admin-summary.json`
- Current Admin description readback: `ops/reports/pinterest-description-html-fix-2026-04-29-post-ingestion-recheck-current-admin-summary.json`
- Prior OOS reconciliation: `ops/reports/pinterest-out-of-stock-reconciliation-2026-04-29-summary.json`

## Completed Feed Recheck

Pinterest data source history confirmed two post-fix Shopify feeds completed:

| Feed | Data source ID | Latest ingestion | Successful | Failed | Warning total |
|---|---:|---:|---:|---:|---:|
| en | 3041760867124595727 | Apr 28 at 10:16 PM EDT | 5,969 | 0 | 61 |
| ar | 3041760849210539103 | Apr 28 at 10:18 PM EDT | 5,969 | 0 | 2,071 |

Source-specific diagnostics after completion:

| Feed | Warning 188 | Warning 1039 | Warning 126 | Notes |
|---|---:|---:|---:|---|
| en | 0 | 114 | 4 | Warning 188 disappeared; total warnings dropped from the prior 2,710 history row to 61. |
| ar | 2,010 | 114 | 4 | Warning 188 still appears in Pinterest diagnostics after the completed ingestion. |

The default diagnostics view still selected the Portuguese data source `3041760900274511922`, whose latest ingestion remained Apr 28 at 9:19 AM EDT, before the fixes. It should not be used as proof of post-fix results yet.

## Current Shopify Admin Cross-Check

- Price dry run found `0` remaining in-scope invalid compare-at changes for ACTIVE products published to Online Store + Pinterest.
- The same price scan found invalid compare-at rows only outside scope: `4,402` archived/unpublished variants.
- Description dry run found `0` in-scope ACTIVE Online Store + Pinterest products/translations over 10,000 characters.
- The Warning 126 source product had already been read back as fixed in Shopify: `backless-striped-jumpsuit` now has Shopify category `Apparel & Accessories > Clothing > One-Pieces` and feed override `Apparel & Accessories > Clothing > One-Pieces > Jumpsuits & Rompers`.

Interpretation: the English source reflects the Warning 188 fix. The Arabic source-specific diagnostics still look stale or channel-cached for Warning 188, because current Shopify Admin has no in-scope invalid compare-at rows left. Warning 1039 and Warning 126 did not drop yet in Pinterest diagnostics, but current Shopify Admin readbacks for the approved scope are clean.

## Distribution/OOS

Pinterest distribution diagnostics after the completed feed check still showed:

- Not approved: `309`
- Limited (ads only): `0`
- Approved: `97.18k`
- Products out of stock: `309`

Shopify-side reconciliation still shows the actionable inventory fact pattern:

- `32` true unavailable active-Pinterest variants with `inventoryPolicy=DENY` and `availableForSale=false`
- `65` zero-or-less inventory rows remain sellable because `inventoryPolicy=CONTINUE`
- `0` fully unavailable products
- `5` mixed products contain the unavailable variants

Decision: intentionally leave the `32` true OOS variants excluded from Pinterest distribution unless merchandising can actually restock those exact variants. Do not force inventory, do not switch them to continue-selling, and do not unpublish the whole mixed products from Pinterest just to chase the diagnostic count.

## Next Action

Recheck the next completed non-English feed, especially Arabic and Portuguese. If Arabic still reports Warning 188 after another completed post-fix ingestion, treat it as a Pinterest/Shopify channel cache or feed-profile support issue rather than a Shopify product-data bug. If Warning 1039/126 persist after another post-fix ingestion, export issue details from Pinterest and decide whether to clean archived/unpublished legacy products globally or keep them out of paid scope.
