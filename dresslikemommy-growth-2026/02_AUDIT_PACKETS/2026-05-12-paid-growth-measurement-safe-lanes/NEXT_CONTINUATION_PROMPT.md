# Next Continuation Prompt Pointer

Use the owner-standard prompt in `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.

Newest anchor:

`AGENT_CONTINUITY_ANCHOR: 2026-05-12-paid-growth-measurement-safe-lanes`

Do not redo:

- Do not redo the 2026-05-11 native rewrite packet. Use its `REVIEW_ONLY_NOT_UPLOAD` replacement rows.
- Do not re-upload completed non-US Search countries: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, `CZ`.
- Do not redo Merchant US/en age_group.
- Do not treat aggregate GA4 purchase revenue as order-level non-US currency/value proof.

Unresolved blockers:

- `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT`: GA4 UI transaction report route is visible, but currency/order-level candidate matching remains unproven. Existing `gcloud` token still lacks GA4 scopes.
- `PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE`: `RO`, `PT`, `GR` absent; `FR`, `BE` parked.
- `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE`: native copy is review-only; landing QA and supplier-token blockers remain.
- `PROB-2026-05-08-PINTEREST-EVENT-QUALITY`, `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP`, and `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` remain approval-gated.

Next subagent workstreams:

- Measurement: GA4 Data/Admin API scope refresh or owner-approved controlled non-US test-purchase procedure.
- Ads: one-country `RO` preview retry only after upload cooldown/no-in-progress/no-RO-campaign readback, or exact owner decision to skip/park `RO` and proceed `PT`, then `GR`.
- Localization: no-upload final URL QA matrix for nine review-ready locales; supplier-token cleanup brief.
- Pinterest: Event Quality verification path or paused US draft path only with exact approval.
- Merchant: US/es source `10627981690` repair review only with exact approval.
