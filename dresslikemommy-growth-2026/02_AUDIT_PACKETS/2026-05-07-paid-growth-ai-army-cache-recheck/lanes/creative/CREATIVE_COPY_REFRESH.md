# Creative Copy Refresh

Date: 2026-05-07 EDT / 2026-05-08 UTC

Lane: creative / RSA / copy packs.

Scope: local copy only. No Google Ads upload, campaign import, campaign edit, Pinterest draft, Pinterest campaign, product group, budget, bid, status, conversion-goal, feed, Merchant, Shopify Admin, product-data, theme, pixel, or spend change was made.

## Decision

`CREATIVE_COPY_REFRESH_LOCAL_READY_NO_UPLOAD_NO_DRAFTS`

This refresh tightens the prior creative packet for the current cache-recheck sprint. It keeps the copy usable for paused US and English-first Search infrastructure, keeps Pinterest concepts as draft-only ideas, and parks localized-market copy until storefront policy/page, route/currency, checkout, catalog, and measurement gates are clean.

## Evidence And Constraints Read

- Current lane board says Creative / RSA / copy must produce local copy only and avoid physical-inventory or shipping promises.
- US nonbrand Search rebuild already exists paused as `DLM_US_SEARCH_NONBRAND_EXACT_PHRASE_PAUSED_20260506`, campaign `23827590655`, with 12 paused ad groups, exact/phrase keywords, Manual CPC, and `$0.15` CPC posture.
- Existing international Search packet is local-only and paused-only: 17 non-US campaigns, 204 ad groups, 612 exact/phrase keywords, 204 paused RSAs, and no CPC above `$0.15`; it has not been imported.
- Latest Ads import gate says any paused import/create action still needs the exact owner approval phrase and just-in-time readbacks.
- Pinterest Event Quality still reads `Fair`; EN Shopify source completed ingestion, but exact item-level paid candidate proof is stale and Pinterest draft creation remains blocked.
- Localized policy/page public copy was only partially clean after the latest translation write. Stale public URLs remain a blocker for ES/IT/PT paid expansion.
- Dress Like Mommy is a dropshipping business with no physical store and no owned physical inventory. Copy must not imply a warehouse, local inventory, stocked inventory, guaranteed on-hand stock, pickup, or retail location.
- Return shipping remains customer-paid. Outbound checkout delivery rates must not be described as returns.

## Files In This Lane

- `CREATIVE_COPY_REFRESH.md`
- `google_search_rsa_refresh.csv`
- `pinterest_copy_concepts.csv`
- `localized_market_copy_notes.csv`

## Google Search RSA Posture

Use `google_search_rsa_refresh.csv` as a local proposal for RSA refreshes. It is not an upload file and does not authorize any live Ads edit.

The pack covers:

- Mommy & Me Dresses
- Family Matching
- Vacation Family
- Matching Pajamas
- Matching Swimwear
- Daddy & Me
- Brand Search fallback

Recommended pinning, if the parent later approves a live copy edit:

- Pin `pin_h1` to Headline 1 only when ad-group intent must stay fixed.
- Pin `pin_h2` to Headline 2 for `Dress Like Mommy` only when brand clarity is needed.
- Use `Official Store` as an optional Headline 3 pin only after parent readback confirms it is still acceptable for the target campaign.
- Leave the remaining headlines/descriptions unpinned where possible so Google can assemble stronger combinations.

Maternity note: the current US and international nonbrand Search structures explicitly carry `maternity` as a campaign negative. Do not add maternity Search copy to these campaigns unless the parent creates a separate maternity lane, removes that negative with approval, and verifies the `/collections/maternity` landing path and economics.

## Pinterest Copy Posture

Use `pinterest_copy_concepts.csv` as concept copy only. No Pinterest drafts should be created from it until:

- Event Quality is rechecked after the official app pixel fix and the parent accepts the result.
- Exact US candidate item-level proof is refreshed.
- Product group or item scope is explicit.
- Owner gives action-time approval for paused drafts.
- Drafts remain paused with no live spend.

Avoid visible Pinterest product-group names such as `Top Sellers`, `Best Deals`, `New Arrivals`, or `Back In Stock` in customer-facing copy unless a fresh storefront/catalog proof backs the exact claim. The concepts below intentionally use neutral family-photo, trip, swim, pajama, and coordinated-look angles instead.

## Localized Market Notes

Use `localized_market_copy_notes.csv` as the translation gate. The short version:

- `US`: local copy can support the existing paused nonbrand campaign, but any live RSA edit still needs approval and readback.
- `GB`, `CA`, `AU`: English-first paused infrastructure is the only currently safe international posture; no live spend.
- `CH`, `DK`: promising but QA-sensitive; English-first only after landing, checkout, currency, duties, and shipping clarity pass.
- `DE`, `NL`, `SE`, `FR`, `BE`, `ES`, `IT`: local-language copy should wait for localized route/policy/page/checkout QA. ES/IT still have specific stale public-copy risk in the latest continuity state.
- `PL`, `CZ`, `RO`, `GR`, `PT`: lower-CPC discovery can be valuable, but translated copy and spend stay blocked until page quality, checkout, and catalog gates clear. PT still has stale Shipping Info risk.
- Arabic, Hebrew, Japanese, Korean, and other mixed-language markets remain hold-only until full localization QA.

## Claims Avoided

Do not add any of these to Google, Pinterest, assets, sitelinks, descriptions, policy-facing copy, or reporting unless fresh proof exists and the parent approves the exact use:

- Fast shipping, free shipping, express shipping, guaranteed delivery, delivery-date, or processing-speed promises.
- Retail store, showroom, pickup, warehouse, stocked inventory, local inventory, owned inventory, or guaranteed availability claims.
- Sale, discount, markdown, promo code, limited-time, Best Deals, or price-drop claims.
- Reviews, star ratings, top-rated, customer counts, social proof, viral, trending, most popular, or bestseller claims.
- Weekly drops, new arrivals, 200+ styles, broad catalog-size claims, or back-in-stock claims.
- Fabric/quality claims such as premium, luxury, quality fabrics, soft cotton, or durable unless product-level evidence supports the exact product/ad.
- Return-shipping claims or any wording that treats outbound delivery rates as returns.

## Approval Gate Before Any Use

Before any Google Search upload or paused campaign import:

- Fresh exact owner approval must cover the action.
- Parent must run just-in-time readbacks.
- Campaigns, ad groups, keywords, and ads must remain paused where the approval says paused.
- Search network only; no Display expansion, no PMax, no AI Max, no broad match.
- Exact/phrase keywords only.
- Location targeting must be one country per campaign with presence-only location option.
- Manual CPC or approved low-CPC posture must remain at or below the approved cap.
- Conversion goals must not be changed.
- Final URLs must return clean pages in the intended language/posture.

Before any Pinterest draft:

- Fresh Event Quality, event receipt, catalog, product group, and item proof must be read back.
- Owner must approve paused draft creation.
- No campaign publish, enablement, spend, budget, bid, or audience expansion without separate approval.

## Verification Summary

Local validation completed in this lane:

- CSV row counts and required columns parsed.
- Google RSA headlines are 30 characters or less.
- Google RSA descriptions are 90 characters or less.
- Forbidden customer-facing claim scan passed for the generated lane files.
- `git diff --check` passed for the creative lane.

## Residual Risk

This is copy strategy and local creative material only. It does not prove ad policy approval, landing-page availability, Pinterest item eligibility, localized page quality, checkout clarity, or conversion economics. Those gates remain with the parent and adjacent lanes.
