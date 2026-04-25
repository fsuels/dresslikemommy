# 1688 Sourcing Scorecard — Phase 1

Purpose: shortlist reliable 1688 products before they enter the canonical Shopify listing workflow.

This is a browser-assisted sourcing gate. It does not publish to Shopify and it does not treat 1688 as a blind server-scraping target. Candidate data should come from a logged-in browser session, screenshots, copied page text, or a CSV filled by the operator/browser AI.

## What Gets Collected

Required for a useful card:

- `product_url`: 1688 product/detail URL
- `image_url`: product image URL shown on the search/detail page
- `title`: vendor product title
- `vendor_name`: supplier/shop/company name when visible

Strong scoring fields:

- `vendor_url`
- `vendor_location`
- `price_cny`
- `moq`
- `monthly_sales`
- `repurchase_rate_pct`
- `rating`
- `years_on_1688`
- `badges`: examples: `实力商家`, `超级工厂`, `深度验厂`, `真实工厂`, `买家保障`, `品质保障`
- `service_flags`: examples: `24小时发货`, `48小时发货`, `官方物流`, `现货`, `一件代发`, `15天包换`
- `dropship_supported`: `yes`, `no`, or blank
- `size_chart`: `yes`, `no`, or blank
- `category_match`: 0-5, where 5 means perfect Dress Like Mommy fit
- `style_fit`: 0-5, where 5 means premium/photo-ready for the catalog
- `image_quality`: 0-5
- `ip_risk_flags`: anything suspicious, e.g. Disney, Mickey, logo, cartoon character, branded print
- `raw_card_text`: copied visible card/page text for traceability
- `notes`

## Scoring

Total score: 100 points.

- Product fit: 25
  - category fit, style fit, photo quality, confirmed size chart
- Vendor reliability: 30
  - years on 1688, verified/assurance badges, repeat-buyer signal, rating, sales volume
- Fulfillment: 25
  - 24h/48h dispatch, ready stock, one-piece/dropship support, MOQ, official logistics
- Risk/readiness: 20
  - no obvious IP risk, buyer/quality protection, stock signal, data completeness

## Review Stages

- `search`: first-pass shortlist from visible 1688 search/category cards. Missing size chart, supplier years, and shop rating should keep a good lead at `Test`, not automatically bury it.
- `detail`: stricter verification after opening the product/supplier pages and filling in size chart, dropship, dispatch, and supplier evidence. Only this stage can produce `Gold`.

## Verdicts

- `Gold`: ready for listing intake after saving the size-chart screenshot and product images.
- `Test`: promising but missing evidence. Verify size chart, one-piece shipping, dispatch speed, or supplier support before listing.
- `Reject`: do not list unless evidence changes.

Hard reject signals:

- missing product URL
- no size chart evidence
- clear IP/brand/cartoon character risk
- poor category fit
- MOQ too high for dropshipping
- not one-piece/dropship friendly when MOQ is above 1

## Recommended Workflow

1. Open 1688 logged in.
2. Search the category, preferably using Chinese product terms or image search.
3. Use `ops/sourcing/1688-browser-collector.js` in the browser console, or ask the browser AI to fill `ops/sourcing/sample-candidates.csv` style fields.
4. Save the collected JSON or CSV under `ops/sourcing/<date>-<search>/candidates.json` or `candidates.csv`.
5. Run:

```bash
python3 ops/scripts/1688_sourcing_score.py \
  --input ops/sourcing/<date>-<search>/candidates.csv \
  --output-dir ops/sourcing/<date>-<search> \
  --stage search
```

6. Open `ops/sourcing/<date>-<search>/shortlist.html`.
7. Open the strongest `Test` cards, verify detail-page evidence, add the missing fields, and rerun with `--stage detail`.
8. For `Gold` cards, click `Copy listing request`, attach the size chart/product images, and run the canonical listing workflow from `ops/prompts/START-HERE.md`.

## Phase 1 Boundary

Phase 1 is intentionally semi-automated. It helps choose better vendors faster, but it does not automatically create products. Shopify creation remains handled by the existing listing runner after a candidate passes review.
