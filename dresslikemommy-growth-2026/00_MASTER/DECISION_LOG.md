# Decision Log

Use this log for durable growth decisions, including decisions not to act.

| Date | Decision | Evidence | Owner | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 2026-04-28 | Created the 2026 growth workspace scaffold. | Local repo structure under `dresslikemommy-growth-2026/`. | Agent | Done | Raw export, audit, analysis, plan, screenshot, and rollback folders are now tracked. |
| 2026-04-28 | Adopted paid-spend product economics gate: all-in non-marketing cost equals 50% of selling price; current AOV is $63.25; max CAC is $9.49; required ROAS is 6.67; low-AOV or unknown-cost products/collections are excluded from paid spend. | Operator instruction on 2026-04-28. | Operator | Active | Marketing cost, returns, and chargebacks are deducted after the 50% all-in product/shipping/fees cost. |
| 2026-04-29 | Pinterest Shopping Ads stay blocked until exact item-level Pinterest catalog status, event/CAPI deduplication proof, USA-only targeting proof, and ROAS guardrails pass; post-gate structure is USA-only Shopping/catalog sales groups for Mommy & Me, Family Matching, and Pajamas. | `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-04-29-pinterest-shopping-ads-gate/summary.json` | Agent | Active | Do not click `Create an ad` or create Pinterest product groups until the gates pass and the operator explicitly approves that exact action. |
