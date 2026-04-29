# Paid-Eligible Row Review

Decision: `APPROVED_FOR_LOCAL_PAUSED_BUILDOUT_MANIFEST_ONLY`

No Merchant Center label upload, Google Ads campaign creation, budget change, or live enablement was performed.

## Result

- Original paid-eligible rows reviewed: `784`
- Duplicate SKU/GTIN rows demoted to fix-before-paid: `4`
- Final paid-eligible rows after review: `780`
- Unique products represented: `81`
- Products with paid variants in more than one family bucket: `8`
- Launch decision remains: `READY_FOR_PAUSED_BUILDOUT`

## Passed Gates

- All final rows are US market rows.
- All final rows have SKU, GTIN/barcode, product URL, image URL, price, cost, and max CAC.
- All final rows have Merchant Center status `Approved`, destination `Shopping ads eligible`, and issue count `0`.
- All final rows have image, price, availability, shipping, return, and PDP status `PASS`.
- No duplicate SKU, GTIN/barcode, Merchant Center item ID, or Shopify variant ID remains in the final paid subset.

## Final Paid Variant Rows By Family

- `daddy_me`: `89` variants
- `family_matching`: `103` variants
- `mommy_me`: `214` variants
- `pajamas`: `29` variants
- `swimsuits`: `345` variants

Product counts by family can overlap because some family-set products contain separate mother, father, child, and swim variants that classify into different role buckets.

## Demoted Duplicate Identifier Rows

- `shopify_US_7110368919649_41500578906209`: SKU `5207291341962-Size:128;Color:Pink orange beach pants;`, GTIN `5207291341962`, product `7110368919649`
- `shopify_US_7110368919649_41500579004513`: SKU `5207291341965-Size:164;Color:Pink orange beach pants;`, GTIN `5207291341965`, product `7110368919649`
- `shopify_US_7510791258209_43768836685921`: SKU `5207291341962-Size:128;Color:Pink orange beach pants;`, GTIN `5207291341962`, product `7510791258209`
- `shopify_US_7510791258209_43768836882529`: SKU `5207291341965-Size:164;Color:Pink orange beach pants;`, GTIN `5207291341965`, product `7510791258209`

## Paused Buildout Gate

The local manifest `11_google_ads_paused_standard_shopping_buildout_manifest_review_only.csv` is prepared for the paused Standard Shopping structure, but the external Ads build was not executed. The current Merchant Center browser evidence still shows older/blank custom label values on the final paid rows, not the new `custom_label_0=paid_eligible` and `custom_label_4=us_test_ready` scheme. Creating the external campaign with those inventory filters before an approved label upload would not reliably isolate this subset.

Approved external next step is therefore still limited to review/planning unless the owner explicitly approves either the label upload or a separate item-ID listing-group build.
