# Next Continuation Prompt

Use the canonical paid-growth prompt:

`ops/prompts/paid-growth-ai-army-continuation-prompt.md`

Newest anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-10-google-ads-non-us-search-paused-build-9-applied-it-preview-parked`

Critical carry-forward:

- Owner already gave the exact paused non-US Google Search TEST BUILD approval on 2026-05-10. Do not request that same approval again for the remaining paused build unless the scope changes.
- Completed paused campaigns from the approved build: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, and `ES`.
- All 9 final readbacks are paused, Search, presence-only, content/YouTube off, and on approved split budgets. Do not re-upload or duplicate them.
- `FR`, `BE`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR` remain absent/uncreated.
- `FR` is parked: preview once validated `88/88 # OK`, but a stale/in-progress apply recovery produced `completed with errors` / `no changes`; no FR campaign exists. Require a fresh completed `88/88 # OK` preview before any FR apply.
- `BE` is parked by Google Ads upload throttling: too many simultaneous/recent uploads. Wait for cooldown/tooling before retry.
- `IT` is parked: a fresh resume preview remained in progress at `0` changes, `0` success, and `0` errors after the helper's 120-second guard plus a 60-second follow-up. No IT apply was clicked, and IT remains absent. Wait for that preview to clear or start a fresh preview that completes `88/88 # OK`.

Next best action:

1. Read `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, `ops/PROBLEM_TRACKER.md`, `ops/AGENT_COORDINATION.md`, and this packet report.
2. Resume only unresolved split files one country at a time from `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/`.
3. Required controls: absent readback, preview/download/validate, apply/download/validate, campaign RPC readback for paused/Search/presence-only/approved budget.
4. Stop on stale/in-progress preview, `0` changes, upload throttle, non-`# OK`, enabled rows, budget/bid mismatch, US/PMax/Standard Shopping/Merchant/Shopify/Pinterest/theme/product/feed/conversion surfaces, or unclear readback.
