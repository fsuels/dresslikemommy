# Google Ads International Search Subagent Handoff

Date: 2026-05-07

Scope completed: local-only planning/build artifacts for segmented paused country Search tests. No Google Ads UI/API, no live campaign creation, no campaign enablement, no budget/bid/status edits, no keywords imported, no conversion-goal edits, and no Standard Shopping/PMax/Remarketing work.

## Done

- Read the existing paused US nonbrand rebuild builder and artifacts.
- Treated existing US nonbrand campaign `23827590655` as the template, not something to duplicate.
- Built local draft artifacts for 17 non-US country campaigns:
  - GB, CA, AU
  - CH, DK
  - DE, NL, SE, FR, BE, ES, IT
  - PL, CZ, RO, GR, PT
- Kept all proposed rows paused-only, Search-only, Manual CPC, exact/phrase-only, and English-only until localization/shipping QA clears local-language variants.
- Kept CPC caps at `$0.10` to `$0.15`, with no cap above `$0.20`.
- Preserved the same six theme structure as the US nonbrand rebuild: Mommy & Me Dresses, Family Matching, Vacation Family, Matching Pajamas, Matching Swimwear, Daddy & Me.

## Files Created

- `build_intl_search_packet.py`
- `GOOGLE_ADS_INTL_SEARCH_INFRASTRUCTURE_PLAN.md`
- `SUBAGENT_HANDOFF.md`
- `manifest.json`
- `country_tier_plan.csv`
- `campaign_structure.csv`
- `keyword_plan.csv`
- `negative_keyword_plan.csv`
- `rsa_copy_pack.csv`
- `web_bulk_upload/00_intl_search_paused_draft_web_bulk.csv`
- `manual_qa/intl_search_pre_import_qa.csv`
- `manual_qa/approval_gate.md`

## Build Readback

- Proposed non-US campaigns: `17`.
- Web bulk rows: `1666`.
- Campaign rows: `17`.
- Ad group rows: `204`.
- Keyword rows: `612`.
- Campaign negative rows: `629`.
- RSA rows: `204`.
- Max CPC ceiling in packet: `$0.15`.
- Existing US campaign: not duplicated.

## Verification Commands

- `python3 dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/build_intl_search_packet.py`
- `python3 -m py_compile dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-07-paid-growth-parallel-infra-sprint/google-ads-intl-search/build_intl_search_packet.py`
- CSV validation script run inline from the shell, confirming row counts, paused statuses, exact/phrase-only keywords, no US duplicate, no CPC over `$0.20`, RSA length limits, and no unsupported shipping/returns claims.

## Approval Gate

Live paused campaign creation still requires the exact owner approval phrase stored in `manual_qa/approval_gate.md`. This packet is not an enablement approval.

After any future approved import, the required readback is:

- Existing US nonbrand campaign `23827590655` still paused and not duplicated.
- Every new country campaign, ad group, keyword, and RSA paused.
- One country per campaign.
- Presence-only location option.
- Google Search only.
- Manual CPC with every default max CPC at or below `$0.20`.
- Exact/phrase keywords only; no broad.
- Campaign negatives present.
- Conversion goals inherited/read back; no conversion-goal edits.
- Policy/ad review clean enough before any later enable request.
- Landing, shipping, checkout, Merchant/catalog, and economics gates passed per country.

## Residual Risk

- The local draft uses English-only keywords and RSAs for all non-US countries; local-language variants are intentionally deferred to the localization/creative lanes.
- Presence-only targeting may need a post-import UI/API confirmation because the local web bulk format does not encode that setting reliably.
- Bulk upload preview must return zero errors before any future apply.
