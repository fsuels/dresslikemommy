# 1688 Short-Query Relevance Readback

Date: 2026-09-04

Problem: the seasonal plan sent long Chinese strings that mixed the desired matching relationship and garment with year, novelty, stock, dropshipping, supplier, market, and export modifiers. Live results drifted into generic women's clothing, lingerie, shoes, accessories, fabric, and other unrelated products.

## Decision-critical evidence

- The prior Mommy & Me query contained `14` space-separated terms and `37` Chinese characters. In one logged-in 1688 result snapshot, `0/29` visible titles showed a matching-family relationship.
- The controlled short alternative `母女亲子装 连衣裙 秋冬` contained `3` terms and `10` Chinese characters. In the same read-only workflow, `30/34` visible titles showed a matching-family relationship and `0/34` were lingerie.
- A more season-specific short query, `母女亲子装 连衣裙 秋季`, returned `44/48` visibly matching-family titles and `0/48` lingerie titles.
- Product-specific relationship queries also stayed substantially more relevant: `母女亲子装 礼服 冬季` returned `43/44` matching titles; `全家亲子装 卫衣 冬季` returned `36/44`; and `情侣卫衣 冬季` returned `33/35`.
- A generic couples query using only `套装` exposed thermal underwear. The plan therefore uses a concrete garment such as `卫衣`, `礼服`, or `西装` where the generic word is ambiguous.
- Tested maternity phrases did not visibly prove both maternity fit and family matching in the title. Maternity now fails closed unless both concepts are evidenced; a zero-result lane is preferable to filling the queue with generic maternity or women's wear.

These are title-level relevance observations from one live result snapshot, not claims about 1688's private ranking algorithm or product quality. Ranking and inventory can change.

## Implemented query contract

1. Put one precise relationship phrase first, such as `母女亲子装`, `父子亲子装`, `兄妹装`, `全家亲子装`, or `情侣装`.
2. Add one concrete garment phrase and one season phrase. Add at most one occasion phrase only when necessary.
3. Cap the execution string at `4` terms and `18` Chinese characters.
4. Show a literal English translation beside the exact Chinese string so the owner can review every search before running it.
5. Search once per matching group for the selected US and Europe markets instead of duplicating identical queries by market.
6. Do not place freshness, availability, dropship, supplier age, supplier quality, or market-fit claims in the search string. Validate those facts after discovery from product and supplier evidence.

The official 1688 app description exposes product/category search and image search as distinct discovery paths. A WorldFirst international-buyer guide likewise directs buyers to enter the desired product name in Chinese or use image search, then apply supplier/product filters. This supports a concise product-first discovery strategy; the live A/B result is the stronger task-specific evidence for the exact term design.

## State and safety readback

- The overlong live run was stopped after `33/36` old searches; the final old maternity/Europe lane was not allowed to continue.
- Automatic daily scouting is paused with the reason `review the new short 1688 terms before the next run`.
- The original replacement plan was `18` fixed searches across `6` shared matching-group lanes. The first full six-lane batch completed as job `6ee644d83878` with frozen plan hash `06b68838642fae61`.
- The strict supplier gate remains at a minimum of `5` verified supplier-context years. Search-card text cannot establish tenure.
- The existing identity, supplier rating, current-listing, availability, dropship, dispatch, size-chart, usable-image, category, and intellectual-property checks remain independent post-search gates.
- No 1688 purchase, order, supplier message, login/CAPTCHA bypass, Shopify write/publication, advertising/feed change, billing action, or credential change occurred.

## First fixed-batch readback

The owner reviewed and selected all `18` literal pairs before execution. Static validation passed: all query IDs and Chinese strings were unique; every pair had the intended relationship, garment, and season meaning; every execution string had exactly `3` terms and at most `10` Chinese characters; and none contained the removed year, novelty, stock, dropship, supplier, export, market, or lingerie terms.

The full batch ran from `2026-09-04T17:39:25Z` to `2026-09-04T17:42:23Z`. A normal 1688 CAPTCHA appeared during the third Siblings search. The scout paused without bypassing it, the normal helper action restored a valid page, and the same frozen query resumed. All `18/18` searches and `6/6` lanes then completed. No second full six-lane batch ran during that validation, and automatic scouting remained off.

The result was honest but not commercially sufficient:

- `653` raw search cards were collected.
- `239/653` visible titles passed the app's strict relationship matcher.
- `69/653` visible titles showed the requested relationship, garment family, and season/holiday together.
- Search scoring produced `652` Reject and `1` Test candidate. The single Test candidate was detail-checked and did not pass the final opportunity gate.
- Final job outcome: `0` Verified, `0` Promising, `1` filtered after supplier checks.

The combined-title count is a deterministic audit of visible titles using the app's strict relationship matcher plus explicit bilingual garment and season synonyms. It is not a quality, inventory, or private-ranking claim.

### Exact-pair decision after the live batch

| # | Exact English meaning | Exact 1688 query | Visible titles with relationship + garment + season | Decision |
|---:|---|---|---:|---|
| 1 | Mother-daughter matching outfits · Dresses · Fall | `母女亲子装 连衣裙 秋季` | `2/25` | Revise before another run |
| 2 | Mother-daughter matching outfits · Formalwear · Winter | `母女亲子装 礼服 冬季` | `1/21` | Revise before another run |
| 3 | Mother-daughter matching outfits · Formalwear · Christmas | `母女亲子装 礼服 圣诞` | `1/42` | Revise before another run |
| 4 | Father-daughter matching outfits · Dresses · Fall | `父女亲子装 连衣裙 秋季` | `0/26` | Revise before another run |
| 5 | Father-son matching outfits · Suits · Winter | `父子亲子装 西装 冬季` | `0/43` | Revise before another run |
| 6 | Father-daughter matching outfits · Formalwear · Christmas | `父女亲子装 礼服 圣诞` | `0/36` | Revise before another run |
| 7 | Sisters matching outfits · Dresses · Fall | `姐妹装 连衣裙 秋季` | `22/52` | Keep as a controlled discovery term |
| 8 | Brother-sister matching outfits · Formalwear · Winter | `兄妹装 礼服 冬季` | `3/48` | Revise before another run |
| 9 | Sisters matching outfits · Formalwear · Christmas | `姐妹装 礼服 圣诞` | `1/43` | Revise before another run |
| 10 | Family matching outfits · Dresses · Fall | `全家亲子装 连衣裙 秋季` | `0/33` | Revise before another run |
| 11 | Family matching outfits · Formalwear · Winter | `全家亲子装 礼服 冬季` | `1/28` | Revise before another run |
| 12 | Family matching outfits · Formalwear · Christmas | `全家亲子装 礼服 圣诞` | `0/19` | Revise before another run |
| 13 | Couples matching outfits · Dresses · Fall | `情侣装 连衣裙 秋季` | `28/53` | Keep as a controlled discovery term |
| 14 | Couples matching outfits · Formalwear · Winter | `情侣装 礼服 冬季` | `10/46` | Keep as a controlled discovery term |
| 15 | Couples matching outfits · Formalwear · Christmas | `情侣装 礼服 圣诞` | `0/28` | Revise before another run |
| 16 | Maternity parent-child matching outfits · Dresses · Fall | `孕妇亲子装 连衣裙 秋季` | `0/43` | Defer as an experimental sparse-supply lane |
| 17 | Maternity parent-child matching outfits · Formalwear · Winter | `孕妇亲子装 礼服 冬季` | `0/36` | Defer as an experimental sparse-supply lane |
| 18 | Maternity parent-child matching outfits · Formalwear · Christmas | `孕妇亲子装 礼服 圣诞` | `0/31` | Defer as an experimental sparse-supply lane |

All `18` pairs were linguistically coherent and safe to test; only `3` earned a keep decision from this live snapshot. The other `12` require a new evidence-backed term design, and the `3` maternity pairs should not re-enter the normal production batch until a matching-family phrase proves useful. No untested replacement has been silently promoted into the saved plan.

### Review-only returned-vocabulary redesign

The next plan changes only the `12` weak non-maternity searches. The `3` successful searches are byte-for-byte unchanged and labeled as controls. The `3` Maternity rows remain visible but are disabled and excluded from every runnable lane. These replacements are hypotheses grounded in the returned titles; they are not yet live-validated searches.

| Role | Exact English meaning | Exact 1688 query | Why this replacement was selected |
|---|---|---|---|
| Replacement | Mother-daughter matching outfits · Long-sleeve dresses · Fall | `母女亲子装 长袖连衣裙 秋季` | Relevant results included a 2026 autumn mother-daughter long-sleeve dress; this narrows the prior broad dress term. |
| Replacement | Mother-daughter matching outfits · Sweatshirts · Winter | `母女亲子装 卫衣 冬季` | Among 17 relationship-matching titles, sweatshirts and knitwear recurred while formalwear did not. |
| Replacement | Mother-daughter matching outfits · Christmas sweatshirts | `母女亲子装 圣诞卫衣` | Christmas results repeatedly used party tops and sweatshirts instead of formalwear. |
| Replacement | Father-son matching outfits · Long-sleeve T-shirts · Fall | `父子亲子装 长袖T恤 秋季` | The father-daughter dress search had almost no Daddy match; returned father-son supply used shirts and autumn long-sleeve T-shirts. |
| Replacement | Father-son matching outfits · Sweaters · Winter | `父子亲子装 毛衣 冬季` | Father-son results included sweaters and knit cardigans; only one visible relationship title mentioned a suit. |
| Replacement | Father-son matching outfits · Christmas sweaters | `父子亲子装 圣诞毛衣` | The direct holiday search had no Daddy match, while returned father-son titles included Christmas/New Year knitwear. |
| Control | Sisters matching outfits · Dresses · Fall | `姐妹装 连衣裙 秋季` | Unchanged; `22/52` titles visibly combined relationship, garment, and season. |
| Replacement | Brother-sister matching outfits · Sweatshirts · Winter | `兄妹装 卫衣 冬季` | Formalwear produced sparse toddler ceremony items; winter family-matching results repeatedly used sweatshirts. |
| Replacement | Brother-sister matching outfits · Christmas sweatshirts | `兄妹装 圣诞卫衣` | `姐妹装 礼服` drifted into bridesmaid accessories; the new phrase keeps a child relationship and a concrete garment. |
| Replacement | Family matching outfits · Sweatshirts · Fall | `全家亲子装 卫衣 秋季` | Family-wide autumn results repeatedly included sweatshirt sets, avoiding a women-and-girls dress bias. |
| Replacement | Family matching outfits · Sweatshirts · Winter | `全家亲子装 卫衣 冬季` | Eight relevant returned titles used sweatshirts and eleven used winter; this exact term also led the earlier controlled relevance check. |
| Replacement | Family matching outfits · Christmas pajamas | `全家亲子装 圣诞睡衣` | Holiday results included 2026 Christmas family homewear/pajama sets, a concrete whole-family product. |
| Control | Couples matching outfits · Dresses · Fall | `情侣装 连衣裙 秋季` | Unchanged; `28/53` titles visibly combined relationship, garment, and season. |
| Control | Couples matching outfits · Formalwear · Winter | `情侣装 礼服 冬季` | Unchanged; `10/46` titles visibly combined relationship, garment, and season. |
| Replacement | Couples matching sweatshirts · Christmas | `情侣卫衣 圣诞` | The formal Christmas search returned no couple matches; the controlled couples-sweatshirt phrase previously returned `33/35` couple titles. |

Deferred and non-runnable:

- `孕妇亲子装 连衣裙 秋季`
- `孕妇亲子装 礼服 冬季`
- `孕妇亲子装 礼服 圣诞`

The review gate is fail closed: the app and backend block the new plan until the owner explicitly confirms its exact hash. Confirming review does not open 1688, start a job, or enable automatic scouting. Any selection or term change creates a different hash and requires review again.

### Subsequent local-state reconciliation

The local state contains two later completed jobs created through the owner-triggered path in the older interface:

- `a1a59f8b13e8`, created at `2026-09-04T18:12:43Z`, ran `2` Mommy & Me queries.
- `287e88cd32f7`, created at `2026-09-04T18:14:00Z` while the pre-lock process was still serving, ran `12` Mommy & Me and Daddy & Me queries.

That means the earlier phrase “first and only batch” was no longer current. Neither job used or validates the new returned-vocabulary replacements. Codex did not launch a 1688 job for this redesign: after the locked build replaced the old process, an unreviewed `/api/scout` request was rejected and the job count remained unchanged. The app now restores the complete review plan and keeps automatic scouting off.

### Detail-candidate correction

The only Test candidate came from `情侣装 连衣裙 秋季`. Its saved detail page proved `9` supplier-context years and one-piece ordering, but the first parser pass replaced the product title with the company name, misread `60天老客价` as MOQ `60`, and treated a generic platform disclaimer containing `品牌` as a product IP-risk flag. The collector was repaired and the saved evidence was reprocessed locally: the product title is preserved, MOQ is `1`, and the generic disclaimer is not a brand-risk signal.

That correction does not promote the item. The reprocessed detail score is Test `59`, while the final opportunity assessment remains Rejected because the product itself claims `2025`, not `2026`, and the page did not prove a valid supplier rating or current availability. The supplier minimum remains `5`; it was not the rejecting factor.

The evidence panel also no longer reuses the generic `代发` (dropshipping) service flag as proof of either availability or dispatch speed. Both now display `Not verified`; dropshipping remains independently confirmed. This prevents one supplier claim from silently satisfying three separate gates.

## Residual proof required

Do not run the same `18`-query plan again. Design a smaller replacement set only for the `12` weak non-maternity pairs, keep the `3` proven discovery terms unchanged as controls, and leave the `3` maternity searches deferred. Any new terms require the same literal English/Chinese review and a separate owner-authorized validation run; supplier and detail gates must not be weakened merely to increase yield.
