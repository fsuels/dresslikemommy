# Footer localization V8 — local proposal only

The saved September 11 MAIN observations in the Ads packet prove malformed Romanian/Dutch rendered headings and German/Greek/Finnish HTML-source headings. No new public request was made: the HTTP 429 stop remains active. A rendered post-change pass is **NOT RUN**.

## Source binding and what V7 already fixes

Parent-owned `source-before.json` and `source-comparison.json` bind all 527 immutable candidate files to uploaded V7, with no mismatches. Candidate footer MD5 is `0975d039b49a52684fd140064e639990`. Fresh private MAIN footer MD5 `f964264999c9a86a94eb9e20c5e87774` exactly matches `baseline/main/sections/footer.liquid`.

Compared with MAIN, V7 already provides Danish alias normalization, strict leading `t:` handling, invalid-translation/menu-title fallback, nonempty heading output, and cookie-preferences markup. Those changes do not recognize the newly observed aliases. `ro.json` already has native footer values; V7 `ro-RO/nl/de/el/fi` values are English. Alias correction therefore needs the parent's separate native locale overlays.

## Bounded proposal

Only `proposed/sections/footer.liquid` changes in this lane: **20 added lines**, extending the existing alias case with these ten tokens, normalized to canonical `sections.footer_headings` keys:

| Locale | Observed malformed key | Canonical key |
| --- | --- | --- |
| RO | `secțiuni.titluri_subsol.informații_companie` | `company_info` |
| RO | `secțiuni.titluri_subsol.ajutor_suport` | `help_support` |
| RO | `asistență_clienți` | `customer_care` |
| NL | `secties.voettekst_koppen.bedrijfsinformatie` | `company_info` |
| NL | `secties.voettekst_koppen.hulp_ondersteuning` | `help_support` |
| DE | `abschnitte.fußzeilen_überschriften.unternehmensinformationen` | `company_info` |
| DE | `abschnitte.footer_überschriften.hilfe_support` | `help_support` |
| EL | `τμήματα.υποσέλιδο_επικεφαλίδες.πληροφορίες_εταιρείας` | `company_info` |
| EL | `τμήματα.υποσέλιδο_επικεφαλίδες.εξυπηρέτηση_πελατών` | `customer_care` |
| FI | `sections.footer_headings.asiakaspalvelu` | `customer_care` |

Bare and leading-`t:` forms use the same existing normalization. No locale, product, settings, canonical or external writes occurred in this lane. Parent owns proposed locale edits. All footer bytes outside the alias case remain identical to V7, including disclosures and consent. Existing Danish aliases and custom headings are preserved.

## Validation

- Frozen prepatch selected suite: **10 failures / 4 passes**. After correction: **14/14**, with the same test hash.
- Complete suite with parent locale overlays: **15/15**. It executes assignments extracted from the production alias case and reads actual locale data; this is not Shopify Liquid rendering.
- Original eight-footer suite against immutable V7: **8/8**. New tests cover Danish, EN/ES/FR, Dutch/German/Greek literals, `Contact: us`, rich text and custom translation inputs.
- Independent whitespace checks passed; exact source comparison proves only the 20-line alias addition. No dependency installation or network use.

Run with the bundled Node runtime:

```sh
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --test dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/footer-localization.test.mjs
```

Frozen SHA256: footer `8e971b8940c4dacf273b57b3c4bbdb25c7799d7521aa7e81680006956d8ae8d6`; test `0c33dfbe511d8e74a7b73a62594d008e71d3020ba3743d73afe52ef4f0b93c4b`. Full Theme Check, independent review and actual rendered validation remain root-owned gates before any staging/publication decision.
