# Project main synchronization — September 14, 2026

Local main contains the complete reviewed storefront fixes and the newer local improvements. GitHub main now contains 6,804 project-file changes, verified at commit `60ec4959d09c5c67e89bef648991921e6979806d`.

The remaining 72 root theme-file changes are committed locally and held from GitHub because that branch controls the active Shopify theme. The overall request is therefore PARTIAL until the owner publication dependency clears.

## Preserved and integrated

- All 527 theme files were independently checked: 520 match the reviewed release exactly, and seven retain additional local fixes for cart updates, Spanish guidance, gift-card recipient errors and password-label accessibility.
- Both configuration files and all 20 templates remain unchanged. All 58 separate V8 files remain unchanged locally; 57 are committed and one private historical worklog copy stays local.
- The four newer GitHub commits were merged, including Shopify's existing changes and the agent harness documents. Three overlapping files were resolved against the reviewed source; no unresolved conflict remains.
- Private supplier records and runtime caches stay local. Private supplier URLs were removed only from the committed copies of two documents; local originals remain intact.
- This snapshot includes work captured through 20:52:55 UTC. Later work by other active tasks remains undisturbed.

## Checks and limits

- PASS: independent 527-file comparison, 22 configuration/template preservation checks, source/index merge checks, 81 syntax checks, 30 reviewed-source regression tests, 14 feed-worker tests and strict continuity before synchronization.
- PASS: the GitHub update preserves all 528 guarded theme/configuration/workflow entries. Every theme directory is identical to the previous remote main; no theme change appears anywhere in the pushed history. No excluded private path was added.
- Existing failures recorded: three Liquid complexity checks, two outdated Python status assertions, nine missing-dependency imports, and whitespace findings in historical/imported archive files. These were preserved and disclosed rather than disabled or represented as passing.
- This synchronization does not establish a new PageSpeed score, live buyer acceptance or conversion increase.

## Source checkpoints and rollback

The original local commit is `8abff26`, retained by `codex/main-before-sync-20260914-2024`. The complete source snapshot is `9ee5c13`, the GitHub merge is `c126eaa`, and the latest captured full-source checkpoint is `2b31878`. The previous remote main, `cc62620`, remains the parent of the project-file synchronization commit. Private before-file copies are also retained.

## One remaining owner action

In [Shopify Admin → Online Store → Themes](https://admin.shopify.com/store/dresslikemommy-com/themes), publish **DLM UX Performance QA 2026-09-10 (137888792673)**. It is the reviewed release and remains a draft. Keep the former live theme for rollback.

The Shopify connector blocks theme publishing and live-theme file writes. Because current theme **dresslikemommy/main (133290917985)** is linked to GitHub main, a push containing the pending theme changes would bypass that restriction. Project files were synced separately using Shopify's documented rule that [folders outside the theme structure are ignored](https://shopify.dev/docs/storefronts/themes/tools/github).

Continuation: “Verify the published theme, reconcile the remaining 72 theme-file changes into GitHub main, and verify the affected buyer paths and PageSpeed.”
