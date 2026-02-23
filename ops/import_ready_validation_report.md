# Import-Ready CSV Validation Report

Input file: `products_export_1 2_IMPORT_READY.csv`
Total rows: `14010`
Target handles: `588`

## Summary

- Errors: `0`
- Warnings: `2`

## Findings

- [WARN] `malformed_gtin`: Found 44 rows with malformed GTIN/barcode format
  Samples: row 3546 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-father-M), row 3547 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-father-L), row 3548 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-father-XL), row 3549 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-father-2XL), row 3550 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-father-3XL), row 3551 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-mother-S), row 3552 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-mother-M), row 3553 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-mother-L), row 3554 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-mother-XL), row 3555 (family-matching-set-cute-and-stylish-outfits-for-mothers-fathers-and-children:white-mother-2XL)
- [WARN] `missing_mpn_for_barcode_less`: Found 1886 rows missing MPN for barcode-less variants
  Samples: row 28 (family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style), row 29 (family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style), row 30 (family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style), row 31 (family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style), row 46 (family-matching-oversized-heart-patch-sweaters-trendy-streetwear-style), row 147 (family-matching-christmas-pajamas-merry-christmas-gnome-fair-isle-pajama-set-for-kids-and-adults), row 153 (family-matching-christmas-pajamas-merry-christmas-gnome-fair-isle-pajama-set-for-kids-and-adults), row 154 (family-matching-christmas-pajamas-merry-christmas-gnome-fair-isle-pajama-set-for-kids-and-adults), row 160 (family-matching-christmas-pajamas-merry-christmas-gnome-fair-isle-pajama-set-for-kids-and-adults), row 161 (family-matching-christmas-pajamas-merry-christmas-gnome-fair-isle-pajama-set-for-kids-and-adults)
