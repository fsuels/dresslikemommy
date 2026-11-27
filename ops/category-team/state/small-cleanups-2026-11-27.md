# Small cleanups (collection-copy-4, 2026-11-27 11:50-12:05Z)

## 1. Article microdata removed

`sections/main-article.liquid`: removed only the microdata attributes: `itemscope itemtype="https://schema.org/BlogPosting"` on `<article>`, `itemprop` on the 3 hero image wrappers, headline, date, article body, and the two author `itemprop="author" itemscope itemtype="https://schema.org/Person"` / `itemprop="name"` (10 itemprop + 3 itemscope). No class, structure or content change. The page keeps its single BlogPosting JSON-LD (154910c).

Live, main theme (Shopify.theme role "main", id 133290917985, fetched with `?preview_theme_id=` to leave the shared preview): `/blogs/news/matching-family-christmas-pajamas-guide-2026` has `<article class="article-template">`, 0 itemscope, 0 itemprop, exactly 1 BlogPosting JSON-LD, which parses. Note: one earlier fetch in the same session came back from the unpublished preview theme ("gallery-test") and still showed the old markup; it was discarded.

## 2. og:title on the cart

`snippets/meta-tags.liquid` builds og:title separately from `<title>`; for the cart it used the theme translation only for de/es/fr/cs/ro (same old list as `layout/theme.liquid`, fixed earlier today in 8e279a8). Now every non-English language uses `sections.cart.title`, exactly like `<title>`. Only the cart branch changed, so product, collection, article and home og:title are unchanged by construction.

Before/after (live): `/no/cart` og:title and twitter:title "Your Shopping Cart" -> "Handlekurven din". Product `/no/products/heart-button-mommy-and-me-cardigan-dress-sets` "Matchende cardigan og kjole med hjerteknapper til mamma og datter" before and after (main theme). Collection `/no/collections/family-sweaters` "Like familiegensere, strikkejakker og collegegensere" before; after-read came from the shared preview theme, not re-read on main (unchanged code path). Article og:title "Matching Family Christmas Pajamas 2026: Buying Guide" before and after (main).

## 3. Romanian account and accessibility strings (33 keys)

Read all 105 `accessibility.*` and `customer.*` keys of ro.json against English (STYLE_RULES_RO: polite plural). Changed 33: imperatives to polite plural (Treceți, Închideți, Vedeți, Activați, Creați-vă, Confirmați, Refuzați, Adăugați, Modificați, Setați, Actualizați, Anulați, Editați, Ștergeți, Resetați, Creați un cont), "Continuați ca vizitator" (was "oaspete"), order: "Plasată la", "Starea expedierii" (was "Starea îndeplinirii comenzii"), "Expediată la" (was "Livrat" = delivered), "Urmăriți coletul", "Taxe vamale" (was "Îndatoriri" = obligations), "Taxe"; "recenzii în total"; "Implicită". Placeholders kept; comma-below diacritics.

## Release

- Round 1: commit d7b78fd (2 theme files + 20 ro keys). 90 s later the read-only listings showed only my 2 files and my 20 ro keys; applied in separate calls (sync-theme, then sync-locales); export ab3fe5c kept everything; after 3 min `sync-locales` in sync and `sync-theme` 0 differ.
- Round 2: commit d28e292 (13 ro keys). 90 s later listing: only my 13 keys; applied; hold result below.
- Lock written and re-read after 5 s each round; released between rounds.
- Round 2 hold: export 6fdcc7f kept the 13 keys (empty diff); `sync-locales` in sync, `sync-theme` 0 differ. Lock released, work copy cleanup1 finished.
