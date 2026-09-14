# Return-label mechanism — 11 September 2026

Confidence: H for documentation; **UNKNOWN** for direct Shopify publisher mapping and account-specific availability. Read-only; sources retrieved 11 September 2026.

No reviewed official source establishes a Shopify Google & YouTube input, supported metafield namespace/key, or automatic Shopify return-rule → `return_policy_label` mapping. Google's Shopify-specific guide documents configuring policies in both systems, without documenting that mapping. Generic Shopify metafield capability is not evidence that this publisher consumes a field. [Shopify-specific return setup](https://support.google.com/merchants/answer/14232691?hl=en), [app product-data instructions](https://support.google.com/merchants/answer/13693394?hl=en)

The required **Google output attribute** is `return_policy_label`, matching the saved exception label. Without it, the standard policy applies. Creating the exception alone does not classify products. [Attribute specification](https://support.google.com/merchants/answer/9445425?hl=en), [exception assignment](https://support.google.com/merchants/answer/14011730?hl=en)

The smallest documented alternative preserving the publisher is a **conditional Merchant attribute rule on its existing primary source**. Documented path: enable **Advanced data source management**, then **Data sources → Product sources → existing source → Attribute rules → correct feed label → Add attribute rule**. If the target dropdown exposes `return_policy_label`, set it to the actual saved exception label using reliable inbound classification conditions. Save as draft and test before applying. Google documents conditions, static values and reapplication on each upload. Actual availability on source **10014302986 / Merchant 513542500** remains unverified. [Attribute-rule instructions](https://support.google.com/merchants/answer/14994083?hl=en)

This becomes usable only after readback proves:

- Product data exists and the rule target is available on this source.
- Existing inbound fields unambiguously identify swimwear, intimates, **explicitly marked Final Sale**, and gift cards where present. Do not infer all discounted items are Final Sale or assume Shopify tags are transmitted.
- Every affected variant receives the intended label; ordinary products retain the correct default. A product leaving an exception group loses that exception on reprocessing. Test additions, classification changes and primary-source removals; lifecycle success is currently unverified.

Rules are source/feed-label scoped. Google's Shopify guide warns that newly split country sources do **not** inherit existing rules automatically, so this alone does not guarantee future-country coverage. [Shopify source changes](https://support.google.com/merchants/answer/13693394?hl=en)

**Next:** inspect the existing source's rule target and raw input fields. If either is unavailable, no usable automatic mechanism is established within this scope. No second publisher, supplemental source, reset or invented metafield is proposed.
