# 1688 Sourcing Shortlist

Phase 1 adds a sourcing gate before the Shopify listing workflow.

## Local Dashboard

Use this as the main operator interface:

```bash
python3 ops/scripts/1688_sourcing_dashboard.py --open
```

Or double-click:

```text
ops/sourcing/Open Dress Like Mommy Sourcing.command
```

The dashboard groups candidates into:

- Mommy & Me
- Daddy & Me
- Family Matching
- Couples
- Maternity

The top numbers use store-owner language:

- `Stored Cards`: every raw 1688 card saved locally
- `Buyer Shortlist`: only fresh, category-fit leads that are worth opening
- `Saved`: products the operator chose with Save/Keep
- `Ready for Draft`: saved products with required proof filled in
- `Rejected`: products remembered so they are not researched again
- `Best Leads`: internal `Gold` candidates
- `Unverified Leads`: internal `Test` candidates that need proof before listing

To add fresh candidates without terminal commands:

1. Pick a category tab, or use All Categories.
2. Click `Find Qualified Leads`.
3. The app first checks the helper Chrome tab. If 1688 is on login/CAPTCHA/interception, it shows that blocker instead of pretending the fetch worked.
4. The collector rotates the category keywords, skips already-seen offer IDs, and stops once it has at least 3 `Unverified Leads`/`Best Leads` candidates.
5. If 1688 asks for login or CAPTCHA, click `Open 1688 Login/Search`, complete the browser step manually, then click `Find Qualified Leads` again.

`Open 1688 Login/Search` reuses the existing helper tab when possible. It should not create a new tab on every click.

Search-stage filtering is intentionally strict about freshness:

- `Unverified Leads`: correct category, visible 2025/2026 or Chinese new-style signal, newer 1688 offer ID, usable image, low MOQ, and at least one useful signal such as repeat rate, sales, dropship wording, or strong score.
- `Reject`: previous reject, older 1688 offer ID, stale year signal such as 2020-2024 in 2026, no visible freshness signal, wrong category, no product URL/image, high MOQ, explicit no-dropship/no-size-chart evidence, or brand/IP risk.
- `MIN_FRESH_OFFER_ID` is currently `850000000000`. It is a practical recency proxy because old 1688 listings can be edited to say 2026.
- Category fit is rechecked from visible title/card text, so an old saved `category_match` value cannot keep a plain women-only dress active for Mommy & Me.
- `Sales`: the number visible on the 1688 search card. If 1688 does not show a time window, treat it as a popularity clue and verify on the product detail page.

Detail-stage filtering is the Best Lead gate:

- `Best Leads` / internal `Gold` must come from detail-page proof, not search-card data.
- Detail proof should include supplier identity, supplier quality signals, size chart, dropship/one-piece support, dispatch or ready-stock proof, usable vendor images, no obvious IP risk, and enough overall score.
- The detail enricher is:

```bash
python3 ops/scripts/1688_sourcing_detail_enrich.py --key <1688-offer-id>
```

- It opens the product page through the logged-in helper browser, saves vendor images under `ops/sourcing/vendor-images/<1688-offer-id>/`, writes detail-stage artifacts under `ops/sourcing/detail-enrichment/<1688-offer-id>/`, and records proof back into `ops/sourcing/state/decisions.json`.
- Supplier memory is tracked in `ops/sourcing/state/vendors.json` when supplier identity is captured.

It also writes Keep/Reject memory to:

```text
ops/sourcing/state/decisions.json
```

Search history and seen-offer memory live in:

```text
ops/sourcing/state/search-history.json
```

After you verify a kept product, use `Save Proof` and then `Draft Package` in the dashboard. Draft packages are written to:

```text
ops/sourcing/draft-packages/<1688-offer-id>/
```

The dashboard also has `Verify Detail Proof` on each product card. Use that before treating any product as a Best Lead. `Draft Package` is blocked until the proof fields are filled, so unverified products do not move too early into listing work.

See `ops/sourcing/AGENT-SOURCING-WORKFLOW.md` for the full workflow.

## Fast Demo

```bash
python3 ops/scripts/1688_sourcing_score.py \
  --input ops/sourcing/sample-candidates.csv \
  --output-dir ops/sourcing/demo-shortlist \
  --stage search
```

Open:

```text
ops/sourcing/demo-shortlist/shortlist.html
```

## Real Workflow

1. Search 1688 while logged in, or run the CDP collector:

```bash
python3 ops/scripts/1688_sourcing_cdp_collect.py --category family-matching --limit 24
```

2. If the CDP collector is blocked by login/CAPTCHA, run `ops/sourcing/1688-browser-collector.js` in the browser console.
3. Save the JSON to a run folder, for example:

```text
ops/sourcing/2026-04-25-family-dresses/candidates.json
```

4. Run:

```bash
python3 ops/scripts/1688_sourcing_score.py \
  --input ops/sourcing/2026-04-25-family-dresses/candidates.json \
  --output-dir ops/sourcing/2026-04-25-family-dresses \
  --stage search \
  --decision-state ops/sourcing/state/decisions.json
```

5. Review the dashboard or `shortlist.html`.
6. Open the strongest `Test` cards, confirm detail-page evidence, then rerun with `--stage detail` after size chart, dropship, dispatch, and supplier evidence are filled in.
7. For a `Gold` product, save the size chart and images, then use the copied listing request with the canonical prompt files in `ops/prompts/`.

## Outputs

Each run writes:

- `shortlist.html`: visual review board with product images, URLs, scores, filters, and copyable listing requests
- `scored-candidates.csv`: spreadsheet-friendly scoring output
- `scored-candidates.json`: structured output for future automation
- `summary.md`: quick text summary
