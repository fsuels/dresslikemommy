Confidence: H for captured source defects; M for cause and proposed repair until current Shopify source/translation records are bound.

The useful finding is a **P1 footer translation defect**, linked to existing `PROB-2026-07-02-LOCALIZED-PDP-ENGLISH-LEAKAGE` and the earlier Spanish footer case. It is not a new empty-collection or country-currency finding.

| Locale | Exact public collection URL | Source evidence |
|---|---|---|
| Danish | https://www.dresslikemommy.com/da/collections/mommy-and-me | `sektioner.fodtekst_overskrifter.firma_info`; missing `kundeservice` translation |
| German | https://www.dresslikemommy.com/de/collections/mommy-and-me | `Abschnitte.Fußzeilen_Überschriften.Unternehmensinformationen`; `Abschnitte.Footer_Überschriften.Hilfe_Support` |
| Greek | https://www.dresslikemommy.com/el/collections/mommy-and-me | Two localized dotted footer identifiers |
| Finnish | https://www.dresslikemommy.com/fi/collections/mommy-and-me | `Translation missing: fi.sections.footer_headings.asiakaspalvelu` |

[Exact headings, source receipts and local source hashes](footer_diagnosis.json) preserve all seven malformed headings. The parent separately rendered Romanian and Dutch footer failures; this subagent could not independently render them. Root owns its `ongoing/root_landing_qa` receipt.

The local footer translates arbitrary `t:` block headings and otherwise prints literals. Its three configured block headings are canonical translation keys. Romanian already has readable canonical footer values; Dutch local values remain English. This is consistent with localized admin heading values having corrupted identifiers. The existing UX candidate handles two Danish aliases and selected invalid prefixes; that does not certify other localized identifier families. Exact live source/translation cause remains unverified.

**Proposed narrow correction:** the existing UX owner should bind current candidate source and the three affected heading records, preserve canonical identifiers, resolve known footer roles to their translation keys, and repair only proved malformed values/aliases. Preserve custom literal/rich-text headings and all other menus/settings. Extend existing EN/ES/DA holdouts with RO/NL/DE/EL/FI cases. Native Dutch wording remains a separate review. Nothing was applied to theme, locale or admin data.

Coverage is partial: nine collection source reads returned200—AR/CS/DA/DE/EL/EN/ES/FI/FR—with exact canonical/language, MAIN133290917985, US context/USD and36 main product links each. Twelve returned429; no deep product read succeeded. An earlier Romanian probe returned200 with correct basic metadata. Source does not certify layout, product selection, translated content, checkout or country/payment acceptance.

The [chronology](http_throttle_chronology.json) records an audit-runner defect: after the first429 at18:54:58.194251UTC,11 queued collection requests and1 product request were still dispatched. French alone was already in flight. Original receipts and the executed runner are preserved. Further public requests stopped; a corrected global stop passed [synthetic tests](local_guard_validation.json) without network access. No browser tab was created in this runtime.

Next action: integrate the exact footer cases into the existing UX owner’s repair and rendered acceptance work. Use the existing [canonical continuation prompt](../../../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md); do not rerun the throttled batch automatically.
