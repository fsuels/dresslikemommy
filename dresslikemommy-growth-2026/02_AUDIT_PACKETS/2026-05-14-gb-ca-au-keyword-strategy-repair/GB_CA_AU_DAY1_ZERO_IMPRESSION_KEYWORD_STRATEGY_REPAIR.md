# GB/CA/AU Day 1 Zero-Impression Keyword Strategy Repair

Timestamp: 2026-05-14 07:47 EDT

Scope: repo-local/read-only strategy repair for currently active keyword campaigns:

- GB exact Search campaign `23838895360`
- CA exact Search campaign `23834423669`
- AU exact Search campaign `23834424182`

No Google Ads, Merchant, Pinterest, Shopify Admin, GA4/GTM, billing, campaign, budget, bid, status, feed, product, conversion, or theme publish write occurred.

## Why This Exists

The active GB/CA/AU Search campaigns are live and eligible, but the currently enabled keyword layer is too shallow to be the whole strategy. The three enabled exact keywords are valid starter controls:

- `[mommy and me dresses]`
- `[mother daughter dresses]`
- `[mom and daughter matching outfits]`

They are not enough as an expert 2026 growth strategy because they are obvious, likely competitive, and not mapped tightly enough to buyer moments such as family photos, vacation, birthdays, beach days, wedding guest needs, pajamas, swimwear, and role-specific outfits. The correct strategy is a market-by-market intent map, not a generic copied keyword set.

## Day 1 Monitor Result From Saved Current-Day Evidence

Latest saved live/read-only evidence remains the 2026-05-14 command-layer reconciliation:

| Market | Campaign state | Reporting day | Spend | Clicks | Impr. | Purchases | Revenue/value | Decision |
|---|---|---:|---:|---:|---:|---:|---:|---|
| GB | Enabled / Eligible, `$2/day`, exact ad group only | 2026-05-13 | `$0.00` | `0` | `0` | `0.00` | `$0.00` | `ACTION_DUE_NOW_LOCAL_DIAGNOSIS_DONE_LIVE_WRITE_GATED` |
| CA | Enabled / Eligible, `$2/day`, exact ad group only | 2026-05-13 | `$0.00` | `0` | `0` | `0.00` | `$0.00` | `ACTION_DUE_NOW_LOCAL_DIAGNOSIS_DONE_LIVE_WRITE_GATED` |
| AU | Enabled / Eligible, `$2/day`, exact ad group only | 2026-05-13 | `$0.00` | `0` | `0` | `0.00` | `$0.00` | `ACTION_DUE_NOW_LOCAL_DIAGNOSIS_DONE_LIVE_WRITE_GATED` |

This clears the local planning obligation: zero impressions after T+24 now has a concrete serving-diagnosis and long-tail candidate map. It does not clear live-write gates.

## Economics

- Target ROAS: `650%`, meaning about `$6.50` tracked revenue per `$1.00` spend.
- Repo-known planning AOV: about `$70`.
- Implied target CPA: `$70 / 6.5 = $10.77`.
- Any live keyword/ad/bid/status action must plausibly improve learning or sales while preserving this target.

Official Google Ads references checked in this pass:

- Target ROAS uses conversion value per cost, and a target that is too high can limit traffic: https://support.google.com/google-ads/answer/6268637
- Low-search-volume keywords can be inactive until traffic increases; options include Keyword Planner, broader match type, or less-specific terms: https://support.google.com/google-ads/answer/2616014
- Exact match gives the most steering but reaches fewer searches; phrase reaches more searches than exact and fewer than broad: https://support.google.com/google-ads/answer/7478529
- Quality Score diagnostics include expected CTR, ad relevance, and landing page experience: https://support.google.com/google-ads/answer/13738235
- Google recommends tightly themed keywords/ad groups, monitoring search terms, and matching landing pages to ads and keywords: https://support.google.com/google-ads/answer/6238826

## Serving Diagnosis

Most likely causes to diagnose before any live change:

1. Exact-match volume is too narrow for a three-keyword starter set.
2. The keywords are obvious and may be too competitive for a `$0.15` max CPC auction-entry cap.
3. The active RSA still needs current ad-strength/policy/readback; saved evidence showed `Pending`.
4. Quality Score components are not yet usable as performance evidence because there are no impressions.
5. GB search terms are readable but empty; CA/AU search-term reads remain blocked by a stale `Keyword: "human hair wigs"` UI filter.
6. The paid landing has a local supplier/source sanitizer fix, but live expansion should wait for approved theme sync and public readback.
7. Purchase/value/currency evidence is not available from these markets, so Target ROAS bidding is not appropriate for the current zero-data state.

## Market Strategy

### GB / English-UK

Strategy:

- Keep the current exact ad group as the owner for core "mommy and me / mother daughter dresses" demand until data proves otherwise.
- Add UK-English discovery only as a separate review-gated exact/phrase layer, not by mixing broad terms into the current ad group.
- Use UK vocabulary where natural: `mum`, `mummy`, `holiday`, `family photo`, `family photoshoot`, `wedding guest`.
- Do not rely only on "mommy and me"; UK buyers may search "mummy and me" or "mum and daughter".
- Do not send pajama, swimwear, or Daddy-and-Me intent to the beige chiffon dress PDP. Those need collection/PDP-specific ad groups and landing routes.

Priority candidate themes:

- Mum/mummy plus dress: `mummy and me dresses`, `mum and daughter matching dresses`.
- Occasion: `mother daughter wedding guest dresses`, `matching dresses for family photos`, `family photoshoot outfits`.
- Travel/summer: `matching family holiday outfits`, `family beach outfits`.
- Style/role: `mother daughter floral dresses`, `mum and baby girl dresses`.

### CA / English-Canada

Strategy:

- Keep the active campaign English-first. Do not mix French-language keywords into this active English ad group without native review, French landing QA, and exact approval.
- Use Canadian English variants and Canada-qualified modifiers where useful: `Canada`, `family photos`, `family pictures`, `vacation`, `beach`, `wedding guest`.
- French-Canada ideas belong in a separate review-only future packet, not this live English-first campaign.

Priority candidate themes:

- Core Canada: `mommy and me dresses Canada`, `mother daughter matching dresses Canada`.
- Photo intent: `family photoshoot outfits Canada`, `family picture outfits`.
- Occasion: `mommy and me birthday dresses`, `mother daughter wedding guest dresses`.
- Travel/summer: `matching family vacation outfits`, `family beach outfits Canada`.
- Category-specific future groups: `matching family pajamas Canada`, `matching family swimsuits Canada` only with correct collection/PDP landings.

### AU / English-Australia

Strategy:

- Use AU English vocabulary: `mum`, `mummy`, `holiday`, `family photo`, `beach holiday`.
- Do not assume US-style "mommy" is the only buyer language in Australia.
- Prioritize beach/holiday/summer intent when landing pages and products are seasonally and visually aligned.
- Keep exact core demand separate from phrase discovery and from Shopping/Pinterest visual discovery.

Priority candidate themes:

- Mum/mummy plus dress: `mummy and me dresses Australia`, `mum and daughter matching dresses`.
- Photo intent: `family photo outfits Australia`, `family photoshoot outfits`.
- Travel/summer: `family beach holiday outfits`, `matching family swimwear Australia`.
- Occasion/style: `mother daughter wedding guest dresses`, `mother daughter floral dresses`.
- Role-specific: `mum and baby girl matching dresses`.

## Watch-Only Negatives

No negative keyword upload is justified from current evidence because there are no attributable search terms with clicks, spend, or conversion data.

Watch-only negative themes by market:

- GB: `Primark`, `Next`, `M&S`, `ASOS`, `Vinted`, `eBay`, `near me`, `same day`, `hire`, `sewing pattern`, `free`, `used`.
- CA: `Walmart`, `Amazon`, `Shein`, `Temu`, `marketplace`, `near me`, `pickup`, `same day`, `pattern`, `free`, `used`, `rental`.
- AU: `Kmart`, `Big W`, `Cotton On`, `Shein`, `Temu`, `op shop`, `near me`, `click and collect`, `same day`, `hire`, `pattern`, `free`.

These remain `watch_only_not_uploaded`. Add exact/phrase negatives only when real search-term evidence proves waste and the change passes the reviewer gate.

## Live-Action Gate

The next live action is not automatically approved by this packet. Before any keyword, negative, ad, bid, budget, status, or campaign change:

- Save fresh before-state readback for campaign/ad group/keyword/RSA/search terms.
- Clear or avoid CA/AU stale `human hair wigs` filters before search-term decisions.
- Confirm live paid landing supplier/source sanitizer readback is clean before expansion.
- Confirm active public purchasable product and landing fit for every row.
- Pass `ops/marketing/reviewer_checklist.md`.
- Keep action inside `spend_authorization.md` caps, or get fresh exact action-time approval.
- Save after-state readback and update the command layer.

## Output Files

- `gb_ca_au_high_intent_candidate_map.csv`
- `GB_CA_AU_DAY1_ZERO_IMPRESSION_KEYWORD_STRATEGY_REPAIR.md`
