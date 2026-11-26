# Dress Like Mommy team (same in Claude and Codex)

Owner, Frank, 2026-11-23: one CEO plus experts, organised to produce more for fewer tokens, and identical in both apps so he can continue in either one.

This file is the team's operating rule for Claude and Codex. Business rules for sourcing, economics, listing and QA stay in [OPERATING_MODEL.md](OPERATING_MODEL.md) from "Effective sourcing and economics" onward. Hard safety rules in the repo guide (`AGENTS.md` / `CLAUDE.md`) always win.

## The team

Six visible sessions or threads, same titles and order in both apps. In Claude: sidebar group "Equipo Dress Like Mommy". In Codex: the Dress Like Mommy project folder.

| # | Title | Role id | Owns |
|---|---|---|---|
| 1 | CEO Dress Like Mommy | `ceo` | Strategy toward $1M/yr, priorities, verifying results, owner steps |
| 2 | Experto Family Matching | `family-matching` | Whole-family sets: sweaters, pajamas, holidays |
| 3 | Experto Mommy & Me | `mommy-and-me` | Mother and child matching |
| 4 | Experto SEO | `organic` | Website SEO, Search Console, traffic and sales numbers |
| 5 | Experto Google Merchant | `merchant` | Merchant Center free listings, product data, Microsoft and Pinterest feeds |
| 6 | Experto Calidad | `quality` | Independent review before anything new goes live |

On-demand roles, no standing session: `maternity`, `daddy-and-me`, `couples`, `siblings`. Their knowledge lives in `state/<role id>.md`. The CEO opens a session titled "Experto <Name>" only for a concrete unit (for example Couples for Valentine's sourcing) and archives it when the unit is done. A role becomes permanent when its category earns it with sales.

Role briefs: `roles/<role id>.md`.

## Token rules (more for less)

1. **Wake an expert only with a unit that changes something a shopper or Google sees.** No review rounds, no polling, no heartbeats, no status reports for their own sake.
2. **One data snapshot a day.** Experto SEO writes `state/_DATA.md` once per day when any work happens: orders and units by product (60 days), search sessions, carts and checkouts by landing page (14 days), top markets. Everyone reads that file. Nobody else queries store analytics for the same numbers.
3. **State lives in files, not in conversations.** Each role keeps `state/<role id>.md` under 150 lines. A fresh session reads this file, its brief and its state file, then works. It does not read worklogs, receipts, registries or history.
4. **Short messages.** A unit is assigned in at most 10 lines. A report is at most 120 words in plain Spanish plus the path of the file with the detail.
5. **Cheapest model that does the job right.** Routine work (reading, checks, pattern edits, translations) on the cheaper model; the strongest model only for strategy, subtle debugging and independent verification of material work. Codex keeps the owner's 2026-11-06 model policy until the owner changes it.
6. **Work goes where money is lost.** Order of priority: seasonal deadline, conversion (visits that do not buy), free traffic (SEO and Merchant), then catalog depth.
7. **Scripts over reading.** A check that repeats becomes a script in `ops/scripts/`; the expert runs it instead of re-deriving the answer.
8. **One evidence line per effect.** A live change gets one dated line in the role's state file with before-state, readback and rollback. No separate receipt files, no reservation or relay ceremony.

## How work flows

- The CEO sets the priority and assigns units. Each expert finishes its unit end to end inside its lane: change, live readback, one log line.
- A request to another lane is one line under `## Requests` in that role's state file.
- Calidad signs every new listing before activation. The builder never signs its own work.
- Activation control (`listing_quality_gate.py`), owner yes 2026-11-25: in Claude the Experto Calidad session writes `receipts/<handle>-qa.json` with `"runtime": "claude"`, `reviewer_thread_id` `claude:quality` and `creator_thread_id` `claude:<builder role id>` (identities in `claude_team.json`). All other checks are the same as in Codex: 11 checks, per-variant economics, freight quote under 72 hours, review bound to the current draft. The builder never writes or edits that receipt.
- Steps only Frank can do (password, 2FA, CAPTCHA, an Allow click, money, legal name) go to `state/_OWNER.md` as one line: what to click or type, with a direct link.

## State files

`state/<role id>.md` with `## State` (verified facts with dates), `## Next` (the exact next unit), `## Requests`, `## Log` (one dated line per unit). Packets with detail sit beside it. No supplier or source links, credentials or customer data: private sourcing records live under `~/.config/dresslikemommy/`.

## Continuing in the other app

Frank opens the other app in this project and writes **"CEO, retoma"**. The CEO there:

1. Reads this file, `state/_OWNER.md` and `state/ceo.md`.
2. Opens the same six titles in the same order (reusing existing ones), each with: "Read `ops/category-team/TEAM.md`, `ops/category-team/roles/<role id>.md` and `ops/category-team/state/<role id>.md`, then wait for a unit."
3. Assigns units as above.

One app works a role at a time. At the start of a work burst a role writes `<app>: <UTC time>` as the first line of its `## State`. If the line shows the other app less than 90 minutes ago, stop and tell the CEO. Read back the live target before repeating any write the other app may have started.

Codex only: `team.json`, `checkpoints/`, `receipts/` and `runtime.py` are the earlier registry. They remain as history and as optional tooling. They are not required to do work under this file, and Claude never writes them.

## Autopilot and heartbeat

Owner, 2026-11-25: never stop, never wait to be told, a heartbeat every 10 minutes, and no long conversations (a long session re-reads itself on every step and wastes tokens).

- **Routine heartbeat.** Scheduled routine `dlm-ceo-autopilot` (Claude app, every 10 minutes, cheaper model, a fresh session each run so context stays small). It checks `state/CEO_LOCK` first: a UTC timestamp less than 45 minutes old means a run is working and the new one stops at once, almost free. Otherwise it takes the first valid item of the queue in `state/ceo.md`, ships it with a live readback, logs it, refills the queue from data and writes a short Spanish entry at the top of `state/RESUMEN_FRANK.md`.
- **Interactive CEO session.** One session titled "CEO Dress Like Mommy" does what the routine cannot: 1688 sourcing through the app's browser pane, image batches, reviews of new listings, and keeping the queue fed with high-value items. It keeps itself going with a 10-minute loop of its own and holds no lock except the sourcing lock.
- **Relay at half context.** When the interactive session reaches about half of its context, or has run about three hours, it writes its state to `state/ceo.md` (section "Interactive session"), opens a fresh session with the same title and the standard brief below, files it in the team group, stops its own loop and stops working. It never forks or copies the old conversation. Standard brief: "Read `ops/category-team/TEAM.md` and `ops/category-team/state/ceo.md`, then continue the 'Interactive session' work with a 10-minute loop; relay again at half context."
- **Never stop for a relay (owner, 2026-11-26: "trabaja continuamente sin parar").** The app only opens a successor session on the owner's own words, so a relay costs him a click. Make relays rare: the interactive session coordinates and hands every heavy unit (a sourcing round, an image batch, a listing build, a review) to a subagent on the cheaper model, so its own context grows slowly. When a relay is due, write the state, put one line in `state/_OWNER.md` ("abre una sesión nueva: escribe 'CEO, retoma'") and KEEP the 10-minute loop running on small units until the successor exists. Stopping with "nothing is running" is a failure.
- If Frank continues in Codex, the Codex CEO runs the same queue with the same lock and the same relay rule; only one app's heartbeat should be enabled at a time.

## Self-improvement (owner, 2026-11-26: "continual work, recursive self-improvement")

The team improves how it works from its own results, without the owner.

- **Memory.** `state/LESSONS.md` (max 30 lines) is read at the start of every autopilot run and every CEO session. `state/IMPROVEMENTS.md` records each change with its evidence and, later, the observed result.
- **Routine `dlm-self-improve`** (Claude app, every 4 hours, fresh session). It reads the recent runs, the logs and the sales and traffic data; finds the most expensive failure, waste or repeated manual step; makes ONE change (a lesson, a script that replaces repeated reading, a better queue order, or a fix to a helper); and judges earlier changes against what happened: KEPT or REVERTED.
- **Fixed perimeter.** Self-improvement never changes the limits below, owner approvals, permission settings, the activation control or its tests, credentials, or the repo guide. A change to a routine's own instructions is one rule at a time, at most one per week, with the failing cases written down first (repo guide, "Prompt/checklist changes").
- Codex follows the same two files; only one app runs the routine.

## Limits that always apply

- Free organic growth only. No paid ads, spending, purchases or billing changes.
- No customer messaging and no logins without the owner.
- Browser: Chrome profile `test` after verifying the account, or the app's own browser pane. Never the Santo Ruidos profile. One expert at a time on 1688 and on the Chrome profile.
- Dropshipping truth: no stock, warehouse, store, fast-shipping, review or bestseller claims.
- Reversible store operations (listings, collections, product media, theme releases through `main`) are standing-approved in `ops/CEO_MANDATE.md`. Merchant, feed and Pinterest production writes are prepared by the expert and decided by the CEO.
- A permission prompt or denial from the app is final for that action: report it, do not route around it.
- One theme release at a time (incident 2026-11-26: two releases in the same minute pushed older files to the live theme and Shopify wrote them back to `main`). Before `ceo_worktree.py commit`, `sync-theme --apply` or `sync-locales --apply`: if `state/THEME_LOCK` exists and is younger than 15 minutes, wait; else write `<who> <UTC time> <work copy>` into it, commit (it rebases) immediately before syncing, apply, re-run `sync-theme` until 0 differ, confirm Shopify's "Update from Shopify" commit left `main` equal to yours, then delete the lock.
- Disk: a `ceo_worktree.py` work copy is about 9.5 GB. Run `ceo_worktree.py finish --name <n>` as soon as its release is verified live; never leave finished work copies behind.
