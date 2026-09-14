# Arabic child selector repair

Status: IMPLEMENTED_LOCAL; bounded code regressions VERIFIED. External staging, independent review and rendered acceptance belong to the parent.

The observed Arabic size prefix `للأولاد` was absent from the role aliases, and canonical `KID` SKU tokens had no fallback. `buildRoleGroups` consequently skipped 49 child variants. The same failure occurs with both the previous and corrected product measurement tables.

The candidate asset matched captured MD5 `1d3544d25d247e50b862a089c9249e9a` before editing. Only three narrow changes were made: add the exact Arabic child alias; recognize bounded `KID` SKU tokens; keep that generic child fallback from replacing a role already recognized from the label. Specific gender/adult SKU precedence remains intact. Existing adult recognition required no ADT change.

Bundled Node ran `--test localized-pdp-v6/arabic-child-selector.test.mjs` (relative to this audit packet): **28 tests passed, 0 failed**. The suite evaluates the actual complete asset in jsdom and reconstructs the original source with its frozen MD5. It reproduces the original adult-only group of 49 offers/seven sizes, then verifies child 49 plus adult 49, two seven-row guides, all IDs/prices/labels/colors/availability preserved, bounded alias/SKU matching, explicit role holdouts, and identical role/guide outputs for all 20 other captured locales. All 140 source table cells remain unchanged. `node --check` passed.

Fixtures use captured API IDs/SKUs/prices/colors and exact localized table size labels. Availability is controlled to isolate classification; unavailable-variant behavior has a separate assertion. Parent must complete the comparison against its fresh browser-embedded 98-variant snapshot.

Frozen asset: 268875 bytes; MD5 `522339c5825769c499e1ad1488b8a138`; SHA-256 `e5a16e0cc2e9dca6cd5b40fce603b1cee54daa023943b1b5cd5033b401842438`.

Test SHA-256: `9179c240ec017af183076af8e98eede75f90cf6dd150a43985475cc6a3020861`.

No product, variant, price, translation, measurement, tracking, account, consent, canonical-state or external write was made. Other candidate repairs were preserved. Work is frozen for parent integration.
