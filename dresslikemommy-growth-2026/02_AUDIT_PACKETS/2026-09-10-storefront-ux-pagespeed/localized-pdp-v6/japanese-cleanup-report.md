# Japanese PDP cleanup repair

IMPLEMENTED and locally VERIFIED. Candidate source matched the fresh preview/MAIN/combined MD5 `44243cbf23a0b608fe400a5c5a48db2b` before editing.

The cleanup snippet added four lines. The canonical HTML language now exempts Japanese, Chinese and Korean locales (including regional tags) from blanket CJK/punctuation deletion. Explicit English vendor-credit removal still runs; existing admin-artifact, internal-label and other copy cleanup remains unchanged. No product data or table changes.

Before the patch, frozen actual-script jsdom fixtures produced **6 failures / 8 passes**, reproducing Japanese paragraphs exactly as `Together。。`, `11。。。`, and `、、、。。`. The unchanged fixtures now produce **14 passes / 0 failures**. Coverage includes exact saved Japanese paragraphs, EN/FR/AR/KO holdouts, five exact saved localized tables, native CJK/regional-tag markup, non-CJK vendor-token removal, and admin-artifact removal. French retains the existing space-before-semicolon normalization. Saved product bodies are bound to SHA256 values in the fixture file.

Validation command (run from repository root):

```sh
/Users/fsuels/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --test dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-pdp-v6/japanese-cleanup.test.mjs
```

Extracted script `node --check`, independent `git diff --no-index --check`, and exact four-line-only source comparison passed. Existing jsdom dependency was reused; no dependency installed.

Frozen SHA256:

- `candidate/snippets/pdp-description-copy-cleanup.liquid`: `04997bf4d29704d478115fac5e6588772e460e04eccffa0f6cd3e712d80e2219`
- `localized-pdp-v6/japanese-cleanup.test.mjs`: `b5440b009cab53b9b6e12abffa7d86b1f2491e7472bdd6fb46c5aad8ad33cd46`

Full Theme Check, independent review, preview staging and real-browser verification remain parent-owned. No external action was performed in this lane.
