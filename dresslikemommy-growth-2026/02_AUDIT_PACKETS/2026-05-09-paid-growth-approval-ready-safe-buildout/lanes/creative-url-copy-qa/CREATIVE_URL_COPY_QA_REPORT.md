# Creative / Final URL / Copy QA For Held Non-US Search CSV

Generated: 2026-05-09

Decision: `PASS_LOCAL_ONLY_APPROVAL_GATED`

## Scope

Worker D inspected the held non-US Google Search CSV and prior local evidence only. No Google Ads preview, import, campaign build, campaign enablement, Shopify Admin write, Merchant write, Pinterest write, feed edit, theme edit, product-data write, budget/bid/status change, conversion-goal change, checkout payment, or order action was made.

Assigned write scope only:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-09-paid-growth-approval-ready-safe-buildout/lanes/creative-url-copy-qa/`

## Inputs

- Held CSV: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/web_bulk_upload/00_intl_search_paused_draft_web_bulk_vacation_family_hold.csv`
- URL-hold report: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/PAID_GROWTH_URL_HOLD_CHECKOUT_SAFE_ADVANCE_REPORT.md`
- URL-hold validation: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/google-ads-url-hold/GOOGLE_ADS_INTL_URL_HOLD_VALIDATION.md`
- Landing metadata report: `dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-url-hold-checkout-safe-advance/lanes/landing-url-quality/LANDING_METADATA_QUALITY_REPORT.md`
- Localization reports from `2026-05-08-paid-growth-controlled-infra-refresh`, `2026-05-08-paid-growth-ai-army-safe-advance-2`, and `2026-05-08-paid-growth-safe-followup`
- Prior creative/economics guardrails, including the unsupported-claims blacklist

## Validation Script

Added and ran:

`validate_held_csv_creative_urls.py`

The first run failed because the script resolved the repo root one directory too high. I fixed the script to discover the repo root by walking upward to `AGENTS.md`, reran it, and produced:

`creative_url_copy_qa_summary.json`

Final script result: `PASS_LOCAL_ONLY_APPROVAL_GATED`.

## Held CSV Shape

| Check | Result |
|---|---:|
| Total rows | `1496` |
| Campaign rows | `17` |
| Ad group rows | `170` |
| Positive keyword rows | `510` |
| Negative keyword rows | `629` |
| Ad rows | `170` |
| Final URL rows | `680` |
| Unique final URLs | `85` |
| Campaign languages | `17` x `en` |

All campaign rows are paused Search campaigns on Google Search only, Manual CPC, with country-specific locations. This lane did not preview or import them.

## Country And URL Coverage

Country coverage passed for all 17 target non-US markets:

`AU`, `BE`, `CA`, `CH`, `CZ`, `DE`, `DK`, `ES`, `FR`, `GB`, `GR`, `IT`, `NL`, `PL`, `PT`, `RO`, `SE`

Final URL country-parameter coverage passed:

- `40` final-URL-bearing rows per country.
- `0` missing `country=<ISO>` parameters.
- `0` campaign-country / final-URL-country mismatches.
- `0` bare language-only URLs.
- `0` localized path mismatches.

URL posture:

- `ES`, `IT`, `RO`, and `PT` use localized product paths plus `country=<ISO>`.
- All other markets use base English product paths plus `country=<ISO>`.
- This matches prior evidence that bare `/es`, `/it`, `/ro`, and `/pt` routes are unsafe for paid final URLs because fresh visitors can land in English / United States / USD without the country parameter.

## Language / Localization Posture

The held CSV is an English-language Search packet:

- Campaign language is `en` for all 17 campaigns.
- RSA copy is English across all campaigns.
- ES/IT/RO/PT final URLs are localized, but the ad copy itself is not localized.

Readiness interpretation:

- Pass for a paused, English-language infrastructure build after exact owner approval and preview-only import validation.
- Not a native-language paid-traffic launch packet.
- Before any live spend, ES/IT/RO/PT need an owner decision on whether English ad copy to localized landing pages is acceptable, or whether local-language ads/keywords should be prepared separately.
- CH/DK/DE/NL/SE/FR/BE/PL/CZ/GR remain English-shell markets until local-language landing/policy/checkout QA clears.

## Unsupported-Claim Scan

Customer-facing ad-copy fields scanned:

- Headlines 1-15
- Descriptions 1-4
- Paths
- Website description

Blocked claim categories scanned:

- fast shipping / rush shipping / same-day or guaranteed delivery
- warehouse, local stock, store pickup, nearby inventory, stocked inventory, on-hand stock
- guaranteed inventory or guaranteed availability
- review counts, star ratings, top-rated claims
- promos, discounts, coupons, free gifts, limited-time offers, free shipping/free delivery claims
- bestseller, most popular, viral, trending, customer-favorite claims

Result: `0` customer-facing unsupported-claim hits.

The validator also scanned targeting/URL fields separately and found `0` unsupported-claim hits there. A manual raw scan initially surfaced `sale` inside the negative keyword `wholesale`; the validator avoids that false positive by using word boundaries and separating negative keywords from ad copy.

Length checks passed:

- Max headline length: `24` characters, under the 30-character RSA limit.
- Max description length: `75` characters, under the 90-character RSA limit.

## Stale Christmas / Vacation Family / Bad-Handle Exclusion

The held CSV keeps the known bad beach product out of the candidate:

- Bad handle hits: `0`
- Bad product ID `7227378892897` hits: `0`
- Exact `Vacation Family` theme/ad-group phrase hits: `0`
- `Christmas` / `Xmas` hits: `0`

Prior evidence remains important: the held list contains all 17 `Vacation Family` rows tied to `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH`. Do not reintroduce that product/theme until owner-approved Shopify SEO/social metadata repair passes public readback, or until the URL is swapped for a clean paid candidate.

## Paid-Traffic Copy Risks

The held CSV is clean enough for local/paused infrastructure, but live spend remains blocked.

Risks to keep gated:

- English-only ad copy across all 17 campaigns. This is not native-language market coverage.
- ES/IT/RO/PT localized final URLs can create an ad-language / landing-language mismatch if used as English-targeted Search without owner acceptance.
- Generic `holidays` wording appears in pajama copy, but no stale `Christmas` metadata/copy remains in the held CSV. Keep the blocked beach/Vacation Family product out.
- No ad copy should add free-shipping, delivery-speed, stock, inventory, review, promo, bestseller, or urgency claims unless fresh market-specific proof is gathered and approved.
- No live-spend-readiness is implied; Merchant/Pinterest/tracking/economics, owner approval, and just-in-time Ads/storefront readbacks still apply.

## Artifacts

- `validate_held_csv_creative_urls.py`
- `creative_url_copy_qa_summary.json`
- `CREATIVE_URL_COPY_QA_REPORT.md`

## Worker D Result

`PASS_LOCAL_ONLY_APPROVAL_GATED`: the held 1,496-row CSV passes creative, unsupported-claim, final URL country-parameter, and stale blocked-product exclusion checks for a future owner-approved paused Search build. It is not cleared for campaign preview/import, campaign build, enablement, or live spend by this lane.
