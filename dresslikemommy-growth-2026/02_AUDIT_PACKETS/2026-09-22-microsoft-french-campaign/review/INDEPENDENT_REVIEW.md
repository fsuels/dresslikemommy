# Independent French campaign payload review

Follow-up: source metadata is corrected and root reports user confirmation of France and Canada. The later `LANDING_QA.md` supersedes those open items below and supplies current public HTTP evidence for all eight destinations. The initial review below is retained as the original review record.

Verdict: **PASS for bounded paused construction; current live destination and inherited-setting verification remain with the root operator.** This is an independent local review, not an account readback or authorization to enable.

Target: Microsoft account `477439`, paused campaign `506255077`, `DLM | MS | FR & CA | FR | Search | 202609`. Root-supplied live source: US English campaign `506254907`, seven groups. Root retains all external-write authority and ownership. No browser, source campaign, shared asset, or canonical state writes were performed by this reviewer.

## Verified local content

`check_payload_independently.py` independently split the supplied attachment and compared each group's name, URL, keywords, ad copy, and negatives with the JSON payload. All **225 checks passed**. Result details and input hashes are in `independent_payload_validation.json`.

- Eight groups; 144 positives: 62 exact and 82 phrase.
- 120 headlines and 32 descriptions, within the attachment's 30/90 character limits; all display paths within 15 characters.
- 251 campaign negatives: 151 French phrase, 86 complementary English phrase, 14 temporary exact restrictions.
- 58 group negatives; no literal or conservatively accent/punctuation-folded positive conflicts at campaign or same-group scope.
- Six callouts, eight sitelinks, and eight structured snippets meet the checked text limits. Sitelink destinations and group associations are internally consistent.
- Eight proposed FR/CA UTM campaign tokens correctly replace the attachment's US/FR token. These remain candidates until the root confirms geography and live tracking inheritance.

## Required corrections and operational readbacks

1. **Metadata correction:** `source_campaign_name` currently identifies the attachment's prepared US/French campaign. It must not be mistaken for the live copied US/English source. Rename it to an attachment-specific field or explicitly store live copy source ID/name alongside it.
2. **Geography:** the attachment explicitly specifies the United States; the current requested target name specifies FR & CA. Root must resolve that conflict before changing location settings or finalizing geographic tracking tokens. Paused language/copy work can proceed independently.
3. **Inherited content:** verify all copied ad text, display paths, final URLs, keywords, negatives, group language, text extensions, and lower-level tracking. English supplementary negatives are intentionally retained. Do not alter source/shared assets to localize the target.
4. **Landing truth:** current landings were not verified by this reviewer. The attachment flags family-tops and family-sweaters as unverified and father-son/cart/shipping text as partly English. Assortment-specific claims include t-shirts, tankinis, cardigans, cable knit, and hoodie styles; verify visible matching products before claiming complete landing readiness. Per-piece and size statements must match the actual purchase selection.
5. **Routing exclusions:** exact negatives in groups 2, 3, and 6 exclude narrower categories. They may be staged with the paused structure but require corresponding destination groups to be eligible before campaign activation. They do not guarantee traffic transfers to those groups.
6. **Images:** the pasted attachment does not contain the 160 claimed caption/alt pairs or usable download links. Preserve source imagery; inspect copied image metadata and associations. Do not invent image-specific descriptions or edit shared image records.
7. **Parities that are not translation:** preserve the target's existing paused state, 20/day budget, and Enhanced CPC while constructing. The source's Maximize Clicks setting is a separate bidding decision. No activation, budget, billing, or source-campaign change is covered by this review.

The 14 temporary catalog negatives exactly reproduce the supplied attachment; their historical assortment premise is not freshly verified. No literal conflict was found, and they must remain exact.

Root's final native readback should establish the final group/keyword/ad/negative counts, French language and visible text, exact geography, paused status, unchanged source/shared objects, destination fit, and remaining approval or platform failures. Local checks do not establish editorial approval, live eligibility, conversion receipt, or sales.
