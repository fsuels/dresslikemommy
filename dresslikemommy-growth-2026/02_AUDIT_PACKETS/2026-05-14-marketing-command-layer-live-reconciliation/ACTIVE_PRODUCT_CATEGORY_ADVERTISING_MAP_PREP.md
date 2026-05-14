# Active Product Category Advertising Map Prep

Timestamp: 2026-05-14 06:05 EDT

Scope: public storefront/catalog readbacks plus existing paid-cohort artifact. No external writes.

## Owner Directive Captured

- Advertise only active, public, purchasable products.
- Never expose supplier/source URLs to shoppers, analytics attributes, feed-visible data, ad copy, or customer-facing copy.
- Build category/event strategy from real shopper intent, not generic product dumps.
- For Father's Day, bias toward Daddy-and-Me, father-inclusive family matching, and broad family matching products.

## Current Readbacks Used

- Public storefront products endpoint: `326` products across pages `1-2` (`250` + `76`; page `3` returned `0`).
- Public storefront collections endpoint: `45` collections.
- Existing local channel-publication audit: `321` active products in `ops/channel-publication-audit-active-products.json`.
- Existing Standard Shopping paid cohort: `780` variant rows across `81` product handles in `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-google-shopping-campaign-gate/paid_cohort_exact_780_rows.csv`.

Public product readback hit rate limiting after the first pages, so this is a prep map, not a replacement for a full Admin/Merchant export.

## Paid-Cohort Shape

From the existing `780`-row paid cohort:

| Slice | Count |
|---|---:|
| Product handles | `81` |
| Variant rows | `780` |
| `swimsuits` | `345` |
| `mommy_me` | `214` |
| `family_matching` | `103` |
| `daddy_me` | `89` |
| `pajamas` | `29` |
| `mother` role rows | `429` |
| `child` role rows | `227` |
| `father` role rows | `89` |
| `summer` label rows | `605` |
| `year-round` label rows | `155` |
| `holiday` label rows | `20` |

## Immediate Category Strategy

### Father's Day / Dad Intent

Use Daddy-and-Me plus father-inclusive family matching only. Do not route Father's Day traffic to generic mommy-only, Christmas, stale holiday, or supplier-leaking URLs.

Existing paid-cohort father/daddy candidate handles found: `19`.

Sample candidates:

- `dynamic-duo-father-and-son-matching-swim-trunks-family-beachwear-set`
- `father-and-son-matching-swim-trunks-bold-cow-print-family-beachwear`
- `father-and-son-matching-swim-trunks-classic-paisley-pattern-in-blue-and-yellow`
- `father-and-son-matching-swim-trunks-elegant-blue-and-white-paisley-design-quick-dry-beachwear`
- `father-and-son-matching-swim-trunks-tropical-floral-print-family-swimwear`
- `green-tropical-leaf-daddy-and-me-matching-swim-shorts-for-pool-days`
- `matching-dad-and-son-green-stripe-swim-trunks-beach-shorts`
- `matching-dad-and-son-pink-black-color-block-swim-shorts`
- `matching-family-yellow-beach-outfits-summer-vacation-dresses-shorts-set`
- `tropical-matching-family-beach-outfits-colorful-leaf-print-summer-dresses-shorts-set`

Collection intent:

- `/collections/daddy-me`
- `/collections/daddy-me-shirts`
- `/collections/daddy-me-t-shirts`
- `/collections/daddy-and-me`
- `/collections/family-sets`
- `/collections/family-tops`
- `/collections/new-women-outfits`
- `/collections/matching-outfits`

### Summer / Vacation / Beach

Prioritize currently active summer, swim, vacation, beach, Hawaiian, resort, and light family-set products after source-leak readback passes.

Exclude or hold:

- Stale Christmas/holiday products during summer unless intentionally used for remarketing/seasonal preorder under a separate plan.
- Any URL with stale metadata, supplier/source-domain leakage, broken add-to-cart, unavailable variants, or unresolved shipping clarity.

### Broad Always-On

Use only products that pass:

- active/public/purchasable storefront readback,
- clean source/DOM supplier-domain readback,
- role/size/variant usability,
- correct shipping-country presentment for target market,
- Merchant/feed eligibility or exact exclusion rationale,
- margin and AOV sanity.

## Next Read-Only Upgrade

Build the full advertising matrix by intersecting:

1. current Shopify active/public products,
2. Online Store publication,
3. Google & YouTube publication / Merchant eligibility,
4. Pinterest catalog eligibility,
5. category/occasion tags,
6. margin/AOV labels,
7. clean landing source/DOM readbacks,
8. current season/event intent.

No campaign upload, feed upload, product-group change, or budget/bid/status change is allowed until the exact row has fresh approval and before/after readbacks.
