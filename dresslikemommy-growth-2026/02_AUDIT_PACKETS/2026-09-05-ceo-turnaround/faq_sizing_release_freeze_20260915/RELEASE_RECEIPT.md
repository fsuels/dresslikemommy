# FAQ sizing correction — live release

Three conflicting sizing answers are corrected in English and all 17 existing global FAQ body translations. The guidance uses the selected product’s size chart and measurement units, avoids fixed size conversions, and directs shoppers to support when measurements are unclear. Each language links to its verified sizing guide.

Target: Page **161933381**, [FAQ](https://www.dresslikemommy.com/pages/faqs). Action: **TA06-FAQ-SIZING-TRUTH-20260914**.

## Exact release

- English pageUpdate succeeded once at **2026-09-15 00:23:51 UTC**.
- One translationsRegister succeeded for 17 existing bodies at **00:26:57–58 UTC**.
- Both returned zero user errors. No retry or rollback was executed.
- English body and source digest: `5256c9db16de36e4410d1981f46b02acd5d802fd9a19e01edb357ebe3441324b`.
- The previous native-disclosure body and every translation are preserved under before/; guarded rollback restores changed translations first and English last.

Independent before-review confirms exactly **54 paragraph changes** across 18 bodies. All other bytes, eight native controls per body, question labels and unrelated links remain exact. The current FAQ source has 12 links in English and 11 in each translated body; those counts are preserved.

## Verification

- Independent after-review **PASS_WITH_LIMITS**, SHA256 `00bf3e8dff414fa10c02cb36612bcee42939a1eace72df27e1ca8c4cf5e284c5`.
- Fresh API comparison passes for all 18 candidate bodies, 19 translated titles, protected page fields, source keys, all 21 locales and six markets. All 130 absent body-translation scopes remain absent.
- Public checks pass for 19 language/viewport cases: English desktop and mobile, plus all 17 repaired languages at 390 pixels. All 57 repaired answer observations match reviewed copy and are visible when opened; all 19 guide links reached the exact localized article.
- Native controls open and close; English keyboard activation passes. No horizontal overflow or captured browser warnings/errors.
- English mobile, Arabic mobile and English desktop screenshots were visually checked.
- The task’s tab was closed, viewport reset and Canada/CAD/cart 0 preserved. No country, basket, checkout, product, theme or paid-media action occurred.

The original intermediate check stopped when Shopify changed both translation timestamps and outdated flags after the English edit. Independent raw comparison confirmed that only those two fields changed, each timestamp exactly matched the page update, and every translation value and title was unchanged. A fresh strict source check passed before registration. The original failed check and independent reconciliation are retained.

A Danish link locator twice left the FAQ visible. Direct activation of the fresh accessibility link succeeded; the complete flow passed after switching the automation method. No storefront change was made for that recovery.

Language review is model-based, not native-human certification. Other FAQ business/policy statements remain unreviewed. Arabic/Hebrew retain the existing FAQ LTR layout; PL/RU/SV retain English body fallback. No PageSpeed score, browser-engine coverage or conversion lift is claimed.

## Separate read-only findings

The article shopping button remains dark text on a dark background in English, Arabic and Dutch. Source review binds this to the .rte a rule overriding button text color in both current MAIN and candidate. A minimal scoped CSS proposal is in diagnostics/source/SOURCE_DIAGNOSIS.md; no theme change was made.

All 12 French findings are reconciled there. Preserve the four already-prepared candidate controls; the remaining theme corrections include accessible size labels, cart tax/shipping text and both sources of the selector heading. Product-owned size-range wording, the typo and two Hip chart labels stay with the existing Merchant owner. All numeric measurements, variants and Ads editor 2 are outside this release.

## Git and publication

The earlier main synchronization remains partial: local main holds the reviewed theme fixes, while 72 theme-file differences remain held from GitHub because that branch controls live theme 133290917985. This continuation made no Git writes. Fresh Shopify readback still shows candidate **DLM UX Performance QA 2026-09-10 (137888792673)** as UNPUBLISHED.

The existing owner action is to publish that reviewed theme in Shopify Admin, preserving the previous theme for rollback. The connector’s live-theme/publication restriction cannot be bypassed through GitHub main.

Parent task 01a08223 owns shared canonical integration; this disjoint packet is the handoff. Continue from the final frozen manifest and independent after-review, preserve this completed FAQ release, then verify the published theme and finish the remaining main synchronization when the publication dependency clears.

