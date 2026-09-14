# U.S. Merchant source recovery — September 14, 2026

**The U.S. source connection is repaired and Google received the fresh file. The exact removal count remains unverified. The international setup is still partially complete.**

| Check | Verified result |
|---|---|
| Existing target | Merchant 513542500; U.S. source 10727274744; English/USD; Free listings only |
| Fresh Shopify scan | 13:16:10.466 UTC; 238 active products and 4,925 variants, including 4,903 available variants |
| Submitted file | 4,741 offers from 232 products; 22 unavailable variants omitted; six existing product holds exclude another 162 offers |
| Live host | Published at 13:33:17.275931 UTC; exact pointer and full file verified; Worker metadata unchanged |
| Google history | September 14, 9:34:09 AM New York / 13:34:09 UTC; 4,741 updated, zero new; all attributes recognized; no file issues |
| Protected offers | Five Adult 2XL variants at $22.99 and the pilot at $17.99; all six approved, in stock, and enabled for U.S. Free listings |
| Remaining discrepancy | The independently reopened source still showed 4,761 products at 13:42:26 UTC; removal of the 20 omitted offers is not yet verified |

The unchanged lifecycle published one new immutable file and one pointer after the independent review passed all 26 checks. One normal Google Update was requested. The previous connection failure is absent from both the successful receiving result and the independently reopened source page.

The file omits 20 offers from two products absent from the complete current Shopify active-product scan. It adds no offers and changes no retained feed fields. Every retained row matches the previously reviewed data, and all prices match the fresh Shopify source. The precise archive, draft, or deletion cause was not inferred.

Google’s individual product pages still displayed a last-update age of 33 hours. The later checks verify the displayed prices and eligibility; they do not establish that every record was rewritten at 13:34. Full Google file-byte equality, exact removal of the 20 offers, and native absence of all 162 held offers remain unproved.

Google documents that [removals can take 24–48 hours to disappear from ads and free listings](https://support.google.com/merchants/answer/14996874?hl=en). That general timing does not prove this specific count discrepancy will reconcile.

The source needs another genuine refresh before **September 16 at 13:16:10.466 UTC**, under the unchanged 48-hour host safeguard. Google’s existing midnight New York schedule next falls on September 15 at 04:00 UTC. Future execution has not been observed. No scheduler, Worker, security setting, credential, Shopify product, theme, return policy, or other country was changed. The expired prior pointer is preserved as evidence and must not be restamped or automatically restored.

Next: use the existing parent follow-up to reconcile the count and 20 omitted IDs without another Update, and refresh the source before its deadline. Parent owns shared canonical integration. Australia, Canada, the UK, other languages, return coverage, and Store Quality retain their separate unfinished work.

Evidence: `host_promotion_receipt.json`, `native_google_receiving_result.json`, `native_protected_after_readback.json`, `release_execution_handoff.json`, the candidate/source-delta receipts, and existing run `20260914T131200Z-us-freshness`.

Continuation: Resume TA07 U.S. source recovery from this exact release. Preserve the successful 13:34:09 UTC fetch and do not repeat promotion or Update. Verify removal/count reconciliation and source freshness, then continue the qualified remaining markets.
