# Google Ads / Pinterest Market Cell Lane Board

Generated: 2026-05-11

Mode: repo-evidence synthesis only. No browser/account access, upload, apply, enable, budget, bid, status, product, feed, conversion, Merchant, Shopify, Pinterest, GA4/GTM, checkout, payment, order, refund, credential, or destructive action occurred in this lane.

## Status Legend

- `live-ready`: existing controlled live platform path is evidenced, but changes remain guarded.
- `paused-built`: account object exists paused and readback passed; live spend still requires gates.
- `local-only`: repo has local/review artifacts or templates, but no account-ready object/readback.
- `absent/parked`: no clean account object; prior attempt is absent, stale, throttled, or intentionally parked.
- `gated`: blocked by explicit owner approval, measurement proof, Event Quality, platform state, or required review.

Important interpretation: non-US Google Ads live-spend-ready markets remain `0` until `PROB-2026-05-10-NON-US-PURCHASE-CURRENCY-MEASUREMENT` is solved with order-level non-US purchase currency/value/transaction proof or an owner-approved controlled test. Pinterest live-spend-ready markets remain `0`; US has a clean local scope but Event Quality is still `Fair`.

## Compact Board

| Market | Google Ads cell | Google Ads exact next unblock action | Pinterest cell | Pinterest exact next unblock action |
|---|---|---|---|---|
| `US` | `live-ready` guarded existing US Ads: Standard Shopping live/eligible, Brand Search controlled, US nonbrand Search paused separately | Monitor only in this lane. Do not change Standard Shopping/Brand Search. US nonbrand enable or expansion requires exact owner approval plus just-in-time readbacks. | `gated` with clean US local scope/templates | Get exact paused US Pinterest draft approval for the `342` EN-US scope and `4` exclusions, or exact Event Quality repair approval. No live spend while Event Quality remains `Fair` unless separately approved. |
| `GB` | `paused-built`: campaign `23838895360`, Search, paused, `$2/day`, presence-only | Solve non-US purchase measurement; then repeat action-time readbacks for campaign `23838895360` and ad group `Mommy & Me Dresses - Exact` before any exact live-enable approval. | `local-only` | After US/Event Quality gate, build a GB Pinterest source/feed proof packet: source ID, clean row count, item links, product groups, copy, targeting readback checklist. |
| `CA` | `paused-built`: campaign `23834423669`, Search, paused, `$2/day`, presence-only | Solve measurement; wait for GB learning or separate exact approval; repeat action-time campaign/ad group/final URL readbacks. | `local-only` | Build CA Pinterest source/scope packet after US/Event Quality gate; keep English-first unless a separate French-Canada packet is approved. |
| `AU` | `paused-built`: campaign `23834424182`, Search, paused, `$2/day`, presence-only | Solve measurement; wait for GB/CA learning or separate exact approval; repeat action-time readbacks. | `local-only` | Build AU Pinterest source/scope packet after US/Event Quality gate with AUD/URL/product-group proof if exposed. |
| `CH` | `paused-built`: campaign `23834425358`, Search, paused, `$1/day`, presence-only | Solve measurement; decide English-first versus German/French/Italian split before native traffic; exact approval/readbacks before enable. | `local-only` | Decide Pinterest language posture first, then build CH source/scope packet with source/feed proof and country targeting readback. |
| `DK` | `paused-built`: campaign `23838969244`, Search, paused, `$1/day`, presence-only | Solve measurement; keep Danish native copy gated until native review/landing QA; exact approval/readbacks before enable. | `local-only` | Prove DK Pinterest source/feed/scope and complete Danish native review before platform use. |
| `DE` | `paused-built`: campaign `23834427575`, Search, paused, `$1/day`, presence-only | Solve measurement; native German review/landing QA required before local-language use; exact approval/readbacks before enable. | `local-only` | Prove DE Pinterest source/feed/scope, product groups, destination consistency, and native German copy review. |
| `NL` | `paused-built`: campaign `23829110118`, Search, paused, `$1/day`, presence-only | Solve measurement; native Dutch review/landing QA required before local-language use; exact approval/readbacks before enable. | `local-only` | Prove NL Pinterest source/feed/scope and native Dutch copy review. |
| `SE` | `paused-built`: campaign `23838970036`, Search, paused, `$1/day`, presence-only | Solve measurement; native Swedish review/landing QA required before local-language use; exact approval/readbacks before enable. | `local-only` | Prove SE Pinterest source/feed/scope and native Swedish copy review. |
| `ES` | `paused-built`: campaign `23829133584`, Search, paused, `$1/day`, presence-only | Solve measurement; use May 11 Spanish rewrite slice only after native review and landing-language QA; exact approval/readbacks before enable. | `local-only` | Prove ES Pinterest source/feed/scope and native Spanish copy review. |
| `IT` | `paused-built`: campaign `23829232530`, Search, paused, `$1/day`, presence-only after repair | Solve measurement; use May 11 Italian rewrite slice only after native review and landing-language QA; exact approval/readbacks before enable. | `local-only` | Prove IT Pinterest source/feed/scope and native Italian copy review. |
| `PL` | `paused-built`: campaign `23829238698`, Search, paused, `$1/day`, presence-only after repair | Solve measurement; use May 11 Polish rewrite slice only after native review and landing-language QA; exact approval/readbacks before enable. | `local-only` | Prove PL Pinterest source/feed/scope and native Polish copy review. |
| `CZ` | `paused-built`: campaign `23829253812`, Search, paused, `$1/day`, presence-only after repair | Solve measurement; use May 11 Czech rewrite slice only after native review and landing-language QA; exact approval/readbacks before enable. | `local-only` | Prove CZ Pinterest source/feed/scope and native Czech copy review. |
| `RO` | `absent/parked`: no campaign; prior preview stale/not visible; later retry blocked before upload by Google Ads throttle | Wait for upload-throttle cooldown, confirm no active in-progress `RO`/`FR`/`BE` upload row and no `RO` campaign, then retry one-country `RO` preview only. Apply only if `88/88 # OK`, then read back. | `local-only` | Do not prioritize Pinterest before RO Ads branch and RON/source proof. Build RO source/scope packet only after source proof and Romanian review. |
| `PT` | `absent/parked`: no campaign; not attempted behind unresolved `RO`; `pt-PT` vs `pt-BR` storefront behavior remains a copy gate | Resolve/park `RO` first, or get exact approval to skip `RO`; then one-country `PT` preview/readback. Resolve `pt-PT` vs `pt-BR` before native copy use. | `local-only` | Resolve Portuguese language behavior, then prove PT Pinterest source/feed/scope and native/country copy before any account action. |
| `GR` | `absent/parked`: no campaign; not attempted behind `RO`/`PT` sequence | Resolve `RO`/`PT` sequence, then one-country `GR` preview/readback. Greek native review/landing QA before local-language use. | `local-only` | Prove GR Pinterest source/feed/scope and Greek native copy review before any account action. |
| `FR` | `absent/parked`: no campaign; stale/in-progress or completed-with-errors/no-changes path | Fresh non-stale `88/88 # OK` preview and no-duplicate readback after branch direction; apply/read back only under exact approval. | `local-only` | Keep Pinterest parked until FR source proof and native French review exist; do not infer readiness from Google artifacts. |
| `BE` | `absent/parked`: no campaign; upload-throttle history and Belgium language split unresolved | Wait for upload-throttle cooldown, decide FR/NL split, then fresh one-country preview/readback only after earlier branch state is clean. | `local-only` | Decide `fr-BE` vs `nl-BE` or split objects, then prove BE source/feed/scope and native copy before any account action. |

## Evidence Index

- Current operating prompt and guardrails: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`.
- Active blockers: `ops/PROBLEM_TRACKER.md`.
- Active coordination state: `ops/AGENT_COORDINATION.md`.
- Latest native rewrite and measurement gate: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-11-paid-growth-native-rewrite-local-measurement-continuation/NATIVE_REWRITE_LOCAL_ONLY_REPORT.md`, `MEASUREMENT_READONLY_CONTINUATION.md`, `native_rewrite_locale_status.csv`, `validation_summary.json`.
- Current Google Ads/Pinterest market matrix baseline: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-platform-matrix/EXECUTION_MATRIX.md`.
- Google Ads launch prep and RO throttle evidence: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/PAID_GROWTH_AUTHORITY_SAFE_LAUNCH_PREP_REPORT.md`, `lanes/google-ads-launch-readiness/google_ads_market_readiness.csv`, `GOOGLE_ADS_FIRST_ENABLE_READBACKS.md`, `RO_RETRY_BLOCKED_BY_UPLOAD_THROTTLE.md`.
- Pinterest US clean scope and Event Quality: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-pinterest-catalog-event-unblock/PINTEREST_CATALOG_EVENT_UNBLOCK_REPORT.md`, `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/pinterest-paused-draft-structure/PINTEREST_PAUSED_US_DRAFT_STRUCTURE.md`.
- Pinterest non-US local prep: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-authority-safe-launch-prep/lanes/pinterest-non-us-local-drafts/PINTEREST_NON_US_LOCAL_DRAFTS_REPORT.md`, `pinterest_non_us_market_readiness_matrix.csv`.
- Pinterest catalog/copy term gates: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-multilingual-keyword-quality-upgrade/PINTEREST_KEYWORD_QUALITY_GATES.md`, `pinterest_multilingual_keyword_interest_quality_plan.csv`.

## Guardrails Preserved

- Do not re-upload completed Google Ads countries: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `ES`, `IT`, `PL`, `CZ`.
- Do not enable non-US Google Ads until the non-US purchase measurement gate is solved and just-in-time campaign/ad group/final URL/conversion readbacks pass.
- Do not change Standard Shopping status, budget, product groups, feed labels, product scope, or conversion goals without fresh explicit owner approval.
- Do not create Pinterest account objects, drafts, campaigns, product groups, audiences, catalog/source changes, budgets, bids, statuses, tag/CAPI changes, or spend without exact owner approval and before/after readbacks.
- Do not make Shopify product-data/theme/feed/Merchant/GA4/GTM changes from this lane.
- Do not treat this board as clearing the separate Merchant `US/es` age_group gate, the beach/Vacation Family SEO metadata gate, or native-language review gates. Use held/excluded ad packets where those gates remain unresolved.

## Next Closest Unblock

1. Measurement: prove order-level non-US `purchase` currency/value/transaction evidence in GA4/Google Ads using GA4 UI Explore/export or refreshed read-only GA4 API scopes.
2. Google Ads build completion: after upload cooldown, retry `RO` one-country preview only; keep `PT`/`GR` unstacked behind unresolved `RO`; handle `FR` with a fresh non-stale preview and `BE` after throttle plus language split.
3. Pinterest: resolve US/Event Quality path first, then build a country-specific local source/scope packet for `GB`, `CA`, or `AU` before any non-US Pinterest approval request.
