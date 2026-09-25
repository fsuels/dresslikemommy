# Google ad-strength repair — September 23, 2026

**Outcome: PARTIAL. Excellent ad strength has not been achieved.**

## Authorized target and changes

Current campaign: `24273103416`, `DLM | GADS | US | EN | Search | 202609`. The user authorizes repairing its six existing ads and adding useful sitelinks. Historical draft identifiers are discovery references only.

All six ads were saved with 15 headlines and four descriptions each. Six existing distinct sitelinks were associated with the campaign without editing shared asset content: Father & Son Shirts, Mommy & Me Dresses, Family Matching Shirts, Family Matching Outfits, Mommy & Me Pajamas, and Mommy & Me Outfits. Public collection headings and product listings were checked for relevance.

Five first-description pins were retained. Pajamas was unpinned, with separate-person pricing disclosed in all four descriptions. All 24 unique group keyword phrases appear completely within their respective ad's headlines or descriptions. Longer phrases were placed in descriptions in accordance with [Google's Ad Strength guidance](https://support.google.com/google-ads/answer/9921843?hl=en).

## Native verification

Every saved ad was reopened and all 22 fields compared exactly: final URL, two display paths, 15 headlines and four descriptions. All six comparisons passed. Each reopened editor displayed six inherited campaign sitelinks. Exact identifiers and before/after copy are in `ad_copy_before_after.json`.

| Ad group | Ad ID | Native editor | Native table | Saved fields |
|---|---|---|---|---|
| Mommy & Me Pajamas | 825605060532 | Poor | Pending | Match |
| Father & Son Shirts | 825646172296 | Poor | Pending | Match |
| Mommy & Me Dresses | 825646199950 | Poor | Pending | Match |
| Mommy & Me Outfits | 825646199956 | Poor | Pending | Match |
| Family Matching Outfits | 825727913987 | Poor | Pending | Match |
| Family Matching Shirts | 825727944842 | Poor | Pending | Match |

Every editor marked the keyword category low and the other four categories high. The keyword View ideas interface showed Recent assets / Asset library but no keyword suggestions. The user correctly identified the empty keyword check; it remains unresolved.

The campaign, all six groups, all six ads and all 48 keywords remain Paused. The USD 210 campaign total and September 22–28 dates were retained. No status, budget, bid, keyword text, negative, measurement or billing changes were made.

## Diagnostics and limits

Static phrase expansion, 15-headline variety, six sitelinks, disclosure-preserving unpinning and full long-keyword descriptions did not clear the keyword indicator. A Pajamas dynamic-keyword insertion trial was reverted; no DKI remains in the final copy. [Google's DKI guidance](https://support.google.com/google-ads/answer/2454041?hl=en) explains fallback behavior but does not establish this scoring cause.

The cause is UNKNOWN. No official evidence was found that paused keywords are excluded from scoring. Pending cells exposed no explanatory title, label or description. In-app browser content export was unsupported. A native CSV download was requested, but no local report receipt was verified; no CSV export is claimed.

Native observations are in the browser transcript. The JSON is a structured reconstruction checked against all six native field arrays using matching FNV transfer hashes. The hashes do not cover pins, sitelinks or statuses; those were read separately from the native UI.

Independent reviewer `/root/ad_review`, `DID_NOT_BUILD_OR_EXECUTE`, returned `PASS_WITH_GATES` for accurate partial reporting and artifact consistency. The reviewer checked six identities, 132 text fields, six transfer hashes, headline/description limits, all 24 phrase matches, unchanged final URLs / paths, disclosure handling and unsupported-claim exclusions. The reviewer did not independently replay the browser.

## Pending next action

Separate permission was requested for one isolated diagnostic: temporarily enable only the eight Family Matching Shirts keyword records under the still-Paused campaign, group `202058006604` and ad `825727944842`; inspect that ad's keyword ideas / strength; then restore all eight keywords to Paused regardless of result. Approval remains PENDING and the test has NOT RUN. Elapsed time is not permission. The original ad-copy / sitelink authorization does not establish keyword-status authority.

Root owns current-task in-app browser 2, original tab 1 for Ads and temporary tab 2 for this read-only keyword baseline. No peer account or browser surface was used.

## Local verification

- Canonical cockpit render: PASS using system Python 3.9.6.
- Marketing command integration: PASS, zero side-document risks.
- Strict continuity integrity: PASS using the bundled Python runtime. System Python was too old for this check; the unavailable python3.13 command was not retried.
- Scoped whitespace check: PASS.

These checks validate continuity records, not Google's ad-strength result.
