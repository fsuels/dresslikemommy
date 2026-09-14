# Feed Integrity Loop

Use this loop for Merchant Center feeds, Pinterest feeds, feed validators, product-group readiness, Cloudflare Worker feed routes, or catalog-source evidence.

## Read First

1. `AGENTS.md`
2. `VISION.md`
3. `scripts/validateFeed/README.md`
4. `ops/cloudflare/pinterest-feed-worker/README.md` when Worker routes are involved
5. `ops/marketing/AGENTS.md` for paid-growth feed decisions
6. Relevant `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md`, and audit packet evidence

## Core Rules

- Feed correctness is revenue-critical and policy-sensitive.
- Do not upload, sync, refresh, configure, or apply Merchant/Pinterest feed/source/catalog/product-group changes without exact current approval.
- Never approve or apply a Pinterest catalog feed that submits same-parent variants without shared `item_group_id`.
- Same-parent Pinterest rows must use the parent product featured image as `image_link`.
- Do not use stale exports as current live proof.

## Local Validation

Use the narrowest relevant local checks:

```bash
cd scripts/validateFeed && node validateFeed.js --input ../../tmp_products.json --out ./reports
python3.13 ops/scripts/check_pinterest_feed_grouping.py --strict
python3.13 ops/scripts/check_continuity_integrity.py --strict
cd ops/cloudflare/pinterest-feed-worker && node --test
```

Only run the commands that match the files or feed surface touched. Do not run deploy commands during local validation. Prefer the direct Node commands above for smoke/test verification; some Codex bundled runtimes expose `node` without `npm`, so record the exact package manager binary used if dependency installation is actually required.

## Worker Route Readback

For Cloudflare feed route work, verify expected behavior locally or against the approved public route:

- HTTP `200` for `GET`.
- `Content-Type: text/tab-separated-values; charset=utf-8`.
- Expected `X-DLM-Feed-SHA256`.
- Expected `X-DLM-Feed-Rows`.
- Body SHA matches the expected feed artifact.
- Non-GET returns `405` with `Allow: GET`.

## External Feed Boundaries

Before clicking or API-calling Save, Apply, Upload, Refresh, Sync, Submit, or Create Product Group:

1. Confirm the write claim in `ops/AGENT_COORDINATION.md`.
2. Confirm the exact owner approval phrase covers this surface and action.
3. Capture before-state readback.
4. Make the smallest approved change.
5. Capture after-state readback and save evidence.

## Done

The loop is done when the feed artifact passes local guards, any Worker route readback matches expected headers/body, and live-source or product-group claims are labeled as current readbacks or explicit unknowns.
