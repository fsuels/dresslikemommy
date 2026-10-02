# Off-site links and Pinterest: playbook for the `offsite-links` routine

Owner (2026-10-02, chat, quoting a Search Console read): "family matching outfits" has 2,658 impressions at pos 12.8 and 5 clicks; page-2 phrases need links from other sites, and holiday guides must be live early. Owner: "ceo have agents take care of this routine." On-page work is the hourly `organic-traffic-engine`; this routine owns the free off-site half: earned backlinks and organic Pinterest. No paid placements, sponsored posts, link swaps or anything that costs money (paid marketing ended 2026-09-28).

Verified 2026-10-02 against the pasted advice: the blog sitemap loads (`/sitemap_blogs_1.xml`, 89 URLs); the homepage links to the blog only once (`/blogs/news`), which is MAIN row H1; head-term de-cannibalization is already running as X1 (measure 2026-10-22).

## What the routine may do unattended (all inside `ops/organic/`)

1. **Prospect.** WebSearch for sites that publish things our guides serve: "2026 holiday gift guide for moms", "matching family Christmas pajamas roundup", "family photo outfit ideas fall 2026", "mommy and me outfit roundup", "what to wear for family photos". Keep only real editorial sites (mom, family, parenting, lifestyle, photographer-tips blogs and resource pages) that link out to shops or guides and have published in the last 12 months. Skip content farms, link-selling pages ("sponsored post", "guest post fee"), coupon sites, forums, marketplaces and anything that wants payment.
2. **Match** each prospect to ONE of our live assets that is genuinely useful to that page's readers (an existing live `/blogs/news/<handle>` guide or a collection with >=3 live products). Check it with `organic_engine.py check`.
3. **Draft** a short, honest pitch (under 110 words, no hype, no claims we cannot prove, no stock/shipping/bestseller/review/guarantee wording, no pets). Lead with the reader benefit, name the asset, give the URL, say we're happy for them to use or credit any of it.
4. **Queue Pins:** for each live article or collection in the Pin rules below, write one Pin packet.
5. **Log** every run in `OFFSITE_LOG.md`.

Files: `OUTREACH_PROSPECTS.md` (table), `OUTREACH_DRAFTS.md` (one block per prospect), `PIN_QUEUE.md` (one block per Pin), `OFFSITE_LOG.md`. The CEO loop commits them with the rest of `ops/organic/`.

## Gates (never cross unattended)

- Never send an email, DM, contact-form, comment or any message to a third party. Drafts only; status `READY_FOR_OWNER`.
- Never post, schedule or save a Pin. Pin packets only; status `READY_FOR_OWNER`. Pinterest limits: max 3 original Pins per rolling 168 h per `ops/marketing/current_marketing_state.md`; the queue may hold more, posting is metered by whoever posts.
- Store only the site's public contact-page URL or the page where it asks for tips; never personal emails, phone numbers or social handles of individuals.
- No account sign-ins, no browser. Tools: WebSearch, Read, Write, Edit under `ops/organic/` only, and the Bash shapes `date -u +%Y-%m-%dT%H:%MZ`, `mkdir -p <dir>`, `curl -s -o <file> <url>`, `/usr/bin/python3 ops/scripts/organic_engine.py check ...`.
- If the owner later grants a standing yes for sending or posting, the owner records it in `BACKLOG.md` row O5; until then nothing leaves the building.

## Prospect table format (`OUTREACH_PROSPECTS.md`)

`| # | Site | Page that fits (URL) | Why it fits | Our asset (live URL, checked) | Contact page URL | Quality (A/B) | Status |`
Status: `NEW` -> `DRAFTED` -> `READY_FOR_OWNER` -> `SENT <date>` / `REPLIED` / `LINKED <url>` / `DROPPED <why>`. Keep at most 40 rows open; A-quality only (real audience, recent posts, editorial links). One pitch per site, never a second without a reply.

## Pin rules (`PIN_QUEUE.md`)

One Pin per live article or collection with >=3 live products, newest seasonal first (Christmas, Thanksgiving, NYE, then evergreen). Each packet: destination URL (with `utm_source=pinterest&utm_medium=organic&utm_campaign=<handle>`), image URL (a real product photo from `/collections/<handle>/products.json?limit=5`, fetched with `curl -s -o` and confirmed to load), Pin title (<=100 chars, query first, honest), description (<=500 chars, 2-3 natural keywords, no hashtags spam, no banned claims), board name (an existing board; if unsure write `OWNER_PICK`), status `READY_FOR_OWNER`. Do not queue a handle that already has a packet.

## Measurement

The window is the same as X1: 2026-10-22. Backlink success = referring pages that link to the site (count LINKED rows with the URL), and Pinterest outbound clicks from `TRAFFIC_PULSE.md`/Search Console Mondays. Kill a prospect class (e.g. gift-guide blogs) if 15 drafted pitches over 3 weeks produce 0 replies; change the angle, not the volume.

## Lesson 2026-10-02 (first run froze)

The first run called `python3 -c` to parse product JSON and froze on an unanswered permission prompt with nothing saved. Rules: no python/jq/grep/pipes; read JSON with Read (fetch `?limit=2`); write results to the tracking files after each step.
