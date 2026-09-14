# Google Shopping Parent-Outfit Paused V2 Live Readback

Generated: `2026-05-20`

Mode: owner-approved paused Google Ads Shopping structure creation plus readback. No activation, spend enablement, Merchant/Shopify feed-label write, product/image write, conversion-goal write, billing write, or existing `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` edit occurred.

## Execution Summary

- Validate-only passed before the live mutate.
- Live mutate timestamp: `20260520T055931Z`.
- Readback timestamp: `20260520T060127Z`.
- Live mutate operations executed: `96`.
- Old campaign `DLM_US_STANDARD_SHOPPING_TEST_PAID_READY` read back `PAUSED` / `PAUSED`.
- New V2 campaigns read back `PAUSED` / `PAUSED`.
- Paused draft requirement values used only for draft creation: daily budget `1000000` micros per campaign and CPC bid `10000` micros.
- The first live execution report had a local after-readback counting bug after the mutate succeeded; the corrected readback report at `20260520T060127Z` passed with no additional mutate.

## Campaign Readback

| Campaign | ID | Status | Primary status | Type | Merchant ID | Feed label | Budget micros | Priority |
|---|---:|---|---|---|---:|---|---:|---:|
| `DLM_US_SHOPPING_MOMMY_ME_PARENT_OUTFIT_V2` | `23868645502` | `PAUSED` | `PAUSED` | `SHOPPING` | `124884876` | `US` | `1000000` | `1` |
| `DLM_US_SHOPPING_FAMILY_MATCHING_PARENT_OUTFIT_V2` | `23858920059` | `PAUSED` | `PAUSED` | `SHOPPING` | `124884876` | `US` | `1000000` | `1` |
| `DLM_US_SHOPPING_DADDY_ME_PARENT_OUTFIT_V2` | `23868645508` | `PAUSED` | `PAUSED` | `SHOPPING` | `124884876` | `US` | `1000000` | `1` |

## Product Group / Ad Group Readback

| Check | Result |
|---|---:|
| V2 campaigns | `3` |
| V2 paused ad groups | `12` |
| V2 paused Shopping product ads | `12` |
| V2 listing-group criteria | `60` |
| Included subgroup product units | `12` |
| Excluded catchall units | `24` |
| Bad catchall units | `0` |
| Campaign listing scopes | `3` |

Ad groups read back:

- `Mommy & Me - Dresses`
- `Mommy & Me - Pajamas`
- `Mommy & Me - Sets`
- `Mommy & Me - Sweaters & Outerwear`
- `Mommy & Me - Swimwear`
- `Mommy & Me - Tops & Shirts`
- `Family Matching - Dresses`
- `Family Matching - Sets`
- `Family Matching - Sweaters & Outerwear`
- `Family Matching - Tops & Shirts`
- `Daddy & Me - Sets`
- `Daddy & Me - Tops & Shirts`

Every V2 ad group uses this no-leakage tree shape:

1. Root subdivision.
2. Included parent-lane subdivision using `custom_label_1`.
3. Excluded `custom_label_1` catchall.
4. Included subgroup product unit using `custom_label_2`.
5. Excluded `custom_label_2` catchall.

## Parent Count / Image Gate

The local parent-outfit spec remains:

| Parent lane | Expected active/feed-mapped parent outfits |
|---|---:|
| Mommy & Me | `99` |
| Family Matching | `77` |
| Daddy & Me | `34` |

Supporting local spec counts:

- Included parent outfits: `210`.
- Included variant rows: `4531`.
- Missing `item_group_id`: `0`.
- Missing hero image: `0`.
- Included hard `404` products: `0`.
- Historically served hard `404` parents held out: `5`.
- Known archived/unpublished Daddy & Me targets held out: `2`.

Important boundary: the paused Google Ads structures now reference the parent-outfit label contract, but this execution did not write Merchant/Shopify feed labels or product images. Before any activation discussion, Merchant-side count/image readback must prove the labels and hero-image discipline are live in Merchant, with no 404/archived products eligible and no catchall leakage.

## Evidence Files

- `GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_20260520T055918Z.md`: validate-only pass.
- `GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_20260520T055931Z.md`: live mutate response, `96` operations.
- `GOOGLE_SHOPPING_PARENT_OUTFIT_PAUSED_REBUILD_EXECUTION_20260520T060127Z.md`: corrected no-mutate after-state readback, validation passed.
- `google_ads_shopping_parent_outfit_after_20260520T060127Z.json`: saved Google Ads API after-state readback.
- `google_shopping_parent_outfit_rebuild_summary.json`: local parent-outfit count/image/spec summary.
