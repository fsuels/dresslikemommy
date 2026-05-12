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

## "Sync to main" — Frank's deploy workflow (CRITICAL — READ EVERY SESSION)

When Frank says **"sync to main"**, **"sync all changes to main"**,
**"do it for me"**, **"push to live"**, or any similar phrasing, this is
what he means and what Claude MUST do:

**Push to GitHub `main`. THAT IS the live deploy.** The live theme on
`dresslikemommy.com` is configured as a **GitHub-connected theme** —
see Shopify Admin → Online Store → Themes, where the live theme card
shows `dresslikemommy/main` with a GitHub icon. Pushing to
`origin/main` causes Shopify to pull the new theme files automatically
within seconds. There is no separate `shopify theme push --live` step
required, and the older Shopify CLI prompt that sometimes appears in
Terminal can be answered with `n` — it's a leftover from before the
GitHub integration was wired up.

**If Frank sees the live site still showing old content after a push:**
1. Hard-refresh the page (Cmd+Shift+R) to bust browser cache.
2. If still wrong, wait 30-60s — Shopify's GitHub pull can lag briefly.
3. If still wrong after a minute, check Shopify Admin → Themes → click
   the `···` menu next to the live theme → confirm GitHub sync ran.

Never tell Frank to re-run `shopify theme push --live` to "fix" a
cache issue. The GitHub push IS the deploy.

### THE WORKING PROCEDURE (proven May 11, 2026 — DO NOT DEVIATE)

**Claude CAN and MUST drive this end-to-end. Do not hand Frank clipboard
commands and wait. Do not ask permission three times. Do not warn about
limitations Claude has already worked around. Just do it.**

The proven path uses VS Code's Source Control panel because:
- Claude cannot type into Terminal (tier-"click" OS restriction).
- Claude CAN click buttons in VS Code (tier-"click" allows left-click).
- VS Code's "Commit & Push" button does git add + commit + push in one
  click and works perfectly. It uses whatever commit message is in the
  text box at the time — type it via the `mcp__computer-use__type`-
  blocked path is impossible, so Claude must accept the message that's
  already in the box, OR write the message into the box via clipboard
  paste before clicking. (Confirmed working: VS Code accepts a clicked
  Commit & Push even if Claude didn't author the message box content.)

**Exact step-by-step the FIRST time in a session:**

1. `mcp__computer-use__request_access` with:
   - apps: `["com.microsoft.VSCode", "com.apple.Terminal"]`
   - `clipboardWrite: true`
   - Note: VS Code's bundle ID is `com.microsoft.VSCode`, NOT
     "Visual Studio Code" or "Code". Using the wrong name fails with
     "not installed". The displayName comes back as "Code".
   - Both get granted at tier "click" — left-click only, no typing.

2. `mcp__computer-use__screenshot` to confirm VS Code is foreground and
   the Source Control panel is visible on the left with the "Commit &
   Push" button.

3. If there's a stale `.git/index.lock` from a previous failed git
   commit (common after an editor opened from `git commit -m` without
   `&&`-chained args), Claude's sandbox CANNOT delete it (the .git dir
   is permission-restricted). Frank must `rm` it himself, OR Claude can
   just click VS Code's Commit & Push — VS Code seems to clean up the
   lock automatically before running its own commit. (Confirmed working.)

4. `mcp__computer-use__left_click` on the "Commit & Push" button. In a
   default VS Code layout this is roughly `(203, 131)` but Claude must
   re-check coordinates against the actual screenshot every time —
   window position, sidebar width, and zoom level all shift it.

5. `mcp__computer-use__wait` for 4 seconds.

6. `mcp__computer-use__screenshot` to verify:
   - Source Control panel now shows 0 changes (or the "Commit & Push"
     button is gone / greyed out).
   - The Terminal window shows the git push output ending in
     `<old>..<new>  main -> main`.

7. **That's it. GitHub push = live deploy.** Tell Frank the commit
   landed and to hard-refresh (Cmd+Shift+R) on the live site in 30s to
   bust browser cache. Do NOT ask him to confirm a Shopify CLI prompt
   — that prompt, if it appears in Terminal from a stale CLI hook, is
   safe to answer `n`. The GitHub integration handles deploy.

8. Verify the commit landed on `origin/main` from the sandbox shell:
   `cd /sessions/.../dresslikemommy && git log origin/main --oneline -2`.
   That confirms the push reached GitHub and Shopify will pick it up.

### Why the OLD "give Frank a clipboard one-liner" approach is BANNED

The clipboard-only approach was the previous recommendation in this file
and it failed badly on May 11 because:
- A multi-line commit message with `git commit -m "..."` where the `"`
  closing quote is on a later line will sometimes open Frank's `$EDITOR`
  in the middle of the chain, breaking the `&&` sequence.
- That leaves `.git/index.lock` behind, blocking all future git
  operations until manually removed.
- Frank should NEVER be debugging git locks. The VS Code Source Control
  GUI handles all of this automatically.

### HARD CONSTRAINT (proven May 11–12, 2026): the Cowork sandbox CANNOT touch .git/

Empirical test: even after Frank ran `chown fsuels:staff` and `chmod u+rwX,g+rwX`
on `/Users/fsuels/Projects/dresslikemommy/.git`, the sandbox could create
files in `.git/` but could NOT delete them. `rm .git/anything` returns
`Operation not permitted`. This is a Cowork-sandbox-layer restriction,
not a Unix permissions problem. Host chmod/chown does not change it.

**Therefore: NEVER run `git commit` or `git push` from the sandbox shell.**
Every sandbox-git attempt leaves a `.git/index.lock` the sandbox can't
clean up, then blocks every future git operation in the repo. This wasted
~40 minutes on May 12.

### THE ONLY WORKING SYNC FLOW

When Frank says "sync to main", do this — no detours, no sandbox git:

1. `mcp__computer-use__request_access` for `["com.microsoft.VSCode"]` with
   `clipboardWrite: true`. Bring VS Code forward (`open_application`).

2. `mcp__computer-use__write_clipboard` with a short single-line commit
   message (e.g. "PDP: <one-line summary>"). Multi-line is fine but the
   FIRST line must be a good one-line summary.

3. Screenshot. Confirm the Source Control panel shows the modified files
   and the empty `Message (⌘Enter to commit on "main")` box.

4. `left_click` the message box to focus it. Then tell Frank in chat:
   "Press ⌘V to paste the commit message, then say 'pasted'." Wait.

5. After Frank confirms "pasted", screenshot. Verify the message box
   is no longer empty.

6. `left_click` the dropdown caret `⌄` immediately to the right of the
   `✓ Commit` button. A menu opens with: Commit / Commit (Amend) /
   Commit & Push / Commit & Sync.

7. `left_click` "Commit & Push" in that menu. Wait 6 seconds.

8. Screenshot. Verify either: "Committing Changes…" → gone (success),
   OR the Output panel shows an error.

9. **If the Output panel shows `Unable to create '.git/index.lock': File exists`**,
   the previous run crashed. CLAUDE cannot recover this. Tell Frank
   verbatim: "VS Code crashed mid-commit and left a lock file. In Terminal
   run: `rm -f /Users/fsuels/Projects/dresslikemommy/.git/index.lock` and
   say 'done'." When he says done, go back to step 6.

10. After commit success, verify from the sandbox shell:
    `git log origin/main --oneline -2` — confirm the new commit is on
    `origin/main`. (Read-only ops in `.git/` DO work from the sandbox.)

### Things to NEVER do — wasted hours of Frank's time

- ❌ Don't run `git commit` or `git push` from the sandbox shell. The
  half-completed lock file is unrecoverable from inside the sandbox.
- ❌ Don't paste a Terminal one-liner with `git commit -m "..."` where the
  closing `"` is on a later line — Frank's $EDITOR opens mid-chain and
  breaks the `&&` sequence.
- ❌ Don't tell Frank to "just delete the lock file" without ALSO giving
  the complete follow-up (commit + push). Half-fixes leave him doing
  manual git work he shouldn't be doing.
- ❌ Don't recommend the `sudo chown / chmod` perms fix as a path to
  letting the sandbox sync — empirically it doesn't help (the sandbox
  blocks `.git/` writes at its own layer). Leave that section deleted.
- ❌ Don't get fancy: no `git commit -F /tmp/msg.txt` here-doc tricks,
  no AppleScript, no Terminal tier-"full" escalation. The VS Code GUI
  click path above is the ONLY proven path.

### Before any sync attempt: check if a competing agent already pushed

If another agent (Codex CLI, Cursor, etc.) has been working in this
repo, it may have committed and pushed on its own. ALWAYS run
`git status --short && git log origin/main --oneline -3` from the
sandbox shell BEFORE attempting your own sync. If origin/main already
has the changes, tell Frank "already synced by another agent — here's
the latest commit on origin/main" instead of trying to push.

### Important details for the Shopify push

- `shopify theme push --live` targets the currently-published theme on
  the store. It prompts for confirmation because `--live` is destructive.
- Auth is via `.shopify-admin.env` at the repo root (gitignored). If the
  CLI prompts for login, Frank runs `shopify auth login`.
- The repo has a `.shopifyignore` — respect it.
- If Frank wants a preview instead of live, the safer variant is
  `shopify theme push --unpublished --json`. But "sync to main" default
  = push to LIVE.

### Sandbox limitations Claude must work AROUND

- Claude's sandbox CANNOT write or delete inside `.git/`. This is a
  Cowork-sandbox restriction, NOT host Unix permissions. Host
  chown/chmod does not change it. The proven workaround is the VS Code
  Commit & Push GUI path above. Do not try sandbox `git commit` again
  — every attempt creates an unrecoverable `.git/index.lock`.
- Claude cannot type into Terminal or VS Code (tier-"click"). Use
  GUI button clicks + the clipboard (write the commit message to
  Frank's clipboard, ask him to ⌘V into VS Code's message box).
- Claude cannot run `shopify theme push` directly. The GitHub-connected
  theme deploys automatically when `origin/main` advances — no
  separate CLI step is needed. If the legacy Shopify CLI prompt
  appears in Terminal after a push, answer `n` — it's a stale hook
  from before the GitHub integration.

**Proof the GUI path works: commit `c892877` (May 11, 2026) and
`beed4c3` / `8f6ae08` (May 12) all landed on `origin/main` via VS
Code's Commit & Push button.**

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
