# Apply Me — Vendor + Brand Auto-Fix Execution

Three deliverables. Total click time: ~3 minutes.

## 1. Shopify Flow workflow (one-time, then permanent)

Goal: Whenever a product is created, updated, or duplicated and its vendor is not `Dress Like Mommy`, Shopify Flow rewrites the vendor.

Steps:

1. Shopify Admin → **Apps** → **Flow**. If Flow isn't installed yet, install it (it's free; published by Shopify).
2. Top right → **Create workflow** → **Import workflow**.
3. Choose file: `auto-vendor-dress-like-mommy.flow` (in this folder).
4. The workflow opens in the editor. The triggers are `Product created`, `Product updated`, `Product duplicated`. The condition checks `product.vendor != "Dress Like Mommy"`. The action sets `vendor = "Dress Like Mommy"`.
5. Top right → **Turn on workflow**.

That's it. From now on, every new product, edit, or duplicate has its vendor auto-corrected.

If Flow import does not accept the schema:

- Click **Create workflow** → **Blank workflow**.
- Add trigger **Product updated** → next step **Condition**: `product.vendor != "Dress Like Mommy"`.
- True branch: action **Update product** → set **Vendor** to `Dress Like Mommy`.
- False branch: leave empty.
- Save, then **Add trigger** → **Product created** with the same body, then **Product duplicated** the same way (or duplicate the workflow with each trigger).

## 2. Merchant Center feed rules (one-time)

Open `MERCHANT_CENTER_FEED_RULES.md` in this folder for the exact rule names, conditions, and target values.

Three rules to add in Merchant Center account `124884876` on the **Shopify Google & YouTube** primary feed:

- **Rule A** — force `brand = "Dress Like Mommy"` on every row.
- **Rule B.1 + B.2** — split `gender` and `age_group` based on variant title (mother/father/girl/boy).
- **Rule C** — set `identifier_exists = no` on every row.

Save all as draft, then click **Apply** once.

## 3. Vendor backfill (already done by the script)

This is the one-shot fix for the 287 products that were already wrong. It was executed in the agent session and summarized in `EXECUTION_REPORT.md`.

The script is idempotent. Re-running it will simply find zero targets if everything is clean. Use it any time you want to verify "is the catalog still 100% Dress Like Mommy?".

## Verification

Run `ops/scripts/verify_vendor_compliance.py` from the agent session to confirm:

- Zero active products with `vendor != "Dress Like Mommy"`.

Latest automation read-only verification: `326` active products checked, `0` non-compliant products, verdict `PASS`, saved as `vendor_compliance_report.json`.

After Merchant Center rules are applied and the feed refetches, run a separate Merchant Center readback on sample offers to confirm:

- `brand = "Dress Like Mommy"`.
- `gender`, `age_group`, and `identifier_exists` reflect the rules in `MERCHANT_CENTER_FEED_RULES.md`.
- `item_group_id` and `image_link` remain unchanged from the feed-grouping plan.
