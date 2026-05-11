# Market Activation Scorecard

Lane: E / Market-Activation
AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-orchestrator-safe-resume

Synthesized from durable state in `AGENTS.md` (paragraphs 70-98), `ops/AGENT_WORKLOG.md` tail entries near the IT-still-in-progress anchor, and the `ops/PROBLEM_TRACKER.md` Active Summary. Read-only synthesis only; no live writes, no browser/account writes, no `ops/PROBLEM_TRACKER.md` edits.

## Live-spend-ready non-US markets today: `0`

## Per-country activation readiness matrix

| Country | Checkout-to-shipping QA | Paused Search campaign | Native-language copy | Tracking gate | Beach-SEO bad-handle exposure | Live-spend-ready? | Remaining gates to live spend |
|---|---|---|---|---|---|---|---|
| `GB` | `PASS` 2026-05-08; `en-GB`, GBP, Standard `FREE`, Express `GBP 10.00`; visual UI pass | `23838895360`, `$2/day`, paused, presence-only, content/YouTube off | `English-first concept-ready` (English market) | Reuses US-tied conversion goal; depends on same goal for non-US Search | `0` (held CSV excludes handle `matching-family-beach-outfits-...`; `0` forbidden hits) | `NO` | Exact owner approval to enable; `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` exclusion must hold; `650%` ROAS economics gate; just-in-time Ads readback |
| `CA` | `PASS` 2026-05-08; `en-CA`, CAD, Standard `FREE`, Express `CAD 19.00`; visual UI pass | `23834423669`, `$2/day`, paused, presence-only | `English-first concept-ready` (English market) | Reuses US-tied conversion goal | `0` (held CSV exclusion) | `NO` | Exact enable approval; ROAS economics; just-in-time readback |
| `AU` | `PASS` 2026-05-08 isolated-browser; AUD, Standard `0.00 AUD`, Express `18.24 AUD`, `en-AU` UI | `23834424182`, `$2/day`, paused, presence-only | `English-first concept-ready` (English market) | Reuses US-tied conversion goal | `0` (held CSV exclusion) | `NO` | Exact enable approval; ROAS economics; just-in-time readback |
| `CH` | `PASS` 2026-05-09; CHF, Standard `0.00 CHF`, Express `10.24 CHF`, `en-CH` UI | `23834425358`, `$1/day`, paused, presence-only | `English-first concept-ready` (DE/FR/IT native pack would need native review) | Reuses US-tied conversion goal | `0` | `NO` | Native-copy decision (`PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE`); enable approval; ROAS economics |
| `DK` | `PASS` 2026-05-09; DKK, Standard `0.00 DKK`, Express `83.60 DKK`, `en-DK` UI | `23838969244`, `$1/day`, paused, presence-only | `English-first concept-ready` (Danish native review pending) | Reuses US-tied conversion goal | `0` | `NO` | Native-copy decision; enable approval; ROAS economics |
| `DE` | `PASS` 2026-05-09; EUR, Standard `0.00 EUR`, Express `11.19 EUR`, `en-DE` UI | `23834427575`, `$1/day`, paused, presence-only | `localized concept-ready (no native-speaker review)` for de | Reuses US-tied conversion goal | `0` | `NO` | Native-speaker review for de; enable approval; ROAS economics |
| `NL` | `PASS` 2026-05-09 (cooldown retry); EUR, Standard `FREE`, Express `EUR 11.95`, `en-NL` UI | `23829110118`, `$1/day`, paused, presence-only | `localized concept-ready (no native-speaker review)` for nl | Reuses US-tied conversion goal | `0` | `NO` | Native-speaker review for nl; enable approval; ROAS economics |
| `SE` | `PASS` 2026-05-09; SEK, Standard `0.00 SEK`, Express `121.52 SEK`, `en-SE` UI | `23838970036`, `$1/day`, paused, presence-only | `localized concept-ready (no native-speaker review)` for sv | Reuses US-tied conversion goal | `0` | `NO` | Native-speaker review for sv; enable approval; ROAS economics |
| `FR` | `PASS` 2026-05-09; EUR, Standard `0.00 EUR`, Express `EUR 11.95`, `en-FR` UI | `absent` (`FR stale preview / no changes`; parked until fresh `88/88 # OK` preview) | `localized concept-ready (no native-speaker review)` for fr | Reuses US-tied conversion goal | `0` | `NO` | Resume preview/apply with fresh `88/88 # OK`; native-speaker review for fr; enable approval; ROAS economics |
| `BE` | `PASS` 2026-05-09; EUR, Standard `0.00 EUR`, Express `EUR 11.95`, `en-BE` UI | `absent` (`BE upload throttle`; retry last after cooldown) | `localized concept-ready (no native-speaker review)` for fr/nl | Reuses US-tied conversion goal | `0` | `NO` | Upload throttle cooldown; preview/apply `88/88 # OK`; native-speaker review for fr/nl; enable approval; ROAS economics |
| `ES` | `PASS` 2026-05-08 (PT-cooldown context); EUR, localized policy/page copy clean; country-qualified URL pass | `23829133584`, `$1/day`, paused, presence-only | `localized concept-ready (no native-speaker review)` for es | Reuses US-tied conversion goal | `0` | `NO` | Native-speaker review for es; enable approval; ROAS economics |
| `IT` | `PASS` storefront-localization checkout pass; EUR; localized policy/page copy clean | `absent` (`IT preview in-progress 0/0/0` per 2026-05-10 02:05 EDT recheck; no apply clicked) | `localized concept-ready (no native-speaker review)` for it | Reuses US-tied conversion goal | `0` | `NO` | IT preview must clear or be replaced with fresh `88/88 # OK`; native-speaker review for it; enable approval; ROAS economics |
| `RO` | `PASS`; RON (not EUR) confirmed; localized policy/page copy clean | `absent` (`not yet attempted` after IT preview block) | `localized concept-ready (no native-speaker review)` for ro | Reuses US-tied conversion goal | `0` | `NO` | Wait for IT preview lane clear; preview/apply `88/88 # OK`; native-speaker review for ro; enable approval; ROAS economics |
| `PT` | `PASS` 2026-05-08 PT cooldown retry; EUR, Standard `GRÁTIS`, Express `EUR 11.95`, total `EUR 24.95`, `pt-BR` | `absent` (`not yet attempted` after IT preview block) | `localized concept-ready (no native-speaker review)` for pt | Reuses US-tied conversion goal | `0` | `NO` | Wait for IT preview lane clear; preview/apply `88/88 # OK`; native-speaker review for pt; enable approval; ROAS economics |
| `PL` | `PASS` 2026-05-09; PLN, Standard `0.00 PLN`, Express `47.40 PLN`, `en-PL` UI | `absent` (`not yet attempted`; safest unattempted file to do first after IT preview clears) | `localized concept-ready (no native-speaker review)` for pl | Reuses US-tied conversion goal | `0` | `NO` | Wait for IT preview lane clear; preview/apply `88/88 # OK`; native-speaker review for pl; enable approval; ROAS economics |
| `CZ` | `PASS` 2026-05-09; CZK, Standard `0.00 CZK`, Express `272.13 CZK`, `en-CZ` UI | `absent` (`not yet attempted`; clean unattempted file) | `localized concept-ready (no native-speaker review)` for cs | Reuses US-tied conversion goal | `0` | `NO` | Wait for IT preview lane clear; preview/apply `88/88 # OK`; native-speaker review for cs; enable approval; ROAS economics |
| `GR` | `PASS` 2026-05-09; EUR, Standard `0.00 EUR`, Express `11.19 EUR`, `en-GR` UI | `absent` (`not yet attempted`; clean unattempted file) | `localized concept-ready (no native-speaker review)` for el | Reuses US-tied conversion goal | `0` | `NO` | Wait for IT preview lane clear; preview/apply `88/88 # OK`; native-speaker review for el; enable approval; ROAS economics |

## Smallest future spend unit recommended after approval

`GB / Mommy & Me Dresses - Exact only` at `$2/day` and CPC `$0.15`, conditional on:
- `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` held-CSV exclusion of handle `matching-family-beach-outfits-holiday-palm-tree-print-summer-dresses-shorts-set` continuing to hold (`0` bad-handle/forbidden hits in the held `1496`-row CSV / per-country split)
- Lane D `650%` ROAS economics: `$70` AOV, max CPA about `$10.77`, `$0.15` CPC needs about `1.39%` CVR, `$16` zero-purchase hard-pause rule applies

## Staged enablement order

1. `GB`
2. `CA`
3. `AU`
4. `ES`
5. `IT` (only after preview clears with fresh `88/88 # OK` apply and a campaign exists)
6. `RO`
7. `PT`

Reason: Tier 1 `GB`/`CA`/`AU` ship in English with checkout-to-shipping passes already in evidence and only need the same US-tied conversion goal plus an approved enable click. Tier 2 `ES`/`IT`/`RO`/`PT` require the native-reviewed romance-language pack to clear `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE` before any spend. Other markets (`CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `PL`, `CZ`, `GR`) sit behind the same native-copy gate plus, for `FR`/`BE`/`IT`/`PL`/`CZ`/`RO`/`PT`/`GR`, the upload/preview lane cleanup.

## Active blockers list (with problem IDs)

- `PROB-2026-05-09-NON-US-SEARCH-TEST-BUILD-GATE` (`P1`, `PARTIAL_9_APPLIED_REMAINING_BLOCKED_BY_FR_STALE_PREVIEW_BE_THROTTLE_IT_STILL_IN_PROGRESS_PREVIEW`): `FR`/`BE`/`IT`/`PL`/`CZ`/`RO`/`PT`/`GR` paused campaigns still absent; do not start more uploads while IT preview is in-progress at `0/0/0`.
- `PROB-2026-05-09-NON-US-SEARCH-NATIVE-LANGUAGE-COPY-GATE` (`P2`, `PARTIALLY_MITIGATED_LOCAL_OPTIONS_READY__OWNER_DECISION_REQUIRED`): `14` locale variants ready as concept copy with `0` forbidden-claim hits but no native-speaker review. Required before any non-English market is enabled.
- `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` (`P2`, `PARTIALLY_MITIGATED_LOCAL_ADS_HOLD__OWNER_APPROVAL_REQUIRED_FOR_SHOPIFY_FIX`): held Ads CSV currently excludes the bad handle. Live spend on any market remains conditional on the exclusion holding or the SEO/social metadata being repaired.
- `PROB-2026-05-08-PINTEREST-EVENT-QUALITY` (`P1`, `OWNER_APPROVAL_REQUIRED`): not a Search blocker but a parallel paid-growth gate; Pinterest live spend separately gated.
- `PROB-2026-05-08-MERCHANT-US-ES-AGE-GROUP` (`P2`, `OWNER_APPROVAL_REQUIRED_FOR_LIVE_FIX`): Merchant US/es feed-label diagnostic; not a Search blocker but flagged for parent integrator awareness.

## Guardrails preserved

- No live writes anywhere; local read-only synthesis only.
- No browser/account writes; no live URLs fetched.
- `ops/PROBLEM_TRACKER.md` not modified by this lane (parent integrates).
- No US campaign `23827590655`, PMax, Standard Shopping, Merchant, Shopify product-data, Pinterest, theme, product-scope, feed-label, product-group, conversion-goal, budget/bid/status-enable, or product/feed/conversion writes contemplated by this report.

## Files touched

- `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-10-paid-growth-orchestrator-safe-resume/lanes/market-activation/MARKET_ACTIVATION_SCORECARD.md` (this file, created).
