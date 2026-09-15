Confidence: H. The live mismatch is explained by the same defect in MAIN and the reviewed candidate. No theme, product, Git, canonical or browser state was changed by this diagnosis.

Root’s 00:48:48 UTC readback binds the complete path: Cardigan pressed, Mother fit `data-fit-garment-key=""`, native Type still Dress, native Size Child 2 Years, empty variant ID, and the expanded Mother table displaying Dress measurements. The served module matches the previously checked MAIN source. Product tables are present; this is not evidence that product measurements should be rewritten.

**Cause and lineage** — references below are candidate/local module lines; `DIAGNOSIS.json` records corresponding MAIN lines and hashes.

1. `getGarmentKeys` at **1157** has no Cardigan recognition. `getMeasurementGarmentKey` at **2649** therefore returns an empty key even when the instance Type is Cardigan. `renderCard` writes that key into the fit trigger at **3269–3302**.
2. `getFitGroupFromProductTables` at **5529–5530** immediately rejects an empty garment key. `renderInlineFitPanel` at **5715–5720** then falls back to `getFitModalActiveGroup`, whose groups were built from the legacy guide’s selected table.
3. `getSelectedGuideTypeValue` at **3974** reads native variant controls. `getSizeGuideTable` at **4430** and `renderGuide` at **5944** therefore retain Dress. The builder’s Type click at **3471–3487** changes `inst.axisSelections` and rebuilds the card; it does not update those native controls. This separation is appropriate for multiple family members; forcing every card into one native selection is the wrong repair.
4. The compact tooltip’s apparent success is accidental. The unrecognized Cardigan chart receives an empty garment key. `addSizeMeasurementEntry` at **2213–2215** lets that untyped entry replace the generic role/size lookup; `findMeasurementsForOption` at **2323–2324** accepts it. This does not prove robust garment selection.

The smallest demonstrated correction is explicit Cardigan recognition in the shared `getGarmentKeys` classifier. An in-memory addition makes the existing per-instance trigger and direct-table resolver choose Cardigan for both Mother and Girl in both source versions. No native control synchronization is needed.

Also derive the displayed card helper from the selected instance Type. `buildRoleGroups` fixes `group.helper` from the first variant at **1581–1587**, while `renderCard` prints it unchanged at **3288–3289**, explaining “Mother Dress” beside selected Cardigan. Preserve the underlying group identity and variant data.

The packet harness passes **24 synthetic routing/lookup cases**: 12 unchanged-source diagnosis cases and 12 in-memory proposal cases. All **41 extracted functions** are byte-identical between MAIN and candidate. It uses invented numeric markers and modeled parsing/role/display dependencies. Actual browser acceptance of a repair is **NOT RUN**; the root browser evidence reproduces the defect. The harness does not certify browser rendering, chart parsing or unit conversion.

Before release, test Dress → Cardigan → Dress for Mother/Girl, with and without a selected size, metric/imperial, reopen/unit changes, independent family cards, and reversed table order. Check header/row provenance, selected-row highlight, displayed garment label, English/French desktop/mobile, and unchanged variant/cart state. Missing, ambiguous or unmatched garment sources must show no misleading chart; current helpers allow empty garment/context fallbacks, so this negative case is a required gate beyond the narrow classifier proof.

Next: prepare and independently review this separate one-module repair, retaining the existing publication boundary. Continue from `DIAGNOSIS.json`; do not replay product-source corrections or edit frozen FAQ evidence.
