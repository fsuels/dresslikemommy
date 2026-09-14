# Actual fulfillment source inventory

2026-09-06 · VERIFIED_LOCAL metadata/document inspection; actual costs UNKNOWN.

**Private worklist found:** `/private/tmp/dlm-reconcile-private-20260905/selected_candidate_cost_worklist.csv`, 1,348 bytes, mode0600; directory mode0700. Only filename/stat metadata inspected; header, rows and identifiers were not opened. [Current reconciliation:68](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/CURRENT_SALES_CANDIDATE_RECONCILIATION.md:68) documents six selected orders. Exact private schema remains unverified.

The separate sanitized [five-pair requirements CSV:1](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/candidate_actual_cost_requirements.csv:1) has `actual_fulfillment_cost_usd`, `actual_payment_fee_usd`, `actual_unrecovered_return_loss_usd`, `actual_other_allocated_costs_usd`, `actual_net_margin`, `status`, `required_inputs`; actual-cost cells are blank. This is not proof of the private worklist header.

**Provider provenance:** [April29 plan:120](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/04_IMPLEMENTATION_PLANS/2026-04-29-vetted-shopify-admin-fix-orchestration.md:120) lists BuckyDrop among installed apps; :542 proposes comparing its fulfillment timing. Neither establishes a historical account/store identity or expense ledger. A raw-export filename matched; it was not opened: `dresslikemommy-growth-2026/01_EXPORTS_RAW/SHOPIFY/2026-04-28_LOCAL_SHOPIFY_EXPORT_raw.json`. Parent-supplied current UI evidence identifies `dresslikemommy-com.myshopify.com`, CNY “Order Cost” and separate “Sale Price”; this lane did not independently inspect that UI.

**Calculation boundary:** [existing reconciliation:121](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-05-ceo-turnaround/reconcile_sales_candidates.py:121) uses modeled Shopify unitCost. [Existing economics calculator:18](/Users/fsuels/Projects/dresslikemommy/ops/scripts/plan_marketing_economics.py:18) is proposal-only scenario arithmetic, requiring explicit order value, cost/return-loss/profit/conversion rates and CPC cap; it does not establish invoice-backed actual profit. No BuckyDrop cost adapter was identified in the targeted local source search. Neither calculator was executed.

Next: root privately matches the six selected orders and verifies component definitions, product/China services/domestic freight/international freight/duties, credits, settled payment charges and explicit FX. [Cost problem:4488](/Users/fsuels/Projects/dresslikemommy/ops/PROBLEM_TRACKER.md:4488) requires disjoint costs/recoveries; CNY Order Cost must not be assumed to equal landed cost or mixed directly with USD revenue.

Sanitized source SHA256s (paths linked above):

| Source | SHA256 |
|---|---|
| Current reconciliation | `82f96609d1b2fafc4501100269858f1e55ee288fc15f6d103ab8329010b8e90b` |
| Requirements CSV | `e08f5e8df8665690eddabd9ab7a6e50c2836a9ebc3727faa3a4e9101a2018d8e` |
| Reconciliation calculator | `7221e8df549c9f90a50704e63115b86ec21a01d996da9510bbdda68e2e829b05` |
| Economics calculator | `73d5e057e93f67bd2c9632c0ab6e28e2b752bf99284fae57785cdb9d6a7629ef` |
| April29 plan | `2eac3b6f8b4daac2fb9c10db6cacab910a62e12f8d48b9a7186e510abf8ef146` |
