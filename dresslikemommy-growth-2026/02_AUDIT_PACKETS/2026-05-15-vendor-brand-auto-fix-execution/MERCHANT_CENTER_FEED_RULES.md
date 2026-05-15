# Merchant Center Feed Rules — Account `124884876`

Source feed: **Shopify Google & YouTube** (primary feed for `www.dresslikemommy.com`).
Apply each rule for every target country/language combination this feed serves (US/en, US/es, CA/en, GB/en, AU/en).

How to open the rule editor:

1. Open Merchant Center, top right confirms account **Dresslikemommy, 124884876**.
2. Left nav → **Products** → **Feeds**.
3. Click the **Shopify Google & YouTube** primary feed row.
4. Tab **Rules** (sometimes shown as **Feed rules**).
5. For each rule below, click **+ Add rule**, select the target attribute, paste the condition and the action, **Save as draft**, then **Apply** once all three are drafted.

---

## Rule A — Force brand to "Dress Like Mommy"

- **Target attribute:** `brand`
- **Rule name:** `force_brand_dress_like_mommy`
- **Condition:** *(no condition — apply to all rows)*
- **Modification:**
  - Type: **Set to**
  - Value: `Dress Like Mommy`
- **Effect:** Every offer in this feed is sent to Google with `brand = "Dress Like Mommy"` regardless of what the Shopify `vendor` field contains. Belt-and-suspenders to the Shopify Flow workflow.

---

## Rule B — Matching-set gender / age_group split

Two attributes get rewritten by this rule pair, based on the variant title (which appears in feed as `title` or `n:product_detail_attribute_value`). Implement as **two attribute rules** (one for `gender`, one for `age_group`) with the same set of conditions.

### B.1 — `gender` rewrite

- **Target attribute:** `gender`
- **Rule name:** `matching_set_gender_split`
- **Condition list (OR within each row, evaluated top-to-bottom; first match wins):**

  | If `title` contains (case-insensitive) | Set `gender` to |
  |---|---|
  | `Mother`, `Mom`, `Mommy`, `Mama`, `Women`, `Woman`, `Mujer`, `Madre` | `female` |
  | `Father`, `Dad`, `Daddy`, `Papa`, `Men`, `Man`, `Hombre`, `Padre` | `male` |
  | `Girl`, `Daughter`, `Niña`, `Hija` | `female` |
  | `Boy`, `Son`, `Niño`, `Hijo` | `male` |
  | *(no match)* | leave unchanged |

### B.2 — `age_group` rewrite

- **Target attribute:** `age_group`
- **Rule name:** `matching_set_age_group_split`
- **Condition list:**

  | If `title` contains | Set `age_group` to |
  |---|---|
  | `Mother`, `Mom`, `Mommy`, `Mama`, `Father`, `Dad`, `Daddy`, `Papa`, `Mujer`, `Hombre`, `Madre`, `Padre`, `Women`, `Men` | `adult` |
  | `Baby`, `Newborn`, `Infant`, `0-12M`, `3M`, `6M`, `9M`, `12M` | `infant` |
  | `Toddler`, `18M`, `2T`, `3T`, `4T`, `90cm`, `100cm` | `toddler` |
  | `Girl`, `Boy`, `Kid`, `Child`, `Daughter`, `Son`, `Niña`, `Niño`, `5T`, `6Y`, `7Y`, `8Y`, `9Y`, `10Y`, `11Y`, `12Y`, `13Y`, `14Y`, `110cm`, `120cm`, `130cm`, `140cm`, `150cm` | `kids` |
  | *(no match)* | leave unchanged |

`item_group_id` is **not** touched. All variants of the same Shopify product continue to share the same `item_group_id` so Google still treats them as one matching set with size/role variants underneath.

---

## Rule C — `identifier_exists = no`

- **Target attribute:** `identifier_exists`
- **Rule name:** `identifier_exists_false_private_label`
- **Condition:** *(no condition — apply to all rows)*
- **Modification:**
  - Type: **Set to**
  - Value: `no`
- **Effect:** Clears the catalog-wide "Missing GTIN" disapproval. Correct because Dress Like Mommy is a private-label brand with no GTINs.

---

## Apply order

Save as draft in this order, then click **Apply** once at the end:

1. Rule A (`brand`)
2. Rule B.1 (`gender`)
3. Rule B.2 (`age_group`)
4. Rule C (`identifier_exists`)

After clicking **Apply**, Merchant Center re-processes the feed within ~15 minutes for a full re-evaluation. Initial Diagnostics counts update on the next feed fetch (≤ 24h).

## Verification checklist (after the next fetch)

- Diagnostics → "Invalid brand" / "Generic brand" count → expect to drop to **0**.
- Diagnostics → "Missing GTIN" count → expect to drop to **0**.
- Sample a variant in **Products → All products → Diagnostics** view, confirm `brand` is `Dress Like Mommy`, `gender` is one of `female|male`, `age_group` is one of `adult|infant|toddler|kids`.
- Confirm `item_group_id` is unchanged (one per parent Shopify product).
- Confirm `image_link` is still the product's main image.
