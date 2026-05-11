# Weekly Scorecard How-To

**Lane:** C / Weekly-Scorecard-Template
**AGENT_CONTINUITY_ANCHOR:** 2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight
**Date (Pacific):** 2026-05-10

## Purpose

`PAID_GROWTH_WEEKLY_SCORECARD_TEMPLATE.csv` is the operator's empty-cell paste-in scorecard for the Dress Like Mommy paid-growth sprint. It captures one row per active or paused campaign per week so the operator can compare actual spend, clicks, conversions, CPA, and ROAS against the canonical economics target (`650%` ROAS, `$70` AOV, `~50%` margin, target CPA `$10.77`, hard-pause `$16` zero-purchase, breakeven CVR `1.39%` at `$0.15` CPC) without re-deriving any numbers and without changing live campaigns.

## Cadence

- Closed every **Monday (Pacific)**, reporting on the prior **Sunday-ending week** (Mon-Sun ISO week).
- Set `week_start_iso` to the Monday that opens the reported week (e.g., `2026-05-04`).
- One row per `campaign_id` per week. Add additional rows for new campaigns as they appear.

## Where to source each numeric column from in Google Ads

Pull values at the **campaign level**, with the date range set to the prior Mon-Sun week, currency normalized to USD:

| CSV column | Google Ads column |
|---|---|
| `cost_usd` | `Cost` |
| `clicks` | `Clicks` |
| `impressions` | `Impr.` |
| `avg_cpc_usd` | `Avg. CPC` |
| `conversions` | `Conversions` (primary purchase action only) |
| `conversion_value_usd` | `Conv. value` |
| `cpa_usd` | `Cost / conv.` (Google Ads' cost-per-conversion column) |
| `roas_pct` | `Conv. value / cost` * 100 (report as percent, e.g. `650`) |

Use **primary purchase value only** for `conversion_value_usd` and `roas_pct`; do not pull historical all-conversion value (per `ECONOMICS_REPORTING_OPERATOR_PACK.md`).

## Decision rules (verbatim from source files)

These are the rules the weekly review must apply to each row. They are not new policy; they are pulled verbatim from the cited source files.

### Zero-purchase guardrails (per ad group)

From `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md` (Section 3):

| Cumulative spend, 0 purchases | ~Clicks at $0.15 CPC | Action |
|---|---|---|
| `$8` | `~53` | **Warning.** Recheck targeting (geo, device, search-term hygiene, audience overlap). No bid/budget change. |
| `$16` | `~106` | **Hard pause.** Pause ad group, log review note, escalate to operator. No restart without fresh approval. |
| `$24` (single ad group, cumulative) | `~160` | **Kill ad group.** Do not resurrect under same configuration; require restructure before any re-enable. |

### First 72-hour rules (post-approved activation)

From `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/economics-reporting/ECONOMICS_REPORTING_OPERATOR_PACK.md` (First 72-Hour Rules):

- **0-24h:** at about `$5` spend with weak terms / broad intent / irrelevant products / no qualified engagement, narrow or pause the smallest unit.
- **24-48h:** at `$9.49-$10.77` spend with `0` purchases, force pause, narrow, or owner decision (lower band for weaker international lanes).
- **48-72h:** at `$16` spend with `0` purchases, hard-pause the unit. For Standard Shopping monitoring, `$16-$20` post-bid-change with `0` purchases triggers rollback decision.
- **No scale before `3` clean purchases** and primary-value pass.
- **Scale only `10%-20%` for borderline winners** or `20%-30%` for clean winners, no more often than every `3-7` days.
- Do not scale from CTR, add-to-cart, checkout starts, saves, impressions, outbound clicks, or cheap CPC alone.

### Canonical economics (verbatim)

From `ROAS_ECONOMICS_REFRESH.md` (Sections 1-2):

- AOV `$70.00`; gross margin `50%`; target ROAS `650%` (6.5x); max CPC `$0.15`; per-country daily budget `$2/day`; hard-pause spend rule `$16` cumulative w/ 0 purchases.
- `CPA_target = $70 / 6.5 = $10.77`
- `GP_pre_ad = $70 * 0.50 = $35.00`
- `Contribution = $35.00 - $10.77 = $24.23`
- Breakeven CVR at `$0.15` CPC = `1.39%`.

### Scaling-eligibility check

A row is eligible to scale (per the operator-pack rules above) only if **all** are true:

- `>= 2` conversions (Lane D's first-evidence floor; `3+` for clean-winner scale).
- `roas_pct` within `80%` of `650%` (i.e., `>= 520%`) for borderline-winner scale; `>= 650%` for clean-winner scale.
- No active blockers per `ops/PROBLEM_TRACKER.md`.

## Operator reminder (read-only)

This scorecard is a **read-only Ads action**. Pulling these numbers from Google Ads requires only viewing campaign reports. **No Save / Edit / Apply / status / budget / bid / targeting / creative changes** in Google Ads, Merchant Center, Shopify, Pinterest, or any other system are authorized by completing this scorecard. Any decision in `actions_taken` or `decision_next_week` that implies a live write must go through an approved gate before execution.

## Source files cited verbatim

- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-ai-army-safe-advance-2/lanes/economics-reporting/ECONOMICS_REPORTING_OPERATOR_PACK.md`
- `/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/market-activation/MARKET_ACTIVATION_SCORECARD.md`
