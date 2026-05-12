# GB/CA/AU Inner Search Enable Execution Report

Date: 2026-05-12

## Scope Approved

Owner approved enabling only the inner exact Search entities in these already-enabled campaign/ad-group shells:

- GB campaign `23838895360`, ad group `194138528537` / `Mommy & Me Dresses - Exact`
- CA campaign `23834423669`, ad group `196679079575` / `Mommy & Me Dresses - Exact`
- AU campaign `23834424182`, ad group `198852670520` / `Mommy & Me Dresses - Exact`

Approved entity scope per market:

- Exact keywords: `mommy and me dresses`, `mother daughter dresses`, `mom and daughter matching outfits`
- One responsive search ad

No other ad groups, ads, keywords, campaigns, budgets, bids, product scope, feed, Merchant, Pinterest, conversion goals, PMax, Standard Shopping, Shopify product data, or billing were changed.

## Landing URL Language/Currency Proof

Before the final enable, the live final URL was rechecked for each market with a browser-style public request:

| Market | Final URL Parameter | Language | Currency Evidence | Country Evidence |
|---|---|---|---|---|
| GB | `?country=GB` | `lang="en"` | `priceCurrency: GBP`, `£` symbols | `United Kingdom` / `country=GB` |
| CA | `?country=CA` | `lang="en"` | `priceCurrency: CAD` | `Canada` / `country=CA` |
| AU | `?country=AU` | `lang="en"` | `priceCurrency: AUD` | `Australia` / `country=AU` |

These are English-first campaigns, so English language plus local presentment currency is the intended match for this first low-risk cohort.

## Execution Notes

First attempt used keyword status code `2`, which Google Ads RPC rejected with `AdGroupCriterionError.INVALID_USER_STATUS`. The RSA enable in that attempt worked, so the rollback path paused the RSA again. Read-only rollback verification showed all GB/CA/AU keywords and ads paused again before recovery.

Recovery tested keyword status code `1` on one GB exact keyword with immediate readback. It succeeded, proving that Google Ads internal keyword `ENABLED` status is code `1` for this surface. The final controlled script was patched to use status code `1` for keyword criteria and then completed the exact approved scope.

## Final Readback

Final RPC readback passed for all three markets:

| Market | Campaign | Ad Group | Enabled Keyword Criterion IDs | Enabled RSA Ad ID | Budget | Safety Readback |
|---|---:|---:|---|---:|---:|---|
| GB | `23838895360` | `194138528537` | `299141671628`, `301154335636`, `301154336396` | `808406712704` | `$2/day` | Search only, presence-only, no conversion override, other ad groups paused |
| CA | `23834423669` | `196679079575` | `299141671628`, `301154335636`, `301154336396` | `808294804728` | `$2/day` | Search only, presence-only, no conversion override, other ad groups paused |
| AU | `23834424182` | `198852670520` | `299141671628`, `301154335636`, `301154336396` | `808328767090` | `$2/day` | Search only, presence-only, no conversion override, other ad groups paused |

Entity-page UI readbacks also supported the RPC result:

- GB/CA/AU keyword pages showed the three exact keyword rows as `Eligible` under `Keyword status: Enabled`.
- GB/CA/AU ads pages showed the target RSA row as `Eligible` under the exact ad group, with `Ad status: Enabled, Paused` visible in filter context.
- Campaign overview pages still showed the stale message `All keywords are paused, All ads are paused` immediately after enablement. Treat this as a UI/serving-status lag unless it persists in the next monitor, because entity-level RPC and UI readbacks show the inner entities enabled/eligible.

## Current Negative Keyword Quality

The first live cohort is deliberately exact-match only, which sharply limits query expansion risk. The current split files include a shared campaign-level negative base of `37` terms for GB/CA/AU, covering free/DIY/sewing-pattern/tutorial intent, marketplace/low-quality source intent, used/rental, adult/sexy, doll/game, supplier/source, and fabric-only traffic.

This shared negative base is suitable for the first exact-match opening, but it is not the final expert negative strategy. The next optimization lane must add country- and language-specific negatives from search-term evidence, for example country marketplace/retailer leakage, regional non-buying phrasing, translation/dialect false positives, and irrelevant photo/costume/tutorial terms per market. Do not blindly copy one negative list across all languages after expansion.

## Evidence Files

- Live script: `enable_gb_ca_au_inner_entities_live_cdp.py`
- Final summary: `raw/post-enable-readback/final_success_summary.json`
- Per-market post checks: `raw/post-enable-readback/*/post_enable_delta_checks.json`
- Failed first-attempt evidence: `raw/enable-action/enable_error.txt`, `raw/enable-action/GB/keyword_*_enable_response.json`, `rollback/trigger_summary.txt`
- Recovery proof: `raw/recovery-status-code-1/GB/`
- Entity-page UI proof: `raw/post-inner-ui-entity-pages/`

## Next Expert Marketing Actions

1. Monitor GB/CA/AU search terms and cost within the first 24 hours and again daily for the first 72 hours.
2. Add country-specific negatives only from evidence or clearly irrelevant country-tail terms, under fresh exact approval if live account edits are needed.
3. Do not scale budget until conversions or high-quality assisted intent supports it. Hold the `$2/day` micro-test until waste/CTR/CVR evidence is visible.
4. Prepare the next market pair only after this cohort is confirmed serving cleanly, or with fresh exact owner approval for the next controlled pair.
5. For image-heavy growth and ad strength work, prioritize Pinterest/asset/PMax-quality lanes only after source-safe images/catalog/product groups are clean and explicitly approved.
