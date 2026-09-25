# Local browser bulk-upload candidates

**NOT UPLOADED. NOT PREVIEWED. NOT APPLIED.** These eight CSV candidates use Google Ads browser-upload templates, not Ads Editor schemas. They contain 146 data rows. Every group, ad, positive keyword and negative-keyword row explicitly says `Paused` (127 rows). No executable campaign CSV was created.

| Candidate | Data rows |
|---|---:|
| `01_ad_groups.PREVIEW_ONLY.csv` | 6 |
| `02_keywords.PREVIEW_ONLY.csv` | 48 |
| `03_responsive_search_ads.PREVIEW_ONLY.csv` | 6 |
| `04_campaign_negatives.PREVIEW_ONLY.csv` | 26 |
| `05_ad_group_negatives.PREVIEW_ONLY.csv` | 41 |
| `06_sitelink_associations.HELP_TEMPLATE_PREVIEW_ONLY.csv` | 14 |
| `07_callouts.HELP_TEMPLATE_PREVIEW_ONLY.csv` | 4 |
| `08_structured_snippet.HELP_TEMPLATE_PREVIEW_ONLY.csv` | 1 |

`campaign_stub.NOT_UPLOADABLE.json` retains a proposed Search/Manual CPC/Paused row with null budget type, amount and dates. It cannot be uploaded as a campaign CSV. Native template inspection confirms Manual CPC is an allowed value, even though the creation wizard did not offer it. The current native template requires Budget and an EU-political-ads classification on creation. Budget and USD currency remain unresolved.

All campaign associations use only `DLM | GADS | US | EN | Search | 202609`. The intended campaign must first resolve to the correct saved Paused record; a wizard draft is not assumed to be an importable campaign. Reconcile the existing eight dress keywords, RSA and four saved callouts before any Add actions. These are full target candidates, not an automatic delta against live account state.

The RSAs preserve all 72 headlines and 24 descriptions and set `Description 1 position` to `1`; all other pinning fields are omitted. Ad-group defaults use the proposed phrase amounts. Exact keywords set their own `Default max. CPC`; phrase keyword cells are blank to inherit the ad-group amount.

The 14 sitelink rows represent six distinct content definitions with their requested associations. They do not prove Google will create exactly six distinct asset objects; inherited assets and deduplication need native inspection. Callouts use the official Help template's campaign-level example; the snippet applies only to Mommy & Me Outfits. No asset status field is advertised by these templates, so asset association is conditional on a verified Paused parent.

## Schema limitations and required readback

- No verified browser-upload fields were found for Presence-only location targeting, purchase-goal/action selection, deduplication, consent, AI Max, text customization or final URL expansion. Check these natively; do not assume new campaign defaults match the recovered draft.
- The native negative template permits Level=Campaign and Paused, but generically labels Ad group required. Campaign rows deliberately leave it blank. Native Preview must validate campaign-level resolution and negative Paused semantics. Do not claim the proposed exclusions are effective.
- Callout and snippet files match the official Help templates; some examples use legacy naming. Their current account acceptance is unverified. Do not replace a rejected field with a guessed Ads Editor or Search Ads 360 field.
- Destination/category readiness and conditional receiving-group rules remain in the unchanged source payload. A valid CSV does not clear them or authorize activation.
- Parent-reported current draft recovery and settings are separately recorded in `../READBACK.md`. This worker did not access the account.

## Verification

`independent_validation.json` records **673 passing assertions** from a separate Python CSV readback: exact headers against downloaded sources, hashes, row counts, all 127 Paused statuses, exact copy/pinning, bid inheritance/overrides, 67 negative scopes, 14 sitelink associations, four callouts and one snippet. Source payload hash is unchanged. Native preview and Apply are NOT RUN. Artifact Tool authored/read back the cell matrices; a small RFC4180 serializer produced CSV because the available documented API did not expose CSV export. No visual workbook, formulas or XLSX were requested.

## Official sources

Google's [bulk-upload template index](https://support.google.com/google-ads/answer/10702525?hl=en) supplies the downloaded Help templates. [Spreadsheet formatting documentation](https://support.google.com/google-ads/answer/10702623?hl=en) describes browser-upload formatting and warns that omitted new-item status defaults to Enabled.

Current native links supplied from the root's Uploads template menu: [campaign](https://www.gstatic.com/adwords/campaignmgmt/templates/campaign_template.csv), [ad group](https://www.gstatic.com/adwords/campaignmgmt/templates/ad_group_template.csv), [RSA](https://www.gstatic.com/adwords/campaignmgmt/templates/responsive_search_ad_template.csv), [keyword](https://www.gstatic.com/adwords/campaignmgmt/templates/keyword_template.csv), and [negative keyword](https://www.gstatic.com/adwords/campaignmgmt/templates/ad_group_negative_keyword_template.csv).

Asset templates: [sitelink](https://storage.googleapis.com/support-kms-prod/er1LbgoAEsIctW1koPH6f4fDr7NNVDCKWPvh), [callout](https://storage.googleapis.com/support-kms-prod/Tqa4nGJSfFLXLSuw0Z4G17HVZJ1nAQMpYH37), and [structured snippet](https://storage.googleapis.com/support-kms-prod/EotlZJ2OljTMZYsB4Qx0a14sIJYwvqTU8Gpu).

Raw downloaded sources, including Google's example values, are preserved only for provenance in `sources/`; do not upload those raw templates. `candidate_manifest.json` maps each actual candidate to its source, hash, status field and unresolved gates.
