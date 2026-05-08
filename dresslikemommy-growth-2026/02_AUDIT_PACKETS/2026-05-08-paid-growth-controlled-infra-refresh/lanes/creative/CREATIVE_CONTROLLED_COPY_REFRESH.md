# Creative Controlled Copy Refresh

Date: 2026-05-08

Lane: creative / RSA / Pinterest copy.

Decision: `CREATIVE_CONTROLLED_COPY_LOCAL_READY_NO_UPLOAD_NO_DRAFTS`

## Scope

This lane refreshed local-only creative assets for the controlled paid-growth infrastructure packet. No Google Ads, Pinterest, Merchant Center, Shopify Admin, feed, product, budget, bid, status, conversion-goal, campaign, asset-upload, catalog, product-group, audience, theme, pixel, or live-spend change was made.

Write scope stayed inside:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/creative/`

## Inputs Read

- `AGENTS.md`
- `ops/prompts/paid-growth-ai-army-continuation-prompt.md`
- `ops/MEMORY_CONTINUITY_PROTOCOL.md`
- `ops/GROWTH_NORTH_STAR.md`
- `ops/AGENT_COORDINATION.md`
- `ops/GOOGLE_ADS_CONTINUITY.md`
- Latest `ops/AGENT_WORKLOG.md` tail
- Prior creative packets from:
  - `2026-05-07-paid-growth-parallel-infra-sprint/creative-copy/`
  - `2026-05-07-paid-growth-ai-army-cache-recheck/lanes/creative/`
- Latest PT and URL readback packet:
  - `2026-05-08-paid-growth-pt-presentment-url-readback/`

## Current Creative Guardrails

- Dress Like Mommy is dropshipping with no physical store and no owned physical inventory.
- Copy must not imply a store, warehouse, pickup, local stock, stocked inventory, guaranteed availability, or guaranteed on-hand stock.
- Copy must avoid unsupported claims around fast delivery, discounts, promotions, best sellers, review counts, social proof, catalog size, and guaranteed stock.
- Return shipping remains customer-paid; outbound delivery rates are not return rates.
- Standard Shopping, PMax, Remarketing, campaign status, budgets, bids, product scope, product groups, feed labels, conversion goals, Merchant source refresh, and Pinterest spend remain outside this lane.

## URL And Market Alignment

The refreshed Google and Pinterest packs now separate copy by current readiness:

- `US`: English local copy remains ready as a proposal only; any use is still a live Ads or Pinterest write requiring approval.
- `GB`, `CA`, `AU`: English-first paused infrastructure only.
- `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `PL`, `CZ`, `GR`: English hold or QA hold; no local-language copy.
- `ES`, `IT`, `RO`, `PT`: local-language draft notes are included because current evidence exists for country-qualified product URLs and checkout presentment. These are still local-only drafts; catalog, tracking, economics, approval, and just-in-time readbacks remain required.
- Bare language final URLs remain unsafe. Future paused packets should use:

```text
https://www.dresslikemommy.com/<locale>/products/<handle>?country=<ISO_COUNTRY>
```

## Files Produced

- `CREATIVE_CONTROLLED_COPY_REFRESH.md`
- `google_rsa_copy_refresh.csv`
- `pinterest_copy_refresh.csv`
- `localized_copy_notes.csv`
- `summary.json`

## Validation Summary

Local checks performed:

- Parsed all CSV files.
- Checked Google RSA headlines are at most 30 characters.
- Checked Google RSA descriptions are at most 90 characters.
- Checked Pinterest titles are at most 100 characters.
- Checked Pinterest descriptions are at most 500 characters.
- Scanned customer-facing Google and Pinterest copy fields for prohibited claims.
- Ran scoped `git diff --check` for this creative lane.

## Residual Risk

This is copy strategy only. It does not prove Google ad policy approval, Pinterest draft eligibility, catalog product-group readiness, Merchant issue resolution, landing-page performance, localized native fluency, or profitable economics. All platform writes and spend remain parent/owner approval-gated.
