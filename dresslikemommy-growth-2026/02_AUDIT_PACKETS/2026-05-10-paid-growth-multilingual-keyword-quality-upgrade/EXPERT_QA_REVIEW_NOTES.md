# Expert QA Review Notes

Anchor: `AGENT_CONTINUITY_ANCHOR: 2026-05-10-paid-growth-keyword-quality-expert-hardening`

This is a local-only expert hardening layer on top of the first keyword-quality packet.

## What Was Tightened

- Natural headline casing: native RSA headline phrases now preserve sentence/native casing instead of forced title case.
- Negative-keyword quality: added `google_ads_native_negative_keyword_review_plan.csv` with localized review-only exclusions for DIY, pattern, used, wholesale, costume, PDF, marketplace, and supplier intent.
- Pinterest quality framing: Pinterest rows remain catalog/copy/product-group terms only, because catalog sales shopping ads do not need Google-style keyword targeting.
- Launch discipline: all native Google Ads and Pinterest rows remain `REVIEW_ONLY_NOT_UPLOAD`.

## Expert Bar Before Platform Use

1. Native reviewer approves or rewrites every locale row.
2. Landing-language QA confirms the ad language matches the country-qualified storefront path.
3. Measurement proves non-US purchase currency/value before non-US live spend.
4. Google Ads preview/readback confirms paused state, language, location, networks, bids, budgets, final URLs, and no duplicate campaign.
5. Pinterest source/catalog/product-group readbacks exist before any non-US Pinterest account action.

## Known Intentional Holds

- `pt-PT`: held until pt-PT vs pt-BR storefront behavior is resolved or accepted.
- `da-DK`: held for Danish native review.
- `fr-BE` / `nl-BE`: held until Belgium language split and route proof.
- `CH`: held until German/French/Italian/English split decision.
- US `Vacation Family`: held until the beach/Christmas metadata blocker is solved or explicitly excluded.
