# US Spanish qualification — September 14, 2026

**PARTIAL. No Spanish Google feed was submitted or produced.** The complete source has 238 active parents and 4,925 variants. Source and translation reconciliation is complete; localized variant entry and the existing collector behavior prevent an executable release.

| Complete variant partition | Offers |
| --- | ---: |
| Source and required Spanish translations qualified; landing unverified | 4,552 |
| Available offers with stale Spanish content | 189 |
| Available offers under the six existing parent holds | 162 |
| Unavailable variants omitted | 22 |
| Total | 4,925 |

The 4,552 potential offers span 221 parents. Fresh required fields mean present and not flagged outdated; this is not a complete linguistic-quality certification. Only the two sampled pages received the described rendered content comparison. They are an analysis manifest, not a Google TSV. The 11 stale parents have 190 variants: 189 available plus one already counted among the 22 unavailable variants. No false availability or translation freshness was introduced.

The unchanged collector completed at 18:04:07.475 UTC. Its US-market-specific Spanish translation arrays were empty for all 238 parents. A separately timestamped global Spanish supplement completed at 18:07:06.528 UTC, matched the full source manifest, and found 227 parents with fresh required content and 11 with stale fields. The original source clock is preserved in the clearly labeled derived review input.

The unchanged builder rejected this original snapshot with exit 2 and 238 `missing_or_stale_translation` errors. No TSV was written. The smallest pipeline repair is documented in [pipeline_correction_proposal.json](pipeline_correction_proposal.json): inherit global translations without discarding the real market checks, preserve exact-market override freshness, and explicitly account for translation-only exclusions. No runtime patch was applied.

Two settled Spanish product links failed exact variant preselection. The swimwear URL requested Child 2–3 years / Black / USD 17.99 but settled on an unselected Mom state and a price range. The shirt URL requested Adult 2XL / White / USD 22.99 but also left size and color unselected. Both showed the expected source price after manual option selection. Add buttons became enabled; no Add/cart/order/consent action was performed. See [buyer_readback.json](buyer_readback.json). The shared implementation cause is not yet established.

**First action:** route the two exact numeric variant URLs to the existing UX owner for a bounded fix and readback. This is first because the buyer landing context cannot be certified even with correctly assembled Spanish data. The collector fallback and explicit stale partition also remain necessary before an executable candidate.

Current Merchant source inventory at 17:57:07 UTC showed only three provided English sources: Content API 10014302986 with 0 rows, US 10727274744 with 4,741, and AU 10727245667 with 4,741. No Spanish source was present. The unsaved source wizard exposes Spanish and a separate feed label, but defaults to 31 countries and all marketing methods; an eventual release must explicitly target US and free listings. The wizard was canceled without a file, URL, continuation or save. A transient unsaved Italian selection is disclosed in the native receipt.

The inspected priority diagnostics view showed no quota issue; numerical account/MCA headroom remains unknown. The published default is not proof of this account capacity. Two shipping pagination clicks misrouted to an existing NZD editor, which was canceled untouched both times; that route was stopped. The previously qualified US delivery context is reused, not restamped. Optional returns are not a blanket language-release gate.

Shopify documents [global and market-specific translation behavior](https://shopify.dev/docs/api/admin-graphql/latest/objects/Translation). Google identifies products by [content language, feed label and offer ID](https://developers.google.com/merchant/api/guides/products/add-manage); the Spanish identity must remain distinct from English. [Published account limits](https://support.google.com/merchants/answer/16564100?hl=en-IE) do not certify current numerical headroom.

Stale Spanish content requiring repair or explicit omission:

| Shopify listing (source title) | Stale fields | Available offers |
| --- | --- | ---: |
| Yellow Beach Outfits Summer Vacation Dresses & Shor... \| DLM — 7227375714401 | stale_body_html | 20 |
| Matching Family Beach Outfits - Palm Tree Dresses & Shorts Set — 7227378892897 | stale_title | 21 |
| Tropical Beach Outfits Colorful Leaf Print Summer D... \| DLM — 7227378925665 | stale_body_html | 23 |
| Elegant Floral Off-Shoulder Dress Set Perfect for S... \| DLM — 7229026304097 | stale_body_html | 12 |
| Washed Denim Family Matching Vests + Jeans - Sleeveless Layer — 7536709664865 | stale_title | 14 |
| Green Palm Safari Family Matching Set - Dress & Shirt — 7536984359009 | stale_title | 30 |
| Scarlet Ruffle Mommy and Me Tank Top - Breezy Beach Top — 7545279217761 | stale_title, stale_body_html | 8 |
| Sunshine Stripe Family Matching Tops - Cotton Tee — 7545279512673 | stale_body_html | 14 |
| Red Heart Raglan Family Matching Tops - Cotton Tee — 7545279840353 | stale_body_html | 17 |
| Red Resort Mommy and Me Set - Tee and Skirt — 7545373130849 | stale_body_html | 10 |
| Golden Daisy Mommy & Me Matching Separates — 7546613530721 | stale_title, stale_body_html | 20 |

Validation: 491 source membership checks passed. Four existing focused tests passed for market/catalog identity, complete replacement lifecycle, malformed buyable row rejection, and foreign translation/landing requirements. The builder rejection above is expected evidence of the current blocker, not a ready-feed pass. Completion checks and frozen hashes are recorded separately.

Preserved: current US/AU submissions and clocks, all six holds, source runtime files, shared canonical controls, paid settings, translations, theme, policies, accounts, hosting and schedulers. This packet plus one additive executor checkpoint key are the only intended local changes.

Broader Canada, UK, other market/language deployment and Store Quality work remain incomplete; no free-listing approval, display, traffic, order or profit lift is claimed by this qualification.

Continuation: Continue TA07-US-SPANISH-QUALIFY-20260914-1658 from this frozen packet. Have the parent independently review it, route the exact Spanish variant-entry failures to the existing UX owner, and separately dispatch the bounded existing-pipeline correction. Do not submit, refresh English sources, replay accepted samples, or claim the manifest is uploadable.
