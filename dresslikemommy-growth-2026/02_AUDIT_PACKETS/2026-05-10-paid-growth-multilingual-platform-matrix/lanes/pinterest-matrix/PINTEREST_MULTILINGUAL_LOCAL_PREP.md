# Pinterest Multilingual Local Prep

Generated: 2026-05-10

Mode: local/read-only planning artifact. No Pinterest account write, catalog source edit, campaign draft, product group, tag/CAPI, audience, budget, bid, status, or spend action was made.

## Current Pinterest Truth

Only `US / en-US` has a clean scoped Pinterest path in current evidence:

- Advertiser: `549756244483`
- Catalog: `Catalog_Retail` / `3041764155561548387`
- Allowed source/feed profile: `3041760867124595727`
- Blocked source/feed profile: `3041760916127467912`
- Clean scope: `342` EN-US in-stock rows
- Exclusions: `41878208249953`, `41878208479329`, `41878208577633`, `41878208610401`
- Review-only templates: product groups, campaign/adgroup, promoted pin copy, QA checklist
- Event Quality: `Fair`

No non-US Pinterest catalog scope, per-country product-group template, localized catalog source proof, paused campaign template, or per-country Pinterest readback artifact was found.

## Per-Market Local Prep Requirements

| Market | Locale | Current Pinterest state | Local artifact needed before any approval request |
|---|---|---|---|
| `GB` | `en-GB` | Not built | Build local GB catalog-source proof, clean item scope, product-group template, copy template, and readback checklist after US gate |
| `CA` | `en-CA` | Not built | Build local CA scope; decide whether Canada remains English-first or needs French-Canada copy later |
| `AU` | `en-AU` | Not built | Build local AU scope and English-first copy/template packet |
| `CH` | `en-CH` first | Not built | Decide whether Pinterest test is English-first or split by German/French/Italian; then build source/scope packet |
| `DK` | `da-DK` | Not built | Build DK source/scope packet; native review needed before localized copy use |
| `DE` | `de-DE` | Not built | Build DE source/scope packet; verify localized catalog/source health and native review |
| `NL` | `nl-NL` | Not built | Build NL source/scope packet; native review and landing-language QA |
| `SE` | `sv-SE` | Not built | Build SE source/scope packet; native review and landing-language QA |
| `FR` | `fr-FR` | Not built | Build FR source/scope packet; native review; keep separate from Google Ads FR parked state |
| `BE` | `fr-BE`, `nl-BE` | Not built | Owner decision on FR/NL split, then build BE source/scope packet |
| `ES` | `es-ES` | Copy-only | Build ES catalog/source proof and product-group template; native review |
| `IT` | `it-IT` | Copy-only | Build IT catalog/source proof and product-group template; native review |
| `PL` | `pl-PL` | Not built | Build PL source/scope packet; native review |
| `CZ` | `cs-CZ` | Not built | Build CZ source/scope packet; native review and source-health proof |
| `RO` | `ro-RO` | Copy-only | Build RO source/scope packet; factor RON economics into guardrails |
| `PT` | `pt-PT` | Copy-only | Build PT source/scope packet; resolve storefront `pt-BR` behavior before pt-PT copy use |
| `GR` | `el-GR` | Not built | Build GR source/scope packet; native review and source-health proof |

## Approval Boundary

The canonical prompt authorizes only approval-gated paused US Pinterest drafts. It does not authorize multilingual Pinterest drafts or account objects.

Before any non-US Pinterest account action, the parent should create a dated local packet for that market with:

- Catalog/source ID and locale proof.
- Clean item scope and explicit exclusions.
- Product group definitions.
- Claim-safe copy.
- Event Quality and tag/CAPI impact check.
- Pre/post readback checklist.
- Exact owner approval phrase.

## Exact Next Unblock

Choose one of these next paths:

1. Get exact approval for the paused US Pinterest draft build from the canonical prompt.
2. Get exact approval for read-only Pinterest Event Quality and official app reconfirmation.
3. If the owner wants non-US Pinterest next, build one local-only country packet first, recommended order `GB`, then `CA`, then `AU`, then the strongest reviewed localized market.
