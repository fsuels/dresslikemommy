# Multilingual Google Ads And Pinterest Execution Matrix

Generated: 2026-05-10

Mode: local/read-only synthesis. No live account write was made.

## Scope Rule

The canonical non-US Google Search target set has 17 countries: `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, and `GR`.

Google Ads has English-first split CSVs for all 17 and native-language copy options for 14 locale variants: `es-ES`, `it-IT`, `pt-PT`, `ro-RO`, `de-DE`, `nl-NL`, `fr-FR`, `fr-BE`, `nl-BE`, `sv-SE`, `da-DK`, `pl-PL`, `cs-CZ`, and `el-GR`.

Pinterest currently has a clean US `en-US` catalog scope only. There is no completed non-US or multilingual Pinterest account setup in the repo evidence.

## Matrix

| Market | Primary locale(s) | Google Ads status | Google Ads safe extent now | Pinterest status | Pinterest safe extent now | Gate / next unblock action |
|---|---|---|---|---|---|---|
| `US` | `en-US` | Existing Standard Shopping live guarded; US nonbrand Search paused infra exists separately | Monitor only; do not change Standard Shopping; US nonbrand enable is separate approval | Clean Pinterest US `en-US` 342-row scope and review-only paused-draft templates exist | Local templates complete; no account draft created in this session | Pinterest paused US draft needs exact owner approval; live spend also needs Event Quality risk decision |
| `GB` | `en-GB` | Built/read back clean: `23838895360`, paused Search, `$2/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated; no local country-specific Pinterest catalog/draft artifact | Measurement purchase proof plus exact owner approval before any Google enable; Pinterest international setup requires separate owner-approved plan after US/Event Quality gate |
| `CA` | `en-CA` | Built/read back clean: `23834423669`, paused Search, `$2/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Same as GB; CA is candidate after GB proof |
| `AU` | `en-AU` | Built/read back clean: `23834424182`, paused Search, `$2/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Same as GB; AU is candidate after GB proof |
| `CH` | `en-CH` first; possible `de/fr/it` future split not prepared | Built/read back clean: `23834425358`, paused Search, `$1/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Native/language-market split decision plus measurement and exact enable approval |
| `DK` | `en-DK` first; `da-DK` local copy option exists | Built/read back clean: `23838969244`, paused Search, `$1/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Danish copy needs native review; row flagged for wording review; measurement and exact enable approval |
| `DE` | `en-DE` first; `de-DE` local copy option exists | Built/read back clean: `23834427575`, paused Search, `$1/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | German copy native review and landing QA before local-language platform use |
| `NL` | `en-NL` first; `nl-NL` local copy option exists | Built/read back clean: `23829110118`, paused Search, `$1/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Dutch copy native review and landing QA before local-language platform use |
| `SE` | `en-SE` first; `sv-SE` local copy option exists | Built/read back clean: `23838970036`, paused Search, `$1/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Swedish copy native review and landing QA before local-language platform use |
| `ES` | `en-ES` first; `es-ES` local copy option exists | Built/read back clean: `23829133584`, paused Search, `$1/day`, presence-only, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Spanish copy native review and landing QA before local-language platform use |
| `IT` | `en-IT` first; `it-IT` local copy option exists | Built/read back clean: `23829232530`, paused Search, `$1/day`, presence-only after repair, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Italian copy native review and landing QA before local-language platform use |
| `PL` | `en-PL` first; `pl-PL` local copy option exists | Built/read back clean: `23829238698`, paused Search, `$1/day`, presence-only after repair, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Polish copy native review and landing QA before local-language platform use |
| `CZ` | `en-CZ` first; `cs-CZ` local copy option exists | Built/read back clean: `23829253812`, paused Search, `$1/day`, presence-only after repair, content/YouTube off | Completed to safe paused-infra extent; no enable | No non-US Pinterest setup | Marked gated | Czech copy native review and landing QA before local-language platform use |
| `RO` | `en-RO` first; `ro-RO` local copy option exists | Absent/uncreated; local split CSV passes guardrails, but prior RO preview became stale/not visible | Local artifact ready only; no new account object under current stricter no budget/bid/status guardrail | No non-US Pinterest setup | Marked gated | Exact owner branch approval to retry RO or skip/park RO; native review before local-language use |
| `PT` | `en-PT` first; `pt-PT` copy exists but storefront showed `pt-BR` behavior | Absent/uncreated; local split CSV passes guardrails; not attempted because RO branch unresolved | Local artifact ready only; no new account object under current stricter guardrail | No non-US Pinterest setup | Marked gated | Resolve RO branch first or exact owner approval to skip RO; Portugal wording/language behavior review required |
| `GR` | `en-GR` first; `el-GR` local copy option exists | Absent/uncreated; local split CSV passes guardrails; not attempted because RO branch unresolved | Local artifact ready only; no new account object under current stricter guardrail | No non-US Pinterest setup | Marked gated | Resolve RO/PT sequence first; Greek copy native review and landing QA before local-language use |
| `FR` | `en-FR` first; `fr-FR` local copy option exists | Parked; no campaign; prior stale/in-progress or completed-with-errors/no-changes path requires fresh non-stale preview and no-duplicate readback | Local split CSV ready only; no account action in this session | No non-US Pinterest setup | Marked gated | Fresh non-stale `88/88 # OK` preview and no-duplicate readback after RO/PT/GR direction |
| `BE` | `en-BE` first; `fr-BE` and `nl-BE` copy options exist | Parked; no campaign; upload-throttle history | Local split CSV ready only; no account action in this session | No non-US Pinterest setup | Marked gated | Upload-throttle cooldown, Belgium FR/NL split decision, then fresh preview/readback |

## Google Ads Local Artifact Verification

All 17 per-country split CSVs exist under:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-localized-copy-pinterest-manifest-safe-advance/lanes/google-ads-split-manifest/split_csvs/`

Fresh local parse this session confirmed every split file has:

- `88` data rows.
- Row type mix: `1` Campaign, `10` Ad group, `30` Keyword, `37` Negative keyword, `10` Ad.
- All importable statuses `Paused`.
- `40` country-qualified final URL rows.
- Max default CPC at or below `$0.15` (`$0.10` for `PL/CZ/RO/PT/GR`, `$0.12` for most other `$1/day` markets, `$0.15` for `GB/CA/AU`).
- `0` forbidden hits for `PMax`, `Performance Max`, `Standard Shopping`, `Shopping`, `conversion-goal`, `product-scope`, `feed-label`, `product-group`, `Vacation Family`, or the stale beach handle.

## Pinterest Local Artifact Verification

Current Pinterest local artifacts are US-only:

- Clean catalog scope: `342` EN-US rows.
- Exclusions: `4` variants (`41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`).
- Catalog: `Catalog_Retail` / `3041764155561548387`.
- Allowed source/feed profile: `3041760867124595727`.
- Blocked source/feed profile: `3041760916127467912`.
- Review-only local templates: product groups, campaign/adgroup template, promoted pin copy, QA checklist.
- Event Quality remains `Fair`.

No evidence was found that Pinterest has completed per-country multilingual catalog, ad, campaign, product-group, locale, or account readback artifacts for `GB`, `CA`, `AU`, `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`, `PL`, `CZ`, `RO`, `PT`, or `GR`.

## Completion Interpretation

Under the stricter current guardrails, Google Ads is complete to the safe local/read-only/previously-approved paused-readback extent for 12 markets, local-only prepared for 3 absent markets, and explicitly gated for 2 parked markets.

Pinterest is complete only to the safe local/read-only US draft-template extent. Every non-US Pinterest language/country cell is gated, because creating drafts or account objects may require campaign/product-group/budget/bid/status/account setup actions and the canonical prompt does not contain fresh Pinterest multilingual approval.
