# Experiment Harness + LM Judge

## Feature Flag Wiring
- Toggle `Enable experiment harness` and list comma-separated slugs inside **Theme Settings -> Experiments**. Layout emits `data-experiment-flags` + `data-experiments-enabled` on `<body>`, and `assets/experiments.js` mirrors the config to `window.experimentConfig` and `window.dataLayer` (`event: "experiments_ready"`).
- Flags are normalized via `handleize`, so enter readable names like `Merch Bundle` → `merch-bundle`. Notes entered in the setting also flow to `window.experimentConfig.notes` for downstream tools.
- In Shopify preview (`Shopify.designMode`), the harness logs `[experiments]` with the active flags so ops can verify the configuration without digging through markup.

## LM Judge Prompt Template
```
System: You are the experiment judge for Dress Like Mommy. Use the rubric below to grade a candidate change that ran behind the <FLAG_SLUG> flag. Accept only evidence that can be derived from the transcript or provided metrics.

User:
- Experiment flag: <FLAG_SLUG>
- Run summary: <WHAT_HAPPENED>
- Metrics: <DATA_TABLE_OR_TEXT>
- Visitor transcript / notes:
<TRANSCRIPT>
```

## Rubric
| Dimension | Description | Scale |
| --- | --- | --- |
| Signal Quality | Did the experiment capture enough qualitative or quantitative signal to justify a decision? | 1 (insufficient) / 3 (marginal) / 5 (actionable) |
| Policy & Brand Safety | Did the treatment stay compliant with Dress Like Mommy constraints (evidence-first, no AI UI, Shopify policies)? | 1 (violation) / 3 (unclear) / 5 (clean) |
| Next Action | Based on the evidence, what is the recommended next step (ship, iterate, rollback)? Provide a 1–2 sentence rationale. | Free-form |

Document every adjudication by attaching the LM judge output to the experiment record in `ops/tests/`.
