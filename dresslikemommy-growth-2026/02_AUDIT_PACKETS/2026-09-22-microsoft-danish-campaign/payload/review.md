# Danish campaign payload review

LOCAL REVIEW PAYLOAD — no external writes or live verification by this worker.

Target: account 477439/customer 770182, existing campaign 506254908 → `DLM | MS | DK | DA | Search | 202609`, Denmark/Danish. Preserve Paused, observed 3.00 budget, bidding and images. Root owns live readback, exact approval scope and all writes. The current user's DK decision supersedes the attachment's US geography; no new campaign or launch is proposed here.

Source: `/Users/fsuels/.codex/attachments/a344cc3d-d59d-4935-a7ce-9ed44882a3b9/Pasted text.txt`. SHA256 `fd3d004ba6258762252d6a494a24ab0aac1fba7afd18b20d5a89076478c8c98e`.

| Group | Danish name | Positive entries | Group negatives | Routing condition |
|---|---|---:|---:|---|
| 1 | Kjoler til mor og datter | 17 | 6 | Source category exclusion or no group negatives |
| 2 | Matchende familietøj | 20 | 8 | CONDITIONAL_DO_NOT_APPLY_BLINDLY |
| 3 | Familieskjorter og T-shirts | 18 | 6 | CONDITIONAL_DO_NOT_APPLY_BLINDLY |
| 4 | Nattøj til mor og datter | 17 | 0 | Source category exclusion or no group negatives |
| 5 | Skjorter til far og søn | 15 | 8 | Source category exclusion or no group negatives |
| 6 | Matchende tøj til mor og datter | 16 | 11 | CONDITIONAL_DO_NOT_APPLY_BLINDLY |
| 7 | Badetøj til mor og datter | 18 | 0 | Source category exclusion or no group negatives |
| 8 | Matchende familietrøjer | 23 | 6 | Source category exclusion or no group negatives |

Verified locally: 8 groups, 144 positive entries, 120 headlines (15 each), 32 descriptions (4 each), 192 campaign Phrase negatives (112 Danish + 80 supplementary English), 9 temporary Exact negatives, 45 group negatives, 8 sitelinks, 6 callouts and 8 structured snippets. All supplied text fields pass attachment limits; maximum headline 30/30, description 90/90, path 14/15, callout 23/25, sitelink title 24/25, sitelink description 34/35. Zero literal positive-versus-own-group/campaign-negative conflicts and zero duplicate same-text/same-match rows within a group. Exact and Phrase pairs are intentional. All 628 extracted customer-facing text values occur unchanged in the supplied source.

## Conditions root must resolve

- Group 2 negatives route to 3/8; group 3 to 5/8; group 6 to 1/4/7/8. Preserve Exact match. Apply each only after corresponding recipient readiness is verified. Attachment explicitly conditions 2/6; the same gate is conservatively marked for 3. Source category-specific Phrase exclusions in 1/5/8 must stay at group level. No broad category negatives are introduced.
- Candidate UTMs use `dlm_ms_dk_da_search_202609`. Do not apply before root confirms manual tagging/no duplicate inherited or automatic tags and checks copied ad-level suffixes. Null templates/custom parameters are no-change placeholders, not clearing instructions. Never translate `bing`, `cpc`, `{AdId}` or `{Keyword}`.
- Every URL is supplied `/da/collections/…` text, not current endpoint evidence. Source author could not verify family-tops/family-sweaters and reported mixed English on pajamas/swimsuits. Current public verification may supersede those historical warnings. Do not attach unverified sitelink destinations.
- 192 campaign Phrase negatives intentionally include 80 supplementary English entries; group-level shirt/swim/sweater English exclusions also remain. These are relevant exclusions, not untranslated positive targeting. Do not alter another campaign's shared assets or lists.
- Brand `Dress Like Mommy`, established Danish loanwords such as T-shirts/outfits, URL slugs and tracking tokens are preserved as supplied; source copy is faithfully extracted, not rewritten.

## Exact missing inputs

1. The 160 image Name/Display Text and Alt Text pairs are referenced but not present; no ZIP, download URL or image mapping was supplied. Zero of these 320 fields was validated. Root may obtain missing pairs or inspect actual copied images/captions for faithful Danish translation; never infer pictured people/garments.
2. Root native inventory/readback of copied IDs, current names/text, all inherited/shared assets and keyword/negative/settings state.
3. Root destination and recipient readiness evidence, and tagging readback as above.

No Keyword Planner demand/CPC, performance, eligibility, purchases or profit are established. Matching validation is literal and cannot reproduce Microsoft's full matching or account-level negatives. The 9 temporary assortment Exact negatives are preserved from source, not freshly stock-qualified.

Reproduce local extraction and checks: `python3 /Users/fsuels/Projects/dresslikemommy/dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-09-22-microsoft-danish-campaign/payload/extract_validate.py`.
Machine-readable content: `payload.json`. No canonical files changed by worker; root integrates its own state/claim/worklog.
