Confidence: H for the returned shipping configuration; checkout acceptance remains untested.

The **19:13:01–19:13:02 UTC, September 11** structured Shopify read found country-level rate configuration for all 65 active countries. No shipping configuration repair is justified by this evidence. The [65-country table](country_shipping_coverage.csv) separates configured coverage from buyer acceptance and preserves the returned province codes.

| Configuration group | Active countries | Configured rates in USD |
| --- | ---: | --- |
| Countries Epacket, explicit country mapping | 7: AU, CA, FR, GB, NO, RU, US | Free Standard: 0, no conditions; Priority: 12.99, inclusive 0–5 lb |
| Rest of world, wildcard mapping | 58, including Romania and Netherlands | Same rates and conditions |

All 65 countries also appear in `shop.shipsToCountries`. The sole General profile `10664050785`, version 4, has one location group, two zones and four active static rate definitions. Every pagination connection is complete. No carrier-calculated provider or order-price minimum was returned. The priority weight limit does not itself leave heavier parcels without a configured rate: standard shipping has no returned conditions.

All **98 Together Heart variants** explicitly link to this profile. That sample does not establish assignment for every advertised product. The profile's `productVariantsCount` is **500, AT_LEAST**, not an exact catalog count. Two origin locations are technical configuration; no location addresses or inventory ownership were inspected.

The common zone, country, province, rate and condition fields match the [September 9 readback](../../../2026-09-09-merchant-expert-audit/market_inventory.json). Province codes remain filters, not proof that every province or address works. The `shipsToCountries` count of 237 and `zoneCountryCount` of 244 have different meanings and are not checkout acceptance counts.

Romania's configured market currency is RON; the Netherlands' is EUR. Actual converted shipping prices, currency rounding, address handling, payment acceptance, supplier serviceability and checkout completion were **NOT RUN**. Blank rate descriptions and the queried schema do not establish whether native delivery estimates exist. Merchant shipping import and Google targeting remain separate, unverified facets. No sales, ROAS or profit conclusion follows from this configuration.

The [original response](provider_response.json), [capture and validation provenance](capture_metadata.json), [normalized evidence](shipping_coverage.json) and [rate table](rates.csv) are retained. `python3 normalize_shipping.py` checks identity, complete pagination, country mapping, conditions, the prior-source comparison, CSV round-trip and unchanged input hashes entirely offline. [Validation](VALIDATION.json) covers data integrity, not buyer acceptance.

Next action: continue the existing RO/NL localized buyer-route repair and measurement investigation. It addresses observed defects; changing these shipping rates would currently be speculative. Parent owns integration and any future checkout acceptance scope.

Continuation: Integrate this packet into the existing all-markets goal while preserving the distinction between shipping configuration and actual checkout acceptance.
