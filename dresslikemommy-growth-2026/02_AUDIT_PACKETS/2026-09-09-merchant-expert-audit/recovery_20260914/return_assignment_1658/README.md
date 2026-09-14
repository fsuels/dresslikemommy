# U.S. and Australia return-policy assignment prerequisite

The local mapping is complete for the exact two submitted September 14 files: **4,741 offers per country, 9,482 country-offer rows**. The effective Google policy/exception assignment is **incomplete**. No live policy, label, feed, product, theme, account or scheduler change was made.

| Country | Source | Submitted | Source-backed nondefective exclusions | Ordinary eligibility unknown | Ordinary eligibility confirmed |
| --- | --- | ---: | ---: | ---: | ---: |
| US | 10727274744 | 4,741 | 700 | 4,041 | 0 |
| AU | 10727245667 | 4,741 | 700 | 4,041 | 0 |

The 700 exclusions in each country belong to 46 swimwear parents. They describe source-backed ordinary/nondefective exclusions; they do not deny the separately stated defective-item remedy. The remaining 4,041 are UNKNOWN, because absence of a classifier match or feed label is not affirmative return eligibility. The Terms and Refund Policy/Page still disagree about sale/personalized items and postage exceptions.

## Evidence and limits

- `submitted_offer_return_mapping.csv` joins each current manifest/TSV offer to the same country's complete frozen snapshot and filtered return cohort.
- `parent_return_cohorts.csv` records all 464 submitted country-parent rows.
- `not_submitted_source_partition.csv` reconciles all 368 source rows outside the submitted files: 324 country-offer rows under the six existing holds, plus 44 unavailable country-variant rows. Holds remain 162 available offers per country. These are separate from return exclusions.
- `capability_receipt.json` records the ordinary policy-table and two expanded representative detail reads. Additional, raw-source, and site-found disclosures were opened. Neither representative exposes an effective policy; site-found regions are empty. The table shows the same sole Standard for Austria policy and Products “-”. The prior same-day AT-only country editor result is reused, not restamped.
- The actual 18-column TSV files contain neither `return_policy_label` nor `returns`. The generator's `returnPolicyLabelsConfirmed=true` is a compatibility flag when emission is disabled, not a Merchant assignment receipt.
- All 9,482 effective Google assignments remain UNKNOWN. Two offers were inspected for UI capability, and 9,480 were not individually inspected. No complete effective-assignment export was obtained; no claim is made that export is currently disabled.
- No receipt, count, price sample or 20-omission check was repeated. No full Shopify refresh was run. Source clocks remain US 13:16:10.466 UTC and AU 15:03:55.842 UTC on September 14.

## Method and validation

The analysis parsed the current TSV files with a tab-aware CSV reader; verified SHA256, exact manifest ID sets, country prefixes, parent grouping and source clocks; joined exact product/variant IDs; and partitioned each complete 4,925-variant snapshot into submitted, unavailable and existing hold membership. It independently recomputed the existing gift-card/product-type/taxonomy/exact-tag classifier and compared all 464 submitted country-parent cohorts against the frozen diagnostics. All 9,482 submitted offers were checked against ACTIVE parents and available source variants. No source builder, worker or lifecycle refresh was invoked.

Recorded validation: **9,983 checks passed**: 9,482 offer-source membership checks, 464 parent classifier comparisons and 37 aggregate checks. This is local evidence validation, not an independent Merchant assignment certification.

Frozen contextual pricing contains price only, with compare-at price absent for all 4,925 variants per country. No literal sale/final-sale/personalized keyword match was found in the collected product title, description, product type or tags. This absence cannot establish policy membership. Four parents have custom wording; custom fit/DIY wording is not equivalent to personalization, and Mother 3XL custom-tailored wording on product7537001431137 requires a precise definition.

Google documents [return-policy labels](https://support.google.com/merchants/answer/9445425?hl=en), [default fallback](https://support.google.com/merchants/answer/15092880?hl=en), [account policies and website-derived return data](https://support.google.com/merchants/answer/14011730?hl=en), and [offer-level returns overrides](https://support.google.com/merchants/answer/17081382?hl=en). Default fallback alone does not prove a suitable country policy or eligible product.

## Exact next step

Resolve the sale/personalized exclusion and postage/defective-remedy conflict between Terms14695813 and Refund14695685/Page161929989 as one policy-truth decision. It goes first because creating a country default or a blanket no-returns exception before that could misstate customer eligibility. `truth_gate_and_repair_packet.json` names the shared facts, exact conflicts and conditional setup path without choosing or rewriting the policy.

Capability inspection is COMPLETE WITH LIMITS; local submitted-source mapping is COMPLETE; effective Google assignment and broader all-market/Store Quality work remain PARTIAL. Parent independent review is pending. Existing Austria policy and blank optional refund-processing days remain unchanged.

Continuation prompt: Continue TA07-RETURN-ASSIGNMENT-20260914-1658 from this packet. Reuse current 4,741-row source files and the existing sole Merchant owner. Resolve only the documented policy-truth and supported effective-assignment gaps before any separately authorized repair; do not repeat completed releases, counts or omitted-ID checks.
