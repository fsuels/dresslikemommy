# Merchant Post-Shopify Region Prune Readback

Generated: 2026-05-15T07:14:39

Mode: read-only Merchant Center browser-RPC export analysis after the bounded
Shopify Markets `International` region prune. No Merchant upload/source sync,
Google Ads campaign/product-group/bid/budget/status/conversion change, Shopify
product edit, Pinterest change, billing change, or credential change occurred.

## Shopify Action Already Executed

- `International` market regions before prune: `73`.
- `International` market regions after prune: `21`.
- Removed first-pass non-priority regions: `52`.
- Protected duplicate `CA` and `AU` remained inside `International`.
- Separate active markets remained present: `us`, `canada`, `united-kingdom`,
  `eu`, `australia`, and `international`.

## Fresh Merchant Re-Export Result

| Gate | Rows |
|---|---:|
| USA English (`US|en|USD`) | `5491` |
| USA Spanish (`US|es|USD`) | `5412` |
| Canada English (`CA|en|CAD`) | `0` |
| Canada French (`CA|fr|CAD`) | `0` |
| GB English (`GB|en|GBP`) | `0` |
| Remaining first-pass removal rows | `199684` |

## Decision

`shopping_build_gate_passed=false`.

The Shopping build remains blocked because the fresh Merchant export still has
`0` Canada English rows, `0` Canada French rows, and `0` GB English rows, while
the first-pass non-priority Merchant row groups still remain in the product-list
export. The Shopify Markets cleanup succeeded, but Merchant/Google product
generation has not yet propagated or still needs a Google & YouTube publishing
sync/control action. Do not build Shopping from absent rows.

## Files

- `merchant_post_prune_priority_market_readback_summary.json`
- `../2026-05-15-merchant-post-shopify-region-prune-export/merchant_source_eligibility_browser_rpc_summary.json`
- `../2026-05-15-merchant-post-shopify-region-prune-export/merchant_ca_en_eligibility.csv`
- `../2026-05-15-merchant-post-shopify-region-prune-export/merchant_ca_fr_eligibility.csv`
- `../2026-05-15-merchant-post-shopify-region-prune-export/merchant_gb_en_eligibility.csv`
