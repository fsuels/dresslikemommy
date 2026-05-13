# Pinterest Access Retry And ES/IT Verifier Refresh

Date: `2026-05-12`
Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-12-pinterest-es-it-verifier-refresh-auth-blocked`

## Why

The next sales-moving lane after the `17:21` GB/CA/AU zero-data monitor was the already-approved paused US Pinterest draft. Because authenticated Ads Manager access remained the likely blocker, the parent retried browser/tooling access and refreshed the local Pinterest and ES/IT verifier evidence so the next operator can act immediately when access or approval is available.

## Pinterest Access Attempt

Target advertiser: `549756244483`

Attempted paths:

- Chrome skill path: fully read the Chrome skill, then searched for the required Node/browser runtime. The preferred `node_repl` execution tool was unavailable in this tool set.
- Chrome DevTools MCP: `list_pages` failed because the chrome-devtools profile is already running/locked.
- Playwright MCP: opened `https://ads.pinterest.com/advertiser/549756244483/campaigns/`; Pinterest returned `404`, then `https://ads.pinterest.com/` loaded the public Pinterest Ads page with `Log in` / `Sign up` controls, not an authenticated Ads Manager session.
- Computer Use: `list_apps` failed with Apple event error `-1743`, matching the existing macOS automation-permission blocker.

Result:

- No authenticated Pinterest Ads Manager workspace was available.
- No campaign, draft, ad group, ad, product group, catalog source, tag, CAPI, audience, budget, bid, status, or spend write occurred.
- The exact unblock remains: authenticate Pinterest Ads Manager for advertiser `549756244483` in a controllable browser/CDP session, or fix macOS automation permission for Computer Use, then build only paused US draft objects from the clean `342` scope with `4` exclusions.

## Local Freshness Verification

Commands:

```bash
wc -l dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv
shasum -a 256 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_clean_launch_scope_resolved_342.csv dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/lanes/pinterest/raw/pinterest_us_unresolved_exclusions_4.csv
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/validate_pinterest_us_paused_draft_spec.py
python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-12-paid-growth-sales-moving-continuation/validate_es_it_golden_daisy_microtest.py
```

Results:

- Pinterest clean scope file is `343` lines, meaning `342` data rows plus header.
- Pinterest exclusions file is `5` lines, meaning `4` data rows plus header.
- Clean scope SHA256: `ae0c1721cc40e1ca0fbb51f3a15e1fa1bc49095f6226c6f73ef908f4b7a7ab83`.
- Exclusions SHA256: `d3fb918a30a61edb2e9aa618f7bd0582f46d7fc0eb3885619205ab64914de14a`.
- Pinterest paused draft verifier: `PASS`, `21` checks.
- ES/IT Golden Daisy microtest verifier: `PASS`, `44` checks.

## Decision

- Pinterest US paused draft is locally ready but blocked by authenticated controllable Ads Manager access.
- ES/IT Golden Daisy remains `REVIEW_ONLY_NOT_UPLOAD`; the local packet is ready for real native-speaker signoff, but no Google Ads platform use is approved.
- GB/CA/AU are still in timed monitoring mode from the `17:21` zero-data readback. No optimization edit is justified until impressions, clicks, search terms, costs, conversions, or value appear.

## Next Action

1. Restore authenticated Pinterest Ads Manager access for advertiser `549756244483`.
2. Run `validate_pinterest_us_paused_draft_spec.py` again immediately before any paused build.
3. Complete the before-write readbacks in `pinterest_us_paused_draft_build_spec.json`.
4. Build only paused/draft US objects from the `342` scope with `4` exclusions if Pinterest allows save without enabled serving, budget/bid activation, audience/source/tag/CAPI/feed edits, or live spend.
5. In parallel, send the ES/IT Golden Daisy microtest packet to native reviewers and re-monitor GB/CA/AU after reporting populates.
