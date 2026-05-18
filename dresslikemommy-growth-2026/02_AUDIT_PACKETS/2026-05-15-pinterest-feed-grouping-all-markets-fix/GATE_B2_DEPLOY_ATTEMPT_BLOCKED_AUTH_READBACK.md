# Gate B-2 Deploy Attempt Blocked On Auth / App Config

Generated: 2026-05-18

Mode: live Gate B-2 deploy attempt under owner instruction. No Cloudflare resource, R2 bucket, R2 object upload, Worker deploy, Shopify app-proxy configuration, Pinterest catalog/source configuration, campaign change, product/feed mutation, billing action, credential persistence, or destructive action occurred.

## What Was Attempted

Owner requested:

```text
Deploy the Cloudflare R2/Worker path, upload the verified TSV, configure Shopify App Proxy to it, then read back the public URL. Gate B-3 stays closed until that URL passes.
```

## Preflight Readback

Verified local feed:

```text
SHA-256: 8aefb9cf4057497e4f56df36c2157b44c913e049fb1ecb2f75f505f1eb5470d7
wc -l: 41815 lines = 1 header + 41814 data rows
size: 145 MiB / 151,559,047 bytes
```

Checked Cloudflare CLI auth:

```text
npx wrangler@4.86.0 whoami
You are not authenticated. Please run `wrangler login`.
```

Checked local credential paths:

```text
No CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, or Wrangler auth token was available in this shell.
No Cloudflare auth file was found under ~/.wrangler, ~/.config/.wrangler, ~/.cloudflare, ~/.config/cloudflare, or ~/.config/dresslikemommy.
```

Checked Shopify app config:

```text
shopify version: 3.90.0
shopify app info: Couldn't find an app toml file at /Users/fsuels/Projects/dresslikemommy
```

## Scope Stop

`npx wrangler@4.86.0 login` opened an OAuth flow requesting many broad scopes beyond this feed-only job, including unrelated AI, D1, Pages, Queues, Pipelines, Containers, Email, Browser, and other write/admin scopes.

The login was stopped instead of authorizing a broad grant.

Wrangler supports narrower OAuth scopes, but it still requires owner login in Cloudflare. A safer path is an owner-created Cloudflare API token scoped only to this deployment.

## Dry-Run Result

The Worker package itself compiles with the Wrangler config:

```bash
cp wrangler.toml.example wrangler.local-check.toml
npx wrangler@4.86.0 deploy --dry-run --config wrangler.local-check.toml
rm -f wrangler.local-check.toml
```

Result:

```text
Total Upload: 4.40 KiB / gzip: 1.71 KiB
Bindings:
- env.PINTEREST_FEED_BUCKET -> R2 Bucket dlm-pinterest-feeds
- FEED_OBJECT_KEY
- FEED_SHA256
- FEED_ROW_COUNT
- REQUIRE_SHOPIFY_PROXY_SIGNATURE
--dry-run: exiting now.
```

## Current Blockers

1. Cloudflare deploy is blocked by missing authenticated Cloudflare API access.
2. Shopify App Proxy configuration is blocked by missing Shopify app project/config (`shopify.app.toml`) or an identified installed app whose app-proxy settings can be changed.
3. Gate B-3 remains closed; Pinterest was not touched.

## Follow-Up Auth Readback

After the owner added real Cloudflare values to `~/.config/dresslikemommy/cloudflare.env`, the shell loaded them and `npx wrangler@4.86.0 whoami` passed:

```text
Logged in with a User API Token for [owner email redacted]
Account: [owner email redacted]'s Account
Account ID: [cloudflare account id redacted]
```

The next Cloudflare write preflight failed before any bucket/object/deploy write:

```text
npx wrangler@4.86.0 r2 bucket list
ERROR: Please enable R2 through the Cloudflare Dashboard. [code: 10042]
```

Updated blocker state:

1. Cloudflare auth is now valid.
2. Cloudflare R2 is not enabled for the account yet.
3. Enabling R2 may involve a dashboard billing/payment-method prompt, so automation stopped for owner action.
4. Shopify App Proxy configuration is still blocked by missing Shopify app project/config or identified installed app.
5. Gate B-3 remains closed; Pinterest was not touched.

## Exact Next Unblock

Owner/operator should provide one of these:

### Preferred Cloudflare auth path

In a non-repo shell, set:

```bash
export CLOUDFLARE_API_TOKEN='redacted-token'
export CLOUDFLARE_ACCOUNT_ID='redacted-account-id'
```

The token should be limited to the Cloudflare account used for Dress Like Mommy and only the permissions needed for:

- Workers script deploy/edit.
- Workers R2 Storage edit.
- Account read.
- Zone read / Workers route edit only if using a custom Cloudflare domain instead of the default `workers.dev` URL.

Do not paste the token into repo files, docs, worklogs, or prompts.

### Shopify app-proxy path

Identify the installed Shopify app or provide a Shopify app project/config that owns the app proxy. The needed final setting is:

```toml
[app_proxy]
url = "https://<deployed-worker-host>/pinterest-feed.tsv"
subpath = "pinterest-feed.tsv"
prefix = "apps"
```

Then the public URL to read back remains:

```text
https://www.dresslikemommy.com/apps/pinterest-feed.tsv
```

Do not configure Pinterest Catalogs until that public URL passes the Gate B-2 readback.

### Current owner action after follow-up

Open Cloudflare Dashboard for the account above and enable R2. If Cloudflare asks for a billing/payment method, the owner must decide and complete that directly. After R2 is enabled, rerun:

```bash
set -a
source ~/.config/dresslikemommy/cloudflare.env
set +a
cd /Users/fsuels/Projects/dresslikemommy/ops/cloudflare/pinterest-feed-worker
npx wrangler@4.86.0 r2 bucket list
```

Then automation can create/reuse `dlm-pinterest-feeds`, upload the TSV object, and deploy the Worker.

## Follow-Up Deploy Readback

After R2 was enabled, Gate B-2 Cloudflare deployment succeeded. Evidence moved to:

```text
GATE_B2_CLOUDFLARE_DEPLOY_READBACK.md
```

Remaining blocker is Shopify App Proxy configuration. The direct Worker URL is live and verified, but `https://www.dresslikemommy.com/apps/...` is not configured yet.
