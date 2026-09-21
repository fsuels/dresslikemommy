# Canadian French landing-page corrections

The existing French ad candidate now has an exact product-to-checkout check for Navy Sprig. Two separately selected dresses reached a French Canadian checkout: mother M at CAD40 and child 4 years at CAD34, subtotal CAD74. Country stayed Canada and currency stayed CAD. Both test items were removed afterward and the cart was empty.

This is a partial buyer-path check. It did not test payment, final shipping after an address, purchase tracking, actual margin or French keyword demand. No ads, theme or product fields were changed live. The French campaign candidate remains held.

## Corrections ready for the existing storefront owners

Four of the twelve corrections already exist in the local JavaScript module referenced by the local product template. Their live result remains unverified; preserve that owner's existing wording and frozen release. The other eight are narrow correction candidates to reconcile with the existing owners. Preserve dynamic recipient, size and price values, measurement numbers, and other languages.

| Current French-route text | Proposed French text | Scope |
| --- | --- | --- |
| Choose who this piece is for | Choisissez à qui cette pièce est destinée | Already prepared locally; verify existing release |
| Choose size and options | Choisissez la taille et les options | Already prepared locally; verify existing release |
| Ready to add | Prête à être ajoutée | Already prepared locally; keep selected item and price |
| ADD THIS PIECE TO BAG | Ajouter cette pièce au panier | Already prepared locally; main and sticky buttons |
| Maman size | Taille pour maman | Accessible label |
| Fille size | Taille pour fille | Accessible label |
| Hip (Cm) | Hanches (cm) | Measurement label only |
| Taxes calculated at checkout. | Taxes calculées au moment du paiement. | Cart and drawer |
| Shipping details | Détails de livraison | Cart and drawer |
| Construisez votre ensemble correspondant | Créez votre ensemble assorti | Selector heading |
| Filles, enfants de 2 ans à enfants de 9 à 10 ans et mère S-3XL pour la robe et le cardigan. | Tailles fille de 2 ans à 9–10 ans et tailles maman du S au 2XL, pour la robe et le cardigan. | This product's French body |
| Echaque pièce est sélectionnée | Chaque pièce est sélectionnée | This product's French body typo |

The size correction is supported by the same-day complete 24-variant source and the visible selector. Mother sizes stop at 2XL. This does not certify any measurement or promise availability beyond the observed source.

## Effect on the existing ads

The French description about choosing each person's item and size separately matches the tested buying flow. The existing two exact keyword seeds and five sewing-related phrase-negative candidates remain unchanged. French demand is still unmeasured; English Canadian keyword data cannot qualify French keywords. Keep floral purchase intent such as “robes mère fille à motifs fleuris”; do not exclude “motif” on its own.

The product check does not qualify the generic collection landing page or other countries. The CAD74 subtotal is not retained revenue, an allowable acquisition cost or profit. Current shipping and returns statements on the page were observed, not independently substantiated for advertising.

## Implementation and verification

The local product template references `assets/product-desktop-ux-20260513-ruler-sync.js`; its French block already contains the four control translations. The old unsuffixed JavaScript mirror is not referenced by this local template. The referenced local module still constructs accessible size labels with the English word “size”; the local cart and drawer still hardcode the observed English tax and shipping-detail labels. The French selector heading is in `locales/fr.json`. These are local source findings, not proof of the script served by the current live theme. The discrepancy alone does not establish its cause: the existing owner still needs to reconcile the effective live asset, locale/runtime selection and publication state before choosing a fix.

The canonical parent should route this reconciled correction set through the existing theme and product-localization owners. Preserve the four prepared values and current frozen release. Before a write for the remaining eight candidates, resolve the current live source and exact key/field, capture its current value, and verify the claim and authority. Any successor change needs a separate review. Apply only the affected French values. Read them back, then check the French product selection and cart on desktop and a narrow viewport. Restore captured exact values if verification fails, taking care not to overwrite intervening edits.

Evidence and action boundaries: [qualification receipt](NAVY_CA_FR_QUALIFICATION_20260914.json). Independent verification is recorded separately in `../review/NAVY_CA_FR_QUALIFICATION_20260914_REVIEW.json`; the receipt alone does not claim that review passed.

Continue using `ops/prompts/paid-growth-ai-army-continuation-prompt.md`. The single next action for this finding is for the existing owners to reconcile the eight remaining candidates with the prepared release, then verify the affected French controls through the authorized release path. The original Google campaign's normal identity/Save handoff remains a separate unresolved dependency.
