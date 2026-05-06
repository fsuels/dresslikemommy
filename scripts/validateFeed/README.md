# validateFeed

Nightly validator that fails fast on Merchant Center feed problems before MC ever sees them. Catches the two issue classes that have been hitting us — missing image links and unreachable landing pages — and buckets results by category so the daily fix queue is already triaged.

## What it does

1. Reads a Shopify product export (`{ products: [...] }` shape from Admin REST `/products.json`, or any equivalent JSON).
2. Flattens it to one feed item per `(product, variant)` and derives the GMC attributes that MC actually consumes (`link`, `image_link`, `color`, `size`, `availability`, `price`).
3. Validates required attributes are populated and that `link` and `image_link` return 2xx/3xx.
4. Tags each item with one or more category buckets (MOMMY, DADDY_ME, FAMILY_MATCHING, PAJAMAS, SWIMSUITS, UNCATEGORIZED) using the regex map in `categories.js`.
5. Writes one folder per bucket containing `valid.jsonl` (good items, ready for downstream feed build) and `errors.csv` (failing items with the offending field, status, and URL).

Default failure mode is **alert + exclude**: failing items are written to `errors.csv` and dropped from `valid.jsonl`, valid items still ship. Pass `--strict` to make the process exit non-zero whenever any item has errors.

## Local run

```bash
cd scripts/validateFeed
npm install

# Smoke-test against the repo fixture
npm run smoke

# Or against any Shopify export
node validateFeed.js --input /path/to/products.json --out ./reports
```

Reports land in `./reports/<BUCKET>/{valid.jsonl,errors.csv}` and `./reports/summary.json`.

## CLI flags

| Flag | Default | Notes |
| --- | --- | --- |
| `--input <path \| ->` | required | Shopify export JSON. `-` reads stdin. |
| `--out <dir>` | `./reports` | Output directory. Created if missing. |
| `--store-domain <host>` | `dresslikemommy.com` | Used to build `link` from `product.handle`. |
| `--concurrency <n>` | `12` | Max parallel URL probes. |
| `--timeout-ms <n>` | `10000` | URL probe timeout. |
| `--skip-url-check` | off | Validate required fields only — useful for fast local sanity checks. |
| `--strict` | off | Exit 1 if any item has errors. |
| `--no-age-group` | off | Disable age_group derivation. |
| `--age-group-min-confidence` | `high` | Floor for inclusion in supplemental feed: `high`, `medium`, `low`. |
| `--id-format` | `shopify_pv` | id column format in supplemental CSV/TSV: `shopify_pv`, `sku`, or `variant_id`. Match whatever your primary GMC feed uses. |

## Output schema

`summary.json`

```json
{
  "started_at": "2026-05-03T06:00:00.000Z",
  "finished_at": "2026-05-03T06:01:42.000Z",
  "duration_ms": 102000,
  "input": ".tmp/products.json",
  "products": 660,
  "items": 16813,
  "buckets": {
    "MOMMY":           { "valid": 5210, "errors": 12, "warnings": 3 },
    "FAMILY_MATCHING": { "valid": 4980, "errors": 7,  "warnings": 4 },
    "PAJAMAS":         { "valid": 1244, "errors": 3,  "warnings": 0 },
    "SWIMSUITS":       { "valid": 998,  "errors": 1,  "warnings": 0 },
    "DADDY_ME":        { "valid": 612,  "errors": 0,  "warnings": 0 },
    "UNCATEGORIZED":   { "valid": 3702, "errors": 4,  "warnings": 0 }
  },
  "age_group_histogram": {
    "adult/high":   7210,
    "kids/high":    4310,
    "toddler/high": 3920,
    "infant/high":  690,
    "infant/medium": 7,
    "unknown/none": 4
  },
  "age_group_supplemental_count": 16130,
  "total_errors": 27
}
```

`errors.csv`

```
id,product_id,variant_id,title,bucket,issue_code,field,value,link,image_link
shopify_123_456,123,456,"Mommy & Me Linen Dress",MOMMY,unreachable_404,link,https://...,https://...,https://...
shopify_789_101,789,101,"Family PJ Set",PAJAMAS,missing_required,image_link,,https://...,
```

`valid.jsonl` — one JSON object per line, ready to be transformed into the GMC TSV/Content API payload.

## Bucketing

`categories.js` exports a `BUCKETS` regex map. To fix tag drift or add a new category, edit that file. A product can land in multiple buckets — that's intentional: a "mommy and me pajama set" appears in both PAJAMAS and FAMILY_MATCHING, which is what the diagnostics queue needs.

## age_group derivation + supplemental feed

`ageGroup.js` derives Google Merchant Center's `age_group` (`newborn` | `infant` | `toddler` | `kids` | `adult`) from variant data. Brackets follow the GMC spec: newborn 0–3mo, infant 3–12mo, toddler 1–5yr, kids 5–13yr, adult 13+yr.

**Tiered fallback.** Variant size is authoritative. Product-level title/tags are used only when the variant size has no age signal. This matters for family-matching catalogs where every variant — including adult ones — carries product tags like `Child 1-2yr` AND `Mother S` simultaneously; combining them naively misclassifies adults as toddlers.

**Confidence levels.**
- `high`: explicit numeric size like `Baby 6 Months`, `Child 8 Years`; or a literal adult/mother/father keyword in the size value.
- `medium`: word-only matches like `baby` or `kids` without a numeric anchor.
- `low`: standalone letter sizes like `S` or `2XL` — could be adult, could be teen.
- `none`: no signal at all.

Only items meeting `--age-group-min-confidence` (default `high`) land in the supplemental feed. Lower-confidence items appear in `<bucket>/warnings.csv` for human review and stay in `valid.jsonl` for the main feed (since their existing data is still valid — they just lack a confident age_group derivation).

**Outputs.**

`reports/age_group_supplemental.tsv` — direct upload to Merchant Center as a supplemental feed:

```
id	age_group
shopify_7241307324513_41930596974689	toddler
shopify_7241307324513_41930597335137	toddler
```

`reports/age_group_supplemental.csv` — same data plus `confidence` and `source_size` columns for human review.

**Uploading to Merchant Center.** Merchant Center → Products → Feeds → Add supplemental feed → Upload file → choose `age_group_supplemental.tsv`. Match it to your primary feed and Merchant Center will overwrite/fill the `age_group` attribute for matching items. Re-review runs automatically as the feed reprocesses.

**Important: id format.** The default `--id-format shopify_pv` produces ids like `shopify_<product_id>_<variant_id>`. If your primary GMC feed uses SKU or just the variant_id as the offer id, pass `--id-format sku` or `--id-format variant_id` so the supplemental feed matches.

**Extending the rules.** Edit `ageGroup.js`. The `classifyOne` function returns `{value, confidence, reason}` for a single string; `deriveAgeGroup` runs the tiered fallback. To add a new size pattern (e.g. `Tween 10`), add a regex matcher to `classifyOne`.

## Nightly job

`.github/workflows/feed-validate.yml` runs at 06:00 UTC. It:

1. Pulls the latest catalog via Shopify Admin REST (paged, 250 at a time) using `SHOPIFY_STORE_DOMAIN` + `SHOPIFY_ADMIN_TOKEN` secrets. If those aren't set, it falls back to the committed `tmp_products.json` fixture so the job still executes (visible smoke test).
2. Runs the validator.
3. Uploads `scripts/validateFeed/reports/` as a 30-day artifact.
4. Posts a Slack summary if `SLACK_WEBHOOK_URL` is set and any errors were found.

Required repo secrets:

- `SHOPIFY_STORE_DOMAIN` — e.g. `dresslikemommy.myshopify.com`
- `SHOPIFY_ADMIN_TOKEN` — Admin API token with `read_products` scope
- `SLACK_WEBHOOK_URL` — optional, only used to post the summary

Optional repo variable:

- `SHOPIFY_PUBLIC_DOMAIN` — defaults to `dresslikemommy.com`. Use this if your storefront host differs from the admin host.

You can also trigger the job manually from the Actions tab; the manual dispatch exposes `strict` and `skip_url_check` toggles.
