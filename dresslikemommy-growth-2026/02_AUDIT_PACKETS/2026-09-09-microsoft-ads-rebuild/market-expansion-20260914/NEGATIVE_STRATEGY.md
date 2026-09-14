# Negative-keyword strategy for the English matching-dress cohorts

Prepared September 14, 2026. **LOCAL CANDIDATE / NO MICROSOFT CHANGES.** The exact machine rows and test results are in [english-master-assets.json](english-master-assets.json). These are proposed campaign-level English negatives for a finished-dress retail offer, not a global account list or proof of wasted spend.

Reuse the existing reviewed work. This packet preserves the US/DE campaign IDs and the US eight-headline/three-description baseline. It reuses `sewing pattern`, `sewing patterns` and `costume rental`; it does not silently remove existing native exclusions. The September11 qualified-seed file has 48 rows but zero US dress rows. Its tee-specific routing terms, including matching dresses, must retain their ad-group scope. The root CSV's garment exclusions remain on HOLD_SEMANTIC_REVIEW.

## Matching rules that change the decision

Positive Exact can reach close variants with the same meaning. Negative matching is narrower: Phrase rejects the specified ordered phrase within a query; Exact rejects the complete query. Plurals, synonyms and misspellings need separate negative entries. Campaign negatives affect every child group, in addition to inherited account/shared/group restrictions. The list uses plain text plus a separate match-type field; quotation marks and brackets are display notation, not characters to import. [Microsoft negative guidance](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_aboutnegativekeywords), [positive match guidance](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_matchoptions).

## Proposed English campaign profile

These 19 rows are local candidates. They have explicit non-retail intent, but no query-performance evidence has yet justified savings or a CPA claim. Reuse identical native rows instead of adding duplicates. New rows need a final native conflict and scope check.

| Negative text | Type | Intent rationale |
|---|---|---|
| `sewing pattern` | Phrase | Sewing instructions rather than finished garments. |
| `sewing patterns` | Phrase | Explicit plural of the sewing-instruction intent. |
| `sewing tutorial` | Phrase | Instructional sewing intent. |
| `sewing tutorials` | Phrase | Separate plural because negative variants are not automatic. |
| `how to sew` | Phrase | Making a garment instead of selecting a finished dress. |
| `costume rental` | Phrase | Rental intent; this campaign offers dresses for purchase. |
| `costume rentals` | Phrase | Separate plural rental intent. |
| `wholesale supplier` | Phrase | Supplier sourcing intent rather than retail shopping. |
| `wholesale suppliers` | Phrase | Separate plural supplier-sourcing intent. |
| `svg file` | Phrase | Digital design file intent rather than clothing. |
| `svg files` | Phrase | Separate plural digital-file intent. |
| `printable template` | Phrase | Printable template rather than finished clothing. |
| `printable templates` | Phrase | Separate plural template intent. |
| `crochet pattern` | Phrase | Instructions for making garments, not this dress offer. |
| `crochet patterns` | Phrase | Separate plural making-instruction intent. |
| `how to make matching dresses` | Exact | Only this complete instructional query; do not blanket-exclude make. |
| `mother daughter dress rental` | Exact | Only this complete rental query; mixed queries remain reviewable. |
| `matching dresses for rent` | Exact | Only this complete rental query. |
| `mommy and me svg` | Exact | Only this complete digital-design query. |

Existing single-word Phrase seeds `diy`, `wholesale`, `svg` and `printable` are **review flags**, not live removal instructions. For new cohorts prefer the narrow profile above or an observed full-query Exact exclusion. For example, `printable` alone could suppress a buyer checking a printable size chart, and `diy` can describe a family photo session. The current paused records require a before/after plan before changing those entries.

Do not exclude single words such as pattern, cheap, affordable, free, sale, gift, reviews, sizes/ages, wedding or birthday. Do not copy garment exclusions such as t shirt, swimsuit or pajamas from another offer. A t-shirt dress or a family outfit with multiple garment types can be legitimate intent. These protected terms are not claims that every size, item or promotion is available.

## Conflict review and the real limitation

**Local checks passed:** 15 unique headlines all ≤30 characters; 4 unique descriptions all ≤90; 8 Exact candidates; 19 Phrase/Exact negatives; no literal conflicts against the 8 candidates plus the 14 existing US-English positive rows. Twenty ordinary buyer holdouts remain unblocked, and all 19 negative-intent probes match the intended row. Three gap probes deliberately remain unblocked, demonstrating spelling/synonym and Exact limits. These are deterministic case-insensitive ordered-token checks, not a Microsoft matching simulator or native certification.

Two adversarial buyer queries still collide with the inherited narrow-phrase design: buying finished dresses *instead of a sewing pattern*, and buying finished dresses *not sewing tutorials*. Those are recorded as known false-positive risks, not counted as passed holdouts. Native queries must decide whether the exclusion is useful. If those mixed intents matter, narrow the affected rule to an observed complete-query Exact negative. Do not automatically broaden the list to close every gap.

Before saving a paused build, download/read the current account and shared-list assignments, campaign/group negatives, positives, destination overrides and native negative-conflict report. Test the proposed delta against all affected groups, inspect deliberate singular/plural forms and preserve scope. Afterwards read back the exact native text, match type and parent IDs. A zero local conflict count does not account for positive semantic variants or unrelated inherited exclusions.

## International and profit decisions

Localize the intent, not just the words. English phrases do not protect German, Spanish or other campaigns. For each actual market-language row, use native idiom, singular/plural and accent/compound checks, and keep buyer-intent holdouts in that language. Reuse the previously reviewed language packet wherever appropriate; do not expand held rows into blanket shared exclusions. The market inventory owner determines actual routes and country-language applicability.

After tracking and the exact cash/loss envelope pass and a launch is authorized, review matured query orders, retained contribution and publisher/country delivery. Exclude clearly irrelevant queries at the narrowest effective scope; for relevant low-converting queries first inspect the offer, landing page, conversion delay and actual cost evidence. Cheap traffic is not the success measure. No CPC, CPA, volume or profit improvement has been observed from these files.

## Implementation constraints

All planned entities stay **Paused**, with existing US 506254907 and DE 506254908 preserved and the USD 0.15 cap unchanged. Actual country/language, cap availability, required native budget, editorial acceptance, destinations, tracking and consent still need live readback. Both current Microsoft distribution options include Search and Audience ads; negatives do not certify Search-only delivery. [Distribution documentation](https://learn.microsoft.com/en-us/advertising/msa-help/hlp_ba_conc_aboutaddistributionhidden).

This JSON is a review artifact. Microsoft Bulk RSA columns use asset arrays, and writing a headline/description field replaces the linked list; adding only the seven candidate headlines would drop the original eight. Merge the whole reviewed list against exact native IDs, validate escaping, preserve Paused status and capture the result. Fifteen headlines are not inherently better than eight. [RSA update rules](https://learn.microsoft.com/en-us/advertising/bulk-service/responsive-search-ad?view=bingads-13).

Parent next action: integrate the finalized country-language inventory, perform the native duplicate/control readback, and build only the exact paused rows whose required fields are resolved. Paid launch remains a separate acceptance decision.
