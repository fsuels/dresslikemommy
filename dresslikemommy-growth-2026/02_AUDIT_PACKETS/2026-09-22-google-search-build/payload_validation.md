# Google Search payload validation

Validation: **PASS_LOCAL_PAYLOAD_ONLY**. Source SHA-256: `26f43ab53bdb959faf498f17d7c4505a55150790cab0679211e0b136c1aaa9b5`.

Source: `/Users/fsuels/.codex/attachments/25001adb-eb38-4875-82c3-c75f8c00cd7c/Pasted text.txt`. Campaign: **DLM | GADS | US | EN | Search | 202609**. This local artifact preserves the supplied copy exactly; it is not a live Google Ads readback.

## Exact inventory

- Six standard Search ad groups; 24 expressions entered as 24 exact and 24 phrase keywords (48 entries).
- Six RSAs; 12 headlines and four descriptions each (72/24 total). Only description 1 is pinned to `DESCRIPTION_1`; all headlines and remaining descriptions are unpinned.
- Campaign negatives: 18 phrase DIY/download/employment entries, four exact navigational entries and four temporary category phrase safeguards (26 total). The temporary safeguard campaign scope follows their test-wide intent.
- Ad-group negatives: five sleepwear phrase entries in each non-pajama group (25 associations), plus 8/4/4 exact routing negatives in Family Matching Outfits / Family Matching Shirts / Mommy & Me Outfits (16 associations). Total: 67 negative associations.
- Six sitelinks and 14 proposed ad-group associations; four callouts; one `Types` structured snippet associated only with Mommy & Me Outfits. The duplicate sitelink labels in the attachment were correctly treated as section label plus one asset text, not duplicate assets.

## Actual text lengths

All text lengths were calculated from the actual extracted strings. All 96 pasted headline/description counts match. Headlines are at most 30, descriptions at most 89, paths at most 15, sitelink titles at most 25, sitelink descriptions at most 35, and callouts/snippet values at most 25.

| Ad group | Headline lengths | Description lengths | Display paths | Default / exact CPC (USD, proposed) |
|---|---|---|---|---|
| Mommy & Me Dresses | 18, 25, 25, 21, 24, 28, 17, 29, 27, 28, 20, 16 | 85, 86, 87, 87 | 8, 7 | 0.15 / 0.20 |
| Family Matching Outfits | 23, 30, 27, 25, 23, 24, 25, 28, 29, 28, 24, 16 | 87, 87, 82, 89 | 6, 14 | 0.12 / 0.18 |
| Family Matching Shirts | 22, 30, 23, 23, 30, 26, 28, 25, 25, 27, 28, 16 | 82, 86, 87, 84 | 6, 15 | 0.15 / 0.20 |
| Mommy & Me Pajamas | 18, 25, 29, 28, 27, 26, 25, 28, 21, 27, 23, 16 | 86, 85, 88, 83 | 8, 7 | 0.15 / 0.20 |
| Father & Son Shirts | 28, 25, 27, 20, 29, 30, 20, 27, 28, 29, 24, 16 | 84, 86, 89, 88 | 11, 6 | 0.15 / 0.20 |
| Mommy & Me Outfits | 18, 25, 27, 25, 27, 30, 25, 24, 28, 28, 29, 16 | 89, 84, 86, 89 | 8, 7 | 0.10 / 0.15 |

| Sitelink | Title / description 1 / description 2 lengths |
|---|---|
| Mommy & Me Dresses | 18 / 29 / 33 |
| Family Matching Outfits | 23 / 29 / 29 |
| Family Matching Shirts | 22 / 32 / 28 |
| Mommy & Me Pajamas | 18 / 25 / 32 |
| Father & Son Shirts | 19 / 32 / 26 |
| Mommy & Me Outfits | 18 / 33 / 31 |

Callout lengths: 21, 23, 15, 19. Snippet value lengths: 7, 7, 13.

## Collision and duplicate checks

Zero duplicate positive entries within or across groups; exact/phrase pairs are deliberate distinct entries. Zero duplicate negatives within an identical scope. Zero repeated headline or description within an RSA. Reuse across distinct RSAs (for example the business name) is deliberate.

Zero literal collisions between all 48 positive entries and their applicable campaign/ad-group negatives. Check method: case-fold and collapse whitespace, then whole-query equality for exact negatives and contiguous whole-token matching for phrase negatives. No stemming, synonym or semantic expansion was simulated.

Eight independently authored wanted-query cases pass. These are new examples for this validation, not a reconstruction of the unspecified eight examples claimed in the source:

- Family Matching Outfits: `matching family dress and shirt` — not excluded by applicable literal negatives.
- Family Matching Outfits: `matching family outfits free shipping` — not excluded by applicable literal negatives.
- Mommy & Me Dresses: `mommy and me dresses on sale` — not excluded by applicable literal negatives.
- Family Matching Shirts: `matching family t shirts for pictures` — not excluded by applicable literal negatives.
- Father & Son Shirts: `father son matching hawaiian shirts for vacation` — not excluded by applicable literal negatives.
- Mommy & Me Pajamas: `mommy and me short sleeve pajamas` — not excluded by applicable literal negatives.
- Mommy & Me Pajamas: `mommy and me long sleeve pajamas` — not excluded by applicable literal negatives.
- Mommy & Me Outfits: `mother daughter matching outfits baby` — not excluded by applicable literal negatives.

## Authority and unresolved gates

The parent may prepare this campaign only as a draft or safely paused, subject to the current user scope and fresh account readback. The attachment explicitly leaves financial approval and activation separate. The payload worker performed no external reads or writes and does not grant account authority.

- Budget type/amount/dates remain **UNSELECTED**. The source offers three alternatives ($210 campaign total, $30 average daily with a management stop, or $15 unchanged average daily for exactly seven active calendar days). None is silently selected or treated as approved exposure.
- USD account currency must be verified before entering the proposed Manual CPC amounts. Default equals the lower phrase amount, with exact keyword overrides; neutral adjustments protect the intended ceilings. No existing campaign recreation, budget change, activation or spend is authorized by this artifact.
- Purchase transaction ID/value/currency receipt, authoritative purchase goal/deduplication, consent/attribution, real US shipping/checkout, exact category/product readiness, inherited exclusions/assets and account controls still require parent verification. These local checks provide no purchase, delivery, demand or profitability evidence.
- All routing exclusions remain conditional on the intended receiving group being active and eligible; sleepwear routing additionally permits an explicit decision to keep that traffic outside the test. Floral entries require relevant product/buyer-path clearance.
- Sitelinks create additional purchase paths and must use cleared destinations only. General callout campaign scope is an explicitly marked operator inference because the source does not specify a level; parent must verify the chosen association.
- Campaign-language availability, total-budget availability and account/shared inherited state are live facts not checked here. Source assertions about current Google features are retained as proposals/qualification notes, not independently verified product documentation.
- A flow that would enable the campaign must not be completed with a plan to pause afterward.

## Checks run and scope

Python standard-library extraction and assertions verified source counts, bid mapping, text limits, pinning, URL alignment, distinct scopes, duplicate entries and literal collisions. `payload.json` was parsed back after writing. A separate source-to-payload pass completed 337 assertions, including copy provenance, exact/phrase pairs, bid micros, correct pinning, matching destination URLs and negative receivers. The scoped `git diff --check` command exited 0. Only `payload.json` and `payload_validation.md` are owned by this worker; canonical state and all external actions remain with the parent.

Substantive copy errors found: **none**. Remaining limitations are live readiness and authority gates.

## Parent-reported creation boundary

The parent reports that Google displayed **Confirm it’s you** and **Changes failed to save** during review navigation. This worker did not access or independently verify that UI. The earlier shell reportedly displayed **All changes saved** for draft `10215314947` / creation campaign `281499249292033`; persistence of the first entered RSA and eight keywords remains unconfirmed.

The parent also reports that the creation selector did not offer Manual CPC. The incomplete UI has Clicks selected with its maximum-CPC checkbox checked but amount blank; the budget UI auto-populated 11.53/day without an owner choice. These values are **not** substituted into the target payload, are **not** approved financial choices, and do not satisfy the requested deliberate keyword bids. `payload.json` retains Manual CPC as the proposed target and keeps selected budget null. Resume only after the user completes Google's normal authentication, then reconcile the saved draft against the payload before further changes or review submission.
