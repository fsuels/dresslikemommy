# Current draft source proof and preview expectations

**PASS — scoped current source verification**, September 6, 2026, **06:45:48 UTC**. This independent check is read-only. Root owns the browser preview and any release decision.

The structured Shopify read returned store `dresslikemommy-com.myshopify.com` / Dress Like Mommy, MAIN `133290917985` named `dresslikemommy/main`, and UNPUBLISHED `137782591585` named `DLM SEO DA NL 2026-09-06`. Both filtered four-file connections are complete, with zero file errors. All eight current checksums match the corresponding saved `danish_runtime_manifest_after.json` entries.

| Requested file | Current MAIN MD5 | Current draft MD5 | Comparison |
|---|---|---|---|
| `assets/cart.js` | `6303a25065e3d6757ea9dc9be25dac92` | `61c560a479ad1e32ec4e84d4bf685f09` | Both match saved source; draft differs as staged |
| `assets/product-desktop-ux-20260513-ruler-sync.js` | `61ded53111ee5002eb5c37b42a2c4b3f` | `379cc0f86d1ed46e357ceca745687c3e` | Both match saved source; draft differs as staged |
| `locales/da.json` | `9b050ed146a416020a0263972f5909a3` | `f501252517157f8ed92ca59a347b46e5` | Both match saved source; exactly two SEO leaf differences |
| `locales/nl.json` | `496897e8c972ba3685ece34aba094e4f` | `8c8aefb0ed28e7025f39c4c86443eaee` | Both match saved source; exactly two SEO leaf differences |

The six returned text bodies pass independent MD5 and byte-size checks. Current MAIN and draft cart text also match the exact bodies in `cart_draft_after_source.json` and the saved local after-files. Draft cart SHA256 is `e2fed4a6ae3abbba3b39d481dfee9eb755f623e7856b2d1c2a8747fe6c059cf7`, matching `cart_draft_execution.json`.

## Four SEO values to compare in the draft preview

These are exact current draft source values, checked against `traffic_seo_release.json`. They are metadata expectations, not proof of rendered HTML or rankings. Check the draft identity before comparing them; current MAIN still contains the previous values captured in the JSON readback.

| Route | Key | Exact expected value |
|---|---|---|
| `/da/collections/dresses` | `sections.collection_seo.meta_titles.dresses` | Kjoler til mor og datter \| Dress Like Mommy |
| `/da/collections/dresses` | `sections.collection_seo.meta_descriptions.dresses` | Find matchende kjoler til mor og datter. Se styles til familiebilleder, fester og ferier, og tjek størrelser og mål på produktsiden, før du vælger. |
| `/nl/collections/dresses` | `sections.collection_seo.meta_titles.dresses` | Jurken voor moeder en dochter \| Dress Like Mommy |
| `/nl/collections/dresses` | `sections.collection_seo.meta_descriptions.dresses` | Ontdek bijpassende jurken voor moeder en dochter. Bekijk stijlen voor familiefoto's, feestjes en vakanties en controleer de maten op de productpagina. |

## Five Danish purchase labels to compare

| Runtime key | Exact expected Danish value |
|---|---|
| `chooseRoleStep` | Vælg, hvem dette stykke tøj er til |
| `chooseOptionsStep` | Vælg størrelse og muligheder |
| `chooseRoleCta` | Vælg et familiemedlem |
| `addCurrentPiece` | Læg denne vare i indkøbskurven |
| `readyToAdd` | Klar til at lægge i kurven |

The five keys were independently extracted from the saved candidate's Danish dictionary and exactly match `danish_buyer_copy_checks.json`. The candidate MD5 matches the current draft server checksum; candidate SHA256 `964872eee1ecbbef337628e14bcd2336022ccffb1e8fdbe1bdd6e635c66b2d50` matches `danish_runtime_execution.json`. Both current runtime bodies were returned as `OnlineStoreThemeFileBodyUrl`. No runtime URL was requested or fetched, so this is checksum-bound source proof rather than newly returned runtime text. These labels may appear in different purchase-selection states; they are not expected to be simultaneously visible everywhere.

## Validation and limits

Followed structured schema discovery → official documentation search → GraphQL validation → read-only query. The structured validator and the Shopify skill validation script both returned VALID. The skill's initial standalone search script returned `fetch failed`; the official structured documentation search succeeded. No authentication, schema or policy failure occurred in the executed query. Relevant docs: [theme query](https://shopify.dev/docs/api/admin-graphql/2026-07/queries/theme) and [theme file checksum/body fields](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/OnlineStoreThemeFile).

**This refresh covers four named files per theme only. A current full 525-file manifest comparison was NOT RUN.** Other current theme drift and include/dependency changes are unknown in this scope. Historical full-manifest proof remains historical. Browser rendering, mobile behavior, selected-country cookies, checkout, product measurement truth, publication and sales lift were not verified by this subagent. No browser action, credential read, external mutation, product/order/customer query or edit outside the two assigned artifacts occurred.

Evidence: `draft_preview_source_readback.json` retains the validated operation, current identity/checksum results, source artifact hashes, exact expectations and scope limits. Next action: root compares the authenticated draft preview against these values and the saved cart behavior. Continue through the [canonical paid-growth prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md); this file is a scoped verifier receipt, not a new operating plan or release authorization.
