# Organic Traffic Engine — backlog

Rules: `ORGANIC_ENGINE.md`. Tags: `ENGINE` = the hourly agent may do it; `MAIN` = needs a CEO main session (theme/git/other surfaces); `OWNER` = needs the owner's yes; `HOLD` = another session owns it, skip. Status: `OPEN`, `DONE <date> <url>`, `BLOCKED <reason>`.

Existing live guides that already cover a topic (do not duplicate; link to them instead): `matching-family-christmas-pajamas-guide-2026`, `matching-family-christmas-sweaters-guide-2026`, `family-christmas-photo-outfits-2026`, `holiday-family-matching-outfits-complete-guide`, `christmas-matching-family-pajamas`, `best-matching-outfits-for-thanksgiving-dinner`, `thanksgiving-family-matching-outfit-ideas`, `mommy-and-me-thanksgiving-style-guide`, `halloween-family-matching-costume-ideas`, `matching-outfit-sizing-guide-right-fit-for-everyone`, `what-to-wear-for-family-photos-matching-outfit-ideas` (full list: inventory `articles`).

## BUILD queue (season clock first)

| # | Tag | Status | Target query cluster | New handle (suggested) | Link to collections |
|---|---|---|---|---|---|
| 1 | MAIN | BLOCKED 2026-09-29: 0 active Christmas dress products (catalog gap, not a content gap; sourcing first) | mommy and me christmas dresses | — | — |
| 2 | ENGINE | OPEN | baby's first christmas matching family outfits / pajamas with baby | `babys-first-christmas-matching-family-outfits` | christmas-pajamas, family-pajamas, matching-family-christmas-outfits, family-sweaters |
| 3 | ENGINE | DONE 2026-09-29 https://www.dresslikemommy.com/blogs/news/matching-couples-christmas-pajamas-and-sweaters (hero image is a family sweatshirt from `couples`; swap for a couple photo if one appears) | matching couples christmas pajamas / sweaters | `matching-couples-christmas-pajamas-and-sweaters` | couples, christmas-pajamas, christmas-sweaters, pajamas |
| 4 | ENGINE | OPEN | daddy and me christmas outfits | `daddy-and-me-christmas-outfits` | daddy-me, daddy-me-shirts, christmas-tops, christmas-pajamas |
| 5 | ENGINE | OPEN | matching family christmas shirts / tees for photos and parties | `matching-family-christmas-shirts` | christmas-tops, christmas-sweaters, family-tops, matching-family-christmas-outfits |
| 6 | ENGINE | OPEN | maternity christmas photo outfits with the family | `maternity-christmas-family-photo-outfits` | maternity, matching-family-christmas-outfits, family-photo-outfits, christmas-pajamas |
| 7 | ENGINE | OPEN | family christmas card photo ideas (poses, settings, color palettes) — must differ from the 2026 photo-outfits guide: focus on card concepts, link to it | `family-christmas-card-photo-ideas` | family-photo-outfits, matching-family-christmas-outfits, christmas-sweaters, christmas-pajamas |
| 8 | ENGINE | OPEN | matching family outfits for a winter cruise / holiday travel | `matching-family-cruise-outfits` | matching-family-vacation-outfits, matching-hawaiian-outfits, swimsuits, family-sets |
| 9 | ENGINE | OPEN | new year's eve family and couples matching outfits | `new-years-eve-matching-family-outfits` | matching-family-christmas-outfits, couples, dresses, family-tops |
| 10 | ENGINE | OPEN | mother daughter matching dresses for weddings, parties and photos (evergreen) | `mother-daughter-matching-dresses-guide` | mother-daughter-matching-dresses, dresses, maxi-dresses, formal-dresses (check ≥3 products) |
| 11 | ENGINE | OPEN | matching family hawaiian shirts and dresses | `matching-family-hawaiian-outfits` | matching-hawaiian-outfits, matching-family-vacation-outfits, daddy-me-shirts, sundresses |
| 12 | ENGINE | OPEN | valentine's day mommy and me / daddy-daughter outfits (publish by early Dec; one exists — refresh angle: daddy-daughter dance) | `daddy-daughter-dance-matching-outfits` | daddy-me, dresses, mother-daughter-matching-dresses, couples |

## FIX queue

| # | Tag | Status | Item |
|---|---|---|---|
| F0 | ENGINE | OPEN (5 of 63 repaired 2026-09-29: best-fall-colors, october-family-style, transitional-weather, spring-break, late-summer; 58 left, rerun `article-links`) | **Top priority FIX.** Repair 63 live articles: 128 dead product links, 9 dead collection links (`family-matching`, `headbands`), unsupported claims in 53 ("one of our bestsellers", "happiness guarantee", "free shipping on all orders", "customer reviews", Disney). 5 per run via `article-links` + `article-body` (see playbook). |
| F1 | ENGINE | OPEN | SEO title/description for live articles missing them (65 of 70 have no custom title tag; start with Christmas/Thanksgiving/winter ones). Query-first title ≤65, description 110–160. |
| F2 | ENGINE | OPEN | Collection SEO meta review for non-theme-owned collections with products: christmas-sweaters, christmas-tops, matching-family-christmas-outfits, family-photo-outfits, matching-family-vacation-outfits, mother-daughter-matching-dresses, matching-hawaiian-outfits, maternity, thanksgiving-family-outfits. Only change weak/missing/templated meta. |
| F3 | ENGINE | OPEN | Dead-URL recovery: take 404 paths from the latest GSC 404 audit packet (`dresslikemommy-growth-2026/02_AUDIT_PACKETS/*/` files from `build_gsc_404_audit.py`), redirect each to the closest live collection (≤10 per run). |

## MAIN / OWNER items

| # | Tag | Status | Item |
|---|---|---|---|
| M1 | MAIN | OPEN | Theme: link the newest seasonal guides from the Christmas and Thanksgiving collection pages (theme-owned copy). |
| M2 | MAIN | OPEN | Review wording risk: collection `best-sellers` and article `black-friday-deals-top-matching-family-outfits` (bestseller/deal claims need evidence). |
| O1 | OWNER | OPEN | Search Console: submit sitemap + request indexing for each new engine article (owner's Chrome GSC login). Also export 16 months of GSC performance for the SEO diagnosis. |
| O2 | OWNER | OPEN | Bing Webmaster Tools: import the site from Search Console (free Bing/Copilot/DuckDuckGo traffic). |
| O3 | OWNER | OPEN | Organic Pinterest: approve the engine preparing one Pin per new article (image + title + link) for posting. |
