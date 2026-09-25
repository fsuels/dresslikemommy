# Portuguese-only campaign cleanup — verified

Campaign **DLM | MS | BR & PT | PT | Search | 202609** (`506255983`, account `477439`) remains **Paused**.

The English copied keywords have been removed. Current keyword and negative inventories exactly match the revised Portuguese payload:

| Level | Verified current records | Missing / extra / duplicate |
|---|---:|---|
| Target keywords | 144 Portuguese | 0 / 0 / 0 |
| Campaign negatives | 158 | 0 / 0 / 0 |
| Ad-group negatives | 66 | 0 / 0 / 0 |

This continuation removed **153 English target keywords, 86 English campaign negatives and 10 English ad-group negatives**. The full paused-keyword filter exposed one previously missed `mommy and me swimsuits` Exact keyword, resolving the earlier297-versus296count discrepancy. Before297=144Portuguese+153English; final native total144. The paused-keyword filter now returns no results.

All144remaining target text/match/group tuples were captured from the rendered table and compared against the Portuguese payload. Both final native negative exports were independently reconciled to the full intended lists. Ad-group negative counts are8dresses,16familyoutfits,10familyshirts,0pajamas,2father/son,22mother/daughterlooks,0swimwear,8sweaters. Pajamas and swimwear inherit campaign negatives; zero additional group negatives follows the supplied plan.

Earlier in this same correction pass, all8responsive ads were checked in their editors:120headlines,32descriptions,16displaypaths,8Portuguese finalURLs and8empty mobileURLs matched. Seven campaign sitelinks,28group associations,6callouts and7snippets were checked in Portuguese. The93remaining image associations contain88Portuguese-captioned and5uncaptioned images, with no English-captioned association. Brand names, file-format acronyms and URL identifiers retain their identity.

## Remaining platform editorial exceptions

Microsoft rejected the pajamas sitelink, pajamas snippet and two Portuguese image-caption replacements. The two English-captioned target associations were detached; original shared assets remain available. No rejection bypass or alternate-wording retry was attempted. **Language cleanup is complete; those four replacement/extension submissions still require normal editorial review.** No activation, monetary, source/peer/shared-content, tracking or storefront changes occurred.

Evidence: `review/portuguese_only_final_verification.json`, `review/portuguese_only_text_readback.json`, `negative_campaign_portuguese_only_final.csv`, `negative_group_portuguese_only_final.csv`. Current target payload: `payload/payload_portuguese_only.json`. The old mixed-language244/76plan and pending248-removal wording are superseded.

Canonical continuation: `ops/prompts/paid-growth-ai-army-continuation-prompt.md`, anchor `2026-09-23-microsoft-portuguese-keywords-cleanup-complete`. No further keyword cleanup or approval is pending.
