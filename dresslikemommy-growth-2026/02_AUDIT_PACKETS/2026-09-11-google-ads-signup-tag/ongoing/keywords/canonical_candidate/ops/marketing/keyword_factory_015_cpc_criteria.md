# $0.15 CPC Keyword Factory Criteria

Last updated: 2026-09-11

Purpose: create a large, market-specific long-tail keyword universe quickly, starting with the United States as the primary market, then promote only validated rows into live Google Ads action packets. This is repo-local strategy; it is not approval to upload or change live campaigns.

Companion command files:

- `keyword_strategy.md`: operating model and forced action rules.
- `keyword_scoring_rubric.md`: canonical scoring weights and thresholds.
- `keyword_universe.csv`: local universe seed; not a live upload file.

## North Star

Get as many Dress Like Mommy paid-growth sales as possible, as fast as possible, while holding about `650% ROAS`.

Use the owner's USD 0.15 CPC ceiling and the stricter of 6.5x return-adjusted ROAS and 30% all-in profit. Calculate allowable CPA from the common retained-revenue basis (merchandise plus shipping, excluding tax), actual variable costs and allocated overhead/other costs; leave it unknown when any necessary cost is missing. The former USD 70 AOV/USD 10.77 CPA/1.4% conversion illustration is historical only.

## Why Not Upload The Biggest Possible List

The smart answer is: build the biggest possible candidate universe locally, but do not upload the biggest possible live list.

Reasons:

- A huge unfiltered live keyword list hides what is working because fragmented budgets buy too few comparable observations; historic USD 2/day was not a current allocation.
- Google can mark overly specific rows as `Low search volume`; those rows may be inactive until traffic increases, so adding thousands of ultra-specific exact terms can look like action while producing no learning.
- Close variants of head terms are not real long tail. `[mummy and me dresses]` or `[mommy and me dresses canada]` can still compete in the same expensive auction.
- Phrase match can discover useful queries, but it can also stretch into adjacent intent. Phrase rows need tighter themes, negatives, and search-term review.
- Every live keyword needs a matching landing promise. Sending pajamas, swimwear, Daddy-and-Me, or general beach outfit searches to a beige mother-daughter chiffon dress PDP wastes traffic.

## Keyword Creation Criteria

A candidate must pass all hard gates before it can move from universe to live packet:

| Gate | Pass standard |
|---|---|
| Market/language | US is the primary market and uses US English first: `mom`, `mommy`, `mommy and me`, `mother daughter`, `family photos`, `family pictures`, `vacation`, `birthday`, `wedding guest`, `beach photos`, and `matching family`. Expansion markets use local vocabulary: GB `mum/mummy/holiday`, CA English `mom/mommy/Canada/family pictures`, AU `mum/mummy/holiday/beach`; no French-Canada rows in English campaign. |
| Buyer intent | Query implies a shopper may buy now for a role, event, photo, vacation, birthday, wedding guest, beach day, or matching family occasion. |
| Product specificity | Includes role + product/style/material/color/occasion when possible, not only generic category language. |
| Landing fit | Current landing truthfully satisfies the query with active, public, purchasable, country/currency-correct, supplier-clean products. |
| Economics | Current effective CPC control, country-specific auction evidence and actual cost/return-based allowable CPA must qualify. A historical bid range or absent warning alone does not pass. |
| Conversion plausibility | Use the exact basket allowable CPA and observed uncertainty; unknown AOV/cost/conversion rate remains gated. |
| No cannibalization | One owner by market/language/query intent/landing. No duplicate exact keyword across live ad groups. |
| Negative fit | Query is not DIY, free-product-only intent, sewing-pattern requests, used, rental, marketplace-only, local pickup, same-day, sexually explicit content, doll/game, supplier/source, inspiration-only, or wrong apparel intent. |

## Scoring

After hard gates, score each candidate `0-100` using `keyword_scoring_rubric.md`:

- `25` buyer intent: buying, event, role, urgency, and product clarity.
- `20` product match: Dress Like Mommy actually sells the item/category/role.
- `15` occasion/deadline: photoshoot, vacation, birthday, wedding, cruise, beach day, holiday, or family pictures.
- `15` landing-page match: exact PDP/collection promise, country/currency, clean supplier readback.
- `10` economics: evidence-backed current CPC/control and actual cost/return qualification; unknown earns zero evidence credit.
- `10` volume/serveability: dated, exact-market demand/auction evidence; unknown earns zero evidence credit.
- `5` waste risk: avoids DIY, free-product-only intent, marketplace, supplier, local-stock, and wrong-intent traffic.

Promotion rule:

- `85-100` `GREEN`: exact candidate for next bounded packet after landing and CPC validation.
- `70-84` `YELLOW`: keep in local universe; use only if stronger rows are too low-volume or as a tight phrase-discovery repair.
- `<70` `RED`: reject for paid Search or route to SEO/Pinterest/content/watchlist.

## Batch Strategy

Build large, upload small:

- Local universe target: hundreds of candidates per market from products, collections, homepage moments, Keyword Planner, search terms, and locale vocabulary.
- US is the primary planning lane; actual current demand and economics determine allocation. If the live US lane is Shopping, the same keyword universe still informs product-title/feed-title priorities, Shopping search-term interpretation, Pinterest creative language, and future US Search packets.
- First live exact batch after gates: about `10-20` best rows per market, split into tight themes.
- Phrase discovery batch only if exact rows are too low-volume: about `3-8` phrase rows per market, one theme per ad group, with search-term review the next day.
- Do not add a keyword just because it is related. Add it because it is likely to produce profitable sales or learning at `$0.15`.
- If an enabled keyword lane has `0` impressions after 24 hours and no technical blocker exists, prepare or execute a green-gated repair using `5-20` exact/phrase long-tail rows. Monitoring without one of repair, expansion, negative action, hold/kill/scale, or exact blocker/unblock is not progress.

## US Primary Market Standard

US is the primary market and should never be omitted from keyword planning.

US keyword universe sources:

- Store positioning: Mommy & Me, Family Matching, Pajamas, Matching Dresses, Swimsuits, Daddy & Me, Vacation, Photo Days, Birthdays, Beach Days.
- US buyer vocabulary: `mom`, `mommy`, `mommy and me`, `mother daughter`, `mom daughter`, `family matching`, `family photos`, `family pictures`, `vacation outfits`, `beach photos`, `birthday dresses`, `wedding guest dresses`.
- Product signals: active public products, product titles, collection names, photos, style/material/color, price point, and size/role availability.
- Shopping signals: US Standard Shopping search terms, product-group serving, impressions, clicks, cost, conversion value, product title/image fit, and Merchant diagnostics.

US seed clusters to expand locally, not blindly upload:

- `mom daughter family photo dresses`
- `mommy daughter picture outfits`
- `mother daughter beach photo dresses`
- `mommy and me birthday dresses`
- `mother daughter wedding guest dresses`
- `mommy daughter vacation dresses`
- `matching family photo dresses`
- `matching family beach dresses`
- `mommy and me summer dresses`
- `beige mother daughter dresses`
- `chiffon mother daughter dresses`
- `floral mommy daughter dresses`

US live promotion rule:

- If using Search, promote only validated exact batches at `$0.15`.
- If using Shopping, use the same universe to diagnose product titles, photos, product groups, and query fit; do not pretend Shopping has manual keywords.
- If using Pinterest, use the same universe for creative/product grouping and lower-funnel wording, not Search keyword uploads.

## Historical GB/CA/AU Watchlist — Current Readback Required

Historical head-term watchlist; do not infer current CPC, eligibility or exclusion from these names:

- `[mommy and me dresses]`
- `[mom and daughter matching outfits]`
- `[mother daughter dresses]`
- `[mummy and me dresses]`
- `[mommy and me dresses canada]`
- `[mummy and me dresses australia]`

Correct next pattern:

- product-specific exact rows such as color/material/role/season
- buyer-moment exact rows such as photo, birthday, wedding guest, vacation, beach photo
- market language variants only when they also add meaningful buyer intent
- separate landings for swim, pajamas, Daddy-and-Me, general family matching, or French-Canada

## Fix-Now Rule

When a mistake is found:

- If it is repo-local/read-only, fix it immediately and verify.
- If it is a live external write but already covered by current exact approval, do it, read back before/after, and log it.
- If it is a live external write not currently approved, produce the exact smallest approval packet and keep other safe work moving.
- Do not leave a blocker as a passive note.

Evidence rule: current command-layer readbacks govern account status and authority. A local score is a research priority, not live readiness. Economic-fit and serveability points require dated evidence for the exact market, keyword and offer; assign zero evidence credit when unknown. Zero credit does not mean zero demand. Recompute the total/threshold without changing keyword identity or promotion status.

Negative intent is not a blanket one-word exclusion: adult sizes are valid apparel; “free shipping” can express buying intent; “pattern” can describe a garment; and “costume/costumi” changes meaning by language. Use original-language, query-specific evidence and check existing negatives before proposing a narrow exclusion.

Economics definitions follow `keyword_strategy.md`: R is retained merchandise plus retained shipping, excluding tax; V is actual variable costs; H is allocated overhead/other costs excluded from V; CM = R − V. Require `A ≤ min(R/6.5, CM − H − 0.30R, approved cash/loss allowance)`. Unknown required inputs remain unqualified; platform value must be reconciled to this basis.
