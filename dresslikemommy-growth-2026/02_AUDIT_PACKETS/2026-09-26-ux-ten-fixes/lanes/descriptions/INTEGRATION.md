# Lane D — theme patches for the parent (not applied)

Lane D writes no theme files. The parent applies these only after checking claims: `snippets/product-internal-links.liquid` is rendered from `sections/main-product.liquid:1175` but isn't named in the L5 claim list, so confirm with the peer before editing.

## 1. Remove the hardcoded "latest 19 arrivals" count (hardcoded_count finding)

File `snippets/product-internal-links.liquid`, line 72. It is inside the `internal_link_locale == 'en'` branch, so this English-only text needs no new translations.

```diff
-        <p>Looking for the newest prints first? <a href="{{ new_pajama_drop_collection.url }}">Shop the New Pajama Drop</a> with the latest 19 arrivals in one edit.</p>
+        <p>Looking for more prints? <a href="{{ new_pajama_drop_collection.url }}">Shop the New Pajama Drop</a> for more matching pajama styles in one place.</p>
```

Why the "newest" wording also goes: `new-pajama-drop` is a MANUAL list of 19 April 2026 pajamas, and none of the 7 September pajamas are in it (see `SORT_ORDER_PACKET.md` §4). If the owner refreshes its membership, "newest" can come back, but still without a count. A count could be written as `{{ new_pajama_drop_collection.products_count }}`, but that counts products published to the Online Store and changes whenever a product is archived. No count is safer.

Verify: `grep -n "latest 19" snippets/product-internal-links.liquid` returns nothing. On a live English pajama PDP (e.g. `/products/beanie-ghost-family-matching-pajamas`), the paragraph renders with no number.

## 2. Optional: sorted "Shop" link to `/collections/all` (SORT_ORDER_PACKET §2 Option A)

File `snippets/header-mega-menu.liquid`, line 98 (unclaimed as of 2026-09-26):

```diff
-          assign nav_link_url = routes.all_products_collection_url
+          assign nav_link_url = routes.all_products_collection_url | append: '?sort_by=created-descending'
```

The canonical stays `/collections/all` (verified live with `?sort_by=created-descending`). Rollback: revert the line.
