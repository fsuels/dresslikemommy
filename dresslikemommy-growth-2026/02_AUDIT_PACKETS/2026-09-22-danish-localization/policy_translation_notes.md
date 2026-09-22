# Danish policy translation notes

Status: CANDIDATE_NOT_APPLIED. Prepared as faithful translations of the exact five `ShopPolicy` body sources in `before_policies.json`. No external state, canonical files, themes, routes, Git refs, or source English policy text were changed by this subtask. Root owns independent review, authority/drift checks, any supported translation API writes, destination readback, and canonical integration.

## Coverage and inverse

| Resource suffix | Policy | Existing da body | Inverse |
| --- | --- | --- | --- |
| 14695685 | Refund/returns | absent | remove da body |
| 14695749 | Privacy | absent | remove da body |
| 14695813 | Terms of service | present, English | restore exact before value |
| 29845782625 | Shipping | present, English | restore exact before value |
| 31171805281 | Contact information | absent | remove da body |

`policy_translation_plan.json` uses the same `plans[]` / `resourceId` / `locale` / `rows[]` shape as `translation_plan.json`. Each row includes exact `source`, `sourceDigest`, and `before`. The added `rollback[]` contains supported restore fields or a remove-key list. A rollback must first verify unchanged source digests and expected current translated values; an API write cannot independently reproduce a previous outdated flag.

## Preserved source ambiguities and differences

- Refund policy: the return window permits requesting a return within 30 days of delivery, while the non-returnable list says items returned after 30 days. Both statements remain distinct; no deadline interpretation was introduced.
- Refund policy versus terms: the refund policy excludes swimwear/intimates, items explicitly marked “Final Sale,” gift cards, and items returned after 30 days. The terms separately state that sale items and personalized items are final sale. These different lists are preserved rather than reconciled.
- Refund policy versus terms: return postage is the customer's responsibility except damaged/defective arrivals in the refund policy, versus an error by the store in the terms. Both original exceptions are preserved.
- The refund policy retains all original commitments: response within 1 business day, refund processing within 5–10 business days, additional bank time of 2–5 business days, reporting damaged/defective arrivals within 7 days, and inquiry after 10 business days from the confirmation email. These were not fact-checked or harmonized.
- Shipping policy processing is “within 1-3 business days,” with a possible additional 1-2 business days during the named periods. The terms say processing is “typically 1-3 business days.” The different qualifiers and the repeated processing paragraph in the shipping policy are retained.
- Shipping policy says matching outfits should “arrive as clearly and reliably as possible,” which is unusual English. Danish renders this as the delivery being as transparent and reliable as possible (“leveringen ... er så gennemskuelig og pålidelig som muligt”). This does not add a delivery guarantee.
- Privacy policy assertions about providers, data handling, retention periods, international transfers, rights and response deadlines are translated as supplied. This translation does not verify those operational claims or assess their legal validity.
- Contact hours retain the source numeric values, AM/PM notation and EST timezone. No daylight-saving conversion or local-time inference was made. The postal address, including “United States” in the contact policy, remains literal.
- “Final Sale” remains literal as an explicitly named product label in the refund policy. Company and platform names, email addresses, postal addresses, phone numbers, currencies (none present), links and HTML attributes remain unchanged.
- Original links remain exactly as supplied, including non-/da destinations. This translation does not broaden any routing claim or certify destination localization. Policy page titles outside the `body` field are not changed by this five-body plan.

## Verification run

A Python validation against `before_policies.json` passed for all five resources:

- exactly five resource IDs, one `body` row each, locale `da` only;
- exact source text, source digest, and existing before-value binding;
- exact ordered HTML tag/attribute/entity event sequences;
- exact ordered numeric token sequences, preserving every deadline, age, date number, address/phone and time value;
- exact URL/mailto sequences and counts of original company, owner, contact, address, timezone and explicit label literals;
- exact inverse restore values for two existing translations and remove-key inverses for three absent translations.

The original January 28, 2026 dates are rendered as 28. januar 2026; January 2026 is rendered as januar 2026. No effective dates changed.

Plan SHA-256 after independent-review correction: `ec5f74b73ee44b5cecc512c287bc1a92c9228276ec8f21123c56d3d9c9512209`.

Manual author review covered each source paragraph against its Danish counterpart. Independent semantic review and fresh public desktop/narrow readback remain root responsibilities before claiming the storefront is fixed.

Independent-review correction: Terms section 8 now begins “Du forpligter dig til ikke at: bruge …” to express the agreement not to perform the prohibited actions unambiguously. The remaining paragraph and all other translations are unchanged.
