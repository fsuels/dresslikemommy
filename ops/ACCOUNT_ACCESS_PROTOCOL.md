# Account Access Protocol

Purpose: prevent false account-access blockers across Google Ads, Merchant Center, GA4/GTM, Search Console, Shopify Admin, Pinterest, GitHub, and business email.

Credentials and sessions are operator-side assets, not repo assets. Do not copy passwords, recovery codes, cookies, session tokens, screenshots showing secrets, or credential values into the repository, worklog, evidence packets, prompts, or final reports.

## Default Rule

An account is not blocked just because a newly opened tab lands on a login page.

Before declaring an account-access blocker, the agent must complete the recovery ladder below, document the attempts, and keep unrelated safe lanes moving.

## Recovery Ladder

1. Check the assigned task-owned background session and configured structured integrations first.
   - Follow `ops/BROWSER_SUBAGENT_COORDINATION.md`; inspect only assigned surfaces, never an unrelated personal tab inventory or another task's active tab.
   - Reuse an authenticated assigned session for the exact account, advertiser, Merchant account, property, store, repository or mailbox.
   - A new dedicated background tab is allowed when isolation requires it. Confirm its identity and availability; do not interpret a copied tab ID as a transferable session.
2. Check repo-known configured access and documented local credential paths within the authorized scope, without exposing secrets.
   - Shopify Admin API: use the documented non-repo credential files under `~/.config/dresslikemommy/`.
   - GitHub: use the configured GitHub connector or `gh` auth state when available.
   - Paid-media and analytics surfaces: use authenticated browser sessions or configured connectors if present.
3. Navigate from the authenticated session to the exact surface.
   - Confirm account identifiers before reading or writing. Examples include advertiser ID, Merchant account ID, Google Ads customer/campaign ID, GA4 property, Shopify store, GitHub repo, or mailbox.
   - If a direct URL redirects to login, check only the assigned session or configured connector before calling it blocked. Do not recover by taking over personal Chrome or bypassing an interactive gate.
4. Use current-session credentials only transiently when the owner has supplied them in the current session and the target site is the expected account.
   - Do not save the password in the browser unless the owner explicitly asks.
   - Do not persist the credential in any file.
   - Do not repeat the credential in logs, evidence, worklogs, prompts, or chat summaries.
5. Stop only on true interactive gates.
   - Stop and report for CAPTCHA, MFA/2FA, account chooser ambiguity, permission denial, billing/payment prompts, policy prompts, destructive-change prompts, or a missing credential that is not available from the current session, connector, local secure source, or existing authenticated browser.
   - Record the exact URL/surface, what was attempted, and the next unblock action.

## Coordination Requirements

- The parent/orchestrator owns account-surface routing.
- Keep one tab/session claim per surface in `ops/AGENT_COORDINATION.md` or the active evidence packet tab map.
- Independent tasks need separate supported browser surfaces. They must not duplicate an active write claim; parallel reads still require separate tab ownership.
- A stopped account lane must be labeled `ACCESS_RECOVERY_REQUIRED`, `MFA_OR_CAPTCHA_REQUIRED`, `PERMISSION_REQUIRED`, or `ACCOUNT_SWITCH_REQUIRED`, not a generic P0 blocker.
- A true P0 blocker requires both:
  - the access is necessary for the next approved sales-moving action, and
  - the recovery ladder has failed or hit an interactive gate.

## Surface Checklist

For each account-side readback, record:

- Surface: Google Ads, Merchant Center, GA4/GTM, Search Console, Shopify Admin, Pinterest, GitHub, or business email.
- Account/store/property/advertiser/repo/mailbox identifier when visible.
- Existing tab/session used or reason a new tab was required.
- Prompt state: authenticated, login, account chooser, MFA/CAPTCHA, permission denied, billing/policy, or unsaved changes.
- Readback result and whether any write controls were touched.

## Write Boundary Reminder

Account access is not action approval. Even when authenticated access exists, live writes still follow `AGENTS.md`, `ops/AGENT_COORDINATION.md`, `ops/BROWSER_SUBAGENT_COORDINATION.md`, and `ops/marketing/spend_authorization.md`.
