# Finding — Shopify Pinterest Channel UI Does Not Expose Path A Toggle

Generated: 2026-05-15
Source: live read-only readback by Claude-in-Chrome session in user Francisco's authenticated Shopify Admin, store `dresslikemommy-com`, channel route `/apps/pinterest-4`.

Mode: repo-local diagnostic only. No Shopify, Pinterest, Merchant, Google Ads, theme, billing, product, feed, source, tag, CAPI, campaign, or budget write occurred.

## What the live UI exposes

The Shopify Pinterest sales-channel Settings tab contains three sub-sections:

- **Account**: connection display, claimed websites list, `Disconnect all` button, `App reset` button. No variant-submission controls.
- **Marketing**: ad account `549756244483`, Pinterest tag `2620007050621`, advertising agreement acceptance display, partial billing card. No variant-submission controls.
- **Shopping**: publishing-status banner ("Merchant account approved"), product-feeds card with a read-only `PRIMARY COUNTRY AND LANGUAGE` block showing country `United States` and language `en`. A `Manage` link opens a "Product feed status" sub-page listing 19 auto-generated feeds.

The 19 feeds are URL-path-derived language variants of a single primary `US / USD` market:

`US (en)`, `US (fr)`, `US (es)`, `US (ja)`, `US (it)`, `US (nl)`, `US (de)`, `US (ar)`, `US (pl)`, `US (cs)`, `US (da)`, `US (fi)`, `US (el)`, `US (he)`, `US (hi)`, `US (ko)`, `US (no)`, `US (ro)`, `US (pt-BR)`

Per-feed action is `Pause` only. There is no per-feed Edit, no variant-submission toggle, no image-source toggle, no additional-images control, and no per-market or per-language editable selector.

There are no Canada / United Kingdom / EU / Australia / International market entries in the Pinterest channel. The 6 active Shopify Markets do not appear here as separate Pinterest feeds — Pinterest is treating the localized URL slugs (`/fr`, `/es`, `/de`, etc.) on the US storefront as feeds.

Stop-condition prompts encountered: none. No re-auth, no scope change, no billing modal, no destructive confirm, no CAPTCHA.

## What this means

**Path A (toggle the Shopify Pinterest channel's variant-submission setting) is not available.** The drafted Path A approval phrases in `MASTER_ALL_MARKETS_APPROVAL_PHRASE.md` and `per_market_packets/*.md` describe a control that does not exist in this channel's current UI.

**Path B (custom Pinterest catalog feed with `item_group_id` per row) is now the only viable path** for fixing the variant duplication.

## Why Path B is correct here

Pinterest's catalog ingestion supports three source types: Shopify-app emitted (current), data feed URL, and Pinterest API. Switching the catalog source from the current Shopify-emitted feeds to a properly grouped data feed URL would:

- Replace the 19 per-language US feeds with one or a small number of properly grouped feeds.
- Carry `item_group_id` on every row, collapsing same-parent variants into a single Pinterest catalog product.
- Pin `image_link` to product featured image.
- Preserve language variants via `language` and `link` columns rather than 19 separate sources.

Path B is Pinterest-side configuration, not Shopify-side. The Shopify Pinterest channel does not need to be disconnected; the Pinterest catalog manager simply uses the new feed source instead of (or in addition to, then deprecating) the auto-emitted source.

## What was NOT changed

- No Shopify product/title/price/inventory/vendor/type/policy edit.
- No Shopify Pinterest channel save / toggle / pause / disconnect / reset.
- No Pinterest catalog / source / feed / tag / CAPI / audience / campaign / budget / bid / status / billing change.
- No theme push, no file deploy, no destructive filesystem action.
- No credentials persisted or exposed.

## Next action

Pivot the packet so Path B is primary. New approval gate must cover:

1. **Generate** the grouped feed locally via `ops/scripts/generate_pinterest_feed_grouped.py` (read-only against Shopify Admin GraphQL).
2. **Decide hosting** for the generated feed (Shopify app-proxy / GitHub raw / external object storage). Each option needs its own approval consideration. See `HOSTING_OPTIONS.md` (to be added).
3. **Configure Pinterest catalog** to ingest the new feed source.
4. **Pause then later remove** the legacy auto-emitted per-language feeds at Pinterest's catalog manager once the new source is verified.
5. **24h re-sync** then capture before/after readback per the existing per-market packets.
6. **Create `FIX_LANDED_FRESHNESS_MARKER.txt`** with the attest phrase to flip the automated guardrail to strict.

Existing repo evidence preserved:
- `pinterest_exact_product_group_item_id_import.csv` (333-variant US active-clean scope) still shows the per-variant pattern that confirms the bug.
- Cross-market diagnosis still applies — the bug is structural to the channel's emission.
- The automated guardrail `ops/scripts/check_pinterest_feed_grouping.py` continues to catch any per-variant snapshots until a clean Path B feed lands.
