# CLAUDE.md — Working notes for the dresslikemommy Shopify theme

This file is Claude's persistent memory for this project. Read it at the
start of any session before touching this repo.

## Project at a glance

- Shopify theme (Dawn 14.0.0 base) for **Dress Like Mommy** at
  `dresslikemommy.com`.
- Repo: `git@github.com:fsuels/dresslikemommy.git`, default branch: **`main`**.
- Theme files live in the standard Shopify layout (`sections/`, `snippets/`,
  `templates/`, `assets/`, `config/`, `locales/`, `layout/`).
- Owner: Frank (suelsferro@hotmail.com).

## "Sync to main" — Frank's deploy workflow (IMPORTANT)

When Frank says **"sync to main"**, **"sync all changes to main"**, or any
similar phrasing, he means TWO things, and both must happen:

1. **Push to GitHub `main`** — commit every local change and push to
   `origin/main`.
2. **Deploy to the Shopify LIVE theme** — push the same files into the
   currently-published theme on `dresslikemommy.com`.

Do not stop after step 1. A GitHub push alone does NOT update the live
storefront for this shop, because the live theme is **not** connected to
the GitHub branch — it's deployed via the Shopify CLI. (This was
confirmed during the May 2026 sync session.)

### The exact two-step procedure

```bash
# Step 1 — GitHub
cd ~/Projects/dresslikemommy
# Remove a stale lock if a previous attempt crashed:
rm -f .git/HEAD.lock
git add -A   # or list specific files
git commit -m "<concise subject>

<body>"
git push origin main

# Step 2 — Shopify (deploys to the LIVE theme)
shopify theme push --live
```

### Important details for the Shopify push

- `shopify theme push --live` targets the currently-published theme on
  the store. It will prompt for confirmation because `--live` is
  destructive — confirm to proceed.
- Auth is via `.shopify-admin.env` at the repo root (present locally,
  gitignored). If the CLI prompts for login, Frank should run
  `shopify auth login` first.
- The repo has a `.shopifyignore` — respect it. Don't try to push files
  it excludes.
- If Frank wants a preview before going live instead, the safer variant is
  `shopify theme push --unpublished --json`, review the preview URL, then
  publish from the Shopify admin. But the default "sync to main" request
  means **push to live**.

### Sandbox limitation Claude must remember

Claude's sandbox **cannot write to this repo's `.git` directory** because
of macOS file-permission boundaries on the workspace mount. That means:

- Claude can stage edits to working-tree files (Edit/Write tools work).
- Claude **cannot** run `git add` / `git commit` / `git push` directly.
- Claude **cannot** run `shopify theme push` directly either.

So when Frank says "sync to main", the right move is:

1. Make/verify the file edits via Edit/Write.
2. **Write the tailored one-liner to Frank's clipboard** using the
   computer-use `write_clipboard` tool (request `clipboardWrite` grant
   the first time in a session). Frank has confirmed he wants the
   clipboard-write step every time — he just opens Terminal and pastes.
3. Also show the same command in the chat as a fenced shell block, so
   it's visible and reviewable, not just hiding in the clipboard.
4. After Frank runs it, confirm the commit landed on `origin/main` (via
   `git log origin/main` in the sandbox shell — that read works fine).

The command MUST be tailored to the actual session:
- `git add` lists the real files that changed (or `-A` if everything
  in the working tree should go).
- The commit message subject and body describe the real work, not a
  template.
- Always include `rm -f .git/HEAD.lock` at the top — stale locks from
  prior failed attempts are common on this mount.
- Always end with `shopify theme push --live` unless the change is
  documentation-only (like editing CLAUDE.md) AND Frank has explicitly
  said no deploy is needed. Default is: deploy.

### Canonical "sync to main" command to give Frank

```bash
cd ~/Projects/dresslikemommy && \
rm -f .git/HEAD.lock && \
git add -A && \
git commit -m "<subject>

<body>" && \
git push origin main && \
shopify theme push --live
```

Adjust `git add` to specific paths when only certain files should be
included.

## Theme layout notes (so Claude doesn't have to re-discover them)

- **PDP entry point**: `sections/main-product.liquid`. The conversion-
  support / trust block lives inside the `.additional-info` wrapper and
  is rendered via `{% render 'pdp-purchase-confidence' %}`.
- **Purchase-confidence trust block**: `snippets/pdp-purchase-confidence.liquid`.
  Three promise rows (shipping, returns, secure checkout) plus three
  collapsed `<details>` (shipping details, return policy, payment & privacy).
- **PDP policy modals** (added May 2026): `snippets/pdp-policy-modals.liquid`.
  Intercepts the "View return details" and "View privacy details" links
  inside `pdp-purchase-confidence.liquid` and opens an in-page modal
  instead of navigating to `/policies/refund-policy` or
  `/policies/privacy-policy`. The triggers keep their real `href` for
  no-JS, right-click "open in new tab", and SEO.
- **Shipping-country checker**: `snippets/shipping-country-checker-modal.liquid`.
  Established modal pattern in this theme — use it as the reference for
  any new modal (z-index 10000, lock `<html>` overflow, simple
  no-transition overlay so sticky PDP elements stay painted).

## Conventions Claude should follow in this repo

- Use the existing CSS variables / colors when extending the design
  (`#1D8656` green, `#201613` near-black for body text). The
  purchase-confidence module is the reference for new PDP trust UI.
- Liquid: prefer `{%- liquid ... -%}` blocks for assignment-heavy logic;
  match the existing whitespace style.
- Wrap new copy in `'<key>' | t` with a sensible English fallback
  via `if … contains 'translation missing'`, mirroring the pattern in
  `pdp-purchase-confidence.liquid`.
- Don't `localStorage` or `sessionStorage` from scripts injected into
  Liquid snippets unless there's a clear reason — the shipping checker
  is the one place this theme does it, with try/catch wrappers.
- Respect `.shopifyignore`.

## Useful repo paths

- `ops/` — internal ops docs (`SHIPPING_SLA.md`, `experiments.md`, etc.).
- `dresslikemommy-growth-2026/` — growth / CRO audit packets and reports.
- `GPT/` — exported reviews, prompt notes, design refs.
- `agent-backend/` — separate Node service for the storefront agent.

## Recent significant work

- **May 2026** — PDP in-page policy modals (CRO). Commit `e8e62e7` on
  `origin/main`. Replaces the standalone refund/privacy page exits inside
  the Purchase Confidence module with a lightweight modal pattern that
  mirrors the shipping-country checker.
