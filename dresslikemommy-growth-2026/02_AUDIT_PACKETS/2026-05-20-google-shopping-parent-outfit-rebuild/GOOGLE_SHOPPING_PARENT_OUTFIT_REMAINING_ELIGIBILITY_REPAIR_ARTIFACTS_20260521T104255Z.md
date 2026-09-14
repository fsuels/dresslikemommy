# Google Shopping Parent-Outfit Remaining Eligibility Repair Artifacts

Generated: `20260521T104255Z`

Mode: local artifact build only. No external write occurred.

## Current Scope

- Approved source spec rows: `4531`
- Ads-visible non-ready rows: `68`
- Ads-visible blank-label repair rows: `68`
- Ads-absent presence repair rows: `71`
- Out-of-stock holdout rows: `20`
- Strict spec after only out-of-stock holdout: `4511`

## Row Split

- Blank-label rows by parent: `{'6718948147297': 40, '6719764463713': 10, '6719792873569': 10, '7535944368225': 6, '7227254276193': 2}`
- Missing rows by parent: `{'7562834215009': 35, '6718945034337': 20, '6719774720097': 10, '7227254276193': 6}`
- Out-of-stock rows by parent: `{'7230645239905': 15, '7537367679073': 3, '7537367384161': 1, '7546613530721': 1}`

## Files

- Blank-label TSV overlay: `google_shopping_parent_outfit_blank_label_overlay_20260521T104255Z.tsv`
- Blank-label CSV evidence: `google_shopping_parent_outfit_blank_label_repair_scope_20260521T104255Z.csv`
- Ads-absent presence CSV evidence: `google_shopping_parent_outfit_ads_absent_presence_repair_scope_20260521T104255Z.csv`
- Out-of-stock holdout CSV: `google_shopping_parent_outfit_out_of_stock_holdout_scope_20260521T104255Z.csv`
- Strict spec excluding only out-of-stock rows: `merchant_label_update_spec_excluding_oos_holdout_20260521T104255Z.csv`
- JSON summary: `google_shopping_parent_outfit_remaining_eligibility_repair_artifacts_20260521T104255Z.json`

## Guardrails

- All Shopping campaigns remain paused.
- No activation discussion is allowed from this artifact.
- The out-of-stock holdout does not change Shopify inventory.
- The blank-label TSV contains only current Ads-visible blank-label rows.
- The Ads-absent file is evidence for the narrow presence repair lane; it is not a broad sync authorization.
