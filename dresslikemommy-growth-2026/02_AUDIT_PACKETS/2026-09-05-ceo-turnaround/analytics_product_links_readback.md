# GA4 product-link access route readback

Status: LIVE_VERIFIED readback; operating Ads access not established; no Merchant link exists in this property. Captured 2026-09-05, approximately 23:27–23:30 UTC. Confidence: high for the displayed states; cause of the access mismatch remains UNKNOWN.

## Scope and method

Read only in Chrome profile `test`, assigned tab `475224120`. Verified Analytics account `88409806`, property `330266838`, displayed name `dresslikemommy.com - GA4`. Inspected Admin → Product links. The parent explicitly clarified authority to select only the already documented current Google identity in the existing account chooser. No other identity, credentials, recovery, MFA, permission, configuration, linking, unlinking, or billing action occurred. No other tab, viewport, zoom, or browser-wide setting was changed.

## Google Ads

Source: [GA4 Google Ads links](https://analytics.google.com/analytics/web/#/a88409806p330266838/admin/integrations/google-ads), including its existing link-detail panel.

| Field | Fresh displayed value |
|---|---|
| Completed links | 1 |
| Approval needed / Request sent / Cancelled | 0 / 0 / 0 |
| Account name | dresslikemommy.com |
| Customer ID | 399-097-6848 |
| Account type | Account |
| Personalized advertising | Enabled |
| Date linked | Sep 1, 2022, 10:57:44 PM |
| Last modified date | Sep 1, 2022, 10:57:44 PM |
| Linked / modified by | Same documented Google identity; email omitted from artifact |
| UI-provided destination | `https://ads.google.com/aw/overview?ocid=220823493` |

The link timestamps' timezone was not shown, so they are not converted to UTC. The detail panel was opened for inspection and closed without changing a control or saving.

**Destination test:** navigated the assigned tab to the exact visible destination. It opened Google Ads' account chooser. Initially stopped there; after the parent's clarified authority, resumed the same destination test and selected only the already documented identity. The resulting fully loaded account was **Dress Like Mommy Manager, 700-107-9966**, with destination `ocid=8241192953`. The operating customer `399-097-6848` was not reached. Authentication callback URLs and user/session query values are deliberately excluded.

This demonstrates that the retained GA4 link identifies the operating Ads customer but did not provide working access to it through the tested route. It does not prove whether the underlying issue is a role, hierarchy, account state, or another cause. The manager's zero metrics are not evidence that the operating account has zero activity.

## Merchant Center

Source: [GA4 Merchant Center links](https://analytics.google.com/analytics/web/#/a88409806p330266838/admin/integrations/merchant-center).

After loading completed, the table displayed **0 of 0** and **“No links yet. Click \"Link\" to create one.”** There was no account ID, account name, link date, or account destination. Consequently no Merchant destination could be tested through this surface. No link was created. This absence applies to this GA4 property; it does not establish absence of a Merchant account or a connection elsewhere.

## Decision and end state

The Analytics route does not currently resolve the operating-account access problem. Add these exact observations to the parent's prepared support request, especially the mismatch between the existing Ads link and the manager reached by its own destination. Do not unlink/relink anything as a speculative fix. Root cause remains UNKNOWN; account recovery/support stays with the parent.

The assigned tab was restored to GA4 Merchant Center links and read back again: correct property, no links, 0 of 0. Browser checks above ran; no external mutation was made. Local validation: scoped whitespace/diff check. Next owner action: continue the prepared support request with this evidence, because the suggested Analytics route is now tested.
