# Structured data (JSON-LD) audit and fix - 2026-11-27

Unit: structured-data. Source read from origin/main (ca1ba5d, then d5a1da0 work copy). Live checks via the app browser pane (geo: ES, so the storefront presents EUR), one page at a time, no 429/403.

## Emitters

| File | Emits | Where |
|---|---|---|
| snippets/jsonld-seo.liquid (from layout/theme.liquid) | Organization (home only), WebSite+SearchAction (all), BreadcrumbList (collection, product), Product (product), calls collection-schema | head |
| snippets/collection-schema.liquid | CollectionPage + ItemList (24 items) | collection |
| sections/main-collection-seo.liquid, main-collection-banner.liquid, snippets/faq-schema-from-html.liquid | FAQPage (when copy has question headings) | collection |
| snippets/article-enhanced-schema.liquid | BreadcrumbList + BlogPosting | article |
| sections/main-article.liquid | second Article block (removed, see below) | article |
| snippets/product-schema-extra, product-faq-schema, article-faq-schema | not rendered anywhere | - |

## Per page type

### Product (live: /products/golden-daisy-mommy-and-me-set, /es/ and /de/ routes)
- Emitted: Product with name, description, url, image[] (absolute ImageObject URLs with captions), sku, brand, category, additionalProperty; one Offer (selected/first available variant): price, priceCurrency, availability InStock/OutOfStock from variant.available, url with ?variant=, itemCondition New, shippingDetails (free rate, destination = visitor country, deliveryTime handling 1-5 + transit from dlm-transit-map only for mapped countries), hasMerchantReturnPolicy (30 days, by mail, customer-paid return fees, link to locale refund policy). BreadcrumbList Home > collection > product.
- Checks: valid JSON, 1 Product block, no empty blocks; priceCurrency EUR = visible "€30,95"; offer URL keeps the locale prefix (/es/, /de/); images absolute https; ES transit 14-21 matches the map.
- Defects: none clear. Not changed.
- Notes: single Offer for the selected variant (not ProductGroup/hasVariant, not AggregateOffer). Valid for Google; ProductGroup would be an enhancement, not a fix. aggregateRating/review code only fires when real review metafields exist; none live. Breadcrumb "Home" item on locale routes points to the root domain, not /es/ (cosmetic).

### Collection (live: /collections/matching-family-vacation-outfits)
- Emitted: BreadcrumbList (2), CollectionPage + ItemList (24 product URLs, absolute), FAQPage when applicable.
- Defects: none clear. Not changed. Possible two FAQPage blocks if both the banner description and the SEO section contain question headings (FAQ rich results are limited to gov/health sites now, so no visibility cost).

### Home
- Emitted: Organization (logo absolute, contact, sameAs), WebSite + SearchAction. Not live-checked (4-page limit); source shows no defect.

### Blog article (live: /blogs/news/family-photo-color-palettes-by-season)
- Before: two article entities for one page. BlogPosting (correct @id, but image = Admin image not shown on the page) plus an Article block whose mainEntityOfPage @id was the home page (page.url is empty on article templates), whose dates were local time with a "Z" (UTC) suffix (4-5 h wrong), and which repeated the full article body. BlogPosting also hard-coded inLanguage "en-US" on translated routes.
- Fix: removed the duplicate Article block (sections/main-article.liquid); BlogPosting now uses the same image rule as the visible hero (news blog -> article-featured-image-fallback) and request.locale.iso_code for inLanguage (snippets/article-enhanced-schema.liquid).
- After (live): WebSite, BreadcrumbList, one BlogPosting; @id = article URL; image = the hero image shown on the page; inLanguage "en"; date with real offset (-0400).

## Release
- Commit 154910c "Keep one Article entity per blog post in structured data" (pushed via ceo_worktree; Shopify write-back 6a252f0 kept it). sync-theme --apply: 2 applied, verified; re-run 0 differ. THEME_LOCK taken 06:34Z after experto-seo released, deleted after confirming main. Work copy finished.
- Rollback: `git revert 154910c` in a ceo_worktree work copy, commit, sync-theme --apply.

## Owner decisions (truth-dependent, not changed)
1. Return policy in Product schema (30 days from delivery, return by mail, customer pays non-defective return shipping; Final Sale/gift cards not returnable) was already live. The return-policy page states 30 days from delivery (delivery-statements-2026-11-26.md); the fee and method terms were not re-read word for word in this unit. Confirm they match the published refund policy, or remove the block.
2. News-blog hero images come from a rotating fallback by article id for unmapped handles (this palette article shows a holiday image). The schema now mirrors what the page shows; choosing a topic-correct hero is a content decision.

## Follow-up: schema vs published policies (read-only, 2026-11-27 ~06:45Z)

Sources: live /policies/refund-policy and /policies/shipping-policy (both "Last updated: September 27, 2026"), one request each; theme snippets/jsonld-seo.liquid and snippets/dlm-transit-map.liquid on main 6a252f0.

| Field | Schema | Published policy | Match |
|---|---|---|---|
| returnPolicyCategory | MerchantReturnFiniteReturnWindow | "request a return or exchange within 30 days of delivery" | yes |
| merchantReturnDays | 30 | 30 days of delivery | yes |
| returnMethod | ReturnByMail | authorized return shipped with a tracked service to the address provided | yes |
| returnFees | ReturnFeesCustomerResponsibility | customer pays return shipping for change of mind / size exchange; store pays only for its error or damaged/defective | yes (schema does not promise free returns) |
| applicableCountry | visitor country (ES, US, ...) | policy applies to all orders; EU/UK 14-day withdrawal is extra legal right, not a shorter window | yes |
| Not returnable | MerchantReturnNotPermitted for gift cards and "final sale" tag | Final Sale items and gift cards non-returnable | yes |
| Swimwear/intimates with hygiene seal removed | still 30-day window | not returnable once seal removed or worn | conditional exclusion; schema cannot express it per condition, does not promise more for normal returns. No change |
| merchantReturnLink | /policies/refund-policy (locale prefix) | same page | yes |
| shippingRate | 0, visitor currency | "Standard shipping is included in product prices" | yes |
| handlingTime | 1-5 days (+ made-to-order days) | "We ship every order within 5 business days" | yes |
| transitTime | from dlm-transit-map (US 7-14, CA 14-24, GB 7-14, DE/FR/IT/ES/CZ/PL 14-21, NL/SE 12-17); none for other countries | no per-country transit; "estimated delivery is shown on each product page; estimates are not guarantees" | yes (no contradiction; same source as the PDP estimate) |
| shippingDestination | visitor country | 64 countries enabled at checkout | partial: schema would also emit free shipping for a visitor from a non-shippable country. Low impact (Google crawls mainly from US); noted, not changed |

Result: nothing in the schema promises more than the published policies (no extra days, no free returns, no faster shipping). No change, no release.

Owner/policy notes (not schema defects): shipping policy still says "most orders ship in about 3" and mentions "any express upgrade"; refund policy mentions "paid express upgrades". Both were already flagged in delivery-statements-2026-11-26.md patterns 4-5.
