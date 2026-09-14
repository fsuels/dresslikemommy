# Search Console server-error resource join

**PASS — complete current source join.** Shopify resource read: September 6, 2026, **07:31:33 UTC**; locale read: **07:34:07 UTC**. Exact shop: `dresslikemommy-com.myshopify.com`, Dress Like Mommy.

All **12 original GSC URLs** joined to **11 unique resources**. Original paths, query strings and June 3/24 crawl dates are preserved in the JSON; the GSC report was last updated August 27.

- **Seven unique products are ARCHIVED**, each with null `onlineStoreUrl`.
- The remaining product, **7228788867169**, is **ACTIVE** with an Online Store URL: the cartoon pajamas appearing in both Vietnamese and Thai examples.
- Articles **559662071905** (family swimsuits) and **559700574305** (sizing guide) are both `isPublished=true`, with exact `news` blog handle **41450437**.
- Collection **353856880737**, `matching-family-vacation-outfits`, exists and its exact ID matches the documented Online Store published filter.

The collection result is **only a base-resource join** for the original `/pt/collections/matching-family-vacation-outfits.atom` request. The `.atom` URL remains intact; no product lookup, redirect, feed-response claim or silent normalization was made.

Shopify returns **21 enabled locales**, all published; primary `en`:

| Requested codes | Current exact-code result |
|---|---|
| `fi`, `hi`, `ja`, `sv` | Enabled and published |
| `vi`, `th`, `tr`, `id`, `pt` | Not returned in enabled locales |
| Related `pt-BR` | Enabled and published; `/pt` alias not verified |

This gives a current configuration mismatch for the active Vietnamese/Thai product paths and Turkish article paths. It does not establish market routing, a historical server-error cause, or justify bulk language publication. Root separately reported ten 404 responses, then a 429 verification response on the eleventh URL and stopped; the `.atom` request was not run. This subagent made no public request or retry.

Schema discovery and both query validators passed; article/collection pagination completed with zero GraphQL errors. Ten integrity assertions pass. Exact IDs, handles, titles, publication indicators, query operations and source hashes are in `gsc_server_error_resource_join.json`. No credentials, customer/order/vendor fields, browser actions or external mutations were used.

Current source publication is not indexing or purchasability proof. Next: root combines these findings with its HTTP and GSC evidence before qualifying a locale or redirect repair; archived status alone is not restoration authority. References: [Product publication indicator](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/Product), [ShopLocale](https://shopify.dev/docs/api/admin-graphql/2026-07/objects/ShopLocale). Continue through the [canonical prompt](../../../ops/prompts/paid-growth-ai-army-continuation-prompt.md).
