All 67 confirmed-missing Swedish `body_html` fields are manually translated in `candidate.json` (36,634 visible English source words). The final release-review files are `final_batch_01.json` through `final_batch_14.json`; `final_manifest.json` binds their hashes. Earlier `candidate_batch_*` files are superseded progress checkpoints.

The translation uses 1,502 manually authored exact text-node translations, including four explicitly translated recurring prose templates and 173 manually translated product-name fragments. It never calls a provider, browser, or API. Raw HTML tags and every attribute value remain unchanged. Whitespace before punctuation is adjusted where Swedish clause order crosses an inline link. No body is shortened or summarized. Source product-name truncations are retained rather than guessed.

Verification performed:

- 67/67 local raw-export source values, returned Shopify digests, source hashes and raw-file hashes match. All 67 exact `sv` + `body_html` + `market:null` translations are absent in the source export; candidates bind `before:null`.
- 67/67 independent helper checks pass for tag/attribute structure, links, numeric values, units, table cells/size labels, and Liquid tokens. Existing helper regression suite: 13 tests passed.
- All 1,502 unique source text nodes have manual Swedish values. Seven exact unchanged nodes consist of punctuation, Instagram, Pinterest, Dress Like Mommy, and `Son:` (also Swedish).
- Author pass examined assembled inline-link prose in all distinct long-form guide layouts and corrected missing spaces, duplicate matching language, name-truncation expansion and one singular/plural garment phrase. No words attach directly after closing inline tags; identified bad-join checks now return zero.

Independent meaning review remains required. These local checks do not establish live Shopify freshness or certify source product claims. `source_claim_holds.json` records 159 exact source segments across 58 articles needing source-owner review, including unqualified free-shipping/satisfaction promises, UPF50+, claims of testing/research/reviews, sales/stock/pricing claims and broad sizing/care advice. The translations preserve those source claims faithfully; no English source or product fact was changed. The existing Halloween editorial hold is retained. If the parent corrects English source facts, use a new source digest and correspondingly reviewed Swedish changes before publication.

Ownership was limited to this artifact directory. No Git/index/refs, theme files, inventory, routing, marketing negatives, canonical state, external provider, or live Shopify writes were changed.
