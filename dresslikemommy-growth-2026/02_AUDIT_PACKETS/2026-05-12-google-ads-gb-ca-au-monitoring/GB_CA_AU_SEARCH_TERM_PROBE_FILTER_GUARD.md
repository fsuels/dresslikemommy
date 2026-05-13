# GB/CA/AU Search-Term Probe Filter Guard

Date: `2026-05-12`
Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-gb-ca-au-searchterms-filter-guard`

## Why

The GB/CA/AU exact Search micro-cohort is live and eligible, but the working Google Ads search-term route has been carrying an unrelated UI filter:

- `Keyword: "human hair wigs"`

This makes the search-term surface non-actionable even when the page loads, because "No search terms match your filters" would reflect the stale unrelated filter rather than the GB/CA/AU campaigns.

## What Changed

Updated local read-only probe:

- `gb_ca_au_perf_search_terms_route_probe.py`

New behavior:

- Adds structured `active_filter_lines`.
- Adds `has_stale_human_hair_filter`.
- Adds `stale_filter_hits`.
- Adds `search_terms_actionable`.
- Adds `search_terms_actionability_note`.
- Adds `--routes` so a future operator can run a fast search-terms-only check:

```bash
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring/gb_ca_au_perf_search_terms_route_probe.py --routes keywords_searchterms
```

Partial-route runs now write a suffixed summary file instead of overwriting the canonical full-route summary.

## Read-Only Verification

Commands:

```bash
python3 -m py_compile dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring/gb_ca_au_perf_search_terms_route_probe.py
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring/gb_ca_au_perf_search_terms_route_probe.py --routes keywords_searchterms
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-google-ads-gb-ca-au-monitoring/gb_ca_au_perf_search_terms_route_probe.py
```

Results:

- Fast search-term-only summary: `raw/perf-search-term-probe/gb_ca_au_perf_search_terms_route_probe_summary__keywords_searchterms.json`.
- Canonical full-route summary restored/refreshed: `raw/perf-search-term-probe/gb_ca_au_perf_search_terms_route_probe_summary.json`.
- Full probe timestamp: `2026-05-12T17:36:21-04:00`.
- Campaign/ad group/keyword routes still show `0` clicks, `0` impressions, `$0.00` cost, `0.00` conversions, and `0.00` conversion value in the visible readbacks.
- Direct `/aw/searchterms` and `/aw/search-terms` still return `404`.
- Working `/aw/keywords/searchterms` loads for GB, CA, and AU, but all three have:
  - `has_stale_human_hair_filter: true`
  - `search_terms_actionable: false`
  - `search_terms_actionability_note: blocked_by_stale_human_hair_filter`

## Decision

No search-term negative, pause, scale, budget, bid, status, CPA, or ROAS action is justified from this readback.

Future operators should not treat "No search terms match your filters" as a real no-query readback until the stale `Keyword: "human hair wigs"` filter is absent or explicitly cleared in the UI under a read-only monitoring context.

## Guardrails

This was a local script/reporting hardening plus read-only page-open probe. No Save, Apply, Enable, Pause, upload, preview, import, budget, bid, status, product-scope, feed-label, product-group, conversion-goal, Merchant, Pinterest, Shopify, checkout, payment, order, billing, credential, or destructive action occurred.
