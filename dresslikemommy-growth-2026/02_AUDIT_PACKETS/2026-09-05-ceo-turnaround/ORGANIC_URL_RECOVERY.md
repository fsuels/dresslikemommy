# Organic URL recovery: current evidence and decision

## September 6 exact server-error follow-up

**TA-05: the missing 12 server-error examples are recovered; no live repair is qualified.** Root read all 12 original URLs and crawl dates from the correct Search Console property. The indexing report remains dated August 27; five examples were last crawled June 24 and seven June 3. This is a current UI read of old observations, not a fresh Google crawl. All query strings are empty. The complete visible table is preserved in gsc_server_error_examples_current.json; it is not a downloaded export or a guarantee of every possible affected URL.

| Exact current result | Count | Shopify source/configuration evidence | Decision |
|---|---:|---|---|
| HTTP 404, archived product | 7 URLs / 7 products | ARCHIVED and no Online Store URL | Archival intent, valuable demand and equivalent replacements remain unknown; no restoration or broad redirect |
| HTTP 404, active cartoon pajamas | 2 URLs / 1 product | Product7228788867169 ACTIVE; exact vi/th locale codes absent from enabled locales | Current path/configuration mismatch; no evidence to republish languages or choose a replacement locale |
| HTTP 404, published swimsuit article | 1 | Article559662071905 published; tr locale absent | Same locale/demand/equivalence gate |
| HTTP 429 verification response, sizing article | 1 | Article559700574305 published; tr locale absent | Public reader stopped immediately; content, historical cause and Googlebot behavior remain unresolved |
| Portuguese collection Atom URL | 1 | Base collection353856880737 published; pt absent, pt-BR published | Public request NOT RUN after429; .atom kept intact, no alias/feed-response inference |

Shopify returned 21 enabled locales, all published, with English primary. Exact vi, th, tr, id and pt are absent; fi, hi, ja and sv are published. These are current configuration facts, not proof of when or why a locale changed, market routing, or the cause of June5xx responses. The .atom source is a derived base-collection lookup only. Product/article publication does not establish a successful localized buyer journey.

The separate Google Crawl Stats read, last updated September3, shows 326K requests over its displayed last90days, 87%200, 12%404 and <1%5xx. Those values are rounded and only five of nine response categories were read. Host status records earlier problems and acceptable recent server connectivity; robots.txt fetch and DNS fail rates are acceptable. It does not establish whole-site uptime now. No daily incident dates were readable from the expanded accessibility panel.

**Chosen action: hold this cohort with evidence and continue the prepared organic release.** None of the ten complete public responses reproduced5xx, but429 and the untested Atom URL prevent an all-fixed claim or Validate Fix. No public retry, alternative access path, Google live test, validation/indexing request, redirect, locale, product, theme, feed or paid change followed. The public429 is not evidence that Googlebot received429. Google recommends correcting known instances before validation; its crawl and indexing reports have distinct scopes. [Google indexing/validation guidance](https://support.google.com/webmasters/answer/7440203#validation)

Reopen these exact examples only if changed current Google evidence identifies an active published-locale failure; valuable search/internal/referring-link demand and an equivalent destination qualify a repair; or documented mistaken resource/language withdrawal establishes an approved restoration scope. Do not repeat this or the prior four-path sample. Original full404 Examples and path-level demand remain a separate unresolved gate. The single owner action remains the exact four-file draft review/publication in DRAFT_RELEASE_REVIEW.md; Google support/Greek approval/paid economics gates retain their existing status. No indexing, traffic, purchase or profit lift is claimed.

Evidence: gsc_server_error_public_readback.json, gsc_server_error_resource_join.json, gsc_crawl_health_current.json and gsc_server_error_classification.json. Independent review and final continuity checks are recorded in gsc_server_error_independent_review.md and gsc_server_error_checks.json. The earlier four-path receipt and helper were preserved rather than overwritten.

## Earlier four-path diagnostic, retained as dated evidence

The missing5xx-URL and browser-access statements below are superseded by the exact follow-up above. The earlier four archived-product HTTP/redirect findings remain valid only for their recorded scope and time.

Decision DLM-DEC-2026-09-06-ORGANIC-URL-RECOVERY; TA-05. September 6, 2026 UTC. Read-only diagnostic, no redirect or product write. The previous goal turn was PROGRESS: one cart file was staged and independently verified on the unpublished theme. This turn checks a separate unresolved organic-traffic dependency.

## Result

All four saved normalized path leads currently return HTTP 404 without a redirect. Shopify returns exactly the four matching products, all ARCHIVED, with complete search pagination. Neither the four localized paths nor their four root paths has a matching saved URL redirect. These observations explain the sampled unavailable product pages; they do not establish why the products were archived or that restoring them is appropriate.

| Saved lead | Product ID | Current product status | Public result |
|---|---|---|---|
| /fr/products/family-matching-hawaiian-shirt-and-floral-dress | 7000997134433 | ARCHIVED | 404, French error title, no redirect |
| /pt/products/matching-love-heart-printing-couple-t-shirts | 6835971424353 | ARCHIVED | 404, Portuguese error title, no redirect |
| /ru/products/couple-matching-shirts-mr-and-mrs-wedding-gift-anniversary | 6826238607457 | ARCHIVED | 404, Russian error title, no redirect |
| /ru/products/parent-child-one-piece-cut-out-bowknot-bathing-suit | 6613920186465 | ARCHIVED | 404, Russian error title, no redirect |

The public responses are not soft 404s in this sample: each actually returns status 404. Their error-page canonicals and noindex/nofollow metadata are recorded without proposing changes. No current active-product outage, misconfigured redirect chain or published buyer-page failure was demonstrated by these four samples. This does not rule out failures elsewhere.

## Evidence limits that change the next action

The September 5 GSC readback uses August 27 index data and reports 8,784 Not found, 12 server-error and 29 soft-404 rows. Those are historical report counts, not current unique commercial pages. Its first-ten-example summary retained only four normalized path leads; the original full URLs, variant/country/currency query strings and last-crawl dates were not saved. There is no saved 5xx example URL. The four paths do not appear in the bounded saved performance rows; clicks, impressions, backlinks and sales must remain UNKNOWN, not zero.

The analyst's organic_url_recovery_candidates.json/md records the source-only extraction and six source hashes. Its empty candidates array means no original exact reported URL was recovered, not that the four public paths were untested. Root's subsequent current HTTP/product/redirect evidence is in organic_url_recovery_readback.json and organic_url_public_readback.json.

## Chosen action and falsifier

No redirect candidate is qualified now. Keep the four products archived and do not create broad homepage/category redirects from their names. The alternative of treating every reported 404 as a repair would risk sending shoppers to a non-equivalent product and would assume demand we have not measured. The competing explanation—archived products returning appropriate unavailable responses—is supported for these four current product identities, but archival intent remains unknown.

After normal browser access returns, obtain the dated GSC Not found (404) → Examples and Server error (5xx) → Examples exports. Preserve the complete URL and last crawl field as supplied. Inspect the small 5xx set first for current active-page failures; separately join 404 candidates to exact page-level search performance and available link evidence. Prioritize a 404 only when there is a relevant, active, public replacement or a documented mistaken withdrawal. If that evidence appears, prepare the exact same-language redirect/source-target proposal, check current conflicts and request the scoped live change. Otherwise leave the unavailable response and continue the already prepared SEO/organic release lanes. Do not rerun this four-path sample without changed source, a concrete replacement or original-URL evidence.

Google documents that unavailable 4xx URLs lose indexing and that 5xx responses can slow crawling; a 200 response alone does not establish indexing. The appropriate action depends on the resource and current response, not the aggregate error count. [Google HTTP status guidance](https://developers.google.com/crawling/docs/troubleshooting/http-status-codes)

Shopify redirects apply to broken paths and need separate handling for market subfolders; query-string behavior has limitations. Exact URLs and locale targets therefore matter before creating a redirect. [Shopify URL redirect guidance](https://help.shopify.com/en/manual/online-store/menus-and-links/url-redirect)

## Execution and verification

The read-only redirect query was discovered from the current schema and validated before use; both filtered result sets have zero rows and no next page. The product search returns four exact requested handles and no next page. Web page-open returned non-retryable internal safe-open errors. The first shell attempt failed public DNS inside the sandbox; its receipt is preserved separately. Normal network escalation then allowed the four cookie-free public GETs, with complete bodies and no access/rate errors. No browser/login gate was bypassed and no raw HTML, cookie, credential or customer data was retained.

Required outcome checks: exact four-path membership, HTTP 404 on all, exact four-handle archived join, complete empty root/localized redirect searches, original URL/demand unknowns retained, no external mutation and unchanged paid-control/paid-payload/evaluator hashes. Independent review and final canonical results are recorded in organic_url_recovery_independent_review.md and organic_url_recovery_checks.json. No live SEO improvement, incremental traffic, purchases or profit is claimed.

Existing gates remain: exact Greek paragraph approval pending after automatic-review rejection; normal Mac unlock for authenticated draft/Vintage/Pin and GA4 checks; Google app access/support form and actual cohort costs unresolved. Root goal and four-hour heartbeat remain ACTIVE. No new owner question, duplicate schedule or competing continuation prompt was created.
