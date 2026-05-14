# US Keyword Route Unblock Packet

Timestamp: 2026-05-14 automation run

Scope: repo-local update to `ops/marketing/keyword_universe.csv` plus public/read-only storefront source checks for replacement US routes. No Google Ads upload/apply/import/add keyword/bid/budget/status/negative action occurred. No Shopify Admin product/vendor/source edit, live theme push, Merchant, Pinterest, GA4/GTM, billing, product-scope, product-group, feed, or conversion write occurred.

## Result

Rerouted `23` US keyword-universe rows away from broken or supplier-risk routes:

- `/collections/vacation`: broken/held route.
- `/collections/matching-dresses`: supplier-source risk from automatic Shopify product JSON.
- `/collections/swimsuits`: supplier-source risk from automatic Shopify product JSON.
- `/collections/daddy-and-me`: conservative reroute away from the previously flagged seasonal-metadata route before future paid use.

Replacement destinations:

- `/collections/matching-outfits`: `15` rows.
- `/collections/mommy-and-me`: `5` rows.
- `/collections/family-swimsuits`: `3` rows.

Public US readback on the replacement routes returned `200` with `0` supplier/source-domain or URL-brand hits and `0` stale seasonal/local-inventory trust hits across both header variants. These rows are still local-only; they need active-product proof, authenticated CPC/search validation, reviewer pass, and a fresh action-queue `GREEN` row before any live Search use.

## Public Replacement Route Readback

| Route | Header variant | Status | Redirected | Supplier/url-brand hits | Stale/trust hits | Product URL count | Decision |
|---|---|---:|---|---:|---:|---:|---|
| /collections/family-swimsuits | text_html | `200` | `False` | `0` | `0` | `3` | `route_clean_for_us_local_validation` |
| /collections/family-swimsuits | star_cache_busted | `200` | `False` | `0` | `0` | `3` | `route_clean_for_us_local_validation` |
| /collections/matching-outfits | text_html | `200` | `False` | `0` | `0` | `39` | `route_clean_for_us_local_validation` |
| /collections/matching-outfits | star_cache_busted | `200` | `False` | `0` | `0` | `39` | `route_clean_for_us_local_validation` |
| /collections/mommy-and-me | text_html | `200` | `False` | `0` | `0` | `39` | `route_clean_for_us_local_validation` |
| /collections/mommy-and-me | star_cache_busted | `200` | `False` | `0` | `0` | `39` | `route_clean_for_us_local_validation` |

## Rerouted Keyword Rows

| CSV row | Keyword | Threshold | Old route | New route | New action |
|---:|---|---|---|---|---|
| 3 | `matching family vacation outfits` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 10 | `mother daughter wedding guest dresses` | GREEN | `/collections/matching-dresses` | `/collections/mommy-and-me` | `rerouted_us_from_supplier_leaking_matching_dresses_to_clean_mommy_route_product_proof_required` |
| 11 | `mommy daughter vacation dresses` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 16 | `beige mother daughter dresses` | YELLOW | `/collections/matching-dresses` | `/collections/mommy-and-me` | `rerouted_us_from_supplier_leaking_matching_dresses_to_clean_mommy_route_product_proof_required` |
| 17 | `chiffon mother daughter dresses` | YELLOW | `/collections/matching-dresses` | `/collections/mommy-and-me` | `rerouted_us_from_supplier_leaking_matching_dresses_to_clean_mommy_route_product_proof_required` |
| 22 | `matching family swimsuits` | GREEN | `/collections/swimsuits` | `/collections/family-swimsuits` | `rerouted_us_from_supplier_leaking_swimsuits_to_clean_family_swimsuits_route_product_proof_required` |
| 23 | `mommy and me swimsuits` | GREEN | `/collections/swimsuits` | `/collections/family-swimsuits` | `rerouted_us_from_supplier_leaking_swimsuits_to_clean_family_swimsuits_route_product_proof_required` |
| 24 | `mother daughter bathing suits` | GREEN | `/collections/swimsuits` | `/collections/family-swimsuits` | `rerouted_us_from_supplier_leaking_swimsuits_to_clean_family_swimsuits_route_product_proof_required` |
| 25 | `daddy and me shirts` | YELLOW | `/collections/daddy-and-me` | `/collections/matching-outfits` | `rerouted_us_from_daddy_route_to_clean_family_matching_route_product_proof_required` |
| 26 | `dad and son vacation shirts` | GREEN | `/collections/daddy-and-me` | `/collections/matching-outfits` | `rerouted_us_from_daddy_route_to_clean_family_matching_route_product_proof_required` |
| 27 | `dad son matching shirts` | YELLOW | `/collections/daddy-and-me` | `/collections/matching-outfits` | `rerouted_us_from_daddy_route_to_clean_family_matching_route_product_proof_required` |
| 28 | `family cruise outfits` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 29 | `family tropical outfits matching` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 30 | `matching family hawaiian outfits` | YELLOW | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 33 | `mother daughter matching maxi dresses` | GREEN | `/collections/matching-dresses` | `/collections/mommy-and-me` | `rerouted_us_from_supplier_leaking_matching_dresses_to_clean_mommy_route_product_proof_required` |
| 35 | `family vacation matching outfits for pictures` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 39 | `matching family outfits for beach vacation` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 41 | `mother daughter matching vacation outfits` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 44 | `matching family outfits for cruise pictures` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 45 | `family resort outfits matching` | YELLOW | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 46 | `mommy and me tropical dresses` | GREEN | `/collections/vacation` | `/collections/matching-outfits` | `rerouted_us_from_vacation_404_to_clean_family_matching_route_product_proof_required` |
| 49 | `daddy son matching beach shirts` | GREEN | `/collections/daddy-and-me` | `/collections/matching-outfits` | `rerouted_us_from_daddy_route_to_clean_family_matching_route_product_proof_required` |
| 53 | `mother daughter holiday dresses` | YELLOW | `/collections/matching-dresses` | `/collections/mommy-and-me` | `rerouted_us_from_supplier_leaking_matching_dresses_to_clean_mommy_route_product_proof_required` |

## Decision

This closes the local dirty-route gap for US keyword-universe planning. It does not make the US rows live-ready. The next US paid action remains:

1. Run authenticated Standard Shopping item-level export for campaign `23802638621` and join it to the public-clean scope.
2. For future US Search, build a small validation packet from these rerouted rows only after active-product fit and `$0.15` CPC/search feasibility are proved.
3. Keep the original dirty collection routes excluded until product/vendor source cleanup is approved and read back clean.
