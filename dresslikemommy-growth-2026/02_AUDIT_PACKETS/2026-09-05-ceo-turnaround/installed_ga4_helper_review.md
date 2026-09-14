# Installed GA4 helper: independent review

2026-09-06 — **PASS for the helper-bound local proposal; deployment remains gated.** I did not capture the browser source, author the correction, or perform an installed save/event send.

The captured baseline is 644 characters excluding its terminal newline; the candidate is 443. Their files contain 645/444 bytes respectively. Both match the receipt hashes and lengths. First-line outer indentation is excluded consistently.

Independent byte comparison verifies exactly one replacement inside the nonempty-string cookie branch: splitting/truncation becomes storing and returning the entire `_ga` string. The guard, cookie lookup, and stored/fresh fallback are identical. The supplied patch exactly equals the generated before/after diff. Both helper files pass bundled Node syntax checks. This proves preservation within the captured helper, not elsewhere in the installed pixel.

I independently executed the unchanged actual-helper tests using an in-memory adapter that only prefixes two spaces and appends the extraction-boundary comment. Baseline: **4 expected failures/3 passes**. Candidate: **7 passes/0 failures**. Test SHA matches the receipt. An initial summary wrapper assumed TAP output and failed on Node’s default reporter format; inspecting that output and correcting the parser required no source/test change. These synthetic cases prove intact cookie return/persistence and fallback behavior; they do not prove live cookie availability, valid production ingestion, or identity continuity. Existing truncated stored IDs persist when no cookie is readable.

The parent’s browser capture is supplied evidence, not my independent live readback. The reported viewport/Select All AX still omit full-pixel source; the inspected menu exposed Delete, with no export observed. A complete installed-pixel backup/fingerprint therefore remains unresolved. This is **not** a complete deployment packet, missing-order causal diagnosis, or live-change approval. Public 429, consent, event-send, and production-save gates remain intact.

**Next owner action:** retain the local proposal while resolving the full-pixel before-state/rollback gate through a permitted normal read path.

| Bound source | SHA-256 |
| --- | --- |
| Captured helper | `f92f5783f9b54170eab6625839ced53feab36d9e529f4dae60e24c47a50a0c69` |
| Candidate helper | `22cf87a52f227ed7c08ddf59261b2a1f611106318e06507fd6d2f1867e09d3a8` |
| Exact patch | `a48f3d4f3d72b6355ea6dfed6083c2a261939fd8b45b6ce287eee6ed6c82d3e0` |
| Test receipt | `af7033fed0ee61e8040de91513c48f8b2860aa080771d679c61130da143e72b7` |
| Unchanged test | `2236d02d6dbe09f39511fe0d9cc423c51efe3f6f1fa2f697554443c65050cbd1` |

## Follow-up — 2026-09-06, 12:26 UTC evidence

**PASS for exact owner review; not deployment approval.** The new root-supplied [binding receipt](installed_ga4_binding_readback.json) supports the previously unresolved full-editor copy path. Helper hashes independently match; the reported full-script reduction of 201 code units matches the helper delta. Single occurrence, unchanged prefix/suffix, inverse restoration, and clipboard restoration are operator-supplied evidence, internally consistent here—not an independent live read or Admin backend export.

Both whole-buffer compile attempts were blocked by `EvalError`; this neither proves a candidate defect nor supplies full-script syntax verification. Isolated helper checks remain valid.

Before any authorized Save, freshly match the approved full-before hash and retain its private buffer through exact candidate/Connected after-readback. Source drift or session reset requires a fresh normal copy; do not rebuild configuration from templates. This makes rollback concrete while the private buffer remains available. The public 429/event-validation gate and unknown purchase-gap cause remain unchanged.

| Bound receipt/source | SHA-256 |
| --- | --- |
| Binding receipt | `fd962922b8673651762f6334a8b5ddde806d814f3832965195da95ff86327afc` |
| Full before, reported | `5aa1a3e64a256511f09e1eddc2445982fa8d1872588d9a0860f571f800a726b5` |
| Full candidate, reported | `6f552b8a71090701fe93c7468012d2911bd1ad869dfb42f65b4bc27b643f484c` |
