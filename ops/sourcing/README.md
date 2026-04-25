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

It also writes Keep/Reject memory to:

```text
ops/sourcing/state/decisions.json
```

After you verify a kept product, use `Save Proof` and then `Draft Package` in the dashboard. Draft packages are written to:

```text
ops/sourcing/draft-packages/<1688-offer-id>/
```

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
