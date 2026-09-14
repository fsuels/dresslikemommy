# Passive Google sender observation — September 14, 2026

Action: `TA02-PASSIVE-SENDER-20260914-0846`.

**Result: PARTIAL measurement acceptance.** The single passive capture ran, but its request summary failed expected-collector coverage. The consent/session sequence remains unknown.

The normal background homepage returned HTTP 200 on published theme `133290917985`, US/USD/en. One instrumented reload, from 09:30:15.451 UTC with a final buffer read at 09:31:01.628 UTC, collected 508 debugger records: 253 requests, 253 responses and two canceled fetch records. There was no reported truncation. Only one source context was observed; worker/child-target coverage was not established.

**Independent-review correction:** the actual request matcher omitted the previously observed `analytics.google.com/g/collect` endpoint. Its zero matches therefore cannot establish whether retained GA4 traffic appeared in this trace. The raw ephemeral records had already been cleared and the temporary tab closed, so reprocessing is unavailable. This is an operator analysis limitation, not proof that the browser lacks network capability or that Google tracking failed. No second capture was run under the one-trace scope.

The current inline source contained `G-N4EQNK0MMB`; this proves only source presence. Neither page source nor observed console exposed `analytics_storage`, `ad_storage`, `ad_user_data` or `ad_personalization` defaults/updates. Actual sender provenance, named consent order, page_view and session freshness remain unknown. A new tab/reload is not proof of a new analytics session; no forced session was attempted.

Migration, legacy pixel disconnection and the accepted real-purchase match were preserved. No production, consent, storage, order, account, native-browser, shared-canonical, goal or schedule action occurred. The temporary tab was closed and diagnostics disabled at 09:31:34.873 UTC.

The parent should record this incomplete attempt and continue independent authorized work. Before a future permitted sender trace, qualify the full expected-collector coverage and access to the executing Google & YouTube context with named consent/event timing. This attempt does not justify a production repair, another tag or a repeat capture. No duplicate owner question was raised.

Source: [OBSERVATION.json](OBSERVATION.json). The final independent decision and source hashes are recorded separately; static review cannot add runtime visibility.
