# GA4 client-ID correction: independent review

2026-09-06 — **PASS, local candidate scope only.** No material local defect found. I did not author this correction or execute any installed-pixel change. This review used local files and bundled Node only.

**Scope verified:** The frozen template’s SHA-256 matches the prior inventory. Byte comparison against `pixels/ga4-custom-pixel.js` confirms that only `getClientId` changed. At current lines 222–232, a nonempty string from `_ga` is stored and returned intact instead of being split and truncated. The stored/fresh fallback is byte-identical, as is every byte outside that helper: consent, session creation, configuration, payloads, subscriptions, transport, and transaction handling are unchanged. The Ads template, README, runbook, and earlier implementation inventory retain their previously recorded hashes. This is scoped preservation proof, not a whole-repository audit.

**Independent execution:** Bundled Node ran `pixels/tests/ga4-client-id.test.cjs` against both versions. Baseline: four expected failures, three passing holdouts. Candidate: seven passes, zero failures. Candidate syntax passed. The test extracts the actual helper into an isolated VM; it cannot initialize a pixel or send traffic. Four synthetic cookie strings test intact return **and persistence** over an existing stored ID. The holdouts cover unavailable/empty cookies and fresh fallback generation. These are repeated examples of one identity contract, not four production incidents; fallback byte equality provides stronger preservation evidence than the generated-ID shape assertion alone.

**Meaning and limits:** Returning the complete cookie value is consistent with the parent-supplied current [Google MP reference](https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference?client_type=gtag). I did not independently fetch that reference in this local-only review. The reported installed pixel `111181921`, Disconnect button, Analytics-only requirement, and matching old parser are likewise operator-supplied observations.

Tests do not establish sandbox cookie availability, MP ingestion, equivalence to another tag’s identity, consent timing, session/Ads attribution, or causal recovery of missing purchases. The candidate accepts any nonempty string; malformed-cookie acceptance is not tested. When no cookie is available, a previously truncated stored ID remains unchanged. No refund, deduplication, transaction-token, or other inventory finding is repaired by this patch. No customer/live installation, settings change, or spend was performed or authorized by this verdict.

**Next owner action:** Bind this reviewed candidate hash to the exact installed-code comparison and any separately authorized deployment/verification packet. Keep live effectiveness UNKNOWN until an actual readback supports it.

| Source | SHA-256 |
| --- | --- |
| `purchase_capture_ga4_template_before.js` | `9dfe2f2e1cf582b43f755963921511c77cb821c1db5eefe02e7624fd7030301d` |
| `pixels/ga4-custom-pixel.js` | `51fdb8617cf9949bc02985b63435bb5e6abcb06b6eb7a19250b9d0ad14dbd80b` |
| `pixels/tests/ga4-client-id.test.cjs` | `2236d02d6dbe09f39511fe0d9cc423c51efe3f6f1fa2f697554443c65050cbd1` |
