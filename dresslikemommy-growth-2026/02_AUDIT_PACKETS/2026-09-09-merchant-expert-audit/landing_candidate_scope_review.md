# Independent landing candidate scope review

2026-09-09. Confidence: H for scope, hashes and policy grounding; M for rendered behavior pending preview. `DID_NOT_BUILD_OR_EXECUTE=true`. **PASS_WITH_GATES for draft upload only. Public release remains HOLD.** This reviewer changed no theme/product/account data.

## Frozen scope and rollback

Reviewed **revision 3**, 40 files, target unpublished clone `137881223265`, based on MAIN `133290917985`.

- `candidate_files.json` SHA-256: `1ac332a2a99ce5ae66dc9f0485f476631457acd52b594b73134f086c433d8a6b`.
- `candidate.patch` SHA-256: `fce6e3fcd3af1bc53d803911be339f425219352296e33242e9487f9a9f09b2e1`.

Independently checked all 40 payload bodies against disk, candidate SHA-256s, baseline MD5s, the changed-file set and uniqueness: zero differences. The saved root readback in `theme_staging_before.json` binds MAIN's complete 525-file manifest at 18:46:51 UTC; every proposed rollback file matches that manifest's checksum. Thirty-nine original bodies also match their saved source records byte-for-byte; the active JS original matches the full MAIN manifest's MD5 and recorded size. Root reports the separate 525-file clone matched MAIN before uploads; this reviewer did not repeat that API read.

Only five runtime/Liquid files, 21 published locale files and 14 inactive locale files are changed. Config, layout, unrelated assets and settings are outside the payload. The inactive locales receive only the two newly required return keys; they are not activated or certified fully corrected. Their existing broader return copy needs review before any future locale activation.

## Copy and policy grounding: PASS

The public web fetch was unavailable. A schema-discovered, validated Shopify read instead verified Shop15571635's **Refund Policy14695685 at 18:56:45 UTC**. The policy supports requests within 30 days of delivery, unworn/unwashed condition, original packaging/tags, swimwear/intimate/Final Sale/gift-card exclusions, customer-paid return shipping except damaged/defective arrivals, and contacting support within seven days of delivery with photos. [Published refund policy](https://www.dresslikemommy.com/policies/refund-policy)

The six published-locale return values match `return_copy.json` exactly. Qualified eligible-item wording removes the unconditional item-level return promise; exceptions, defect guidance and the full-policy link remain. It adds no guaranteed refund, free-return or delivery promise. The summary is not an exhaustive replacement for the full policy, including packaging requirements.

Independent dictionary comparison confirms **98 additions, zero changed/deleted prior values**, including both preserved Spanish selector strings. Existing fallback behavior remains. The new prompts describe selecting and adding the current family-member item. Bootstrap quantity remains one selected purchasable variant, rather than a whole family bundle. Preview must keep that sale unit clear; “piece” must not be interpreted as a claim that a multi-garment swimsuit variant contains only one physical garment.

## Preview and public-release gates

Revision 2's literal HTML-entity price issue was amended in revision 3. The saved validation reports cover 40 files without diagnostics and 18 passing synthetic DOM regressions. I inspected the corrected entity-decoding path and did not repeat another reviewer's runtime tests. These results do not establish browser, cart or checkout acceptance.

Before draft upload, root must confirm the exact target remains unpublished and unchanged against the recorded baseline. Upload only the frozen 40-file payload; read back every written asset. Any partial failure requires inspecting actual changes before retry. Rollback uses only the affected original files and must preserve later unrelated edits.

Before public release, test desktop/mobile EN/ES plus another published locale: adult/child explicit links, generic/invalid/unavailable selections, subsequent option changes, localized prices, image, cart variant/quantity, and return summary/modal/policy consistency. **The inherited 12–16-day delivery-date display lacks verified fulfillment support and blocks public-readiness certification.** Root is preparing its removal; any amendment requires a new freeze and scoped review.

The isolated clone must not overwrite the existing consent/SEO/cart drafts. Merge approved deltas against the common MAIN baseline, preserve independent changes, and verify the integrated candidate before any eventual release. Draft preparation is within current nonspend correction authority. This review does not authorize MAIN changes or bypass the connector's publication restrictions; it does not prove zero indirect paid effects.

## Audit report and next action

The updated main report correctly treats current Merchant counts as unknown, the old source-zero as history, Google-app feedback as unbound to Merchant513, and 36/65 table matches as support rather than eligibility. Prefer “same existing images” over “unchanged images” to avoid implying byte identity after reencoding. No Merchant approval, all-market coverage or profit claim is supported.

**Next:** root may stage this exact revision on the verified unpublished clone for preview; include the reviewed delivery amendment before public-release acceptance. Continuation: “Verify the isolated draft, preserve other approved drafts, and re-review any changed frozen payload before release.”
