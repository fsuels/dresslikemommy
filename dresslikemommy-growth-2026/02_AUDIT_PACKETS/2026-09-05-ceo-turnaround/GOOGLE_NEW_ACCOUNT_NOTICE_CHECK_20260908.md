# September 8 Google new-account notice check

Status: `VERIFIED_NOTICE_EVIDENCE__CURRENT_LINK_AND_CLAIM_UNCONFIRMED`. Parent owns canonical integration and external execution. This is one bounded read of the new September 8 evidence window, not a repeated historical mailbox audit.

## Query and coverage

Connector: Gmail structured API. One `gmail_search_email_ids` call, `max_results=10`, returned **2 message IDs** and `next_page_token=null`. Both returned messages were read once in full; the profile was read once to compare recipient identity transiently. No additional search, pagination, attachments, invitation link, sign-in link, browser, account, role, message, or tracking mutation occurred.

Window: September 8, 2026 00:00–September 9 00:00 America/New_York, encoded as Unix seconds (04:00 UTC boundaries).

```text
in:anywhere after:1788840000 before:1788926400 from:google.com {4683483813 "468-348-3813" 5849297181 5849532286}
```

Both messages have Google `dkim=pass`, `spf=pass`, and `dmarc=pass` in the returned authentication headers. Their Delivered-To addresses match the currently connected Gmail mailbox; their original To addresses do not. This is forwarded delivery and does not establish that the Google identity currently connected to Shopify has direct administrator access. No private address, service-account identifier, authentication token, recovery code, or link token was saved.

## Verified notification facts

| Notice time | Account/entity | Exact supported fact | Limit |
|---|---|---|---|
| September 8 17:19:59 UTC / 13:19:59 EDT | Ads `468-348-3813`; manager `768-709-3497`, named Shopify Google Channel App | Google says the operating Ads account is now linked to that manager. The notice describes a completed link and says no action is needed if expected. | Does not prove current link persistence, direct human Admin, billing, active campaigns, tracking, or relationship to intended owner manager `7001079966`. |
| September 8 17:26:47 UTC / 13:26:47 EDT | Merchant `5849532286`, named Dress Like Mommy; `dresslikemommy.com` | Google says this account lost its website URL claim because another Merchant account verified and claimed the same or a parent URL. The notice says affected-domain feeds will be disapproved and products will not appear on Google Shopping or other Google services. | The winning Merchant ID is not supplied. This is a claim-change event at the notice time, not a current claim readback or proof the present conflict is unresolved. |

The Merchant notice identifies the claim-winning principal and contact principal as service-account addresses under `gserviceaccount.com`; neither matches the connected Gmail principal. Those are non-human service principals, not proof of the current owner's direct Merchant role. The notice alone does not establish who controls the service accounts or which app caused the claim transition. Do not infer malicious activity or a specific owning app/project.

## Consequence for the active task

New Ads `4683483813` and Merchant `5849532286` now have authenticated notification evidence of existence/activity on September 8. They are no longer supported only by memory. Do not create duplicate replacements merely because their IDs or current access were unknown. This query does not independently identify Merchant `5849297181`, and its lack of a dedicated matching notice does not disprove that candidate.

The precise hypothesis to verify is a competing Merchant claim plus a possible service-principal/direct-human-access mismatch. Two notices establish the link and claim events, not that mismatch's cause or current state. No pending invitation or owner acceptance step was identified in these two messages.

Single next action: root should reconcile the persisted Shopify Google & YouTube Merchant selection and current claim-owning account through a permitted access path, using the existing IDs without asking the owner to recover them. Keep the CUA forbidden-URL restriction intact; no browser substitute or unchanged authentication retry follows from these emails. Continue the separate tracking-source lane while account access remains unresolved.

## Evidence and checks

- Ads message: [Gmail notification](https://mail.google.com/mail/u/0/#all/1a08208a69716522); immutable message ID `1a08208a69716522`.
- Merchant message: [Gmail notification](https://mail.google.com/mail/u/0/#all/1a0820ee279083db); immutable message ID `1a0820ee279083db`.
- Exact query count: 1; result IDs: 2; full message reads: 2; profile identity comparison: 1; returned next page: none; external writes: 0.
- Only sanitized findings are stored. Raw MIME, personal/service addresses and embedded action URLs remain outside repository evidence.
- Evidence covers only the named query in the currently connected mailbox. It is not proof that no other account, invitation, notification, owner, suspension, or claim change exists.

Continuation: TA-01/TA-07 account connection and tracking cleanup under the existing paid-growth prompt; preserve the new goal/heartbeat transfer handled and verified by root, all full-paid controls, GA4 property `330266838`, and the completed local-retail sync repair.

Final verification: the Merchant notice's exact public website is `https://www.dresslikemommy.com`. A `python3` check passed for whitespace, trailing newline, absence of stored email addresses, bounded query/coverage statements, and the three evidenced account/manager IDs.
