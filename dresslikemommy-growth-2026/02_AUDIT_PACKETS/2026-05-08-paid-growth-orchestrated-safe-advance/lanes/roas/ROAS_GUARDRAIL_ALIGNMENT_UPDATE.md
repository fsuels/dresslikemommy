# ROAS Guardrail Alignment Update

Date: 2026-05-08
Mode: local/read-only; no budget, bid, campaign, or platform write

## Economics

At `$70` AOV and `650%` ROAS:

- Max CPA: `$10.77`.
- Gross profit before ads at `50%` margin: `$35.00`.
- Contribution after target CPA before returns/chargebacks: `$24.23`.

Required CVR by CPC:

| CPC | Required CVR |
|---:|---:|
| `$0.04` | `0.37%` |
| `$0.08` | `0.74%` |
| `$0.10` | `0.93%` |
| `$0.12` | `1.11%` |
| `$0.15` | `1.39%` |
| `$0.20` | `1.86%` |
| `$0.25` | `2.32%` |

## Fix Applied Locally

Updated the current ROAS packet to align with current evidence:

- Pinterest scope changed from stale `337/9` language to `342` clean rows / `4` exclusions.
- Country CPC caps now match the Ads international packet:
  - `GB`, `CA`, `AU`: `$0.15`.
  - `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`: `$0.12`.
  - `PL`, `CZ`, `RO`, `GR`, `PT`: `$0.10`.
- Romania caveat remains: RO presents in `RON`, so ROAS needs native RON or FX-normalized value before USD comparison.

Files updated:

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/roas/ROAS_CONTROLLED_GUARDRAILS.md`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/roas/country_budget_guardrails.csv`.
- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-controlled-infra-refresh/lanes/roas/summary.json`.

## Kill Rules

- `$5` with weak traffic: pause/narrow after approval.
- `$9.49-$10.77` with zero purchases: force pause/narrow/owner decision.
- `$16` with zero purchases: hard pause.
- Scale only after `3+` clean purchases, primary purchase value is trusted, CPA is at or below target, and country/product/query quality is clean.

