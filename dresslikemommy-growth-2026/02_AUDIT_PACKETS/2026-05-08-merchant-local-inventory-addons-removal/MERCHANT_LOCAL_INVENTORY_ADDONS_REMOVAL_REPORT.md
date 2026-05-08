# Merchant Local Inventory Add-ons Removal Report

Date: 2026-05-08 02:06 EDT
Account: Dresslikemommy / Merchant Center `124884876`

## Result

Fixed the `Missing local inventory data` prioritized Merchant Center issue by removing the physical-store-only `Local inventory ads` add-on.

This was the correct dropshipping fix. No local inventory feed, store pickup claim, physical store claim, Shopify inventory edit, product data edit, feed label edit, campaign edit, or budget/bid/status change was made.

## Why This Was Happening

Merchant Center showed the issue on the Local inventory/physical-store surface:

- Before fix: `Missing local inventory data`
- Detail text: `Missing inventory data for products in your physical stores`
- Merchant's own issue panel stated: `If you don't have a physical store, remove Free local listings and Local inventory ads add-ons from your Merchant Center account`

Google's Help Center also says this issue can happen when local inventory ads/free local listings are opted in for products that are not actually available in physical stores, and local inventory requires store-level attributes such as `store_code` and `availability`.

Sources:
- https://support.google.com/merchants/answer/14980864
- https://support.google.com/merchants/answer/14819809

## Actions Taken

1. Read back the active issue in Merchant Center diagnostics.
2. Read back Add-ons:
   - `Local inventory ads` was active under `Your add-ons`.
   - `Free local listings` was already inactive and showed as `Add Free local listings` under `Discover`.
3. Clicked `Remove Local inventory ads`.
4. Confirmed the dialog that said removal would deactivate the ability to show local inventory ads.
5. Read back Add-ons after removal:
   - `Local inventory ads` now shows under `Discover` as `Add Local inventory ads`.
   - `Free local listings` still shows under `Discover` as `Add Free local listings`.
   - Neither local add-on appears under `Your add-ons`.
6. Read back diagnostics after removal:
   - `Great, all your prioritized fixes are resolved`

## Evidence Files

- `merchant_main_snapshot.md`: before-fix diagnostics showed `Missing local inventory data`.
- `merchant_viewfix_snapshot.md`: Merchant issue panel stated the no-physical-store fix.
- `merchant_active_addons_snapshot.md`: before-fix active add-ons showed `Remove Local inventory ads`.
- `merchant_remove_lia_dialog_snapshot.md`: confirmation dialog.
- `merchant_addons_after_remove_discover_snapshot.md`: after-fix Discover page showed `Add Local inventory ads` and `Add Free local listings`.
- `merchant_active_addons_after_remove_snapshot.md`: after-fix Your add-ons no longer listed local inventory add-ons.
- `merchant_diagnostics_after_lia_remove_snapshot.md`: after-fix diagnostics showed all prioritized fixes resolved.

## Residual Risk

Merchant Center UI can keep stale issue counts around while backend diagnostics refresh. The immediate prioritized diagnostics readback cleared, but if another cached screen still shows the old issue, recheck after the next Merchant refresh window rather than creating local inventory data.

## Next Best Action

Monitor Merchant Center diagnostics later today. If the issue reappears, check whether a data source still has a physical-store marketing method enabled, but do not upload local inventory or make store-availability claims for this dropshipping business.
