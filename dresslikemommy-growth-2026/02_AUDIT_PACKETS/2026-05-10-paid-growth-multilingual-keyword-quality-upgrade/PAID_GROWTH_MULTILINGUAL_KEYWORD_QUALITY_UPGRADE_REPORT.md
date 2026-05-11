# Paid Growth Multilingual Keyword Quality Upgrade

Generated: 2026-05-10

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-keyword-quality-expert-hardening`

Mode: local-only evidence and campaign-quality planning. No Google Ads or Pinterest account objects were created or edited. No live spend, enablement, budget, bid, status, feed, product, product-group, conversion-goal, Merchant, Shopify, Pinterest, GA4/GTM, or theme change occurred.

## Executive Decision

`LOCAL_EXPERT_HARDENED_KEYWORD_QUALITY_PACKET_READY_NATIVE_REVIEW_GATED`

The existing Google Search campaign infrastructure is structurally complete for the safe paused English-first path: all one-country split files still contain tightly scoped exact/phrase keywords, one RSA per ad group, paused statuses, country-qualified final URLs, and tight negatives. The quality gap is language depth, not raw campaign structure.

To satisfy "best keywords in each language" without bloating live accounts or violating guardrails, this packet stages a separate native-language second-stage plan:

- `google_ads_native_language_keyword_master.csv`: 700 native exact/phrase keyword rows across 14 locale variants and 5 themes.
- `google_ads_native_language_rsa_quality_pack.csv`: 70 RSA rows, each with 15 headlines and 4 descriptions, all under Google character limits.
- `google_ads_native_negative_keyword_review_plan.csv`: 205 localized negative-keyword review rows for DIY, pattern, used, wholesale, costume, PDF, marketplace, and supplier intent.
- `google_ads_native_campaign_shell_plan.csv`: proposed native campaign naming and gating for every local-language lane, marked `REVIEW_ONLY_NOT_UPLOAD`.
- `google_ads_english_first_keyword_expansion_candidates.csv`: expansion candidates for existing English-first Search campaigns, held for search-term-proof or a separately approved paused edit.
- `pinterest_multilingual_keyword_interest_quality_plan.csv`: Pinterest local copy/catalog-term plan that respects Pinterest catalog-sales behavior and keeps non-US Pinterest account writes gated.

All native Google Ads and Pinterest planning rows in this packet are local-only and marked `REVIEW_ONLY_NOT_UPLOAD`; none are upload-ready account instructions.

## Official Platform Basis

Google's Search quality guidance ties Quality Score diagnostics to expected CTR, ad relevance, and landing-page experience. Google also says responsive search ad Ad Strength should be improved with more unique assets, keyword-relevant copy, and enough headlines/descriptions. Google keyword match documentation confirms exact match provides tighter steering and phrase match is broader but still controlled. This packet therefore keeps first-launch Search exact/phrase only and avoids broad-match expansion until conversion tracking and bidding gates are trustworthy.

Pinterest's Shopping Ads help states that shopping ads require a business account, uploaded catalog, and product groups, and that keyword or interest targeting is not necessary for catalog sales campaigns. Pinterest campaign structure guidance puts regions, product lines, targeting, budget, and bids at the ad group level, and Pinterest policy emphasizes consistent ad/landing-page experience and ad quality. This packet therefore treats Pinterest "keyword quality" as catalog terms, product-group naming, promoted Pin copy, and destination consistency, not as a Google-style keyword import.

Sources used:

- Google Ads Help, About Quality Score for Search campaigns: https://support.google.com/google-ads/answer/6167118
- Google Ads Help, About keyword matching options: https://support.google.com/google-ads/answer/7478529
- Google Ads Help, About Ad Strength for responsive search ads: https://support.google.com/google-ads/answer/9921843
- Google Ads Help, Create effective Search ads: https://support.google.com/google-ads/answer/6167122
- Pinterest Business Help, Create shopping ads: https://help.pinterest.com/en/business/article/shopping-ads
- Pinterest Business Help, Campaign structure: https://help.pinterest.com/en-gb/business/article/campaign-structure
- Pinterest Advertising Guidelines: https://policy.pinterest.com/en/advertising-guidelines

## Google Ads Status

- Current English-first non-US campaign build: `12 built / 3 absent / 2 parked`, unchanged from the authority-safe-launch-prep anchor.
- Current US nonbrand Search: campaign `23827590655` exists as paused infrastructure and must not be duplicated.
- All current Search keyword rows remain exact/phrase only.
- Every existing RSA row parsed in the audited files has 15 headlines. Current split non-US files have 4 descriptions per RSA; the US nonbrand packet also has one RSA per ad group.
- Native-language copy is not platform-ready until native review, landing-language QA, and exact approval.
- The US paused nonbrand packet still contains `Vacation Family` ad groups. They remain a hold under the existing beach/Christmas metadata blocker and must not be included in a future enable action unless the metadata blocker is solved or those ad groups are deliberately excluded.

## Native-Language Gates

- Expert hardening note: RSA headline casing now preserves natural phrase casing instead of forcing title case across all languages. This avoids obvious machine-generated casing in Spanish, Italian, French, Dutch, Swedish, Danish, Polish, Czech, Romanian, Portuguese, and Greek.
- `es-ES`, `it-IT`, `ro-RO`: concept-ready after this packet, still native-review and landing-QA gated.
- `de-DE`, `nl-NL`, `fr-FR`, `sv-SE`, `pl-PL`, `cs-CZ`, `el-GR`: keyword/RSA pack exists, still native-review plus native landing-language QA gated.
- `pt-PT`: platform-use-blocked until Portugal storefront language behavior is resolved or explicitly accepted because prior `/pt` behavior read as `pt-BR`.
- `da-DK`: platform-use-blocked until Danish native review/rewrite confirms the corrected wording.
- `fr-BE`, `nl-BE`: platform-use-blocked until Belgium French/Dutch split and route proof are decided.
- `CH`: no ambiguous native Swiss campaign should be created; decide English-first, German, French, Italian, or split setup first.

## Pinterest Status

Pinterest is not keyword-import-ready for non-US. The local plan provides catalog/copy terms, but every non-US Pinterest market remains account-write-gated because country-specific source/catalog/product-group readbacks do not exist. For Pinterest catalog sales, the safe quality focus is:

- clean product source and product groups,
- destination consistency,
- readable and policy-safe creative,
- market/country targeting readbacks,
- Event Quality/tag proof before spend.

## Expert-Level Stop Conditions

- Do not import machine-generated native rows directly. Native reviewer PASS/REWRITE/REJECT is required per locale.
- Do not add all expansion keywords at once. Keep the existing English-first campaigns tight and use expansion terms only after search-term proof or separately approved paused edits.
- Do not use broad match until conversion tracking, Smart Bidding readiness, search-term hygiene, and ROAS guardrails are proven.
- Do not use native-language ads where the storefront still serves English or a different dialect unless the owner explicitly accepts that mismatch.
- Do not treat Pinterest as a keyword-import platform; use Pinterest catalog/source, product groups, creative consistency, and Event Quality as the quality system.

## Files Created

- `README.md`
- `PAID_GROWTH_MULTILINGUAL_KEYWORD_QUALITY_UPGRADE_REPORT.md`
- `google_ads_current_search_campaign_quality_audit.csv`
- `google_ads_existing_keywords_by_market_theme.csv`
- `google_ads_native_language_keyword_master.csv`
- `google_ads_native_language_rsa_quality_pack.csv`
- `google_ads_native_negative_keyword_review_plan.csv`
- `google_ads_native_campaign_shell_plan.csv`
- `google_ads_english_first_keyword_expansion_candidates.csv`
- `pinterest_multilingual_keyword_interest_quality_plan.csv`
- `keyword_quality_validation_summary.json`
- `GOOGLE_ADS_NATIVE_LANGUAGE_IMPORT_GATES.md`
- `PINTEREST_KEYWORD_QUALITY_GATES.md`
- `EXPERT_QA_REVIEW_NOTES.md`
- `NEXT_CONTINUATION_PROMPT.md`
- `working/build_keyword_quality_upgrade_packet.py`

## Guardrails Preserved

- No live spend.
- No campaign enablement.
- No budget, bid, or status changes.
- No PMax, Standard Shopping, product-scope, feed-label, product-group, or conversion-goal change.
- No Merchant upload/source edit/sync.
- No Shopify live product-data change.
- No Pinterest account/campaign/draft/product-group/catalog/source/tag/CAPI/audience/budget/bid/status/spend write.
- No checkout payment, order, refund, or cancelation.

## Next Best Action

1. Native review the `google_ads_native_language_keyword_master.csv` and `google_ads_native_language_rsa_quality_pack.csv` rows per locale.
2. Keep the existing English-first paused campaigns as the first controlled Search path after measurement proof and exact enable approval.
3. Do not import the native campaign shell plan until native review, landing-language QA, and exact action-time approval are complete.
4. For Pinterest, resolve the US/Event Quality gate before non-US account builds; use the Pinterest CSV here only as local copy/catalog-term guidance.
