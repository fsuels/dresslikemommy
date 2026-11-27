# Google title and description audit, active products (Experto SEO, 2026-11-26)

Scope: 328 active products, Admin API only. Fields: SEO title (English), meta_description (English + 20 languages).

## Measured before any change

| Check | SEO title (EN) | SEO description (EN) |
| --- | --- | --- |
| Empty | 0 | 0 |
| Duplicate | 0 | 0 |
| Too long (>60 / >160) | 86 (85 only because of the "\| Dress Like Mommy" suffix; 1 long without it) | 33 |
| Short (<90) | n/a | 0 |
| Cut off | n/a | 0 |
| popular / best seller / premium / perfect fit / quick-dry | 0 | 0 |
| Fabric-feel words | 1 (colour name "Soft Teal") | soft 31, lightweight 2, warm 2, stretch 1, cozy 1 (includes colour names) |

"Starts with what the product is": 229 titles open with a design name ("Santa Tree Topper Family Sweaters") instead of audience + product. This is the house style; only seasonal Christmas titles were rewritten now.

Translations of meta_description: none missing, none outdated. Over 160 characters (18 languages, ja and ko none): 1,224 rows
(el 76, da 51, no 53, nl 72, he 29, it 81, cs 67, ro 76, pl 89, de 75, fr 75, es 85, pt-BR 76, sv 58, fi 86, ru 78, ar 34, hi 63).
Literal "mom and I" calques in descriptions: es 22, no 22, nl 22, pl 23, plus one each in ro, fr, pt-BR, fi, ja, ko, hi. One pt-BR row was partly in English.

## Fixed

- Christmas first: English SEO titles of Santa/reindeer sweaters, Christmas pajamas and the Santa sweatshirt now open with "Matching Family Christmas ...".
- Descriptions over 160 characters shortened by whole trailing sentences (40 rows rewritten by hand).
- Fabric-feel words removed from descriptions (colour and design names kept).
- Calques replaced with natural phrases (mother and daughter).
- Before-state and new values per product: `ops/organic/receipts/2026-11-26/seo-meta-audit/<handle>.json`.

## Not changed

- meta_title in the 20 other languages (a prepared batch waits for the owner). The retitled English products now show their old translated meta_title as "outdated" in Shopify; the old text keeps being served.
- Design-name-first titles outside Christmas, and the suffix length: both can wait for Search Console data per product.

## Result

Applied through the Admin API on 161 products, 0 userErrors, full readback of 328:

- 23 English SEO titles rewritten; 63 English descriptions and about 1,860 translated rows updated.
- English descriptions: 0 over 160, 0 under 90; translations over 160: 0; meta_description outdated: 0.
- "soft" left in one English description, as the colour name "Soft Teal" ("warm yellow" also stays as a colour).
- Titles over 60 characters went from 86 to 109: the new Christmas titles plus the brand suffix pass 60; without the suffix only one is long.
- meta_title translations shown as outdated: 0 before, 460 after (the 460 new ones belong to the retitled products).
- Claim scan over the 161 touched products, all locales: 92 findings in 19 products before and after, identical (old glued-letter defects in body text), nothing new.
- Live spot check (5 public reads, en/es/de/pl): new descriptions served; an outdated translated title (es, Santa Tree Topper) is still served unchanged. The es lamb pajamas page still shows the old translated title with "mamá y yo" (meta_title, out of scope).

## Follow-up (same day)

meta_title registered in 20 languages for the 23 retitled products: 460 rows, 0 errors, 0 outdated across all 328; claim scan on those 23: 0 findings. 203 rows are 60 characters or fewer; the rest pass 60 with the brand suffix (max 85). Before-state: `meta-title-before.json`; ownership list: `meta-title-owned-by-seo.json` (both in the receipts folder). This supersedes the meta_title line under "Not changed" for these 23.

## Correction after Quality V31

The sentence-trim rule had removed made-to-order notes and size ranges. Restored in 467 rows (461 + 6): maternity gowns carry translated product title plus the original made-to-order/size sentence; other rows keep their size sentence; the floral smocked sundress lists the 7 variant colours (Pink added; lists dropped for length keep the count). Readback of 328: 0 over 160, 0 outdated meta_title/meta_description, 0 size ranges lost against the original. Before-state: `fix-v31/` and `fix-v31b/` in the receipts folder.

Rule for any future shortening: never remove lead time, made-to-order, sold-per-piece or size information; verify against the original.
