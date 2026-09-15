The French compact-unit correction is IMPLEMENTED and locally VERIFIED. It changes one line in `normalizeGuideUnit`: the observed French `po` and `pouces` tokens normalize to `in`. The saved draft's `cm/po` headers previously failed to select the imperial part of the original measurement cell. No source measurements or values were rewritten.

Saved draft predecessor SHA256: `86c6bf6ab98ee2a61f60dd755c41a2861c3d371d040db45655de23e9ce0f46b3`.

Corrected module SHA256: `dbd748d10828f52bb24c2dfb22d019261f4abeb7f3e9f61eb86d350ee96c1bcb`.

`french-unit-normalization.diff` is the exact one-line delta. The predecessor source and its existing evidence are preserved under `round2-before-french-unit-normalization/`; original root-owned upload and browser receipts remain untouched.

The new focused case uses the actual French Mother S/Cardigan source in `../preview-before-french.json` and real module rendering/extraction functions. Imperial compact output retains the exact source strings `31,5 pouces`, `22 pouces`, and `15,7 pouces`, plus `82,7-99,2 lbs`. Returning to metric retains `80 cm`, `56 cm`, and `40 cm`. The source records remain unchanged. The case failed on the predecessor as recorded in `french-normalization-original-failure.txt`, then passed with this correction.

Checks actually run: bundled Node syntax PASS; focused regressions 26/26 PASS; unchanged independent two-case provenance oracle PASS; 14 protected functions remain byte-identical to the original candidate baseline. `VERIFICATION.json`, `PRESERVED_FUNCTIONS.json`, and `regressions-output.txt` contain the evidence. The tests model DOM and state bindings; browser acceptance is NOT RUN in this lane.

Existing separate in-memory table/compact unit controls and role-switch resets are unchanged. The fixture does not establish cross-control synchronization. The Arabic normalizer aliases and exact source values remain covered and unchanged. This lane performed no external writes and changed no production file other than the assigned module.

Root owns independent review, the exact one-module draft save/readback, and rendered French compact imperial/metric acceptance on mobile and desktop. The expected visible imperial compact values are `31,5 pouces`, `22 pouces`, and `15,7 pouces`; verify by pressing the compact control itself (`data-unit-set`), separately from the table control.
