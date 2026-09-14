# Google account identity evidence from both owner mailboxes

Readback: September5 EDT / September6 UTC,2026. Scope: owner-requested, read-only search for the login/access information associated with the original Google Ads and Merchant Center accounts. Stage: HANDOFF. The exact Gmail and Microsoft business-mailbox profiles were verified against the owner's requested identities. Login addresses are omitted from repo evidence; connector profiles and the owner's current message establish them.

## Finding

The strongest identity evidence supports the already-used Chrome test Gmail as historically associated with Ads399-097-6848 and Merchant124884876. The Microsoft business mailbox has correspondence about the same original Ads account dating to2018 and a later approval for manager700-107-9966. No alternate Google login or actionable account-access invitation was found in these targeted searches. Notification receipt alone does not prove ownership or current app permission. No password, code or new sign-in route was recovered or used.

## Decisive correspondence

| Mailbox | Date | Verified content | What it establishes |
|---|---|---|---|
| Chrome test Gmail | May25,2026 | Google Ads setup notice explicitly names customer399-097-6848; recipient matches the current Gmail profile | Historical association with the operating customer, beyond the manager name |
| Chrome test Gmail | May15 and June10,2026 | Merchant alert and May performance report explicitly name customer124884876; recipients match the current Gmail profile | Historical association with the original Merchant account and actual report data |
| Chrome test Gmail | June1,2026 | Announces future June15 linking of Ads399-097-6848 to Business Manager om-1794417514559008712 | Planned link only; not completion or evidence of the cause of missing access |
| Microsoft business mailbox | August21,2018 at18:35:47UTC | Sent reply to Google implementation support quotes a conversion-code session for AdWords399-097-6848 | The original Ads account existed in older business correspondence; no separate login identity or access invitation |
| Microsoft business mailbox | May18,2026 at23:23:01UTC | Google Ads API Basic Access approval concerns manager700-107-9966 and was sent to the business mailbox | Historical manager/API correspondence; not evidence of today's client linkage |

Gmail message IDs and authenticated mailbox links are in `google_mailbox_search_summary.json`. The Outlook reader retrieved the two decisive full messages because previews omitted recipients; subjects/date/account IDs identify them without storing personal names or full bodies. Re-search the exact Ads or manager ID in the verified Microsoft mailbox to recover them.

## Additional clues and rejected inferences

- September4,2026: Google's email identifies the current Gmail principal as the Google Ads user who shared a conversion tag. Its public tag ID is AW-18164235932. The message does not contain the original customer3990976848 or manager7001079966 ID, and that public tag ID was not found in the scoped project search. Its customer-account mapping is UNKNOWN; a public tag ID is not a login or proof that the original client is accessible. No tag installation or conversion change occurred.
- July22,2026: a Google passkey notice discusses sensitive actions such as adding users/linking accounts. It expressly says the change does not affect sign-in. This does not establish the cause of Merchant denial or the missing Ads client. No passkey/security setting was changed.
- August17,2026: Google's AI CMO sign-in notice lists shared profile name/picture and email. It does not establish Ads/Merchant account permissions or prove that AI CMO caused the access problem. No app access was revoked.
- Root checked recipient identity and Google DKIM/DMARC results on all7 Gmail messages read in full: all matched/passed. No action, tracking, invitation or reset link in any email was clicked.

## Coverage and limits

Root ran12 targeted Gmail searches, including `in:anywhere`, exact account IDs, official senders, access/invitation/removal subjects, a pre-May1 query, later correspondence and the new tag ID. These returned17 unique IDs, including unrelated keyword matches; all responses had no next-page token. Seven relevant full messages were read. Unrelated survey/newsletter/Workspace/search-marketing matches were excluded from login conclusions. The earlier pre-May query returned no matches; this is not proof that older mail never existed.

Independent Outlook reader `/root/outlook_google_identity_search` ran23 searches with page sizes20/30; every response returned has_more=false. Exact hyphenated Ads and manager IDs returned one message each; unhyphenated forms, Merchant124884876 and Business Manager exact ID returned none. Broad service/access/invitation/removal/welcome queries supplied no alternative identity or usable invitation. Two decisive full reads were required. Absence in connector-indexed results does not prove absence from deleted, unsynced or differently indexed historical mail.

No email was sent, forwarded, archived, labeled, deleted, marked read/unread, or used to accept an invitation. No browser account, credential, role, link, campaign, feed, tag, billing or storefront state changed. Complete message bodies, login addresses, security codes, tracked-action links and unrelated personal/customer data are not saved here.

## Continuation

Current business action remains READ_ONLY_MARKETING_RECONCILIATION. Email evidence strengthens the existing account-identity record; it does not restore access. The exact previously approved support request remains OWNER_AUTHORIZED_NOT_SUBMITTED with its existing form-input/readback gate. Its approved payload was not edited or submitted during this search. The owner input remains manual Contact email/optional CC correction; then obtain consistent current readback before the already-approved send. Do not repeat the approval question or infer a password reset/another account is the remedy.

Reuse the existing paid-growth continuation prompt and current memory digest. Independent analytics and local SEO/CRO tasks remain available while app access is unresolved. `google_access_recovery.md` owns the recovery chronology; this file is its bounded mailbox-evidence addendum.
