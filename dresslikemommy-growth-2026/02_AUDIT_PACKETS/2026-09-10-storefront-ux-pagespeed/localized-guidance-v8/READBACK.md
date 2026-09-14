# V8 local footer and Romanian guidance repairs

Confidence: H for the bounded source changes and local checks; rendered acceptance is BLOCKED by the active public HTTP 429 stop.

V8 is IMPLEMENTED locally in seven proposed files. **The overall live UX outcome remains unfinished.** V8 has not been uploaded or published. The existing 527-file V7 candidate and uploaded UNPUBLISHED theme **137888792673** remain unchanged. The current V7 release manifests in the parent packet still describe V7. No new draft theme was created.

## Findings and changes

| Verified finding | Existing V7 behavior | New local V8 change |
|---|---|---|
| MAIN Romanian and Dutch collection footers expose translation keys; successful German, Greek and Finnish source responses show related malformed headings. | Ten proved aliases are absent. The earlier Danish repair is already present. | Add ten exact aliases in `sections/footer.liquid`, mapping them to the existing canonical company/help/customer-care keys. Preserve intentional literal headings and all surrounding markup. |
| Canonical footer labels in NL/DE/EL/FI and regional RO locale files are English. | Canonical Romanian `ro.json` footer labels are already Romanian. | Translate three footer labels in each of five locale files: 15 values total. |
| MAIN Romanian Together Heart displays English role/size/return/security labels. | The actual V7 runtime already returns Romanian role/size/add/ready labels; V7 `ro.json` already has qualified Romanian returns. Seven payment/privacy/policy-link values remain English. | Translate only those seven remaining `ro.json` values. No JavaScript or product-content change. |

The seven files are `sections/footer.liquid`, `locales/nl.json`, `locales/de.json`, `locales/el.json`, `locales/fi.json`, `locales/ro-RO.json`, and `locales/ro.json`. The footer diff is 20 added lines; the locale diff is exactly 22 changed values. See [proposal.diff](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/proposal.diff) and [locale-changes.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/locale-changes.json) for exact before/after text.

Return eligibility, deadlines, exclusions, amounts, policy URLs, placeholders, product descriptions, size charts, prices, reviews, consent and tracking code are preserved. The security translations retain the existing English claims; they do not certify any payment-provider acceptance.

## Evidence and verification

- Private Admin source read at **2026-09-11 19:01:42 UTC**: preview 137888792673 is UNPUBLISHED, processing=false, 527 files; MAIN 133290917985 has 525 files; predecessor 137881223265 is UNPUBLISHED with 527 files. All three manifests match the final V7 readback. All 527 local V7 files match the fresh preview hashes and sizes.
- Exactly **7 changed / 520 preserved** versus V7 in the local composite. If later applied, the proposal would have 25 cumulative differences from the predecessor and 61 differences from captured MAIN. These are proposed counts, not an applied release.
- Full 527-file local composite: Shopify `theme check --output json` returned exit 0 and `[]` diagnostics.
- Footer suite **15/15 PASS**; Romanian source/runtime suite **21/21 PASS**; existing V7 footer holdouts **8/8 PASS**. Total **44/44 PASS**.
- Frozen footer cases: the same selected test source produced **10 failures / 4 passes before**, then **14 passes after**. The footer harness executes parsed production alias assignments; it is not a Shopify Liquid renderer. The Romanian harness executes the actual V7 JavaScript in jsdom; it is not a storefront browser test.
- Seven original files are saved under `rollback/`, byte-matched to the captured V7 source. [proposed-manifest.json](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-10-storefront-ux-pagespeed/localized-guidance-v8/proposed-manifest.json) records every before/after digest plus the complete local composite manifest. No external apply payload was executed.
- Independent source review **PASS** and evidence integrity are recorded in `INDEPENDENT_REVIEW.md`, `independent-review.json` and `VALIDATION.json`.

The original defects are grounded in the Ads owner's saved [rendered RO/NL capture](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/root_landing_qa/ROOT_RENDERED.json) and [footer source diagnosis](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/landing_qa/footer_diagnosis.json). Those captures are bound to MAIN, US/USD. Language routes do not establish destination-country checkout behavior. The RO mobile capture proves no DOM overflow but is not a valid full visual pass.

Shared-record closeout passed after the parent task's explicit handback. Only the existing UX row, additive notes in the two existing problems and one worklog append changed. All other coordination/problem/worklog bytes and all 26 marketing files were preserved. Strict continuity, integration and scoped whitespace checks passed. The anchor is `2026-09-11-storefront-v7-publication-gate-and-v8-local-review`; exact receipt and before-state hashes are in `canonical-closeout.json` and `canonical-preservation.json`. The owner's current priority is the existing V7 Admin publication; V8 remains local and unapplied.

Five fresh MAIN text files were independently checksum-bound in `source/main/`. MAIN runtime is available only as `OnlineStoreThemeFileBodyUrl` metadata in this read; its contents were not fetched. A different runtime checksum alone does not prove the cause of its English labels.

## Remaining gates

**Rendered V8 desktop/mobile acceptance, preview upload, publication, checkout/payment acceptance, fresh PageSpeed results and conversion impact are NOT verified.** No public requests or external writes occurred in this V8 continuation. The public HTTP 429 stop remains active; elapsed time alone does not clear it, and alternate browsers/routes/downloads must not bypass it.

Regional `ro-RO.json` purchase-confidence/returns values still include English because this regional file's change is restricted to its three footer labels. Romanian runtime fallback does not repair that server-side JSON. The coordinating Ads owner's saved [current locale inventory](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-11-google-ads-signup-tag/ongoing/markets/locale_routes.csv) from 18:41–18:42 UTC contains `ro`, not `ro-RO`. The regional English is therefore a potential coverage gap, not another proved current Romanian route failure. Broader locale coverage, review-widget text, Japanese/Arabic size guidance, policy-modal content and Amazon Pay acceptance remain separate open work. These changes do not establish that the site is perfect or that conversion has improved.

The next action is a bounded unpublished-preview verification after an actual access-condition change, because local checks cannot confirm what shoppers see. Re-read the exact preview/MAIN/predecessor sources and reconcile intervening changes before a separately authorized seven-file upload to the **same existing theme 137888792673**. Verify its full source readback, RO/NL desktop/mobile, the proved DE/EL/FI footer cases, and DA/EN/ES/FR holdouts. Once accepted, complete supported owner Admin publication and public regression/PageSpeed testing. The connector's MAIN/publication restriction remains binding. Stop on the first throttle, authentication or policy gate. Preserve V7 and its owner publication gate until that process is complete.

Continuation prompt: “Continue the existing V8 footer/Romanian repair from READBACK.md. Preserve uploaded V7. Confirm the public-access gate has actually cleared, recheck all source hashes, and complete the bounded unpublished-preview verification without broadening product, policy, payment or publication scope.”
