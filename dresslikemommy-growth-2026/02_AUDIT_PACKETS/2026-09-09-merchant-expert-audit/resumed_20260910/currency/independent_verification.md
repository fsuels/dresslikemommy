Confidence: H — **PASS_WITH_LIMITS**. Reviewed 2026-09-10T00:46:39.113Z.

Six ACTIVE markets contain 68 country memberships and **65 unique countries**; AU, CA and GB overlap. All 19 queried connections have complete pagination. Independently parsing the separate root-retained MAIN menu read (2026-09-10T00:43:21.095Z) produces **130 rows, 65 countries, two occurrences each and zero currency conflicts**, exactly matching the earlier saved map.

All 65 correctly bound contextual-pricing aliases return a price for variant **41498026442849**. Recalculation reproduces **63 currency matches** and only **NO/RU differences: public menu USD versus Admin EUR 17.95**. The Admin query window is 00:36:58–00:37:02 UTC.

The unchanged [country selector](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/release_candidate/theme/snippets/country-localization.liquid:149) displays Shopify-provided currency. Its [click handler](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/release_candidate/theme/assets/localization-form.js:105) submits the selected country code; isolated executions of the actual handler submit NO/RU once without remapping. Both files match baseline and the fresh 00:29:11 UTC MAIN/UNPUBLISHED manifests by MD5 and size. Full SHA-256 bindings are in the [machine report](/Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-09-merchant-expert-audit/resumed_20260910/currency/independent_verification.json). **16 narrow checks passed.**

No theme currency override is supported by these observations. Changing a label would not establish Shopify's actual selling or checkout currency. The cause remains unresolved.

Limits: the market source lacks an exact query timestamp; 00:34:05 UTC is persistence time. Raw menu retention was a separate root browser read, independently parsed here. US/en remained selected; these are available-menu labels and one variant's Admin contexts, not 65 selected landing, checkout, payment or Merchant receiver checks. No profit or serving proof follows. This reviewer performed no browser/API calls, external writes or source edits.

Next: root should resolve NO/RU using authorized selected-country, checkout and relevant Shopify settings evidence before proposing a correction. Continuation: “Resolve NO/RU selling-currency disagreement using the recorded evidence limits; preserve the unpublished release.”
