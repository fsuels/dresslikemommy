# Shipping SLA Playbook

This repo now centralizes every delivery promise in Theme Settings → **Shipping promise**. Use this guide to keep storefront content, policy pages, and experiments aligned.

## 1. Update the master settings
- `processing`: **shipping_processing_days_min/max**
- `default transit`: **shipping_transit_days_min/max**
- **shipping_promises**: one ISO-2 code per line, `US:7-10`. Leave a blank line to remove an override.
- Optional:
  - `shipping_holiday_cutoff_label/date` (YYYY-MM-DD) to show “Order by …” messaging when still in the future.
  - Toggle `shipping_delay_banner_enabled` + `shipping_delay_banner_message` for temporary disruptions.

Every change is injected into `snippets/shipping-promise-data.liquid` and read by `assets/shipping-promises.js`, so PDPs, carts, announcements, etc. update automatically.

## 2. Pages/sections wired to the SLA
| Surface | File | Notes |
| --- | --- | --- |
| Announcement fallback | `sections/announcement-bar.liquid` | Uses `[data-shipping-summary]`. |
| PDP hero + accordions | `sections/main-product.liquid` | Renders `shipping-estimate-inline` + destination list. |
| Cart drawer / cart footer / quick-order list / cart notification | `snippets/cart-drawer.liquid`, `sections/main-cart-footer.liquid`, `snippets/quick-order-list.liquid`, `snippets/cart-notification.liquid` | All call the shared snippet. |
| Delay banner | `snippets/shipping-delay-banner.liquid` | Rendered globally from `layout/theme.liquid`. |
| Policy / FAQ pages | `sections/shipping-faq.liquid`, templates `page.shipping.json` + `page.faq.json`. Assign these templates in admin to append the SLA below CMS-managed copy. |

## 3. Editing Shopify’s policy content
The Shopify admin’s *Settings → Policies → Shipping policy* page still controls the legal copy that appears in checkout + emails. After updating the theme settings, copy/paste the same numbers into that admin field so there are no contradictions.

Suggested boilerplate (replace the numbers with whatever you set in Theme Settings):
```
Processing: 2–3 business days.
Transit windows:
- US: 7–10 business days
- CA: 9–13 business days
- GB: 8–12 business days
- AU: 10–15 business days
- DE: 9–14 business days
```

## 4. QA checklist after edits
1. Preview the storefront with localization set to each key market (US/CA/GB/AU/DE) and confirm the estimator says “Delivers to XX by …”.
2. Trigger the cart drawer + cart notification + quick order table to ensure they show the same copy.
3. Load the Shipping Policy / FAQ pages assigned to the new templates and confirm the Shipping FAQ section appears.
4. If a holiday cutoff is active, verify `[data-shipping-holiday-note]` shows the correct label and disappears once the cutoff date passes.
