Confidence: H for local checks. **FAIL/REVISE: the English-only release does not establish localized-description preservation.** Twenty-one mechanical checks pass; one newly identified release gate fails. No mutation ran according to root.

The 151-character description remains source-supported and identical across copy, plan and variables. The exact Article559471886433 `global.description_tag` create-only payload retains explicit `compareDigest:null`; source snapshots agree on absence, title, body and published state. The body SHA remains `01c2e9ab6b5c02346c0653bcc526205b5d52c856679e4f8446698999ba53522d`.

However, the fresh French MAIN head renders a French description. Root additionally reports French title/body translations without an SEO override and no existing SEO key in the English translatable resource. Those resource observations are operator-supplied, not independently inspected here. Creating a primary English description could replace localized fallback excerpts across other locales. This is a material unresolved risk, **not an observed regression**. Preserving stored article fields does not prove preservation of rendered localized metadata.

The earlier prewrite PASS/execute-next instruction is superseded before execution. **Do not release this English-only payload.** Root’s next action is a bounded locale-aware replacement plan covering exact locale/translation guards, reviewed text, partial failures and restoration of prior absence. No future multi-locale payload is approved by this review.

Existing rollback is correctly limited to deleting the newly created field, never writing the old rendered excerpt. Its non-atomic deletion still requires exact field/value/digest checks and no concurrent writer; a superseding plan must also address any added translations.

I did not author the copy, execute the mutation or inspect Shopify UI. Connector validation and existing owner authority were supplied by root; no new authority, spend or SEO lift is inferred.

Source SHA256: plan `524baa55f3a65ae7aaccff7af6528b4703a4e6bb1587bec35896e9d4bcb2fd06`; payload `5b2216673fee8d2df932ed89b884b1a6dff668409b42070a85863773b4cc0c00`; French head `148157b0e7b497650df5374307a14174bed8c2db89fce8bf780d210ddd78d9a0`. Full checks and bindings accompany this review in JSON.
