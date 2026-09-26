# Approval packet — footer menu item "Contact US" → "Contact us" (NOT EXECUTED)

Status: PREPARED, awaiting owner approval. Lane L6 made no Admin write.

## Target (read-only Admin GraphQL readback, 2026-09-26, `footer_menus_readback_2026-09-26.jsonl`)

| Field | Value |
|---|---|
| Menu | `gid://shopify/Menu/184582996065`, handle `footer-menu-3`, title `Footer menu 3` |
| Item | `gid://shopify/MenuItem/429413761121` |
| Current title | `Contact US` |
| Proposed title | `Contact us` (sentence case, matches "About us", "Help & support") |
| Type / resource | `PAGE` → `gid://shopify/Page/161932805` (`/pages/contact-us`) |
| Other items in menu | none (menu has exactly 1 item) |

Why: menu data, not theme text, so the theme cannot fix the capitalization. Only the English source changes; the German storefront already shows "Kontaktieren Sie uns" from Translate & Adapt.

## Before-state check (run immediately before applying; abort if it differs)

```graphql
query { menu(id: "gid://shopify/Menu/184582996065") { id handle title items { id title type url resourceId items { id } } } }
```
Expect exactly one item: `429413761121`, title `Contact US`, type `PAGE`, resourceId `gid://shopify/Page/161932805`, no children.

## Exact mutation (`menuUpdate` replaces the whole item list, so the full list is resent)

```graphql
mutation {
  menuUpdate(
    id: "gid://shopify/Menu/184582996065"
    title: "Footer menu 3"
    handle: "footer-menu-3"
    items: [
      { id: "gid://shopify/MenuItem/429413761121", title: "Contact us", type: PAGE,
        resourceId: "gid://shopify/Page/161932805", url: "/pages/contact-us", items: [] }
    ]
  ) {
    menu { id handle items { id title url } }
    userErrors { field message }
  }
}
```
Schema-validated 2026-09-26 against the Admin API (Shopify validator: VALID). Requires `write_online_store_navigation`. Equivalent manual path: Admin → Content → Menus → Footer menu 3 → "Contact US" → rename → Save.

## After-state verification

1. Re-run the before-state query; expect title `Contact us`, the same item id, and `userErrors: []`.
2. Storefront: `https://www.dresslikemommy.com/` footer shows "Contact us". `/de`, `/fr`, `/es` still show their translated labels. Check Translate & Adapt: the item's translations may be flagged "outdated" because the source changed. Re-confirm them there if needed.

## Rollback

Same mutation with `title: "Contact US"`, then run the same readback.

## Risk

Low. It is cosmetic, one item, and reversible. The only side effect is the possible "outdated" flag on that item's existing translations.
