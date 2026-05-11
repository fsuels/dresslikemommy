# Native Copy Risk Triage

Date: 2026-05-10

Lane: native-copy-risk-triage

Scope: local decision triage only. No browser use, no Google Ads / Merchant / Shopify / Pinterest / GA4 writes, no `ops/` edits.

## Source Evidence Read

- Prior native-language checklist: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-deep-followup/lanes/native-language-review-checklist/NATIVE_LANGUAGE_REVIEW_CHECKLIST_REPORT.md`
- Native copy options CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/native_language_rsa_options.csv`
- Native copy options report: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/native-language-copy-options/NATIVE_LANGUAGE_COPY_OPTIONS_REPORT.md`
- Market activation scorecard: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/market-activation/MARKET_ACTIVATION_SCORECARD.md`

## Executive Decision

English-first paused infrastructure can proceed as paused infrastructure only, provided it stays clearly labeled as English-first, local/paused, and separate from native-language launch readiness. It must not be used as evidence that any non-English market is live-spend-ready.

Native-language Ads copy remains concept-only. The immediate unresolved risks below require explicit owner and/or native-speaker decisions before any localized Ads copy is imported, associated with campaigns, or enabled.

## Immediate Risk Triage

| Risk | Severity | Evidence | Exact Decision Needed | Safe Next Action | Must Not Import Or Enable Yet |
|---|---|---|---|---|---|
| Portugal: `pt-PT` Ads copy against storefront behavior previously read as `pt-BR` | `P1 / HIGH` | CSV row says `/pt product URLs with country=PT previously read back as Portugal / pt-BR / EUR`; checklist marks `pt-PT` as `HIGH RISK` and says if `/pt` still serves `pt-BR`, fail the locale. | Owner must choose one: 1. repair/confirm storefront serves European Portuguese before `pt-PT` Ads use; 2. explicitly accept a documented `pt-PT` ad to `pt-BR` landing mismatch; 3. do not use localized PT Ads copy and keep PT English-first/paused only. Native Portuguese reviewer must confirm final ad copy and the live landing language. | Commission or request a Portugal-native review with landing QA on `https://dresslikemommy.com/pt/products/<HANDLE>?country=PT`; mark PASS only if PDP, cart, checkout, and policy/page copy read as Portugal-appropriate or the owner documents the mismatch acceptance. | Do not import or enable `pt-PT` localized RSAs, PT localized keywords, or any PT live spend based on current concept copy. Do not treat Portugal checkout/currency pass as native-language copy pass. |
| Denmark: `da-DK` headline contains `Mamma datter kjoler` | `P2 / MEDIUM-HIGH` | CSV row includes `Mor datter kjoler|Mamma datter kjoler|Dress Like Mommy`; checklist says `Mamma` appears Swedish/Norwegian inside Danish and should be marked REWRITE. | Danish native speaker must decide replacement wording, likely either remove the option, reuse `Mor datter kjoler`, or rewrite as `Mor og datter kjoler` if it fits Ads length and reads natively. Owner must approve the final Danish option set after native review. | Produce a corrected `da-DK` final row after native review, then rerun length and forbidden-claim checks before any platform use. | Do not import any `da-DK` RSA containing `Mamma datter kjoler`. Do not enable DK localized copy; DK may only remain English-first paused infrastructure unless a separate explicit decision is recorded. |
| Belgium: unresolved `fr-BE` / `nl-BE` split | `P2 / HIGH for BE local-language structure` | CSV has two Belgium variants, `BE-FR/fr-BE` and `BE-NL/nl-BE`; checklist says `fr-BE` is identical to `fr-FR`, `nl-BE` is identical to `nl-NL`, and Belgium split decision is prerequisite. | Owner must choose BE structure before localized BE use: 1. one English-first BE paused campaign only; 2. two localized BE ad groups/campaigns split by French/Dutch language targeting and landing path; 3. defer BE localized build until storefront language routing can be proven. Native reviewers must explicitly accept `fr-FR` copy for Belgian French and `nl-NL` copy for Flemish, or rewrite. | Keep BE absent/parked until upload throttle and split decision clear. If preparing locally, make a BE decision memo first: target language(s), final URL pattern, campaign/ad group split, reviewer sign-off, and landing-language QA evidence for Belgium/EUR. | Do not import `fr-BE` or `nl-BE` copy as if reviewed. Do not create a BE localized structure that mixes French and Dutch intent without an owner decision. Do not enable BE spend from the concept rows. |
| English-first paused infrastructure while native copy remains concept-only | `P2 / MANAGEABLE IF LABELED` | Prior packets state held Search CSV is English-language (`en`) and not a native-language launch packet; market scorecard says GB/CA/AU are the only markets not blocked by native-copy review, while 14 other locale variants still need native-speaker review before spend. | Owner must explicitly distinguish two approvals: paused English-first infrastructure build approval vs localized/native copy approval vs live-spend enable approval. A paused build approval must not imply localized-copy approval or spend approval. | Continue one-country-at-a-time paused infrastructure recovery only after the Ads upload lane is clean, using English-first artifacts where already approved, and keep all localized/native copy in local concept status until per-locale review closes. | Do not import native-language RSA rows into Google Ads yet. Do not enable non-English markets on the claim that concept copy exists. Do not mark ES/IT/RO/PT/DE/NL/FR/BE/SE/DK/PL/CZ/GR live-spend-ready until native review, landing-language QA, tracking/economics gates, exact owner enable approval, and just-in-time Ads readbacks pass. |

## Decision Tree For The Next Operator

1. If the action is only recovering paused English-first Google Search infrastructure, proceed only under the existing paused-build approval and only after the current Ads upload/preview lane is clean. Keep status paused and label the work English-first.
2. If the action would use local-language headlines/descriptions, stop until the relevant locale has native-speaker sign-off, landing-language QA, validation for Ads limits, and owner approval for that locale.
3. If the action involves Portugal, resolve the `pt-PT` vs `pt-BR` storefront mismatch first.
4. If the action involves Denmark localized copy, remove or rewrite `Mamma datter kjoler` first.
5. If the action involves Belgium localized copy, record the FR/NL split decision before building or importing any BE localized structure.

## Safe Immediate Next Actions

- Build a short owner decision prompt with three checkboxes: PT storefront choice, DK rewrite approval path, and BE FR/NL split posture.
- Request native-speaker review only for the next market that could plausibly be activated after English-first GB/CA/AU; do not bulk-approve all locale rows.
- Keep GB/CA/AU as the first English-first candidates; native copy is not on their critical path, but live enablement still requires separate exact approval and fresh readbacks.
- Keep all native copy artifacts local until final per-locale CSVs exist and pass length plus forbidden-claim validation.

## Hard Blocks

- No localized Portugal import until `pt-PT` landing behavior is resolved or consciously accepted by the owner as a mismatch.
- No Danish localized import while `Mamma datter kjoler` remains in the candidate row.
- No Belgium localized import without the owner choosing the BE French/Dutch structure.
- No enabled non-English Search spend from concept-only localized copy.
- No Merchant, Shopify Admin, theme, Pinterest, conversion-goal, budget, bid, status-enable, or external-account write follows from this triage.

## Bottom Line

Paused English-first infrastructure and native-language readiness are separate tracks. The former can continue under paused-build controls; the latter is still blocked per locale. PT, DK, and BE are the three immediate copy-risk decisions that must be cleared before localized import or enablement.
