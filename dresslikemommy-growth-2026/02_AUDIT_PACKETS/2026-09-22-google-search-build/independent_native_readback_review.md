# Independent native export review

**PASS_WITH_LIMITS** — 349 final source checks passed; no saved-content defects found.

Verified independently from the supplied native exports:

- 48 Paused keywords, eight per group,24exact/24phrase, all USD bids match the payload.
- 67 negative keywords:26campaign/41ad-group; exact text, match types and scopes match.
- 14 sitelink associations with exact text/descriptions/URLs, four campaign callouts and one correctly scoped Types snippet.
- Two saved Paused RSAs: Mommy & Me Dresses and Family Matching Outfits. Each matches12headlines/four descriptions, first-description pin1, URL and paths; all other pins are empty.

**Overall build remains PARTIAL.** Family Matching Shirts, Mommy & Me Pajamas, Father & Son Shirts and Mommy & Me Outfits have no saved ad rows. Parent reports entered wizard fields blocked by a new Google verification prompt; those fields are not counted as saved.

All48keywords,2ads and19requested assets show Draft change=Yes. Requested asset statuses are Enabled, separately from campaign-paused reasons in keyword/ad reports. One additional Account-level Call association is inherited, outside the requested new assets, and omitted from new-asset counts.

Negative status is absent from its export. Campaign budget/date fields are absent from all four exports, so this review does not independently verify210USD Campaign Total/seven-day settings. Current user authority permits that setup while paused; provisionalSep22-28 dates are not activation approval. Original payload budget gates are an older snapshot superseded by the current user choice.

Keyword/ad reports omit campaign identity columns; their exact campaign scope depends on parent-supplied export provenance. Negative/asset reports explicitly name the campaign. This is saved-file verification, not a fresh browser read or complete historical activation audit.

The three operator verification summaries agree. Keyword totals were explicitly excluded wherever their Total label occurs, including the Match type field. An initial first-column-only filter was corrected and all keyword checks rerun; no genuine extra keyword existed.

Source hashes, row filtering and exact executed checks are retained in independent_native_readback_review.json. No browser, external write or canonical-file edit was performed by the reviewer.

Next: complete normal Google verification, save the four remaining RSAs, then obtain a six-ad export. Keep campaign and positive entities paused.
