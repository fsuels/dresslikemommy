# Shopify Google connection repair

Initial observations recorded September 6, 2026, 05:46 UTC. Owner: `shopify_merchant_connection_repair`; parent owns external writes and canonical integration. Current status: `LOCAL_RETAIL_SYNC_REPAIR_IMPLEMENTED_AND_VERIFIED_BY_ROOT__APP_ACCESS_UNRESOLVED`. The tables below preserve the before-state. The execution addendum supersedes the proposed action status.

The user explicitly requested a subagent to repair the Shopify–Merchant connection, then identified [Google channel settings](https://admin.shopify.com/store/dresslikemommy-com/apps/google/settings) and requested every problem there be fixed. This bounded pass used only existing Chrome test tab `475224124`, browser `2`, for store `dresslikemommy-com`. No other user tab was opened, no account was changed, and no setting was saved.

## Verified observations

| Surface | Current UI evidence | Meaning and limitation |
|---|---|---|
| Google services in Settings | Existing Google identity matches the owner-designated Chrome test identity. Merchant `124884876` and Analytics `G-N4EQNK0MMB` / property `330266838` appear connected. | The saved link points to the expected Merchant account. This does not prove usable Google app permission or successful ingestion. |
| Online feed settings | Product sync, countries/languages, shipping-information sync, search-engine product titles and descriptions all display `On`. | A simple off toggle does not explain the missing online listings. No source-level current ingestion, product approval, country coverage, or public purchasability proof was returned. |
| Measurement | Conversion measurement displays `On`; its expanded section offers event settings and Google tags. | Setting presence is not purchase-event parity or attribution proof. No measurement settings changed. |
| Local inventory | Retail-locations automatic sync displays `On`; its modal lists one fulfillment location. Business Profile separately offers `Connect`. | Physical-retail sync is mismatched with this business, which has no physical retail store. Location address and supplier details are intentionally omitted. Its actual impact on online product eligibility remains unproven. |
| Overview | Merchant Center appears `Inactive` under opportunities, with `Get started`; Google Ads appears `Error`, with “Google Ads account issue” and a link to review the account. | Conflicts with the linked Merchant shown in Settings. There are no product-status counts on this overview. This is not proof that Merchant is empty, deleted, or suspended. |
| Loading reliability | “An error occurred. Please try again later.” appeared on Overview and again on return to Settings. Notification summary changed from 3 of 3 to 0 of 3 without operator edits. | Do not treat every displayed default or a transient toast as persisted backend state. Error cause is unknown. |

Parent-supplied fresh evidence, separate from this agent's observations: root selected only the existing connected identity in the exact Merchant route and reached `merchants.google.com/noaccess` for `124884876`. The page explicitly says that Google account lacks access. No alternate account was inspected. This corroborates current app-access denial; it does not establish why access was lost or prove the denial caused every Shopify error.

## Exact action handed to parent

The open **Retail locations** modal shows **Automatic sync — On**, button **Turn off automatic sync for all locations**, **Cancel**, and disabled **Save**. The agent opened this dialog but did not press Turn Off or Save. Tab ownership was handed to root before any external mutation.

Proposed smallest correction: turn off only automatic local-retail inventory sync, inspect the resulting scope, then Save if confined to that setting. Preserve Merchant `124884876`, the existing identity, Online Store product syncing, countries/languages, shipping sync, product title/description sync, Analytics, and conversion measurement. Do not remove or alter the fulfillment location or product quantities.

Why this is supported: both [Google's local-inventory requirements](https://support.google.com/merchants/answer/13709335?hl=en) and [Shopify's local-inventory requirements](https://help.shopify.com/en/manual/online-sales-channels/marketplaces/google/shopping-on-google/local-inventory) require a physical retail location. The new request names these settings for repair. Parent must retain the independent action review, exact before-state and after-state checks. This does not authorize a new account, new permissions, billing, a broad disconnect/reconnect, or feed/product-scope changes.

Verification: reopen the modal after Save and, if necessary, a normal reload; require persisted `Off`, same Merchant/Analytics IDs, and preserved online sync controls. Read Overview separately afterward. Success is removal of this specific mismatched retail sync, not a claim of recovered online distribution. Stop if Save fails, permissions/consent appear, scope broadens, other settings change, or Off does not persist. The inverse local control would be the rollback; its exact labels must be read fresh, and it must not be used to invent physical-store inventory.

## Main remaining dependency

Restore supported app-specific access to existing Merchant `124884876` and Ads `3990976848`, then read exact online product diagnostics and source states. Root's already-authorized support request remains a separate unresolved workflow; this report does not claim it was sent. Preserve the existing account links and data while access is recovered. Do not use Get started to create a replacement Merchant or disconnect the correct stored link as a diagnostic experiment.

Historical records are leads, not current action authority: US/en age_group was solved; do not repeat broad attribute repair. US/es source `10627981690`, capacity/duplicate market rows and Canada/GB feed absence require fresh source-level readback. This pass did not inspect an active product cohort, images, titles, prices, availability, supplier-clean landing fit, or current Shopping scope, so it makes no product/feed recommendation and does not release Shopping or paid spend.

## Evidence, checks and handoff

Machine-readable observations and action boundary: `shopify_google_connection_readback.json`. Repository sources used: current marketing control and spend authority, matching Google-access problem, current coordination claim, `google_access_recovery.md`, and the latest relevant historical-access worklog anchor. Canonical updates remain parent-owned. No screenshot containing the location address or embedded authentication URL was saved.

Initial handoff next action was the narrowly scoped local-retail-sync correction. It is now completed as documented below. Continue through [the canonical paid-growth prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md) and current command layer, with root's execution receipt and latest worklog anchor.

## Parent execution outcome — September 6

Read the expanded `shopify_google_settings_repair_execution.json`: initial repair recorded **05:52:59 UTC**, receipt updated **06:00:29 UTC**. The current receipt fingerprint and both times are captured in the readback addendum. Root executed one Save after independent review. A normal settings reload and reopened Retail locations modal showed **Automatic sync Off**, unchecked sync-all-locations, and disabled Save. Merchant `124884876`, GA4 property `330266838`, and online product, country/language, shipping, title, description and conversion-measurement controls remained unchanged. No broader settings were touched. The subagent did not independently repeat these browser checks; the exact root receipt and its hash are preserved in the readback addendum.

This fixes the specific unsupported physical-retail sync. The receipt does **not** establish restored Merchant account access, online product eligibility, traffic or sales. The expanded receipt confirms Merchant Inactive after repair and a Google Ads account issue in the loaded after-state; a later brief omission of the Error text does not establish resolution. Existing Google tags were inspected without changes.

Root then encountered a native before-unload warning while inspecting Merchant setup. The documented rich browser API supports `Tab.getJsDialog()`; both `BeforeUnloadDialog` and `ConfirmDialog` have `dismiss()` to cancel. Root subsequently reported an actual `confirm` type; the subagent supplied the documented `ConfirmDialog.dismiss(): Promise<void>` signature. The subagent relayed that exact API and made no browser call, dismissal, save, account or permission action in this follow-up. **Cancellation is already verified:** the expanded root receipt records `ConfirmDialog.dismiss()` and Overview remaining visible with Merchant Inactive. No account was created, connected, disconnected or activated. The pending-navigation instruction is superseded; do not repeat that dismissal or the completed local-retail-sync mutation. Current next action: supported existing-account access recovery. Root is checking whether the current contact/CC/summary validation passes in the same already-authorized Google support request before its submission. This subagent did not inspect or act on that support form, and no submitted case is established by this report.
