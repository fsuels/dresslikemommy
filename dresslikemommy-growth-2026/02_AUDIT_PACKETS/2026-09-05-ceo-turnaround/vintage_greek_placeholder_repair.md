Confidence: H. The two fragments are recoverable HTML, so a minimal Greek-only proposal is ready for root review.

For active product **7533081133153**, locale `el`, key `body_html`, replace exactly once:

| Visible fragment | Restoration | Current English source position |
|---|---|---|
| `QZ012QZ0` | `</li>` | End of “Vintage cottage floral print” bullet; protected HTML index12 |
| `QZXTOKEN0001` | `</li>` | End of “Classic design details” bullet; protected HTML index16 |

The current English body returned by the product tool and translation readback is identical. Its SHA256 equals Shopify source digest `625065cab57e8cf33b60ac675345cd0df0cb026fb1bb43a928d31f36ed6f2633` and exactly matches the English key in `ops/content/shopify-product-translation-live-cache.json`; that cache's Greek value exactly matches the live Greek body. The existing protection routine numbers HTML tags; those positions map to `QZXTOKEN00012QXZ` and `QZXTOKEN00016QXZ`, both `</li>`. The Greek sentences contain their corresponding facts but end in malformed fragments where the closing tags belong. Historical transport corruption itself was not audited.

The proposal changes **two literal fragments only**, restoring the first list from six starts/four closures to six/six. All remaining Greek text is identical. The one size table and all **11 size rows**, measurements, existing materials/fulfillment copy, later paragraphs, English source, title/meta, options, variants and other locales are preserved. No additional product fact or wording is supplied.

Fresh readback captured **2026-09-06 03:07:53 UTC**, Greek `outdated=false`. Before: **5789chars**, SHA256 `e6f515a8e667588357d848a31e4391beabee5d029e571d0b116781010799467b`. Proposed after: **5779chars**, SHA256 `481ef235d1e403af18be84f6ad4c58d2e4081b7b5e3d463cd009316f09917498`. These Greek hashes are distinct from the Shopify English-source digest. [JSON evidence and exact proposed body](vintage_greek_placeholder_repair.json) include contextual replacements, cache/source proof and all passed checks.

Validation: GraphQL schema/operation PASS; exact cache match,17 local scope/content checks, preserved table hash, balanced proposed HTML and zero QZ fragments PASS. The current token detector misses both malformed shapes; no engine/cache edit was made.

Only these two local evidence files were created. No external write or browser action occurred. Rendered after-state is NOT RUN: the change is unapplied and the parent reports the Mac/browser locked. Existing English controls/table labels and broader Greek quality issues remain outside scope; this is not full localized-PDP certification.

Next: root reviews, binds to a fresh source digest and Greek before hash, applies only the two restorations if permitted, and verifies Admin plus the [Greek PDP](https://www.dresslikemommy.com/el/products/vintage-cottage-floral-mommy-and-me-pajama-set) after-state when browsing is available. Continuation: “Review and apply only the two source-backed Greek closing-tag restorations.”
