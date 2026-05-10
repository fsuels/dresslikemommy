# Claim-Safe Creative Refresh

Date: 2026-05-08
Lane: Worker 4 creative-copy controls
Decision: `LOCAL_READY_NO_EXTERNAL_WRITES`

## Scope

Local-only claim-safe RSA and Pinterest snippets for the held non-US Search packet after `Vacation Family` is excluded.

No Google Ads, Pinterest, Merchant Center, Shopify Admin, feed, catalog, campaign, ad, draft, import, preview, asset upload, budget, bid, status, product-scope, feed-label, product-group, conversion-goal, tag, CAPI, theme, checkout payment, or live-spend action was taken.

Write scope stayed inside:

`dresslikemommy-growth-2026/02_AUDIT_PACKETS/2026-05-08-paid-growth-market-readiness-safe-advance/lanes/creative-copy/`

## Current Creative Guardrails

- Exclude `Vacation Family` until `PROB-2026-05-08-BEACH-OUTFIT-SEO-TITLE-MISMATCH` is repaired in Shopify and public metadata readback passes.
- Do not imply physical store, warehouse, store pickup, local stock, stocked inventory, nearby inventory, or guaranteed on-hand stock.
- Do not use fast shipping, guaranteed delivery, review counts, ratings, bestseller, most popular, viral, trending, discounts, promotions, coupon, free gift, guaranteed fit, guaranteed availability, or no-risk returns.
- Do not call outbound shipping rates "returns"; return shipping remains customer-paid unless separately proven otherwise.
- Do not use bare `/es`, `/it`, `/ro`, or `/pt` language-only final URLs. Use country-qualified URLs only.

## Held Non-US Search Themes

The held `1496`-row candidate preserves these themes across the `17` non-US campaigns:

| Theme | Match Ad Groups |
|---|---|
| Mommy & Me Dresses | `Mommy & Me Dresses - Exact`, `Mommy & Me Dresses - Phrase` |
| Family Matching | `Family Matching - Exact`, `Family Matching - Phrase` |
| Matching Pajamas | `Matching Pajamas - Exact`, `Matching Pajamas - Phrase` |
| Matching Swimwear | `Matching Swimwear - Exact`, `Matching Swimwear - Phrase` |
| Daddy & Me | `Daddy & Me - Exact`, `Daddy & Me - Phrase` |

Excluded:

| Theme | Reason |
|---|---|
| Vacation Family | Stale Christmas SEO/social metadata on the beach/vacation product handle; keep excluded until exact owner-approved repair and public readback. |

## Google RSA Snippets

These are local snippets only, not upload instructions. Headlines are kept at or below `30` characters. Descriptions are kept at or below `90` characters.

### Mommy & Me Dresses

Headlines:

- `Mommy & Me Dresses`
- `Mother Daughter Dresses`
- `Family Photo Dresses`
- `Matching Dresses`
- `Dress Like Mommy`

Descriptions:

- `Browse mother daughter matching dresses for photos, birthdays and family days.`
- `Choose separate sizes for each person and build a coordinated look.`

### Family Matching

Headlines:

- `Matching Family Outfits`
- `Family Photo Outfits`
- `Coordinated Family Looks`
- `Mom Dad Kids Outfits`
- `Dress Like Mommy`

Descriptions:

- `Browse coordinated family outfits for photos, birthdays and special days.`
- `Pick sizes separately for moms, dads, kids and babies on the product page.`

### Matching Pajamas

Headlines:

- `Matching Family Pajamas`
- `Mommy & Me Pajamas`
- `Family Pajama Ideas`
- `Cozy Matching Looks`
- `Dress Like Mommy`

Descriptions:

- `Find matching pajama ideas for cozy mornings, holidays and family photos.`
- `Choose sizes for each person and create an easy coordinated pajama look.`

### Matching Swimwear

Headlines:

- `Matching Family Swimwear`
- `Mommy & Me Swimsuits`
- `Pool Day Family Looks`
- `Beach Swim Looks`
- `Dress Like Mommy`

Descriptions:

- `Browse coordinated swimwear ideas for beach days, pool trips and photos.`
- `Choose swim sizes for each family member and build a matching look.`

### Daddy & Me

Headlines:

- `Daddy & Me Outfits`
- `Father Son Matching`
- `Dad And Kid Outfits`
- `Family Photo Looks`
- `Dress Like Mommy`

Descriptions:

- `Browse daddy and me outfit ideas for father-child photos and family days.`
- `Choose sizes for dad and child to build a coordinated matching look.`

## Pinterest Snippets

Pinterest snippets are local planning copy only. Do not create Pinterest drafts or spend from this lane.

| Theme | Title | Description |
|---|---|---|
| Mommy & Me Dresses | `Mommy & Me Dress Ideas` | `Coordinated mother daughter dress ideas for photos, birthdays and family plans.` |
| Family Matching | `Family Photo Outfit Ideas` | `Matching outfit ideas for moms, dads, kids and planned family moments.` |
| Matching Pajamas | `Matching Family Pajamas` | `Coordinated pajama ideas for cozy mornings, holidays and family snapshots.` |
| Matching Swimwear | `Family Swimwear Ideas` | `Matching swimwear ideas for beach days, pool plans and sunny family photos.` |
| Daddy & Me | `Daddy & Me Outfit Ideas` | `Father-child matching outfit ideas for photos, trips and family days.` |

Pinterest US catalog/retargeting remains a separate approval-gated lane. Future paused US drafts should preserve the clean `342` EN-US scope and exclude the `4` unresolved variants unless fresh proof re-resolves them. Event Quality `Fair` remains a spend gate.

## Localized Copy Posture

Use local-language concepts only where country-qualified URLs and language/checkout readbacks support the market. The current safer posture:

| Market | Copy Posture |
|---|---|
| `GB`, `CA`, `AU` | English-first snippets above. |
| `ES`, `IT`, `RO`, `PT` | Local-language drafts may be prepared only against country-qualified URLs and just-in-time readbacks. |
| `CH`, `DK`, `DE`, `NL`, `SE`, `FR`, `BE`, `PL`, `CZ`, `GR` | English paused shells or QA hold until local language and checkout quality pass. |

### ES Draft Concepts

- `Vestidos mama e hija`
- `Looks familiares coordinados`
- `Pijamas familiares a juego`
- `Banos familiares a juego`
- `Looks papa e hijo`

### IT Draft Concepts

- `Abiti mamma e figlia`
- `Look coordinati famiglia`
- `Pigiami coordinati famiglia`
- `Costumi coordinati famiglia`
- `Look papa e figlio`

### RO Draft Concepts

- `Rochii mama si fiica`
- `Tinute asortate familie`
- `Pijamale asortate familie`
- `Costume de baie asortate`
- `Tinute tata si copil`

### PT Draft Concepts

- `Vestidos mae e filha`
- `Looks familiares combinando`
- `Pijamas familiares combinando`
- `Moda praia combinando`
- `Looks pai e filho`

These localized phrases are concept notes, not final upload rows. Native fluency, final URL, price/currency, checkout, catalog, and tracking readbacks are required before any live use.

## Blocked Claims

Do not use:

- `fast shipping`, `rush shipping`, `same-day shipping`, `guaranteed delivery`
- `warehouse`, `local stock`, `stocked inventory`, `store pickup`, `nearby inventory`, `on hand`
- `best seller`, `top rated`, `viral`, `trending`, `customer favorite`
- review counts, star ratings, customer-volume claims
- `sale`, `discount`, `coupon`, `limited time`, `free gift`, unverified promotion claims
- `guaranteed fit`, `guaranteed availability`, `no-risk returns`
- `free shipping` as ad copy unless target-country checkout rate and policy source are freshly proven and approved for that claim

## Next Best Action

If a future owner-approved paused non-US Google Search build happens before beach metadata repair, pair the held `1496`-row CSV with only these five safe themes. Keep `Vacation Family` out until public metadata readback proves the beach/vacation URL is clean.
