# First-Enable Scorecard

Generated: 2026-05-10

Lane: Worker D / first-enable-scorecard

Mode: local/read-only synthesis only. No Google Ads, Merchant Center, Shopify, Pinterest, theme, tracker, worklog, coordination, budget, bid, status, product, feed, conversion, payment, or order writes were made.

## Executive State

Live-spend-ready non-US markets today: `0`.

Closest possible first live enable remains `GB` campaign `23838895360`, ad group `Mommy & Me Dresses - Exact`, at `$2/day` and `$0.15` max CPC. It is still blocked by the non-US purchase-event currency/value measurement gate and a fresh exact owner approval phrase at action time.

Current paused non-US Search build state:

- Built and final-readback passed, all paused: `GB` `23838895360`, `CA` `23834423669`, `AU` `23834424182`, `CH` `23834425358`, `DK` `23838969244`, `DE` `23834427575`, `NL` `23829110118`, `SE` `23838970036`, `ES` `23829133584`, `IT` `23829232530`, `PL` `23829238698`, `CZ` `23829253812`.
- Absent/uncreated: `RO`, `PT`, `GR`, `FR`, `BE`.
- `RO` is parked because the prior preview became not visible after in-progress/error-0 readback. `PT` and `GR` remain unattempted under the one-country-at-a-time guard. `FR` needs a fresh non-stale `88/88 # OK` preview and no-duplicate readback. `BE` remains last after upload-throttle cooldown.

## Ranked Next Safe Business Actions

| Rank | Action | Why it matters for profit growth | Current status | Safe next step without live writes |
|---:|---|---|---|---|
| 1 | Close measurement gate | ROAS cannot be trusted if non-US purchases arrive with missing, duplicated, or mis-currencied value. This is the highest-value unblock before any spend. | `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT` remains `OWNER_APPROVAL_REQUIRED_FOR_PURCHASE_EVENT_PROOF`. Pre-purchase presentment is supported; app-fired purchase currency/value is unproven. | Run browser-enabled Tag Assistant/GA4/Google Ads conversion readbacks. If no historical non-US purchase proves it, request the controlled-test approval phrase before one low-value non-US purchase/refund/cancel. |
| 2 | Resolve RO/PT/GR direction | Completing paused infrastructure keeps the team moving, but it must not stack uploads behind stale Google Ads state. | `RO` absent after stale/not-visible preview; `PT`/`GR` absent/unattempted. | Get owner direction: retry `RO` with a new one-country preview after confirming no in-progress row/no RO campaign, or skip `RO` and continue `PT` then `GR`, one country at a time. |
| 3 | Prepare GB first-enable gate | GB is the smallest credible first spend unit: English, prior checkout-to-shipping pass, paused campaign built, exact-only ad group available. | Not live-spend-ready until measurement gate passes and exact owner approval is received. | Keep the runbook current. At action time, do just-in-time Ads readbacks, then request the verbatim first-enable phrase from the runbook. |
| 4 | Keep Merchant/Pinterest/Beach gates routed | These are parallel growth blockers. They should not block the GB measurement work, but they do block broader profitable scaling. | Merchant US/es age_group needs approval; Pinterest Event Quality remains `Fair`; beach/Vacation Family metadata remains mitigated only by held Ads CSV exclusion. | Keep each gate separate: Merchant Path A approval, Pinterest paused draft or Event Quality repair approval, or narrow Shopify SEO/social metadata approval for product `7227378892897`. No bundled live write. |

## Economics Guardrails

Canonical assumptions preserved:

| Metric | Value |
|---|---:|
| AOV | `$70.00` |
| Gross margin | `50%` |
| Target ROAS | `650%` / `6.5x` |
| Target CPA | `$10.77` |
| Gross profit before ads | `$35.00` |
| Contribution after target CPA, before returns | `$24.23` |
| First GB daily budget | `$2/day` |
| First GB max CPC | `$0.15` |
| Breakeven CVR at `$0.15` CPC | `1.39%` |
| Breakeven CVR at `$0.20` CPC | `1.86%` |
| Breakeven CVR at `$0.25` CPC | `2.32%` |

Zero-purchase kill rules, applied per ad group:

| Cumulative spend with 0 purchases | Approx clicks at `$0.15` CPC | Action |
|---:|---:|---|
| `$8` | `~53` | Warning. Recheck geo, device, search terms, and audience overlap. No bid/budget change. |
| `$16` | `~106` | Hard pause. Pause the ad group, log evidence, no restart without fresh approval. |
| `$24` | `~160` | Kill this configuration. Do not resurrect under the same structure. |

Decision thresholds:

- Do not scale from cheap CPC, CTR, impressions, saves, add-to-cart, checkout starts, or outbound clicks alone.
- At 24h after any approved enable: observe only. No optimization actions.
- At 72h: if spend is `< $8`, keep observing; if spend is `>= $16` with `0` purchases, hard pause.
- At 7d: evaluate CVR only when the row has enough signal. A credible win needs CVR `>= 1.39%` at `$0.15` CPC or CPA `<= $10.77`, with purchase value supporting ROAS near or above `650%`.
- Scale requires fresh approval and should be gradual only after purchase evidence, not pre-purchase engagement.

## Gate Detail

### Measurement Gate

Pass condition: a non-US `purchase` event is proven to send correct `currency`, `value`, and transaction/order id into GA4 and Google Ads through the official Shopify Google & YouTube app, with no duplicate purchase fires. Acceptable outcomes are presentment currency with presentment value, or documented USD with FX-converted USD value. Blocking outcomes are missing currency/value, duplicates, no Google Ads purchase request, or USD with unconverted non-US numeric value.

### RO/PT/GR Gate

No completed country should be re-uploaded. `RO` needs either exact owner direction to retry after fresh no-in-progress/no-campaign readback, or exact owner direction to skip/park and proceed to `PT`, then `GR`. `FR` and `BE` are lower priority than RO/PT/GR because they each have a separate stale-preview/throttle history.

### GB First-Enable Gate

Required before any click:

- Measurement gate passes.
- Owner pastes the exact first-enable phrase from `FIRST_ENABLE_RUNBOOK_REPORT.md`.
- Just-in-time Google Ads readback confirms campaign `23838895360` is paused Search, `$2/day`, Manual CPC, `$0.15`, GB presence-only, Search-only, no conversion-goal override, and all ad groups paused.
- Only campaign `23838895360` and ad group `Mommy & Me Dresses - Exact` are enabled; all other ad groups stay paused.
- No Standard Shopping, PMax, US Search, Merchant, Shopify, Pinterest, feed, product-scope, feed-label, product-group, conversion-goal, budget, or bid change happens.

### Merchant / Pinterest / Beach Gates

Merchant: US/en age_group is solved, but US/es remains isolated to source `10627981690` and needs exact approval for a narrow age_group-only supplemental source or source-specific refresh path.

Pinterest: clean US paused-draft scope exists (`342` rows, `4` exclusions), but Event Quality remains `Fair`. Paused drafts and Event Quality repair are separate approvals; live spend remains separately gated.

Beach: product `7227378892897` has stale Christmas SEO/social metadata on a beach/vacation product. Ads risk is currently mitigated by held CSV/splits excluding Vacation Family and the bad handle. Restoring the theme requires exact narrow Shopify SEO/social metadata approval plus public readback.

## Weekly Template Refresh

Created `weekly_scorecard_template.csv` in this lane because the prior weekly template is now stale: it still has `PL-PENDING` and `CZ-PENDING`, while both campaigns are now built and read back with actual IDs. The refreshed template also adds simple gate/status columns so weekly rows can be filtered by live spend readiness without reading prose reports.

Use one row per campaign per closed Monday-Sunday week. Keep spend and value in Google Ads reporting currency normalized to USD where possible. For non-US rows, add notes if GA4 or Google Ads has FX-converted values.

## Evidence Paths

- `ops/GROWTH_NORTH_STAR.md`
- `ops/AGENT_WORKLOG.md` tail anchor `2026-05-10-paid-growth-ro-parked-preview-not-visible`
- `ops/PROBLEM_TRACKER.md` Active Summary
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/first-enable-runbook/FIRST_ENABLE_RUNBOOK_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/roas-economics/ROAS_ECONOMICS_REFRESH.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/PAID_GROWTH_RO_PT_GR_SEARCH_CONTINUATION_REPORT.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/measurement-gate-recheck/PURCHASE_EVENT_CURRENCY_GATE_RECHECK.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-ro-pt-gr-search-continuation/lanes/csv-guardrail-revalidation/CSV_GUARDRAIL_REVALIDATION.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/merchant-pinterest-beach-gates/MERCHANT_PINTEREST_BEACH_APPROVAL_GATES.md`
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-decision-pack-and-preflight/lanes/weekly-scorecard-template/PAID_GROWTH_WEEKLY_SCORECARD_TEMPLATE.csv`

## Read-Only Inspections / Commands

- `git status --short`
- `find dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-goal-orchestrated-followup -maxdepth 4 -type f`
- `sed -n` reads of `ops/GROWTH_NORTH_STAR.md`, worklog tail, problem tracker active/current sections, first-enable runbook, ROAS economics refresh, current RO/PT/GR continuation report, measurement gate report, CSV guardrail report, Merchant/Pinterest/Beach gate report, prior weekly template, and market activation scorecard.
- `rg` / `find` searches for relevant prior scorecard, economics, runbook, measurement, Merchant, Pinterest, beach, and weekly-template artifacts.
- `mkdir -p` only for this assigned lane directory.

## Residual Risks

- This scorecard is a synthesis, not a live platform readback. Fresh browser/account readbacks remain required before any action-time enablement.
- The weekly template assumes Google Ads values can be normalized to USD. If non-US purchase measurement proves presentment currency or lossy FX behavior, add a per-market currency note to each affected row.
- `GB` is only the first candidate, not a live-spend clearance. The measurement gate plus exact owner approval are still hard blockers.
