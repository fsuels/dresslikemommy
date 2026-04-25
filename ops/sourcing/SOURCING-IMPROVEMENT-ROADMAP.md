# 1688 Sourcing Improvement Roadmap

This roadmap captures the agreed audit findings for the Dress Like Mommy sourcing app.

## Current Truth

- The dashboard is useful as a local review surface, but search-card data alone is not enough to find best vendors.
- Search-stage candidates are `Unverified Leads`, not winners.
- `Best Lead` / internal `Gold` must require detail-page proof.
- CAPTCHA/login must be handled manually in the helper browser. Do not bypass 1688 protections.

## Phase 1 - Detail Proof Gate

Implemented direction:

- Use `ops/scripts/1688_sourcing_detail_enrich.py` to open a shortlisted 1688 product page through the logged-in helper browser.
- Extract supplier, dropship, dispatch, size chart, availability, risk, sales/repeat clues, and product image evidence.
- Save vendor images to `ops/sourcing/vendor-images/<offer-id>/`.
- Save detail artifacts to `ops/sourcing/detail-enrichment/<offer-id>/`.
- Rescore with `--stage detail`.
- Block `Gold` if supplier proof, size chart, dropship/one-piece proof, dispatch/stock proof, or usable vendor images are missing.
- Update `ops/sourcing/state/decisions.json` with detail proof fields.
- Track supplier memory in `ops/sourcing/state/vendors.json`.

## Phase 2 - Vendor Database

Next implementation target:

- Expand `ops/sourcing/state/vendors.json` into supplier memory used by collection, scoring, and dashboard.
- Track vendor name, shop URL, shop ID when known, location, years, badges, service flags, rating, accepted offers, rejected offers, categories, last seen date, and risk notes.
- Penalize products from known weak/rejected suppliers.
- Boost products from suppliers with proven fulfillment and repeated accepted offers.

## Phase 3 - Search History

Add `ops/sourcing/state/search-history.json`:

- Track category, query, page URL, search date, offer IDs seen, reviewable offers, rejected offers, and blocked CAPTCHA/login events.
- Prevent repeated searches from showing the same already-seen products.
- Record blocked runs as blocked, not empty successful searches.

## Phase 4 - Category Tuning

Tune categories separately:

- Mommy & Me: preserve strong mother-daughter/family dress terms.
- Daddy & Me: focus father-son/father-daughter shirts, polos, pajamas, swim/resort sets.
- Family Matching: require multiple family-role signals or clear adult/child matching pieces.
- Couples: avoid generic men/women clothing; require coordinated adult couple terms.
- Maternity: add pregnancy, nursing, postpartum, bump-friendly, baby-shower, and mommy-baby terms.

Category queries should support metadata later:

```json
{
  "text": "父子装 夏季 衬衫 一件代发",
  "intent": "father-son vacation shirts",
  "priority": 1,
  "min_reviewable_target": 3
}
```

## Phase 5 - Business Scoring

Add business fields to the candidate model:

- landed cost estimate
- estimated USD cost
- target Shopify price
- gross margin estimate
- variant complexity
- seasonality
- assortment fit
- risk of confusing size chart or excessive variants

Missing critical business data should reduce confidence, not create a fake high score.

## Phase 6 - Image Quality

Add image-quality analysis after vendor images are downloaded:

- image count
- usable image count
- low-resolution detection
- collage/contact-sheet detection
- watermark/logo/brand risk
- product-only/detail/fit image availability

Feed the result back into detail scoring and dashboard proof.

## Phase 7 - Safer Draft Pipeline

- Keep `Draft Package` blocked until required proof exists.
- Require generated Shopify images before a product is considered ready for Shopify draft creation.
- Continue creating Shopify products as drafts only until the operator explicitly asks to publish.
